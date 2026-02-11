<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  TrendCharts,
  DataAnalysis,
  InfoFilled,
  Film,
  Calendar,
  Search,
  ArrowUp,
  ArrowDown,
  Minus
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getMovies } from '@/api/movie'
import { getMoviePrediction, getMovieHistory, getAlgorithmInfo } from '@/api/prediction'

// 加载状态
const loading = ref(false)
const chartLoading = ref(false)
const movieLoading = ref(false)

// 图表实例
let chartInstance = null
const chartRef = ref(null)

// 查询参数
const queryParams = reactive({
  movieId: null,
  algorithm: 'combined',
  predictDays: 7,
  historyDays: 30
})

// 电影选项
const movieOptions = ref([])

// 算法选项
const algorithmOptions = [
  { label: '综合预测', value: 'combined', desc: '同时返回线性回归和移动平均预测' },
  { label: '线性回归', value: 'linear_regression', desc: '使用最小二乘法拟合趋势' },
  { label: '移动平均', value: 'moving_average', desc: '基于历史数据加权平均' }
]

// 预测天数选项
const predictDaysOptions = [7, 14, 30]

// 统计数据
const stats = ref({
  avgDailyBoxOffice: '--',
  trendDirection: 'stable',
  trendPercent: '0',
  totalPredicted: '--'
})

// 算法信息
const algorithms = ref([])

// 预测数据
const predictionData = ref(null)

// 历史数据
const historyData = ref([])

// 趋势判断
const trendInfo = computed(() => {
  if (stats.value.trendDirection === 'up') {
    return { icon: ArrowUp, text: '上升趋势', color: 'text-emerald-400' }
  } else if (stats.value.trendDirection === 'down') {
    return { icon: ArrowDown, text: '下降趋势', color: 'text-red-400' }
  }
  return { icon: Minus, text: '平稳趋势', color: 'text-amber-400' }
})

// 当前算法信息
const currentAlgorithmInfo = computed(() => {
  return algorithms.value.find(a => a.id === queryParams.algorithm) || algorithms.value[0]
})

// 加载电影选项
const loadMovieOptions = async () => {
  movieLoading.value = true
  try {
    const res = await getMovies({ pageSize: 1000 })
    movieOptions.value = (res.data || []).map(m => ({
      label: m.title,
      value: m.id
    }))
  } catch (error) {
    console.error('加载电影失败:', error)
  } finally {
    movieLoading.value = false
  }
}

// 加载算法信息
const loadAlgorithmInfo = async () => {
  try {
    const res = await getAlgorithmInfo()
    algorithms.value = res.data || []
  } catch (error) {
    console.error('加载算法信息失败:', error)
  }
}

// 执行预测
const handleExecutePrediction = async () => {
  if (!queryParams.movieId) {
    ElMessage.warning('请选择要预测的影片')
    return
  }

  chartLoading.value = true
  try {
    // 获取预测数据
    const predictionRes = await getMoviePrediction(queryParams.movieId, {
      predictDays: queryParams.predictDays,
      algorithm: queryParams.algorithm
    })

    // 获取历史数据
    const historyRes = await getMovieHistory(queryParams.movieId, queryParams.historyDays)

    predictionData.value = predictionRes.data
    historyData.value = historyRes.data?.history || []

    // 计算统计数据
    calculateStats()

    // 渲染图表
    renderChart()

    ElMessage.success('预测执行成功')
  } catch (error) {
    console.error('预测失败:', error)
    ElMessage.error('预测执行失败: ' + (error.response?.data?.message || error.message))
  } finally {
    chartLoading.value = false
  }
}

// 计算统计数据
const calculateStats = () => {
  if (!predictionData.value || !historyData.value.length) return

  const data = predictionData.value

  // 计算历史平均票房
  const historySum = historyData.value.reduce((sum, item) => sum + (item.daily_box_office || 0), 0)
  const avgDaily = historySum / historyData.value.length

  // 计算预测总票房
  let predictedTotal = 0
  let predictions = []

  if (data.algorithm === 'combined') {
    // 综合预测 - 取两种算法的平均值
    const lrPredictions = data.linear_regression?.predictions || []
    const maPredictions = data.moving_average?.predictions || []
    predictions = lrPredictions.map((val, i) => (val + (maPredictions[i] || 0)) / 2)
  } else if (data.algorithm === 'linear_regression') {
    predictions = data.predictions || []
  } else {
    predictions = data.predictions || []
  }

  predictedTotal = predictions.reduce((sum, val) => sum + (val || 0), 0)

  // 计算趋势
  const recentHistory = historyData.value.slice(-3)
  const recentAvg = recentHistory.reduce((sum, item) => sum + (item.daily_box_office || 0), 0) / recentHistory.length
  const firstPrediction = predictions[0] || 0

  let trendDirection = 'stable'
  let trendPercent = '0'

  if (firstPrediction > recentAvg * 1.05) {
    trendDirection = 'up'
    trendPercent = (((firstPrediction - recentAvg) / recentAvg) * 100).toFixed(1)
  } else if (firstPrediction < recentAvg * 0.95) {
    trendDirection = 'down'
    trendPercent = (((recentAvg - firstPrediction) / recentAvg) * 100).toFixed(1)
  }

  stats.value = {
    avgDailyBoxOffice: (avgDaily / 10000).toFixed(2),
    trendDirection,
    trendPercent,
    totalPredicted: (predictedTotal / 10000).toFixed(2)
  }
}

