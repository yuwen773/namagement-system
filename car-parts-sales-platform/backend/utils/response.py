"""
统一响应封装模块
"""
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional


class ApiResponse:
    """统一响应封装类"""

    @staticmethod
    def success(data: Any = None, message: str = "操作成功", code: int = 200) -> Response:
        """
        成功响应

        Args:
            data: 响应数据
            message: 响应消息
            code: 业务状态码

        Returns:
            Response
        """
        return Response({
            'code': code,
            'message': message,
            'data': data
        }, status=status.HTTP_200_OK if code == 200 else status.HTTP_201_CREATED)

    @staticmethod
    def error(message: str, code: int = 400, errors: Optional[dict] = None, data: Any = None) -> Response:
        """
        错误响应

        Args:
            message: 错误消息
            code: 错误状态码
            errors: 详细错误信息
            data: 额外数据

        Returns:
            Response
        """
        response_data = {
            'code': code,
            'message': message,
            'data': data
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def paginate(data: dict, message: str = "获取成功") -> Response:
        """
        分页响应

        Args:
            data: 分页数据（包含 count, next, previous, results）
            message: 响应消息

        Returns:
            Response
        """
        return Response({
            'code': 200,
            'message': message,
            'data': data
        })
