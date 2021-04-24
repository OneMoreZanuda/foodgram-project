from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from recipes.models import Chef, FoodProduct, Recipe

from .serializers import FoodProductSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
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
    recipe = get_object_or_404(Recipe, id=recipe_id)
    request.user.favorite_recipes.add(recipe)

    return Response({'success': True})


@api_view(['DELETE'])
def remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
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


@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_purchases(request):
    recipe_id = request.data.get('recipe')
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_authenticated:
        request.user.purchases.add(recipe)
    elif request.user:
        purchases = request.session.setdefault('purchases', [])
        if recipe_id not in purchases:
            purchases.append(int(recipe_id))
            request.session.modified = True

    return Response({'success': True})


@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_from_purchases(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_authenticated:
        request.user.purchases.remove(recipe)
    elif request.user:
        purchases = request.session.setdefault('purchases', [])
        try:
            purchases.remove(recipe.id)
        except ValueError:
            return Response({'success': False})
        else:
            request.session.modified = True

    return Response({'success': True})
