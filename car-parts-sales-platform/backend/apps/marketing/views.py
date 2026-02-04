"""
营销管理视图

包含优惠券、用户优惠券等视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.db import transaction
from django.db.models import F

from utils.response import ApiResponse
from utils.pagination import StandardPagination
from .models import Coupon, UserCoupon
from .serializers import (
    CouponSerializer,
    CouponListSerializer,
    UserCouponSerializer,
    UserCouponListSerializer,
)


class CouponViewSet(viewsets.ModelViewSet):
    """
    优惠券管理 ViewSet

    list: 获取优惠券列表（只显示启用的）
    retrieve: 获取优惠券详情
    create: 创建优惠券（管理员）
    update: 更新优惠券（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除优惠券（管理员）
    claim: 领取优惠券
    my-coupons: 获取当前用户的优惠券
    """
    queryset = Coupon.objects.all()
    pagination_class = StandardPagination
    filter_backends = []  # 优惠券列表不需要复杂过滤
    permission_classes = [AllowAny]  # 允许匿名查看优惠券列表

    def get_queryset(self):
        """普通用户只看启用的有效优惠券"""
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'claim']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return CouponListSerializer
        return CouponSerializer

    def list(self, request, *args, **kwargs):
        """获取优惠券列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取优惠券详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建优惠券"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新优惠券"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除优惠券"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        """
        领取优惠券

        业务逻辑：
        1. 检查优惠券是否存在且有效
        2. 检查是否在有效期内
        3. 检查是否还有剩余数量
        4. 检查用户是否超过限领数量
        5. 记录领取信息并增加已发放数量
        """
        coupon = self.get_object()

        # 检查优惠券是否启用
        if not coupon.is_active:
            return ApiResponse.error(message='优惠券已停用', code=400)

        # 检查是否在有效期内
        now = timezone.now()
        if now < coupon.valid_from:
            return ApiResponse.error(message='优惠券尚未开始', code=400)
        if now > coupon.valid_until:
            return ApiResponse.error(message='优惠券已过期', code=400)

        # 检查剩余数量
        if coupon.total_quantity > 0 and coupon.issued_quantity >= coupon.total_quantity:
            return ApiResponse.error(message='优惠券已领完', code=400)

        # 检查用户已领取数量
        user = request.user
        user_coupon_count = UserCoupon.objects.filter(
            user=user,
            coupon=coupon,
            status='unused'
        ).count()

        if user_coupon_count >= coupon.per_user_limit:
            return ApiResponse.error(message='您已达到该优惠券的领取上限', code=400)

        # 使用事务确保数据一致性
        with transaction.atomic():
            # 再次检查剩余数量（防止并发超领）
            if coupon.total_quantity > 0:
                updated = Coupon.objects.filter(
                    id=coupon.id,
                    issued_quantity__lt=F('total_quantity')
                ).update(issued_quantity=F('issued_quantity') + 1)

                if not updated:
                    return ApiResponse.error(message='优惠券已领完', code=400)

            # 创建用户优惠券记录
            user_coupon = UserCoupon.objects.create(
                user=user,
                coupon=coupon,
                status='unused'
            )

        return ApiResponse.success(
            message='领取成功',
            data=UserCouponSerializer(user_coupon).data,
            code=201
        )

    @action(detail=False, methods=['get'], url_path='my-coupons')
    def my_coupons(self, request):
        """
        获取当前用户的优惠券

        查询参数：
        - status: 状态筛选（unused/used/expired）
        """
        user = request.user
        queryset = UserCoupon.objects.filter(user=user)

        # 按状态筛选
        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        # 按有效期排序
        queryset = queryset.order_by('-obtained_at')

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserCouponListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserCouponListSerializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)


class UserCouponViewSet(viewsets.ModelViewSet):
    """
    用户优惠券管理 ViewSet

    list: 获取用户优惠券列表（管理员）
    retrieve: 获取用户优惠券详情
    """
    queryset = UserCoupon.objects.all()
    pagination_class = StandardPagination
    serializer_class = UserCouponSerializer
    filter_backends = []

    def get_queryset(self):
        """管理员可以查看所有用户的优惠券"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # 非管理员只能看自己的
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        """获取用户优惠券列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取用户优惠券详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)
