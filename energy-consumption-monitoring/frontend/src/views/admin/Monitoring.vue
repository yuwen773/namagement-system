<template>
  <div class="monitoring-container">
    <!-- Left Tree Navigation -->
    <div class="tree-sidebar">
      <div class="sidebar-header">
        <h3 class="sidebar-title">
          <span class="title-icon"><icon-ep-location-information /></span>
          监测点导航
        </h3>
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索建筑/房间..."
            prefix-icon="Search"
            clearable
            size="small"
          />
        </div>
      </div>

      <div class="tree-content">
        <el-tree
          ref="treeRef"
          :data="buildingTree"
          :props="treeProps"
          :filter-node-method="filterNode"
          :highlight-current="true"
          node-key="id"
          :expand-on-click-node="false"
          @node-click="handleNodeClick"
          class="location-tree"
        >
          <template #default="{ node, data }">
            <div class="tree-node">
              <span class="node-icon" :class="`icon-${data.type}`">
                <el-icon v-if="data.type === 'campus'"><icon-ep-school /></el-icon>
                <el-icon v-else-if="data.type === 'building'"><icon-ep-office-building /></el-icon>
                <el-icon v-else-if="data.type === 'floor'"><icon-ep-map-location /></el-icon>
                <el-icon v-else><icon-ep-house /></el-icon>
              </span>
              <span class="node-label">{{ node.label }}</span>
              <span v-if="data.deviceCount" class="node-badge">{{ data.deviceCount }}</span>
            </div>
          </template>
        </el-tree>
      </div>

      <div class="sidebar-footer">
        <div class="tree-legend">
          <div class="legend-item">
            <span class="legend-dot dot-online"></span>
            <span>在线</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot dot-offline"></span>
            <span>离线</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot dot-warning"></span>
            <span>告警</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Content Area -->
    <div class="content-area">
      <!-- Selection Info Bar -->
      <div class="selection-bar">
        <div class="selection-breadcrumb">
          <span class="breadcrumb-item" v-for="(item, index) in breadcrumbPath" :key="index">
            <el-icon><icon-ep-arrow-right /></el-icon>
            {{ item }}
          </span>
        </div>
        <div class="selection-actions">
          <el-button size="small" @click="refreshData">
            <el-icon><icon-ep-refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </div>

      <!-- Real-time Data Cards -->
      <div class="data-cards-grid" v-if="selectedNode">
        <div class="data-card" v-for="(card, index) in dataCards" :key="index">
          <div class="card-background">
            <div class="grid-pattern"></div>
            <div class="glow-effect" :style="{ background: card.color }"></div>
          </div>
          <div class="card-content">
            <div class="card-header-row">
              <span class="card-label">{{ card.label }}</span>
              <span class="card-unit">{{ card.unit }}</span>
            </div>
            <div class="card-value-row">
              <span class="card-value" :style="{ color: card.color }">
                {{ card.displayValue }}
              </span>
              <span class="card-change" :class="card.trend">
                <el-icon><icon-ep-caret-top v-if="card.trend === 'up'" /><icon-ep-caret-bottom v-else /></el-icon>
                {{ card.change }}
              </span>
            </div>
            <div class="card-sparkline">
              <svg :viewBox="`0 0 ${card.sparkline.length * 8} 20`" class="sparkline-svg">
                <polyline
                  :points="card.sparkline.map((v, i) => `${i * 8},${20 - v}`).join(' ')"
                  fill="none"
                  :stroke="card.color"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
          </div>
          <div class="live-indicator" v-if="card.live">
            <span class="live-dot"></span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state" v-else>
        <div class="empty-icon">
          <el-icon :size="64"><icon-ep-location-information /></el-icon>
        </div>
        <h3>请选择监测点</h3>
        <p>从左侧树形导航中选择要查看的建筑、楼层或房间</p>
      </div>

      <!-- Trend Chart -->
      <div class="trend-section" v-if="selectedNode">
        <div class="section-header">
          <h3 class="section-title">
            <span class="title-icon"><icon-ep-data-line /></span>
            数据趋势
          </h3>
          <div class="time-range-tabs">
            <button
              v-for="range in timeRanges"
              :key="range.value"
              :class="['range-tab', { active: activeTimeRange === range.value }]"
              @click="handleTimeRangeChange(range.value)"
            >
              {{ range.label }}
            </button>
          </div>
        </div>
        <div class="chart-container-wrapper">
          <div ref="trendChartRef" class="trend-chart"></div>
        </div>
      </div>

      <!-- Device List for Selected Location -->
      <div class="devices-section" v-if="selectedNode && selectedNode.type !== 'campus'">
        <div class="section-header">
          <h3 class="section-title">
            <span class="title-icon"><icon-ep-cpu /></span>
            关联设备
          </h3>
        </div>
        <div class="devices-grid">
          <div
            v-for="device in locationDevices"
            :key="device.id"
            class="device-card"
            @click="viewDeviceDetail(device)"
          >
            <div class="device-status" :class="device.status"></div>
            <div class="device-icon" :style="{ background: `${device.color}15`, color: device.color }">
              <el-icon><component :is="device.icon" /></el-icon>
            </div>
            <div class="device-info">
              <div class="device-name">{{ device.name }}</div>
              <div class="device-type">{{ device.type }}</div>
            </div>
            <div class="device-value">
              <span class="value-text">{{ device.value }}</span>
              <span class="value-unit">{{ device.unit }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getBuildingTree } from '@/api/building'
