<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { TrendCharts } from '@element-plus/icons-vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    required: true
  },
  data: {
    type: [Array, Object],
    default: null
  }
})

const chartRef = ref(null)
let chartInstance = null

// 清新自然风格配色
const natureColors = ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#00B4D8', '#90E0EF']

const initChart = () => {
  if (!chartRef.value || !props.data) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  let option = {}

  switch (props.type) {
    case 'price-distribution':
      option = getPriceDistributionOption()
      break
    case 'sales-distribution':
      option = getSalesDistributionOption()
      break
    case 'price-sales-correlation':
      option = getCorrelationOption()
      break
    default:
      option = {}
  }

  chartInstance.setOption(option)
}

const getPriceDistributionOption = () => {
  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      borderWidth: 1,
      textStyle: { color: '#1C1917', fontSize: 13 },
      formatter: '{b}<br/>数量: {c}<br/>占比: {d}%'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#57534E', fontSize: 12 },
      itemGap: 12
    },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 12,
        borderColor: '#FFFFFF',
        borderWidth: 3
      },
      label: {
        show: true,
        color: '#57534E',
        fontSize: 13,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold' },
        itemStyle: {
          shadowBlur: 20,
          shadowOffsetX: 0,
          shadowColor: 'rgba(45, 106, 79, 0.3)'
        }
      },
      labelLine: {
        lineStyle: { color: '#A8A29E' },
        smooth: 0.3,
        length: 15,
        length2: 10
      },
      data: props.data.map((item, index) => ({
        value: item.count,
        name: item.range,
        itemStyle: { color: natureColors[index % natureColors.length] }
      }))
    }]
  }
}

const getSalesDistributionOption = () => {
  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      borderWidth: 1,
      textStyle: { color: '#1C1917', fontSize: 13 }
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
      data: props.data.map(d => d.range),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#57534E',
        fontSize: 12
      }
    },
    series: [{
      type: 'bar',
      data: props.data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: natureColors[index % natureColors.length] },
            { offset: 1, color: natureColors[(index + 1) % natureColors.length] }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '60%',
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
}

const getCorrelationOption = () => {
  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      borderWidth: 1,
      textStyle: { color: '#1C1917', fontSize: 13 },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}<br/>商品数: ${param.value[1]}<br/>平均销量: ${param.value[2]}`
      }
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '10%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.data.map(d => d.price_range),
      axisLine: { lineStyle: { color: '#E7E5E4' } },
      axisLabel: {
        color: '#A8A29E',
        fontSize: 11,
        rotate: 30
      },
      splitLine: { show: false }
    },
    yAxis: [
      {
        type: 'value',
        name: '商品数',
        position: 'left',
        axisLine: { show: false },
        axisLabel: { color: '#A8A29E' },
        splitLine: { lineStyle: { color: '#F5F5F4' } }
      },
      {
        type: 'value',
        name: '平均销量',
        position: 'right',
        axisLine: { show: false },
        axisLabel: { color: '#A8A29E' },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: '商品数',
        type: 'bar',
        data: props.data.map(d => d.count),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(45, 106, 79, 0.8)' },
            { offset: 1, color: 'rgba(45, 106, 79, 0.3)' }
          ]),
          borderRadius: [8, 8, 0, 0]
        },
        barWidth: '40%'
      },
      {
        name: '平均销量',
        type: 'line',
        yAxisIndex: 1,
        data: props.data.map(d => d.avg_sales),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: '#00B4D8',
          shadowColor: 'rgba(0, 180, 216, 0.5)',
          shadowBlur: 10
        },
        itemStyle: {
          color: '#00B4D8',
          borderColor: '#fff',
          borderWidth: 2
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 180, 216, 0.4)' },
            { offset: 1, color: 'rgba(0, 180, 216, 0)' }
          ])
        }
      }
    ]
  }
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
  <div class="chart-section">
    <div class="section-header">
      <div class="header-left">
        <div class="header-icon-wrapper">
          <TrendCharts class="header-icon" />
        </div>
        <div class="header-text">
          <h3 class="section-title">{{ title }}</h3>
          <p class="section-subtitle">{{ subtitle }}</p>
        </div>
      </div>
      <div class="header-badge">数据可视化</div>
    </div>

    <div class="chart-container">
      <div v-if="data && data.length > 0" ref="chartRef" class="chart-wrapper"></div>
      <div v-else class="chart-empty">
        <div class="empty-icon">📊</div>
        <p class="empty-text">暂无数据</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Base Section - 清新自然风格
   ============================================ */
.chart-section {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
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

.chart-section:hover {
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
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.08));
  border-radius: 10px;
  border: 1px solid rgba(116, 198, 157, 0.2);
}

.header-icon {
  width: 18px;
  height: 18px;
  color: var(--primary-green);
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
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.08));
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--primary-green);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Chart Container
   ============================================ */
.chart-container {
  padding: 18px 22px;
  min-height: 350px;
  position: relative;
}

.chart-wrapper {
  width: 100%;
  height: 300px;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
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
  .section-header {
    padding: 16px 18px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .chart-container {
    padding: 16px 18px;
    min-height: 280px;
  }

  .chart-wrapper {
    height: 250px;
  }
}
</style>
