"""
管理员数据分析接口测试脚本

测试阶段十五第1步：菜系深度分析接口

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


class AdminAnalyticsTester:
    """管理员数据分析接口测试类"""

    def __init__(self):
        self.client = APIClient()
        self.base_url = '/api/admin/analytics/cuisines/'
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
        print(f"  - total_cuisines: {summary.get('total_cuisines')}")

        # 检查 cuisines
        cuisines = result.get('cuisines')
        if not isinstance(cuisines, list):
            print("✗ cuisines 字段类型错误")
            return False

        print(f"✓ cuisines 字段存在（共 {len(cuisines)} 个菜系）")

        # 检查每个菜系的数据结构
        required_fields = ['name', 'count', 'percentage', 'avg_view_count',
                          'avg_favorite_count', 'avg_cooking_time', 'difficulty_distribution']

        for idx, cuisine in enumerate(cuisines):
            print(f"\n菜系 {idx + 1}: {cuisine.get('name')}")
            for field in required_fields:
                if field not in cuisine:
                    print(f"  ✗ 缺少字段: {field}")
                    return False
                print(f"  ✓ {field}: {cuisine[field]}")

            # 检查难度分布
            difficulty_dist = cuisine.get('difficulty_distribution')
            if not isinstance(difficulty_dist, dict):
                print(f"  ✗ difficulty_distribution 类型错误")
                return False
            print(f"  ✓ difficulty_distribution: {difficulty_dist}")

        print("\n✓ 数据完整性验证通过")
        return True

    def verify_data_accuracy(self, data):
        """验证数据准确性"""
        print("\n" + "=" * 60)
        print("6. 验证数据准确性")
        print("=" * 60)

        result = data.get('data', {})
        summary = result.get('summary')
        cuisines = result.get('cuisines', [])

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

        # 验证各菜系数据
        cuisine_count_sum = 0
        for cuisine in cuisines:
            cuisine_name = cuisine['name']
            reported_count = cuisine['count']

            # 从数据库查询该菜系的实际数量
            actual_count = Recipe.objects.filter(cuisine_type=cuisine_name).count()

            print(f"\n菜系: {cuisine_name}")
            print(f"  API 返回数量: {reported_count}")
            print(f"  数据库实际数量: {actual_count}")

            if reported_count == actual_count:
                print(f"  ✓ 数量准确")
            else:
                print(f"  ✗ 数量不准确")
                return False

            cuisine_count_sum += reported_count

            # 验证百分比计算
            expected_percentage = round((reported_count / actual_total * 100), 2) if actual_total > 0 else 0
            reported_percentage = cuisine['percentage']

            print(f"  API 返回占比: {reported_percentage}%")
            print(f"  计算预期占比: {expected_percentage}%")

            if abs(reported_percentage - expected_percentage) < 0.01:
                print(f"  ✓ 占比计算准确")
            else:
                print(f"  ✗ 占比计算不准确")
                return False

            # 验证难度分布
            reported_diff_dist = cuisine['difficulty_distribution']
            print(f"  难度分布: {reported_diff_dist}")

            # 验证 easy 数量
            actual_easy = Recipe.objects.filter(
                cuisine_type=cuisine_name,
                difficulty='easy'
            ).count()
            if reported_diff_dist['easy'] == actual_easy:
                print(f"  ✓ easy 难度数量准确 ({actual_easy})")
            else:
                print(f"  ✗ easy 难度数量不准确 (报告: {reported_diff_dist['easy']}, 实际: {actual_easy})")
                return False

            # 验证 medium 数量
            actual_medium = Recipe.objects.filter(
                cuisine_type=cuisine_name,
                difficulty='medium'
            ).count()
            if reported_diff_dist['medium'] == actual_medium:
                print(f"  ✓ medium 难度数量准确 ({actual_medium})")
            else:
                print(f"  ✗ medium 难度数量不准确 (报告: {reported_diff_dist['medium']}, 实际: {actual_medium})")
                return False

            # 验证 hard 数量
            actual_hard = Recipe.objects.filter(
                cuisine_type=cuisine_name,
                difficulty='hard'
            ).count()
            if reported_diff_dist['hard'] == actual_hard:
                print(f"  ✓ hard 难度数量准确 ({actual_hard})")
            else:
                print(f"  ✗ hard 难度数量不准确 (报告: {reported_diff_dist['hard']}, 实际: {actual_hard})")
                return False

        # 验证总菜系数量
        reported_cuisine_count = summary.get('total_cuisines')
        actual_cuisine_count = len(cuisines)

        print(f"\n菜系类型数量:")
        print(f"  API 返回: {reported_cuisine_count}")
        print(f"  实际数量: {actual_cuisine_count}")

        if reported_cuisine_count == actual_cuisine_count:
            print("✓ 菜系类型数量准确")
        else:
            print("✗ 菜系类型数量不准确")
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
        cuisines = result.get('cuisines', [])

        print(f"\n【数据概览】")
        print(f"  总菜谱数: {summary.get('total_recipes')}")
        print(f"  菜系数: {summary.get('total_cuisines')}")

        print(f"\n【各菜系详细数据】(最多显示前5个)")
        for idx, cuisine in enumerate(cuisines[:5]):
            print(f"\n{idx + 1}. {cuisine['name']}")
            print(f"   数量: {cuisine['count']} ({cuisine['percentage']}%)")
            print(f"   平均点击量: {cuisine['avg_view_count']}")
            print(f"   平均收藏量: {cuisine['avg_favorite_count']}")
            print(f"   平均烹饪时长: {cuisine['avg_cooking_time']} 分钟")
            print(f"   难度分布: 简单({cuisine['difficulty_distribution']['easy']}), "
                  f"中等({cuisine['difficulty_distribution']['medium']}), "
                  f"困难({cuisine['difficulty_distribution']['hard']})")

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
        print("管理员菜系深度分析接口测试")
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
    tester = AdminAnalyticsTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
