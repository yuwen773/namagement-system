<template>
  <div class="admin-dashboard-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">数据总览仪表盘</h1>
          <p class="page-subtitle">实时监控平台关键指标与数据趋势</p>
        </div>
        <div class="header-actions">
          <el-select v-model="trendPeriod" @change="fetchTrends" class="period-select" :disabled="loading">
            <el-option label="按天" value="day" />
            <el-option label="按周" value="week" />
            <el-option label="按月" value="month" />
          </el-select>
          <el-select v-model="trendDays" @change="fetchTrends" class="days-select" :disabled="loading">
            <el-option label="最近7天" :value="7" />
            <el-option label="最近30天" :value="30" />
            <el-option label="最近60天" :value="60" />
            <el-option label="最近90天" :value="90" />
          </el-select>
          <button @click="refreshData" class="refresh-btn" :disabled="loading" title="刷新数据">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            刷新
          </button>
        </div>
      </div>
      <div v-if="lastUpdated" class="last-updated">
        上次更新：{{ formatTime(lastUpdated) }}
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !overviewData" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">加载数据中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">!</div>
      <h3 class="error-title">数据加载失败</h3>
      <p class="error-message">{{ error }}</p>
      <button @click="fetchData" class="retry-button">重试</button>
    </div>

    <!-- Content Area -->
    <div v-else class="dashboard-content">
      <!-- Overview Metrics Cards -->
      <section class="metrics-section">
        <div class="metric-card" :class="{ 'loading': loading }">
          <div class="metric-icon" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="metric-content">
            <span class="metric-label">总菜谱数</span>
            <span class="metric-value">{{ formatNumber(overviewData?.total_recipes) }}</span>
            <div class="metric-footer">
              <span class="metric-change positive">+{{ overviewData?.today_new_recipes || 0 }}</span>
              <span class="metric-change-label">今日新增</span>
            </div>
          </div>
        </div>

        <div class="metric-card" :class="{ 'loading': loading }">
          <div class="metric-icon" style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="metric-content">
            <span class="metric-label">总用户数</span>
            <span class="metric-value">{{ formatNumber(overviewData?.total_users) }}</span>
            <div class="metric-footer">
              <span class="metric-change positive">+{{ overviewData?.today_new_users || 0 }}</span>
              <span class="metric-change-label">今日新增</span>
            </div>
          </div>
        </div>

        <div class="metric-card" :class="{ 'loading': loading }">
          <div class="metric-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="metric-content">
            <span class="metric-label">总收藏数</span>
            <span class="metric-value">{{ formatNumber(overviewData?.total_favorites) }}</span>
            <div class="metric-footer">
              <span class="metric-info">总收藏量</span>
            </div>
          </div>
        </div>

        <div class="metric-card" :class="{ 'loading': loading }">
          <div class="metric-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="metric-content">
            <span class="metric-label">今日活跃用户</span>
            <span class="metric-value">{{ formatNumber(overviewData?.today_active_users) }}</span>
            <div class="metric-footer">
              <span class="metric-info">日活跃(DAU)</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Charts Section -->
      <div class="charts-grid">
        <!-- Trend Chart -->
        <section class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">数据增长趋势</h2>
            <span class="chart-subtitle">{{ periodLabel }}趋势分析</span>
          </div>
          <div ref="trendChart" class="chart-container"></div>
        </section>

        <!-- Active Users Chart -->
        <section class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">活跃用户分布</h2>
            <span class="chart-subtitle">DAU / WAU / MAU</span>
          </div>
          <div ref="activeUsersChart" class="chart-container"></div>
        </section>
      </div>

      <!-- Behavior Distribution -->
      <div class="charts-grid">
        <!-- Behavior Distribution Chart -->
        <section class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">用户行为分布</h2>
            <span class="chart-subtitle">各类行为数量统计</span>
          </div>
          <div ref="behaviorChart" class="chart-container"></div>
        </section>

        <!-- Page Views Chart -->
        <section class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">页面访问量</h2>
            <span class="chart-subtitle">各页面访问统计</span>
          </div>
          <div ref="pageViewsChart" class="chart-container"></div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  getDashboardOverview,
  getDashboardTrends,
  getDashboardBehaviors
} from '../api/analytics'

// State
const loading = ref(false)
const error = ref(null)
const overviewData = ref(null)
const trendsData = ref(null)
const behaviorsData = ref(null)
const lastUpdated = ref(null)

// Trend params
const trendPeriod = ref('day')
const trendDays = ref(30)

// Chart refs
const trendChart = ref(null)
const activeUsersChart = ref(null)
const behaviorChart = ref(null)
const pageViewsChart = ref(null)

