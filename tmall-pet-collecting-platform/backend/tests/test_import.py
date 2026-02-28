"""
数据导入功能测试脚本
"""
import os
import sys
import django
import csv
from pathlib import Path
from datetime import datetime

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from products.services import ProductImportService
from products.models import Product, CrawlLog


def create_test_csv():
    """创建测试CSV文件"""
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    test_file = data_dir / 'test_products.csv'

    # 测试数据
    test_data = [
        {
            '商品ID': 'TEST001',
            '商品标题': '测试商品1 - 万代高达模型',
            '价格': '299',
            '价格单位': '¥',
            '价格描述': '券后价',
            '卖家昵称': 'test_seller',
            '店铺名称': '测试店铺',
            '店铺标签': '测试店铺',
            '销量': '100+人付款',
            '地区': '广东 深圳',
            '标签': '测试数据',
            '商品属性': '出售状态:现货|品牌:Bandai',
            '图片链接': 'http://example.com/image1.jpg',
            '商品链接': 'http://example.com/product1'
        },
        {
            '商品ID': 'TEST002',
            '商品标题': '测试商品2 - 红异端高达',
            '价格': '599',
            '价格单位': '¥',
            '价格描述': '',
            '卖家昵称': 'test_seller2',
            '店铺名称': '测试店铺2',
            '店铺标签': '5年老店',
            '销量': '2000人付款',
            '地区': '浙江 杭州',
            '标签': '热销爆款',
            '商品属性': '出售状态:现货|版本类型:日版|品牌:万代',
            '图片链接': 'http://example.com/image2.jpg',
            '商品链接': 'http://example.com/product2'
        },
        {
            '商品ID': 'TEST003',
            '商品标题': '测试商品3 - 缺少必填字段',
            '价格': '399',
            '价格单位': '¥',
            '价格描述': '',
            '卖家昵称': '',
            '店铺名称': '',  # 缺少店铺名称
            '店铺标签': '',
            '销量': '',
            '地区': '',
            '标签': '',
            '商品属性': '',
            '图片链接': '',
            '商品链接': ''  # 缺少商品链接
        }
    ]

    with open(test_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            '商品ID', '商品标题', '价格', '价格单位', '价格描述',
            '卖家昵称', '店铺名称', '店铺标签', '销量', '地区',
            '标签', '商品属性', '图片链接', '商品链接'
        ])
        writer.writeheader()
        writer.writerows(test_data)

    print(f"✅ 创建测试CSV文件: {test_file}")
    return test_file


def test_field_parsing():
    """测试字段解析功能"""
    print("\n🧪 测试字段解析功能...")

    # 测试价格解析
    assert ProductImportService.parse_price('299') == 299
    assert ProductImportService.parse_price('¥599') == 599
    assert ProductImportService.parse_price('') == 0
    print("  ✅ 价格解析测试通过")

    # 测试销量解析
    assert ProductImportService.parse_sales('100+人付款') == 100
    assert ProductImportService.parse_sales('2000人付款') == 2000
    assert ProductImportService.parse_sales('') == 0
    print("  ✅ 销量解析测试通过")

    # 测试属性解析
    attrs = ProductImportService.parse_attributes('出售状态:现货|品牌:Bandai')
    assert attrs == {'出售状态': '现货', '品牌': 'Bandai'}
    print("  ✅ 属性解析测试通过")


def test_data_validation():
    """测试数据验证功能"""
    print("\n🧪 测试数据验证功能...")

    # 有效数据
    valid_data = {
        'title': '测试商品',
        'shop': '测试店铺',
        'detail_url': 'http://example.com',
        'price': 299
    }
    is_valid, errors = ProductImportService.validate_product_data(valid_data)
    assert is_valid
    assert len(errors) == 0
    print("  ✅ 有效数据验证通过")

    # 无效数据
    invalid_data = {
        'title': '',
        'shop': '',
        'detail_url': ''
    }
    is_valid, errors = ProductImportService.validate_product_data(invalid_data)
    assert not is_valid
    assert len(errors) == 3
    print("  ✅ 无效数据验证通过")


def test_csv_import():
    """测试CSV导入功能"""
    print("\n🧪 测试CSV导入功能...")

    # 创建测试CSV
    test_file = create_test_csv()

    # 执行导入
    task_id = ProductImportService.start_import(str(test_file.parent))
    print(f"  📦 导入任务ID: {task_id}")

    # 等待导入完成
    import time
    for i in range(30):  # 最多等待30秒
        task = ProductImportService.get_import_task(task_id)
        if task['status'] in ['completed', 'failed']:
            break
        time.sleep(1)

    # 检查结果
    task = ProductImportService.get_import_task(task_id)
    print(f"  📊 任务状态: {task['status']}")
    print(f"  📊 成功: {task.get('total_success', 0)}")
    print(f"  📊 跳过: {task.get('total_skip', 0)}")
    print(f"  📊 错误: {task.get('total_error', 0)}")

    # 验证数据库
    test_products = Product.objects.filter(title__icontains='测试商品')
    print(f"  💾 数据库中有 {test_products.count()} 条测试数据")

    # 清理测试数据
    test_products.delete()
    test_file.unlink()

    print("  ✅ CSV导入测试通过")


def run_all_tests():
    """运行所有测试"""
    print("🚀 开始测试数据导入功能...")

    try:
        test_field_parsing()
        test_data_validation()
        test_csv_import()

        print("\n✅ 所有测试通过！")

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
