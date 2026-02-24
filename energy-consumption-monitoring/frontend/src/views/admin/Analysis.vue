<template>
  <div class="analysis-container">
    <!-- Top Filter Section -->
    <div class="filter-bar">
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
    </div>

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
            :data="paginatedTableData"
            stripe
            border
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#64748b' }"
          >
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="building" label="建筑" width="120" />
            <el-table-column prop="energyType" label="能源类型" width="100">
              <template #default="{ row }">
                <span class="type-badge" :style="{ background: `${getEnergyColor(row.energyType)}15`, color: getEnergyColor(row.energyType) }">
                  {{ row.energyType }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="consumption" label="能耗量" width="120">
              <template #default="{ row }">
                <span class="value-text">{{ row.consumption }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="cost" label="费用 (元)" width="120" />
            <el-table-column prop="comparison" label="同比变化" width="100">
              <template #default="{ row }">
                <span :class="['change-text', row.comparison >= 0 ? 'up' : 'down']">
                  <el-icon><icon-ep-caret-top v-if="row.comparison >= 0" /><icon-ep-caret-bottom v-else /></el-icon>
                  {{ Math.abs(row.comparison) }}%
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
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
import { exportEnergyData } from '@/api/energy'

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
        type: 'cross',
        lineStyle: { color: '#f97316', type: 'dashed' },
      },
    },
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text },
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        name: '本期',
        type: 'line',
        smooth: true,
        data: [4200, 4800, 4500, 5200, 4900, 5800, 6200, 5900, 5100, 4800, 5300, 5600],
        lineStyle: { width: 3, color: chartColors.primary },
        itemStyle: { color: chartColors.primary, borderWidth: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(249, 115, 22, 0.3)' },
            { offset: 1, color: 'rgba(249, 115, 22, 0)' },
          ]),
        },
      },
      {
        name: '同期',
        type: 'line',
        smooth: true,
        data: [3800, 4200, 4000, 4800, 4500, 5200, 5500, 5300, 4600, 4300, 4800, 5100],
        lineStyle: { width: 2, color: chartColors.text, type: 'dashed' },
        itemStyle: { color: chartColors.text },
      },
    ],
  }

  trendChart.value.setOption(option)
}

// Initialize comparison chart
function initComparisonChart() {
  if (!comparisonChartRef.value) return

  comparisonChart.value = echarts.init(comparisonChartRef.value)

  const option = {
    grid: {
      left: '3%',
      right: '3%',
      bottom: '3%',
      top: '8%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: { type: 'shadow' },
    },
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text },
    },
    xAxis: {
      type: 'category',
      data: ['教学楼A', '教学楼B', '实验楼', '图书馆', '行政楼'],
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 10, rotate: 30 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        name: '本期',
        type: 'bar',
        data: [12500, 9800, 8600, 7200, 5400],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#f97316' },
            { offset: 1, color: '#ea580c' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
      },
      {
        name: '同期',
        type: 'bar',
        data: [11200, 9200, 8100, 6800, 5100],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#94a3b8' },
            { offset: 1, color: '#64748b' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
      },
    ],
  }

  comparisonChart.value.setOption(option)
}

// Initialize ranking chart
function initRankingChart() {
  if (!rankingChartRef.value) return

  rankingChart.value = echarts.init(rankingChartRef.value)

  updateRankingChart()
}

