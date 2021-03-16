from django.contrib import admin

from .models import Ingredient, FoodProduct, Recipe, Unit

admin.site.register(Ingredient)
admin.site.register(FoodProduct)
admin.site.register(Recipe)
admin.site.register(Unit)
