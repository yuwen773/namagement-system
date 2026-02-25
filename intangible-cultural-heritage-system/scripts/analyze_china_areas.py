#!/usr/bin/env python3
"""
分析中国非遗记录的省份信息
对比数据库记录与原始CSV数据，找出可以更新的记录
"""
import csv
import re
import pymysql
from collections import defaultdict

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'yuwen123.',
    'database': 'heritage_db',
    'charset': 'utf8mb4'
}

# 中国省份列表（英文）
CHINESE_PROVINCES = {
    'Anhui Province': '安徽省',
    'Beijing': '北京市',
    'Chongqing': '重庆市',
    'Fujian Province': '福建省',
    'Gansu Province': '甘肃省',
    'Guangdong Province': '广东省',
    'Guangxi Zhuang Autonomous Region': '广西壮族自治区',
    'Guizhou Province': '贵州省',
    'Hainan Province': '海南省',
    'Hebei Province': '河北省',
    'Heilongjiang Province': '黑龙江省',
    'Henan Province': '河南省',
    'Hubei Province': '湖北省',
    'Hunan Province': '湖南省',
    'Inner Mongolia Autonomous Region': '内蒙古自治区',
    'Jiangsu Province': '江苏省',
    'Jiangxi Province': '江西省',
    'Jilin Province': '吉林省',
    'Liaoning Province': '辽宁省',
    'Ningxia Hui Autonomous Region': '宁夏回族自治区',
    'Qinghai Province': '青海省',
    'Shaanxi Province': '陕西省',
    'Shandong Province': '山东省',
    'Shanghai': '上海市',
    'Shanxi Province': '山西省',
    'Sichuan Province': '四川省',
    'Tianjin': '天津市',
    'Tibet Autonomous Region': '西藏自治区',
    'Xinjiang Uygur Autonomous Region': '新疆维吾尔自治区',
    'Yunnan Province': '云南省',
    'Zhejiang Province': '浙江省',
    # 台湾省、香港特别行政区、澳门特别行政区暂不处理
    'Taiwan Province': '台湾省',
    'Hong Kong Special Administrative Region': '香港特别行政区',
    'Macau Special Administrative Region': '澳门特别行政区',
}

def extract_province(area_text):
    """从地区文本中提取省份信息"""
    if not area_text or area_text == 'China':
        return None

    # 检查是否包含已知的省份名称
    for province_en, province_cn in CHINESE_PROVINCES.items():
        if province_en in area_text:
            return {
                'en': province_en,
                'cn': province_cn,
                'full_text': area_text
            }

    return None

def load_csv_data(csv_path):
    """加载CSV数据，建立名称到地区的映射"""
    name_to_areas = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            area = row['Area'].strip()
            country = row['Country'].strip()

            if country == 'China' and area and area != 'China':
                province_info = extract_province(area)
                if province_info:
                    name_to_areas[name].append({
                        'area': area,
                        'province': province_info,
                        'protection_unit': row['Protection Unit'].strip(),
                        'description': row['Description'].strip()
                    })

    return name_to_areas

