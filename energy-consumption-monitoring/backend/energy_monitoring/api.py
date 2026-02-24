from collections.abc import Mapping

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def _extract_message(detail) -> str:
    if isinstance(detail, list):
        if not detail:
            return "请求参数错误"
        return _extract_message(detail[0])
    if isinstance(detail, dict):
        if "detail" in detail:
            return _extract_message(detail["detail"])
        first_key = next(iter(detail), None)
        if first_key is None:
            return "请求参数错误"
        if first_key in {"message", "non_field_errors"}:
            return _extract_message(detail[first_key])
        return f"{first_key}: {_extract_message(detail[first_key])}"
    return str(detail)


def _infer_total(data) -> int:
    if data is None:
        return 0
    if isinstance(data, list):
        return len(data)
    if isinstance(data, Mapping) and "count" in data and "results" in data:
        return int(data["count"])
    return 1


class UnifiedPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "code": 0,
                "data": data,
                "message": "success",
                "total": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "total_pages": self.page.paginator.num_pages,
            }
        )


class UnifiedJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        # Skip wrapping for binary responses (file downloads)
        content_type = response.get("Content-Type", "")
        if not content_type.startswith("application/json"):
            return super().render(data, accepted_media_type, renderer_context)

        if isinstance(data, Mapping) and "code" in data and "message" in data:
            payload = dict(data)
            payload.setdefault("data", None)
            payload.setdefault("total", _infer_total(payload.get("data")))
            return super().render(payload, accepted_media_type, renderer_context)

        if response.status_code >= status.HTTP_400_BAD_REQUEST:
            payload = {
                "code": response.status_code,
                "data": None,
                "message": _extract_message(data),
                "total": 0,
            }
            return super().render(payload, accepted_media_type, renderer_context)

        payload = {
            "code": 0,
            "data": data,
            "message": "success",
            "total": _infer_total(data),
        }
        return super().render(payload, accepted_media_type, renderer_context)


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return Response(
            {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "message": "服务器内部错误",
                "total": 0,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response.data = {
        "code": response.status_code,
        "data": None,
        "message": _extract_message(response.data),
        "total": 0,
    }
    return response
