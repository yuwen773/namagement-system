"""
Unified API response wrapper.

All APIs return a consistent structure (per API_DOCS.md):
{
  "code": 0,          # 成功响应 code 为 0，错误响应为 HTTP 状态码 (400/401/403/404/500)
  "data": ...,
  "message": "",
  # optionally:
  "total": 123,
  "page": 1,
  "page_size": 20
}
"""

from __future__ import annotations

from typing import Any, Optional

from rest_framework.response import Response


class APIResponse(Response):
    def __init__(
        self,
        data: Any = None,
        code: int = 200,
        message: str = "",
        total: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs,
    ):
        payload = {"code": code, "data": data, "message": message}
        if total is not None:
            payload["total"] = total
        if page is not None:
            payload["page"] = page
        if page_size is not None:
            payload["page_size"] = page_size

        # Keep HTTP status aligned with code for 4xx/5xx.
        super().__init__(data=payload, status=code if 100 <= code < 600 else 200, **kwargs)

    @classmethod
    def success(cls, data: Any = None, message: str = "") -> "APIResponse":
        # API_DOCS.md 规定：成功响应 code 为 0
        return cls(data=data, code=0, message=message)

    @classmethod
    def error(cls, code: int, message: str) -> "APIResponse":
        return cls(data=None, code=code, message=message)

    @classmethod
    def paginate(
        cls, data: list, total: int, page: int = 1, page_size: int = 20, message: str = ""
    ) -> "APIResponse":
        # API_DOCS.md 规定：成功响应 code 为 0
        return cls(data=data, code=0, message=message, total=total, page=page, page_size=page_size)

