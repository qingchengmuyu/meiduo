from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import Group, Permission

from meiduo_admin.serializers.group_serializer import GroupSerializer, GroupSimperSerializer
from meiduo_admin.pages import Page


class GroupViews(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = Page


class GroupSimpleViews(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = GroupSimperSerializer
