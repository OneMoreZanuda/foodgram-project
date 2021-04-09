from recipes.models import FoodProduct, Preference
from rest_framework import serializers


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ('name', 'unit')


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ('recipe',)
