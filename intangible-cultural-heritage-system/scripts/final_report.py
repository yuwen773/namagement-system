#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国非遗系统数据地区信息分析报告
"""
import csv
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'yuwen123.',
    'database': 'heritage_db',
    'charset': 'utf8mb4'
}

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    report = []
    report.append("=" * 100)
    report.append("中国非遗系统数据地区信息分析报告")
    report.append("=" * 100)
    report.append("")
    report.append("生成时间: 2026-02-25")
    report.append("")

    # 1. 数据库总体统计
    report.append("-" * 100)
    report.append("一、数据库总体统计")
    report.append("-" * 100)
    report.append("")

    cursor.execute("SELECT COUNT(*) as total FROM heritage_items")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as count FROM heritage_items WHERE area = 'China'")
    china_only = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM heritage_items WHERE area LIKE '%Province%' OR area LIKE '%Autonomous Region%' OR area IN ('Beijing', 'Shanghai', 'Tianjin', 'Chongqing')")
    with_province = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM heritage_items WHERE area LIKE '%City%' AND area NOT LIKE '%Province%'")
    city_only = cursor.fetchone()['count']

    report.append(f"总记录数: {total}")
    report.append(f"  - area='China' (无具体地区): {china_only} 条 ({china_only/total*100:.1f}%)")
    report.append(f"  - 包含省份信息: {with_province} 条 ({with_province/total*100:.1f}%)")
    report.append(f"  - 仅有城市信息: {city_only} 条 ({city_only/total*100:.1f}%)")
    report.append(f"  - 其他国家/地区: {total - china_only - with_province - city_only} 条")
    report.append("")

    # 2. 省份分布统计
    report.append("-" * 100)
    report.append("二、中国省份分布统计（包含省份信息的记录）")
    report.append("-" * 100)
    report.append("")

    province_stats = {
        'Guizhou Province': 0, 'Yunnan Province': 0, 'Sichuan Province': 0,
        'Shaanxi Province': 0, 'Gansu Province': 0, 'Qinghai Province': 0,
        'Fujian Province': 0, 'Zhejiang Province': 0, 'Jiangsu Province': 0,
        'Shandong Province': 0, 'Henan Province': 0, 'Hubei Province': 0,
        'Hunan Province': 0, 'Guangdong Province': 0, 'Guangxi Zhuang Autonomous Region': 0,
        'Xinjiang Uygur Autonomous Region': 0, 'Tibet Autonomous Region': 0,
        'Inner Mongolia Autonomous Region': 0, 'Ningxia Hui Autonomous Region': 0,
        'Jilin Province': 0, 'Liaoning Province': 0, 'Heilongjiang Province': 0,
        'Hebei Province': 0, 'Shanxi Province': 0, 'Anhui Province': 0,
        'Jiangxi Province': 0, 'Hainan Province': 0, 'Chongqing': 0,
        'Beijing': 0, 'Shanghai': 0, 'Tianjin': 0
    }

    cursor.execute("SELECT area FROM heritage_items WHERE area LIKE '%Province%' OR area LIKE '%Autonomous Region%' OR area IN ('Beijing', 'Shanghai', 'Tianjin', 'Chongqing')")
    areas = cursor.fetchall()

    for row in areas:
        area = row['area']
        for province in province_stats:
            if province in area:
                province_stats[province] += 1

    sorted_provinces = sorted(province_stats.items(), key=lambda x: x[1], reverse=True)
    province_cn_map = {
        'Zhejiang Province': '浙江省', 'Guizhou Province': '贵州省',
        'Fujian Province': '福建省', 'Jiangsu Province': '江苏省',
        'Shandong Province': '山东省', 'Shaanxi Province': '陕西省',
        'Guangdong Province': '广东省', 'Sichuan Province': '四川省',
        'Yunnan Province': '云南省', 'Gansu Province': '甘肃省',
        'Henan Province': '河南省', 'Hubei Province': '湖北省',
        'Hunan Province': '湖南省', 'Anhui Province': '安徽省',
        'Hebei Province': '河北省', 'Shanxi Province': '山西省',
        'Liaoning Province': '辽宁省', 'Jilin Province': '吉林省',
        'Heilongjiang Province': '黑龙江省', 'Jiangxi Province': '江西省',
        'Guangxi Zhuang Autonomous Region': '广西壮族自治区',
        'Xinjiang Uygur Autonomous Region': '新疆维吾尔自治区',
        'Tibet Autonomous Region': '西藏自治区',
        'Inner Mongolia Autonomous Region': '内蒙古自治区',
        'Ningxia Hui Autonomous Region': '宁夏回族自治区',
        'Qinghai Province': '青海省', 'Hainan Province': '海南省',
        'Beijing': '北京市', 'Shanghai': '上海市',
        'Tianjin': '天津市', 'Chongqing': '重庆市'
    }

    report.append("省/自治区/直辖市\t\t记录数")
    report.append("-" * 50)
    for province_en, count in sorted_provinces:
        if count > 0:
            cn_name = province_cn_map.get(province_en, province_en)
            report.append(f"{cn_name}\t\t{count}")

    report.append("")

    # 3. 重复记录分析
    report.append("-" * 100)
    report.append("三、重复记录分析（同一项目有多个记录，部分有详细地区信息）")
    report.append("-" * 100)
    report.append("")

    cursor.execute("""
        SELECT name, GROUP_CONCAT(id ORDER BY id) as ids,
               GROUP_CONCAT(area ORDER BY id SEPARATOR ' | ') as areas,
               COUNT(*) as count
        FROM heritage_items
        GROUP BY name
        HAVING COUNT(*) > 1 AND SUM(area = 'China') > 0
        ORDER BY count DESC
    """)
    duplicates = cursor.fetchall()

    report.append(f"找到 {len(duplicates)} 个项目存在重复记录，其中部分有详细地区信息")
    report.append("")
    report.append("项目名称\t\t\t\t\tarea='China'的ID\t有详细地区的ID\t\t地区")
    report.append("-" * 100)

    updates_via_duplicates = []

    for dup in duplicates:
        name = dup['name']
        ids = dup['ids'].split(',')
        areas = dup['areas'].split(' | ')

        china_ids = []
        detailed_records = []

        for i, area in enumerate(areas):
            if area.strip() == 'China':
                china_ids.append(ids[i])
            elif 'Province' in area or 'Autonomous' in area or area.strip() in ['Beijing', 'Shanghai', 'Tianjin', 'Chongqing']:
                detailed_records.append((ids[i], area))

        if china_ids and detailed_records:
            # 显示前15个
            for i in range(min(15, len(china_ids))):
                updates_via_duplicates.append({
                    'id': china_ids[i],
                    'name': name,
                    'new_area': detailed_records[0][1],
                    'source_id': detailed_records[0][0]
                })

            name_short = (name[:40] + '...') if len(name) > 40 else name
            china_str = ', '.join(china_ids[:3])
            if len(china_ids) > 3:
                china_str += f" ({len(china_ids)}个)"
            detailed_str = ', '.join([f"{did}({darea[:30]}...)" for did, darea in detailed_records[:2]])

            report.append(f"{name_short}\t\t{china_str}\t\t{detailed_str}")

    report.append("")
    report.append(f"共找到 {len(updates_via_duplicates)} 条可更新的记录（通过数据库内重复匹配）")
    report.append("")

    # 4. CSV数据匹配分析
    report.append("-" * 100)
    report.append("四、CSV数据源（IhChina_2006-2021）分析")
    report.append("-" * 100)
    report.append("")

    csv_name_to_areas = {}
    with open('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/IhChina_2006-2021_import.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            area = row['Area'].strip()
            if area and area != 'China' and ('Province' in area or 'Autonomous' in area):
                if name not in csv_name_to_areas:
                    csv_name_to_areas[name] = []
                csv_name_to_areas[name].append(area)

    report.append(f"CSV文件中有 {len(csv_name_to_areas)} 个不同的项目名称包含省份信息")
    report.append("")

    # 检查CSV中的项目在数据库中的情况
    cursor.execute("SELECT id, name, area FROM heritage_items WHERE area = 'China'")
    china_records = cursor.fetchall()

    csv_exact_matches = []
    for record in china_records:
        if record['name'] in csv_name_to_areas:
            csv_exact_matches.append({
                'id': record['id'],
                'name': record['name'],
                'csv_areas': csv_name_to_areas[record['name']]
            })

    report.append(f"在数据库 area='China' 的记录中，找到 {len(csv_exact_matches)} 条与CSV完全匹配")
    report.append("")

    # 5. 建议的更新操作
    report.append("=" * 100)
    report.append("五、建议的更新操作")
    report.append("=" * 100)
    report.append("")

    report.append(f"通过数据库内重复匹配，可更新 {len(updates_via_duplicates)} 条记录")
    report.append(f"通过CSV数据匹配，可更新 {len(csv_exact_matches)} 条记录")
    report.append("")

    # 生成SQL语句
    report.append("-" * 100)
    report.append("SQL更新语句（执行前请备份数据库！）")
    report.append("-" * 100)
    report.append("")
    report.append("-- 方法1: 使用数据库中已有的详细地区信息更新")
    report.append("")

    processed_ids = set()
    for item in updates_via_duplicates:
        if item['id'] not in processed_ids:
            new_area = item['new_area'].replace("'", "''").replace("\\", "\\\\")
            report.append(f"UPDATE heritage_items SET area = '{new_area}' WHERE id = {item['id']}; -- {item['name']} (参考: ID={item['source_id']})")
            processed_ids.add(item['id'])

    report.append("")
    report.append("-- 方法2: 使用CSV数据更新（完全匹配的记录）")
    report.append("")

    for item in csv_exact_matches:
        if item['id'] not in processed_ids:
            # 取第一个地区
            area = item['csv_areas'][0].replace("'", "''")
            report.append(f"UPDATE heritage_items SET area = '{area}' WHERE id = {item['id']}; -- {item['name']}")
            processed_ids.add(item['id'])

    # 6. 总结
    report.append("")
    report.append("=" * 100)
    report.append("六、总结")
    report.append("=" * 100)
    report.append("")

    report.append("1. 数据库现状:")
    report.append(f"   - 总记录数: {total} 条")
    report.append(f"   - area='China' (无具体地区): {china_only} 条")
    report.append(f"   - 有详细省份信息: {with_province} 条")
    report.append("")

    report.append("2. 数据来源分析:")
    report.append("   - UNESCO世界级非遗数据: area='China'的记录（如Kun Qu opera, Peking opera等）")
    report.append("   - 中国国家级非遗数据: 有详细省份信息的记录（ID 1411-4452）")
    report.append("   - 部分项目在两个数据源中都有（如Manas）")
    report.append("")

    report.append("3. 更新建议:")
    report.append(f"   - 可立即更新（通过数据库内重复匹配）: {len(set(item['id'] for item in updates_via_duplicates))} 条")
    report.append(f"   - 可更新（通过CSV匹配）: {len(set(item['id'] for item in csv_exact_matches))} 条")
    report.append(f"   - 建议优先更新: {len(set(item['id'] for item in updates_via_duplicates) | set(item['id'] for item in csv_exact_matches))} 条")
    report.append("")

    report.append("4. 注意事项:")
    report.append("   - 执行SQL前请备份数据库")
    report.append("   - UNESCO的世界级非遗项目可能没有特定的省份，使用'China'可能是正确的")
    report.append("   - 建议人工审核后再批量更新")
    report.append("")

    # 保存报告
    report_path = 'D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/heritage_china_area_analysis_final.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f"分析完成！报告已保存到: {report_path}")
    print()
    print("摘要:")
    print(f"  - 数据库总记录数: {total}")
    print(f"  - area='China': {china_only} 条")
    print(f"  - 有省份信息: {with_province} 条")
    print(f"  - 可更新记录: {len(set(item['id'] for item in updates_via_duplicates) | set(item['id'] for item in csv_exact_matches))} 条")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
