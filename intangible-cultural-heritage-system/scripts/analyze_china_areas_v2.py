#!/usr/bin/env python3
"""
分析中国非遗记录的省份信息 - 第二版
专注于找出数据库中 area='China' 但可以在 CSV 中找到对应详细地区的记录
"""
import csv
import re
import pymysql
from collections import defaultdict
from difflib import SequenceMatcher

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'yuwen123.',
    'database': 'heritage_db',
    'charset': 'utf8mb4'
}

# 中国省份列表（英文）及其常见变体
CHINESE_PROVINCES = {
    # 省份
    'Anhui Province': '安徽省',
    'Fujian Province': '福建省',
    'Gansu Province': '甘肃省',
    'Guangdong Province': '广东省',
    'Guizhou Province': '贵州省',
    'Hainan Province': '海南省',
    'Hebei Province': '河北省',
    'Heilongjiang Province': '黑龙江省',
    'Henan Province': '河南省',
    'Hubei Province': '湖北省',
    'Hunan Province': '湖南省',
    'Jiangsu Province': '江苏省',
    'Jiangxi Province': '江西省',
    'Jilin Province': '吉林省',
    'Liaoning Province': '辽宁省',
    'Qinghai Province': '青海省',
    'Shaanxi Province': '陕西省',
    'Shandong Province': '山东省',
    'Shanxi Province': '山西省',
    'Sichuan Province': '四川省',
    'Yunnan Province': '云南省',
    'Zhejiang Province': '浙江省',
    # 自治区
    'Guangxi Zhuang Autonomous Region': '广西壮族自治区',
    'Inner Mongolia Autonomous Region': '内蒙古自治区',
    'Ningxia Hui Autonomous Region': '宁夏回族自治区',
    'Tibet Autonomous Region': '西藏自治区',
    'Xinjiang Uygur Autonomous Region': '新疆维吾尔自治区',
    # 直辖市
    'Beijing': '北京市',
    'Chongqing': '重庆市',
    'Shanghai': '上海市',
    'Tianjin': '天津市',
    # 特别行政区
    'Hong Kong Special Administrative Region': '香港特别行政区',
    'Macau Special Administrative Region': '澳门特别行政区',
}

def normalize_name(name):
    """标准化名称，用于匹配"""
    if not name:
        return ""
    # 转小写
    name = name.lower()
    # 移除多余空格
    name = re.sub(r'\s+', ' ', name).strip()
    # 移除常见的标点符号（保留括号）
    name = re.sub(r'[,\.:;!?"/\-\uff0c\u3002\uff1f\uff01\uff1b\uff1a\u201c\u201d\u2018\u2019]', ' ', name)
    # 再次清理空格
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def similarity(str1, str2):
    """计算两个字符串的相似度"""
    return SequenceMatcher(None, str1, str2).ratio()

def extract_province_info(area_text):
    """从地区文本中提取省份信息"""
    if not area_text or area_text == 'China':
        return None

    for province_en, province_cn in CHINESE_PROVINCES.items():
        if province_en in area_text:
            return {
                'en': province_en,
                'cn': province_cn
            }
    return None

def load_csv_data(csv_path):
    """加载CSV数据，建立索引"""
    # 按名称建立索引
    name_index = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            area = row['Area'].strip()
            country = row['Country'].strip()

            if country == 'China' and area and area != 'China':
                province_info = extract_province_info(area)
                if province_info:
                    name_index[normalize_name(name)].append({
                        'original_name': name,
                        'area': area,
                        'province': province_info,
                        'category': row['Category'].strip(),
                        'level': row['Level'].strip(),
                        'protection_unit': row['Protection Unit'].strip()
                    })

    return name_index

def get_china_records_from_db():
    """从数据库获取所有 area='China' 的记录"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT id, name, area, description, category_id, level
        FROM heritage_items
        WHERE area = 'China'
        ORDER BY id
    """)

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return records

def find_matches(db_records, csv_data):
    """查找匹配的记录"""
    results = {
        'exact_match': [],
        'high_similarity': [],  # 相似度 > 0.85
        'medium_similarity': [],  # 相似度 0.6-0.85
        'low_similarity': [],  # 相似度 < 0.6
        'no_match': [],
        'province_stats': defaultdict(set)  # 省份 -> 记录ID集合
    }

    for record in db_records:
        record_id = record['id']
        name = record['name']
        normalized_name = normalize_name(name)

        # 1. 尝试精确匹配
        if normalized_name in csv_data:
            for area_info in csv_data[normalized_name]:
                results['exact_match'].append({
                    'id': record_id,
                    'name': name,
                    'current_area': record['area'],
                    'new_area': area_info['area'],
                    'province': area_info['province'],
                    'csv_name': area_info['original_name'],
                    'match_type': 'exact'
                })
                results['province_stats'][area_info['province']['en']].add(record_id)
            continue

        # 2. 尝试模糊匹配
        best_match = None
        best_similarity = 0

        for csv_name, areas in csv_data.items():
            sim = similarity(normalized_name, csv_name)
            if sim > best_similarity:
                best_similarity = sim
                best_match = (csv_name, areas)

        if best_match and best_similarity > 0.6:
            csv_name, areas = best_match
            for area_info in areas:
                match_item = {
                    'id': record_id,
                    'name': name,
                    'current_area': record['area'],
                    'new_area': area_info['area'],
                    'province': area_info['province'],
                    'csv_name': area_info['original_name'],
                    'similarity': best_similarity
                }

                if best_similarity > 0.85:
                    results['high_similarity'].append(match_item)
                    results['province_stats'][area_info['province']['en']].add(record_id)
                elif best_similarity > 0.6:
                    results['medium_similarity'].append(match_item)
                    results['province_stats'][area_info['province']['en']].add(record_id)
        else:
            results['no_match'].append({
                'id': record_id,
                'name': name
            })

    return results

