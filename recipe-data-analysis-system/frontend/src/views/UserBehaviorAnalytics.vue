<template>
  <div class="user-behavior-analytics-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">用户行为分析</h1>
          <p class="page-subtitle">深度洞察用户行为模式，优化产品体验</p>
        </div>
        <div class="header-actions">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="default"
            @change="handleDateChange"
          />
          <button @click="exportData" class="export-btn" :disabled="loading || !currentTabData">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            导出数据
          </button>
        </div>
      </div>
    </div>

    <!-- Analysis Tabs -->
    <div class="tabs-container">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="switchTab(tab.key)"
        class="tab-btn"
        :class="{ active: currentTab === tab.key }"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
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
    <div v-else class="content-area">
      <!-- Click Stream Analysis -->
      <div v-if="currentTab === 'clickstream'" class="analysis-content">
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总行为记录</span>
            <span class="card-value">{{ formatNumber(clickstreamData?.summary?.total_logs) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">独立用户数</span>
            <span class="card-value">{{ formatNumber(clickstreamData?.summary?.unique_users) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">分析天数</span>
            <span class="card-value">{{ clickstreamData?.summary?.days || 0 }} 天</span>
          </div>
          <div class="summary-card">
            <span class="card-label">整体转化率</span>
            <span class="card-value">{{ clickstreamData?.conversion_funnel?.overall_conversion_rate?.toFixed(2) || 0 }}%</span>
          </div>
        </div>

        <!-- Conversion Funnel -->
        <div class="chart-section">
          <h3 class="section-title">转化漏斗</h3>
          <div ref="funnelChart" class="chart-container funnel-chart"></div>
        </div>

        <!-- Behavior Distribution -->
        <div class="chart-section">
          <h3 class="section-title">行为类型分布</h3>
          <div ref="behaviorChart" class="chart-container"></div>
        </div>

        <!-- Path Patterns -->
        <div class="table-section">
          <h3 class="section-title">常见访问路径</h3>
          <el-table :data="clickstreamData?.path_patterns || []" stripe style="width: 100%">
            <el-table-column prop="path" label="访问路径" min-width="250" show-overflow-tooltip />
            <el-table-column prop="count" label="次数" sortable width="100">
              <template #default="{ row }">{{ formatNumber(row.count) }}</template>
            </el-table-column>
            <el-table-column prop="percentage" label="占比" width="100">
              <template #default="{ row }">{{ row.percentage.toFixed(2) }}%</template>
            </el-table-column>
            <el-table-column prop="views" label="浏览数" width="100">
              <template #default="{ row }">{{ formatNumber(row.views) }}</template>
            </el-table-column>
            <el-table-column prop="collects" label="收藏数" width="100">
              <template #default="{ row }">{{ formatNumber(row.collects) }}</template>
            </el-table-column>
            <el-table-column prop="conversion_rate" label="转化率" width="100">
              <template #default="{ row }">{{ row.conversion_rate.toFixed(2) }}%</template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Active Users Analysis -->
      <div v-else-if="currentTab === 'active'" class="analysis-content">
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总用户数</span>
            <span class="card-value">{{ formatNumber(activeData?.summary?.total_users) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">今日活跃</span>
            <span class="card-value highlight">{{ formatNumber(activeData?.summary?.active_today) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">本周活跃</span>
            <span class="card-value">{{ formatNumber(activeData?.summary?.active_week) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">本月活跃</span>
            <span class="card-value">{{ formatNumber(activeData?.summary?.active_month) }}</span>
          </div>
        </div>

        <!-- DAU/WAU/MAU Trend -->
        <div class="chart-section">
          <h3 class="section-title">活跃用户趋势</h3>
          <div ref="activeTrendChart" class="chart-container"></div>
        </div>

        <!-- DAU Change -->
        <div class="stats-row">
          <div class="stat-card">
            <span class="stat-label">日活跃用户（DAU）</span>
            <span class="stat-value">{{ formatNumber(activeData?.dau?.today) }}</span>
            <span class="stat-change" :class="activeData?.dau?.change_rate >= 0 ? 'positive' : 'negative'">
              {{ activeData?.dau?.change_rate >= 0 ? '+' : '' }}{{ activeData?.dau?.change_rate?.toFixed(2) }}%
            </span>
          </div>
          <div class="stat-card">
            <span class="stat-label">周活跃用户（WAU）</span>
            <span class="stat-value">{{ formatNumber(activeData?.wau?.current) }}</span>
            <span class="stat-change" :class="activeData?.wau?.change_rate >= 0 ? 'positive' : 'negative'">
              {{ activeData?.wau?.change_rate >= 0 ? '+' : '' }}{{ activeData?.wau?.change_rate?.toFixed(2) }}%
            </span>
          </div>
          <div class="stat-card">
            <span class="stat-label">月活跃用户（MAU）</span>
            <span class="stat-value">{{ formatNumber(activeData?.mau?.current) }}</span>
            <span class="stat-change" :class="activeData?.mau?.change_rate >= 0 ? 'positive' : 'negative'">
              {{ activeData?.mau?.change_rate >= 0 ? '+' : '' }}{{ activeData?.mau?.change_rate?.toFixed(2) }}%
            </span>
          </div>
          <div class="stat-card">
            <span class="stat-label">留存率（DAU/MAU）</span>
            <span class="stat-value">{{ activeData?.stickiness?.dau_mau_ratio?.toFixed(2) || 0 }}%</span>
            <span class="stat-label-small">粘性指标</span>
          </div>
        </div>
      </div>

      <!-- Login Frequency Analysis -->
      <div v-else-if="currentTab === 'login'" class="analysis-content">
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总登录次数</span>
            <span class="card-value">{{ formatNumber(loginData?.summary?.total_logs) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">分析天数</span>
            <span class="card-value">{{ loginData?.summary?.days || 0 }} 天</span>
          </div>
          <div class="summary-card">
            <span class="card-label">总用户数</span>
            <span class="card-value">{{ formatNumber(loginData?.summary?.total_users) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">日均登录</span>
            <span class="card-value">{{ formatNumber(Math.round(loginData?.summary?.total_logs / loginData?.summary?.days)) }}</span>
          </div>
        </div>

        <!-- Login Frequency Distribution -->
        <div class="chart-section">
          <h3 class="section-title">用户登录频率分布</h3>
          <div ref="loginFreqChart" class="chart-container"></div>
        </div>

        <!-- Hourly Distribution -->
        <div class="chart-section">
          <h3 class="section-title">登录时段分布</h3>
          <div ref="hourlyChart" class="chart-container"></div>
        </div>

        <!-- Daily Trend -->
        <div class="chart-section">
          <h3 class="section-title">每日登录趋势</h3>
          <div ref="loginTrendChart" class="chart-container"></div>
        </div>
      </div>

      <!-- Page Duration Analysis -->
      <div v-else-if="currentTab === 'duration'" class="analysis-content">
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总访问记录</span>
            <span class="card-value">{{ formatNumber(pageData?.summary?.total_logs) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">分析天数</span>
            <span class="card-value">{{ pageData?.summary?.days || 0 }} 天</span>
          </div>
          <div class="summary-card">
            <span class="card-label">页面类型</span>
            <span class="card-value">{{ pageData?.summary?.total_pages || 0 }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均停留</span>
            <span class="card-value">{{ getOverallAvgDuration() }} 秒</span>
          </div>
        </div>

        <!-- Duration Distribution -->
        <div class="chart-section">
          <h3 class="section-title">停留时长分布</h3>
          <div ref="durationDistChart" class="chart-container"></div>
        </div>

        <!-- Page Statistics Table -->
        <div class="table-section">
          <h3 class="section-title">各页面停留时间统计</h3>
          <el-table :data="pageData?.page_statistics || []" stripe style="width: 100%">
            <el-table-column prop="page" label="页面" width="120" />
            <el-table-column prop="total_visits" label="访问次数" sortable width="120">
              <template #default="{ row }">{{ formatNumber(row.total_visits) }}</template>
            </el-table-column>
            <el-table-column prop="avg_duration" label="平均停留(秒)" sortable width="130">
              <template #default="{ row }">{{ row.avg_duration.toFixed(1) }}</template>
            </el-table-column>
            <el-table-column prop="median_duration" label="中位数(秒)" width="120">
              <template #default="{ row }">{{ row.median_duration.toFixed(1) }}</template>
            </el-table-column>
            <el-table-column prop="min_duration" label="最短(秒)" width="100" />
            <el-table-column prop="max_duration" label="最长(秒)" width="100">
              <template #default="{ row }">{{ formatDuration(row.max_duration) }}</template>
            </el-table-column>
          </el-table>
        </div>

        <!-- Duration Trend -->
        <div class="chart-section">
          <h3 class="section-title">停留时长趋势</h3>
          <div ref="durationTrendChart" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  getClickStreamAnalytics,
  getActiveUsersAnalytics,
  getLoginFrequencyAnalytics,
  getPageDurationAnalytics
} from '../api/analytics'

// State
const currentTab = ref('clickstream')
const loading = ref(true)
const error = ref(null)
const dateRange = ref(null)

const clickstreamData = ref(null)
const activeData = ref(null)
const loginData = ref(null)
const pageData = ref(null)

// Chart refs
const funnelChart = ref(null)
const behaviorChart = ref(null)
const activeTrendChart = ref(null)
const loginFreqChart = ref(null)
const hourlyChart = ref(null)
const loginTrendChart = ref(null)
const durationDistChart = ref(null)
const durationTrendChart = ref(null)

// Chart instances
let funnelChartInstance = null
let behaviorChartInstance = null
let activeTrendChartInstance = null
let loginFreqChartInstance = null
let hourlyChartInstance = null
let loginTrendChartInstance = null
let durationDistChartInstance = null
let durationTrendChartInstance = null

// Tabs
const tabs = [
  { key: 'clickstream', label: '点击流分析', icon: '🔀' },
  { key: 'active', label: '活跃用户', icon: '👥' },
  { key: 'login', label: '登录频次', icon: '🔐' },
  { key: 'duration', label: '页面停留', icon: '⏱️' }
]

// Current tab data for export
const currentTabData = computed(() => {
  switch (currentTab.value) {
    case 'clickstream': return clickstreamData.value
    case 'active': return activeData.value
    case 'login': return loginData.value
    case 'duration': return pageData.value
    default: return null
  }
})

/**
 * Format number with commas
 */
function formatNumber(num) {
  if (num === null || num === undefined) return '-'
  return Number(num).toLocaleString('zh-CN')
}

/**
 * Format duration from seconds to readable format
 */
function formatDuration(seconds) {
  if (seconds < 60) return `${seconds}s`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`
}

/**
 * Get overall average duration
 */
function getOverallAvgDuration() {
  if (!pageData.value?.page_statistics?.length) return 0
  const stats = pageData.value.page_statistics
  let totalVisits = 0
  let totalDuration = 0
  stats.forEach(item => {
    totalVisits += item.total_visits
    totalDuration += item.avg_duration * item.total_visits
  })
  return totalVisits > 0 ? (totalDuration / totalVisits).toFixed(1) : 0
}

/**
 * Switch tab
 */
function switchTab(tab) {
  currentTab.value = tab
  if (!currentTabData.value) {
    fetchData()
  } else {
    nextTick(() => renderCurrentChart())
  }
}

/**
 * Handle date range change
 */
function handleDateChange() {
  fetchData()
}

/**
 * Render current chart
 */
function renderCurrentChart() {
  switch (currentTab.value) {
    case 'clickstream':
      renderFunnelChart()
      renderBehaviorChart()
      break
    case 'active':
      renderActiveTrendChart()
      break
    case 'login':
      renderLoginFreqChart()
      renderHourlyChart()
      renderLoginTrendChart()
      break
    case 'duration':
      renderDurationDistChart()
      renderDurationTrendChart()
      break
  }
}

/**
 * Fetch all data
 */
async function fetchData() {
  loading.value = true
  error.value = null

  try {
    // Calculate days from date range if set
    let days = 30
    if (dateRange.value && dateRange.value[0] && dateRange.value[1]) {
      const diffTime = Math.abs(dateRange.value[1] - dateRange.value[0])
      days = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    }

    const params = { days: Math.min(days, 90) }

    await Promise.all([
      fetchClickstreamData(params),
      fetchActiveData(params),
      fetchLoginData(params),
      fetchPageData(params)
    ])

    loading.value = false
    await nextTick()
    renderCurrentChart()
  } catch (err) {
    error.value = err.message || '数据加载失败，请稍后重试'
    loading.value = false
  }
}

/**
 * Fetch clickstream data
 */
async function fetchClickstreamData(params) {
  const response = await getClickStreamAnalytics(params)
  clickstreamData.value = response?.data || null
}

/**
 * Fetch active users data
 */
async function fetchActiveData(params) {
  const response = await getActiveUsersAnalytics(params)
  activeData.value = response?.data || null
}

/**
 * Fetch login frequency data
 */
async function fetchLoginData(params) {
  const response = await getLoginFrequencyAnalytics(params)
  loginData.value = response?.data || null
}

/**
 * Fetch page duration data
 */
async function fetchPageData(params) {
  const response = await getPageDurationAnalytics(params)
  pageData.value = response?.data || null
}

// ==================== Chart Rendering Functions ====================

/**
 * Render conversion funnel chart
 */
function renderFunnelChart() {
  if (!funnelChart.value || !clickstreamData.value?.conversion_funnel) return

  if (funnelChartInstance) {
    funnelChartInstance.dispose()
  }

  funnelChartInstance = echarts.init(funnelChart.value)
  const funnel = clickstreamData.value.conversion_funnel

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    series: [
      {
        type: 'funnel',
        left: '10%',
        top: 20,
        bottom: 20,
        width: '80%',
        min: 0,
        max: funnel.login_users,
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 2,
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}\n{c}人',
          fontSize: 14,
          fontWeight: 'bold'
        },
        labelLine: {
          length: 10,
          lineStyle: {
            width: 1,
            type: 'solid'
          }
        },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 2
        },
        data: [
          { value: funnel.login_users, name: '登录用户', itemStyle: { color: '#c2622e' } },
          { value: funnel.view_users, name: '浏览用户', itemStyle: { color: '#d4773a' } },
          { value: funnel.collect_users, name: '收藏用户', itemStyle: { color: '#e8a87c' } }
        ]
      }
    ]
  }

  funnelChartInstance.setOption(option)
}

/**
 * Render behavior distribution chart
 */
function renderBehaviorChart() {
  if (!behaviorChart.value || !clickstreamData.value?.behavior_distribution) return

  if (behaviorChartInstance) {
    behaviorChartInstance.dispose()
  }

  behaviorChartInstance = echarts.init(behaviorChart.value)
  const dist = clickstreamData.value.behavior_distribution

  const behaviorLabels = {
    'login': '登录',
    'search': '搜索',
    'view': '浏览',
    'collect': '收藏'
  }

  const data = Object.entries(dist)
    .filter(([key]) => !key.endsWith('_percentage'))
    .map(([key, value]) => ({
      name: behaviorLabels[key] || key,
      value: value
    }))
    .sort((a, b) => b.value - a.value)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
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
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: data
      }
    ]
  }

  behaviorChartInstance.setOption(option)
}

/**
 * Render active users trend chart
 */
function renderActiveTrendChart() {
  if (!activeTrendChart.value || !activeData.value?.trend?.length) return

  if (activeTrendChartInstance) {
    activeTrendChartInstance.dispose()
  }

  activeTrendChartInstance = echarts.init(activeTrendChart.value)
  const trend = activeData.value.trend

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['DAU', 'WAU', 'MAU'],
      bottom: 0
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
      boundaryGap: false,
      data: trend.map(item => item.date)
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } }
    },
    series: [
      {
        name: 'DAU',
        type: 'line',
        data: trend.map(item => item.dau),
        smooth: true,
        itemStyle: { color: '#c2622e' },
        lineStyle: { width: 2 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(194, 98, 46, 0.3)' },
              { offset: 1, color: 'rgba(194, 98, 46, 0.05)' }
            ]
          }
        }
      },
      {
        name: 'WAU',
        type: 'line',
        data: trend.map(item => item.wau),
        smooth: true,
        itemStyle: { color: '#d4773a' },
        lineStyle: { width: 2 }
      },
      {
        name: 'MAU',
        type: 'line',
        data: trend.map(item => item.mau),
        smooth: true,
        itemStyle: { color: '#a35220' },
        lineStyle: { width: 2 }
      }
    ]
  }

  activeTrendChartInstance.setOption(option)
}

/**
 * Render login frequency distribution chart
 */
function renderLoginFreqChart() {
  if (!loginFreqChart.value || !loginData.value?.login_frequency_distribution) return

  if (loginFreqChartInstance) {
    loginFreqChartInstance.dispose()
  }

  loginFreqChartInstance = echarts.init(loginFreqChart.value)
  const dist = loginData.value.login_frequency_distribution

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
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
      data: ['高频用户\n(≥20次)', '中频用户\n(5-19次)', '低频用户\n(1-4次)', '沉默用户\n(0次)'],
      axisLabel: { interval: 0, fontSize: 12 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } }
    },
    series: [
      {
        type: 'bar',
        data: [
          dist.high_frequency,
          dist.medium_frequency,
          dist.low_frequency,
          dist.silent
        ],
        itemStyle: {
          color: (params) => {
            const colors = ['#4caf50', '#ff9800', '#2196f3', '#9e9e9e']
            return colors[params.dataIndex] || '#c2622e'
          },
          borderRadius: [8, 8, 0, 0]
        },
        barWidth: '50%',
        label: {
          show: true,
          position: 'top',
          formatter: (params) => {
            const values = [dist.high_percentage, dist.medium_percentage, dist.low_percentage, dist.silent_percentage]
            return `${params.value}\n(${values[params.dataIndex].toFixed(1)}%)`
          }
        }
      }
    ]
  }

  loginFreqChartInstance.setOption(option)
}

/**
 * Render hourly distribution chart
 */
function renderHourlyChart() {
  if (!hourlyChart.value || !loginData.value?.hourly_distribution) return

  if (hourlyChartInstance) {
    hourlyChartInstance.dispose()
  }

  hourlyChartInstance = echarts.init(hourlyChart.value)
  const hourly = loginData.value.hourly_distribution.detail

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
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
      data: Object.keys(hourly),
      name: '小时',
      nameLocation: 'middle',
      nameGap: 25
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } }
    },
    series: [
      {
        type: 'bar',
        data: Object.values(hourly),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#c2622e' },
            { offset: 1, color: '#e8a87c' }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        barWidth: '60%'
      }
    ]
  }

  hourlyChartInstance.setOption(option)
}

/**
 * Render login trend chart
 */
function renderLoginTrendChart() {
  if (!loginTrendChart.value || !loginData.value?.daily_trend?.length) return

  if (loginTrendChartInstance) {
    loginTrendChartInstance.dispose()
  }

  loginTrendChartInstance = echarts.init(loginTrendChart.value)
  const trend = loginData.value.daily_trend

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['登录次数', '登录用户数'],
      bottom: 0
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
      data: trend.map(item => item.date)
    },
    yAxis: [
      {
        type: 'value',
        name: '次数',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } }
      },
      {
        type: 'value',
        name: '用户数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: '登录次数',
        type: 'bar',
        data: trend.map(item => item.login_count),
        itemStyle: {
          color: '#c2622e',
          borderRadius: [4, 4, 0, 0]
        }
      },
      {
        name: '登录用户数',
        type: 'line',
        yAxisIndex: 1,
        data: trend.map(item => item.login_users),
        smooth: true,
        itemStyle: { color: '#d4773a' },
        lineStyle: { width: 2 }
      }
    ]
  }

  loginTrendChartInstance.setOption(option)
}

/**
 * Render duration distribution chart
 */
function renderDurationDistChart() {
  if (!durationDistChart.value || !pageData.value?.duration_distribution) return

  if (durationDistChartInstance) {
    durationDistChartInstance.dispose()
  }

  durationDistChartInstance = echarts.init(durationDistChart.value)
  const dist = pageData.value.duration_distribution

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 0
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['50%', '45%'],
        roseType: 'radius',
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c}次'
        },
        data: [
          { value: dist.short, name: '短停留 (<30秒)', itemStyle: { color: '#ff7043' } },
          { value: dist.medium, name: '中停留 (30-120秒)', itemStyle: { color: '#ffa726' } },
          { value: dist.long, name: '长停留 (>120秒)', itemStyle: { color: '#66bb6a' } }
        ]
      }
    ]
  }

  durationDistChartInstance.setOption(option)
}

/**
 * Render duration trend chart
 */
function renderDurationTrendChart() {
  if (!durationTrendChart.value || !pageData.value?.trend?.length) return

  if (durationTrendChartInstance) {
    durationTrendChartInstance.dispose()
  }

  durationTrendChartInstance = echarts.init(durationTrendChart.value)
  const trend = pageData.value.trend

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['平均停留时长', '访问次数'],
      bottom: 0
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
      data: trend.map(item => item.date)
    },
    yAxis: [
      {
        type: 'value',
        name: '时长(秒)',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } }
      },
      {
        type: 'value',
        name: '访问次数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: '平均停留时长',
        type: 'bar',
        data: trend.map(item => item.avg_duration),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#c2622e' },
            { offset: 1, color: '#e8a87c' }
          ]),
          borderRadius: [4, 4, 0, 0]
        }
      },
      {
        name: '访问次数',
        type: 'line',
        yAxisIndex: 1,
        data: trend.map(item => item.visit_count),
        smooth: true,
        itemStyle: { color: '#4caf50' },
        lineStyle: { width: 2 }
      }
    ]
  }

  durationTrendChartInstance.setOption(option)
}

/**
 * Export data as JSON
 */
function exportData() {
  const data = currentTabData.value
  if (!data) return

  const tabNames = {
    clickstream: '点击流分析',
    active: '活跃用户',
    login: '登录频次',
    duration: '页面停留'
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `user-behavior-${currentTab.value}-${new Date().toISOString().slice(0, 10)}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)

  ElMessage.success(`${tabNames[currentTab.value]}数据已导出`)
}

/**
 * Handle window resize
 */
function handleResize() {
  funnelChartInstance?.resize()
  behaviorChartInstance?.resize()
  activeTrendChartInstance?.resize()
  loginFreqChartInstance?.resize()
  hourlyChartInstance?.resize()
  loginTrendChartInstance?.resize()
  durationDistChartInstance?.resize()
  durationTrendChartInstance?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  funnelChartInstance?.dispose()
  behaviorChartInstance?.dispose()
  activeTrendChartInstance?.dispose()
  loginFreqChartInstance?.dispose()
  hourlyChartInstance?.dispose()
  loginTrendChartInstance?.dispose()
  durationDistChartInstance?.dispose()
  durationTrendChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* Base Styles */
.user-behavior-analytics-page {
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
  gap: 1rem;
  align-items: center;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

.export-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.export-btn svg {
  width: 18px;
  height: 18px;
}

/* Tabs Container */
.tabs-container {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  max-width: 1600px;
  margin-left: auto;
  margin-right: auto;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.5rem;
  background: white;
  border: 2px solid #e5ddd3;
  border-radius: 14px;
  font-size: 0.95rem;
  font-weight: 500;
  color: #6b5c4d;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  border-color: #c2622e;
  color: #c2622e;
}

.tab-btn.active {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 4px 16px rgba(194, 98, 46, 0.3);
}

.tab-icon {
  font-size: 1.1rem;
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

/* Content Area */
.content-area {
  max-width: 1600px;
  margin: 0 auto;
}

/* Summary Cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-label {
  font-size: 0.85rem;
  color: #8b7355;
}

.card-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #c2622e;
}

.card-value.highlight {
  color: #4caf50;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #8b7355;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3d2914;
}

.stat-change {
  font-size: 0.9rem;
  font-weight: 500;
}

.stat-change.positive {
  color: #4caf50;
}

.stat-change.negative {
  color: #f44336;
}

.stat-label-small {
  font-size: 0.8rem;
  color: #b8a99a;
}

/* Chart Section */
.chart-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  margin-bottom: 2rem;
}

.chart-container {
  width: 100%;
  height: 350px;
}

.funnel-chart {
  height: 300px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 1.5rem 0;
}

/* Table Section */
.table-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  margin-bottom: 2rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .user-behavior-analytics-page {
    padding: 1rem;
  }

  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-container {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 250px;
  }

  .stats-row {
    grid-template-columns: 1fr;
  }
}
</style>
