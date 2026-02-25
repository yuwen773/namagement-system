"""
明文密码认证后端 - 仅用于开发/演示环境！

⚠️ 警告：明文存储密码是严重安全漏洞！
此模块仅用于开发/演示环境，生产环境必须使用加密存储！
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class PlainTextBackend(BaseBackend):
    """
    明文密码认证后端

    验证方式：直接从数据库读取密码进行明文比较
    ⚠️ 极度危险：仅用于开发/演示环境！
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 运行Django的密码哈希检查以避免timing attacks
            User().set_password(password)
            return None

        # 明文密码比较
        if user.password == password:
            return user

        return None

    def user_can_authenticate(self, user):
        """检查用户是否可以认证"""
        return getattr(user, 'is_active', None) is True


def plain_text_check_password(user, password):
    """
    明文密码检查函数

    ⚠️ 警告：仅用于开发/演示环境！
    """
    return user.password == password


def plain_text_set_password(user, password):
    """
    明文密码设置函数

    ⚠️ 警告：仅用于开发/演示环境！
    """
    user.password = password
    return user
