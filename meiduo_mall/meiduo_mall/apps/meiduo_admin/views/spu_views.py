from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from goods.models import SPU, Brand, GoodsCategory
from meiduo_admin.serializers.spu_serializer import SPUSerializer, BrandSerializer, GoodCatSerializer
from meiduo_admin.pages import Page


class SPUViews(ModelViewSet):
    queryset = SPU.objects.all()
    serializer_class = SPUSerializer
    pagination_class = Page

    def get_queryset(self):
        if self.action == 'brands':
            return Brand.objects.all()
        if self.action == 'categories':
            return GoodsCategory.objects.filter(parent=None)
        if self.action == 'categoriess':
            return GoodsCategory.objects.filter(parent=self.kwargs['pk'])
        return self.queryset.all()

    def get_serializer_class(self):
        if self.action == 'brands':
            return BrandSerializer
        if self.action == 'categories':
            return GoodCatSerializer
        if self.action == 'categoriess':
            return GoodCatSerializer
        return self.serializer_class

    @action(methods=['get'], detail=False)
    def brands(self, request):
        brands_queryset = self.get_queryset()
        brands_serializer = self.get_serializer(brands_queryset, many=True)
        return Response(brands_serializer.data)

    @action(methods=['get'], detail=False)
    def categories(self, request):
        categories_queryset = self.get_queryset()
        categories_serializer = self.get_serializer(categories_queryset, many=True)
        return Response(categories_serializer.data)

    @action(methods=['get'], detail=True)
    def categoriess(self, request, pk):
        categoriess_queryset = self.get_queryset()
        categoriess_serializer = self.get_serializer(categoriess_queryset, many=True)
        return Response(categoriess_serializer.data)


