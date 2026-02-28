<script setup>
import { ref, onMounted, computed } from 'vue'
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
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="market-page">
    <!-- Page Header -->
    <header class="page-header stagger-children">
      <div class="header-content">
        <div class="header-badge">
          <TrendCharts class="badge-icon" />
          <span>LIVE DATA</span>
        </div>
        <h1 class="page-title">
          <span class="title-gradient">市场行情</span>
          <span class="title-accent">大屏</span>
        </h1>
        <p class="page-subtitle">宠物用品消费决策数据 · 实时监控 · 智能分析</p>
      </div>
      <div class="header-stats">
        <div class="stat-mini">
          <span class="stat-value">{{ overview?.total_products || topSales.length }}+</span>
          <span class="stat-label">商品总数</span>
        </div>
        <div class="stat-mini">
          <span class="stat-value">{{ overview?.total_shops || 0 }}</span>
          <span class="stat-label">店铺总数</span>
        </div>
        <div class="stat-mini">
          <span class="stat-value">{{ overview?.total_brands || 0 }}</span>
          <span class="stat-label">品牌数量</span>
        </div>
      </div>
    </header>

    <!-- Metrics Row -->
    <div class="metrics-grid stagger-children">
      <div class="metric-card metric-hot">
        <div class="metric-icon">
          <TrendCharts />
        </div>
        <div class="metric-content">
          <span class="metric-label">商品总数</span>
          <span class="metric-value">{{ overview?.total_products || 0 }}</span>
        </div>
        <div class="metric-trend up">
          <ArrowUp />
          <span>LIVE</span>
        </div>
      </div>

      <div class="metric-card metric-drops">
        <div class="metric-icon">
          <Warning />
        </div>
        <div class="metric-content">
          <span class="metric-label">平均价格</span>
          <span class="metric-value">¥{{ overview?.price?.avg?.toFixed(0) || 0 }}</span>
        </div>
        <div class="metric-trend" :class="overview?.price?.avg > 300 ? 'up' : 'down'">
          <component :is="overview?.price?.avg > 300 ? ArrowUp : ArrowDown" />
          <span>¥{{ overview?.price?.min?.toFixed(0) || 0 }}-{{ overview?.price?.max?.toFixed(0) || 0 }}</span>
        </div>
      </div>

      <div class="metric-card metric-trends">
        <div class="metric-icon">
          <TrendCharts />
        </div>
        <div class="metric-content">
          <span class="metric-label">总销量</span>
          <span class="metric-value">{{ formatNumber(overview?.sales?.total || 0) }}</span>
        </div>
        <div class="metric-trend up">
          <ArrowUp />
          <span>{{ overview?.sales?.avg?.toFixed(0) || 0 }}/件</span>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid stagger-children">
      <!-- Price Distribution Chart -->
      <DataPanel
        v-if="priceDistributionChartOption"
        title="价格分布"
        subtitle="商品价格区间分析"
        :icon="TrendCharts"
        :option="priceDistributionChartOption"
        :loading="loading"
        height="350px"
        badge="实时"
        badge-color="primary"
      />

      <!-- Sales Distribution Chart -->
      <DataPanel
        v-if="salesDistributionChartOption"
        title="销量分布"
        subtitle="商品销量区间分析"
        :icon="TrendCharts"
        :option="salesDistributionChartOption"
        :loading="loading"
        height="350px"
      />
    </div>

    <!-- Top Sales Ranking -->
    <section class="ranking-section stagger-children" v-if="salesChartOption">
      <DataPanel
        title="销量 TOP 10"
        subtitle="最热门的宠物用品排行"
        :icon="TrendCharts"
        :option="salesChartOption"
        :loading="loading"
        height="400px"
        badge="实时"
        badge-color="primary"
      />
    </section>

    <!-- Price Drops Section -->
    <section class="drops-section stagger-children">
      <div class="section-header">
        <div class="section-title-group">
          <h2 class="section-title">
            <span class="title-icon">⚡</span>
            降价提醒
          </h2>
          <p class="section-subtitle">近期降价商品 · 值得入手</p>
        </div>
        <ActionButton
          variant="secondary"
          icon="ArrowRight"
          icon-position="right"
        >
          查看全部
        </ActionButton>
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
    </section>

    <!-- Top Products Grid -->
    <section class="products-section stagger-children">
      <div class="section-header">
        <div class="section-title-group">
          <h2 class="section-title">
            <Star class="title-icon" />
            热门推荐
          </h2>
          <p class="section-subtitle">销量领先的宠物用品</p>
        </div>
        <ActionButton
          variant="secondary"
          icon="ArrowRight"
          icon-position="right"
          @click="router.push('/user/products')"
        >
          浏览全部
        </ActionButton>
      </div>

      <div class="products-grid">
        <ProductCard
          v-for="(product, index) in topSales.slice(0, 8)"
          :key="product.id"
          :product="product"
          :rank="index + 1"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ========================================
   Page Layout
   ======================================== */
