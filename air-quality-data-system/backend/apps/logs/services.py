from __future__ import annotations

from apps.logs.models import OperationLog


def get_request_ip(request) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()[:45]
    return (request.META.get("REMOTE_ADDR") or "")[:45]


def create_operation_log(request, operation_type: str, operation_content: str, user=None):
    user = user or getattr(request, "user", None) or getattr(request, "_force_auth_user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return

    OperationLog.objects.create(
        user=user,
        operation_type=str(operation_type)[:50],
        operation_content=str(operation_content)[:5000],
        ip_address=get_request_ip(request),
    )
    setattr(request, "_operation_logged", True)
