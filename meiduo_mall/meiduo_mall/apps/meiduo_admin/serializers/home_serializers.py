from rest_framework import serializers
from goods.models import GoodsVisitCount


class GoodsPageviewsSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = GoodsVisitCount
        fields = ['category', 'count']
