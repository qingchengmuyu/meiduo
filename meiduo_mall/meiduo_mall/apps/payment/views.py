from django import http
from django.shortcuts import render
from alipay import AliPay
from django.conf import settings
import os
from django.views import View

from meiduo_mall.utils.views import LoginRequiredViews
from orders.models import OrderInfo
from meiduo_mall.utils.response_code import RETCODE


class PaymentView(LoginRequiredViews):
    """生成支付链接"""

    def get(self, request, order_id):
        try:
            order = OrderInfo.objects.get(user=request.user, order_id=order_id,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单错误')
        alipay = AliPay(
            appid="2016101100662502",
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'keys/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG  # 默认False
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject='美多商城:%s' % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )
        alipay_url = settings.ALIPAY_URL + '?' + order_string
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})


# class PaymentStatusView(View):
#     """验证支付结果"""
#
#     def get(self, request):
#         query_dict = request.GET
#         data = query_dict.dict(
#             sing
#         )

