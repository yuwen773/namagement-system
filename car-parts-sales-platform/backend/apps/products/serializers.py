from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductAttribute, Review


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
    category_name = serializers.SerializerMethodField()
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

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器（完整版）"""
    category_name = serializers.SerializerMethodField()
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

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None


class ReviewSerializer(serializers.ModelSerializer):
    """评价序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_id_display = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'product', 'product_name', 'user_id', 'user_id_display',
            'order_item_id', 'rating', 'comment', 'images',
            'is_anonymous', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_id_display(self, obj):
        """获取用户ID显示（匿名则隐藏）"""
        if obj.is_anonymous:
            return None
        return obj.user_id


class ReviewCreateSerializer(serializers.ModelSerializer):
    """评价创建序列化器"""

    class Meta:
        model = Review
        fields = ['order_item_id', 'rating', 'comment', 'images', 'is_anonymous']

    def validate_rating(self, value):
        """校验评分范围"""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("评分必须在1-5之间")
        return value

    def validate_images(self, value):
        """校验图片格式"""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("图片必须是列表格式")
        return value

    def validate(self, attrs):
        """验证订单项是否属于已完成订单"""
        order_item_id = attrs.get('order_item_id')

        if order_item_id:
            from apps.orders.models import OrderItem, Order

            try:
                order_item = OrderItem.objects.select_related('order').get(id=order_item_id)
                order = order_item.order

                # 验证订单状态必须是已完成
                if order.status != Order.Status.COMPLETED:
                    raise serializers.ValidationError("只有已完成的订单才能评价")

                # 验证订单商品是否匹配（在视图层面验证 product_id）
                # 这里只是验证订单状态的有效性

            except OrderItem.DoesNotExist:
                raise serializers.ValidationError("订单项不存在")

        return attrs


class ReviewListSerializer(serializers.ModelSerializer):
    """评价列表序列化器（简洁版）"""
    user_id_display = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'comment', 'images',
            'user_id_display', 'is_anonymous', 'created_at'
        ]

    def get_user_id_display(self, obj):
        if obj.is_anonymous:
            return '匿名用户'
        return f'用户{obj.user_id}'
