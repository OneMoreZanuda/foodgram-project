from django.contrib import admin

from .models import Cook, Ingredient, FoodProduct, Recipe

admin.site.register(Cook)
admin.site.register(Ingredient)
admin.site.register(FoodProduct)
admin.site.register(Recipe)
