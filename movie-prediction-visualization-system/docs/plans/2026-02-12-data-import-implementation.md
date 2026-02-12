# 数据导入功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建完整的 TMDB 数据集导入功能，包括电影、影院、地域、票房记录的智能数据导入与生成

**Architecture:** 采用 Django management commands 架构，分为公共工具模块、分模块导入脚本、一键执行脚本三层结构

**Tech Stack:** Django 5.2, pandas, Python 3.11+

---

## Task 1: 创建公共数据处理工具模块

**Files:**
- Create: `backend/scripts/data_utils.py`

**Step 1: 创建 scripts 目录和初始化文件**

```bash
mkdir -p backend/scripts
touch backend/scripts/__init__.py
```

**Step 2: 编写 data_utils.py 完整代码**

```python
"""
数据导入公共工具模块
提供数据解析、验证、增强的通用函数
"""

import json
from datetime import datetime, date
from decimal import Decimal

# ==================== JSON 解析 ====================
def parse_json_safe(json_str):
    """安全解析 JSON 字符串"""
    if not json_str or json_str == 'NaN':
        return []
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return []

# ==================== 数据验证 ====================
def is_valid_movie(row):
    """验证电影数据是否有效"""
    # 过滤成人电影
    if row.get('adult') == True:
        return False, "成人电影"

    # 过滤已取消电影
    if str(row.get('status', '')) == 'Canceled':
        return False, "已取消"

    # 必填字段验证
    if not row.get('title') or not str(row.get('title', '')).strip():
        return False, "缺少标题"

    if not row.get('release_date'):
        return False, "缺少上映日期"

    return True, ""

# ==================== 字段提取 ====================
def extract_genres(genres_json):
    """从 genres JSON 提取类型名称列表"""
    genres = parse_json_safe(genres_json)
    return [g['name'] for g in genres if 'name' in g]

def extract_director(crew_json):
    """从 crew JSON 提取导演"""
    crew = parse_json_safe(crew_json)
    directors = [p['name'] for p in crew if p.get('job') == 'Director']
    return ', '.join(directors) if directors else '未知导演'

def extract_actors(cast_json, limit=5):
    """从 cast JSON 提取主演"""
    cast = parse_json_safe(cast_json)
    actors = [a['name'] for a in cast[:limit] if 'name' in a]
    return ', '.join(actors) if actors else '未知演员'

def extract_production_companies(companies_json):
    """提取制作公司"""
    companies = parse_json_safe(companies_json)
    return [c['name'] for c in companies if 'name' in c]

# ==================== 单位转换 ====================
def convert_revenue_to_rmb(usd_revenue):
    """
    票房单位转换：美元 → 人民币万元
    汇率：1美元 = 7人民币
    """
    if usd_revenue and float(usd_revenue) > 0:
        return round(Decimal(str(usd_revenue)) / Decimal('7') / Decimal('10000'), 2)
    return Decimal('0.00')

def map_status(tmdb_status):
    """映射 TMDb 状态到系统状态"""
    status_map = {
        'Released': 'RELEASED',
        'Post Production': 'COMING',
        'In Production': 'COMING',
        'Planned': 'COMING',
        'Rumored': 'OFF',
    }
    return status_map.get(tmdb_status, 'RELEASED')

# ==================== 日期处理 ====================
def parse_release_date(date_str):
    """解析上映日期"""
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

# ==================== 数据增强 ====================
def build_enhanced_description(row):
    """构建增强的影片描述"""
    parts = []

    # 基础简介
    if row.get('overview'):
        parts.append(row['overview'])

    # 宣传语
    if row.get('tagline'):
        parts.append(f"【宣传语】{row['tagline']}")

    # 制作公司
    companies = extract_production_companies(row.get('production_companies'))
    if companies:
        parts.append(f"【制作】{', '.join(companies[:3])}")

    # 制作国家
    countries = parse_json_safe(row.get('production_countries'))
    if countries:
        country_names = [c['name'] for c in countries[:3] if 'name' in c]
        parts.append(f"【制片】{', '.join(country_names)}")

    # 对白语言
    spoken = parse_json_safe(row.get('spoken_languages'))
    if spoken:
        lang_names = [l['name'] for l in spoken[:3] if 'name' in l]
        parts.append(f"【语言】{', '.join(lang_names)}")

    # 系列电影
    collection = parse_json_safe(row.get('belongs_to_collection'))
    if collection and 'name' in collection:
        parts.append(f"【系列】{collection['name']}")

    # IMDb
    if row.get('imdb_id'):
        parts.append(f"【IMDb】tt{row['imdb_id']}")

    return ' | '.join(parts) if parts else '暂无简介'

def get_poster_url(poster_path):
    """构建完整海报 URL"""
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Poster"

def get_language_name(iso_code):
    """ISO语言代码转中文名"""
    lang_map = {
        'en': '英语', 'zh': '中文', 'ja': '日语', 'ko': '韩语',
        'fr': '法语', 'de': '德语', 'es': '西班牙语', 'it': '意大利语',
        'ru': '俄语', 'th': '泰语', 'vi': '越南语', 'ar': '阿拉伯语',
    }
    return lang_map.get(iso_code, iso_code)

# ==================== 日志统计 ====================
class ImportStats:
    """导入统计器"""
    def __init__(self):
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []

    def add_success(self):
        self.success += 1

    def add_failed(self, reason, record_id=None):
        self.failed += 1
        self.errors.append({'reason': reason, 'id': record_id})

    def add_skipped(self):
        self.skipped += 1

    def summary(self):
        total = self.success + self.failed + self.skipped
        if total == 0:
            return "\n===== 导入统计 =====\n总数: 0\n==================\n"
        return f"""
===== 导入统计 =====
总数: {total}
成功: {self.success} ({self.success/total*100:.1f}%)
失败: {self.failed} ({self.failed/total*100:.1f}%)
跳过: {self.skipped} ({self.skipped/total*100:.1f}%)
==================
"""

    def print_errors(self, limit=10):
        """打印错误详情（限制数量）"""
        if not self.errors:
            return
        print(f"\n--- 失败详情（前{min(limit, len(self.errors))}条）---")
        for err in self.errors[:limit]:
            print(f"  ID: {err.get('id')}, 原因: {err['reason']}")
```

