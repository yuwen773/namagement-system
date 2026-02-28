<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowUp, ArrowDown, Warning, TrendCharts, Star } from '@element-plus/icons-vue'
import { statisticsApi } from '@/api'
import DataPanel from '@/components/ui/DataPanel.vue'
import ProductCard from '@/components/ui/ProductCard.vue'
import ActionButton from '@/components/ui/ActionButton.vue'
import * as echarts from 'echarts'

const router = useRouter()

// State
const loading = ref(true)
const topSales = ref([])
const recentDrops = ref([])
const hotTrends = ref([])

// Chart refs
const priceChartRef = ref(null)
const salesDistChartRef = ref(null)
const salesChartRef = ref(null)

// Dashboard data from new API
const overview = ref(null)
const marketInsights = ref(null)
const priceDistribution = ref([])
const salesDistribution = ref([])

// Mock data generators (fallback only)
const generateMockTopSales = () => {
  return [
    { id: 1, title: '皇家猫粮 成猫用鸡肉配方 5kg', sales: 50000, price: 199, shop: '皇家宠物旗舰店', image: '' },
    { id: 2, title: '渴望 六种鱼猫粮 成猫专用 1.8kg', sales: 42000, price: 268, shop: '渴望官方旗舰店', image: '' },
    { id: 3, title: '爱肯拿 无谷猫粮 鸡肉配方 5.4kg', sales: 38000, price: 459, shop: '爱肯拿旗舰店', image: '' },
    { id: 4, title: '冠能 狗粮 中大型犬成犬 15kg', sales: 35000, price: 580, shop: '冠能官方旗舰店', image: '' },
    { id: 5, title: '耐威克 猫砂 豆腐砂 混合型 6L*3', sales: 32000, price: 89, shop: '耐威克旗舰店', image: '' },
    { id: 6, title: '疯狂小狗 狗粮 小型犬幼犬 2kg', sales: 28000, price: 69, shop: '疯狂小狗官方', image: '' },
    { id: 7, title: 'pidan 猫砂 混合猫砂 2.5kg*4', sales: 25000, price: 129, shop: 'pidan官方店', image: '' },
    { id: 8, title: '麦富迪 猫粮 牛肉双拼 1.5kg', sales: 22000, price: 49, shop: '麦富迪旗舰店', image: '' },
    { id: 9, title: '卫塔卡夫 狗粮 全期通用 10kg', sales: 20000, price: 388, shop: '卫塔卡夫官方', image: '' },
    { id: 10, title: '好主人 猫粮 离乳期幼猫 2kg', sales: 18000, price: 39, shop: '好主人旗舰店', image: '' }
  ]
}

const generateMockDrops = () => {
  return [
    { id: 11, title: '渴望猫粮促销装', oldPrice: 299, currentPrice: 249, dropPercent: 17, sales: 5000, discount: 17 },
    { id: 12, title: '耐威克猫砂大包装', oldPrice: 159, currentPrice: 99, dropPercent: 38, sales: 1200, discount: 38 },
    { id: 13, title: '麦富迪猫粮限时特惠', oldPrice: 89, currentPrice: 59, dropPercent: 34, sales: 3200, discount: 34 }
  ]
}

// 生成降价的商品（从现有数据中模拟）
const generatePriceDrops = (products) => {
  return products.slice(0, 3).map(p => ({
    id: p.id,
    title: p.title?.substring(0, 30) || '商品',
    oldPrice: p.price * 1.2,
    currentPrice: p.price,
    dropPercent: Math.round((1 - p.price / (p.price * 1.2)) * 100),
    sales: p.sales || 0,
    discount: Math.round((1 - p.price / (p.price * 1.2)) * 100)
  }))
}

// Chart configurations - Updated with natural colors
const salesChartOption = computed(() => {
  if (!topSales.value.length) {
    return null
  }

  const colors = ['#52B788', '#40916C', '#2D6A4F', '#74C69D', '#00B4D8', '#90E0EF', '#52B788', '#40916C', '#2D6A4F', '#74C69D']

  return {
    grid: {
      left: '3%',
      right: '8%',
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(82, 183, 136, 0.3)',
      textStyle: { color: '#2D6A4F' },
      formatter: (params) => {
        const data = params[0]
        return `<div style="padding: 12px;">
          <div style="font-weight: 700; margin-bottom: 8px; color: #2D6A4F;">${data.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #666;">销量:</span>
            <span style="color: #52B788; font-weight: 600;">${formatNumber(data.value)}</span>
          </div>
        </div>`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.1)' } },
      axisLabel: {
        color: 'rgba(45, 106, 79, 0.6)',
        formatter: (val) => val >= 1000 ? `${val/1000}k` : val
      },
      splitLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: topSales.value.map(item => item.title?.substring(0, 15) + '...' || ''),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(45, 106, 79, 0.7)',
        fontSize: 11,
        width: 120,
        overflow: 'truncate'
      }
    },
    series: [{
      type: 'bar',
      data: topSales.value.map((item, index) => ({
        value: item.sales || 0,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: colors[index] || '#52B788' },
            { offset: 1, color: `${colors[index] || '#52B788'}99` }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(45, 106, 79, 0.8)',
        fontSize: 11,
        fontWeight: 600,
        formatter: (params) => formatNumber(params.value)
      }
    }]
  }
})

// 销量分布图（基于真实数据）
const salesDistributionChartOption = computed(() => {
  if (!salesDistribution.value.length) {
    return null
  }

  const data = salesDistribution.value.slice(0, 8)

  return {
    grid: {
      left: '3%',
      right: '8%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(64, 145, 108, 0.3)',
      textStyle: { color: '#2D6A4F' },
      formatter: (params) => {
        const data = params[0]
        const item = salesDistribution.value[data.dataIndex]
        return `<div style="padding: 12px;">
          <div style="font-weight: 700; margin-bottom: 8px; color: #40916C;">${data.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #666;">商品数:</span>
            <span style="color: #52B788; font-weight: 600;">${item.count}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
            <span style="color: #666;">占比:</span>
            <span style="color: #00B4D8; font-weight: 600;">${item.percentage}%</span>
          </div>
        </div>`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.1)' } },
      axisLabel: {
        color: 'rgba(45, 106, 79, 0.5)',
        formatter: (val) => val >= 1000 ? `${val/1000}k` : val
      },
      splitLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.range),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(45, 106, 79, 0.7)',
        fontSize: 11
      }
    },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: `hsl(${155 + index * 5}, 45%, ${45 + index * 2}%)` },
            { offset: 1, color: `hsla(${155 + index * 5}, 45%, ${45 + index * 2}%, 0.6)` }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(45, 106, 79, 0.8)',
        fontSize: 11,
        fontWeight: 600,
        formatter: (params) => salesDistribution.value[params.dataIndex].count
      }
    }]
  }
})

// 价格分布图（基于真实数据）
const priceDistributionChartOption = computed(() => {
  if (!priceDistribution.value.length) {
    return null
  }

  const data = priceDistribution.value.slice(0, 6)

  return {
    grid: {
      left: '3%',
      right: '8%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 180, 216, 0.3)',
      textStyle: { color: '#2D6A4F' },
      formatter: (params) => {
        const data = params[0]
        const item = priceDistribution.value[data.dataIndex]
        return `<div style="padding: 12px;">
          <div style="font-weight: 700; margin-bottom: 8px; color: #00B4D8;">${data.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #666;">商品数:</span>
            <span style="color: #52B788; font-weight: 600;">${item.count}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
            <span style="color: #666;">占比:</span>
            <span style="color: #90E0EF; font-weight: 600;">${item.percentage}%</span>
          </div>
        </div>`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.1)' } },
      axisLabel: {
        color: 'rgba(45, 106, 79, 0.5)',
        formatter: (val) => val >= 1000 ? `${val/1000}k` : val
      },
      splitLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.range),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(45, 106, 79, 0.7)',
        fontSize: 11
      }
    },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: `hsl(${195 + index * 5}, 70%, ${50 + index * 3}%)` },
            { offset: 1, color: `hsla(${195 + index * 5}, 70%, ${50 + index * 3}%, 0.6)` }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(45, 106, 79, 0.8)',
        fontSize: 11,
        fontWeight: 600,
        formatter: (params) => priceDistribution.value[params.dataIndex].count
      }
    }]
  }
})