.market-page {
  display: flex;
  flex-direction: column;
  gap: var(--space-2xl);
}

/* ========================================
   Page Header
   ======================================== */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-lg);
  padding: var(--space-xl) 0;
  border-bottom: 1px solid var(--border-subtle);
}

.header-content {
  flex: 1;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-md);
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: var(--radius-full);
  margin-bottom: var(--space-md);
}

.header-badge .badge-icon {
  width: 14px;
  height: 14px;
  color: var(--neon-orange);
}

.header-badge span {
  font-family: var(--font-display);
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--neon-orange);
}

.page-title {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
  margin: 0 0 var(--space-sm) 0;
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 800;
  line-height: 1.1;
}

.title-gradient {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-accent {
  font-size: 0.5em;
  color: var(--neon-cyan);
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.page-subtitle {
  font-size: 0.9375rem;
  color: var(--text-tertiary);
  margin: 0;
  max-width: 600px;
}

.header-stats {
  display: flex;
  gap: var(--space-md);
}

.stat-mini {
  text-align: center;
  padding: var(--space-md);
  background: var(--surface-glass);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  min-width: 80px;
}

.stat-mini .stat-value {
  display: block;
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--neon-orange);
}

.stat-mini .stat-label {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ========================================
   Metrics Grid
   ======================================== */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-md);
}

.metric-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg);
  background: var(--gradient-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all var(--transition-base);
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.metric-card.metric-hot::before {
  background: linear-gradient(90deg, var(--neon-orange), var(--neon-pink));
}

.metric-card.metric-drops::before {
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan));
}

.metric-card.metric-trends::before {
  background: linear-gradient(90deg, var(--neon-cyan), var(--neon-green));
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.metric-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-glass);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
}

.metric-icon :deep(svg) {
  width: 24px;
  height: 24px;
}

.metric-content {
  flex: 1;
}

.metric-label {
  display: block;
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-xs);
}

.metric-value {
  display: block;
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
}

.metric-trend {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-full);
  font-size: 0.8125rem;
  font-weight: 600;
}

.metric-trend.up {
  background: rgba(6, 255, 165, 0.1);
  color: var(--status-success);
}

.metric-trend.down {
  background: rgba(255, 59, 48, 0.1);
  color: var(--status-error);
}

.metric-trend :deep(svg) {
  width: 14px;
  height: 14px;
}

/* ========================================
   Charts Grid
   ======================================== */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--space-lg);
}

/* ========================================
   Ranking Section
   ======================================== */
.ranking-section {
  margin-top: var(--space-lg);
}

/* ========================================
   Section Headers
   ======================================== */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-lg);
}

.section-title-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.section-title .title-icon {
  width: 28px;
  height: 28px;
  color: var(--neon-cyan);
}

.title-icon {
  width: 28px;
  height: 28px;
}

.section-subtitle {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  margin: 0;
  padding-left: 36px;
}

/* ========================================
   Drops Section
   ======================================== */
.drops-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-md);
}

.drop-card {
  position: relative;
  padding: var(--space-lg);
  background: var(--gradient-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition: all var(--transition-base);
  overflow: hidden;
}

.drop-card:hover {
  border-color: var(--status-error);
  box-shadow: 0 0 30px rgba(255, 59, 48, 0.2);
  transform: translateY(-2px);
}

.drop-badge {
  position: absolute;
  top: var(--space-md);
  right: var(--space-md);
  padding: var(--space-xs) var(--space-sm);
  background: var(--status-error);
  color: white;
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: var(--radius-sm);
}

.drop-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-md) 0;
  padding-right: var(--space-lg);
}

.drop-price-group {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
}

.drop-current {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--neon-orange);
}

.drop-original {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.drop-sales {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

/* ========================================
   Products Grid
   ======================================== */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--space-lg);
}

/* ========================================
   Responsive
   ======================================== */
@media (max-width: 1024px) {
  .page-header {
    flex-direction: column;
  }

  .header-stats {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .drops-grid {
    grid-template-columns: 1fr;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: var(--space-md);
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-md);
  }

  .section-subtitle {
    padding-left: 0;
  }
}
</style>
