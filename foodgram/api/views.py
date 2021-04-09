from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from recipes.models import FoodProduct, Preference

from .serializers import FoodProductSerializer, PreferenceSerializer


class FoodProductListView(generics.ListAPIView):
    serializer_class = FoodProductSerializer

    def get_queryset(self):
        template = self.request.GET.get('query')
        if template is not None:
            return FoodProduct.objects.filter(name__istartswith=template)
        raise NotFound(detail="Не передан параметр 'query'", code=404)


class CreatePreferenceView(generics.CreateAPIView):
    # permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

        return Response({'success': True})


class DestroyPreferenceView(generics.DestroyAPIView):
    lookup_field = 'recipe'
    queryset = Preference.objects.all()
    # permission_classes = [Preference]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'success': True})
