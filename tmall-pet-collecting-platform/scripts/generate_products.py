"""
潮玩商品数据生成脚本
生成 10,000+ 条真实感强的潮玩商品数据并导入数据库

使用方法:
    python scripts/generate_products.py [--count N]
"""

import random
import uuid
import argparse
from datetime import datetime, timedelta
import sys
import os

# 添加 backend 到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')

import django
django.setup()

from products.models import Product


# 品牌与店铺配置
BRANDS = {
    '泡泡玛特': ['泡泡玛特旗舰店', 'POP MART官方', '泡泡玛特盲盒店', '潮玩实验室'],
    '万代': ['万代官方旗舰店', 'BANDAI官方店', '高达基地', '万代模型专营'],
    '乐高': ['乐高官方旗舰店', 'LEGO专卖店', '乐高授权专卖店', '颗粒积木乐园'],
    '原神': ['原神旗舰店', 'miHoYo官方', '原神周边商城', '提瓦特周边'],
    '宝可梦': ['宝可梦官方', '宝可梦中心', '口袋妖怪旗舰店', '宝可梦专营'],
    '航海王': ['航海王官方店', 'ONE PIECE周边', '海贼王专卖店', '尾田工作室'],
    '龙珠': ['龙珠官方店', '七龙珠周边店', '赛亚人装备', '龙珠超官方'],
    '初音未来': ['初音未来官方', 'MIKU官方店', 'VOCALOID周边', '未来音乐'],
    '明日方舟': ['明日方舟官方', '鹰角网络', 'Arknights周边', '罗德岛商店'],
    '蓝色监狱': ['蓝色监狱官方', '蓝色监狱周边店', '蹴击修业', '洁世一专区'],
    '三丽鸥': ['三丽鸥官方', 'HelloKitty旗舰店', '玉桂狗专卖店', '美乐蒂乐园'],
    '迪士尼': ['迪士尼官方', 'Disney旗舰店', '米奇专卖店', '漫威授权'],
    '变形金刚': ['变形金刚官方', '孩之宝旗舰店', '博派汽车人', '狂派霸天虎'],
    '假面骑士': ['假面骑士官方', '东映官方店', '骑士腰带专卖店', '昭和平成馆'],
    '新世纪福音战士': ['EVA官方', '新世纪福音战士店', '碇真嗣专区', '绫波丽周边'],
    '宫崎骏': ['吉卜力官方', '龙猫专卖店', '千与千寻周边', '天空之城'],
    '鬼灭之刃': ['鬼灭之刃官方', 'ufotable官方店', '灶门炭治郎', '鬼杀队'],
    '咒术回战': ['咒术回战官方', 'JUMP官方店', '五条悟专区', '宿傩周边'],
    'chiikawa': ['chiikawa官方', '吉伊卡哇旗舰店', '小八猫专卖店', '乌奇奇乐园'],
    '线条小狗': ['线条小狗官方', '马尔济斯专卖店', '线条修勾', '修勾小镇'],
}

