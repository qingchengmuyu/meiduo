import json
from django.utils import timezone
from decimal import Decimal
from django import http
from django.shortcuts import render
from django_redis import get_redis_connection
from django.db import transaction

from meiduo_mall.utils.views import LoginRequiredViews
from users.models import Address
from goods.models import SKU
from .models import OrderInfo, OrderGoods
from meiduo_mall.utils.response_code import RETCODE


class OrderSettlementView(LoginRequiredViews):
    """去结算"""

    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user, is_deleted=False)
        if addresses.exists() is False:
            addresses = None
        redis_conn = get_redis_connection('carts')
        redis_carts = redis_conn.hgetall('carts_%s' % user.id)
        selected_ids = redis_conn.smembers('selected_%s' % user.id)
        cart_dict = {}
        for sku_id_bytes in selected_ids:
            cart_dict[int(sku_id_bytes)] = int(redis_carts[sku_id_bytes])
        skus = SKU.objects.filter(id__in=cart_dict.keys())
        total_count = 0
        total_amount = 0
        freight = Decimal('10.00')
        for sku in skus:
            sku.count = cart_dict[sku.id]
            sku.amount = sku.price * sku.count
            total_count += sku.count
            total_amount += sku.amount
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight
        }
        return render(request, 'place_order.html', context)


class OrderCommitView(LoginRequiredViews):
    """提交订单"""

    def post(self, request):
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get("address_id")
        pay_method = json_dict.get("pay_method")
        user = request.user
        if all([address_id, pay_method]) is False:
            return http.HttpResponseForbidden("缺少必传参数")
        try:
            address = Address.objects.get(user=user, id=address_id)
        except Address.DoesNotExist:
            return http.HttpResponseForbidden("address_id错误")
        if pay_method not in OrderInfo.PAY_METHODS_ENUM.values():
            return http.HttpResponseForbidden('支付方式有误')
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id
        status = (OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                  if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                  else OrderInfo.ORDER_STATUS_ENUM['UNSEND'])

        with transaction.atomic():
            save_point = transaction.savepoint()

            try:
                order_model = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address_id=address_id,
                    total_count=0,
                    total_amount=Decimal('0.00'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=status
                )
                redis_conn = get_redis_connection('carts')
                redis_carts = redis_conn.hgetall('carts_%s' % user.id)
                selected_ids = redis_conn.smembers('selected_%s' % user.id)
                cart_dict = {}
                for sku_id_bytes in selected_ids:
                    cart_dict[int(sku_id_bytes)] = int(redis_carts[sku_id_bytes])
                for sku_id in cart_dict:
                    while True:
                        sku = SKU.objects.get(id=sku_id)
                        buy_count = cart_dict[sku_id]
                        origin_stock = sku.stock
                        origin_sales = sku.sales
                        # import time
                        # time.sleep(5)
                        if buy_count > origin_stock:
                            transaction.savepoint_rollback(save_point)

                            return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})
                        new_stock = origin_stock - buy_count
                        new_sales = origin_sales + buy_count
                        resuat = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                        if resuat == 0:
                            continue

                        # sku.stock = new_stock
                        # sku.sales = new_sales
                        # sku.save()
                        spu = sku.spu
                        spu.sales += buy_count
                        spu.save()

                        OrderGoods.objects.create(
                            order_id=order_id,
                            sku=sku,
                            count=buy_count,
                            price=sku.price
                        )
                        order_model.total_count += buy_count
                        order_model.total_amount += (sku.price * buy_count)
                        break
                order_model.total_amount += order_model.freight
                order_model.save()
            except Exception as e:
                print(e)
                transaction.savepoint_rollback(save_point)
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': "下单失败"})
            else:
                transaction.savepoint_commit(save_point)
        pl = redis_conn.pipeline()
        pl.hdel("carts_%s" % user.id, *selected_ids)
        pl.delete('selected_%s' % user.id)
        pl.execute()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order_id})


class OrderSuccessView(LoginRequiredViews):
    """提交订单成功后的界面"""

    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')
        try:
            OrderInfo.objects.get(order_id=order_id, pay_method=pay_method, total_amount=payment_amount,
                                  user=request.user)
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单有误')
        context = {
            'payment_amount': payment_amount,
            'order_id': order_id,
            'pay_method': pay_method
        }
        return render(request, 'order_success.html', context)