from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from users.models import User
from meiduo_admin.pages import Page
from meiduo_admin.serializers.admin_serializer import AdminSerializer


class AdminViews(ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminSerializer
    pagination_class = Page


class AdminSimpleViews(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
