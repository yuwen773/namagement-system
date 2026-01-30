"""
JWT 认证模块

提供基于 JWT Token 的身份验证功能。
"""
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JWT 认证类

    从请求头中提取 JWT Token 并验证用户身份。

    认证流程：
    1. 从 Authorization 请求头中提取 Token
    2. 验证 Token 格式（需以 'Bearer ' 开头）
    3. 解析并验证 Token
    4. 返回认证用户

    使用方式：
        # 在视图中使用
        @api_view(['GET'])
        @permission_classes([IsAuthenticated])
        def protected_view(request):
            user = request.user
            ...

    请求头格式：
        Authorization: Bearer <access_token>

    错误处理：
        - 401: Token 缺失、格式错误、过期或无效
        - 401: 用户不存在或已禁用
    """

    keyword = 'Bearer'

    def authenticate(self, request):
        """
        认证请求

        Args:
            request: DRF Request 对象

        Returns:
            tuple: (user, auth) 如果认证成功
            None: 如果认证失败（未提供 Token）

        Raises:
            AuthenticationFailed: Token 无效、过期或格式错误
        """
        # 获取 Authorization 请求头
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            # 未提供 Token，返回 None（允许匿名访问）
            return None

        if len(auth_header) == 1:
            # 只有关键字，没有 Token
            raise exceptions.AuthenticationFailed(
                '无效的 Token 请求头，未提供 Token'
            )

        if len(auth_header) > 2:
            # 请求头格式错误
            raise exceptions.AuthenticationFailed(
                '无效的 Token 请求头，Token 字符串不应包含空格'
            )

        # 检查关键字是否为 'Bearer'
        if auth_header[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(
                f'不支持的认证类型，应使用 {self.keyword}'
            )

        # 提取 Token 字符串
        token = auth_header[1].decode()

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """
        验证 Token 并返回用户

        Args:
            token: JWT Token 字符串

        Returns:
            tuple: (user, token)

        Raises:
            AuthenticationFailed: Token 无效、过期或用户不存在
        """
        try:
            # 使用 SimpleJWT 验证 Token
            access_token = AccessToken(token)

            # 获取用户 ID
            user_id = access_token.get('user_id')

            if not user_id:
                raise exceptions.AuthenticationFailed(
                    'Token 中未包含用户信息'
                )

            # 导入 User 模型（避免循环导入）
            from .models import User

            # 查询用户
            user = User.objects.get(id=user_id)

            # 检查用户是否激活
            if not user.is_active:
                raise exceptions.AuthenticationFailed(
                    '该用户已被禁用'
                )

            # 返回用户和 Token
            return (user, access_token)

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                '用户不存在'
            )

        except (InvalidToken, TokenError) as e:
            # Token 无效或过期
            raise exceptions.AuthenticationFailed(
                f'Token 无效或已过期：{str(e)}'
            )

        except Exception as e:
            # 其他未预期的错误
            raise exceptions.AuthenticationFailed(
                f'认证失败：{str(e)}'
            )

    def authenticate_header(self, request):
        """
        返回用于 WWW-Authenticate 头的字符串

        Args:
            request: DRF Request 对象

        Returns:
            str: 认证类型关键字
        """
        return self.keyword
