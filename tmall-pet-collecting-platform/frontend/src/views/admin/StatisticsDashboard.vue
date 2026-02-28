<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { statisticsApi } from '@/api'
import { TrendCharts, ShoppingCart, ShoppingBag, Wallet, DataAnalysis, Location, Collection, Refresh, Loading } from '@element-plus/icons-vue'
import MetricCard from './components/MetricCard.vue'
import ChartSection from './components/ChartSection.vue'
import BrandAnalysis from './components/BrandAnalysis.vue'
import TopProducts from './components/TopProducts.vue'
import MarketInsights from './components/MarketInsights.vue'
import RegionAnalysis from './components/RegionAnalysis.vue'

const loading = ref(true)
const refreshing = ref(false)
const error = ref(null)
const dashboardData = ref(null)

const activeSort = ref('sales')
const selectedBrand = ref('')
const selectedRegion = ref('')

const chartInstances = ref([])

const loadData = async () => {
  try {
    error.value = null
    if (refreshing.value) {
      await new Promise(resolve => setTimeout(resolve, 800))
    }

    const params = {}
    if (selectedBrand.value) params.brand = selectedBrand.value
    if (selectedRegion.value) params.region = selectedRegion.value

    const res = await statisticsApi.getDashboard(params)
    if (res.code === 0) {
      dashboardData.value = res.data
    } else {
      throw new Error(res.message || '加载失败')
    }
  } catch (err) {
    error.value = err.message
    console.error('Failed to load dashboard data:', err)
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const handleRefresh = async () => {
  refreshing.value = true
  await loadData()
}

const handleSortChange = (sortType) => {
  activeSort.value = sortType
}

const handleFilterChange = () => {
  loading.value = true
  loadData()
}

const formatNumber = (num) => {
  if (!num) return '0'
  return new Intl.NumberFormat('zh-CN').format(num)
}

const formatPrice = (price) => {
  if (!price) return '¥0.00'
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2
  }).format(price)
}

const overviewMetrics = computed(() => {
  if (!dashboardData.value?.overview) return []
  const ov = dashboardData.value.overview
  return [
    {
      label: '商品总数',
      value: formatNumber(ov.total_products),
      icon: ShoppingBag,
      color: '#2D6A4F',
      gradient: 'from-emerald-600 to-teal-600',
      detail: `+${ov.completeness_pct?.with_sales_pct || 0}% 有销量`
    },
    {
      label: '店铺数量',
      value: formatNumber(ov.total_shops),
      icon: ShoppingCart,
      color: '#00B4D8',
      gradient: 'from-cyan-500 to-blue-500',
      detail: `${ov.total_regions || 0} 个地区`
    },
    {
      label: '品牌数量',
      value: formatNumber(ov.total_brands || 0),
      icon: Collection,
      color: '#52B788',
      gradient: 'from-emerald-400 to-green-500',
      detail: `${ov.completeness_pct?.with_brand_pct || 0}% 覆盖率`
    },
    {
      label: '平均价格',
      value: formatPrice(ov.price?.avg || 0),
      icon: Wallet,
      color: '#40916C',
      gradient: 'from-teal-500 to-emerald-500',
      detail: `¥${ov.price?.min?.toFixed(0)} - ¥${ov.price?.max?.toFixed(0)}`
    },
    {
      label: '总销量',
      value: formatNumber(ov.sales?.total || 0),
      icon: TrendCharts,
      color: '#74C69D',
      gradient: 'from-green-400 to-emerald-400',
      detail: `平均 ${formatNumber(ov.sales?.avg || 0)}`
    },
    {
      label: '数据质量',
      value: `${Math.round(
        ((ov.completeness_pct?.with_brand_pct || 0) +
         (ov.completeness_pct?.with_region_pct || 0) +
         (ov.completeness_pct?.with_sales_pct || 0)) / 3
      )}%`,
      icon: DataAnalysis,
      color: '#90E0EF',
      gradient: 'from-cyan-300 to-teal-300',
      detail: '品牌/地区/销量'
    }
  ]
})

const availableBrands = computed(() => {
  return dashboardData.value?.top_brands?.map(b => b.brand) || []
})

const availableRegions = computed(() => {
  return dashboardData.value?.top_regions?.map(r => r.region) || []
})

let refreshInterval = null

