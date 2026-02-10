<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// 图表实例
const trendChartRef = ref(null)
const regionChartRef = ref(null)
const typeChartRef = ref(null)
let trendChart = null
let regionChart = null
let typeChart = null

// 初始化图表
const initCharts = () => {
  // 趋势图
  if (trendChartRef.value) {
    trendChart = echarts.init(trendChartRef.value)
    trendChart.setOption({
      title: { text: '票房趋势', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
      yAxis: { type: 'value' },
      series: [{ data: [820, 932, 901, 934, 1290, 1330, 1320], type: 'line', smooth: true }]
    })
  }

  // 地域分布图
  if (regionChartRef.value) {
    regionChart = echarts.init(regionChartRef.value)
    regionChart.setOption({
      title: { text: '地域分布', left: 'center' },
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: '50%',
        data: [
          { value: 1048, name: '北京' },
          { value: 735, name: '上海' },
          { value: 580, name: '深圳' },
          { value: 484, name: '广州' },
          { value: 300, name: '成都' }
        ]
      }]
    })
  }

  // 类型占比图
  if (typeChartRef.value) {
    typeChart = echarts.init(typeChartRef.value)
    typeChart.setOption({
      title: { text: '类型占比', left: 'center' },
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 1048, name: '动作' },
          { value: 735, name: '喜剧' },
          { value: 580, name: '剧情' },
          { value: 484, name: '科幻' },
          { value: 300, name: '动画' }
        ]
      }]
    })
  }
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  trendChart?.resize()
  regionChart?.resize()
  typeChart?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  regionChart?.dispose()
  typeChart?.dispose()
})
</script>

<template>
  <div class="visualization-page">
    <h2 class="text-2xl font-bold mb-6">可视化图表库</h2>

    <el-row :gutter="20">
      <el-col :span="24" class="mb-4">
        <el-card shadow="hover">
          <div ref="trendChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12" class="mb-4">
        <el-card shadow="hover">
          <div ref="regionChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12" class="mb-4">
        <el-card shadow="hover">
          <div ref="typeChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.chart-container {
  height: 400px;
}
</style>

<script>
export default {
  name: 'UserVisualization'
}
</script>
