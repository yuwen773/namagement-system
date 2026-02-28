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
  <div class="statistics-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="dashboard-title">
            <DataAnalysis class="title-icon" />
            宠物用品统计分析
          </h1>
          <p class="dashboard-subtitle">天猫宠物用品数据洞察与可视化分析</p>
        </div>
        <div class="header-actions">
          <el-button
            :loading="refreshing"
            :icon="Refresh"
            @click="handleRefresh"
            class="refresh-btn"
          >
            刷新数据
          </el-button>
        </div>
      </div>

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
    </div>

    <div v-if="loading" class="loading-container">
      <Loading class="loading-icon" />
      <p class="loading-text">加载数据中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <p class="error-message">{{ error }}</p>
        <el-button @click="loadData" type="primary">重试</el-button>
      </div>
    </div>

    <div v-else class="dashboard-content">
      <section class="metrics-section">
        <div class="metrics-grid">
          <MetricCard
            v-for="(metric, index) in overviewMetrics"
            :key="metric.label"
            :metric="metric"
            :style="{ animationDelay: `${index * 0.1}s` }"
          />
        </div>
      </section>

      <section class="charts-section">
        <div class="charts-row">
          <ChartSection
            title="价格分布"
            subtitle="商品价格区间分布情况"
            type="price-distribution"
            :data="dashboardData?.price_distribution"
            class="chart-item price-chart"
          />

          <ChartSection
            title="销量分布"
            subtitle="商品销量区间分布情况"
            type="sales-distribution"
            :data="dashboardData?.sales_distribution"
            class="chart-item sales-chart"
          />
        </div>

        <div class="charts-row">
          <BrandAnalysis
            :data="dashboardData?.top_brands"
            class="chart-item brand-analysis"
          />

          <RegionAnalysis
            :data="dashboardData?.top_regions"
            class="chart-item region-analysis"
          />
        </div>

        <div class="charts-row full-width">
          <ChartSection
            title="价格-销量关联分析"
            subtitle="不同价格区间的平均销量表现"
            type="price-sales-correlation"
            :data="dashboardData?.price_sales_correlation"
            class="chart-item correlation-chart"
          />
        </div>
      </section>

      <section class="products-section">
        <TopProducts
          :sales-products="dashboardData?.top_products_sales"
          :price-products="dashboardData?.top_products_price"
          :active-sort="activeSort"
          @sort-change="handleSortChange"
        />
      </section>

      <section class="insights-section">
        <MarketInsights
          :insights="dashboardData?.market_insights"
        />
      </section>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Exo+2:wght@300;400;500;600;700&display=swap');

.statistics-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
  position: relative;
  overflow-x: hidden;
}

.statistics-dashboard::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background:
    radial-gradient(circle at 20% 80%, rgba(255, 107, 53, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(123, 44, 191, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(6, 255, 165, 0.03) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
  animation: gradientShift 20s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(-2%, -2%) rotate(5deg); }
}

.dashboard-header {
  position: relative;
  z-index: 1;
  background: rgba(15, 15, 26, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 32px 40px;
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dashboard-title {
  display: flex;
  align-items: center;
  gap: 16px;
  font-family: 'Exo 2', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  letter-spacing: -0.5px;
}

.title-icon {
  width: 36px;
  height: 36px;
  color: #FF6B35;
  filter: drop-shadow(0 0 20px rgba(255, 107, 53, 0.5));
}

.dashboard-subtitle {
  font-family: 'Exo 2', sans-serif;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  padding-left: 52px;
  font-weight: 400;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.refresh-btn {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(123, 44, 191, 0.2));
  border: 1px solid rgba(255, 107, 53, 0.3);
  color: #FF6B35;
  font-family: 'Exo 2', sans-serif;
  font-weight: 600;
  padding: 12px 24px;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.3), rgba(123, 44, 191, 0.3));
  border-color: rgba(255, 107, 53, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

.filter-bar {
  display: flex;
  gap: 32px;
  padding-left: 52px;
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
  font-family: 'Exo 2', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
}

.filter-icon {
  width: 16px;
  height: 16px;
  color: #FF6B35;
}

.filter-select {
  width: 180px;
}

.filter-select :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

.filter-select :deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  font-family: 'Exo 2', sans-serif;
}

.loading-container,
.error-container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 40px;
}

.loading-icon {
  width: 64px;
  height: 64px;
  color: #FF6B35;
  animation: spin 1s linear infinite;
  margin-bottom: 24px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  font-family: 'Exo 2', sans-serif;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.error-content {
  text-align: center;
}

.error-icon {
  font-size: 64px;
  display: block;
  margin-bottom: 24px;
}

.error-message {
  font-family: 'Exo 2', sans-serif;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 32px 0;
}

.dashboard-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: 0 40px 40px 40px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metrics-section {
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
}

.charts-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.charts-row.full-width {
  grid-template-columns: 1fr;
}

.chart-item {
  min-height: 400px;
}

.products-section,
.insights-section {
  animation: fadeInUp 0.6s ease-out 0.3s both;
}

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
    padding: 24px 20px;
  }

  .dashboard-content {
    padding: 0 20px 24px 20px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .dashboard-title {
    font-size: 24px;
  }

  .filter-bar {
    flex-direction: column;
    gap: 16px;
    padding-left: 0;
  }

  .filter-select {
    width: 100%;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }
}
</style>
