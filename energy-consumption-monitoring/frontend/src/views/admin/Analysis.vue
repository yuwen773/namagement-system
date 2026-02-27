<template>
  <div class="analysis-container">
    <!-- Top Filter Section -->
    <!-- <div class="filter-bar">
      <div class="filter-group">
        <div class="filter-item">
          <label class="filter-label">时间范围</label>
          <div class="time-range-selector">
            <button
              v-for="range in timeRanges"
              :key="range.value"
              :class="['range-btn', { active: filters.timeRange === range.value }]"
              @click="handleTimeRangeChange(range.value)"
            >
              {{ range.label }}
            </button>
          </div>
        </div>

        <div class="filter-item">
          <label class="filter-label">日期选择</label>
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="small"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateChange"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">建筑位置</label>
          <el-cascader
            v-model="filters.building"
            :options="buildingOptions"
            :props="cascaderProps"
            placeholder="选择建筑"
            size="small"
            clearable
            collapse-tags
            @change="handleFilterChange"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">能源类型</label>
          <el-select
            v-model="filters.energyType"
            placeholder="选择能源"
            size="small"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="type in energyTypes"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            >
              <span class="option-dot" :style="{ background: type.color }"></span>
              {{ type.label }}
            </el-option>
          </el-select>
        </div>
      </div>

      <div class="filter-actions">
        <el-button size="small" @click="resetFilters">
          <el-icon><icon-ep-refresh-left /></el-icon>
          重置
        </el-button>
        <el-button type="primary" size="small" @click="applyFilters">
          <el-icon><icon-ep-search /></el-icon>
          查询
        </el-button>
        <el-dropdown trigger="click" @command="handleExport">
          <el-button type="warning" size="small">
            <el-icon><icon-ep-download /></el-icon>
            导出
            <el-icon><icon-ep-arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="excel">
                <el-icon><icon-ep-document /></el-icon>
                导出 Excel
              </el-dropdown-item>
              <el-dropdown-item command="pdf">
                <el-icon><icon-ep-files /></el-icon>
                导出 PDF
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div> -->

    <!-- Charts Grid -->
    <div class="charts-section">
      <!-- Trend Chart -->
      <div class="chart-row full-width">
        <div class="chart-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-trend-charts /></span>
              能耗趋势分析
            </h3>
            <div class="chart-actions">
              <el-button-group size="small">
                <el-button
                  v-for="period in periods"
                  :key="period.value"
                  :class="['period-btn', { active: activePeriod === period.value }]"
                  @click="handlePeriodChange(period.value)"
                >
                  {{ period.label }}
                </el-button>
              </el-button-group>
            </div>
          </div>
          <div class="card-body">
            <div ref="trendChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- Second Row: Comparison and Ranking -->
      <div class="chart-row">
        <!-- Comparison Chart -->
        <div class="chart-card half-width">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-data-analysis /></span>
              同比环比分析
            </h3>
          </div>
          <div class="card-body">
            <div ref="comparisonChartRef" class="chart-container"></div>
          </div>
        </div>

        <!-- Ranking Chart -->
        <div class="chart-card half-width">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-histogram /></span>
              能耗排名
              <el-select v-model="rankingType" size="small" style="width: 100px;" @change="updateRankingChart">
                <el-option label="建筑" value="building"></el-option>
                <el-option label="部门" value="department"></el-option>
                <el-option label="房间" value="room"></el-option>
              </el-select>
            </h3>
          </div>
          <div class="card-body">
            <div ref="rankingChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- Third Row: Distribution and Forecast -->
      <div class="chart-row">
        <!-- Distribution Chart -->
        <div class="chart-card half-width">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-pie-chart /></span>
              能耗分布
            </h3>
          </div>
          <div class="card-body">
            <div ref="distributionChartRef" class="chart-container"></div>
          </div>
        </div>

        <!-- Forecast Chart -->
        <div class="chart-card half-width">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-magic-stick /></span>
              趋势预测
              <el-select v-model="forecastDays" size="small" style="width: 100px;" @change="updateForecastChart">
                <el-option label="7天" :value="7"></el-option>
                <el-option label="30天" :value="30"></el-option>
              </el-select>
            </h3>
          </div>
          <div class="card-body">
            <div ref="forecastChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Table Section -->
    <div class="table-section">
      <div class="table-card">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-document /></span>
            数据明细
          </h3>
          <div class="table-actions">
            <el-input
              v-model="tableSearch"
              placeholder="搜索..."
              prefix-icon="Search"
              size="small"
              style="width: 200px;"
              clearable
            />
          </div>
        </div>
        <div class="card-body">
          <el-table
            :data="tableData"
            stripe
            border
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#64748b' }"
          >
            <el-table-column prop="date" label="日期" min-width="160" />
            <el-table-column prop="building" label="建筑" min-width="120" />
            <el-table-column prop="energyType" label="能源类型" min-width="100">
              <template #default="{ row }">
                <span class="type-badge" :style="{ background: `${getEnergyColor(row.energyType)}15`, color: getEnergyColor(row.energyType) }">
                  {{ row.energyType }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="consumption" label="能耗量" min-width="120">
              <template #default="{ row }">
                <span class="value-text">{{ row.consumption }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="cost" label="费用 (元)" min-width="120" />
            <el-table-column prop="comparison" label="同比变化" min-width="100">
              <template #default="{ row }">
                <span :class="['change-text', row.comparison >= 0 ? 'up' : 'down']">
                  <el-icon><icon-ep-caret-top v-if="row.comparison >= 0" /><icon-ep-caret-bottom v-else /></el-icon>
                  {{ Math.abs(row.comparison) }}%
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="100">
              <template #default="{ row }">
                <span :class="['status-badge', `status-${row.status}`]">
                  {{ row.statusText }}
                </span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewDetail(row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Pagination -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="pagination.page"
              v-model:page-size="pagination.size"
              :page-sizes="[10, 20, 50, 100]"
              :total="pagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  getTrendData,
  getDistributionData,
  getRankingData,
  getComparisonData,
  getForecastData
} from '@/api/analysis'
import { getBuildings } from '@/api/building'
import { getEnergyTypes } from '@/api/device'
import { exportEnergyData, getEnergyDataDetails } from '@/api/energy'

// Chart refs
const trendChartRef = ref(null)
const comparisonChartRef = ref(null)
const rankingChartRef = ref(null)
const distributionChartRef = ref(null)
const forecastChartRef = ref(null)

// Chart instances
const trendChart = shallowRef(null)
const comparisonChart = shallowRef(null)
const rankingChart = shallowRef(null)
const distributionChart = shallowRef(null)
const forecastChart = shallowRef(null)

// Filters
const filters = ref({
  timeRange: 'week',
  dateRange: [],
  building: [],
  energyType: '',
})

// Time range options
const timeRanges = [
  { label: '今日', value: 'today' },
  { label: '近7天', value: 'week' },
  { label: '近30天', value: 'month' },
  { label: '本年', value: 'year' },
]

// Period options
const periods = [
  { label: '日', value: 'day' },
  { label: '月', value: 'month' },
  { label: '年', value: 'year' },
]

const activePeriod = ref('day')

// Ranking type
const rankingType = ref('building')

// Forecast days
const forecastDays = ref(7)

// Energy types
const energyTypes = ref([
  { label: '电', value: 'ELECTRICITY', color: '#eab308' },
  { label: '水', value: 'WATER', color: '#3b82f6' },
  { label: '气', value: 'GAS', color: '#ef4444' },
])

// Building options for cascader
const buildingOptions = ref([])

const cascaderProps = {
  multiple: false,
  checkStrictly: true,
  emitPath: false,
  value: 'id',
  label: 'name',
  children: 'children',
}

// Table data
const tableData = ref([])
const tableSearch = ref('')
const pagination = ref({
  page: 1,
  size: 10,
  total: 0,
})

// Computed filtered table data
const filteredTableData = computed(() => {
  if (!tableSearch.value) return tableData.value

  const search = tableSearch.value.toLowerCase()
  return tableData.value.filter(item =>
    item.date?.includes(search) ||
    item.building?.toLowerCase().includes(search) ||
    item.energyType?.toLowerCase().includes(search)
  )
})

const paginatedTableData = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.size
  const end = start + pagination.value.size
  return filteredTableData.value.slice(start, end)
})

