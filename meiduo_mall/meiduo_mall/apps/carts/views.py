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
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection("carts")
            redis_carts = redis_conn.hgetall('carts_%s' % user.id)
            selected_ids = redis_conn.smembers('selected_%s' % user.id)
            cart_dict = {}
            for sku_id_bytes in redis_carts:
                cart_dict[int(sku_id_bytes)] = {
                    'count': int(redis_carts[sku_id_bytes]),
                    'selected': sku_id_bytes in selected_ids
                }
        else:
            cat_str = request.COOKIES.get('carts')
            if cat_str:
                cart_dict = pickle.loads(base64.b64decode(cat_str.encode()))
            else:
                return render(request, 'cart.html')
        sku_qs = SKU.objects.filter(id__in=cart_dict.keys())
        cart_skus = []
        for sku in sku_qs:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),
                'count': cart_dict[sku.id]['count'],
                'selected': str(cart_dict[sku.id]['selected']),
                'amount': str(sku.price * cart_dict[sku.id]['count'])
            })
        return render(request, 'cart.html', {'cart_skus': cart_skus})

    def put(self, request):
        """修改购物车逻辑"""
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected')
        if all([sku_id, ]) is False:
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku_id错误')
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数错误')
        if count < 0 or isinstance(selected, bool) is False:
            return http.HttpResponseForbidden('参数类型错误')
        user = request.user
        cart_skus = {
            'id': sku.id,
            'name': sku.name,
            'default_image_url': sku.default_image.url,
            'price': str(sku.price),
            'count': count,
            'selected': selected,
            'amount': str(sku.price * count)
        }
        response = http.HttpResponse({'code': RETCODE.OK, 'errmsg': '修改购物车数据成功', 'cart_skus': cart_skus})
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hset('carts_%s' % user.id, sku_id, count)
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return render(request, 'cart.html')
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response.set_cookie('carts', cart_str)
        return response

    def delete(self, request):
        """删除购物车数据"""
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku_id不存在')
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hdel('carts_%s' % user.id, sku_id)
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': "删除购物车成功"})
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return http.HttpResponseForbidden('缺少cookie')
            if sku_id in cart_dict:
                del cart_dict[sku_id]
            response = http.HttpResponse({'code': RETCODE.OK, 'errmsg': '删除购物车成功'})
            if not cart_dict:
                response.delete_cookie('carts')
                return response
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response.set_cookie('carts', cart_str)
            return response


class CartsSelectedAllView(View):
    """购物车全选"""

    def put(self, request):
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected')
        if isinstance(selected, bool) is False:
            return http.HttpResponseForbidden("参数类型错误")
        user = request.user
        if user.is_authenticated:
            redise_conn = get_redis_connection('carts')
            redis_carts = redise_conn.hgetall('carts_%s' % user.id)
            if selected:
                redise_conn.sadd('selected_%s' % user.id, *redis_carts.keys())
            else:
                redise_conn.delete('selected_%s' % user.id)
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': "ok"})
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return http.HttpResponseForbidden("cookie没有获取到")
            for sku_dict in cart_dict.values():
                sku_dict['selected'] = selected
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
            response.set_cookie('carts', cart_str)
            return response