import { getLatestEnergyData } from '@/api/energy'
import { getTrendData } from '@/api/analysis'
import { getDevices } from '@/api/device'

// Tree ref
const treeRef = ref(null)

// Chart refs
const trendChartRef = ref(null)
const trendChart = shallowRef(null)

// Search and tree state
const searchQuery = ref('')
const buildingTree = ref([])
const selectedNode = ref(null)

// Tree configuration
const treeProps = {
  children: 'children',
  label: 'name',
  value: 'id',
}

// Breadcrumb path
const breadcrumbPath = computed(() => {
  if (!selectedNode.value) return []

  const path = []
  let current = selectedNode.value
  while (current) {
    path.unshift(current.name)
    current = current.parent
  }
  return path
})

// Time range options
const timeRanges = [
  { label: '今日', value: 'today' },
  { label: '近7天', value: 'week' },
  { label: '近30天', value: 'month' },
]

const activeTimeRange = ref('today')

// Data cards for real-time metrics
const dataCards = ref([
  {
    label: '实时功率',
    value: 2458,
    unit: 'kW',
    change: '+3.2%',
    trend: 'up',
    color: '#f97316',
    live: true,
    displayValue: '2,458',
    sparkline: [5, 8, 12, 10, 15, 13, 18, 14, 16, 12],
  },
  {
    label: '今日用电',
    value: 18542,
    unit: 'kWh',
    change: '+5.8%',
    trend: 'up',
    color: '#eab308',
    live: false,
    displayValue: '18,542',
    sparkline: [8, 10, 8, 12, 14, 10, 8, 12, 15, 12],
  },
  {
    label: '今日用水',
    value: 125,
    unit: 'm³',
    change: '-2.1%',
    trend: 'down',
    color: '#3b82f6',
    live: false,
    displayValue: '125',
    sparkline: [12, 10, 14, 8, 10, 12, 10, 8, 10, 8],
  },
  {
    label: '今日用气',
    value: 42,
    unit: 'm³',
    change: '+1.5%',
    trend: 'up',
    color: '#ef4444',
    live: false,
    displayValue: '42',
    sparkline: [6, 8, 6, 10, 8, 6, 8, 6, 8, 6],
  },
])

// Devices at selected location
const locationDevices = ref([])

// Filter tree nodes
function filterNode(value, data) {
  if (!value) return true
  return data.name.toLowerCase().includes(value.toLowerCase())
}

// Watch search query
watch(searchQuery, (val) => {
  treeRef.value?.filter(val)
})

// Handle node click
function handleNodeClick(data) {
  selectedNode.value = data
  loadLocationData(data)
}

