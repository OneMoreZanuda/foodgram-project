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
        'new/',
        views.CreateRecipeView.as_view(),
        name='recipe_new'
    ),
    path(
        '<int:pk>/edit/',
        views.UpdateRecipeView.as_view(),
        name='recipe_edit'
    ),
    path(
        '<int:pk>',
        views.RecipeView.as_view(),
        name='recipe'
    ),
]
