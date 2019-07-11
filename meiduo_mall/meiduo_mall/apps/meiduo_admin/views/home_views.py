from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.response import Response
import pytz
from django.conf import settings
from datetime import timedelta

from users.models import User
from goods.models import GoodsVisitCount
from meiduo_admin.serializers.home_serializers import GoodsPageviewsSerializers


class HomeViewSet(ViewSet):
    permission_classes = [IsAdminUser]

    @action(methods=['get'], detail=False)
    def total_count(self, request):
        count = User.objects.count()
        date = timezone.now().date()
        return Response({
            'count': count,
            'date': date
        })

    @action(methods=['get'], detail=False)
    def day_increment(self, request):
        # 获取上海零点
        data_0_shanghai = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE)).replace(hour=0, minute=0,
                                                                                               second=0)
        count = User.objects.filter(date_joined__gte=data_0_shanghai).count()
        return Response({
            'count': count,
            'date': data_0_shanghai.date()
        })

    @action(methods=['get'], detail=False)
    def day_active(self, request):
        date_0_shanghai = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE)).replace(hour=0, minute=0,
                                                                                               second=0)
        count = User.objects.filter(last_login__gte=date_0_shanghai).count()
        return Response({
            'count': count,
            'date': date_0_shanghai.date()
        })

    @action(methods=['get'], detail=False)
    def day_orders(self, request):
        date_0_shanghai = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE)).replace(hour=0, minute=0,
                                                                                               second=0)
        # 从主表开始过滤
        user_queryset = User.objects.filter(orderinfo__create_time__gte=date_0_shanghai)
        count = len(set(user_queryset))
        return Response({
            "count": count,
            "date": date_0_shanghai.date()
        })

    @action(methods=['get'], detail=False)
    def month_increment(self, request):
        cur__date = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))
        start_date = cur__date - timedelta(days=29)
        date_list = []
        for index in range(30):
            clac_date = (start_date + timedelta(index)).replace(hour=0, minute=0, second=0)
            count = User.objects.filter(date_joined__gte=clac_date,
                                        date_joined__lt=(clac_date + timedelta(days=1))).count()
            date_list.append({
                'count': count,
                'date': clac_date.date()
            })
        return Response(date_list)

    @action(methods=['get'], detail=False)
    def goods_day_views(self, request):
        date_0_shanghai = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE)).replace(hour=0, minute=0,
                                                                                               second=0)
        gv = GoodsVisitCount.objects.filter(create_time__gte=date_0_shanghai)
        gvs = GoodsPageviewsSerializers(gv, many=True)
        return Response(gvs.data)

