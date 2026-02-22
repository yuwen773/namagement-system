<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">数据概览</h1>
          <p class="page-subtitle">智能问答采集系统 · 实时数据监控</p>
        </div>
        <div class="header-right">
          <div class="user-badge">
            <div class="user-avatar">{{ userInitials }}</div>
            <span class="user-name">{{ authStore.userInfo?.username }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Overview Cards -->
    <section class="overview-section">
      <div class="overview-grid">
        <div v-for="(card, index) in overviewCards" :key="index" class="stat-card" :style="{ '--delay': `${index * 0.08}s` }">
          <div class="stat-icon" :style="{ background: card.gradient }">
            <component :is="card.icon" />
          </div>
          <div class="stat-content">
            <span class="stat-value" :style="{ color: card.color }">{{ card.value }}</span>
            <span class="stat-label">{{ card.label }}</span>
          </div>
          <div class="stat-trend" v-if="card.trend">
            <span class="trend-icon" :class="card.trend > 0 ? 'up' : 'down'">
              {{ card.trend > 0 ? '↑' : '↓' }}
            </span>
            <span class="trend-text">{{ Math.abs(card.trend) }}%</span>
          </div>
          <div class="stat-glow"></div>
        </div>
      </div>
    </section>

    <!-- Charts Grid -->
    <section class="charts-section">
      <div class="charts-grid">
        <!-- Trend Chart -->
        <div class="chart-card large">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
              </span>
              问答趋势
            </h3>
            <div class="card-actions">
              <span class="data-badge">最近30天</span>
            </div>
          </div>
          <div class="card-body">
            <div v-if="loading.trend" class="chart-loading">
              <div class="loading-spinner"></div>
            </div>
            <ECharts v-else :options="trendChartOptions" theme="light" />
            <div v-if="!loading.trend && !trendData.length" class="chart-empty">
              <span class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M3 3v18h18"/>
                  <path d="M18 17V9"/>
                  <path d="M13 17V5"/>
                  <path d="M8 17v-3"/>
                </svg>
              </span>
              <p>暂无数据</p>
            </div>
          </div>
        </div>

        <!-- Answerers Chart -->
        <div class="chart-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </span>
              高频回答者
            </h3>
          </div>
          <div class="card-body">
            <div v-if="loading.answerers" class="chart-loading">
              <div class="loading-spinner"></div>
            </div>
            <ECharts v-else :options="answerersChartOptions" theme="light" />
            <div v-if="!loading.answerers && !answerersData.length" class="chart-empty">
              <span class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                  <line x1="9" y1="9" x2="9.01" y2="9"/>
                  <line x1="15" y1="9" x2="15.01" y2="9"/>
                </svg>
              </span>
              <p>暂无数据</p>
            </div>
          </div>
        </div>

        <!-- Tags Treemap -->
        <div class="chart-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
                  <line x1="7" y1="7" x2="7.01" y2="7"/>
                </svg>
              </span>
              标签分布
            </h3>
          </div>
          <div class="card-body">
            <div v-if="loading.tags" class="chart-loading">
              <div class="loading-spinner"></div>
            </div>
            <ECharts v-else :options="tagsChartOptions" theme="light" />
            <div v-if="!loading.tags && !tagsData.length" class="chart-empty">
              <span class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="3" y1="9" x2="21" y2="9"/>
                  <line x1="9" y1="21" x2="9" y2="9"/>
                </svg>
              </span>
              <p>暂无数据</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Crawler Control (Admin Only) -->
    <section v-if="authStore.isAdmin" class="crawler-section">
      <div class="crawler-card">
        <div class="crawler-header">
          <div class="crawler-title">
            <span class="crawler-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polygon points="10 8 16 12 10 16 10 8"/>
              </svg>
            </span>
            <h3>爬虫控制台</h3>
          </div>
          <div class="crawler-status" :class="crawlerStatusClass">
            <span class="status-dot"></span>
            <span class="status-text">{{ crawlerStatusText }}</span>
          </div>
        </div>

        <div class="crawler-body">
          <div class="progress-section" v-if="crawlerData.has_active_task">
            <div class="progress-info">
              <span class="progress-label">采集进度</span>
              <span class="progress-percent">{{ crawlerData.current_task?.progress || 0 }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${crawlerData.current_task?.progress || 0}%` }"></div>
            </div>
            <p class="progress-detail">
              已采集 {{ crawlerData.current_task?.collected || 0 }} / {{ crawlerData.current_task?.total || 0 }} 条
            </p>
          </div>

          <div class="crawler-actions">
            <button
              class="crawler-btn primary"
              :disabled="crawlerLoading || crawlerData.has_active_task"
              @click="handleStartCrawler('demo')"
            >
              <span class="btn-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5 3 19 12 5 21 5 3"/>
                </svg>
              </span>
              <span>{{ crawlerLoading ? '启动中...' : '开始采集' }}</span>
            </button>
            <button
              class="crawler-btn secondary"
              :disabled="crawlerLoading || !crawlerData.has_active_task"
              @click="handleStopCrawler"
            >
              <span class="btn-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="6" y="4" width="4" height="16"/>
                  <rect x="14" y="4" width="4" height="16"/>
                </svg>
              </span>
              <span>停止采集</span>
            </button>
          </div>

          <div v-if="crawlerMessage" class="crawler-message" :class="crawlerMessageType">
            {{ crawlerMessage }}
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { useAuthStore } from '@/stores/auth'
import request from '@/utils/request'
import ECharts from '@/components/ECharts.vue'

// Icons
const IconQuestion = { render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [h('path', { d: 'M9.5 3C6.5 3 4 5.5 4 8.5C4 10.5 5 12.5 6.5 13.5V17C6.5 17.55 6.95 18 7.5 18H12.5C13.05 18 13.5 17.55 13.5 17V13.5C15 12.5 16 10.5 16 8.5C16 5.5 13.5 3 10.5 3H9.5Z' })]) }
const IconTag = { render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [h('path', { d: 'M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z' }), h('line', { x1: '7', y1: '7', x2: '7.01', y2: '7' })]) }
const IconUser = { render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }), h('circle', { cx: '12', cy: '7', r: '4' })]) }
const IconCalendar = { render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [h('rect', { x: '3', y: '4', width: '18', height: '18', rx: '2', ry: '2' }), h('line', { x1: '16', y1: '2', x2: '16', y2: '6' }), h('line', { x1: '8', y1: '2', x2: '8', y2: '6' }), h('line', { x1: '3', y1: '10', x2: '21', y2: '10' })]) }

const authStore = useAuthStore()

// State
const loading = ref({
  overview: true,
  trend: true,
  answerers: true,
  tags: true
})

const overviewData = ref({
  total_questions: 0,
  total_categories: 0,
  total_answerers: 0,
  today_questions: 0
})

const trendData = ref([])
const answerersData = ref([])
const tagsData = ref([])

const crawlerLoading = ref(false)
const crawlerData = ref({
  has_active_task: false,
  current_task: null,
  resume_available: false
})
const crawlerMessage = ref('')
const crawlerMessageType = ref('info')

// Computed
const userInitials = computed(() => {
  const name = authStore.userInfo?.username || ''
  return name.charAt(0).toUpperCase()
})

const overviewCards = computed(() => [
  {
    icon: IconQuestion,
    label: '问答总数',
    value: overviewData.value.total_questions.toLocaleString(),
    color: '#0d9488',
    gradient: 'linear-gradient(135deg, #0d9488 0%, #14b8a6 100%)',
    trend: 12
  },
  {
    icon: IconTag,
    label: '标签数量',
    value: overviewData.value.total_categories.toLocaleString(),
    color: '#8b5cf6',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
    trend: 5
  },
  {
    icon: IconUser,
    label: '回答者',
    value: overviewData.value.total_answerers.toLocaleString(),
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)',
    trend: -2
  },
  {
    icon: IconCalendar,
    label: '今日新增',
    value: overviewData.value.today_questions.toLocaleString(),
    color: '#ec4899',
    gradient: 'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)',
    trend: 8
  }
])

const crawlerStatusClass = computed(() => {
  if (!crawlerData.value.has_active_task) return 'idle'
  const status = crawlerData.value.current_task?.status
  if (status === 'running') return 'running'
  return 'completed'
})

const crawlerStatusText = computed(() => {
  if (!crawlerData.value.has_active_task) return '空闲中'
  const status = crawlerData.value.current_task?.status
  if (status === 'running') return '采集中'
  return '已完成'
})

// Chart Options
const trendChartOptions = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    borderColor: '#e5e7eb',
    borderWidth: 1,
    textStyle: { color: '#374151', fontSize: 12 },
    extraCssText: 'box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-radius: 8px;'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: trendData.value.map(d => d.date),
    axisLine: { lineStyle: { color: '#e5e7eb' } },
    axisLabel: { color: '#6b7280', fontSize: 11 },
    boundaryGap: false
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
    axisLabel: { color: '#6b7280', fontSize: 11 }
  },
  series: [{
    data: trendData.value.map(d => d.count),
    type: 'line',
    smooth: true,
    symbol: 'circle',
    symbolSize: 8,
    lineStyle: {
      color: '#0d9488',
      width: 3
    },
    itemStyle: {
      color: '#0d9488',
      borderColor: '#fff',
      borderWidth: 2
    },
    areaStyle: {
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(13, 148, 136, 0.25)' },
          { offset: 1, color: 'rgba(13, 148, 136, 0)' }
        ]
      }
    }
  }]
}))

const answerersChartOptions = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    borderColor: '#e5e7eb',
    borderWidth: 1,
    textStyle: { color: '#374151', fontSize: 12 },
    extraCssText: 'box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-radius: 8px;'
  },
  grid: {
    left: '3%',
    right: '8%',
    bottom: '3%',
    top: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
    axisLabel: { color: '#6b7280', fontSize: 11 }
  },
  yAxis: {
    type: 'category',
    data: answerersData.value.map(d => d.name),
    axisLine: { lineStyle: { color: '#e5e7eb' } },
    axisLabel: { color: '#6b7280', fontSize: 11 }
  },
  series: [{
    data: answerersData.value.map((d, i) => ({
      value: d.count,
      itemStyle: {
        color: i < 3 ? '#0d9488' : '#14b8a6',
        borderRadius: [0, 4, 4, 0]
      }
    })),
    type: 'bar',
    barWidth: '60%',
    label: {
      show: true,
      position: 'right',
      color: '#6b7280',
      fontSize: 11
    }
  }]
}))

const tagsChartOptions = computed(() => {
  const data = tagsData.value.map((d, i) => ({
    name: d.name,
    value: d.value,
    itemStyle: {
      color: ['#0d9488', '#14b8a6', '#2dd4bf', '#5eead4', '#99f6e4', '#f59e0b', '#fbbf24', '#fcd34d'][i % 8]
    }
  }))
  return {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.98)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: { color: '#374151', fontSize: 12 },
      formatter: '{b}: {c}',
      extraCssText: 'box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border-radius: 8px;'
    },
    series: [{
      type: 'treemap',
      data,
      roam: false,
      label: {
        show: true,
        formatter: '{b}',
        color: '#fff',
        fontSize: 11,
        fontWeight: 500
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 2,
        gapWidth: 2
      },
      upperLabel: {
        show: false
      },
      levels: [
        {
          itemStyle: {
            borderColor: '#e5e7eb',
            borderWidth: 3,
            gapWidth: 3
          }
        },
        {
          colorSaturation: [0.25, 0.5],
          itemStyle: {
            borderColorSaturation: 0.6,
            borderWidth: 2,
            gapWidth: 2
          }
        }
      ]
    }]
  }
})

// Methods
const fetchOverview = async () => {
  try {
    const res = await request.get('/api/statistics/overview/')
    if (res.code === 0) {
      overviewData.value = res.data
    }
  } catch (e) {
    console.error('Failed to fetch overview:', e)
  } finally {
    loading.value.overview = false
  }
}

const fetchTrend = async () => {
  try {
    const res = await request.get('/api/statistics/trend/')
    if (res.code === 0) {
      trendData.value = res.data || []
    }
  } catch (e) {
    console.error('Failed to fetch trend:', e)
  } finally {
    loading.value.trend = false
  }
}

const fetchAnswerers = async () => {
  try {
    const res = await request.get('/api/statistics/answerers/')
    if (res.code === 0) {
      answerersData.value = (res.data || []).slice(0, 10)
    }
  } catch (e) {
    console.error('Failed to fetch answerers:', e)
  } finally {
    loading.value.answerers = false
  }
}

const fetchTags = async () => {
  try {
    const res = await request.get('/api/statistics/categories/')
    if (res.code === 0) {
      tagsData.value = (res.data || []).slice(0, 50)
    }
  } catch (e) {
    console.error('Failed to fetch categories:', e)
  } finally {
    loading.value.tags = false
  }
}

const fetchCrawlerStatus = async () => {
  try {
    const res = await request.get('/api/crawler/status/')
    if (res.code === 0) {
      crawlerData.value = res.data
    }
  } catch (e) {
    console.error('Failed to fetch crawler status:', e)
  }
}

const handleStartCrawler = async (mode) => {
  crawlerLoading.value = true
  crawlerMessage.value = ''
  try {
    const res = await request.post('/api/crawler/start/', { mode, limit: 20 })
    if (res.code === 0) {
      crawlerMessage.value = '采集任务已启动'
      crawlerMessageType.value = 'success'
      await fetchCrawlerStatus()
    } else {
      crawlerMessage.value = res.message || '启动失败'
      crawlerMessageType.value = 'error'
    }
  } catch (e) {
    crawlerMessage.value = '启动失败，请稍后重试'
    crawlerMessageType.value = 'error'
  } finally {
    crawlerLoading.value = false
  }
}

const handleStopCrawler = async () => {
  crawlerLoading.value = true
  crawlerMessage.value = ''
  try {
    const res = await request.post('/api/crawler/stop/')
    if (res.code === 0) {
      crawlerMessage.value = '采集已停止'
      crawlerMessageType.value = 'info'
      await fetchCrawlerStatus()
    } else {
      crawlerMessage.value = res.message || '停止失败'
      crawlerMessageType.value = 'error'
    }
  } catch (e) {
    crawlerMessage.value = '停止失败，请稍后重试'
    crawlerMessageType.value = 'error'
  } finally {
    crawlerLoading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchOverview()
  fetchTrend()
  fetchAnswerers()
  fetchTags()
  fetchCrawlerStatus()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 2rem;
  position: relative;
}

.dashboard::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(13, 148, 136, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(245, 158, 11, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

/* Header */
.dashboard-header {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-family: 'Outfit', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.user-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  border-radius: 50%;
  font-size: 0.875rem;
  font-weight: 600;
  color: #fff;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #334155;
}

/* Overview Cards */
.overview-section {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.stat-card {
  position: relative;
  padding: 1.5rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out forwards;
  animation-delay: var(--delay);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border-color: rgba(13, 148, 136, 0.3);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--card-accent, #0d9488);
}

.stat-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-icon :deep(svg) {
  width: 24px;
  height: 24px;
  color: #fff;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  font-family: 'Outfit', 'SF Mono', 'Fira Code', monospace;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.trend-icon {
  font-size: 0.75rem;
}

.trend-icon.up {
  color: #10b981;
}

.trend-icon.down {
  color: #ef4444;
}

.trend-text {
  color: #64748b;
}

.stat-glow {
  position: absolute;
  bottom: -30px;
  right: -30px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, var(--card-accent, #0d9488) 0%, transparent 70%);
  opacity: 0.08;
  border-radius: 50%;
}

/* Charts */
.charts-section {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

.chart-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chart-card:hover {
  border-color: rgba(13, 148, 136, 0.3);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.chart-card.large {
  grid-row: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.title-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(20, 184, 166, 0.1) 100%);
  border-radius: 10px;
  color: #0d9488;
}

.title-icon svg {
  width: 18px;
  height: 18px;
}

.data-badge {
  padding: 0.375rem 0.875rem;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.08) 0%, rgba(20, 184, 166, 0.08) 100%);
  border: 1px solid rgba(13, 148, 136, 0.2);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #0d9488;
}

.card-body {
  position: relative;
  height: 300px;
  padding: 1rem;
}

.chart-card.large .card-body {
  height: calc(100% - 65px);
}

.chart-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(13, 148, 136, 0.15);
  border-top-color: #0d9488;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #94a3b8;
}

.empty-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  margin-bottom: 0.75rem;
}

.empty-icon svg {
  width: 24px;
  height: 24px;
  color: #cbd5e1;
}

.chart-empty p {
  margin: 0;
  font-size: 0.875rem;
}

/* Crawler Section */
.crawler-section {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.crawler-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.08);
}

.crawler-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(90deg, rgba(245, 158, 11, 0.08) 0%, transparent 100%);
  border-bottom: 1px solid rgba(245, 158, 11, 0.15);
}

.crawler-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.crawler-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  border-radius: 10px;
}

.crawler-icon svg {
  width: 18px;
  height: 18px;
  color: #fff;
}

.crawler-title h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.crawler-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 1rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.crawler-status.idle {
  background: #f1f5f9;
  color: #64748b;
}

.crawler-status.idle .status-dot {
  background: #94a3b8;
}

.crawler-status.running {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
}

.crawler-status.running .status-dot {
  background: #f59e0b;
}

.crawler-status.completed {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
}

.crawler-status.completed .status-dot {
  background: #10b981;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.crawler-body {
  padding: 1.5rem;
}

.progress-section {
  margin-bottom: 1.5rem;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.875rem;
  color: #64748b;
}

.progress-percent {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f59e0b;
}

.progress-bar {
  height: 10px;
  background: #f1f5f9;
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
  border-radius: 5px;
  transition: width 0.3s ease;
}

.progress-detail {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #94a3b8;
}

.crawler-actions {
  display: flex;
  gap: 1rem;
}

.crawler-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.crawler-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.crawler-btn.primary {
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  color: #fff;
}

.crawler-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(13, 148, 136, 0.3);
}

.crawler-btn.secondary {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.crawler-btn.secondary:hover:not(:disabled) {
  background: #e2e8f0;
}

.btn-icon {
  display: flex;
}

.btn-icon svg {
  width: 14px;
  height: 14px;
}

.crawler-message {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.875rem;
}

.crawler-message.success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #059669;
}

.crawler-message.error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #dc2626;
}

.crawler-message.info {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

/* Responsive */
@media (max-width: 1280px) {
  .overview-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr 1fr;
  }

  .chart-card.large {
    grid-column: span 2;
    grid-row: span 1;
  }

  .chart-card.large .card-body {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .overview-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-card.large {
    grid-column: span 1;
  }

  .crawler-actions {
    flex-direction: column;
  }
}
</style>
