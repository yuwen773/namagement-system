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
    required: true,
    validator: (value) => {
      return value.every(item =>
        Array.isArray(item) && item.length >= 2
      )
    }
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
  xAxisName: {
    type: String,
    default: 'X 轴'
  },
  yAxisName: {
    type: String,
    default: 'Y 轴'
  },
  xAxisUnit: {
    type: String,
    default: ''
  },
  yAxisUnit: {
    type: String,
    default: ''
  },
  color: {
    type: String,
    default: '#0066CC'
  },
  showRegression: {
    type: Boolean,
    default: false
  },
  regressionData: {
    type: Array,
    default: () => []
  },
  symbolSize: {
    type: [Number, Function],
    default: 8
  },
  showLabels: {
    type: Boolean,
    default: false
  },
  labels: {
    type: Array,
    default: () => []
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
  const textMain = isDark ? '#F1F5F9' : '#1E293B'
  const gridColor = isDark ? '#1E293B' : '#F1F5F9'
  const axisColor = isDark ? '#334155' : '#E2E8F0'

  const series = [{
    name: '数据点',
    type: 'scatter',
    data: props.data,
    symbolSize: props.symbolSize,
    itemStyle: {
      color: props.color,
      borderColor: isDark ? '#1E293B' : '#fff',
      borderWidth: 2
    },
    emphasis: {
      focus: 'self',
      itemStyle: {
        shadowBlur: 10,
        shadowColor: props.color + '60',
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        borderWidth: 2
      },
      scale: true,
      scaleSize: 1.3
    },
    label: props.showLabels ? {
      show: true,
      position: 'top',
      formatter: (params) => {
        return props.labels[params.dataIndex] || ''
      },
      color: textColor,
      fontSize: 11
    } : undefined
  }]

  if (props.showRegression && props.regressionData.length >= 2) {
    series.push({
      name: '回归线',
      type: 'line',
      data: props.regressionData,
      lineStyle: {
        color: '#EF4444',
        width: 2,
        type: 'dashed'
      },
      symbol: 'none',
      emphasis: {
        disabled: true
      }
    })
  }

  return {
    grid: {
      left: '10%',
      right: '5%',
      bottom: '12%',
      top: '8%',
      containLabel: true
    },
    tooltip: {
      trigger: 'item',
      axisPointer: {
        type: 'cross',
        lineStyle: {
          color: isDark ? '#475569' : '#CBD5E1',
          type: 'dashed'
        }
      },
      formatter: (params) => {
        if (params.componentSubType === 'line') {
          return `<div style="font-weight: 600; color: ${textMain};">回归线</div>`
        }
        return `
          <div style="font-weight: 600; margin-bottom: 8px; color: ${textMain};">数据点 ${params.dataIndex + 1}</div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span style="color: ${textColor};">${props.xAxisName}:</span>
            <span style="font-weight: 600; color: ${textMain};">${params.value[0]}${props.xAxisUnit}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: ${textColor};">${props.yAxisName}:</span>
            <span style="font-weight: 600; color: ${textMain};">${params.value[1]}${props.yAxisUnit}</span>
          </div>
        `
      }
    },
    xAxis: {
      name: props.xAxisName,
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: {
        color: textColor,
        fontSize: 13,
        fontWeight: 500
      },
      type: 'value',
      scale: true,
      splitLine: {
        lineStyle: {
          color: gridColor,
          type: 'dashed'
        }
      },
      axisLine: {
        lineStyle: {
          color: axisColor
        }
      },
      axisLabel: {
        color: textColor,
        fontSize: 12,
        formatter: `{value}${props.xAxisUnit}`
      }
    },
    yAxis: {
      name: props.yAxisName,
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: {
        color: textColor,
        fontSize: 13,
        fontWeight: 500
      },
      type: 'value',
      scale: true,
      splitLine: {
        lineStyle: {
          color: gridColor,
          type: 'dashed'
        }
      },
      axisLine: {
        show: false
      },
      axisLabel: {
        color: textColor,
        fontSize: 12,
        formatter: `{value}${props.yAxisUnit}`
      }
    },
    series,
    animationDuration: 600,
    animationEasing: 'cubicOut'
  }
})
</script>