// Load data for selected location
async function loadLocationData(node) {
  try {
    const roomIds = collectRoomIds(node)
    const devices = await loadDevicesByNode(node, roomIds)
    const latestItems = await loadLatestDataByNode(node, roomIds)

    locationDevices.value = devices.map(device => ({
        id: device.id,
        name: device.name,
        type: device.energy_type_detail?.name || device.energy_type || '--',
        value: device.latest_data?.value || '--',
        unit: device.energy_type_detail?.unit || '',
        status: device.status?.toLowerCase() || 'offline',
        color: getEnergyColor(device.energy_type_detail?.code || device.energy_type),
        icon: getEnergyIcon(device.energy_type_detail?.code || device.energy_type),
      }))

    updateDataCards(latestItems)

    // Update trend chart
    await updateTrendChart(node)
  } catch (error) {
    console.error('Failed to load location data:', error)
    ElMessage.warning('部分数据加载失败，已保留最近一次有效卡片数据')
    updateTrendChart(node)
  }
}

function collectRoomIds(node) {
  if (!node) return []
  if (node.type === 'room') return [node.id]

  const roomIds = []
  const stack = [node]
  while (stack.length) {
    const current = stack.pop()
    if (current.type === 'room') {
      roomIds.push(current.id)
      continue
    }
    if (Array.isArray(current.children)) {
      current.children.forEach(child => stack.push(child))
    }
  }
  return roomIds
}

async function loadDevicesByNode(node, roomIds) {
  if (node.type === 'room') {
    const response = await getDevices({ room_id: node.id })
    return response.code === 0 ? normalizeListData(response.data) : []
  }

  if (roomIds.length === 0) return []

  const responseList = await Promise.allSettled(roomIds.map(roomId => getDevices({ room_id: roomId })))
  const deviceMap = new Map()
  responseList.forEach((result) => {
    if (result.status !== 'fulfilled') return
    const response = result.value
    if (response.code !== 0) return
    normalizeListData(response.data).forEach((device) => {
      deviceMap.set(device.id, device)
    })
  })
  return Array.from(deviceMap.values())
}

async function loadLatestDataByNode(node, roomIds) {
  if (node.type === 'room') {
    const response = await getLatestEnergyData({ room_id: node.id })
    return response.code === 0 ? normalizeListData(response.data) : []
  }

  if (roomIds.length === 0) return []

  const responseList = await Promise.allSettled(roomIds.map(roomId => getLatestEnergyData({ room_id: roomId })))
  const latestItems = []
  responseList.forEach((result) => {
    if (result.status !== 'fulfilled') return
    const response = result.value
    if (response.code !== 0) return
    latestItems.push(...normalizeListData(response.data))
  })
  return latestItems
}

function normalizeListData(data) {
  if (Array.isArray(data)) return data
  if (data && Array.isArray(data.results)) return data.results
  return []
}

function updateDataCards(latestItems) {
  const previous = new Map(dataCards.value.map(card => [card.label, card.value]))

  const totals = {
    power: 0,
    electricity: 0,
    water: 0,
    gas: 0,
  }

  latestItems.forEach((item) => {
    const energyType = String(item.energy_type || '').toUpperCase()
    const value = Number(item.value) || 0
    const power = Number(item.power) || 0

    totals.power += power
    if (energyType === 'ELECTRICITY') totals.electricity += value
    if (energyType === 'WATER') totals.water += value
    if (energyType === 'GAS') totals.gas += value
  })

  dataCards.value = [
    createDataCard('实时功率', totals.power, 'kW', '#f97316', true, previous.get('实时功率')),
    createDataCard('今日用电', totals.electricity, 'kWh', '#eab308', false, previous.get('今日用电')),
    createDataCard('今日用水', totals.water, 'm³', '#3b82f6', false, previous.get('今日用水')),
    createDataCard('今日用气', totals.gas, 'm³', '#ef4444', false, previous.get('今日用气')),
  ]
}

