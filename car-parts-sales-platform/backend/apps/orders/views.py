"""
订单管理视图集

包含订单、订单商品、退换货申请、购物车的视图
"""
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q

from utils.response import ApiResponse
from utils.pagination import StandardPagination
from .models import Order, OrderItem, ReturnRequest, Cart, CartItem
from .serializers import (
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    OrderUpdateSerializer, OrderShipSerializer,
    ReturnRequestListSerializer, ReturnRequestDetailSerializer,
    ReturnRequestCreateSerializer, ReturnRequestProcessSerializer,
    CartSerializer, CartItemSerializer, CartItemCreateSerializer, CartItemUpdateSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    订单视图集

    提供订单的 CRUD 操作：
    - list: 获取订单列表
    - retrieve: 获取订单详情
    - create: 创建订单
    - update: 更新订单
    - destroy: 删除订单
    """

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'created_at': ['gte', 'lte', 'exact'],
    }
    ordering_fields = ['created_at', 'pay_amount', 'total_amount']
    ordering = ['-created_at']

    def get_queryset(self):
        """获取查询集"""
        user = self.request.user
        # 普通用户只能查看自己的订单
        if not user.is_staff and not user.is_superuser:
            return Order.objects.filter(user=user)
        return Order.objects.select_related('user', 'coupon').all()

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return OrderListSerializer
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderDetailSerializer

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """详情查询"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建订单"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(
                data=OrderDetailSerializer(serializer.instance).data,
                message='订单创建成功',
                code=201
            )
        return ApiResponse.error(message='订单创建失败', errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """更新订单"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='订单更新成功')
        return ApiResponse.error(message='订单更新失败', errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """删除订单"""
        instance = self.get_object()
        # 只有待付款和已取消的订单可以删除
        if instance.status not in [Order.Status.PENDING_PAYMENT, Order.Status.CANCELLED]:
            return ApiResponse.error(message='当前状态不允许删除订单')
        instance.delete()
        return ApiResponse.success(message='订单删除成功')

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """
        取消订单

        只有待付款和待发货的订单可以取消
        """
        order = self.get_object()

        if order.status not in [Order.Status.PENDING_PAYMENT, Order.Status.PENDING_SHIPMENT]:
            return ApiResponse.error(message='当前状态不允许取消订单')

        order.status = Order.Status.CANCELLED
        order.save()

        serializer = OrderDetailSerializer(order)
        return ApiResponse.success(data=serializer.data, message='订单已取消')

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        """
        确认收货

        只有已发货的订单可以确认收货
        """
        order = self.get_object()

        if order.status != Order.Status.SHIPPED:
            return ApiResponse.error(message='当前状态不允许确认收货')

        order.status = Order.Status.COMPLETED
        order.completed_at = timezone.now()
        order.save()

        serializer = OrderDetailSerializer(order)
        return ApiResponse.success(data=serializer.data, message='确认收货成功')

    @action(detail=True, methods=['post'], url_path='ship')
    def ship(self, request, pk=None):
        """
        订单发货（管理员操作）

        请求参数：
        - express_company: 物流公司
        - tracking_number: 物流单号
        """
        order = self.get_object()

        if order.status != Order.Status.PENDING_SHIPMENT:
            return ApiResponse.error(message='当前状态不允许发货')

        serializer = OrderShipSerializer(data=request.data)
        if serializer.is_valid():
            order.express_company = serializer.validated_data['express_company']
            order.tracking_number = serializer.validated_data['tracking_number']
            order.status = Order.Status.SHIPPED
            order.shipped_at = timezone.now()
            order.save()

            result_serializer = OrderDetailSerializer(order)
            return ApiResponse.success(data=result_serializer.data, message='订单发货成功')
        return ApiResponse.error(message='参数验证失败', errors=serializer.errors)

    @action(detail=False, methods=['get'], url_path='my-orders')
    def my_orders(self, request):
        """
        我的订单

        查询参数：
        - status: 订单状态筛选（可选）
        """
        queryset = self.get_queryset()

        # 可选筛选
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        queryset = queryset.order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderListSerializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = OrderListSerializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    @action(detail=True, methods=['post'], url_path='return')
    def return_order(self, request, pk=None):
        """
        申请退换货

        从订单直接申请退换货，自动关联订单信息

        请求参数：
        - request_type: 申请类型 (return/refund)
        - reason: 原因描述
        - evidence_images: 凭证图片列表（可选）
        """
        order = self.get_object()

        # 只有已完成的订单可以申请退换货
        if order.status != Order.Status.COMPLETED:
            return ApiResponse.error(message='只有已完成订单可以申请退换货')

        # 检查是否已有待处理的退换货申请
        existing_return = ReturnRequest.objects.filter(
            order=order,
            status__in=[ReturnRequest.Status.PENDING, ReturnRequest.Status.APPROVED]
        ).first()
        if existing_return:
            return ApiResponse.error(message='该订单已有退换货申请正在处理中')

        # 创建退换货申请
        data = request.data.copy()
        data['order'] = order.id

        serializer = ReturnRequestCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(order=order)
            return ApiResponse.success(
                data=ReturnRequestDetailSerializer(serializer.instance).data,
                message='退换货申请提交成功',
                code=201
            )
        return ApiResponse.error(message='申请提交失败', errors=serializer.errors)


class ReturnRequestViewSet(viewsets.ModelViewSet):
    """
    退换货申请视图集

    提供退换货申请的 CRUD 操作：
    - list: 获取退换货申请列表
    - retrieve: 获取退换货申请详情
    - create: 创建退换货申请
    - update: 更新退换货申请（管理员）
    """

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'request_type': ['exact'],
        'created_at': ['gte', 'lte', 'exact'],
    }
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """获取查询集"""
        user = self.request.user
        # 普通用户只能查看自己的申请
        if not user.is_staff and not user.is_superuser:
            return ReturnRequest.objects.filter(order__user=user).select_related('order')
        return ReturnRequest.objects.select_related('order', 'order__user').all()

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return ReturnRequestListSerializer
        if self.action == 'create':
            return ReturnRequestCreateSerializer
        return ReturnRequestDetailSerializer

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """详情查询"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建退换货申请"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(
                data=ReturnRequestDetailSerializer(serializer.instance).data,
                message='退换货申请提交成功',
                code=201
            )
        return ApiResponse.error(message='申请提交失败', errors=serializer.errors)

    @action(detail=True, methods=['post'], url_path='process')
    def process(self, request, pk=None):
        """
        处理退换货申请（管理员操作）

        请求参数：
        - status: 处理状态 (approved/rejected/completed)
        - admin_note: 处理意见
        """
        return_request = self.get_object()

        if return_request.status != ReturnRequest.Status.PENDING:
            return ApiResponse.error(message='该申请已被处理')

        serializer = ReturnRequestProcessSerializer(data=request.data)
        if serializer.is_valid():
            return_request.status = serializer.validated_data['status']
            return_request.admin_note = serializer.validated_data.get('admin_note', '')
            return_request.processed_at = timezone.now()
            return_request.save()

            result_serializer = ReturnRequestDetailSerializer(return_request)
            return ApiResponse.success(data=result_serializer.data, message='退换货申请处理成功')
        return ApiResponse.error(message='参数验证失败', errors=serializer.errors)


class CartViewSet(viewsets.ViewSet):
    """
    购物车视图集

    提供购物车的操作：
    - GET /api/orders/cart/ - 获取购物车
    - POST /api/orders/cart/items/ - 添加商品
    - PUT /api/orders/cart/items/{id}/ - 更新数量
    - DELETE /api/orders/cart/items/{id}/ - 删除商品
    - DELETE /api/orders/cart/items/ - 清空购物车
    """

    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """获取或创建用户的购物车"""
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        """
        获取购物车

        返回购物车信息及所有商品列表
        """
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return ApiResponse.success(data=serializer.data, message='获取购物车成功')

    @action(detail=False, methods=['post'], url_path='items')
    def add_item(self, request):
        """
        添加商品到购物车

        请求参数：
        - product: 商品ID
        - quantity: 数量（可选，默认为1）
        """
        serializer = CartItemCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(message='参数验证失败', errors=serializer.errors)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart = self.get_cart(request.user)

        # 检查商品是否已在购物车中
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            # 更新数量
            new_quantity = cart_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return ApiResponse.error(message=f'商品库存不足，最多可添加{product.stock_quantity}件')
            cart_item.quantity = new_quantity
            cart_item.save()
            message = '购物车商品数量已更新'
        except CartItem.DoesNotExist:
            # 添加新商品
            if product.stock_quantity < quantity:
                return ApiResponse.error(message=f'商品库存不足，最多可添加{product.stock_quantity}件')
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                product_name=product.name,
                product_image=product.main_image or '',
                price=product.price,
                quantity=quantity
            )
            message = '商品已添加到购物车'

        # 更新购物车统计
        cart.update_totals()

        result_serializer = CartItemSerializer(cart_item)
        return ApiResponse.success(data=result_serializer.data, message=message)

    @action(detail=False, methods=['put', 'patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """
        更新购物车商品数量

        URL参数：
        - item_id: 购物车商品ID

        请求参数：
        - quantity: 新的数量
        """
        serializer = CartItemUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(message='参数验证失败', errors=serializer.errors)

        quantity = serializer.validated_data['quantity']

        cart = self.get_cart(request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
        except CartItem.DoesNotExist:
            return ApiResponse.error(message='购物车商品不存在')

        # 检查库存
        if cart_item.product.stock_quantity < quantity:
            return ApiResponse.error(message=f'商品库存不足，最多可设置{cart_item.product.stock_quantity}件')

        cart_item.quantity = quantity
        cart_item.save()

        # 更新购物车统计
        cart.update_totals()

        result_serializer = CartItemSerializer(cart_item)
        return ApiResponse.success(data=result_serializer.data, message='商品数量已更新')

    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """
        删除购物车商品

        URL参数：
        - item_id: 购物车商品ID
        """
        cart = self.get_cart(request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
        except CartItem.DoesNotExist:
            return ApiResponse.error(message='购物车商品不存在')

        cart_item.delete()

        # 更新购物车统计
        cart.update_totals()

        return ApiResponse.success(message='商品已从购物车删除')

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        """
        清空购物车

        删除购物车中的所有商品
        """
        cart = self.get_cart(request.user)

        # 删除所有购物车商品
        CartItem.objects.filter(cart=cart).delete()

        # 更新购物车统计
        cart.update_totals()

        return ApiResponse.success(message='购物车已清空')

    @action(detail=False, methods=['get'], url_path='count')
    def cart_count(self, request):
        """
        获取购物车商品数量

        返回购物车中商品的总数量
        """
        cart = self.get_cart(request.user)
        return ApiResponse.success(data={'count': cart.total_items})
