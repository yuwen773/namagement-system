<template>
  <div class="dashboard-container">
    <!-- Top Metric Cards -->
    <div class="metrics-row">
      <div v-for="(metric, index) in metrics" :key="index" class="metric-card" :class="`metric-${index}`">
        <div class="metric-background">
          <div class="grid-pattern"></div>
          <div class="glow-effect" :style="{ background: metric.color }"></div>
        </div>
        <div class="metric-content">
          <div class="metric-icon" :style="{ color: metric.color, background: `${metric.color}15` }">
            <component :is="metric.icon" />
          </div>
          <div class="metric-info">
            <div class="metric-label">{{ metric.label }}</div>
            <div class="metric-value">
              <span class="value-animate" :data-value="metric.value">{{ metric.displayValue }}</span>
              <span class="metric-unit">{{ metric.unit }}</span>
            </div>
            <div class="metric-change" :class="metric.trend">
              <el-icon><icon-ep-caret-top v-if="metric.trend === 'up'" /><icon-ep-caret-bottom v-else /></el-icon>
              <span>{{ metric.change }}</span>
            </div>
          </div>
        </div>
        <div class="metric-pulse" v-if="metric.pulse" :style="{ borderColor: metric.color }"></div>
      </div>
    </div>

    <!-- Middle Charts Section -->
    <div class="charts-grid">
      <!-- Energy Trend Chart -->
      <div class="chart-card trend-chart">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-trend-charts /></span>
            能耗趋势
            <span class="time-tag">近7天</span>
          </h3>
          <div class="legend-tabs">
            <button
              v-for="type in energyTypes"
              :key="type.key"
              :class="['legend-tab', { active: activeTrendType === type.key }]"
              @click="activeTrendType = type.key"
            >
              <span class="legend-dot" :style="{ background: type.color }"></span>
              {{ type.label }}
            </button>
          </div>
        </div>
        <div class="chart-body">
          <div ref="trendChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- Energy Distribution Pie -->
      <div class="chart-card distribution-chart">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-pie-chart /></span>
            能耗分布
          </h3>
        </div>
        <div class="chart-body">
          <div ref="distributionChartRef" class="chart-container"></div>
          <div class="distribution-summary">
            <div v-for="(item, index) in distributionData" :key="index" class="summary-item">
              <span class="summary-dot" :style="{ background: item.color }"></span>
              <span class="summary-label">{{ item.name }}</span>
              <span class="summary-value">{{ item.percent }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Real-time Power Chart -->
      <div class="chart-card power-chart">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-data-analysis /></span>
            实时功率
            <span class="live-indicator">
              <span class="live-dot"></span>
              实时
            </span>
          </h3>
        </div>
        <div class="chart-body">
          <div ref="powerChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- 2D Map Heatmap -->
      <div class="chart-card map-chart">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-location /></span>
            校区能耗热力图
          </h3>
        </div>
        <div class="chart-body">
          <div ref="mapChartRef" class="chart-container"></div>
        </div>
      </div>
    </div>

    <!-- Bottom Tables Section -->
    <div class="tables-row">
      <!-- Recent Alarms -->
      <div class="table-card alarms-table">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-warning /></span>
            最新告警
            <span class="badge-count">{{ alarmCount }}</span>
          </h3>
          <el-button text type="primary" @click="$router.push('/admin/alarms')">
            查看全部 <el-icon><icon-ep-arrow-right /></el-icon>
          </el-button>
        </div>
        <div class="table-body">
          <div v-if="recentAlarms.length > 0" class="alarm-list">
            <div
              v-for="alarm in recentAlarms"
              :key="alarm.id"
              class="alarm-item"
              :class="`severity-${alarm.severity}`"
              @click="$router.push(`/admin/alarms`)"
            >
              <div class="alarm-icon" :class="`icon-${alarm.severity}`">
                <el-icon><icon-ep-warning /></el-icon>
              </div>
              <div class="alarm-content">
                <div class="alarm-title">{{ alarm.title }}</div>
                <div class="alarm-detail">{{ alarm.device }} · {{ alarm.time }}</div>
              </div>
              <div class="alarm-status" :class="alarm.status">{{ alarm.statusText }}</div>
            </div>
          </div>
          <el-empty v-else description="暂无告警" :image-size="100" />
        </div>
      </div>

      <!-- Device Status -->
      <div class="table-card devices-table">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-cpu /></span>
            设备状态概览
          </h3>
          <el-button text type="primary" @click="$router.push('/admin/devices')">
            设备管理 <el-icon><icon-ep-arrow-right /></el-icon>
          </el-button>
        </div>
        <div class="table-body">
          <div class="device-stats">
            <div v-for="(stat, index) in deviceStats" :key="index" class="stat-item">
              <div class="stat-bar">
                <div class="stat-fill" :style="{
                  width: stat.percent + '%',
                  background: stat.color
                }"></div>
              </div>
              <div class="stat-info">
                <span class="stat-label">{{ stat.label }}</span>
                <span class="stat-count" :style="{ color: stat.color }">{{ stat.count }}</span>
              </div>
            </div>
          </div>
          <div class="device-list">
            <div
              v-for="device in deviceList"
              :key="device.id"
              class="device-item"
              @click="$router.push(`/admin/devices`)"
            >
              <div class="device-status-dot" :class="device.status"></div>
              <div class="device-info">
                <div class="device-name">{{ device.name }}</div>
                <div class="device-location">{{ device.location }}</div>
              </div>
              <div class="device-value">{{ device.value }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getDashboardData, getTrendData, getDistributionData, getRealTimePowerData } from '@/api/analysis'