**Step 3: 测试工具模块**

```bash
cd backend
python -c "from scripts.data_utils import parse_json_safe, extract_genres; print(parse_json_safe('[{\"name\": \"Action\"}]')); print(extract_genres('[{\"name\": \"Action\"}]'))"
```

Expected: `[]` and `['Action']`

**Step 4: 提交**

```bash
git add backend/scripts/
git commit -m "feat: 添加数据导入公共工具模块"
```

---

## Task 2: 创建影片导入命令

**Files:**
- Create: `backend/movies/management/commands/import_movies.py`

**Step 1: 确保 management/commands 目录存在**

```bash
mkdir -p backend/movies/management/commands
touch backend/movies/management/__init__.py
touch backend/movies/management/commands/__init__.py
```

**Step 2: 编写 import_movies.py 完整代码**

```python
from django.core.management.base import BaseCommand
import pandas as pd
import sys
import os

# 添加 scripts 路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(backend_dir, 'scripts'))

from data_utils import *

class Command(BaseCommand):
    help = '导入电影数据（从 tmdb CSV 文件）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--movies-file',
            type=str,
            default='data/tmdb_5000_movies.csv',
            help='电影数据文件路径'
        )
        parser.add_argument(
            '--credits-file',
            type=str,
            default='data/tmdb_5000_credits-1.csv',
            help='演职员数据文件路径'
        )
        parser.add_argument(
            '--metadata-file',
            type=str,
            default='data/movies_metadata.csv',
            help='元数据文件路径（可选，用于增强）'
        )

    def handle(self, *args, **options):
        from movies.models import Movie, MovieType

        stats = ImportStats()

        self.stdout.write(self.style.HTTP_INFO("开始导入电影数据..."))

        # 读取数据
        try:
            movies_df = pd.read_csv(options['movies_file'])
            credits_df = pd.read_csv(options['credits_file'])
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f"文件未找到: {e}"))
            return

        metadata_df = None
        if options['metadata_file'] and os.path.exists(options['metadata_file']):
            metadata_df = pd.read_csv(options['metadata_file'])
            self.stdout.write(f"读取 metadata: {len(metadata_df)} 条")

        self.stdout.write(f"读取到 {len(movies_df)} 条电影记录")

        # 第一阶段：创建所有类型
        self.stdout.write(self.style.HTTP_INFO("\n=== 第一阶段：导入影片类型 ==="))
        self.import_movie_types(movies_df, stats)

        # 第二阶段：合并数据并导入电影
        self.stdout.write(self.style.HTTP_INFO("\n=== 第二阶段：导入影片数据 ==="))
        self.import_movies(movies_df, credits_df, metadata_df, stats)

        # 输出统计
        self.stdout.write(stats.summary())
        stats.print_errors()

    def import_movie_types(self, movies_df, stats):
        """导入影片类型"""
        from movies.models import MovieType

        all_genres = set()
        for genres_json in movies_df['genres']:
            genres = extract_genres(genres_json)
            all_genres.update(genres)

        for genre_name in all_genres:
            obj, created = MovieType.objects.get_or_create(name=genre_name)
            if created:
                stats.add_success()
            else:
                stats.add_skipped()

        self.stdout.write(f"影片类型导入完成：{stats.success} 个新类型")

    def import_movies(self, movies_df, credits_df, metadata_df, stats):
        """导入影片数据"""
        from movies.models import Movie, MovieType

        # 合并 credits
        merged = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='left')

        # 合并 metadata（如果存在）
        if metadata_df is not None:
            # 只合并 metadata 中有 poster_path 的记录以增强数据
            merged = merged.merge(
                metadata_df[['id', 'poster_path', 'imdb_id', 'popularity',
                             'vote_average', 'vote_count', 'tagline',
                             'production_companies', 'production_countries',
                             'spoken_languages', 'homepage', 'belongs_to_collection',
                             'original_language', 'original_title']],
                on='id',
                how='left',
                suffixes=('', '_meta')
            )

        for idx, row in merged.iterrows():
            # 验证数据
            is_valid, reason = is_valid_movie(row)
            if not is_valid:
                stats.add_failed(reason, row.get('id'))
                continue

            try:
                # 检查是否已存在
                existing = Movie.objects.filter(title=row['title']).first()
                if existing:
                    stats.add_skipped()
                    continue

                # 获取类型
                genre_names = extract_genres(row.get('genres', '[]'))
                genre_obj = None
                if genre_names:
                    genre_obj = MovieType.objects.filter(name=genre_names[0]).first()

                # 创建电影
                movie = Movie.objects.create(
                    title=str(row['title']),
                    director=extract_director(row.get('crew', '[]')),
                    actors=extract_actors(row.get('cast', '[]')),
                    release_date=parse_release_date(row.get('release_date')),
                    duration=int(row['runtime']) if pd.notna(row['runtime']) else 90,
                    type=genre_obj,
                    poster_url=get_poster_url(row.get('poster_path')),
                    description=build_enhanced_description(row),
                    box_office_total=convert_revenue_to_rmb(row.get('revenue', 0)),
                    status=map_status(str(row.get('status', 'Released'))),
                )
                stats.add_success()

                if stats.success % 100 == 0:
                    self.stdout.write(f"已导入 {stats.success} 部电影...")

            except Exception as e:
                stats.add_failed(str(e), row.get('id'))

        self.stdout.write(self.style.SUCCESS(f"影片导入完成：{stats.success} 部"))
```

