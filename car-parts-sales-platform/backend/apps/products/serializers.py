from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductAttribute


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True, default=None)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'parent', 'parent_name',
            'sort_order', 'is_active', 'created_at', 'updated_at',
            'children_count'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_children_count(self, obj):
        return obj.children.count()


class CategoryTreeSerializer(serializers.ModelSerializer):
    """分类树序列化器（支持递归嵌套）"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'sort_order', 'is_active', 'children']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('sort_order')
        return CategoryTreeSerializer(children, many=True).data


class ProductImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'sort_order', 'created_at']


class ProductAttributeSerializer(serializers.ModelSerializer):
    """商品属性序列化器"""

    class Meta:
        model = ProductAttribute
        fields = ['id', 'attr_name', 'attr_value', 'sort_order', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器（简洁版）"""
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'original_price',
            'category', 'category_name', 'main_image',
            'status', 'sales_count', 'view_count',
            'is_featured', 'is_new', 'stock_quantity',
            'image_count', 'created_at'
        ]
        read_only_fields = ['sales_count', 'view_count', 'created_at']

    def get_image_count(self, obj):
        return obj.images.count()


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器（完整版）"""
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'original_price',
            'category', 'category_name', 'main_image',
            'status', 'stock_quantity',
            'sales_count', 'view_count',
            'is_featured', 'is_new',
            'images', 'attributes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['sales_count', 'view_count', 'created_at', 'updated_at']
