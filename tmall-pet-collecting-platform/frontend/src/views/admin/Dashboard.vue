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

// 清新自然风格配色
const natureColors = ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#00B4D8', '#90E0EF']

const priceChartOption = computed(() => {
  if (!priceDistribution.value || priceDistribution.value.length === 0) {
    return null
  }

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      textStyle: { color: '#1C1917' },
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#57534E', fontSize: 12 }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#FFFFFF',
        borderWidth: 3
      },
      label: {
        show: true,
        color: '#57534E',
        fontSize: 11,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' },
        itemStyle: {
          shadowBlur: 16,
          shadowOffsetX: 0,
          shadowColor: 'rgba(45, 106, 79, 0.25)'
        }
      },
      labelLine: {
        lineStyle: { color: '#A8A29E' },
        smooth: 0.3
      },
      data: priceDistribution.value.map((item, index) => ({
        value: item.count,
        name: item.range,
        itemStyle: { color: natureColors[index % natureColors.length] }
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
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      textStyle: { color: '#1C1917' }
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
      axisLine: { lineStyle: { color: '#E7E5E4' } },
      axisLabel: { color: '#A8A29E' },
      splitLine: { lineStyle: { color: '#F5F5F4', type: 'dashed' } }
    },
    yAxis: {
      type: 'category',
      data: shopRanking.value.map(item => item.shop),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#57534E',
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
            { offset: 0, color: natureColors[index % natureColors.length] },
            { offset: 1, color: natureColors[(index + 1) % natureColors.length] }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '65%',
      label: {
        show: true,
        position: 'right',
        color: '#57534E',
        fontSize: 11,
        fontWeight: '600'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 12,
          shadowColor: 'rgba(45, 106, 79, 0.2)'
        }
      }
    }]
  }
})

