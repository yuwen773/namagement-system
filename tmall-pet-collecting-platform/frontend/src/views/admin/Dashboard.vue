<script setup>
import { ref, onMounted, computed } from 'vue'
import { statisticsApi, crawlerApi } from '@/api'
import ChartContainer from '@/components/common/ChartContainer.vue'
import { TrendCharts, ShoppingCart, ShoppingBag, Wallet, DataAnalysis, Loading } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const loading = ref(true)
const overview = ref({
  total_products: 0,
  total_shops: 0,
  total_brands: 0,
  avg_price: 0
})

const priceDistribution = ref([])
const shopRanking = ref([])
const petTypeDistribution = ref([])
const systemStatus = ref({
  database: 'normal',
  crawler: 'idle',
  activeTasks: 0,
  lastCrawlTime: null
})

const fetchOverview = async () => {
  try {
    const res = await statisticsApi.getOverview()
    if (res.code === 0) {
      overview.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch overview:', error)
  }
}

const fetchPriceDistribution = async () => {
  try {
    const res = await statisticsApi.getPriceDistribution()
    if (res.code === 0) {
      priceDistribution.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch price distribution:', error)
  }
}

const fetchShopRanking = async () => {
  try {
    const res = await statisticsApi.getShopRanking({ limit: 10 })
    if (res.code === 0) {
      shopRanking.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch shop ranking:', error)
  }
}

const fetchSystemStatus = async () => {
  try {
    const res = await crawlerApi.getSystemHealth()
    if (res.code === 0) {
      systemStatus.value = {
        database: res.data.database,
        crawler: res.data.crawler,
        activeTasks: res.data.active_tasks,
        lastCrawlTime: res.data.last_crawl_time
      }
    }
  } catch (error) {
    console.error('Failed to fetch system status:', error)
  }
}

const fetchPetTypeDistribution = async () => {
  try {
    const res = await statisticsApi.getPetTypeDistribution()
    if (res.code === 0) {
      petTypeDistribution.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch pet type distribution:', error)
  }
}

const priceChartOption = computed(() => {
  if (!priceDistribution.value || priceDistribution.value.length === 0) {
    return null
  }

  const colors = ['#FF6B35', '#FFD700', '#7B2CBF', '#06FFA5']
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(13, 13, 20, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' },
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: 'rgba(255,255,255,0.6)', fontSize: 12 }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#0D0D14',
        borderWidth: 2
      },
      label: {
        show: true,
        color: 'rgba(255,255,255,0.7)',
        fontSize: 11,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' },
        itemStyle: {
          shadowBlur: 16,
          shadowOffsetX: 0,
          shadowColor: 'rgba(255, 107, 53, 0.4)'
        }
      },
      labelLine: {
        lineStyle: { color: 'rgba(255,255,255,0.2)' },
        smooth: 0.3
      },
      data: priceDistribution.value.map((item, index) => ({
        value: item.count,
        name: item.range,
        itemStyle: { color: colors[index] }
      }))
    }]
  }
})

const shopChartOption = computed(() => {
  if (!shopRanking.value || shopRanking.value.length === 0) {
    return null
  }

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(13, 13, 20, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
      axisLabel: { color: 'rgba(255,255,255,0.4)' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } }
    },
    yAxis: {
      type: 'category',
      data: shopRanking.value.map(item => item.shop),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 11,
        width: 100,
        overflow: 'truncate'
      }
    },
    series: [{
      type: 'bar',
      data: shopRanking.value.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#7B2CBF' },
            { offset: 0.5, color: '#FF6B35' },
            { offset: 1, color: '#FFD700' }
          ]),
          borderRadius: [0, 6, 6, 0]
        }
      })),
      barWidth: '65%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(255,255,255,0.7)',
        fontSize: 11
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 12,
          shadowColor: 'rgba(255, 107, 53, 0.3)'
        }
      }
    }]
  }
})

const petTypeChartOption = computed(() => {
  if (!petTypeDistribution.value || petTypeDistribution.value.length === 0) {
    return null
  }

  const colors = ['#FF6B35', '#7B2CBF', '#FFD700', '#06FFA5', '#FF6B9D', '#9D4EDD']
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(13, 13, 20, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' }
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: 'rgba(255,255,255,0.6)', fontSize: 11 }
    },
    series: [{
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['40%', '50%'],
      itemStyle: {
        borderRadius: 8,
        borderColor: '#0D0D14',
        borderWidth: 2
      },
      data: petTypeDistribution.value.map((item, index) => ({
        name: item.label,
        value: item.count,
        itemStyle: { color: colors[index % colors.length] }
      })),
      label: {
        show: true,
        color: 'rgba(255,255,255,0.7)',
        fontSize: 11,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 12,
          shadowOffsetX: 0,
          shadowColor: 'rgba(255, 107, 53, 0.4)'
        }
      }
    }]
  }
})

