from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from meiduo_admin.serializers.perms_serializer import PermSerializer, ContentSerializer
from meiduo_admin.pages import Page
from django.contrib.auth.models import Permission, ContentType


class PermViews(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermSerializer
    pagination_class = Page


class ContentViews(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentSerializer
