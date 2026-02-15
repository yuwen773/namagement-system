from __future__ import annotations

from datetime import datetime

from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminUser
from apps.logs.models import ErrorLog, OperationLog
from apps.logs.serializers import ErrorLogSerializer, OperationLogSerializer
from utils.exception_handler import ValidationError
from utils.response import APIResponse


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


class OperationLogListView(APIView):
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


class ErrorLogListView(APIView):
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