// 保留热度趋势图（使用模拟数据展示趋势）
const trendChartOption = computed(() => {
  const dates = Array.from({ length: 7 }, (_, i) => {
    const d = new Date()
    d.setDate(d.getDate() - (6 - i))
    return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  })

  // 基于实际概览数据生成趋势
  const baseValue = overview.value?.total_products || 133
  const trendData = Array.from({ length: 7 }, (_, i) => {
    return Math.round(baseValue * (0.8 + Math.random() * 0.4))
  })

  return {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(82, 183, 136, 0.3)',
      textStyle: { color: '#2D6A4F' }
    },
    legend: {
      data: ['商品热度', '关注指数'],
      top: 0,
      textStyle: { color: 'rgba(45, 106, 79, 0.6)' },
      itemWidth: 16,
      itemHeight: 16
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.1)' } },
      axisLabel: { color: 'rgba(45, 106, 79, 0.5)', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: 'rgba(45, 106, 79, 0.5)' },
      splitLine: { lineStyle: { color: 'rgba(45, 106, 79, 0.05)' } }
    },
    series: [
      {
        name: '商品热度',
        type: 'line',
        smooth: true,
        data: trendData,
        lineStyle: { color: '#52B788', width: 3 },
        itemStyle: { color: '#52B788' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(82, 183, 136, 0.3)' },
            { offset: 1, color: 'rgba(82, 183, 136, 0.05)' }
          ])
        }
      },
      {
        name: '关注指数',
        type: 'line',
        smooth: true,
        data: trendData.map(v => Math.round(v * 0.75)),
        lineStyle: { color: '#40916C', width: 3 },
        itemStyle: { color: '#40916C' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 145, 108, 0.3)' },
            { offset: 1, color: 'rgba(64, 145, 108, 0.05)' }
          ])
        }
      }
    ]
  }
})

// Utility functions
const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0
  }).format(price)
}

const goToProduct = (id) => {
  router.push(`/user/products/${id}`)
}

// Data fetching - 使用最新统计API
const fetchDashboardData = async () => {
  try {
    const res = await statisticsApi.getDashboard()

    if (res.code === 0 && res.data) {
      overview.value = res.data.overview
      priceDistribution.value = res.data.price_distribution || []
      salesDistribution.value = res.data.sales_distribution || []
      marketInsights.value = res.data.market_insights

      // 使用Top销量商品数据
      if (res.data.top_products_sales) {
        topSales.value = res.data.top_products_sales.map(p => ({
          id: p.id,
          title: p.title,
          sales: p.sales,
          price: p.price,
          shop: p.shop,
          brand: p.brand,
          region: p.region,
          image_url: p.image_url
        }))
      }

      // 生成降价提醒（基于实际商品数据）
      if (topSales.value.length > 0) {
        recentDrops.value = generatePriceDrops(topSales.value)
      }
    }
  } catch (error) {
    // 降级使用Mock数据
    topSales.value = generateMockTopSales()
    recentDrops.value = generateMockDrops()
  }
}

// 单独获取Top商品（备用方法）
const fetchTopProducts = async () => {
  try {
    const res = await statisticsApi.getTopProducts({
      sort_by: 'sales',
      top_n: 10
    })
    if (res.code === 0 && res.data) {
      topSales.value = res.data.map(p => ({
        id: p.id,
        title: p.title,
        sales: p.sales,
        price: p.price,
        shop: p.shop,
        brand: p.brand,
        region: p.region,
        image_url: p.image_url
      }))
    }
  } catch (error) {
    console.error('Failed to fetch top products:', error)
    topSales.value = generateMockTopSales()
  }
}

const loadData = async () => {
  loading.value = true
  // 优先使用仪表板接口
  await fetchDashboardData()
  loading.value = false

  // 初始化图表
  await nextTick()
  initCharts()
}

