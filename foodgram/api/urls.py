from django.urls import path

# from rest_framework.routers import DefaultRouter

from . import views

# router = DefaultRouter()
# router.register('favorites', views.FavoritesViewSet, basename='favorites')


urlpatterns = [
    path('products/', views.get_products, name='get_products'),
    path('favorites/', views.add_to_favorites, name='add_to_favorites'),
    path(
        'favorites/<int:recipe_id>',
        views.remove_from_favorites,
        name='remove_from_favorites'
     )
]
