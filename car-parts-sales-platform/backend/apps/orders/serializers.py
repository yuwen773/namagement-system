"""
订单管理序列化器

包含订单、订单商品、退换货申请、购物车的序列化器
"""
from rest_framework import serializers
from .models import Order, OrderItem, ReturnRequest, Cart, CartItem


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
                    product_image=product.main_image,
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


# ==================== 购物车序列化器 ====================

class CartItemSerializer(serializers.ModelSerializer):
    """购物车商品序列化器"""

    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_status = serializers.CharField(source='product.status', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'product_name', 'product_image',
            'product_status', 'price', 'quantity', 'subtotal', 'added_at'
        ]
        read_only_fields = ['id', 'product_name', 'product_image', 'price', 'subtotal', 'added_at']


class CartItemCreateSerializer(serializers.ModelSerializer):
    """购物车商品创建/更新序列化器"""

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        """验证数量"""
        if value < 1:
            raise serializers.ValidationError('数量必须大于0')
        if value > 999:
            raise serializers.ValidationError('数量不能超过999')
        return value

    def validate(self, attrs):
        """验证商品是否存在且可购买"""
        from apps.products.models import Product
        product = attrs['product']
        if product.status != Product.Status.PUBLISHED:
            raise serializers.ValidationError('该商品暂不可购买')
        if product.stock < attrs['quantity']:
            raise serializers.ValidationError('商品库存不足')
        return attrs


class CartSerializer(serializers.ModelSerializer):
    """购物车序列化器"""

    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 'total_items', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_items', 'total_price', 'created_at', 'updated_at']


class CartItemUpdateSerializer(serializers.Serializer):
    """购物车商品数量更新序列化器"""

    quantity = serializers.IntegerField(min_value=1, max_value=999)

    def validate_quantity(self, value):
        """验证数量"""
        if value < 1:
            raise serializers.ValidationError('数量必须大于0')
        if value > 999:
            raise serializers.ValidationError('数量不能超过999')
        return value

    def validate(self, attrs):
        """验证库存"""
        quantity = attrs['quantity']
        # 在视图验证商品库存
        return attrs
