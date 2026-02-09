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
            <span class="user-avatar">{{ userInitials }}</span>
            <span class="user-name">{{ authStore.userInfo?.username }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Overview Cards -->
    <section class="overview-section">
      <div class="overview-grid">
        <div v-for="(card, index) in overviewCards" :key="index" class="stat-card" :style="{ '--delay': `${index * 0.1}s` }">
          <div class="stat-icon" :style="{ background: card.gradient }">
            <component :is="card.icon" />
          </div>
          <div class="stat-content">
            <span class="stat-value" :style="{ color: card.color }">{{ card.value }}</span>
            <span class="stat-label">{{ card.label }}</span>
          </div>
          <div class="stat-decoration"></div>
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
              <span class="title-icon">↗</span>
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
            <ECharts v-else :options="trendChartOptions" theme="dark" />
            <div v-if="!loading.trend && !trendData.length" class="chart-empty">
              <span class="empty-icon">○</span>
              <p>暂无数据</p>
            </div>
          </div>
        </div>

        <!-- Answerers Chart -->
        <div class="chart-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon">◉</span>
              高频回答者
            </h3>
          </div>
          <div class="card-body">
            <div v-if="loading.answerers" class="chart-loading">
              <div class="loading-spinner"></div>
            </div>
            <ECharts v-else :options="answerersChartOptions" theme="dark" />
            <div v-if="!loading.answerers && !answerersData.length" class="chart-empty">
              <span class="empty-icon">○</span>
              <p>暂无数据</p>
            </div>
          </div>
        </div>

        <!-- Tags Treemap -->
        <div class="chart-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon">▦</span>
              标签分布
            </h3>
          </div>
          <div class="card-body">
            <div v-if="loading.tags" class="chart-loading">
              <div class="loading-spinner"></div>
            </div>
            <ECharts v-else :options="tagsChartOptions" theme="dark" />
            <div v-if="!loading.tags && !tagsData.length" class="chart-empty">
              <span class="empty-icon">○</span>
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
            <span class="crawler-icon">⚡</span>
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
              <span class="btn-icon">▶</span>
              <span>{{ crawlerLoading ? '启动中...' : '开始采集' }}</span>
            </button>
            <button
              class="crawler-btn secondary"
              :disabled="crawlerLoading || !crawlerData.has_active_task"
              @click="handleStopCrawler"
            >
              <span class="btn-icon">◼</span>
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
  total_tags: 0,
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
    color: '#f0a500',
    gradient: 'linear-gradient(135deg, #f0a500 0%, #f5af19 100%)'
  },
  {
    icon: IconTag,
    label: '标签数量',
    value: overviewData.value.total_tags.toLocaleString(),
    color: '#00d2ff',
    gradient: 'linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)'
  },
  {
    icon: IconUser,
    label: '回答者',
    value: overviewData.value.total_answerers.toLocaleString(),
    color: '#a8ff78',
    gradient: 'linear-gradient(135deg, #a8ff78 0%, #78ffd6 100%)'
  },
  {
    icon: IconCalendar,
    label: '今日新增',
    value: overviewData.value.today_questions.toLocaleString(),
    color: '#ff6b6b',
    gradient: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)'
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
    backgroundColor: 'rgba(20, 25, 40, 0.95)',
    borderColor: '#2d3748',
    textStyle: { color: '#e2e8f0' }
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
    axisLine: { lineStyle: { color: '#4a5568' } },
    axisLabel: { color: '#a0aec0', fontSize: 11 },
    boundaryGap: false
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    splitLine: { lineStyle: { color: '#2d3748', type: 'dashed' } },
    axisLabel: { color: '#a0aec0', fontSize: 11 }
  },
  series: [{
    data: trendData.value.map(d => d.count),
    type: 'line',
    smooth: true,
    symbol: 'circle',
    symbolSize: 8,
    lineStyle: {
      color: '#f0a500',
      width: 3
    },
    itemStyle: {
      color: '#f0a500',
      borderColor: '#1a202c',
      borderWidth: 2
    },
    areaStyle: {
      color: {
        type: 'linear',
        x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(240, 165, 0, 0.4)' },
          { offset: 1, color: 'rgba(240, 165, 0, 0)' }
        ]
      }
    }
  }]
}))

const answerersChartOptions = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(20, 25, 40, 0.95)',
    borderColor: '#2d3748',
    textStyle: { color: '#e2e8f0' }
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
    splitLine: { lineStyle: { color: '#2d3748', type: 'dashed' } },
    axisLabel: { color: '#a0aec0', fontSize: 11 }
  },
  yAxis: {
    type: 'category',
    data: answerersData.value.map(d => d.name),
    axisLine: { lineStyle: { color: '#4a5568' } },
    axisLabel: { color: '#a0aec0', fontSize: 11 }
  },
  series: [{
    data: answerersData.value.map((d, i) => ({
      value: d.count,
      itemStyle: {
        color: i < 3 ? '#f0a500' : '#00d2ff',
        borderRadius: [0, 4, 4, 0]
      }
    })),
    type: 'bar',
    barWidth: '60%',
    label: {
      show: true,
      position: 'right',
      color: '#a0aec0',
      fontSize: 11
    }
  }]
}))

