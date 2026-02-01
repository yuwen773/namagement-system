# -*- coding: utf-8 -*-
"""
页面访问模拟脚本

为模拟用户生成页面访问行为数据，包括：
- 首页访问
- 菜谱列表页访问
- 菜谱详情页访问
- 分类页访问
- 热门页访问
- 计算页面停留时间
- 记录访问路径（模拟点击流）

页面访问记录的行为类型为 'page_view'，extra_data 中包含停留时长和访问路径信息。
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / 'backend'))

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import models
from accounts.models import User
from recipes.models import Recipe
from behavior_logs.models import UserBehaviorLog


class PageVisitSimulator:
    """页面访问模拟器"""

    # 行为类型常量
    BEHAVIOR_PAGE_VIEW = 'page_view'

    # 页面路径定义
    PAGE_PATHS = {
        'home': '/',
        'recipe_list': '/recipes',
        'recipe_detail': '/recipes/',
        'category': '/category/',
        'hot': '/hot',
        'ingredients_frequency': '/ingredients-frequency',
        'analytics': '/analytics',
        'login': '/login',
        'register': '/register',
    }

    # 页面停留时间范围（秒）
    PAGE_STAY_DURATIONS = {
        'home': (5, 30),           # 首页：5-30秒
        'recipe_list': (15, 60),   # 列表页：15-60秒
        'recipe_detail': (30, 180),# 详情页：30秒-3分钟（阅读菜谱）
        'category': (10, 45),      # 分类页：10-45秒
        'hot': (15, 60),           # 热门页：15-60秒
        'ingredients_frequency': (20, 90),   # 食材频率页：20-90秒
        'analytics': (30, 120),    # 数据分析页：30秒-2分钟
        'login': (5, 20),          # 登录页：5-20秒
        'register': (10, 30),      # 注册页：10-30秒
    }

    # 页面访问权重（更可能访问的页面）
    PAGE_WEIGHTS = {
        'home': 30,
        'recipe_list': 25,
        'recipe_detail': 40,
        'category': 15,
        'hot': 20,
        'ingredients_frequency': 10,
        'analytics': 5,
        'login': 5,
        'register': 3,
    }

    # 用户活跃时段权重（白天更活跃）
    HOUR_WEIGHTS = {
        0: 3, 1: 2, 2: 1, 3: 1, 4: 2, 5: 5,
        6: 15, 7: 30, 8: 35, 9: 30, 10: 25, 11: 30,
        12: 35, 13: 25, 14: 25, 15: 30, 16: 35, 17: 40,
        18: 45, 19: 40, 20: 35, 21: 30, 22: 25, 23: 15
    }

    # 常见访问路径模式
    PATH_PATTERNS = [
        ['home', 'recipe_list', 'recipe_detail', 'hot'],
        ['home', 'recipe_list', 'category', 'recipe_detail'],
        ['home', 'hot', 'recipe_detail'],
        ['home', 'recipe_list', 'recipe_detail', 'recipe_detail'],
        ['home', 'category', 'recipe_list', 'recipe_detail'],
        ['home', 'hot'],
        ['home', 'ingredients_frequency', 'recipe_list', 'recipe_detail'],
        ['home', 'analytics', 'recipe_list'],
        ['home', 'recipe_list'],
        ['recipe_detail', 'recipe_list', 'recipe_detail'],
    ]

    def __init__(self, visits_per_user_min: int = 10, visits_per_user_max: int = 50):
        """
        初始化页面访问模拟器

        Args:
            visits_per_user_min: 每个用户最少页面访问次数
            visits_per_user_max: 每个用户最多页面访问次数
        """
        self.visits_per_user_min = visits_per_user_min
        self.visits_per_user_max = visits_per_user_max

        # 获取所有模拟用户
        from django.db.models import Q
        self.users = list(User.objects.filter(
            Q(username__startswith='mock_user_') | Q(id__gte=31)
        ).distinct())

        # 获取所有菜谱（用于详情页访问）
        self.recipes = list(Recipe.objects.all())

        # 统计信息
        self.stats = {
            'total_users': len(self.users),
            'total_recipes': len(self.recipes),
            'visits_generated': 0,
            'visits_by_page': {},
            'avg_stay_duration': 0,
            'path_patterns_found': 0,
        }

        # 初始化页面访问统计
        for page in self.PAGE_PATHS.keys():
            self.stats['visits_by_page'][page] = 0

    def _get_random_visit_time(self, days_range: int = 30) -> datetime:
        """
        生成随机的访问时间

        Args:
            days_range: 过去天数

        Returns:
            访问时间
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

        visit_time = now - timedelta(
            days=days_ago,
            hours=hour if hour > now.hour else 0,
            minutes=minute,
            seconds=second
        )

        return visit_time

    def _get_random_stay_duration(self, page_type: str) -> int:
        """
        获取随机停留时间

        Args:
            page_type: 页面类型

        Returns:
            停留时间（秒）
        """
        duration_range = self.PAGE_STAY_DURATIONS.get(page_type, (10, 60))
        return random.randint(duration_range[0], duration_range[1])

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

    def _get_page_path(self, page_type: str, recipe_id: int = None, category_value: str = None) -> str:
        """
        获取完整页面路径

        Args:
            page_type: 页面类型
            recipe_id: 菜谱ID（用于详情页）
            category_value: 分类值（用于分类页）

        Returns:
            完整页面路径
        """
        base_path = self.PAGE_PATHS.get(page_type, '/')

        if page_type == 'recipe_detail' and recipe_id:
            return f"{base_path}{recipe_id}"
        elif page_type == 'category' and category_value:
            return f"{base_path}{category_value}"
        else:
            return base_path

    def _generate_visit_path(self) -> list:
        """
        生成访问路径（模拟点击流）

        Returns:
            页面访问序列
        """
        # 30%概率使用预定义路径模式
        if random.random() < 0.3:
            pattern = random.choice(self.PATH_PATTERNS)
            path = pattern.copy()
        else:
            # 生成随机路径
            path_length = random.randint(2, 6)
            path = []
            page_types = list(self.PAGE_WEIGHTS.keys())
            weights = list(self.PAGE_WEIGHTS.values())

            prev_page = None
            for _ in range(path_length):
                # 选择页面类型
                if prev_page == 'home' and random.random() < 0.7:
                    # 从首页后，更可能进入列表页或详情页
                    page = random.choices(['recipe_list', 'recipe_detail', 'hot', 'category'], weights=[30, 40, 15, 15])[0]
                elif prev_page == 'recipe_list' and random.random() < 0.6:
                    # 从列表页后，更可能进入详情页
                    page = random.choices(['recipe_detail', 'category', 'recipe_list'], weights=[50, 20, 30])[0]
                elif prev_page == 'recipe_detail' and random.random() < 0.5:
                    # 从详情页后，可能继续浏览或返回列表
                    page = random.choices(['recipe_list', 'recipe_detail', 'hot'], weights=[40, 35, 25])[0]
                else:
                    page = random.choices(page_types, weights=weights)[0]
                path.append(page)
                prev_page = page

        return path

    def _generate_session_visits(self, user: User, session_start: datetime) -> list:
        """
        生成单个会话的页面访问记录

        Args:
            user: 用户对象
            session_start: 会话开始时间

        Returns:
            页面访问记录列表
        """
        visits = []
        path = self._generate_visit_path()
        current_time = session_start

        for i, page_type in enumerate(path):
            # 计算停留时间
            stay_duration = self._get_random_stay_duration(page_type)

            # 生成页面访问数据
            visit_data = {
                'user': user,
                'behavior_type': self.BEHAVIOR_PAGE_VIEW,
                'target': None,  # 稍后填充
                'timestamp': current_time,
                'extra_data': {
                    'page_type': page_type,
                    'stay_duration': stay_duration,
                    'session_position': i + 1,
                    'path_length': len(path),
                },
                'ip_address': self._get_random_ip(),
                'user_agent': self._get_random_user_agent(),
            }

            # 设置目标路径
            if page_type == 'recipe_detail':
                recipe = random.choice(self.recipes) if self.recipes else None
                if recipe:
                    visit_data['target'] = self._get_page_path('recipe_detail', recipe.id)
                    visit_data['extra_data']['recipe_id'] = recipe.id
                    visit_data['extra_data']['recipe_name'] = recipe.name
                else:
                    visit_data['target'] = self._get_page_path('recipe_detail', 1)
            elif page_type == 'category':
                category_types = ['cuisine', 'scene', 'crowd', 'taste']
                category_type = random.choice(category_types)
                category_values = {
                    'cuisine': ['川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '闽菜', '湘菜', '徽菜'],
                    'scene': ['早餐', '午餐', '晚餐', '夜宵', '下午茶'],
                    'crowd': ['单人', '二人世界', '家庭聚餐', '朋友聚会'],
                    'taste': ['辣', '清淡', '甜', '酸', '咸'],
                }
                category_value = random.choice(category_values.get(category_type, ['川菜']))
                visit_data['target'] = self._get_page_path('category', category_value=category_value)
                visit_data['extra_data']['category_type'] = category_type
                visit_data['extra_data']['category_value'] = category_value
            else:
                visit_data['target'] = self._get_page_path(page_type)

            visits.append(visit_data)

            # 更新时间（加上停留时间）
            current_time += timedelta(seconds=stay_duration + random.randint(1, 10))

        return visits

    def generate_visits_for_user(self, user: User) -> list:
        """
        为单个用户生成页面访问数据

        Args:
            user: 用户对象

        Returns:
            页面访问记录列表
        """
        visits = []
        # 每个用户生成1-3个会话
        session_count = random.randint(1, 3)

        for _ in range(session_count):
            # 生成会话开始时间
            session_start = self._get_random_visit_time(30)
            session_visits = self._generate_session_visits(user, session_start)
            visits.extend(session_visits)

        return visits

    def save_visits(self, visits: list) -> dict:
        """
        保存页面访问数据到数据库

        Args:
            visits: 页面访问数据列表

        Returns:
            保存结果统计
        """
        result = {
            'success': 0,
            'failed': 0,
            'errors': []
        }

        for i, visit in enumerate(visits):
            try:
                UserBehaviorLog.objects.create(
                    user=visit['user'],
                    behavior_type=visit['behavior_type'],
                    target=visit['target'],
                    timestamp=visit['timestamp'],
                    extra_data=visit['extra_data'],
                    ip_address=visit['ip_address'],
                    user_agent=visit['user_agent']
                )

                # 统计页面访问
                page_type = visit['extra_data'].get('page_type')
                if page_type:
                    self.stats['visits_by_page'][page_type] = self.stats['visits_by_page'].get(page_type, 0) + 1

                result['success'] += 1

            except Exception as e:
                result['failed'] += 1
                result['errors'].append(f"访问记录 {i}: {str(e)}")

        return result

    def run(self) -> dict:
        """
        运行页面访问模拟

        Returns:
            模拟结果统计
        """
        print("=" * 60)
        print("页面访问模拟脚本")
        print("=" * 60)

        print(f"\n配置:")
        print(f"  - 模拟用户数: {self.stats['total_users']}")
        print(f"  - 可用菜谱数: {self.stats['total_recipes']}")
        print(f"  - 每用户最少访问: {self.visits_per_user_min}")
        print(f"  - 每用户最多访问: {self.visits_per_user_max}")

        if not self.users:
            print("\n[错误] 没有找到模拟用户，请先运行 generate_mock_users.py")
            return self.stats

        print(f"\n开始生成页面访问数据...")
        all_visits = []

        for i, user in enumerate(self.users):
            visits = self.generate_visits_for_user(user)
            all_visits.extend(visits)

            if (i + 1) % 10 == 0:
                print(f"  已处理 {i + 1}/{len(self.users)} 个用户，生成了 {len(all_visits)} 条访问记录...")

        print(f"\n共生成 {len(all_visits)} 条页面访问记录")

        # 保存到数据库
        print("\n保存页面访问数据到数据库...")
        result = self.save_visits(all_visits)

        print(f"\n数据库保存结果:")
        print(f"  成功: {result['success']} 条")
        print(f"  失败: {result['failed']} 条")

        # 更新统计信息
        self.stats['visits_generated'] = result['success']

        # 计算平均停留时间
        total_duration = sum(
            visit['extra_data'].get('stay_duration', 0)
            for visit in all_visits
            if 'extra_data' in visit and visit['extra_data']
        )
        self.stats['avg_stay_duration'] = total_duration / max(len(all_visits), 1)

        # 打印页面访问分布
        print(f"\n页面访问分布:")
        for page_type, count in self.stats['visits_by_page'].items():
            pct = count / max(self.stats['visits_generated'], 1) * 100
            print(f"  - {page_type}: {count} ({pct:.1f}%)")

        print(f"\n平均停留时间: {self.stats['avg_stay_duration']:.1f} 秒")

        if result['errors']:
            print(f"\n错误信息（前5条）:")
            for error in result['errors'][:5]:
                print(f"  - {error}")

        print("\n" + "=" * 60)
        print("[OK] 页面访问模拟完成！")
        print("=" * 60)

        # 验证结果
        page_view_count = UserBehaviorLog.objects.filter(behavior_type='page_view').count()
        print(f"\n当前数据库 page_view 行为日志总数: {page_view_count}")

        return self.stats


def main():
    """主函数"""
    # 配置参数
    VISITS_PER_USER_MIN = 10   # 每个用户最少10次页面访问
    VISITS_PER_USER_MAX = 50   # 每个用户最多50次页面访问

    # 创建模拟器并运行
    simulator = PageVisitSimulator(
        visits_per_user_min=VISITS_PER_USER_MIN,
        visits_per_user_max=VISITS_PER_USER_MAX
    )
    simulator.run()


if __name__ == "__main__":
    main()
