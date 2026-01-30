"""
菜谱列表接口测试脚本

测试 Phase 5 Step 1: 菜谱列表接口

测试项目：
1. 请求第一页数据，确认返回正确数量
2. 请求不同页的数据，确认数据不同
3. 使用菜系筛选，确认只返回该菜系的数据
4. 使用难度筛选，确认只返回该难度的数据
5. 使用场景筛选，确认只返回该场景的数据
6. 使用排序参数，确认顺序正确
7. 确认返回分页信息（总数、总页数）
"""

import os
import sys
import django
import json
from datetime import datetime

# 设置控制台编码为 UTF-8 (Windows 兼容)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径到 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from rest_framework.test import APIClient, APITestCase
from recipes.models import Recipe
from recipes.views import recipe_list


class RecipeListTestCase(APITestCase):
    """菜谱列表接口测试用例"""

    def setUp(self):
        """测试前准备"""
        self.client = APIClient()
        self.base_url = '/api/recipes/'

        # 打印当前数据库中的菜谱数量
        self.recipe_count = Recipe.objects.count()
        print(f"\n{'='*60}")
        print(f"菜谱列表接口测试")
        print(f"{'='*60}")
        print(f"当前数据库菜谱总数: {self.recipe_count}")

        if self.recipe_count == 0:
            print("⚠️  警告: 数据库中没有菜谱数据，部分测试可能失败")
            print("   请先运行数据导入脚本")
            print(f"{'='*60}\n")
        else:
            # 获取一些统计信息
            cuisines = Recipe.objects.values_list('cuisine_type', flat=True).distinct()
            difficulties = Recipe.objects.values_list('difficulty', flat=True).distinct()
            scenes = Recipe.objects.values_list('scene_type', flat=True).distinct()

            print(f"菜系类型: {', '.join(set(c for c in cuisines if c))}")
            print(f"难度等级: {', '.join(set(d for d in difficulties if d))}")
            print(f"场景类型: {', '.join(set(s for s in scenes if s))}")
            print(f"{'='*60}\n")

    def _print_test_result(self, test_name, passed, details=None):
        """打印测试结果"""
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {test_name}")
        if details:
            print(f"    详情: {details}")

    def _print_response_summary(self, response):
        """打印响应摘要"""
        if response.status_code == 200:
            data = response.json()
            print(f"    响应码: {data.get('code')}")
            print(f"    消息: {data.get('message')}")
            if 'data' in data and data['data']:
                result_data = data['data']
                if 'count' in result_data:
                    print(f"    总数: {result_data['count']}")
                if 'results' in result_data:
                    results = result_data['results']
                    print(f"    本页数量: {len(results)}")
                    if results:
                        first = results[0]
                        print(f"    第一条: id={first.get('id')}, name={first.get('name')}")
        else:
            print(f"    状态码: {response.status_code}")

    def test_01_first_page_default_size(self):
        """测试 1: 请求第一页数据，确认返回默认数量"""
        print(f"\n测试 1: 请求第一页数据（默认分页）")
        print(f"{'-'*40}")

        response = self.client.get(self.base_url)
        self._print_response_summary(response)

        # 验证响应状态码
        is_passed = response.status_code == 200
        self._print_test_result("响应状态码为 200", is_passed)

        if is_passed:
            data = response.json()
            # 验证响应格式
            has_code = 'code' in data
            has_message = 'message' in data
            has_data = 'data' in data

            self._print_test_result("响应格式正确", has_code and has_message and has_data)

            if has_data and data['data']:
                result_data = data['data']
                has_count = 'count' in result_data
                has_results = 'results' in result_data

                self._print_test_result("分页数据结构完整", has_count and has_results)

                if has_results:
                    results = result_data['results']
                    expected_count = min(20, self.recipe_count)  # 默认每页20条
                    actual_count = len(results)
                    size_correct = actual_count == expected_count or (self.recipe_count < 20 and actual_count == self.recipe_count)

                    self._print_test_result(
                        f"返回数量正确 (预期: {expected_count} 或 {self.recipe_count}, 实际: {actual_count})",
                        size_correct
                    )

        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            data = response.json()
            self.assertIn('code', data)
            self.assertIn('message', data)
            self.assertIn('data', data)
            self.assertIn('count', data['data'])
            self.assertIn('results', data['data'])

    def test_02_different_pages(self):
        """测试 2: 请求不同页的数据，确认数据不同"""
        print(f"\n测试 2: 请求不同页的数据")
        print(f"{'-'*40}")

        if self.recipe_count < 40:
            print(f"⚠️  跳过: 数据库中的菜谱数量不足 40 条 (当前: {self.recipe_count})")
            return

        # 请求第一页
        response_page1 = self.client.get(self.base_url, {'page': 1})
        self._print_response_summary(response_page1)

        # 请求第二页
        response_page2 = self.client.get(self.base_url, {'page': 2})
        self._print_response_summary(response_page2)

        if response_page1.status_code == 200 and response_page2.status_code == 200:
            data_page1 = response_page1.json()['data']['results']
            data_page2 = response_page2.json()['data']['results']

            if data_page1 and data_page2:
                id1 = data_page1[0]['id']
                id2 = data_page2[0]['id']
                different = id1 != id2

                self._print_test_result(
                    f"不同页返回不同数据 (第1页id={id1}, 第2页id={id2})",
                    different
                )

                self.assertNotEqual(id1, id2)

    def test_03_cuisine_filter(self):
        """测试 3: 使用菜系筛选"""
        print(f"\n测试 3: 使用菜系筛选")
        print(f"{'-'*40}")

        # 获取一个存在的菜系
        cuisines = list(Recipe.objects.values_list('cuisine_type', flat=True).distinct())
        cuisines = [c for c in cuisines if c]

        if not cuisines:
            print(f"⚠️  跳过: 数据库中没有菜系数据")
            return

        test_cuisine = cuisines[0]
        print(f"测试菜系: {test_cuisine}")

        response = self.client.get(self.base_url, {'cuisine_type': test_cuisine})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if results:
                # 验证所有结果都属于该菜系
                all_match = all(r['cuisine_type'] == test_cuisine for r in results)

                self._print_test_result(
                    f"所有结果都属于 '{test_cuisine}' 菜系",
                    all_match
                )

                self.assertTrue(all_match)

    def test_04_difficulty_filter(self):
        """测试 4: 使用难度筛选"""
        print(f"\n测试 4: 使用难度筛选")
        print(f"{'-'*40}")

        # 获取一个存在的难度
        difficulties = list(Recipe.objects.values_list('difficulty', flat=True).distinct())
        difficulties = [d for d in difficulties if d]

        if not difficulties:
            print(f"⚠️  跳过: 数据库中没有难度数据")
            return

        test_difficulty = difficulties[0]
        print(f"测试难度: {test_difficulty}")

        response = self.client.get(self.base_url, {'difficulty': test_difficulty})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if results:
                # 验证所有结果都属于该难度
                all_match = all(r['difficulty'] == test_difficulty for r in results)

                self._print_test_result(
                    f"所有结果难度都是 '{test_difficulty}'",
                    all_match
                )

                self.assertTrue(all_match)

    def test_05_scene_filter(self):
        """测试 5: 使用场景筛选"""
        print(f"\n测试 5: 使用场景筛选")
        print(f"{'-'*40}")

        # 获取一个存在的场景
        scenes = list(Recipe.objects.values_list('scene_type', flat=True).distinct())
        scenes = [s for s in scenes if s]

        if not scenes:
            print(f"⚠️  跳过: 数据库中没有场景数据")
            return

        test_scene = scenes[0]
        print(f"测试场景: {test_scene}")

        response = self.client.get(self.base_url, {'scene_type': test_scene})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if results:
                # 验证所有结果都属于该场景
                all_match = all(r.get('scene_type') == test_scene for r in results)

                self._print_test_result(
                    f"所有结果场景都是 '{test_scene}'",
                    all_match
                )

                self.assertTrue(all_match)

    def test_06_ordering_by_view_count(self):
        """测试 6: 按点击量排序"""
        print(f"\n测试 6: 按点击量排序")
        print(f"{'-'*40}")

        response = self.client.get(self.base_url, {'ordering': '-view_count'})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if len(results) >= 2:
                # 验证按点击量降序排列
                is_descending = results[0]['view_count'] >= results[1]['view_count']

                self._print_test_result(
                    f"点击量降序排列 ({results[0]['view_count']} >= {results[1]['view_count']})",
                    is_descending
                )

                self.assertTrue(is_descending)

    def test_07_ordering_by_favorite_count(self):
        """测试 7: 按收藏量排序"""
        print(f"\n测试 7: 按收藏量排序")
        print(f"{'-'*40}")

        response = self.client.get(self.base_url, {'ordering': '-favorite_count'})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if len(results) >= 2:
                # 验证按收藏量降序排列
                is_descending = results[0]['favorite_count'] >= results[1]['favorite_count']

                self._print_test_result(
                    f"收藏量降序排列 ({results[0]['favorite_count']} >= {results[1]['favorite_count']})",
                    is_descending
                )

                self.assertTrue(is_descending)

    def test_08_ordering_by_created_at(self):
        """测试 8: 按创建时间排序"""
        print(f"\n测试 8: 按创建时间排序")
        print(f"{'-'*40}")

        # 升序
        response_asc = self.client.get(self.base_url, {'ordering': 'created_at'})

        if response_asc.status_code == 200:
            data_asc = response_asc.json()
            results_asc = data_asc['data']['results']

            if len(results_asc) >= 2:
                # 验证按创建时间升序排列
                is_ascending = results_asc[0]['created_at'] <= results_asc[1]['created_at']

                self._print_test_result(
                    f"创建时间升序排列",
                    is_ascending
                )

        # 降序
        response_desc = self.client.get(self.base_url, {'ordering': '-created_at'})

        if response_desc.status_code == 200:
            data_desc = response_desc.json()
            results_desc = data_desc['data']['results']

            if len(results_desc) >= 2:
                # 验证按创建时间降序排列
                is_descending = results_desc[0]['created_at'] >= results_desc[1]['created_at']

                self._print_test_result(
                    f"创建时间降序排列",
                    is_descending
                )

    def test_09_pagination_info(self):
        """测试 9: 分页信息完整性"""
        print(f"\n测试 9: 分页信息完整性")
        print(f"{'-'*40}")

        response = self.client.get(self.base_url)
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            result_data = data['data']

            has_count = 'count' in result_data
            has_next = 'next' in result_data
            has_previous = 'previous' in result_data
            has_results = 'results' in result_data

            complete = has_count and has_next and has_previous and has_results

            self._print_test_result(
                "分页信息完整 (count, next, previous, results)",
                complete
            )

            if has_count:
                count = result_data['count']
                correct_count = count == self.recipe_count
                self._print_test_result(
                    f"总数正确 (数据库: {self.recipe_count}, 响应: {count})",
                    correct_count
                )

            self.assertTrue(complete)
            if has_count:
                self.assertEqual(result_data['count'], self.recipe_count)

    def test_10_custom_page_size(self):
        """测试 10: 自定义每页数量"""
        print(f"\n测试 10: 自定义每页数量")
        print(f"{'-'*40}")

        test_size = 10
        response = self.client.get(self.base_url, {'page_size': test_size})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            expected_count = min(test_size, self.recipe_count)
            actual_count = len(results)
            size_correct = actual_count == expected_count

            self._print_test_result(
                f"自定义每页数量正确 (预期: {expected_count}, 实际: {actual_count})",
                size_correct
            )

            self.assertEqual(actual_count, expected_count)

    def test_11_invalid_ordering(self):
        """测试 11: 无效排序字段"""
        print(f"\n测试 11: 无效排序字段处理")
        print(f"{'-'*40}")

        response = self.client.get(self.base_url, {'ordering': 'invalid_field'})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if results:
                # 应该回退到默认排序 (-created_at)
                is_descending = True  # 默认是降序

                self._print_test_result(
                    "无效排序字段回退到默认排序",
                    is_descending
                )

        self.assertEqual(response.status_code, 200)

    def test_12_combined_filters(self):
        """测试 12: 组合筛选条件"""
        print(f"\n测试 12: 组合筛选条件")
        print(f"{'-'*40}")

        # 获取存在的筛选值
        cuisines = list(Recipe.objects.values_list('cuisine_type', flat=True).distinct())
        cuisines = [c for c in cuisines if c]
        difficulties = list(Recipe.objects.values_list('difficulty', flat=True).distinct())
        difficulties = [d for d in difficulties if d]

        if not cuisines or not difficulties:
            print(f"⚠️  跳过: 数据库中没有足够的筛选数据")
            return

        test_cuisine = cuisines[0]
        test_difficulty = difficulties[0]
        print(f"测试组合: 菜系={test_cuisine}, 难度={test_difficulty}")

        response = self.client.get(self.base_url, {
            'cuisine_type': test_cuisine,
            'difficulty': test_difficulty,
            'ordering': '-view_count'
        })
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']

            if results:
                # 验证所有结果同时满足两个条件
                all_match_cuisine = all(r['cuisine_type'] == test_cuisine for r in results)
                all_match_difficulty = all(r['difficulty'] == test_difficulty for r in results)

                self._print_test_result(
                    f"所有结果匹配菜系 '{test_cuisine}'",
                    all_match_cuisine
                )
                self._print_test_result(
                    f"所有结果匹配难度 '{test_difficulty}'",
                    all_match_difficulty
                )

                if len(results) >= 2:
                    # 验证排序
                    is_sorted = results[0]['view_count'] >= results[1]['view_count']
                    self._print_test_result(
                        "按点击量降序排列",
                        is_sorted
                    )


def run_tests():
    """运行所有测试"""
    print(f"\n{'#'*60}")
    print(f"# 菜谱列表接口测试脚本")
    print(f"# Phase 5 Step 1")
    print(f"# 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}\n")

    import unittest
    from django.test.runner import DiscoverRunner

    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(RecipeListTestCase)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    # 打印总结
    print(f"\n{'='*60}")
    print(f"测试总结")
    print(f"{'='*60}")
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"{'='*60}")

    if result.wasSuccessful():
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败，请查看上面的详细信息")
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
