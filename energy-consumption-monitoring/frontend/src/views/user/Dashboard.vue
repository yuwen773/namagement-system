<template>
  <div class="user-dashboard">
    <!-- Welcome Section -->
    <div class="welcome-banner">
      <div class="banner-content">
        <div class="banner-greeting">
          <h1 class="greeting-text">{{ greetingText }}</h1>
          <p class="greeting-sub">今天也要节约能源哦 💡</p>
        </div>
        <div class="banner-decoration">
          <div class="decoration-circle circle-1"></div>
          <div class="decoration-circle circle-2"></div>
          <div class="decoration-circle circle-3"></div>
        </div>
      </div>
    </div>

    <!-- Top Metric Cards -->
    <div class="metrics-grid">
      <div v-for="(metric, index) in metrics" :key="index" class="metric-card" :class="`metric-${metric.type}`">
        <div class="metric-bg">
          <div class="grid-pattern"></div>
        </div>
        <div class="metric-header">
          <div class="metric-icon" :style="{ background: `${metric.color}15`, color: metric.color }">
            <component :is="metric.icon" />
          </div>
          <span class="metric-label">{{ metric.label }}</span>
        </div>
        <div class="metric-value-section">
          <span class="metric-value">{{ metric.value }}</span>
          <span class="metric-unit">{{ metric.unit }}</span>
        </div>
        <div v-if="metric.trend" class="metric-trend" :class="metric.trendClass">
          <el-icon><icon-ep-caret-top v-if="metric.trendClass === 'up'" /><icon-ep-caret-bottom v-else /></el-icon>
          <span>{{ metric.trend }}</span>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <!-- Weekly Trend Chart -->
      <div class="chart-card trend-card">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-trend-charts /></span>
            本周用能趋势
          </h3>
          <div class="period-selector">
            <button
              v-for="period in periods"
              :key="period.key"
              :class="['period-btn', { active: activePeriod === period.key }]"
              @click="changePeriod(period.key)"
            >
              {{ period.label }}
            </button>
          </div>
        </div>
        <div class="card-body">
          <div ref="trendChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- Energy Composition Pie -->
      <div class="chart-card composition-card">
        <div class="card-header">
          <h3 class="card-title">
            <span class="title-icon"><icon-ep-pie-chart /></span>
            用能构成
          </h3>
        </div>
        <div class="card-body">
          <div ref="compositionChartRef" class="chart-container"></div>
          <div class="composition-legend">
            <div v-for="(item, index) in compositionData" :key="index" class="legend-item">
              <span class="legend-dot" :style="{ background: item.color }"></span>
              <span class="legend-label">{{ item.name }}</span>
              <span class="legend-value">{{ item.percent }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Section -->
    <div class="bottom-section">
      <!-- Energy Saving Tips -->
      <div class="tips-card">
        <div class="tips-header">
          <h3 class="tips-title">
            <span class="tips-icon">🌱</span>
            节能小贴士
          </h3>
          <el-button text type="primary" @click="refreshTips">
            <el-icon><icon-ep-refresh /></el-icon>
            换一批
          </el-button>
        </div>
        <div class="tips-list">
          <div v-for="(tip, index) in tips" :key="index" class="tip-item">
            <div class="tip-icon" :class="`tip-${index + 1}`">
              <el-icon><icon-ep-opportunity /></el-icon>
            </div>
            <div class="tip-content">
              <h4 class="tip-title">{{ tip.title }}</h4>
              <p class="tip-text">{{ tip.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Latest Notices -->
      <div class="notices-card">
        <div class="notices-header">
          <h3 class="notices-title">
            <span class="notices-icon"><icon-ep-bell /></span>
            最新公告
          </h3>
          <el-button text type="primary" @click="$router.push('/user/notices')">
            查看全部 <el-icon><icon-ep-arrow-right /></el-icon>
          </el-button>
        </div>
        <div class="notices-list">
          <div
            v-for="notice in latestNotices"
            :key="notice.id"
            class="notice-item"
            @click="$router.push('/user/notices')"
          >
            <div class="notice-badge" :class="`badge-${notice.type}`">
              {{ notice.typeLabel }}
            </div>
            <div class="notice-content">
              <h4 class="notice-title">{{ notice.title }}</h4>
              <p class="notice-preview">{{ notice.preview }}</p>
              <span class="notice-time">{{ notice.time }}</span>
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
import { getTrendData, getDistributionData } from '@/api/analysis'
import { getMyBills, getNotices, getTips } from '@/api/system'

// Chart refs using shallowRef to avoid deep reactivity
const trendChartRef = ref(null)
const compositionChartRef = ref(null)

// Chart instances
const trendChart = shallowRef(null)
const compositionChart = shallowRef(null)

// Period selector
const periods = [
  { key: 'day', label: '本周' },
  { key: 'month', label: '本月' },
  { key: 'year', label: '本年' },
]
const activePeriod = ref('day')

// Metrics data - 从API获取
const metrics = ref([
  {
    type: 'room',
    label: '当前房间',
    value: '-',
    unit: '',
    icon: 'icon-ep-house',
    color: '#f97316',
  },
  {
    type: 'electricity',
    label: '今日用电',
    value: '-',
    unit: 'kWh',
    trend: '',
    trendClass: 'down',
    icon: 'icon-ep-lightning',
    color: '#eab308',
  },
  {
    type: 'water',
    label: '今日用水',
    value: '-',
    unit: 'm³',
    trend: '',
    trendClass: 'down',
    icon: 'icon-ep-circle',
    color: '#3b82f6',
  },
  {
    type: 'cost',
    label: '本月费用',
    value: '-',
    unit: '元',
    trend: '',
    trendClass: 'up',
    icon: 'icon-ep-wallet',
    color: '#22c55e',
  },
])

// Composition data - 从API获取
const compositionData = ref([])

// Tips data - 从API获取
const tips = ref([])

// Latest notices - 从API获取
const latestNotices = ref([])

// Greeting text based on time
const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  if (hour < 22) return '晚上好'
  return '晚安'
})

// ECharts colors
const chartColors = {
  primary: '#f97316',
  secondary: '#eab308',
  water: '#3b82f6',
  gas: '#ef4444',
  green: '#22c55e',
  text: '#64748b',
  grid: '#e2e8f0',
  areaStart: 'rgba(249, 115, 22, 0.3)',
  areaEnd: 'rgba(249, 115, 22, 0)',
}

// Initialize trend chart
function initTrendChart() {
  if (!trendChartRef.value) return

  trendChart.value = echarts.init(trendChartRef.value)

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
        name: '用能',
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
    ],
  }

  trendChart.value.setOption(option)
}

