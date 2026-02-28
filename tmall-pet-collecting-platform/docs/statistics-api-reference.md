# 数据统计API文档

## 概述

本文档描述了优化后的数据统计API接口，提供丰富的数据分析能力。

**基础路径**: `/api/products/statistics/`

---

## 1. 增强概览 (Enhanced Overview)

### GET `/overview/`

获取增强的数据概览，包含更多维度的统计信息。

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| search | string | 否 | 搜索关键词（标题/店铺） |
| brand | string | 否 | 品牌筛选 |
| region | string | 否 | 地区筛选 |

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "total_products": 133,
    "total_shops": 73,
    "total_brands": 5,
    "total_regions": 16,
    "price": {
      "avg": 412.03,
      "max": 7000.0,
      "min": 9.9,
      "range": 6990.1
    },
    "sales": {
      "avg": 1298.0,
      "max": 5000,
      "total": 172670
    },
    "completeness": {
      "with_brand": 68,
      "with_category": 40,
      "with_region": 93,
      "with_image": 133,
      "with_sales": 132
    },
    "completeness_pct": {
      "with_brand_pct": 51,
      "with_category_pct": 30,
      "with_region_pct": 69,
      "with_image_pct": 100,
      "with_sales_pct": 99
    },
    "latest_batch": {
      "batch_no": "IMPORT_20260208_185633",
      "crawl_time": "2026-02-08T10:56:33+00:00"
    }
  }
}
```

---

## 2. 价格分布 (Price Distribution)

### GET `/price-distribution/`

获取智能价格区间分布（根据实际数据自动生成区间）。

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "range": "0-50",
      "min_price": 0,
      "max_price": 50,
      "count": 29,
      "percentage": 21.8
    },
    {
      "range": "50-100",
      "min_price": 50,
      "max_price": 100,
      "count": 28,
      "percentage": 21.05
    },
    {
      "range": "100-200",
      "min_price": 100,
      "max_price": 200,
      "count": 24,
      "percentage": 18.05
    },
    {
      "range": "200-500",
      "min_price": 200,
      "max_price": 500,
      "count": 38,
      "percentage": 28.57
    },
    {
      "range": "500-1000",
      "min_price": 500,
      "max_price": 1000,
      "count": 5,
      "percentage": 3.76
    },
    {
      "range": "1000-2000",
      "min_price": 1000,
      "max_price": 2000,
      "count": 2,
      "percentage": 1.5
    },
    {
      "range": "2000-5000",
      "min_price": 2000,
      "max_price": 5000,
      "count": 5,
      "percentage": 3.76
    },
    {
      "range": "7000+",
      "min_price": 7000,
      "max_price": null,
      "count": 2,
      "percentage": 1.5
    }
  ]
}
```

---

## 3. 销量分布 (Sales Distribution) 🆕

### GET `/sales-distribution/`

获取销量区间分布统计。

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {"range": "无销量", "count": 1, "percentage": 0.75},
    {"range": "1-100", "count": 28, "percentage": 21.05},
    {"range": "100-500", "count": 35, "percentage": 26.32},
    {"range": "500-1000", "count": 20, "percentage": 15.04},
    {"range": "1000-2000", "count": 38, "percentage": 28.57},
    {"range": "2000-5000", "count": 10, "percentage": 7.52},
    {"range": "5000+", "count": 1, "percentage": 0.75}
  ]
}
```

---

## 4. 品牌分析 (Brand Analysis) 🆕

### GET `/brand-analysis/`

获取品牌详细分析，包含价格、销量等维度。

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| top_n | integer | 否 | 返回前N个品牌（默认15） |
| search | string | 否 | 搜索关键词 |

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "brand": "未分类",
      "count": 65,
      "price": {
        "avg": 283.7,
        "min": 9.9,
        "max": 5000.0
      },
      "sales": {
        "avg": 1289.0,
        "total": 83785
      }
    },
    {
      "brand": "万代潮玩",
      "count": 40,
      "price": {
        "avg": 268.28,
        "min": 9.9,
        "max": 3500.0
      },
      "sales": {
        "avg": 1375.0,
        "total": 55000
      }
    }
  ],
  "total": 5
}
```

