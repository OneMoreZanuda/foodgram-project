from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
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
    path('products/', views.get_food_products, name='products')
]
