"""
自定义异常处理器

统一处理所有异常，确保返回标准格式的响应。
包含详细的错误信息、错误码和建议操作。
"""
import traceback
import uuid
import logging
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied as DRFPermissionDenied,
)
from rest_framework import status
from django.db import DatabaseError as DjangoDatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError

from .response import ApiResponse
from .exceptions import (
    BusinessError,
    ErrorCode,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    TokenExpiredError,
    TokenInvalidError,
    PermissionDeniedError,
    DatabaseError,
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义异常处理器

    将所有异常转换为统一的响应格式：
    {
        "code": xxx,
        "message": "xxx",
        "type": "xxx",
        "data": null,
        "trace_id": "xxx",
        "suggestions": [...]
    }

    Args:
        exc: 异常实例
        context: 上下文信息

    Returns:
        Response: 标准格式的响应
    """
    # 生成追踪ID，方便问题排查
    trace_id = str(uuid.uuid4())[:8]

    # 先调用 DRF 默认的异常处理器
    response = exception_handler(exc, context)

    # 处理 DRF 验证错误
    if isinstance(exc, DRFValidationError):
        return _handle_validation_error(exc, trace_id)

    # 处理认证相关错误
    if isinstance(exc, NotAuthenticated):
        return ApiResponse.error(
            message='请先登录后再操作',
            code=ErrorCode.UNAUTHORIZED,
            data={'trace_id': trace_id, 'error_type': 'not_authenticated'}
        )

    if isinstance(exc, AuthenticationFailed):
        return _handle_authentication_failed(exc, trace_id)

    if isinstance(exc, DRFPermissionDenied):
        return ApiResponse.error(
            message='权限不足，无法访问此资源',
            code=ErrorCode.PERMISSION_DENIED,
            data={'trace_id': trace_id, 'error_type': 'permission_denied'}
        )

    # 处理 Django 数据库错误
    if isinstance(exc, DjangoDatabaseError):
        logger.error(f"Database error (trace_id={trace_id}): {str(exc)}\n{traceback.format_exc()}")
        return ApiResponse.error(
            message='数据操作失败，请稍后重试',
            code=ErrorCode.DATABASE_ERROR,
            data={'trace_id': trace_id, 'error_type': 'database_error'},
            errors={'detail': '数据库操作异常'}
        )

    # 处理 Django 表单验证错误
    if isinstance(exc, DjangoValidationError):
        return ApiResponse.error(
            message='数据验证失败',
            code=ErrorCode.VALIDATION_ERROR,
            data={'trace_id': trace_id, 'error_type': 'validation_error'},
            errors={'detail': list(exc.messages) if hasattr(exc, 'messages') else str(exc)}
        )

    # 处理已定义的业务异常
    if isinstance(exc, BusinessError):
        return _handle_business_error(exc, trace_id)

    # 处理未捕获的异常
    if response is None:
        logger.error(f"Unhandled exception (trace_id={trace_id}): {str(exc)}\n{traceback.format_exc()}")
        return ApiResponse.error(
            message='服务器内部错误，请稍后重试',
            code=ErrorCode.INTERNAL_ERROR,
            data={
                'trace_id': trace_id,
                'error_type': 'internal_error',
                'error_id': str(exc.__class__.__name__)
            }
        )

    # DRF 已处理，转换响应格式
    return _handle_drf_response(response, exc, trace_id)


def _handle_validation_error(exc, trace_id):
    """
    处理 DRF 验证错误

    Args:
        exc: ValidationError 异常
        trace_id: 追踪ID

    Returns:
        Response: 格式化后的响应
    """
    detail = exc.detail

    # 构建字段错误信息
    errors = {}
    error_messages = []

    if isinstance(detail, dict):
        # 多个字段的验证错误
        for field, field_errors in detail.items():
            field_error_list = []
            for field_error in field_errors:
                if hasattr(field_error, 'detail'):
                    field_error_list.append(str(field_error.detail))
                else:
                    field_error_list.append(str(field_error))
            errors[field] = field_error_list
            # 收集错误消息用于主消息
            error_messages.extend(field_error_list)
    elif isinstance(detail, list):
        # 列表形式的错误
        error_messages = [str(d) for d in detail]
        errors['non_field_errors'] = error_messages
    else:
        # 单个错误信息
        error_messages = [str(detail)]

    # 构建主错误消息
    main_message = error_messages[0] if error_messages else '参数验证失败'

    return ApiResponse.error(
        message=main_message,
        code=ErrorCode.VALIDATION_ERROR,
        data={
            'trace_id': trace_id,
            'error_type': 'validation_error',
            'errors': errors
        },
        errors=errors if errors else None
    )


def _handle_authentication_failed(exc, trace_id):
    """
    处理认证失败错误

    根据不同的认证失败原因返回不同的错误信息

    Args:
        exc: AuthenticationFailed 异常
        trace_id: 追踪ID

    Returns:
        Response: 格式化后的响应
    """
    detail = str(exc.detail)

    # 根据错误详情判断具体原因
    if 'credentials' in detail.lower() or 'invalid' in detail.lower():
        # Token 无效
        return ApiResponse.error(
            message='认证令牌无效，请重新登录',
            code=ErrorCode.TOKEN_INVALID,
            data={
                'trace_id': trace_id,
                'error_type': 'token_invalid',
                'suggestions': ['请重新登录', '如问题持续，请清除缓存后重试']
            }
        )
    elif 'expired' in detail.lower():
        # Token 过期
        return ApiResponse.error(
            message='登录已过期，请重新登录',
            code=ErrorCode.TOKEN_EXPIRED,
            data={
                'trace_id': trace_id,
                'error_type': 'token_expired',
                'suggestions': ['请重新登录', '如需记住登录状态，登录时勾选"记住我"']
            }
        )
    else:
        # 其他认证失败
        return ApiResponse.error(
            message=detail or '认证失败',
            code=ErrorCode.UNAUTHORIZED,
            data={
                'trace_id': trace_id,
                'error_type': 'authentication_failed'
            }
        )


def _handle_business_error(exc, trace_id):
    """
    处理业务异常

    Args:
        exc: BusinessError 异常
        trace_id: 追踪ID

    Returns:
        Response: 格式化后的响应
    """
    # 构建响应数据
    data = {
        'trace_id': trace_id,
        'error_type': exc.error_type if hasattr(exc, 'error_type') else 'business_error',
    }

    # 添加建议操作
    if hasattr(exc, 'suggestions') and exc.suggestions:
        data['suggestions'] = exc.suggestions

    # 添加字段信息
    if hasattr(exc, 'field') and exc.field:
        data['field'] = exc.field

    # 使用异常定义的 HTTP 状态码
    http_status = getattr(exc, 'status_code', status.HTTP_400_BAD_REQUEST)

    # 构建错误响应
    response_data = {
        'code': exc.code if hasattr(exc, 'code') else ErrorCode.BAD_REQUEST,
        'message': str(exc.detail),
        'data': data
    }

    return Response(response_data, status=http_status)


def _handle_drf_response(response, exc, trace_id):
    """
    处理 DRF 标准响应

    Args:
        response: DRF 响应对象
        exc: 原始异常
        trace_id: 追踪ID

    Returns:
        Response: 格式化后的响应
    """
    # 获取原始状态码
    status_code = response.status_code

    # 根据状态码确定错误码和消息
    code_mapping = {
        400: ErrorCode.BAD_REQUEST,
        401: ErrorCode.UNAUTHORIZED,
        403: ErrorCode.FORBIDDEN,
        404: ErrorCode.RESOURCE_NOT_FOUND,
        405: ErrorCode.BAD_REQUEST,
        409: ErrorCode.RESOURCE_EXISTS,
        500: ErrorCode.INTERNAL_ERROR,
    }

    error_code = code_mapping.get(status_code, ErrorCode.BAD_REQUEST)

    # 构建错误消息
    message = _get_default_message(status_code)

    # 提取错误详情
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            message = list(exc.detail.values())[0] if exc.detail else message
        elif isinstance(exc.detail, list):
            message = exc.detail[0] if exc.detail else message
        else:
            message = str(exc.detail)

    # 构建响应
    response_data = {
        'code': error_code,
        'message': message,
        'data': {
            'trace_id': trace_id,
            'error_type': _get_error_type(status_code)
        }
    }

    # 添加详细错误信息
    if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
        response_data['data']['errors'] = exc.detail

    response.data = response_data
    return response


def _get_default_message(status_code):
    """获取默认错误消息"""
    default_messages = {
        400: '请求参数错误',
        401: '未登录或登录已过期',
        403: '权限不足',
        404: '请求的资源不存在',
        405: '请求方法不允许',
        409: '资源冲突',
        410: '资源已被删除',
        422: '无法处理的',
        429: '请求过于实体频繁，请稍后重试',
        500: '服务器内部错误',
        502: '网关错误',
        503: '服务不可用',
    }
    return default_messages.get(status_code, '请求失败')


def _get_error_type(status_code):
    """获取错误类型"""
    error_types = {
        400: 'bad_request',
        401: 'unauthorized',
        403: 'forbidden',
        404: 'not_found',
        405: 'method_not_allowed',
        409: 'conflict',
        500: 'internal_error',
        502: 'bad_gateway',
        503: 'service_unavailable',
    }
    return error_types.get(status_code, 'unknown_error')
