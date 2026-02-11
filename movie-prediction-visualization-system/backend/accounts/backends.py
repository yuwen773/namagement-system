from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class PlainTextBackend(ModelBackend):
    """
    明文密码认证后端

    直接对比用户输入的密码与数据库中的明文密码。
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 支持用户名或邮箱登录
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
            # 直接对比明文密码
            if user.password == password and user.is_active:
                return user
        except User.DoesNotExist:
            return None
        return None

    def user_can_authenticate(self, user):
        """
        拒绝已禁用用户登录
        """
        return user.is_active

    def get_user(self, user_id):
        """获取用户"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
