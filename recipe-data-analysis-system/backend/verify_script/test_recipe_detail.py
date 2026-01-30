#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
菜谱详情接口测试脚本

测试内容：
1. 请求存在的菜谱 ID，确认返回完整信息
2. 请求不存在的菜谱 ID，确认返回 404
3. 多次请求同一菜谱，确认点击量增加
4. 检查行为日志，确认浏览行为被记录
"""
import os
import sys
import django
import json

# 设置控制台输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置 Django 环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from rest_framework.test import APIClient
from django.db.models import Max
from accounts.models import User
from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from behavior_logs.models import UserBehaviorLog


def print_test_header(test_name):
    """打印测试标题"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")


def print_result(success, message):
    """打印测试结果"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")


def test_recipe_detail_with_valid_id():
    """测试1: 请求存在的菜谱 ID，确认返回完整信息"""
    print_test_header("请求存在的菜谱 ID")

    # 获取第一个菜谱
    recipe = Recipe.objects.first()
    if not recipe:
        print_result(False, "数据库中没有菜谱数据，请先导入数据")
        return False

    # 记录初始点击量
    initial_view_count = recipe.view_count

    # 使用 APIClient 发送请求
    client = APIClient()
    response = client.get(f'/api/recipes/{recipe.id}/')

    # 解析响应
    response_data = response.json()

    # 验证响应
    success = True
    messages = []

    # 检查响应状态
    if response.status_code != 200:
        success = False
        messages.append(f"响应状态码错误: 期望 200, 实际 {response.status_code}")
    else:
        messages.append(f"响应状态码: {response.status_code}")

    # 检查响应格式
    if 'code' not in response_data or 'message' not in response_data or 'data' not in response_data:
        success = False
        messages.append("响应格式错误: 缺少 code/message/data 字段")
    else:
        messages.append(f"响应格式正确: code={response_data['code']}, message={response_data['message']}")

    # 检查返回的完整信息
    data = response_data.get('data', {})
    required_fields = ['id', 'name', 'cuisine_type', 'difficulty', 'cooking_time',
                       'image_url', 'steps', 'flavor_tags', 'view_count', 'favorite_count',
                       'ingredients', 'flavor_list']

    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        success = False
        messages.append(f"缺少字段: {', '.join(missing_fields)}")
    else:
        messages.append(f"返回字段完整: {len(required_fields)} 个字段")

    # 检查食材列表
    ingredients = data.get('ingredients', [])
    messages.append(f"食材列表: {len(ingredients)} 个食材")
    if ingredients:
        messages.append(f"  示例食材: {ingredients[0].get('ingredient_name', 'N/A')}")

    # 检查口味标签列表
    flavor_list = data.get('flavor_list', [])
    messages.append(f"口味标签: {flavor_list}")

    # 检查基本信息
    messages.append(f"菜谱名称: {data.get('name', 'N/A')}")
    messages.append(f"菜系: {data.get('cuisine_type', 'N/A')}")
    messages.append(f"难度: {data.get('difficulty', 'N/A')}")
    messages.append(f"烹饪时长: {data.get('cooking_time', 'N/A')} 分钟")

    # 检查点击量是否增加
    recipe.refresh_from_db()
    if recipe.view_count <= initial_view_count:
        success = False
        messages.append(f"点击量未增加: 初始 {initial_view_count}, 当前 {recipe.view_count}")
    else:
        messages.append(f"点击量增加: 初始 {initial_view_count} -> 当前 {recipe.view_count}")

    # 打印结果
    for msg in messages:
        print(f"  - {msg}")

    print_result(success, "请求存在的菜谱 ID 返回完整信息")
    return success


def test_recipe_detail_with_invalid_id():
    """测试2: 请求不存在的菜谱 ID，确认返回 404"""
    print_test_header("请求不存在的菜谱 ID")

    # 获取最大的菜谱 ID
    max_id = Recipe.objects.aggregate(max_id=Max('id'))['max_id'] or 0
    invalid_id = max_id + 99999  # 使用一个肯定不存在的 ID

    # 使用 APIClient 发送请求
    client = APIClient()
    response = client.get(f'/api/recipes/{invalid_id}/')

    # 解析响应
    response_data = response.json()

    # 验证响应
    success = True
    messages = []

    if response.status_code != 404:
        success = False
        messages.append(f"响应状态码错误: 期望 404, 实际 {response.status_code}")
    else:
        messages.append(f"响应状态码: {response.status_code}")

    # DRF 默认异常处理器返回 {detail: "错误消息"} 格式
    # 统一格式处理器返回 {code, message, data} 格式
    # 两种格式都接受，只要状态码是 404 且包含错误消息
    error_message = response_data.get('message') or response_data.get('detail', '')

    if '菜谱不存在' not in error_message:
        success = False
        messages.append(f"错误消息不正确: {error_message}")
    else:
        messages.append(f"错误消息: {error_message}")

    # 检查是否有 code 字段（统一格式）
    if 'code' in response_data:
        if response_data['code'] != 404:
            success = False
            messages.append(f"业务状态码错误: 期望 404, 实际 {response_data.get('code')}")
        else:
            messages.append(f"业务状态码: {response_data.get('code')}")

    for msg in messages:
        print(f"  - {msg}")

    print_result(success, "请求不存在的菜谱 ID 返回 404")
    return success


def test_view_count_increases():
    """测试3: 多次请求同一菜谱，确认点击量增加"""
    print_test_header("多次请求同一菜谱，点击量增加")

    # 获取第一个菜谱
    recipe = Recipe.objects.first()
    if not recipe:
        print_result(False, "数据库中没有菜谱数据")
        return False

    # 记录初始点击量
    initial_view_count = recipe.view_count

    # 使用 APIClient 发送多次请求
    client = APIClient()
    request_count = 3
    for i in range(request_count):
        response = client.get(f'/api/recipes/{recipe.id}/')
        print(f"  - 第 {i+1} 次请求: 响应状态 {response.status_code}")

    # 刷新菜谱数据
    recipe.refresh_from_db()
    final_view_count = recipe.view_count

    # 验证点击量增加
    expected_increase = request_count
    actual_increase = final_view_count - initial_view_count

    success = (actual_increase == expected_increase)
    messages = [
        f"初始点击量: {initial_view_count}",
        f"请求次数: {request_count}",
        f"最终点击量: {final_view_count}",
        f"期望增加: {expected_increase}",
        f"实际增加: {actual_increase}"
    ]

    for msg in messages:
        print(f"  - {msg}")

    print_result(success, "多次请求点击量正确增加")
    return success


def test_behavior_log_created():
    """测试4: 检查行为日志，确认浏览行为被记录"""
    print_test_header("检查行为日志记录")

    # 获取第一个菜谱
    recipe = Recipe.objects.first()
    if not recipe:
        print_result(False, "数据库中没有菜谱数据")
        return False

    # 清空该菜谱的最近行为日志（仅用于测试）
    UserBehaviorLog.objects.filter(
        behavior_type='view',
        target=f'recipe:{recipe.id}'
    ).delete()

    # 使用 APIClient 发送请求
    client = APIClient()
    response = client.get(f'/api/recipes/{recipe.id}/', HTTP_USER_AGENT='Test User Agent')

    # 检查行为日志
    behavior_logs = UserBehaviorLog.objects.filter(
        behavior_type='view',
        target=f'recipe:{recipe.id}'
    ).order_by('-timestamp')

    success = True
    messages = []

    if behavior_logs.count() == 0:
        success = False
        messages.append("❌ 没有创建行为日志记录")
    else:
        messages.append(f"✓ 创建了 {behavior_logs.count()} 条行为日志")

        # 检查最新的一条日志
        log = behavior_logs.first()
        messages.append(f"✓ 行为类型: {log.behavior_type}")
        messages.append(f"✓ 行为目标: {log.target}")
        messages.append(f"✓ IP 地址: {log.ip_address}")
        ua = log.user_agent[:50] if log.user_agent else 'N/A'
        messages.append(f"✓ User-Agent: {ua}...")

        # 检查用户（未登录用户应该为 None）
        if log.user is None:
            messages.append(f"✓ 用户: 未登录（正确）")
        else:
            messages.append(f"✓ 用户: {log.user.username}")

        # 检查 extra_data
        if log.extra_data:
            messages.append(f"✓ 额外数据:")
            for key, value in log.extra_data.items():
                messages.append(f"    - {key}: {value}")
        else:
            messages.append("✓ 额外数据为空")

    for msg in messages:
        print(f"  - {msg}")

    print_result(success, "浏览行为被正确记录到行为日志表")
    return success


def test_behavior_log_with_authenticated_user():
    """测试5: 测试登录用户的行为日志记录"""
    print_test_header("登录用户的行为日志记录")

    # 获取第一个菜谱
    recipe = Recipe.objects.first()
    if not recipe:
        print_result(False, "数据库中没有菜谱数据")
        return False

    # 获取或创建测试用户
    user, created = User.objects.get_or_create(
        username='test_detail_user',
        defaults={
            'email': 'test_detail@example.com',
            'role': 'user'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()

    # 清空该用户对该菜谱的最近行为日志
    UserBehaviorLog.objects.filter(
        user=user,
        behavior_type='view',
        target=f'recipe:{recipe.id}'
    ).delete()

    # 使用 APIClient 发送请求（需要先登录获取 token）
    client = APIClient()

    # 先登录获取 token
    login_response = client.post('/api/accounts/login/', {
        'username': 'test_detail_user',
        'password': 'testpass123'
    })

    if login_response.status_code != 200:
        print_result(False, "登录失败，无法测试认证用户行为日志")
        return False

    token = login_response.json().get('data', {}).get('token') or login_response.json().get('data', {}).get('access')
    if not token:
        print_result(False, "登录成功但未获取到 token")
        print(f"  Response data: {login_response.json().get('data', {})}")
        return False

    # 使用 token 认证访问菜谱详情
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(f'/api/recipes/{recipe.id}/', HTTP_USER_AGENT='Test User Agent (Authenticated)')

    # 检查行为日志
    behavior_logs = UserBehaviorLog.objects.filter(
        user=user,
        behavior_type='view',
        target=f'recipe:{recipe.id}'
    )

    success = True
    messages = []

    if behavior_logs.count() == 0:
        success = False
        messages.append("❌ 没有为登录用户创建行为日志记录")
    else:
        log = behavior_logs.first()
        messages.append(f"✓ 为用户 {user.username} 创建了行为日志")
        messages.append(f"✓ 用户ID: {log.user_id}")
        messages.append(f"✓ 行为类型: {log.behavior_type}")
        messages.append(f"✓ 用户字段不为空: {log.user is not None}")

    for msg in messages:
        print(f"  - {msg}")

    print_result(success, "登录用户的行为日志记录正确")
    return success


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("菜谱详情接口测试 - 阶段五第3步")
    print("="*60)

    # 检查数据库中是否有菜谱数据
    recipe_count = Recipe.objects.count()
    print(f"\n当前数据库中有 {recipe_count} 条菜谱记录")

    if recipe_count == 0:
        print("\n❌ 数据库中没有菜谱数据，请先运行数据导入脚本")
        return

    # 运行所有测试
    test_results = []
    test_results.append(("请求存在的菜谱 ID", test_recipe_detail_with_valid_id()))
    test_results.append(("请求不存在的菜谱 ID", test_recipe_detail_with_invalid_id()))
    test_results.append(("点击量增加", test_view_count_increases()))
    test_results.append(("行为日志记录", test_behavior_log_created()))
    test_results.append(("登录用户行为日志", test_behavior_log_with_authenticated_user()))

    # 打印测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n通过率: {passed}/{total} ({passed*100//total}%)")

    if passed == total:
        print("\n🎉 所有测试通过!")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查")


if __name__ == '__main__':
    main()
