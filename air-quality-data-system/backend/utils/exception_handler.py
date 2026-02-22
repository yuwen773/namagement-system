"""
Custom DRF exception handler to enforce unified response format.
"""

from __future__ import annotations

import logging

from django.db import DatabaseError
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    PermissionDenied,
    Throttled,
    ValidationError as DRFValidationError,
)
from rest_framework.views import exception_handler

from utils.response import APIResponse

logger = logging.getLogger(__name__)

# 字段名中英文映射表
FIELD_NAME_MAP = {
    # 通用字段
    "id": "ID",
    "name": "名称",
    "title": "标题",
    "content": "内容",
    "status": "状态",
    "sort": "排序",
    "sort_order": "排序",
    "is_enabled": "启用状态",
    "is_announcement": "是否公告",
    # 用户相关
    "username": "用户名",
    "password": "密码",
    "email": "邮箱",
    "phone": "手机号",
    "role": "角色",
    # 规则相关
    "rule_name": "规则名称",
    "min_aqi": "AQI最小值",
    "max_aqi": "AQI最大值",
    "population_type": "人群类型",
    "advice": "防护建议",
    # 文章相关
    "category_id": "文章分类",
    "category": "文章分类",
    "category_name": "分类名称",
    # 数据导入相关
    "dataset_type": "数据集类型",
    "file_type": "文件类型",
    "file_name": "文件名",
    # 通用操作字段
    "ids": "ID列表",
    "keyword": "关键词",
    "page": "页码",
    "page_size": "每页数量",
}


def translate_field_name(field_name: str) -> str:
    """将英文字段名翻译为中文"""
    return FIELD_NAME_MAP.get(field_name, field_name)


class ValidationError(Exception):
    """User input validation error."""

    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        super().__init__(message)


class BusinessError(Exception):
    """Business logic error."""

    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return _format_drf_response(response, exc)

    if isinstance(exc, ValidationError):
        msg = exc.message
        if exc.field:
            translated_field = translate_field_name(exc.field)
            msg = f"参数 '{translated_field}' {msg}"
        return APIResponse.error(400, msg)

    if isinstance(exc, BusinessError):
        return APIResponse.error(exc.code, exc.message)

    if isinstance(exc, DatabaseError):
        logger.error("Database error", exc_info=True)
        return APIResponse.error(500, "数据处理失败，请稍后重试或联系技术支持")

    logger.error("Unhandled exception", exc_info=True)
    return APIResponse.error(500, "服务器内部错误，请稍后重试")


def _format_drf_response(response, exc) -> APIResponse:
    status_code = response.status_code

    if isinstance(exc, NotFound):
        return APIResponse.error(status_code, str(getattr(exc, "detail", "请求的资源不存在")))
    if isinstance(exc, PermissionDenied):
        return APIResponse.error(status_code, "您没有权限访问此资源")
    if isinstance(exc, AuthenticationFailed):
        return APIResponse.error(status_code, "请先登录")
    if isinstance(exc, Throttled):
        return APIResponse.error(status_code, "请求过于频繁，请稍后再试")

    if isinstance(exc, DRFValidationError):
        detail = getattr(exc, "detail", None)
        if isinstance(detail, dict):
            parts = []
            for field, err in detail.items():
                translated_field = translate_field_name(field)
                if isinstance(err, list) and err:
                    parts.append(f"{translated_field}: {err[0]}")
                else:
                    parts.append(f"{translated_field}: {err}")
            message = "; ".join(parts) if parts else "参数校验失败"
        elif isinstance(detail, list) and detail:
            message = str(detail[0])
        else:
            message = str(detail) if detail is not None else "参数校验失败"
        return APIResponse.error(status_code, message)

    # Fallback: best-effort extraction.
    message = str(getattr(exc, "detail", str(exc)))
    return APIResponse.error(status_code, message)