function createDataCard(label, value, unit, color, live, previousValue) {
  const numericValue = Number.isFinite(value) ? value : 0
  const diff = Number.isFinite(previousValue) ? numericValue - previousValue : 0
  const base = previousValue && previousValue !== 0 ? previousValue : 1
  const ratio = (diff / base) * 100
  const absRatio = Math.abs(ratio)

  return {
    label,
    value: numericValue,
    unit,
    change: `${ratio >= 0 ? '+' : '-'}${absRatio.toFixed(1)}%`,
    trend: diff >= 0 ? 'up' : 'down',
    color,
    live,
    displayValue: numericValue.toLocaleString('zh-CN', { maximumFractionDigits: 2 }),
    sparkline: buildSparkline(numericValue),
  }
}

function buildSparkline(baseValue) {
  const safeBase = Number.isFinite(baseValue) ? baseValue : 0
  return Array.from({ length: 10 }, (_, i) => {
    const wave = Math.sin(i * 0.9) * 4 + Math.cos(i * 0.5) * 2
    const value = 8 + wave + (safeBase > 0 ? Math.min(safeBase / 200, 8) : 0)
    return Math.max(2, Math.min(20, Number(value.toFixed(1))))
  })
}

// Get energy type color
function getEnergyColor(type) {
  const colors = {
    'ELECTRICITY': '#eab308',
    'WATER': '#3b82f6',
    'GAS': '#ef4444',
  }
  return colors[type] || '#64748b'
}

// Get energy type icon
function getEnergyIcon(type) {
  const icons = {
    'ELECTRICITY': 'icon-ep-lightning',
    'WATER': 'icon-ep-circle',
    'GAS': 'icon-ep-cpu',
  }
  return icons[type] || 'icon-ep-cpu'
}

// Update trend chart
async function updateTrendChart(node) {
  await nextTick()

  if (!trendChartRef.value) return
  if (!trendChart.value) initTrendChart()
  if (!trendChart.value) return

  // Generate mock trend data based on time range
  const chartData = generateTrendData(activeTimeRange.value)

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
    xAxis: {
      type: 'category',
      data: chartData.categories,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#64748b', fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#64748b', fontSize: 11 },
      splitLine: { lineStyle: { color: '#f1f5f9', type: 'dashed' } },
    },
    series: [
      {
        name: '电',
        type: 'line',
        smooth: true,
        data: chartData.electricity,
        lineStyle: { width: 3, color: '#eab308' },
        itemStyle: { color: '#eab308', borderWidth: 2 },
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
        data: chartData.water,
        lineStyle: { width: 3, color: '#3b82f6' },
        itemStyle: { color: '#3b82f6', borderWidth: 2 },
      },
    ],
    legend: {
      bottom: 0,
      textStyle: { color: '#64748b', fontSize: 12 },
    },
  }

  trendChart.value.setOption(option, true)
}

// Generate trend data based on time range
function generateTrendData(range) {
  let categories = []
  const electricity = []
  const water = []

  if (range === 'today') {
    // Hourly data for today
    for (let i = 0; i < 24; i++) {
      categories.push(`${i}:00`)
      electricity.push(Math.floor(100 + Math.random() * 200))
      water.push(Math.floor(20 + Math.random() * 50))
    }
  } else if (range === 'week') {
    // Daily data for 7 days
    const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    categories = days
    days.forEach(() => {
      electricity.push(Math.floor(2000 + Math.random() * 1500))
      water.push(Math.floor(400 + Math.random() * 300))
    })
  } else {
    // Daily data for 30 days
    for (let i = 1; i <= 30; i++) {
      categories.push(`${i}日`)
      electricity.push(Math.floor(2000 + Math.random() * 1500))
      water.push(Math.floor(400 + Math.random() * 300))
    }
  }

  return { categories, electricity, water }
}

// Initialize trend chart
function initTrendChart() {
  if (!trendChartRef.value) return

  if (trendChart.value) {
    trendChart.value.dispose()
  }

  trendChart.value = echarts.init(trendChartRef.value)
}

