# 驾驶舱数据可视化重设计实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 重设计驾驶舱数据可视化，从3个图表扩展到6个图表，解决地图显示、类别重叠、数据维度单一等问题。

**Architecture:** 后端Django + DRF新增3个API接口；前端Vue3 + ECharts重构地图图表并新增3个图表组件。

**Tech Stack:** Django 5.2, DRF, Vue 3, ECharts 5, echarts-wordcloud, jieba

---

## 前置准备

### Task 0: 安装依赖

**Files:**
- Modify: `backend/requirements.txt`
- Modify: `frontend/package.json`

**Step 0.1: 后端添加 jieba 依赖**

编辑 `backend/requirements.txt`，在文件末尾添加：

```txt
jieba>=0.42.1
```

**Step 0.2: 安装后端依赖**

```bash
cd backend
pip install jieba
```

预期输出：Successfully installed jieba-0.42.x

**Step 0.3: 前端添加词云库依赖**

编辑 `frontend/package.json`，在 dependencies 中添加：

```json
"echarts-wordcloud": "^2.1.0"
```

**Step 0.4: 安装前端依赖**

```bash
cd frontend
npm install
```

预期输出：added 1 package

**Step 0.5: 提交依赖变更**

```bash
git add backend/requirements.txt frontend/package.json frontend/package-lock.json
git commit -m "chore: 添加 jieba 和 echarts-wordcloud 依赖"
```

---

## 阶段一：后端 API 开发

### Task 1: 时间趋势 API

**Files:**
- Modify: `backend/apps/dashboard/views.py`
- Test: `backend/apps/dashboard/tests/test_views.py`

**Step 1.1: 编写时间趋势测试**

编辑 `backend/apps/dashboard/tests/test_views.py`，在文件末尾添加：

```python
from django.utils.timezone import make_aware
from datetime import datetime
from apps.heritage.models import HeritageItem
from apps.categories.models import Category
from apps.regions.models import Region


class DashboardTrendViewTests(APITestCase):
    """时间趋势 API 测试"""

    def setUp(self):
        """创建测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # 创建测试用类别和地区
        self.category = Category.objects.create(
            name='测试类别',
            code='TEST',
            level='national'
        )
        self.region = Region.objects.create(
            country_code='CN',
            country_name='China',
            latitude=39.9,
            longitude=116.4
        )

        # 创建不同年份的非遗项目
        HeritageItem.objects.create(
            name='2008年项目',
            category=self.category,
            region=self.region,
            level='national',
            created_at=make_aware(datetime(2008, 6, 15))
        )
        HeritageItem.objects.create(
            name='2010年项目',
            category=self.category,
            region=self.region,
            level='national',
            created_at=make_aware(datetime(2010, 3, 20))
        )
        HeritageItem.objects.create(
            name='2010年项目2',
            category=self.category,
            region=self.region,
            level='national',
            created_at=make_aware(datetime(2010, 8, 10))
        )

    def test_trend_returns_yearly_counts(self):
        """测试返回按年份统计的数据"""
        response = self.client.get('/dashboard/trend/')
        self.assertEqual(response.status_code, 200)
        data = response.data['data']
        self.assertEqual(len(data), 2)

        # 验证数据结构
        self.assertIn('year', data[0])
        self.assertIn('count', data[0])

    def test_trend_ordered_by_year(self):
        """测试数据按年份排序"""
        response = self.client.get('/dashboard/trend/')
        data = response.data['data']
        years = [item['year'] for item in data]
        self.assertEqual(years, sorted(years))

    def test_trend_requires_auth(self):
        """测试需要认证"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/dashboard/trend/')
        self.assertEqual(response.status_code, 401)
```

**Step 1.2: 运行测试验证失败**

```bash
cd backend
python manage.py test apps.dashboard.tests.test_views.DashboardTrendViewTests -v 2
```

预期输出：FAIL (URL pattern not found or view not defined)

**Step 1.3: 实现时间趋势视图**

编辑 `backend/apps/dashboard/views.py`，在文件末尾添加：

```python
from django.db.models import Count
from django.db.models.functions import ExtractYear


class DashboardTrendView(APIView):
    """
    时间趋势 - 按年份统计新增项目
    GET /dashboard/trend/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 按年份分组统计
        queryset = (
            HeritageItem.objects
            .annotate(year=ExtractYear('created_at'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        data = [
            {
                'year': item['year'],
                'count': item['count']
            }
            for item in queryset
        ]

        return success_response(data=data, message="获取成功")
```

**Step 1.4: 注册 URL**

编辑 `backend/apps/dashboard/urls.py`：

修改导入部分：
```python
from .views import (
    DashboardCategoryDistributionView,
    DashboardCountryRankingView,
    DashboardMapDistributionView,
    DashboardOverviewView,
    DashboardTrendView,  # 新增
)
```

修改 urlpatterns：
```python
urlpatterns = [
    re_path(r"^dashboard/overview/?$", DashboardOverviewView.as_view(), name="dashboard-overview"),
    re_path(
        r"^dashboard/map-distribution/?$",
        DashboardMapDistributionView.as_view(),
        name="dashboard-map-distribution",
    ),
    re_path(
        r"^dashboard/category-distribution/?$",
        DashboardCategoryDistributionView.as_view(),
        name="dashboard-category-distribution",
    ),
    re_path(
        r"^dashboard/country-ranking/?$",
        DashboardCountryRankingView.as_view(),
        name="dashboard-country-ranking",
    ),
    re_path(r"^dashboard/trend/?$", DashboardTrendView.as_view(), name="dashboard-trend"),  # 新增
]
```

**Step 1.5: 运行测试验证通过**

```bash
cd backend
python manage.py test apps.dashboard.tests.test_views.DashboardTrendViewTests -v 2
```

预期输出：PASS (3 tests)

**Step 1.6: 提交**

