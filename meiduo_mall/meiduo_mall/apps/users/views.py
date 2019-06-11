from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
import re
from .models import User



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

        if all([username, password, mobile, allow]) is False:
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

        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        login(request, user)
        return redirect('/')



# Create your views here.
