from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from goods.models import SKU
from meiduo_admin.serializers.sku_serializer import *
from meiduo_admin.pages import Page
from goods.models import GoodsCategory, SPU, SPUSpecification


class SKUViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    pagination_class = Page

    def get_queryset(self):
        if self.action == 'categories':
            return GoodsCategory.objects.filter(parent_id__gt=37)
        if self.action == 'simple':
            return SPU.objects.all()
        if self.action == 'specs':
            return SPUSpecification.objects.filter(spu_id=self.kwargs['pk'])

        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.filter(name__contains=keyword)
        return self.queryset.all()

    def get_serializer_class(self):
        if self.action == 'categories':
            return GoodsCategorySimpleSerializer
        if self.action == 'simple':
            return SPUSimpleSerializer
        if self.action == 'specs':
            return SPUSpecSerializer

        return self.serializer_class

    @action(methods=['get'], detail=False)
    def categories(self, request):
        cates = self.get_queryset()
        cates_serializer = self.get_serializer(cates, many=True)
        return Response(cates_serializer.data)

    @action(methods=['get'], detail=False)
    def simple(self, request):
        spu_query = self.get_queryset()
        spu_serializer = self.get_serializer(spu_query, many=True)
        return Response(spu_serializer.data)

    @action(methods=['get'], detail=True)
    def specs(self, request, pk):
        specs_queryset = self.get_queryset()
        specs_serializer = self.get_serializer(specs_queryset, many=True)
        return Response(specs_serializer.data)
