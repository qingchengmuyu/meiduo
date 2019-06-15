from django import http
from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
import logging
from  django.conf import settings


from meiduo_mall.utils.response_code import RETCODE

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







