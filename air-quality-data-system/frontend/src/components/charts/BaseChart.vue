<template>
  <div
    ref="chartContainer"
    class="base-chart"
    :style="{ height: props.height || '400px', width: '100%' }"
  />
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  option: {
    type: Object,
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
  }
})

const emit = defineEmits(['chart-ready', 'chart-click'])

const chartContainer = ref(null)
let chartInstance = null
let resizeObserver = null

// Commercial SaaS Theme
const commercialTheme = {
  light: {
    backgroundColor: 'transparent',
    textStyle: {
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    },
    title: {
      textStyle: {
        color: '#1E293B',
        fontWeight: 600
      }
    },
    legend: {
      textStyle: {
        color: '#475569'
      }
    },
    categoryAxis: {
      axisLine: {
        lineStyle: {
          color: '#E2E8F0'
        }
      },
      axisLabel: {
        color: '#64748B',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: '#F1F5F9',
          type: 'dashed'
        }
      }
    },
    valueAxis: {
      axisLine: {
        show: false
      },
      axisLabel: {
        color: '#64748B',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: '#F1F5F9',
          type: 'dashed'
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.98)',
      borderColor: '#E2E8F0',
      borderWidth: 1,
      textStyle: {
        color: '#1E293B',
        fontSize: 13
      },
      padding: [12, 16],
      extraCssText: 'backdrop-filter: blur(8px); border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'
    }
  },
  dark: {
    backgroundColor: 'transparent',
    textStyle: {
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    },
    title: {
      textStyle: {
        color: '#F1F5F9',
        fontWeight: 600
      }
    },
    legend: {
      textStyle: {
        color: '#94A3B8'
      }
    },
    categoryAxis: {
      axisLine: {
        lineStyle: {
          color: '#334155'
        }
      },
      axisLabel: {
        color: '#94A3B8',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: '#1E293B',
          type: 'dashed'
        }
      }
    },
    valueAxis: {
      axisLine: {
        show: false
      },
      axisLabel: {
        color: '#94A3B8',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: '#1E293B',
          type: 'dashed'
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(30, 41, 59, 0.98)',
      borderColor: '#334155',
      borderWidth: 1,
      textStyle: {
        color: '#F1F5F9',
        fontSize: 13
      },
      padding: [12, 16],
      extraCssText: 'backdrop-filter: blur(8px); border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'
    }
  }
}

// Commercial color palette
const commercialColors = {
  primary: '#0066CC',
  primaryLight: '#3385D6',
  primaryDark: '#0052A3',
  secondary: '#64748B',
  accent: '#0EA5E9',
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6'
}

// AQI color levels (used for air quality data)
const aqiColors = {
  excellent: '#10B981',    // 0-50    优
  good: '#F59E0B',         // 51-100  良
  lightPollution: '#F97316', // 101-150 轻度污染
  moderate: '#EF4444',     // 151-200 中度污染
  heavy: '#A855F7',        // 201-300 重度污染
  severe: '#DC2626'        // 301-500 严重污染
}

const initChart = () => {
  if (!chartContainer.value) return

  chartInstance = echarts.init(chartContainer.value, null, {
    renderer: 'canvas',
    ...commercialTheme[props.theme]
  })

  chartInstance.setOption(props.option, true)

  chartInstance.on('click', (params) => {
    emit('chart-click', params)
  })

  emit('chart-ready', chartInstance)
}

const updateChart = () => {
  if (!chartInstance) return
  chartInstance.setOption(props.option, true)
}

const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

const showLoading = () => {
  if (chartInstance) {
    chartInstance.showLoading({
      text: '',
      color: props.theme === 'dark' ? '#0EA5E9' : '#0066CC',
      textColor: props.theme === 'dark' ? '#94A3B8' : '#64748B',
      maskColor: props.theme === 'dark' ? 'rgba(30, 41, 59, 0.4)' : 'rgba(255, 255, 255, 0.6)',
      zlevel: 0
    })
  }
}

const hideLoading = () => {
  if (chartInstance) {
    chartInstance.hideLoading()
  }
}

watch(() => props.option, updateChart, { deep: true })
watch(() => props.theme, () => {
  if (chartInstance) {
    chartInstance.dispose()
    initChart()
  }
})
watch(() => props.loading, (loading) => {
  if (loading) {
    showLoading()
  } else {
    hideLoading()
  }
})

onMounted(() => {
  nextTick(() => {
    initChart()
    if (props.loading) {
      showLoading()
    }

    resizeObserver = new ResizeObserver(() => {
      resizeChart()
    })
    if (chartContainer.value) {
      resizeObserver.observe(chartContainer.value)
    }
  })
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})

defineExpose({
  chartInstance,
  resize: resizeChart,
  showLoading,
  hideLoading,
  commercialColors,
  aqiColors
})
</script>

<style scoped>
.base-chart {
  position: relative;
  overflow: hidden;
}
</style>
