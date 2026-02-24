from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import UserRole
from apps.system.models import Bill, BillStatus, Notice, NoticeTargetRole, OperationLog, RechargeRecord
from apps.system.serializers import (
    AdminNoticeSerializer,
    BillSerializer,
    OperationLogSerializer,
    ProfileAlarmSubscriptionSerializer,
    ProfileBindRoomsSerializer,
    ProfileSerializer,
    RechargeRecordSerializer,
    RechargeSimulateSerializer,
    ResetPasswordSerializer,
    RoleSerializer,
    UserManagementSerializer,
    UserNoticeSerializer,
    _ensure_profile,
)
from energy_monitoring.permissions import IsAdmin, IsOwnerOrAdmin, is_admin_user


User = get_user_model()

SimpleMessageSerializer = inline_serializer(
    name="SimpleMessage",
    fields={
        "message": serializers.CharField(),
    },
)
BindRoomsResponseSerializer = inline_serializer(
    name="BindRoomsResponse",
    fields={
        "bind_rooms": serializers.ListField(child=serializers.IntegerField()),
    },
)
RechargeSimulateResponseSerializer = inline_serializer(
    name="RechargeSimulateResponse",
    fields={
        "record": RechargeRecordSerializer(),
        "paid_bill_ids": serializers.ListField(child=serializers.IntegerField()),
        "paid_bill_count": serializers.IntegerField(),
        "remaining_amount": serializers.CharField(),
    },
)


def _client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _write_operation_log(request, action_name, resource):
    OperationLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action_name,
        resource=resource,
        ip_address=_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
        request_method=request.method,
        request_path=request.path,
    )


def _bound_room_ids(user):
    profile = _ensure_profile(user)
    return [int(item) for item in profile.bind_rooms if str(item).isdigit()]


@extend_schema_view(
    list=extend_schema(summary="获取用户列表"),
    retrieve=extend_schema(summary="获取用户详情"),
    create=extend_schema(summary="创建用户"),
    update=extend_schema(summary="更新用户"),
    partial_update=extend_schema(summary="部分更新用户"),
    destroy=extend_schema(summary="删除用户"),
)
class UserViewSet(viewsets.ModelViewSet):
    """管理员用户管理接口。"""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserManagementSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["id", "username", "is_active", "date_joined"]
    ordering = ["id"]

    def perform_create(self, serializer):
        user = serializer.save()
        _write_operation_log(self.request, "create_user", f"user:{user.id}")

    def perform_update(self, serializer):
        user = serializer.save()
        _write_operation_log(self.request, "update_user", f"user:{user.id}")

    def perform_destroy(self, instance):
        user_id = instance.id
        super().perform_destroy(instance)
        _write_operation_log(self.request, "delete_user", f"user:{user_id}")

    @action(detail=True, methods=["post"], url_path="reset-password")
    @extend_schema(
        summary="重置用户密码",
        request=ResetPasswordSerializer,
        responses={200: SimpleMessageSerializer},
    )
    def reset_password(self, request, pk=None):
        """重置指定用户密码。"""
        target_user = self.get_object()
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user.set_password(serializer.validated_data["new_password"])
        target_user.save(update_fields=["password"])
        _write_operation_log(request, "reset_password", f"user:{target_user.id}")
        return Response({"message": "密码重置成功。"})


@extend_schema_view(
    list=extend_schema(summary="获取角色列表"),
    retrieve=extend_schema(summary="获取角色详情"),
    create=extend_schema(summary="创建角色"),
    update=extend_schema(summary="更新角色"),
    partial_update=extend_schema(summary="部分更新角色"),
    destroy=extend_schema(summary="删除角色"),
)
class RoleViewSet(viewsets.ModelViewSet):
    """角色管理接口。"""

    queryset = Group.objects.all().order_by("id")
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    ordering = ["id"]

    def perform_create(self, serializer):
        role = serializer.save(name=str(serializer.validated_data["name"]).strip().upper())
        _write_operation_log(self.request, "create_role", f"role:{role.id}")

    def perform_update(self, serializer):
        role = serializer.save(name=str(serializer.validated_data["name"]).strip().upper())
        _write_operation_log(self.request, "update_role", f"role:{role.id}")

    def perform_destroy(self, instance):
        role_id = instance.id
        super().perform_destroy(instance)
        _write_operation_log(self.request, "delete_role", f"role:{role_id}")