**Step 3: 测试导入命令**

```bash
cd backend
python manage.py import_movies --help
```

Expected: 显示命令帮助信息

**Step 4: 提交**

```bash
git add backend/movies/management/commands/
git commit -m "feat: 添加电影数据导入命令"
```

---

## Task 3: 创建影院和地域导入命令

**Files:**
- Create: `backend/cinemas/management/commands/import_cinemas.py`

**Step 1: 确保 management/commands 目录存在**

```bash
mkdir -p backend/cinemas/management/commands
touch backend/cinemas/management/__init__.py
touch backend/cinemas/management/commands/__init__.py
```

**Step 2: 编写 import_cinemas.py 完整代码**

```python
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = '导入地域和影院数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cinema-count',
            type=int,
            default=200,
            help='目标影院数量'
        )

    def handle(self, *args, **options):
        from cinemas.models import Region, Cinema

        stats = {'regions': 0, 'cinemas': 0}

        self.stdout.write(self.style.HTTP_INFO("开始导入地域和影院数据..."))

        # 第一阶段：导入地域
        self.stdout.write(self.style.HTTP_INFO("\n=== 第一阶段：导入地域 ==="))
        self.import_regions(stats)

        # 第二阶段：生成影院
        self.stdout.write(self.style.HTTP_INFO("\n=== 第二阶段：生成影院 ==="))
        self.import_cinemas(options['cinema_count'], stats)

        self.stdout.write(self.style.SUCCESS(f"\n导入完成：地域 {stats['regions']} 个，影院 {stats['cinemas']} 家"))

    # ============= 地域数据 =============
    REGIONS_DATA = [
        # 直辖市
        {'name': '北京市', 'level': 'PROVINCE', 'children': ['东城区', '朝阳区', '海淀区', '丰台区']},
        {'name': '上海市', 'level': 'PROVINCE', 'children': ['黄浦区', '徐汇区', '浦东新区', '静安区']},
        {'name': '天津市', 'level': 'PROVINCE', 'children': ['和平区', '河西区', '南开区']},
        {'name': '重庆市', 'level': 'PROVINCE', 'children': ['渝中区', '江北区', '沙坪坝区']},
        # 华东
        {'name': '浙江省', 'level': 'PROVINCE', 'children': ['杭州市', '宁波市', '温州市']},
        {'name': '江苏省', 'level': 'PROVINCE', 'children': ['南京市', '苏州市', '无锡市']},
        {'name': '山东省', 'level': 'PROVINCE', 'children': ['济南市', '青岛市']},
        {'name': '福建省', 'level': 'PROVINCE', 'children': ['福州市', '厦门市', '泉州市']},
        {'name': '安徽省', 'level': 'PROVINCE', 'children': ['合肥市', '芜湖市']},
        # 华南
        {'name': '广东省', 'level': 'PROVINCE', 'children': ['广州市', '深圳市', '佛山市', '东莞市']},
        {'name': '广西壮族自治区', 'level': 'PROVINCE', 'children': ['南宁市', '桂林市', '柳州市']},
        {'name': '海南省', 'level': 'PROVINCE', 'children': ['海口市', '三亚市']},
        # 华中
        {'name': '湖北省', 'level': 'PROVINCE', 'children': ['武汉市', '宜昌市', '襄阳市']},
        {'name': '湖南省', 'level': 'PROVINCE', 'children': ['长沙市', '株洲市']},
        {'name': '河南省', 'level': 'PROVINCE', 'children': ['郑州市', '洛阳市', '开封市']},
        {'name': '江西省', 'level': 'PROVINCE', 'children': ['南昌市', '赣州市']},
        # 华北
        {'name': '河北省', 'level': 'PROVINCE', 'children': ['石家庄市', '唐山市', '秦皇岛市']},
        {'name': '山西省', 'level': 'PROVINCE', 'children': ['太原市', '大同市']},
        {'name': '内蒙古自治区', 'level': 'PROVINCE', 'children': ['呼和浩特市', '包头市']},
        # 西南
        {'name': '四川省', 'level': 'PROVINCE', 'children': ['成都市', '绵阳市', '德阳市']},
        {'name': '云南省', 'level': 'PROVINCE', 'children': ['昆明市', '大理市']},
        {'name': '贵州省', 'level': 'PROVINCE', 'children': ['贵阳市', '遵义市']},
        {'name': '西藏自治区', 'level': 'PROVINCE', 'children': ['拉萨市']},
        # 西北
        {'name': '陕西省', 'level': 'PROVINCE', 'children': ['西安市', '宝鸡市']},
        {'name': '甘肃省', 'level': 'PROVINCE', 'children': ['兰州市', '敦煌市']},
        {'name': '青海省', 'level': 'PROVINCE', 'children': ['西宁市']},
        {'name': '宁夏回族自治区', 'level': 'PROVINCE', 'children': ['银川市']},
        {'name': '新疆维吾尔自治区', 'level': 'PROVINCE', 'children': ['乌鲁木齐市']},
        # 东北
        {'name': '辽宁省', 'level': 'PROVINCE', 'children': ['沈阳市', '大连市', '鞍山市']},
        {'name': '吉林省', 'level': 'PROVINCE', 'children': ['长春市', '吉林市']},
        {'name': '黑龙江省', 'level': 'PROVINCE', 'children': ['哈尔滨市', '大庆市']},
    ]

    # ============= 影院品牌数据 =============
    CINEMA_CHAINS = {
        # 高端
        '万达影城': {'prefix': '万达影城', 'screen': (8, 15), 'seat': (1500, 3000), 'tier': 3},
        'CGV影城': {'prefix': 'CGV影城', 'screen': (7, 14), 'seat': (1300, 2800), 'tier': 3},
        '博纳国际影城': {'prefix': '博纳国际影城', 'screen': (7, 12), 'seat': (1200, 2500), 'tier': 3},
        'UME影城': {'prefix': 'UME影城', 'screen': (7, 13), 'seat': (1400, 2600), 'tier': 3},
        '中影国际影城': {'prefix': '中影国际影城', 'screen': (7, 14), 'seat': (1300, 2700), 'tier': 3},
        '耀莱成龙国际影城': {'prefix': '耀莱成龙国际影城', 'screen': (9, 16), 'seat': (1800, 3500), 'tier': 3},
        # 中端
        '大地影院': {'prefix': '大地影院', 'screen': (5, 10), 'seat': (800, 1800), 'tier': 2},
        '金逸影城': {'prefix': '金逸影城', 'screen': (6, 12), 'seat': (1000, 2200), 'tier': 2},
        '横店电影城': {'prefix': '横店电影城', 'screen': (6, 11), 'seat': (900, 2000), 'tier': 2},
        '上影影城': {'prefix': '上影影城', 'screen': (6, 12), 'seat': (1100, 2300), 'tier': 2},
        '星美国际影城': {'prefix': '星美国际影城', 'screen': (6, 10), 'seat': (1000, 1900), 'tier': 2},
        '保利万和电影院': {'prefix': '保利万和电影院', 'screen': (5, 9), 'seat': (800, 1600), 'tier': 2},
        '沃美影城': {'prefix': '沃美影城', 'screen': (6, 11), 'seat': (1000, 2000), 'tier': 2},
        '幸福蓝海国际影城': {'prefix': '幸福蓝海国际影城', 'screen': (6, 11), 'seat': (950, 2000), 'tier': 2},
        '苏宁影城': {'prefix': '苏宁影城', 'screen': (5, 10), 'seat': (900, 1800), 'tier': 2},
        '恒大嘉凯影城': {'prefix': '恒大嘉凯影城', 'screen': (7, 12), 'seat': (1200, 2400), 'tier': 2},
        '奥斯卡影城': {'prefix': '奥斯卡影城', 'screen': (5, 10), 'seat': (850, 1800), 'tier': 2},
        '长城国际影城': {'prefix': '长城国际影城', 'screen': (5, 9), 'seat': (850, 1700), 'tier': 2},
        '华人影城': {'prefix': '华人影城', 'screen': (5, 8), 'seat': (750, 1500), 'tier': 2},
        '金球影城': {'prefix': '金球影城', 'screen': (5, 8), 'seat': (800, 1500), 'tier': 2},
        '启航国际影城': {'prefix': '启航国际影城', 'screen': (5, 9), 'seat': (850, 1600), 'tier': 2},
        '博纳影业': {'prefix': '博纳影业', 'screen': (6, 11), 'seat': (1100, 2300), 'tier': 2},
        '传奇影城': {'prefix': '传奇影城', 'screen': (5, 9), 'seat': (850, 1700), 'tier': 2},
        # 艺术
        '百老汇电影中心': {'prefix': '百老汇电影中心', 'screen': (5, 9), 'seat': (600, 1300), 'tier': 2},
        '卢米埃影城': {'prefix': '卢米埃影城', 'screen': (4, 8), 'seat': (700, 1500), 'tier': 2},
        '美亚影城': {'prefix': '美亚影城', 'screen': (4, 7), 'seat': (600, 1200), 'tier': 2},
        '百老汇影院': {'prefix': '百老汇影院', 'screen': (4, 8), 'seat': (600, 1400), 'tier': 2},
        '新天地国际影城': {'prefix': '新天地国际影城', 'screen': (4, 8), 'seat': (650, 1400), 'tier': 2},
        '星光国际影城': {'prefix': '星光国际影城', 'screen': (4, 8), 'seat': (700, 1500), 'tier': 2},
        # 基础
        '今世界国际影城': {'prefix': '今世界国际影城', 'screen': (4, 7), 'seat': (600, 1100), 'tier': 1},
        '博悦影城': {'prefix': '博悦影城', 'screen': (4, 7), 'seat': (600, 1200), 'tier': 1},
        '银河电影院': {'prefix': '银河电影院', 'screen': (4, 7), 'seat': (650, 1300), 'tier': 1},
        '百花电影院': {'prefix': '百花电影院', 'screen': (3, 6), 'seat': (500, 1000), 'tier': 1},
        '大众影剧院': {'prefix': '大众影剧院', 'screen': (3, 6), 'seat': (500, 1000), 'tier': 1},
    }

    def import_regions(self, stats):
        """导入地域数据"""
        for province_data in self.REGIONS_DATA:
            # 创建省份
            province, created = Region.objects.get_or_create(
                name=province_data['name'],
                defaults={'level': 'PROVINCE', 'parent': None}
            )
            if created:
                stats['regions'] += 1

            # 创建城市
            for city_name in province_data['children']:
                city, created = Region.objects.get_or_create(
                    name=city_name,
                    defaults={'level': 'CITY', 'parent': province}
                )
                if created:
                    stats['regions'] += 1

        self.stdout.write(f"地域导入完成：{stats['regions']} 个")

    def import_cinemas(self, target_count, stats):
        """生成影院数据"""
        cities = list(Region.objects.filter(level='CITY'))

        if not cities:
            self.stdout.write(self.style.ERROR("请先导入地域数据！"))
            return

        # 城市等级分配权重
        city_weights = {}
        for city in cities:
            province = city.parent.name if city.parent else ''
            if province in ['北京市', '上海市', '广州市', '深圳市']:
                city_weights[city] = 5  # 一线城市权重高
            elif province in ['浙江省', '江苏省', '四川省', '湖北省', '福建省', '山东省']:
                city_weights[city] = 3
            else:
                city_weights[city] = 1

        for i in range(target_count):
            # 加权随机选择城市
            selected_city = random.choices(
                cities,
                weights=[city_weights.get(c, 1) for c in cities],
                k=1
            )[0]

            # 随机选择品牌
            brand = random.choice(list(self.CINEMA_CHAINS.keys()))
            brand_info = self.CINEMA_CHAINS[brand]

            # 生成影院名称
            suffix = random.choice(['广场店', '购物中心店', '凯德店', '店', f'{selected_city.name}店'])
            cinema_name = f"{brand_info['prefix']}({selected_city.name}{suffix})"

            # 生成地址
            street = random.choice(['建设路', '人民路', '中山路', '解放路', '文化路', '商业街', '步行街', '广场路'])
            number = random.randint(1, 999)
            address = f"{selected_city.name}{street}{number}号"

            # 生成电话
            phone = f"{random.randint(10000000000, 99999999999)}"

            # 创建影院
            Cinema.objects.create(
                name=cinema_name,
                address=address,
                phone=phone,
                region=selected_city,
                screen_count=random.randint(*brand_info['screen']),
                seats_count=random.randint(*brand_info['seat']),
                is_active=True
            )
            stats['cinemas'] += 1

            if stats['cinemas'] % 50 == 0:
                self.stdout.write(f"已生成 {stats['cinemas']} 家影院...")

        self.stdout.write(self.style.SUCCESS(f"影院生成完成：{stats['cinemas']} 家"))
```

