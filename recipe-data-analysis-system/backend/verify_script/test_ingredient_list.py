"""
食材列表接口测试脚本

测试内容：
1. 获取所有食材（无筛选条件）
2. 按分类筛选食材
3. 按关键词搜索食材
4. 分页功能测试
5. 无效分类参数
6. 空搜索结果
"""
import requests
import json
import sys
import os
import io

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# API 基础 URL
BASE_URL = 'http://localhost:8000'
API_URL = f'{BASE_URL}/api/ingredients/'


def print_test_header(test_name):
    """打印测试标题"""
    print(f'\n{"=" * 60}')
    print(f'测试: {test_name}')
    print('=' * 60)


def print_result(response, test_name='测试'):
    """打印测试结果"""
    print(f'\n{test_name}结果:')
    print(f'状态码: {response.status_code}')
    try:
        data = response.json()
        print(f'响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}')
    except:
        print(f'响应内容: {response.text}')


def test_get_all_ingredients():
    """测试1: 获取所有食材（无筛选条件）"""
    print_test_header('获取所有食材（无筛选条件）')

    params = {
        'page': 1,
        'page_size': 20
    }

    response = requests.get(API_URL, params=params)
    print_result(response, '获取所有食材')

    # 验证响应
    assert response.status_code == 200, f'期望状态码200，实际{response.status_code}'
    data = response.json()
    assert data['code'] == 200, f'期望code=200'
    assert 'data' in data, '响应应包含data字段'
    assert 'results' in data['data'], 'data应包含results字段'

    print(f'\n✅ 测试通过！共 {len(data["data"]["results"])} 条食材数据')
    return data['data'].get('count', 0)


def test_filter_by_category():
    """测试2: 按分类筛选食材"""
    print_test_header('按分类筛选食材')

    # 测试肉类分类
    categories = [
        ('meat', '肉类'),
        ('vegetable', '蔬菜'),
        ('seafood', '海鲜'),
        ('seasoning', '调料'),
    ]

    for category_value, category_name in categories:
        print(f'\n--- 测试分类: {category_name} ({category_value}) ---')

        params = {
            'category': category_value,
            'page': 1,
            'page_size': 10
        }

        response = requests.get(API_URL, params=params)
        print(f'请求参数: category={category_value}')

        # 验证响应
        assert response.status_code == 200, f'期望状态码200，实际{response.status_code}'
        data = response.json()
        assert data['code'] == 200, f'期望code=200'

        results = data['data']['results']
        print(f'✅ 找到 {len(results)} 条{category_name}食材')

        # 验证返回的结果都是该分类
        if results:
            for item in results:
                assert item['category'] == category_value, \
                    f'期望分类为{category_value}，实际为{item["category"]}'

    print(f'\n✅ 分类筛选测试通过！')


def test_search_ingredients():
    """测试3: 按关键词搜索食材"""
    print_test_header('按关键词搜索食材')

    # 常见搜索关键词
    search_keywords = ['鸡', '肉', '蛋', '油', '盐', '番茄']

    for keyword in search_keywords:
        print(f'\n--- 搜索关键词: {keyword} ---')

        params = {
            'search': keyword,
            'page': 1,
            'page_size': 10
        }

        response = requests.get(API_URL, params=params)
        print(f'请求参数: search={keyword}')

        # 验证响应
        assert response.status_code == 200, f'期望状态码200，实际{response.status_code}'
        data = response.json()
        assert data['code'] == 200, f'期望code=200'

        results = data['data']['results']
        print(f'✅ 找到 {len(results)} 条包含"{keyword}"的食材')

        # 验证搜索结果包含关键词
        if results:
            for item in results:
                assert keyword in item['name'], \
                    f'食材名称"{item["name"]}"应包含关键词"{keyword}"'

    print(f'\n✅ 搜索功能测试通过！')