@extend_schema_view(
    list=extend_schema(summary="获取账单列表"),
)
class BillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """账单查询接口（管理员全量、用户个人）。"""

    queryset = Bill.objects.select_related("room", "room__floor__building", "energy_type").all()
    serializer_class = BillSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["room__room_number", "room__floor__building__name", "bill_period"]
    ordering_fields = ["id", "bill_period", "amount", "status", "due_date", "created_at"]
    ordering = ["-bill_period", "-id"]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value:
            queryset = queryset.filter(status=str(status_value).strip().upper())
        room_id = self.request.query_params.get("room_id")
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        energy_type = self.request.query_params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                queryset = queryset.filter(energy_type_id=int(energy_type))
            else:
                queryset = queryset.filter(energy_type__code__iexact=str(energy_type).strip())
        return queryset

    @action(detail=False, methods=["get"], url_path="my", permission_classes=[IsAuthenticated])
    @extend_schema(
        summary="获取当前用户账单列表",
        responses={200: BillSerializer(many=True)},
    )
    def my(self, request):
        """返回当前用户已绑定房间的账单。"""
        room_ids = _bound_room_ids(request.user)
        queryset = Bill.objects.select_related("room", "room__floor__building", "energy_type").filter(
            room_id__in=room_ids
        )
        status_value = request.query_params.get("status")
        if status_value:
            queryset = queryset.filter(status=str(status_value).strip().upper())
        queryset = queryset.order_by("-bill_period", "-id")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BillSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = BillSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="获取通知公告列表"),
    retrieve=extend_schema(summary="获取通知公告详情"),
)
class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    """用户可见通知公告只读接口。"""

    queryset = Notice.objects.select_related("publisher").all().order_by("-publish_time", "-id")
    serializer_class = UserNoticeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["id", "publish_time", "priority", "created_at"]
    ordering = ["-publish_time", "-id"]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        now = timezone.now()
        queryset = queryset.filter(Q(publish_time__lte=now) | Q(publish_time__isnull=True))
        profile = _ensure_profile(self.request.user)
        if profile.role == UserRole.ADMIN:
            return queryset
        return queryset.filter(target_role__in=[NoticeTargetRole.ALL, NoticeTargetRole.USER])


@extend_schema_view(
    list=extend_schema(summary="管理员获取公告列表"),
    retrieve=extend_schema(summary="管理员获取公告详情"),
    create=extend_schema(summary="管理员创建公告"),
    update=extend_schema(summary="管理员更新公告"),
    partial_update=extend_schema(summary="管理员部分更新公告"),
    destroy=extend_schema(summary="管理员删除公告"),
)
class AdminNoticeViewSet(viewsets.ModelViewSet):
    """管理员通知公告管理接口。"""

    queryset = Notice.objects.select_related("publisher").all().order_by("-created_at", "-id")
    serializer_class = AdminNoticeSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["id", "publish_time", "priority", "is_published", "created_at"]
    ordering = ["-created_at", "-id"]

    def perform_create(self, serializer):
        publish_time = serializer.validated_data.get("publish_time")
        is_published = serializer.validated_data.get("is_published", False)
        if is_published and publish_time is None:
            publish_time = timezone.now()
        notice = serializer.save(publisher=self.request.user, publish_time=publish_time)
        _write_operation_log(self.request, "create_notice", f"notice:{notice.id}")

    def perform_update(self, serializer):
        publish_time = serializer.validated_data.get("publish_time")
        is_published = serializer.validated_data.get("is_published")
        instance = serializer.instance
        if is_published is True and publish_time is None and instance.publish_time is None:
            publish_time = timezone.now()
        notice = serializer.save(publish_time=publish_time if publish_time is not None else instance.publish_time)
        _write_operation_log(self.request, "update_notice", f"notice:{notice.id}")

    def perform_destroy(self, instance):
        notice_id = instance.id
        super().perform_destroy(instance)
        _write_operation_log(self.request, "delete_notice", f"notice:{notice_id}")


@extend_schema_view(
    list=extend_schema(summary="获取操作日志列表"),
)
class OperationLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """操作日志只读列表接口。"""

    queryset = OperationLog.objects.select_related("user").all().order_by("-create_time", "-id")
    serializer_class = OperationLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["action", "resource", "request_path", "ip_address", "user__username"]
    ordering_fields = ["id", "create_time", "action"]
    ordering = ["-create_time", "-id"]
    http_method_names = ["get", "head", "options"]


