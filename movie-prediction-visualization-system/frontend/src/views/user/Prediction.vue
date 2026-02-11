<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { getMoviePrediction } from '@/api/prediction'
import { getMovies } from '@/api/movie'
import { ElMessage } from 'element-plus'
import {
  VideoCamera,
  TrendCharts,
  MagicStick
} from '@element-plus/icons-vue'

const selectedMovie = ref('')
const selectedAlgorithm = ref('linear_regression')
const predictionDays = ref(7)
const loading = ref(false)
const predicting = ref(false)

// Chart reference
const chartRef = ref(null)
let chart = null

// Data
const movies = ref([])
const predictionResult = ref(null)

const algorithms = [
  { value: 'linear_regression', label: '线性回归', description: '基于历史数据的线性趋势预测' },
  { value: 'moving_average', label: '移动平均法', description: '基于近期数据的加权平均预测' }
]

// Load movies
const loadMovies = async () => {
  try {
    const res = await getMovies({ pageSize: 1000 })
    movies.value = res.data || []
  } catch (error) {
    console.error('加载影片列表失败:', error)
  }
}

// Initialize chart
const initChart = () => {
  if (!chartRef.value) return

  if (chart) {
    chart.dispose()
  }

  chart = echarts.init(chartRef.value)

  // Default empty chart
  const option = {
    title: {
      text: '票房预测结果',
      left: 'center',
      textStyle: { color: '#fff', fontSize: 16 }
    },
    grid: {
      left: '60px',
      right: '40px',
      bottom: '60px',
      top: '80px'
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: '#4b5563' } },
      axisLabel: { color: '#9ca3af' }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#4b5563' } },
      axisLabel: {
        color: '#9ca3af',
        formatter: (value) => (value / 10000).toFixed(0) + '万'
      },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    series: []
  }

  chart.setOption(option)
}

// Update chart with prediction data
const updateChart = () => {
  if (!chart || !predictionResult.value) return

  const historical = predictionResult.value.historical || []
  const forecast = predictionResult.value.forecast || []

  const dates = [
    ...historical.map(item => item.date),
    ...forecast.map(item => item.date)
  ]

  const historicalData = historical.map(item => item.box_office)
  const forecastData = new Array(historical.length).fill(null).concat(forecast.map(item => item.box_office))

  const option = {
    title: {
      text: `${movies.value.find(m => m.id === selectedMovie.value)?.title || ''} - 票房预测`,
      left: 'center',
      textStyle: { color: '#fff', fontSize: 16 }
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        let result = params[0].axisValue + '<br/>'
        params.forEach(item => {
          if (item.value !== null) {
            result += `${item.marker} ${item.seriesName}: ${(item.value / 10000).toFixed(2)}万元<br/>`
          }
        })
        return result
      }
    },
    legend: {
      data: ['历史票房', '预测票房'],
      top: 40,
      textStyle: { color: '#9ca3af' }
    },
    grid: {
      left: '60px',
      right: '40px',
      bottom: '60px',
      top: '100px'
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#4b5563' } },
      axisLabel: {
        color: '#9ca3af',
        rotate: 30,
        interval: 0
      }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#4b5563' } },
      axisLabel: {
        color: '#9ca3af',
        formatter: (value) => (value / 10000).toFixed(0) + '万'
      },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    series: [
      {
        name: '历史票房',
        type: 'line',
        smooth: true,
        data: historicalData,
        lineStyle: { color: '#3b82f6', width: 3 },
        itemStyle: { color: '#3b82f6' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
            { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
          ])
        }
      },
      {
        name: '预测票房',
        type: 'line',
        smooth: true,
        data: forecastData,
        lineStyle: { color: '#10b981', width: 3, type: 'dashed' },
        itemStyle: { color: '#10b981' }
      }
    ]
  }

  chart.setOption(option)
}

// Get prediction conclusion
const getPredictionConclusion = () => {
  if (!predictionResult.value || !predictionResult.value.forecast) return ''

  const forecast = predictionResult.value.forecast
  if (forecast.length === 0) return '数据不足，无法生成预测结论'

  const lastForecast = forecast[forecast.length - 1].box_office
  const firstForecast = forecast[0].box_office

  if (lastForecast > firstForecast * 1.1) {
    return '预测结果显示，该影片票房将呈现明显上升趋势，建议加大宣传力度。'
  } else if (lastForecast < firstForecast * 0.9) {
    return '预测结果显示，该影片票房将呈现下降趋势，建议考虑调整排片策略。'
  } else {
    return '预测结果显示，该影片票房将保持相对稳定，继续维持当前运营策略。'
  }
}

