# 电影票房预测与可视化系统 - 数据集评估报告

## 一、系统数据库表结构概览

根据 backend/movies/models.py, cinemas/models.py, boxoffice/models.py 分析：

### 1. movie_types (影片类型表)
- **name**: 类型名称
- **示例**: 动作、科幻、爱情
- **用途**: 电影分类管理

### 2. movies (影片表)
- **title**: 影片名称
- **director**: 导演
- **actors**: 主演
- **release_date**: 上映时间
- **duration**: 片长（分钟）
- **type_id**: 类型（外键）
- **poster_url**: 海报URL
- **description**: 简介
- **box_office_total**: 累计票房（万元）
- **status**: 状态（RELEASED/COMING/OFF）

### 3. regions (地域表 - 自关联)
- **name**: 地域名称
- **parent_id**: 父级地域ID
- **level**: 层级（PROVINCE/CITY）

### 4. cinemas (影院表)
- **name**: 影院名称
- **address**: 地址
- **phone**: 联系电话
- **region_id**: 所属区域（外键）
- **screen_count**: 屏幕数量
- **seats_count**: 座位数量
- **is_active**: 是否营业

### 5. boxoffice_records (票房记录表)
- **movie_id**: 影片ID（外键）
- **cinema_id**: 影院ID（外键）
- **record_date**: 记录日期
- **daily_box_office**: 当日票房（元）
- **screening_count**: 排片场次
- **audience_count**: 观影人次

---

## 二、数据集清单

### 1. tmdb_5000_movies.csv
- **文件大小**: 5.43 MB
- **记录数**: 4,803 条
- **格式**: CSV
- **主要字段**:
  - budget: 预算
  - genres: 类型（JSON格式）
  - id: 电影ID
  - original_language: 原始语言
  - original_title: 原始标题
  - overview: 简介
  - popularity: 人气度
  - release_date: 上映日期
  - revenue: 票房收入
  - runtime: 片长
  - status: 状态
  - title: 标题
  - vote_average: 评分
  - vote_count: 评分数

### 2. tmdb_5000_movies-1.csv
- **文件大小**: 5.43 MB
- **说明**: 与 tmdb_5000_movies.csv 完全重复

### 3. tmdb_5000_credits-1.csv
- **文件大小**: 38.19 MB
- **记录数**: 4,803 条
- **格式**: CSV
- **主要字段**:
  - movie_id: 电影ID
  - title: 标题
  - cast: 演员阵容（JSON格式，包含演员姓名、角色等信息）
  - crew: 制作团队（JSON格式，包含导演、编剧等）

### 4. movies_metadata.csv
- **文件大小**: 32.85 MB
- **记录数**: 45,466 条
- **格式**: CSV
- **主要字段**:
  - adult: 是否成人内容
  - belongs_to_collection: 所属系列
  - budget: 预算
  - genres: 类型（JSON格式）
  - homepage: 官网
  - id: 电影ID
  - imdb_id: IMDb ID
  - original_language: 原始语言
  - original_title: 原始标题
  - overview: 简介
  - popularity: 人气度
  - poster_path: 海报路径
  - production_companies: 制作公司（JSON格式）
  - production_countries: 制作国家（JSON格式）
  - release_date: 上映日期
  - revenue: 票房收入
  - runtime: 片长
  - spoken_languages: 语言（JSON格式）
  - status: 状态
  - tagline: 标语
  - title: 标题
  - video: 是否有视频
  - vote_average: 评分
  - vote_count: 评分数

### 5. ratings_small.csv
- **文件大小**: 2.33 MB
- **记录数**: 100,004 条
- **格式**: CSV
- **主要字段**:
  - userId: 用户ID
  - movieId: 电影ID
  - rating: 评分（0.5-5.0）
  - timestamp: 时间戳
- **唯一用户数**: 671
- **唯一电影数**: 9,066

---

## 三、各数据集可用性分析

### 1. tmdb_5000_movies.csv - 高可用性

**可以直接导入系统使用**

#### 字段映射关系：
| 数据集字段 | 系统字段 | 转换说明 |
|-----------|---------|---------|
| title | title | 直接映射 |
| release_date | release_date | 直接映射，需转换为Date类型 |
| runtime | duration | 直接映射，字段含义相同 |
| revenue | box_office_total | 需要单位转换（美元转万元人民币） |
| overview | description | 直接映射 |
| status | status | 需要映射值转换 |
| genres (JSON) | type_id | 需要解析JSON，提取类型名称 |
| - | poster_url | 需要从其他数据集获取 |
| - | director | 需要从credits数据集获取 |
| - | actors | 需要从credits数据集获取 |

#### 数据质量评估：
- ✅ release_date 完整度: 100%
- ✅ revenue 有数据占比: 70.3% (3,376/4,803)
- ✅ budget 有数据占比: 78.4% (3,766/4,803)
- ✅ runtime 缺失仅: 2条
- ✅ 数据范围: 1916-2017年，2000年后电影占72.7%