import { getBuildingHeatmap } from '@/api/building'
import { getAlarms } from '@/api/alarm'
import { getDevices } from '@/api/device'

// Chart refs using shallowRef to avoid deep reactivity
const trendChartRef = ref(null)
const distributionChartRef = ref(null)
const powerChartRef = ref(null)
const mapChartRef = ref(null)

// Chart instances
const trendChart = shallowRef(null)
const distributionChart = shallowRef(null)
const powerChart = shallowRef(null)
const mapChart = shallowRef(null)

// Auto refresh timer
let refreshTimer = null

// Energy types for filtering
const energyTypes = [
  { key: 'all', label: '全部', color: '#f97316' },
  { key: 'ELECTRICITY', label: '电', color: '#eab308' },
  { key: 'WATER', label: '水', color: '#3b82f6' },
  { key: 'GAS', label: '气', color: '#ef4444' },
]

const activeTrendType = ref('all')

// Metrics data (placeholder, will be replaced by API data)
const metrics = ref([
  {
    label: '总能耗',
    value: 0,
    unit: 'kWh',
    change: '--',
    trend: 'up',
    color: '#f97316',
    icon: 'icon-ep-lightning',
    pulse: true,
    displayValue: '--',
  },
  {
    label: '平均功率',
    value: 0,
    unit: 'kW',
    change: '--',
    trend: 'up',
    color: '#eab308',
    icon: 'icon-ep-odometer',
    pulse: true,
    displayValue: '--',
  },
  {
    label: '数据覆盖率',
    value: 0,
    unit: '%',
    change: '--',
    trend: 'up',
    color: '#22c55e',
    icon: 'icon-ep-circle-check',
    pulse: false,
    displayValue: '--',
  },
  {
    label: '今日告警',
    value: 0,
    unit: '条',
    change: '--',
    trend: 'down',
    color: '#ef4444',
    icon: 'icon-ep-warning',
    pulse: true,
    displayValue: '--',
  },
])

// Distribution data (empty, will be filled by API data)
const distributionData = ref([])

// Alarms data
const recentAlarms = ref([])
const alarmCount = computed(() => recentAlarms.value.length)

// Device data (empty, will be filled by API data)
const deviceStats = ref([])

