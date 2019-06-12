from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection


from meiduo_mall.libs.captcha.captcha import captcha
from verifications import contants


class ImageCodeView(View):
    def get(self, request, uuid):
        image_name, image_text, image_bytes = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_code")
        redis_conn.setex(uuid, contants.IMAGE_CODE_REDIS_EXPIRES, image_text)
        return http.HttpResponse(image_bytes, content_type='image/jpg')





# Create your views here.
