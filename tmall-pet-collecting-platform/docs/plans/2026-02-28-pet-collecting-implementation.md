# 天猫宠物用品数据采集系统改造实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将天猫潮玩数据采集系统改造为天猫宠物用品数据采集系统，保持技术架构不变，更换数据类目并扩展宠物特有的分析维度。

**Architecture:** 最小改动原则，最大程度复用现有代码：
1. 数据清理 - 清除潮玩商品数据
2. 模型迁移 - 添加 pet_type, pet_use 新字段
3. 爬虫配置 - 更新关键词为宠物用品
4. 后端统计 - 新增宠物类型/用途分析接口
5. 前端更新 - 改造页面标题、筛选器、统计卡片

**Tech Stack:** Django 5.2 + DRF, Vue 3 + Element Plus + ECharts, MySQL 8.0

---

## 任务总览

| 阶段 | 任务数 | 说明 |
|------|--------|------|
| 数据清理 | 1 | 清除现有潮玩商品数据 |
| 后端模型 | 2 | 添加字段、序列化器更新 |
| 爬虫配置 | 1 | 更新关键词 |
| 后端统计 | 2 | 添加新分析接口 |
| 前端 | 3 | Dashboard/Products/路由更新 |
| 测试验证 | 1 | 功能验证 |

---

## 阶段1: 数据清理

### Task 1: 清除潮玩商品数据

**Files:**
- Modify: `backend/products/models.py` - 无需修改，仅执行数据清理
- 执行命令清理数据库

**Step 1: 清理数据**

在MySQL中执行清理命令:

```sql
-- 清理商品表数据（保留结构）
TRUNCATE TABLE products;

-- 清理价格历史表
TRUNCATE TABLE price_history;

-- 清理采集日志表
TRUNCATE TABLE crawl_logs;
```

或者使用Django shell:
```bash
cd backend
python manage.py shell
```

```python
from products.models import Product, PriceHistory, CrawlLog
Product.objects.all().delete()
PriceHistory.objects.all().delete()
CrawlLog.objects.all().delete()
print("数据清理完成")
```

---

## 阶段2: 后端模型

### Task 2: 添加宠物类型和用途字段

**Files:**
- Modify: `backend/products/models.py:1-54`

**Step 1: 编辑 Product 模型添加新字段**

在 `Product` 类中添加:

```python
class Product(models.Model):
    """商品模型 - 存储天猫宠物用品数据"""

    # 新增字段定义（在 class Meta 之前）
    PET_TYPE_CHOICES = [
        ('cat', '猫咪'),
        ('dog', '狗狗'),
        ('aquatic', '水族'),
        ('small_pet', '小宠物'),
        ('other', '其他'),
    ]
    PET_USE_CHOICES = [
        ('food', '食品'),
        ('supplies', '用品'),
        ('toy', '玩具'),
        ('healthcare', '医疗保健'),
        ('grooming', '清洁护理'),
    ]

    # ... 现有字段 ...

    # 在 category 字段后添加新字段
    pet_type = models.CharField(
        max_length=20,
        choices=PET_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name='宠物类型'
    )
    pet_use = models.CharField(
        max_length=20,
        choices=PET_USE_CHOICES,
        null=True,
        blank=True,
        verbose_name='用途分类'
    )

    # ... 现有字段 ...
```

**Step 2: 更新 Meta 类注释**

```python
class Meta:
    db_table = 'products'
    verbose_name = '宠物商品'
    verbose_name_plural = '宠物商品'
    # ... 现有 indexes ...
    indexes = [
        # ... 现有索引 ...
        models.Index(fields=['pet_type']),
        models.Index(fields=['pet_use']),
    ]
```

**Step 3: 生成迁移文件**

```bash
cd backend
python manage.py makemigrations products --name add_pet_fields
```

**Step 4: 执行迁移**

```bash
python manage.py migrate products
```

**Step 5: 提交**

```bash
git add backend/products/models.py
git commit -m "feat: 添加宠物类型和用途字段到Product模型"
```

---

### Task 3: 更新序列化器支持新字段

**Files:**
- Modify: `backend/products/serializers.py`

**Step 1: 查看现有序列化器**

```bash
cat backend/products/serializers.py
```

**Step 2: 更新 ProductSerializer**

在序列化器中添加新字段:

```python
class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器"""

    class Meta:
        model = Product
        fields = [
            # ... 现有字段 ...
            'pet_type', 'pet_use',
            # ... 其他字段 ...
        ]
```

**Step 3: 提交**

```bash
git add backend/products/serializers.py
git commit -m "feat: 更新商品序列化器支持宠物类型和用途字段"
```