const deviceList = ref([])

// ECharts theme colors
const chartColors = {
  primary: '#f97316',
  secondary: '#eab308',
  water: '#3b82f6',
  gas: '#ef4444',
  green: '#22c55e',
  text: '#64748b',
  grid: '#e2e8f0',
}

function initChartWhenReady(containerRef, chartInstanceRef, applyOption, retryCount = 0) {
  const container = containerRef.value
  if (!container) return

  if (container.clientWidth === 0 || container.clientHeight === 0) {
    if (retryCount < 10) {
      setTimeout(() => initChartWhenReady(containerRef, chartInstanceRef, applyOption, retryCount + 1), 16)
    } else {
      console.warn('Chart container still has no size after retries')
    }
    return
  }

  if (chartInstanceRef.value) {
    chartInstanceRef.value.dispose()
  }

  chartInstanceRef.value = echarts.init(container)
  applyOption(chartInstanceRef.value)
}

// Initialize trend chart (empty, will be filled by API data)
function initTrendChart() {
  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: {
        type: 'line',
        lineStyle: { color: '#f97316', type: 'dashed' },
      },
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 12 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 12 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        name: '电',
        type: 'line',
        smooth: true,
        data: [],
        lineStyle: { width: 3, color: chartColors.secondary },
        itemStyle: { color: chartColors.secondary, borderWidth: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(234, 179, 8, 0.3)' },
            { offset: 1, color: 'rgba(234, 179, 8, 0)' },
          ]),
        },
      },
      {
        name: '水',
        type: 'line',
        smooth: true,
        data: [],
        lineStyle: { width: 3, color: chartColors.water },
        itemStyle: { color: chartColors.water, borderWidth: 2 },
      },
    ],
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text },
    },
  }

  initChartWhenReady(trendChartRef, trendChart, (chart) => chart.setOption(option))
}

// Initialize distribution chart (empty, will be filled by API data)
function initDistributionChart() {
  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      formatter: (params) => `${params.name}: ${formatNumber(params.value)} (${params.percent}%)`,
    },
    series: [
      {
        type: 'pie',
        radius: ['45%', '70%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: { show: false },
        emphasis: {
          label: { show: true, fontSize: 16, fontWeight: 'bold', color: '#1f2937' },
        },
        labelLine: { show: false },
        data: [],
      },
    ],
  }

  initChartWhenReady(distributionChartRef, distributionChart, (chart) => chart.setOption(option))
}

// Initialize power chart (empty, will be filled by API data)
function initPowerChart() {
  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const item = params[0]
        return `${item.axisValue}<br/>功率: ${item.value} kW`
      },
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 10 },
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 12, formatter: '{value} kW' },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        type: 'bar',
        data: [],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#f97316' },
            { offset: 1, color: '#ea580c' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        emphasis: {
          itemStyle: { color: '#fbbf24' },
        },
      },
    ],
  }

  initChartWhenReady(powerChartRef, powerChart, (chart) => chart.setOption(option))
}

// Initialize 2D map chart
function initMapChart(retryCount = 0) {
  const option = {
    grid: { top: 10, bottom: 10, left: 10, right: 10 },
    xAxis: { show: false, min: -1, max: 8 },
    yAxis: { show: false, min: -1, max: 8 },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const data = params.data || {}
        const indexValue = data.heat_index || 0
        const latestPower = data.latest_power == null ? '-' : `${data.latest_power} kW`
        return `${data.name || ''}<br/>热力指数: ${indexValue}<br/>最新功率: ${latestPower}`
      },
    },
    series: [
      {
        type: 'scatter',
        symbolSize: 18,
        data: [],
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(249, 115, 22, 0.5)',
          shadowOffsetY: 0,
        },
        label: {
          show: true,
          position: 'bottom',
          color: '#1f2937',
          fontSize: 10,
          formatter: '{b}',
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(249, 115, 22, 0.8)',
          },
          scale: 1.2,
        },
      },
    ],
  }

  initChartWhenReady(mapChartRef, mapChart, (chart) => {
    chart.setOption(option)

    // Add click handler
    chart.on('click', (params) => {
      if (params.data && params.data.name) {
        ElMessage.info(`已选中: ${params.data.name}`)
      }
    })
  }, retryCount)
}