```bash
git add backend/apps/dashboard/views.py backend/apps/dashboard/urls.py backend/apps/dashboard/tests/test_views.py
git commit -m "feat(dashboard): 添加时间趋势 API 接口

- 新增 DashboardTrendView 按年份统计非遗项目
- 支持 /dashboard/trend/ 端点
- 添加单元测试验证数据准确性和排序"
```

---

### Task 2: 保护级别分布 API

**Files:**
- Modify: `backend/apps/dashboard/views.py`
- Test: `backend/apps/dashboard/tests/test_views.py`

**Step 2.1: 编写保护级别测试**

编辑 `backend/apps/dashboard/tests/test_views.py`，在文件末尾添加：

```python
class DashboardLevelDistributionViewTests(APITestCase):
    """保护级别分布 API 测试"""

    def setUp(self):
        """创建测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name='测试类别',
            code='TEST',
            level='national'
        )
        self.region = Region.objects.create(
            country_code='CN',
            country_name='China',
            latitude=39.9,
            longitude=116.4
        )

        # 创建不同级别的项目
        HeritageItem.objects.create(
            name='国家级项目1',
            category=self.category,
            region=self.region,
            level='national'
        )
        HeritageItem.objects.create(
            name='国家级项目2',
            category=self.category,
            region=self.region,
            level='national'
        )
        HeritageItem.objects.create(
            name='省级项目',
            category=self.category,
            region=self.region,
            level='provincial'
        )
        HeritageItem.objects.create(
            name='县级项目',
            category=self.category,
            region=self.region,
            level='city_county'
        )

    def test_level_distribution_returns_all_levels(self):
        """测试返回所有保护级别"""
        response = self.client.get('/dashboard/level-distribution/')
        self.assertEqual(response.status_code, 200)
        data = response.data['data']
        self.assertEqual(len(data), 3)

    def test_level_distribution_counts_are_correct(self):
        """测试统计数据正确"""
        response = self.client.get('/dashboard/level-distribution/')
        data = response.data['data']

        level_counts = {item['level']: item['count'] for item in data}
        self.assertEqual(level_counts['national'], 2)
        self.assertEqual(level_counts['provincial'], 1)
        self.assertEqual(level_counts['city_county'], 1)

    def test_level_distribution_has_level_name(self):
        """测试返回级别中文名"""
        response = self.client.get('/dashboard/level-distribution/')
        data = response.data['data']

        self.assertIn('level_name', data[0])
```

**Step 2.2: 运行测试验证失败**

```bash
cd backend
python manage.py test apps.dashboard.tests.test_views.DashboardLevelDistributionViewTests.test_level_distribution_returns_all_levels -v 2
```

预期输出：FAIL (404 or endpoint not found)

**Step 2.3: 实现保护级别分布视图**

编辑 `backend/apps/dashboard/views.py`，在文件末尾添加：

```python
class DashboardLevelDistributionView(APIView):
    """
    保护级别分布
    GET /dashboard/level-distribution/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.heritage.models import HeritageItem

        level_choices_dict = dict(HeritageItem.LEVEL_CHOICES)

        data = []
        for level_value, level_name in HeritageItem.LEVEL_CHOICES:
            count = HeritageItem.objects.filter(level=level_value).count()
            data.append({
                'level': level_value,
                'level_name': level_name,
                'count': count
            })

        return success_response(data=data, message="获取成功")
```

**Step 2.4: 注册 URL**

编辑 `backend/apps/dashboard/urls.py`：

修改导入：
```python
from .views import (
    DashboardCategoryDistributionView,
    DashboardCountryRankingView,
    DashboardLevelDistributionView,  # 新增
    DashboardMapDistributionView,
    DashboardOverviewView,
    DashboardTrendView,
)
```

修改 urlpatterns：
```python
urlpatterns = [
    re_path(r"^dashboard/overview/?$", DashboardOverviewView.as_view(), name="dashboard-overview"),
    re_path(
        r"^dashboard/map-distribution/?$",
        DashboardMapDistributionView.as_view(),
        name="dashboard-map-distribution",
    ),
    re_path(
        r"^dashboard/category-distribution/?$",
        DashboardCategoryDistributionView.as_view(),
        name="dashboard-category-distribution",
    ),
    re_path(
        r"^dashboard/country-ranking/?$",
        DashboardCountryRankingView.as_view(),
        name="dashboard-country-ranking",
    ),
    re_path(
        r"^dashboard/trend/?$",
        DashboardTrendView.as_view(),
        name="dashboard-trend",
    ),
    re_path(
        r"^dashboard/level-distribution/?$",
        DashboardLevelDistributionView.as_view(),
        name="dashboard-level-distribution",
    ),
]
```

**Step 2.5: 运行测试验证通过**

```bash
cd backend
python manage.py test apps.dashboard.tests.test_views.DashboardLevelDistributionViewTests -v 2
```

预期输出：PASS (3 tests)

**Step 2.6: 提交**

```bash
git add backend/apps/dashboard/views.py backend/apps/dashboard/urls.py backend/apps/dashboard/tests/test_views.py
git commit -m "feat(dashboard): 添加保护级别分布 API 接口

- 新增 DashboardLevelDistributionView 统计各级别项目数
- 支持 /dashboard/level-distribution/ 端点
- 添加单元测试验证统计数据正确性"
```

---

### Task 3: 关键词词云 API

**Files:**
- Modify: `backend/apps/dashboard/views.py`
- Test: `backend/apps/dashboard/tests/test_views.py`

**Step 3.1: 编写关键词词云测试**

编辑 `backend/apps/dashboard/tests/test_views.py`，在文件末尾添加：

