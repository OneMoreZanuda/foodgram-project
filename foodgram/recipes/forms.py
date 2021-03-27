from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, Recipe


FOOD_PRODUCT_WIDGET_NAME = 'nameIngredient'
QUANTITY_WIDGET_NAME = 'valueIngredient'


class CustomModelChoiceField(forms.ModelChoiceField):
    default_error_messages = {
        'invalid_choice': ('К сожалению, продукта "%(value)s" больше нет'
                           ' в перечне доступных продуктов. Соответсвующий'
                           ' ингредиент убран из списка.'),
    }

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            if isinstance(value, self.queryset.model):
                value = getattr(value, key)
            value = self.queryset.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value}
            )
        return value


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe',)
        field_classes = {
            'food_product': CustomModelChoiceField,
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'time_for_preparing', 'description')
        labels = {
            'title': 'Название рецепта',
            'tags': 'Теги',
            'time_for_preparing': 'Время приготовления',
            'description': 'Описание'
        }
        error_messages = {
            'tags': {'required': 'Необходимо выбрать минимум 1 тег'}
        }
        widgets = {
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredients = []

    def clean_title(self):
        title = self.cleaned_data['title']
        author = self.instance.author
        if author.recipes.filter(title=title).exists():
            raise ValidationError(
                'Вы уже создавали рецепт с таким названием',
                code='invalid'
            )
        return title

    def clean(self):
        super().clean()
        food_products = filter(
            lambda item: item[0].startswith(FOOD_PRODUCT_WIDGET_NAME),
            self.data.items()
        )

        for key, food_product_name in food_products:
            try:
                index = key.split('_')[1]
            except IndexError:
                raise ValueError(
                    'Некорректное имя HTML-элемента, '
                    f'содержащего имя продукта {food_product_name}'
                )

            quantity = self.data.get(f'{QUANTITY_WIDGET_NAME}_{index}', '')
            data = {
                'food_product': food_product_name,
                'quantity': quantity
            }
            ingredient_form = IngredientForm(data)
            if ingredient_form.is_valid():
                self.ingredients.append(ingredient_form.instance)
            else:
                ingredient_errors = sum(ingredient_form.errors.values(), [])
                self.add_error(None, ingredient_errors)

        if not self.ingredients:
            self.add_error(None, 'Необходимо добавить хотя бы один ингредиент')

    def _save_ingredients(self):
        self.instance.ingredients.clear()
        for ingredient in self.ingredients:
            ingredient.recipe = self.instance
            ingredient.save()

    _save_m2m = _save_ingredients
