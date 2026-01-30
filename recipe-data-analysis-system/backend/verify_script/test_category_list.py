"""
分类列表接口测试脚本

测试内容：
1. 获取所有分类
2. 按类型筛选分类（菜系、场景、人群、口味）
3. 验证排序顺序
4. 测试无效的类型参数
"""
import requests

class CategoryListTester:
    """分类列表接口测试类"""

    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.passed = 0
        self.failed = 0
        self.results = []

    def print_header(self, title):
        """打印测试标题"""
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")

    def print_test(self, test_name, passed, message=""):
        """打印测试结果"""
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} - {test_name}")
        if message:
            print(f"    {message}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def test_get_all_categories(self):
        """测试获取所有分类"""
        self.print_header("测试 1: 获取所有分类")

        try:
            response = requests.get(f"{self.base_url}/api/categories/")
            result = response.json()

            # 检查响应格式
            assert response.status_code == 200, f"状态码应为 200，实际为 {response.status_code}"
            assert result['code'] == 200, f"响应 code 应为 200，实际为 {result['code']}"
            assert 'data' in result, "响应中应包含 data 字段"
            assert isinstance(result['data'], list), "data 应为列表类型"

            categories = result['data']
            print(f"\n总共获取 {len(categories)} 个分类")

            # 验证分类数据结构
            if categories:
                first = categories[0]
                assert 'id' in first, "分类应包含 id 字段"
                assert 'name' in first, "分类应包含 name 字段"
                assert 'type' in first, "分类应包含 type 字段"
                assert 'sort_order' in first, "分类应包含 sort_order 字段"
                print(f"\n示例分类: {first['name']} ({first['type']})")

            self.print_test("获取所有分类", True, f"共 {len(categories)} 个分类")
            self.results.append({"test": "获取所有分类", "passed": True})

        except AssertionError as e:
            self.print_test("获取所有分类", False, str(e))
            self.results.append({"test": "获取所有分类", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("获取所有分类", False, f"请求失败: {str(e)}")
            self.results.append({"test": "获取所有分类", "passed": False, "error": str(e)})

    def test_filter_by_cuisine_type(self):
        """测试按菜系类型筛选"""
        self.print_header("测试 2: 按菜系类型筛选")

        try:
            response = requests.get(f"{self.base_url}/api/categories/?type=cuisine")
            result = response.json()

            assert response.status_code == 200, f"状态码应为 200，实际为 {response.status_code}"
            assert result['code'] == 200, f"响应 code 应为 200，实际为 {result['code']}"

            categories = result['data']
            print(f"\n菜系分类数量: {len(categories)}")

            # 验证都是菜系类型
            for cat in categories:
                assert cat['type'] == 'cuisine', f"分类类型应为 cuisine，实际为 {cat['type']}"
                print(f"  - {cat['name']} (排序: {cat['sort_order']})")

            # 验证八大菜系
            cuisine_names = [cat['name'] for cat in categories]
            expected_cuisines = ['川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '湘菜', '徽菜', '闽菜']
            for expected in expected_cuisines:
                assert expected in cuisine_names, f"应包含菜系: {expected}"

            self.print_test("按菜系类型筛选", True, f"共 {len(categories)} 个菜系，包含八大菜系")
            self.results.append({"test": "按菜系类型筛选", "passed": True})

        except AssertionError as e:
            self.print_test("按菜系类型筛选", False, str(e))
            self.results.append({"test": "按菜系类型筛选", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("按菜系类型筛选", False, f"请求失败: {str(e)}")
            self.results.append({"test": "按菜系类型筛选", "passed": False, "error": str(e)})

    def test_filter_by_scene_type(self):
        """测试按场景类型筛选"""
        self.print_header("测试 3: 按场景类型筛选")

        try:
            response = requests.get(f"{self.base_url}/api/categories/?type=scene")
            result = response.json()

            assert response.status_code == 200, f"状态码应为 200，实际为 {response.status_code}"
            assert result['code'] == 200, f"响应 code 应为 200，实际为 {result['code']}"

            categories = result['data']
            print(f"\n场景分类数量: {len(categories)}")

            # 验证都是场景类型
            for cat in categories:
                assert cat['type'] == 'scene', f"分类类型应为 scene，实际为 {cat['type']}"
                print(f"  - {cat['name']} (排序: {cat['sort_order']})")

            # 验证常见场景
            scene_names = [cat['name'] for cat in categories]
            expected_scenes = ['早餐', '午餐', '晚餐', '下午茶', '夜宵']
            for expected in expected_scenes:
                assert expected in scene_names, f"应包含场景: {expected}"

            self.print_test("按场景类型筛选", True, f"共 {len(categories)} 个场景")
            self.results.append({"test": "按场景类型筛选", "passed": True})

        except AssertionError as e:
            self.print_test("按场景类型筛选", False, str(e))
            self.results.append({"test": "按场景类型筛选", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("按场景类型筛选", False, f"请求失败: {str(e)}")
            self.results.append({"test": "按场景类型筛选", "passed": False, "error": str(e)})

    def test_filter_by_crowd_type(self):
        """测试按人群类型筛选"""
        self.print_header("测试 4: 按人群类型筛选")

        try:
            response = requests.get(f"{self.base_url}/api/categories/?type=crowd")
            result = response.json()

            assert response.status_code == 200, f"状态码应为 200，实际为 {response.status_code}"
            assert result['code'] == 200, f"响应 code 应为 200，实际为 {result['code']}"

            categories = result['data']
            print(f"\n人群分类数量: {len(categories)}")

            for cat in categories:
                assert cat['type'] == 'crowd', f"分类类型应为 crowd，实际为 {cat['type']}"
                print(f"  - {cat['name']} (排序: {cat['sort_order']})")

            self.print_test("按人群类型筛选", True, f"共 {len(categories)} 个人群分类")
            self.results.append({"test": "按人群类型筛选", "passed": True})

        except AssertionError as e:
            self.print_test("按人群类型筛选", False, str(e))
            self.results.append({"test": "按人群类型筛选", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("按人群类型筛选", False, f"请求失败: {str(e)}")
            self.results.append({"test": "按人群类型筛选", "passed": False, "error": str(e)})

    def test_filter_by_taste_type(self):
        """测试按口味类型筛选"""
        self.print_header("测试 5: 按口味类型筛选")

        try:
            response = requests.get(f"{self.base_url}/api/categories/?type=taste")
            result = response.json()

            assert response.status_code == 200, f"状态码应为 200，实际为 {response.status_code}"
            assert result['code'] == 200, f"响应 code 应为 200，实际为 {result['code']}"

            categories = result['data']
            print(f"\n口味分类数量: {len(categories)}")

            for cat in categories:
                assert cat['type'] == 'taste', f"分类类型应为 taste，实际为 {cat['type']}"
                print(f"  - {cat['name']} (排序: {cat['sort_order']})")

            self.print_test("按口味类型筛选", True, f"共 {len(categories)} 个口味分类")
            self.results.append({"test": "按口味类型筛选", "passed": True})

        except AssertionError as e:
            self.print_test("按口味类型筛选", False, str(e))
            self.results.append({"test": "按口味类型筛选", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("按口味类型筛选", False, f"请求失败: {str(e)}")
            self.results.append({"test": "按口味类型筛选", "passed": False, "error": str(e)})

    def test_sort_order(self):
        """测试排序顺序"""
        self.print_header("测试 6: 验证排序顺序")

        try:
            response = requests.get(f"{self.base_url}/api/categories/?type=cuisine")
            result = response.json()

            categories = result['data']

            # 验证按 sort_order 排序
            sort_orders = [cat['sort_order'] for cat in categories]
            assert sort_orders == sorted(sort_orders), "分类应按 sort_order 升序排列"

            print(f"\n菜系排序: {' -> '.join(str(o) for o in sort_orders)}")
            print(f"菜系顺序: {' -> '.join(cat['name'] for cat in categories)}")

            self.print_test("验证排序顺序", True, "分类按 sort_order 正确排序")
            self.results.append({"test": "验证排序顺序", "passed": True})

        except AssertionError as e:
            self.print_test("验证排序顺序", False, str(e))
            self.results.append({"test": "验证排序顺序", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("验证排序顺序", False, f"请求失败: {str(e)}")
            self.results.append({"test": "验证排序顺序", "passed": False, "error": str(e)})

    def test_invalid_type_parameter(self):
        """测试无效的类型参数"""
        self.print_header("测试 7: 无效的类型参数")

        try:
            response = requests.get(f"{self.base_url}/api/categories/?type=invalid")
            result = response.json()

            assert response.status_code == 400, f"状态码应为 400，实际为 {response.status_code}"
            assert result['code'] == 400, f"响应 code 应为 400，实际为 {result['code']}"
            assert 'message' in result, "响应中应包含 message 字段"

            print(f"\n错误信息: {result['message']}")

            self.print_test("无效的类型参数", True, "正确返回 400 错误")
            self.results.append({"test": "无效的类型参数", "passed": True})

        except AssertionError as e:
            self.print_test("无效的类型参数", False, str(e))
            self.results.append({"test": "无效的类型参数", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("无效的类型参数", False, f"请求失败: {str(e)}")
            self.results.append({"test": "无效的类型参数", "passed": False, "error": str(e)})

    def test_category_by_type_path(self):
        """测试按类型路径获取分类"""
        self.print_header("测试 8: 按类型路径获取分类")

        try:
            # 测试菜系路径
            response = requests.get(f"{self.base_url}/api/categories/cuisine/")
            result = response.json()

            assert response.status_code == 200, f"状态码应为 200，实际为 {response.status_code}"
            assert result['code'] == 200, f"响应 code 应为 200，实际为 {result['code']}"

            categories = result['data']
            print(f"\n通过路径获取菜系: {len(categories)} 个")

            for cat in categories:
                assert cat['type'] == 'cuisine', f"分类类型应为 cuisine，实际为 {cat['type']}"

            self.print_test("按类型路径获取分类", True, f"路径 /categories/cuisine/ 正常工作")
            self.results.append({"test": "按类型路径获取分类", "passed": True})

        except AssertionError as e:
            self.print_test("按类型路径获取分类", False, str(e))
            self.results.append({"test": "按类型路径获取分类", "passed": False, "error": str(e)})
        except Exception as e:
            self.print_test("按类型路径获取分类", False, f"请求失败: {str(e)}")
            self.results.append({"test": "按类型路径获取分类", "passed": False, "error": str(e)})

    def print_summary(self):
        """打印测试总结"""
        self.print_header("测试总结")
        total = self.passed + self.failed
        print(f"\n总计: {total} 个测试")
        print(f"[PASS]: {self.passed} 个")
        print(f"[FAIL]: {self.failed} 个")

        if self.failed == 0:
            print(f"\n所有测试通过!")
        else:
            print(f"\n有 {self.failed} 个测试失败，请检查")
            for result in self.results:
                if not result['passed']:
                    print(f"  - {result['test']}: {result.get('error', '未知错误')}")

    def run_all_tests(self):
        """运行所有测试"""
        print(f"\n[TEST] 开始分类列表接口测试...")
        print(f"[URL] 测试地址: {self.base_url}/api/categories/")

        self.test_get_all_categories()
        self.test_filter_by_cuisine_type()
        self.test_filter_by_scene_type()
        self.test_filter_by_crowd_type()
        self.test_filter_by_taste_type()
        self.test_sort_order()
        self.test_invalid_type_parameter()
        self.test_category_by_type_path()

        self.print_summary()


if __name__ == '__main__':
    tester = CategoryListTester()
    tester.run_all_tests()
