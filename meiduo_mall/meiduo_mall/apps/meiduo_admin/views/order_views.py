from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from orders.models import OrderInfo, OrderGoods
from meiduo_admin.pages import Page
from meiduo_admin.serializers.order_serializer import Orderserializer, OrderDetailSerializer


class OrderViews(ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = Orderserializer
    pagination_class = Page

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(order_id__contains=keyword)
        return self.queryset.all()


class OrderDetailViews(RetrieveAPIView, UpdateAPIView):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderDetailSerializer