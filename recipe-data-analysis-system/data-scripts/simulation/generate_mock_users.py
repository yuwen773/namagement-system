# -*- coding: utf-8 -*-
"""
模拟用户生成脚本

生成 100+ 模拟用户账号，用于系统测试和用户行为数据模拟。
"""

import os
import sys
import random
import json
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from accounts.models import User, UserProfile


class MockUserGenerator:
    """模拟用户生成器"""

    # 常用姓氏（前 100 个）
    SURNAMES = [
        '王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周',
        '徐', '孙', '马', '朱', '胡', '郭', '何', '罗', '高', '林',
        '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹',
        '彭', '曾', '萧', '田', '董', '袁', '潘', '于', '蒋', '蔡',
        '余', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈',
        '姚', '卢', '姜', '崔', '钟', '谭', '陆', '汪', '范', '金',
        '石', '廖', '贾', '夏', '韦', '付', '方', '白', '邹', '孟',
        '熊', '秦', '邱', '江', '尹', '薛', '闫', '段', '雷', '侯',
        '龙', '史', '陶', '黎', '贺', '顾', '毛', '郝', '龚', '邵'
    ]

    # 常用名字
    NAMES = [
        '伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋',
        '勇', '艳', '杰', '娟', '涛', '明', '超', '秀英', '霞', '平',
        '刚', '桂英', '玉兰', '萍', '毅', '浩', '宇', '轩', '然', '博',
        '文', '斌', '雨', '欣', '梦', '晗', '怡', '梓', '晨', '子涵',
        '诗涵', '一诺', '子轩', '欣怡', '梓涵', '浩宇', '宇轩', '浩然',
        '子墨', '宇航', '雨泽', '皓轩', '子豪', '一帆', '天宇', '俊杰',
        '晨', '浩然', '博文', '子轩', '一鸣', '宇航', '浩宇', '子涵',
        '欣怡', '诗涵', '梦洁', '雨桐', '雅琪', '梓萱', '紫萱', '思怡',
        '美', '秀兰', '桂花', '春梅', '秀珍', '华', '玉兰', '桂英', '萍'
    ]

    # 昵称形容词
    NICKNAME_PREFIXES = [
        '快乐', '美食', '幸福', '阳光', '吃货', '烹饪', '厨艺', '美味',
        '温暖', '热爱', '享受', '品味', '家常', '厨房', '小厨', '大厨',
        '美食家', '烹饪达人', '吃货', '美食爱好者', '厨师', '烘焙'
    ]

    NICKNAME_SUFFIXES = [
        '控', '达人', '爱好者', '大师', '高手', '小白', '新人', '粉丝',
        '之友', '王子', '公主', '宝宝', '小妹', '哥哥', '姐姐', '大叔'
    ]

    # 个人简介模板
    BIO_TEMPLATES = [
        "热爱美食，喜欢尝试各种菜谱。",
        "烹饪爱好者，喜欢在家研究新菜式。",
        "美食博主，分享日常美食制作。",
        "家常菜爱好者，追求简单美味的料理。",
        "喜欢收集和尝试各种菜谱。",
        "美食探索者，致力于发掘美味。",
        "烹饪让我快乐，享受美食的每一刻。",
        "厨房新手，正在努力学习烹饪。",
        "资深吃货，对美食有着独特的见解。",
        "简单烹饪，美味生活。",
        "爱做饭，爱分享，爱生活。",
        "用美食记录生活，用味道传递幸福。",
        "家常菜小能手，简简单单做美食。",
        "追求健康饮食，热爱自然食材。",
        "烹饪是生活的艺术，每一道菜都是作品。"
    ]

    # 邮箱域名
    EMAIL_DOMAINS = [
        'qq.com', '163.com', '126.com', 'gmail.com', 'outlook.com',
        'sina.com', 'hotmail.com', 'yahoo.com', 'yeah.net', 'foxmail.com'
    ]

    def __init__(self, count: int = 100):
        """
        初始化生成器

        Args:
            count: 要生成的用户数量
        """
        self.count = count
        self.generated_users = []
        self.used_usernames = set()
        self.used_emails = set()

        # 获取已存在的用户名，避免冲突
        existing_users = User.objects.values_list('username', flat=True)
        self.existing_usernames = set(existing_users)

        existing_emails = User.objects.exclude(email__isnull=True).values_list('email', flat=True)
        self.existing_emails = set(existing_emails)

    def _generate_username(self, index: int) -> str:
        """
        生成唯一的用户名

        Args:
            index: 当前用户的索引

        Returns:
            唯一的用户名
        """
        # 尝试多种方式生成用户名
        for _ in range(100):
            # 方法1: 姓氏 + 名字 + 数字
            if random.random() < 0.5:
                surname = random.choice(self.SURNAMES)
                name = random.choice(self.NAMES)
                suffix = random.randint(1, 9999)
                username = f"{surname}{name}{suffix}"
            # 方法2: mock_user_前缀
            else:
                username = f"mock_user_{index + 1}"

            # 检查是否已使用
            if username not in self.used_usernames and username not in self.existing_usernames:
                self.used_usernames.add(username)
                return username

        # 如果尝试多次仍有冲突，使用时间戳
        username = f"user_{datetime.now().timestamp()}_{index}"
        self.used_usernames.add(username)
        return username

    def _generate_email(self, username: str) -> str:
        """
        生成唯一的邮箱地址

        Args:
            username: 用户名（用于生成邮箱）

        Returns:
            唯一的邮箱地址
        """
        for _ in range(100):
            domain = random.choice(self.EMAIL_DOMAINS)
            # 添加随机数字以避免冲突
            random_num = random.randint(1, 99999)
            email = f"{username}{random_num}@{domain}"

            if email not in self.used_emails and email not in self.existing_emails:
                self.used_emails.add(email)
                return email

        # 如果仍有冲突，使用更长的随机数
        email = f"{username}_{random.randint(100000, 999999)}@{domain}"
        self.used_emails.add(email)
        return email

    def _generate_nickname(self, surname: str, name: str) -> str:
        """
        生成昵称

        Args:
            surname: 姓氏
            name: 名字

        Returns:
            生成的昵称
        """
        nickname_patterns = [
            lambda: f"{random.choice(self.NICKNAME_PREFIXES)}{random.choice(self.NICKNAME_SUFFIXES)}",
            lambda: f"{surname}{name}",
            lambda: f"{surname}小{name}",
            lambda: f"{random.choice(self.NICKNAME_PREFIXES)}的{surname}{name}",
            lambda: f"{random.choice(['小', '大'])}{surname}",
        ]

        return random.choice(nickname_patterns)()

    def _generate_password(self) -> str:
        """
        生成随机密码（明文存储，根据项目需求）

        Returns:
            生成的密码
        """
        # 根据项目需求，密码明文存储
        # 生成8-12位随机密码
        password_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        password_length = random.randint(8, 12)
        password = ''.join(random.choice(password_chars) for _ in range(password_length))
        return password

    def _generate_created_at(self, index: int, total: int) -> datetime:
        """
        生成创建时间，在过去一年内均匀分布

        Args:
            index: 当前用户的索引
            total: 总用户数

        Returns:
            创建时间
        """
        now = datetime.now()
        days_ago = 365
        # 按索引均匀分布在过去一年内
        days_offset = int((index / total) * days_ago)
        # 添加一些随机性（±10天）
        random_days = random.randint(-10, 10)
        # 随机时间（0-23小时）
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)

        created_at = now - timedelta(days=days_offset + random_days,
                                     hours=random_hours,
                                     minutes=random_minutes)
        return created_at

    def generate_user(self, index: int) -> dict:
        """
        生成单个用户数据

        Args:
            index: 当前用户的索引

        Returns:
            用户数据字典
        """
        # 生成基本信息
        surname = random.choice(self.SURNAMES)
        name = random.choice(self.NAMES)

        username = self._generate_username(index)
        password = self._generate_password()
        email = self._generate_email(username)
        nickname = self._generate_nickname(surname, name)
        bio = random.choice(self.BIO_TEMPLATES)

        # 创建时间
        created_at = self._generate_created_at(index, self.count)

        # 最后登录时间（在创建时间之后，有30%的概率从未登录）
        last_login = None
        if random.random() < 0.7:
            days_since_creation = (datetime.now() - created_at).days
            # 确保至少有1天的间隔，或者允许当天登录
            max_days = max(1, min(30, days_since_creation))
            days_after_creation = random.randint(0, max_days)
            last_login = created_at + timedelta(days=days_after_creation,
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))

        return {
            'username': username,
            'password': password,
            'email': email,
            'nickname': nickname,
            'bio': bio,
            'created_at': created_at,
            'last_login': last_login,
            'is_active': True,
            'role': 'user'
        }

    def generate_users(self) -> list:
        """
        批量生成用户数据

        Returns:
            用户数据列表
        """
        users = []
        for i in range(self.count):
            user_data = self.generate_user(i)
            users.append(user_data)

            if (i + 1) % 10 == 0:
                print(f"  已生成 {i + 1}/{self.count} 个用户...")

        return users

    def save_to_database(self, users_data: list) -> dict:
        """
        将用户数据保存到数据库

        Args:
            users_data: 用户数据列表

        Returns:
            保存结果统计
        """
        result = {
            'success': 0,
            'failed': 0,
            'user_ids': [],
            'errors': []
        }

        print(f"\n开始保存 {len(users_data)} 个用户到数据库...")

        for i, user_data in enumerate(users_data):
            try:
                # 提取各字段
                username = user_data.pop('username')
                password = user_data.pop('password')
                email = user_data.pop('email')
                nickname = user_data.pop('nickname', '')
                bio = user_data.pop('bio', '')
                created_at = user_data.pop('created_at')
                last_login = user_data.pop('last_login', None)
                is_active = user_data.pop('is_active', True)
                role = user_data.pop('role', 'user')

                # 创建用户（只传 User 模型的字段）
                user = User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    is_active=is_active,
                    role=role
                )

                # 手动设置创建时间
                user.created_at = created_at
                if last_login:
                    user.last_login = last_login
                user.save(update_fields=['created_at', 'last_login'])

                # 创建用户资料
                UserProfile.objects.create(
                    user=user,
                    nickname=nickname,
                    bio=bio
                )

                result['success'] += 1
                result['user_ids'].append(user.id)

                if (i + 1) % 10 == 0:
                    print(f"  已保存 {i + 1}/{len(users_data)} 个用户...")

            except Exception as e:
                result['failed'] += 1
                error_msg = f"用户 {user_data.get('username', 'unknown')}: {str(e)}"
                result['errors'].append(error_msg)
                print(f"  [错误] {error_msg}")

        return result

    def save_to_file(self, users_data: list, filename: str = None) -> str:
        """
        保存用户数据到 JSON 文件

        Args:
            users_data: 用户数据列表
            filename: 输出文件名

        Returns:
            保存的文件路径
        """
        output_dir = Path(__file__).parent.parent / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mock_users_{timestamp}.json"

        output_path = output_dir / filename

        # 序列化日期时间对象
        serializable_data = []
        for user in users_data:
            user_copy = user.copy()
            user_copy['created_at'] = user_copy['created_at'].isoformat()
            if user_copy['last_login']:
                user_copy['last_login'] = user_copy['last_login'].isoformat()
            serializable_data.append(user_copy)

        output_data = {
            'metadata': {
                'total': len(users_data),
                'generated_at': datetime.now().isoformat(),
                'source': 'mock_user_generator'
            },
            'users': serializable_data
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        return str(output_path)


def main():
    """主函数"""
    print("=" * 60)
    print("模拟用户生成脚本")
    print("=" * 60)

    # 配置生成参数
    USER_COUNT = 100
    SAVE_TO_DB = True
    SAVE_TO_FILE = True

    print(f"\n配置:")
    print(f"  - 生成用户数量: {USER_COUNT}")
    print(f"  - 保存到数据库: {'是' if SAVE_TO_DB else '否'}")
    print(f"  - 保存到文件: {'是' if SAVE_TO_FILE else '否'}")

    # 创建生成器
    generator = MockUserGenerator(count=USER_COUNT)

    # 生成用户数据
    print(f"\n开始生成 {USER_COUNT} 个模拟用户...")
    users_data = generator.generate_users()
    print(f"[OK] 用户数据生成完成")

    # 保存到文件
    output_file = None
    if SAVE_TO_FILE:
        print(f"\n保存到文件...")
        output_file = generator.save_to_file(users_data)
        print(f"[OK] 数据已保存到: {output_file}")

    # 保存到数据库
    db_result = None
    if SAVE_TO_DB:
        db_result = generator.save_to_database(users_data)
        print(f"\n数据库保存完成:")
        print(f"  成功: {db_result['success']} 个")
        print(f"  失败: {db_result['failed']} 个")

        if db_result['user_ids']:
            print(f"\n生成的用户 ID 范围: {min(db_result['user_ids'])} - {max(db_result['user_ids'])}")

        if db_result['errors']:
            print(f"\n错误信息:")
            for error in db_result['errors'][:5]:  # 只显示前5个错误
                print(f"  - {error}")
            if len(db_result['errors']) > 5:
                print(f"  ... 还有 {len(db_result['errors']) - 5} 个错误")

    print("\n" + "=" * 60)
    print("[OK] 模拟用户生成完成！")
    print("=" * 60)

    # 验证结果
    total_users = User.objects.count()
    print(f"\n当前数据库总用户数: {total_users}")


if __name__ == "__main__":
    main()
