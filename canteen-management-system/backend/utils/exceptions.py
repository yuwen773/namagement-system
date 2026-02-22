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


# =====================================================
# 带错误码的新异常类体系 (E100 系列)
# =====================================================

class BaseAPIException(APIException):
    """API 异常基类，带错误码支持"""

    status_code = 400
    error_code = 'E100'
    default_message = '操作失败'

    def __init__(self, message=None, detail=None):
        self.detail = message or self.default_message
        super().__init__(detail=self.detail)

    @property
    def error_code_value(self):
        return self.error_code


class ValidationException(BaseAPIException):
    """参数验证失败异常"""

    status_code = 400
    error_code = 'E100'
    default_message = '参数验证失败'


class RequiredFieldException(BaseAPIException):
    """缺少必需参数异常"""

    status_code = 400
    error_code = 'E101'
    default_message = '缺少必需参数'


class FormatErrorException(BaseAPIException):
    """参数格式错误异常"""

    status_code = 400
    error_code = 'E102'
    default_message = '参数格式错误'


class RangeErrorException(BaseAPIException):
    """参数值范围错误异常"""

    status_code = 400
    error_code = 'E103'
    default_message = '参数值范围错误'


class AuthenticationException(BaseAPIException):
    """认证异常"""

    status_code = 401
    error_code = 'E010'
    default_message = '未登录或登录已过期'


class InvalidCredentialsException(AuthenticationException):
    """用户名或密码错误异常"""

    error_code = 'E011'
    default_message = '用户名或密码错误'


class PermissionException(BaseAPIException):
    """权限不足异常"""

    status_code = 403
    error_code = 'E020'
    default_message = '权限不足'


class NotFoundException(BaseAPIException):
    """资源不存在异常"""

    status_code = 404
    error_code = 'E030'
    default_message = '资源不存在'


class EmployeeNotFoundException(NotFoundException):
    """员工不存在异常"""

    error_code = 'E031'
    default_message = '员工不存在'


class ScheduleNotFoundException(NotFoundException):
    """排班不存在异常"""

    error_code = 'E032'
    default_message = '排班不存在'


class UserNotFoundException(NotFoundException):
    """用户不存在异常"""

    error_code = 'E033'
    default_message = '用户不存在'


class DuplicateException(BaseAPIException):
    """数据已存在异常"""

    status_code = 409
    error_code = 'E040'
    default_message = '数据已存在'


class UsernameExistsException(DuplicateException):
    """用户名已存在异常"""

    error_code = 'E041'
    default_message = '用户名已存在'


class StateNotAllowedException(BaseAPIException):
    """状态不允许异常"""

    status_code = 422
    error_code = 'E050'
    default_message = '当前状态不允许此操作'


class AlreadyProcessedException(StateNotAllowedException):
    """申请已被处理异常"""

    error_code = 'E051'
    default_message = '申请已被处理，无法重复操作'


class InvalidStateException(StateNotAllowedException):
    """状态无效异常"""

    error_code = 'E052'
    default_message = '只能操作草稿状态的记录'


class ServerException(BaseAPIException):
    """服务器异常"""

    status_code = 500
    error_code = 'E900'
    default_message = '服务器内部错误'


class DatabaseException(ServerException):
    """数据库操作失败异常"""

    error_code = 'E901'
    default_message = '数据操作失败'
