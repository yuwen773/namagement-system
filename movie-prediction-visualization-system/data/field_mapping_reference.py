# -*- coding: utf-8 -*-
"""
数据集字段映射参考
用于将 TMDb 数据集映射到系统数据库表
"""

# ============================================================
# tmdb_5000_movies.csv -> movies 表
# ============================================================
MOVIES_FIELD_MAPPING = {
    # 数据集字段 -> (系统字段, 转换函数/说明)
    'title': ('title', '直接映射'),
    'release_date': ('release_date', '转换为Date类型'),
    'runtime': ('duration', '直接映射'),
    'revenue': ('box_office_total', '美元转万元: revenue / 70000'),
    'overview': ('description', '直接映射'),
    'status': ('status', '需要映射: Released->RELEASED, Post Production->COMING'),
    'genres': ('type_id', '解析JSON, 创建type记录'),
}

# 需要额外处理的字段
MOVIES_EXTRA_FIELDS = {
    'director': '从 tmdb_5000_credits-1.csv 的 crew 提取',
    'actors': '从 tmdb_5000_credits-1.csv 的 cast 提取',
    'poster_url': '从 movies_metadata.csv 的 poster_path 构建',
}

# ============================================================
# tmdb_5000_credits-1.csv -> movies 表（补充）
# ============================================================
CREDITS_FIELD_MAPPING = {
    'movie_id': ('关联字段', '用于与 movies 表关联'),
    'cast': ('actors', '解析JSON, 提取前5名演员'),
    'crew': ('director', '解析JSON, 提取 job="Director" 的记录'),
}

# ============================================================
# movies_metadata.csv -> movies 表（补充）
# ============================================================
METADATA_EXTRA_FIELDS = {
    'poster_path': ('poster_url', '拼接完整URL: https://image.tmdb.org/t/p/w500/ + poster_path'),
    'imdb_id': ('外部引用', '可存储用于外部链接'),
    'belongs_to_collection': ('系列信息', '可选字段'),
}

# ============================================================
# JSON 解析规则
# ============================================================

# genres JSON 格式:
# [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]
GENRES_PARSE_RULE = """
def parse_genres(genres_json):
    import json
    genres = json.loads(genres_json)
    return [g['name'] for g in genres]
"""

# cast JSON 格式:
# [{"cast_id": 242, "character": "Jake Sully", "name": "Sam Worthington", "order": 0}, ...]
CAST_PARSE_RULE = """
def parse_cast(cast_json, limit=5):
    import json
    cast = json.loads(cast_json)
    # 按 order 排序
    cast_sorted = sorted(cast, key=lambda x: x.get('order', 999))
    # 提取前 N 名演员
    actors = [a['name'] for a in cast_sorted[:limit]]
    return ', '.join(actors)
"""

# crew JSON 格式:
# [{"credit_id": "...", "department": "Directing", "job": "Director", "name": "James Cameron"}, ...]
CREW_PARSE_RULE = """
def parse_crew(crew_json, job='Director'):
    import json
    crew = json.loads(crew_json)
    # 筛选指定职位
    persons = [p['name'] for p in crew if p['job'] == job]
    return ', '.join(persons) if persons else None
"""

# ============================================================
# 数据质量检查规则
# ============================================================

# 必填字段检查
REQUIRED_FIELDS = {
    'movies': ['title', 'release_date'],
    'credits': ['movie_id'],
}

# 数据验证规则
DATA_VALIDATION_RULES = {
    'release_date': {
        'format': '%Y-%m-%d',
        'min': '1900-01-01',
        'max': '2030-12-31',
    },
    'runtime': {
        'type': 'int',
        'min': 0,
        'max': 300,  # 最长5小时
    },
    'box_office_total': {
        'type': 'decimal',
        'min': 0,
        'max': 1000000,  # 最大100亿元
    },
}

# ============================================================
# 状态值映射
# ============================================================

STATUS_MAPPING = {
    # TMDb status -> System status
    'Released': 'RELEASED',
    'Post Production': 'COMING',
    'Planned': 'COMING',
    'In Production': 'COMING',
    'Rumored': 'OFF',
}

# ============================================================
# 数据导入优先级
# ============================================================

# 优先级 1: 核心数据（必须导入）
PRIORITY_1 = [
    'tmdb_5000_movies.csv',
    'tmdb_5000_credits-1.csv',
]

# 优先级 2: 补充数据（可选导入）
PRIORITY_2 = [
    'movies_metadata.csv',
]

# 优先级 3: 不推荐导入
PRIORITY_3 = [
    'ratings_small.csv',  # 与系统需求不符
]

# ============================================================
# 数据处理注意事项
# ============================================================

NOTES = """
1. 票房单位转换:
   - TMDb revenue 单位: 美元
   - 系统字段单位: 万元人民币
   - 转换公式: box_office_total = revenue / 70000
   - 假设汇率: 1 USD = 7 CNY

2. 日期格式:
   - TMDb 格式: YYYY-MM-DD
   - 系统字段类型: Date
   - 需要确保日期格式正确

3. JSON 字段解析:
   - genres: 提取类型名称，创建 movie_types 记录
   - cast: 提取前3-5名演员，用逗号连接
   - crew: 提取导演，用逗号连接（可能有多个导演）

4. 缺失值处理:
   - revenue = 0: 视为缺失数据，设置为 0
   - runtime 缺失: 设置为 NULL
   - director 缺失: 设置为 NULL
   - actors 缺失: 设置为 NULL

5. 重复数据处理:
   - tmdb_5000_movies.csv 和 tmdb_5000_movies-1.csv 完全相同
   - 建议删除 -1 后缀的重复文件

6. 数据关联:
   - tmdb_5000_movies.csv.id = tmdb_5000_credits-1.csv.movie_id
   - 使用此关系合并两个数据集
"""

if __name__ == '__main__':
    print("数据集字段映射参考")
    print("=" * 80)
    print("\n请参考此文件了解如何将 TMDb 数据集映射到系统数据库表")
    print("\n数据导入优先级:")
    print("  PRIORITY_1 (核心数据):", ', '.join(PRIORITY_1))
    print("  PRIORITY_2 (补充数据):", ', '.join(PRIORITY_2))
    print("  PRIORITY_3 (不推荐):", ', '.join(PRIORITY_3))