#### 推荐使用方案：
1. **直接导入 movies 表**: 使用 title, release_date, runtime, overview, status
2. **解析 genres**: 提取类型名称，导入 movie_types 表
3. **revenue 转换**: revenue (美元) ÷ 7 × 10000 = box_office_total (万元)

---

### 2. tmdb_5000_credits-1.csv - 高可用性

**需要字段映射后使用**

#### 字段映射关系：
| 数据集字段 | 系统字段 | 转换说明 |
|-----------|---------|---------|
| movie_id | - | 用于关联 movies 表 |
| title | title | 用于关联验证 |
| cast (JSON) | actors | 需要解析JSON，提取前3-5名演员 |
| crew (JSON) | director | 需要解析JSON，提取 job="Director" 的记录 |

#### 数据处理方法：
```python
# 解析 cast JSON，提取主演
cast_data = json.loads(cast_json)
actors = ', '.join([actor['name'] for actor in cast_data[:5]])

# 解析 crew JSON，提取导演
crew_data = json.loads(crew_json)
directors = [person['name'] for person in crew_data if person['job'] == 'Director']
director = ', '.join(directors)
```

#### 推荐使用方案：
1. **关联 tmdb_5000_movies.csv**: 使用 movie_id = id
2. **解析 JSON 数据**: 提取 director 和 actors
3. **更新 movies 表**: 将解析出的导演和主演信息补充到影片记录中

---

### 3. movies_metadata.csv - 高可用性

**需要清洗转换后使用**

#### 优势：
- 数据量大: 45,466 条记录（是 tmdb_5000 的9.5倍）
- 包含额外字段: poster_path, imdb_id, belongs_to_collection

#### 劣势：
- 数据质量参差不齐: budget, revenue 字段类型不一致
- 需要清洗: 部分记录的 revenue 和 budget 为 0 或空值

#### 推荐使用方案：
1. **数据清洗**:
   - 转换 budget, revenue 为数值类型
   - 过滤掉 revenue=0 的记录（或标记为待补充）
   - 处理 runtime 缺失值（263条）

2. **字段映射**:
   - poster_path: 可用于构建 poster_url（需要拼接 TMDb 图片基础URL）
   - imdb_id: 可作为外部引用

3. **使用建议**:
   - 优先使用 tmdb_5000_movies.csv（数据质量更高）
   - 将 movies_metadata.csv 作为补充数据源
   - 仅用于提取 poster_url 和 imdb_id 等额外信息

---

### 4. ratings_small.csv - 低可用性

**完全不适用当前系统**

#### 原因分析：
1. **数据类型不匹配**: 用户评分数据，系统需要的是票房数据
2. **业务逻辑不符**: 系统核心功能是票房预测，不是推荐系统
3. **字段无对应**: 无票房、排片场次、观影人次等核心字段

#### 可能的扩展用途：
- 未来如果添加"用户评价"或"推荐系统"功能，可以考虑使用
- 当前阶段建议暂不使用

---

### 5. tmdb_5000_movies-1.csv - 重复文件

**可以直接删除**

- 与 tmdb_5000_movies.csv 完全相同
- 建议保留原始文件，删除重复副本

---

## 四、数据集成方案

### 方案 A: 基础导入方案（推荐）

**适用场景**: 快速搭建系统，填充测试数据

**步骤**:
1. 导入 tmdb_5000_movies.csv 到 movies 表
2. 解析 genres，填充 movie_types 表
3. 使用 tmdb_5000_credits-1.csv 补充 director 和 actors

**优点**:
- 数据质量高
- 字段完整
- 实施简单

**缺点**:
- 影片数量有限（4,803部）
- 缺少 poster_url

---

### 方案 B: 扩展导入方案

**适用场景**: 需要更多数据和完整信息

**步骤**:
1. 执行方案A的所有步骤
2. 从 movies_metadata.csv 提取 poster_path，构建 poster_url
3. 过滤并导入 revenue > 0 的记录
4. 处理数据质量问题（缺失值、类型转换）

**优点**:
- 数据量更大
- 信息更完整

**缺点**:
- 需要额外的数据清洗工作
- 部分数据质量不佳

---

### 方案 C: 完整集成方案

**适用场景**: 生产环境，需要高质量数据

**步骤**:
1. 数据预处理脚本开发
   - JSON 解析（genres, cast, crew）
   - 数据类型转换
   - 缺失值处理
   - 单位转换（美元 → 人民币万元）

2. 数据验证
   - 检查必填字段完整性
   - 验证数据范围合理性
   - 处理异常值

3. 分阶段导入
   - 第一阶段: 导入 movie_types
   - 第二阶段: 导入 movies（基础信息）
   - 第三阶段: 补充 director, actors
   - 第四阶段: 更新 poster_url

**优点**:
- 数据质量最高
- 信息最完整
- 便于维护

**缺点**:
- 开发工作量大
- 需要测试验证

---

## 五、缺失数据处理建议

由于当前数据集缺少以下关键信息，建议：

