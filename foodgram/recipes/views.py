from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, View
)

from .forms import RecipeForm
from .models import Recipe, Tag, Chef


class AuthorshipRequired(UserPassesTestMixin):
    permission_denied_message = ('Вы должны быть автором рецепта, чтобы '
                                 'иметь возможность редактировать или '
                                 'удалить его')

    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user


class RecipeIndex(ListView):
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

    def mark_favorite(self, queryset):
        if not self.request.user.is_authenticated:
            return

        favorites = self.request.user.favorite_recipes.values_list(
            'id', flat=True
        )
        favorites_set = set(favorites)
        for recipe in queryset:
            recipe.is_favorite = recipe.id in favorites_set

    def mark_added_to_cart(self, queryset):
        if self.request.user.is_authenticated:
            purchases = self.request.user.purchases.values_list(
                'id', flat=True
            )
        else:
            purchases = self.request.session.get('purchases', [])

        purchases_set = set(purchases)
        for recipe in queryset:
            recipe.is_recipe_in_cart = recipe.id in purchases_set


class AllRecipesView(RecipeIndex):
    def get_queryset(self):
        checked_tags = [tag for tag in self.tags if tag.checked]

        recipes = Recipe.objects.select_related('author')
        recipes_filtered_by_tags = recipes.filter(
            tags__in=checked_tags).distinct()

        self.mark_favorite(recipes_filtered_by_tags)
        self.mark_added_to_cart(recipes_filtered_by_tags)
        return recipes_filtered_by_tags


class ChefRecipesView(RecipeIndex):
    template_name = 'recipes/chef_recipes.html'

    @cached_property
    def chef(self):
        chef_id = self.kwargs.get('id')
        chef = get_object_or_404(Chef, id=chef_id)
        return chef

    def get_queryset(self):
        checked_tags = [tag for tag in self.tags if tag.checked]

        chef_recipes = self.chef.recipes.all()
        chef_recipes_filtered_by_tags = chef_recipes.filter(
            tags__in=checked_tags).distinct()

        self.mark_favorite(chef_recipes_filtered_by_tags)
        self.mark_added_to_cart(chef_recipes_filtered_by_tags)
        return chef_recipes_filtered_by_tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            is_user_subscribed = self.request.user.subscriptions.filter(
                id=self.chef.id
            ).exists()
            context['is_user_subscribed'] = is_user_subscribed
        context['chef'] = self.chef
        return context


class FavoriteRecipesView(LoginRequiredMixin, RecipeIndex):
    template_name = 'recipes/favorite_recipes.html'

    def get_queryset(self):
        checked_tags = [tag for tag in self.tags if tag.checked]
        user = self.request.user
        favorite_recipes = user.favorite_recipes.select_related('author')
        favorite_recipes_filtered_by_tags = favorite_recipes.filter(
            tags__in=checked_tags
        ).distinct()

        for recipe in favorite_recipes_filtered_by_tags:
            recipe.is_favorite = True
        self.mark_added_to_cart(favorite_recipes_filtered_by_tags)
        return favorite_recipes_filtered_by_tags


class SubscriptionsView(LoginRequiredMixin, RecipeIndex):
    template_name = 'recipes/subscriptions.html'

    def get_queryset(self):
        return self.request.user.subscriptions.all()


class GetPurchasesMixin:
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.purchases.all()
        else:
            purchases = self.request.session.get('purchases', [])
            return Recipe.objects.filter(id__in=purchases).all()    


class PurchasesView(GetPurchasesMixin, ListView):
    template_name = 'recipes/purchases.html'
    context_object_name = 'purchases'


class DownloadPurchasesList(GetPurchasesMixin, View):
    def get_file_content(self, recipes):
        to_buy = {}
        max_length = 0
        for recipe in recipes:
            for ingredient in recipe.ingredient_set.all():
                product = ingredient.food_product
                key = f'{product.name}, {product.unit}'
                to_buy.setdefault(key, 0)
                to_buy[key] += ingredient.quantity
                if len(key) > max_length:
                    max_length = len(key)

        first_column_width = max_length + 15
        rows = []
        for product_with_unit, quantity in to_buy.items():
            rows.append(
                '{:<{width}}|{:>15}\n'.format(
                    product_with_unit,
                    quantity,
                    width=first_column_width
                )
            )

        sep = '-' * (first_column_width + 16) + '\n'
        return sep.join(rows)


    def get(self, request, *args, **kwargs):
        recipes = self.get_queryset()
        file_content = self.get_file_content(recipes)

        response = HttpResponse(
            file_content,
            content_type='text/plain'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="purchases_list.txt"'
        )

        return response


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_new.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form.instance.author = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UpdateRecipeView(LoginRequiredMixin, AuthorshipRequired, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_edit.html'


class RecipeView(DetailView):
    model = Recipe
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        recipe = context['recipe']
        if user.is_authenticated:
            is_favorite_recipe = user.favorite_recipes.filter(
                id=recipe.id
            ).exists()
            context['is_favorite_recipe'] = is_favorite_recipe

            is_user_subscribed = user.subscriptions.filter(
                id=recipe.author.id
            ).exists()
            context['is_user_subscribed'] = is_user_subscribed

            is_recipe_in_cart = user.purchases.filter(
                id=recipe.id
            ).exists()
        else:
            purchases = self.request.session.get('purchases', [])
            is_recipe_in_cart = recipe.id in purchases

        context['is_recipe_in_cart'] = is_recipe_in_cart

        return context


class DeleteRecipeView(LoginRequiredMixin, AuthorshipRequired, DeleteView):
    model = Recipe
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('index')
