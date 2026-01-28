"""
统一响应封装模块

提供统一的 API 响应格式，确保所有接口返回结构一致
"""
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional, Dict


class ApiResponse:
    """
    统一响应封装类

    所有 API 接口必须使用此类返回响应，确保响应格式一致
    响应格式：{code, message, data}
    """

    @staticmethod
    def success(data: Any = None, message: str = "操作成功", code: int = 200) -> Response:
        """
        成功响应

        Args:
            data: 响应数据，可以是 None、dict、list 等任意类型
            message: 响应消息，默认 "操作成功"
            code: 业务状态码，默认 200（201 表示创建成功）

        Returns:
            Response: DRF Response 对象

        Examples:
            >>> ApiResponse.success()
            >>> ApiResponse.success(data={'id': 1}, message='获取成功')
            >>> ApiResponse.success(data=serializer.data, message='创建成功', code=201)
        """
        response_data = {
            'code': code,
            'message': message,
            'data': data
        }
        http_status = status.HTTP_201_CREATED if code == 201 else status.HTTP_200_OK
        return Response(response_data, status=http_status)

    @staticmethod
    def error(
        message: str,
        code: int = 400,
        errors: Optional[Dict] = None,
        data: Any = None
    ) -> Response:
        """
        错误响应

        Args:
            message: 错误消息
            code: 错误状态码，默认 400
            errors: 详细错误信息字典（可选），用于返回参数校验详情
            data: 额外数据（可选）

        Returns:
            Response: DRF Response 对象

        Examples:
            >>> ApiResponse.error(message='参数验证失败')
            >>> ApiResponse.error(message='创建失败', errors=serializer.errors)
            >>> ApiResponse.error(message='资源不存在', code=404)
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
    def paginate(data: Dict, message: str = "获取成功") -> Response:
        """
        分页响应

        Args:
            data: 分页数据字典，包含 count, next, previous, results
            message: 响应消息，默认 "获取成功"

        Returns:
            Response: DRF Response 对象

        Examples:
            >>> ApiResponse.paginate(data={
            ...     'count': 100,
            ...     'next': 'url',
            ...     'previous': None,
            ...     'results': [...]
            ... })
        """
        return Response({
            'code': 200,
            'message': message,
            'data': data
        })

    @staticmethod
    def server_error(message: str = "服务器内部错误", data: Any = None) -> Response:
        """
        服务器错误响应

        Args:
            message: 错误消息
            data: 额外数据

        Returns:
            Response: DRF Response 对象
        """
        return Response({
            'code': 500,
            'message': message,
            'data': data
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def unauthorized(message: str = "未授权或认证失败", data: Any = None) -> Response:
        """
        未认证响应

        Args:
            message: 错误消息
            data: 额外数据

        Returns:
            Response: DRF Response 对象
        """
        return Response({
            'code': 401,
            'message': message,
            'data': data
        }, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden(message: str = "权限不足", data: Any = None) -> Response:
        """
        权限不足响应

        Args:
            message: 错误消息
            data: 额外数据

        Returns:
            Response: DRF Response 对象
        """
        return Response({
            'code': 403,
            'message': message,
            'data': data
        }, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def not_found(message: str = "资源不存在", data: Any = None) -> Response:
        """
        资源不存在响应

        Args:
            message: 错误消息
            data: 额外数据

        Returns:
            Response: DRF Response 对象
        """
        return Response({
            'code': 404,
            'message': message,
            'data': data
        }, status=status.HTTP_404_NOT_FOUND)