# 商品关键词模板（按品牌分组）
PRODUCT_TEMPLATES = {
    '泡泡玛特': [
        'SKULLPANDA 夜之城系列 盲盒', 'SKULLPANDA 温度系列 隐藏款',
        'LABUBU 森林小屋 隐藏款', 'LABUBU 搪胶毛绒大娃', 'HIRONO 小野 失落人鱼',
        'HIRONO 小野 庇护所', 'Dimoo 太空旅行 盲盒', 'Dimoo 水族馆 隐藏款',
        'Crybaby 夜游系列', 'Crybaby 巡游系列', 'Zsiga 允许你难过',
        'Hacipupu 幼苗系列', 'Nyara 夜游神系列', 'Kubo 疯狂实验室',
        'The Monsters 怪物公司', 'Pinoo 豆豆眼'
    ],
    '万代': [
        'MG RX-78-2 高达模型', 'PG 独角兽 高达', 'RG 沙扎比',
        'MEGA 成品高达', '超合金魂 初始高达', 'HIRM 自由高达',
        'Figure-Rise 赛罗奥特曼', '假面骑士Decade腰带', '假面骑士极狐变身器',
        '龙珠Z 超四孙悟空', '龙珠超 悟吉塔', '航海王 草帽团手办',
        '航海王 POP系列 娜美', '海贼王 战国元帅', '龙珠 布罗利'
    ],
    '乐高': [
        'Technic 兰博基尼', 'Ideas 打字机', 'Botanical 花卉系列',
        'Icons 保时捷911', 'Creator Expert 街景', 'Architecture 系列',
        'City 城市系列', 'Ninjago 幻影忍者', 'Star Wars 星球大战',
        'Marvel 复仇者联盟', 'Disney 城堡系列', 'Friends 友谊系列',
        'Art 星球大战', 'Speed 赛车', 'Fortnite 堡垒之夜'
    ],
    '原神': [
        '钟离 璃月仙人 手办', '甘雨 椰羊 手办', '雷电将军 永恒 手办',
        '胡桃 往生堂主 手办', '温迪 吟游诗人 手办', '可莉 火花骑士 手办',
        '魈 降魔大圣 手办', '达达利亚 公子 手办', '神里绫华 稻妻 手办',
        '刻晴 璃月七星 手办', '宵宫 烟花工匠 手办', '优菈 浪花骑士 手办',
        '心海 军师 手办', '荒泷一斗 大孩子 手办', '申鹤 仙麟 手办',
        '角色立牌', '神之眼 周边', '派蒙 毛绒玩偶'
    ],
    '宝可梦': [
        '皮卡丘 毛绒玩具', '伊布 毛绒', '杰尼龟 喷火龙 妙蛙种子',
        '宝可梦 中心 玩偶', '宝可梦 手办', '宝可梦 盲盒',
        'Pokemon 官方徽章', '精灵球 道具', '宝可梦 拼装模型',
        '超梦 耿鬼 化石翼龙', '梦幻 基亚西', '烈空坐',
        '宝可梦 收藏卡片', 'Mega 进化模型', 'Z-Move 装置'
    ],
    '默认': [
        '盲盒 隐藏款', '手办 限量版', '扭蛋 动物系列', '景品 动漫角色',
        'GK 雕像 手办', '可动 关节人偶', 'Q版 卡通人物',
        '毛绒玩偶 大号', '徽章 挂件', '立牌 桌面',
        '海报 挂画', '钥匙扣 盲袋', '手机壳 定制',
        '水杯 周边', '抱枕 动漫', 'T恤 印花',
        '背包 周边', '手表 定制', '耳机 联名',
        '手链 配饰', '戒指 周边'
    ]
}

# 价格区间（品牌商品通常更贵）
PRICE_RANGES = {
    '泡泡玛特': (29, 199),
    '万代': (50, 2800),
    '乐高': (49, 6999),
    '原神': (35, 2880),
    '宝可梦': (19, 999),
    '航海王': (35, 1888),
    '龙珠': (35, 1688),
    '初音未来': (25, 1288),
    '明日方舟': (35, 1588),
    '迪士尼': (29, 2999),
    '三丽鸥': (15, 888),
    '默认': (9, 399)
}

# 销量范围（根据价格可能有差异）
SALES_RANGES = {
    '低价': (50, 5000),      # 0-100元
    '中价': (20, 2000),      # 100-500元
    '高价': (5, 500),        # 500-2000元
    '顶价': (1, 100),        # 2000+
}


def get_random_datetime(days_back=365):
    """生成随机日期时间（过去一年内）"""
    now = datetime.now()
    days_offset = random.randint(0, days_back)
    hours_offset = random.randint(0, 23)
    minutes_offset = random.randint(0, 59)
    return now - timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)


def generate_price(brand, base_range=None):
    """根据品牌生成价格"""
    if base_range:
        low, high = base_range
    else:
        low, high = PRICE_RANGES.get(brand, PRICE_RANGES['默认'])
    return round(random.uniform(low, high), 2)


