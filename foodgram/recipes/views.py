from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from .models import Recipe
from .utils import CachedPaginator


class Index(ListView):
    queryset = Recipe.objects.select_related('author')
    context_object_name = 'recipes'
    template_name = 'recipes/indexNotAuth.html'
    paginator_class = CachedPaginator
    paginate_by = 6

    def get_context_data(self, **kwargs):
        data = super(Index, self).get_context_data(**kwargs)
        query_params = self.request.GET
        for tag_name, _ in Recipe.tags.field.choices:
            if tag_name not query_params:
                tag_checked = True
            elif query_params[tag_name] == 'no':
                tag_checked = False
            else:
                raise Http404(f'Invalid value of the parameter "{tag_name}"')
            data[tag_name] = tag_checked
        return data


class CreateRecipeView(CreateView):
    model = Recipe
    fields = ('title', 'text', 'ingredients', 'tags', 'time_for_preparing')
    template_name = 'recipes/formRecipe.html'
