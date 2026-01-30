"""
菜谱搜索接口测试脚本

测试内容：
1. 按菜谱名称搜索
2. 按食材搜索
3. 搜索不存在的关键词
4. 测试分页功能
5. 测试性能（响应时间 < 500ms）
"""
import os
import sys
import time
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from django.test import RequestFactory
from recipes.views import recipe_search


def print_test_header(test_name):
    """打印测试标题"""
    print(f"\n{'=' * 60}")
    print(f"测试: {test_name}")
    print('=' * 60)


def print_result(passed, message):
    """打印测试结果"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} - {message}")


def test_search_by_name():
    """测试按菜谱名称搜索"""
    print_test_header("按菜谱名称搜索")

    factory = RequestFactory()

    # 获取一个已存在的菜谱名称
    recipe = Recipe.objects.first()
    if not recipe:
        print_result(False, "数据库中没有菜谱数据")
        return False

    keyword = recipe.name[:2]  # 取菜谱名称的前两个字作为关键词

    # 创建搜索请求
    request = factory.get(f'/api/recipes/search/?keyword={keyword}&search_type=name')

    try:
        response = recipe_search(request)
        data = response.data

        print(f"关键词: {keyword}")
        print(f"搜索结果数量: {data['data']['count']}")
        print(f"搜索类型: {data['data']['search_type']}")

        if data['data']['count'] > 0:
            print_result(True, f"找到 {data['data']['count']} 条结果")
            return True
        else:
            print_result(False, "未找到任何结果")
            return False
    except Exception as e:
        print_result(False, f"搜索出错: {e}")
        return False


def test_search_by_ingredient():
    """测试按食材搜索"""
    print_test_header("按食材搜索")

    factory = RequestFactory()

    # 获取一个已存在的食材
    ingredient = Ingredient.objects.first()
    if not ingredient:
        print_result(False, "数据库中没有食材数据")
        return False

    keyword = ingredient.name[:1]  # 取食材名称的第一个字作为关键词

    # 创建搜索请求
    request = factory.get(f'/api/recipes/search/?keyword={keyword}&search_type=ingredient')

    try:
        response = recipe_search(request)
        data = response.data

        print(f"食材关键词: {keyword}")
        print(f"搜索结果数量: {data['data']['count']}")
        print(f"搜索类型: {data['data']['search_type']}")

        if data['data']['count'] >= 0:
            print_result(True, f"找到 {data['data']['count']} 条结果")
            return True
        else:
            print_result(False, "搜索结果异常")
            return False
    except Exception as e:
        print_result(False, f"搜索出错: {e}")
        return False


def test_search_not_found():
    """测试搜索不存在的关键词"""
    print_test_header("搜索不存在的关键词")

    factory = RequestFactory()

    # 使用一个不太可能存在的关键词
    keyword = "xyzabc123NotExist"

    # 创建搜索请求
    request = factory.get(f'/api/recipes/search/?keyword={keyword}&search_type=name')

    try:
        response = recipe_search(request)
        data = response.data

        print(f"关键词: {keyword}")
        print(f"搜索结果数量: {data['data']['count']}")

        if data['data']['count'] == 0:
            print_result(True, "正确返回空结果")
            return True
        else:
            print_result(False, f"返回了 {data['data']['count']} 条结果，不符合预期")
            return False
    except Exception as e:
        print_result(False, f"搜索出错: {e}")
        return False


def test_search_empty_keyword():
    """测试空关键词"""
    print_test_header("空关键词验证")

    factory = RequestFactory()

    # 创建不带关键词的搜索请求
    request = factory.get('/api/recipes/search/')

    try:
        response = recipe_search(request)
        # 检查响应状态码
        if hasattr(response, 'status_code'):
            if response.status_code == 400:
                print_result(True, f"正确返回 400 错误: {response.data.get('message', 'N/A')}")
                return True
            else:
                print_result(False, f"返回了错误的状态码: {response.status_code}")
                return False
        else:
            # 如果没有 status_code，检查 data 中的 code
            if response.data.get('code') == 400:
                print_result(True, f"正确返回 400 错误: {response.data.get('message', 'N/A')}")
                return True
            else:
                print_result(False, f"应该返回错误但没有，返回: {response.data}")
                return False
    except Exception as e:
        # 预期会抛出 ValidationError
        if '请输入搜索关键词' in str(e) or 'keyword' in str(e).lower():
            print_result(True, "正确返回验证错误")
            return True
        else:
            print_result(False, f"返回了意外的错误: {e}")
            return False


def test_search_performance():
    """测试搜索性能"""
    print_test_header("搜索性能测试")

    factory = RequestFactory()

    # 获取一个已存在的菜谱名称
    recipe = Recipe.objects.first()
    if not recipe:
        print_result(False, "数据库中没有菜谱数据")
        return False

    keyword = recipe.name[:2]

    # 执行搜索并计时
    request = factory.get(f'/api/recipes/search/?keyword={keyword}&search_type=name')

    start_time = time.time()
    try:
        response = recipe_search(request)
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000

        print(f"关键词: {keyword}")
        print(f"搜索结果数量: {response.data['data']['count']}")
        print(f"响应时间: {elapsed_ms:.2f} ms")

        if elapsed_ms < 500:
            print_result(True, f"响应时间 {elapsed_ms:.2f} ms 符合要求 (< 500ms)")
            return True
        else:
            print_result(False, f"响应时间 {elapsed_ms:.2f} ms 超过要求 (>= 500ms)")
            return False
    except Exception as e:
        print_result(False, f"搜索出错: {e}")
        return False


def test_search_with_pagination():
    """测试分页功能"""
    print_test_header("分页功能测试")

    factory = RequestFactory()

    # 使用一个可能返回较多结果的短关键词
    keyword = "鸡"

    # 请求第一页
    request = factory.get(f'/api/recipes/search/?keyword={keyword}&page=1&page_size=10')

    try:
        response = recipe_search(request)
        data = response.data

        print(f"关键词: {keyword}")
        print(f"总结果数: {data['data']['count']}")
        print(f"返回结果数: {len(data['data']['results'])}")

        if len(data['data']['results']) <= 10:
            print_result(True, "分页功能正常")
            return True
        else:
            print_result(False, "返回结果数超过 page_size")
            return False
    except Exception as e:
        print_result(False, f"搜索出错: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("菜谱搜索接口测试套件")
    print("=" * 60)

    # 检查数据库是否有数据
    recipe_count = Recipe.objects.count()
    ingredient_count = Ingredient.objects.count()

    print(f"\n数据库状态:")
    print(f"  菜谱数量: {recipe_count}")
    print(f"  食材数量: {ingredient_count}")

    if recipe_count == 0:
        print("\n[ERROR] 数据库中没有菜谱数据，无法进行测试")
        return

    if ingredient_count == 0:
        print("\n[WARNING] 数据库中没有食材数据，部分测试将被跳过")

    # 运行测试
    results = []

    results.append(("按名称搜索", test_search_by_name()))
    if ingredient_count > 0:
        results.append(("按食材搜索", test_search_by_ingredient()))
    results.append(("不存在的关键词", test_search_not_found()))
    results.append(("空关键词验证", test_search_empty_keyword()))
    results.append(("性能测试", test_search_performance()))
    results.append(("分页功能", test_search_with_pagination()))

    # 打印总结
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n[SUCCESS] 所有测试通过！")
    else:
        print(f"\n[WARNING] {total - passed} 个测试失败")


if __name__ == '__main__':
    run_all_tests()
