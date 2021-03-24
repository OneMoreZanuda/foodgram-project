from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, FoodProduct, Recipe


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        exclude = ('recipe',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author', 'ingredients')
        labels = {
            'title': 'Название рецепта'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tags = self.fields['tags']
        tags.error_messages['required'] = ('Необходимо выбрать минимум '
                                           '{tags.min_choices} тег/тегов')


IngredientsFormSet = forms.inlineformset_factory(
    Recipe, Ingredient,
    exclude=('recipe',), fk_name='recipe', extra=1, can_delete=False
)