// Initialize composition chart
function initCompositionChart() {
  if (!compositionChartRef.value) return

  compositionChart.value = echarts.init(compositionChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      formatter: '{b}: {c}% ({d}%)',
    },
    series: [
      {
        type: 'pie',
        radius: ['50%', '75%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
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

  compositionChart.value.setOption(option)
}

// Load trend data
async function loadTrendData() {
  try {
    const response = await getTrendData({ period: activePeriod.value })
    if (response.code === 0 && response.data) {
      // Update chart with real data
      if (trendChart.value && response.data.series) {
        const option = trendChart.value.getOption()
        // Format series data for chart
        const labels = response.data.series.map(s => s.period)
        const values = response.data.series.map(s => s.total_value || 0)
        option.xAxis.data = labels
        option.series = [{
          name: '用能',
          type: 'line',
          data: values,
          smooth: true,
        }]
        trendChart.value.setOption(option)

        // Update today's metrics from series data (latest period data)
        if (response.data.series.length > 0) {
          const latestData = response.data.series[response.data.series.length - 1]
          if (latestData && latestData.total_value) {
            // Show total value as approximate electricity
            metrics.value[1].value = (latestData.total_value * 0.7).toFixed(1)
            metrics.value[2].value = (latestData.total_value * 0.1).toFixed(1)
          }
        }
      }
    }
  } catch (error) {
    console.error('Failed to load trend data:', error)
  }
}

// Load composition data
async function loadCompositionData() {
  try {
    const response = await getDistributionData({ type: 'energy_type' })
    if (response.code === 0 && response.data && response.data.items) {
      const items = response.data.items
      // Calculate total for percentage
      const total = items.reduce((sum, item) => sum + item.value, 0)
      compositionData.value = items.map(item => ({
        ...item,
        percent: total > 0 ? Math.round((item.value / total) * 100) : 0,
      }))
      // Update chart
      if (compositionChart.value) {
        const option = compositionChart.value.getOption()
        if (option && option.series && option.series[0]) {
          option.series[0].data = items.map(item => ({
            value: item.value,
            name: item.label || item.name,
          }))
          compositionChart.value.setOption(option)
        }
      }
    }
  } catch (error) {
    console.error('Failed to load composition data:', error)
  }
}

// Load bills data
async function loadBillsData() {
  try {
    const response = await getMyBills()
    if (response.code === 0 && response.data) {
      const currentMonthBills = response.data.filter(b => {
        const billDate = new Date(bill.bill_period)
        const now = new Date()
        return billDate.getMonth() === now.getMonth() && billDate.getFullYear() === now.getFullYear()
      })

      if (currentMonthBills.length > 0) {
        const totalCost = currentMonthBills.reduce((sum, b) => sum + (b.amount || 0), 0)
        metrics.value[3].value = totalCost.toFixed(2)
      }
    }
  } catch (error) {
    console.error('Failed to load bills:', error)
  }
}

// Load notices
async function loadNotices() {
  try {
    const response = await getNotices({ limit: 3 })
    if (response.code === 0 && response.data) {
      latestNotices.value = response.data.map(notice => ({
        id: notice.id,
        type: notice.priority === 'high' ? 'urgent' : notice.notice_type === 'TIP' ? 'tip' : 'info',
        typeLabel: notice.priority === 'high' ? '紧急' : notice.notice_type === 'TIP' ? '贴士' : '通知',
        title: notice.title,
        preview: notice.content?.substring(0, 30) + '...' || '',
        time: formatTime(notice.publish_time),
      }))
    }
  } catch (error) {
    console.error('Failed to load notices:', error)
  }
}

// Load tips from API
async function loadTips() {
  try {
    const response = await getTips({ limit: 10 })
    if (response.code === 0 && response.data) {
      tips.value = response.data.map(tip => ({
        title: tip.title,
        content: tip.content,
      }))
    }
  } catch (error) {
    console.error('Failed to load tips:', error)
  }
}

function formatTime(timeStr) {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)

  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  return `${Math.floor(diff / 1440)}天前`
}

// Change period
function changePeriod(period) {
  activePeriod.value = period
  loadTrendData()
}

// Refresh tips
function refreshTips() {
  const allTips = [
    {
      title: '随手关灯',
      content: '离开房间时记得关闭不必要的灯具，每节约1度电相当于减少0.8公斤碳排放。',
    },
    {
      title: '合理使用空调',
      content: '夏季空调温度设置在26℃最节能，每调高1℃可节约约6%的电力消耗。',
    },
    {
      title: '及时关闭水龙头',
      content: '洗手刷牙时及时关闭水龙头，一个漏水的龙头一天可浪费数十升水。',
    },
    {
      title: '冰箱节能',
      content: '冰箱内部食物不要塞得太满，保持冷空气流通，定期清理霜层可省电30%。',
    },
    {
      title: '电视节能',
      content: '电视亮度不要开得太亮，音量适中，不看电视时记得关闭电源而非待机。',
    },
    {
      title: '洗衣节能',
      content: ' accumulated足够的衣物再使用洗衣机，使用温水而非热水洗涤可节省大量电能。',
    },
  ]

  // Shuffle and pick 3
  tips.value = allTips.sort(() => Math.random() - 0.5).slice(0, 3)
  ElMessage.success('已更新节能小贴士')
}

// Handle window resize
function handleResize() {
  trendChart.value?.resize()
  compositionChart.value?.resize()
}

// Lifecycle
onMounted(async () => {
  // Wait for DOM to be ready
  await nextTick()
  await new Promise(resolve => setTimeout(resolve, 100))

  // Initialize charts
  initTrendChart()
  initCompositionChart()

  // Load data
  loadTrendData()
  loadCompositionData()
  loadBillsData()
  loadNotices()
  loadTips()

  // Handle resize
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // Dispose charts
  trendChart.value?.dispose()
  compositionChart.value?.dispose()

  // Remove event listener
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Orbitron:wght@400;500;600;700&display=swap');

.user-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========================================
   WELCOME BANNER
   ======================================== */
.welcome-banner {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #dc2626 100%);
  border-radius: 20px;
  padding: 32px 40px;
  color: white;
  box-shadow: 0 20px 40px rgba(249, 115, 22, 0.25);
}

.banner-content {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.banner-greeting .greeting-text {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

.banner-greeting .greeting-sub {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.banner-decoration {
  position: absolute;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 16px;
}

.decoration-circle {
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.circle-1 {
  width: 80px;
  height: 80px;
  animation: float 3s ease-in-out infinite;
}

.circle-2 {
  width: 50px;
  height: 50px;
  animation: float 3s ease-in-out infinite 0.5s;
}

.circle-3 {
  width: 30px;
  height: 30px;
  animation: float 3s ease-in-out infinite 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* ========================================
   METRICS GRID
   ======================================== */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.metric-card {
  position: relative;
  background: linear-gradient(135deg, #fff 0%, #fefefc 100%);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(249, 115, 22, 0.1);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(249, 115, 22, 0.15);
  border-color: rgba(249, 115, 22, 0.3);
}

.metric-bg {
  position: absolute;
  inset: 0;
  opacity: 0.5;
}

.grid-pattern {
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 16px 16px;
}

.metric-header {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  font-size: 18px;
}

.metric-label {
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
}

.metric-value-section {
  position: relative;
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 8px;
}

.metric-value {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.metric-unit {
  font-size: 14px;
  color: #9ca3af;
}

.metric-trend {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.metric-trend.up {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.metric-trend.down {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

/* ========================================
   CHARTS SECTION
   ======================================== */
.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
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

.period-selector {
  display: flex;
  background: #f8fafc;
  border-radius: 8px;
  padding: 2px;
}

.period-btn {
  padding: 6px 14px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-btn:hover {
  color: #1f2937;
}

.period-btn.active {
  background: white;
  color: #f97316;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.card-body {
  flex: 1;
  position: relative;
  padding: 16px 20px;
  min-height: 280px;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 250px;
}

.composition-legend {
  position: absolute;
  bottom: 16px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-label {
  color: #64748b;
  flex: 1;
}

.legend-value {
  font-weight: 600;
  color: #1f2937;
}

/* ========================================
   BOTTOM SECTION
   ======================================== */
.bottom-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* Tips Card */
.tips-card {
  background: linear-gradient(135deg, #f0fdf4 0%, #fff 100%);
  border-radius: 16px;
  border: 1px solid rgba(34, 197, 94, 0.2);
  padding: 20px;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.08);
}

.tips-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.tips-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.tips-icon {
  font-size: 20px;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  gap: 12px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  border: 1px solid rgba(34, 197, 94, 0.1);
  transition: all 0.3s ease;
}

.tip-item:hover {
  background: white;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.1);
  transform: translateX(4px);
}

.tip-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  color: white;
  font-size: 16px;
}

.tip-1 { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); }
.tip-2 { background: linear-gradient(135deg, #34d399 0%, #10b981 100%); }
.tip-3 { background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%); }

.tip-content {
  flex: 1;
}

.tip-title {
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.tip-text {
  margin: 0;
  font-size: 12px;
  color: #64748b;
  line-height: 1.6;
}

/* Notices Card */
.notices-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  padding: 20px;
}

.notices-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.notices-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.notices-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 18px;
}

.notices-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.notice-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.notice-item:hover {
  background: white;
  border-color: #f97316;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

.notice-badge {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
}

.badge-urgent {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.badge-info {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.badge-tip {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.notice-content {
  flex: 1;
  min-width: 0;
}

.notice-title {
  margin: 0 0 2px;
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.notice-preview {
  margin: 0 0 4px;
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notice-time {
  font-size: 11px;
  color: #9ca3af;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .bottom-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .welcome-banner {
    padding: 24px;
  }

  .banner-greeting .greeting-text {
    font-size: 24px;
  }

  .banner-decoration {
    display: none;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .metric-value {
    font-size: 24px;
  }

  .card-body {
    padding: 12px;
  }

  .chart-container {
    min-height: 200px;
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
