from rest_framework.generics import ListAPIView, CreateAPIView

from meiduo_admin.pages import Page
from users.models import User
from meiduo_admin.serializers.user_serializer import UserSerializer


class UserViews(ListAPIView, CreateAPIView,):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
    pagination_class = Page

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.filter(username__startswith=keyword)
        return self.queryset.all()