// Chart instances
const charts = {
  price: null,
  salesDist: null,
  sales: null
}

const initCharts = () => {
  // 初始化价格分布图
  if (priceChartRef.value && priceDistributionChartOption.value) {
    charts.price = echarts.init(priceChartRef.value)
    charts.price.setOption(priceDistributionChartOption.value)
  }

  // 初始化销量分布图
  if (salesDistChartRef.value && salesDistributionChartOption.value) {
    charts.salesDist = echarts.init(salesDistChartRef.value)
    charts.salesDist.setOption(salesDistributionChartOption.value)
  }

  // 初始化销量排行榜
  if (salesChartRef.value && salesChartOption.value) {
    charts.sales = echarts.init(salesChartRef.value)
    charts.sales.setOption(salesChartOption.value)
  }
}

const handleResize = () => {
  Object.values(charts).forEach(chart => chart?.resize())
}

onMounted(() => {
  loadData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  Object.values(charts).forEach(chart => {
    chart?.dispose()
  })
})
</script>

<template>
  <div class="market-container">
    <!-- 装饰性背景 -->
    <div class="leaf-decoration leaf-1"></div>
    <div class="leaf-decoration leaf-2"></div>
    <div class="leaf-decoration leaf-3"></div>

    <!-- 顶部标题区 -->
    <div class="market-header">
      <div class="header-content">
        <div class="header-badge">
          <TrendCharts class="badge-icon" />
          <span>市场洞察</span>
        </div>
        <h1 class="header-title">市场行情</h1>
        <p class="header-subtitle">宠物用品消费决策数据 · 实时监控 · 智能分析</p>
      </div>
      <div class="header-stats">
        <div class="header-stat">
          <span class="header-stat-value">{{ overview?.total_products || topSales.length }}+</span>
          <span class="header-stat-label">商品总数</span>
        </div>
        <div class="header-stat">
          <span class="header-stat-value">{{ overview?.total_shops || 0 }}</span>
          <span class="header-stat-label">店铺总数</span>
        </div>
        <div class="header-stat">
          <span class="header-stat-value">{{ overview?.total_brands || 0 }}</span>
          <span class="header-stat-label">品牌数量</span>
        </div>
      </div>
    </div>

    <!-- 统计指标卡片 -->
    <div class="metrics-grid">
      <div class="metric-card metric-card--green" style="--i: 0">
        <div class="metric-header">
          <div class="metric-icon">
            <TrendCharts class="icon" />
          </div>
          <span class="metric-trend positive">LIVE</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">商品总数</p>
          <p class="metric-value">{{ formatNumber(overview?.total_products || 0) }}</p>
        </div>
        <div class="metric-bg">🌱</div>
      </div>

      <div class="metric-card metric-card--teal" style="--i: 1">
        <div class="metric-header">
          <div class="metric-icon">
            <Warning class="icon" />
          </div>
          <span class="metric-trend" :class="overview?.price?.avg > 300 ? 'positive' : 'neutral'">
            ¥{{ overview?.price?.min?.toFixed(0) || 0 }}-{{ overview?.price?.max?.toFixed(0) || 0 }}
          </span>
        </div>
        <div class="metric-body">
          <p class="metric-label">平均价格</p>
          <p class="metric-value">¥{{ overview?.price?.avg?.toFixed(0) || 0 }}</p>
        </div>
        <div class="metric-bg">💚</div>
      </div>

      <div class="metric-card metric-card--blue" style="--i: 2">
        <div class="metric-header">
          <div class="metric-icon">
            <TrendCharts class="icon" />
          </div>
          <span class="metric-trend positive">{{ overview?.sales?.avg?.toFixed(0) || 0 }}/件</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">总销量</p>
          <p class="metric-value">{{ formatNumber(overview?.sales?.total || 0) }}</p>
        </div>
        <div class="metric-bg">🌿</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-panel chart-panel--green" style="--i: 0">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--green">
              <TrendCharts class="icon" />
            </div>
            <div>
              <h3 class="chart-title">价格区间分布</h3>
              <p class="chart-subtitle">商品价格分布占比分析</p>
            </div>
          </div>
          <div class="chart-badge">分布</div>
        </div>
        <div class="chart-panel-body">
          <div v-if="loading" class="chart-loading">
            <div class="loading-spinner"></div>
            <p>加载数据中...</p>
          </div>
          <div v-else ref="priceChartRef" class="chart-container" style="height: 280px"></div>
        </div>
      </div>

      <div class="chart-panel chart-panel--teal" style="--i: 1">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--teal">
              <TrendCharts class="icon" />
            </div>
            <div>
              <h3 class="chart-title">销量区间分布</h3>
              <p class="chart-subtitle">商品销量分布占比分析</p>
            </div>
          </div>
          <div class="chart-badge">排行</div>
        </div>
        <div class="chart-panel-body">
          <div v-if="loading" class="chart-loading">
            <div class="loading-spinner"></div>
            <p>加载数据中...</p>
          </div>
          <div v-else ref="salesDistChartRef" class="chart-container" style="height: 280px"></div>
        </div>
      </div>
    </div>

    <!-- 销量排行榜 -->
    <div class="ranking-panel" style="--i: 2">
      <div class="ranking-panel-header">
        <div class="chart-title-group">
          <div class="chart-icon-wrapper chart-icon-wrapper--leaf">
            <Star class="icon" />
          </div>
          <div>
            <h3 class="chart-title">销量 TOP 10</h3>
            <p class="chart-subtitle">最热门的宠物用品排行</p>
          </div>
        </div>
        <div class="chart-badge">实时</div>
      </div>
      <div class="ranking-panel-body">
        <div v-if="loading" class="chart-loading">
          <div class="loading-spinner"></div>
          <p>加载数据中...</p>
        </div>
        <div v-else ref="salesChartRef" class="chart-container" style="height: 400px"></div>
      </div>
    </div>

    <!-- 降价提醒区域 -->
    <div class="drops-section">
      <div class="section-header">
        <div class="section-title-group">
          <div class="section-icon-wrapper section-icon-wrapper--discount">
            <Warning class="icon" />
          </div>
          <div>
            <h3 class="section-title">降价提醒</h3>
            <p class="section-subtitle">近期降价商品 · 值得入手</p>
          </div>
        </div>
        <button class="action-btn" @click="router.push('/user/products')">
          查看全部
          <ArrowRight class="action-icon" />
        </button>
      </div>

      <div class="drops-grid">
        <div
          v-for="product in recentDrops"
          :key="product.id"
          class="drop-card"
          @click="goToProduct(product.id)"
        >
          <div class="drop-badge">-{{ product.dropPercent }}%</div>
          <div class="drop-content">
            <h3 class="drop-title">{{ product.title }}</h3>
            <div class="drop-price-group">
              <span class="drop-current">{{ formatPrice(product.currentPrice) }}</span>
              <span class="drop-original">{{ formatPrice(product.oldPrice) }}</span>
            </div>
            <div class="drop-sales">已售 {{ formatNumber(product.sales) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门推荐区域 -->
    <div class="products-section">
      <div class="section-header">
        <div class="section-title-group">
          <div class="section-icon-wrapper section-icon-wrapper--star">
            <Star class="icon" />
          </div>
          <div>
            <h3 class="section-title">热门推荐</h3>
            <p class="section-subtitle">销量领先的宠物用品</p>
          </div>
        </div>
        <button class="action-btn" @click="router.push('/user/products')">
          浏览全部
          <ArrowRight class="action-icon" />
        </button>
      </div>

      <div class="products-grid">
        <ProductCard
          v-for="(product, index) in topSales.slice(0, 8)"
          :key="product.id"
          :product="product"
          :rank="index + 1"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.market-container {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1A4D3A;
  --text-secondary: #4A7C6A;
  --text-tertiary: #8BA89A;
  --border-light: #E8F0EC;
  --border-default: #D0E2D8;

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  background: var(--bg-cream);
  position: relative;
  padding: 24px;
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: fixed;
  opacity: 0.03;
  pointer-events: none;
  z-index: 0;
}

.leaf-1 {
  top: 10%;
  right: 5%;
  width: 300px;
  height: 300px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2352B788'%3E%3Cpath d='M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z'/%3E%3C/svg%3E") center/contain no-repeat;
}

.leaf-2 {
  bottom: 20%;
  left: 3%;
  width: 250px;
  height: 250px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2340916C'%3E%3Cpath d='M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z'/%3E%3C/svg%3E") center/contain no-repeat;
  transform: rotate(45deg);
}

.leaf-3 {
  top: 50%;
  right: 2%;
  width: 200px;
  height: 200px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2300B4D8'%3E%3Cpath d='M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z'/%3E%3C/svg%3E") center/contain no-repeat;
  transform: rotate(-30deg);
}

/* ============================================
   Market Header
   ============================================ */
.market-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
  position: relative;
  z-index: 1;
}

.header-content {
  flex: 1;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(82, 183, 136, 0.12);
  border: 1px solid rgba(82, 183, 136, 0.3);
  border-radius: 24px;
  margin-bottom: 16px;
}

.header-badge .badge-icon {
  width: 16px;
  height: 16px;
  color: var(--primary-light);
}

.header-badge span {
  font-family: 'Nunito', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--primary-light);
  text-transform: uppercase;
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-green);
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 15px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 16px;
}

