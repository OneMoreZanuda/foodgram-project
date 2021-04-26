from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('products/', views.get_products, name='get_products'),
    path(
        'favorites/',
        views.add_to_favorites,
        name='add_to_favorites',
    ),
    path(
        'favorites/<int:recipe_id>/',
        views.remove_from_favorites,
        name='remove_from_favorites',
    ),
    path(
        'subscriptions/',
        views.add_to_subscriptions,
        name='add_to_subscriptions',
    ),
    path(
        'subscriptions/<int:author_id>/',
        views.remove_from_subscriptions,
        name='remove_from_subscriptions',
    ),
    path(
        'purchases/',
        views.add_to_purchases,
        name='add_to_purchases',
    ),
    path(
        'purchases/<int:recipe_id>/',
        views.remove_from_purchases,
        name='remove_from_purchases',
    ),
]
