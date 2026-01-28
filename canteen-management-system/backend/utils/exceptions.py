"""
自定义异常类模块

提供业务异常类，用于处理各种业务逻辑错误
"""
from rest_framework.exceptions import APIException


class BusinessError(APIException):
    """
    业务异常基类

    用于处理业务逻辑中的错误，如数据验证失败、状态不允许等
    所有自定义业务异常都应继承此类

    Attributes:
        status_code: HTTP 状态码，默认 400
        default_detail: 默认错误消息
        default_code: 错误代码
    """

    status_code = 400
    default_detail = '业务处理失败'
    default_code = 'business_error'

    def __init__(self, detail: str = None, code: int = 400):
        """
        初始化业务异常

        Args:
            detail: 错误详情消息
            code: 业务状态码
        """
        self.detail = detail or self.default_detail
        self.code = code


class ValidationError(BusinessError):
    """
    参数验证异常

    用于请求参数验证失败的场景
    """

    default_detail = '参数验证失败'
    default_code = 'validation_error'


class NotFoundError(BusinessError):
    """
    资源不存在异常

    用于请求的资源不存在的场景
    """

    status_code = 404
    default_detail = '资源不存在'
    default_code = 'not_found'


class PermissionDeniedError(BusinessError):
    """
    权限不足异常

    用于用户权限不足的场景
    """

    status_code = 403
    default_detail = '权限不足'
    default_code = 'permission_denied'


class StateNotAllowedError(BusinessError):
    """
    状态不允许异常

    用于对象当前状态不允许执行某操作的场景
    例如：已审批的请假不能再次审批、已发布的薪资不能修改等
    """

    default_detail = '当前状态不允许此操作'
    default_code = 'state_not_allowed'


class DuplicateError(BusinessError):
    """
    重复数据异常

    用于数据重复的场景，如用户名已存在等
    """

    default_detail = '数据已存在'
    default_code = 'duplicate'


class InvalidOperationError(BusinessError):
    """
    无效操作异常

    用于不允许的操作场景
    """

    default_detail = '无效的操作'
    default_code = 'invalid_operation'


class InsufficientDataError(BusinessError):
    """
    数据不足异常

    用于数据不完整的场景
    """

    default_detail = '数据不完整'
    default_code = 'insufficient_data'
