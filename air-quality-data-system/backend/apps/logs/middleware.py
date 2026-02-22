from __future__ import annotations

import traceback

from apps.logs.models import ErrorLog
from apps.logs.services import create_operation_log


class AdminOperationAndErrorLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as exc:
            self._log_exception(exc)
            raise

        self._log_operation(request, response)
        return response

    def _log_operation(self, request, response):
        if getattr(request, "_operation_logged", False):
            return
        if not request.path.startswith("/api/admin/"):
            return
        if request.method not in {"POST", "PUT", "PATCH", "DELETE"}:
            return
        if response.status_code >= 400:
            return

        user = getattr(request, "user", None) or getattr(request, "_force_auth_user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return

        try:
            body_text = request.body.decode("utf-8", errors="ignore")
        except Exception:
            body_text = ""
        if len(body_text) > 2000:
            body_text = f"{body_text[:2000]}..."

        create_operation_log(
            request,
            operation_type=f"{request.method} {request.path}",
            operation_content=body_text,
            user=user,
        )

    @staticmethod
    def _log_exception(exc: Exception):
        try:
            ErrorLog.objects.create(
                error_type=exc.__class__.__name__,
                error_message=str(exc),
                stack_trace=traceback.format_exc(),
            )
        except Exception:
            # Avoid recursive errors during exception handling.
            return
