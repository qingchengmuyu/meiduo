from rest_framework import serializers
from fdfs_client.client import Fdfs_client
from django.conf import settings

from goods.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'logo',
            'first_letter'
        ]

    def create(self, validated_data):
        file = validated_data.pop('logo')
        conent = file.read()
        conn = Fdfs_client(settings.FDFS_CONFPATH)
        res = conn.upload_appender_by_buffer(conent)
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        validated_data['logo'] = res['Remote file_id']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        file = validated_data.pop('logo')
        conent = file.read()
        conn = Fdfs_client(settings.FDFS_CONFPATH)
        res = conn.upload_appender_by_buffer(conent)
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        # logo = res['Remote file_id']
        # instance.logo = logo
        # instance.save()
        # return instance
        validated_data['logo'] = res['Remote file_id']
        return super().update(instance, validated_data)

