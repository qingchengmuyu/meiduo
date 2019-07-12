from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import SimpleRouter

from .views.home_views import *
from .views.user_views import UserViews

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^users/$', UserViews.as_view()),
]

router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='statistical')
urlpatterns += router.urls
