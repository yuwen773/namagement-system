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
      color: '#FF6B35',
      gradient: 'from-orange-500 to-rose-500',
      detail: `+${ov.completeness_pct?.with_sales_pct || 0}% 有销量`
    },
    {
      label: '店铺数量',
      value: formatNumber(ov.total_shops),
      icon: ShoppingCart,
      color: '#7B2CBF',
      gradient: 'from-purple-500 to-indigo-500',
      detail: `${ov.total_regions || 0} 个地区`
    },
    {
      label: '品牌数量',
      value: formatNumber(ov.total_brands || 0),
      icon: Collection,
      color: '#FFD700',
      gradient: 'from-yellow-400 to-orange-400',
      detail: `${ov.completeness_pct?.with_brand_pct || 0}% 覆盖率`
    },
    {
      label: '平均价格',
      value: formatPrice(ov.price?.avg || 0),
      icon: Wallet,
      color: '#06FFA5',
      gradient: 'from-emerald-400 to-teal-400',
      detail: `¥${ov.price?.min?.toFixed(0)} - ¥${ov.price?.max?.toFixed(0)}`
    },
    {
      label: '总销量',
      value: formatNumber(ov.sales?.total || 0),
      icon: TrendCharts,
      color: '#FF4785',
      gradient: 'from-pink-500 to-rose-500',
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
      color: '#4CC9F0',
      gradient: 'from-cyan-400 to-blue-400',
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
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">宠物用品统计分析</h1>
        <p class="header-subtitle">天猫宠物用品数据洞察与可视化分析</p>
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
      <Loading class="loading-icon spinning" />
      <p class="loading-text">加载数据中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <p class="error-message">{{ error }}</p>
        <el-button @click="loadData" type="primary">重试</el-button>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Metrics Section -->
      <section class="metrics-section">
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.stats-dashboard {
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
   Dashboard Header
   ============================================ */
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.header-content {
  flex: 1;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.refresh-btn {
  display: flex;
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

.refresh-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--primary-orange);
  color: var(--primary-orange);
}

.refresh-btn .icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
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
  display: flex;
  gap: 24px;
  padding: 16px 0;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.filter-icon {
  width: 16px;
  height: 16px;
  color: var(--primary-orange);
}

.filter-select {
  width: 180px;
}

.filter-select :deep(.el-input__wrapper) {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  box-shadow: none;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.filter-select :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.filter-select :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-orange);
}

.filter-select :deep(.el-input__inner) {
  color: var(--text-primary);
}

.filter-select :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

.filter-select :deep(.el-select__placeholder) {
  color: var(--text-tertiary);
}

/* ============================================
   Loading & Error States
   ============================================ */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  padding: 40px;
}

.loading-icon {
  width: 48px;
  height: 48px;
  color: var(--primary-orange);
  margin-bottom: 16px;
}

.loading-icon.spinning {
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.error-content {
  text-align: center;
}

.error-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.error-message {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0 0 24px 0;
}

/* ============================================
   Dashboard Content
   ============================================ */
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
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
  gap: 20px;
  animation: sectionSlideIn 0.6s ease-out 0.2s both;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.charts-row--full {
  grid-template-columns: 1fr;
}

.chart-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(var(--i) * 0.1s);
  transition: all 0.3s ease;
}

@keyframes panelFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.chart-panel:hover {
  border-color: var(--border-default);
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
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-title {
    font-size: 22px;
  }

  .filter-bar {
    flex-direction: column;
    gap: 16px;
  }

  .filter-select {
    width: 100%;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }
}
</style>
