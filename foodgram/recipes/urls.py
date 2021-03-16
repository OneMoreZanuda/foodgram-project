from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('recipes/new/', views.CreateRecipeView.as_view(), name='new_recipe'),
]