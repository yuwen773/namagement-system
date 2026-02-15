from __future__ import annotations

from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.serializers import UserManageSerializer
from apps.logs.services import create_operation_log
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


def _parse_bool_query_param(request, field: str, default: bool = False) -> bool:
    raw_value = request.query_params.get(field)
    if raw_value is None:
        return default
    normalized = str(raw_value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValidationError("格式错误，应为布尔值", field=field)


def _parse_int_payload(value, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError("格式错误，应为整数", field=field)


def _raise_serializer_validation_error(errors: dict):
    first_field, first_errors = next(iter(errors.items()))
    if isinstance(first_errors, (list, tuple)) and first_errors:
        message = str(first_errors[0])
    else:
        message = str(first_errors)
    raise ValidationError(message=message, field=str(first_field))


class UserManageView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = User.objects.all()
        include_deleted = _parse_bool_query_param(request, "include_deleted", default=False)
        if not include_deleted:
            queryset = queryset.filter(is_deleted=False)

        keyword = (request.query_params.get("keyword") or "").strip()
        if keyword:
            queryset = queryset.filter(
                Q(username__icontains=keyword)
                | Q(email__icontains=keyword)
                | Q(phone__icontains=keyword)
            )

        role = (request.query_params.get("role") or "").strip()
        if role:
            queryset = queryset.filter(role=role)

        status = request.query_params.get("status")
        if status is not None:
            normalized = str(status).strip().lower()
            if normalized in {"true", "1", "yes"}:
                queryset = queryset.filter(status=True)
            elif normalized in {"false", "0", "no"}:
                queryset = queryset.filter(status=False)
            else:
                raise ValidationError("格式错误，应为布尔值", field="status")

        queryset = queryset.order_by("-date_joined", "-id")
        page = _parse_int_query_param(request, "page", 1, 1, 100_000)
        page_size = _parse_int_query_param(request, "page_size", 20, 1, 200)
        total = queryset.count()
        items = queryset[(page - 1) * page_size : page * page_size]
        data = UserManageSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)

    def put(self, request):
        user_id = _parse_int_payload(request.data.get("id"), field="id")
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return APIResponse.error(404, "用户不存在")

        allowed_fields = {"role", "status", "email", "phone"}
        update_data = {key: value for key, value in request.data.items() if key in allowed_fields}
        if not update_data:
            raise ValidationError("至少提供一个可更新字段", field="id")

        serializer = UserManageSerializer(user, data=update_data, partial=True)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        serializer.save()

        if "role" in update_data and not user.is_superuser:
            user.is_staff = user.role == User.Role.ADMIN
            user.save(update_fields=["is_staff", "is_active"])

        create_operation_log(
            request,
            operation_type="USER_UPDATE",
            operation_content=f"user_id={user.id}, fields={','.join(sorted(update_data.keys()))}",
        )
        return APIResponse.success(data=UserManageSerializer(user).data)

    def delete(self, request):
        single_id = request.data.get("id")
        id_list = request.data.get("ids")

        if single_id is None and not id_list:
            raise ValidationError("至少提供 id 或 ids", field="id")

        if single_id is not None:
            user_id = _parse_int_payload(single_id, field="id")
            updated_count = (
                User.objects.filter(id=user_id, is_deleted=False).update(
                    is_deleted=True,
                    status=False,
                    is_active=False,
                )
            )
            if updated_count == 0:
                return APIResponse.error(404, "用户不存在或已删除")
            create_operation_log(
                request,
                operation_type="USER_SOFT_DELETE",
                operation_content=f"user_id={user_id}",
            )
            return APIResponse.success(data={"deleted_count": updated_count}, message="删除成功")

        if not isinstance(id_list, list):
            raise ValidationError("格式错误，应为整数数组", field="ids")

        normalized_ids = []
        for raw in id_list:
            value = _parse_int_payload(raw, field="ids")
            if value > 0 and value not in normalized_ids:
                normalized_ids.append(value)
        if not normalized_ids:
            raise ValidationError("至少提供一个有效 id", field="ids")

        updated_count = (
            User.objects.filter(id__in=normalized_ids, is_deleted=False).update(
                is_deleted=True,
                status=False,
                is_active=False,
            )
        )
        create_operation_log(
            request,
            operation_type="USER_SOFT_DELETE_BATCH",
            operation_content=f"user_ids={normalized_ids}",
        )
        return APIResponse.success(data={"deleted_count": updated_count}, message="批量删除完成")
