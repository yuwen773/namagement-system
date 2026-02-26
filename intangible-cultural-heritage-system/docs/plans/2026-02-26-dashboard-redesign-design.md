# 驾驶舱数据可视化重设计方案

**日期**: 2026-02-26
**项目**: 非物质文化遗产管理系统
**设计目标**: 解决当前驾驶舱图表简单、数据展示不充分的问题

---

## 问题分析

### 当前问题
1. **寰宇分布图** - 使用经纬度散点图，无法直观展示全球地理分布
2. **类别玉璧图** - 类别过多导致图例重叠，可读性差
3. **图表数量不足** - 仅3个图表，数据可视化维度单一

### 根本原因
- 图表类型选择与数据特征不匹配
- 缺少时间、级别、内容等多维度数据展示

---

## 设计方案

### 整体布局 (6+1 卡片式)

```
┌─────────────────────────────────────────────────────────┐
│  统计卡片行 (4个): 非遗项目 | 传承人 | 分类 | 覆盖国家      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│           寰宇分布图 (世界地图) - 全宽 12列                │
│                   [可缩放/拖拽/筛选]                       │
│                                                           │
├──────────────────────┬──────────────────────────────────┤
│                       │                                  │
│   类别矩形树图 6列     │   保护级别玫瑰图 6列               │
│   [替代玉璧图]        │   [新增]                          │
│                       │                                  │
├──────────────────────┼──────────────────────────────────┤
│                       │                                  │
│   时间趋势面积图 6列   │   关键词词云 6列                   │
│   [新增]              │   [新增]                          │
│                       │                                  │
└──────────────────────┴──────────────────────────────────┘
```

---

## 图表详细设计

### 1. 寰宇分布图 (改造)

**图表类型**: 世界地图 + 气泡散点

**技术实现**:
```javascript
{
  geo: {
    map: 'world',
    roam: true,  // 支持缩放拖拽
    itemStyle: {
      areaColor: '#F7F4ED',
      borderColor: '#D4AF37'
    }
  },
  series: [{
    type: 'effectScatter',
    coordinateSystem: 'geo',
    data: mapData,
    symbolSize: val => Math.sqrt(val.count) * 8,
    itemStyle: { color: '#C23531' }
  }]
}
```

**数据接口**: `/dashboard/map-distribution/` (已存在)

**需要补充**: 返回数据增加 `dominant_category` 字段用于颜色编码

---

### 2. 类别矩形树图 (新增，替代玉璧图)

**图表类型**: 矩形树图 (Treemap)

**技术实现**:
```javascript
{
  series: [{
    type: 'treemap',
    data: categoryData,
    label: {
      formatter: params =>
        `${params.name}\n${params.value}项\n${params.percent}%`
    },
    itemStyle: {
      borderColor: '#F7F4ED',
      gapWidth: 2
    },
    colors: traditionalColors
  }]
}
```

**数据接口**: `/dashboard/category-distribution/` (已存在)

**优势**:
- 可容纳20+类别无压力
- 面积大小直观反映占比
- 支持点击下钻查看子分类

---

### 3. 保护级别玫瑰图 (新增)

**图表类型**: 南丁格尔玫瑰图

**技术实现**:
```javascript
{
  series: [{
    type: 'pie',
    roseType: 'area',
    radius: ['30%', '70%'],
    data: levelData,
    label: {
      formatter: '{b}: {c}项\n({d}%)'
    }
  }]
}
```

**数据接口**: `/dashboard/level-distribution/` (新增)

**返回格式**:
```json
[
  { "level": "国家级", "count": 1234 },
  { "level": "省级", "count": 5678 },
  { "level": "县级", "count": 9012 }
]
```

---

### 4. 时间趋势面积图 (新增)

**图表类型**: 面积折线图

**技术实现**:
```javascript
{
  xAxis: { type: 'category', data: years },
  yAxis: { type: 'value' },
  series: [{
    type: 'line',
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(194, 35, 49, 0.4)' },
        { offset: 1, color: 'rgba(194, 35, 49, 0.05)' }
      ])
    },
    data: yearlyCounts
  }]
}
```

**数据接口**: `/dashboard/trend/` (新增)

**返回格式**:
```json
[
  { "year": 2008, "count": 35 },
  { "year": 2009, "count": 42 },
  ...
]
```

---

### 5. 关键词词云 (新增)

**图表类型**: 词云图

**技术实现**:
```javascript
{
  series: [{
    type: 'wordCloud',
    shape: 'circle',
    gridSize: 8,
    sizeRange: [12, 50],
    rotationRange: [-45, 45],
    data: keywordData
  }]
}
```

