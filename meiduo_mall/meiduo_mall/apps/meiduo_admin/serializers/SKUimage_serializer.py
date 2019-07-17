from rest_framework import serializers
from fdfs_client.client import Fdfs_client
from django.conf import settings

from goods.models import SKUImage, SKU


class SKUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = [
            'id',
            'name'
        ]


class SKUImageSerializer(serializers.ModelSerializer):
    # sku = serializers.StringRelatedField()

    class Meta:
        model = SKUImage
        fields = [
            'id',
            'sku',
            'image'
        ]

    def create(self, validated_data):
        file = validated_data.pop('image')
        conent = file.read()
        conn = Fdfs_client(settings.FDFS_CONFPATH)
        res = conn.upload_appender_by_buffer(conent)
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        validated_data['image'] = res['Remote file_id']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        file = validated_data.pop('image')
        conent = file.read()
        conn = Fdfs_client(settings.FDFS_CONFPATH)
        res = conn.upload_appender_by_buffer(conent)
        if res['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        validated_data['image'] = res['Remote file_id']
        # instance.image = res['Remote file_id']
        # instance.save()
        # return instance
        return super().update(instance, validated_data)