// 渲染图表
const renderChart = () => {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  // 准备图表数据
  const dates = []
  const historySeries = []
  const lrPredictions = []
  const maPredictions = []

  // 历史数据
  historyData.value.forEach(item => {
    dates.push(formatDateShort(item.record_date))
    historySeries.push((item.daily_box_office || 0) / 10000)
  })

  // 预测数据
  const data = predictionData.value
  const predictDays = queryParams.predictDays

  if (data.algorithm === 'combined') {
    const lrPred = data.linear_regression?.predictions || []
    const maPred = data.moving_average?.predictions || []

    for (let i = 0; i < predictDays; i++) {
      const date = new Date()
      date.setDate(date.getDate() + i + 1)
      dates.push(formatDateShort(date))
      historySeries.push(null)
      lrPredictions.push((lrPred[i] || 0) / 10000)
      maPredictions.push((maPred[i] || 0) / 10000)
    }
  } else {
    const predictions = data.predictions || []

    for (let i = 0; i < predictDays; i++) {
      const date = new Date()
      date.setDate(date.getDate() + i + 1)
      dates.push(formatDateShort(date))
      historySeries.push(null)
      lrPredictions.push((predictions[i] || 0) / 10000)
    }
  }

  const series = [
    {
      name: '历史票房',
      type: 'line',
      data: historySeries,
      smooth: true,
      lineStyle: { color: '#10b981', width: 2 },
      itemStyle: { color: '#10b981' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
          { offset: 1, color: 'rgba(16, 185, 129, 0)' }
        ])
      }
    }
  ]

  if (data.algorithm === 'combined') {
    series.push(
      {
        name: '线性回归预测',
        type: 'line',
        data: lrPredictions.map((v, i) => i < historyData.value.length ? null : v),
        smooth: true,
        lineStyle: { color: '#3b82f6', width: 2, type: 'dashed' },
        itemStyle: { color: '#3b82f6' }
      },
      {
        name: '移动平均预测',
        type: 'line',
        data: maPredictions.map((v, i) => i < historyData.value.length ? null : v),
        smooth: true,
        lineStyle: { color: '#f59e0b', width: 2, type: 'dashed' },
        itemStyle: { color: '#f59e0b' }
      }
    )
  } else {
    series.push({
      name: '预测票房',
      type: 'line',
      data: lrPredictions.map((v, i) => i < historyData.value.length ? null : v),
      smooth: true,
      lineStyle: { color: '#3b82f6', width: 2, type: 'dashed' },
      itemStyle: { color: '#3b82f6' }
    })
  }

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: `${movieOptions.value.find(m => m.value === queryParams.movieId)?.label || ''} - 票房预测趋势`,
      left: 'center',
      textStyle: { color: '#fff', fontSize: 16 }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        let result = `<div style="padding: 8px;"><div style="color: #94a3b8; margin-bottom: 4px;">${params[0].axisValue}</div>`
        params.forEach(item => {
          if (item.value !== null && item.value !== undefined) {
            result += `<div style="display: flex; align-items: center; gap: 8px; margin: 4px 0;">
              <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: ${item.color};"></span>
              <span style="color: #fff;">${item.seriesName}:</span>
              <span style="color: ${item.color}; font-weight: bold;">${item.value.toFixed(2)} 万元</span>
            </div>`
          }
        })
        result += '</div>'
        return result
      }
    },
    legend: {
      data: series.map(s => s.name),
      bottom: 0,
      textStyle: { color: 'rgba(255, 255, 255, 0.7)' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
      axisLabel: { color: 'rgba(255, 255, 255, 0.6)' }
    },
    yAxis: {
      type: 'value',
      name: '票房（万元）',
      nameTextStyle: { color: 'rgba(255, 255, 255, 0.5)' },
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
      axisLabel: { color: 'rgba(255, 255, 255, 0.6)' },
      splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } }
    },
    series
  }

  chartInstance.setOption(option)
}

