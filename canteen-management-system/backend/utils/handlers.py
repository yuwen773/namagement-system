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
        Response: 统一格式的错误响应，或 None（交给 DRF 默认处理）
    """
    # 调用 DRF 默认异常处理
    response = exception_handler(exc, context)

    # 获取视图信息
    view = context.get('view')
    view_name = view.__class__.__name__ if view else 'UnknownView'

    if response is not None:
        # DRF 已处理的异常（如 ValidationError、NotFound 等）
        # 格式化为统一响应
        return _format_drf_response(exc, response, view_name)

    # 处理 Django 特定异常
    if isinstance(exc, DjangoValidationError):
        logger.warning(f"Django 验证错误 in {view_name}: {str(exc)}")
        return Response({
            'code': 400,
            'message': '数据验证失败',
            'data': None,
            'errors': {'detail': str(exc)}
        }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, DatabaseError):
        logger.error(f"数据库错误 in {view_name}: {str(exc)}", exc_info=True)
        return Response({
            'code': 500,
            'message': '数据操作失败',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 处理未捕获的异常
    logger.error(
        f"未捕获的异常 in {view_name}: {type(exc).__name__}: {str(exc)}",
        exc_info=True
    )
    return Response({
        'code': 500,
        'message': '服务器内部错误',
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

    # 构建统一响应格式
    custom_response_data = {
        'code': response.status_code,
        'message': _get_error_message(exc),
        'data': None
    }

    # 处理错误详情
    if hasattr(exc, 'detail'):
        detail = exc.detail

        # 如果 detail 是字典（如字段验证错误），添加到 errors
        if isinstance(detail, dict):
            # 格式化字段错误
            formatted_errors = {}
            for field, errors in detail.items():
                if isinstance(errors, list):
                    formatted_errors[field] = errors[0] if errors else ''
                else:
                    formatted_errors[field] = str(errors)
            custom_response_data['errors'] = formatted_errors
        # 如果 detail 是列表（如非字段错误）
        elif isinstance(detail, list):
            custom_response_data['errors'] = {'detail': detail[0] if detail else ''}
        # 如果 detail 是字符串
        elif isinstance(detail, str):
            if response.status_code == 400:
                # 对于 400 错误，将 detail 作为 errors
                custom_response_data['errors'] = {'detail': detail}
            # 其他情况保持 message 作为错误消息

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
    # 如果异常有 detail 属性
    if hasattr(exc, 'detail'):
        detail = exc.detail

        if isinstance(detail, str):
            return detail

        if isinstance(detail, dict):
            # 返回第一个字段的第一个错误
            for value in detail.values():
                if isinstance(value, list) and value:
                    return str(value[0])
                return str(value)

        if isinstance(detail, list) and detail:
            return str(detail[0])

    # 默认错误消息
    return str(exc)