@extend_schema_view(
    list=extend_schema(summary="获取充值记录列表"),
)
class RechargeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """充值记录查询与模拟充值接口。"""

    queryset = RechargeRecord.objects.select_related("room", "room__floor__building", "operator").all()
    serializer_class = RechargeRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["room__room_number", "room__floor__building__name", "remark"]
    ordering_fields = ["id", "recharge_time", "amount", "created_at"]
    ordering = ["-recharge_time", "-id"]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not is_admin_user(self.request.user):
            queryset = queryset.filter(room_id__in=_bound_room_ids(self.request.user))

        room_id = self.request.query_params.get("room_id")
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset

    @action(detail=False, methods=["post"], url_path="simulate")
    @extend_schema(
        summary="模拟充值并自动冲抵账单",
        request=RechargeSimulateSerializer,
        responses={
            200: RechargeSimulateResponseSerializer,
            403: OpenApiResponse(description="用户无权限操作该房间"),
        },
    )
    def simulate(self, request):
        """创建模拟充值记录，并按到期顺序结清账单。"""
        serializer = RechargeSimulateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_id = serializer.validated_data["room_id"]
        amount = Decimal(serializer.validated_data["amount"])

        if not is_admin_user(request.user) and room_id not in _bound_room_ids(request.user):
            return Response(
                {"message": "只能为已绑定房间进行充值。"},
                status=status.HTTP_403_FORBIDDEN,
            )

        now = timezone.now()
        payment_method = serializer.validated_data.get("payment_method") or "SIMULATED"
        remark = serializer.validated_data.get("remark", "")

        with transaction.atomic():
            record = RechargeRecord.objects.create(
                room_id=room_id,
                amount=amount,
                payment_method=payment_method,
                recharge_time=now,
                operator=request.user,
                remark=remark,
            )

            remaining = amount
            paid_bill_ids = []
            unpaid_bills = (
                Bill.objects.select_for_update()
                .filter(room_id=room_id, status=BillStatus.UNPAID)
                .order_by("due_date", "bill_period", "id")
            )
            for bill in unpaid_bills:
                bill_amount = Decimal(bill.amount or 0)
                if bill_amount <= 0:
                    bill.status = BillStatus.PAID
                    bill.paid_time = now
                    bill.save(update_fields=["status", "paid_time", "updated_at"])
                    paid_bill_ids.append(bill.id)
                    continue
                if remaining < bill_amount:
                    continue
                remaining -= bill_amount
                bill.status = BillStatus.PAID
                bill.paid_time = now
                bill.save(update_fields=["status", "paid_time", "updated_at"])
                paid_bill_ids.append(bill.id)

        _write_operation_log(request, "simulate_recharge", f"room:{room_id}")
        return Response(
            {
                "record": RechargeRecordSerializer(record).data,
                "paid_bill_ids": paid_bill_ids,
                "paid_bill_count": len(paid_bill_ids),
                "remaining_amount": f"{remaining:.2f}",
            }
        )


class ProfileViewSet(viewsets.GenericViewSet):
    """个人中心接口。"""

    queryset = User.objects.none()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = ProfileSerializer

    def _profile_object(self):
        profile = _ensure_profile(self.request.user)
        self.check_object_permissions(self.request, profile)
        return profile

    @extend_schema(
        summary="获取当前用户个人资料",
        responses={200: ProfileSerializer},
    )
    def retrieve_profile(self, request):
        """返回当前登录用户的资料与订阅配置。"""
        self._profile_object()
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="更新当前用户个人资料",
        request=ProfileSerializer,
        responses={200: ProfileSerializer},
    )
    def update_profile(self, request):
        """更新当前登录用户的基础资料。"""
        self._profile_object()
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        _write_operation_log(request, "update_profile", f"user:{request.user.id}")
        return Response(ProfileSerializer(request.user).data)

    @action(detail=False, methods=["post", "delete"], url_path="bind-rooms")
    @extend_schema(
        summary="绑定或解绑房间",
        request=ProfileBindRoomsSerializer,
        responses={200: BindRoomsResponseSerializer},
    )
    def bind_rooms(self, request):
        """POST 绑定房间；DELETE 解绑房间。"""
        profile = self._profile_object()
        serializer = ProfileBindRoomsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_ids = serializer.validated_data["room_ids"]
        current_room_ids = sorted(set(int(item) for item in profile.bind_rooms if str(item).isdigit()))
        current_room_id_set = set(current_room_ids)

        if request.method.lower() == "post":
            updated = sorted(current_room_id_set.union(room_ids))
            action_name = "bind_rooms"
        else:
            updated = sorted(current_room_id_set.difference(room_ids))
            action_name = "unbind_rooms"

        profile.bind_rooms = updated
        profile.save(update_fields=["bind_rooms", "updated_at"])
        _write_operation_log(request, action_name, f"user:{request.user.id}")
        return Response({"bind_rooms": updated})

    @action(detail=False, methods=["get", "put"], url_path="alarm-subscriptions")
    @extend_schema(
        summary="查询或更新告警订阅",
        request=ProfileAlarmSubscriptionSerializer,
        responses={200: ProfileAlarmSubscriptionSerializer},
    )
    def alarm_subscriptions(self, request):
        """GET 查询订阅；PUT 更新订阅开关。"""
        profile = self._profile_object()
        if request.method.lower() == "get":
            return Response(ProfileAlarmSubscriptionSerializer(profile.alarm_subscriptions).data)

        serializer = ProfileAlarmSubscriptionSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = ProfileAlarmSubscriptionSerializer(profile.alarm_subscriptions).data
        updated.update(serializer.validated_data)
        profile.alarm_subscriptions = updated
        profile.save(update_fields=["alarm_subscriptions", "updated_at"])
        _write_operation_log(request, "update_alarm_subscriptions", f"user:{request.user.id}")
        return Response(ProfileAlarmSubscriptionSerializer(updated).data)
