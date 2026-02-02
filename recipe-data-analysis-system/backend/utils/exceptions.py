"""
自定义异常模块

定义业务异常类，用于处理业务逻辑中的错误。
包含详细的错误码和错误信息，便于前端展示和问题排查。
"""
from rest_framework.exceptions import APIException


# ==================== 错误码定义 ====================
class ErrorCode:
    """业务错误码常量定义"""
    # 通用错误码 (1xxx)
    SUCCESS = 200
    BAD_REQUEST = 400
    VALIDATION_ERROR = 4001
    PARAMETER_ERROR = 4002
    RESOURCE_NOT_FOUND = 4040
    RESOURCE_EXISTS = 4041
    UNAUTHORIZED = 4010
    TOKEN_EXPIRED = 4011
    TOKEN_INVALID = 4012
    FORBIDDEN = 4030
    PERMISSION_DENIED = 4031
    ACCOUNT_DISABLED = 4032
    ACCOUNT_BANNED = 4033
    INTERNAL_ERROR = 5000
    DATABASE_ERROR = 5001

    # 认证错误码 (41xx)
    USERNAME_NOT_FOUND = 4101
    PASSWORD_WRONG = 4102
    USERNAME_ALREADY_EXISTS = 4103
    EMAIL_ALREADY_EXISTS = 4104
    PHONE_ALREADY_EXISTS = 4105
    OLD_PASSWORD_WRONG = 4106
    NEW_PASSWORD_SAME_AS_OLD = 4107
    PASSWORD_TOO_WEAK = 4108

    # 业务操作错误码 (42xx)
    ALREADY_FAVORITED = 4201
    NOT_FAVORITED = 4202
    RECIPE_NOT_FOUND = 4203
    CATEGORY_NOT_FOUND = 4204
    INGREDIENT_NOT_FOUND = 4205
    CANNOT_OPERATE_SELF = 4206
    USER_NOT_FOUND = 4207
    USER_ALREADY_BANNED = 4208
    USER_NOT_BANNED = 4209

    # 文件上传错误码 (43xx)
    FILE_TOO_LARGE = 4301
    INVALID_FILE_TYPE = 4302
    FILE_UPLOAD_FAILED = 4303
    NO_FILE_UPLOADED = 4304


# ==================== 异常类定义 ====================

class BusinessError(APIException):
    """
    业务异常基类

    用于处理业务逻辑中的错误，如数据验证失败、状态不允许等
    """
    status_code = 400
    default_detail = '业务处理失败'
    default_code = ErrorCode.BAD_REQUEST
    default_error_type = 'business_error'

    def __init__(
        self,
        detail: str = None,
        code: int = None,
        error_type: str = None,
        field: str = None,
        suggestions: list = None
    ):
        """
        Args:
            detail: 错误详情（用户友好的描述）
            code: 业务状态码（对应 ErrorCode）
            error_type: 错误类型（用于前端分类处理）
            field: 关联的字段名（表单验证用）
            suggestions: 建议操作列表
        """
        self.detail = detail or self.default_detail
        self.code = code if code is not None else self.default_code
        self.error_type = error_type or self.default_error_type
        self.field = field
        self.suggestions = suggestions or []
        # 组合 detail 用于 DRF
        super().__init__(detail)

    def to_dict(self):
        """转换为字典格式"""
        result = {
            'code': self.code,
            'message': self.detail,
            'type': self.error_type,
        }
        if self.field:
            result['field'] = self.field
        if self.suggestions:
            result['suggestions'] = self.suggestions
        return result