const tagsChartOptions = computed(() => {
  const data = tagsData.value.map(d => ({
    name: d.name,
    value: d.value
  }))
  return {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(20, 25, 40, 0.95)',
      borderColor: '#2d3748',
      textStyle: { color: '#e2e8f0' },
      formatter: '{b}: {c}'
    },
    series: [{
      type: 'treemap',
      data,
      roam: false,
      label: {
        show: true,
        formatter: '{b}',
        color: '#fff',
        fontSize: 11
      },
      itemStyle: {
        borderColor: '#0a0e17',
        borderWidth: 2,
        gapWidth: 2
      },
      upperLabel: {
        show: false
      },
      levels: [
        {
          itemStyle: {
            borderColor: '#1a202c',
            borderWidth: 3,
            gapWidth: 3
          }
        },
        {
          colorSaturation: [0.3, 0.6],
          itemStyle: {
            borderColorSaturation: 0.7,
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
    const res = await request.get('/api/statistics/tags/')
    if (res.code === 0) {
      tagsData.value = (res.data || []).slice(0, 50)
    }
  } catch (e) {
    console.error('Failed to fetch tags:', e)
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
  background: linear-gradient(180deg, #0a0e17 0%, #111827 50%, #0d1117 100%);
  padding: 2rem;
}

/* Header */
.dashboard-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 0.25rem;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(71, 85, 105, 0.4);
  border-radius: 9999px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0a500 0%, #f5af19 100%);
  border-radius: 50%;
  font-size: 0.875rem;
  font-weight: 600;
  color: #0a0e17;
}

.user-name {
  font-size: 0.875rem;
  color: #e2e8f0;
}

/* Overview Cards */
.overview-section {
  margin-bottom: 2rem;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.stat-card {
  position: relative;
  padding: 1.5rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(51, 65, 85, 0.4);
  border-radius: 16px;
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out forwards;
  animation-delay: var(--delay);
  opacity: 0;
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
  height: 3px;
  background: var(--card-accent, #f0a500);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  margin-bottom: 1rem;
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
  font-size: 1.75rem;
  font-weight: 700;
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.stat-label {
  font-size: 0.85rem;
  color: #64748b;
}

.stat-decoration {
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, var(--card-accent, #f0a500) 0%, transparent 70%);
  opacity: 0.1;
  border-radius: 50%;
}

/* Charts */
.charts-section {
  margin-bottom: 2rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

.chart-card {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(51, 65, 85, 0.4);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.chart-card:hover {
  border-color: rgba(71, 85, 105, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.chart-card.large {
  grid-row: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.3);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0;
}

.title-icon {
  color: #f0a500;
  font-size: 1.125rem;
}

.data-badge {
  padding: 0.25rem 0.75rem;
  background: rgba(240, 165, 0, 0.1);
  border: 1px solid rgba(240, 165, 0, 0.3);
  border-radius: 9999px;
  font-size: 0.75rem;
  color: #f0a500;
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
  border: 3px solid rgba(240, 165, 0, 0.2);
  border-top-color: #f0a500;
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
  color: #64748b;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.chart-empty p {
  margin: 0;
  font-size: 0.875rem;
}

/* Crawler Section */
.crawler-section {
  margin-bottom: 2rem;
}

.crawler-card {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
  border: 1px solid rgba(240, 165, 0, 0.3);
  border-radius: 16px;
  overflow: hidden;
}

.crawler-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(90deg, rgba(240, 165, 0, 0.1) 0%, transparent 100%);
  border-bottom: 1px solid rgba(240, 165, 0, 0.2);
}

.crawler-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.crawler-icon {
  font-size: 1.25rem;
}

.crawler-title h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #f1f5f9;
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
  background: rgba(71, 85, 105, 0.3);
  color: #94a3b8;
}

.crawler-status.idle .status-dot {
  background: #94a3b8;
}

.crawler-status.running {
  background: rgba(240, 165, 0, 0.15);
  color: #f0a500;
}

.crawler-status.running .status-dot {
  background: #f0a500;
}

.crawler-status.completed {
  background: rgba(168, 255, 120, 0.15);
  color: #a8ff78;
}

.crawler-status.completed .status-dot {
  background: #a8ff78;
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
  color: #94a3b8;
}

.progress-percent {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f0a500;
}

.progress-bar {
  height: 8px;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f0a500 0%, #f5af19 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-detail {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #64748b;
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.crawler-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.crawler-btn.primary {
  background: linear-gradient(135deg, #f0a500 0%, #f5af19 100%);
  color: #0a0e17;
}

.crawler-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(240, 165, 0, 0.4);
}

.crawler-btn.secondary {
  background: rgba(51, 65, 85, 0.5);
  color: #e2e8f0;
  border: 1px solid rgba(71, 85, 105, 0.5);
}

.crawler-btn.secondary:hover:not(:disabled) {
  background: rgba(71, 85, 105, 0.6);
}

.btn-icon {
  font-size: 0.75rem;
}

.crawler-message {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
}

.crawler-message.success {
  background: rgba(168, 255, 120, 0.1);
  border: 1px solid rgba(168, 255, 120, 0.3);
  color: #a8ff78;
}

.crawler-message.error {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: #ff6b6b;
}

.crawler-message.info {
  background: rgba(100, 116, 139, 0.2);
  border: 1px solid rgba(100, 116, 139, 0.3);
  color: #94a3b8;
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
