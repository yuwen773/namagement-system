"""
订单管理序列化器

包含订单、订单商品、退换货申请的序列化器
"""
from rest_framework import serializers
from .models import Order, OrderItem, ReturnRequest


class OrderItemSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_image',
            'product_price', 'quantity', 'subtotal', 'created_at'
        ]
        read_only_fields = ['id', 'subtotal', 'created_at']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """订单商品创建序列化器（简化版）"""

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderListSerializer(serializers.ModelSerializer):
    """订单列表序列化器（简化版）"""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'user', 'user_phone', 'user_nickname',
            'total_amount', 'discount_amount', 'pay_amount',
            'status', 'status_display', 'items_count',
            'express_company', 'tracking_number',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_no', 'created_at', 'updated_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器（完整版）"""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    coupon_name = serializers.CharField(source='coupon.coupon.name', read_only=True, allow_null=True)
    items = OrderItemSerializer(many=True, read_only=True)
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'user', 'user_phone', 'user_nickname',
            'recipient_name', 'recipient_phone',
            'recipient_province', 'recipient_city', 'recipient_district',
            'recipient_address', 'full_address',
            'total_amount', 'discount_amount', 'shipping_fee', 'pay_amount',
            'coupon', 'coupon_name',
            'status', 'status_display',
            'express_company', 'tracking_number',
            'remark', 'items',
            'created_at', 'updated_at', 'paid_at', 'shipped_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'order_no', 'user', 'total_amount', 'discount_amount',
            'pay_amount', 'created_at', 'updated_at'
        ]

    def get_full_address(self, obj):
        """获取完整地址"""
        return f'{obj.recipient_province}{obj.recipient_city}{obj.recipient_district}{obj.recipient_address}'


class OrderCreateSerializer(serializers.ModelSerializer):
    """订单创建序列化器"""

    items = OrderItemCreateSerializer(many=True, write_only=True)
    coupon_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'recipient_name', 'recipient_phone',
            'recipient_province', 'recipient_city', 'recipient_district',
            'recipient_address',
            'total_amount', 'discount_amount', 'shipping_fee', 'pay_amount',
            'coupon_id', 'items', 'remark'
        ]

    def create(self, validated_data):
        """创建订单"""
        items_data = validated_data.pop('items', [])
        coupon_id = validated_data.pop('coupon_id', None)
        user = self.context['request'].user

        # 设置优惠券
        if coupon_id:
            from apps.marketing.models import UserCoupon
            try:
                validated_data['coupon'] = UserCoupon.objects.get(id=coupon_id, user=user)
            except UserCoupon.DoesNotExist:
                pass

        # 创建订单
        order = Order.objects.create(user=user, **validated_data)

        # 创建订单商品
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_image=product.image,
                product_price=product.price,
                quantity=quantity
            )

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """订单更新序列化器（部分更新）"""

    class Meta:
        model = Order
        fields = [
            'status', 'express_company', 'tracking_number', 'remark'
        ]


class OrderShipSerializer(serializers.Serializer):
    """订单发货序列化器"""

    express_company = serializers.CharField(max_length=50, required=True)
    tracking_number = serializers.CharField(max_length=100, required=True)


class ReturnRequestListSerializer(serializers.ModelSerializer):
    """退换货申请列表序列化器"""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    request_type_display = serializers.CharField(source='get_request_type_display', read_only=True)
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    user_phone = serializers.CharField(source='order.user.phone', read_only=True)

    class Meta:
        model = ReturnRequest
        fields = [
            'id', 'order', 'order_no', 'user_phone',
            'request_type', 'request_type_display',
            'reason', 'status', 'status_display',
            'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'created_at', 'processed_at']


class ReturnRequestDetailSerializer(serializers.ModelSerializer):
    """退换货申请详情序列化器"""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    request_type_display = serializers.CharField(source='get_request_type_display', read_only=True)
    order_info = OrderListSerializer(source='order', read_only=True)

    class Meta:
        model = ReturnRequest
        fields = [
            'id', 'order', 'order_info',
            'request_type', 'request_type_display',
            'reason', 'evidence_images',
            'status', 'status_display',
            'admin_note', 'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'created_at', 'processed_at']


class ReturnRequestCreateSerializer(serializers.ModelSerializer):
    """退换货申请创建序列化器"""

    class Meta:
        model = ReturnRequest
        fields = ['order', 'request_type', 'reason', 'evidence_images']

    def validate_order(self, value):
        """验证订单状态"""
        if value.status != Order.Status.COMPLETED:
            raise serializers.ValidationError('只有已完成的订单才能申请退换货')
        return value


class ReturnRequestProcessSerializer(serializers.Serializer):
    """退换货申请处理序列化器"""

    status = serializers.ChoiceField(choices=ReturnRequest.Status.choices[1:])  # 排除待处理
    admin_note = serializers.CharField(required=False, allow_blank=True, max_length=500)