```python
class DashboardKeywordCloudViewTests(APITestCase):
    """关键词词云 API 测试"""

    def setUp(self):
        """创建测试数据"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name='传统技艺',
            code='CRAFT',
            level='national'
        )
        self.region = Region.objects.create(
            country_code='CN',
            country_name='China',
            latitude=39.9,
            longitude=116.4
        )

        # 创建包含重复关键词的项目
        HeritageItem.objects.create(
            name='剪纸艺术',
            category=self.category,
            region=self.region,
            level='national'
        )
        HeritageItem.objects.create(
            name='传统剪纸',
            category=self.category,
            region=self.region,
            level='national'
        )
        HeritageItem.objects.create(
            name='刺绣技艺',
            category=self.category,
            region=self.region,
            level='national'
        )

    def test_keyword_cloud_returns_word_counts(self):
        """测试返回词频统计"""
        response = self.client.get('/dashboard/keyword-cloud/')
        self.assertEqual(response.status_code, 200)
        data = response.data['data']

        # 验证数据结构
        self.assertIn('name', data[0])
        self.assertIn('value', data[0])

    def test_keyword_cloud_counts_correctly(self):
        """测试词频统计正确"""
        response = self.client.get('/dashboard/keyword-cloud/')
        data = response.data['data']

        word_counts = {item['name']: item['value'] for item in data}
        self.assertEqual(word_counts.get('剪纸'), 2)
        self.assertEqual(word_counts.get('技艺'), 2)

    def test_keyword_cloud_limits_results(self):
        """测试结果限制在100个"""
        response = self.client.get('/dashboard/keyword-cloud/')
        data = response.data['data']
        self.assertLessEqual(len(data), 100)
```

**Step 3.2: 运行测试验证失败**

```bash
cd backend
python manage.py test apps.dashboard.tests.test_views.DashboardKeywordCloudViewTests.test_keyword_cloud_returns_word_counts -v 2
```

预期输出：FAIL (404)

**Step 3.3: 实现关键词词云视图**

编辑 `backend/apps/dashboard/views.py`，在文件顶部添加导入：

```python
import jieba
```

在文件末尾添加：

```python
class DashboardKeywordCloudView(APIView):
    """
    关键词词云
    GET /dashboard/keyword-cloud/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取所有非遗项目名称
        names = HeritageItem.objects.values_list('name', flat=True)

        # 分词统计
        word_count = {}
        for name in names:
            words = jieba.cut(name)
            for word in words:
                if len(word) >= 2:  # 过滤单字
                    word_count[word] = word_count.get(word, 0) + 1

        # 按词频排序，取前100
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:100]

        data = [{'name': word, 'value': count} for word, count in sorted_words]

        return success_response(data=data, message="获取成功")
```

**Step 3.4: 注册 URL**

编辑 `backend/apps/dashboard/urls.py`：

修改导入：
```python
from .views import (
    DashboardCategoryDistributionView,
    DashboardCountryRankingView,
    DashboardKeywordCloudView,  # 新增
    DashboardLevelDistributionView,
    DashboardMapDistributionView,
    DashboardOverviewView,
    DashboardTrendView,
)
```

修改 urlpatterns：
```python
urlpatterns = [
    re_path(r"^dashboard/overview/?$", DashboardOverviewView.as_view(), name="dashboard-overview"),
    re_path(
        r"^dashboard/map-distribution/?$",
        DashboardMapDistributionView.as_view(),
        name="dashboard-map-distribution",
    ),
    re_path(
        r"^dashboard/category-distribution/?$",
        DashboardCategoryDistributionView.as_view(),
        name="dashboard-category-distribution",
    ),
    re_path(
        r"^dashboard/country-ranking/?$",
        DashboardCountryRankingView.as_view(),
        name="dashboard-country-ranking",
    ),
    re_path(
        r"^dashboard/trend/?$",
        DashboardTrendView.as_view(),
        name="dashboard-trend",
    ),
    re_path(
        r"^dashboard/level-distribution/?$",
        DashboardLevelDistributionView.as_view(),
        name="dashboard-level-distribution",
    ),
    re_path(
        r"^dashboard/keyword-cloud/?$",
        DashboardKeywordCloudView.as_view(),
        name="dashboard-keyword-cloud",
    ),
]
```

**Step 3.5: 运行测试验证通过**

```bash
cd backend
python manage.py test apps.dashboard.tests.test_views.DashboardKeywordCloudViewTests -v 2
```

预期输出：PASS (3 tests)

**Step 3.6: 提交**

```bash
git add backend/apps/dashboard/views.py backend/apps/dashboard/urls.py backend/apps/dashboard/tests/test_views.py
git commit -m "feat(dashboard): 添加关键词词云 API 接口

- 新增 DashboardKeywordCloudView 使用 jieba 分词统计
- 支持 /dashboard/keyword-cloud/ 端点
- 返回前100个高频关键词
- 添加单元测试验证分词准确性"
```

---

## 阶段二：前端类型和API定义

### Task 4: 添加 TypeScript 类型定义

**Files:**
- Modify: `frontend/src/types/index.ts`

**Step 4.1: 添加新类型**

编辑 `frontend/src/types/index.ts`，在文件末尾（在 `export interface ResetUserPasswordRequest` 之后）添加：

```typescript
// 驾驶舱新增类型
export interface TrendData {
  year: number
  count: number
}

export interface LevelDistribution {
  level: string
  level_name: string
  count: number
}

export interface KeywordCloudData {
  name: string
  value: number
}
```

**Step 4.2: 运行类型检查**

```bash
cd frontend
npm run type-check
```

预期输出：No type errors found

**Step 4.3: 提交**

```bash
git add frontend/src/types/index.ts
git commit -m "feat(types): 添加驾驶舱新增图表的 TypeScript 类型定义"
```

---

### Task 5: 添加前端 API 调用函数

**Files:**
- Modify: `frontend/src/api/dashboard.ts`

**Step 5.1: 添加 API 函数**

编辑 `frontend/src/api/dashboard.ts`，在文件末尾（在 `getCountryRanking` 函数之后）添加：

