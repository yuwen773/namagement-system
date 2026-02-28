<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: [String, Object],
    default: null
  },
  trend: {
    type: String,
    default: null,
    validator: (value) => ['up', 'down', null].includes(value)
  },
  trendValue: {
    type: String,
    default: null
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'accent', 'success', 'warning', 'error'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  delay: {
    type: Number,
    default: 0
  }
})

const colorClasses = computed(() => {
  const colors = {
    primary: 'stat-card-primary',
    secondary: 'stat-card-secondary',
    accent: 'stat-card-accent',
    success: 'stat-card-success',
    warning: 'stat-card-warning',
    error: 'stat-card-error'
  }
  return colors[props.color] || colors.primary
})

const cardStyle = computed(() => ({
  animationDelay: `${props.delay}ms`
}))
</script>

<template>
  <div :class="['stat-card', colorClasses, { loading }]" :style="cardStyle">
    <div v-if="loading" class="stat-card-shimmer"></div>

    <div class="stat-card-header">
      <div v-if="icon" class="stat-card-icon">
        <component :is="icon" class="icon" />
      </div>
      <div class="stat-card-content">
        <div class="stat-card-value">{{ value }}</div>
        <div class="stat-card-label">{{ title }}</div>
      </div>
    </div>

    <div v-if="trend && trendValue" :class="['stat-card-trend', trend]">
      <component :is="trend === 'up' ? 'ArrowUp' : 'ArrowDown'" class="trend-icon" />
      <span>{{ trendValue }}</span>
    </div>

    <div class="stat-card-glow"></div>
  </div>
</template>

<style scoped>
.stat-card {
  background: var(--gradient-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-lg);
  position: relative;
  overflow: hidden;
  transition: all var(--transition-base);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
}

.stat-card-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
}

.stat-card-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  flex-shrink: 0;
}

.stat-card-primary .stat-card-icon {
  background: var(--gradient-primary);
}

.stat-card-secondary .stat-card-icon {
  background: var(--gradient-secondary);
}

.stat-card-accent .stat-card-icon {
  background: var(--gradient-accent);
}

.stat-card-success .stat-card-icon {
  background: rgba(6, 255, 165, 0.15);
  color: var(--status-success);
}

.stat-card-warning .stat-card-icon {
  background: rgba(255, 215, 0, 0.15);
  color: var(--status-warning);
}

.stat-card-error .stat-card-icon {
  background: rgba(255, 59, 48, 0.15);
  color: var(--status-error);
}

.stat-card-icon .icon {
  width: 24px;
  height: 24px;
  color: white;
}

.stat-card-content {
  flex: 1;
}

.stat-card-value {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: var(--space-xs);
}

.stat-card-label {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

.stat-card-trend {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-full);
  font-size: 0.8125rem;
  font-weight: 600;
}

.stat-card-trend.up {
  background: rgba(6, 255, 165, 0.1);
  color: var(--status-success);
}

.stat-card-trend.down {
  background: rgba(255, 59, 48, 0.1);
  color: var(--status-error);
}

.stat-card-trend .trend-icon {
  width: 14px;
  height: 14px;
}

.stat-card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.stat-card:hover .stat-card-glow {
  opacity: 1;
}

.stat-card-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 100%
  );
  transform: translateX(-100%);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  to {
    transform: translateX(100%);
  }
}

.stat-card.loading {
  pointer-events: none;
}
</style>
