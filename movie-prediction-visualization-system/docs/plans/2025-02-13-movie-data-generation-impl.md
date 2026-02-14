# 电影数据批量生成实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为电影票房预测系统生成5000+部电影、80家影院及约100万条票房记录，确保预测功能可用。

**Architecture:** 使用Django management command批量生成数据，利用bulk_create提高性能，数据按合理规则分布以模拟真实场景。

**Tech Stack:** Django management command, Faker, random, bulk_create批量插入

---

## 任务概览

| 任务 | 说明 |
|-----|------|
| Task 1 | 创建数据生成工具模块 (data_generator.py) |
| Task 2 | 创建电影生成management command |
| Task 3 | 生成电影数据（5000+部） |
| Task 4 | 创建票房数据生成management command |
| Task 5 | 生成票房记录（约100万条） |
| Task 6 | 验证数据完整性和预测功能 |

---

### Task 1: 创建数据生成工具模块

**Files:**
- Create: `backend/scripts/data_generator.py`

**Step 1: 创建工具模块**

```python
# backend/scripts/data_generator.py
"""数据生成工具模块"""

import random
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker('zh_CN')

# 电影类型及权重
MOVIE_TYPES = [
    ('动作', 0.20),
    ('喜剧', 0.18),
    ('爱情', 0.15),
    ('科幻', 0.12),
    ('悬疑', 0.10),
    ('恐怖', 0.08),
    ('动画', 0.07),
    ('剧情', 0.05),
    ('战争', 0.03),
    ('惊悚', 0.02),
]

# 类型对应的片长范围（分钟）
TYPE_DURATION = {
    '动作': (90, 150),
    '喜剧': (80, 120),
    '爱情': (90, 130),
    '科幻': (100, 180),
    '悬疑': (90, 140),
    '恐怖': (75, 110),
    '动画': (70, 130),
    '剧情': (90, 150),
    '战争': (100, 180),
    '惊悚': (85, 120),
}

# 类型对应的票房范围（万元）
TYPE_BOXOFFICE = {
    '动作': (500, 50000),
    '喜剧': (300, 30000),
    '爱情': (200, 25000),
    '科幻': (1000, 80000),
    '悬疑': (300, 20000),
    '恐怖': (100, 15000),
    '动画': (500, 40000),
    '剧情': (100, 20000),
    '战争': (800, 60000),
    '惊悚': (200, 18000),
}

# 热门词汇
MOVIE_PREFIXES = ['超能', '星际', '传奇', '王者', '风暴', '联盟', '特工', '追凶', '末日', '重生',
                  '速度与激情', '流浪地球', '复仇者', '变形金刚', '蜘蛛侠', ' Batman', ' X战警',
                  '疯狂', '开心', '囧途', '大闹', '疯狂动物', '哪吒', '姜子牙', '熊出没']
MOVIE_WORDS = ['宇宙', '地球', '黎明', '黄昏', '之夜', '归来', '崛起', '终极', '决战', '起源',
               '行者', '飞驰', '狂潮', '烈焰', '冰霜', '雷霆', '风暴', '深海', '苍穹', '都市',
               '乡村', '校园', '职场', '商场', '战场', '沙场', '剧场', '赌场', '坟场', '刑场']
MOVIE_SUFFIXES = ['联盟', '宇宙', '传奇', '英雄', '崛起', '归来', '终结', '重生', '破晓', '逆袭',
                  '之恋', '之战', '之旅', '之路', '风云', '风暴', '狂欢', '谜案', '疑云', '真相']

# 导演/演员姓名库
DIRECTORS = ['张艺谋', '陈凯歌', '冯小刚', '姜文', '周星驰', '徐克', '吴京', '黄渤', '沈腾', '韩寒',
             '宁浩', '管虎', '陆川', '贾樟柯', '娄烨', '王小帅', '李安', '吴宇森', '周星驰', '王家卫',
             '克里斯托弗·诺兰', '詹姆斯·卡梅隆', '史蒂文·斯皮尔伯格', '马丁·斯科塞斯', '昆汀·塔伦蒂诺']
ACTORS = ['吴京', '沈腾', '黄渤', '徐峥', '邓超', '周星驰', '王宝强', '刘昊然', '易烊千玺', '王千源',
          '胡歌', '张译', '张涵予', '梁朝伟', '周润发', '成龙', '李连杰', '甄子丹', '赵又廷', '彭于晏',
          '马丽', '贾玲', '张小斐', '周冬雨', '刘亦菲', '杨幂', '赵丽颖', '杨紫', '迪丽热巴', 'Angelababy']


def generate_movie_title():
    """生成随机电影名称"""
    if random.random() < 0.3:
        # 英文+中文组合
        return f"{random.choice(MOVIE_PREFIXES)}: {fake.word().upper()}{random.choice(MOVIE_SUFFIXES)}"
    else:
        return f"{random.choice(MOVIE_PREFIXES)}{random.choice(MOVIE_WORDS)}{random.choice(MOVIE_SUFFIXES)}"


def select_movie_type():
    """根据权重选择电影类型"""
    types, weights = zip(*MOVIE_TYPES)
    return random.choices(types, weights=weights, k=1)[0]


def generate_movie_data(release_date):
    """生成单部电影的完整数据"""
    movie_type = select_movie_type()

    # 片长
    min_dur, max_dur = TYPE_DURATION.get(movie_type, (90, 120))
    duration = random.randint(min_dur, max_dur)

    # 票房（根据上映时间调整）
    min_bo, max_bo = TYPE_BOXOFFICE.get(movie_type, (100, 10000))
    # 周末/节假日上映的票房更高
    if release_date.weekday() in [4, 5, 6]:  # 周五周六周日
        min_bo *= 1.5
        max_bo *= 1.5
    # 暑期/贺岁档更高
    if release_date.month in [7, 8, 12, 1]:
        min_bo *= 1.3
        max_bo *= 1.3

    box_office_total = random.uniform(min_bo, max_bo)

    return {
        'title': generate_movie_title(),
        'director': random.choice(DIRECTORS) if random.random() > 0.3 else None,
        'actors': ', '.join(random.sample(ACTORS, random.randint(1, 5))),
        'release_date': release_date,
        'duration': duration,
        'type_name': movie_type,
        'box_office_total': round(box_office_total, 2),
    }


def get_release_dates(count, start_date, end_date):
    """生成均匀分布的上映日期"""
    delta = (end_date - start_date).days
    return [start_date + timedelta(days=random.randint(0, delta)) for _ in range(count)]


def decay_factor(day):
    """票房衰减系数（每周约15%衰减）"""
    return 0.85 ** (day / 7)
```