const petTypeChartOption = computed(() => {
  if (!petTypeDistribution.value || petTypeDistribution.value.length === 0) {
    return null
  }

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      textStyle: { color: '#1C1917' }
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#57534E', fontSize: 11 }
    },
    series: [{
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['40%', '50%'],
      itemStyle: {
        borderRadius: 10,
        borderColor: '#FFFFFF',
        borderWidth: 3
      },
      data: petTypeDistribution.value.map((item, index) => ({
        name: item.label,
        value: item.count,
        itemStyle: { color: natureColors[index % natureColors.length] }
      })),
      label: {
        show: true,
        color: '#57534E',
        fontSize: 11,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 12,
          shadowOffsetX: 0,
          shadowColor: 'rgba(45, 106, 79, 0.25)'
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
        <div class="header-decoration">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="20" fill="url(#headerGrad)" fill-opacity="0.15"/>
            <path d="M24 10C24 10 36 16 36 26C36 34 30 38 24 38C18 38 12 34 12 26C12 16 24 10 24 10Z" fill="url(#headerGrad)"/>
            <path d="M24 10L24 38" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
            <defs>
              <linearGradient id="headerGrad" x1="12" y1="10" x2="36" y2="38">
                <stop offset="0%" stop-color="#74C69D"/>
                <stop offset="100%" stop-color="#40916C"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div>
          <h1 class="header-title">数据概览</h1>
          <p class="header-subtitle">实时监控宠物用品市场数据指标</p>
        </div>
      </div>
      <button class="refresh-btn" @click="loadData" :class="{ loading }">
        <Loading class="icon" :class="{ spinning: loading }" />
        <span>刷新数据</span>
      </button>
    </div>

    <!-- 统计指标卡片 -->
    <div class="metrics-grid">
      <div class="metric-card metric-card--green" style="--i: 0">
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
        <div class="metric-leaf">
          <svg width="60" height="60" viewBox="0 0 60 80" fill="none">
            <path d="M30 5C30 5 50 20 50 40C50 60 40 70 30 70C20 70 10 60 10 40C10 20 30 5 30 5Z" fill="currentColor" opacity="0.08"/>
          </svg>
        </div>
      </div>

      <div class="metric-card metric-card--teal" style="--i: 1">
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
        <div class="metric-leaf">
          <svg width="50" height="70" viewBox="0 0 50 70" fill="none">
            <path d="M25 5C25 5 42 18 42 35C42 52 34 60 25 60C16 60 8 52 8 35C8 18 25 5 25 5Z" fill="currentColor" opacity="0.08"/>
          </svg>
        </div>
      </div>

      <div class="metric-card metric-card--blue" style="--i: 2">
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
        <div class="metric-leaf">
          <svg width="40" height="60" viewBox="0 0 40 60" fill="none">
            <path d="M20 5C20 5 34 15 34 30C34 45 28 52 20 52C12 52 6 45 6 30C6 15 20 5 20 5Z" fill="currentColor" opacity="0.08"/>
          </svg>
        </div>
      </div>

      <div class="metric-card metric-card--light" style="--i: 3">
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
        <div class="metric-leaf">
          <svg width="35" height="50" viewBox="0 0 35 50" fill="none">
            <path d="M17.5 4C17.5 4 30 12 30 25C30 38 24 44 17.5 44C11 44 5 38 5 25C5 12 17.5 4 17.5 4Z" fill="currentColor" opacity="0.08"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <!-- 价格分布 -->
      <div class="chart-panel chart-panel--green" style="--i: 0">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper">
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
      <div class="chart-panel chart-panel--teal" style="--i: 1">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper">
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
      <div class="chart-panel chart-panel--blue" style="--i: 2">
        <div class="chart-panel-header">
          <div class="chart-title-group">
            <div class="chart-icon-wrapper">
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
            <div class="metric-icon-small metric-icon-small--database">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 3C9 3 14 4 14 6C14 8 9 9 9 9C9 9 4 8 4 6C4 4 9 3 9 3Z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M4 6V12C4 14 9 15 9 15C9 15 14 14 14 12V6" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </div>
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
            <div class="metric-icon-small metric-icon-small--crawler">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 3L3 7V13C3 14.1 3.9 15 5 15H13C14.1 15 15 14.1 15 13V7L9 3Z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M9 9V13" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="metric-content">
              <span class="metric-name">爬虫服务</span>
              <span class="metric-status" :class="systemStatus.crawler === 'running' ? 'online' : 'idle'">
                {{ systemStatus.crawler === 'running' ? '运行中' : '空闲' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 装饰植物 -->
      <div class="system-plant">
        <svg width="50" height="50" viewBox="0 0 50 50" fill="none">
          <path d="M25 48V20" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M25 35C25 35 40 28 40 18C40 12 35 8 25 8C15 8 10 12 10 18C10 28 25 35 25 35Z" fill="#74C69D" fill-opacity="0.15"/>
          <path d="M25 22C25 22 35 17 35 10C35 6 31 4 25 4C19 4 15 6 15 10C15 17 25 22 25 22Z" fill="#52B788" fill-opacity="0.2"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.dashboard-container {
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

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  animation: pageFadeIn 0.5s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-decoration {
  flex-shrink: 0;
  animation: headerFloat 4s ease-in-out infinite;
}

@keyframes headerFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.01em;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.refresh-btn:hover {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
  transform: translateY(-2px);
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
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: metricSlideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: calc(var(--i) * 0.1s);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-soft);
}

@keyframes metricSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
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
  border-radius: 20px 20px 0 0;
}

.metric-card--green::before { background: linear-gradient(90deg, var(--primary-green), var(--accent-green)); }
.metric-card--teal::before { background: linear-gradient(90deg, var(--primary-teal), var(--primary-light)); }
.metric-card--blue::before { background: linear-gradient(90deg, var(--accent-blue), var(--accent-blue-light)); }
.metric-card--light::before { background: linear-gradient(90deg, var(--accent-green), var(--accent-blue-light)); }

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
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

.metric-card--green .metric-icon { background: rgba(45, 106, 79, 0.1); }
.metric-card--teal .metric-icon { background: rgba(64, 145, 108, 0.1); }
.metric-card--blue .metric-icon { background: rgba(0, 180, 216, 0.1); }
.metric-card--light .metric-icon { background: rgba(116, 198, 157, 0.1); }

.metric-icon .icon {
  width: 22px;
  height: 22px;
}

.metric-card--green .metric-icon .icon { color: var(--primary-green); }
.metric-card--teal .metric-icon .icon { color: var(--primary-teal); }
.metric-card--blue .metric-icon .icon { color: var(--accent-blue); }
.metric-card--light .metric-icon .icon { color: var(--accent-green); }

.metric-trend {
  font-family: 'Nunito', monospace;
  font-size: 11px;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 20px;
}

.metric-trend.positive {
  background: rgba(45, 106, 79, 0.1);
  color: var(--primary-green);
}

.metric-trend.neutral {
  background: var(--bg-sand);
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
  font-family: 'Nunito', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-card--green .metric-value { color: var(--primary-green); }
.metric-card--teal .metric-value { color: var(--primary-teal); }
.metric-card--blue .metric-value { color: var(--accent-blue); }
.metric-card--light .metric-value { color: var(--accent-green); }

.metric-leaf {
  position: absolute;
  bottom: -8px;
  right: -8px;
  color: var(--primary-green);
  opacity: 0.15;
  pointer-events: none;
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
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(0.4s + var(--i) * 0.1s);
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

@keyframes panelFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.chart-panel:hover {
  box-shadow: var(--shadow-hover);
}

.chart-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
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
  background: rgba(45, 106, 79, 0.08);
}

.chart-icon-wrapper .icon {
  width: 18px;
  height: 18px;
  color: var(--primary-green);
}

.chart-title {
  font-family: 'Noto Serif SC', serif;
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
  background: rgba(45, 106, 79, 0.1);
  border: 1px solid rgba(45, 106, 79, 0.15);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--primary-green);
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
  color: var(--primary-green);
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
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: 0.7s;
  box-shadow: var(--shadow-soft);
}

.system-panel::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(116, 198, 157, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.system-panel-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
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
  background: var(--accent-green);
  box-shadow: 0 0 20px var(--accent-green);
}

.status-pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid var(--primary-green);
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
  font-family: 'Noto Serif SC', serif;
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
  font-family: 'Nunito', sans-serif;
  font-weight: 600;
  color: var(--primary-green);
}

.system-metrics {
  display: flex;
  gap: 16px;
  position: relative;
  z-index: 1;
}

.system-metric {
  flex: 1;
  padding: 16px 20px;
  background: var(--bg-sand);
  border-radius: 16px;
  border: 1px solid var(--border-light);
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
  color: white;
}

.metric-icon-small--database {
  background: linear-gradient(135deg, var(--primary-green), var(--accent-green));
}

.metric-icon-small--crawler {
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-blue-light));
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
  font-weight: 500;
}

.metric-status {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}

.metric-status.online {
  background: rgba(45, 106, 79, 0.1);
  color: var(--primary-green);
  border: 1px solid rgba(45, 106, 79, 0.2);
}

.metric-status.idle {
  background: rgba(144, 224, 239, 0.15);
  color: var(--accent-blue);
  border: 1px solid rgba(0, 180, 216, 0.2);
}

.metric-status.offline {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.system-plant {
  position: absolute;
  bottom: 20px;
  right: 20px;
  opacity: 0.4;
  animation: plantSway 4s ease-in-out infinite;
  pointer-events: none;
}

@keyframes plantSway {
  0%, 100% { transform: rotate(-3deg); }
  50% { transform: rotate(3deg); }
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

  .system-plant {
    display: none;
  }
}
</style>