def get_china_records_from_db():
    """从数据库获取所有中国的记录"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 获取所有 area = 'China' 的记录
    cursor.execute("""
        SELECT id, name, area, description
        FROM heritage_items
        WHERE area = 'China'
        ORDER BY id
    """)

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return records

def normalize_name(name):
    """标准化名称，用于匹配"""
    # 移除多余空格、标点
    name = re.sub(r'\s+', ' ', name).strip()
    # 移除括号内容（如中文翻译）
    name = re.sub(r'\([^)]*\)', '', name).strip()
    return name

def analyze_matches(db_records, csv_data):
    """分析匹配情况"""
    results = {
        'exact_match': [],      # 完全匹配
        'fuzzy_match': [],      # 模糊匹配
        'no_match': [],         # 无匹配
        'province_stats': defaultdict(int)  # 省份统计
    }

    for record in db_records:
        record_id = record['id']
        name = normalize_name(record['name'])

        # 尝试精确匹配
        if name in csv_data:
            for area_info in csv_data[name]:
                province = area_info['province']
                results['exact_match'].append({
                    'id': record_id,
                    'name': record['name'],
                    'current_area': record['area'],
                    'new_area': area_info['area'],
                    'province': province,
                    'protection_unit': area_info['protection_unit']
                })
                results['province_stats'][province['en']] += 1
        else:
            # 尝试模糊匹配
            found = False
            for csv_name, areas in csv_data.items():
                csv_name_normalized = normalize_name(csv_name)
                if name.lower() in csv_name_normalized.lower() or csv_name_normalized.lower() in name.lower():
                    for area_info in areas:
                        province = area_info['province']
                        results['fuzzy_match'].append({
                            'id': record_id,
                            'name': record['name'],
                            'csv_name': csv_name,
                            'current_area': record['area'],
                            'new_area': area_info['area'],
                            'province': province,
                            'protection_unit': area_info['protection_unit']
                        })
                        results['province_stats'][province['en']] += 1
                    found = True
                    break

            if not found:
                results['no_match'].append({
                    'id': record_id,
                    'name': record['name'],
                    'current_area': record['area']
                })

    return results

def generate_report(results):
    """生成分析报告"""
    report = []
    report.append("=" * 80)
    report.append("中国非遗记录地区信息分析报告")
    report.append("=" * 80)
    report.append("")

    # 总体统计
    total_exact = len(results['exact_match'])
    total_fuzzy = len(results['fuzzy_match'])
    total_no_match = len(results['no_match'])
    total_can_update = total_exact + total_fuzzy

    report.append("【总体统计】")
    report.append(f"  数据库中 area='China' 的记录总数: {total_exact + total_fuzzy + total_no_match}")
    report.append(f"  可精确匹配的记录: {total_exact}")
    report.append(f"  可模糊匹配的记录: {total_fuzzy}")
    report.append(f"  无法匹配的记录: {total_no_match}")
    report.append(f"  可更新记录总数: {total_can_update}")
    report.append("")

    # 省份分布统计
    report.append("【省份分布统计】")
    sorted_provinces = sorted(results['province_stats'].items(), key=lambda x: x[1], reverse=True)
    for province, count in sorted_provinces:
        cn_name = CHINESE_PROVINCES.get(province, province)
        report.append(f"  {cn_name} ({province}): {count} 条记录")
    report.append("")

    # 精确匹配示例（前20条）
    report.append("【精确匹配示例（前20条）】")
    for i, item in enumerate(results['exact_match'][:20], 1):
        report.append(f"  {i}. ID={item['id']}")
        report.append(f"     名称: {item['name']}")
        report.append(f"     当前地区: {item['current_area']}")
        report.append(f"     建议更新为: {item['new_area']}")
        report.append(f"     省份: {item['province']['cn']} ({item['province']['en']})")
        report.append("")

    # 模糊匹配示例（前10条）
    if results['fuzzy_match']:
        report.append("【模糊匹配示例（前10条）- 需人工确认】")
        for i, item in enumerate(results['fuzzy_match'][:10], 1):
            report.append(f"  {i}. ID={item['id']}")
            report.append(f"     数据库名称: {item['name']}")
            report.append(f"     CSV名称: {item['csv_name']}")
            report.append(f"     建议更新为: {item['new_area']}")
            report.append("")

    # 无法匹配的记录（前20条）
    if results['no_match']:
        report.append("【无法匹配的记录（前20条）- 可能需要单独处理】")
        for i, item in enumerate(results['no_match'][:20], 1):
            report.append(f"  {i}. ID={item['id']}, 名称: {item['name']}")
        report.append("")

    # 生成SQL更新语句
    report.append("=" * 80)
    report.append("【SQL更新语句（精确匹配）】")
    report.append("注意：执行前请先备份数据库！")
    report.append("=" * 80)
    report.append("")

    for item in results['exact_match']:
        # 转义单引号
        new_area = item['new_area'].replace("'", "''")
        report.append(f"UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']}")

    report.append("")
    report.append("=" * 80)
    report.append("【SQL更新语句（模糊匹配 - 需人工确认）】")
    report.append("=" * 80)
    report.append("")

    for item in results['fuzzy_match']:
        new_area = item['new_area'].replace("'", "''")
        report.append(f"-- UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']} (CSV: {item['csv_name']})")

    return "\n".join(report)

def main():
    # CSV文件路径
    csv_path = "D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/IhChina_2006-2021_import.csv"

    print("正在加载CSV数据...")
    csv_data = load_csv_data(csv_path)
    print(f"CSV数据加载完成，共 {len(csv_data)} 个项目")

    print("正在从数据库获取中国记录...")
    db_records = get_china_records_from_db()
    print(f"数据库查询完成，共 {len(db_records)} 条记录")

    print("正在分析匹配情况...")
    results = analyze_matches(db_records, csv_data)

    print("正在生成报告...")
    report = generate_report(results)

    # 保存报告
    report_path = "D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/china_areas_analysis_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"分析完成！报告已保存到: {report_path}")
    print("\n" + "=" * 80)
    print("报告摘要:")
    print("=" * 80)
    print(f"可精确匹配: {len(results['exact_match'])} 条")
    print(f"可模糊匹配: {len(results['fuzzy_match'])} 条")
    print(f"无法匹配: {len(results['no_match'])} 条")

    return report

if __name__ == "__main__":
    print(main())