**数据接口**: `/dashboard/keyword-cloud/` (新增)

**返回格式**:
```json
[
  { "name": "剪纸", "value": 45 },
  { "name": "刺绣", "value": 38 },
  { "name": "陶瓷", "value": 32 },
  ...
]
```

**分词方案**: 后端使用 jieba 对 `heritage_items.name` 进行分词统计

---

### 6. 各国项目排行 (保留)

**图表类型**: 横向柱状图 (已有)

**无变化**: 当前实现已满足需求

---

## 后端 API 设计

### 新增接口

```python
# dashboard/views.py

class DashboardTrendView(APIView):
    """
    时间趋势 - 按年份统计新增项目
    GET /dashboard/trend/
    """
    def get(self, request):
        data = (
            HeritageItem.objects
            .extra(select={'year': 'EXTRACT(year FROM created_at)'})
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )
        return success_response(data=list(data))


class DashboardLevelDistributionView(APIView):
    """
    保护级别分布
    GET /dashboard/level-distribution/
    """
    def get(self, request):
        data = []
        for level_value, level_name in HeritageItem.LEVEL_CHOICES:
            count = HeritageItem.objects.filter(level=level_value).count()
            data.append({
                'level': level_value,
                'level_name': level_name,
                'count': count
            })
        return success_response(data=data)


class DashboardKeywordCloudView(APIView):
    """
    关键词词云
    GET /dashboard/keyword-cloud/
    """
    def get(self, request):
        import jieba

        # 获取所有非遗项目名称
        names = HeritageItem.objects.values_list('name', flat=True)

        # 分词统计
        word_count = {}
        for name in names:
            words = jieba.cut(name)
            for word in words:
                if len(word) >= 2:  # 过滤单字
                    word_count[word] = word_count.get(word, 0) + 1

        # 排序取前100
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:100]

        data = [{'name': word, 'value': count} for word, count in sorted_words]
        return success_response(data=data)
```

---

## 前端实现要点

### 依赖安装

```bash
npm install echarts-wordcloud
```

### API 定义

```typescript
// api/dashboard.ts 新增
export const getTrendData = () =>
  request.get<ApiResponse<TrendData[]>>('/dashboard/trend/')

export const getLevelDistribution = () =>
  request.get<ApiResponse<LevelDistribution[]>>('/dashboard/level-distribution/')

export const getKeywordCloud = () =>
  request.get<ApiResponse<KeywordCloudData[]>>('/dashboard/keyword-cloud/')
```

### 类型定义

```typescript
// types/index.ts 新增
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

### 布局调整

```vue
<template>
  <div class="charts-section">
    <!-- 12列 -->
    <div class="chart-card map-chart">寰宇分布图</div>

    <!-- 6列 + 6列 -->
    <div class="chart-card treemap-chart">类别矩形树图</div>
    <div class="chart-card rose-chart">保护级别玫瑰图</div>

    <!-- 6列 + 6列 -->
    <div class="chart-card trend-chart">时间趋势面积图</div>
    <div class="chart-card wordcloud-chart">关键词词云</div>
  </div>
</template>

<style scoped>
.charts-section {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.map-chart { grid-column: span 12; }
.treemap-chart,
.rose-chart,
.trend-chart,
.wordcloud-chart {
  grid-column: span 6;
}
</style>
```

---

## 实施计划

### 阶段一: 后端 API 开发
1. 新增3个 dashboard 接口
2. 安装 jieba 分词库
3. 编写单元测试

### 阶段二: 前端图表开发
1. 安装 echarts-wordcloud
2. 改造寰宇分布图 (引入世界地图)
3. 实现类别矩形树图
4. 实现3个新增图表

### 阶段三: 联调测试
1. 数据准确性验证
2. 响应式布局测试
3. 性能优化

---

## 技术栈

- **后端**: Django 5.2 + DRF
- **前端**: Vue 3 + ECharts 5 + Element Plus
- **分词**: jieba
- **词云**: echarts-wordcloud

---

## 风险与注意事项

1. **世界地图数据**: 需要确保 echarts 世界地图 JSON 可用
2. **分词准确度**: jieba 分词结果可能需要调整停用词
3. **性能**: 6个图表同时加载可能影响首屏性能，考虑懒加载
4. **移动端适配**: 小屏幕下图表需要堆叠显示

---

**设计文档版本**: v1.0
**最后更新**: 2026-02-26
