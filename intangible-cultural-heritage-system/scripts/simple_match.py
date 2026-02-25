#!/usr/bin/env python3
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

# 读取CSV数据
csv_data = {}
with open('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/tmp/IhChina_2006-2021_import.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name'].strip()
        area = row['Area'].strip()
        if area and area != 'China' and 'Province' in area:
            csv_data[name] = area

# 连接数据库
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor(pymysql.cursors.DictCursor)

# 获取 area = 'China' 的记录
cursor.execute("SELECT id, name, area FROM heritage_items WHERE area = 'China'")
db_records = cursor.fetchall()

matches = []
for record in db_records:
    if record['name'] in csv_data:
        matches.append({
            'id': record['id'],
            'name': record['name'],
            'new_area': csv_data[record['name']]
        })

print(f"Found {len(matches)} exact matches")
for m in matches[:20]:
    print(f"ID={m['id']}: {m['name']} -> {m['new_area']}")

cursor.close()
conn.close()
