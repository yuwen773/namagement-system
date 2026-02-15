<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import {
  getRegionDistribution,
  getTypeDistribution,
  getTimeSeries
} from '@/api/visualization'
import { ElMessage } from 'element-plus'
import {
  MapLocation,
  PieChart,
  TrendCharts
} from '@element-plus/icons-vue'

// 当前激活的 Tab
const activeTab = ref('region')

// Tab 配置
const tabs = [
  { name: 'region', label: '地域分布', icon: MapLocation },
  { name: 'type', label: '类型偏好', icon: PieChart },
  { name: 'trend', label: '时间走势', icon: TrendCharts }
]

// Chart refs
const regionChartRef = ref(null)
const typeChartRef = ref(null)
const trendChartRef = ref(null)

// Chart instances
let regionChart = null
let typeChart = null
let trendChart = null

// 数据状态
const regionData = ref([])
const typeData = ref([])
const trendData = ref([])
const loading = ref({
  region: false,
  type: false,
  trend: false
})

// 数据加载状态跟踪
const dataLoaded = ref({
  region: false,
  type: false,
  trend: false
})

// 时间维度（用于走势图）
const timeRange = ref('week')
const timeRangeOptions = [
  { label: '最近7天', value: 'week' },
  { label: '最近30天', value: 'month' },
  { label: '全年', value: 'year' }
]

// ============ 地域分布图 ============
const loadRegionData = async () => {
  // 如果已经加载过，不再重复加载
  if (dataLoaded.value.region) {
    return
  }

  loading.value.region = true
  try {
    const res = await getRegionDistribution()
    regionData.value = res.data || []
    dataLoaded.value.region = true
    nextTick(() => initRegionChart())
  } catch (error) {
    console.error('加载地域数据失败:', error)
    ElMessage.error('加载地域数据失败')
  } finally {
    loading.value.region = false
  }
}

const initRegionChart = () => {
  if (!regionChartRef.value || regionData.value.length === 0) return

  if (regionChart) regionChart.dispose()
  regionChart = echarts.init(regionChartRef.value)

  const data = regionData.value.map(item => ({
    name: item.region_name || item.region || item.name || '未知',
    value: item.total_box_office || item.box_office || 0
  })).sort((a, b) => b.value - a.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(59, 130, 246, 0.3)',
      textStyle: { color: '#e2e8f0' },
      formatter: (params) => {
        const item = params[0]
        return `${item.name}<br/>票房: ${(item.value / 10000).toFixed(2)}万元`
      }
    },
    grid: {
      left: '5%',
      right: '15%',
      top: '5%',
      bottom: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.2)' } },
      axisLabel: { color: '#94a3b8', formatter: (v) => (v / 10000).toFixed(0) + '万' },
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(d => d.name),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#e2e8f0', fontSize: 13 }
    },
    series: [{
      type: 'bar',
      data: data.map(d => d.value),
      itemStyle: {
        borderRadius: [0, 8, 8, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#3b82f6' },
          { offset: 1, color: '#06b6d4' }
        ])
      },
      label: {
        show: true,
        position: 'right',
        color: '#e2e8f0',
        formatter: (params) => (params.value / 10000).toFixed(1) + '万'
      },
      barWidth: '60%'
    }]
  }

  regionChart.setOption(option)
}

// ============ 类型偏好图 ============
const loadTypeData = async () => {
  // 如果已经加载过，不再重复加载
  if (dataLoaded.value.type) {
    return
  }

  loading.value.type = true
  try {
    const res = await getTypeDistribution()
    typeData.value = res.data || []
    dataLoaded.value.type = true
    nextTick(() => initTypeChart())
  } catch (error) {
    console.error('加载类型数据失败:', error)
    ElMessage.error('加载类型数据失败')
  } finally {
    loading.value.type = false
  }
}

const initTypeChart = () => {
  if (!typeChartRef.value || typeData.value.length === 0) return

  if (typeChart) typeChart.dispose()
  typeChart = echarts.init(typeChartRef.value)

  const data = typeData.value.map(item => ({
    name: item.type_name || item.name || '未知',
    value: item.total_box_office || item.box_office || 0
  }))

  const colors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#6366f1']

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(59, 130, 246, 0.3)',
      textStyle: { color: '#e2e8f0' },
      formatter: (params) => `${params.name}<br/>票房: ${(params.value / 10000).toFixed(2)}万元<br/>占比: ${params.percent}%`
    },
    legend: {
      orient: 'vertical',
      right: 20,
      top: 'center',
      textStyle: { color: '#94a3b8', fontSize: 13 },
      itemGap: 16,
      icon: 'circle'
    },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['40%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#0f172a',
        borderWidth: 3
      },
      label: { show: false },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold',
          color: '#f8fafc',
          formatter: '{d}%'
        },
        itemStyle: {
          shadowBlur: 20,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      labelLine: { show: false },
      data: data.map((item, index) => ({
        ...item,
        itemStyle: {
          color: colors[index % colors.length]
        }
      }))
    }]
  }

  typeChart.setOption(option)
}

