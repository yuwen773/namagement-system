# 数据导入设计方案

**文档日期**: 2026-02-12
**设计目标**: 完美、准确、高质量地将 TMDB 数据集导入电影票房预测与可视化系统

---

## 一、设计概述

### 1.1 导入目标

- **数据覆盖**: 导入所有可用电影数据（tmdb_5000_movies.csv 4,803部 + movies_metadata.csv 45,466部）
- **数据质量**: 智能数据增强，合理处理缺省值
- **完整度**: 同时生成影院、地域、票房记录等关联数据

### 1.2 数据源

| 文件 | 记录数 | 用途 |
|------|-------|------|
| tmdb_5000_movies.csv | 4,803 | 主要数据源（高质量） |
| tmdb_5000_credits-1.csv | 4,803 | 导演、演员信息 |
| movies_metadata.csv | 45,466 | 扩展数据（海报、评分等） |

---

## 二、数据增强策略

### 2.1 Metadata 字段分类与利用

```
┌────────────────────────────────────────────────────────────────────────┐
│                    Metadata 数据增强分类                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  📊 数据质量验证字段（用于过滤和清洗）                                   │
│  ├── adult          → 过滤成人电影                                      │
│  ├── status        → 验证电影状态（Canceled 电影跳过）                   │
│  ├── vote_count    → 评分数验证（>0 才认为有参考价值）                 │
│  └── video         → 标记是否有预告片资源                              │
│                                                                        │
│  🎯 核心展示字段（存入扩展模型）                                        │
│  ├── popularity    → 热度评分（用于排序、推荐）                         │
│  ├── vote_average → 用户评分（0-10分）                                  │
│  ├── vote_count   → 评分人数（验证评分可信度）                         │
│  ├── imdb_id      → 外部引用（可跳转 IMDb）                            │
│  └── original_language → 原始语言（多语言筛选）                        │
│                                                                        │
│  📝 内容增强字段（合并到 description）                                 │
│  ├── overview       → 基础简介                                        │
│  ├── tagline       → 宣传语                                          │
│  ├── production_companies → 制作公司                                  │
│  ├── production_countries → 制作国家                                  │
│  └── spoken_languages → 对白语言                                      │
│                                                                        │
│  🖼️ 视觉资源字段                                                      │
│  ├── poster_path   → 海报图片 URL                                      │
│  ├── belongs_to_collection → 系列电影信息                             │
│  └── homepage     → 官网链接                                          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 缺失数据处理

| 字段 | 缺失处理方式 |
|------|-------------|
| `title` | 必填，缺失则跳过该记录 |
| `release_date` | 必填，缺失则跳过该记录 |
| `runtime` → `duration` | 缺失填充为 90 分钟（中等长度） |
| `revenue` → `box_office_total` | 为 0 则填充为 0，后续可标记为"待补充" |
| `director` | 缺失填充为"未知导演" |
| `actors` | 缺失填充为"未知演员" |
| `overview` → `description` | 缺失填充为"暂无简介" |
| `poster_url` | 从 metadata 提取，仍缺失则使用默认占位图 |
| `genres` → `type_id` | 缺失则分配到"其他"类型 |

### 2.3 单位转换

```python
# 票房：美元 → 人民币万元
def convert_revenue(usd_revenue):
    return usd_revenue / 7 / 10000  # 汇率 1:7