// ECharts colors
const chartColors = {
  primary: '#f97316',
  secondary: '#eab308',
  water: '#3b82f6',
  gas: '#ef4444',
  green: '#22c55e',
  text: '#64748b',
  grid: '#e5e7eb',
}

// Initialize trend chart
function initTrendChart() {
  if (!trendChartRef.value) return

  trendChart.value = echarts.init(trendChartRef.value)

  // Load trend data from API
  loadTrendData()
}

// Initialize comparison chart
function initComparisonChart() {
  if (!comparisonChartRef.value) return

  comparisonChart.value = echarts.init(comparisonChartRef.value)

  // Load comparison data from API
  loadComparisonData()
}

// Load comparison data from API
async function loadComparisonData() {
  try {
    // Backend expects period (day/month/year) and optional anchor_date
    const response = await getComparisonData({ period: activePeriod.value })
    if (response.code === 0 && response.data) {
      updateComparisonChartWithData(response.data)
    }
  } catch (error) {
    console.error('Failed to load comparison data:', error)
    updateComparisonChartEmpty()
  }
}

// Update comparison chart with API data
function updateComparisonChartWithData(data) {
  if (!comparisonChart.value || !data) return

  // Backend returns { current_total, chain_total, yoy_total, chain_change_rate, yoy_change_rate }
  const currentTotal = data.current_total || 0
  const chainTotal = data.chain_total || 0
  const yoyTotal = data.yoy_total || 0
  const chainRate = data.chain_change_rate || 0
  const yoyRate = data.yoy_change_rate || 0

  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const item = params[0]
        const value = item.value
        let changeInfo = ''
        if (item.name === '本期') {
          changeInfo = `\n环比: ${chainRate >= 0 ? '+' : ''}${chainRate.toFixed(1)}%\n同比: ${yoyRate >= 0 ? '+' : ''}${yoyRate.toFixed(1)}%`
        }
        return `${item.name}<br/>能耗: ${value} kWh${changeInfo}`
      },
    },
    title: {
      text: `能耗对比`,
      left: 'center',
      top: '2%',
      textStyle: {
        fontSize: 12,
        color: chartColors.text,
      },
    },
    xAxis: {
      type: 'category',
      data: ['本期', '上期', '同期'],
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 12 },
    },
    yAxis: {
      type: 'value',
      name: 'kWh',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        type: 'bar',
        data: [
          {
            value: currentTotal,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#f97316' },
                { offset: 1, color: '#fbbf24' },
              ]),
              borderRadius: [4, 4, 0, 0],
            },
          },
          {
            value: chainTotal,
            itemStyle: {
              color: '#94a3b8',
              borderRadius: [4, 4, 0, 0],
            },
          },
          {
            value: yoyTotal,
            itemStyle: {
              color: '#64748b',
              borderRadius: [4, 4, 0, 0],
            },
          },
        ],
        label: {
          show: true,
          position: 'top',
          color: '#1f2937',
          fontSize: 11,
          formatter: '{c} kWh',
        },
      },
    ],
  }

  comparisonChart.value.setOption(option, true)
}

