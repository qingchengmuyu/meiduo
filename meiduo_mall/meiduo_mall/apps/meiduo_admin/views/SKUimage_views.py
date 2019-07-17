from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU
from meiduo_admin.pages import Page
from meiduo_admin.serializers.SKUimage_serializer import SKUImageSerializer, SKUSimpleSerializer


class SKUImageViews(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer
    pagination_class = Page


class SKUSimpleViews(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer
