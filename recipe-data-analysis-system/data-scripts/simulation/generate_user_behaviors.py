# -*- coding: utf-8 -*-
"""
用户行为模拟脚本

为模拟用户生成真实的行为数据，包括：
- 登录行为
- 搜索行为
- 浏览菜谱行为
- 收藏菜谱行为

行为时间分布在过去30天内，模拟真实用户活跃模式。
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from accounts.models import User
from recipes.models import Recipe
from behavior_logs.models import UserBehaviorLog


class BehaviorSimulator:
    """用户行为模拟器"""

    # 行为类型常量
    BEHAVIOR_LOGIN = 'login'
    BEHAVIOR_SEARCH = 'search'
    BEHAVIOR_VIEW = 'view'
    BEHAVIOR_FAVORITE = 'favorite'

    # 行为类型列表
    BEHAVIOR_TYPES = [BEHAVIOR_LOGIN, BEHAVIOR_SEARCH, BEHAVIOR_VIEW, BEHAVIOR_FAVORITE]

    # 搜索关键词（常见菜谱名称和食材）
    SEARCH_KEYWORDS = [
        '红烧肉', '宫保鸡丁', '糖醋排骨', '麻婆豆腐', '鱼香肉丝',
        '西红柿炒鸡蛋', '土豆炖牛肉', '可乐鸡翅', '蒜蓉西兰花', '清蒸鱼',
        '红烧茄子', '回锅肉', '水煮鱼', '蒸蛋羹', '凉拌黄瓜',
        '蛋炒饭', '手擀面', '饺子', '包子', '馒头',
        '蛋糕', '饼干', '面包', '披萨', '意面',
        '沙拉', '汤', '粥', '炖菜', '烧烤'
    ]

    # 页面路径
    PAGE_PATHS = [
        '/', '/recipes', '/recipes/', '/hot', '/category/',
        '/login', '/register', '/profile'
    ]

    # 用户活跃时段权重（白天更活跃）
    HOUR_WEIGHTS = {
        0: 5, 1: 3, 2: 2, 3: 1, 4: 1, 5: 2,
        6: 10, 7: 25, 8: 30, 9: 25, 10: 20, 11: 25,
        12: 30, 13: 20, 14: 20, 15: 25, 16: 30, 17: 35,
        18: 40, 19: 35, 20: 30, 21: 25, 22: 20, 23: 15
    }

    def __init__(self, behaviors_per_user_min: int = 20, behaviors_per_user_max: int = 100):
        """
        初始化行为模拟器

        Args:
            behaviors_per_user_min: 每个用户最少行为数
            behaviors_per_user_max: 每个用户最多行为数
        """
        self.behaviors_per_user_min = behaviors_per_user_min
        self.behaviors_per_user_max = behaviors_per_user_max

        # 获取所有模拟用户
        from django.db.models import Q
        self.users = list(User.objects.filter(
            Q(username__startswith='mock_user_') | Q(id__gte=31)
        ).distinct())

        # 获取所有菜谱
        self.recipes = list(Recipe.objects.all())

        # 统计信息
        self.stats = {
            'total_users': len(self.users),
            'total_recipes': len(self.recipes),
            'behaviors_generated': 0,
            'behaviors_by_type': {bt: 0 for bt in self.BEHAVIOR_TYPES},
            'login_count': 0,
            'search_count': 0,
            'view_count': 0,
            'favorite_count': 0,
            'view_updates': 0,
            'favorite_updates': 0
        }

    def _get_random_behavior_time(self, days_range: int = 30) -> datetime:
        """
        生成随机的行为时间

        Args:
            days_range: 过去天数

        Returns:
            行为时间
        """
        now = datetime.now()
        # 随机选择天数（过去days_range天内）
        days_ago = random.randint(0, days_range - 1)
        # 根据权重选择小时
        hours = list(self.HOUR_WEIGHTS.keys())
        weights = list(self.HOUR_WEIGHTS.values())
        hour = random.choices(hours, weights=weights)[0]
        # 随机选择分钟和秒
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        behavior_time = now - timedelta(
            days=days_ago,
            hours=hour if hour > now.hour else 0,
            minutes=minute,
            seconds=second
        )

        return behavior_time

    def _get_random_search_keyword(self) -> str:
        """获取随机搜索关键词"""
        return random.choice(self.SEARCH_KEYWORDS)

    def _get_random_ip(self) -> str:
        """生成随机IP地址"""
        return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    def _get_random_user_agent(self) -> str:
        """生成随机User-Agent"""
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
        os_list = ['Windows NT 10.0', 'Macintosh', 'Linux x86_64', 'Android 10']
        browser = random.choice(browsers)
        os_str = random.choice(os_list)

        if browser == 'Chrome':
            version = f"{random.randint(100, 120)}.0.{random.randint(4000, 5000)}.0"
            return f"Mozilla/5.0 ({os_str}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
        elif browser == 'Firefox':
            version = random.randint(100, 120)
            return f"Mozilla/5.0 ({os_str}; rv:{version}.0) Gecko/20100101 Firefox/{version}.0"
        elif browser == 'Safari':
            version = random.randint(15, 17)
            return f"Mozilla/5.0 ({os_str}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version}.0 Safari/605.1.15"
        else:  # Edge
            version = f"{random.randint(100, 120)}.0.{random.randint(0, 9999)}.0"
            return f"Mozilla/5.0 ({os_str}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36 Edg/{version}.0"

    def simulate_login(self, user: User, timestamp: datetime) -> dict:
        """
        模拟登录行为

        Args:
            user: 用户对象
            timestamp: 行为时间

        Returns:
            行为数据字典
        """
        return {
            'user': user,
            'behavior_type': self.BEHAVIOR_LOGIN,
            'target': None,
            'timestamp': timestamp,
            'extra_data': {
                'login_method': random.choice(['password', 'remember_token']),
                'login_device': random.choice(['desktop', 'mobile', 'tablet']),
                'login_result': 'success'
            },
            'ip_address': self._get_random_ip(),
            'user_agent': self._get_random_user_agent()
        }

    def simulate_search(self, user: User, timestamp: datetime) -> dict:
        """
        模拟搜索行为

        Args:
            user: 用户对象
            timestamp: 行为时间

        Returns:
            行为数据字典
        """
        keyword = self._get_random_search_keyword()
        search_result_count = random.randint(0, 50)  # 搜索结果数量

        return {
            'user': user,
            'behavior_type': self.BEHAVIOR_SEARCH,
            'target': f"/api/recipes/search/?keyword={keyword}",
            'timestamp': timestamp,
            'extra_data': {
                'keyword': keyword,
                'results_count': search_result_count,
                'search_page': random.randint(1, 5)
            },
            'ip_address': self._get_random_ip(),
            'user_agent': self._get_random_user_agent()
        }

    def simulate_view(self, user: User, timestamp: datetime) -> dict:
        """
        模拟浏览菜谱行为

        Args:
            user: 用户对象
            timestamp: 行为时间

        Returns:
            行为数据字典
        """
        if not self.recipes:
            return None

        recipe = random.choice(self.recipes)
        stay_duration = random.randint(30, 300)  # 停留30秒到5分钟

        return {
            'user': user,
            'behavior_type': self.BEHAVIOR_VIEW,
            'target': str(recipe.id),
            'timestamp': timestamp,
            'extra_data': {
                'recipe_name': recipe.name,
                'cuisine_type': recipe.cuisine_type,
                'difficulty': recipe.difficulty,
                'stay_duration': stay_duration,  # 停留时长（秒）
                'scroll_depth': random.randint(50, 100)  # 滚动深度百分比
            },
            'ip_address': self._get_random_ip(),
            'user_agent': self._get_random_user_agent(),
            'recipe_id': recipe.id  # 用于更新点击量
        }

    def simulate_favorite(self, user: User, timestamp: datetime, view_timestamp: datetime = None) -> dict:
        """
        模拟收藏菜谱行为

        Args:
            user: 用户对象
            timestamp: 行为时间
            view_timestamp: 浏览时间（可选，用于模拟先浏览后收藏）

        Returns:
            行为数据字典
        """
        if not self.recipes:
            return None

        recipe = random.choice(self.recipes)

        return {
            'user': user,
            'behavior_type': self.BEHAVIOR_FAVORITE,
            'target': str(recipe.id),
            'timestamp': timestamp,
            'extra_data': {
                'recipe_name': recipe.name,
                'source_page': random.choice(['recipe_detail', 'recipe_list', 'search_result']),
                'action_time': random.randint(1, 10)  # 从浏览到收藏的操作时间（秒）
            },
            'ip_address': self._get_random_ip(),
            'user_agent': self._get_random_user_agent(),
            'recipe_id': recipe.id  # 用于更新收藏量
        }

    def generate_behaviors_for_user(self, user: User) -> list:
        """
        为单个用户生成行为数据

        Args:
            user: 用户对象

        Returns:
            行为数据列表
        """
        behaviors = []
        behavior_count = random.randint(self.behaviors_per_user_min, self.behaviors_per_user_max)

        # 行为类型分布权重
        # 登录: 5%, 搜索: 20%, 浏览: 60%, 收藏: 15%
        type_weights = [5, 20, 60, 15]

        # 生成行为时间列表（按时间顺序）
        now = datetime.now()
        days_range = 30
        timestamps = []

        for _ in range(behavior_count):
            timestamp = self._get_random_behavior_time(days_range)
            timestamps.append(timestamp)

        timestamps.sort()  # 按时间排序

        # 生成各类行为
        for timestamp in timestamps:
            behavior_type = random.choices(self.BEHAVIOR_TYPES, weights=type_weights)[0]

            if behavior_type == self.BEHAVIOR_LOGIN:
                behavior = self.simulate_login(user, timestamp)
            elif behavior_type == self.BEHAVIOR_SEARCH:
                behavior = self.simulate_search(user, timestamp)
            elif behavior_type == self.BEHAVIOR_VIEW:
                behavior = self.simulate_view(user, timestamp)
            else:  # favorite
                # 收藏前先浏览（随机选择过去的时间点）
                view_offset = random.randint(1, 1440)  # 1分钟到24小时前
                view_timestamp = timestamp - timedelta(minutes=view_offset)
                behavior = self.simulate_favorite(user, timestamp, view_timestamp)

            if behavior:
                behaviors.append(behavior)
                self.stats['behaviors_by_type'][behavior_type] += 1

        return behaviors

    def save_behaviors(self, behaviors: list) -> dict:
        """
        保存行为数据到数据库

        Args:
            behaviors: 行为数据列表

        Returns:
            保存结果统计
        """
        result = {
            'success': 0,
            'failed': 0,
            'view_updates': 0,
            'favorite_updates': 0,
            'errors': []
        }

        # 用于批量更新菜谱点击量和收藏量
        view_updates = {}
        favorite_updates = {}

        for i, behavior in enumerate(behaviors):
            try:
                # 提取菜谱ID用于更新统计
                recipe_id = behavior.pop('recipe_id', None)

                # 创建行为日志
                UserBehaviorLog.objects.create(
                    user=behavior['user'],
                    behavior_type=behavior['behavior_type'],
                    target=behavior['target'],
                    timestamp=behavior['timestamp'],
                    extra_data=behavior['extra_data'],
                    ip_address=behavior['ip_address'],
                    user_agent=behavior['user_agent']
                )

                # 统计点击和收藏用于更新菜谱
                if recipe_id:
                    if behavior['behavior_type'] == self.BEHAVIOR_VIEW:
                        view_updates[recipe_id] = view_updates.get(recipe_id, 0) + 1
                    elif behavior['behavior_type'] == self.BEHAVIOR_FAVORITE:
                        favorite_updates[recipe_id] = favorite_updates.get(recipe_id, 0) + 1

                result['success'] += 1

            except Exception as e:
                result['failed'] += 1
                result['errors'].append(f"行为 {i}: {str(e)}")

        # 批量更新菜谱点击量
        for recipe_id, count in view_updates.items():
            try:
                Recipe.objects.filter(id=recipe_id).update(
                    view_count=models.F('view_count') + count
                )
                result['view_updates'] += 1
            except Exception as e:
                result['errors'].append(f"更新点击量失败 (recipe_id={recipe_id}): {str(e)}")

        # 批量更新菜谱收藏量
        for recipe_id, count in favorite_updates.items():
            try:
                Recipe.objects.filter(id=recipe_id).update(
                    favorite_count=models.F('favorite_count') + count
                )
                result['favorite_updates'] += 1
            except Exception as e:
                result['errors'].append(f"更新收藏量失败 (recipe_id={recipe_id}): {str(e)}")

        return result

    def run(self) -> dict:
        """
        运行行为模拟

        Returns:
            模拟结果统计
        """
        print("=" * 60)
        print("用户行为模拟脚本")
        print("=" * 60)

        print(f"\n配置:")
        print(f"  - 模拟用户数: {self.stats['total_users']}")
        print(f"  - 可用菜谱数: {self.stats['total_recipes']}")
        print(f"  - 每用户最少行为: {self.behaviors_per_user_min}")
        print(f"  - 每用户最多行为: {self.behaviors_per_user_max}")

        if not self.users:
            print("\n[错误] 没有找到模拟用户，请先运行 generate_mock_users.py")
            return self.stats

        if not self.recipes:
            print("\n[错误] 没有找到菜谱数据，请先导入菜谱数据")
            return self.stats

        print(f"\n开始生成用户行为数据...")
        all_behaviors = []

        for i, user in enumerate(self.users):
            behaviors = self.generate_behaviors_for_user(user)
            all_behaviors.extend(behaviors)

            if (i + 1) % 10 == 0:
                print(f"  已处理 {i + 1}/{len(self.users)} 个用户，生成了 {len(all_behaviors)} 条行为记录...")

        print(f"\n共生成 {len(all_behaviors)} 条行为记录")

        # 保存到数据库
        print("\n保存行为数据到数据库...")
        result = self.save_behaviors(all_behaviors)

        print(f"\n数据库保存结果:")
        print(f"  成功: {result['success']} 条")
        print(f"  失败: {result['failed']} 条")
        print(f"  更新点击量: {result['view_updates']} 个菜谱")
        print(f"  更新收藏量: {result['favorite_updates']} 个菜谱")

        # 更新统计信息
        self.stats['behaviors_generated'] = result['success']
        self.stats['login_count'] = self.stats['behaviors_by_type'][self.BEHAVIOR_LOGIN]
        self.stats['search_count'] = self.stats['behaviors_by_type'][self.BEHAVIOR_SEARCH]
        self.stats['view_count'] = self.stats['behaviors_by_type'][self.BEHAVIOR_VIEW]
        self.stats['favorite_count'] = self.stats['behaviors_by_type'][self.BEHAVIOR_FAVORITE]
        self.stats['view_updates'] = result['view_updates']
        self.stats['favorite_updates'] = result['favorite_updates']

        # 打印行为分布
        print(f"\n行为类型分布:")
        for bt in self.BEHAVIOR_TYPES:
            count = self.stats['behaviors_by_type'][bt]
            pct = count / max(self.stats['behaviors_generated'], 1) * 100
            print(f"  - {bt}: {count} ({pct:.1f}%)")

        if result['errors']:
            print(f"\n错误信息（前5条）:")
            for error in result['errors'][:5]:
                print(f"  - {error}")

        print("\n" + "=" * 60)
        print("[OK] 用户行为模拟完成！")
        print("=" * 60)

        # 验证结果
        total_logs = UserBehaviorLog.objects.count()
        print(f"\n当前数据库行为日志总数: {total_logs}")

        return self.stats


def main():
    """主函数"""
    # 配置参数
    BEHAVIORS_PER_USER_MIN = 20  # 每个用户最少20条行为
    BEHAVIORS_PER_USER_MAX = 100  # 每个用户最多100条行为

    # 创建模拟器并运行
    simulator = BehaviorSimulator(
        behaviors_per_user_min=BEHAVIORS_PER_USER_MIN,
        behaviors_per_user_max=BEHAVIORS_PER_USER_MAX
    )
    simulator.run()


if __name__ == "__main__":
    # 导入 F 表达式（需要在 django.setup() 之后）
    from django.db import models
    main()
