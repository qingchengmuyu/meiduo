from rest_framework import serializers

from goods.models import SKU, SKUSpecification, GoodsCategory, SPU, SPUSpecification, SpecificationOption


class SKUPecSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


class SKUSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    specs = SKUPecSerializer(many=True, read_only=True)

    class Meta:
        model = SKU
        fields = '__all__'


class GoodsCategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class SPUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


class SpecOptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = [
            'id',
            'value'
        ]


class SPUSpecSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()
    options = SpecOptSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = [
            "id",
            "name",
            "spu",
            "spu_id",
            "options"
        ]
