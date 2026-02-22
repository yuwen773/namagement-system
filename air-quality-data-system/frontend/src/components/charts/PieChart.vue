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
        item.hasOwnProperty('name') && item.hasOwnProperty('value')
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
  donut: {
    type: Boolean,
    default: false
  },
  radius: {
    type: [String, Array],
    default: () => ['0%', '75%']
  },
  position: {
    type: String,
    default: 'center'
  },
  showPercentage: {
    type: Boolean,
    default: true
  },
  colors: {
    type: Array,
    default: () => ['#0066CC', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#64748B']
  }
})

const emit = defineEmits(['chart-ready', 'chart-click'])

let chartInstance = null

const handleChartReady = (chart) => {
  chartInstance = chart
  emit('chart-ready', chart)
}

const total = computed(() => {
  return props.data.reduce((sum, item) => sum + item.value, 0)
})

const chartOption = computed(() => {
  const isDark = props.theme === 'dark'
  const textColor = isDark ? '#94A3B8' : '#64748B'
  const textMain = isDark ? '#F1F5F9' : '#1E293B'
  const borderColor = isDark ? '#1E293B' : '#fff'

  const radius = typeof props.radius === 'string'
    ? [props.donut ? '50%' : '0%', props.radius]
    : props.radius

  return {
    grid: {
      top: 0,
      left: 0,
      right: 0,
      bottom: 0
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const value = Number(params.value) || 0
        const totalVal = Number(total.value) || 1
        const percent = totalVal > 0 ? ((value / totalVal) * 100).toFixed(1) : '0.0'
        return `
          <div style="font-weight: 600; margin-bottom: 6px; color: ${textMain};">${params.name}</div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: ${param.color};"></span>
            <span style="color: ${textColor};">数量:</span>
            <span style="font-weight: 600; color: ${textMain};">${params.value}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
            <span style="width: 10px;"></span>
            <span style="color: ${textColor};">占比:</span>
            <span style="font-weight: 600; color: ${textMain};">${percent}%</span>
          </div>
        `
      }
    },
    legend: {
      show: true,
      orient: 'vertical',
      right: '5%',
      top: 'center',
      itemWidth: 14,
      itemHeight: 14,
      itemGap: 16,
      textStyle: {
        color: textColor,
        fontSize: 13
      },
      formatter: (name) => {
        const item = props.data.find(d => d.name === name)
        if (!item) return name
        const value = Number(item.value) || 0
        const totalVal = Number(total.value) || 1
        const percent = totalVal > 0 ? ((value / totalVal) * 100).toFixed(1) : '0.0'
        return `${name} ${percent}%`
      }
    },
    series: [{
      type: 'pie',
      radius,
      center: ['40%', '50%'],
      data: props.data.map((item, index) => ({
        ...item,
        itemStyle: {
          borderRadius: 6,
          borderColor: borderColor,
          borderWidth: 2,
          color: props.colors[index % props.colors.length]
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 12,
            shadowColor: props.colors[index % props.colors.length] + '60',
            shadowOffsetX: 0,
            shadowOffsetY: 0
          },
          scale: true,
          scaleSize: 8
        }
      })),
      label: {
        show: !props.donut,
        position: 'outside',
        color: textMain,
        fontSize: 13,
        fontWeight: 500,
        formatter: '{b}',
        distance: 10
      },
      labelLine: {
        show: !props.donut,
        length: 15,
        length2: 10,
        lineStyle: {
          color: isDark ? '#334155' : '#E2E8F0',
          width: 1.5
        }
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: '600'
        }
      }
    }],
    animationDuration: 800,
    animationEasing: 'cubicOut',
    animationDelay: (idx) => idx * 50
  }
})
</script>
