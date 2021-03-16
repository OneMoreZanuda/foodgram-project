from django.shortcuts import render
from django.views.generic import CreateView, ListView

from .models import Recipe
from .utils import CachedPaginator

# def index(request):
#     return render(request, 'recipes/indexNotAuth.html', context={})


class Index(ListView):
    queryset = Recipe.objects.select_related('author')
    context_object_name = 'recipes'
    template_name = 'recipes/indexNotAuth.html'
    paginator_class = CachedPaginator
    paginate_by = 6


class CreateRecipeView(CreateView):
    model = Recipe
    fields = ('title', 'text', 'ingredients', 'tags', 'time_for_preparing')
    template_name = 'recipes/formRecipe.html'
