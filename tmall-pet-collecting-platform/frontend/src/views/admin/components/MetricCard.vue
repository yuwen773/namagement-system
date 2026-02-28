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
      <div class="gradient-orb"></div>
      <div class="leaf-decoration">
        <svg viewBox="0 0 60 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M30 5C30 5 50 20 50 40C50 60 40 70 30 70C20 70 10 60 10 40C10 20 30 5 30 5Z" fill="currentColor" opacity="0.08"/>
        </svg>
      </div>
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
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Base Card - 清新自然风格
   ============================================ */
.metric-card {
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;

  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.08);
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
  border-radius: 20px 20px 0 0;
}

.metric-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 35px rgba(45, 106, 79, 0.15);
  border-color: var(--metric-color);
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
  width: 150%;
  height: 150%;
  top: -25%;
  right: -25%;
  border-radius: 50%;
  opacity: 0.05;
  filter: blur(50px);
  background: radial-gradient(circle, var(--metric-color) 0%, transparent 70%);
  transition: all 0.6s ease;
}

.metric-card:hover .gradient-orb {
  opacity: 0.1;
  transform: scale(1.1);
}

.leaf-decoration {
  position: absolute;
  bottom: -10px;
  right: -10px;
  width: 70px;
  height: 90px;
  color: var(--metric-color);
  opacity: 0.15;
  transition: all 0.4s ease;
  pointer-events: none;
}

.metric-card:hover .leaf-decoration {
  transform: scale(1.1) rotate(5deg);
  opacity: 0.25;
}

/* ============================================
   Card Content
   ============================================ */
.card-content {
  position: relative;
  z-index: 1;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.icon-wrapper {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.08), rgba(116, 198, 157, 0.05));
  border-radius: 16px;
  border: 1px solid rgba(116, 198, 157, 0.2);
  transition: all 0.3s ease;
}

.metric-card:hover .icon-wrapper {
  transform: scale(1.08) rotate(3deg);
  background: linear-gradient(135deg, var(--metric-color) 15%, rgba(116, 198, 157, 0.1) 100%);
  border-color: var(--metric-color);
  box-shadow: 0 8px 25px rgba(45, 106, 79, 0.2);
}

.icon {
  width: 24px;
  height: 24px;
  color: var(--metric-color);
  transition: color 0.3s ease;
}

.metric-card:hover .icon {
  color: white;
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-label {
  font-family: 'Nunito', sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: var(--metric-color);
  margin: 0;
  line-height: 1;
  transition: all 0.3s ease;
}

.metric-card:hover .metric-value {
  transform: translateX(3px);
}

.metric-detail {
  font-family: 'Noto Serif SC', serif;
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .card-content {
    padding: 18px;
  }

  .metric-value {
    font-size: 24px;
  }

  .icon-wrapper {
    width: 46px;
    height: 46px;
  }

  .icon {
    width: 20px;
    height: 20px;
  }

  .leaf-decoration {
    width: 50px;
    height: 65px;
  }
}
</style>
