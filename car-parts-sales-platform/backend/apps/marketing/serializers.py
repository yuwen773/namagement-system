"""
营销管理序列化器

包含优惠券、用户优惠券等序列化器
"""
from rest_framework import serializers
from .models import Coupon, UserCoupon


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
