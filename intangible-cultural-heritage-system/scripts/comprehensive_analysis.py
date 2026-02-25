#!/usr/bin/env python3
"""
全面分析中国非遗记录的地区信息
"""
import csv
import pymysql
from collections import defaultdict

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'yuwen123.',
    'database': 'heritage_db',
    'charset': 'utf8mb4'
}

# 中国省份映射
PROVINCE_MAP = {
    'Anhui Province': '安徽省',
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
    'Beijing': '北京市',
    'Chongqing': '重庆市',
}

def extract_province(area):
    """从地区字符串中提取省份"""
    if not area or area == 'China':
        return None
    for prov_en, prov_cn in PROVINCE_MAP.items():
        if prov_en in area:
            return prov_en
    return None

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    print("=" * 80)
    print("中国非遗记录地区信息分析")
    print("=" * 80)
    print()

    # 1. 总体统计
    cursor.execute("SELECT COUNT(*) as total FROM heritage_items")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as count FROM heritage_items WHERE area = 'China'")
    china_only = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM heritage_items WHERE area LIKE '%Province%' OR area LIKE '%Autonomous Region%' OR area LIKE '%Municipality%'")
    with_province = cursor.fetchone()['count']

    print("【数据库总体统计】")
    print(f"  总记录数: {total}")
    print(f"  area='China' 的记录: {china_only}")
    print(f"  有省份信息的记录: {with_province}")
    print(f"  其他: {total - china_only - with_province}")
    print()

    # 2. 检查有重复名称的记录
    cursor.execute("""
        SELECT name, GROUP_CONCAT(id ORDER BY id) as ids, GROUP_CONCAT(area ORDER BY id SEPARATOR ' | ') as areas, COUNT(*) as count
        FROM heritage_items
        GROUP BY name
        HAVING COUNT(*) > 1 AND (SUM(area = 'China') > 0 OR SUM(area LIKE '%Province%') > 0)
        ORDER BY count DESC
        LIMIT 30
    """)
    duplicates = cursor.fetchall()

    print("【有重复名称且包含 'China' 或省份信息的记录】")
    print(f"共找到 {len(duplicates)} 组重复记录")
    print()

    update_candidates = []

    for dup in duplicates:
        name = dup['name']
        ids = dup['ids'].split(',')
        areas = dup['areas'].split(' | ')

        # 找出有地区信息的记录
        china_ids = []
        detailed_ids = []

        for i, area in enumerate(areas):
            if area == 'China':
                china_ids.append(ids[i])
            elif extract_province(area):
                detailed_ids.append((ids[i], area))

        if china_ids and detailed_ids:
            print(f"名称: {name}")
            print(f"  area='China' 的ID: {', '.join(china_ids)}")
            print(f"  有地区信息的ID: {', '.join(f'{id}({area})' for id, area in detailed_ids)}")

            # 对于每个 China ID，建议使用第一个详细地区信息
            for china_id in china_ids:
                if detailed_ids:
                    update_candidates.append({
                        'id': china_id,
                        'name': name,
                        'current_area': 'China',
                        'suggested_area': detailed_ids[0][1],
                        'source_id': detailed_ids[0][0]
                    })
            print()

    # 3. CSV 数据分析
    print("=" * 80)
    print("【CSV 数据分析】")
    print()

    csv_name_to_areas = defaultdict(list)
    with open('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/IhChina_2006-2021_import.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            area = row['Area'].strip()
            if area and area != 'China':
                province = extract_province(area)
                if province:
                    csv_name_to_areas[name].append(area)

    print(f"CSV 文件中有 {len(csv_name_to_areas)} 个不同的项目名称")
    print(f"涉及 {sum(len(v) for v in csv_name_to_areas.values())} 条记录（同一项目可能有多个地区）")
    print()

    # 4. 找出 CSV 中的项目在数据库中的情况
    cursor.execute("SELECT id, name, area FROM heritage_items WHERE area = 'China'")
    china_records = cursor.fetchall()

    csv_matches = []
    for record in china_records:
        if record['name'] in csv_name_to_areas:
            csv_matches.append({
                'id': record['id'],
                'name': record['name'],
                'csv_areas': csv_name_to_areas[record['name']]
            })

    print(f"在 CSV 中找到匹配的 area='China' 记录: {len(csv_matches)} 条")
    print()

    # 5. 生成 SQL 更新语句
    print("=" * 80)
    print("【SQL 更新建议】")
    print()
    print("-- 方法1: 使用数据库中已有的详细地区信息更新 'China' 记录")
    print()

    for item in update_candidates[:50]:  # 只显示前50条
        new_area = item['suggested_area'].replace("'", "''")
        print(f"UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']} (参考 ID: {item['source_id']})")

    print()
    print("-- 方法2: 使用 CSV 数据更新 'China' 记录（如果名称匹配）")
    print()

    for item in csv_matches[:20]:  # 只显示前20条
        for area in item['csv_areas'][:1]:  # 每个项目只取第一个地区
            new_area = area.replace("'", "''")
            print(f"UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']}")

    print()
    print("=" * 80)
    print("【总结】")
    print()
    print(f"通过数据库内重复记录匹配，可更新 {len(update_candidates)} 条记录")
    print(f"通过 CSV 数据匹配，可更新 {len(csv_matches)} 条记录")
    print()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