// 格式化日期短格式
const formatDateShort = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

// 窗口大小变化时调整图表
const handleResize = () => {
  chartInstance?.resize()
}

// 初始化
onMounted(() => {
  loadMovieOptions()
  loadAlgorithmInfo()
  window.addEventListener('resize', handleResize)
})

// 清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
    <!-- 动画背景 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <div class="relative z-10 p-6 lg:p-8">
      <!-- 页面标题 -->
      <div class="mb-6 animate-fade-in">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
            <TrendCharts class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">趋势预测分析</h1>
            <p class="text-slate-400 text-sm">基于历史数据的票房趋势预测与算法对比</p>
          </div>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="glass-card rounded-xl p-5 border border-white/10 animate-slide-up" style="animation-delay: 0.1s">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500/20 to-green-500/20 flex items-center justify-center">
              <DataAnalysis class="w-5 h-5 text-emerald-400" />
            </div>
            <div class="flex-1">
              <div class="text-xs text-slate-400 mb-1">历史日均票房</div>
              <div class="text-xl font-bold text-white">{{ stats.avgDailyBoxOffice }} <span class="text-sm font-normal text-slate-400">万元</span></div>
            </div>
          </div>
        </div>

        <div class="glass-card rounded-xl p-5 border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                 :class="stats.trendDirection === 'up' ? 'bg-emerald-500/20' : stats.trendDirection === 'down' ? 'bg-red-500/20' : 'bg-amber-500/20'">
              <component :is="trendInfo.icon" class="w-5 h-5" :class="trendInfo.color" />
            </div>
            <div class="flex-1">
              <div class="text-xs text-slate-400 mb-1">预测趋势</div>
              <div class="text-lg font-bold" :class="trendInfo.color">
                {{ trendInfo.text }}
                <span class="text-sm font-normal text-slate-400">({{ stats.trendPercent }}%)</span>
              </div>
            </div>
          </div>
        </div>

        <div class="glass-card rounded-xl p-5 border border-white/10 animate-slide-up" style="animation-delay: 0.3s">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
              <TrendCharts class="w-5 h-5 text-blue-400" />
            </div>
            <div class="flex-1">
              <div class="text-xs text-slate-400 mb-1">预测总票房</div>
              <div class="text-xl font-bold text-white">{{ stats.totalPredicted }} <span class="text-sm font-normal text-slate-400">万元</span></div>
            </div>
          </div>
        </div>

        <div class="glass-card rounded-xl p-5 border border-white/10 animate-slide-up" style="animation-delay: 0.4s">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
              <InfoFilled class="w-5 h-5 text-violet-400" />
            </div>
            <div class="flex-1">
              <div class="text-xs text-slate-400 mb-1">预测算法</div>
              <div class="text-lg font-bold text-white">{{ algorithmOptions.find(a => a.value === queryParams.algorithm)?.label || '--' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 预测配置 -->
      <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.5s">
        <div class="flex items-center gap-2 mb-4">
          <Search class="w-4 h-4 text-violet-400" />
          <span class="text-sm font-medium text-slate-300">预测配置</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- 影片选择 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <Film class="w-3.5 h-3.5" />
              选择影片
            </label>
            <el-select
              v-model="queryParams.movieId"
              placeholder="请选择影片"
              clearable
              filterable
              loading="movieLoading"
              class="filter-input"
              style="width: 100%"
            >
              <el-option
                v-for="item in movieOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <!-- 预测算法 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <DataAnalysis class="w-3.5 h-3.5" />
              预测算法
            </label>
            <el-select
              v-model="queryParams.algorithm"
              class="filter-input"
              style="width: 100%"
            >
              <el-option
                v-for="algo in algorithmOptions"
                :key="algo.value"
                :label="algo.label"
                :value="algo.value"
              >
                <div class="flex flex-col">
                  <span>{{ algo.label }}</span>
                  <span class="text-xs text-slate-500">{{ algo.desc }}</span>
                </div>
              </el-option>
            </el-select>
          </div>

          <!-- 预测天数 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <Calendar class="w-3.5 h-3.5" />
              预测天数
            </label>
            <div class="flex gap-2">
              <button
                v-for="days in predictDaysOptions"
                :key="days"
                @click="queryParams.predictDays = days"
                class="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all"
                :class="queryParams.predictDays === days
                  ? 'bg-gradient-to-r from-violet-500 to-purple-500 text-white shadow-lg shadow-violet-500/30'
                  : 'bg-white/5 text-slate-400 hover:bg-white/10'"
              >
                {{ days }}天
              </button>
            </div>
          </div>
        </div>

        <!-- 执行按钮 -->
        <div class="flex items-center justify-end mt-4 pt-4 border-t border-white/10">
          <button
            @click="handleExecutePrediction"
            :disabled="!queryParams.movieId || chartLoading"
            class="px-6 py-2.5 rounded-xl font-medium text-white transition-all flex items-center gap-2"
            :class="!queryParams.movieId || chartLoading
              ? 'bg-white/5 cursor-not-allowed'
              : 'bg-gradient-to-r from-violet-500 to-purple-500 hover:shadow-lg hover:shadow-violet-500/30 hover:-translate-y-0.5'"
          >
            <TrendCharts class="w-4 h-4" />
            {{ chartLoading ? '预测中...' : '执行预测' }}
          </button>
        </div>
      </div>

      <!-- 预测图表 -->
      <div class="glass-card rounded-2xl p-6 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.6s">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-white font-medium flex items-center gap-2">
            <div class="w-6 h-6 rounded bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
              <TrendCharts class="w-3.5 h-3.5 text-violet-400" />
            </div>
            预测趋势图
          </h3>
          <div class="text-sm text-slate-400">
            实线 = 历史数据 | 虚线 = 预测数据
          </div>
        </div>
        <div
          ref="chartRef"
          class="w-full"
          style="height: 400px;"
          v-loading="chartLoading"
          element-loading-background="rgba(15, 23, 42, 0.5)"
        />
      </div>

      <!-- 算法说明 -->
      <div class="glass-card rounded-2xl p-6 border border-white/10 animate-slide-up" style="animation-delay: 0.7s">
        <div class="flex items-center gap-2 mb-4">
          <div class="w-6 h-6 rounded bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
            <InfoFilled class="w-3.5 h-3.5 text-violet-400" />
          </div>
          <h3 class="text-white font-medium">算法说明</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            v-for="algo in algorithmOptions"
            :key="algo.value"
            class="p-4 rounded-xl border transition-all"
            :class="queryParams.algorithm === algo.value
              ? 'bg-violet-500/10 border-violet-500/30'
              : 'bg-white/5 border-white/10 hover:border-white/20'"
          >
            <div class="flex items-center gap-2 mb-2">
              <div class="w-2 h-2 rounded-full"
                   :class="queryParams.algorithm === algo.value ? 'bg-violet-400' : 'bg-slate-500'" />
              <span class="font-medium" :class="queryParams.algorithm === algo.value ? 'text-white' : 'text-slate-300'">
                {{ algo.label }}
              </span>
            </div>
            <p class="text-sm text-slate-400">{{ algo.desc }}</p>
          </div>
        </div>

        <div class="mt-4 p-4 rounded-xl bg-white/5 border border-white/10">
          <div class="text-sm text-slate-300 space-y-2">
            <p><span class="text-violet-400 font-medium">线性回归</span>：使用最小二乘法拟合历史票房数据，建立线性模型 y = kx + b 进行预测</p>
            <p><span class="text-amber-400 font-medium">移动平均</span>：基于最近N天的票房数据计算加权平均值，权重随时间递减（最近的一天权重最高）</p>
            <p><span class="text-blue-400 font-medium">综合预测</span>：同时返回两种算法结果供对比分析，可评估预测置信度</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 玻璃态卡片 */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* 网格背景 */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* 渐变光球 */
.gradient-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #8b5cf6, #a855f7);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #7c3aed, #6366f1);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #a855f7, #8b5cf6);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -20px) scale(1.05);
  }
  50% {
    transform: translate(-10px, 20px) scale(0.95);
  }
  75% {
    transform: translate(-20px, -10px) scale(1.02);
  }
}

/* 淡入动画 */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

/* 滑入动画 */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* 筛选输入框样式 */
:deep(.filter-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  transition: all 0.3s ease;
}

:deep(.filter-input .el-input__wrapper:hover) {
  border-color: rgba(139, 92, 246, 0.5);
}

:deep(.filter-input .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #8b5cf6;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
}

:deep(.filter-input .el-input__inner) {
  color: #fff;
}

:deep(.filter-input .el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

:deep(.filter-input .el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

:deep(.filter-input .el-select__selected-item) {
  color: #fff;
}

:deep(.filter-input .el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

/* 下拉选项样式 */
:deep(.el-select-dropdown__item) {
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
}

:deep(.el-select-dropdown__item:hover) {
  background: rgba(139, 92, 246, 0.2);
}

:deep(.el-select-dropdown__item.is-selected) {
  background: rgba(139, 92, 246, 0.3);
  color: #fff;
}
</style>