def test_pagination():
    """测试4: 分页功能测试"""
    print_test_header('分页功能测试')

    # 测试第一页
    print('\n--- 第一页 (page=1, page_size=5) ---')
    params = {'page': 1, 'page_size': 5}
    response = requests.get(API_URL, params=params)

    assert response.status_code == 200
    data = response.json()
    page1_results = data['data']['results']

    print(f'第一页返回 {len(page1_results)} 条数据')
    assert len(page1_results) <= 5, '第一页不应超过5条'

    # 测试第二页
    print('\n--- 第二页 (page=2, page_size=5) ---')
    params = {'page': 2, 'page_size': 5}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        page2_results = data['data']['results']

        print(f'第二页返回 {len(page2_results)} 条数据')

        # 验证两页数据不同
        if page1_results and page2_results:
            assert page1_results[0]['id'] != page2_results[0]['id'], '两页数据应不同'
            print('✅ 两页数据不重复')

    print(f'\n✅ 分页功能测试通过！')


def test_invalid_category():
    """测试5: 无效分类参数"""
    print_test_header('无效分类参数')

    params = {
        'category': 'invalid_category'
    }

    response = requests.get(API_URL, params=params)
    print_result(response, '无效分类参数')

    # 验证返回错误
    assert response.status_code == 400, f'期望状态码400，实际{response.status_code}'
    data = response.json()
    assert data['code'] == 400, f'期望code=400'
    assert '无效的分类' in data['message'], '错误消息应包含"无效的分类"'

    print(f'\n✅ 无效参数测试通过！')


def test_empty_search():
    """测试6: 空搜索结果"""
    print_test_header('空搜索结果')

    params = {
        'search': '不可能存在的食材名称xyz123'
    }

    response = requests.get(API_URL, params=params)
    print_result(response, '空搜索结果')

    # 验证返回空结果
    assert response.status_code == 200, f'期望状态码200，实际{response.status_code}'
    data = response.json()
    assert data['code'] == 200, f'期望code=200'
    assert data['data']['count'] == 0, '搜索结果应为0'
    assert len(data['data']['results']) == 0, 'results应为空列表'

    print(f'\n✅ 空搜索结果测试通过！')


def test_combined_filters():
    """测试7: 组合筛选（分类+搜索）"""
    print_test_header('组合筛选（分类+搜索）')

    params = {
        'category': 'meat',
        'search': '鸡'
    }

    response = requests.get(API_URL, params=params)
    print_result(response, '组合筛选')

    # 验证响应
    assert response.status_code == 200, f'期望状态码200，实际{response.status_code}'
    data = response.json()
    assert data['code'] == 200, f'期望code=200'

    results = data['data']['results']
    print(f'\n✅ 找到 {len(results)} 条肉类且包含"鸡"的食材')

    # 验证结果同时满足两个条件
    if results:
        for item in results:
            assert item['category'] == 'meat', f'应属于肉类分类'
            assert '鸡' in item['name'], f'名称应包含"鸡"'

    print(f'\n✅ 组合筛选测试通过！')


def main():
    """主测试函数"""
    print('=' * 60)
    print('食材列表接口测试')
    print('=' * 60)

    # 检查服务是否运行
    try:
        response = requests.get(BASE_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        print('\n❌ 错误: 无法连接到服务器')
        print('请确保 Django 服务已启动 (python manage.py runserver)')
        return
    except requests.exceptions.Timeout:
        print('\n❌ 错误: 连接服务器超时')
        return

    tests = [
        ('获取所有食材', test_get_all_ingredients),
        ('按分类筛选', test_filter_by_category),
        ('搜索食材', test_search_ingredients),
        ('分页功能', test_pagination),
        ('无效分类参数', test_invalid_category),
        ('空搜索结果', test_empty_search),
        ('组合筛选', test_combined_filters),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f'\n❌ {test_name} 测试失败: {e}')
            failed += 1
        except Exception as e:
            print(f'\n❌ {test_name} 测试出错: {e}')
            failed += 1

    # 打印测试总结
    print(f'\n{"=" * 60}')
    print(f'测试总结: {passed} 通过, {failed} 失败')
    print('=' * 60)

    if failed == 0:
        print('\n🎉 所有测试通过！')
    else:
        print(f'\n⚠️  有 {failed} 个测试失败')


if __name__ == '__main__':
    main()
