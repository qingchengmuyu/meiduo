from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        # username = attrs.get('username')
        # password = attrs.get('password')
        # authenticate(username=username, password=password)  # 传统用户验证
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('用户名或密码错误!')
        payload = jwt_payload_handler(user)
        jwt_token = jwt_encode_handler(payload)
        return ({
            'user': user,
            'tocken': jwt_token
        })