// ============ 时间走势图 ============
const loadTrendData = async () => {
  // 如果已经加载过，不再重复加载
  if (dataLoaded.value.trend) {
    return
  }

  loading.value.trend = true
  try {
    let params = {}
    if (timeRange.value === 'week') {
      params = { period: 'day', days: 7 }
    } else if (timeRange.value === 'month') {
      params = { period: 'day', days: 30 }
    } else if (timeRange.value === 'year') {
      params = { period: 'month', days: 365 }
    }

    const res = await getTimeSeries(params)
    trendData.value = res.data || []
    dataLoaded.value.trend = true
    nextTick(() => initTrendChart())
  } catch (error) {
    console.error('加载趋势数据失败:', error)
    ElMessage.error('加载趋势数据失败')
  } finally {
    loading.value.trend = false
  }
}

const initTrendChart = () => {
  if (!trendChartRef.value || trendData.value.length === 0) return

  if (trendChart) trendChart.dispose()
  trendChart = echarts.init(trendChartRef.value)

  const dates = trendData.value.map(item => item.date || item.date_str)
  const values = trendData.value.map(item => item.total_box_office || item.box_office || 0)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(59, 130, 246, 0.3)',
      textStyle: { color: '#e2e8f0' },
      formatter: (params) => {
        const item = params[0]
        return `${item.axisValue}<br/>票房: ${(item.value / 10000).toFixed(2)}万元`
      }
    },
    grid: {
      left: '5%',
      right: '5%',
      top: '10%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.2)' } },
      axisLabel: { color: '#94a3b8', rotate: dates.length > 7 ? 30 : 0 },
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#94a3b8', formatter: (v) => (v / 10000).toFixed(0) + '万' },
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } }
    },
    series: [{
      name: '票房',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      data: values,
      lineStyle: {
        color: '#3b82f6',
        width: 3
      },
      itemStyle: {
        color: '#3b82f6',
        borderColor: '#0f172a',
        borderWidth: 2
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(59, 130, 246, 0.4)' },
          { offset: 1, color: 'rgba(59, 130, 246, 0.02)' }
        ])
      }
    }]
  }

  trendChart.setOption(option)
}

// ============ 事件处理 ============
const handleTabChange = (tab) => {
  activeTab.value = tab
  nextTick(() => {
    // 懒加载：切换到某个 tab 时才加载该图表的数据
    if (tab === 'region' && !dataLoaded.value.region) {
      loadRegionData()
    } else if (tab === 'region' && regionData.value.length > 0) {
      initRegionChart()
    }

    if (tab === 'type' && !dataLoaded.value.type) {
      loadTypeData()
    } else if (tab === 'type' && typeData.value.length > 0) {
      initTypeChart()
    }

    if (tab === 'trend' && !dataLoaded.value.trend) {
      loadTrendData()
    } else if (tab === 'trend' && trendData.value.length > 0) {
      initTrendChart()
    }
  })
}

const handleTimeRangeChange = () => {
  // 时间范围改变时，重新加载趋势数据
  dataLoaded.value.trend = false  // 重置加载状态
  loadTrendData()
}

const handleResize = () => {
  regionChart?.resize()
  typeChart?.resize()
  trendChart?.resize()
}

