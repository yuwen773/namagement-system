# 全国 AQI 分布地图改进设计

## 需求背景

当前首页的"全国 AQI 分布"地图使用省级 GeoJSON，只能按省份着色，无法显示已有的 10 个城市（北京、上海、成都、广州、深圳等）的具体位置和数据。

## 解决方案

采用**散点/气泡图**方案：在现有省份地图基础上叠加散点系列，用气泡标记城市位置，气泡颜色反映 AQI 等级。

## 数据流设计

### 当前数据流
```
API /overview/ → rawMapData → mapData (name, value) → MapChart → 省份着色
```

### 改进后数据流
```
API /overview/ → rawMapData → mapData (name, value, longitude, latitude) → MapChart → 省份背景 + 城市散点
```

## 改动点

### 1. Overview.vue - 数据准备

修改 `updateMapData` 函数，传递城市经纬度坐标：

```javascript
const updateMapData = () => {
  const field = metricFields[selectedMetric.value] || 'aqi'
  mapData.value = rawMapData.value
    .filter(item => item && item.city_name && item[field] !== null && item[field] !== undefined)
    .map(item => ({
      name: item.city_name,
      value: item[field],
      // 新增：经纬度坐标
      coord: [item.longitude, item.latitude]
    }))
}
```

### 2. MapChart.vue - ECharts 配置

在现有 `geo` 系列基础上，新增 `scatter` 系列：

```javascript
series: [
  {
    // 现有：省份地图
    type: 'map',
    map: 'china',
    geoIndex: 0,
    // ...
  },
  {
    // 新增：城市散点
    type: 'scatter',  // 或 'effectScatter' 带涟漪效果
    coordinateSystem: 'geo',
    symbol: 'circle',
    symbolSize: (val, params) => {
      // 气泡大小基于 AQI 值，范围 8-25px
      const aqi = params.value[2] || 0
      return Math.max(8, Math.min(25, aqi / 10))
    },
    itemStyle: {
      color: (params) => getAQIColor(params.value[2]),
      shadowBlur: 4,
      shadowColor: 'rgba(0,0,0,0.3)'
    },
    emphasis: {
      scale: 1.2,
      itemStyle: {
        shadowBlur: 10,
        shadowColor: 'rgba(0,0,0,0.5)'
      }
    },
    data: props.data.map(item => ({
      name: item.name,
      value: [...item.coord, item.value]  // [lng, lat, aqi]
    }))
  }
]
```

### 3. 交互增强

- **涟漪效果**：可选 `effectScatter` 让气泡有呼吸效果，突出显示
- **提示框**：散点 hover 时显示城市名称和具体 AQI 值
- **动态大小**：气泡大小随 AQI 数值变化，污染越重气泡越大
- **颜色映射**：保持与现有 AQI 等级一致的颜色

## 可选增强

如果希望同时保留省份聚合显示，可以：

1. 后端增加按省份聚合的 AQI 数据
2. 前端判断：如果某省份有城市数据，则省份显示平均 AQI 颜色
3. 散点覆盖在省份之上显示具体城市

**本次实现先简化为只显示城市散点。**

## 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `frontend/src/views/user/Overview.vue` | 修改 | 传递城市经纬度数据 |
| `frontend/src/components/charts/MapChart.vue` | 修改 | 添加散点系列配置 |
| `docs/plans/2026-02-19-aqi-map-design.md` | 新增 | 本设计文档 |

## 验收标准

1. 首页地图上显示所有 10 个城市的气泡标记
2. 气泡颜色符合 AQI 等级（优=绿，良=黄，轻度=橙，中度=红，重度=紫，严重=深红）
3. 切换 AQI/PM2.5/PM10/O3 时，散点颜色同步变化
4. 鼠标悬停气泡显示城市名称和具体数值
5. 省份地图背景保持不变
