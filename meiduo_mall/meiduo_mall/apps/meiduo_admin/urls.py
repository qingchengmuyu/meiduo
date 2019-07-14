from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import SimpleRouter

from .views.home_views import *
from .views.user_views import UserViews
from .views.sku_views import SKUViewSet
from .views.spu_views import *

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^users/$', UserViews.as_view()),
    url(r'^skus/$', SKUViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^skus/categories/$', SKUViewSet.as_view({'get': 'categories'})),
    url(r'^goods/simple/$', SKUViewSet.as_view({'get': 'simple'})),
    url(r'^goods/(?P<pk>\d+)/specs/$', SKUViewSet.as_view({'get': 'specs'})),
    url(r'^goods/(?P<pk>\d+)/$', SPUViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^goods//specs/$', SKUViewSet.as_view({'get': 'list'})),
    url(r'^goods/$', SPUViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^goods/brands/simple/$', SPUViews.as_view({'get': 'brands'})),
    url(r'^goods/channel/categories/$', SPUViews.as_view({'get': 'categories'})),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', SPUViews.as_view({'get': 'categoriess'})),
    url(r'^skus/(?P<pk>\d+)/$', SKUViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]

router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='statistical')
urlpatterns += router.urls
