<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { Loading } from '@element-plus/icons-vue'

const props = defineProps({
  option: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  height: {
    type: String,
    default: '400px'
  }
})

const chartRef = ref(null)
const chartInstance = ref(null)
const resizeObserver = ref(null)

const initChart = () => {
  if (!chartRef.value) return

  chartInstance.value = echarts.init(chartRef.value)
  updateChart()

  // 监听窗口大小变化
  resizeObserver.value = new ResizeObserver(() => {
    chartInstance.value?.resize()
  })
  resizeObserver.value.observe(chartRef.value)
}

const updateChart = () => {
  if (!chartInstance.value || !props.option) return

  // Don't use notMerge: true to avoid coordinate system issues
  try {
    chartInstance.value.setOption({
      backgroundColor: 'transparent',
      ...props.option
    })
  } catch (error) {
    console.warn('Chart update error:', error)
  }
}

watch(() => props.option, () => {
  updateChart()
}, { deep: true })

onMounted(() => {
  nextTick(() => {
    initChart()
  })
})

onUnmounted(() => {
  if (resizeObserver.value) {
    resizeObserver.value.disconnect()
  }
  chartInstance.value?.dispose()
  chartInstance.value = null
})

defineExpose({
  resize: () => chartInstance.value?.resize()
})
</script>

<template>
  <div class="chart-container" :style="{ height }">
    <div v-if="loading" class="chart-loading">
      <Loading class="loading-icon" />
      <p>加载中...</p>
    </div>
    <div ref="chartRef" class="chart-content"></div>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.chart-content {
  width: 100%;
  height: 100%;
}

.chart-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(15, 15, 26, 0.8);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-icon {
  width: 32px;
  height: 32px;
  color: #FF6B35;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.chart-loading p {
  margin-top: 12px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}
</style>
