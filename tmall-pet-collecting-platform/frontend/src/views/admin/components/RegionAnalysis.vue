<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { Location } from '@element-plus/icons-vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const chartRef = ref(null)
let chartInstance = null

const topRegions = computed(() => {
  return props.data?.slice(0, 10) || []
})

const initChart = () => {
  if (!chartRef.value || !topRegions.value.length) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(15, 15, 26, 0.95)',
      borderColor: 'rgba(6, 255, 165, 0.3)',
      borderWidth: 1,
      textStyle: { color: '#fff', fontSize: 13 },
      formatter: (params) => {
        const param = params[0]
        const region = topRegions.value.find(r => r.region === param.name)
        return `
          <div style="padding: 8px;">
            <div style="font-weight: 600; margin-bottom: 8px;">${param.name}</div>
            <div>商品数: ${region?.count || 0}</div>
            <div>均价: ¥${region?.avg_price?.toFixed(2) || '0'}</div>
            <div>均销量: ${Math.round(region?.avg_sales || 0)}</div>
            <div>店铺数: ${region?.shop_count || 0}</div>
          </div>
        `
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: 'rgba(255,255,255,0.5)' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: topRegions.value.map(r => r.region || '未分类'),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 12
      }
    },
    series: [{
      type: 'bar',
      data: topRegions.value.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: 'rgba(6, 255, 165, 0.8)' },
            { offset: 0.5, color: 'rgba(6, 255, 165, 0.5)' },
            { offset: 1, color: 'rgba(6, 255, 165, 0.2)' }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '50%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(255,255,255,0.8)',
        fontSize: 12,
        formatter: '{c}'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 15,
          shadowColor: 'rgba(6, 255, 165, 0.4)'
        }
      }
    }]
  }

  chartInstance.setOption(option)
}

watch(() => props.data, () => {
  initChart()
}, { deep: true })

onMounted(() => {
  initChart()

  const resizeHandler = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }

  window.addEventListener('resize', resizeHandler)

  onUnmounted(() => {
    window.removeEventListener('resize', resizeHandler)
    if (chartInstance) {
      chartInstance.dispose()
    }
  })
})
</script>

<template>
  <div class="region-analysis">
    <div class="section-header">
      <div class="header-left">
        <Location class="header-icon" />
        <div class="header-text">
          <h3 class="section-title">地区分布</h3>
          <p class="section-subtitle">商品地区分布与热力分析</p>
        </div>
      </div>
      <div class="header-badge">TOP 10</div>
    </div>

    <div class="chart-container">
      <div v-if="topRegions.length > 0" ref="chartRef" class="chart-wrapper"></div>
      <div v-else class="chart-empty">
        <div class="empty-icon">🗺️</div>
        <p class="empty-text">暂无地区数据</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Base Analysis
   ============================================ */
.region-analysis {
  --primary-cyan: #06FFA5;
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);

  background: rgba(20, 20, 32, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.region-analysis:hover {
  border-color: rgba(6, 255, 165, 0.15);
  box-shadow: 0 10px 40px rgba(6, 255, 165, 0.08);
}

/* ============================================
   Section Header
   ============================================ */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  width: 22px;
  height: 22px;
  color: var(--primary-cyan);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.section-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-subtitle {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-badge {
  padding: 6px 14px;
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.2);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
  color: var(--primary-cyan);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Chart Container
   ============================================ */
.chart-container {
  padding: 20px 24px;
  min-height: 320px;
}

.chart-wrapper {
  width: 100%;
  height: 280px;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 280px;
  color: var(--text-tertiary);
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-text {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 13px;
  margin: 0;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .chart-container {
    padding: 18px 20px;
    min-height: 280px;
  }

  .chart-wrapper {
    height: 240px;
  }
}
</style>
