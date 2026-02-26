<template>
  <div class="stat-card" :class="`stat-card-${variant}`">
    <div class="stat-card-content">
      <div class="stat-icon">
        <component :is="icon" />
      </div>
      <div class="stat-info">
        <div class="stat-label">{{ label }}</div>
        <div class="stat-value">
          <span class="stat-number">{{ displayValue }}</span>
          <span v-if="unit" class="stat-unit">{{ unit }}</span>
        </div>
      </div>
    </div>
    <div class="stat-decoration"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

interface Props {
  label: string
  value: number
  icon: any
  variant?: 'primary' | 'success' | 'warning' | 'danger'
  unit?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary'
})

const displayValue = ref(0)

// 数字滚动动画
const animateValue = (start: number, end: number, duration: number) => {
  const startTime = Date.now()
  const animate = () => {
    const now = Date.now()
    const progress = Math.min((now - startTime) / duration, 1)
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)
    displayValue.value = Math.floor(start + (end - start) * easeOutQuart)
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  requestAnimationFrame(animate)
}

watch(() => props.value, (newValue) => {
  animateValue(displayValue.value, newValue, 1000)
}, { immediate: true })

onMounted(() => {
  animateValue(0, props.value, 1500)
})
</script>

<style scoped>
.stat-card {
  position: relative;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-card-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
  transition: all 0.3s;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(5deg);
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.stat-unit {
  font-size: 14px;
  color: #909399;
  font-weight: 500;
}

.stat-decoration {
  position: absolute;
  right: -20px;
  bottom: -20px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  opacity: 0.05;
  transition: all 0.3s;
}

.stat-card:hover .stat-decoration {
  transform: scale(1.2);
  opacity: 0.08;
}

/* Primary variant */
.stat-card-primary .stat-icon {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
}

.stat-card-primary .stat-number {
  color: #8b4513;
}

.stat-card-primary .stat-decoration {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
}

/* Success variant */
.stat-card-success .stat-icon {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.stat-card-success .stat-number {
  color: #67c23a;
}

.stat-card-success .stat-decoration {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

/* Warning variant */
.stat-card-warning .stat-icon {
  background: linear-gradient(135deg, #e6a23c 0%, #f0b659 100%);
  color: white;
}

.stat-card-warning .stat-number {
  color: #e6a23c;
}

.stat-card-warning .stat-decoration {
  background: linear-gradient(135deg, #e6a23c 0%, #f0b659 100%);
}

/* Danger variant */
.stat-card-danger .stat-icon {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: white;
}

.stat-card-danger .stat-number {
  color: #f56c6c;
}

.stat-card-danger .stat-decoration {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}
</style>
