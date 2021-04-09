from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import RecipeForm
from .models import Preference, Recipe, Tag, User
from .utils import CachedPaginator


class RecipeIndex(ListView):
    paginator_class = CachedPaginator
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.tags
        return context

    @cached_property
    def tags(self):
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


class AllRecipesView(RecipeIndex):
    def get_queryset(self):
        checked_tags = [tag for tag in self.tags if tag.checked]

        recipes = Recipe.objects.select_related('author')
        recipes_filtered_by_tags = recipes.filter(
            tags__in=checked_tags).distinct()

        favorites = self.request.user.preferences.values_list(
            'recipe', flat=True
        )
        for recipe in recipes_filtered_by_tags:
            recipe.is_favorite = recipe.id in favorites
        return recipes_filtered_by_tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Рецепты'
        return context


class FavoriteRecipesView(RecipeIndex):
    def get_queryset(self):
        checked_tags = [tag for tag in self.tags if tag.checked]
        user = self.request.user
        favorite_recipe_ids = user.preferences.values_list('recipe', flat=True)
        favorite_recipes = Recipe.objects.filter(id__in=favorite_recipe_ids)
        favorite_recipes_filtered_by_tags = favorite_recipes.filter(
            tags__in=checked_tags
        ).distinct()

        for recipe in favorite_recipes_filtered_by_tags:
            recipe.is_favorite = True
        return favorite_recipes_filtered_by_tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Избранное'
        return context


class CreateRecipeView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_new.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form.instance.author = User.objects.get_or_create(username='deleted')[0]
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


class UpdateRecipeView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_edit.html'

    # def dispatch(self, request, *args, **kwargs):
    #     recipe = self.get_object()
    #     if self.recipe.author != request.user:
    #         raise Forbidden

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


class RecipeView(DetailView):
    queryset = Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_favorite_recipe = Preference.objects.filter(
            user=self.request.user, recipe=self.get_object()
        ).exists()
        context['is_favorite_recipe'] = is_favorite_recipe
        return context


class DeleteRecipeView(DeleteView):
    queryset = Recipe.objects.all()
