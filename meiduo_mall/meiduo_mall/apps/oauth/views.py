import re
from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
import logging
from django.conf import settings
from django_redis import get_redis_connection

from meiduo_mall.utils.response_code import RETCODE
from .models import OAuthQQUser
from .utils import generate_openid_signature, check_openid_signature
from users.models import User
from carts.utils import merge_cart_cookie_to_redis

logger = logging.getLogger('django')


class QQAuthURLView(View):
    def get(self, request):
        next = request.GET.get('next', '/')
        oauth_qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                           client_secret=settings.QQ_CLIENT_SECRET,
                           redirect_uri=settings.QQ_REDIRECT_URI,
                           state=next)
        login_url = oauth_qq.get_qq_url()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': login_url})


class QQAuthView(View):
    """QQ登陆成功后的回调处理"""

    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            return http.HttpResponseForbidden('缺少code')
        auth_qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                          client_secret=settings.QQ_CLIENT_SECRET,
                          redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token = auth_qq.get_access_token(code)
            openid = auth_qq.get_open_id(access_token)
            print('openid', openid)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')

        try:
            oauth_modle = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            openid = generate_openid_signature(openid)
            return render(request, 'oauth_callback.html', {'openid': openid})

        else:
            user = oauth_modle.user
            login(request, user)
            response = redirect(request.GET.get('next', '/'))
            response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
            return response

    def post(self, request):

        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        sms_code = request.POST.get("sms_code")
        openid_sign = request.POST.get('openid')

        redis_conn = get_redis_connection("verify_code")
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return http.HttpResponseForbidden('验证码已过期')
        redis_conn.delete('sms_%s' % mobile)
        sms_code_server = sms_code_server.decode()

        if all([mobile, password, sms_code, openid_sign]) is False:
            return http.HttpResponseForbidden("缺少必要的参数")

        if not re.match(r'1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入11位手机号')

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20个字符的密码')

        if sms_code != sms_code_server:
            return http.HttpResponseForbidden('验证码错误')

        openid = check_openid_signature(openid_sign)
        if openid is None:
            return http.HttpResponseForbidden('openid无效')
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)
        else:
            if user.check_password(password) is False:
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})
        OAuthQQUser.objects.create(openid=openid, user=user)
        login(request, user)
        response = redirect(request.GET.get('next', '/'))
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
        return response
        login(request, user)
        response = redirect('/')
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
        merge_cart_cookie_to_redis(request, response)
        return response
