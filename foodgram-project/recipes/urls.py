from django.urls import path

from . import views

urlpatterns = [
    path('', views.AllRecipesView.as_view(), name='index'),
    path(
        'favorites/',
        views.FavoriteRecipesView.as_view(),
        name='favorites',
    ),
    path(
        'subscriptions/',
        views.SubscriptionsView.as_view(),
        name='subscriptions',
    ),
    path(
        'purchases/',
        views.PurchasesView.as_view(),
        name='purchases',
    ),
    path(
        'purchases/download',
        views.DownloadPurchasesList.as_view(),
        name='download_purchases',
    ),
    path(
        'chefs/<int:id>',
        views.ChefRecipesView.as_view(),
        name='chef',
    ),
    path(
        'recipes/new/',
        views.CreateRecipeView.as_view(),
        name='recipe_new',
    ),
    path(
        'recipes/<int:id>/edit/',
        views.UpdateRecipeView.as_view(),
        name='recipe_edit',
    ),
    path(
        'recipes/<int:id>/delete/',
        views.DeleteRecipeView.as_view(),
        name='recipe_delete',
    ),
    path(
        'recipes/<int:id>',
        views.RecipeView.as_view(),
        name='recipe',
    ),
]
