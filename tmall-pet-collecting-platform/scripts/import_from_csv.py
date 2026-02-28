"""
从 CSV 文件批量导入真实商品数据
支持从公开数据集（如 Kaggle/天池）或自定义 CSV 导入
"""

import csv
import sys
import os
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation

# 添加 backend 到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')

import django
django.setup()

from django.utils import timezone
from products.models import Product

def clean_price(price_str):
    """清洗价格字符串"""
    if not price_str:
        return None
    s = str(price_str).strip().replace('¥', '').replace('￥', '').replace('元', '').replace(',', '')
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None

def clean_sales(sales_str):
    """清洗销量字符串"""
    if not sales_str:
        return 0
    s = str(sales_str).strip().replace('人付款', '').replace('付款', '').replace('+', '').replace(',', '')
    if '万' in s:
        try:
            return int(float(s.replace('万', '')) * 10000)
        except ValueError:
            return 0
    try:
        return int(s)
    except ValueError:
        return 0

def import_csv(file_path, batch_size=1000):
    """导入 CSV 数据"""
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 {file_path}")
        return

    print(f"开始导入: {file_path}")
    
    products_to_create = []
    batch_no = timezone.now().strftime('IMPORT_%Y%m%d%H%M%S')
    success_count = 0
    skip_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 字段映射（根据 CSV 表头调整）
            title = row.get('title') or row.get('Title') or row.get('item_name')
            price_raw = row.get('price') or row.get('Price')
            sales_raw = row.get('sales') or row.get('Sales') or row.get('sold')
            shop = row.get('shop') or row.get('Shop') or row.get('shop_name')
            
            if not title or not price_raw:
                continue
                
            price = clean_price(price_raw)
            if price is None:
                continue
                
            sales = clean_sales(sales_raw)
            
            # 查重
            if Product.objects.filter(title=title, shop=shop).exists():
                skip_count += 1
                continue
                
            product = Product(
                title=title[:200], # 截断过长标题
                price=price,
                sales=sales,
                shop=shop or '未知店铺',
                brand=row.get('brand', '') or row.get('Brand', ''),
                category=row.get('category', '') or row.get('Category', '潮玩'),
                image_url=row.get('image_url', '') or row.get('pict_url', ''),
                detail_url=row.get('detail_url', '') or row.get('item_url', ''),
                batch_no=batch_no,
                crawl_time=timezone.now()
            )
            products_to_create.append(product)
            
            if len(products_to_create) >= batch_size:
                Product.objects.bulk_create(products_to_create)
                success_count += len(products_to_create)
                print(f"已导入 {success_count} 条...")
                products_to_create = []
                
    # 插入剩余数据
    if products_to_create:
        Product.objects.bulk_create(products_to_create)
        success_count += len(products_to_create)
        
    print(f"\n导入完成!")
    print(f"- 成功: {success_count}")
    print(f"- 跳过(重复): {skip_count}")
    print(f"- 批次号: {batch_no}")

def main():
    parser = argparse.ArgumentParser(description='导入商品数据 CSV')
    parser.add_argument('file', help='CSV 文件路径')
    args = parser.parse_args()
    
    import_csv(args.file)

if __name__ == '__main__':
    main()
