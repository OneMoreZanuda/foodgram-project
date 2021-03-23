from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, FoodProduct, Recipe


class IngredientForm(forms.ModelForm):
    food_product_name = forms.CharField(max_length=200)

    class Meta:
        model = Ingredient
        exclude = ('recipe', 'food_product')

    def clean_food_product_name(self):
        name = self.cleaned_data['food_product_name']

        try:
            FoodProduct.objects.get(name=name)
        except FoodProduct.DoesNotExist:
            mes = (f'Продукт "{name}" не найден в перечне доступных'
                   ' для выбора продуктов')
            raise ValidationError(mes)

        return name

    def save(self, commit=True):
        name = self.cleaned_data['food_product_name']
        self.instance.food_product = FoodProduct.objects.get(name=name)
        return super().save(commit)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author', 'ingredients')
        labels = {
            'title': 'Название рецепта',
            'tags': 'Теги',
            'time_for_preparing': 'Время приготовления',
            'text': 'Описание'
        }


IngredientsFormSet = forms.inlineformset_factory(
    Recipe, Ingredient,
    exclude=('recipe',), fk_name='recipe', extra=1, can_delete=False
)
