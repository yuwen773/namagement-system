"""
自定义异常模块

定义业务异常类，用于处理业务逻辑中的错误。
"""
from rest_framework.exceptions import APIException


class BusinessError(APIException):
    """
    业务异常基类

    用于处理业务逻辑中的错误，如数据验证失败、状态不允许等
    """
    status_code = 400
    default_detail = '业务处理失败'
    default_code = 'business_error'

    def __init__(self, detail: str = None, code: int = 400):
        """
        Args:
            detail: 错误详情
            code: 业务状态码
        """
        self.detail = detail or self.default_detail
        self.code = code


class ValidationError(BusinessError):
    """参数验证异常"""
    default_detail = '参数验证失败'


class NotFoundError(BusinessError):
    """资源不存在异常"""
    status_code = 404
    default_detail = '资源不存在'


class PermissionDeniedError(BusinessError):
    """权限不足异常"""
    status_code = 403
    default_detail = '权限不足'


class StateNotAllowedError(BusinessError):
    """状态不允许异常"""
    default_detail = '当前状态不允许此操作'
