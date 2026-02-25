<template>
  <div class="usage-history-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="page-title">
            <span class="title-icon"><icon-ep-data-line /></span>
            用能查询
          </h1>
          <p class="page-subtitle">追踪您的能耗足迹，发现节能潜力</p>
        </div>
        <div class="header-actions">
          <el-button-group class="view-toggle">
            <el-button
              :type="viewMode === 'calendar' ? 'primary' : ''"
              @click="viewMode = 'calendar'"
            >
              <el-icon><icon-ep-calendar /></el-icon>
              日历视图
            </el-button>
            <el-button
              :type="viewMode === 'list' ? 'primary' : ''"
              @click="viewMode = 'list'"
            >
              <el-icon><icon-ep-list /></el-icon>
              列表视图
            </el-button>
          </el-button-group>
        </div>
      </div>
      <div class="header-decoration">
        <div class="decoration-wave"></div>
        <div class="decoration-wave"></div>
        <div class="decoration-wave"></div>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="filter-card">
        <div class="filter-row">
          <div class="filter-item">
            <label class="filter-label">
              <el-icon><icon-ep-calendar /></el-icon>
              时间范围
            </label>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :clearable="true"
              @change="loadData"
            />
          </div>
          <div class="filter-item">
            <label class="filter-label">
              <el-icon><icon-ep-cpu /></el-icon>
              能源类型
            </label>
            <el-select v-model="selectedEnergyType" placeholder="全部" @change="loadData">
              <el-option label="全部" value="" />
              <el-option label="电" value="ELECTRICITY">
                <div class="energy-option">
                  <span class="energy-dot" style="background: #eab308"></span>
                  <span>电 (kWh)</span>
                </div>
              </el-option>
              <el-option label="水" value="WATER">
                <div class="energy-option">
                  <span class="energy-dot" style="background: #3b82f6"></span>
                  <span>水 (m³)</span>
                </div>
              </el-option>
              <el-option label="气" value="GAS">
                <div class="energy-option">
                  <span class="energy-dot" style="background: #ef4444"></span>
                  <span>气 (m³)</span>
                </div>
              </el-option>
            </el-select>
          </div>
          <div class="filter-item">
            <label class="filter-label">
              <el-icon><icon-ep-house /></el-icon>
              房间
            </label>
            <el-select v-model="selectedRoom" placeholder="全部房间" @change="loadData">
              <el-option label="全部房间" value="" />
              <el-option
                v-for="room in boundRooms"
                :key="room.id"
                :label="room.name"
                :value="room.id"
              />
            </el-select>
          </div>
          <div class="filter-actions">
            <el-button type="primary" @click="loadData">
              <el-icon><icon-ep-search /></el-icon>
              查询
            </el-button>
            <el-button @click="handleExport">
              <el-icon><icon-ep-download /></el-icon>
              导出
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Summary -->
    <div class="stats-summary">
      <div v-for="(stat, index) in summaryStats" :key="index" class="stat-card">
        <div class="stat-bg-pattern"></div>
        <div class="stat-icon" :style="{ background: stat.color + '20', color: stat.color }">
          <component :is="stat.icon" />
        </div>
        <div class="stat-content">
          <span class="stat-label">{{ stat.label }}</span>
          <div class="stat-value-wrapper">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-unit">{{ stat.unit }}</span>
          </div>
          <span v-if="stat.change" class="stat-change" :class="stat.changeClass">
            <el-icon><icon-ep-caret-top v-if="stat.changeClass === 'up'" /><icon-ep-caret-bottom v-else /></el-icon>
            {{ stat.change }}
          </span>
        </div>
      </div>
    </div>

    <!-- Calendar View -->
    <div v-show="viewMode === 'calendar'" class="calendar-view">
      <div class="calendar-card">
        <div class="calendar-header">
          <h3 class="calendar-title">
            <span class="title-icon"><icon-ep-calendar /></span>
            能耗日历热力图
          </h3>
          <div class="calendar-legend">
            <span class="legend-label">能耗强度：</span>
            <div class="legend-scale">
              <span class="scale-item low">低</span>
              <div class="scale-gradient"></div>
              <span class="scale-item high">高</span>
            </div>
          </div>
        </div>
        <div class="calendar-body">
          <div class="calendar-grid">
            <div
              v-for="(day, index) in calendarDays"
              :key="index"
              class="calendar-day"
              :class="{
                'is-empty': !day.value,
                'is-today': day.isToday,
                [`level-${day.level || 0}`]: day.value
              }"
              @click="showDayDetail(day)"
            >
              <span class="day-date">{{ day.date }}</span>
              <span v-if="day.value" class="day-value">{{ day.value }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <div class="chart-card trend-chart">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-trend-charts /></span>
            用能趋势分析
          </h3>
        </div>
        <div class="card-body">
          <div ref="trendChartRef" class="chart-container"></div>
        </div>
      </div>

      <div class="chart-card hourly-chart">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-data-analysis /></span>
            时段分析
          </h3>
        </div>
        <div class="card-body">
          <div ref="hourlyChartRef" class="chart-container"></div>
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="table-section">
      <div class="table-card">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-document /></span>
            详细数据记录
          </h3>
          <div class="table-actions">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索..."
              prefix-icon="Search"
              style="width: 200px"
            />
          </div>
        </div>
        <div class="card-body">
          <el-table
            :data="filteredTableData"
            style="width: 100%"
            stripe
            :header-cell-style="{ background: '#fef7f0', color: '#1f2937' }"
          >
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column label="能源类型" width="100">
              <template #default="{ row }">
                <div class="energy-type-cell">
                  <span class="type-dot" :style="{ background: getEnergyColor(row.type) }"></span>
                  <span>{{ getEnergyLabel(row.type) }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="value" label="用量" width="120">
              <template #default="{ row }">
                <span class="value-text">{{ row.value }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="unit" label="单位" width="80" />
            <el-table-column prop="cost" label="费用" width="120">
              <template #default="{ row }">
                <span class="cost-text">¥{{ row.cost.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="room" label="房间" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'normal' ? 'success' : 'warning'" size="small">
                  {{ row.status === 'normal' ? '正常' : '异常' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="totalRecords"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadData"
              @current-change="loadData"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Day Detail Dialog -->
    <el-dialog
      v-model="showDayDialog"
      :title="`${selectedDay?.date} 能耗详情`"
      width="500px"
      class="day-detail-dialog"
    >
      <div v-if="selectedDay" class="day-detail-content">
        <div class="detail-summary">
          <div class="summary-item">
            <span class="summary-label">日期</span>
            <span class="summary-value">{{ selectedDay.date }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">总用量</span>
            <span class="summary-value">{{ selectedDay.value }} {{ selectedDay.unit }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">费用</span>
            <span class="summary-value">¥{{ selectedDay.cost?.toFixed(2) || '0.00' }}</span>
          </div>
        </div>
        <div class="detail-breakdown">
          <h4>分项明细</h4>
          <div v-for="(item, index) in selectedDay.breakdown" :key="index" class="breakdown-item">
            <span class="breakdown-dot" :style="{ background: item.color }"></span>
            <span class="breakdown-label">{{ item.label }}</span>
            <span class="breakdown-value">{{ item.value }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getEnergyData, getEnergyStatistics, exportEnergyData } from '@/api/energy'
import { getMyBindRooms } from '@/api/profile'
import { getHourlyDistribution } from '@/api/analysis'

// Chart refs
const trendChartRef = ref(null)
const hourlyChartRef = ref(null)

// Chart instances using shallowRef
const trendChart = shallowRef(null)
const hourlyChart = shallowRef(null)

// View mode
const viewMode = ref('calendar')

// Filters
const dateRange = ref([])
const selectedEnergyType = ref('')
const selectedRoom = ref('')
const searchKeyword = ref('')

// Data
const boundRooms = ref([])
const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)

// Summary stats - 从API获取
const summaryStats = ref([
  {
    label: '总用量',
    value: '-',
    unit: 'kWh',
    icon: 'icon-ep-lightning',
    color: '#eab308',
    change: '',
    changeClass: 'down',
  },
  {
    label: '总费用',
    value: '-',
    unit: '元',
    icon: 'icon-ep-wallet',
    color: '#22c55e',
    change: '',
    changeClass: 'up',
  },
  {
    label: '日均用量',
    value: '-',
    unit: 'kWh/天',
    icon: 'icon-ep-trend-charts',
    color: '#3b82f6',
    change: '',
    changeClass: 'down',
  },
  {
    label: '数据记录',
    value: '-',
    unit: '条',
    icon: 'icon-ep-document',
    color: '#f97316',
  },
])

// Calendar data
const calendarDays = ref([])
const showDayDialog = ref(false)
const selectedDay = ref(null)

// ECharts colors
const chartColors = {
  primary: '#f97316',
  secondary: '#eab308',
  water: '#3b82f6',
  gas: '#ef4444',
  green: '#22c55e',
  text: '#64748b',
  grid: '#e2e8f0',
}

// Computed
const filteredTableData = computed(() => {
  if (!searchKeyword.value) return tableData.value
  return tableData.value.filter(item =>
    item.date.includes(searchKeyword.value) ||
    item.room.includes(searchKeyword.value)
  )
})

// Initialize trend chart
function initTrendChart() {
  if (!trendChartRef.value) return

  trendChart.value = echarts.init(trendChartRef.value)

  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
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
      textStyle: { color: chartColors.text, fontSize: 12 },
      itemGap: 20,
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [],
  }

  trendChart.value.setOption(option)
}

// Initialize hourly chart with API data
async function initHourlyChart() {
  if (!hourlyChartRef.value) return

  hourlyChart.value = echarts.init(hourlyChartRef.value)

  // Default data in case API fails
  let hourlyData = [0, 0, 0, 0, 0, 0]

  try {
    const response = await getHourlyDistribution({})
    if (response.code === 0 && response.data && response.data.buckets) {
      hourlyData = response.data.buckets.map(bucket => parseFloat(bucket.total_value.toFixed(2)))
    }
  } catch (error) {
    console.error('Failed to load hourly distribution:', error)
  }

  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '8%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: {
        type: 'shadow',
      },
    },
    xAxis: {
      type: 'category',
      data: ['0-4时', '4-8时', '8-12时', '12-16时', '16-20时', '20-24时'],
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
        name: '用量',
        type: 'bar',
        data: hourlyData,
        itemStyle: {
          borderRadius: [6, 6, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#f97316' },
            { offset: 1, color: '#ea580c' },
          ]),
        },
        barWidth: '50%',
      },
    ],
  }

  hourlyChart.value.setOption(option)
}

// Generate calendar days from actual energy data
function generateCalendarDays() {
  const days = []
  const today = new Date()
  const daysInMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate()

  // Group data by date
  const dataByDate = {}
  tableData.value.forEach(item => {
    if (!dataByDate[item.date]) {
      dataByDate[item.date] = { total: 0, count: 0, byType: {} }
    }
    const value = parseFloat(item.value) || 0
    dataByDate[item.date].total += value
    dataByDate[item.date].count += 1
    if (!dataByDate[item.date].byType[item.type]) {
      dataByDate[item.date].byType[item.type] = 0
    }
    dataByDate[item.date].byType[item.type] += value
  })

  for (let i = 1; i <= daysInMonth; i++) {
    const date = new Date(today.getFullYear(), today.getMonth(), i)
    const isToday = i === today.getDate()
    const dateStr = date.toISOString().split('T')[0]
    const dayOfWeek = date.getDay()

    // Get actual value from data
    const dayData = dataByDate[dateStr]
    const value = dayData ? dayData.total : (dayOfWeek === 0 ? 0 : 0)
    const level = value === 0 ? 0 : value < 15 ? 1 : value < 30 ? 2 : value < 45 ? 3 : 4

    // Build breakdown from actual data
    const breakdown = []
    if (dayData && dayData.byType) {
      if (dayData.byType.ELECTRICITY) {
        breakdown.push({ label: '电', value: dayData.byType.ELECTRICITY.toFixed(1), color: '#eab308' })
      }
      if (dayData.byType.WATER) {
        breakdown.push({ label: '水', value: dayData.byType.WATER.toFixed(1), color: '#3b82f6' })
      }
      if (dayData.byType.GAS) {
        breakdown.push({ label: '气', value: dayData.byType.GAS.toFixed(1), color: '#ef4444' })
      }
    }

    days.push({
      date: `${i}日`,
      fullDate: dateStr,
      value,
      unit: 'kWh',
      cost: value * 0.52,
      isToday,
      level,
      breakdown: breakdown.length > 0 ? breakdown : [
        { label: '电', value: '0', color: '#eab308' },
        { label: '水', value: '0', color: '#3b82f6' },
        { label: '气', value: '0', color: '#ef4444' },
      ],
    })
  }

  calendarDays.value = days
}

// Load data
async function loadData() {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
    }

    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0].toISOString().split('T')[0]
      params.end_date = dateRange.value[1].toISOString().split('T')[0]
    }

    if (selectedEnergyType.value) {
      params.energy_type = selectedEnergyType.value
    }

    if (selectedRoom.value) {
      params.room_id = selectedRoom.value
    }

    const response = await getEnergyData(params)
    if (response.code === 0) {
      tableData.value = (response.data || []).map(item => ({
        date: item.timestamp?.split('T')[0] || '',
        type: item.energy_type || 'ELECTRICITY',
        value: typeof item.value === 'number' ? item.value.toFixed(2) : String(item.value || '0'),
        unit: getEnergyUnit(item.energy_type),
        cost: item.cost || 0,
        room: item.room_name || '301宿舍',
        status: item.value > 50 ? 'high' : 'normal',
      }))
      totalRecords.value = response.total || tableData.value.length

      // Update summary
      const totalValue = tableData.value.reduce((sum, item) => sum + parseFloat(item.value), 0)
      summaryStats.value[0].value = totalValue.toFixed(1)
      summaryStats.value[1].value = (totalValue * 0.52).toFixed(2)
      summaryStats.value[2].value = (totalValue / Math.max(tableData.value.length, 1)).toFixed(1)
      summaryStats.value[3].value = totalRecords.value.toString()

      // Update charts
      updateChartsWithData(tableData.value)
    }
  } catch (error) {
    console.error('Failed to load energy data:', error)
    ElMessage.error('加载能耗数据失败，请稍后重试')
    tableData.value = []
    totalRecords.value = 0
  }
}