// ============ 生命周期 ============
onMounted(() => {
  // 只加载默认激活的 tab，并在 DOM 渲染后执行
  nextTick(() => {
    loadRegionData()
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  regionChart?.dispose()
  typeChart?.dispose()
  trendChart?.dispose()
})

// 监听 Tab 变化重新渲染图表
watch(activeTab, (newTab) => {
  nextTick(() => {
    if (newTab === 'region') initRegionChart()
    if (newTab === 'type') initTypeChart()
    if (newTab === 'trend') initTrendChart()
  })
})
</script>

<template>
  <div class="page-container">
    <div class="content-wrapper">
      <!-- 页面标题 -->
      <div class="mb-6 animate-fade-in">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
            <PieChart class="w-6 h-6 text-white" />
          </div>
          <div class="flex-1">
            <h1 class="text-2xl font-bold text-white">可视化图表库</h1>
            <p class="text-slate-400 text-sm">多维度数据分析，深度挖掘票房洞察</p>
          </div>
        </div>
      </div>

      <!-- Tab 切换 -->
      <div class="glass-card rounded-2xl p-2 mb-6 animate-slide-up" style="animation-delay: 0.1s">
        <div class="flex gap-2">
          <button
            v-for="tab in tabs"
            :key="tab.name"
            @click="handleTabChange(tab.name)"
            class="tab-btn"
            :class="{ 'tab-active': activeTab === tab.name }"
          >
            <component :is="tab.icon" class="w-5 h-5 mr-2" />
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- 图表展示区域 -->
      <div class="animate-slide-up" style="animation-delay: 0.2s">
        <!-- 地域分布图 -->
        <div v-show="activeTab === 'region'" class="glass-card rounded-2xl border border-white/10 p-6">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
              <MapLocation class="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">地域票房分布</h3>
              <p class="text-sm text-slate-400">各省份票房贡献对比</p>
            </div>
          </div>

          <div v-if="loading.region" class="chart-loading">
            <div class="w-12 h-12 rounded-full border-2 border-blue-500/30 border-t-blue-500 animate-spin"></div>
            <p class="text-slate-400 mt-4">加载中...</p>
          </div>

          <div v-else-if="regionData.length === 0" class="chart-empty">
            <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
              <MapLocation class="w-8 h-8 text-slate-600" />
            </div>
            <p class="text-slate-500 mb-1">暂无地域数据</p>
          </div>

          <div v-else ref="regionChartRef" class="chart-container"></div>
        </div>

        <!-- 类型偏好图 -->
        <div v-show="activeTab === 'type'" class="glass-card rounded-2xl border border-white/10 p-6">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500/20 to-green-500/20 flex items-center justify-center">
              <PieChart class="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">影片类型占比</h3>
              <p class="text-sm text-slate-400">各类型市场份额分析</p>
            </div>
          </div>

          <div v-if="loading.type" class="chart-loading">
            <div class="w-12 h-12 rounded-full border-2 border-emerald-500/30 border-t-emerald-500 animate-spin"></div>
            <p class="text-slate-400 mt-4">加载中...</p>
          </div>

          <div v-else-if="typeData.length === 0" class="chart-empty">
            <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
              <PieChart class="w-8 h-8 text-slate-600" />
            </div>
            <p class="text-slate-500 mb-1">暂无类型数据</p>
          </div>

          <div v-else ref="typeChartRef" class="chart-container"></div>
        </div>

        <!-- 时间走势图 -->
        <div v-show="activeTab === 'trend'" class="glass-card rounded-2xl border border-white/10 p-6">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
                <TrendCharts class="w-5 h-5 text-violet-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">票房趋势分析</h3>
                <p class="text-sm text-slate-400">大盘票房变化曲线</p>
              </div>
            </div>

            <!-- 时间维度切换 -->
            <div class="flex items-center gap-2">
              <span class="text-sm text-slate-400">时间范围：</span>
              <el-select
                v-model="timeRange"
                @change="handleTimeRangeChange"
                class="time-select"
                style="width: 140px"
              >
                <el-option
                  v-for="opt in timeRangeOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </div>
          </div>

          <div v-if="loading.trend" class="chart-loading">
            <div class="w-12 h-12 rounded-full border-2 border-violet-500/30 border-t-violet-500 animate-spin"></div>
            <p class="text-slate-400 mt-4">加载中...</p>
          </div>

          <div v-else-if="trendData.length === 0" class="chart-empty">
            <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
              <TrendCharts class="w-8 h-8 text-slate-600" />
            </div>
            <p class="text-slate-500 mb-1">暂无趋势数据</p>
          </div>

          <div v-else ref="trendChartRef" class="chart-container-large"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Page Container
   ======================================== */
.page-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ========================================
   Animations
   ======================================== */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }
.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* ========================================
   Glass Card
   ======================================== */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  transition: all 0.3s ease;
}

.glass-card:hover {
  border-color: rgba(6, 182, 212, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ========================================
   Tab Buttons
   ======================================== */
.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #94a3b8;
  background: transparent;
  border: none;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
}

.tab-active {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  color: #fff;
  box-shadow: 0 4px 20px rgba(6, 182, 212, 0.4);
}

/* ========================================
   Chart Containers
   ======================================== */
.chart-container {
  height: 400px;
}

.chart-container-large {
  height: 450px;
}

.chart-loading,
.chart-empty {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* ========================================
   Select Styling
   ======================================== */
:deep(.time-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

:deep(.time-select .el-input__wrapper:hover) {
  border-color: rgba(6, 182, 212, 0.3);
}

:deep(.time-select .el-input__wrapper.is-focus) {
  border-color: #06b6d4;
  box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.2);
}

:deep(.time-select .el-input__inner) {
  color: #fff;
}

:deep(.time-select .el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

/* ========================================
   Responsive Design
   ======================================== */
@media (max-width: 768px) {
  .page-container {
    padding: 1rem;
  }
}
</style>
