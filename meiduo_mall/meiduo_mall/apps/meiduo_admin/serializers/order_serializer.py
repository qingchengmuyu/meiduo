from rest_framework import serializers

from orders.models import OrderInfo, OrderGoods
from goods.models import SKU


class Orderserializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = [
            'order_id',
            'create_time'
        ]


class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = [
            'name',
            'default_image'
        ]


class SkusSerializer(serializers.ModelSerializer):
    sku = SkuSerializer()

    class Meta:
        model = OrderGoods
        fields = [
            'count',
            'price',
            'sku'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    skus = SkusSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