---

## 阶段3: 爬虫配置

### Task 4: 更新爬虫默认关键词

**Files:**
- Modify: `backend/crawler/config.py:27-36`

**Step 1: 更新 default_keywords**

将现有的潮玩关键词:

```python
default_keywords: List[str] = field(default_factory=lambda: [
    '高达模型',
    '盲盒',
    '手办',
    '潮玩',
    '泡泡玛特',
    '乐高',
    '变形金刚'
])
```

修改为宠物用品关键词:

```python
default_keywords: List[str] = field(default_factory=lambda: [
    '猫粮',
    '狗粮',
    '猫砂',
    '宠物零食',
    '宠物玩具',
    '宠物用品',
    '宠物窝',
    '宠物牵引绳',
    '宠物笼子',
    '宠物食具',
    '宠物自动饮水机',
    '宠物爬架',
    '猫爬架'
])
```

**Step 2: 更新爬虫名称（可选）**

```python
name: str = "pet_tmall_spider"  # 从 tmall_spider 改为 pet_tmall_spider
```

**Step 3: 提交**

```bash
git add backend/crawler/config.py
git commit -m "feat: 更新爬虫默认关键词为宠物用品"
```

---

## 阶段4: 后端统计分析

### Task 5: 添加宠物分析统计方法

**Files:**
- Modify: `backend/products/analytics.py`

**Step 1: 在 analytics.py 添加新方法**

在 `ProductAnalytics` 类中添加:

```python
def get_pet_type_distribution(self) -> list:
    """
    获取宠物类型分布统计

    Returns:
        宠物类型分布数据列表
    """
    products = self.products
    total = products.count()

    pet_types = dict(Product.PET_TYPE_CHOICES)
    data = []

    for pet_key, pet_label in pet_types:
        count = products.filter(pet_type=pet_key).count()
        percentage = count * 100 / total if total > 0 else 0

        data.append({
            'type': pet_key,
            'label': pet_label,
            'count': count,
            'percentage': round(percentage, 2)
        })

    return data


def get_pet_use_distribution(self) -> list:
    """
    获取用途分类分布统计

    Returns:
        用途分类分布数据列表
    """
    products = self.products
    total = products.count()

    pet_uses = dict(Product.PET_USE_CHOICES)
    data = []

    for use_key, use_label in pet_uses:
        count = products.filter(pet_use=use_key).count()
        percentage = count * 100 / total if total > 0 else 0

        data.append({
            'use': use_key,
            'label': use_label,
            'count': count,
            'percentage': round(percentage, 2)
        })

    return data
```

**Step 2: 提交**

```bash
git add backend/products/analytics.py
git commit -m "feat: 添加宠物类型和用途分布统计方法"
```

---

### Task 6: 添加宠物统计API视图

**Files:**
- Modify: `backend/products/statistics_views.py`

**Step 1: 添加新的API视图类**

在 `statistics_views.py` 末尾添加:

```python
class StatisticsPetTypeView(APIResponseMixin, APIView):
    """宠物类型分布统计"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取宠物类型分布"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        analytics = ProductAnalytics(queryset)
        data = analytics.get_pet_type_distribution()

        return self.success_response(data)


class StatisticsPetUseView(APIResponseMixin, APIView):
    """用途分类分布统计"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用途分类分布"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        analytics = ProductAnalytics(queryset)
        data = analytics.get_pet_use_distribution()

        return self.success_response(data)
```

**Step 2: 在 urls.py 注册新路由**

**Files:**
- Modify: `backend/products/urls.py`

添加:

```python
from . import views

# 在 urlpatterns 中添加
path('statistics/pet-type/', views.StatisticsPetTypeView.as_view(), name='statistics-pet-type'),
path('statistics/pet-use/', views.StatisticsPetUseView.as_view(), name='statistics-pet-use'),
```

**Step 3: 提交**

```bash
git add backend/products/statistics_views.py backend/products/urls.py
git commit -m "feat: 添加宠物类型和用途统计API视图"
```

---

## 阶段5: 前端更新

### Task 7: 更新前端API接口

**Files:**
- Modify: `frontend/src/api/index.js`

**Step 1: 更新 statisticsApi**

在 `statisticsApi` 中添加:

```javascript
export const statisticsApi = {
  // ... 现有方法 ...

  // 新增宠物统计接口
  getPetTypeDistribution: () => request.get('/products/statistics/pet-type/'),
  getPetUseDistribution: () => request.get('/products/statistics/pet-use/'),
}
```

**Step 2: 提交**