**Step 3: 测试导入命令**

```bash
cd backend
python manage.py import_cinemas --help
```

Expected: 显示命令帮助信息

**Step 4: 提交**

```bash
git add backend/cinemas/management/commands/
git commit -m "feat: 添加影院和地域数据导入命令"
```

---

## Task 4: 创建票房记录生成命令

**Files:**
- Create: `backend/boxoffice/management/commands/generate_boxoffice.py`

**Step 1: 确保 management/commands 目录存在**

```bash
mkdir -p backend/boxoffice/management/commands
touch backend/boxoffice/management/__init__.py
touch backend/boxoffice/management/commands/__init__.py
```

**Step 2: 编写 generate_boxoffice.py 完整代码**

```python
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
from decimal import Decimal
import random

class Command(BaseCommand):
    help = '生成票房记录数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='开始日期 (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2025-12-31',
            help='结束日期 (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='批量插入大小'
        )

    def handle(self, *args, **options):
        from movies.models import Movie
        from cinemas.models import Cinema
        from boxoffice.models import BoxOfficeRecord

        start_date = datetime.strptime(options['start-date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(options['end-date'], '%Y-%m-%d').date()
        batch_size = options['batch-size']

        stats = {'records': 0, 'movies_processed': 0}

        self.stdout.write(f"生成票房记录：{start_date} 到 {end_date}")

        # 获取有票房的电影
        movies = Movie.objects.filter(box_office_total__gt=0)
        cinemas = list(Cinema.objects.filter(is_active=True))

        if not cinemas:
            self.stdout.write(self.style.ERROR("请先导入影院数据！"))
            return

        self.stdout.write(f"处理 {movies.count()} 部电影，{len(cinemas)} 家影院")

        batch_records = []

        for movie in movies:
            stats['movies_processed'] += 1
            if stats['movies_processed'] % 100 == 0:
                self.stdout.write(f"已处理 {stats['movies_processed']} 部电影...")

            # 生成该电影的票房记录
            movie_records = self.generate_movie_records(movie, cinemas, start_date, end_date)
            batch_records.extend(movie_records)

            # 批量插入
            if len(batch_records) >= batch_size:
                BoxOfficeRecord.objects.bulk_create(batch_records, ignore_conflicts=True)
                stats['records'] += len(batch_records)
                batch_records = []

        # 插入剩余记录
        if batch_records:
            BoxOfficeRecord.objects.bulk_create(batch_records, ignore_conflicts=True)
            stats['records'] += len(batch_records)

        self.stdout.write(self.style.SUCCESS(f"完成！生成 {stats['records']} 条票房记录"))

    def generate_movie_records(self, movie, cinemas, start_date, end_date):
        """为单部电影生成票房记录"""
        records = []

        total_box_office_yuan = movie.box_office_total * Decimal('10000')
        show_days = random.randint(30, 90)

        # 确定电影实际上映期间
        movie_start = max(movie.release_date, start_date) if movie.release_date else start_date
        movie_end = min(movie_start + timedelta(days=show_days), end_date)

        if movie_start >= movie_end:
            return records

        # 计算每日衰减系数总和
        decay_sum = sum([self.decay_factor(i) for i in range(show_days)])

        current_day = 0
        current_date = movie_start

        while current_date <= movie_end and current_day < show_days:
            # 计算当日总票房
            daily_total = int(float(total_box_office_yuan) * self.decay_factor(current_day) / decay_sum)

            if daily_total > 0:
                # 分配到影院
                cinema_records = self.distribute_to_cinemas(
                    daily_total, movie, cinemas, current_date
                )
                records.extend(cinema_records)

            current_date += timedelta(days=1)
            current_day += 1

        return records

    def decay_factor(self, day):
        """票房衰减系数"""
        return 0.85 ** (day / 7)  # 每周衰减15%

    def distribute_to_cinemas(self, daily_total, movie, cinemas, record_date):
        """将当日票房分配到影院"""
        # 根据热度选择影院数量
        popularity = getattr(movie, 'popularity', 10) if hasattr(movie, 'popularity') else 10
        if popularity > 50:
            num_cinemas = random.randint(8, 15)
        elif popularity > 20:
            num_cinemas = random.randint(4, 8)
        else:
            num_cinemas = random.randint(1, 3)

        # 按座位数排序，优先选择大影院
        sorted_cinemas = sorted(cinemas, key=lambda c: c.seats_count, reverse=True)
        selected = sorted_cinemas[:min(num_cinemas, len(sorted_cinemas))]

        records = []
        remaining = daily_total

        for i, cinema in enumerate(selected):
            if i == len(selected) - 1:
                amount = remaining
            else:
                ratio = cinema.seats_count / sum(c.seats_count for c in selected)
                amount = int(daily_total * ratio)
                remaining -= amount

            # 计算场次和人次
            is_weekend = record_date.weekday() in [5, 6]
            base_screenings = cinema.screen_count * 0.6
            weekend_mult = 1.5 if is_weekend else 1.0
            screenings = int(base_screenings * weekend_mult)
            screenings = max(1, min(screenings, cinema.screen_count))

            # 观影人次（平均票价35-45元）
            avg_price = random.uniform(35, 45)
            audience = max(0, int(amount / avg_price))

            records.append(BoxOfficeRecord(
                movie=movie,
                cinema=cinema,
                record_date=record_date,
                daily_box_office=amount,
                screening_count=screenings,
                audience_count=audience
            ))

        return records
```