function updateRankingChart() {
  const data = rankingType.value === 'building'
    ? [
        { name: '教学楼A', value: 12500 },
        { name: '教学楼B', value: 9800 },
        { name: '实验楼', value: 8600 },
        { name: '图书馆', value: 7200 },
        { name: '行政楼', value: 5400 },
        { name: '食堂', value: 4800 },
        { name: '体育馆', value: 3200 },
        { name: '宿舍A', value: 8900 },
        { name: '宿舍B', value: 8200 },
        { name: '活动中心', value: 2800 },
      ]
    : [
        { name: '计算机学院', value: 15600 },
        { name: '物理学院', value: 12300 },
        { name: '化学学院', value: 10800 },
        { name: '图书馆', value: 7200 },
        { name: '行政部', value: 5400 },
        { name: '后勤部', value: 4800 },
        { name: '学生会', value: 3200 },
        { name: '教务处', value: 2800 },
      ]

  const sortedData = [...data].sort((a, b) => b.value - a.value)

  const option = {
    grid: {
      left: '3%',
      right: '8%',
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
      data: sortedData.map(d => d.name),
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
    },
    series: [
      {
        type: 'bar',
        data: sortedData.map(d => d.value),
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

  rankingChart.value?.setOption(option, true)
}

// Initialize distribution chart
function initDistributionChart() {
  if (!distributionChartRef.value) return

  distributionChart.value = echarts.init(distributionChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      formatter: '{b}: {c}% ({d}%)',
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
        data: [
          { value: 45, name: '教学楼', itemStyle: { color: '#f97316' } },
          { value: 20, name: '宿舍楼', itemStyle: { color: '#eab308' } },
          { value: 15, name: '实验楼', itemStyle: { color: '#3b82f6' } },
          { value: 10, name: '图书馆', itemStyle: { color: '#22c55e' } },
          { value: 10, name: '其他', itemStyle: { color: '#64748b' } },
        ],
      },
    ],
  }

  distributionChart.value.setOption(option)
}

// Initialize forecast chart
function initForecastChart() {
  if (!forecastChartRef.value) return

  forecastChart.value = echarts.init(forecastChartRef.value)

  updateForecastChart()
}

function updateForecastChart() {
  const days = forecastDays.value
  const categories = []
  const historicalData = []
  const forecastData = []

  const today = new Date()
  for (let i = days; i > 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    categories.push(`${date.getMonth() + 1}/${date.getDate()}`)
    historicalData.push(Math.floor(4000 + Math.random() * 2000))
  }

  for (let i = 0; i < Math.min(days, 7); i++) {
    const date = new Date(today)
    date.setDate(date.getDate() + i)
    if (i === 0 && categories.length > 0) {
      // Today is already in categories
    } else {
      categories.push(`${date.getMonth() + 1}/${date.getDate()}`)
    }
    forecastData.push(Math.floor(4500 + Math.random() * 2000))
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
        data: historicalData.concat(Array(Math.min(days, 7)).fill(null)),
        smooth: true,
        lineStyle: { width: 2, color: chartColors.primary },
        itemStyle: { color: chartColors.primary },
      },
      {
        name: '预测趋势',
        type: 'line',
        data: Array(historicalData.length - 1).fill(null).concat(historicalData[historicalData.length - 1]).concat(forecastData),
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
    // Mock data
    buildingOptions.value = [
      {
        id: 1,
        name: '主校区',
        children: [
          { id: 11, name: '教学楼A' },
          { id: 12, name: '实验楼' },
          { id: 13, name: '图书馆' },
        ],
      },
    ]
  }
}

// Load table data
async function loadTableData() {
  // Mock data
  tableData.value = [
    { date: '2024-01-15', building: '教学楼A', energyType: '电', consumption: '12,450 kWh', cost: '9,867.50', comparison: 5.2, status: 'normal', statusText: '正常' },
    { date: '2024-01-15', building: '教学楼A', energyType: '水', consumption: '125 m³', cost: '562.50', comparison: -3.1, status: 'normal', statusText: '正常' },
    { date: '2024-01-15', building: '实验楼', energyType: '电', consumption: '8,620 kWh', cost: '6,842.80', comparison: 12.5, status: 'warning', statusText: '偏高' },
    { date: '2024-01-15', building: '实验楼', energyType: '水', consumption: '45 m³', cost: '202.50', comparison: -8.2, status: 'normal', statusText: '正常' },
    { date: '2024-01-14', building: '教学楼B', energyType: '电', consumption: '9,800 kWh', cost: '7,762.00', comparison: 2.8, status: 'normal', statusText: '正常' },
    { date: '2024-01-14', building: '图书馆', energyType: '电', consumption: '7,200 kWh', cost: '5,688.00', comparison: -1.5, status: 'normal', statusText: '正常' },
    { date: '2024-01-14', building: '行政楼', energyType: '电', consumption: '5,400 kWh', cost: '4,284.00', comparison: 0, status: 'normal', statusText: '正常' },
    { date: '2024-01-13', building: '教学楼A', energyType: '气', consumption: '82 m³', cost: '328.00', comparison: 4.2, status: 'normal', statusText: '正常' },
    { date: '2024-01-13', building: '食堂', energyType: '电', consumption: '4,800 kWh', cost: '3,648.00', comparison: 8.5, status: 'normal', statusText: '正常' },
    { date: '2024-01-13', building: '食堂', energyType: '水', consumption: '156 m³', cost: '702.00', comparison: -2.3, status: 'normal', statusText: '正常' },
  ]
  pagination.value.total = tableData.value.length
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
function handlePeriodChange(period) {
  activePeriod.value = period
  // Update trend chart
}

// Handle export
async function handleExport(format) {
  try {
    ElMessage.info(`正在导出 ${format.toUpperCase()}...`)

    // Call export API
    const response = await exportEnergyData({
      format: format,
      ...filters.value,
    })

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response]))
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
}

function handlePageChange(page) {
  pagination.value.page = page
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

  // Initialize all charts
  initTrendChart()
  initComparisonChart()
  initRankingChart()
  initDistributionChart()
  initForecastChart()

  // Load data
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
  padding: 8px 0;
}
</style>
