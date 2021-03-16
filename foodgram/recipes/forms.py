from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author',)
        labels = {'title': 'Название рецепта',
                  'tags': 'Теги',
                  'ingredients': 'Ингредиенты',
                  'time_for_preparing': 'Время приготовления',
                  'text': 'Описание'}
