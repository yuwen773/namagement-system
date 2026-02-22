<template>
  <BaseChart
    :option="chartOption"
    :height="height"
    :theme="theme"
    :loading="loading"
    @chart-ready="handleChartReady"
    @chart-click="$emit('chart-click', $event)"
  />
</template>

<script setup>
import { computed } from 'vue'
import BaseChart from './BaseChart.vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  xAxis: {
    type: Array,
    required: true
  },
  height: {
    type: String,
    default: '400px'
  },
  theme: {
    type: String,
    default: 'light'
  },
  loading: {
    type: Boolean,
    default: false
  },
  smooth: {
    type: Boolean,
    default: true
  },
  areaStyle: {
    type: Boolean,
    default: false
  },
  showDataZoom: {
    type: Boolean,
    default: false
  },
  legend: {
    type: Array,
    default: () => []
  },
  colors: {
    type: Array,
    default: () => ['#0066CC', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
  },
  unit: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['chart-ready', 'chart-click'])

let chartInstance = null

const handleChartReady = (chart) => {
  chartInstance = chart
  emit('chart-ready', chart)
}

const chartOption = computed(() => {
  const isDark = props.theme === 'dark'
  const textColor = isDark ? '#94A3B8' : '#64748B'
  const gridColor = isDark ? '#1E293B' : '#F1F5F9'
  const axisColor = isDark ? '#334155' : '#E2E8F0'

  const series = props.data.map((item, index) => ({
    name: item.name || `系列${index + 1}`,
    type: 'line',
    data: item.values,
    smooth: props.smooth,
    symbol: 'circle',
    symbolSize: 6,
    lineStyle: {
      width: 2.5,
      cap: 'round'
    },
    itemStyle: {
      borderWidth: 2,
      borderColor: isDark ? '#1E293B' : '#fff'
    },
    emphasis: {
      focus: 'series',
      itemStyle: {
        symbolSize: 9,
        borderWidth: 3,
        shadowBlur: 8,
        shadowColor: props.colors[index % props.colors.length] + '40'
      }
    },
    areaStyle: props.areaStyle ? {
      opacity: 0.2,
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [{
          offset: 0,
          color: props.colors[index % props.colors.length] + '99'
        }, {
          offset: 1,
          color: props.colors[index % props.colors.length] + '10'
        }]
      }
    } : undefined,
    color: props.colors[index % props.colors.length]
  }))

  return {
    grid: {
      left: '3%',
      right: '4%',
      bottom: props.showDataZoom ? '15%' : '3%',
      top: props.legend?.length ? '15%' : '8%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line',
        lineStyle: {
          type: 'dashed',
          width: 1.5,
          color: isDark ? '#475569' : '#CBD5E1'
        }
      },
      formatter: (params) => {
        let result = `<div style="font-weight: 600; margin-bottom: 8px; color: ${isDark ? '#F1F5F9' : '#1E293B'};">${params[0].axisValue}</div>`
        params.forEach(param => {
          result += `
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
              <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: ${param.color};"></span>
              <span style="color: ${textColor};">${param.seriesName}:</span>
              <span style="font-weight: 600; color: ${isDark ? '#F1F5F9' : '#1E293B'};">${param.value}${props.unit}</span>
            </div>
          `
        })
        return result
      }
    },
    legend: props.legend?.length ? {
      data: props.legend,
      top: 0,
      itemWidth: 16,
      itemHeight: 16,
      itemGap: 16,
      textStyle: {
        color: textColor,
        fontSize: 13
      }
    } : undefined,
    xAxis: {
      type: 'category',
      data: props.xAxis,
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: axisColor
        }
      },
      axisLabel: {
        color: textColor,
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        show: false
      },
      axisLabel: {
        color: textColor,
        fontSize: 12,
        formatter: `{value}${props.unit}`
      },
      splitLine: {
        lineStyle: {
          color: gridColor,
          type: 'dashed'
        }
      }
    },
    dataZoom: props.showDataZoom ? [{
      type: 'inside',
      start: 0,
      end: 100
    }, {
      start: 0,
      end: 100,
      height: 20,
      bottom: 10,
      brushSelect: false,
      textStyle: {
        color: textColor,
        fontSize: 11
      },
      borderColor: 'transparent',
      backgroundColor: isDark ? '#1E293B' : '#F1F5F9',
      fillerColor: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [{
          offset: 0,
          color: props.colors[0] + '40'
        }, {
          offset: 1,
          color: props.colors[0] + '20'
        }]
      },
      handleStyle: {
        color: props.colors[0]
      }
    }] : undefined,
    series,
    animationDuration: 600,
    animationEasing: 'cubicOut'
  }
})
</script>