// Mock function removed - using real API

function updateChartsWithData(data) {
  if (trendChart.value && data.length > 0) {
    const dates = [...new Set(data.map(d => d.date))].sort().slice(-30)
    const values = dates.map(date => {
      return data.filter(d => d.date === date).reduce((sum, d) => sum + parseFloat(d.value), 0)
    })

    trendChart.value.setOption({
      xAxis: { data: dates.map(d => d.slice(5)) },
      series: [
        {
          name: '用量',
          type: 'line',
          smooth: true,
          data: values,
          lineStyle: { width: 3, color: chartColors.secondary },
          itemStyle: { color: chartColors.secondary },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(234, 179, 8, 0.3)' },
              { offset: 1, color: 'rgba(234, 179, 8, 0)' },
            ]),
          },
        },
      ],
    })
  }
}

// Export data
async function handleExport() {
  try {
    const format = 'excel'
    ElMessage.info('正在导出数据...')
    const response = await exportEnergyData({ file_format: format })
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `能耗数据_${new Date().toISOString().split('T')[0]}.xlsx`
    a.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('Export failed:', error)
    ElMessage.error('导出失败，请重试')
  }
}

// Show day detail
function showDayDetail(day) {
  if (!day.value) return
  selectedDay.value = day
  showDayDialog.value = true
}

