from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import SimpleRouter

from .views.home_views import *
from .views.user_views import UserViews
from .views.sku_views import SKUViewSet
from .views.spu_views import *
from .views.specs_views import SpecsViews
from .views.option_views import OptionViews, SimpleViews
from .views.channels_views import ChannelViews, ChannelGroupViews
from .views.brand_views import BrandViews
from .views.SKUimage_views import SKUImageViews, SKUSimpleViews
from .views.order_views import OrderViews, OrderDetailViews
from .views.perms_views import PermViews, ContentViews
from .views.group_views import GroupViews, GroupSimpleViews
from .views.admin_views import AdminViews,AdminSimpleViews


urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^users/$', UserViews.as_view()),
    url(r'^skus/$', SKUViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^skus/categories/$', SKUViewSet.as_view({'get': 'categories'})),
    url(r'^goods/simple/$', SKUViewSet.as_view({'get': 'simple'})),
    url(r'^skus/simple/$', SKUSimpleViews.as_view({'get': 'list'})),
    url(r'^goods/(?P<pk>\d+)/specs/$', SKUViewSet.as_view({'get': 'specs'})),
    url(r'^goods/(?P<pk>\d+)/$', SPUViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^goods//specs/$', SKUViewSet.as_view({'get': 'list'})),
    url(r'^goods/specs/$', SpecsViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^goods/specs/(?P<pk>\d+)/$', SpecsViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^goods/$', SPUViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^goods/brands/simple/$', SPUViews.as_view({'get': 'brands'})),
    url(r'^goods/channel/categories/$', SPUViews.as_view({'get': 'categories'})),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', SPUViews.as_view({'get': 'categoriess'})),
    url(r'^skus/(?P<pk>\d+)/$', SKUViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^specs/options/$', OptionViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^specs/options/(?P<pk>\d+)/$', OptionViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^goods/specs/simple/$', SimpleViews.as_view()),
    url(r'^goods/channels/$', ChannelViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^goods/channels/(?P<pk>\d+)/$', ChannelViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^goods/categories/$', SPUViews.as_view({'get': 'categories'})),
    url(r'^goods/channel_types/$', ChannelGroupViews.as_view()),
    url(r'^goods/brands/$', BrandViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^goods/brands/(?P<pk>\d+)/$', BrandViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^skus/images/$', SKUImageViews.as_view({'get': 'list', 'post': 'create'})),
    url(r'^skus/images/(?P<pk>\d+)/$', SKUImageViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetailViews.as_view()),
    url(r'^orders/(?P<pk>\d+)/status/$', OrderDetailViews.as_view()),
    url(r'^orders/$', OrderViews.as_view({'get': 'list'})),
    url(r'^permission/content_types/$', ContentViews.as_view()),
    url(r'^permission/simple/$', GroupSimpleViews.as_view()),
    url(r'^permission/groups/simple/$', AdminSimpleViews.as_view()),
]

router = SimpleRouter()
router.register(prefix='statistical', viewset=HomeViewSet, base_name='statistical')
router.register(prefix='permission/perms', viewset=PermViews, base_name='PermViews')
router.register(prefix='permission/groups', viewset=GroupViews, base_name='GroupViews')
router.register(prefix='permission/admins', viewset=AdminViews, base_name='GroupViews')
urlpatterns += router.urls
