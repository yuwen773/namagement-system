"""
管理员热门菜谱分析接口测试脚本

测试阶段十五第3步：热门菜谱分析接口

测试场景：
1. 无权限访问测试（未登录）
2. 普通用户权限测试（无管理员权限）
3. 管理员访问测试（正常场景，默认按点击量排序）
4. 管理员访问测试（按收藏量排序）
5. 参数验证测试（无效 sort_by 参数）
6. 参数验证测试（无效 limit 参数）
7. 数据完整性验证
8. 数据准确性验证
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
from django.db.models import Avg

User = get_user_model()


class AdminHotRecipeAnalysisTester:
    """管理员热门菜谱分析接口测试类"""

    def __init__(self):
        self.client = APIClient()
        self.base_url = '/api/admin/analytics/hot/'
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

    def test_admin_access_default_sort(self):
        """测试管理员访问（默认按点击量排序）"""
        print("=" * 60)
        print("4. 测试管理员访问（默认按点击量排序）")
        print("=" * 60)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.base_url)

        print(f"请求 URL: {self.base_url}")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 管理员访问成功返回 200")
            data = response.json()
            return data
        else:
            print(f"✗ 预期 200，实际返回 {response.status_code}")
            return None
        print()

    def test_admin_access_sort_by_favorite(self):
        """测试管理员访问（按收藏量排序）"""
        print("=" * 60)
        print("5. 测试管理员访问（按收藏量排序）")
        print("=" * 60)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.base_url, {'sort_by': 'favorite_count'})

        print(f"请求 URL: {self.base_url}?sort_by=favorite_count")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 管理员访问成功返回 200")
            data = response.json()
            result = data.get('data', {})

            # 验证排序方式
            summary = result.get('summary', {})
            if summary.get('sort_by') == 'favorite_count':
                print(f"✓ 排序方式正确: {summary.get('sort_by_label')}")
            else:
                print(f"✗ 排序方式错误: {summary.get('sort_by')}")

            # 验证菜谱列表按收藏量降序排列
            recipes = result.get('recipes', [])
            if len(recipes) > 1:
                is_sorted = all(
                    recipes[i]['favorite_count'] >= recipes[i + 1]['favorite_count']
                    for i in range(len(recipes) - 1)
                )
                if is_sorted:
                    print("✓ 菜谱列表正确按收藏量降序排列")
                else:
                    print("✗ 菜谱列表排序错误")

            return data
        else:
            print(f"✗ 预期 200，实际返回 {response.status_code}")
            return None
        print()

    def test_invalid_sort_by_parameter(self):
        """测试无效 sort_by 参数"""
        print("=" * 60)
        print("6. 测试无效 sort_by 参数（应使用默认值）")
        print("=" * 60)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.base_url, {'sort_by': 'invalid_field'})

        print(f"请求 URL: {self.base_url}?sort_by=invalid_field")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 请求成功返回 200")
            data = response.json()
            result = data.get('data', {})
            summary = result.get('summary', {})

            # 验证使用了默认排序方式
            if summary.get('sort_by') == 'view_count':
                print(f"✓ 无效参数时使用默认排序: {summary.get('sort_by_label')}")
            else:
                print(f"✗ 排序方式异常: {summary.get('sort_by')}")
        else:
            print(f"✗ 预期 200，实际返回 {response.status_code}")
        print()

    def test_invalid_limit_parameter(self):
        """测试无效 limit 参数"""
        print("=" * 60)
        print("7. 测试无效 limit 参数（边界值测试）")
        print("=" * 60)

        self.client.force_authenticate(user=self.admin_user)

        # 测试 limit < 1
        print("\n测试 limit=0（应使用最小值 1）")
        response = self.client.get(self.base_url, {'limit': 0})
        if response.status_code == 200:
            data = response.json()
            limit = data['data']['summary']['limit']
            if limit == 1:
                print(f"✓ limit=0 被修正为 1")
            else:
                print(f"✗ limit 值异常: {limit}")

        # 测试 limit > 100
        print("\n测试 limit=200（应使用最大值 100）")
        response = self.client.get(self.base_url, {'limit': 200})
        if response.status_code == 200:
            data = response.json()
            limit = data['data']['summary']['limit']
            if limit == 100:
                print(f"✓ limit=200 被修正为 100")
            else:
                print(f"✗ limit 值异常: {limit}")

        # 测试 limit 为无效值
        print("\n测试 limit=abc（应使用默认值 50）")
        response = self.client.get(self.base_url, {'limit': 'abc'})
        if response.status_code == 200:
            data = response.json()
            limit = data['data']['summary']['limit']
            if limit == 50:
                print(f"✓ 无效 limit 使用默认值 50")
            else:
                print(f"✗ limit 值异常: {limit}")
        print()

    def verify_data_completeness(self, data):
        """验证数据完整性"""
        print("=" * 60)
        print("8. 验证数据完整性")
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
        required_summary_fields = ['total_recipes', 'sort_by', 'sort_by_label', 'limit']
        for field in required_summary_fields:
            if field in summary:
                print(f"  ✓ {field}: {summary[field]}")
            else:
                print(f"  ✗ 缺少字段: {field}")
                return False

        # 检查 trends
        trends = result.get('trends')
        if not trends:
            print("✗ 缺少 trends 字段")
            return False

        print("✓ trends 字段存在")
        required_trend_fields = ['avg_view_count', 'avg_favorite_count', 'avg_conversion_rate']
        for field in required_trend_fields:
            if field in trends:
                print(f"  ✓ {field}: {trends[field]}")
            else:
                print(f"  ✗ 缺少字段: {field}")
                return False

        # 检查 recipes
        recipes = result.get('recipes')
        if not isinstance(recipes, list):
            print("✗ recipes 字段类型错误")
            return False

        print(f"✓ recipes 字段存在（共 {len(recipes)} 个菜谱）")

        # 检查每个菜谱的数据结构
        required_recipe_fields = ['id', 'name', 'cuisine_type', 'difficulty',
                                  'view_count', 'favorite_count', 'conversion_rate']

        # 只显示前3个菜谱的详细信息
        display_count = min(3, len(recipes))
        for idx in range(display_count):
            recipe = recipes[idx]
            print(f"\n菜谱 {idx + 1}: {recipe.get('name')}")
            for field in required_recipe_fields:
                if field not in recipe:
                    print(f"  ✗ 缺少字段: {field}")
                    return False
                print(f"  ✓ {field}: {recipe[field]}")

        if len(recipes) > display_count:
            print(f"\n... 还有 {len(recipes) - display_count} 个菜谱")

        print("\n✓ 数据完整性验证通过")
        return True

    def verify_data_accuracy(self, data):
        """验证数据准确性"""
        print("\n" + "=" * 60)
        print("9. 验证数据准确性")
        print("=" * 60)

        result = data.get('data', {})
        summary = result.get('summary')
        trends = result.get('trends')
        recipes = result.get('recipes', [])

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

        # 验证平均点击量
        actual_avg_view = Recipe.objects.aggregate(avg_view=Avg('view_count'))['avg_view'] or 0
        reported_avg_view = trends.get('avg_view_count')

        print(f"\nAPI 返回平均点击量: {reported_avg_view}")
        print(f"数据库实际平均点击量: {round(actual_avg_view, 2)}")

        if abs(reported_avg_view - round(actual_avg_view, 2)) < 0.1:
            print("✓ 平均点击量准确")
        else:
            print("✗ 平均点击量不准确")
            return False

        # 验证平均收藏量
        actual_avg_fav = Recipe.objects.aggregate(avg_fav=Avg('favorite_count'))['avg_fav'] or 0
        reported_avg_fav = trends.get('avg_favorite_count')

        print(f"\nAPI 返回平均收藏量: {reported_avg_fav}")
        print(f"数据库实际平均收藏量: {round(actual_avg_fav, 2)}")

        if abs(reported_avg_fav - round(actual_avg_fav, 2)) < 0.1:
            print("✓ 平均收藏量准确")
        else:
            print("✗ 平均收藏量不准确")
            return False

        # 验证平均转化率
        actual_avg_conversion = (actual_avg_fav / actual_avg_view * 100) if actual_avg_view > 0 else 0
        reported_avg_conversion = trends.get('avg_conversion_rate')

        print(f"\nAPI 返回平均转化率: {reported_avg_conversion}%")
        print(f"数据库实际平均转化率: {round(actual_avg_conversion, 2)}%")

        if abs(reported_avg_conversion - round(actual_avg_conversion, 2)) < 0.1:
            print("✓ 平均转化率准确")
        else:
            print("✗ 平均转化率不准确")
            return False

        # 验证 Top 菜谱数据
        sort_by = summary.get('sort_by')
        limit = summary.get('limit')

        print(f"\n验证 Top {limit} 菜谱数据（按 {summary.get('sort_by_label')} 排序）:")

        # 从数据库获取实际 Top 菜谱
        order_field = f'-{sort_by}'
        actual_top_recipes = list(Recipe.objects.order_by(order_field)[:limit].values(
            'id', 'name', 'cuisine_type', 'difficulty', 'view_count', 'favorite_count'
        ))

        # 验证数量
        if len(recipes) == len(actual_top_recipes):
            print(f"✓ 返回菜谱数量正确: {len(recipes)}")
        else:
            print(f"✗ 返回菜谱数量错误: 预期 {len(actual_top_recipes)}，实际 {len(recipes)}")
            return False

        # 验证每个菜谱的数据
        all_accurate = True
        for idx in range(min(5, len(recipes))):  # 只验证前5个
            api_recipe = recipes[idx]
            actual_recipe = actual_top_recipes[idx]

            print(f"\n菜谱 {idx + 1}: {api_recipe['name']} (ID: {api_recipe['id']})")

            # 验证各字段
            if api_recipe['id'] == actual_recipe['id']:
                print(f"  ✓ ID 匹配")
            else:
                print(f"  ✗ ID 不匹配")
                all_accurate = False

            if api_recipe['view_count'] == actual_recipe['view_count']:
                print(f"  ✓ 点击量匹配: {api_recipe['view_count']}")
            else:
                print(f"  ✗ 点击量不匹配")
                all_accurate = False

            if api_recipe['favorite_count'] == actual_recipe['favorite_count']:
                print(f"  ✓ 收藏量匹配: {api_recipe['favorite_count']}")
            else:
                print(f"  ✗ 收藏量不匹配")
                all_accurate = False

            # 验证转化率计算
            expected_conversion = (api_recipe['favorite_count'] / api_recipe['view_count'] * 100) if api_recipe['view_count'] > 0 else 0
            if abs(api_recipe['conversion_rate'] - round(expected_conversion, 2)) < 0.1:
                print(f"  ✓ 转化率计算正确: {api_recipe['conversion_rate']}%")
            else:
                print(f"  ✗ 转化率计算错误: 预期 {round(expected_conversion, 2)}%，实际 {api_recipe['conversion_rate']}%")
                all_accurate = False

        if len(recipes) > 5:
            print(f"\n... 还有 {len(recipes) - 5} 个菜谱未详细验证")

        if all_accurate:
            print("\n✓ 数据准确性验证通过")
        else:
            print("\n✗ 数据准确性验证失败")

        return all_accurate

    def display_sample_data(self, data):
        """展示示例数据"""
        print("\n" + "=" * 60)
        print("10. 示例数据展示")
        print("=" * 60)

        result = data.get('data', {})
        summary = result.get('summary', {})
        trends = result.get('trends', {})
        recipes = result.get('recipes', [])

        print(f"\n【数据概览】")
        print(f"  总菜谱数: {summary.get('total_recipes')}")
        print(f"  排序方式: {summary.get('sort_by_label')} ({summary.get('sort_by')})")
        print(f"  返回数量: {summary.get('limit')}")

        print(f"\n【趋势统计】")
        print(f"  平均点击量: {trends.get('avg_view_count')}")
        print(f"  平均收藏量: {trends.get('avg_favorite_count')}")
        print(f"  平均转化率: {trends.get('avg_conversion_rate')}%")

        print(f"\n【Top 10 热门菜谱】")
        for idx, recipe in enumerate(recipes[:10]):
            print(f"\n{idx + 1}. {recipe['name']} (ID: {recipe['id']})")
            print(f"   菜系: {recipe['cuisine_type']} | 难度: {recipe['difficulty']}")
            print(f"   点击量: {recipe['view_count']:,} | 收藏量: {recipe['favorite_count']:,}")
            print(f"   转化率: {recipe['conversion_rate']}%")

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
        print("管理员热门菜谱分析接口测试")
        print("=" * 60)
        print()

        try:
            # 设置测试用户
            self.setup_users()

            # 测试未登录访问
            self.test_unauthorized_access()

            # 测试普通用户访问
            self.test_regular_user_access()

            # 测试管理员访问（默认排序）
            data = self.test_admin_access_default_sort()

            if data:
                # 测试按收藏量排序
                self.test_admin_access_sort_by_favorite()

                # 测试无效参数
                self.test_invalid_sort_by_parameter()
                self.test_invalid_limit_parameter()

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
    tester = AdminHotRecipeAnalysisTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
