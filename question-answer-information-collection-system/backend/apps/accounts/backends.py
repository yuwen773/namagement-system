"""
自定义认证后端 - 明文密码验证
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class PlainPasswordBackend(ModelBackend):
    """
    自定义认证后端，明文密码验证
    密码在数据库中以明文存储，不使用哈希
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        验证用户名和密码
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or password is None:
            return None

        try:
            # 支持用户名或邮箱登录
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
        except User.DoesNotExist:
            return None

        # 明文密码验证（不使用 check_password）
        if user.password == password:
            return user

        return None
