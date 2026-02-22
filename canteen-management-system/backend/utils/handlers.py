"""
全局异常处理器模块

提供自定义的全局异常处理，统一返回错误响应格式
"""
import logging
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.db import DatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义全局异常处理器

    处理所有未被视图捕获的异常，返回统一格式的错误响应

    Args:
        exc: 异常对象
        context: 上下文信息，包含 view、request、args 等

    Returns:
        Response: 统一格式的错误响应
    """
    # 获取视图信息
    view = context.get('view')
    view_name = view.__class__.__name__ if view else 'UnknownView'

    # 检查是否是自定义异常
    if hasattr(exc, 'detail') and hasattr(exc, 'status_code'):
        logger.warning(f"自定义异常 in {view_name}: {str(exc)}")
        return Response({
            'code': exc.status_code,
            'message': _get_error_message(exc),
            'data': None
        }, status=exc.status_code)

    # 调用 DRF 默认异常处理
    response = exception_handler(exc, context)

    if response is not None:
        return _format_drf_response(exc, response, view_name)

    # 处理 Django 特定异常
    if isinstance(exc, DjangoValidationError):
        logger.warning(f"Django 验证错误 in {view_name}: {str(exc)}")
        return Response({
            'code': 400,
            'message': _get_error_message(exc),
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, DatabaseError):
        logger.error(f"数据库错误 in {view_name}: {str(exc)}", exc_info=True)
        return Response({
            'code': 500,
            'message': '服务器错误，请稍后重试',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 处理未捕获的异常
    logger.error(
        f"未捕获的异常 in {view_name}: {type(exc).__name__}: {str(exc)}",
        exc_info=True
    )
    return Response({
        'code': 500,
        'message': '服务器内部错误，请稍后重试',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _format_drf_response(exc, response, view_name: str) -> Response:
    """
    格式化 DRF 异常响应为统一格式

    Args:
        exc: DRF 异常对象
        response: DRF 原始响应
        view_name: 视图名称

    Returns:
        Response: 格式化后的响应
    """
    # 记录错误日志
    if response.status_code >= 500:
        logger.error(f"服务器错误 in {view_name}: {str(exc)}", exc_info=True)
    elif response.status_code >= 400:
        logger.warning(f"客户端错误 in {view_name}: {str(exc)}")

    # 获取错误消息
    error_message = _get_error_message(exc)

    # 构建统一响应格式
    custom_response_data = {
        'code': response.status_code,
        'message': error_message,
        'data': None
    }

    response.data = custom_response_data
    return response


def _get_error_message(exc) -> str:
    """
    获取友好的错误消息

    Args:
        exc: 异常对象

    Returns:
        str: 错误消息
    """
    # 辅助函数：从 ErrorDetail 或其他对象中提取字符串
    def extract_error_message(error):
        if isinstance(error, str):
            return error
        # ErrorDetail 对象有 string 属性，直接返回
        if hasattr(error, 'string'):
            return error.string
        return str(error)

    if hasattr(exc, 'detail'):
        detail = exc.detail

        if isinstance(detail, str):
            return detail

        if isinstance(detail, dict):
            # 遍历字典，返回第一个有意义的错误
            for field_name, errors in detail.items():
                if isinstance(errors, list) and errors:
                    return extract_error_message(errors[0])
                elif isinstance(errors, str):
                    return errors
            # 兜底
            first_field = list(detail.keys())[0]
            first_error = detail[first_field]
            if isinstance(first_error, list) and first_error:
                return extract_error_message(first_error[0])
            return extract_error_message(first_error)

        if isinstance(detail, list) and detail:
            return extract_error_message(detail[0])

    # 没有 detail 属性时，直接提取错误信息
    def extract_final_message(error):
        if isinstance(error, str):
            return error
        if hasattr(error, 'string'):
            return error.string
        return str(error)

    return extract_final_message(exc)