onMounted(() => {
  loadData()
  refreshInterval = setInterval(() => {
    if (!loading.value && !refreshing.value) {
      loadData()
    }
  }, 300000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  chartInstances.value.forEach(chart => {
    if (chart?.dispose) chart.dispose()
  })
})
</script>

<template>
  <div class="stats-dashboard">
    <!-- Leaf Decoration Top Left -->
    <div class="leaf-decoration leaf-decoration--top-left">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 95C50 95 20 80 15 50C10 20 30 5 50 5C70 5 90 20 85 50C80 80 50 95 50 95Z" fill="url(#leafGradient1)" opacity="0.3"/>
        <path d="M50 90C50 90 25 75 20 50C15 25 35 10 50 10C65 10 85 25 80 50C75 75 50 90 50 90Z" fill="url(#leafGradient2)" opacity="0.5"/>
        <path d="M50 5L50 95M50 50C35 40 20 45 15 50M50 50C65 40 80 45 85 50M50 30C40 25 30 20 25 15M50 30C60 25 70 20 75 15" stroke="#40916C" stroke-width="1" opacity="0.3"/>
        <defs>
          <linearGradient id="leafGradient1" x1="15" y1="5" x2="85" y2="95" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#74C69D"/>
            <stop offset="100%" stop-color="#2D6A4F"/>
          </linearGradient>
          <linearGradient id="leafGradient2" x1="20" y1="10" x2="80" y2="90" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#52B788"/>
            <stop offset="100%" stop-color="#40916C"/>
          </linearGradient>
        </defs>
      </svg>
    </div>

    <!-- Leaf Decoration Bottom Right -->
    <div class="leaf-decoration leaf-decoration--bottom-right">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 95C50 95 20 80 15 50C10 20 30 5 50 5C70 5 90 20 85 50C80 80 50 95 50 95Z" fill="url(#leafGradient3)" opacity="0.3"/>
        <path d="M50 90C50 90 25 75 20 50C15 25 35 10 50 10C65 10 85 25 80 50C75 75 50 90 50 90Z" fill="url(#leafGradient4)" opacity="0.5"/>
        <path d="M50 5L50 95M50 50C35 40 20 45 15 50M50 50C65 40 80 45 85 50M50 30C40 25 30 20 25 15M50 30C60 25 70 20 75 15" stroke="#00B4D8" stroke-width="1" opacity="0.3"/>
        <defs>
          <linearGradient id="leafGradient3" x1="15" y1="5" x2="85" y2="95" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#90E0EF"/>
            <stop offset="100%" stop-color="#00B4D8"/>
          </linearGradient>
          <linearGradient id="leafGradient4" x1="20" y1="10" x2="80" y2="90" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#90E0EF"/>
            <stop offset="100%" stop-color="#00B4D8"/>
          </linearGradient>
        </defs>
      </svg>
    </div>

    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-icon-wrapper">
          <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3V21H21" stroke="url(#headerIconGrad)" stroke-width="2" stroke-linecap="round"/>
            <path d="M7 14L11 10L15 14L19 8" stroke="url(#headerIconGrad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="headerIconGrad" x1="3" y1="3" x2="21" y2="21" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#2D6A4F"/>
                <stop offset="100%" stop-color="#00B4D8"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div>
          <h1 class="header-title">宠物用品统计分析</h1>
          <p class="header-subtitle">天猫宠物用品数据洞察与可视化分析</p>
        </div>
      </div>
      <div class="header-actions">
        <button class="refresh-btn" @click="handleRefresh" :class="{ loading: refreshing }">
          <Loading class="icon" :class="{ spinning: refreshing }" />
          <span>刷新数据</span>
        </button>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-group">
        <label class="filter-label">
          <Location class="filter-icon" />
          地区筛选
        </label>
        <el-select
          v-model="selectedRegion"
          placeholder="全部地区"
          clearable
          @change="handleFilterChange"
          class="filter-select"
        >
          <el-option
            v-for="region in availableRegions"
            :key="region"
            :label="region || '未分类'"
            :value="region"
          />
        </el-select>
      </div>

      <div class="filter-group">
        <label class="filter-label">
          <Collection class="filter-icon" />
          品牌筛选
        </label>
        <el-select
          v-model="selectedBrand"
          placeholder="全部品牌"
          clearable
          @change="handleFilterChange"
          class="filter-select"
        >
          <el-option
            v-for="brand in availableBrands"
            :key="brand"
            :label="brand || '未分类'"
            :value="brand"
          />
        </el-select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner">
        <Loading class="loading-icon spinning" />
        <div class="loading-dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
      <p class="loading-text">加载数据中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-content">
        <div class="error-icon-wrapper">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="#E76F51" stroke-width="2"/>
            <path d="M12 8V12M12 16H12.01" stroke="#E76F51" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <p class="error-message">{{ error }}</p>
        <el-button @click="loadData" type="primary" class="retry-btn">重试</el-button>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Metrics Section -->
      <section class="metrics-section">
        <div class="section-header">
          <h2 class="section-title">数据概览</h2>
          <p class="section-subtitle">核心业务指标一览</p>
        </div>
        <div class="metrics-grid">
          <MetricCard
            v-for="(metric, index) in overviewMetrics"
            :key="metric.label"
            :metric="metric"
            :style="{ '--i': index }"
          />
        </div>
      </section>

      <!-- Charts Section -->
      <section class="charts-section">
        <div class="section-header">
          <h2 class="section-title">趋势分析</h2>
          <p class="section-subtitle">价格、销量与品牌数据可视化</p>
        </div>
        <div class="charts-row">
          <ChartSection
            title="价格分布"
            subtitle="商品价格区间分布情况"
            type="price-distribution"
            :data="dashboardData?.price_distribution"
            class="chart-panel"
            style="--i: 0"
          />

          <ChartSection
            title="销量分布"
            subtitle="商品销量区间分布情况"
            type="sales-distribution"
            :data="dashboardData?.sales_distribution"
            class="chart-panel"
            style="--i: 1"
          />
        </div>

        <div class="charts-row">
          <BrandAnalysis
            :data="dashboardData?.top_brands"
            class="chart-panel"
            style="--i: 2"
          />

          <RegionAnalysis
            :data="dashboardData?.top_regions"
            class="chart-panel"
            style="--i: 3"
          />
        </div>

        <div class="charts-row charts-row--full">
          <ChartSection
            title="价格-销量关联分析"
            subtitle="不同价格区间的平均销量表现"
            type="price-sales-correlation"
            :data="dashboardData?.price_sales_correlation"
            class="chart-panel"
            style="--i: 4"
          />
        </div>
      </section>

      <!-- Products Section -->
      <section class="products-section">
        <TopProducts
          :sales-products="dashboardData?.top_products_sales"
          :price-products="dashboardData?.top_products_price"
          :active-sort="activeSort"
          @sort-change="handleSortChange"
        />
      </section>

      <!-- Insights Section -->
      <section class="insights-section">
        <MarketInsights
          :insights="dashboardData?.market_insights"
        />
      </section>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.stats-dashboard {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);
  --shadow-card: 0 2px 12px rgba(45, 106, 79, 0.06);

  position: relative;
  display: flex;
  flex-direction: column;
  gap: 28px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  background: linear-gradient(135deg, var(--bg-cream) 0%, var(--bg-sand) 100%);
  min-height: 100vh;
  padding: 32px;
  overflow-x: hidden;
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: fixed;
  width: 180px;
  height: 180px;
  pointer-events: none;
  z-index: 0;
  opacity: 0.8;
}

.leaf-decoration--top-left {
  top: -40px;
  left: -40px;
  animation: leafFloat1 8s ease-in-out infinite;
}

.leaf-decoration--bottom-right {
  bottom: -40px;
  right: -40px;
  animation: leafFloat2 10s ease-in-out infinite;
}

@keyframes leafFloat1 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(15px, 15px) rotate(5deg); }
}

@keyframes leafFloat2 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(-15px, -15px) rotate(-5deg); }
}