def get_sales_category(price):
    """根据价格确定销量档位"""
    if price < 100:
        return '低价'
    elif price < 500:
        return '中价'
    elif price < 2000:
        return '高价'
    else:
        return '顶价'


def generate_sales(price):
    """生成符合价格区间的销量"""
    category = get_sales_category(price)
    low, high = SALES_RANGES[category]
    return random.randint(int(low), int(high))


def generate_product(index, brand=None, shops=None, templates=None):
    """生成单个商品数据"""
    # 随机选择品牌
    if brand is None:
        brand = random.choice(list(BRANDS.keys()))

    # 获取该品牌的店铺
    if shops is None:
        shops = BRANDS.get(brand, ['潮流店铺'])
    shop = random.choice(shops)

    # 获取该品牌的商品模板
    if templates is None:
        templates = PRODUCT_TEMPLATES.get(brand, PRODUCT_TEMPLATES['默认'])

    # 生成标题
    title_template = random.choice(templates)
    # 随机添加属性使标题更真实
    modifiers = ['', '', '', f'[{random.choice(["全新", "现货", "正版", "官方"])}]',
                 f'[{random.choice(["包邮", "送人", "收藏级", "展示级"])}]',
                 f'-{random.choice(["A", "B", "C", "隐藏"])}款']
    modifier = random.choice(modifiers)

    # 特殊处理：有些商品是系列名称
    if '系列' in title_template or '盲盒' in title_template or '手办' in title_template:
        series_suffix = ['', ' 第{}弹'.format(random.randint(1, 10)),
                        ' {}代'.format(random.randint(1, 5)),
                        ' 经典款', ' 新款', '']
        title = title_template + random.choice(series_suffix) + modifier
    else:
        title = title_template + ' ' + modifier

    # 随机添加数量标识
    if random.random() < 0.1:
        title = '{} {}个装'.format(title, random.randint(2, 6))

    # 生成价格和销量
    price = generate_price(brand)
    sales = generate_sales(price)

    # 生成批次号
    batch_no = 'BATCH_{}_{}'.format(
        datetime.now().strftime('%Y%m%d'),
        str(index).zfill(5)
    )

    # 生成类目
    categories = ['手办', '模型', '盲盒', '毛绒', '挂件', '周边', '收藏品', '潮玩']
    category = random.choice(categories)

    # 生成图片URL（使用占位图）
    image_url = f'https://placeholder.pics/svg/200x200/FF6B35/FFFFFF/Product_{index}'
    detail_url = f'https://detail.tmall.com/item.htm?id={6000000000000 + index}'

    # 生成采集时间
    crawl_time = get_random_datetime()

    return {
        'title': title[:200] if len(title) > 200 else title,
        'price': price,
        'sales': sales,
        'shop': shop,
        'image_url': image_url,
        'detail_url': detail_url,
        'brand': brand,
        'category': category,
        'batch_no': batch_no,
        'crawl_time': crawl_time,
    }


def generate_products(count=10000):
    """生成指定数量的商品数据"""
    print(f"正在生成 {count:,} 条商品数据...")
    products = []

    # 计算每个品牌生成的商品数量
    brands = list(BRANDS.keys())
    brand_counts = {}

    # 主要品牌分配更多权重
    weights = [10, 8, 7, 6, 5, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1][:len(brands)]
    total_weight = sum(weights)

    for i, brand in enumerate(brands):
        weight = weights[i] if i < len(weights) else 1
        brand_counts[brand] = int(count * weight / total_weight)

    # 调整确保总数正确
    current_total = sum(brand_counts.values())
    brand_counts[brands[0]] += count - current_total

    print(f"品牌分配: {dict(sorted(brand_counts.items(), key=lambda x: -x[1]))}")

    # 生成商品
    index = 0
    for brand in brands:
        brand_product_count = brand_counts[brand]
        shops = BRANDS[brand]
        templates = PRODUCT_TEMPLATES.get(brand, PRODUCT_TEMPLATES['默认'])

        for _ in range(brand_product_count):
            index += 1
            product_data = generate_product(index, brand, shops, templates)
            products.append(Product(**product_data))

            if index % 1000 == 0:
                print(f"  已生成 {index:,} 条商品...")

    return products