```typescript
// 获取时间趋势数据
export const getTrendData = () => {
  return request.get<ApiResponse<TrendData[]>>('/dashboard/trend/')
}

// 获取保护级别分布
export const getLevelDistribution = () => {
  return request.get<ApiResponse<LevelDistribution[]>>('/dashboard/level-distribution/')
}

// 获取关键词词云
export const getKeywordCloud = () => {
  return request.get<ApiResponse<KeywordCloudData[]>>('/dashboard/keyword-cloud/')
}
```

**Step 5.2: 运行类型检查**

```bash
cd frontend
npm run type-check
```

预期输出：No type errors found

**Step 5.3: 提交**

```bash
git add frontend/src/api/dashboard.ts
git commit -m "feat(api): 添加驾驶舱新增图表的 API 调用函数"
```

---

## 阶段三：前端图表实现

### Task 6: 引入世界地图数据

**Files:**
- Create: `frontend/public/world.json`

**Step 6.1: 下载 ECharts 世界地图数据**

```bash
curl -o frontend/public/world.json https://raw.githubusercontent.com/apache/echarts-examples/gh-pages/public/data/asset/geo/world.json
```

如果 curl 不可用，手动下载：
1. 访问 https://github.com/apache/echarts-examples/blob/master/public/data/asset/geo/world.json
2. 保存为 `frontend/public/world.json`

**Step 6.2: 验证文件存在**

```bash
ls -la frontend/public/world.json
```

预期输出：world.json 文件大小约 200KB+

**Step 6.3: 提交**

```bash
git add frontend/public/world.json
git commit -m "chore: 添加 ECharts 世界地图 JSON 数据"
```

---

### Task 7: 改造寰宇分布图为世界地图

**Files:**
- Modify: `frontend/src/views/Dashboard.vue`

**Step 7.1: 注册世界地图**

编辑 `frontend/src/views/Dashboard.vue`，在 `<script setup>` 中，`import * as echarts from 'echarts'` 后添加：

```typescript
// 注册世界地图
import worldJson from '/world.json'
echarts.registerMap('world', worldJson)
```

**Step 7.2: 修改 initMapChart 函数**

编辑 `frontend/src/views/Dashboard.vue`，找到 `initMapChart` 函数，替换整个函数为：

```typescript
// 初始化世界地图散点图
const initMapChart = () => {
  if (!mapChartRef.value) return

  mapChart = echarts.init(mapChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: (params: any) => {
        if (params.componentType === 'series') {
          return `
            <div style="padding: 8px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #D4AF37;">
                ${params.data.country_name}
              </div>
              <div style="display: flex; align-items: center; gap: 8px; margin: 4px 0;">
                <span style="color: #909399;">非遗项目：</span>
                <span style="font-weight: 600;">${params.data.heritage_count} 项</span>
              </div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #909399;">传承人：</span>
                <span style="font-weight: 600;">${params.data.inheritor_count} 人</span>
              </div>
            </div>
          `
        }
        return params.name
      }
    },
    geo: {
      map: 'world',
      roam: true,  // 支持缩放拖拽
      itemStyle: {
        areaColor: '#F7F4ED',
        borderColor: '#D4AF37',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          areaColor: '#E8E4DA'
        }
      },
      label: {
        show: false
      }
    },
    series: [
      {
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: mapData.value.map(item => ({
          name: item.country_name,
          value: [item.longitude, item.latitude, item.heritage_count],
          country_name: item.country_name,
          heritage_count: item.heritage_count,
          inheritor_count: item.inheritor_count
        })),
        symbolSize: (val: any) => Math.max(Math.sqrt(val[2]) * 6, 12),
        itemStyle: {
          color: '#C23531',
          opacity: 0.8,
          borderColor: '#D4AF37',
          borderWidth: 2
        },
        emphasis: {
          itemStyle: {
            color: '#DC143C',
            opacity: 1,
            borderWidth: 3,
            shadowBlur: 20,
            shadowColor: 'rgba(194, 35, 49, 0.6)'
          },
          scale: 1.15
        },
        rippleEffect: {
          brushType: 'stroke',
          scale: 3,
          period: 4
        }
      }
    ]
  }

  mapChart.setOption(option)
}
```

**Step 7.3: 修改地图图表高度**

编辑 `frontend/src/views/Dashboard.vue`，找到 `.map-chart .chart-body` 样式，修改为：

```css
.map-chart .chart-body {
  min-height: 580px;
}
```

**Step 7.4: 运行开发服务器测试**

```bash
cd frontend
npm run dev
```

访问 http://localhost:5173/dashboard，验证地图显示正常

**Step 7.5: 提交**

```bash
git add frontend/src/views/Dashboard.vue
git commit -m "feat(dashboard): 改造寰宇分布图为世界地图

- 引入 ECharts 世界地图 JSON 数据
- 使用 geo 坐标系替代经纬度散点图
- 支持缩放和拖拽交互
- 添加涟漪动画效果"
```

---

### Task 8: 改造类别玉璧图为矩形树图

**Files:**
- Modify: `frontend/src/views/Dashboard.vue`

**Step 8.1: 修改 initPieChart 函数为 treemap**

编辑 `frontend/src/views/Dashboard.vue`，找到 `initPieChart` 函数，将函数名改为 `initTreemapChart` 并替换整个函数：

