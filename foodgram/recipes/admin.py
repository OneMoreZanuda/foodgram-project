from django.contrib import admin

from .models import Chef, Ingredient, FoodProduct, Recipe, Tag

admin.site.register(Chef)
admin.site.register(Ingredient)
admin.site.register(FoodProduct)
admin.site.register(Recipe)
admin.site.register(Tag)
