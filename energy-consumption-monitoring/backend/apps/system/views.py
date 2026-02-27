from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import UserProfile, UserRole
from apps.buildings.models import Room
from apps.system.models import Notice, NoticeTargetRole, NoticeType, OperationLog
from apps.system.serializers import (
    AdminNoticeSerializer,
    AdminTipSerializer,
    OperationLogSerializer,
    ProfileAlarmSubscriptionSerializer,
    ProfileBindRoomsSerializer,
    ProfileSerializer,
    ResetPasswordSerializer,
    RoleSerializer,
    TipSerializer,
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


class TipsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """节能知识只读接口。"""

    queryset = Notice.objects.select_related("publisher").all().order_by("-publish_time", "-id")
    serializer_class = TipSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(
                notice_type=NoticeType.KNOWLEDGE,
                is_published=True,
            )
        )
        now = timezone.now()
        queryset = queryset.filter(Q(publish_time__lte=now) | Q(publish_time__isnull=True))
        profile = _ensure_profile(self.request.user)
        if profile.role != UserRole.ADMIN:
            queryset = queryset.filter(target_role__in=[NoticeTargetRole.ALL, NoticeTargetRole.USER])
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__iexact=str(category).strip())
        limit = self.request.query_params.get("limit")
        if limit and str(limit).isdigit():
            queryset = queryset[: int(limit)]
        return queryset


@extend_schema_view(
    list=extend_schema(summary="管理员获取节能知识列表"),
    retrieve=extend_schema(summary="管理员获取节能知识详情"),
    create=extend_schema(summary="管理员创建节能知识"),
    update=extend_schema(summary="管理员更新节能知识"),
    partial_update=extend_schema(summary="管理员部分更新节能知识"),
    destroy=extend_schema(summary="管理员删除节能知识"),
)
class AdminTipsViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.filter(notice_type=NoticeType.KNOWLEDGE).order_by("-created_at", "-id")
    serializer_class = AdminTipSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "category"]
    ordering_fields = ["id", "publish_time", "is_published", "created_at"]
    ordering = ["-created_at", "-id"]

    def perform_create(self, serializer):
        publish_time = serializer.validated_data.get("publish_time")
        is_published = serializer.validated_data.get("is_published", False)
        if is_published and publish_time is None:
            publish_time = timezone.now()
        tip = serializer.save(
            publisher=self.request.user,
            publish_time=publish_time,
            notice_type=NoticeType.KNOWLEDGE,
        )
        _write_operation_log(self.request, "create_tip", f"notice:{tip.id}")

    def perform_update(self, serializer):
        publish_time = serializer.validated_data.get("publish_time")
        is_published = serializer.validated_data.get("is_published")
        instance = serializer.instance
        if is_published is True and publish_time is None and instance.publish_time is None:
            publish_time = timezone.now()
        tip = serializer.save(
            publish_time=publish_time if publish_time is not None else instance.publish_time,
            notice_type=NoticeType.KNOWLEDGE,
        )
        _write_operation_log(self.request, "update_tip", f"notice:{tip.id}")

    def perform_destroy(self, instance):
        tip_id = instance.id
        super().perform_destroy(instance)
        _write_operation_log(self.request, "delete_tip", f"notice:{tip_id}")


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

    @action(detail=False, methods=["get"], url_path="balance")
    @extend_schema(
        summary="获取账户余额",
        responses={200: OpenApiResponse(description="账户余额")},
    )
    def balance(self, request):
        profile = self._profile_object()
        return Response(
            {
                "balance": f"{Decimal(profile.balance or 0):.2f}",
                "currency": "CNY",
            }
        )

    @action(detail=False, methods=["get", "post", "delete"], url_path="bind-rooms")
    @extend_schema(
        summary="绑定或解绑房间",
        request=ProfileBindRoomsSerializer,
        responses={200: BindRoomsResponseSerializer},
    )
    def bind_rooms(self, request):
        """POST 绑定房间；DELETE 解绑房间。"""
        profile = self._profile_object()
        if request.method.lower() == "get":
            current_room_ids = sorted(set(int(item) for item in profile.bind_rooms if str(item).isdigit()))
            if not current_room_ids:
                return Response([])
            room_map = {
                room.id: room
                for room in Room.objects.select_related("floor", "floor__building").filter(id__in=current_room_ids)
            }
            rooms = []
            for room_id in current_room_ids:
                room = room_map.get(room_id)
                if room is None:
                    continue
                rooms.append(
                    {
                        "id": room.id,
                        "room_number": room.room_number,
                        "name": room.room_number,
                        "building_name": room.floor.building.name,
                        "building": room.floor.building.name,
                        "floor_name": room.floor.name,
                        "floor": room.floor.name,
                        "department": room.department,
                    }
                )
            return Response(rooms)
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
