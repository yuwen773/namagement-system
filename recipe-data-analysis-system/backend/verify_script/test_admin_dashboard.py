"""
管理员 Dashboard 接口测试脚本

本脚本测试以下接口：
1. GET /api/admin/dashboard/overview - 数据总览接口
2. GET /api/admin/dashboard/trends - 数据趋势接口
3. GET /api/admin/dashboard/behaviors - 用户行为统计接口

运行方式：
    python verify_script/test_admin_dashboard.py
"""

import os
import sys
import django
import json
from datetime import datetime, timedelta

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置 Django 环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from favorites.models import UserFavorite

User = get_user_model()


class DashboardAPITester:
    """Dashboard API 测试类"""

    def __init__(self):
        self.client = Client()
        self.admin_user = None
        self.normal_user = None
        self.admin_token = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0

    def setup_test_data(self):
        """创建测试数据"""
        print("=" * 60)
        print("【准备阶段】创建测试数据...")
        print("=" * 60)

        # 创建或获取管理员用户
        try:
            self.admin_user = User.objects.get(username='admin_dashboard_test')
            print(f"  ✅ 使用现有管理员用户: {self.admin_user.username}")
        except User.DoesNotExist:
            self.admin_user = User.objects.create_user(
                username='admin_dashboard_test',
                email='admin_dashboard_test@example.com',
                password='admin123456',
                role='admin'
            )
            print(f"  ✅ 创建管理员用户: {self.admin_user.username}")

        # 创建或获取普通用户
        try:
            self.normal_user = User.objects.get(username='user_dashboard_test')
            print(f"  ✅ 使用现有普通用户: {self.normal_user.username}")
        except User.DoesNotExist:
            self.normal_user = User.objects.create_user(
                username='user_dashboard_test',
                email='user_dashboard_test@example.com',
                password='user123456',
                role='user'
            )
            print(f"  ✅ 创建普通用户: {self.normal_user.username}")

        # 更新管理员用户的最后登录时间（用于测试活跃用户）
        self.admin_user.last_login = datetime.now()
        self.admin_user.save()

        print(f"  📊 当前数据库状态:")
        print(f"     - 用户总数: {User.objects.count()}")
        print(f"     - 菜谱总数: {Recipe.objects.count()}")
        print(f"     - 收藏总数: {UserFavorite.objects.count()}")
        print()

    def login_as_admin(self):
        """管理员登录"""
        print("=" * 60)
        print("【登录阶段】管理员登录...")
        print("=" * 60)

        response = self.client.post('/api/accounts/login/', {
            'username': 'admin_dashboard_test',
            'password': 'admin123456'
        }, content_type='application/json')

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                self.admin_token = data['data'].get('token')
                print(f"  ✅ 管理员登录成功")
                print(f"  📝 Token: {self.admin_token[:50]}..." if self.admin_token else "  ⚠️ 未返回 Token")
                print()
                return True

        print(f"  ❌ 管理员登录失败")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        print()
        return False

    def test_1_dashboard_overview_without_auth(self):
        """测试 1: 未认证访问数据总览接口（应返回 401）"""
        test_name = "未认证访问数据总览接口"
        self.total_tests += 1

        print(f"【测试 {self.total_tests}】{test_name}")
        print("-" * 60)

        response = self.client.get('/api/admin/dashboard/overview/')

        if response.status_code == 401:
            print(f"  ✅ 通过: 未认证访问返回 401")
            self.passed_tests += 1
            self.test_results.append((test_name, True, "未认证访问正确返回 401"))
        else:
            print(f"  ❌ 失败: 预期 401，实际 {response.status_code}")
            self.test_results.append((test_name, False, f"预期 401，实际 {response.status_code}"))
        print()

    def test_2_dashboard_overview_with_normal_user(self):
        """测试 2: 普通用户访问数据总览接口（应返回 403）"""
        test_name = "普通用户访问数据总览接口"
        self.total_tests += 1

        print(f"【测试 {self.total_tests}】{test_name}")
        print("-" * 60)

        # 普通用户登录
        login_response = self.client.post('/api/accounts/login/', {
            'username': 'user_dashboard_test',
            'password': 'user123456'
        }, content_type='application/json')

        token = None
        if login_response.status_code == 200:
            data = login_response.json()
            if data.get('code') == 200:
                token = data['data'].get('token')

        if not token:
            print(f"  ⚠️ 跳过: 无法获取普通用户 Token")
            self.test_results.append((test_name, None, "无法获取普通用户 Token"))
            print()
            return

        response = self.client.get('/api/admin/dashboard/overview/',
                                   HTTP_AUTHORIZATION=f'Bearer {token}')

        if response.status_code == 403:
            print(f"  ✅ 通过: 普通用户访问返回 403")
            self.passed_tests += 1
            self.test_results.append((test_name, True, "普通用户访问正确返回 403"))
        else:
            print(f"  ❌ 失败: 预期 403，实际 {response.status_code}")
            self.test_results.append((test_name, False, f"预期 403，实际 {response.status_code}"))
        print()

    def test_3_dashboard_overview_success(self):
        """测试 3: 管理员访问数据总览接口（应成功）"""
        test_name = "管理员访问数据总览接口"
        self.total_tests += 1

        print(f"【测试 {self.total_tests}】{test_name}")
        print("-" * 60)

        if not self.admin_token:
            print(f"  ⚠️ 跳过: 管理员未登录")
            self.test_results.append((test_name, None, "管理员未登录"))
            print()
            return

        response = self.client.get('/api/admin/dashboard/overview/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                result = data.get('data', {})
                print(f"  ✅ 通过: 接口调用成功")
                print(f"  📊 返回数据:")
                print(f"     - 总菜谱数: {result.get('total_recipes', 0)}")
                print(f"     - 总用户数: {result.get('total_users', 0)}")
                print(f"     - 今日新增菜谱: {result.get('today_new_recipes', 0)}")
                print(f"     - 今日新增用户: {result.get('today_new_users', 0)}")
                print(f"     - 今日活跃用户: {result.get('today_active_users', 0)}")
                print(f"     - 总收藏数: {result.get('total_favorites', 0)}")

                # 验证必需字段
                required_fields = ['total_recipes', 'total_users', 'today_new_recipes',
                                 'today_new_users', 'today_active_users', 'total_favorites']
                missing_fields = [f for f in required_fields if f not in result]

                if missing_fields:
                    print(f"  ⚠️ 警告: 缺少字段: {', '.join(missing_fields)}")
                    self.test_results.append((test_name, True, "接口调用成功但缺少部分字段"))
                else:
                    self.passed_tests += 1
                    self.test_results.append((test_name, True, "接口调用成功，数据完整"))
            else:
                print(f"  ❌ 失败: 业务错误 - {data.get('message', 'Unknown error')}")
                self.test_results.append((test_name, False, f"业务错误: {data.get('message')}"))
        else:
            print(f"  ❌ 失败: HTTP 状态码 {response.status_code}")
            print(f"  响应: {response.json()}")
            self.test_results.append((test_name, False, f"HTTP 状态码: {response.status_code}"))
        print()

    def test_4_dashboard_trends_default_params(self):
        """测试 4: 数据趋势接口（默认参数）"""
        test_name = "数据趋势接口（默认参数）"
        self.total_tests += 1

        print(f"【测试 {self.total_tests}】{test_name}")
        print("-" * 60)

        if not self.admin_token:
            print(f"  ⚠️ 跳过: 管理员未登录")
            self.test_results.append((test_name, None, "管理员未登录"))
            print()
            return

        response = self.client.get('/api/admin/dashboard/trends/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                result = data.get('data', {})
                print(f"  ✅ 通过: 接口调用成功")
                print(f"  📊 返回数据:")
                print(f"     - 时间范围: {result.get('period', 'N/A')}")
                print(f"     - 天数: {result.get('days', 0)}")
                print(f"     - 数据点数量: {len(result.get('data', {}).get('dates', []))}")

                # 验证数据结构
                if 'data' in result and 'dates' in result['data']:
                    self.passed_tests += 1
                    self.test_results.append((test_name, True, "接口调用成功，数据结构正确"))
                else:
                    print(f"  ⚠️ 警告: 数据结构不完整")
                    self.test_results.append((test_name, True, "接口调用成功但数据结构不完整"))
            else:
                print(f"  ❌ 失败: 业务错误 - {data.get('message', 'Unknown error')}")
                self.test_results.append((test_name, False, f"业务错误: {data.get('message')}"))
        else:
            print(f"  ❌ 失败: HTTP 状态码 {response.status_code}")
            self.test_results.append((test_name, False, f"HTTP 状态码: {response.status_code}"))
        print()

    def test_5_dashboard_trends_custom_params(self):
        """测试 5: 数据趋势接口（自定义参数）"""
        test_name = "数据趋势接口（自定义参数）"
        self.total_tests += 1

        print(f"【测试 {self.total_tests}】{test_name}")
        print("-" * 60)

        if not self.admin_token:
            print(f"  ⚠️ 跳过: 管理员未登录")
            self.test_results.append((test_name, None, "管理员未登录"))
            print()
            return

        response = self.client.get('/api/admin/dashboard/trends/',
                                   {'period': 'week', 'days': 4},
                                   HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                result = data.get('data', {})
                print(f"  ✅ 通过: 接口调用成功")
                print(f"  📊 返回数据:")
                print(f"     - 时间范围: {result.get('period', 'N/A')}")
                print(f"     - 天数: {result.get('days', 0)}")

                if result.get('period') == 'week' and result.get('days') == 4:
                    self.passed_tests += 1
                    self.test_results.append((test_name, True, "接口调用成功，参数处理正确"))
                else:
                    print(f"  ⚠️ 警告: 参数处理可能不正确")
                    self.test_results.append((test_name, True, "接口调用成功但参数处理有疑问"))
            else:
                print(f"  ❌ 失败: 业务错误 - {data.get('message', 'Unknown error')}")
                self.test_results.append((test_name, False, f"业务错误: {data.get('message')}"))
        else:
            print(f"  ❌ 失败: HTTP 状态码 {response.status_code}")
            self.test_results.append((test_name, False, f"HTTP 状态码: {response.status_code}"))
        print()

    def test_6_dashboard_behaviors(self):
        """测试 6: 用户行为统计接口"""
        test_name = "用户行为统计接口"
        self.total_tests += 1

        print(f"【测试 {self.total_tests}】{test_name}")
        print("-" * 60)

        if not self.admin_token:
            print(f"  ⚠️ 跳过: 管理员未登录")
            self.test_results.append((test_name, None, "管理员未登录"))
            print()
            return

        response = self.client.get('/api/admin/dashboard/behaviors/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                result = data.get('data', {})
                print(f"  ✅ 通过: 接口调用成功")
                print(f"  📊 返回数据:")

                if 'active_user_distribution' in result:
                    au_dist = result['active_user_distribution']
                    print(f"     - 日活跃用户(DAU): {au_dist.get('dau', 0)}")
                    print(f"     - 周活跃用户(WAU): {au_dist.get('wau', 0)}")
                    print(f"     - 月活跃用户(MAU): {au_dist.get('mau', 0)}")

                if 'behavior_distribution' in result:
                    b_dist = result['behavior_distribution']
                    print(f"     - 今日登录: {b_dist.get('login', 0)}")
                    print(f"     - 今日收藏: {b_dist.get('favorite', 0)}")
                    print(f"     - 总浏览量: {b_dist.get('view', 0)}")

                # 验证必需字段
                if 'active_user_distribution' in result and 'behavior_distribution' in result:
                    self.passed_tests += 1
                    self.test_results.append((test_name, True, "接口调用成功，数据完整"))
                else:
                    print(f"  ⚠️ 警告: 数据结构不完整")
                    self.test_results.append((test_name, True, "接口调用成功但数据结构不完整"))
            else:
                print(f"  ❌ 失败: 业务错误 - {data.get('message', 'Unknown error')}")
                self.test_results.append((test_name, False, f"业务错误: {data.get('message')}"))
        else:
            print(f"  ❌ 失败: HTTP 状态码 {response.status_code}")
            self.test_results.append((test_name, False, f"HTTP 状态码: {response.status_code}"))
        print()

    def print_summary(self):
        """打印测试总结"""
        print("=" * 60)
        print("【测试总结】")
        print("=" * 60)

        skipped = sum(1 for _, passed, _ in self.test_results if passed is None)
        failed = self.total_tests - self.passed_tests - skipped

        print(f"  总测试数: {self.total_tests}")
        print(f"  ✅ 通过: {self.passed_tests}")
        print(f"  ❌ 失败: {failed}")
        print(f"  ⚠️ 跳过: {skipped}")
        print(f"  通过率: {(self.passed_tests / self.total_tests * 100):.1f}%")
        print()

        # 详细结果
        if failed > 0 or skipped > 0:
            print("【详细结果】")
            for test_name, passed, message in self.test_results:
                if passed is False:
                    print(f"  ❌ {test_name}: {message}")
                elif passed is None:
                    print(f"  ⚠️ {test_name}: {message}")
            print()

        # 最终结论
        print("=" * 60)
        if self.passed_tests == self.total_tests - skipped:
            print("🎉 所有测试通过！Dashboard 接口工作正常。")
        elif self.passed_tests > 0:
            print(f"⚠️ 部分测试通过（{self.passed_tests}/{self.total_tests - skipped}）。")
        else:
            print("❌ 测试失败，请检查接口实现。")
        print("=" * 60)

    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("     管理员 Dashboard 接口测试")
        print("=" * 60 + "\n")

        # 准备测试数据
        self.setup_test_data()

        # 登录
        if not self.login_as_admin():
            print("❌ 无法继续测试：管理员登录失败")
            return

        # 运行测试
        self.test_1_dashboard_overview_without_auth()
        self.test_2_dashboard_overview_with_normal_user()
        self.test_3_dashboard_overview_success()
        self.test_4_dashboard_trends_default_params()
        self.test_5_dashboard_trends_custom_params()
        self.test_6_dashboard_behaviors()

        # 打印总结
        self.print_summary()


if __name__ == '__main__':
    tester = DashboardAPITester()
    tester.run_all_tests()