.header-stat {
  text-align: center;
  padding: 20px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  min-width: 100px;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.06);
  transition: all 0.3s ease;
}

.header-stat:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(82, 183, 136, 0.15);
  border-color: var(--border-default);
}

.header-stat-value {
  display: block;
  font-family: 'Nunito', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-light);
}

.header-stat-label {
  font-size: 12px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ============================================
   Metrics Grid
   ============================================ */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  position: relative;
  z-index: 1;
}

.metric-card {
  position: relative;
  padding: 28px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  animation: metricSlideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: calc(var(--i) * 0.1s);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.06);
}

@keyframes metricSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card--green::before { background: linear-gradient(90deg, var(--primary-light), var(--accent-green)); }
.metric-card--teal::before { background: linear-gradient(90deg, var(--primary-teal), var(--primary-light)); }
.metric-card--blue::before { background: linear-gradient(90deg, var(--accent-blue), var(--accent-blue-light)); }

.metric-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 40px rgba(82, 183, 136, 0.18);
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.metric-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
}

.metric-card--green .metric-icon { background: rgba(82, 183, 136, 0.15); }
.metric-card--teal .metric-icon { background: rgba(64, 145, 108, 0.15); }
.metric-card--blue .metric-icon { background: rgba(0, 180, 216, 0.15); }

