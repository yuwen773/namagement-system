<script setup>
import { ref, onMounted, onUnmounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'
import {
  getPrediction,
  executePrediction,
  getPredictionHistory,
  getAlgorithmInfo
} from '@/api/prediction'
import { getMovies } from '@/api/movie'

const loading = ref(false)
const chartLoading = ref(false)

// 统计数据
const stats = ref({
  accuracy: '--',
  predictionCount: 0
})

// 算法信息
const algorithms = ref([])
const algorithmLoading = ref(false)

// 预测历史
const historyData = ref([])
const historyLoading = ref(false)

// 查询参数
const queryParams = reactive({
  movie: null,
  algorithm: 'combined',
  days: 7
})

// 电影选项
const movieOptions = ref([])
const movieLoading = ref(false)

// 图表实例
let chartInstance = null
const chartRef = ref(null)

// 算法选项
const algorithmOptions = [
  { label: '线性回归', value: 'linear_regression' },
  { label: '移动平均', value: 'moving_average' },
  { label: '综合预测', value: 'combined' }
]

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
  algorithmLoading.value = true
  try {
    const res = await getAlgorithmInfo()
    algorithms.value = res.data || []
  } catch (error) {
    console.error('加载算法信息失败:', error)
  } finally {
    algorithmLoading.value = false
  }
}

// 加载预测历史
const loadHistory = async () => {
  historyLoading.value = true
  try {
    const res = await getPredictionHistory({ pageSize: 10 })
    historyData.value = res.data || []
    stats.value.predictionCount = res.total || 0
  } catch (error) {
    console.error('加载历史失败:', error)
  } finally {
    historyLoading.value = false
  }
}

// 执行预测
const handleExecutePrediction = async () => {
  if (!queryParams.movie) {
    ElMessage.warning('请选择要预测的影片')
    return
  }

  chartLoading.value = true
  try {
    const res = await executePrediction({
      movie_id: queryParams.movie,
      algorithm: queryParams.algorithm,
      days: queryParams.days
    })

    const predictionData = res.data || {}

    // 更新统计
    if (predictionData.accuracy) {
      stats.value.accuracy = (predictionData.accuracy * 100).toFixed(1) + '%'
    }

    // 渲染图表
    renderChart(predictionData)

    ElMessage.success('预测执行成功')
    loadHistory()
  } catch (error) {
    console.error('预测失败:', error)
    ElMessage.error('预测执行失败')
  } finally {
    chartLoading.value = false
  }
}

// 渲染图表
const renderChart = (data) => {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const dates = data.dates || []
  const history = data.history || []
  const predictions = data.predictions || []

  const option = {
    title: {
      text: '票房预测趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['历史票房', '预测票房'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      name: '票房(万)'
    },
    series: [
      {
        name: '历史票房',
        type: 'line',
        data: dates.map((_, i) => i < history.length ? history[i] : null),
        smooth: true,
        lineStyle: {
          color: '#409eff',
          width: 2
        },
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: '预测票房',
        type: 'line',
        data: dates.map((_, i) => i >= history.length ? predictions[i - history.length] : null),
        smooth: true,
        lineStyle: {
          color: '#e6a23c',
          width: 2,
          type: 'dashed'
        },
        itemStyle: {
          color: '#e6a23c'
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

// 窗口大小变化时调整图表
const handleResize = () => {
  chartInstance?.resize()
}

// 格式化数字
const formatNumber = (num) => {
  if (!num) return '--'
  return num.toLocaleString()
}

// 组件挂载时
onMounted(() => {
  loadMovieOptions()
  loadAlgorithmInfo()
  loadHistory()

  window.addEventListener('resize', handleResize)
})

// 组件卸载时
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<template>
  <div class="prediction-page">
    <h2 class="text-2xl font-bold mb-6">趋势预测分析</h2>

    <!-- 预测概览 -->
    <el-row :gutter="20" class="mb-6">
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="text-center">
            <el-icon :size="48" color="#409eff"><TrendCharts /></el-icon>
            <div class="text-xl font-bold mt-2">预测准确率</div>
            <div class="text-3xl font-bold text-primary mt-2">{{ stats.accuracy }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="text-center">
            <el-icon :size="48" color="#67c23a"><DataAnalysis /></el-icon>
            <div class="text-xl font-bold mt-2">预测次数</div>
            <div class="text-3xl font-bold text-success mt-2">{{ stats.predictionCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="text-center">
            <el-icon :size="48" color="#e6a23c"><InfoFilled /></el-icon>
            <div class="text-xl font-bold mt-2">可用算法</div>
            <div class="text-gray-500 mt-2">{{ algorithms.length }} 种</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预测配置 -->
    <el-card class="mb-6">
      <el-form :inline="true" :model="queryParams" label-width="100px">
        <el-form-item label="选择影片">
          <el-select
            v-model="queryParams.movie"
            placeholder="请选择影片"
            clearable
            filterable
            loading="movieLoading"
            style="width: 300px"
          >
            <el-option
              v-for="movie in movieOptions"
              :key="movie.value"
              :label="movie.label"
              :value="movie.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预测算法">
          <el-select v-model="queryParams.algorithm" style="width: 150px">
            <el-option
              v-for="algo in algorithmOptions"
              :key="algo.value"
              :label="algo.label"
              :value="algo.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预测天数">
          <el-input-number v-model="queryParams.days" :min="1" :max="30" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleExecutePrediction" :loading="chartLoading">
            执行预测
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 预测图表 -->
    <el-card class="mb-6">
      <div ref="chartRef" style="width: 100%; height: 400px;" v-loading="chartLoading" />
    </el-card>

    <!-- 预测历史 -->
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <span>预测历史记录</span>
        </div>
      </template>

      <el-table :data="historyData" v-loading="historyLoading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="movie_title" label="影片" min-width="150" />
        <el-table-column prop="algorithm" label="算法" width="120">
          <template #default="{ row }">
            {{ row.algorithm === 'linear_regression' ? '线性回归' :
               row.algorithm === 'moving_average' ? '移动平均' : '综合预测' }}
          </template>
        </el-table-column>
        <el-table-column prop="predicted_days" label="预测天数" width="100" align="center" />
        <el-table-column prop="predicted_revenue" label="预测票房(万)" width="120">
          <template #default="{ row }">
            {{ formatNumber(row.predicted_revenue) }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ new Date(row.created_at).toLocaleString('zh-CN') }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>