**Step 3: 测试生成命令**

```bash
cd backend
python manage.py generate_boxoffice --help
```

Expected: 显示命令帮助信息

**Step 4: 提交**

```bash
git add backend/boxoffice/management/commands/
git commit -m "feat: 添加票房记录生成命令"
```

---

## Task 5: 创建一键导入命令

**Files:**
- Create: `backend/management/commands/import_all.py`

**Step 1: 确保 management/commands 目录存在**

```bash
mkdir -p backend/management/commands
touch backend/management/__init__.py
touch backend/management/commands/__init__.py
```

**Step 2: 编写 import_all.py 完整代码**

```python
from django.core.management.base import BaseCommand
from django.core import management
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = '一键执行所有数据导入（地域→影院→电影→票房）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cinema-count',
            type=int,
            default=200,
            help='生成影院数量'
        )
        parser.add_argument(
            '--skip-movies',
            action='store_true',
            help='跳过电影导入'
        )
        parser.add_argument(
            '--skip-boxoffice',
            action='store_true',
            help='跳过票房生成'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='票房数据开始日期'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2025-12-31',
            help='票房数据结束日期'
        )

    def handle(self, *args, **options):
        start_time = timezone.now()

        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS("    电影票房预测系统 - 数据导入工具"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write("")

        try:
            # ============ 阶段1: 导入地域和影院 ============
            self.stdout.write(self.style.HTTP_INFO("\n【1/4】导入地域和影院数据..."))
            management.call_command('import_cinemas', '--cinema-count', str(options['cinema_count']))
            self.stdout.write(self.style.SUCCESS("✓ 地域和影院数据导入完成"))

            # ============ 阶段2: 导入电影 ============
            if not options['skip_movies']:
                self.stdout.write(self.style.HTTP_INFO("\n【2/4】导入电影数据..."))
                management.call_command('import_movies')
                self.stdout.write(self.style.SUCCESS("✓ 电影数据导入完成"))
            else:
                self.stdout.write(self.style.WARNING("⊘ 跳过电影导入"))

            # ============ 阶段3: 生成票房 ============
            if not options['skip_boxoffice']:
                self.stdout.write(self.style.HTTP_INFO("\n【3/4】生成票房记录..."))
                management.call_command(
                    'generate_boxoffice',
                    '--start-date', options['start-date'],
                    '--end-date', options['end-date']
                )
                self.stdout.write(self.style.SUCCESS("✓ 票房记录生成完成"))
            else:
                self.stdout.write(self.style.WARNING("⊘ 跳过票房生成"))

            # ============ 阶段4: 数据统计 ============
            self.stdout.write(self.style.HTTP_INFO("\n【4/4】数据统计..."))
            self.print_statistics()

            # ============ 完成 ============
            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("=" * 50))
            self.stdout.write(self.style.SUCCESS(f"导入完成！耗时: {duration:.1f}秒"))
            self.stdout.write(self.style.SUCCESS("=" * 50))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n导入失败: {str(e)}"))
            raise

    def print_statistics(self):
        """打印导入后的数据统计"""
        from movies.models import Movie, MovieType
        from cinemas.models import Region, Cinema
        from boxoffice.models import BoxOfficeRecord

        stats = {
            '影片类型': MovieType.objects.count(),
            '影片总数': Movie.objects.count(),
            '有票房影片': Movie.objects.filter(box_office_total__gt=0).count(),
            '地域总数': Region.objects.count(),
            '影院总数': Cinema.objects.filter(is_active=True).count(),
            '票房记录': BoxOfficeRecord.objects.count(),
        }

        self.stdout.write("\n┌────────────────────────────────────┐")
        self.stdout.write("│           数据统计                  │")
        self.stdout.write("├────────────────────────────────────┤")
        for key, value in stats.items():
            self.stdout.write(f"│ {key:12s}: {value:>12}      │")
        self.stdout.write("└────────────────────────────────────┘")
```