// Load dashboard data from API
async function loadDashboardData() {
  const summaryTask = (async () => {
    try {
      const response = await getDashboardData()
      if (response.code === 0 && response.data) {
        const summary = response.data.summary || {}
        const alarmStats = response.data.alarm_statistics || {}

        // 总能耗 - use total_energy
        if (summary.total_energy !== undefined) {
          metrics.value[0].value = summary.total_energy
          metrics.value[0].displayValue = formatNumber(summary.total_energy)
        }

        // 平均功率 - use average_power
        if (summary.average_power !== undefined) {
          metrics.value[1].value = summary.average_power
          metrics.value[1].displayValue = formatNumber(summary.average_power)
        }

        // 数据覆盖率 - use data_coverage_rate
        if (summary.data_coverage_rate !== undefined) {
          metrics.value[2].value = summary.data_coverage_rate
          metrics.value[2].displayValue = String(summary.data_coverage_rate)
        }

        // 今日告警 - use alarm_statistics.today
        if (alarmStats.today !== undefined) {
          metrics.value[3].value = alarmStats.today
          metrics.value[3].displayValue = String(alarmStats.today)
        }
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    }
  })()

  // Start chart requests immediately, avoid waiting for summary API first.
  await Promise.all([
    summaryTask,
    loadTrendData(),
    loadDistributionData(),
    loadRealTimePowerData(),
    loadBuildingHeatmapData(),
  ])
}

// Load trend data from API
async function loadTrendData() {
  try {
    const response = await getTrendData({ period: 'day' })
    if (response.code === 0 && response.data && trendChart.value) {
      const labels = response.data.labels || ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      const electricityData = response.data.electricity || [3200, 3800, 3500, 4200, 3900, 3100, 2800]
      const waterData = response.data.water || [2100, 2400, 2200, 2800, 2600, 2000, 1800]

      trendChart.value.setOption({
        xAxis: { data: labels },
        series: [
          { data: electricityData },
          { data: waterData },
        ],
      })
    }
  } catch (error) {
    console.error('Failed to load trend data:', error)
  }
}

// Load distribution data from API
async function loadDistributionData() {
  try {
    const response = await getDistributionData({ type: 'energy_type' })
    if (response.code === 0 && response.data) {
      const data = Array.isArray(response.data) ? response.data : (response.data.items || [])
      if (data.length > 0) {
        const totalValue = data.reduce((sum, item) => sum + Number(item.value || 0), 0)
        distributionData.value = data.map((item, index) => ({
          name: item.label || item.name || ['电', '水', '气'][index] || `能源${index + 1}`,
          value: Number(item.value || 0),
          percent: item.percent !== undefined
            ? (Number(item.percent) <= 1 ? Number(item.percent) * 100 : Number(item.percent))
            : (totalValue > 0 ? (Number(item.value || 0) / totalValue) * 100 : 0),
          color: item.color || ['#eab308', '#3b82f6', '#ef4444'][index] || '#f97316',
        }))

        distributionData.value.forEach((item) => {
          item.percent = Number(item.percent.toFixed(2))
        })

        // Update distribution chart
        if (distributionChart.value) {
          distributionChart.value.setOption({
            series: [{
              data: distributionData.value.map(d => ({
                value: d.value,
                name: d.name,
                itemStyle: { color: d.color },
              })),
            }],
          })
        }
      }
    }
  } catch (error) {
    console.error('Failed to load distribution data:', error)
  }
}

function formatClockLabel(timestamp) {
  const dt = new Date(timestamp)
  if (Number.isNaN(dt.getTime())) return ''
  return `${String(dt.getHours()).padStart(2, '0')}:${String(dt.getMinutes()).padStart(2, '0')}`
}

function resolveHeatColor(level) {
  if (level === 'high') return '#ef4444'
  if (level === 'normal') return '#f97316'
  if (level === 'low') return '#22c55e'
  return '#94a3b8'
}

// Load real-time power data from API
async function loadRealTimePowerData() {
  try {
    const response = await getRealTimePowerData({ hours: 24, interval_minutes: 15 })
    if (response.code === 0 && response.data && powerChart.value) {
      const series = response.data.series || []
      const xData = series.map(item => formatClockLabel(item.timestamp))
      const yData = series.map(item => Number(item.total_power || 0))
      const maxPower = yData.length > 0 ? Math.max(...yData) : 0

      powerChart.value.setOption({
        xAxis: { data: xData },
        yAxis: { max: Math.max(100, Math.ceil(maxPower * 1.15)) },
        series: [{ data: yData }],
      })
    }
  } catch (error) {
    console.error('Failed to load real-time power data:', error)
  }
}

// Load building heatmap data from API
async function loadBuildingHeatmapData() {
  try {
    const response = await getBuildingHeatmap({ days: 7 })
    if (response.code === 0 && response.data && mapChart.value) {
      const buildings = response.data.buildings || []
      const scatterData = buildings.map(item => ({
        name: item.name,
        value: [item.position?.x ?? 0, item.position?.y ?? 0, item.heat_index ?? 0],
        heat_index: Number(item.heat_index || 0),
        latest_power: item.latest_power,
        itemStyle: { color: resolveHeatColor(item.heat_level) },
      }))

      mapChart.value.setOption({
        series: [
          {
            symbolSize: (data) => Math.max(14, Number(data[2] || 0) * 0.45),
            data: scatterData,
          },
        ],
      })
    }
  } catch (error) {
    console.error('Failed to load building heatmap data:', error)
  }
}

// Format number helper
function formatNumber(num) {
  if (typeof num !== 'number') return String(num)
  return num.toLocaleString('en-US')
}

// Load alarms data
async function loadAlarmsData() {
  try {
    const response = await getAlarms({ status: 'PENDING', limit: 5 })
    if (response.code === 0 && response.data) {
      recentAlarms.value = response.data.map(alarm => ({
        id: alarm.id,
        title: alarm.alarm_type === 'THRESHOLD' ? '超限告警' : '突变告警',
        device: alarm.device_name || `设备${alarm.device}`,
        time: formatTime(alarm.alarm_time),
        severity: alarm.alarm_value > 100 ? 'high' : 'medium',
        status: alarm.status.toLowerCase(),
        statusText: alarm.status === 'PENDING' ? '待处理' : alarm.status === 'PROCESSED' ? '已处理' : '已忽略',
      }))
    }
  } catch (error) {
    console.error('Failed to load alarms:', error)
    // Use mock data for development
    recentAlarms.value = [
      { id: 1, title: '用电量超限', device: '教学楼A-301', time: '5分钟前', severity: 'high', status: 'pending', statusText: '待处理' },
      { id: 2, title: '数据突变', device: '实验楼-201', time: '15分钟前', severity: 'medium', status: 'pending', statusText: '待处理' },
      { id: 3, title: '设备离线', device: '宿舍楼1-102', time: '1小时前', severity: 'high', status: 'processed', statusText: '已处理' },
    ]
  }
}

// Load device status
async function loadDeviceStatus() {
  // Get all devices to calculate stats
  let allDevices = []
  try {
    // Get total count for stats
    const countResponse = await getDevices({ page: 1, page_size: 100 })
    if (countResponse.code === 0 && countResponse.data) {
      allDevices = countResponse.data

      // Calculate stats from device list
      const online = allDevices.filter(d => d.status === 'ONLINE').length
      const offline = allDevices.filter(d => d.status === 'OFFLINE').length
      const fault = allDevices.filter(d => d.status === 'FAULT').length
      const total = allDevices.length

      deviceStats.value = [
        {
          label: '在线',
          count: online,
          percent: total > 0 ? Math.round(online / total * 100) : 0,
          color: '#22c55e',
        },
        {
          label: '离线',
          count: offline,
          percent: total > 0 ? Math.round(offline / total * 100) : 0,
          color: '#94a3b8',
        },
        {
          label: '故障',
          count: fault,
          percent: total > 0 ? Math.round(fault / total * 100) : 0,
          color: '#ef4444',
        },
      ]
    }
  } catch (error) {
    console.error('Failed to load device status:', error)
  }

  // Load device list for preview (use already fetched data or fetch again)
  try {
    let devicesToShow = allDevices.length > 0 ? allDevices.slice(0, 5) : []
    if (devicesToShow.length === 0) {
      const response = await getDevices({ limit: 5 })
      if (response.code === 0 && response.data) {
        devicesToShow = response.data
      }
    }

    deviceList.value = devicesToShow.map(device => ({
      id: device.id,
      name: device.name,
      location: device.room_name
        ? `${device.building_name || ''} ${device.floor_name || ''} ${device.room_name}`
        : (device.building_name || '未绑定'),
      value: device.status === 'ONLINE' ? '正常' : device.status === 'OFFLINE' ? '离线' : '故障',
      status: device.status?.toLowerCase() || 'offline',
    }))
  } catch (error) {
    console.error('Failed to load devices:', error)
    // Use mock data only when API fails
    deviceList.value = [
      { id: 1, name: '电表-001', location: '教学楼A-301', value: '正常', status: 'online' },
      { id: 2, name: '水表-003', location: '实验楼-201', value: '正常', status: 'online' },
      { id: 3, name: '气表-002', location: '食堂-101', value: '正常', status: 'online' },
      { id: 4, name: '电表-015', location: '宿舍1-102', value: '离线', status: 'offline' },
      { id: 5, name: '电表-018', location: '行政楼-301', value: '正常', status: 'online' },
    ]
  }
}

// Format time helper
function formatTime(timeStr) {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)

  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  return `${Math.floor(diff / 1440)}天前`
}

