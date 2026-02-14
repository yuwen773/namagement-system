# 景点图片批量添加实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标：** 为数据库中 3700 个景点添加封面图和轮播图，包括 12 个精确匹配景点和其余按类别分配的景点。

**架构方案：** 创建 Django management command，读取 images_config.py 精确匹配配置 + 类别默认图片配置，遍历景点并批量更新 cover_image 和 images 字段。

**技术栈：** Django ORM, management commands, Unsplash 图片

---

## 任务 1: 创建类别图片配置

**文件：**
- 修改: `backend/attractions/images_config.py`

**步骤 1: 添加类别默认图片配置**

在 `ATTRACTION_IMAGES` 字典后添加类别配置：

```python
# 类别默认图片配置
CATEGORY_DEFAULT_IMAGES = {
    "自然风光": {
        "cover": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200&q=80",
            "https://images.unsplash.com/photo-1518173946687-a4c036bc1e3e?w=1200&q=80",
        ],
    },
    "人文古迹": {
        "cover": "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=1200&q=80",
            "https://images.unsplash.com/photo-1599658880436-c61792e70672?w=1200&q=80",
            "https://images.unsplash.com/photo-1529686734068-64bdda8ad66c?w=1200&q=80",
            "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
        ],
    },
    "主题乐园": {
        "cover": "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=1200&q=80",
            "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&q=80",
            "https://images.unsplash.com/photo-1533114876105-5fe5019509d8?w=1200&q=80",
            "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=1200&q=80",
        ],
    },
    "海滩": {
        "cover": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1200&q=80",
            "https://images.unsplash.com/photo-1506953823976-52e1fdc0149a?w=1200&q=80",
            "https://images.unsplash.com/photo-1473116763241-2e4a44daa1fa?w=1200&q=80",
        ],
    },
    "其他": {
        "cover": "https://images.unsplash.com/photo-1473116763241-2e4a44daa1fa?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1473116763241-2e4a44daa1fa?w=1200&q=80",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
            "https://images.unsplash.com/photo-1518173946687-a4c036bc1e3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
        ],
    },
}
```

**步骤 2: 添加获取类别图片的函数**

```python
def get_category_default_images(category: str) -> dict:
    """获取类别默认图片"""
    # 处理类别名称映射
    category_map = {
        "自然风光": "自然风光",
        "人文古迹": "人文古迹",
        "主题乐园": "主题乐园",
        "海滩": "海滩",
        "海滩/海滨": "海滩",
        "其他": "其他",
    }
    mapped = category_map.get(category, "其他")
    return CATEGORY_DEFAULT_IMAGES.get(mapped, CATEGORY_DEFAULT_IMAGES["其他"])
```

**步骤 3: 提交代码**

```bash
git add backend/attractions/images_config.py
git commit -m "feat: 添加景点类别默认图片配置"
```

---

## 任务 2: 创建 update_attraction_images 命令

**文件：**
- 创建: `backend/attractions/management/commands/update_attraction_images.py`

**步骤 1: 创建命令文件**

```python
"""
景点图片批量更新命令

用法: python manage.py update_attraction_images [--dry-run]
"""
from django.core.management.base import BaseCommand
from attractions.models import Attraction
from attractions.images_config import (
    ATTRACTION_IMAGES,
    CATEGORY_DEFAULT_IMAGES,
    get_category_default_images
)


class Command(BaseCommand):
    help = '批量更新景点图片'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅预览不实际更新',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # 获取所有未删除的景点
        attractions = Attraction.objects.filter(is_deleted=False)
        total = attractions.count()

        self.stdout.write(f'共找到 {total} 个景点')

        updated_count = 0
        skipped_count = 0

        for attraction in attractions:
            name = attraction.name
            category = attraction.category

            # 1. 尝试精确匹配
            if name in ATTRACTION_IMAGES:
                images = ATTRACTION_IMAGES[name]
                cover_image = images.get('cover')
                gallery = images.get('gallery', [])
                match_type = '精确匹配'
            else:
                # 2. 使用类别默认图
                images = get_category_default_images(category)
                cover_image = images.get('cover')
                gallery = images.get('gallery', [])
                match_type = f'类别: {category}'

            if dry_run:
                self.stdout.write(
                    f'[DRY-RUN] {name}: {match_type} -> {cover_image}'
                )
                skipped_count += 1
            else:
                attraction.cover_image = cover_image
                attraction.images = gallery
                attraction.save(update_fields=['cover_image', 'images'])
                updated_count += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'\n[DRY-RUN] 共 {skipped_count} 个景点待更新')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n成功更新 {updated_count} 个景点')
            )
```

**步骤 2: 测试命令帮助**

```bash
cd backend
python manage.py update_attraction_images --help
```

预期输出：
```
usage: manage.py update_attraction_images [-h] [--dry-run]
...
```

**步骤 3: 提交代码**

```bash
git add backend/attractions/management/commands/update_attraction_images.py
git commit -m "feat: 添加景点图片批量更新命令"
```

---

## 任务 3: 执行命令并验证

**步骤 1: 先运行 dry-run 预览**

```bash
cd backend
python manage.py update_attraction_images --dry-run
```

预期：输出前 20 个景点的匹配情况

**步骤 2: 执行实际更新**

```bash
cd backend
python manage.py update_attraction_images
```

预期输出：`成功更新 3700 个景点`

**步骤 3: 验证结果**

```bash
cd backend
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist.settings')
django.setup()

from attractions.models import Attraction
# 抽查精确匹配的景点
for name in ['故宫', '长城', '西湖', '黄山']:
    a = Attraction.objects.get(name=name, is_deleted=False)
    print(f'{name}: {a.cover_image[:50]}...')

# 抽查类别匹配的景点
a = Attraction.objects.filter(category='自然风光', is_deleted=False).first()
print(f'自然风光示例: {a.name} -> {a.cover_image[:50]}...')
"
```

**步骤 4: 测试 API**

访问 http://127.0.0.1:8123/api/attractions/ 验证图片 URL 返回正常

**步骤 5: 提交完成**

```bash
git add -A
git commit -m "feat: 批量更新景点封面图和轮播图"
```

---

## 总结

| 任务 | 描述 |
|------|------|
| 1 | 添加类别默认图片配置到 images_config.py |
| 2 | 创建 update_attraction_images 命令 |
| 3 | 执行命令并验证结果 |

执行完成后，所有 3700 个景点将拥有封面图和 4 张轮播图。
