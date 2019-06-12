from random import randint

from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection


from meiduo_mall.libs.captcha.captcha import captcha
from verifications import contants
from meiduo_mall.libs.yuntongxun.sms import CCP
from meiduo_mall.utils.response_code import RETCODE


class ImageCodeView(View):
    def get(self, request, uuid):
        image_name, image_text, image_bytes = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_code")
        redis_conn.setex(uuid, contants.IMAGE_CODE_REDIS_EXPIRES, image_text)
        return http.HttpResponse(image_bytes, content_type='image/jpg')


class SmsCodeView(View):
    def get(self, request, mobile):
        redis_conn = get_redis_connection('verify_code')

        image_code_client = request.GET.get("image_code")
        uuid = request.GET.get("uuid")
        if all([image_code_client, uuid]) is False:
            return http.HttpResponseForbidden("缺少必要参数")
        image_code_server = redis_conn.get(uuid)
        redis_conn.delete(uuid)
        if image_code_server is None:
            return http.HttpResponseForbidden('图形验证码过期')
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():
            return http.HttpResponseForbidden('图形验证码错误')
        sms_code = '%06d' % randint(0, 999999)
        print("*" * 50)
        print(sms_code)
        print("*" * 50)
        redis_conn.setex('sms_%s' % mobile, contants.SMS_CODE_REDIS_EXPIRES, sms_code)
        CCP().send_template_sms(mobile, [sms_code, contants.SMS_CODE_REDIS_EXPIRES / 60], 1)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '短信验证码发送成功'})




# Create your views here.
