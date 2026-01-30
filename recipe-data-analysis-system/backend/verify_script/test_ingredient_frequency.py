"""
食材使用频率分析接口测试脚本

测试 GET /api/analytics/ingredients/ 接口

测试项：
1. 数据获取 - 验证接口能正常返回数据
2. 结构验证 - 验证返回数据包含 id, name, count, category 字段
3. 数量验证 - 验证返回数据量不超过 limit 参数
4. 排序验证 - 验证按使用次数降序排列
5. 数据类型 - 验证各字段类型正确
6. 参数测试 - 验证 limit 参数功能
"""

import sys
import io
import requests
import json

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 配置
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/analytics/ingredients/"


def print_test_header(test_name):
    """打印测试标题"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print('='*60)


def print_test_result(passed, message=""):
    """打印测试结果"""
    status = "✅ 通过" if passed else "❌ 失败"
    print(f"{status} - {message}")


def test_1_data_fetch():
    """测试1：数据获取 - 验证接口能正常返回数据"""
    print_test_header("数据获取")

    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            result = response.json()
            print(f"状态码: {response.status_code}")
            print(f"响应消息: {result.get('message', '')}")
            print(f"数据条数: {len(result.get('data', []))}")

            # 检查是否有数据
            data = result.get('data', [])
            if len(data) > 0:
                print_test_result(True, f"成功获取 {len(data)} 条食材数据")
                return True, data
            else:
                print_test_result(False, "返回数据为空")
                return False, None
        else:
            print_test_result(False, f"状态码异常: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False, None

    except Exception as e:
        print_test_result(False, f"请求异常: {str(e)}")
        return False, None


def test_2_structure_validation(data):
    """测试2：结构验证 - 验证返回数据包含必需字段"""
    print_test_header("结构验证")

    if not data:
        print_test_result(False, "无数据可验证")
        return False

    required_fields = ['id', 'name', 'count', 'category']

    # 检查第一条数据的结构
    first_item = data[0]
    missing_fields = [f for f in required_fields if f not in first_item]

    if missing_fields:
        print_test_result(False, f"缺少字段: {missing_fields}")
        print(f"数据示例: {json.dumps(first_item, ensure_ascii=False, indent=2)}")
        return False

    print("数据结构示例:")
    print(json.dumps(first_item, ensure_ascii=False, indent=2))
    print_test_result(True, "数据结构完整，包含 id, name, count, category 字段")
    return True


def test_3_count_validation(data):
    """测试3：数量验证 - 验证默认返回20条数据"""
    print_test_header("数量验证（默认 limit=20）")

    if not data:
        print_test_result(False, "无数据可验证")
        return False

    count = len(data)
    print(f"返回数据条数: {count}")

    # 默认应该是20条，或者少于20条（如果数据库中食材不足）
    if count <= 20:
        print_test_result(True, f"返回 {count} 条数据，符合默认 limit=20 的限制")
        return True
    else:
        print_test_result(False, f"返回 {count} 条数据，超过默认 limit=20 的限制")
        return False


def test_4_sort_validation(data):
    """测试4：排序验证 - 验证按使用次数降序排列"""
    print_test_header("排序验证")

    if not data or len(data) < 2:
        print_test_result(False, "数据不足，无法验证排序")
        return False

    # 检查 count 是否降序排列
    counts = [item['count'] for item in data]
    is_descending = all(counts[i] >= counts[i+1] for i in range(len(counts)-1))

    print("前5条食材的使用次数:")
    for i, item in enumerate(data[:5]):
        print(f"  {i+1}. {item['name']}: {item['count']} 次使用")

    if is_descending:
        print_test_result(True, "数据按使用次数降序排列")
        return True
    else:
        print_test_result(False, "数据未按使用次数降序排列")
        return False


def test_5_data_type_validation(data):
    """测试5：数据类型 - 验证各字段类型正确"""
    print_test_header("数据类型验证")

    if not data:
        print_test_result(False, "无数据可验证")
        return False

    type_checks = []

    for item in data[:3]:  # 检查前3条
        type_checks.append({
            'name': item['name'],
            'id_is_int': isinstance(item.get('id'), int),
            'name_is_str': isinstance(item.get('name'), str),
            'count_is_int': isinstance(item.get('count'), int),
            'category_is_str': isinstance(item.get('category'), str)
        })

    all_valid = all(
        check['id_is_int'] and check['name_is_str'] and
        check['count_is_int'] and check['category_is_str']
        for check in type_checks
    )

    print("数据类型检查结果:")
    for check in type_checks:
        status = "✅" if all([
            check['id_is_int'], check['name_is_str'],
            check['count_is_int'], check['category_is_str']
        ]) else "❌"
        print(f"  {status} {check['name']}: id={type(check.get('id')).__name__}, "
              f"name={type(check.get('name')).__name__}, "
              f"count={type(check.get('count')).__name__}, "
              f"category={type(check.get('category')).__name__}")

    if all_valid:
        print_test_result(True, "所有字段类型正确")
        return True
    else:
        print_test_result(False, "部分字段类型错误")
        return False


def test_6_limit_parameter():
    """测试6：参数测试 - 验证 limit 参数功能"""
    print_test_header("Limit 参数测试")

    test_cases = [
        {'limit': 5, 'expected': '5条'},
        {'limit': 10, 'expected': '10条'},
        {'limit': 50, 'expected': '50条'},
    ]

    all_passed = True

    for case in test_cases:
        limit = case['limit']
        try:
            response = requests.get(API_URL, params={'limit': limit})

            if response.status_code == 200:
                result = response.json()
                data = result.get('data', [])
                actual_count = len(data)

                # 检查数量是否正确
                if actual_count <= limit:
                    print(f"  ✅ limit={limit}: 返回 {actual_count} 条（预期 ≤ {limit}）")
                else:
                    print(f"  ❌ limit={limit}: 返回 {actual_count} 条（预期 ≤ {limit}）")
                    all_passed = False
            else:
                print(f"  ❌ limit={limit}: 请求失败，状态码 {response.status_code}")
                all_passed = False

        except Exception as e:
            print(f"  ❌ limit={limit}: 请求异常 - {str(e)}")
            all_passed = False

    if all_passed:
        print_test_result(True, "limit 参数功能正常")
    else:
        print_test_result(False, "limit 参数功能异常")

    return all_passed


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("食材使用频率分析接口测试")
    print("="*60)

    results = []

    # 测试1：数据获取
    passed, data = test_1_data_fetch()
    results.append(('数据获取', passed))

    if not passed:
        print("\n❌ 数据获取失败，无法继续后续测试")
        return

    # 测试2：结构验证
    results.append(('结构验证', test_2_structure_validation(data)))

    # 测试3：数量验证
    results.append(('数量验证', test_3_count_validation(data)))

    # 测试4：排序验证
    results.append(('排序验证', test_4_sort_validation(data)))

    # 测试5：数据类型验证
    results.append(('数据类型验证', test_5_data_type_validation(data)))

    # 测试6：limit 参数测试
    results.append(('Limit参数测试', test_6_limit_parameter()))

    # 打印测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {test_name}")

    print(f"\n总计: {passed_count}/{total_count} 通过")

    if passed_count == total_count:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ {total_count - passed_count} 个测试失败")


if __name__ == "__main__":
    run_all_tests()
