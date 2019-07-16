from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializers.brand_serializer import BrandSerializer
from meiduo_admin.pages import Page


class BrandViews(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = Page
