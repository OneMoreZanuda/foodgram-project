from django.http import Http404, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView


from .forms import RecipeForm
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
    template_name = 'recipes/formRecipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form.instance.author = User.objects.get_or_create(username='deleted')[0]
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
