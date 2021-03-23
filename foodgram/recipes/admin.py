from django.contrib import admin

from .models import Ingredient, FoodProduct, Recipe

admin.site.register(Ingredient)
admin.site.register(FoodProduct)
admin.site.register(Recipe)
