from django.http import Http404, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView
)


from .forms import RecipeForm
from .models import Recipe, Tag, User
from .utils import CachedPaginator


class Index(ListView):
    queryset = Recipe.objects.select_related('author')
    # paginator_class = CachedPaginator
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        tags = self.get_tags()
        checked_tags = [tag for tag in tags if tag.checked]
        self.object_list = self.get_queryset().filter(tags__in=checked_tags) # DISTINCT?

        context = self.get_context_data()
        context['tags'] = tags
        return self.render_to_response(context)

    def get_tags(self):
        tags = []
        query_params = self.request.GET
        for tag in Tag.objects.all():
            if tag.name not in query_params:
                tag.checked = True
            elif query_params[tag.name] == 'no':
                tag.checked = False
            else:
                raise Http404(f'Invalid value of the parameter "{tag.name}"')
            tags.append(tag)
        return tags


class CreateRecipeView(CreateView):
    model = Recipe
    form_class = RecipeForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form.instance.author = User.objects.get_or_create(username='deleted')[0]
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UpdateRecipeView(UpdateView):
    model = Recipe
    form_class = RecipeForm


class RecipeView(DetailView):
    queryset = Recipe.objects.all()


from django.http import JsonResponse

from .models import FoodProduct


def get_food_products(request):
    data = []
    template = request.GET.get('query')
    if template:
        qs = FoodProduct.objects.filter(name__istartswith=template)
        for product in qs:
            data.append(
                {
                    'title': product.name,
                    'dimension': product.unit
                }
            )
    return JsonResponse(data, safe=False)