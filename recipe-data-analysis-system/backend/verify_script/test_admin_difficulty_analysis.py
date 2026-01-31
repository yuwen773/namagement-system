"""
管理员难度深度分析接口测试脚本

测试阶段十五第2步：难度深度分析接口

测试场景：
1. 无权限访问测试（未登录）
2. 普通用户权限测试（无管理员权限）
3. 管理员访问测试（正常场景）
4. 数据完整性验证
5. 数据准确性验证
"""

import os
import sys
import django
import json

# 设置输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from recipes.models import Recipe

User = get_user_model()


class AdminDifficultyAnalysisTester:
    """管理员难度深度分析接口测试类"""

    def __init__(self):
        self.client = APIClient()
        self.base_url = '/api/admin/analytics/difficulty/'
        self.admin_user = None
        self.regular_user = None
        self.admin_token = None

    def setup_users(self):
        """创建测试用户"""
        print("=" * 60)
        print("1. 设置测试用户")
        print("=" * 60)

        # 删除已存在的测试用户
        User.objects.filter(username__in=['test_admin', 'test_user']).delete()

        # 创建管理员用户
        self.admin_user = User.objects.create_user(
            username='test_admin',
            password='admin123',
            email='admin@test.com',
            role='admin'
        )
        print(f"✓ 创建管理员用户: {self.admin_user.username} (role={self.admin_user.role})")

        # 创建普通用户
        self.regular_user = User.objects.create_user(
            username='test_user',
            password='user123',
            email='user@test.com',
            role='user'
        )
        print(f"✓ 创建普通用户: {self.regular_user.username} (role={self.regular_user.role})")

        # 获取管理员 token
        response = self.client.post('/api/accounts/login/', {
            'username': 'test_admin',
            'password': 'admin123'
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                self.admin_token = data['data']['token']
                print(f"✓ 获取管理员 Token 成功")
        print()

    def test_unauthorized_access(self):
        """测试未登录访问"""
        print("=" * 60)
        print("2. 测试未登录访问（应返回401）")
        print("=" * 60)

        self.client.force_authenticate(user=None)
        response = self.client.get(self.base_url)

        print(f"状态码: {response.status_code}")
        if response.status_code == 401:
            print("✓ 未登录访问正确返回 401")
        else:
            print(f"✗ 预期 401，实际返回 {response.status_code}")
        print()

    def test_regular_user_access(self):
        """测试普通用户访问"""
        print("=" * 60)
        print("3. 测试普通用户访问（应返回403）")
        print("=" * 60)

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.base_url)

        print(f"状态码: {response.status_code}")
        if response.status_code == 403:
            print("✓ 普通用户访问正确返回 403")
        else:
            print(f"✗ 预期 403，实际返回 {response.status_code}")
        print()

    def test_admin_access(self):
        """测试管理员访问"""
        print("=" * 60)
        print("4. 测试管理员访问（应返回200）")
        print("=" * 60)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.base_url)

        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 管理员访问成功返回 200")
            data = response.json()
            return data
        else:
            print(f"✗ 预期 200，实际返回 {response.status_code}")
            return None
        print()

    def verify_data_completeness(self, data):
        """验证数据完整性"""
        print("=" * 60)
        print("5. 验证数据完整性")
        print("=" * 60)

        if not data or data.get('code') != 200:
            print("✗ 响应数据格式错误")
            return False

        result = data.get('data', {})

        # 检查 summary
        summary = result.get('summary')
        if not summary:
            print("✗ 缺少 summary 字段")
            return False

        print("✓ summary 字段存在")
        print(f"  - total_recipes: {summary.get('total_recipes')}")
        print(f"  - total_difficulty_levels: {summary.get('total_difficulty_levels')}")

        # 检查 difficulties
        difficulties = result.get('difficulties')
        if not isinstance(difficulties, list):
            print("✗ difficulties 字段类型错误")
            return False

        print(f"✓ difficulties 字段存在（共 {len(difficulties)} 个难度等级）")

        # 检查每个难度的数据结构
        required_fields = ['name', 'value', 'count', 'percentage',
                          'avg_cooking_time', 'avg_view_count', 'avg_favorite_count']

        for idx, difficulty in enumerate(difficulties):
            print(f"\n难度等级 {idx + 1}: {difficulty.get('name')} ({difficulty.get('value')})")
            for field in required_fields:
                if field not in difficulty:
                    print(f"  ✗ 缺少字段: {field}")
                    return False
                print(f"  ✓ {field}: {difficulty[field]}")

        print("\n✓ 数据完整性验证通过")
        return True

    def verify_data_accuracy(self, data):
        """验证数据准确性"""
        print("\n" + "=" * 60)
        print("6. 验证数据准确性")
        print("=" * 60)

        result = data.get('data', {})
        summary = result.get('summary')
        difficulties = result.get('difficulties', [])

        # 验证 total_recipes
        actual_total = Recipe.objects.count()
        reported_total = summary.get('total_recipes')

        print(f"数据库实际菜谱总数: {actual_total}")
        print(f"API 返回菜谱总数: {reported_total}")

        if actual_total == reported_total:
            print("✓ 菜谱总数准确")
        else:
            print("✗ 菜谱总数不准确")
            return False

        # 验证各难度等级数据
        difficulty_count_sum = 0
        for difficulty in difficulties:
            difficulty_value = difficulty['value']
            difficulty_name = difficulty['name']
            reported_count = difficulty['count']

            # 从数据库查询该难度的实际数量
            actual_count = Recipe.objects.filter(difficulty=difficulty_value).count()

            print(f"\n难度等级: {difficulty_name} ({difficulty_value})")
            print(f"  API 返回数量: {reported_count}")
            print(f"  数据库实际数量: {actual_count}")

            if reported_count == actual_count:
                print(f"  ✓ 数量准确")
            else:
                print(f"  ✗ 数量不准确")
                return False

            difficulty_count_sum += reported_count

            # 验证百分比计算
            expected_percentage = round((reported_count / actual_total * 100), 2) if actual_total > 0 else 0
            reported_percentage = difficulty['percentage']

            print(f"  API 返回占比: {reported_percentage}%")
            print(f"  计算预期占比: {expected_percentage}%")

            if abs(reported_percentage - expected_percentage) < 0.01:
                print(f"  ✓ 占比计算准确")
            else:
                print(f"  ✗ 占比计算不准确")
                return False

            # 验证平均烹饪时长
            from django.db.models import Avg
            actual_avg_cooking = Recipe.objects.filter(
                difficulty=difficulty_value
            ).aggregate(avg_cooking=Avg('cooking_time'))['avg_cooking']

            reported_avg_cooking = difficulty['avg_cooking_time']
            actual_avg_cooking_rounded = round(actual_avg_cooking, 1) if actual_avg_cooking else 0

            print(f"  API 返回平均烹饪时长: {reported_avg_cooking} 分钟")
            print(f"  数据库实际平均烹饪时长: {actual_avg_cooking_rounded} 分钟")

            if reported_avg_cooking == actual_avg_cooking_rounded:
                print(f"  ✓ 平均烹饪时长准确")
            else:
                print(f"  ✗ 平均烹饪时长不准确")
                return False

            # 验证平均点击量
            actual_avg_view = Recipe.objects.filter(
                difficulty=difficulty_value
            ).aggregate(avg_view=Avg('view_count'))['avg_view']

            reported_avg_view = difficulty['avg_view_count']
            actual_avg_view_rounded = round(actual_avg_view, 2) if actual_avg_view else 0

            print(f"  API 返回平均点击量: {reported_avg_view}")
            print(f"  数据库实际平均点击量: {actual_avg_view_rounded}")

            if reported_avg_view == actual_avg_view_rounded:
                print(f"  ✓ 平均点击量准确")
            else:
                print(f"  ✗ 平均点击量不准确")
                return False

            # 验证平均收藏量
            actual_avg_fav = Recipe.objects.filter(
                difficulty=difficulty_value
            ).aggregate(avg_fav=Avg('favorite_count'))['avg_fav']

            reported_avg_fav = difficulty['avg_favorite_count']
            actual_avg_fav_rounded = round(actual_avg_fav, 2) if actual_avg_fav else 0

            print(f"  API 返回平均收藏量: {reported_avg_fav}")
            print(f"  数据库实际平均收藏量: {actual_avg_fav_rounded}")

            if reported_avg_fav == actual_avg_fav_rounded:
                print(f"  ✓ 平均收藏量准确")
            else:
                print(f"  ✗ 平均收藏量不准确")
                return False

        # 验证总难度等级数量
        reported_difficulty_count = summary.get('total_difficulty_levels')
        actual_difficulty_count = len(difficulties)

        print(f"\n难度等级类型数量:")
        print(f"  API 返回: {reported_difficulty_count}")
        print(f"  实际数量: {actual_difficulty_count}")

        if reported_difficulty_count == actual_difficulty_count:
            print("✓ 难度等级类型数量准确")
        else:
            print("✗ 难度等级类型数量不准确")
            return False

        print("\n✓ 数据准确性验证通过")
        return True

    def display_sample_data(self, data):
        """展示示例数据"""
        print("\n" + "=" * 60)
        print("7. 示例数据展示")
        print("=" * 60)

        result = data.get('data', {})
        summary = result.get('summary', {})
        difficulties = result.get('difficulties', [])

        print(f"\n【数据概览】")
        print(f"  总菜谱数: {summary.get('total_recipes')}")
        print(f"  难度等级数: {summary.get('total_difficulty_levels')}")

        print(f"\n【各难度等级详细数据】")
        for idx, difficulty in enumerate(difficulties):
            print(f"\n{idx + 1}. {difficulty['name']} ({difficulty['value']})")
            print(f"   数量: {difficulty['count']} ({difficulty['percentage']}%)")
            print(f"   平均点击量: {difficulty['avg_view_count']}")
            print(f"   平均收藏量: {difficulty['avg_favorite_count']}")
            print(f"   平均烹饪时长: {difficulty['avg_cooking_time']} 分钟")

    def cleanup(self):
        """清理测试数据"""
        print("\n" + "=" * 60)
        print("清理测试数据")
        print("=" * 60)

        User.objects.filter(username__in=['test_admin', 'test_user']).delete()
        print("✓ 测试用户已清理")

    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("管理员难度深度分析接口测试")
        print("=" * 60)
        print()

        try:
            # 设置测试用户
            self.setup_users()

            # 测试未登录访问
            self.test_unauthorized_access()

            # 测试普通用户访问
            self.test_regular_user_access()

            # 测试管理员访问并获取数据
            data = self.test_admin_access()

            if data:
                # 验证数据完整性
                if not self.verify_data_completeness(data):
                    print("\n✗ 数据完整性验证失败")
                    return False

                # 验证数据准确性
                if not self.verify_data_accuracy(data):
                    print("\n✗ 数据准确性验证失败")
                    return False

                # 展示示例数据
                self.display_sample_data(data)

            print("\n" + "=" * 60)
            print("✓ 所有测试通过！")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n✗ 测试过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            # 清理测试数据
            self.cleanup()


if __name__ == '__main__':
    tester = AdminDifficultyAnalysisTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
