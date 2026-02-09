<template>
  <div ref="chartRef" class="echarts-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  options: {
    type: Object,
    required: true
  },
  theme: {
    type: String,
    default: 'dark'
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = async () => {
  await nextTick()
  if (chartRef.value && !chartInstance) {
    try {
      chartInstance = echarts.init(chartRef.value, props.theme, {
        renderer: 'canvas'
      })
      if (props.options) {
        chartInstance.setOption(props.options, true)
      }
    } catch (e) {
      console.error('ECharts init error:', e)
    }
  }
}

const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
  chartInstance = null
})

watch(() => props.options, (newOptions) => {
  if (chartInstance && newOptions) {
    chartInstance.setOption(newOptions, true)
  }
}, { deep: true })
</script>

<style scoped>
.echarts-container {
  width: 100%;
  height: 100%;
  min-height: 280px;
}
</style>