/* ============================================
   Dashboard Header
   ============================================ */
.dashboard-header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  background: var(--bg-card);
  border-radius: 20px;
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--border-light);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
}

.header-icon-wrapper {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-teal) 50%, var(--accent-blue) 100%);
  border-radius: 16px;
  box-shadow: var(--shadow-card);
}

.header-icon {
  width: 28px;
  height: 28px;
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.refresh-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent-green) 100%);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 14px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(82, 183, 136, 0.3);
  overflow: hidden;
}

.refresh-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--accent-green) 0%, var(--primary-teal) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.refresh-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(82, 183, 136, 0.4);
}

.refresh-btn:hover::before {
  opacity: 1;
}

.refresh-btn:active {
  transform: translateY(0);
}

.refresh-btn.loading {
  pointer-events: none;
  opacity: 0.8;
}

.refresh-btn .icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
  position: relative;
  z-index: 1;
}

.refresh-btn span {
  position: relative;
  z-index: 1;
}

.refresh-btn .icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============================================
   Filter Bar
   ============================================ */
.filter-bar {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 24px;
  padding: 20px 28px;
  background: var(--bg-card);
  border-radius: 16px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--border-light);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  font-family: 'Noto Serif SC', serif;
}

.filter-icon {
  width: 18px;
  height: 18px;
  color: var(--primary-teal);
}