// Handle time range change
function handleTimeRangeChange(range) {
  activeTimeRange.value = range
  if (selectedNode.value) {
    updateTrendChart(selectedNode.value)
  }
}

// Refresh data
function refreshData() {
  if (selectedNode.value) {
    loadLocationData(selectedNode.value)
    ElMessage.success('数据已刷新')
  }
}

// View device detail
function viewDeviceDetail(device) {
  ElMessage.info(`查看设备: ${device.name}`)
  // Navigate to device detail or show modal
}

// Handle window resize
function handleResize() {
  trendChart.value?.resize()
}

// Load building tree
async function loadBuildingTree() {
  try {
    const response = await getBuildingTree()
    if (response.code === 0 && response.data) {
      buildingTree.value = buildTreeStructure(response.data)
    }
  } catch (error) {
    console.error('Failed to load building tree:', error)
    // Use mock data
    buildingTree.value = [
      {
        id: 1,
        name: '主校区',
        type: 'campus',
        deviceCount: 142,
        children: [
          {
            id: 11,
            name: '教学楼A',
            type: 'building',
            deviceCount: 48,
            children: [
              { id: 111, name: '1层', type: 'floor', deviceCount: 16, children: [
                { id: 1111, name: '101室', type: 'room', deviceCount: 4 },
                { id: 1112, name: '102室', type: 'room', deviceCount: 4 },
              ]},
              { id: 112, name: '2层', type: 'floor', deviceCount: 16 },
              { id: 113, name: '3层', type: 'floor', deviceCount: 16 },
            ],
          },
          {
            id: 12,
            name: '实验楼',
            type: 'building',
            deviceCount: 35,
            children: [
              { id: 121, name: '1层', type: 'floor', deviceCount: 18 },
              { id: 122, name: '2层', type: 'floor', deviceCount: 17 },
            ],
          },
          {
            id: 13,
            name: '图书馆',
            type: 'building',
            deviceCount: 28,
            children: [
              { id: 131, name: '1层', type: 'floor', deviceCount: 14 },
              { id: 132, name: '2层', type: 'floor', deviceCount: 14 },
            ],
          },
        ],
      },
    ]
  }
}

// Build tree structure with type info
function buildTreeStructure(data) {
  const campusList = normalizeListData(data)
  return campusList.map((campus) => ({
    id: campus.id,
    name: campus.name,
    type: 'campus',
    children: normalizeListData(campus.buildings).map((building) => ({
      id: building.id,
      name: building.name,
      type: 'building',
      children: normalizeListData(building.floors).map((floor) => ({
        id: floor.id,
        name: floor.name || `${floor.floor_number || ''}层`,
        type: 'floor',
        children: normalizeListData(floor.rooms).map((room) => ({
          id: room.id,
          name: room.room_number,
          type: 'room',
        })),
      })),
    })),
  }))
}

// Auto refresh timer
let refreshTimer = null

// Setup auto refresh
function setupAutoRefresh() {
  refreshTimer = setInterval(() => {
    if (selectedNode.value) {
      // Update live data cards
      dataCards.value.forEach(card => {
        if (card.live) {
          card.value = Math.floor(card.value * (0.95 + Math.random() * 0.1))
          card.displayValue = card.value.toLocaleString()
        }
      })
    }
  }, 10000) // 10 seconds for live data
}