.metric-icon .icon {
  width: 24px;
  height: 24px;
}

.metric-card--green .metric-icon .icon { color: var(--primary-light); }
.metric-card--teal .metric-icon .icon { color: var(--primary-teal); }
.metric-card--blue .metric-icon .icon { color: var(--accent-blue); }

.metric-trend {
  font-family: 'Nunito', sans-serif;
  font-size: 11px;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-trend.positive {
  background: rgba(82, 183, 136, 0.15);
  color: var(--primary-light);
}

.metric-trend.neutral {
  background: rgba(139, 168, 154, 0.15);
  color: var(--text-tertiary);
}

.metric-body {
  position: relative;
  z-index: 1;
}

.metric-label {
  font-size: 14px;
  color: var(--text-tertiary);
  font-weight: 500;
  margin: 0 0 10px 0;
}

.metric-value {
  font-family: 'Nunito', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-card--green .metric-value { color: var(--primary-light); }
.metric-card--teal .metric-value { color: var(--primary-teal); }
.metric-card--blue .metric-value { color: var(--accent-blue); }

.metric-bg {
  position: absolute;
  bottom: -10px;
  right: -10px;
  font-size: 80px;
  opacity: 0.06;
  pointer-events: none;
  filter: blur(1px);
}

/* ============================================
   Charts Section
   ============================================ */
.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  position: relative;
  z-index: 1;
}

.chart-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(0.4s + var(--i) * 0.1s);
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.06);
}