.filter-select {
  width: 200px;
}

.filter-select :deep(.el-input__wrapper) {
  background: var(--bg-sand);
  border: 2px solid var(--border-light);
  box-shadow: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  padding: 6px 14px;
}

.filter-select :deep(.el-input__wrapper:hover) {
  border-color: var(--accent-green);
  background: white;
}

.filter-select :deep(.el-input__wrapper.is-focus) {
  border-color: var(--border-focus);
  background: white;
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.filter-select :deep(.el-input__inner) {
  color: var(--text-primary);
  font-weight: 500;
}

.filter-select :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

.filter-select :deep(.el-select__placeholder) {
  color: var(--text-tertiary);
}

/* ============================================
   Section Headers
   ============================================ */
.section-header {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 20px;
}

.section-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.section-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 500;
}

/* ============================================
   Loading & Error States
   ============================================ */
.loading-state,
.error-state {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  padding: 60px;
  background: var(--bg-card);
  border-radius: 24px;
  box-shadow: var(--shadow-soft);
}

.loading-spinner {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
}

.loading-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  color: var(--primary-teal);
}

.loading-icon.spinning {
  animation: spin 1s linear infinite;
}

.loading-dots {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 8px;
}

.loading-dots .dot {
  width: 8px;
  height: 8px;
  background: var(--accent-green);
  border-radius: 50%;
  animation: dotPulse 1.4s ease-in-out infinite;
}

.loading-dots .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotPulse {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.loading-text {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 600;
  font-family: 'Noto Serif SC', serif;
}

.error-content {
  text-align: center;
}

.error-icon-wrapper {
  width: 72px;
  height: 72px;
  margin: 0 auto 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFF5F5 0%, #FED7D7 100%);
  border-radius: 20px;
}

.error-icon {
  width: 36px;
  height: 36px;
}

.error-message {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0 0 28px 0;
  font-weight: 500;
}

.retry-btn {
  padding: 14px 32px !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
}

/* ============================================
   Dashboard Content
   ============================================ */
.dashboard-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 32px;
  animation: contentFadeIn 0.5s ease-out;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ============================================
   Metrics Section
   ============================================ */
.metrics-section {
  animation: sectionSlideIn 0.6s ease-out 0.1s both;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
}

/* ============================================
   Charts Section
   ============================================ */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: sectionSlideIn 0.6s ease-out 0.2s both;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.charts-row--full {
  grid-template-columns: 1fr;
}

.chart-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-card);
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(var(--i) * 0.1s);
  transition: all 0.3s ease;
}

@keyframes panelFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.chart-panel:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
  border-color: var(--accent-green);
}

/* ============================================
   Products & Insights Sections
   ============================================ */
.products-section,
.insights-section {
  animation: sectionSlideIn 0.6s ease-out 0.3s both;
}

@keyframes sectionSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1600px) {
  .metrics-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1200px) {
  .stats-dashboard {
    padding: 20px;
    gap: 20px;
  }

  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
    padding: 20px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .filter-bar {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }

  .filter-select {
    width: 100%;
  }

  .filter-group {
    justify-content: space-between;
  }

  .header-actions {
    width: 100%;
  }

  .refresh-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .stats-dashboard {
    padding: 16px;
  }

  .header-title {
    font-size: 22px;
  }

  .header-icon-wrapper {
    width: 48px;
    height: 48px;
  }

  .header-icon {
    width: 24px;
    height: 24px;
  }

  .leaf-decoration {
    width: 120px;
    height: 120px;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