---

## 5. 地区分析 (Region Analysis) 🆕

### GET `/region-analysis/`

获取地区详细分析，用于热力图展示。

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| top_n | integer | 否 | 返回前N个地区（默认15） |
| search | string | 否 | 搜索关键词 |

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "region": "广东 深圳",
      "count": 34,
      "avg_price": 450.5,
      "avg_sales": 1350.0,
      "shop_count": 25
    },
    {
      "region": "浙江 金华",
      "count": 10,
      "avg_price": 280.3,
      "avg_sales": 1200.0,
      "shop_count": 8
    }
  ],
  "total": 16
}
```

---

## 6. 店铺分析 (Shop Analysis) 🆕

### GET `/shop-analysis/`

获取店铺详细分析，包含商品数、均价、销量等。

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| top_n | integer | 否 | 返回前N个店铺（默认20） |
| search | string | 否 | 搜索关键词 |

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "shop": "永乐玩具",
      "count": 15,
      "avg_price": 350.5,
      "avg_sales": 1500.0,
      "max_price": 5000.0,
      "total_sales": 22500
    }
  ],
  "total": 73
}
```

---

## 7. Top商品 (Top Products) 🆕

### GET `/top-products/`

获取Top商品，支持多维度排序。

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sort_by | string | 否 | 排序方式：sales/price/price_asc/newest（默认sales） |
| top_n | integer | 否 | 返回前N个商品（默认20） |
| search | string | 否 | 搜索关键词 |

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "uuid",
      "title": "万代PG独角兽高达",
      "price": 3599.0,
      "sales": 5000,
      "shop": "永乐玩具",
      "brand": "Bandai/万代",
      "region": "广东 深圳",
      "image_url": "http://...",
      "crawl_time": "2026-02-08T10:56:33+00:00"
    }
  ],
  "total": 20
}
```

---

## 8. 价格-销量关联分析 (Price-Sales Correlation) 🆕

### GET `/price-sales-correlation/`

分析不同价格区间的平均销量，发现价格与销量的关系。

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {"price_range": "0-50", "count": 29, "avg_sales": 1500.0},
    {"price_range": "50-100", "count": 28, "avg_sales": 1350.0},
    {"price_range": "100-200", "count": 24, "avg_sales": 1200.0},
    {"price_range": "200-500", "count": 38, "avg_sales": 1100.0},
    {"price_range": "500-1000", "count": 5, "avg_sales": 800.0},
    {"price_range": "1000-2000", "count": 2, "avg_sales": 500.0},
    {"price_range": "2000+", "count": 7, "avg_sales": 300.0}
  ]
}
```

---

## 9. 属性分析 (Attribute Analysis) 🆕

### GET `/attribute-analysis/`

获取商品属性（如版本、级别等）的统计分析。

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "出售状态": [
      {"value": "现货", "count": 60},
      {"value": "预售", "count": 7}
    ],
    "版本类型": [
      {"value": "日版", "count": 35},
      {"value": "大陆", "count": 22}
    ],
    "模型级别": [
      {"value": "HG", "count": 40},
      {"value": "MG", "count": 25},
      {"value": "RG", "count": 15},
      {"value": "PG", "count": 5}
    ]
  }
}
```

---

## 10. 批次分析 (Batch Analysis) 🆕

### GET `/batch-analysis/`

获取采集批次分析，了解数据采集趋势。

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "batch_no": "IMPORT_20260208_185633",
      "count": 93,
      "avg_price": 412.03,
      "avg_sales": 1298.0,
      "first_time": "2026-02-08T10:56:33+00:00",
      "last_time": "2026-02-08T10:56:33+00:00"
    },
    {
      "batch_no": "20260208084415",
      "count": 20,
      "avg_price": 380.5,
      "avg_sales": 1200.0,
      "first_time": "2026-02-08T08:44:15+00:00",
      "last_time": "2026-02-08T08:44:15+00:00"
    }
  ],
  "total": 3
}
```

