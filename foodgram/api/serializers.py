from recipes.models import FoodProduct
from rest_framework import serializers


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ('name', 'unit')
