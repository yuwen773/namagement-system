"""
分类管理功能完整测试脚本
Phase 14 Step 3 - 分类管理页面测试

测试范围：
1. 管理员权限验证（仅管理员可访问）
2. 分类列表接口（分页、筛选、搜索）
3. 创建分类（成功场景、参数验证）
4. 更新分类（成功场景、参数验证）
5. 删除分类（成功场景、使用保护）
6. 边界条件和异常处理
"""

import os
import sys
import json
import django

# Windows console fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
django.setup()

from django.test import Client
from accounts.models import User
from categories.models import Category
from recipes.models import Recipe
from utils.constants import UserRole, CategoryType


# ==================== Test Helpers ====================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_section(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}  {title}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")


def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")


def cleanup():
    """清理测试数据"""
    User.objects.filter(username__startswith='test_cat_').delete()
    Category.objects.filter(name__startswith='TEST_').delete()


def get_auth_headers(client, username, password):
    """获取认证头"""
    resp = client.post('/api/accounts/login/',
        data=json.dumps({'username': username, 'password': password}),
        content_type='application/json'
    )
    if resp.status_code != 200:
        return None
    token = resp.json()['data']['token']
    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}


# ==================== Test Cases ====================

def test_permission_checks():
    """测试1: 权限验证 - 仅管理员可访问"""
    print_section("测试1: 权限验证")

    client = Client()

    # 创建普通用户
    print_info("创建普通用户...")
    normal_user = User.objects.create_user(
        username='test_cat_normal',
        email='normal@test.com',
        password='Password123',
        role=UserRole.USER
    )
    normal_user.is_active = True
    normal_user.save()

    # 创建管理员用户
    print_info("创建管理员用户...")
    admin_user = User.objects.create_user(
        username='test_cat_admin',
        email='admin@test.com',
        password='Password123',
        role=UserRole.ADMIN
    )
    admin_user.is_active = True
    admin_user.save()

    # 测试未登录访问
    print_info("测试未登录访问分类管理接口...")
    resp = client.get('/api/admin/categories/')
    if resp.status_code == 401:
        print_success("未登录访问被正确拒绝 (401)")
    else:
        print_error(f"未登录访问应返回401，实际返回: {resp.status_code}")
        return False

    # 测试普通用户访问
    print_info("测试普通用户访问分类管理接口...")
    normal_headers = get_auth_headers(client, 'test_cat_normal', 'Password123')
    if normal_headers is None:
        print_error("普通用户登录失败")
        return False

    resp = client.get('/api/admin/categories/', **normal_headers)
    if resp.status_code == 403:
        print_success("普通用户访问被正确拒绝 (403)")
    else:
        print_error(f"普通用户访问应返回403，实际返回: {resp.status_code}")
        return False

    # 测试管理员访问
    print_info("测试管理员访问分类管理接口...")
    admin_headers = get_auth_headers(client, 'test_cat_admin', 'Password123')
    if admin_headers is None:
        print_error("管理员登录失败")
        return False

    resp = client.get('/api/admin/categories/', **admin_headers)
    if resp.status_code == 200:
        print_success("管理员访问成功 (200)")
    else:
        print_error(f"管理员访问应返回200，实际返回: {resp.status_code}")
        return False

    return True, admin_headers


