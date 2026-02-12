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
    票房单位转换：美元 -> 人民币万元
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
