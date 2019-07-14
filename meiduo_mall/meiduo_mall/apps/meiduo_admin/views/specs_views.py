from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from goods.models import SPUSpecification
from meiduo_admin.serializers.specs_serializer import SpecSerializer
from meiduo_admin.pages import Page


class SpecsViews(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSerializer
    pagination_class = Page

    def get_queryset(self):
        if self.action == 'specs':
            return SPUSpecification.objects.filter(id=self.kwargs['pk'])
        return self.queryset.all()

    def get_serializer_class(self):
        return self.serializer_class

    @action(methods=['get'], detail=True)
    def specs(self, request, pk):
        specs_queryset = self.get_queryset()
        specs_serializer = self.serializer_class(specs_queryset)
        return Response(specs_serializer.data)
