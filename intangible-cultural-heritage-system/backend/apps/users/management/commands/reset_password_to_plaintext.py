"""
Django 管理命令：重置用户密码为明文

使用方法:
    python manage.py reset_password_to_plaintext
    python manage.py reset_password_to_plaintext --username admin
    python manage.py reset_password_to_plaintext --password newpass123

警告: 仅用于开发/测试环境，切勿用于生产环境
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = '重置用户密码为明文格式（开发环境专用）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='指定要重置密码的用户名（不指定则重置所有用户）',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='password123',
            help='设置的新密码（默认: password123）',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        new_password = options.get('password', 'password123')

        if username:
            # 重置指定用户
            try:
                user = User.objects.get(username=username)
                user.password = new_password
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] 用户 "{username}" 密码已重置为明文: "{new_password}"')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] 用户 "{username}" 不存在')
                )
        else:
            # 重置所有用户
            count = User.objects.count()
            for user in User.objects.all():
                user.password = new_password
                user.save()

            self.stdout.write(
                self.style.SUCCESS(f'[OK] 已将 {count} 个用户的密码重置为明文: "{new_password}"')
            )

        self.stdout.write(
            self.style.WARNING('[WARNING] 密码以明文存储，仅适用于开发/测试环境！')
        )
