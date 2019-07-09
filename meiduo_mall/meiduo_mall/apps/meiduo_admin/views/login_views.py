from rest_framework.views import APIView
from rest_framework.response import Response

from meiduo_admin.serializers.login_seralizers import *


class LoginView(APIView):
    def post(self, request):
        s = LoginSerializers(data=request.data)
        s.is_valid(raise_exception=True)
        return Response({
            'username': s.validated_data['user'].username,
            'user_id': s.validated_data['user'].id,
            'token': s.validated_data['token']
        })
