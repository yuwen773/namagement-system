"""
自定义异常模块

提供业务异常类和全局异常处理器
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)


class BusinessError(Exception):
    """
    业务异常基类

    用于处理业务逻辑中的错误，如数据验证失败、状态不允许等
    """

    def __init__(self, message: str = "业务处理失败", code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(Exception):
    """参数校验异常"""

    def __init__(self, message: str = "参数验证失败", errors: dict = None):
        self.message = message
        self.errors = errors or {}
        super().__init__(message)


class NotFoundError(Exception):
    """资源不存在异常"""

    def __init__(self, message: str = "资源不存在"):
        self.message = message
        self.code = 404
        super().__init__(message)


class PermissionDeniedError(Exception):
    """权限不足异常"""

    def __init__(self, message: str = "权限不足"):
        self.message = message
        self.code = 403
        super().__init__(message)


def custom_exception_handler(exc, context):
    """
    自定义全局异常处理器

    Args:
        exc: 异常对象
        context: 上下文信息

    Returns:
        Response 或 None
    """
    # 调用 DRF 默认异常处理
    response = exception_handler(exc, context)

    if response is not None:
        # 处理 DRF 异常
        if isinstance(exc, DatabaseError):
            logger.error(f"数据库错误: {str(exc)}")
            return Response({
                'code': 500,
                'message': '数据操作失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 格式化 DRF 异常响应
        custom_response_data = {
            'code': response.status_code,
            'message': _get_error_message(exc),
            'data': None
        }
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            custom_response_data['errors'] = exc.detail

        response.data = custom_response_data
        return response

    # 处理未捕获的异常
    logger.error(f"未捕获的异常: {str(exc)}", exc_info=True)
    return Response({
        'code': 500,
        'message': '服务器内部错误',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_error_message(exc):
    """获取友好的错误消息"""
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, str):
            return exc.detail
        elif isinstance(exc.detail, dict):
            return list(exc.detail.values())[0][0] if exc.detail else '请求参数错误'
    return str(exc)
