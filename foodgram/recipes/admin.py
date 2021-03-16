from django.contrib import admin

from .models import Ingredient, FoodProduct, Recipe, Tag, Unit

admin.site.register(Ingredient)
admin.site.register(FoodProduct)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Unit)
