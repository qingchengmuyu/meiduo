from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredViews(LoginRequiredMixin, View):
    """自定义一个登陆判断类"""
    pass
