from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def success_response(data=None, message="操作成功", total=None, status_code=status.HTTP_200_OK):
    payload = {
        "code": 0,
        "message": message,
        "data": data,
    }
    if total is not None:
        payload["total"] = total
    return Response(payload, status=status_code)


def error_response(message="操作失败", code=1, data=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "code": code,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def _extract_error_message(detail):
    if isinstance(detail, list) and detail:
        return _extract_error_message(detail[0])

    if isinstance(detail, dict) and detail:
        if "detail" in detail:
            return _extract_error_message(detail["detail"])
        first_value = next(iter(detail.values()))
        return _extract_error_message(first_value)

    return str(detail) if detail else "请求失败"


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        if isinstance(exc, DjangoValidationError):
            return error_response(
                message=_extract_error_message(getattr(exc, "messages", str(exc))),
            )
        return error_response(
            message="服务器内部错误",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response.data = {
        "code": 1,
        "message": _extract_error_message(response.data),
        "data": None,
    }
    return response
