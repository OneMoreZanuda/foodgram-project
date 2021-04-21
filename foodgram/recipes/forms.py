from collections import Counter
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
        fields = ('food_product', 'quantity')
        field_classes = {
            'food_product': CustomModelChoiceField,
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'time_for_preparing', 'description', 'image')
        error_messages = {
            'tags': {'required': 'Необходимо выбрать минимум 1 тег'}
        }
        widgets = {
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].to_field_name = 'name'
        self.ingredients = self.instance.ingredient_set.all()

    def clean_title(self):
        title = self.cleaned_data['title']
        author_recipes = self.instance.author.recipes.filter(title=title)

        if author_recipes.exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                'У вас уже есть рецепт с таким названием',
                code='invalid'
            )
        return title

    def clean(self):
        super().clean()
        self.collect_ingredients()

        self.check_uniqueness_of_ingredients()
        self.check_availability_of_ingredients()

    def collect_ingredients(self):
        self.ingredients = []
        food_products = filter(
            lambda item: item[0].startswith(FOOD_PRODUCT_WIDGET_NAME),
            self.data.items()
        )

        for key, food_product_name in food_products:
            index = key.split('_')[1]

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

    def check_uniqueness_of_ingredients(self):
        products = [ing.food_product.name for ing in self.ingredients]
        for product, count in Counter(products).most_common():
            if count > 1:
                mes = (f'Продукт {product} встречается в списке '
                       'несколько раз. Пожалуйста, исправьте список так, '
                       'чтобы каждый продукт был указан только один раз')
                self.add_error(None, mes)

    def check_availability_of_ingredients(self):
        if not self.ingredients:
            self.add_error(None, 'Необходимо добавить хотя бы один ингредиент')

    def _save_m2m(self):
        super()._save_m2m()
        self.instance.ingredients.clear()
        self.instance.ingredient_set.set(self.ingredients, bulk=False)
