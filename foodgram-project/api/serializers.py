from rest_framework import serializers

from recipes.models import FoodProduct


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ('name', 'unit')