---

## 11. 关键词分析 (Keyword Analysis) 🆕

### GET `/keyword-analysis/`

分析商品标题中的热门关键词。

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| top_n | integer | 否 | 返回前N个关键词（默认30） |
| sample_size | integer | 否 | 分析的商品样本数（默认200） |

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {"keyword": "高达模型", "count": 14},
    {"keyword": "强袭", "count": 13},
    {"keyword": "高达", "count": 8},
    {"keyword": "拼装", "count": 7},
    {"keyword": "红异端", "count": 7}
  ],
  "total": 30
}
```

---

## 12. 市场洞察 (Market Insights) 🆕

### GET `/market-insights/`

获取综合市场洞察分析，包含市场规模、价格定位、品牌洞察等。

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "market_size": {
      "total_products": 133,
      "total_shops": 73,
      "total_sales": 172670
    },
    "price_positioning": {
      "avg_price": 412.03,
      "main_range": "200-500",
      "main_range_pct": 28.57,
      "low_end_pct": 21.8,
      "high_end_pct": 1.5
    },
    "brand_insights": {
      "top_brand": "未分类",
      "top_brand_count": 65,
      "top_brand_avg_price": 283.7,
      "total_brands": 5
    },
    "regional_distribution": {
      "top_region": "未知",
      "top_region_count": 40,
      "total_regions": 16
    },
    "product_insights": {
      "top_product_title": "万代HG水星的魔女...",
      "top_product_price": 21.8,
      "top_product_sales": 5000,
      "top_product_shop": "鑫哥模型店"
    },
    "data_quality": {
      "brand_coverage": 51,
      "region_coverage": 69,
      "sales_coverage": 99
    }
  }
}
```

---

## 13. 仪表板数据 (Dashboard) 🆕

### GET `/dashboard/`

一次性获取仪表板所需的所有关键数据，减少前端请求次数。

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "overview": { /* 概览数据 */ },
    "price_distribution": [ /* 价格分布 */ ],
    "sales_distribution": [ /* 销量分布 */ ],
    "top_brands": [ /* Top 5 品牌 */ ],
    "top_regions": [ /* Top 5 地区 */ ],
    "top_shops": [ /* Top 5 店铺 */ ],
    "top_products_sales": [ /* Top 5 销量商品 */ ],
    "top_products_price": [ /* Top 5 高价商品 */ ],
    "price_sales_correlation": [ /* 价格销量关联 */ ],
    "market_insights": { /* 市场洞察 */ }
  }
}
```

---

## 使用示例

### JavaScript (前端)

```javascript
// 获取增强概览
import { statisticsApi } from '@/api'

const overview = await statisticsApi.getOverview()

// 获取品牌分析（Top 10）
const brands = await statisticsApi.getBrandAnalysis({ top_n: 10 })

// 获取仪表板数据
const dashboard = await statisticsApi.getDashboard()

// 按价格获取Top商品
const expensiveProducts = await statisticsApi.getTopProducts({
  sort_by: 'price',
  top_n: 10
})
```

### cURL

```bash
# 获取概览
curl -X GET "http://localhost:8000/api/products/statistics/overview/" \
  -H "Authorization: Bearer <token>"

# 获取品牌分析
curl -X GET "http://localhost:8000/api/products/statistics/brand-analysis/?top_n=10" \
  -H "Authorization: Bearer <token>"

# 获取仪表板数据
curl -X GET "http://localhost:8000/api/products/statistics/dashboard/" \
  -H "Authorization: Bearer <token>"
```

---

## 性能优化建议

1. **使用仪表板接口**: 一次性获取所有数据，减少请求次数
2. **合理使用top_n参数**: 避免返回过多数据
3. **利用search参数**: 后端筛选比前端筛选更高效
4. **缓存数据**: 概览数据可以适当缓存

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0 | 2024-02-08 | 全面优化统计接口，新增13个数据分析端点 |
| v1.0 | 2024-02-08 | 初始版本 |

---

最后更新: 2024-02-08