### 1. cinemas（影院数据）
- **状态**: 无相关数据
- **建议**: 手动创建测试数据或从其他数据源获取
- **示例数据**:
  - 万达影城（北京）
  - 大地影院（上海）
  - 百老汇电影中心（深圳）

### 2. regions（地域数据）
- **状态**: 无相关数据
- **建议**: 导入中国行政区划数据
- **数据源**: 国家统计局行政区划代码

### 3. boxoffice_records（票房记录）
- **状态**: 数据集包含累计票房（revenue），但缺少按日期、按影院的明细数据
- **建议**:
  - 使用 revenue 作为 box_office_total（累计票房）
  - 生成模拟的每日票房数据（基于累计票房按时间分配）
  - 或从其他数据源获取真实日票房数据

---

## 六、数据导入脚本示例

```python
import pandas as pd
import json
from datetime import datetime
from decimal import Decimal

# 读取数据
movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
credits_df = pd.read_csv('data/tmdb_5000_credits-1.csv')

# 合并数据
merged_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id')

# 解析genres，提取类型
def extract_genres(genres_json):
    try:
        genres = json.loads(genres_json)
        return [g['name'] for g in genres]
    except:
        return []

merged_df['genre_list'] = merged_df['genres'].apply(extract_genres)

# 解析credits，提取导演和主演
def extract_crew(crew_json, job='Director'):
    try:
        crew = json.loads(crew_json)
        persons = [p['name'] for p in crew if p['job'] == job]
        return ', '.join(persons) if persons else None
    except:
        return None

def extract_cast(cast_json, limit=5):
    try:
        cast = json.loads(cast_json)
        actors = [a['name'] for a in cast[:limit]]
        return ', '.join(actors)
    except:
        return None

merged_df['director'] = merged_df['crew'].apply(lambda x: extract_crew(x, 'Director'))
merged_df['actors'] = merged_df['cast'].apply(lambda x: extract_cast(x, 5))

# 单位转换：美元转万元人民币
def convert_revenue(usd_revenue):
    if usd_revenue > 0:
        return round(usd_revenue / 7 * 0.0001, 2)  # 假设汇率1:7
    return 0

merged_df['box_office_total'] = merged_df['revenue'].apply(convert_revenue)

# 准备导入数据
import_data = merged_df[[
    'title', 'director', 'actors', 'release_date',
    'runtime', 'overview', 'box_office_total', 'status'
]].copy()

import_data.columns = [
    'title', 'director', 'actors', 'release_date',
    'duration', 'description', 'box_office_total', 'status'
]

# 导入数据库（使用Django ORM）
# from movies.models import Movie, MovieType
# for _, row in import_data.iterrows():
#     Movie.objects.create(**row.to_dict())
```

---

## 七、总结与建议

### 可直接使用的数据集：
1. ✅ **tmdb_5000_movies.csv** - 主要数据源，质量高
2. ✅ **tmdb_5000_credits-1.csv** - 补充导演和主演信息

### 需要清洗转换的数据集：
3. ⚠️ **movies_metadata.csv** - 作为补充，提取 poster_url 等额外信息

### 不适用的数据集：
4. ❌ **ratings_small.csv** - 用户评分数据，与票房预测无关
5. ❌ **tmdb_5000_movies-1.csv** - 重复文件

### 推荐实施步骤：
1. **第一阶段**: 导入 tmdb_5000_movies.csv 和 credits 数据
2. **第二阶段**: 手动补充 cinemas 和 regions 测试数据
3. **第三阶段**: 生成模拟的 boxoffice_records 数据
4. **第四阶段**（可选）: 从 movies_metadata.csv 提取 poster_url

### 数据质量注意事项：
- tmdb 数据集的票房单位为美元，需要转换为人民币万元
- revenue 为累计票房，不是每日票房，需要模拟生成时间序列数据
- genres, cast, crew 为 JSON 格式，需要解析处理
- 部分记录的 revenue 为 0，表示缺失票房数据

---

## 八、数据统计汇总

| 数据集 | 记录数 | 文件大小 | 可用性 | 主要用途 |
|-------|-------|---------|-------|---------|
| tmdb_5000_movies.csv | 4,803 | 5.43 MB | 高 | 影片基础数据 |
| tmdb_5000_credits-1.csv | 4,803 | 38.19 MB | 高 | 导演、演员信息 |
| movies_metadata.csv | 45,466 | 32.85 MB | 中 | 补充数据（poster等） |
| ratings_small.csv | 100,004 | 2.33 MB | 低 | 不适用 |
| tmdb_5000_movies-1.csv | 4,803 | 5.43 MB | 无 | 重复文件 |

**总可用数据量**: 4,803 部电影的完整信息
**总潜在数据量**: 45,466 部电影（需要清洗）
**核心数据文件**: tmdb_5000_movies.csv + tmdb_5000_credits-1.csv

---

*报告生成时间: 2026-02-12*
*数据集路径: D:\work\code\personal\namagement-system\movie-prediction-visualization-system\data*