```bash
git add frontend/src/api/index.js
git commit -m "feat: 前端API添加宠物统计接口"
```

---

### Task 8: 更新前端Dashboard

**Files:**
- Modify: `frontend/src/views/admin/Dashboard.vue`

**Step 1: 更新页面标题和标签**

在模板中找到标题区域，修改为:

```vue
<h1 class="page-title">宠物用品数据概览</h1>
```

**Step 2: 添加宠物类型图表**

在 Dashboard 中添加新的图表配置:

```javascript
// 添加 petTypeChartOption 计算属性
const petTypeChartOption = computed(() => {
  if (!petTypeDistribution.value || petTypeDistribution.value.length === 0) {
    return null
  }

  return {
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', right: '5%', top: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['40%', '50%'],
      data: petTypeDistribution.value.map(item => ({
        name: item.label,
        value: item.count
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
})
```

**Step 3: 添加数据获取方法**

```javascript
const fetchPetTypeDistribution = async () => {
  try {
    const res = await statisticsApi.getPetTypeDistribution()
    if (res.code === 0) {
      petTypeDistribution.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch pet type distribution:', error)
  }
}
```

**Step 4: 在 onMounted 中调用**

```javascript
onMounted(async () => {
  await Promise.all([
    fetchOverview(),
    fetchPriceDistribution(),
    fetchShopRanking(),
    fetchSystemStatus(),
    fetchPetTypeDistribution()  // 新增
  ])
  loading.value = false
})
```

**Step 5: 提交**

```bash
git add frontend/src/views/admin/Dashboard.vue
git commit -m "feat: Dashboard添加宠物类型统计图表"
```

---

### Task 9: 更新前端页面标题和路由

**Files:**
- Modify: `frontend/src/views/admin/StatisticsDashboard.vue`
- Modify: `frontend/src/views/admin/Products.vue`
- Modify: `frontend/src/views/admin/Crawler.vue`
- Modify: `frontend/src/router/index.js` (如需更新路由meta)

**Step 1: 更新 StatisticsDashboard 标题**

在 StatisticsDashboard.vue 中找到页面标题，修改为:

```vue
<h1 class="page-title">宠物用品统计分析</h1>
```

**Step 2: 更新 Products 管理页标题**

在 Products.vue 中修改标题:

```vue
<h1 class="page-title">宠物商品管理</h1>
```

**Step 3: 更新 Crawler 页面标题**

在 Crawler.vue 中修改标题:

```vue
<h1 class="page-title">宠物数据采集</h1>
```

**Step 4: 提交**

```bash
git add frontend/src/views/admin/StatisticsDashboard.vue frontend/src/views/admin/Products.vue frontend/src/views/admin/Crawler.vue
git commit -m "feat: 更新前端页面标题为宠物用品相关"
```

---

## 阶段6: 测试验证

### Task 10: 功能验证

**Step 1: 启动后端服务**

```bash
cd backend
python manage.py runserver 8000
```

**Step 2: 启动前端服务**

```bash
cd frontend
npm run dev
```

**Step 3: 测试API接口**

```bash
# 测试宠物类型分布
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/products/statistics/pet-type/

# 测试用途分类分布
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/products/statistics/pet-use/
```

预期响应:

```json
{
  "code": 0,
  "data": [
    {"type": "cat", "label": "猫咪", "count": 0, "percentage": 0},
    {"type": "dog", "label": "狗狗", "count": 0, "percentage": 0},
    {"type": "aquatic", "label": "水族", "count": 0, "percentage": 0},
    {"type": "small_pet", "label": "小宠物", "count": 0, "percentage": 0},
    {"type": "other", "label": "其他", "count": 0, "percentage": 0}
  ]
}
```

**Step 4: 测试爬虫配置**

验证新关键词是否生效:

```bash
cd backend
python -c "from crawler.config import default_config; print(default_config.default_keywords)"
```

预期输出包含: `['猫粮', '狗粮', '猫砂', ...]`

**Step 5: 提交**

```bash
git add .
git commit -m "feat: 完成宠物用品数据采集系统改造"
```

---

## 执行顺序

1. 数据清理 (Task 1)
2. 后端模型修改 (Task 2-3)
3. 爬虫配置更新 (Task 4)
4. 后端统计分析 (Task 5-6)
5. 前端更新 (Task 7-9)
6. 测试验证 (Task 10)

---

## 预期产出

- 清除所有潮玩商品数据
- Product 模型新增 pet_type, pet_use 字段
- 爬虫默认关键词更换为宠物用品
- 新增宠物类型/用途分布统计API
- 前端页面标题和统计图表更新

---

## Plan complete

Two execution options:

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
