<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: null
  },
  icon: {
    type: [String, Object],
    default: null
  },
  option: {
    type: Object,
    default: () => ({})
  },
  height: {
    type: String,
    default: '400px'
  },
  loading: {
    type: Boolean,
    default: false
  },
  actions: {
    type: Array,
    default: () => []
  },
  badge: {
    type: String,
    default: null
  },
  badgeColor: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'error'].includes(value)
  }
})

const emit = defineEmits(['action'])

const chartRef = ref(null)
const chartInstance = ref(null)

const hasValidOption = (opt) => {
  return opt && typeof opt === 'object' && Object.keys(opt).length > 0 && opt.grid && opt.xAxis && opt.yAxis && opt.series
}

const initOrUpdateChart = () => {
  if (!chartRef.value || !hasValidOption(props.option)) return

  if (!chartInstance.value) {
    chartInstance.value = echarts.init(chartRef.value)
  }

  try {
    chartInstance.value.setOption({
      backgroundColor: 'transparent',
      ...props.option
    }, true)
  } catch (error) {
    // 忽略 ECharts 配置错误
  }
}

const handleResize = () => {
  chartInstance.value?.resize()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance.value) {
    chartInstance.value.dispose()
    chartInstance.value = null
  }
})

// 监听 option 变化
watch(() => props.option, (newOption) => {
  if (hasValidOption(newOption)) {
    nextTick(() => {
      initOrUpdateChart()
    })
  }
}, { deep: true })

// 监听 loading 变化，当加载完成后初始化图表
watch(() => props.loading, (isLoading) => {
  if (!isLoading && hasValidOption(props.option)) {
    nextTick(() => {
      initOrUpdateChart()
    })
  }
})

// 监听 chartRef 变化
watch(chartRef, (newRef) => {
  if (newRef && hasValidOption(props.option) && !chartInstance.value) {
    nextTick(() => {
      initOrUpdateChart()
    })
  }
})

const handleAction = (action) => {
  emit('action', action)
}
</script>

<template>
  <div class="data-panel">
    <div class="data-panel-header">
      <div class="data-panel-title-group">
        <div v-if="icon" class="data-panel-icon">
          <component :is="icon" class="icon" />
        </div>
        <div>
          <h3 class="data-panel-title">{{ title }}</h3>
          <p v-if="subtitle" class="data-panel-subtitle">{{ subtitle }}</p>
        </div>
      </div>

      <div class="data-panel-header-right">
        <div v-if="badge" :class="['data-panel-badge', `badge-${badgeColor}`]">
          {{ badge }}
        </div>
        <div v-if="actions.length > 0" class="data-panel-actions">
          <button
            v-for="action in actions"
            :key="action.key"
            :class="['action-btn', action.type || 'default']"
            @click="handleAction(action.key)"
          >
            <component v-if="action.icon" :is="action.icon" class="action-icon" />
            <span v-if="action.label">{{ action.label }}</span>
          </button>
        </div>
      </div>
    </div>

    <div class="data-panel-body">
      <div v-if="loading" class="data-panel-loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      <div
        v-else
        ref="chartRef"
        class="data-panel-chart"
        :style="{ height }"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.data-panel {
  background: var(--gradient-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all var(--transition-base);
}

.data-panel:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-md);
}

.data-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg) var(--space-lg) var(--space-md);
  border-bottom: 1px solid var(--border-subtle);
}

.data-panel-title-group {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.data-panel-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.data-panel-icon .icon {
  width: 20px;
  height: 20px;
  color: white;
}

.data-panel-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.data-panel-subtitle {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  margin: var(--space-xs) 0 0 0;
}

.data-panel-header-right {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.data-panel-badge {
  padding: var(--space-xs) var(--space-sm);
  font-family: var(--font-display);
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: var(--radius-full);
}

.data-panel-badge.badge-primary {
  background: rgba(255, 107, 53, 0.15);
  color: var(--neon-orange);
  border: 1px solid rgba(255, 107, 53, 0.3);
}

.data-panel-badge.badge-success {
  background: rgba(6, 255, 165, 0.15);
  color: var(--status-success);
  border: 1px solid rgba(6, 255, 165, 0.3);
}

.data-panel-badge.badge-warning {
  background: rgba(255, 215, 0, 0.15);
  color: var(--status-warning);
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.data-panel-badge.badge-error {
  background: rgba(255, 59, 48, 0.15);
  color: var(--status-error);
  border: 1px solid rgba(255, 59, 48, 0.3);
}

.data-panel-actions {
  display: flex;
  gap: var(--space-xs);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  background: transparent;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--bg-elevated);
  border-color: var(--neon-cyan);
  color: var(--text-primary);
}

.action-btn.primary {
  background: var(--gradient-primary);
  border-color: transparent;
  color: white;
}

.action-btn.primary:hover {
  opacity: 0.9;
}

.action-icon {
  width: 14px;
  height: 14px;
}

.data-panel-body {
  padding: var(--space-md) var(--space-lg) var(--space-lg);
  position: relative;
}

.data-panel-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(10, 10, 18, 0.8);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-default);
  border-top-color: var(--neon-orange);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.data-panel-loading p {
  margin-top: var(--space-md);
  font-size: 0.875rem;
  color: var(--text-tertiary);
}

.data-panel-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-tertiary);
  font-size: 0.875rem;
}

.data-panel-chart {
  width: 100%;
}

@media (max-width: 768px) {
  .data-panel-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-md);
  }

  .data-panel-header-right {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