**Step 2: 验证模块可导入**

Run: `cd backend && python -c "from scripts.data_generator import *; print(generate_movie_title())"`
Expected: 输出随机生成的电影名称

---

### Task 2: 创建电影生成management command

**Files:**
- Modify: `backend/movies/management/commands/__init__.py` (确认存在)
- Create: `backend/movies/management/commands/generate_movies.py`

**Step 1: 创建command文件**

```python
# backend/movies/management/commands/generate_movies.py
from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
scripts_dir = os.path.join(backend_dir, 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from data_generator import *


class Command(BaseCommand):
    help = '生成电影数据（5000+部，2025-2026年）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5000,
            help='生成电影数量'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            default='2025-01-01',
            help='上映开始日期'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2026-12-31',
            help='上映结束日期'
        )

    def handle(self, *args, **options):
        from movies.models import Movie, MovieType

        count = options['count']
        start_date = date.fromisoformat(options['start_date'])
        end_date = date.fromisoformat(options['end_date'])

        self.stdout.write(self.style.HTTP_INFO(f"开始生成 {count} 部电影..."))

        # 确保电影类型存在
        self.ensure_movie_types()

        # 生成上映日期（均匀分布）
        release_dates = get_release_dates(count, start_date, end_date)

        # 获取类型映射
        genre_map = {g.name: g for g in MovieType.objects.all()}

        # 批量创建电影
        movies_to_create = []
        existing_titles = set(Movie.objects.values_list('title', flat=True))

        for i, release_date in enumerate(release_dates):
            # 生成电影数据
            movie_data = generate_movie_data(release_date)

            # 检查是否重复
            if movie_data['title'] in existing_titles:
                # 生成新的
                movie_data['title'] = f"{movie_data['title']} {random.randint(1,999)}"

            existing_titles.add(movie_data['title'])

            movies_to_create.append(Movie(
                title=movie_data['title'],
                director=movie_data['director'],
                actors=movie_data['actors'],
                release_date=movie_data['release_date'],
                duration=movie_data['duration'],
                type=genre_map.get(movie_data['type_name']),
                box_office_total=movie_data['box_office_total'],
                status='RELEASED',
            ))

            if (i + 1) % 500 == 0:
                Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)
                self.stdout.write(f"已生成 {i + 1} 部电影...")
                movies_to_create = []
                existing_titles = set(Movie.objects.values_list('title', flat=True))

        # 插入剩余
        if movies_to_create:
            Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)

        total = Movie.objects.count()
        self.stdout.write(self.style.SUCCESS(f"电影生成完成！共 {total} 部"))

    def ensure_movie_types(self):
        """确保电影类型存在"""
        from movies.models import MovieType

        types = [t[0] for t in MOVIE_TYPES]
        for t in types:
            MovieType.objects.get_or_create(name=t)

        self.stdout.write(f"电影类型已准备: {len(types)} 个")
```

