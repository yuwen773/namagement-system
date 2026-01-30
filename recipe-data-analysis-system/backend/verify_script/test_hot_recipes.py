"""
热门菜谱接口测试脚本

测试接口：GET /api/recipes/hot/

测试场景：
1. 获取默认热门菜谱（按点击量，Top 20）
2. 按收藏量排序获取热门菜谱
3. 自定义返回数量
4. 测试限制数量的边界值
5. 测试无效的排序参数
6. 测试无效的数量参数
"""

import requests
import json
import sys
from datetime import datetime

# 设置输出编码为 UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class HotRecipesTester:
    """热门菜谱接口测试器"""

    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.api_url = f'{base_url}/api/recipes/hot/'
        self.test_results = []
        self.passed = 0
        self.failed = 0

    def print_test_header(self, test_name):
        """打印测试标题"""
        print(f"\n{'='*60}")
        print(f"测试: {test_name}")
        print(f"{'='*60}")

    def print_test_result(self, test_name, passed, details=None):
        """打印测试结果"""
        status = "[通过]" if passed else "[失败]"
        print(f"\n{status} {test_name}")
        if details:
            print(f"详情: {details}")
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def test_1_default_hot_recipes(self):
        """测试1: 获取默认热门菜谱（按点击量，Top 20）"""
        self.print_test_header("默认热门菜谱（按点击量，Top 20）")

        params = {}
        print(f"请求参数: {params}")

        try:
            response = requests.get(self.api_url, params=params)
            print(f"响应状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}...")

                # 验证响应结构
                assert data['code'] == 200, "code 应为 200"
                assert 'data' in data, "应包含 data 字段"
                assert 'results' in data['data'], "data 应包含 results 字段"
                assert 'sort_by' in data['data'], "data 应包含 sort_by 字段"
                assert 'limit' in data['data'], "data 应包含 limit 字段"

                # 验证默认值
                assert data['data']['sort_by'] == 'view_count', "默认排序应为 view_count"
                assert data['data']['limit'] == 20, "默认数量应为 20"
                assert data['data']['count'] <= 20, "返回数量应 <= 20"

                # 验证排序是否正确（点击量降序）
                results = data['data']['results']
                if len(results) > 1:
                    for i in range(len(results) - 1):
                        assert results[i]['view_count'] >= results[i+1]['view_count'], \
                            "应按点击量降序排列"

                self.print_test_result(
                    "默认热门菜谱",
                    True,
                    f"返回 {len(results)} 条菜谱，按点击量降序排列"
                )
            else:
                self.print_test_result(
                    "默认热门菜谱",
                    False,
                    f"状态码错误: {response.status_code}"
                )

        except Exception as e:
            self.print_test_result("默认热门菜谱", False, str(e))

    def test_2_sort_by_favorite_count(self):
        """测试2: 按收藏量排序获取热门菜谱"""
        self.print_test_header("按收藏量排序的热门菜谱")

        params = {'sort_by': 'favorite_count'}
        print(f"请求参数: {params}")

        try:
            response = requests.get(self.api_url, params=params)
            print(f"响应状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                # 验证排序参数
                assert data['data']['sort_by'] == 'favorite_count', "排序应为 favorite_count"

                # 验证排序是否正确（收藏量降序）
                results = data['data']['results']
                if len(results) > 1:
                    for i in range(len(results) - 1):
                        assert results[i]['favorite_count'] >= results[i+1]['favorite_count'], \
                            "应按收藏量降序排列"

                self.print_test_result(
                    "按收藏量排序",
                    True,
                    f"返回 {len(results)} 条菜谱，按收藏量降序排列"
                )
            else:
                self.print_test_result(
                    "按收藏量排序",
                    False,
                    f"状态码错误: {response.status_code}"
                )

        except Exception as e:
            self.print_test_result("按收藏量排序", False, str(e))

    def test_3_custom_limit(self):
        """测试3: 自定义返回数量"""
        self.print_test_header("自定义返回数量（10条）")

        params = {'limit': 10}
        print(f"请求参数: {params}")

        try:
            response = requests.get(self.api_url, params=params)
            print(f"响应状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                assert data['data']['limit'] == 10, "limit 应为 10"
                assert data['data']['count'] <= 10, "返回数量应 <= 10"

                self.print_test_result(
                    "自定义返回数量",
                    True,
                    f"返回 {data['data']['count']} 条菜谱"
                )
            else:
                self.print_test_result(
                    "自定义返回数量",
                    False,
                    f"状态码错误: {response.status_code}"
                )

        except Exception as e:
            self.print_test_result("自定义返回数量", False, str(e))

    def test_4_limit_boundary_values(self):
        """测试4: 限制数量的边界值"""
        self.print_test_header("限制数量边界值测试")

        test_cases = [
            (0, 20, "0 应使用默认值 20"),
            (1, 1, "1 应返回 1 条"),
            (50, 50, "50 应返回 50 条"),
            (100, 50, "100 应限制为最大值 50"),
            (-5, 20, "负数应使用默认值 20"),
        ]

        all_passed = True

        for limit_value, expected_count, description in test_cases:
            print(f"\n--- 测试: {description} ---")
            params = {'limit': limit_value}
            print(f"请求参数: limit={limit_value}")

            try:
                response = requests.get(self.api_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    actual_count = data['data']['count']

                    if actual_count <= expected_count and data['data']['limit'] == expected_count:
                        print(f"[通过] 返回 {actual_count} 条，limit={data['data']['limit']}")
                    else:
                        print(f"[失败] 期望 limit={expected_count}, 实际 limit={data['data']['limit']}, 返回 {actual_count} 条")
                        all_passed = False
                else:
                    print(f"[失败] 状态码 {response.status_code}")
                    all_passed = False

            except Exception as e:
                print(f"[失败] {str(e)}")
                all_passed = False

        self.print_test_result(
            "限制数量边界值",
            all_passed,
            "所有边界值测试"
        )

    def test_5_invalid_sort_by(self):
        """测试5: 无效的排序参数"""
        self.print_test_header("无效的排序参数")

        params = {'sort_by': 'invalid_field'}
        print(f"请求参数: {params}")

        try:
            response = requests.get(self.api_url, params=params)
            print(f"响应状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                # 无效参数应回退到默认值
                assert data['data']['sort_by'] == 'view_count', "无效参数应使用默认值 view_count"

                self.print_test_result(
                    "无效排序参数",
                    True,
                    "无效参数回退到默认值 view_count"
                )
            else:
                self.print_test_result(
                    "无效排序参数",
                    False,
                    f"状态码错误: {response.status_code}"
                )

        except Exception as e:
            self.print_test_result("无效排序参数", False, str(e))

    def test_6_invalid_limit(self):
        """测试6: 无效的数量参数"""
        self.print_test_header("无效的数量参数")

        test_cases = [
            ('abc', 20, "字符串应使用默认值"),
            ('10.5', 20, "小数应使用默认值"),
        ]

        all_passed = True

        for limit_value, expected_limit, description in test_cases:
            print(f"\n--- 测试: {description} ---")
            params = {'limit': limit_value}
            print(f"请求参数: limit={limit_value}")

            try:
                response = requests.get(self.api_url, params=params)
                if response.status_code == 200:
                    data = response.json()

                    if data['data']['limit'] == expected_limit:
                        print(f"[通过] limit={data['data']['limit']}")
                    else:
                        print(f"[失败] 期望 limit={expected_limit}, 实际 limit={data['data']['limit']}")
                        all_passed = False
                else:
                    print(f"[失败] 状态码 {response.status_code}")
                    all_passed = False

            except Exception as e:
                print(f"[失败] {str(e)}")
                all_passed = False

        self.print_test_result(
            "无效数量参数",
            all_passed,
            "所有无效参数测试"
        )

    def run_all_tests(self):
        """运行所有测试"""
        print(f"\n{'#'*60}")
        print(f"# 热门菜谱接口测试")
        print(f"# API: {self.api_url}")
        print(f"# 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}")

        self.test_1_default_hot_recipes()
        self.test_2_sort_by_favorite_count()
        self.test_3_custom_limit()
        self.test_4_limit_boundary_values()
        self.test_5_invalid_sort_by()
        self.test_6_invalid_limit()

        # 打印测试总结
        self.print_summary()

    def print_summary(self):
        """打印测试总结"""
        print(f"\n{'='*60}")
        print(f"测试总结")
        print(f"{'='*60}")
        print(f"总测试数: {self.passed + self.failed}")
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        print(f"成功率: {self.passed / (self.passed + self.failed) * 100:.1f}%")

        if self.failed == 0:
            print(f"\n[成功] 所有测试通过！")
        else:
            print(f"\n[警告] 有 {self.failed} 个测试失败，请检查")

        print(f"{'='*60}\n")


if __name__ == '__main__':
    tester = HotRecipesTester()
    tester.run_all_tests()
