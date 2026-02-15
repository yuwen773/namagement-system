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
  value: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 500
  },
  height: {
    type: String,
    default: '300px'
  },
  theme: {
    type: String,
    default: 'light'
  },
  loading: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'AQI 指数'
  },
  showDetail: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

const emit = defineEmits(['chart-ready', 'chart-click'])

let chartInstance = null

const handleChartReady = (chart) => {
  chartInstance = chart
  emit('chart-ready', chart)
}

// AQI level definitions (Commercial colors)
const aqiLevels = [
  { max: 50, label: '优', color: '#10B981', description: '空气质量令人满意，基本无空气污染' },
  { max: 100, label: '良', color: '#F59E0B', description: '空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响' },
  { max: 150, label: '轻度污染', color: '#F97316', description: '易感人群症状有轻度加剧，健康人群出现刺激症状' },
  { max: 200, label: '中度污染', color: '#EF4444', description: '进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响' },
  { max: 300, label: '重度污染', color: '#A855F7', description: '心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状' },
  { max: 500, label: '严重污染', color: '#DC2626', description: '健康人群运动耐受力降低，有强烈症状，提前出现某些疾病' }
]

const currentLevel = computed(() => {
  for (const level of aqiLevels) {
    if (props.value <= level.max) {
      return level
    }
  }
  return aqiLevels[aqiLevels.length - 1]
})

const sizeConfig = computed(() => {
  switch (props.size) {
    case 'small':
      return { radius: '75%', center: ['50%', '55%'], titleSize: 13, valueSize: 22 }
    case 'large':
      return { radius: '90%', center: ['50%', '50%'], titleSize: 17, valueSize: 34 }
    default:
      return { radius: '85%', center: ['50%', '52%'], titleSize: 15, valueSize: 30 }
  }
})

const chartOption = computed(() => {
  const isDark = props.theme === 'dark'
  const textColor = isDark ? '#94A3B8' : '#64748B'
  const textMain = isDark ? '#F1F5F9' : '#1E293B'
  const axisColor = isDark ? '#334155' : '#E2E8F0'

  const config = sizeConfig.value

  return {
    grid: {
      top: 0,
      left: 0,
      right: 0,
      bottom: 0
    },
    tooltip: {
      trigger: 'item',
      formatter: () => `
        <div style="font-weight: 600; margin-bottom: 8px; color: ${currentLevel.value.color};">${currentLevel.value.label}</div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
          <span style="color: ${textColor};">AQI:</span>
          <span style="font-weight: 600; color: ${textMain};">${props.value}</span>
        </div>
        <div style="font-size: 12px; color: ${textColor}; margin-top: 8px; max-width: 200px;">${currentLevel.value.description}</div>
      `
    },
    series: [
      // Progress ring (background)
      {
        type: 'gauge',
        radius: config.radius,
        center: config.center,
        startAngle: 200,
        endAngle: -20,
        splitNumber: 50,
        axisLine: {
          lineStyle: {
            color: [[1, {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: aqiLevels.map((level, index) => ({
                offset: (index + 1) / aqiLevels.length,
                color: level.color + '40'
              }))
            }]],
            width: 22
          }
        },
        axisLabel: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        detail: { show: false },
        pointer: { show: false }
      },
      // Main gauge
      {
        type: 'gauge',
        radius: config.radius,
        center: config.center,
        startAngle: 200,
        endAngle: -20,
        min: 0,
        max: 500,
        splitNumber: 5,
        itemStyle: {
          color: currentLevel.value.color,
          shadowColor: currentLevel.value.color + '60',
          shadowBlur: 8,
          shadowOffsetX: 0,
          shadowOffsetY: 2
        },
        progress: {
          show: true,
          roundCap: true,
          width: 22,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: currentLevel.value.color + '60' },
                { offset: 0.5, color: currentLevel.value.color + 'cc' },
                { offset: 1, color: currentLevel.value.color }
              ]
            }
          }
        },
        pointer: {
          icon: 'path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z',
          length: '75%',
          width: 14,
          offsetCenter: [0, '5%']
        },
        axisLine: {
          lineStyle: {
            width: 22,
            color: [[1, {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: aqiLevels.map((level, index) => ({
                offset: (index + 1) / aqiLevels.length,
                color: level.color + '20'
              }))
            }]]
          }
        },
        axisTick: {
          distance: -28,
          length: 6,
          lineStyle: {
            color: axisColor,
            width: 2
          }
        },
        splitLine: {
          distance: -32,
          length: 12,
          lineStyle: {
            color: axisColor,
            width: 2
          }
        },
        axisLabel: {
          distance: -45,
          color: textColor,
          fontSize: 11,
          fontWeight: 500,
          formatter: (value) => {
            const level = aqiLevels.find(l => value === l.max)
            return level ? level.label : ''
          }
        },
        title: {
          offsetCenter: [0, '20%'],
          fontSize: config.titleSize,
          color: textColor,
          fontWeight: 500
        },
        detail: {
          valueAnimation: true,
          offsetCenter: [0, '0%'],
          fontSize: config.valueSize,
          fontWeight: '700',
          formatter: '{value}',
          color: textMain
        },
        data: [{ value: props.value, name: props.title }]
      }
    ],
    animationDuration: 900,
    animationEasing: 'cubicOut'
  }
})
</script>
