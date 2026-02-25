#!/usr/bin/env python3
"""
名称匹配分析 - 找出数据库中 area='China' 的记录在 CSV 中的对应项
"""
import csv
import pymysql
import re
from difflib import SequenceMatcher

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'yuwen123.',
    'database': 'heritage_db',
    'charset': 'utf8mb4'
}

def normalize(name):
    """标准化名称"""
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r'[,\.\-\(\)]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def similarity(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 获取数据库中 area='China' 的记录
    cursor.execute("SELECT id, name FROM heritage_items WHERE area = 'China'")
    db_records = cursor.fetchall()

    # 读取CSV数据
    csv_data = []
    with open('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/IhChina_2006-2021_import.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            area = row['Area'].strip()
            if area and area != 'China' and ('Province' in area or 'Autonomous' in area):
                csv_data.append({
                    'name': row['Name'].strip(),
                    'area': area,
                    'category': row['Category'].strip()
                })

    print(f"数据库中 area='China' 的记录: {len(db_records)} 条")
    print(f"CSV 中有省份信息的记录: {len(csv_data)} 条")
    print()

    # 匹配分析
    matches = {
        'exact': [],
        'high_sim': [],  # 相似度 >= 0.7
        'partial': [],   # 部分匹配
        'no_match': []
    }

    for record in db_records:
        db_name = record['name']
        db_norm = normalize(db_name)

        # 精确匹配
        exact = [c for c in csv_data if c['name'] == db_name]
        if exact:
            for e in exact:
                matches['exact'].append({
                    'db_id': record['id'],
                    'db_name': db_name,
                    'csv_name': e['name'],
                    'csv_area': e['area'],
                    'match_type': 'exact'
                })
            continue

        # 高相似度匹配
        best_sim = 0
        best_match = None
        for c in csv_data:
            sim = similarity(db_norm, normalize(c['name']))
            if sim > best_sim:
                best_sim = sim
                best_match = c

        if best_sim >= 0.7:
            matches['high_sim'].append({
                'db_id': record['id'],
                'db_name': db_name,
                'csv_name': best_match['name'],
                'csv_area': best_match['area'],
                'similarity': best_sim
            })
        elif best_sim >= 0.4:
            matches['partial'].append({
                'db_id': record['id'],
                'db_name': db_name,
                'csv_name': best_match['name'],
                'csv_area': best_match['area'],
                'similarity': best_sim
            })
        else:
            matches['no_match'].append({
                'db_id': record['id'],
                'db_name': db_name
            })

    print("=" * 80)
    print("匹配结果统计")
    print("=" * 80)
    print(f"精确匹配: {len(matches['exact'])} 条")
    print(f"高相似度匹配 (>=0.7): {len(matches['high_sim'])} 条")
    print(f"部分匹配 (0.4-0.7): {len(matches['partial'])} 条")
    print(f"无法匹配: {len(matches['no_match'])} 条")
    print()

    # 显示高相似度匹配
    print("=" * 80)
    print("高相似度匹配详情 (建议人工确认)")
    print("=" * 80)
    for m in matches['high_sim'][:30]:
        print(f"ID={m['db_id']}: {m['db_name']}")
        print(f"  -> CSV: {m['csv_name']}")
        print(f"  -> 地区: {m['csv_area']}")
        print(f"  -> 相似度: {m['similarity']:.3f}")
        print()

    # 生成SQL
    print("=" * 80)
    print("SQL更新语句")
    print("=" * 80)
    print()
    print("-- 精确匹配")
    for m in matches['exact']:
        area = m['csv_area'].replace("'", "''")
        print(f"UPDATE heritage_items SET area = '{area}' WHERE id = {m['db_id']}; -- {m['db_name']}")

    print()
    print("-- 高相似度匹配 (需人工确认)")
    for m in matches['high_sim']:
        area = m['csv_area'].replace("'", "''")
        print(f"-- UPDATE heritage_items SET area = '{area}' WHERE id = {m['db_id']}; -- {m['db_name']} (CSV: {m['csv_name']}, 相似度: {m['similarity']:.3f})")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
