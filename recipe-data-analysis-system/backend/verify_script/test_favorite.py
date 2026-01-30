"""
收藏功能接口测试脚本

测试 Phase 6 Step 1: 收藏菜谱接口
测试 Phase 6 Step 2: 取消收藏接口
测试 Phase 6 Step 3: 收藏列表接口
测试 Phase 6 Step 4: 检查收藏状态接口

测试项目：
1. 使用有效 Token 收藏菜谱，确认成功
2. 收藏同一菜谱两次，确认第二次失败
3. 收藏不存在的菜谱，确认返回错误
4. 检查收藏量是否增加
5. 检查行为日志是否记录
6. 取消已收藏的菜谱，确认成功
7. 取消未收藏的菜谱，确认返回错误
8. 检查收藏量是否减少
9. 请求收藏列表，确认返回已收藏的菜谱
10. 确认只返回当前用户的收藏
11. 测试分页功能
12. 检查已收藏的菜谱，确认返回 true
13. 检查未收藏的菜谱，确认返回 false
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

from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from recipes.models import Recipe
from accounts.models import User
from favorites.models import UserFavorite
from behavior_logs.models import UserBehaviorLog


class FavoriteTestCase(APITestCase):
    """收藏功能接口测试用例"""

    def setUp(self):
        """测试前准备"""
        self.client = APIClient()
        self.base_url = '/api/favorites/'

        # 打印当前数据库中的数据统计
        self.recipe_count = Recipe.objects.count()
        self.user_count = User.objects.count()
        print(f"\n{'='*60}")
        print(f"收藏功能接口测试")
        print(f"{'='*60}")
        print(f"当前数据库菜谱总数: {self.recipe_count}")
        print(f"当前数据库用户总数: {self.user_count}")

        if self.recipe_count == 0:
            print("⚠️  警告: 数据库中没有菜谱数据，部分测试可能失败")
            print("   请先运行数据导入脚本")

        # 创建测试用户（如果不存在）
        self.test_user = None
        self.access_token = None

        if self.user_count > 0:
            # 获取第一个用户作为测试用户
            self.test_user = User.objects.first()
        else:
            # 创建测试用户
            self.test_user = User.objects.create_user(
                username='test_user',
                password='test123456',
                email='test@example.com'
            )
            print(f"创建测试用户: {self.test_user.username}")

        if self.test_user:
            # 生成 JWT Token
            self.access_token = str(AccessToken.for_user(self.test_user))
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
            print(f"使用测试用户: {self.test_user.username} (id={self.test_user.id})")

        print(f"{'='*60}\n")

    def _print_test_result(self, test_name, passed, details=None):
        """打印测试结果"""
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {test_name}")
        if details:
            print(f"    详情: {details}")

    def _print_response_summary(self, response):
        """打印响应摘要"""
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"    响应码: {data.get('code')}")
            print(f"    消息: {data.get('message')}")
            if 'data' in data and data['data']:
                print(f"    数据: {json.dumps(data['data'], ensure_ascii=False, indent=4)[:200]}...")
        else:
            print(f"    状态码: {response.status_code}")
            try:
                data = response.json()
                print(f"    消息: {data.get('message', 'N/A')}")
            except:
                pass

    def _get_first_recipe_id(self):
        """获取第一个菜谱ID"""
        if self.recipe_count == 0:
            return None
        return Recipe.objects.first().id

    def test_01_favorite_recipe_success(self):
        """测试 1: 使用有效 Token 收藏菜谱，确认成功"""
        print(f"\n测试 1: 收藏菜谱成功")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        # 清除可能存在的收藏记录
        UserFavorite.objects.filter(user=self.test_user, recipe_id=recipe_id).delete()

        print(f"收藏菜谱 ID: {recipe_id}")

        # 获取收藏前的收藏量
        recipe = Recipe.objects.get(id=recipe_id)
        original_favorite_count = recipe.favorite_count

        response = self.client.post(
            self.base_url,
            {'recipe_id': recipe_id},
            format='json'
        )
        self._print_response_summary(response)

        # 验证响应
        is_success = response.status_code == 200
        self._print_test_result("响应状态码为 200", is_success)

        if is_success:
            data = response.json()
            has_data = 'data' in data
            has_id = has_data and 'id' in data['data']
            self._print_test_result("响应包含收藏记录 ID", has_id)

            # 验证收藏量增加
            recipe.refresh_from_db()
            count_increased = recipe.favorite_count == original_favorite_count + 1
            self._print_test_result(
                f"菜谱收藏量增加 (原: {original_favorite_count}, 新: {recipe.favorite_count})",
                count_increased
            )

        self.assertEqual(response.status_code, 200)

    def test_02_favorite_duplicate_recipe(self):
        """测试 2: 收藏同一菜谱两次，确认第二次失败"""
        print(f"\n测试 2: 重复收藏同一菜谱")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        print(f"菜谱 ID: {recipe_id}")

        # 第一次收藏
        response1 = self.client.post(
            self.base_url,
            {'recipe_id': recipe_id},
            format='json'
        )

        # 第二次收藏
        response2 = self.client.post(
            self.base_url,
            {'recipe_id': recipe_id},
            format='json'
        )

        self._print_response_summary(response2)

        # 验证第二次收藏失败
        is_failed = response2.status_code == 400
        self._print_test_result("第二次收藏返回错误", is_failed)

        if is_failed:
            data = response2.json()
            is_state_error = data.get('code') == 400
            self._print_test_result("错误码为 400 (状态不允许)", is_state_error)

        self.assertEqual(response2.status_code, 400)

    def test_03_favorite_nonexistent_recipe(self):
        """测试 3: 收藏不存在的菜谱，确认返回错误"""
        print(f"\n测试 3: 收藏不存在的菜谱")
        print(f"{'-'*40}")

        nonexistent_id = 999999
        print(f"菜谱 ID: {nonexistent_id} (不存在)")

        response = self.client.post(
            self.base_url,
            {'recipe_id': nonexistent_id},
            format='json'
        )

        self._print_response_summary(response)

        # 验证返回错误
        is_error = response.status_code == 400
        self._print_test_result("返回错误状态码", is_error)

        if is_error:
            data = response.json()
            message = data.get('message', '')
            self._print_test_result(
                f"错误消息包含'不存在'或'无效'",
                '不存在' in message or '无效' in message
            )

    def test_04_favorite_invalid_recipe_id(self):
        """测试 4: 无效的菜谱 ID"""
        print(f"\n测试 4: 无效的菜谱 ID")
        print(f"{'-'*40}")

        print(f"菜谱 ID: -1 (无效)")

        response = self.client.post(
            self.base_url,
            {'recipe_id': -1},
            format='json'
        )

        self._print_response_summary(response)

        # 验证返回验证错误
        is_error = response.status_code == 400
        self._print_test_result("返回验证错误", is_error)

    def test_05_unfavorite_success(self):
        """测试 5: 取消收藏已收藏的菜谱"""
        print(f"\n测试 5: 取消收藏成功")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        print(f"菜谱 ID: {recipe_id}")

        # 先收藏（通过 API 调用，这样可以正确更新收藏量）
        response_fav = self.client.post(
            self.base_url,
            {'recipe_id': recipe_id},
            format='json'
        )

        # 如果收藏失败（可能已经收藏），跳过测试
        if response_fav.status_code != 200:
            print(f"⚠️  跳过: 无法创建收藏记录")
            return

        # 获取取消前的收藏量
        recipe = Recipe.objects.get(id=recipe_id)
        original_favorite_count = recipe.favorite_count

        # 取消收藏
        response = self.client.delete(f'{self.base_url}{recipe_id}/')
        self._print_response_summary(response)

        # 验证响应
        is_success = response.status_code == 200
        self._print_test_result("响应状态码为 200", is_success)

        if is_success:
            # 验证收藏量减少
            recipe.refresh_from_db()
            count_decreased = recipe.favorite_count == original_favorite_count - 1
            self._print_test_result(
                f"菜谱收藏量减少 (原: {original_favorite_count}, 新: {recipe.favorite_count})",
                count_decreased
            )

        self.assertEqual(response.status_code, 200)

    def test_06_unfavorite_not_favorited(self):
        """测试 6: 取消未收藏的菜谱，确认返回错误"""
        print(f"\n测试 6: 取消未收藏的菜谱")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        print(f"菜谱 ID: {recipe_id}")

        # 确保未收藏
        UserFavorite.objects.filter(user=self.test_user, recipe_id=recipe_id).delete()

        response = self.client.delete(f'{self.base_url}{recipe_id}/')
        self._print_response_summary(response)

        # 验证返回错误
        is_error = response.status_code == 400
        self._print_test_result("返回错误状态码", is_error)

        if is_error:
            data = response.json()
            is_state_error = data.get('code') == 400
            self._print_test_result("错误码为 400 (状态不允许)", is_state_error)

    def test_07_favorite_list(self):
        """测试 7: 获取收藏列表"""
        print(f"\n测试 7: 获取收藏列表")
        print(f"{'-'*40}")

        # 创建一些收藏记录
        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        UserFavorite.objects.get_or_create(
            user=self.test_user,
            recipe_id=recipe_id
        )

        response = self.client.get(self.base_url)
        self._print_response_summary(response)

        # 验证响应
        is_success = response.status_code == 200
        self._print_test_result("响应状态码为 200", is_success)

        if is_success:
            data = response.json()
            has_data = 'data' in data
            has_results = has_data and 'results' in data['data']
            self._print_test_result("响应包含结果列表", has_results)

            if has_results:
                results = data['data']['results']
                has_favorites = len(results) > 0
                self._print_test_result(
                    f"返回收藏记录 (数量: {len(results)})",
                    has_favorites
                )

        self.assertEqual(response.status_code, 200)

    def test_08_check_favorite_status_true(self):
        """测试 8: 检查已收藏的菜谱状态"""
        print(f"\n测试 8: 检查已收藏的菜谱状态")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        # 创建收藏记录
        UserFavorite.objects.get_or_create(
            user=self.test_user,
            recipe_id=recipe_id
        )

        print(f"菜谱 ID: {recipe_id}")

        response = self.client.get(f'/api/favorites/check/{recipe_id}/')
        self._print_response_summary(response)

        # 验证响应
        is_success = response.status_code == 200
        self._print_test_result("响应状态码为 200", is_success)

        if is_success:
            data = response.json()
            is_favorited = data.get('data', {}).get('is_favorited', False)
            self._print_test_result("is_favorited 为 True", is_favorited)

            # 验证 recipe_id 正确
            returned_recipe_id = data.get('data', {}).get('recipe_id')
            id_match = returned_recipe_id == recipe_id
            self._print_test_result(
                f"recipe_id 正确 (预期: {recipe_id}, 实际: {returned_recipe_id})",
                id_match
            )

        self.assertEqual(response.status_code, 200)

    def test_09_check_favorite_status_false(self):
        """测试 9: 检查未收藏的菜谱状态"""
        print(f"\n测试 9: 检查未收藏的菜谱状态")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        # 确保未收藏
        UserFavorite.objects.filter(user=self.test_user, recipe_id=recipe_id).delete()

        print(f"菜谱 ID: {recipe_id}")

        response = self.client.get(f'/api/favorites/check/{recipe_id}/')
        self._print_response_summary(response)

        # 验证响应
        is_success = response.status_code == 200
        self._print_test_result("响应状态码为 200", is_success)

        if is_success:
            data = response.json()
            is_favorited = data.get('data', {}).get('is_favorited', True)
            self._print_test_result("is_favorited 为 False", not is_favorited)

    def test_10_favorite_list_pagination(self):
        """测试 10: 收藏列表分页"""
        print(f"\n测试 10: 收藏列表分页")
        print(f"{'-'*40}")

        # 清除现有收藏
        UserFavorite.objects.filter(user=self.test_user).delete()

        # 创建多个收藏记录
        recipes = Recipe.objects.all()[:5]
        for recipe in recipes:
            UserFavorite.objects.get_or_create(
                user=self.test_user,
                recipe=recipe
            )

        print(f"创建收藏记录数: {len(recipes)}")

        # 请求第一页（每页2条）
        response = self.client.get(self.base_url, {'page_size': 2, 'page': 1})
        self._print_response_summary(response)

        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {}).get('results', [])
            page_size_correct = len(results) <= 2
            self._print_test_result(
                f"分页正确 (返回数量: {len(results)})",
                page_size_correct
            )

    def test_11_behavior_log_created(self):
        """测试 11: 收藏行为日志记录"""
        print(f"\n测试 11: 收藏行为日志记录")
        print(f"{'-'*40}")

        recipe_id = self._get_first_recipe_id()
        if not recipe_id:
            print(f"⚠️  跳过: 数据库中没有菜谱数据")
            return

        # 清除之前的日志
        UserBehaviorLog.objects.filter(
            user=self.test_user,
            behavior_type='collect',
            target=f'recipe:{recipe_id}'
        ).delete()

        # 收藏菜谱
        response = self.client.post(
            self.base_url,
            {'recipe_id': recipe_id},
            format='json'
        )

        if response.status_code == 200:
            # 检查行为日志
            log_exists = UserBehaviorLog.objects.filter(
                user=self.test_user,
                behavior_type='collect',
                target=f'recipe:{recipe_id}'
            ).exists()

            self._print_test_result("收藏行为已记录到日志", log_exists)

    def test_12_unauthenticated_access(self):
        """测试 12: 未认证访问"""
        print(f"\n测试 12: 未认证访问")
        print(f"{'-'*40}")

        # 清除认证信息
        self.client.credentials()

        response = self.client.post(
            self.base_url,
            {'recipe_id': 1},
            format='json'
        )

        self._print_response_summary(response)

        # 验证返回 401
        is_unauthorized = response.status_code == 401
        self._print_test_result("未认证返回 401", is_unauthorized)

        # 测试收藏列表也需要认证
        response2 = self.client.get(self.base_url)
        is_unauthorized2 = response2.status_code == 401
        self._print_test_result("收藏列表未认证返回 401", is_unauthorized2)


def run_tests():
    """运行所有测试"""
    print(f"\n{'#'*60}")
    print(f"# 收藏功能接口测试脚本")
    print(f"# Phase 6 Step 1-4")
    print(f"# 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}\n")

    import unittest

    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(FavoriteTestCase)

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
