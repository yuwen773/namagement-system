from __future__ import annotations

from datetime import datetime
from typing import TypedDict

from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminUser
from apps.logs.models import ErrorLog, OperationLog
from apps.logs.serializers import ErrorLogSerializer, OperationLogSerializer
from utils.exception_handler import ValidationError
from utils.response import APIResponse


class SystemLogItem(TypedDict):
    id: int
    level: str
    module: str
    timestamp: str
    message: str
    username: str | None
    ip_address: str | None
    extra_data: dict | None


def _parse_int_query_param(request, field: str, default: int, min_value: int, max_value: int) -> int:
    raw_value = request.query_params.get(field, str(default))
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        raise ValidationError(f"格式错误，应为整数，范围 {min_value}-{max_value}", field=field)
    if value < min_value or value > max_value:
        raise ValidationError(f"超出范围，应为 {min_value}-{max_value}", field=field)
    return value


def _parse_int_value(value, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError("格式错误，应为整数", field=field)


def _get_optional_date_query_param(request, field: str):
    raw_value = request.query_params.get(field)
    if not raw_value:
        return None
    try:
        return datetime.strptime(raw_value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("格式错误，应为 YYYY-MM-DD", field=field)


@extend_schema_view(
    get=extend_schema(
        tags=["Admin - Logs"],
        summary="查询操作日志",
        description="管理员分页查询操作日志，支持用户、操作类型和日期区间过滤。",
        responses=OpenApiTypes.OBJECT,
    )
)
class OperationLogListView(APIView):
    """Admin endpoint for operation log query with date/user/type filters."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = OperationLog.objects.select_related("user").all()

        user_id = request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=_parse_int_value(user_id, field="user_id"))

        operation_type = (request.query_params.get("operation_type") or "").strip()
        if operation_type:
            queryset = queryset.filter(operation_type=operation_type)

        start_date = _get_optional_date_query_param(request, "start_date")
        end_date = _get_optional_date_query_param(request, "end_date")
        if start_date:
            queryset = queryset.filter(operation_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(operation_time__date__lte=end_date)

        page = _parse_int_query_param(request, "page", 1, 1, 100_000)
        page_size = _parse_int_query_param(request, "page_size", 20, 1, 200)

        queryset = queryset.order_by("-operation_time", "-id")
        total = queryset.count()
        items = queryset[(page - 1) * page_size : page * page_size]
        data = OperationLogSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)


@extend_schema_view(
    get=extend_schema(
        tags=["Admin - Logs"],
        summary="查询异常日志",
        description="管理员分页查询异常日志，支持异常类型和日期区间过滤。",
        responses=OpenApiTypes.OBJECT,
    )
)
class ErrorLogListView(APIView):
    """Admin endpoint for error log query with date/type filters."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = ErrorLog.objects.all()

        error_type = (request.query_params.get("error_type") or "").strip()
        if error_type:
            queryset = queryset.filter(error_type=error_type)

        start_date = _get_optional_date_query_param(request, "start_date")
        end_date = _get_optional_date_query_param(request, "end_date")
        if start_date:
            queryset = queryset.filter(occurred_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(occurred_at__date__lte=end_date)

        page = _parse_int_query_param(request, "page", 1, 1, 100_000)
        page_size = _parse_int_query_param(request, "page_size", 20, 1, 200)

        queryset = queryset.order_by("-occurred_at", "-id")
        total = queryset.count()
        items = queryset[(page - 1) * page_size : page * page_size]
        data = ErrorLogSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)


def _extract_module_from_operation_type(operation_type: str) -> str:
    """Extract module name from operation type."""
    parts = operation_type.split(".")
    return parts[0].lower() if parts else "system"


def _extract_module_from_error_type(error_type: str) -> str:
    """Extract module name from error type."""
    parts = error_type.split(".")
    return parts[0].lower() if parts else "system"


def _convert_operation_log_to_system_log(log: OperationLog) -> SystemLogItem:
    """Convert operation log to system log format."""
    return {
        "id": f"op_{log.id}",
        "level": "INFO",
        "module": _extract_module_from_operation_type(log.operation_type),
        "timestamp": log.operation_time.isoformat(),
        "message": f"{log.operation_type}: {log.operation_content}",
        "username": log.user.username,
        "ip_address": log.ip_address,
        "extra_data": {"operation_type": log.operation_type},
    }


def _convert_error_log_to_system_log(log: ErrorLog) -> SystemLogItem:
    """Convert error log to system log format."""
    return {
        "id": f"err_{log.id}",
        "level": "ERROR",
        "module": _extract_module_from_error_type(log.error_type),
        "timestamp": log.occurred_at.isoformat(),
        "message": f"{log.error_type}: {log.error_message}",
        "username": None,
        "ip_address": None,
        "extra_data": {"error_type": log.error_type, "stack_trace": log.stack_trace},
    }


@extend_schema_view(
    get=extend_schema(
        tags=["Admin - Logs"],
        summary="查询系统日志",
        description="管理员分页查询系统日志（包括操作日志和异常日志），支持级别、模块和关键词过滤。",
        responses=OpenApiTypes.OBJECT,
    )
)
class SystemLogListView(APIView):
    """Admin endpoint for unified system log query with filters."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        # Build querysets for both operation and error logs
        operation_qs = OperationLog.objects.select_related("user").all()
        error_qs = ErrorLog.objects.all()

        # Apply level filter
        level = (request.query_params.get("level") or "").strip().upper()
        if level:
            if level == "INFO":
                error_qs = error_qs.none()
            elif level == "ERROR":
                operation_qs = operation_qs.none()
            else:
                # For other levels (DEBUG, WARNING, CRITICAL), return empty
                operation_qs = operation_qs.none()
                error_qs = error_qs.none()

        # Apply module filter
        module = (request.query_params.get("module") or "").strip().lower()
        if module:
            operation_qs = [
                log for log in operation_qs if _extract_module_from_operation_type(log.operation_type) == module
            ]
            error_qs = [log for log in error_qs if _extract_module_from_error_type(log.error_type) == module]

        # Apply search filter
        search = (request.query_params.get("search") or "").strip()
        if search:
            search_lower = search.lower()
            operation_qs = [
                log for log in operation_qs
                if search_lower in log.operation_content.lower()
                or search_lower in log.operation_type.lower()
                or search_lower in log.user.username.lower()
            ]
            error_qs = [
                log for log in error_qs
                if search_lower in log.error_message.lower()
                or search_lower in log.error_type.lower()
            ]

        # Apply date range filter
        start_date = _get_optional_date_query_param(request, "start_date")
        end_date = _get_optional_date_query_param(request, "end_date")
        if start_date:
            if isinstance(operation_qs, QuerySet):
                operation_qs = operation_qs.filter(operation_time__date__gte=start_date)
            if isinstance(error_qs, QuerySet):
                error_qs = error_qs.filter(occurred_at__date__gte=start_date)
        if end_date:
            if isinstance(operation_qs, QuerySet):
                operation_qs = operation_qs.filter(operation_time__date__lte=end_date)
            if isinstance(error_qs, QuerySet):
                error_qs = error_qs.filter(occurred_at__date__lte=end_date)

        # Convert to list format
        if isinstance(operation_qs, QuerySet):
            operation_qs = list(operation_qs)
        if isinstance(error_qs, QuerySet):
            error_qs = list(error_qs)

        # Combine and sort by timestamp (descending)
        all_logs: list[SystemLogItem] = [
            *_convert_operation_logs_to_system_logs(operation_qs),
            *_convert_error_logs_to_system_logs(error_qs),
        ]
        all_logs.sort(key=lambda x: x["timestamp"], reverse=True)

        # Apply pagination
        page = _parse_int_query_param(request, "page", 1, 1, 100_000)
        page_size = _parse_int_query_param(request, "page_size", 50, 1, 200)

        total = len(all_logs)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_logs = all_logs[start_idx:end_idx]

        return APIResponse.paginate(data=paginated_logs, total=total, page=page, page_size=page_size)


def _convert_operation_logs_to_system_logs(logs: list[OperationLog] | QuerySet) -> list[SystemLogItem]:
    """Convert operation logs to system log format."""
    return [_convert_operation_log_to_system_log(log) for log in logs]


def _convert_error_logs_to_system_logs(logs: list[ErrorLog] | QuerySet) -> list[SystemLogItem]:
    """Convert error logs to system log format."""
    return [_convert_error_log_to_system_log(log) for log in logs]