// Show empty state for comparison chart
function updateComparisonChartEmpty() {
  if (!comparisonChart.value) return
  comparisonChart.value.setOption({
    title: {
      text: '暂无数据',
      left: 'center',
      top: 'center',
      textStyle: { color: '#94a3b8', fontSize: 14 },
    },
    xAxis: { data: [] },
    yAxis: { data: [] },
    series: [],
  })
}

// Initialize ranking chart
function initRankingChart() {
  if (!rankingChartRef.value) return

  rankingChart.value = echarts.init(rankingChartRef.value)

  // Load ranking data from API
  loadRankingData()
}

// Load ranking data from API
async function loadRankingData() {
  try {
    const response = await getRankingData({ type: rankingType.value, limit: 10 })
    if (response.code === 0 && response.data) {
      updateRankingChartWithData(response.data)
    }
  } catch (error) {
    console.error('Failed to load ranking data:', error)
    updateRankingChartEmpty()
  }
}

// Update ranking chart with API data
function updateRankingChartWithData(data) {
  if (!rankingChart.value || !data) return

  const chartData = Array.isArray(data) ? data : (data.items || [])
  // Sort by value descending
  const sortedData = [...chartData].sort((a, b) => (b.value || b.total_value || 0) - (a.value || a.total_value || 0))

  const option = {
    grid: {
      left: '3%',
      right: '12%',
      bottom: '3%',
      top: '3%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const item = params[0]
        return `${item.name}<br/>能耗: ${item.value} kWh`
      },
    },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    yAxis: {
      type: 'category',
      data: sortedData.map((d, i) => d.name || d.target_name || `排名${i + 1}`),
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
    },
    series: [
      {
        type: 'bar',
        data: sortedData.map(d => d.value || d.total_value || 0),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#f97316' },
            { offset: 1, color: '#fbbf24' },
          ]),
          borderRadius: [0, 4, 4, 0],
        },
        label: {
          show: true,
          position: 'right',
          color: '#1f2937',
          fontSize: 11,
          formatter: '{c} kWh',
        },
      },
    ],
  }

  rankingChart.value.setOption(option, true)
}

