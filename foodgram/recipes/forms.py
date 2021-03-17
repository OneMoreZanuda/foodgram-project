from django import forms

from .models import Ingredient, Recipe


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input'}),
        }
        labels = {
            'title': 'Название рецепта',
            'tags': 'Теги',
            'ingredients': 'Ингредиенты',
            'time_for_preparing': 'Время приготовления',
            'text': 'Описание'
        }
