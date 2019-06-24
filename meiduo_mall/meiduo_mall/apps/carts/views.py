import base64
import pickle

from django import http
from django.shortcuts import render
from django.views import View
import json
from django_redis import get_redis_connection

from goods.models import SKU
from meiduo_mall.utils.response_code import RETCODE


class CartsView(View):
    """购物车添加"""

    def post(self, request):
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)
        if all([sku_id, count]) is False:
            return http.HttpResponseForbidden('缺少必要参数')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden("商品不存在")
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden("参数错误")
        if isinstance(selected, bool) is False:
            return http.HttpResponseForbidden("参数错误")

        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection("carts")
            pl = redis_conn.pipeline()
            pl.hincrby("carts_%s" % user.id, sku_id, count)
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            pl.execute()
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': "添加购物车成功"})
        else:
            cart_str = request.COOKIES.get("carts")
            if cart_str:
                cart_str_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_str_bytes)
                cart_dict = pickle.loads(cart_bytes)
                if sku_id in cart_dict:
                    origin_count = cart_dict[sku_id]['count']
                    count += origin_count
            else:
                cart_dict = {}
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            cart_bytes = pickle.dumps(cart_dict)
            cart_str_bytes = base64.b64encode(cart_bytes)
            cart_str = cart_str_bytes.decode()
            response = http.HttpResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
            response.set_cookie('carts', cart_str)
            return response

    def get(self, request):
        """购物车数据展示"""

        return render(request, 'cart.html')
