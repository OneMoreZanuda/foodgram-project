from django.contrib import admin

from .models import Chef, FoodProduct, Ingredient, Recipe, Tag


class ChefAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')
    list_filter = ('email',)
    search_fields = ['last_name', 'first_name', 'email']


class IngredientInline(admin.StackedInline):
    model = Ingredient
    autocomplete_fields = ['food_product']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInline,
    ]
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tags')
    search_fields = [
        'title', 'author__last_name', 'author__first_name',
    ]
    readonly_fields = ('number_of_added_to_favorites',)

    @admin.display(description='Количество пользователей, '
                               'добавивших в "Избранное"')
    def number_of_added_to_favorites(self, recipe):
        return recipe.chef_set.count()


class FoodProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name',)
    search_fields = ['name']


admin.site.register(Chef, ChefAdmin)
admin.site.register(FoodProduct, FoodProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