def insert_products(products, batch_size=1000):
    """批量插入商品数据"""
    total = len(products)
    print(f"\n开始插入 {total:,} 条商品数据到数据库...")

    # 分批插入
    for i in range(0, total, batch_size):
        batch = products[i:i + batch_size]
        Product.objects.bulk_create(batch)
        inserted = min(i + batch_size, total)
        print(f"  已插入 {inserted:,}/{total:,} 条 ({inserted/total*100:.1f}%)")

    print(f"插入完成！共插入 {total:,} 条商品。")


def verify_data():
    """验证数据质量"""
    print("\n数据质量验证:")
    print("-" * 50)

    total = Product.objects.count()
    print(f"1. 商品总数: {total:,} {'✅' if total >= 10000 else '❌'}")

    # 检查空标题
    empty_titles = Product.objects.filter(title__isnull=True).count() + \
                   Product.objects.filter(title='').count()
    print(f"2. 空标题数量: {empty_titles} {'✅' if empty_titles == 0 else '❌'}")

    # 检查无效价格
    invalid_prices = Product.objects.filter(price__lte=0).count()
    print(f"3. 无效价格数量: {invalid_prices} {'✅' if invalid_prices == 0 else '❌'}")

    # 检查无效销量
    invalid_sales = Product.objects.filter(sales__lt=0).count()
    print(f"4. 负销量数量: {invalid_sales} {'✅' if invalid_sales == 0 else '❌'}")

    # 检查重复（完全相同的标题+店铺+价格）
    from django.db.models import Count
    duplicates = Product.objects.values('title', 'shop', 'price').annotate(
        count=Count('id')
    ).filter(count__gt=1).count()
    print(f"5. 潜在重复组合数: {duplicates}")

    # 价格分布
    print("\n价格分布:")
    ranges = [
        (0, 50), (50, 100), (100, 200), (200, 500), (500, 1000), (1000, 99999)
    ]
    for low, high in ranges:
        count = Product.objects.filter(price__gte=low, price__lt=high).count()
        bar = '█' * int(count / 100)
        print(f"   ¥{low:>6}-¥{high:<6}: {count:>6,} {bar}")

    # 品牌分布
    print("\n品牌分布:")
    brand_counts = Product.objects.values('brand').annotate(
        count=Count('id')
    ).order_by('-count')

    for item in brand_counts[:10]:
        bar = '█' * int(item['count'] / 50)
        print(f"   {item['brand']:<10}: {item['count']:>6,} {bar}")

    # 销量统计
    print("\n销量统计:")
    avg_sales = Product.objects.aggregate(avg=models.Avg('sales'))['avg']
    max_sales = Product.objects.aggregate(max=models.Max('sales'))['max']
    print(f"   平均销量: {avg_sales:,.0f}")
    print(f"   最高销量: {max_sales:,}")

    print("-" * 50)
    return total >= 10000


def main():
    parser = argparse.ArgumentParser(description='生成潮玩商品数据')
    parser.add_argument('--count', type=int, default=10000, help='生成商品数量 (默认: 10000)')
    parser.add_argument('--skip-insert', action='store_true', help='仅生成数据不插入数据库')
    parser.add_argument('--verify-only', action='store_true', help='仅验证现有数据')
    args = parser.parse_args()

    if args.verify_only:
        success = verify_data()
        return 0 if success else 1

    # 生成数据
    products = generate_products(args.count)

    if not args.skip_insert:
        insert_products(products)
        verify_data()
    else:
        print(f"\n数据已生成 (共 {len(products)} 条)，未插入数据库")
        print("如需插入数据库，请运行: python scripts/generate_products.py")

    return 0


if __name__ == '__main__':
    sys.exit(main())
