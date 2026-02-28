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

// 清新自然风格配色
const natureColors = ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#00B4D8', '#90E0EF']

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
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      borderWidth: 1,
      textStyle: { color: '#1C1917', fontSize: 13 },
      formatter: (params) => {
        const param = params[0]
        const region = topRegions.value.find(r => r.region === param.name)
        return `
          <div style="padding: 8px;">
            <div style="font-weight: 600; margin-bottom: 8px; color: #1C1917;">${param.name}</div>
            <div style="color: #57534E;">商品数: ${region?.count || 0}</div>
            <div style="color: #57534E;">均价: ¥${region?.avg_price?.toFixed(2) || '0'}</div>
            <div style="color: #57534E;">均销量: ${Math.round(region?.avg_sales || 0)}</div>
            <div style="color: #57534E;">店铺数: ${region?.shop_count || 0}</div>
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
      axisLine: { lineStyle: { color: '#E7E5E4' } },
      axisLabel: { color: '#A8A29E' },
      splitLine: { lineStyle: { color: '#F5F5F4', type: 'dashed' } }
    },
    yAxis: {
      type: 'category',
      data: topRegions.value.map(r => r.region || '未分类'),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#57534E',
        fontSize: 12
      }
    },
    series: [{
      type: 'bar',
      data: topRegions.value.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: natureColors[index % natureColors.length] },
            { offset: 1, color: natureColors[(index + 1) % natureColors.length] }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '50%',
      label: {
        show: true,
        position: 'right',
        color: '#57534E',
        fontSize: 12,
        formatter: '{c}'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 15,
          shadowColor: 'rgba(45, 106, 79, 0.3)'
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
        <div class="header-icon-wrapper">
          <Location class="header-icon" />
        </div>
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Base Analysis - 清新自然风格
   ============================================ */
.region-analysis {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;

  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(45, 106, 79, 0.06);
}

.region-analysis:hover {
  box-shadow: 0 8px 30px rgba(45, 106, 79, 0.12);
  transform: translateY(-2px);
}

/* ============================================
   Section Header
   ============================================ */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, #F5F5F4 0%, transparent 100%);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon-wrapper {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.1), rgba(144, 224, 239, 0.08));
  border-radius: 10px;
  border: 1px solid rgba(0, 180, 216, 0.3);
}

.header-icon {
  width: 18px;
  height: 18px;
  color: var(--accent-blue);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.section-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-subtitle {
  font-family: 'Nunito', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-badge {
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.1), rgba(144, 224, 239, 0.08));
  border: 1px solid rgba(0, 180, 216, 0.3);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--accent-blue);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Chart Container
   ============================================ */
.chart-container {
  padding: 18px 22px;
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
  font-family: 'Noto Serif SC', serif;
  font-size: 13px;
  margin: 0;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .chart-container {
    padding: 16px 18px;
    min-height: 280px;
  }

  .chart-wrapper {
    height: 240px;
  }
}
</style>