// Get energy color
function getEnergyColor(type) {
  const colors = {
    ELECTRICITY: '#eab308',
    WATER: '#3b82f6',
    GAS: '#ef4444',
  }
  return colors[type] || '#eab308'
}

// Get energy label
function getEnergyLabel(type) {
  const labels = {
    ELECTRICITY: '电',
    WATER: '水',
    GAS: '气',
  }
  return labels[type] || '电'
}

// Get energy unit
function getEnergyUnit(type) {
  const units = {
    ELECTRICITY: 'kWh',
    WATER: 'm³',
    GAS: 'm³',
  }
  return units[type] || 'kWh'
}

// Load bound rooms
async function loadBoundRooms() {
  try {
    const response = await getMyBindRooms()
    if (response.code === 0 && response.data) {
      boundRooms.value = response.data.map(room => ({
        id: room.id,
        name: room.room_number || `房间${room.id}`,
      }))
    }
  } catch (error) {
    console.error('Failed to load rooms:', error)
    boundRooms.value = [
      { id: 1, name: '301宿舍' },
      { id: 2, name: '实验室201' },
    ]
  }
}

// Handle resize
function handleResize() {
  trendChart.value?.resize()
  hourlyChart.value?.resize()
}

// Lifecycle
onMounted(async () => {
  // Set default date range (current month)
  const now = new Date()
  dateRange.value = [
    new Date(now.getFullYear(), now.getMonth(), 1),
    new Date(now.getFullYear(), now.getMonth() + 1, 0),
  ]

  await Promise.all([
    new Promise(resolve => setTimeout(resolve, 100)).then(() => initTrendChart()),
    new Promise(resolve => setTimeout(resolve, 100)).then(() => initHourlyChart()),
  ])

  generateCalendarDays()
  loadBoundRooms()
  loadData()

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  trendChart.value?.dispose()
  hourlyChart.value?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Orbitron:wght@400;500;600;700&display=swap');

.usage-history-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   PAGE HEADER
   ======================================== */
.page-header {
  position: relative;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 20px;
  padding: 28px 32px;
  color: white;
  overflow: hidden;
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-text .page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

.page-title .title-icon {
  display: flex;
  font-size: 24px;
}

.page-subtitle {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.header-decoration {
  position: absolute;
  right: 0;
  bottom: 0;
  display: flex;
  gap: 8px;
  opacity: 0.3;
}

.decoration-wave {
  width: 120px;
  height: 60px;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 120 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 30 Q30 10 60 30 T120 30 V60 H0 Z' fill='white'/%3E%3C/svg%3E") no-repeat;
  animation: wave 3s ease-in-out infinite;
}

.decoration-wave:nth-child(2) {
  animation-delay: 0.5s;
  opacity: 0.7;
}

.decoration-wave:nth-child(3) {
  animation-delay: 1s;
  opacity: 0.4;
}

@keyframes wave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.view-toggle :deep(.el-button) {
  border-radius: 10px;
  font-weight: 500;
}

/* ========================================
   FILTER SECTION
   ======================================== */
.filter-section {
  animation: fadeInUp 0.5s ease-out 0.1s both;
}

.filter-card {
  background: white;
  border-radius: 16px;
  padding: 20px 24px;
  border: 1px solid #e5e7eb;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: flex-end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
}

.filter-label .el-icon {
  font-size: 14px;
  color: #f97316;
}

.filter-actions {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.energy-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.energy-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* ========================================
   STATS SUMMARY
   ======================================== */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  animation: fadeInUp 0.5s ease-out 0.2s both;
}

.stat-card {
  position: relative;
  background: linear-gradient(135deg, #fff 0%, #fefefc 100%);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(249, 115, 22, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(249, 115, 22, 0.15);
}

.stat-bg-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.4;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 12px 12px;
}

.stat-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  font-size: 18px;
  margin-bottom: 12px;
}

.stat-content {
  position: relative;
}

.stat-label {
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
}

.stat-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin: 8px 0;
}

.stat-value {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #1f2937;
}

.stat-unit {
  font-size: 13px;
  color: #9ca3af;
}

.stat-change {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 8px;
  font-weight: 500;
}

.stat-change.up {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.stat-change.down {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

/* ========================================
   CALENDAR VIEW
   ======================================== */
.calendar-view {
  animation: fadeInUp 0.5s ease-out 0.3s both;
}

.calendar-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.calendar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.calendar-legend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748b;
}

.legend-scale {
  display: flex;
  align-items: center;
  gap: 6px;
}

.scale-gradient {
  width: 80px;
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(90deg, #fef3c7 0%, #fde047 25%, #facc15 50%, #eab308 75%, #ca8a04 100%);
}

.calendar-body {
  padding: 20px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.calendar-day.is-empty {
  background: #f8fafc;
  color: #cbd5e1;
  cursor: default;
}

.calendar-day.is-today {
  border: 2px solid #f97316;
}

.calendar-day.level-1 { background: #fef9c3; }
.calendar-day.level-2 { background: #fef08a; }
.calendar-day.level-3 { background: #fde047; }
.calendar-day.level-4 { background: #facc15; }

.calendar-day:not(.is-empty):hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.day-date {
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 2px;
}

.day-value {
  font-size: 11px;
  font-weight: 600;
  color: #1f2937;
}

/* ========================================
   CHARTS SECTION
   ======================================== */
.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
  animation: fadeInUp 0.5s ease-out 0.4s both;
}

.chart-card {
  background: white;
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
  color: #1f2937;
}

.title-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 18px;
}

.card-body {
  flex: 1;
  padding: 16px 20px;
  min-height: 280px;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 250px;
}

/* ========================================
   TABLE SECTION
   ======================================== */
.table-section {
  animation: fadeInUp 0.5s ease-out 0.5s both;
}

.table-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.table-actions {
  display: flex;
  gap: 12px;
}

.energy-type-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.type-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.value-text {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-weight: 600;
  color: #1f2937;
}

.cost-text {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-weight: 600;
  color: #22c55e;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   DIALOG
   ======================================== */
.day-detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
}

.summary-label {
  font-size: 12px;
  color: #64748b;
}

.summary-value {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.detail-breakdown h4 {
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
}

.breakdown-item:last-child {
  border-bottom: none;
}

.breakdown-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.breakdown-label {
  flex: 1;
  font-size: 13px;
  color: #64748b;
}

.breakdown-value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

/* ========================================
   ANIMATIONS
   ======================================== */
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

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .filter-row {
    flex-direction: column;
  }

  .filter-actions {
    margin-left: 0;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .calendar-grid {
    gap: 4px;
  }

  .detail-summary {
    grid-template-columns: 1fr;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-input__wrapper) {
  border-radius: 10px;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 10px;
}

:deep(.el-picker__popper) {
  border-radius: 12px;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-table th) {
  font-weight: 600;
}

:deep(.el-dialog) {
  border-radius: 16px;
}
</style>
