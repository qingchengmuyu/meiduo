from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'mobile',

            'groups',
            'user_permissions',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def create(self, validated_data):









