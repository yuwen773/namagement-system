<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

const selectedMovie = ref('')
const selectedAlgorithm = ref('linear_regression')
const predictionDays = ref(7)
const loading = ref(false)

// 预测结果图表
const chartRef = ref(null)
let chart = null

const movies = ref([
  { id: 1, title: '流浪地球2' },
  { id: 2, title: '满江红' },
  { id: 3, title: '熊出没·伴我熊芯' }
])

const algorithms = [
  { value: 'linear_regression', label: '线性回归' },
  { value: 'moving_average', label: '移动平均法' }
]

// 初始化图表
const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    chart.setOption({
      title: { text: '票房预测结果', left: 'center' },
      tooltip: { trigger: 'axis' },
      legend: { data: ['历史票房', '预测票房'], top: 30 },
      xAxis: {
        type: 'category',
        data: ['第1天', '第2天', '第3天', '第4天', '第5天', '第6天', '第7天', '第8天', '第9天', '第10天', '第11天', '第12天', '第13天', '第14天']
      },
      yAxis: { type: 'value' },
      series: [
        {
          name: '历史票房',
          data: [820, 932, 901, 934, 1290, 1330, 1320, 1200, 1100, 1000, null, null, null, null],
          type: 'line',
          smooth: true
        },
        {
          name: '预测票房',
          data: [null, null, null, null, null, null, null, 1150, 1200, 1250, 1300, 1350, 1400, 1450],
          type: 'line',
          smooth: true,
          lineStyle: { type: 'dashed' }
        }
      ]
    })
  }
}

const handleResize = () => {
  chart?.resize()
}

const executePrediction = async () => {
  if (!selectedMovie.value) {
    ElMessage.warning('请选择影片')
    return
  }

  loading.value = true
  try {
    // TODO: 调用预测 API
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('预测完成')
  } catch (error) {
    ElMessage.error('预测失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<template>
  <div class="prediction-page">
    <h2 class="text-2xl font-bold mb-6">未来票房预测</h2>

    <!-- 预测配置 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="selectedMovie">
        <el-form-item label="选择影片">
          <el-select v-model="selectedMovie" placeholder="请选择影片" clearable>
            <el-option
              v-for="movie in movies"
              :key="movie.id"
              :label="movie.title"
              :value="movie.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预测算法">
          <el-select v-model="selectedAlgorithm" placeholder="请选择算法">
            <el-option
              v-for="algo in algorithms"
              :key="algo.value"
              :label="algo.label"
              :value="algo.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预测天数">
          <el-input-number v-model="predictionDays" :min="1" :max="30" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="executePrediction">
            执行预测
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 预测结果 -->
    <el-card>
      <div ref="chartRef" class="chart-container"></div>

      <!-- 趋势结论 -->
      <div class="prediction-conclusion mt-4 p-4 bg-gray-50 rounded">
        <h4 class="font-bold mb-2">预测结论</h4>
        <p class="text-gray-600">
          基于历史票房数据分析和所选预测算法，预计该影片在未来 {{ predictionDays }} 天的票房将呈现
          <span class="text-success">稳中有升</span> 的趋势。
        </p>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.chart-container {
  height: 400px;
}
</style>

<script>
export default {
  name: 'UserPrediction'
}
</script>