def generate_report(results):
    """生成分析报告"""
    report = []
    report.append("=" * 100)
    report.append("中国非遗记录地区信息分析报告 (v2)")
    report.append("=" * 100)
    report.append("")

    # 总体统计
    total_exact = len(results['exact_match'])
    total_high = len(results['high_similarity'])
    total_medium = len(results['medium_similarity'])
    total_no_match = len(results['no_match'])

    # 计算唯一记录数（因为一个记录可能有多个匹配）
    unique_exact_ids = set(item['id'] for item in results['exact_match'])
    unique_high_ids = set(item['id'] for item in results['high_similarity'])
    unique_medium_ids = set(item['id'] for item in results['medium_similarity'])

    report.append("【总体统计】")
    report.append(f"  数据库中 area='China' 的记录总数: {total_exact + total_high + total_medium + total_no_match}")
    report.append("")
    report.append("  按匹配类型统计（匹配次数）:")
    report.append(f"    - 精确匹配: {total_exact} 次")
    report.append(f"    - 高相似度匹配 (>0.85): {total_high} 次")
    report.append(f"    - 中等相似度匹配 (0.6-0.85): {total_medium} 次")
    report.append(f"    - 无法匹配: {total_no_match} 条")
    report.append("")
    report.append("  按记录数统计（唯一记录）:")
    report.append(f"    - 可精确匹配的记录: {len(unique_exact_ids)} 条")
    report.append(f"    - 可高相似度匹配的记录: {len(unique_high_ids)} 条")
    report.append(f"    - 可中等相似度匹配的记录: {len(unique_medium_ids)} 条")
    report.append(f"    - 建议可更新的记录: {len(unique_exact_ids | unique_high_ids)} 条")
    report.append("")

    # 省份分布统计
    report.append("【省份分布统计】")
    province_counts = {prov: len(ids) for prov, ids in results['province_stats'].items()}
    sorted_provinces = sorted(province_counts.items(), key=lambda x: x[1], reverse=True)

    for province, count in sorted_provinces:
        cn_name = CHINESE_PROVINCES.get(province, province)
        report.append(f"  {cn_name} ({province}): {count} 条记录")
    report.append("")

    # 精确匹配详情
    report.append("=" * 100)
    report.append("【精确匹配详情】")
    report.append("=" * 100)
    report.append("")

    for item in results['exact_match']:
        report.append(f"ID={item['id']}: {item['name']}")
        report.append(f"  CSV名称: {item['csv_name']}")
        report.append(f"  当前地区: {item['current_area']}")
        report.append(f"  建议更新为: {item['new_area']}")
        report.append(f"  省份: {item['province']['cn']}")
        report.append("")

    # 高相似度匹配详情
    if results['high_similarity']:
        report.append("=" * 100)
        report.append("【高相似度匹配详情 (>0.85) - 建议人工确认后更新】")
        report.append("=" * 100)
        report.append("")

        for item in results['high_similarity']:
            report.append(f"ID={item['id']}: {item['name']}")
            report.append(f"  CSV名称: {item['csv_name']}")
            report.append(f"  相似度: {item['similarity']:.3f}")
            report.append(f"  建议更新为: {item['new_area']}")
            report.append(f"  省份: {item['province']['cn']}")
            report.append("")

    # SQL 更新语句
    report.append("=" * 100)
    report.append("【SQL 更新语句】")
    report.append("=" * 100)
    report.append("注意：执行前请先备份数据库！")
    report.append("")
    report.append("-- 精确匹配的更新语句")
    report.append("")

    processed_ids = set()
    for item in results['exact_match']:
        if item['id'] not in processed_ids:
            new_area = item['new_area'].replace("'", "''").replace("\\", "\\\\")
            report.append(f"UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']}")
            processed_ids.add(item['id'])

    report.append("")
    report.append("-- 高相似度匹配的更新语句（需人工确认）")
    report.append("")

    for item in results['high_similarity']:
        if item['id'] not in processed_ids:
            new_area = item['new_area'].replace("'", "''").replace("\\", "\\\\")
            report.append(f"-- UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']} (CSV: {item['csv_name']}, 相似度: {item['similarity']:.3f})")

    return "\n".join(report)

def main():
    csv_path = "D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/IhChina_2006-2021_import.csv"

    print("正在加载CSV数据...")
    csv_data = load_csv_data(csv_path)
    print(f"CSV数据加载完成，共 {len(csv_data)} 个不同名称的项目")

    print("正在从数据库获取中国记录...")
    db_records = get_china_records_from_db()
    print(f"数据库查询完成，共 {len(db_records)} 条 area='China' 的记录")

    print("正在分析匹配情况...")
    results = find_matches(db_records, csv_data)

    print("正在生成报告...")
    report = generate_report(results)

    # 保存报告
    report_path = "D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/china_areas_analysis_report_v2.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"分析完成！报告已保存到: {report_path}")
    print("\n" + "=" * 80)
    print("报告摘要:")
    print("=" * 80)

    unique_exact = len(set(item['id'] for item in results['exact_match']))
    unique_high = len(set(item['id'] for item in results['high_similarity']))
    unique_medium = len(set(item['id'] for item in results['medium_similarity']))

    print(f"可精确匹配: {unique_exact} 条")
    print(f"可高相似度匹配: {unique_high} 条")
    print(f"可中等相似度匹配: {unique_medium} 条")
    print(f"无法匹配: {len(results['no_match'])} 条")
    print(f"\n建议可直接更新: {unique_exact} 条")
    print(f"建议人工确认后更新: {unique_high} 条")

    return results

if __name__ == "__main__":
    main()
