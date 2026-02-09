<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
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
  const colors = ['#FF6B35', '#FF8C42', '#FFAD5D', '#7B2CBF', '#9D4EDD', '#C77DFF']

  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 15, 26, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      borderWidth: 1,
      textStyle: { color: '#fff', fontSize: 13 },
      formatter: '{b}<br/>数量: {c}<br/>占比: {d}%'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: 'rgba(255,255,255,0.7)', fontSize: 12 },
      itemGap: 12
    },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 12,
        borderColor: '#0f0f1a',
        borderWidth: 3
      },
      label: {
        show: true,
        color: 'rgba(255,255,255,0.8)',
        fontSize: 13,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold' },
        itemStyle: {
          shadowBlur: 20,
          shadowOffsetX: 0,
          shadowColor: 'rgba(255, 107, 53, 0.5)'
        }
      },
      labelLine: {
        lineStyle: { color: 'rgba(255,255,255,0.3)' },
        smooth: 0.3,
        length: 15,
        length2: 10
      },
      data: props.data.map((item, index) => ({
        value: item.count,
        name: item.range,
        itemStyle: { color: colors[index % colors.length] }
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
      backgroundColor: 'rgba(15, 15, 26, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      borderWidth: 1,
      textStyle: { color: '#fff', fontSize: 13 }
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
      data: props.data.map(d => d.range),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 12
      }
    },
    series: [{
      type: 'bar',
      data: props.data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: index % 2 === 0 ? '#7B2CBF' : '#FF6B35' },
            { offset: 0.5, color: index % 2 === 0 ? '#9D4EDD' : '#FF8C42' },
            { offset: 1, color: index % 2 === 0 ? '#C77DFF' : '#FFAD5D' }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '60%',
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
          shadowColor: 'rgba(255, 107, 53, 0.4)'
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
      backgroundColor: 'rgba(15, 15, 26, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      borderWidth: 1,
      textStyle: { color: '#fff', fontSize: 13 },
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
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
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
        axisLabel: { color: 'rgba(255,255,255,0.5)' },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
      },
      {
        type: 'value',
        name: '平均销量',
        position: 'right',
        axisLine: { show: false },
        axisLabel: { color: 'rgba(255,255,255,0.5)' },
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
            { offset: 0, color: 'rgba(123, 44, 191, 0.8)' },
            { offset: 1, color: 'rgba(123, 44, 191, 0.3)' }
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
          color: '#FF6B35',
          shadowColor: 'rgba(255, 107, 53, 0.5)',
          shadowBlur: 10
        },
        itemStyle: {
          color: '#FF6B35',
          borderColor: '#fff',
          borderWidth: 2
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 107, 53, 0.4)' },
            { offset: 1, color: 'rgba(255, 107, 53, 0)' }
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
        <TrendCharts class="header-icon" />
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
.chart-section {
  background: rgba(15, 15, 26, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.chart-section:hover {
  border-color: rgba(255, 107, 53, 0.15);
  box-shadow: 0 10px 40px rgba(255, 107, 53, 0.1);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #FF6B35;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-family: 'Exo 2', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
}

.section-subtitle {
  font-family: 'Exo 2', sans-serif;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.header-badge {
  padding: 8px 16px;
  background: linear-gradient(135deg,
    rgba(255, 107, 53, 0.15),
    rgba(123, 44, 191, 0.15));
  border: 1px solid rgba(255, 107, 53, 0.25);
  border-radius: 20px;
  font-family: 'Exo 2', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #FF6B35;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.chart-container {
  padding: 24px;
  min-height: 400px;
  position: relative;
}

.chart-wrapper {
  width: 100%;
  height: 350px;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 350px;
  color: rgba(255, 255, 255, 0.3);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-family: 'Exo 2', sans-serif;
  font-size: 14px;
  margin: 0;
}

@media (max-width: 768px) {
  .section-header {
    padding: 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .chart-container {
    padding: 20px;
    min-height: 350px;
  }

  .chart-wrapper {
    height: 300px;
  }
}
</style>