**Step 2: 测试command帮助**

Run: `cd backend && python manage.py generate_movies --help`
Expected: 显示帮助信息

---

### Task 3: 生成电影数据（5000+部）

**Step 1: 执行生成命令**

Run: `cd backend && python manage.py generate_movies --count=5000`
Expected: 输出生成进度，最终显示完成

**Step 2: 验证数据**

Run: `cd backend && python -c "from movies.models import Movie; print(f'电影总数: {Movie.objects.count()}')"`
Expected: 约5000

**Step 3: 提交**

```bash
git add backend/scripts/data_generator.py backend/movies/management/commands/generate_movies.py
git commit -m "feat: 添加电影数据生成功能，生成5000+部电影"
```

---

### Task 4: 创建票房数据生成management command

**Files:**
- Create: `backend/boxoffice/management/commands/generate_boxoffice_2025.py`

**Step 1: 创建command**

```python
# backend/boxoffice/management/commands/generate_boxoffice_2025.py
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
from decimal import Decimal
import random
from boxoffice.models import BoxOfficeRecord


class Command(BaseCommand):
    help = '生成2024-2026年票房记录数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            default='2024-12-01',
            help='票房记录开始日期'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2026-12-31',
            help='票房记录结束日期'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2000,
            help='批量插入大小'
        )

    def handle(self, *args, **options):
        from movies.models import Movie
        from cinemas.models import Cinema

        start_date = date.fromisoformat(options['start_date'])
        end_date = date.fromisoformat(options['end_date'])
        batch_size = options['batch_size']

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
            if stats['movies_processed'] % 500 == 0:
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

        # 上映前预热期（30-60天）
        pre_heat_days = random.randint(30, 60)
        # 上映后放映期（30-90天）
        show_days = random.randint(30, 90)

        # 确定电影实际上映期间
        movie_release = movie.release_date if movie.release_date else start_date

        # 预热期：从 start_date 或 上映前60天 开始
        pre_heat_start = max(start_date, movie_release - timedelta(days=pre_heat_days))
        pre_heat_end = movie_release - timedelta(days=1) if movie_release > start_date else start_date - timedelta(days=1)

        # 放映期：从上映日开始
        show_start = movie_release
        show_end = min(movie_release + timedelta(days=show_days), end_date)

        # 生成预热期数据（热度递增）
        if pre_heat_start <= pre_heat_end:
            for day_offset in range((pre_heat_end - pre_heat_start).days + 1):
                current_date = pre_heat_start + timedelta(days=day_offset)
                if current_date < start_date or current_date > end_date:
                    continue

                # 热度递增
                heat_ratio = (day_offset + 1) / pre_heat_days
                daily_heat = int(float(total_box_office_yuan) * 0.001 * heat_ratio)  # 预热期票房很低

                if daily_heat > 0:
                    selected_cinemas = random.sample(cinemas, min(random.randint(2, 5), len(cinemas)))
                    for cinema in selected_cinemas:
                        records.append(BoxOfficeRecord(
                            movie=movie,
                            cinema=cinema,
                            record_date=current_date,
                            daily_box_office=daily_heat // len(selected_cinemas),
                            screening_count=random.randint(1, 3),
                            audience_count=random.randint(10, 100)
                        ))

        # 生成上映期数据（首周高峰，后逐渐衰减）
        if show_start <= show_end:
            # 计算每日衰减系数总和
            show_days_count = (show_end - show_start).days + 1
            decay_sum = sum([self.decay_factor(i) for i in range(show_days_count)])

            current_day = 0
            current_date = show_start

            while current_date <= show_end:
                # 计算当日总票房
                daily_total = int(float(total_box_office_yuan) * self.decay_factor(current_day) / decay_sum)

                if daily_total > 0:
                    # 根据热度选择影院数量
                    if current_day < 7:  # 首周
                        num_cinemas = random.randint(10, 20)
                    elif current_day < 30:
                        num_cinemas = random.randint(6, 12)
                    else:
                        num_cinemas = random.randint(3, 8)

                    num_cinemas = min(num_cinemas, len(cinemas))

                    # 按座位数排序，优先选择大影院
                    sorted_cinemas = sorted(cinemas, key=lambda c: c.seats_count, reverse=True)
                    selected = sorted_cinemas[:num_cinemas]

                    # 分配票房
                    remaining = daily_total
                    for i, cinema in enumerate(selected):
                        if i == len(selected) - 1:
                            amount = remaining
                        else:
                            ratio = cinema.seats_count / sum(c.seats_count for c in selected)
                            amount = int(daily_total * ratio)
                            remaining -= amount

                        # 计算场次和人次
                        is_weekend = current_date.weekday() in [5, 6]
                        base_screenings = cinema.screen_count * 0.6
                        weekend_mult = 1.5 if is_weekend else 1.0
                        screenings = int(base_screenings * weekend_mult)
                        screenings = max(1, min(screenings, cinema.screen_count))

                        avg_price = random.uniform(35, 45)
                        audience = max(0, int(amount / avg_price))

                        records.append(BoxOfficeRecord(
                            movie=movie,
                            cinema=cinema,
                            record_date=current_date,
                            daily_box_office=amount,
                            screening_count=screenings,
                            audience_count=audience
                        ))

                current_date += timedelta(days=1)
                current_day += 1

        return records

    def decay_factor(self, day):
        """票房衰减系数"""
        return 0.85 ** (day / 7)  # 每周衰减15%
```