class ValidationError(BusinessError):
    """参数验证异常"""
    status_code = 400
    default_detail = '参数验证失败'
    default_code = ErrorCode.VALIDATION_ERROR
    default_error_type = 'validation_error'

    def __init__(self, detail: str = '参数验证失败', field: str = None, code: int = None):
        super().__init__(
            detail=detail,
            code=code or ErrorCode.VALIDATION_ERROR,
            error_type='validation_error',
            field=field,
            suggestions=self._get_suggestions(field)
        )

    @staticmethod
    def _get_suggestions(field: str) -> list:
        """根据字段返回建议"""
        suggestions_map = {
            'username': ['用户名长度需在3-20个字符之间', '仅支持字母、数字、下划线'],
            'password': ['密码长度至少8位', '建议包含字母、数字和特殊字符'],
            'email': ['请输入有效的邮箱地址'],
            'phone': ['请输入有效的手机号（11位数字）'],
        }
        return suggestions_map.get(field, [])


class ParameterError(BusinessError):
    """参数错误异常"""
    status_code = 400
    default_detail = '请求参数错误'
    default_code = ErrorCode.PARAMETER_ERROR
    default_error_type = 'parameter_error'


class NotFoundError(BusinessError):
    """资源不存在异常"""
    status_code = 404
    default_detail = '资源不存在'
    default_code = ErrorCode.RESOURCE_NOT_FOUND
    default_error_type = 'not_found'

    def __init__(self, detail: str = None, resource_name: str = None, code: int = None):
        message = detail or f'{resource_name or "资源"}不存在或已被删除'
        super().__init__(
            detail=message,
            code=code or ErrorCode.RESOURCE_NOT_FOUND,
            error_type='not_found',
            suggestions=['请检查资源ID是否正确', '刷新页面后重试']
        )


class ResourceExistsError(BusinessError):
    """资源已存在异常"""
    status_code = 409
    default_detail = '资源已存在'
    default_code = ErrorCode.RESOURCE_EXISTS
    default_error_type = 'resource_exists'

    def __init__(self, detail: str = None, resource_name: str = None, code: int = None):
        message = detail or f'{resource_name or "资源"}已存在'
        super().__init__(
            detail=message,
            code=code or ErrorCode.RESOURCE_EXISTS,
            error_type='resource_exists'
        )


class PermissionDeniedError(BusinessError):
    """权限不足异常"""
    status_code = 403
    default_detail = '权限不足'
    default_code = ErrorCode.PERMISSION_DENIED
    default_error_type = 'permission_denied'

    def __init__(self, detail: str = None, code: int = None, require_role: str = None):
        message = detail or f'权限不足{"，需要" + require_role + "角色" if require_role else ""}'
        suggestions = []
        if require_role:
            suggestions.append(f'请使用具有{require_role}权限的账号登录')
        else:
            suggestions.append('请联系管理员获取相应权限')
        super().__init__(
            detail=message,
            code=code or ErrorCode.PERMISSION_DENIED,
            error_type='permission_denied',
            suggestions=suggestions
        )


class UnauthorizedError(BusinessError):
    """未认证异常"""
    status_code = 401
    default_detail = '未登录或登录已过期'
    default_code = ErrorCode.UNAUTHORIZED
    default_error_type = 'unauthorized'

    def __init__(self, detail: str = None, code: int = None, token_required: bool = True):
        message = detail or ('请先登录后再操作' if token_required else '认证失败')
        super().__init__(
            detail=message,
            code=code or ErrorCode.UNAUTHORIZED,
            error_type='unauthorized',
            suggestions=['请登录后重试', '检查登录状态是否过期']
        )


class TokenExpiredError(UnauthorizedError):
    """Token过期异常"""
    default_detail = '登录已过期，请重新登录'
    default_code = ErrorCode.TOKEN_EXPIRED
    default_error_type = 'token_expired'

    def __init__(self, detail: str = None):
        super().__init__(
            detail=detail or '登录已过期，请重新登录',
            code=ErrorCode.TOKEN_EXPIRED,
            suggestions=['请重新登录', '如需记住登录状态，登录时勾选"记住我"']
        )


