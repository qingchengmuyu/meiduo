from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serializers.option_serializer import OptionSerializer
from meiduo_admin.pages import Page
from meiduo_admin.serializers.specs_serializer import SpecSerializer


class OptionViews(ModelViewSet):
    queryset = SpecificationOption.objects.all()
    serializer_class = OptionSerializer
    pagination_class = Page


class SimpleViews(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSerializer
