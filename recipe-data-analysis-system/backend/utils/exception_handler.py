"""
自定义异常处理器

统一处理所有异常，确保返回标准格式的响应。
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import status
from .response import ApiResponse


def custom_exception_handler(exc, context):
    """
    自定义异常处理器

    将所有异常转换为统一的响应格式：
    {"code": xxx, "message": "xxx", "data": null}

    Args:
        exc: 异常实例
        context: 上下文信息

    Returns:
        Response: 标准格式的响应
    """
    # 先调用 DRF 默认的异常处理器
    response = exception_handler(exc, context)

    if response is not None:
        # DRF 已经处理了异常，转换响应格式
        # 获取状态码对应的业务码
        status_code = response.status_code

        # 提取错误信息
        if isinstance(exc, DRFValidationError):
            # 验证错误可能包含多个字段
            detail = exc.detail
            if isinstance(detail, dict):
                # 多个字段的验证错误
                message = "参数验证失败"
                errors = detail
            elif isinstance(detail, list):
                # 列表形式的错误
                message = detail[0] if detail else "参数验证失败"
                errors = None
            else:
                # 单个错误信息
                message = str(detail)
                errors = None
        else:
            # 其他类型的异常
            message = str(exc.detail) if hasattr(exc, 'detail') else str(exc)
            errors = None

        # 构建标准响应
        custom_response_data = {
            'code': status_code,
            'message': message,
            'data': None
        }

        if errors:
            custom_response_data['errors'] = errors

        response.data = custom_response_data

    return response
