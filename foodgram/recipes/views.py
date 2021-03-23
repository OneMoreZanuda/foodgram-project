from django.http import Http404, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView


from .forms import RecipeForm, IngredientForm
from .models import Recipe, User
from .utils import CachedPaginator


class Index(ListView):
    queryset = Recipe.objects.select_related('author')
    context_object_name = 'recipes'
    template_name = 'recipes/indexNotAuth.html'
    # paginator_class = CachedPaginator
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        tags = self.get_tags()

        query_q = Q()
        for tag, checked in tags.items():
            if checked:
                query_q |= Q(**{"tags__contains": tag})
        if query_q:
            self.object_list = self.get_queryset().filter(query_q)
        else:
            self.object_list = Recipe.objects.none()

        context = self.get_context_data()
        context.update(tags)
        return self.render_to_response(context)

    def get_tags(self):
        tags = {}
        query_params = self.request.GET
        for tag_name, _ in Recipe.tags.field.choices:
            if tag_name not in query_params:
                tags[tag_name] = True
            elif query_params[tag_name] == 'no':
                tags[tag_name] = False
            else:
                raise Http404(f'Invalid value of the parameter "{tag_name}"')
        return tags


class CreateRecipeView(CreateView):
    model = Recipe
    fields = ('title', 'tags', 'time_for_preparing', 'description')
    template_name = 'recipes/formRecipe.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'ingredient_forms' not in kwargs:
            data['ingredient_forms'] = self.get_ingredient_forms()

        ingredients_error = ''
        for ing_form in data['ingredient_forms']:
            if ing_form.errors:
                ingredients_error = list(ing_form.errors.values())[0]
                break

        data['ingredients_error'] = ingredients_error

        return data
# """
# Сделать так, чтобы при создании рецепта с тем же именем тем же автором не валилось все с ошибкой
# Проверять, что не добавлены одинаковые ингредиенты
# Убирать ошибку неправильных ингредиентов, после того, как пользователь поправил (удалил например неправильный ингредиент)
# показывать ошибку, если ни один ингредиент не был добавлен
# """
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        ingredient_forms = self.get_ingredient_forms()
        if form.is_valid() and all(f.is_valid() for f in ingredient_forms):
            return self.forms_valid(form, ingredient_forms)
        else:
            return self.forms_invalid(form, ingredient_forms)

    def get_ingredient_forms(self):
        ingredient_forms = []
        if self.request.method in ('POST', 'PUT'):
            return ingredient_forms

        request_data = self.request.POST
        ingredients_data = filter(
            lambda item: item[0].startswith('nameIngredient_'),
            request_data.items()
        )

        for key, value in ingredients_data:
            try:
                index = key.split('_')[1]
            except IndexError:
                raise ValueError(
                    'Некорректное имя HTML-элемента, '
                    f'содержащего имя продукта {value}'
                )

            quantity = request_data.get(f'valueIngredient_{index}', '')
            data = {
                'food_product': value,
                'quantity': quantity
            }
            ingredient_forms.append(IngredientForm(data))
        return ingredient_forms

    def forms_valid(self, form, ingredient_forms):
        # form.instance.author = self.request.user
        form.instance.author = User.objects.get_or_create(username='deleted')[0]
        self.object = form.save()
        self.object.ingredients.clear()
        for form in ingredient_forms:
            form.instance.recipe = self.object
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, ingredient_forms):
        data = self.get_context_data(
            form=form, ingredient_forms=ingredient_forms
        )
        return self.render_to_response(data)
