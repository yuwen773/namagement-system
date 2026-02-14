#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为景点分配多样化图片的脚本
"""

import hashlib
import json
import pymysql

# 图片URL池 - 每个类别准备多种图片
IMAGE_POOLS = {
    '自然风光': [
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',  # 山脉
        'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800',  # 自然风景
        'https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=800',  # 森林
        'https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=800',  # 瀑布
        'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800',  # 湖泊
        'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800',  # 山谷
        'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800',  # 草原
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',  # 山脉日出
        'https://images.unsplash.com/photo-1518173946687-a4c036bc1e4f?w=800',  # 峡谷
        'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800',  # 雪山
    ],
    '人文古迹': [
        'https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800',  # 故宫
        'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',  # 长城
        'https://images.unsplash.com/photo-1548565322-153d471e2bdc?w=800',  # 古建筑
        'https://images.unsplash.com/photo-1527838832700-5059252407fa?w=800',  # 古镇
        'https://images.unsplash.com/photo-1526716173434-a1b1c64f6bd2?w=800',  # 古街
        'https://images.unsplash.com/photo-1576633066407-5c5c6c5e9b7e?w=800',  # 寺庙
        'https://images.unsplash.com/photo-1569183091675-4a28d43161de?w=800',  # 塔
        'https://images.unsplash.com/photo-1591123120675-6f7f1aae0e5b?w=800',  # 兵马俑
        'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800',  # 古典建筑
        'https://images.unsplash.com/photo-1529921879218-f99e50a72d3f?w=800',  # 长城
    ],
    '主题乐园': [
        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',  # 城堡
        'https://images.unsplash.com/photo-1514533450685-4493e01d1fdc?w=800',  # 游乐场
        'https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=800',  # 摩天轮
        'https://images.unsplash.com/photo-1565008447742-97f6f38c985c?w=800',  # 乐园
        'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800',  # 主题公园
        'https://images.unsplash.com/photo-1543794407-09e62e82c228?w=800',  # 游乐园
        'https://images.unsplash.com/photo-1585412727339-54e4bae3bbf9?w=800',  # 旋转木马
        'https://images.unsplash.com/photo-1606851181060-c7c4bc24c3df?w=800',  # 游乐设施
    ],
    '现代建筑': [
        'https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800',  # 现代建筑
        'https://images.unsplash.com/photo-1479839672679-a455b180eda7?w=800',  # 玻璃幕墙
        'https://images.unsplash.com/photo-1496568816309-51d7c20e3b21?w=800',  # 科技馆
        'https://images.unsplash.com/photo-1518005020951-eccb494ad742?w=800',  # 展览馆
        'https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=800',  # 博物馆
        'https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=800',  # 城市规划馆
    ],
    '其他': [
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
        'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800',
        'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800',
        'https://images.unsplash.com/photo-1548565322-153d471e2bdc?w=800',
        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',
    ]
}

# 知名景点特定图片
FAMOUS_ATTRACTION_IMAGES = {
    # 故宫
    '故宫': 'https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800',
    '北京故宫': 'https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800',

    # 长城
    '长城': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
    '八达岭长城': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
    '慕田峪长城': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
    '金山岭长城': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
    '司马台长城': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',

    # 颐和园
    '颐和园': 'https://images.unsplash.com/photo-1576633066407-5c5c6c5e9b7e?w=800',

    # 天坛
    '天坛': 'https://images.unsplash.com/photo-1569183091675-4a28d43161de?w=800',

    # 圆明园
    '圆明园': 'https://images.unsplash.com/photo-1527838832700-5059252407fa?w=800',

    # 西湖
    '西湖': 'https://images.unsplash.com/photo-1581591524425-c7e0978865fc?w=800',
    '杭州西湖': 'https://images.unsplash.com/photo-1581591524425-c7e0978865fc?w=800',

    # 黄山
    '黄山': 'https://images.unsplash.com/photo-1551981327-152924333a66?w=800',

    # 九寨沟
    '九寨沟': 'https://images.unsplash.com/photo-1583067570494-b771f28d88e7?w=800',

    # 丽江古城
    '丽江古城': 'https://images.unsplash.com/photo-1527838832700-5059252407fa?w=800',

    # 张家界
    '张家界': 'https://images.unsplash.com/photo-1580834341589-8c17a3a630ca?w=800',
    '张家界国家森林公园': 'https://images.unsplash.com/photo-1580834341589-8c17a3a630ca?w=800',

    # 桂林山水
    '桂林山水': 'https://images.unsplash.com/photo-1537531383496-f4749a4b8590?w=800',
    '桂林': 'https://images.unsplash.com/photo-1537531383496-f4749a4b8590?w=800',

    # 兵马俑
    '兵马俑': 'https://images.unsplash.com/photo-1591123120675-6f7f1aae0e5b?w=800',
    '秦始皇兵马俑': 'https://images.unsplash.com/photo-1591123120675-6f7f1aae0e5b?w=800',

    # 三亚
    '三亚': 'https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=800',
    '三亚湾': 'https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=800',
    '亚龙湾': 'https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=800',
    '蜈支洲岛': 'https://images.unsplash.com/photo-1506929562872-bb421503ef21?w=800',

    # 鼓浪屿
    '鼓浪屿': 'https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?w=800',

    # 迪士尼
    '上海迪士尼': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',
    '上海迪士尼乐园': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',
    '迪士尼': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',
    '香港迪士尼': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800',

    # 天安门
    '天安门': 'https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800',
    '天安门广场': 'https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800',
}


def get_image_for_attraction(name, category):
    """根据景点名称和类别获取图片URL"""
    # 1. 优先检查是否是知名景点
    for key, url in FAMOUS_ATTRACTION_IMAGES.items():
        if key in name:
            return url

    # 2. 根据类别和名称哈希分配图片
    pool = IMAGE_POOLS.get(category, IMAGE_POOLS['其他'])
    # 使用名称的MD5哈希值来选择图片，保证同一名称获得相同图片
    hash_val = int(hashlib.md5(name.encode('utf-8')).hexdigest(), 16)
    index = hash_val % len(pool)
    return pool[index]


def get_images_for_attraction(name, category, cover_url):
    """生成轮播图列表"""
    # 使用与封面不同的图片作为轮播图
    pool = IMAGE_POOLS.get(category, IMAGE_POOLS['其他'])

    # 找到封面图在池中的位置
    cover_index = 0
    for i, url in enumerate(pool):
        if url.replace('?w=800', '?w=1200') in cover_url:
            cover_index = i
            break

    # 选择2-3张其他图片作为轮播图
    images = [cover_url.replace('?w=800', '?w=1200')]
    for i in range(3):
        idx = (cover_index + i + 1) % len(pool)
        images.append(pool[idx].replace('?w=800', '?w=1200'))

    return json.dumps(images[:4])  # 最多4张图


def main():
    # 连接数据库
    conn = pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='yuwen123',
        database='tourist_attraction_db',
        charset='utf8mb4'
    )

    cursor = conn.cursor()

    # 获取所有景点
    cursor.execute("SELECT id, name, category FROM attractions")
    attractions = cursor.fetchall()

    print(f"开始更新 {len(attractions)} 个景点的图片...")

    update_count = 0
    for attr_id, name, category in attractions:
        cover_image = get_image_for_attraction(name, category)
        images = get_images_for_attraction(name, category, cover_image)

        cursor.execute(
            "UPDATE attractions SET cover_image = %s, images = %s WHERE id = %s",
            (cover_image, images, attr_id)
        )
        update_count += 1

        if update_count % 500 == 0:
            print(f"已更新 {update_count} 个景点...")
            conn.commit()

    conn.commit()
    print(f"更新完成！共更新 {update_count} 个景点")

    # 验证更新结果
    cursor.execute("SELECT category, COUNT(*) FROM attractions GROUP BY category")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