// Lifecycle
onMounted(async () => {
  await nextTick()

  // Load building tree
  await loadBuildingTree()

  // Initialize chart
  initTrendChart()

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

  // Dispose chart
  trendChart.value?.dispose()

  // Remove event listener
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.monitoring-container {
  display: flex;
  gap: 16px;
  height: calc(100vh - 140px);
}

/* ========================================
   TREE SIDEBAR
   ======================================== */
.tree-sidebar {
  width: 280px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px;
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

.search-box {
  width: 100%;
}

.tree-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.tree-content::-webkit-scrollbar {
  width: 6px;
}

.tree-content::-webkit-scrollbar-track {
  background: transparent;
}

.tree-content::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 3px;
}

.location-tree {
  background: transparent;
}

.location-tree :deep(.el-tree-node__content) {
  height: 40px;
  border-radius: 8px;
  padding-right: 8px;
  transition: all 0.2s ease;
}

.location-tree :deep(.el-tree-node__content:hover) {
  background: #fef3c7;
}

.location-tree :deep(.is-current > .el-tree-node__content) {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  font-weight: 500;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.node-icon {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.node-icon.icon-campus { color: #f97316; }
.node-icon.icon-building { color: #64748b; }
.node-icon.icon-floor { color: #94a3b8; }
.node-icon.icon-room { color: #cbd5e1; }

.node-label {
  flex: 1;
  font-size: 13px;
}

.node-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 18px;
  padding: 0 6px;
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
  font-size: 11px;
  font-weight: 600;
  border-radius: 9px;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #f1f5f9;
}

.tree-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #64748b;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-dot.dot-online { background: #22c55e; box-shadow: 0 0 6px rgba(34, 197, 94, 0.5); }
.legend-dot.dot-offline { background: #94a3b8; }
.legend-dot.dot-warning { background: #ef4444; }

/* ========================================
   CONTENT AREA
   ======================================== */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.content-area::-webkit-scrollbar {
  width: 8px;
}

.content-area::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.content-area::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

/* Selection Bar */
.selection-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.selection-breadcrumb {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.breadcrumb-item:first-child .el-icon {
  display: none;
}

/* Data Cards Grid */
.data-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.data-card {
  position: relative;
  height: 120px;
  background: linear-gradient(135deg, #fff 0%, #f8fafc 100%);
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: all 0.3s ease;
}

.data-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.12);
  border-color: #f97316;
}

.card-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.02) 1px, transparent 1px);
  background-size: 12px 12px;
}

.glow-effect {
  position: absolute;
  top: -30%;
  right: -20%;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  filter: blur(30px);
  opacity: 0.3;
}

.card-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding: 14px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-label {
  font-size: 12px;
  color: #64748b;
}

.card-unit {
  font-size: 11px;
  color: #94a3b8;
}

.card-value-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.card-value {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 22px;
  font-weight: 700;
  font-feature-settings: 'tnum';
}

.card-change {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 8px;
  font-weight: 500;
}

.card-change.up {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.card-change.down {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

.card-sparkline {
  height: 20px;
}

.sparkline-svg {
  width: 100%;
  height: 100%;
}

.live-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
}

.live-dot {
  display: block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #64748b;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
  color: #94a3b8;
}

/* Trend Section */
.trend-section {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.time-range-tabs {
  display: flex;
  background: #f8fafc;
  border-radius: 8px;
  padding: 2px;
}

.range-tab {
  padding: 6px 14px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.range-tab:hover {
  color: #1f2937;
}

.range-tab.active {
  background: #fff;
  color: #f97316;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-container-wrapper {
  flex: 1;
  min-height: 280px;
  padding: 12px;
}

.trend-chart {
  width: 100%;
  height: 100%;
}

/* Devices Section */
.devices-section {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.devices-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 16px;
}

.device-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.device-card:hover {
  background: #fff;
  border-color: #f97316;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

.device-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.device-status.online {
  background: #22c55e;
  box-shadow: 0 0 6px rgba(34, 197, 94, 0.5);
}

.device-status.offline {
  background: #94a3b8;
}

.device-status.fault {
  background: #ef4444;
}

.device-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  font-size: 18px;
}

.device-info {
  flex: 1;
  min-width: 0;
}

.device-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 2px;
}

.device-type {
  font-size: 11px;
  color: #64748b;
}

.device-value {
  text-align: right;
}

.value-text {
  display: block;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Orbitron', sans-serif;
  color: #1f2937;
}

.value-unit {
  font-size: 11px;
  color: #94a3b8;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .data-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .devices-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .monitoring-container {
    flex-direction: column;
    height: auto;
  }

  .tree-sidebar {
    width: 100%;
    max-height: 300px;
  }

  .data-cards-grid {
    grid-template-columns: 1fr;
  }

  .devices-grid {
    grid-template-columns: 1fr;
  }
}
</style>
