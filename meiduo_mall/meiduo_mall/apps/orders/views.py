from decimal import Decimal
from django.shortcuts import render
from django_redis import get_redis_connection

from meiduo_mall.utils.views import LoginRequiredViews
from users.models import Address
from goods.models import SKU


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
