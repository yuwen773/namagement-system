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

  const historical = predictionResult.value.history || []
  const forecast = predictionResult.value.predictions || []

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
        lineStyle: { color: '#f59e0b', width: 3 },
        itemStyle: { color: '#f59e0b' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(245, 158, 11, 0.3)' },
            { offset: 1, color: 'rgba(245, 158, 11, 0.05)' }
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
  <div class="page-container">
    <div class="content-wrapper">
      <!-- Header -->
      <div class="section-header animate-fade-in">
        <div class="glass-card header-card">
          <div class="flex items-center gap-4">
            <div class="icon-box icon-red">
              <MagicStick class="w-7 h-7" />
            </div>
            <div>
              <h1 class="page-title">未来票房预测</h1>
              <p class="page-subtitle">基于历史数据与算法模型</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Prediction configuration -->
      <div class="animate-slide-up">
        <div class="glass-card config-card">
          <el-form :inline="true" :model="{ selectedMovie, selectedAlgorithm, predictionDays }">
            <el-form-item label="选择影片">
              <el-select
                v-model="selectedMovie"
                placeholder="请选择影片"
                clearable
                filterable
                popper-class="dark-select-dropdown"
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
                popper-class="dark-select-dropdown"
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
        <div class="glass-card result-card">
          <!-- Chart -->
          <div v-if="predictionResult" class="chart-section">
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
          <div v-if="predictionResult" class="conclusion-section">
            <div class="conclusion-box">
              <TrendCharts class="conclusion-icon" />
              <div class="conclusion-content">
                <h4 class="conclusion-title">预测结论</h4>
                <p class="conclusion-text">
                  {{ getPredictionConclusion() }}
                </p>
                <div v-if="predictionResult.forecast && predictionResult.forecast.length > 0" class="conclusion-meta">
                  预测未来 {{ predictionDays }} 天票房走势，基于{{ selectedAlgorithm === 'linear_regression' ? '线性回归' : '移动平均' }}算法
                </div>
              </div>
            </div>
          </div>
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
  border-color: rgba(220, 38, 38, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ========================================
   Header Section
   ======================================== */
.section-header {
  margin-bottom: 0;
}

.header-card {
  padding: 1.5rem;
}

.icon-box {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-red {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  color: white;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
}

.page-subtitle {
  color: #94a3b8;
  margin-top: 0.25rem;
  font-size: 0.875rem;
}

/* ========================================
   Config Card
   ======================================== */
.config-card {
  padding: 1.5rem;
}

/* ========================================
   Result Card
   ======================================== */
.result-card {
  padding: 1.5rem;
}

.chart-section {
  margin-bottom: 1.5rem;
}

.chart-container-large {
  height: 400px;
}

.chart-placeholder {
  min-height: 400px;
}

/* ========================================
   Conclusion Section
   ======================================== */
.conclusion-section {
  margin-top: 1.5rem;
}

.conclusion-box {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.75rem;
  background: linear-gradient(to right, rgba(16, 185, 129, 0.1), rgba(20, 184, 166, 0.1));
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.conclusion-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.conclusion-content {
  flex: 1;
}

.conclusion-title {
  color: #10b981;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.conclusion-text {
  color: #cbd5e1;
  font-size: 0.875rem;
  line-height: 1.625;
}

.conclusion-meta {
  margin-top: 0.75rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

/* ========================================
   Form Styling
   ======================================== */
:deep(.el-form-item__label) {
  color: #94a3b8;
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper),
:deep(.el-input-number__decrease),
:deep(.el-input-number__increase) {
  background-color: rgba(255, 255, 255, 0.05) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
  color: #fff !important;
}

:deep(.el-input__wrapper:hover),
:deep(.el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(220, 38, 38, 0.5) inset !important;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px #dc2626 inset !important;
}

:deep(.el-input__inner) {
  color: #fff !important;
  background: transparent !important;
}

:deep(.el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3) !important;
}

:deep(.el-select__caret) {
  color: rgba(255, 255, 255, 0.5) !important;
}

:deep(.el-input-number .el-input-number__decrease),
:deep(.el-input-number .el-input-number__increase) {
  border-color: rgba(255, 255, 255, 0.1) !important;
  color: #94a3b8 !important;
}

:deep(.el-input-number .el-input-number__decrease:hover),
:deep(.el-input-number .el-input-number__increase:hover) {
  color: #fff !important;
  background-color: rgba(255, 255, 255, 0.1) !important;
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

<style>
/* ========================================
   Global Overrides (Poppers)
   ======================================== */

/* Select Dropdown */
.dark-select-dropdown.el-popper {
  background: #12121f !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.dark-select-dropdown .el-popper__arrow::before {
  background: #12121f !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.dark-select-dropdown .el-select-dropdown__item {
  color: #94a3b8;
}

.dark-select-dropdown .el-select-dropdown__item.hover,
.dark-select-dropdown .el-select-dropdown__item:hover {
  background: rgba(220, 38, 38, 0.1);
  color: #fff;
}

.dark-select-dropdown .el-select-dropdown__item.selected {
  color: #dc2626;
  font-weight: bold;
}
</style>
