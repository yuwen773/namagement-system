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
  horizontal: {
    type: Boolean,
    default: false
  },
  stack: {
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
  },
  showValues: {
    type: Boolean,
    default: false
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
    type: 'bar',
    data: item.values,
    stack: props.stack ? 'total' : undefined,
    barMaxWidth: props.horizontal ? 40 : 60,
    itemStyle: {
      borderRadius: props.horizontal ? [0, 6, 6, 0] : [6, 6, 0, 0],
      color: props.colors[index % props.colors.length]
    },
    emphasis: {
      focus: 'series',
      itemStyle: {
        shadowBlur: 8,
        shadowColor: props.colors[index % props.colors.length] + '40',
        shadowOffsetX: 0,
        shadowOffsetY: 2
      }
    },
    label: props.showValues ? {
      show: true,
      position: props.horizontal ? 'right' : 'top',
      color: textColor,
      fontSize: 12,
      fontWeight: 500,
      formatter: `{c}${props.unit}`
    } : undefined
  }))

  const categoryAxis = {
    type: 'category',
    data: props.xAxis,
    axisLine: {
      lineStyle: {
        color: axisColor
      }
    },
    axisLabel: {
      color: textColor,
      fontSize: 12,
      interval: 0,
      rotate: props.horizontal ? 0 : (props.xAxis.length > 10 ? 45 : 0)
    }
  }

  const valueAxis = {
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
  }

  return {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: props.legend?.length ? '12%' : '5%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        let result = `<div style="font-weight: 600; margin-bottom: 8px; color: ${isDark ? '#F1F5F9' : '#1E293B'};">${params[0].axisValue}</div>`
        params.forEach(param => {
          result += `
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
              <span style="display: inline-block; width: 10px; height: 10px; border-radius: 2px; background: ${param.color};"></span>
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
    xAxis: props.horizontal ? valueAxis : categoryAxis,
    yAxis: props.horizontal ? categoryAxis : valueAxis,
    series,
    animationDuration: 600,
    animationEasing: 'cubicOut'
  }
})
</script>
