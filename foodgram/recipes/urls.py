from django.urls import path

from . import views

urlpatterns = [
    path('', views.AllRecipesView.as_view(), name='index'),
    path(
        'favorites/',
        views.FavoriteRecipesView.as_view(),
        name='favorites'
    ),
    path(
        'subscriptions/',
        views.SubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path(
        'chefs/<int:pk>',
        views.ChefRecipesView.as_view(),
        name='chef'
    ),
    path(
        'recipes/new/',
        views.CreateRecipeView.as_view(),
        name='recipe_new'
    ),
    path(
        'recipes/<int:pk>/edit/',
        views.UpdateRecipeView.as_view(),
        name='recipe_edit'
    ),
    path(
        'recipes/<int:pk>',
        views.RecipeView.as_view(),
        name='recipe'
    ),
]