// Chart instances
let trendChartInstance = null
let activeUsersChartInstance = null
let behaviorChartInstance = null
let pageViewsChartInstance = null

// Period label
const periodLabel = computed(() => {
  const labels = {
    day: '每日',
    week: '每周',
    month: '每月'
  }
  return labels[trendPeriod.value] || '每日'
})

/**
 * Format number with commas
 */
function formatNumber(num) {
  if (num === null || num === undefined) return '-'
  return Number(num).toLocaleString('zh-CN')
}

/**
 * Format time
 */
function formatTime(isoString) {
  if (!isoString) return '-'
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * Fetch all data
 */
async function fetchData() {
  loading.value = true
  error.value = null

  try {
    await Promise.all([
      fetchOverview(),
      fetchTrends(),
      fetchBehaviors()
    ])

    loading.value = false
    await renderAllCharts()
  } catch (err) {
    error.value = err.message || '数据加载失败，请稍后重试'
    loading.value = false
  }
}

/**
 * Refresh data
 */
async function refreshData() {
  await fetchData()
  ElMessage.success('数据已刷新')
}

/**
 * Fetch overview data
 */
async function fetchOverview() {
  const response = await getDashboardOverview()
  overviewData.value = response?.data || null
  lastUpdated.value = response?.data?.updated_at || null
}

/**
 * Fetch trends data
 */
async function fetchTrends() {
  const response = await getDashboardTrends({
    period: trendPeriod.value,
    days: trendDays.value
  })
  trendsData.value = response?.data || null
  await renderTrendChart()
}

/**
 * Fetch behaviors data
 */
async function fetchBehaviors() {
  const response = await getDashboardBehaviors()
  behaviorsData.value = response?.data || null
  await renderBehaviorCharts()
}

/**
 * Render all charts
 */
async function renderAllCharts() {
  await Promise.all([
    renderTrendChart(),
    renderBehaviorCharts()
  ])
}

/**
 * Render trend chart
 */
async function renderTrendChart() {
  if (!trendChart.value || !trendsData.value?.data) return

  if (trendChartInstance) {
    trendChartInstance.dispose()
  }

  trendChartInstance = echarts.init(trendChart.value)
  const data = trendsData.value.data

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' }
    },
    legend: {
      data: ['菜谱数量', '用户数量', '收藏数量'],
      bottom: 10,
      textStyle: { color: '#6b5c4d', fontFamily: 'DM Sans' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.dates || [],
      axisLine: { lineStyle: { color: '#e5ddd3' } },
      axisTick: { show: false },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 10,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } },
      axisLabel: { color: '#8b7355', fontFamily: 'DM Sans' }
    },
    series: [
      {
        name: '菜谱数量',
        type: 'line',
        data: data.recipe_counts || [],
        smooth: true,
        itemStyle: { color: '#ff6b6b' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(255, 107, 107, 0.3)' },
              { offset: 1, color: 'rgba(255, 107, 107, 0.05)' }
            ]
          }
        }
      },
      {
        name: '用户数量',
        type: 'line',
        data: data.user_counts || [],
        smooth: true,
        itemStyle: { color: '#4ecdc4' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(78, 205, 196, 0.3)' },
              { offset: 1, color: 'rgba(78, 205, 196, 0.05)' }
            ]
          }
        }
      },
      {
        name: '收藏数量',
        type: 'line',
        data: data.favorite_counts || [],
        smooth: true,
        itemStyle: { color: '#667eea' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
              { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
            ]
          }
        }
      }
    ]
  }

  trendChartInstance.setOption(option)
}

/**
 * Render behavior charts
 */
async function renderBehaviorCharts() {
  await Promise.all([
    renderActiveUsersChart(),
    renderBehaviorDistributionChart(),
    renderPageViewsChart()
  ])
}

/**
 * Render active users chart
 */
async function renderActiveUsersChart() {
  if (!activeUsersChart.value || !behaviorsData.value?.active_user_distribution) return

  if (activeUsersChartInstance) {
    activeUsersChartInstance.dispose()
  }

  activeUsersChartInstance = echarts.init(activeUsersChart.value)
  const data = behaviorsData.value.active_user_distribution

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' },
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 20,
      top: 'center',
      textStyle: { color: '#6b5c4d', fontFamily: 'DM Sans' }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
            color: '#3d2914'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: data.dau || 0, name: '日活跃(DAU)', itemStyle: { color: '#ff6b6b' } },
          { value: data.wau || 0, name: '周活跃(WAU)', itemStyle: { color: '#4ecdc4' } },
          { value: data.mau || 0, name: '月活跃(MAU)', itemStyle: { color: '#667eea' } }
        ]
      }
    ]
  }

  activeUsersChartInstance.setOption(option)
}

/**
 * Render behavior distribution chart
 */
