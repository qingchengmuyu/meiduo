from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password = make_password(password)
        attrs['password'] = password
        attrs['is_staff'] = True
        return attrs

    # def create(self, validated_data):
    #     # validated_data['password'] = make_password(validated_data['password'])
    #     # validated_data['is_staff'] = True
    #     # return super().create(validated_data)
    #
    #     return self.Meta.model.objects.create_superuser(**validated_data)

