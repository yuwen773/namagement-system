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
.metric-card {
  position: relative;
  background: rgba(15, 15, 26, 0.6);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: slideInUp 0.6s ease-out both;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metric-card:hover {
  transform: translateY(-8px) scale(1.02);
}

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
  opacity: 0.15;
  filter: blur(60px);
  transition: all 0.6s ease;
}

.metric-card:hover .gradient-orb {
  opacity: 0.25;
  transform: scale(1.2);
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

.card-content {
  position: relative;
  z-index: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.icon-wrapper {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 100%);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.metric-card:hover .icon-wrapper {
  transform: scale(1.1) rotate(5deg);
  border-color: var(--metric-color);
  box-shadow: 0 8px 30px rgba(255, 107, 53, 0.3);
}

.icon {
  width: 28px;
  height: 28px;
  color: var(--metric-color);
  filter: drop-shadow(0 2px 8px var(--metric-color));
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-label {
  font-family: 'Exo 2', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.metric-value {
  font-family: 'Orbitron', monospace;
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  line-height: 1;
  text-shadow: 0 0 30px var(--metric-color);
  letter-spacing: -1px;
}

.metric-detail {
  font-family: 'Exo 2', sans-serif;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

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
  opacity: 0.3;
  bottom: -30%;
}

@media (max-width: 768px) {
  .card-content {
    padding: 20px;
  }

  .metric-value {
    font-size: 28px;
  }

  .icon-wrapper {
    width: 48px;
    height: 48px;
  }

  .icon {
    width: 24px;
    height: 24px;
  }
}
</style>