def test_category_list_filters(admin_headers):
    """测试2: 分类列表 - 筛选和搜索功能"""
    print_section("测试2: 分类列表筛选和搜索")

    client = Client()

    # 创建测试分类数据
    print_info("创建测试分类数据...")
    test_categories = [
        {'name': 'TEST_川菜', 'type': CategoryType.CUISINE, 'sort_order': 1},
        {'name': 'TEST_粤菜', 'type': CategoryType.CUISINE, 'sort_order': 2},
        {'name': 'TEST_鲁菜', 'type': CategoryType.CUISINE, 'sort_order': 3},
        {'name': 'TEST_早餐', 'type': CategoryType.SCENE, 'sort_order': 1},
        {'name': 'TEST_午餐', 'type': CategoryType.SCENE, 'sort_order': 2},
        {'name': 'TEST_儿童', 'type': CategoryType.CROWD, 'sort_order': 1},
    ]

    created_ids = []
    for cat_data in test_categories:
        resp = client.post('/api/admin/categories/create/',
            data=json.dumps(cat_data),
            content_type='application/json',
            **admin_headers
        )
        if resp.status_code in [200, 201]:
            created_ids.append(resp.json()['data']['id'])

    print_success(f"创建了 {len(created_ids)} 个测试分类")

    # 测试获取所有分类
    print_info("测试获取所有分类...")
    resp = client.get('/api/admin/categories/', **admin_headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        total_count = data['count']
        print_success(f"获取所有分类成功，总数: {total_count}")
    else:
        print_error(f"获取分类列表失败: {resp.status_code}")
        return False

    # 测试按类型筛选
    print_info("测试按菜系类型筛选...")
    resp = client.get('/api/admin/categories/?type=cuisine', **admin_headers)
    if resp.status_code == 200:
        results = resp.json()['data']['results']
        cuisine_count = len([r for r in results if r['name'].startswith('TEST_川菜') or r['name'].startswith('TEST_粤菜') or r['name'].startswith('TEST_鲁菜')])
        if cuisine_count == 3:
            print_success("菜系类型筛选正确，找到3个测试菜系")
        else:
            print_error(f"菜系筛选结果不正确，期望3个，实际: {cuisine_count}")
    else:
        print_error(f"类型筛选失败: {resp.status_code}")

    # 测试搜索功能
    print_info("测试搜索功能（搜索'川菜'）...")
    resp = client.get('/api/admin/categories/?search=川菜', **admin_headers)
    if resp.status_code == 200:
        results = resp.json()['data']['results']
        found = any(r['name'] == 'TEST_川菜' for r in results)
        if found:
            print_success("搜索功能正常，找到'川菜'")
        else:
            print_error("搜索功能异常，未找到'川菜'")
    else:
        print_error(f"搜索请求失败: {resp.status_code}")

    # 测试分页
    print_info("测试分页功能（page_size=3）...")
    resp = client.get('/api/admin/categories/?page=1&page_size=3', **admin_headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        if len(data['results']) <= 3:
            print_success(f"分页功能正常，返回 {len(data['results'])} 条记录")
        else:
            print_error(f"分页功能异常，返回了 {len(data['results'])} 条记录（应为3条）")
    else:
        print_error(f"分页请求失败: {resp.status_code}")

    # 测试无效类型筛选
    print_info("测试无效类型筛选...")
    resp = client.get('/api/admin/categories/?type=invalid_type', **admin_headers)
    if resp.status_code == 400:
        print_success("无效类型筛选被正确拒绝 (400)")
    else:
        print_error(f"无效类型筛选应返回400，实际返回: {resp.status_code}")

    return True


def test_create_category(admin_headers):
    """测试3: 创建分类"""
    print_section("测试3: 创建分类")

    client = Client()

    # 测试成功创建
    print_info("测试成功创建分类...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'name': 'TEST_湘菜',
            'type': CategoryType.CUISINE,
            'sort_order': 10
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 201:
        cat_data = resp.json()['data']
        print_success(f"分类创建成功，ID: {cat_data['id']}")
        test_cat_id = cat_data['id']
    else:
        print_error(f"分类创建失败: {resp.status_code}, {resp.content}")
        return False

    # 测试缺少必填字段
    print_info("测试缺少name字段...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'type': CategoryType.CUISINE,
            'sort_order': 10
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 400:
        print_success("缺少name字段被正确拒绝 (400)")
    else:
        print_error(f"缺少必填字段应返回400，实际返回: {resp.status_code}")

    # 测试无效类型
    print_info("测试无效分类类型...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'name': 'TEST_无效',
            'type': 'invalid_type',
            'sort_order': 10
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 400:
        print_success("无效分类类型被正确拒绝 (400)")
    else:
        print_error(f"无效类型应返回400，实际返回: {resp.status_code}")

    # 测试默认排序值
    print_info("测试默认排序值...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'name': 'TEST_默认排序',
            'type': CategoryType.CUISINE
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 201:
        cat_data = resp.json()['data']
        if cat_data['sort_order'] == 0:
            print_success("默认排序值为0")
        else:
            print_error(f"默认排序值应为0，实际: {cat_data['sort_order']}")
    else:
        print_error(f"创建分类失败: {resp.status_code}")

    return True


def test_update_category(admin_headers):
    """测试4: 更新分类"""
    print_section("测试4: 更新分类")

    client = Client()

    # 先创建一个测试分类
    print_info("创建测试分类...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'name': 'TEST_待更新',
            'type': CategoryType.CUISINE,
            'sort_order': 5
        }),
        content_type='application/json',
        **admin_headers
    )
    cat_id = resp.json()['data']['id']
    print_success(f"测试分类创建成功，ID: {cat_id}")

    # 测试完整更新 (PUT)
    print_info("测试完整更新 (PUT)...")
    resp = client.put(f'/api/admin/categories/{cat_id}/update/',
        data=json.dumps({
            'name': 'TEST_已更新',
            'type': CategoryType.CUISINE,
            'sort_order': 15
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 200:
        cat_data = resp.json()['data']
        if cat_data['name'] == 'TEST_已更新' and cat_data['sort_order'] == 15:
            print_success("完整更新成功")
        else:
            print_error(f"更新后数据不正确: {cat_data}")
    else:
        print_error(f"更新失败: {resp.status_code}, {resp.content}")

    # 测试部分更新 (PATCH)
    print_info("测试部分更新 (PATCH)...")
    resp = client.patch(f'/api/admin/categories/{cat_id}/update/',
        data=json.dumps({
            'sort_order': 20
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 200:
        cat_data = resp.json()['data']
        if cat_data['name'] == 'TEST_已更新' and cat_data['sort_order'] == 20:
            print_success("部分更新成功，name保持不变")
        else:
            print_error(f"部分更新后数据不正确: {cat_data}")
    else:
        print_error(f"部分更新失败: {resp.status_code}")

    # 测试更新不存在的分类
    print_info("测试更新不存在的分类...")
    resp = client.put('/api/admin/categories/99999/update/',
        data=json.dumps({
            'name': 'TEST_不存在',
            'type': CategoryType.CUISINE
        }),
        content_type='application/json',
        **admin_headers
    )
    if resp.status_code == 404:
        print_success("更新不存在的分类返回404")
    else:
        print_error(f"应返回404，实际返回: {resp.status_code}")

    return True


def test_delete_category(admin_headers):
    """测试5: 删除分类"""
    print_section("测试5: 删除分类")

    client = Client()

    # 先创建一个测试分类
    print_info("创建测试分类...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'name': 'TEST_待删除',
            'type': CategoryType.CUISINE,
            'sort_order': 5
        }),
        content_type='application/json',
        **admin_headers
    )
    cat_id = resp.json()['data']['id']
    print_success(f"测试分类创建成功，ID: {cat_id}")

    # 测试删除未使用的分类
    print_info("测试删除未使用的分类...")
    resp = client.delete(f'/api/admin/categories/{cat_id}/delete/', **admin_headers)
    if resp.status_code == 200:
        print_success("删除未使用的分类成功")

        # 验证删除
        resp = client.get('/api/admin/categories/', **admin_headers)
        results = resp.json()['data']['results']
        found = any(r['id'] == cat_id for r in results)
        if not found:
            print_success("分类已被正确删除")
        else:
            print_error("分类仍然存在")
    else:
        print_error(f"删除失败: {resp.status_code}")

    # 测试删除正在使用的分类
    print_info("创建一个被菜谱使用的分类...")

    # 首先检查是否有现有的菜谱使用某个菜系
    from recipes.models import Recipe
    existing_recipe = Recipe.objects.first()

    if existing_recipe:
        # 获取菜谱的菜系
        cuisine_name = existing_recipe.cuisine_type

        # 创建对应的分类（如果不存在）
        category, created = Category.objects.get_or_create(
            name=cuisine_name,
            defaults={'type': CategoryType.CUISINE, 'sort_order': 1}
        )

        print_info(f"测试删除正在被使用的分类: {category.name}")
        resp = client.delete(f'/api/admin/categories/{category.id}/delete/', **admin_headers)
        if resp.status_code == 400:
            print_success("删除正在使用的分类被正确拒绝 (400)")
            print_info(f"错误信息: {resp.json()['message']}")
        else:
            print_error(f"应返回400，实际返回: {resp.status_code}")
    else:
        print_info("数据库中没有菜谱，跳过使用保护测试")

    # 测试删除不存在的分类
    print_info("测试删除不存在的分类...")
    resp = client.delete('/api/admin/categories/99999/delete/', **admin_headers)
    if resp.status_code == 404:
        print_success("删除不存在的分类返回404")
    else:
        print_error(f"应返回404，实际返回: {resp.status_code}")

    return True


def test_pagination_edge_cases(admin_headers):
    """测试6: 分页边界条件"""
    print_section("测试6: 分页边界条件")

    client = Client()

    # 测试超出范围的页码
    print_info("测试超出范围的页码...")
    resp = client.get('/api/admin/categories/?page=9999', **admin_headers)
    if resp.status_code == 200:
        results = resp.json()['data']['results']
        if len(results) == 0:
            print_success("超出范围页码返回空列表")
        else:
            print_info(f"返回了 {len(results)} 条记录")
    else:
        print_error(f"请求失败: {resp.status_code}")

    # 测试不同page_size
    print_info("测试不同page_size值...")
    for page_size in [10, 20, 50, 100]:
        resp = client.get(f'/api/admin/categories/?page_size={page_size}', **admin_headers)
        if resp.status_code == 200:
            data = resp.json()['data']
            print_success(f"page_size={page_size} 正常工作")
        else:
            print_error(f"page_size={page_size} 失败: {resp.status_code}")

    # 测试超过最大page_size限制
    print_info("测试超过最大page_size限制...")
    resp = client.get('/api/admin/categories/?page_size=999', **admin_headers)
    if resp.status_code == 200:
        data = resp.json()['data']
        print_info(f"page_size=999 返回 {len(data['results'])} 条记录（可能被限制）")
    else:
        print_error(f"请求失败: {resp.status_code}")

    return True


def test_category_type_display(admin_headers):
    """测试7: 分类类型显示"""
    print_section("测试7: 分类类型显示")

    client = Client()

    # 创建各类型分类
    type_mapping = {
        CategoryType.CUISINE: '菜系',
        CategoryType.SCENE: '场景',
        CategoryType.CROWD: '人群',
        CategoryType.TASTE: '口味',
        CategoryType.DIFFICULTY: '难度',
    }

    print_info("创建各类型测试分类...")
    for type_value, type_name in type_mapping.items():
        resp = client.post('/api/admin/categories/create/',
            data=json.dumps({
                'name': f'TEST_{type_name}分类',
                'type': type_value,
                'sort_order': 1
            }),
            content_type='application/json',
            **admin_headers
        )
        if resp.status_code in [200, 201]:
            cat_data = resp.json()['data']
            display_name = cat_data.get('type_display', '')
            print_success(f"类型 {type_value} 显示名称: {display_name}")
        else:
            print_error(f"创建 {type_name} 分类失败: {resp.status_code}")

    return True


# ==================== Main Test Runner ====================

def run_all_tests():
    """运行所有测试"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     分类管理功能完整测试 - Phase 14 Step 3               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")

    # 清理旧数据
    cleanup()

    # 测试1: 权限验证
    result = test_permission_checks()
    if result is False:
        print_error("权限测试失败，停止后续测试")
        cleanup()
        return
    admin_headers = result[1]

    # 测试2: 列表筛选
    test_category_list_filters(admin_headers)

    # 测试3: 创建分类
    test_create_category(admin_headers)

    # 测试4: 更新分类
    test_update_category(admin_headers)

    # 测试5: 删除分类
    test_delete_category(admin_headers)

    # 测试6: 分页边界
    test_pagination_edge_cases(admin_headers)

    # 测试7: 类型显示
    test_category_type_display(admin_headers)

    # 清理测试数据
    print_section("清理测试数据")
    cleanup()
    print_success("测试数据清理完成")

    # 测试总结
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                  所有测试执行完成                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")


if __name__ == '__main__':
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n{Colors.RED}测试执行出错: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        cleanup()
