"""
难度等级统计接口测试脚本

测试 GET /api/analytics/difficulty/ 接口

测试项目：
1. 数据获取 - 能正常获取难度统计数据
2. 结构验证 - 返回数据包含 name, value, count, percentage, avg_cooking_time 字段
3. 数量总和 - 各难度数量总和等于总菜谱数
4. 占比计算 - 百分比总和等于 100（允许小误差）
5. 排序验证 - 按数量降序排列
6. 空值处理 - 平均烹饪时间为 None 时返回 0
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


class TestDifficultyStats:
    """难度等级统计测试类"""

    def __init__(self):
        self.client = Client()
        self.url = '/api/analytics/difficulty/'
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
        """测试1：数据获取 - 能正常获取难度统计数据"""
        response = self.client.get(self.url)
        response_data = response.json()

        is_passed = (
            response_data.get('code') == 200 and
            isinstance(response_data.get('data'), list) and
            len(response_data.get('data', [])) > 0
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

        first_item = data[0]
        required_fields = ['name', 'value', 'count', 'percentage', 'avg_cooking_time']

        missing_fields = [f for f in required_fields if f not in first_item]
        is_passed = len(missing_fields) == 0

        details = (
            f"包含所有字段: {required_fields}" if is_passed
            else f"缺少字段: {missing_fields}"
        )
        self.log_test("结构验证", is_passed, details)

    def test_3_count_sum(self, data):
        """测试3：数量总和 - 各难度数量总和等于总菜谱数"""
        if not data:
            self.log_test("数量总和", False, "数据为空，无法验证")
            return

        api_total = sum(item['count'] for item in data)
        db_total = Recipe.objects.count()

        is_passed = api_total == db_total
        details = f"API总和: {api_total}, 数据库总数: {db_total}"
        self.log_test("数量总和", is_passed, details)

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

        details = f"排序: {[item['count'] for item in data]}"
        self.log_test("排序验证", is_sorted, details)

    def test_6_null_handling(self):
        """测试6：空值处理 - avg_cooking_time 应该是数值类型"""
        response = self.client.get(self.url)
        data = response.json().get('data', [])

        if not data:
            self.log_test("空值处理", False, "数据为空，无法验证")
            return

        is_passed = all(
            isinstance(item.get('avg_cooking_time'), (int, float))
            for item in data
        )

        avg_times = [item.get('avg_cooking_time') for item in data]
        details = f"平均烹饪时长: {avg_times}"
        self.log_test("空值处理", is_passed, details)

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("难度等级统计接口测试")
        print("=" * 60)
        print()

        # 测试1：数据获取
        data = self.test_1_data_fetch()

        # 测试2：结构验证
        self.test_2_structure_validation(data)

        # 测试3：数量总和
        self.test_3_count_sum(data)

        # 测试4：占比计算
        self.test_4_percentage_calculation(data)

        # 测试5：排序验证
        self.test_5_sorting(data)

        # 测试6：空值处理
        self.test_6_null_handling()

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
            for item in data:
                print(f"  {item['name']}: {item['count']} 个 ({item['percentage']}%)")
                print(f"    平均烹饪时长: {item['avg_cooking_time']} 分钟")
            print("-" * 60)

        return self.passed_tests == self.total_tests


if __name__ == '__main__':
    tester = TestDifficultyStats()
    all_passed = tester.run_all_tests()
    sys.exit(0 if all_passed else 1)