// Handle window resize
function handleResize() {
  trendChart.value?.resize()
  distributionChart.value?.resize()
  powerChart.value?.resize()
  mapChart.value?.resize()
}

// Setup auto refresh
function setupAutoRefresh() {
  refreshTimer = setInterval(async () => {
    await loadDashboardData()
    await loadAlarmsData()
    await loadDeviceStatus()
  }, 30000) // 30 seconds
}

// Lifecycle
onMounted(async () => {
  await nextTick()

  // Initialize charts
  initTrendChart()
  initDistributionChart()
  initPowerChart()
  initMapChart()

  // Load initial data in parallel
  await Promise.all([
    loadDashboardData(),
    loadAlarmsData(),
    loadDeviceStatus(),
  ])

  // Setup auto refresh
  setupAutoRefresh()

  // Handle resize
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // Clear timer
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }

  // Dispose charts
  trendChart.value?.dispose()
  distributionChart.value?.dispose()
  powerChart.value?.dispose()
  mapChart.value?.dispose()

  // Remove event listener
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   METRIC CARDS
   ======================================== */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.metric-card {
  position: relative;
  height: 120px;
  background: linear-gradient(135deg, #fff 0%, #f8fafc 100%);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e5e7eb;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(249, 115, 22, 0.15);
  border-color: #f97316;
}

.metric-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
}

.glow-effect {
  position: absolute;
  top: -50%;
  right: -30%;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.4;
}

.metric-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 16px;
  height: 100%;
  padding: 20px;
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 14px;
  font-size: 24px;
}

