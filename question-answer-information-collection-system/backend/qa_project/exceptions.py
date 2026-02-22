"""
Custom exception handler for API response format consistency.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    ValidationError as DRFValidationError,
)


def custom_exception_handler(exc, context):
    """
    Custom exception handler to ensure consistent API response format.
    Format: { "code": -1, "message": "友好中文错误信息", "data": null }

    错误信息映射：
    - AuthenticationFailed: "登录信息已过期，请重新登录"
    - NotAuthenticated: "请先登录后再访问"
    - PermissionDenied: "您没有权限执行此操作"
    - NotFound: "请求的资源不存在"
    - ValidationError: "参数校验失败"
    - 其他: "系统繁忙，请稍后重试"
    """
    response = exception_handler(exc, context)

    if response is not None:
        # 根据异常类型返回友好的中文错误信息
        message = _get_friendly_message(exc, response)

        response.data = {
            "code": -1,
            "message": message,
            "data": None,
        }

    return response


def _get_friendly_message(exc, response):
    """
    根据异常类型获取友好的中文错误信息
    """
    # AuthenticationFailed: 登录失败
    if isinstance(exc, AuthenticationFailed):
        return "用户名或密码错误"

    # NotAuthenticated: 未登录
    if isinstance(exc, NotAuthenticated):
        return "请先登录后再访问"

    # PermissionDenied: 权限不足
    if isinstance(exc, PermissionDenied):
        detail = exc.detail if hasattr(exc, 'detail') else str(exc)
        return str(detail) if detail else "您没有权限执行此操作"

    # NotFound: 资源不存在
    if isinstance(exc, NotFound):
        return "请求的资源不存在"

    # ValidationError: 参数校验失败，需要具体指出哪个字段
    if isinstance(exc, DRFValidationError):
        return _format_validation_error(exc.detail)

    # 获取默认错误信息
    if hasattr(response, "data"):
        if isinstance(response.data, dict):
            detail = response.data.get("detail", "")
            if detail:
                return str(detail)
            # 如果是字段错误，返回格式化后的信息
            return _format_validation_error(response.data)
        else:
            return str(response.data)

    return "系统繁忙，请稍后重试"


def _format_validation_error(detail):
    """
    格式化参数校验错误，明确指出哪个字段出错
    """
    if isinstance(detail, dict):
        errors = []
        for field, messages in detail.items():
            if isinstance(messages, list):
                for msg in messages:
                    errors.append(f"{field}: {msg}")
            else:
                errors.append(f"{field}: {messages}")
        return "；".join(errors) if errors else "参数校验失败"
    elif isinstance(detail, list):
        return "；".join(str(msg) for msg in detail)
    else:
        return str(detail)
