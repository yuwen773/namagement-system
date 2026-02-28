<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  metric: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="metric-card" :style="{ '--metric-color': metric.color }">
    <div class="card-background">
      <div class="gradient-orb" :class="metric.gradient"></div>
      <div class="grid-pattern"></div>
    </div>

    <div class="card-content">
      <div class="icon-wrapper">
        <component :is="metric.icon" class="icon" />
      </div>

      <div class="metric-info">
        <p class="metric-label">{{ metric.label }}</p>
        <p class="metric-value">{{ metric.value }}</p>
        <p class="metric-detail">{{ metric.detail }}</p>
      </div>
    </div>

    <div class="card-border"></div>
    <div class="card-glow"></div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Base Card
   ============================================ */
.metric-card {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);

  position: relative;
  background: rgba(20, 20, 32, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: metricSlideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: calc(var(--i) * 0.1s);
}

@keyframes metricSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0;
  transition: opacity 0.3s ease;
  background: linear-gradient(90deg, var(--metric-color), transparent);
}

.metric-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.1);
}

.metric-card:hover::before {
  opacity: 1;
}

/* ============================================
   Card Background
   ============================================ */
.card-background {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  right: -50%;
  border-radius: 50%;
  opacity: 0.08;
  filter: blur(60px);
  transition: all 0.6s ease;
}

.metric-card:hover .gradient-orb {
  opacity: 0.15;
  transform: scale(1.1);
}

.from-orange-500 {
  background: radial-gradient(circle, #FF6B35 0%, transparent 70%);
}

.from-purple-500 {
  background: radial-gradient(circle, #7B2CBF 0%, transparent 70%);
}

.from-yellow-400 {
  background: radial-gradient(circle, #FFD700 0%, transparent 70%);
}

.from-emerald-400 {
  background: radial-gradient(circle, #06FFA5 0%, transparent 70%);
}

.from-pink-500 {
  background: radial-gradient(circle, #FF4785 0%, transparent 70%);
}

.from-cyan-400 {
  background: radial-gradient(circle, #4CC9F0 0%, transparent 70%);
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.5;
}

/* ============================================
   Card Content
   ============================================ */
.card-content {
  position: relative;
  z-index: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.metric-card:hover .icon-wrapper {
  transform: scale(1.05);
  border-color: var(--metric-color);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.icon {
  width: 22px;
  height: 22px;
  color: var(--metric-color);
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.metric-label {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-tertiary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-detail {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
}

/* ============================================
   Card Border & Glow
   ============================================ */
.card-border {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  padding: 1px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.02) 50%,
    rgba(255, 255, 255, 0.05) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.card-glow {
  position: absolute;
  bottom: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 100%;
  background: radial-gradient(ellipse at center,
    var(--metric-color) 0%,
    transparent 70%);
  opacity: 0;
  filter: blur(40px);
  transition: all 0.4s ease;
  pointer-events: none;
}

.metric-card:hover .card-glow {
  opacity: 0.2;
  bottom: -30%;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .card-content {
    padding: 18px;
  }

  .metric-value {
    font-size: 22px;
  }

  .icon-wrapper {
    width: 42px;
    height: 42px;
  }

  .icon {
    width: 20px;
    height: 20px;
  }
}
</style>