**Step 3: 测试一键导入命令**

```bash
cd backend
python manage.py import_all --help
```

Expected: 显示命令帮助信息

**Step 4: 提交**

```bash
git add backend/management/commands/
git commit -m "feat: 添加一键导入命令"
```

---

## Task 6: 更新进度文档

**Files:**
- Modify: `memory-bank/progress.md`

**Step 1: 更新进度**

```bash
git add memory-bank/progress.md
git commit -m "docs(progress): 更新数据导入功能完成状态"
```

---

## Task 7: 最终验证与测试

**Step 1: 确保数据文件存在**

```bash
ls -la data/
# 确保存在:
# - tmdb_5000_movies.csv
# - tmdb_5000_credits-1.csv
# - movies_metadata.csv
```

**Step 2: 执行完整导入测试**

```bash
cd backend
python manage.py import_all --cinema-count 50
```

Expected: 成功导入所有数据，显示统计信息

**Step 3: 验证数据**

```bash
python manage.py shell
>>> from movies.models import Movie, MovieType
>>> from cinemas.models import Region, Cinema
>>> from boxoffice.models import BoxOfficeRecord
>>> print(f"影片类型: {MovieType.objects.count()}")
>>> print(f"影片总数: {Movie.objects.count()}")
>>> print(f"地域: {Region.objects.count()}")
>>> print(f"影院: {Cinema.objects.count()}")
>>> print(f"票房记录: {BoxOfficeRecord.objects.count()}")
```

**Step 4: 最终提交**

```bash
git add .
git commit -m "feat: 完成数据导入功能实现与测试"
```
