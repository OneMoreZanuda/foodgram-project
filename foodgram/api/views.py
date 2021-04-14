from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from recipes.models import Chef, FoodProduct, Recipe

from .serializers import FoodProductSerializer


@api_view(['GET'])
def get_products(request):
    template = request.GET.get('query')
    if template is None:
        raise NotFound(detail="Не передан параметр 'query'", code=404)

    queryset = FoodProduct.objects.filter(name__istartswith=template)
    serializer = FoodProductSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def add_to_favorites(request):
    recipe_id = request.data.get('recipe')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    request.user.favorite_recipes.add(recipe)

    return Response({'success': True})


@api_view(['DELETE'])
def remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    request.user.favorite_recipes.remove(recipe)

    return Response({'success': True})


@api_view(['POST'])
def add_to_subscriptions(request):
    author_id = request.data.get('author')
    if author_id == request.user.id:
        return Response({'success': False})
    author = get_object_or_404(Chef, id=author_id)
    request.user.subscriptions.add(author)

    return Response({'success': True})


@api_view(['DELETE'])
def remove_from_subscriptions(request, author_id):
    author = get_object_or_404(Chef, id=author_id)
    request.user.subscriptions.remove(author)

    return Response({'success': True})