const loadData = async () => {
  loading.value = true
  await Promise.all([
    fetchOverview(),
    fetchPriceDistribution(),
    fetchShopRanking(),
    fetchSystemStatus(),
    fetchPetTypeDistribution()
  ])
  loading.value = false
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2
  }).format(price)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="dashboard-container">
    <!-- 顶部欢迎区 -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">数据概览</h1>
        <p class="header-subtitle">实时监控宠物用品市场数据指标</p>
      </div>
      <div class="header-actions">
        <button class="refresh-btn" @click="loadData" :class="{ loading }">
          <Loading class="icon" :class="{ spinning: loading }" />
          <span>刷新数据</span>
        </button>
      </div>
    </div>

    <!-- 统计指标卡片 -->
    <div class="metrics-grid">
      <div class="metric-card metric-card--orange" style="--i: 0">
        <div class="metric-header">
          <div class="metric-icon">
            <ShoppingBag class="icon" />
          </div>
          <span class="metric-trend positive">+12.5%</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">商品总数</p>
          <p class="metric-value">{{ formatNumber(overview.total_products) }}</p>
        </div>
        <div class="metric-bg">📦</div>
      </div>

      <div class="metric-card metric-card--purple" style="--i: 1">
        <div class="metric-header">
          <div class="metric-icon">
            <ShoppingCart class="icon" />
          </div>
          <span class="metric-trend positive">+8.3%</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">店铺数量</p>
          <p class="metric-value">{{ formatNumber(overview.total_shops) }}</p>
        </div>
        <div class="metric-bg">🏪</div>
      </div>

      <div class="metric-card metric-card--gold" style="--i: 2">
        <div class="metric-header">
          <div class="metric-icon">
            <TrendCharts class="icon" />
          </div>
          <span class="metric-trend positive">+15.2%</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">品牌数量</p>
          <p class="metric-value">{{ formatNumber(overview.total_brands) }}</p>
        </div>
        <div class="metric-bg">🎯</div>
      </div>

      <div class="metric-card metric-card--cyan" style="--i: 3">
        <div class="metric-header">
          <div class="metric-icon">
            <Wallet class="icon" />
          </div>
          <span class="metric-trend neutral">0.0%</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">平均价格</p>
          <p class="metric-value">{{ formatPrice(overview.price?.avg || 0) }}</p>
        </div>
        <div class="metric-bg">💰</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <!-- 价格分布 -->
      <div class="chart-panel" style="--i: 0">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--orange">
              <DataAnalysis class="icon" />
            </div>
            <div>
              <h3 class="chart-title">价格区间分布</h3>
              <p class="chart-subtitle">商品价格分布占比分析</p>
            </div>
          </div>
          <div class="chart-badge">分布</div>
        </div>
        <div class="chart-panel-body">
          <ChartContainer
            v-if="!loading && priceDistribution.length > 0"
            :option="priceChartOption"
            height="280px"
          />
          <div v-else class="chart-loading">
            <Loading class="loading-icon spinning" />
            <p>加载数据中...</p>
          </div>
        </div>
      </div>

      <!-- 店铺排行 -->
      <div class="chart-panel" style="--i: 1">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--purple">
              <ShoppingCart class="icon" />
            </div>
            <div>
              <h3 class="chart-title">店铺商品排行</h3>
              <p class="chart-subtitle">TOP 10 店铺商品数量</p>
            </div>
          </div>
          <div class="chart-badge">排行</div>
        </div>
        <div class="chart-panel-body">
          <ChartContainer
            v-if="!loading && shopRanking.length > 0"
            :option="shopChartOption"
            height="280px"
          />
          <div v-else class="chart-loading">
            <Loading class="loading-icon spinning" />
            <p>加载数据中...</p>
          </div>
        </div>
      </div>

      <!-- 宠物类型分布 -->
      <div class="chart-panel" style="--i: 2">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper chart-icon-wrapper--gold">
              <DataAnalysis class="icon" />
            </div>
            <div>
              <h3 class="chart-title">宠物类型分布</h3>
              <p class="chart-subtitle">各类型商品占比统计</p>
            </div>
          </div>
          <div class="chart-badge">类型</div>
        </div>
        <div class="chart-panel-body">
          <ChartContainer
            v-if="!loading && petTypeDistribution.length > 0"
            :option="petTypeChartOption"
            height="280px"
          />
          <div v-else class="chart-loading">
            <Loading class="loading-icon spinning" />
            <p>加载数据中...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 系统状态面板 -->
    <div class="system-panel">
      <div class="system-panel-header">
        <div class="system-status-indicator">
          <div class="status-dot" :class="{ active: systemStatus.crawler === 'running' }"></div>
          <div class="status-pulse" :class="{ active: systemStatus.crawler === 'running' }"></div>
        </div>
        <div class="system-title-group">
          <h3 class="system-title">系统运行状态</h3>
          <p class="system-subtitle">实时监控系统核心服务</p>
        </div>
        <div class="system-info">
          <div class="info-item">
            <span class="info-label">活跃任务</span>
            <span class="info-value">{{ systemStatus.activeTasks }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">上次采集</span>
            <span class="info-value">{{ systemStatus.lastCrawlTime || '暂无' }}</span>
          </div>
        </div>
      </div>

      <div class="system-metrics">
        <div class="system-metric">
          <div class="metric-row">
            <div class="metric-icon-small metric-icon-small--database"></div>
            <div class="metric-content">
              <span class="metric-name">数据库连接</span>
              <span class="metric-status" :class="systemStatus.database === 'normal' ? 'online' : 'offline'">
                {{ systemStatus.database === 'normal' ? '正常' : '异常' }}
              </span>
            </div>
          </div>
        </div>

        <div class="system-metric">
          <div class="metric-row">
            <div class="metric-icon-small metric-icon-small--crawler"></div>
            <div class="metric-content">
              <span class="metric-name">爬虫服务</span>
              <span class="metric-status" :class="systemStatus.crawler === 'running' ? 'online' : 'idle'">
                {{ systemStatus.crawler === 'running' ? '运行中' : '空闲' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.dashboard-container {
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
   Metrics Grid
   ============================================ */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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
.metric-card--cyan::before { background: linear-gradient(90deg, var(--primary-cyan), transparent); }

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
.metric-card--cyan .metric-icon { background: rgba(6, 255, 165, 0.15); }

.metric-icon .icon {
  width: 22px;
  height: 22px;
}

.metric-card--orange .metric-icon .icon { color: var(--primary-orange); }
.metric-card--purple .metric-icon .icon { color: var(--primary-purple); }
.metric-card--gold .metric-icon .icon { color: var(--primary-gold); }
.metric-card--cyan .metric-icon .icon { color: var(--primary-cyan); }

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
.metric-card--cyan .metric-value { color: var(--primary-cyan); }

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
  grid-template-columns: repeat(3, 1fr);
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

.chart-loading .loading-icon {
  width: 32px;
  height: 32px;
  color: var(--primary-orange);
  margin-bottom: 12px;
}

.chart-loading p {
  font-size: 13px;
  margin: 0;
}

/* ============================================
   System Panel
   ============================================ */
.system-panel {
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.08), rgba(255, 107, 53, 0.04));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(123, 44, 191, 0.15);
  border-radius: 24px;
  padding: 24px;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: 0.7s;
}

.system-panel-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.system-status-indicator {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--text-tertiary);
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.status-dot.active {
  background: var(--primary-cyan);
  box-shadow: 0 0 20px var(--primary-cyan);
}

.status-pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid var(--primary-orange);
  opacity: 0;
  transition: all 0.3s ease;
}

.status-pulse.active {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}

.system-title-group {
  flex: 1;
}

.system-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.system-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.system-info {
  display: flex;
  gap: 24px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.info-label {
  color: var(--text-tertiary);
}

.info-value {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: var(--primary-orange);
}

.system-metrics {
  display: flex;
  gap: 16px;
}

.system-metric {
  flex: 1;
  padding: 16px 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
}

.metric-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.metric-icon-small {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.metric-icon-small--database {
  background: rgba(123, 44, 191, 0.15);
}

.metric-icon-small--crawler {
  background: rgba(255, 215, 0, 0.15);
}

.metric-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.metric-name {
  font-size: 14px;
  color: var(--text-secondary);
}

.metric-status {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}

.metric-status.online {
  background: rgba(6, 255, 165, 0.15);
  color: var(--primary-cyan);
  border: 1px solid rgba(6, 255, 165, 0.3);
}

.metric-status.idle {
  background: rgba(255, 215, 0, 0.15);
  color: var(--primary-gold);
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.metric-status.offline {
  background: rgba(255, 59, 48, 0.15);
  color: #FF3B30;
  border: 1px solid rgba(255, 59, 48, 0.3);
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1400px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .system-panel {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .system-info {
    flex-direction: column;
    gap: 8px;
  }

  .system-metrics {
    flex-direction: column;
  }
}
</style>