```typescript
// 初始化类别矩形树图
const initTreemapChart = () => {
  if (!pieChartRef.value) return

  pieChart = echarts.init(pieChartRef.value)

  const total = categoryData.value.reduce((sum, item) => sum + item.heritage_count, 0)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: (params: any) => {
        const percent = ((params.value / total) * 100).toFixed(1)
        return `
          <div style="padding: 8px;">
            <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #D4AF37;">
              ${params.name}
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #909399;">项目数量：</span>
              <span style="font-weight: 600;">${params.value} 项</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="color: #909399;">占比：</span>
              <span style="font-weight: 600;">${percent}%</span>
            </div>
          </div>
        `
      }
    },
    series: [
      {
        type: 'treemap',
        data: categoryData.value.map((item, index) => ({
          name: item.category_name,
          value: item.heritage_count,
          itemStyle: {
            color: traditionalColors[index % traditionalColors.length]
          }
        })),
        breadcrumb: { show: false },
        label: {
          show: true,
          formatter: (params: any) => {
            const percent = ((params.value / total) * 100).toFixed(1)
            if (params.value > 0) {
              return `${params.name}\n${params.value}项\n${percent}%`
            }
            return params.name
          },
          color: '#FFFFFF',
          fontSize: 13,
          fontWeight: 600
        },
        itemStyle: {
          borderColor: '#F7F4ED',
          borderWidth: 3,
          gapWidth: 2
        },
        emphasis: {
          itemStyle: {
            borderColor: '#D4AF37',
            borderWidth: 4,
            shadowBlur: 20,
            shadowColor: 'rgba(212, 175, 55, 0.4)'
          },
          label: {
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        levels: [
          {
            itemStyle: {
              borderColor: '#F7F4ED',
              borderWidth: 3,
              gapWidth: 2
            }
          }
        ]
      }
    ]
  }

  pieChart.setOption(option)
}
```

**Step 8.2: 修改 initCharts 函数调用**

编辑 `frontend/src/views/Dashboard.vue`，找到 `initCharts` 函数，修改为：

```typescript
const initCharts = () => {
  initMapChart()
  initTreemapChart()  // 改名
  initBarChart()
}
```

**Step 8.3: 修改模板中标题**

编辑 `frontend/src/views/Dashboard.vue`，找到 `<!-- 类别玉璧图 -->` 部分，修改标题和印章：

```vue
<!-- 类别矩形树图 -->
<div class="chart-card treemap-chart">
  <div class="chart-frame">
    <div class="frame-corner top-left"></div>
    <div class="frame-corner top-right"></div>
    <div class="frame-corner bottom-left"></div>
    <div class="frame-corner bottom-right"></div>
    <div class="chart-header">
      <div class="header-title-group">
        <span class="title-seal">类</span>
        <h3 class="chart-title">类别矩形树图</h3>
      </div>
    </div>
    <div ref="pieChartRef" class="chart-body"></div>
  </div>
</div>
```

**Step 8.4: 添加样式类**

编辑 `frontend/src/views/Dashboard.vue`，在 `.pie-chart, .bar-chart` 样式处添加：

```css
.treemap-chart,
.bar-chart {
  grid-column: span 6;
}
```

删除原有的 `.pie-chart` 样式定义（如有单独定义）

**Step 8.5: 运行开发服务器测试**

```bash
cd frontend
npm run dev
```

访问 http://localhost:5173/dashboard，验证矩形树图显示正常

**Step 8.6: 提交**

```bash
git add frontend/src/views/Dashboard.vue
git commit -m "feat(dashboard): 改造类别玉璧图为矩形树图

- 使用 Treemap 替代饼图，解决类别过多问题
- 在矩形内直接显示名称、数量和占比
- 支持悬停高亮效果"
```

---

### Task 9: 添加保护级别玫瑰图

**Files:**
- Modify: `frontend/src/views/Dashboard.vue`

**Step 9.1: 添加图表 ref 和变量**

编辑 `frontend/src/views/Dashboard.vue`，在图表实例定义部分添加：

```typescript
// 图表实例
const mapChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()
const barChartRef = ref<HTMLElement>()
const roseChartRef = ref<HTMLElement>()  // 新增

let mapChart: ECharts | null = null
let pieChart: ECharts | null = null
let barChart: ECharts | null = null
let roseChart: ECharts | null = null  // 新增
```

添加数据变量：

```typescript
const rankingData = ref<CountryRanking[]>([])
const levelData = ref<LevelDistribution[]>([])  // 新增
const categories = ref<Category[]>([])
```

**Step 9.2: 在 loadData 中获取数据**

编辑 `frontend/src/views/Dashboard.vue`，找到 `loadData` 函数，修改为：

```typescript
const loadData = async () => {
  try {
    const [overviewRes, mapRes, categoryRes, rankingRes, categoriesRes, levelRes] = await Promise.all([
      getOverview(),
      getMapDistribution(),
      getCategoryDistribution(),
      getCountryRanking({ limit: 20 }),
      getCategoryList(),
      getLevelDistribution()  // 新增
    ])

    overview.value = overviewRes.data.data
    mapData.value = mapRes.data.data
    categoryData.value = categoryRes.data.data
    rankingData.value = rankingRes.data.data
    categories.value = categoriesRes.data.data
    levelData.value = levelRes.data.data  // 新增

    // ... 保持原有的动画代码不变

    setTimeout(initCharts, 500)
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    ElMessage.error('加载数据失败')
  }
}
```

**Step 9.3: 实现 initRoseChart 函数**

编辑 `frontend/src/views/Dashboard.vue`，在 `initBarChart` 函数后添加：

```typescript
// 初始化保护级别玫瑰图
const initRoseChart = () => {
  if (!roseChartRef.value) return

  roseChart = echarts.init(roseChartRef.value)

  const total = levelData.value.reduce((sum, item) => sum + item.count, 0)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: '{b}: {c} 项 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: {
        color: '#2F3640',
        fontSize: 13,
        fontWeight: 500
      },
      itemGap: 16
    },
    series: [
      {
        name: '保护级别',
        type: 'pie',
        roseType: 'area',
        radius: ['35%', '70%'],
        center: ['35%', '50%'],
        data: levelData.value.map((item, index) => ({
          name: item.level_name,
          value: item.count,
          itemStyle: {
            color: traditionalColors[index % traditionalColors.length]
          }
        })),
        label: {
          show: true,
          formatter: (params: any) => {
            const percent = ((params.value / total) * 100).toFixed(1)
            return `${params.name}\n${params.value}项\n${percent}%`
          },
          color: '#2F3640',
          fontSize: 12,
          fontWeight: 500
        },
        labelLine: {
          show: true,
          length: 10,
          length2: 15,
          smooth: true,
          lineStyle: { color: '#D4AF37', width: 1.5 }
        },
        itemStyle: {
          borderRadius: 6,
          borderColor: '#F7F4ED',
          borderWidth: 3
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(212, 175, 55, 0.4)'
          }
        }
      }
    ]
  }

  roseChart.setOption(option)
}
```

