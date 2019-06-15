from django import http
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
import re
from .models import User
from meiduo_mall.utils.response_code import RETCODE
from django_redis import get_redis_connection



class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        mobile = request.POST.get("mobile")
        sms_code = request.POST.get("sms_code")
        allow = request.POST.get("allow")
        redis_conn = get_redis_connection("verify_code")
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return http.HttpResponseForbidden('验证码已过期')
        redis_conn.delete('sms_%s' % mobile)
        sms_code_server = sms_code_server.decode()

        if all([username, password, mobile, sms_code, allow]) is False:
            return http.HttpResponseForbidden("缺少必要的参数")
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')

        # if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
        #     return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        #

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20个字符的密码')
        if password != password2:
            return http.HttpResponseForbidden("两次密码不一致")
        if not re.match(r'1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入11位手机号')
        if sms_code != sms_code_server:
            return http.HttpResponseForbidden('验证码错误')

        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        login(request, user)

        response = redirect('/')
        response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)
        return response


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        content = {"count": count, "code": RETCODE.OK, "errmsg": "OK"}
        return http.JsonResponse(content)


class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        content = {'count': count, "code": RETCODE.OK, "errmsg": "OK"}
        return http.JsonResponse(content)


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        query_dist = request.POST
        username = query_dist.get('username')
        password = query_dist.get('password')
        remembered = query_dist.get('remembered')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': "账号或密码错误"})
        login(request, user)
        if remembered is None:
            request.session.set_expiry(0)
        response = redirect(request.GET.get('next', '/'))
        response.set_cookie('username', user.username, max_age=(settings.SESSION_COOKIE_AGE if remembered else None))
        return response


class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect('/login/')
        response.delete_cookie('username')
        return response