class TokenInvalidError(UnauthorizedError):
    """Token无效异常"""
    default_detail = '无效的认证令牌'
    default_code = ErrorCode.TOKEN_INVALID
    default_error_type = 'token_invalid'

    def __init__(self, detail: str = None):
        super().__init__(
            detail=detail or '认证令牌无效，请重新登录',
            code=ErrorCode.TOKEN_INVALID,
            suggestions=['请重新登录', '如问题持续，请清除缓存后重试']
        )


class StateNotAllowedError(BusinessError):
    """状态不允许异常"""
    default_detail = '当前状态不允许此操作'
    default_code = ErrorCode.BAD_REQUEST
    default_error_type = 'state_not_allowed'

    def __init__(self, detail: str = None, code: int = None, suggestions: list = None):
        super().__init__(
            detail=detail or '当前状态不允许此操作',
            code=code or ErrorCode.BAD_REQUEST,
            error_type='state_not_allowed',
            suggestions=suggestions or ['请刷新页面后重试', '如问题持续，请联系管理员']
        )


class AccountDisabledError(PermissionDeniedError):
    """账户被禁用异常"""
    default_detail = '账户已被禁用'
    default_code = ErrorCode.ACCOUNT_DISABLED
    default_error_type = 'account_disabled'

    def __init__(self, detail: str = None):
        super().__init__(
            detail=detail or '账户已被禁用，请联系管理员',
            code=ErrorCode.ACCOUNT_DISABLED,
            suggestions=['请联系平台管理员', '如需申诉，请联系客服']
        )


class AccountBannedError(PermissionDeniedError):
    """账户被封禁异常"""
    default_detail = '账户已被封禁'
    default_code = ErrorCode.ACCOUNT_BANNED
    default_error_type = 'account_banned'

    def __init__(self, detail: str = None, ban_reason: str = None, ban_expire: str = None):
        message = detail or '账户已被封禁'
        suggestions = ['请联系平台管理员', '如需申诉，请联系客服']
        if ban_expire:
            message += f'，解封时间：{ban_expire}'
        if ban_reason:
            message += f'，封禁原因：{ban_reason}'
        super().__init__(
            detail=message,
            code=ErrorCode.ACCOUNT_BANNED,
            suggestions=suggestions
        )


class FileTooLargeError(BusinessError):
    """文件过大异常"""
    default_detail = '文件大小超出限制'
    default_code = ErrorCode.FILE_TOO_LARGE
    default_error_type = 'file_too_large'

    def __init__(self, detail: str = None, max_size: str = '5MB'):
        super().__init__(
            detail=detail or f'文件大小超出限制，最大支持{max_size}',
            code=ErrorCode.FILE_TOO_LARGE,
            error_type='file_too_large',
            suggestions=[f'请上传小于{max_size}的文件', '可尝试压缩图片后上传']
        )


class InvalidFileTypeError(BusinessError):
    """不支持的文件类型异常"""
    default_detail = '不支持的文件类型'
    default_code = ErrorCode.INVALID_FILE_TYPE
    default_error_type = 'invalid_file_type'

    def __init__(self, detail: str = None, valid_types: list = None):
        valid = valid_types or ['jpg', 'jpeg', 'png', 'webp']
        message = detail or f'仅支持 {", ".join(valid)} 格式的图片'
        super().__init__(
            detail=message,
            code=ErrorCode.INVALID_FILE_TYPE,
            error_type='invalid_file_type',
            suggestions=[f'请上传 {", ".join(valid)} 格式的图片']
        )


class DatabaseError(BusinessError):
    """数据库操作异常"""
    status_code = 500
    default_detail = '数据操作失败'
    default_code = ErrorCode.DATABASE_ERROR
    default_error_type = 'database_error'

    def __init__(self, detail: str = None, code: int = None):
        super().__init__(
            detail=detail or '数据操作失败，请稍后重试',
            code=code or ErrorCode.DATABASE_ERROR,
            error_type='database_error',
            suggestions=['请稍后重试', '如问题持续，请联系管理员']
        )
