"""
创建管理员账号的 Django 管理命令

用法:
    python manage.py create_admin
    python manage.py create_admin --username admin --password admin123
"""

from django.core.management.base import BaseCommand, CommandError
from accounts.models import User


class Command(BaseCommand):
    help = '创建系统管理员账号'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='管理员账号 (默认: admin)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='管理员密码 (默认: admin123)'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        # 检查账号是否已存在
        if User.objects.filter(username=username).exists():
            existing_user = User.objects.get(username=username)
            if existing_user.role == User.Role.ADMIN:
                self.stdout.write(
                    self.style.WARNING(f'管理员账号 "{username}" 已存在')
                )
                self.stdout.write(f'  账号: {username}')
                self.stdout.write(f'  密码: {existing_user.password} (开发阶段明文存储)')
                return
            else:
                # 如果是普通员工账号，询问是否升级为管理员
                self.stdout.write(
                    self.style.WARNING(f'账号 "{username}" 已存在，但角色是普通员工')
                )
                response = input('是否将该账号升级为管理员? (y/n): ')
                if response.lower() == 'y':
                    existing_user.role = User.Role.ADMIN
                    existing_user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'账号 "{username}" 已升级为管理员')
                    )
                    return
                else:
                    self.stdout.write(self.style.ERROR('操作已取消'))
                    return

        # 创建新管理员账号
        try:
            admin = User.objects.create(
                username=username,
                password=password,  # 开发阶段明文存储
                role=User.Role.ADMIN,
                status=User.Status.ENABLED
            )
            self.stdout.write(
                self.style.SUCCESS('[SUCCESS] 管理员账号创建成功!')
            )
            self.stdout.write(f'  账号: {admin.username}')
            self.stdout.write(f'  密码: {admin.password}')
            self.stdout.write(f'  角色: {admin.get_role_display()}')
            self.stdout.write(f'  状态: {admin.get_status_display()}')
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('[WARNING] 注意: 开发阶段密码为明文存储，生产环境请使用加密存储'))
        except Exception as e:
            raise CommandError(f'创建管理员账号失败: {e}')
