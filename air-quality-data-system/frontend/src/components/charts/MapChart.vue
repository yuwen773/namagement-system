<template>
  <BaseChart
    :option="chartOption"
    :height="height"
    :theme="theme"
    :loading="loading || mapLoading"
    @chart-ready="handleMapReady"
    @chart-click="$emit('chart-click', $event)"
  />
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import BaseChart from './BaseChart.vue'
import { registerMap } from 'echarts/core'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
    validator: (value) => {
      // Allow empty array
      if (!Array.isArray(value) || value.length === 0) {
        return true
      }
      // Check each item has required properties
      return value.every(item => {
        return item && typeof item === 'object' && 'name' in item && 'value' in item
      })
    }
  },
  height: {
    type: String,
    default: '600px'
  },
  theme: {
    type: String,
    default: 'light'
  },
  loading: {
    type: Boolean,
    default: false
  },
  mapType: {
    type: String,
    default: 'china'
  },
  roam: {
    type: Boolean,
    default: true
  },
  zoom: {
    type: Number,
    default: 1.2
  },
  center: {
    type: Array,
    default: () => [104.114129, 37.550339]
  },
  visualMin: {
    type: Number,
    default: 0
  },
  visualMax: {
    type: Number,
    default: 500
  }
})

const emit = defineEmits(['chart-ready', 'chart-click'])

let chartInstance = null
const mapRegistered = ref(false)
const mapLoading = ref(true)

// AQI level colors for visual map (Commercial colors)
const aqiLevels = [
  { value: 50, color: '#10B981', label: '优' },
  { value: 100, color: '#F59E0B', label: '良' },
  { value: 150, color: '#F97316', label: '轻度污染' },
  { value: 200, color: '#EF4444', label: '中度污染' },
  { value: 300, color: '#A855F7', label: '重度污染' },
  { value: 500, color: '#DC2626', label: '严重污染' }
]

const visualMapPieces = computed(() => {
  return aqiLevels.map((level, index) => {
    const prevMax = index > 0 ? aqiLevels[index - 1].value : 0
    return {
      min: prevMax + (index === 0 ? 0 : 1),
      max: level.value,
      label: level.label,
      color: level.color
    }
  })
})

const chartOption = computed(() => {
  // Don't render chart until map is registered
  if (!mapRegistered.value) {
    return {}
  }

  const isDark = props.theme === 'dark'
  const textColor = isDark ? '#94A3B8' : '#64748B'
  const textMain = isDark ? '#F1F5F9' : '#1E293B'
  const mapBgColor = isDark ? '#1E293B' : '#F1F5F9'
  const mapBorderColor = isDark ? '#334155' : '#E2E8F0'
  const hoverColor = '#0EA5E9'

  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (!params.value) return `<div style="font-weight: 600;">${params.name}</div><div style="color: ${textColor};">暂无数据</div>`

        const aqiLevel = getAQILevel(params.value)
        return `
          <div style="font-weight: 600; margin-bottom: 8px; color: ${textMain};">${params.name}</div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span style="display: inline-block; width: 12px; height: 12px; border-radius: 2px; background: ${aqiLevel.color};"></span>
            <span style="color: ${textColor};">AQI:</span>
            <span style="font-weight: 600; color: ${textMain}; font-size: 16px;">${params.value}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="width: 12px;"></span>
            <span style="color: ${textColor};">等级:</span>
            <span style="font-weight: 600; color: ${aqiLevel.color};">${aqiLevel.label}</span>
          </div>
        `
      }
    },
    visualMap: {
      min: props.visualMin,
      max: props.visualMax,
      left: '20',
      bottom: '20',
      text: ['高', '低'],
      calculable: true,
      inRange: {
        color: aqiLevels.map(level => level.color)
      },
      textStyle: {
        color: textColor,
        fontSize: 12
      },
      pieces: visualMapPieces.value,
      show: true
    },
    geo: {
      map: props.mapType,
      roam: props.roam,
      zoom: props.zoom,
      center: props.center,
      label: {
        show: false,
        color: textColor
      },
      emphasis: {
        label: {
          show: true,
          color: textMain
        },
        itemStyle: {
          areaColor: hoverColor,
          shadowBlur: 8,
          shadowColor: 'rgba(0, 0, 0, 0.3)'
        }
      },
      itemStyle: {
        areaColor: mapBgColor,
        borderColor: mapBorderColor,
        borderWidth: 1
      }
    },
    series: [{
      type: 'map',
      map: props.mapType,
      geoIndex: 0,
      data: props.data.map(item => ({
        name: item.name,
        value: item.value,
        itemStyle: {
          areaColor: getAQIColor(item.value)
        }
      })),
      emphasis: {
        label: {
          show: true
        },
        itemStyle: {
          shadowBlur: 8,
          shadowColor: 'rgba(0, 0, 0, 0.3)'
        }
      }
    }],
    animationDuration: 800,
    animationEasing: 'cubicOut'
  }
})

function getAQIColor(aqi) {
  for (const level of aqiLevels) {
    if (aqi <= level.value) {
      return level.color
    }
  }
  return aqiLevels[aqiLevels.length - 1].color
}

function getAQILevel(aqi) {
  for (const level of aqiLevels) {
    if (aqi <= level.value) {
      return level
    }
  }
  return aqiLevels[aqiLevels.length - 1]
}

async function loadChinaMap() {
  try {
    // Using a reliable China GeoJSON source
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    const geoJson = await response.json()
    registerMap('china', geoJson)
    mapRegistered.value = true
  } catch (error) {
    console.error('Failed to load China map:', error)
  }
}

const handleMapReady = async (chart) => {
  chartInstance = chart
  if (mapRegistered.value) {
    emit('chart-ready', chart)
  }
}

// Load map on component mount
onMounted(async () => {
  mapLoading.value = true
  await loadChinaMap()
  mapLoading.value = false
})

watch(() => props.mapType, async () => {
  mapRegistered.value = false
  if (chartInstance) {
    chartInstance.showLoading()
    await loadChinaMap()
    chartInstance.hideLoading()
  }
})
</script>

<style scoped>
:deep(.canvas-container) {
  position: relative;
}
</style>