.metric-info {
  flex: 1;
  min-width: 0;
}

.metric-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.metric-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 4px;
}

.value-animate {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 24px;
  font-weight: 700;
  font-feature-settings: 'tnum';
  color: #1f2937;
}

.metric-unit {
  font-size: 13px;
  color: #94a3b8;
}

.metric-change {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.metric-change.up {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.metric-change.down {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

.metric-pulse {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse-ring 2s ease-out infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

/* ========================================
   CHARTS GRID
   ======================================== */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 320px 280px;
  gap: 16px;
}

.chart-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.trend-chart {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}

.distribution-chart {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
}

.power-chart {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}

.map-chart {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.title-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 18px;
}

.time-tag {
  font-size: 11px;
  padding: 2px 8px;
  background: #fef3c7;
  color: #f97316;
  border-radius: 10px;
  font-weight: 500;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 3px 8px;
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border-radius: 10px;
  font-weight: 500;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.badge-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #ef4444;
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  border-radius: 10px;
}

.legend-tabs {
  display: flex;
  gap: 4px;
}

.legend-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.legend-tab:hover {
  background: #f8fafc;
  color: #1f2937;
}

.legend-tab.active {
  background: #fef3c7;
  color: #f97316;
  font-weight: 500;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.chart-body {
  flex: 1;
  position: relative;
  padding: 12px;
}

.chart-container {
  width: 100%;
  height: 100%;
}

/* Distribution summary */
.distribution-summary {
  position: absolute;
  bottom: 12px;
  right: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  border: 1px solid #f1f5f9;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.summary-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.summary-label {
  color: #64748b;
}

.summary-value {
  margin-left: auto;
  font-weight: 600;
  color: #1f2937;
}

/* ========================================
   TABLES ROW
   ======================================== */
.tables-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.table-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.table-body {
  flex: 1;
  padding: 16px;
  min-height: 200px;
}

/* Alarm List */
.alarm-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alarm-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.alarm-item:hover {
  background: #fff;
  border-color: #f97316;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

.alarm-item.severity-high {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, #f8fafc 100%);
  border-left: 3px solid #ef4444;
}

.alarm-item.severity-medium {
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.05) 0%, #f8fafc 100%);
  border-left: 3px solid #eab308;
}

.alarm-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
}

.alarm-icon.icon-high {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.alarm-icon.icon-medium {
  background: rgba(234, 179, 8, 0.15);
  color: #eab308;
}

.alarm-content {
  flex: 1;
  min-width: 0;
}

.alarm-title {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 2px;
}

.alarm-detail {
  font-size: 12px;
  color: #64748b;
}

.alarm-status {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 10px;
  font-weight: 500;
  white-space: nowrap;
}

.alarm-status.pending {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.alarm-status.processed {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.alarm-status.ignored {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
}

/* Device Stats */
.device-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-bar {
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
}

.stat-count {
  font-size: 14px;
  font-weight: 600;
}

.device-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.device-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.device-item:hover {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.device-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.device-status-dot.online {
  background: #22c55e;
  box-shadow: 0 0 6px rgba(34, 197, 94, 0.5);
}

.device-status-dot.offline {
  background: #94a3b8;
}

.device-status-dot.fault {
  background: #ef4444;
}

.device-info {
  flex: 1;
  min-width: 0;
}

.device-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.device-location {
  font-size: 11px;
  color: #64748b;
}

.device-value {
  font-size: 13px;
  font-weight: 600;
  font-family: 'Orbitron', sans-serif;
  color: #64748b;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .metrics-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }

  .trend-chart,
  .distribution-chart,
  .power-chart,
  .map-chart {
    grid-column: 1 / -1;
    grid-row: auto;
  }
}

@media (max-width: 768px) {
  .metrics-row {
    grid-template-columns: 1fr;
  }

  .tables-row {
    grid-template-columns: 1fr;
  }

  .metric-card {
    height: 100px;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-button--text.is-text) {
  color: #f97316;
}

:deep(.el-button--text.is-text:hover) {
  color: #ea580c;
  background: rgba(249, 115, 22, 0.1);
}
</style>
