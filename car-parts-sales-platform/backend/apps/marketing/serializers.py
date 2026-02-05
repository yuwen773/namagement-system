"""
营销管理序列化器

包含优惠券、用户优惠券、促销活动、Banner 轮播图等序列化器
"""
from rest_framework import serializers
from .models import Coupon, UserCoupon, Promotion, Banner


class CouponSerializer(serializers.ModelSerializer):
    """优惠券序列化器"""

    class Meta:
        model = Coupon
        fields = [
            'id', 'name', 'description', 'discount_type', 'min_amount',
            'discount_amount', 'discount_rate', 'valid_from', 'valid_until',
            'total_quantity', 'per_user_limit', 'issued_quantity', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['issued_quantity', 'created_at', 'updated_at']


class CouponListSerializer(serializers.ModelSerializer):
    """优惠券列表序列化器（简化版）"""

    class Meta:
        model = Coupon
        fields = [
            'id', 'name', 'description', 'discount_type', 'min_amount',
            'discount_amount', 'discount_rate', 'valid_from', 'valid_until',
            'total_quantity', 'issued_quantity', 'is_active'
        ]


class UserCouponSerializer(serializers.ModelSerializer):
    """用户优惠券序列化器"""
    coupon = CouponSerializer(read_only=True)
    coupon_id = serializers.PrimaryKeyRelatedField(
        queryset=Coupon.objects.all(),
        source='coupon',
        write_only=True
    )

    class Meta:
        model = UserCoupon
        fields = [
            'id', 'coupon', 'coupon_id', 'status', 'used_order',
            'obtained_at', 'used_at'
        ]
        read_only_fields = ['status', 'used_order', 'obtained_at', 'used_at']


class UserCouponListSerializer(serializers.ModelSerializer):
    """用户优惠券列表序列化器（简化版）"""
    coupon_name = serializers.CharField(source='coupon.name', read_only=True)
    coupon_type = serializers.CharField(source='coupon.discount_type', read_only=True)
    discount_info = serializers.SerializerMethodField()

    class Meta:
        model = UserCoupon
        fields = [
            'id', 'coupon_name', 'coupon_type', 'discount_info', 'status',
            'obtained_at', 'used_at'
        ]

    def get_discount_info(self, obj):
        """获取优惠信息"""
        if obj.coupon.discount_type == 'full_reduction':
            return f'满{obj.coupon.min_amount}减{obj.coupon.discount_amount}'
        else:
            return f'{obj.coupon.discount_rate}折'


class PromotionSerializer(serializers.ModelSerializer):
    """促销活动序列化器"""
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text='关联商品ID列表'
    )
    products = serializers.SerializerMethodField(read_only=True)
    coupon_name = serializers.CharField(source='coupon.name', read_only=True)
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Promotion
        fields = [
            'id', 'name', 'description', 'promotion_type', 'products', 'product_ids',
            'coupon', 'coupon_name', 'start_time', 'end_time', 'discount_rate',
            'discount_amount', 'image', 'sort_order', 'is_active', 'is_valid',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_products(self, obj):
        """获取关联商品列表"""
        from apps.products.serializers import ProductListSerializer
        products = obj.products.all()
        return ProductListSerializer(products, many=True).data

    def create(self, validated_data):
        """创建促销活动"""
        product_ids = validated_data.pop('product_ids', [])
        promotion = Promotion.objects.create(**validated_data)
        if product_ids:
            promotion.products.set(product_ids)
        return promotion

    def update(self, instance, validated_data):
        """更新促销活动"""
        product_ids = validated_data.pop('product_ids', None)

        # 更新基本字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 更新关联商品
        if product_ids is not None:
            instance.products.set(product_ids)

        return instance


class PromotionListSerializer(serializers.ModelSerializer):
    """促销活动列表序列化器（简化版）"""
    coupon_name = serializers.CharField(source='coupon.name', read_only=True)
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Promotion
        fields = [
            'id', 'name', 'promotion_type', 'coupon_name', 'start_time',
            'end_time', 'discount_rate', 'discount_amount', 'image',
            'sort_order', 'is_active', 'is_valid', 'created_at'
        ]


class BannerSerializer(serializers.ModelSerializer):
    """Banner 轮播图序列化器"""
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'subtitle', 'image', 'link_type', 'link_value',
            'position', 'sort_order', 'is_active', 'start_time', 'end_time',
            'is_valid', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BannerListSerializer(serializers.ModelSerializer):
    """Banner 列表序列化器（简化版）"""
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'image', 'link_type', 'link_value',
            'position', 'sort_order', 'is_active', 'is_valid'
        ]