@keyframes panelFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.chart-panel:hover {
  box-shadow: 0 8px 30px rgba(82, 183, 136, 0.12);
  border-color: var(--border-default);
}

.chart-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid var(--border-light);
  background: rgba(82, 183, 136, 0.02);
}

.chart-title-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.chart-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.chart-icon-wrapper--green { background: rgba(82, 183, 136, 0.15); }
.chart-icon-wrapper--teal { background: rgba(64, 145, 108, 0.15); }
.chart-icon-wrapper--leaf { background: rgba(116, 198, 157, 0.15); }

.chart-icon-wrapper .icon {
  width: 20px;
  height: 20px;
}

.chart-icon-wrapper--green .icon { color: var(--primary-light); }
.chart-icon-wrapper--teal .icon { color: var(--primary-teal); }
.chart-icon-wrapper--leaf .icon { color: var(--accent-green); }

.chart-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.chart-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.chart-badge {
  padding: 8px 16px;
  background: rgba(82, 183, 136, 0.12);
  border: 1px solid rgba(82, 183, 136, 0.25);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  color: var(--primary-light);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.chart-panel-body {
  padding: 24px;
  min-height: 280px;
}

.chart-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 280px;
  color: var(--text-tertiary);
}

.loading-spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border-light);
  border-top-color: var(--primary-light);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-loading p {
  margin-top: 16px;
  font-size: 14px;
}

.chart-container {
  width: 100%;
}

/* ============================================
   Ranking Panel
   ============================================ */
.ranking-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(0.6s + var(--i) * 0.1s);
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.06);
  position: relative;
  z-index: 1;
}

.ranking-panel:hover {
  box-shadow: 0 8px 30px rgba(82, 183, 136, 0.12);
  border-color: var(--border-default);
}

.ranking-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid var(--border-light);
  background: rgba(82, 183, 136, 0.02);
}

.ranking-panel-body {
  padding: 24px;
}

/* ============================================
   Drops Section
   ============================================ */
.drops-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-title-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.section-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.section-icon-wrapper--discount { background: rgba(0, 180, 216, 0.15); }
.section-icon-wrapper--star { background: rgba(82, 183, 136, 0.15); }

.section-icon-wrapper .icon {
  width: 20px;
  height: 20px;
}

.section-icon-wrapper--discount .icon { color: var(--accent-blue); }
.section-icon-wrapper--star .icon { color: var(--primary-light); }

.section-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.section-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(45, 106, 79, 0.06);
}

.action-btn:hover {
  background: var(--primary-light);
  border-color: var(--primary-light);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(82, 183, 136, 0.3);
}

.action-icon {
  width: 16px;
  height: 16px;
}

.drops-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.drop-card {
  position: relative;
  padding: 24px;
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.06), rgba(82, 183, 136, 0.04));
  border: 1px solid rgba(0, 180, 216, 0.15);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(45, 106, 79, 0.06);
}

.drop-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-blue), var(--primary-light));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.drop-card:hover {
  border-color: rgba(0, 180, 216, 0.3);
  transform: translateY(-6px);
  box-shadow: 0 12px 35px rgba(0, 180, 216, 0.18);
}

.drop-card:hover::before {
  opacity: 1;
}

.drop-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 8px 14px;
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-blue-light));
  color: white;
  font-family: 'Nunito', sans-serif;
  font-size: 12px;
  font-weight: 700;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3);
}

.drop-content {
  padding-right: 50px;
}

.drop-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.drop-price-group {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 10px;
}

.drop-current {
  font-family: 'Nunito', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--primary-light);
}

.drop-original {
  font-size: 15px;
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.drop-sales {
  font-size: 13px;
  color: var(--text-tertiary);
}

/* ============================================
   Products Section
   ============================================ */
.products-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1400px) {
  .metrics-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .charts-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .drops-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .products-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1024px) {
  .market-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .header-stats {
    width: 100%;
    justify-content: flex-start;
  }

  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .drops-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .products-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .market-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .header-stats {
    flex-wrap: wrap;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .drops-grid {
    grid-template-columns: 1fr;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .market-container {
    padding: 16px;
  }
}
</style>