**Step 9.4: 更新 initCharts 函数**

编辑 `frontend/src/views/Dashboard.vue`，修改 `initCharts` 函数：

```typescript
const initCharts = () => {
  initMapChart()
  initTreemapChart()
  initBarChart()
  initRoseChart()  // 新增
}
```

**Step 9.5: 更新 handleResize 函数**

编辑 `frontend/src/views/Dashboard.vue`，修改 `handleResize` 函数：

```typescript
const handleResize = () => {
  mapChart?.resize()
  pieChart?.resize()
  barChart?.resize()
  roseChart?.resize()  // 新增
}
```

**Step 9.6: 更新 onUnmounted 清理**

编辑 `frontend/src/views/Dashboard.vue`，修改 `onUnmounted`：

```typescript
onUnmounted(() => {
  mapChart?.dispose()
  pieChart?.dispose()
  barChart?.dispose()
  roseChart?.dispose()  // 新增
  window.removeEventListener('resize', handleResize)
})
```

**Step 9.7: 添加模板结构**

编辑 `frontend/src/views/Dashboard.vue`，在类别矩形树图后添加：

```vue
<!-- 保护级别玫瑰图 -->
<div class="chart-card rose-chart">
  <div class="chart-frame">
    <div class="frame-corner top-left"></div>
    <div class="frame-corner top-right"></div>
    <div class="frame-corner bottom-left"></div>
    <div class="frame-corner bottom-right"></div>
    <div class="chart-header">
      <div class="header-title-group">
        <span class="title-seal">级</span>
        <h3 class="chart-title">保护级别玫瑰图</h3>
      </div>
    </div>
    <div ref="roseChartRef" class="chart-body"></div>
  </div>
</div>
```

**Step 9.8: 添加导入**

编辑 `frontend/src/views/Dashboard.vue`，在 API 导入处添加：

```typescript
import {
  getOverview,
  getMapDistribution,
  getCategoryDistribution,
  getCountryRanking,
  getLevelDistribution  // 新增
} from '@/api/dashboard'
```

同时在 types 导入处添加：

```typescript
import type {
  DashboardOverview,
  MapPoint,
  CategoryDistribution,
  CountryRanking,
  Category,
  LevelDistribution  // 新增
} from '@/types'
```

**Step 9.9: 运行开发服务器测试**

```bash
cd frontend
npm run dev
```

验证玫瑰图显示正常

**Step 9.10: 提交**

```bash
git add frontend/src/views/Dashboard.vue
git commit -m "feat(dashboard): 添加保护级别玫瑰图

- 新增南丁格尔玫瑰图展示国家级/省级/县级分布
- 支持悬停显示详细数据
- 使用传统中国色彩"
```

---

### Task 10: 添加时间趋势面积图

**Files:**
- Modify: `frontend/src/views/Dashboard.vue`

**Step 10.1: 添加图表 ref 和变量**

编辑 `frontend/src/views/Dashboard.vue`，添加：

```typescript
const trendChartRef = ref<HTMLElement>()  // 新增
let trendChart: ECharts | null = null  // 新增
const trendData = ref<TrendData[]>([])  // 新增
```

**Step 10.2: 在 loadData 中获取数据**

编辑 `frontend/src/views/Dashboard.vue`，修改 `loadData` 函数的 Promise.all：

```typescript
const [overviewRes, mapRes, categoryRes, rankingRes, categoriesRes, levelRes, trendRes] = await Promise.all([
  getOverview(),
  getMapDistribution(),
  getCategoryDistribution(),
  getCountryRanking({ limit: 20 }),
  getCategoryList(),
  getLevelDistribution(),
  getTrendData()  // 新增
])
```

添加赋值：

```typescript
trendData.value = trendRes.data.data  // 新增
```

**Step 10.3: 实现 initTrendChart 函数**

在 `initRoseChart` 函数后添加：

```typescript
// 初始化时间趋势面积图
const initTrendChart = () => {
  if (!trendChartRef.value) return

  trendChart = echarts.init(trendChartRef.value)

  const years = trendData.value.map(item => item.year)
  const counts = trendData.value.map(item => item.count)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: (params: any) => {
        const data = params[0]
        return `<span style="color: #D4AF37; font-weight: 600;">${data.name}年</span>: ${data.value} 项`
      }
    },
    grid: {
      left: '10%',
      right: '8%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: years,
      axisLine: { lineStyle: { color: '#D4AF37', opacity: 0.5 } },
      axisLabel: {
        color: '#606266',
        fontSize: 11,
        formatter: (value: number) => value.toString()
      },
      axisTick: { alignWithLabel: true }
    },
    yAxis: {
      type: 'value',
      name: '新增项目数',
      axisLine: { show: false },
      axisLabel: { color: '#606266', fontSize: 11 },
      splitLine: {
        lineStyle: { color: '#D4AF37', type: 'dashed', opacity: 0.15 }
      },
      nameTextStyle: { color: '#606266', fontSize: 12 }
    },
    series: [
      {
        name: '新增项目',
        type: 'line',
        data: counts,
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          color: '#C23531',
          width: 3
        },
        itemStyle: {
          color: '#C23531',
          borderColor: '#D4AF37',
          borderWidth: 2
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(194, 35, 49, 0.4)' },
            { offset: 1, color: 'rgba(194, 35, 49, 0.02)' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: '#DC143C',
            borderColor: '#D4AF37',
            borderWidth: 3,
            shadowBlur: 15,
            shadowColor: 'rgba(194, 35, 49, 0.5)'
          },
          scale: 1.3
        }
      }
    ]
  }

  trendChart.setOption(option)
}
```