```

---

## 三、地域与影院数据

### 3.1 地域覆盖

| 区域 | 省份数 | 城市数 |
|------|-------|-------|
| 直辖市 | 4 | 14 |
| 华东 | 5 | 15 |
| 华南 | 3 | 9 |
| 华中 | 4 | 11 |
| 华北 | 3 | 7 |
| 西南 | 4 | 8 |
| 西北 | 5 | 7 |
| 东北 | 3 | 8 |
| **总计** | **31** | **~80** |

### 3.2 影院品牌（40个）

| 档次 | 品牌 |
|------|------|
| 高端 (high) | 万达影城、CGV影城、博纳国际影城、UME影城、中影国际影城、耀莱成龙国际影城 |
| 中端 (mid) | 大地影院、金逸影城、横店电影城、上影影城、星美国际影城、保利万和电影院等 |
| 艺术 (art) | 百老汇电影中心、卢米埃影城、美亚影城、星光国际影城、新天地国际影城 |
| 基础 (basic) | 今世界国际影城、博悦影城、银河电影院、百花电影院、大众影剧院 |

### 3.3 影院分布规划

| 城市等级 | 示例城市 | 影院数量 |
|---------|---------|---------|
| 一线城市 | 北京、上海、广州、深圳 | 各15家 |
| 新一线 | 成都、杭州、武汉、西安等 | 各8-10家 |
| 二线 | 宁波、青岛、郑州、无锡等 | 各5-7家 |
| 三线 | 温州、绍兴、洛阳等 | 各3-4家 |
| 其他 | 各地级市 | 各2-3家 |

---

## 四、票房记录生成策略

### 4.1 衰减模型

```python
# 票房衰减公式：每周衰减 15%
decay_factor = 0.85 ** (days_since_release / 7)

# 周末加成：票房 × 1.3
weekend_boost = 1.3 if is_weekend else 1.0

# 当日票房 = 总票房 × 衰减系数 × 周末加成
daily_box_office = total_box_office × decay_factor × weekend_boost
```

### 4.2 影院分配

| 电影热度 | 上映影院数 | 说明 |
|---------|-----------|------|
| popularity > 50 | 8-15家 | 高热度电影 |
| popularity > 20 | 4-8家 | 中等热度 |
| popularity ≤ 20 | 1-3家 | 低热度电影 |

### 4.3 场次与人次计算

```python
# 场次 = 影院屏幕数 × 0.6 × 周末系数 × 票房系数
screening_count = cinema.screen_count × 0.6 × weekend_mult × amount_mult

# 人次 = 当日票房 ÷ 平均票价(35-45元)
audience_count = daily_box_office / avg_ticket_price
```

---

## 五、文件结构

```
backend/
├── scripts/
│   └── data_utils.py                     # 公共数据处理工具
├── movies/
│   └── management/commands/
│       └── import_movies.py             # 导入影片和类型
├── cinemas/
│   └── management/commands/
│       └── import_cinemas.py            # 导入影院和地域
├── boxoffice/
│   └── management/commands/
│       └── generate_boxoffice.py        # 生成票房记录
└── management/commands/
    └── import_all.py                   # 一键执行所有导入
```

---

## 六、执行方式

### 6.1 一键导入（推荐）

```bash
# 默认配置（200家影院）
python manage.py import_all

# 自定义影院数量
python manage.py import_all --cinema-count 300

# 自定义票房日期范围
python manage.py import_all --start-date 2020-01-01 --end-date 2025-12-31
```

### 6.2 分步执行

```bash
# 步骤1: 导入电影
python manage.py import_movies

# 步骤2: 导入影院和地域
python manage.py import_cinemas --cinema-count 200

# 步骤3: 生成票房记录
python manage.py generate_boxoffice
```

---

## 七、预期结果

| 数据类型 | 预期数量 |
|---------|---------|
| 影片类型 | ~20 个 |
| 影片 | 4,803+ 部 |
| 地域 | ~100 个 |
| 影院 | 200 家 |
| 票房记录 | 数十万条 |

---

## 八、扩展模型字段（可选）

如需存储更多 metadata 信息，可在 Movie 模型中新增：

```python
'original_title': 'CharField',      # 原始标题
'popularity': 'FloatField',          # 热度评分
'rating': 'FloatField',              # 用户评分 (0-10)
'rating_count': 'IntegerField',      # 评分人数
'imdb_id': 'CharField',            # IMDb ID
'homepage': 'CharField',           # 官网链接
'original_language': 'CharField',  # 原始语言代码
'language_name': 'CharField',       # 语言中文名
'spoken_languages': 'TextField',   # 对白语言
'is_series': 'BooleanField',        # 是否系列电影
'collection_name': 'CharField',    # 系列名称
'has_trailer': 'BooleanField',     # 是否有预告片
```
