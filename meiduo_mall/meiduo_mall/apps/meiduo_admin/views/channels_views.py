from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from meiduo_admin.pages import Page
from goods.models import GoodsChannel, GoodsChannelGroup
from meiduo_admin.serializers.channels_serializer import ChannelSerializer, ChannelGroupSerializer


class ChannelViews(ModelViewSet):
    queryset = GoodsChannel.objects.all()
    serializer_class = ChannelSerializer
    pagination_class = Page


class ChannelGroupViews(ListAPIView):
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = ChannelGroupSerializer