**Step 10.4: 更新相关函数**

修改 `initCharts`、`handleResize`、`onUnmounted`：

```typescript
const initCharts = () => {
  initMapChart()
  initTreemapChart()
  initBarChart()
  initRoseChart()
  initTrendChart()  // 新增
}

const handleResize = () => {
  mapChart?.resize()
  pieChart?.resize()
  barChart?.resize()
  roseChart?.resize()
  trendChart?.resize()  // 新增
}

onUnmounted(() => {
  mapChart?.dispose()
  pieChart?.dispose()
  barChart?.dispose()
  roseChart?.dispose()
  trendChart?.dispose()  // 新增
  window.removeEventListener('resize', handleResize)
})
```

**Step 10.5: 添加模板和样式**

在模板中添加（在各国项目排行后）：

```vue
<!-- 时间趋势面积图 -->
<div class="chart-card trend-chart">
  <div class="chart-frame">
    <div class="frame-corner top-left"></div>
    <div class="frame-corner top-right"></div>
    <div class="frame-corner bottom-left"></div>
    <div class="frame-corner bottom-right"></div>
    <div class="chart-header">
      <div class="header-title-group">
        <span class="title-seal">时</span>
        <h3 class="chart-title">时间趋势面积图</h3>
      </div>
    </div>
    <div ref="trendChartRef" class="chart-body"></div>
  </div>
</div>
```

添加样式：

```css
.trend-chart,
.wordcloud-chart {
  grid-column: span 6;
}
```

添加导入：

```typescript
import {
  // ... 其他导入
  getTrendData  // 新增
} from '@/api/dashboard'

import type {
  // ... 其他导入
  TrendData  // 新增
} from '@/types'
```

**Step 10.6: 运行开发服务器测试**

验证趋势图显示正常

**Step 10.7: 提交**

```bash
git add frontend/src/views/Dashboard.vue
git commit -m "feat(dashboard): 添加时间趋势面积图

- 新增面积折线图展示按年份统计的非遗项目数
- 使用渐变填充和平滑曲线
- 支持悬停显示具体年份数据"
```

---

### Task 11: 添加关键词词云图

**Files:**
- Modify: `frontend/src/views/Dashboard.vue`

**Step 11.1: 安装并注册词云组件**

编辑 `frontend/src/views/Dashboard.vue`，在 import 部分添加：

```typescript
import 'echarts-wordcloud'
```

**Step 11.2: 添加图表 ref 和变量**

```typescript
const wordcloudChartRef = ref<HTMLElement>()  // 新增
let wordcloudChart: ECharts | null = null  // 新增
const keywordData = ref<KeywordCloudData[]>([])  // 新增
```

**Step 11.3: 在 loadData 中获取数据**

编辑 `frontend/src/views/Dashboard.vue`，修改 `loadData`：

```typescript
const [overviewRes, mapRes, categoryRes, rankingRes, categoriesRes, levelRes, trendRes, keywordRes] = await Promise.all([
  getOverview(),
  getMapDistribution(),
  getCategoryDistribution(),
  getCountryRanking({ limit: 20 }),
  getCategoryList(),
  getLevelDistribution(),
  getTrendData(),
  getKeywordCloud()  // 新增
])
```

添加赋值：

```typescript
keywordData.value = keywordRes.data.data  // 新增
```

**Step 11.4: 实现 initWordcloudChart 函数**

```typescript
// 初始化关键词词云图
const initWordcloudChart = () => {
  if (!wordcloudChartRef.value) return

  wordcloudChart = echarts.init(wordcloudChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: (params: any) => {
        return `<span style="color: #D4AF37; font-weight: 600;">${params.name}</span>: 出现 ${params.value} 次`
      }
    },
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        left: 'center',
        top: 'center',
        width: '90%',
        height: '85%',
        right: null,
        bottom: null,
        gridSize: 6,
        sizeRange: [14, 48],
        rotateRange: [-30, 30],
        rotationStep: 15,
        drawOutOfBound: false,
        textStyle: {
          fontFamily: 'STSong, SimSun, serif',
          fontWeight: 'bold'
        },
        emphasis: {
          textStyle: {
            textShadowBlur: 8,
            textShadowColor: '#D4AF37'
          }
        },
        data: keywordData.value.map((item, index) => ({
          name: item.name,
          value: item.value,
          textStyle: {
            color: traditionalColors[index % traditionalColors.length]
          }
        }))
      }
    ]
  }

  wordcloudChart.setOption(option)
}
```

**Step 11.5: 更新相关函数**

```typescript
const initCharts = () => {
  initMapChart()
  initTreemapChart()
  initBarChart()
  initRoseChart()
  initTrendChart()
  initWordcloudChart()  // 新增
}

const handleResize = () => {
  mapChart?.resize()
  pieChart?.resize()
  barChart?.resize()
  roseChart?.resize()
  trendChart?.resize()
  wordcloudChart?.resize()  // 新增
}

onUnmounted(() => {
  mapChart?.dispose()
  pieChart?.dispose()
  barChart?.dispose()
  roseChart?.dispose()
  trendChart?.dispose()
  wordcloudChart?.dispose()  // 新增
  window.removeEventListener('resize', handleResize)
})
```

**Step 11.6: 添加模板**

```vue
<!-- 关键词词云图 -->
<div class="chart-card wordcloud-chart">
  <div class="chart-frame">
    <div class="frame-corner top-left"></div>
    <div class="frame-corner top-right"></div>
    <div class="frame-corner bottom-left"></div>
    <div class="frame-corner bottom-right"></div>
    <div class="chart-header">
      <div class="header-title-group">
        <span class="title-seal">词</span>
        <h3 class="chart-title">关键词词云</h3>
      </div>
    </div>
    <div ref="wordcloudChartRef" class="chart-body"></div>
  </div>
</div>
```

