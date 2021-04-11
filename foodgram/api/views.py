from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from recipes.models import FoodProduct

from .serializers import FoodProductSerializer

@api_view(['GET'])
def get_products(request):
    template = self.request.GET.get('query')
    if template is None:
        raise NotFound(detail="Не передан параметр 'query'", code=404)

    queryset = FoodProduct.objects.filter(name__istartswith=template)

    serializer = FoodProductSerializer(queryset, many=True)
    return Response(serializer.data)


# class CreatePreferenceView(generics.CreateAPIView):
#     # permission_classes = []

#     def create(self, request, *args, **kwargs):
#         serializer = PreferenceSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)

#         return Response({'success': True})


# class DestroyPreferenceView(generics.DestroyAPIView):
#     lookup_field = 'recipe'
#     queryset = Preference.objects.all()
#     # permission_classes = [Preference]

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response({'success': True})