**Step 2: 测试command**

Run: `cd backend && python manage.py generate_boxoffice_2025 --help`
Expected: 显示帮助信息

---

### Task 5: 生成票房记录（约100万条）

**Step 1: 确保影院数据存在**

Run: `cd backend && python -c "from cinemas.models import Cinema; print(f'影院数量: {Cinema.objects.count()}')"`
Expected: 如果不足80家，先运行 `python manage.py import_cinemas --cinema-count=80`

**Step 2: 执行票房生成**

Run: `cd backend && python manage.py generate_boxoffice_2025`
Expected: 输出进度，最终显示完成，可能需要5-10分钟

**Step 3: 验证数据量**

Run: `cd backend && python -c "from boxoffice.models import BoxOfficeRecord; print(f'票房记录: {BoxOfficeRecord.objects.count()}')"`
Expected: 约100万条

**Step 4: 提交**

```bash
git add backend/boxoffice/management/commands/generate_boxoffice_2025.py
git commit -m "feat: 添加票房数据生成功能，支持2024-2026年数据"
```

---

### Task 6: 验证数据完整性和预测功能

**Step 1: 验证电影数据**

```python
from movies.models import Movie
print(f"电影总数: {Movie.objects.count()}")
print(f"2025年电影: {Movie.objects.filter(release_date__year=2025).count()}")
print(f"2026年电影: {Movie.objects.filter(release_date__year=2026).count()}")
```

**Step 2: 验证票房数据时间范围**

```python
from boxoffice.models import BoxOfficeRecord
from django.db.models import Min, Max
stats = BoxOfficeRecord.objects.aggregate(
    min_date=Min('record_date'),
    max_date=Max('record_date')
)
print(f"票房日期范围: {stats['min_date']} ~ {stats['max_date']}")
```

**Step 3: 测试预测功能**

Run: `cd backend && python -c "
from prediction.services import prediction_service
# 选一部有数据的电影测试
from movies.models import Movie
movie = Movie.objects.first()
result = prediction_service.linear_regression_predict(movie.id, 7)
print(f'预测成功: {result[\"success\"]}')
print(f'预测天数: {len(result[\"predictions\"])}')
print(f'历史数据天数: {len(result[\"history\"])}')
"`
Expected: 预测成功，有历史数据和预测结果

**Step 4: 最终提交**

```bash
git add .
git commit -m "feat: 完成5000+电影数据生成，票房记录约100万条"
```

---

## 执行选项

**Plan complete and saved to `docs/plans/2025-02-13-movie-data-generation-impl.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing_plans, batch execution with checkpoints

**Which approach?**