**Step 11.7: 添加导入**

```typescript
import {
  // ... 其他导入
  getKeywordCloud  // 新增
} from '@/api/dashboard'

import type {
  // ... 其他导入
  KeywordCloudData  // 新增
} from '@/types'
```

**Step 11.8: 运行开发服务器测试**

验证词云图显示正常

**Step 11.9: 提交**

```bash
git add frontend/src/views/Dashboard.vue
git commit -m "feat(dashboard): 添加关键词词云图

- 新增词云图展示非遗项目名称高频关键词
- 使用 jieba 分词统计
- 支持圆形布局和随机旋转"
```

---

### Task 12: 移除原有各国项目排行图（如需要）

**根据设计方案，各国排行图保留，无需修改。**

---

## 阶段四：响应式布局优化

### Task 13: 优化响应式布局

**Files:**
- Modify: `frontend/src/views/Dashboard.vue`

**Step 13.1: 修改响应式样式**

编辑 `frontend/src/views/Dashboard.vue`，找到响应式部分，更新为：

```css
/* ========== 响应式 ========== */
@media (max-width: 1400px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .pie-chart,
  .bar-chart {
    grid-column: span 12;
  }

  .treemap-chart,
  .rose-chart,
  .trend-chart,
  .wordcloud-chart {
    grid-column: span 12;
  }
}

@media (max-width: 768px) {
  .heritage-dashboard {
    padding: 24px 16px;
  }

  .header-decoration {
    flex-direction: column;
    gap: 16px;
  }

  .decoration-line {
    width: 80px;
  }

  .page-title {
    font-size: 32px;
    letter-spacing: 4px;
  }

  .stats-section {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .map-chart,
  .treemap-chart,
  .rose-chart,
  .trend-chart,
  .wordcloud-chart {
    grid-column: span 1;
  }

  .chart-frame {
    padding: 20px;
  }

  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  :deep(.heritage-select) {
    width: 100%;
  }
}
```

**Step 13.2: 测试响应式**

调整浏览器窗口大小，验证布局正常

**Step 13.3: 提交**

```bash
git add frontend/src/views/Dashboard.vue
git commit -m "style(dashboard): 优化响应式布局

- 中等屏幕下图表单列显示
- 移动端优化卡片间距和字体大小"
```

---

## 阶段五：测试和收尾

### Task 14: 运行完整测试

**Step 14.1: 运行后端所有测试**

```bash
cd backend
python manage.py test apps.dashboard -v 2
```

预期输出：所有测试 PASS

**Step 14.2: 运行前端类型检查**

```bash
cd frontend
npm run type-check
```

预期输出：No type errors found

**Step 14.3: 构建前端验证**

```bash
cd frontend
npm run build
```

预期输出：构建成功

---

### Task 15: 最终验收

**Step 15.1: 启动完整系统**

```bash
# 终端1: 后端
cd backend
python manage.py runserver

# 终端2: 前端
cd frontend
npm run dev
```

**Step 15.2: 验证清单**

访问 http://localhost:5173/dashboard，验证以下功能：

- [ ] 世界地图显示正常，支持缩放拖拽
- [ ] 类别矩形树图显示，无重叠
- [ ] 保护级别玫瑰图显示各级别分布
- [ ] 时间趋势面积图显示年份趋势
- [ ] 关键词词云显示高频词
- [ ] 响应式布局在不同屏幕尺寸下正常
- [ ] 所有图表 tooltip 显示正确

**Step 15.3: 性能检查**

- 打开浏览器 DevTools > Network
- 刷新页面
- 验证 API 响应时间 < 500ms

---

### Task 16: 创建实施总结

**Step 16.1: 创建实施总结文档**

```bash
cat > docs/implementation-summary-2026-02-26.md << 'EOF'
# 驾驶舱重设计实施总结

**完成日期**: 2026-02-26
**实施人员**: Claude
**文档版本**: v1.0

---

## 完成的功能

### 后端 API (3个新增)

| 端点 | 功能 | 测试覆盖 |
|------|------|----------|
| `/dashboard/trend/` | 按年份统计新增项目 | ✅ 3个测试 |
| `/dashboard/level-distribution/` | 保护级别分布统计 | ✅ 3个测试 |
| `/dashboard/keyword-cloud/` | 关键词词云数据 | ✅ 3个测试 |

### 前端图表 (6个)

| 图表 | 类型 | 状态 |
|------|------|------|
| 寰宇分布图 | 世界地图 + 散点 | ✅ 改造完成 |
| 类别矩形树图 | Treemap | ✅ 替代玉璧图 |
| 保护级别玫瑰图 | 南丁格尔玫瑰图 | ✅ 新增 |
| 时间趋势面积图 | 面积折线图 | ✅ 新增 |
| 关键词词云 | 词云图 | ✅ 新增 |
| 各国项目排行 | 横向柱状图 | ✅ 保留 |

---

## 技术债务与改进建议

1. **性能优化**: 6个图表同时加载可考虑懒加载
2. **缓存**: 后端关键词词云计算可加缓存
3. **停用词**: jieba 分词可添加非遗领域停用词表

---

## 已知问题

无

---

**下一步**: 根据用户反馈进行微调优化
EOF
```

**Step 16.2: 提交最终代码**

```bash
git add docs/implementation-summary-2026-02-26.md
git commit -m "docs: 添加驾驶舱重设计实施总结"
```

---

## 实施计划完成

本实施计划包含 **16 个任务**，涵盖：
- 后端 3 个新 API 接口开发（带 TDD 测试）
- 前端 6 个图表组件实现
- 响应式布局优化
- 完整的验收测试

预计工作量：**4-6 小时**

---

**For Claude (执行时):** 使用 `@superpowers:executing-plans` 技能按任务顺序执行。