// Show empty state for ranking chart
function updateRankingChartEmpty() {
  if (!rankingChart.value) return
  rankingChart.value.setOption({
    title: {
      text: '暂无数据',
      left: 'center',
      top: 'center',
      textStyle: { color: '#94a3b8', fontSize: 14 },
    },
    xAxis: { data: [] },
    yAxis: { data: [] },
    series: [],
  })
}

// Handle ranking type change
async function updateRankingChart() {
  await loadRankingData()
}

// Initialize distribution chart
function initDistributionChart() {
  if (!distributionChartRef.value) return

  distributionChart.value = echarts.init(distributionChartRef.value)

  // Load distribution data from API
  loadDistributionData()
}

// Load distribution data from API
async function loadDistributionData() {
  try {
    const response = await getDistributionData({ type: 'area' })
    if (response.code === 0 && response.data) {
      updateDistributionChartWithData(response.data)
    }
  } catch (error) {
    console.error('Failed to load distribution data:', error)
    updateDistributionChartEmpty()
  }
}

// Update distribution chart with API data
function updateDistributionChartWithData(data) {
  if (!distributionChart.value || !data) return

  // Backend returns { type, items: [{name, label, value}] }
  const rawItems = Array.isArray(data) ? data : (data.items || data.distribution || [])

  // Add color mapping based on energy type or area
  const energyTypeColors = {
    'ELECTRICITY': '#eab308',
    'WATER': '#3b82f6',
    'GAS': '#ef4444',
  }
  const defaultColors = ['#f97316', '#eab308', '#3b82f6', '#22c55e', '#64748b']

  const chartData = rawItems.map((item, index) => {
    const color = energyTypeColors[item.name] || defaultColors[index % defaultColors.length]
    return {
      name: item.label || item.name,
      value: item.value || 0,
      itemStyle: { color },
    }
  })

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      formatter: '{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: chartColors.text },
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%',
          color: chartColors.text,
          fontSize: 12,
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.2)',
          },
        },
        data: chartData,
      },
    ],
  }

  distributionChart.value.setOption(option)
}

// Show empty state for distribution chart
function updateDistributionChartEmpty() {
  if (!distributionChart.value) return
  distributionChart.value.setOption({
    title: {
      text: '暂无数据',
      left: 'center',
      top: 'center',
      textStyle: { color: '#94a3b8', fontSize: 14 },
    },
    series: [],
  })
}

// Initialize forecast chart
function initForecastChart() {
  if (!forecastChartRef.value) return

  forecastChart.value = echarts.init(forecastChartRef.value)

  updateForecastChart()
}

async function updateForecastChart() {
  // Load forecast data from API
  await loadForecastData()
}

