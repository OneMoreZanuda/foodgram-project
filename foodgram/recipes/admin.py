from django.contrib import admin

from .models import Cook, Ingredient, FoodProduct, Recipe, Tag

admin.site.register(Cook)
admin.site.register(Ingredient)
admin.site.register(FoodProduct)
admin.site.register(Recipe)
admin.site.register(Tag)
