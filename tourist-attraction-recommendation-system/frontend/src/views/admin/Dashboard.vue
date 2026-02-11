<template>
  <div>
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb-6">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">{{ stat.title }}</p>
              <p class="text-3xl font-bold mt-1">{{ stat.value }}</p>
            </div>
            <div class="p-3 rounded-full" :class="stat.bgColor">
              <el-icon :size="24" :class="stat.color"><component :is="stat.icon" /></el-icon>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20">
      <el-col :span="16">
        <div class="bg-white rounded-xl shadow-md p-6">
          <h3 class="text-lg font-bold mb-4">月度数据趋势</h3>
          <div ref="chartRef" class="h-80"></div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="bg-white rounded-xl shadow-md p-6">
          <h3 class="text-lg font-bold mb-4">热门景点 TOP 5</h3>
          <div ref="hotChartRef" class="h-80"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import request from '@/api/request'
import { User, View, ChatDotRound, Star } from '@element-plus/icons-vue'

const chartRef = ref(null)
const hotChartRef = ref(null)
let chartInstance = null
let hotChartInstance = null

const stats = ref([
  { title: '用户总数', value: 0, icon: User, color: 'text-blue-600', bgColor: 'bg-blue-100' },
  { title: '浏览量', value: 0, icon: View, color: 'text-green-600', bgColor: 'bg-green-100' },
  { title: '评论数', value: 0, icon: ChatDotRound, color: 'text-orange-600', bgColor: 'bg-orange-100' },
  { title: '景点数', value: 0, icon: Star, color: 'text-red-600', bgColor: 'bg-red-100' }
])

async function fetchDashboard() {
  try {
    const res = await request.get('/statistics/dashboard/')
    Object.assign(stats.value, res.data.stats)
    initCharts(res.data.charts)
  } catch (error) {
    console.error(error)
  }
}

function initCharts(data) {
  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['新增用户', '浏览量', '评论数'] },
    xAxis: { type: 'category', data: data.months },
    yAxis: { type: 'value' },
    series: [
      { name: '新增用户', type: 'line', data: data.users },
      { name: '浏览量', type: 'line', data: data.views },
      { name: '评论数', type: 'line', data: data.comments }
    ]
  })

  hotChartInstance = echarts.init(hotChartRef.value)
  hotChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: data.hotNames },
    series: [{ type: 'bar', data: data.hotValues }]
  })
}

onMounted(fetchDashboard)
onUnmounted(() => {
  chartInstance?.dispose()
  hotChartInstance?.dispose()
})
</script>
