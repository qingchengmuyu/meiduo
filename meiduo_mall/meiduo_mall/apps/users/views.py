import json

from django import http
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import mixins
from django.utils.decorators import method_decorator
from django.views import View
import re
from django.core.mail import send_mail

from .models import User
from meiduo_mall.utils.response_code import RETCODE
from django_redis import get_redis_connection
from meiduo_mall.utils.views import LoginRequiredViews
from .utils import generate_verify_email_url, check_verify_email_token
from celery_tasks.email.tasks import send_verify_email


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
        # 实现手机号登陆
        if re.match(r'^1[3-9]\d{9}$', username):
            User.USERNAME_FIELD = 'mobile'

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


# class InfoView(View):
#     """个人中心"""
#     def get(self, request):
#         user = request.user
#         if user.is_authenticated:
#             return render(request, 'user_center_info.html')
#         else:
#             return redirect('/login/?next=/info/')


# class InfoView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         return render(request, 'user_center_info.html')

#
# class InfoView(View):
#     """展示用户中心"""
#     @method_decorator(login_required)
#     def get(self, request):
#         # 判断用户是否登录, 如果登录显示个人中心界面
#         return render(request, 'user_center_info.html')


class InfoView(mixins.LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_info.html')


class EmailView(LoginRequiredViews):
    def put(self, request):
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('邮箱格式错误')
        user = request.user
        user.email = email
        user.save()
        verify_url = generate_verify_email_url(user)
        print('verify_url:', verify_url)

        send_verify_email(email, verify_url)
        print('邮件异步发送')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class EmailVerificationView(View):
    """验证账户"""
    def get(self, request):
        token = request.GET.get('token')
        if token is None:
            return http.HttpResponseForbidden('缺少token参数')
        user = check_verify_email_token(token)
        if user is None:
            return http.HttpResponseForbidden('token无效')
        user.email_active = True
        user.save()

        return redirect('/info/')


class AddressView(LoginRequiredViews):
    def get(self, request):
        return render(request, 'user_center_site.html')