// Execute prediction
const executePrediction = async () => {
  if (!selectedMovie.value) {
    ElMessage.warning('请选择影片')
    return
  }

  predicting.value = true
  try {
    const res = await getMoviePrediction(selectedMovie.value, {
      predictDays: predictionDays.value,
      algorithm: selectedAlgorithm.value
    })

    predictionResult.value = res.data
    updateChart()
    ElMessage.success('预测完成')
  } catch (error) {
    console.error('预测失败:', error)
    ElMessage.error('预测失败，请稍后重试')
  } finally {
    predicting.value = false
  }
}

// Handle window resize
const handleResize = () => {
  chart?.resize()
}

// Handle movie selection change - auto execute prediction
watch(selectedMovie, (newVal) => {
  if (newVal) {
    predictionResult.value = null
  }
})

onMounted(() => {
  loadMovies()
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6 lg:p-8">
    <!-- Animated background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none -z-10">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <!-- Header -->
    <div class="mb-8 animate-fade-in">
      <div class="glass-card rounded-2xl p-6 border border-white/10">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-violet-500 to-purple-500 flex items-center justify-center">
            <MagicStick class="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">未来票房预测</h1>
            <p class="text-slate-400 mt-1">基于历史数据与算法模型</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Prediction configuration -->
    <div class="mb-6 animate-slide-up">
      <div class="glass-card rounded-2xl p-6 border border-white/10">
        <el-form :inline="true" :model="{ selectedMovie, selectedAlgorithm, predictionDays }">
          <el-form-item label="选择影片">
            <el-select
              v-model="selectedMovie"
              placeholder="请选择影片"
              clearable
              filterable
              style="width: 240px"
            >
              <el-option
                v-for="movie in movies"
                :key="movie.id"
                :label="movie.title"
                :value="movie.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="预测算法">
            <el-select
              v-model="selectedAlgorithm"
              placeholder="请选择算法"
              style="width: 200px"
            >
              <el-option
                v-for="algo in algorithms"
                :key="algo.value"
                :label="algo.label"
                :value="algo.value"
              >
                <div class="flex flex-col">
                  <span>{{ algo.label }}</span>
                  <span class="text-xs text-slate-500">{{ algo.description }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="预测天数">
            <el-input-number
              v-model="predictionDays"
              :min="3"
              :max="30"
              :step="1"
              style="width: 150px"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              :loading="predicting"
              :disabled="!selectedMovie"
              @click="executePrediction"
            >
              执行预测
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- Prediction result -->
    <div class="animate-slide-up" style="animation-delay: 0.2s">
      <div class="glass-card rounded-2xl border border-white/10 p-6">
        <!-- Chart -->
        <div v-if="predictionResult" class="mb-6">
          <div ref="chartRef" class="chart-container-large"></div>
        </div>
        <div v-else class="chart-placeholder">
          <div class="text-center text-slate-500 py-20">
            <VideoCamera class="w-20 h-20 mx-auto mb-4 opacity-30" />
            <p class="text-lg">请选择影片并执行预测</p>
            <p class="text-sm mt-2">预测结果将在此处显示</p>
          </div>
        </div>

        <!-- Prediction conclusion -->
        <div v-if="predictionResult" class="prediction-conclusion">
          <div class="flex items-start gap-3 p-4 rounded-xl bg-gradient-to-r from-emerald-500/10 to-teal-500/10 border border-emerald-500/20">
            <TrendCharts class="w-6 h-6 text-emerald-400 flex-shrink-0 mt-1" />
            <div>
              <h4 class="text-emerald-400 font-semibold mb-2">预测结论</h4>
              <p class="text-slate-300 text-sm leading-relaxed">
                {{ getPredictionConclusion() }}
              </p>
              <div v-if="predictionResult.forecast && predictionResult.forecast.length > 0" class="mt-3 text-xs text-slate-400">
                预测未来 {{ predictionDays }} 天票房走势，基于{{ selectedAlgorithm === 'linear_regression' ? '线性回归' : '移动平均' }}算法
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Grid background */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* Gradient orbs */
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
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #10b981, #3b82f6);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -20px) scale(1.05); }
  50% { transform: translate(-10px, 20px) scale(0.95); }
  75% { transform: translate(-20px, -10px) scale(1.02); }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

.chart-container-large {
  height: 400px;
}

.chart-placeholder {
  min-height: 400px;
}

/* Form styling */
:deep(.el-form-item__label) {
  color: #9ca3af;
}

:deep(.el-input__wrapper),
:deep(.el-select .el-input__wrapper),
:deep(.el-input-number .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

:deep(.el-input__inner) {
  color: #fff;
}

:deep(.el-select__placeholder),
:deep(.el-input__placeholder) {
  color: #6b7280;
}

:deep(.el-input-number .el-input-number__decrease),
:deep(.el-input-number .el-input-number__increase) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #9ca3af;
}

:deep(.el-input-number .el-input-number__decrease:hover),
:deep(.el-input-number .el-input-number__increase:hover) {
  color: #fff;
}
</style>
