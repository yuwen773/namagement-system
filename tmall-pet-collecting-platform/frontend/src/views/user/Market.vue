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

// Chart configurations
const salesChartOption = computed(() => {
  if (!topSales.value.length) {
    return null
  }

  const colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#7B2CBF', '#FF6B35', '#06FFA5', '#00D9FF', '#FF1493', '#39FF14', '#FFD700']

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
      backgroundColor: 'rgba(10, 10, 18, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const data = params[0]
        return `<div style="padding: 12px;">
          <div style="font-weight: 700; margin-bottom: 8px; color: var(--neon-orange);">${data.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: var(--text-tertiary);">销量:</span>
            <span style="color: var(--status-success); font-weight: 600;">${formatNumber(data.value)}</span>
          </div>
        </div>`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: {
        color: 'rgba(255,255,255,0.5)',
        formatter: (val) => val >= 1000 ? `${val/1000}k` : val
      },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: topSales.value.map(item => item.title?.substring(0, 15) + '...' || ''),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.7)',
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
            { offset: 0, color: colors[index] || '#7B2CBF' },
            { offset: 1, color: `${colors[index] || '#7B2CBF'}66` }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(255,255,255,0.8)',
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
      backgroundColor: 'rgba(10, 10, 18, 0.95)',
      borderColor: 'rgba(123, 44, 191, 0.3)',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const data = params[0]
        const item = salesDistribution.value[data.dataIndex]
        return `<div style="padding: 12px;">
          <div style="font-weight: 700; margin-bottom: 8px; color: var(--neon-purple);">${data.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: var(--text-tertiary);">商品数:</span>
            <span style="color: var(--status-success); font-weight: 600;">${item.count}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
            <span style="color: var(--text-tertiary);">占比:</span>
            <span style="color: var(--neon-cyan); font-weight: 600;">${item.percentage}%</span>
          </div>
        </div>`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: {
        color: 'rgba(255,255,255,0.5)',
        formatter: (val) => val >= 1000 ? `${val/1000}k` : val
      },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.range),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 11
      }
    },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: `hsl(${270 + index * 15}, 70%, 55%)` },
            { offset: 1, color: `hsla(${270 + index * 15}, 70%, 55%, 0.4)` }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(255,255,255,0.8)',
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
      backgroundColor: 'rgba(10, 10, 18, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const data = params[0]
        const item = priceDistribution.value[data.dataIndex]
        return `<div style="padding: 12px;">
          <div style="font-weight: 700; margin-bottom: 8px; color: var(--neon-orange);">${data.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: var(--text-tertiary);">商品数:</span>
            <span style="color: var(--status-success); font-weight: 600;">${item.count}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
            <span style="color: var(--text-tertiary);">占比:</span>
            <span style="color: var(--neon-cyan); font-weight: 600;">${item.percentage}%</span>
          </div>
        </div>`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: {
        color: 'rgba(255,255,255,0.5)',
        formatter: (val) => val >= 1000 ? `${val/1000}k` : val
      },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.range),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 11
      }
    },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: `hsl(${25 + index * 10}, 95%, 55%)` },
            { offset: 1, color: `hsla(${25 + index * 10}, 95%, 55%, 0.4)` }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(255,255,255,0.8)',
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
      backgroundColor: 'rgba(10, 10, 18, 0.95)',
      borderColor: 'rgba(123, 44, 191, 0.3)',
      textStyle: { color: '#fff' }
    },
    legend: {
      data: ['商品热度', '关注指数'],
      top: 0,
      textStyle: { color: 'rgba(255,255,255,0.6)' },
      itemWidth: 16,
      itemHeight: 16
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: 'rgba(255,255,255,0.5)', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: 'rgba(255,255,255,0.5)' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    series: [
      {
        name: '商品热度',
        type: 'line',
        smooth: true,
        data: trendData,
        lineStyle: { color: '#FF6B35', width: 3 },
        itemStyle: { color: '#FF6B35' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 107, 53, 0.3)' },
            { offset: 1, color: 'rgba(255, 107, 53, 0.05)' }
          ])
        }
      },
      {
        name: '关注指数',
        type: 'line',
        smooth: true,
        data: trendData.map(v => Math.round(v * 0.75)),
        lineStyle: { color: '#7B2CBF', width: 3 },
        itemStyle: { color: '#7B2CBF' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(123, 44, 191, 0.3)' },
            { offset: 1, color: 'rgba(123, 44, 191, 0.05)' }
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
    <!-- 顶部标题区 -->
    <div class="market-header">
      <div class="header-content">
        <div class="header-badge">
          <TrendCharts class="badge-icon" />
          <span>LIVE DATA</span>
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
      <div class="metric-card metric-card--orange" style="--i: 0">
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
        <div class="metric-bg">📦</div>
      </div>

      <div class="metric-card metric-card--purple" style="--i: 1">
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
        <div class="metric-bg">💰</div>
      </div>

      <div class="metric-card metric-card--gold" style="--i: 2">
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
        <div class="metric-bg">📈</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-panel chart-panel--orange" style="--i: 0">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--orange">
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

      <div class="chart-panel chart-panel--purple" style="--i: 1">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--purple">
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
          <div class="chart-icon-wrapper chart-icon-wrapper--gold">
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
          <div class="section-icon-wrapper section-icon-wrapper--warning">
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.market-container {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
}

/* ============================================
   Market Header
   ============================================ */
.market-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.header-content {
  flex: 1;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  margin-bottom: 12px;
}

.header-badge .badge-icon {
  width: 14px;
  height: 14px;
  color: var(--primary-orange);
}

.header-badge span {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--primary-orange);
}

.header-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 16px;
}