// Load forecast data from API
async function loadForecastData() {
  try {
    // Backend expects period: "7d" or "30d"
    const period = forecastDays.value === 7 ? '7d' : '30d'
    const response = await getForecastData({ period })
    if (response.code === 0 && response.data) {
      updateForecastChartWithData(response.data)
    }
  } catch (error) {
    console.error('Failed to load forecast data:', error)
    updateForecastChartEmpty()
  }
}

// Update forecast chart with API data
function updateForecastChartWithData(data) {
  if (!forecastChart.value || !data) return

  // Process API response data - backend returns { history: [{date, value}], forecast: [{date, predicted_value}] }
  const historyItems = data.history || []
  const forecastItems = data.forecast || []

  // Handle empty data
  if (historyItems.length === 0 && forecastItems.length === 0) {
    updateForecastChartEmpty()
    return
  }

  // Extract dates for x-axis
  const categories = [
    ...historyItems.map(item => item.date || ''),
    ...forecastItems.map(item => item.date || '')
  ]

  // Historical data
  const historicalData = historyItems.map(item => item.value || 0)

  // Forecast data - pad with null to align after historical data
  // The forecast should start from the last historical point
  let forecastData = []
  if (historicalData.length > 0) {
    const lastHistoryValue = historicalData[historicalData.length - 1] || 0
    forecastData = [
      ...Array(historicalData.length - 1).fill(null),
      lastHistoryValue, // Connect to last historical point
      ...forecastItems.map(item => item.predicted_value || 0)
    ]
  } else {
    forecastData = forecastItems.map(item => item.predicted_value || 0)
  }

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
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text },
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 10 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        name: '历史数据',
        type: 'line',
        data: historicalData,
        smooth: true,
        lineStyle: { width: 2, color: chartColors.primary },
        itemStyle: { color: chartColors.primary },
      },
      {
        name: '预测趋势',
        type: 'line',
        data: forecastData,
        smooth: true,
        lineStyle: { width: 2, color: chartColors.green, type: 'dashed' },
        itemStyle: { color: chartColors.green },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(34, 197, 94, 0.2)' },
            { offset: 1, color: 'rgba(34, 197, 94, 0)' },
          ]),
        },
      },
    ],
  }

  forecastChart.value?.setOption(option, true)
}

// Show empty state for forecast chart
function updateForecastChartEmpty() {
  if (!forecastChart.value) return
  forecastChart.value.setOption({
    title: {
      text: '暂无数据',
      left: 'center',
      top: 'center',
      textStyle: { color: '#94a3b8', fontSize: 14 },
    },
    xAxis: { data: [] },
    yAxis: { data: [] },
    series: [],
  })
}

// Get energy type color
function getEnergyColor(type) {
  const colors = {
    '电': '#eab308',
    'WATER': '#3b82f6',
    'GAS': '#ef4444',
    'ELECTRICITY': '#eab308',
  }
  return colors[type] || '#64748b'
}

// Load building options
async function loadBuildingOptions() {
  try {
    const response = await getBuildings()
    if (response.code === 0 && response.data) {
      buildingOptions.value = response.data.map(building => ({
        id: building.id,
        name: building.name,
        children: building.floors?.map(floor => ({
          id: floor.id,
          name: floor.name,
          children: floor.rooms?.map(room => ({
            id: room.id,
            name: room.room_number,
          })),
        })),
      }))
    }
  } catch (error) {
    console.error('Failed to load buildings:', error)
  }
}

