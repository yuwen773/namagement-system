"""
食材关联分析接口测试脚本

测试管理员食材关联分析 API 的各项功能。

运行方式：
    cd backend
    python verify_script/test_admin_ingredient_pairs_analysis.py
"""

import os
import sys
import django
import json
from decimal import Decimal

# 设置控制台输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from rest_framework.test import APIClient
from accounts.models import User


class IngredientPairsAnalysisTest:
    """食材关联分析测试类"""

    def __init__(self):
        self.client = APIClient()
        self.admin_token = None
        self.user_token = None
        self.test_results = []

    def log(self, test_name, passed, message=""):
        """记录测试结果"""
        status = "[PASS]" if passed else "[FAIL]"
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message
        })
        print(f"{status} - {test_name}")
        if message:
            print(f"    {message}")

    def setup_users(self):
        """设置测试用户"""
        print("\n=== 设置测试用户 ===")

        # 创建或重置管理员用户（使用已知密码）
        admin, created = User.objects.get_or_create(
            username='test_admin_001',
            defaults={
                'role': 'admin',
                'is_active': True
            }
        )
        admin.set_password('admin123')
        admin.save()

        # 创建或重置普通用户（使用已知密码）
        user, created = User.objects.get_or_create(
            username='test_user_001',
            defaults={
                'role': 'user',
                'is_active': True
            }
        )
        user.set_password('test123')
        user.save()

        # 登录管理员获取 Token
        response = self.client.post('/api/accounts/login/', {
            'username': 'test_admin_001',
            'password': 'admin123'
        })
        if response.status_code == 200:
            self.admin_token = response.data.get('data', {}).get('token')
            self.log("设置管理员用户", True, f"管理员 Token: {self.admin_token[:20] if self.admin_token else 'N/A'}...")
        else:
            self.log("设置管理员用户", False, f"登录失败: {response.data}")

        # 登录普通用户获取 Token
        response = self.client.post('/api/accounts/login/', {
            'username': 'test_user_001',
            'password': 'test123'
        })
        if response.status_code == 200:
            self.user_token = response.data.get('data', {}).get('token')
            self.log("设置普通用户", True, f"用户 Token: {self.user_token[:20] if self.user_token else 'N/A'}...")
        else:
            self.log("设置普通用户", False, f"登录失败: {response.data}")

    def test_permission_check(self):
        """测试1：权限检查"""
        print("\n=== 测试1：权限检查 ===")

        # 未登录访问
        response = self.client.get('/api/admin/analytics/ingredient-pairs/')
        self.log(
            "未登录访问应返回 401",
            response.status_code == 401,
            f"实际状态码: {response.status_code}"
        )

        # 普通用户访问
        if self.user_token:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
            response = self.client.get('/api/admin/analytics/ingredient-pairs/')
            self.log(
                "普通用户访问应返回 403",
                response.status_code == 403,
                f"实际状态码: {response.status_code}"
            )

        # 管理员访问
        if self.admin_token:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
            response = self.client.get('/api/admin/analytics/ingredient-pairs/')
            self.log(
                "管理员访问应返回 200",
                response.status_code == 200,
                f"实际状态码: {response.status_code}"
            )

    def test_default_response(self):
        """测试2：默认响应数据结构"""
        print("\n=== 测试2：默认响应数据结构 ===")

        if not self.admin_token:
            self.log("默认响应测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/admin/analytics/ingredient-pairs/')

        if response.status_code != 200:
            self.log("默认响应测试", False, f"请求失败: {response.status_code}")
            return

        data = response.data.get('data', {})

        # 检查 summary
        summary = data.get('summary', {})
        has_total_recipes = 'total_recipes' in summary
        has_total_pairs = 'total_pairs' in summary
        has_min_count = 'min_count' in summary
        has_limit = 'limit' in summary
        has_category_filter = 'category_filter' in summary

        self.log(
            "包含 summary 字段",
            all([has_total_recipes, has_total_pairs, has_min_count, has_limit, has_category_filter]),
            f"缺失字段: {self._get_missing_fields(summary, ['total_recipes', 'total_pairs', 'min_count', 'limit', 'category_filter'])}"
        )

        # 检查 pairs
        pairs = data.get('pairs', [])
        is_list = isinstance(pairs, list)
        has_data = len(pairs) > 0

        self.log(
            "包含 pairs 数组",
            is_list,
            f"类型: {type(pairs)}"
        )

        self.log(
            "返回配对数据",
            has_data,
            f"配对数量: {len(pairs)}"
        )

        # 检查单个配对结构
        if has_data:
            pair = pairs[0]
            has_ing1 = 'ingredient_1' in pair
            has_ing2 = 'ingredient_2' in pair
            has_count = 'count' in pair
            has_percentage = 'percentage' in pair

            self.log(
                "配对包含完整字段",
                all([has_ing1, has_ing2, has_count, has_percentage]),
                f"缺失字段: {self._get_missing_fields(pair, ['ingredient_1', 'ingredient_2', 'count', 'percentage'])}"
            )

            # 检查食材对象结构
            if has_ing1:
                ing1 = pair['ingredient_1']
                has_ing1_id = 'id' in ing1
                has_ing1_name = 'name' in ing1
                has_ing1_category = 'category' in ing1

                self.log(
                    "食材1包含完整信息",
                    all([has_ing1_id, has_ing1_name, has_ing1_category]),
                    f"缺失字段: {self._get_missing_fields(ing1, ['id', 'name', 'category'])}"
                )

            # 打印示例配对
            print(f"\n示例配对: {pair.get('ingredient_1', {}).get('name', 'N/A')} + "
                  f"{pair.get('ingredient_2', {}).get('name', 'N/A')} = "
                  f"{pair.get('count', 0)} 次 ({pair.get('percentage', 0)}%)")

    def test_limit_parameter(self):
        """测试3：limit 参数"""
        print("\n=== 测试3：limit 参数 ===")

        if not self.admin_token:
            self.log("limit 参数测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # 测试 limit=10
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=10')
        pairs = response.data.get('data', {}).get('pairs', [])
        self.log(
            "limit=10 返回 10 条数据",
            len(pairs) == 10,
            f"实际数量: {len(pairs)}"
        )

        # 测试 limit=5
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=5')
        pairs = response.data.get('data', {}).get('pairs', [])
        self.log(
            "limit=5 返回 5 条数据",
            len(pairs) == 5,
            f"实际数量: {len(pairs)}"
        )

        # 测试无效 limit（应使用默认值 50）
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=invalid')
        pairs = response.data.get('data', {}).get('pairs', [])
        self.log(
            "无效 limit 使用默认值",
            len(pairs) <= 50,
            f"实际数量: {len(pairs)}"
        )

        # 测试 limit=0（应使用最小值 1）
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=0')
        pairs = response.data.get('data', {}).get('pairs', [])
        self.log(
            "limit=0 使用最小值 1",
            len(pairs) >= 1,
            f"实际数量: {len(pairs)}"
        )

        # 测试 limit=100（最大值）
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=100')
        pairs = response.data.get('data', {}).get('pairs', [])
        self.log(
            "limit=100 使用最大值",
            len(pairs) <= 100,
            f"实际数量: {len(pairs)}"
        )

    def test_min_count_parameter(self):
        """测试4：min_count 参数"""
        print("\n=== 测试4：min_count 参数 ===")

        if not self.admin_token:
            self.log("min_count 参数测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # 测试 min_count=100
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?min_count=100')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])
        min_count = data.get('summary', {}).get('min_count')

        # 检查所有配对的 count 都 >= 100
        all_above_min = all(pair['count'] >= 100 for pair in pairs) if pairs else True

        self.log(
            "min_count=100 所有配对次数 >= 100",
            all_above_min,
            f"配对数量: {len(pairs)}, summary.min_count: {min_count}"
        )

        # 测试 min_count=500
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?min_count=500')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])

        all_above_min_500 = all(pair['count'] >= 500 for pair in pairs) if pairs else True

        self.log(
            "min_count=500 所有配对次数 >= 500",
            all_above_min_500,
            f"配对数量: {len(pairs)}"
        )

        # 测试 min_count=1（最小值）
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?min_count=1')
        data = response.data.get('data', {})
        total_pairs = data.get('summary', {}).get('total_pairs', 0)

        self.log(
            "min_count=1 返回所有配对",
            total_pairs > 0,
            f"总配对数: {total_pairs}"
        )

    def test_category_parameter(self):
        """测试5：category 参数"""
        print("\n=== 测试5：category 参数 ===")

        if not self.admin_token:
            self.log("category 参数测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # 测试 vegetable 分类
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?category=vegetable')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])
        category_filter = data.get('summary', {}).get('category_filter')

        # 检查返回的食材都是 vegetable 分类
        all_vegetable = True
        if pairs:
            for pair in pairs:
                if pair['ingredient_1']['category'] != 'vegetable' or pair['ingredient_2']['category'] != 'vegetable':
                    all_vegetable = False
                    break

        self.log(
            "category=vegetable 返回蔬菜配对",
            all_vegetable,
            f"配对数量: {len(pairs)}, 分类筛选: {category_filter}"
        )

        # 测试 meat 分类
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?category=meat')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])

        # 检查返回的食材都是 meat 分类
        all_meat = True
        if pairs:
            for pair in pairs:
                if pair['ingredient_1']['category'] != 'meat' or pair['ingredient_2']['category'] != 'meat':
                    all_meat = False
                    break

        self.log(
            "category=meat 返回肉类配对",
            all_meat,
            f"配对数量: {len(pairs)}"
        )

        # 不指定分类（显示全部）
        response = self.client.get('/api/admin/analytics/ingredient-pairs/')
        data = response.data.get('data', {})
        category_filter = data.get('summary', {}).get('category_filter')

        self.log(
            "不指定分类显示全部",
            category_filter == '全部',
            f"分类筛选: {category_filter}"
        )

    def test_data_accuracy(self):
        """测试6：数据准确性"""
        print("\n=== 测试6：数据准确性 ===")

        if not self.admin_token:
            self.log("数据准确性测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # 获取配对数据
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=5')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])

        if not pairs:
            self.log("数据准确性测试", False, "没有配对数据")
            return

        # 检查按 count 降序排列
        is_sorted = True
        for i in range(len(pairs) - 1):
            if pairs[i]['count'] < pairs[i + 1]['count']:
                is_sorted = False
                break

        self.log(
            "配对按 count 降序排列",
            is_sorted,
            f"前3个配对次数: {[p['count'] for p in pairs[:3]]}"
        )

        # 验证百分比计算正确性
        total_recipes = data.get('summary', {}).get('total_recipes', 1)
        percentage_correct = True

        for pair in pairs[:5]:  # 检查前5个
            expected_percentage = round((pair['count'] / total_recipes * 100), 2)
            if abs(pair['percentage'] - expected_percentage) > 0.01:
                percentage_correct = False
                print(f"    百分比误差: {pair['percentage']} vs {expected_percentage}")
                break

        self.log(
            "百分比计算正确",
            percentage_correct,
            f"总菜谱数: {total_recipes}"
        )

        # 验证食材名称存在
        all_have_names = all(
            pair['ingredient_1']['name'] and pair['ingredient_2']['name']
            for pair in pairs
        )

        self.log(
            "所有食材都有名称",
            all_have_names,
            f"检查数量: {len(pairs)}"
        )

    def test_edge_cases(self):
        """测试7：边界情况"""
        print("\n=== 测试7：边界情况 ===")

        if not self.admin_token:
            self.log("边界情况测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # 测试超大 min_count
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?min_count=999999')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])

        self.log(
            "超大 min_count 返回空数组",
            len(pairs) == 0,
            f"实际数量: {len(pairs)}"
        )

        # 测试组合参数
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?limit=5&min_count=10&category=other')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])
        summary = data.get('summary', {})

        conditions_met = (
            len(pairs) <= 5 and
            summary.get('limit') == 5 and
            summary.get('min_count') == 10 and
            summary.get('category_filter') == 'other'
        )

        self.log(
            "组合参数正确处理",
            conditions_met,
            f"配对数: {len(pairs)}, limit: {summary.get('limit')}, min_count: {summary.get('min_count')}, category: {summary.get('category_filter')}"
        )

        # 测试无效分类
        response = self.client.get('/api/admin/analytics/ingredient-pairs/?category=invalid_category')
        data = response.data.get('data', {})
        pairs = data.get('pairs', [])

        self.log(
            "无效分类返回空结果",
            len(pairs) == 0,
            f"实际数量: {len(pairs)}"
        )

    def test_response_format(self):
        """测试8：响应格式"""
        print("\n=== 测试8：响应格式 ===")

        if not self.admin_token:
            self.log("响应格式测试", False, "缺少管理员 Token")
            return

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/admin/analytics/ingredient-pairs/')

        # 检查响应结构
        has_code = 'code' in response.data
        has_message = 'message' in response.data
        has_data = 'data' in response.data

        self.log(
            "响应包含 code/message/data",
            all([has_code, has_message, has_data]),
            f"缺失字段: {self._get_missing_fields(response.data, ['code', 'message', 'data'])}"
        )

        # 检查 code=200
        self.log(
            "响应 code=200",
            response.data.get('code') == 200,
            f"实际 code: {response.data.get('code')}"
        )

        # 检查 message 非空
        self.log(
            "响应 message 非空",
            bool(response.data.get('message')),
            f"message: {response.data.get('message')}"
        )

    def _get_missing_fields(self, data, expected_fields):
        """获取缺失的字段"""
        missing = []
        for field in expected_fields:
            if field not in data:
                missing.append(field)
        return missing if missing else "无"

    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "="*60)
        print("测试摘要")
        print("="*60)

        passed = sum(1 for r in self.test_results if "PASS" in r['status'])
        failed = sum(1 for r in self.test_results if "FAIL" in r['status'])
        total = len(self.test_results)

        print(f"总计: {total} 个测试")
        print(f"通过: {passed} 个")
        print(f"失败: {failed} 个")
        print(f"成功率: {passed/total*100:.1f}%")

        if failed > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if "FAIL" in result['status']:
                    print(f"  - {result['test']}: {result['message']}")

        print("="*60)

    def run_all_tests(self):
        """运行所有测试"""
        print("="*60)
        print("食材关联分析接口测试")
        print("="*60)

        self.setup_users()
        self.test_permission_check()
        self.test_default_response()
        self.test_limit_parameter()
        self.test_min_count_parameter()
        self.test_category_parameter()
        self.test_data_accuracy()
        self.test_edge_cases()
        self.test_response_format()

        self.print_summary()


if __name__ == '__main__':
    tester = IngredientPairsAnalysisTest()
    tester.run_all_tests()
