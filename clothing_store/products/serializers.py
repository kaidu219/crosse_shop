from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Cериалайзер используется для товаров, при отображении списком
    """
    dimensions = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'new_price',
                  'old_price', 'dimensions', 'colors']

    def get_dimensions(self, obj):
        dimensions = obj.dimensions.all()
        return [dimension.title for dimension in dimensions]

    def get_colors(self, obj):
        colors = obj.colors.all()
        return [color.title for color in colors]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dimensions'] = self.get_dimensions(instance)
        representation['colors'] = self.get_colors(instance)
        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Cериалайзер используется для товаров, при детальном отображении 
    """
    dimensions = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_dimensions(self, obj):
        dimensions = obj.dimensions.all()
        return [dimension.title for dimension in dimensions]

    def get_colors(self, obj):
        colors = obj.colors.all()
        return [color.title for color in colors]

    def get_brand(self, obj):
        return obj.brand.title

    def get_category(self, obj):
        return obj.category.title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dimensions'] = self.get_dimensions(instance)
        representation['colors'] = self.get_colors(instance)
        representation['brand'] = self.get_brand(instance)
        representation['category'] = self.get_category(instance)
        return representation