// Load table data
async function loadTableData() {
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.size,
    }

    // Add filters if any
    if (filters.value.building?.length > 0) {
      // Get building ID from selected building
      params.building_id = filters.value.building[filters.value.building.length - 1]
    }

    if (filters.value.energyType) {
      params.energy_type = filters.value.energyType
    }

    // Add date range if specified
    if (filters.value.dateRange?.length === 2) {
      params.start_date = filters.value.dateRange[0]
      params.end_date = filters.value.dateRange[1]
    }

    const response = await getEnergyDataDetails(params)

    if (response.code === 0 || response.data) {
      // Backend returns { code: 0, data: [...], total: n }
      const items = response.data || []
      tableData.value = items.map((item) => {
        const value = parseFloat(item.value) || 0
        // Estimate cost based on energy type
        const unitPrice = item.energy_type_code === 'ELECTRICITY' ? 0.8 :
                         item.energy_type_code === 'WATER' ? 5.0 : 3.0
        const cost = value * unitPrice
        return {
          id: item.id,
          date: formatTimestamp(item.timestamp),
          building: item.device_code || '-',
          energyType: item.energy_type_code || '-',
          consumption: value.toFixed(2),
          cost: cost.toFixed(2),
          comparison: 0, // Would need historical data to calculate
          status: 'normal',
          statusText: '正常',
        }
      })
      pagination.value.total = response.total || 0
    } else {
      tableData.value = []
      pagination.value.total = 0
    }
  } catch (error) {
    console.error('Failed to load table data:', error)
    tableData.value = []
    pagination.value.total = 0
  }
}

// Helper function to get energy type name
function getEnergyTypeName(energyType) {
  if (!energyType) return '-'
  if (typeof energyType === 'object') {
    return energyType.name || energyType.code || '-'
  }
  return energyType
}

// Helper function to format timestamp
function formatTimestamp(timestamp) {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

// Handle time range change
function handleTimeRangeChange(range) {
  filters.value.timeRange = range
  // Update charts based on time range
}

// Handle date change
function handleDateChange(dates) {
  filters.value.dateRange = dates
}

// Handle filter change
function handleFilterChange() {
  // Reload data with new filters
}

// Reset filters
function resetFilters() {
  filters.value = {
    timeRange: 'week',
    dateRange: [],
    building: [],
    energyType: '',
  }
}

// Apply filters
async function applyFilters() {
  ElMessage.success('查询中...')
  // Reload all chart data
}

// Handle period change
async function handlePeriodChange(period) {
  activePeriod.value = period
  // Update trend chart based on period - load from API
  await loadTrendData(period)
}

// Load trend data from API
async function loadTrendData(period = activePeriod.value) {
  try {
    const response = await getTrendData({ period })
    if (response.code === 0 && response.data) {
      const series = response.data.series || []
      if (series.length > 0) {
        updateTrendChartWithData(response.data)
      } else {
        // Show empty state
        updateTrendChartEmpty()
      }
    }
  } catch (error) {
    console.error('Failed to load trend data:', error)
  }
}

// Show empty state for trend chart
function updateTrendChartEmpty() {
  if (!trendChart.value) return
  trendChart.value.setOption({
    title: {
      text: '暂无数据',
      left: 'center',
      top: 'center',
      textStyle: {
        color: '#94a3b8',
        fontSize: 14,
      },
    },
    xAxis: { data: [] },
    yAxis: { data: [] },
    series: [],
  })
}

// Update trend chart with API data
function updateTrendChartWithData(data) {
  if (!trendChart.value || !data) return

  // Process API response data - backend returns { period, series }
  const series = data.series || []
  const xAxisData = series.map(item => item.period || '')
  const totalValueData = series.map(item => item.total_value || 0)
  const avgPowerData = series.map(item => item.avg_power || 0)

  trendChart.value.setOption({
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
      axisPointer: { type: 'line' },
    },
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text },
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 10 },
    },
    yAxis: [
      {
        type: 'value',
        name: '能耗量',
        position: 'left',
        axisLine: { show: false },
        axisLabel: { color: chartColors.text, fontSize: 11 },
        splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
      },
      {
        type: 'value',
        name: '平均功率',
        position: 'right',
        axisLine: { show: false },
        axisLabel: { color: chartColors.text, fontSize: 11 },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        name: '能耗量',
        type: 'line',
        yAxisIndex: 0,
        data: totalValueData,
        smooth: true,
        lineStyle: { width: 2, color: chartColors.primary },
        itemStyle: { color: chartColors.primary },
      },
      {
        name: '平均功率',
        type: 'line',
        yAxisIndex: 1,
        data: avgPowerData,
        smooth: true,
        lineStyle: { width: 2, color: chartColors.secondary, type: 'dashed' },
        itemStyle: { color: chartColors.secondary },
      },
    ],
  }, true)
}