async function renderBehaviorDistributionChart() {
  if (!behaviorChart.value || !behaviorsData.value?.behavior_distribution) return

  if (behaviorChartInstance) {
    behaviorChartInstance.dispose()
  }

  behaviorChartInstance = echarts.init(behaviorChart.value)
  const data = behaviorsData.value.behavior_distribution

  const behaviorNames = {
    login: '登录',
    search: '搜索',
    view: '浏览',
    favorite: '收藏'
  }

  const chartData = Object.entries(data).map(([key, value]) => ({
    name: behaviorNames[key] || key,
    value: value
  }))

  const colors = ['#f093fb', '#667eea', '#4ecdc4', '#ff6b6b']

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' },
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 20,
      top: 'center',
      textStyle: { color: '#6b5c4d', fontFamily: 'DM Sans' }
    },
    series: [
      {
        type: 'pie',
        radius: ['45%', '75%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}\n{d}%',
          color: '#6b5c4d',
          fontFamily: 'DM Sans'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.2)'
          }
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10
        },
        data: chartData.map((item, index) => ({
          ...item,
          itemStyle: { color: colors[index % colors.length] }
        }))
      }
    ]
  }

  behaviorChartInstance.setOption(option)
}

/**
 * Render page views chart
 */
async function renderPageViewsChart() {
  if (!pageViewsChart.value || !behaviorsData.value?.page_views) return

  if (pageViewsChartInstance) {
    pageViewsChartInstance.dispose()
  }

  pageViewsChartInstance = echarts.init(pageViewsChart.value)
  const data = behaviorsData.value.page_views

  const pageNames = {
    recipe_detail: '菜谱详情页'
  }

  const chartData = Object.entries(data).map(([key, value]) => ({
    name: pageNames[key] || key,
    value: value
  }))

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' },
      formatter: '{b}: {c}'
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
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } },
      axisLabel: { color: '#8b7355', fontFamily: 'DM Sans' }
    },
    yAxis: {
      type: 'category',
      data: chartData.map(item => item.name),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 12
      }
    },
    series: [
      {
        type: 'bar',
        data: chartData.map((item, index) => ({
          value: item.value,
          itemStyle: {
            color: index === 0 ? '#ff6b6b' : '#c2622e',
            borderRadius: [0, 8, 8, 0]
          }
        })),
        barWidth: '60%',
        label: {
          show: true,
          position: 'right',
          formatter: '{c}',
          color: '#6b5c4d',
          fontFamily: 'DM Sans'
        }
      }
    ]
  }

  pageViewsChartInstance.setOption(option)
}

/**
 * Handle window resize
 */
function handleResize() {
  trendChartInstance?.resize()
  activeUsersChartInstance?.resize()
  behaviorChartInstance?.resize()
  pageViewsChartInstance?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  trendChartInstance?.dispose()
  activeUsersChartInstance?.dispose()
  behaviorChartInstance?.dispose()
  pageViewsChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* Base Styles */
.admin-dashboard-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
  padding: 2rem;
  font-family: 'DM Sans', 'Noto Sans SC', sans-serif;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-left {
  text-align: left;
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  font-size: 1rem;
  color: #8b7355;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.period-select,
.days-select {
  min-width: 100px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem;
  white-space: nowrap;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn svg {
  width: 16px;
  height: 16px;
}

.last-updated {
  max-width: 1600px;
  margin: 0.5rem auto 0;
  font-size: 0.85rem;
  color: #8b7355;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e5ddd3;
  border-top-color: #c2622e;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #8b7355;
  margin-top: 1rem;
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.error-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  font-size: 2rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.error-message {
  color: #8b7355;
  margin: 0 0 1.5rem 0;
}

.retry-button {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

/* Dashboard Content */
.dashboard-content {
  max-width: 1600px;
  margin: 0 auto;
}

/* Metrics Section */
.metrics-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  display: flex;
  gap: 1rem;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(61, 41, 20, 0.12);
}

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.metric-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.metric-label {
  font-size: 0.85rem;
  color: #8b7355;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #3d2914;
}

.metric-footer {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.metric-change {
  font-size: 0.85rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #4caf50;
}

.metric-change-label,
.metric-info {
  font-size: 0.8rem;
  color: #8b7355;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

/* Chart Card */
.chart-card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
}

.chart-header {
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 0.25rem 0;
}

.chart-subtitle {
  font-size: 0.85rem;
  color: #8b7355;
}

.chart-container {
  width: 100%;
  height: 320px;
}

/* Responsive */
@media (max-width: 1024px) {
  .admin-dashboard-page {
    padding: 1rem;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 280px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .period-select,
  .days-select {
    flex: 1;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .metrics-section {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 250px;
  }
}
</style>
