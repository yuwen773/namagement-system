"""
从淘宝爬虫 JSON 文件中提取 itemsArray 数据并导出为 CSV
"""

import csv
import json
import re
import sys
from typing import List, Dict, Any
from pathlib import Path


def clean_html(text: str) -> str:
    """移除 HTML 标签"""
    if not text:
        return ""
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def extract_item_data(item: Dict[str, Any]) -> Dict[str, str]:
    """
    从单个商品数据中提取关键字段

    Args:
        item: 商品数据字典

    Returns:
        提取后的数据字典
    """
    # 基本信息
    item_id = item.get('item_id', '')
    title = clean_html(item.get('title', ''))
    nick = item.get('nick', '')

    # 价格信息
    price = item.get('price', '')
    price_show = item.get('priceShow', {})
    price_unit = price_show.get('unit', '')
    price_desc = price_show.get('priceDesc', '')

    # 销量和地区
    real_sales = item.get('realSales', '')
    procity = item.get('procity', '')

    # 图片和链接
    pic_path = item.get('pic_path', '')
    auction_url = item.get('auctionURL', '')

    # 店铺信息
    shop_info = item.get('shopInfo', {})
    shop_title = shop_info.get('title', '')
    shop_tag = item.get('shopTag', '')

    # 标签
    icons = item.get('icons', [])
    icon_tags = []
    for icon in icons:
        text = icon.get('text', '')
        if text:
            icon_tags.append(text)
    tags = ', '.join(icon_tags)

    # 商品属性
    structured_usp = item.get('structuredUSPInfo', [])
    usp_list = []
    for usp in structured_usp:
        prop_name = usp.get('propertyName', '')
        prop_value = usp.get('propertyValueName', '')
        if prop_name and prop_value:
            usp_list.append(f"{prop_name}:{prop_value}")
    properties = ' | '.join(usp_list)

    return {
        '商品ID': item_id,
        '商品标题': title,
        '价格': price,
        '价格单位': price_unit,
        '价格描述': price_desc,
        '卖家昵称': nick,
        '店铺名称': shop_title,
        '店铺标签': shop_tag,
        '销量': real_sales,
        '地区': procity,
        '标签': tags,
        '商品属性': properties,
        '图片链接': pic_path,
        '商品链接': auction_url
    }


def extract_items_from_json(json_file: str) -> List[Dict[str, str]]:
    """
    从 JSON 文件中提取 itemsArray 数据

    支持两种格式:
    1. 单页格式: data.itemsArray
    2. 合并格式: items (数组)

    Args:
        json_file: JSON 文件路径

    Returns:
        商品数据列表
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取 itemsArray - 支持两种格式
    items_array = []

    # 格式1: 单页格式 data.itemsArray
    if 'data' in data and 'itemsArray' in data.get('data', {}):
        items_array = data.get('data', {}).get('itemsArray', [])
    # 格式2: 合并格式 items
    elif 'items' in data:
        items_array = data.get('items', [])

    if not items_array:
        print(f"未找到商品数据")
        return []

    print(f"找到 {len(items_array)} 个商品")

    # 提取每个商品的数据
    extracted_data = []
    for item in items_array:
        try:
            extracted_item = extract_item_data(item)
            extracted_data.append(extracted_item)
        except Exception as e:
            print(f"提取商品数据失败: {e}")
            continue

    return extracted_data


def save_to_csv(data: List[Dict[str, str]], csv_file: str):
    """
    将数据保存为 CSV 文件

    Args:
        data: 数据列表
        csv_file: CSV 文件路径
    """
    if not data:
        print("没有数据可保存")
        return

    # 定义字段顺序
    fieldnames = [
        '商品ID',
        '商品标题',
        '价格',
        '价格单位',
        '价格描述',
        '卖家昵称',
        '店铺名称',
        '店铺标签',
        '销量',
        '地区',
        '标签',
        '商品属性',
        '图片链接',
        '商品链接'
    ]

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"数据已保存到 {csv_file}")


def main():
    """主函数"""
    # 输入文件（支持命令行参数）
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = '高达模型_all_pages.json'

    # 输出文件
    if len(sys.argv) > 2:
        csv_file = sys.argv[2]
    else:
        # 自动生成 CSV 文件名
        json_path = Path(json_file)
        csv_file = json_path.stem + '.csv'

    # 检查文件是否存在
    if not Path(json_file).exists():
        print(f"文件不存在: {json_file}")
        return

    # 提取数据
    print(f"正在处理文件: {json_file}")
    data = extract_items_from_json(json_file)

    # 保存为 CSV
    if data:
        save_to_csv(data, csv_file)
        print(f"成功导出 {len(data)} 条商品数据到 {csv_file}")


if __name__ == '__main__':
    main()