// Handle export
async function handleExport(format) {
  try {
    ElMessage.info(`正在导出 ${format.toUpperCase()}...`)

    // Call export API
    const response = await exportEnergyData({
      file_format: format,
      ...filters.value,
    })

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `能耗数据_${new Date().toISOString().slice(0, 10)}.${format === 'excel' ? 'xlsx' : 'pdf'}`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功!')
  } catch (error) {
    console.error('Export failed:', error)
    ElMessage.error('导出失败')
  }
}

// Pagination handlers
function handleSizeChange(size) {
  pagination.value.size = size
  pagination.value.page = 1
  loadTableData()
}

function handlePageChange(page) {
  pagination.value.page = page
  loadTableData()
}

// View detail
function viewDetail(row) {
  ElMessage.info(`查看详情: ${row.building} - ${row.date}`)
}

// Handle window resize
function handleResize() {
  trendChart.value?.resize()
  comparisonChart.value?.resize()
  rankingChart.value?.resize()
  distributionChart.value?.resize()
  forecastChart.value?.resize()
}

// Lifecycle
onMounted(async () => {
  await nextTick()

  // Initialize all charts (they will load data from API)
  initTrendChart()
  initComparisonChart()
  initRankingChart()
  initDistributionChart()
  initForecastChart()

  // Load initial data from API
  loadTrendData(activePeriod.value)
  loadBuildingOptions()
  loadTableData()

  // Handle resize
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // Dispose all charts
  trendChart.value?.dispose()
  comparisonChart.value?.dispose()
  rankingChart.value?.dispose()
  distributionChart.value?.dispose()
  forecastChart.value?.dispose()

  // Remove event listener
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.analysis-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ========================================
   FILTER BAR
   ======================================== */
.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-group {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-label {
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
}

.time-range-selector {
  display: flex;
  background: #f8fafc;
  border-radius: 8px;
  padding: 2px;
}

.range-btn {
  padding: 6px 14px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.range-btn:hover {
  color: #1f2937;
}

.range-btn.active {
  background: #fff;
  color: #f97316;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.option-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.filter-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

/* ========================================
   CHARTS SECTION
   ======================================== */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.chart-row.full-width {
  grid-template-columns: 1fr;
}

.chart-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.title-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 16px;
}

.period-btn {
  padding: 5px 12px;
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 6px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-btn:hover {
  border-color: #f97316;
  color: #f97316;
}

.period-btn.active {
  background: #f97316;
  border-color: #f97316;
  color: #fff;
}

.card-body {
  flex: 1;
  min-height: 280px;
  padding: 12px;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 260px;
}

/* ========================================
   TABLE SECTION
   ======================================== */
.table-section {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.table-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.table-actions {
  display: flex;
  gap: 8px;
}

.type-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.value-text {
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  color: #1f2937;
}

.change-text {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 12px;
  font-weight: 500;
}

.change-text.up {
  color: #ef4444;
}

.change-text.down {
  color: #22c55e;
}

.status-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.status-badge.status-normal {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.status-badge.status-warning {
  background: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.status-badge.status-danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: 12px 16px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .chart-row {
    grid-template-columns: 1fr;
  }

  .half-width {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-actions {
    margin-left: 0;
    justify-content: stretch;
  }

  .filter-actions .el-button {
    flex: 1;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-input__wrapper),
:deep(.el-select .el-input__wrapper),
:deep(.el-cascader .el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #e5e7eb inset;
}

:deep(.el-input__wrapper:hover),
:deep(.el-select:hover .el-input__wrapper) {
  box-shadow: 0 0 0 1px #f97316 inset;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-select:focus .el-input__wrapper) {
  box-shadow: 0 0 0 1px #f97316 inset;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
  border: none;
}

:deep(.el-table) {
  font-size: 13px;
}

:deep(.el-table th) {
  font-weight: 600;
}

:deep(.el-table .cell) {
  padding: 8px 12px;
}
</style>