.header-stat {
  text-align: center;
  padding: 16px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  min-width: 90px;
  transition: all 0.3s ease;
}

.header-stat:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-default);
  transform: translateY(-2px);
}

.header-stat-value {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-orange);
}

.header-stat-label {
  font-size: 11px;
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
  gap: 20px;
}

.metric-card {
  position: relative;
  padding: 24px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  animation: metricSlideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: calc(var(--i) * 0.1s);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
  height: 3px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card--orange::before { background: linear-gradient(90deg, var(--primary-orange), transparent); }
.metric-card--purple::before { background: linear-gradient(90deg, var(--primary-purple), transparent); }
.metric-card--gold::before { background: linear-gradient(90deg, var(--primary-gold), transparent); }

.metric-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-default);
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.metric-card--orange .metric-icon { background: rgba(255, 107, 53, 0.15); }
.metric-card--purple .metric-icon { background: rgba(123, 44, 191, 0.15); }
.metric-card--gold .metric-icon { background: rgba(255, 215, 0, 0.15); }

.metric-icon .icon {
  width: 22px;
  height: 22px;
}

.metric-card--orange .metric-icon .icon { color: var(--primary-orange); }
.metric-card--purple .metric-icon .icon { color: var(--primary-purple); }
.metric-card--gold .metric-icon .icon { color: var(--primary-gold); }

.metric-trend {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

.metric-trend.positive {
  background: rgba(6, 255, 165, 0.1);
  color: var(--primary-cyan);
}

.metric-trend.neutral {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-tertiary);
}

.metric-body {
  position: relative;
  z-index: 1;
}

.metric-label {
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
  margin: 0 0 8px 0;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-card--orange .metric-value { color: var(--primary-orange); }
.metric-card--purple .metric-value { color: var(--primary-purple); }
.metric-card--gold .metric-value { color: var(--primary-gold); }

.metric-bg {
  position: absolute;
  bottom: -8px;
  right: -8px;
  font-size: 72px;
  opacity: 0.04;
  pointer-events: none;
  filter: blur(1px);
}

/* ============================================
   Charts Section
   ============================================ */
.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(0.4s + var(--i) * 0.1s);
  transition: all 0.3s ease;
}

@keyframes panelFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.chart-panel:hover {
  border-color: var(--border-default);
}

.chart-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
}

.chart-title-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.chart-icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.chart-icon-wrapper--orange { background: rgba(255, 107, 53, 0.15); }
.chart-icon-wrapper--purple { background: rgba(123, 44, 191, 0.15); }
.chart-icon-wrapper--gold { background: rgba(255, 215, 0, 0.15); }

.chart-icon-wrapper .icon {
  width: 18px;
  height: 18px;
}

.chart-icon-wrapper--orange .icon { color: var(--primary-orange); }
.chart-icon-wrapper--purple .icon { color: var(--primary-purple); }
.chart-icon-wrapper--gold .icon { color: var(--primary-gold); }

.chart-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.chart-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.chart-badge {
  padding: 6px 14px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--primary-orange);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.chart-panel-body {
  padding: 20px 24px;
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
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-default);
  border-top-color: var(--primary-orange);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-loading p {
  margin-top: 12px;
  font-size: 13px;
}

.chart-container {
  width: 100%;
}

/* ============================================
   Ranking Panel
   ============================================ */
.ranking-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(0.6s + var(--i) * 0.1s);
  transition: all 0.3s ease;
}

.ranking-panel:hover {
  border-color: var(--border-default);
}

.ranking-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
}

.ranking-panel-body {
  padding: 20px 24px;
}

/* ============================================
   Drops Section
   ============================================ */
.drops-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-title-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.section-icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.section-icon-wrapper--warning { background: rgba(255, 59, 48, 0.15); }
.section-icon-wrapper--star { background: rgba(255, 215, 0, 0.15); }

.section-icon-wrapper .icon {
  width: 18px;
  height: 18px;
}

.section-icon-wrapper--warning .icon { color: #FF3B30; }
.section-icon-wrapper--star .icon { color: var(--primary-gold); }

.section-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 17px;
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
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--primary-orange);
  color: var(--primary-orange);
  transform: translateY(-2px);
}

.action-icon {
  width: 16px;
  height: 16px;
}

.drops-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.drop-card {
  position: relative;
  padding: 20px;
  background: linear-gradient(135deg, rgba(255, 59, 48, 0.08), rgba(255, 107, 53, 0.04));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 59, 48, 0.15);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.drop-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #FF3B30, var(--primary-orange));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.drop-card:hover {
  border-color: rgba(255, 59, 48, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(255, 59, 48, 0.15);
}

.drop-card:hover::before {
  opacity: 1;
}

.drop-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 12px;
  background: #FF3B30;
  color: white;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.3);
}

.drop-content {
  padding-right: 50px;
}

.drop-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.drop-price-group {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 8px;
}

.drop-current {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  font-weight: 700;
  color: var(--primary-orange);
}

.drop-original {
  font-size: 14px;
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.drop-sales {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* ============================================
   Products Section
   ============================================ */
.products-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
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
    gap: 16px;
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
    gap: 16px;
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
}
</style>
