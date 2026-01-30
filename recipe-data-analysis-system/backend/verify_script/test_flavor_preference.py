"""
口味偏好分析接口测试脚本

测试 GET /api/analytics/flavors/ 接口

测试项目：
1. 数据获取 - 能正常获取口味偏好数据
2. 结构验证 - 返回数据包含 name, count, percentage 字段
3. 数量验证 - 统计的口味数量合理
4. 占比计算 - 百分比总和约等于 100（允许小误差）
5. 排序验证 - 按数量降序排列
6. 数据类型 - 字段类型正确（count 为 int，percentage 为 float）
"""
import os
import sys
import django
import json

# 设置控制台输出编码为 UTF-8（兼容 Windows）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recipes.models import Recipe
from django.test import Client
from django.urls import reverse


class TestFlavorPreference:
    """口味偏好分析测试类"""

    def __init__(self):
        self.client = Client()
        self.url = '/api/analytics/flavors/'
        self.passed_tests = 0
        self.total_tests = 6
        self.test_results = []

    def log_test(self, test_name, passed, details=""):
        """记录测试结果"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append(f"{status} - {test_name}")
        if details:
            self.test_results.append(f"    {details}")
        if passed:
            self.passed_tests += 1
        print(f"{status} - {test_name}")
        if details:
            print(f"    {details}")

    def test_1_data_fetch(self):
        """测试1：数据获取 - 能正常获取口味偏好数据"""
        response = self.client.get(self.url)
        response_data = response.json()

        is_passed = (
            response_data.get('code') == 200 and
            isinstance(response_data.get('data'), list)
        )

        data = response_data.get('data', [])
        details = f"返回数据量: {len(data)}" if is_passed else f"响应: {response_data}"
        self.log_test("数据获取", is_passed, details)

        return data if is_passed else None

    def test_2_structure_validation(self, data):
        """测试2：结构验证 - 返回数据包含必要字段"""
        if not data:
            self.log_test("结构验证", False, "数据为空，无法验证")
            return

        first_item = data[0] if data else {}
        required_fields = ['name', 'count', 'percentage']

        missing_fields = [f for f in required_fields if f not in first_item]
        is_passed = len(missing_fields) == 0

        details = (
            f"包含所有字段: {required_fields}" if is_passed
            else f"缺少字段: {missing_fields}"
        )
        self.log_test("结构验证", is_passed, details)

    def test_3_count_validation(self, data):
        """测试3：数量验证 - 统计的口味数量合理"""
        if not data:
            self.log_test("数量验证", False, "数据为空，无法验证")
            return

        total_count = sum(item['count'] for item in data)

        # 检查数据库中有口味标签的菜谱数量
        recipes_with_flavors = Recipe.objects.exclude(
            flavor_tags=''
        ).exclude(flavor_tags__isnull=True).count()

        is_passed = total_count >= recipes_with_flavors

        details = f"API统计总数: {total_count}, 数据库有口味标签的菜谱: {recipes_with_flavors}"
        self.log_test("数量验证", is_passed, details)

    def test_4_percentage_calculation(self, data):
        """测试4：占比计算 - 百分比总和约等于 100"""
        if not data:
            self.log_test("占比计算", False, "数据为空，无法验证")
            return

        total_percentage = sum(item['percentage'] for item in data)
        is_passed = 99.99 <= total_percentage <= 100.01

        details = f"百分比总和: {total_percentage}%"
        self.log_test("占比计算", is_passed, details)

    def test_5_sorting(self, data):
        """测试5：排序验证 - 按数量降序排列"""
        if not data:
            self.log_test("排序验证", False, "数据为空，无法验证")
            return

        counts = [item['count'] for item in data]
        is_sorted = all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1))

        details = f"排序: {[item['count'] for item in data[:5]]}{'...' if len(data) > 5 else ''}"
        self.log_test("排序验证", is_sorted, details)

    def test_6_data_types(self, data):
        """测试6：数据类型 - 字段类型正确"""
        if not data:
            self.log_test("数据类型", False, "数据为空，无法验证")
            return

        is_passed = all(
            isinstance(item.get('name'), str) and
            isinstance(item.get('count'), int) and
            isinstance(item.get('percentage'), (int, float))
            for item in data
        )

        details = f"数据类型检查通过" if is_passed else f"数据类型不正确"
        self.log_test("数据类型", is_passed, details)

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("口味偏好分析接口测试")
        print("=" * 60)
        print()

        # 测试1：数据获取
        data = self.test_1_data_fetch()

        # 测试2：结构验证
        self.test_2_structure_validation(data)

        # 测试3：数量验证
        self.test_3_count_validation(data)

        # 测试4：占比计算
        self.test_4_percentage_calculation(data)

        # 测试5：排序验证
        self.test_5_sorting(data)

        # 测试6：数据类型
        self.test_6_data_types(data)

        # 输出测试摘要
        print()
        print("=" * 60)
        print(f"测试结果: {self.passed_tests}/{self.total_tests} 通过")
        print("=" * 60)

        # 输出数据预览
        if data:
            print()
            print("数据预览:")
            print("-" * 60)
            for item in data[:10]:
                print(f"  {item['name']}: {item['count']} 个 ({item['percentage']}%)")
            if len(data) > 10:
                print(f"  ... (共 {len(data)} 种口味)")
            print("-" * 60)

        return self.passed_tests == self.total_tests


if __name__ == '__main__':
    tester = TestFlavorPreference()
    all_passed = tester.run_all_tests()
    sys.exit(0 if all_passed else 1)
