from django.urls import path

# from rest_framework.routers import DefaultRouter

from . import views

# router = DefaultRouter()
# router.register('favorites', views.FavoritesViewSet, basename='favorites')


urlpatterns = [
    path('products/', views.FoodProductListView.as_view()),
    path('favorites/', views.CreatePreferenceView.as_view()),
    path('favorites/<int:recipe>', views.DestroyPreferenceView.as_view())
]
