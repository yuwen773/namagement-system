<template>
  <div class="protection-guide-page grid-background">
    <!-- Floating Particles -->
    <div class="particles">
      <div v-for="i in 15" :key="i" class="particle" :style="{ '--delay': `${i * 0.5}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
    </div>

    <div class="container">
      <!-- Header -->
      <header class="page-header fade-in-down">
        <h1 class="page-title">
          <span class="title-icon">🛡️</span>
          个人防护指南
        </h1>
        <p class="page-subtitle">根据空气质量等级，科学防护，守护健康</p>
      </header>

      <!-- AQI Level Selector -->
      <div class="aqi-selector-wrapper fade-in" style="animation-delay: 0.1s">
        <div class="aqi-selector glass-card">
          <div class="selector-header">
            <h3>选择 AQI 等级</h3>
            <p class="selector-hint">点击查看对应等级的防护建议</p>
          </div>
          <div class="aqi-levels">
            <button
              v-for="level in aqiLevels"
              :key="level.value"
              :class="['level-btn', { active: selectedLevel === level.value }]"
              :style="{ '--level-color': level.color, '--level-bg': level.bgColor }"
              @click="selectLevel(level.value)"
            >
              <span class="level-badge">{{ level.value }}</span>
              <span class="level-name">{{ level.name }}</span>
              <span class="level-range">{{ level.range }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container fade-in">
        <div class="loading-spinner"></div>
        <p>加载防护指南中...</p>
      </div>

      <!-- Protection Guide Content -->
      <div v-else-if="guideData" class="guide-content fade-in" style="animation-delay: 0.2s">
        <!-- Level Info Card -->
        <div class="level-info-card glass-card hover-scale" :style="{ '--accent-color': currentAQIInfo.color }">
          <div class="level-info-header">
            <div class="level-badge-large" :style="{ background: `linear-gradient(135deg, ${currentAQIInfo.color}, ${currentAQIInfo.color}dd)` }">
              {{ selectedLevel }}
            </div>
            <div class="level-info-text">
              <h2>{{ currentAQIInfo.name }}</h2>
              <p class="level-range-text">{{ currentAQIInfo.range }}</p>
              <p class="level-description">{{ guideData.health_impact || '暂无描述' }}</p>
            </div>
          </div>
        </div>

        <!-- Protection Measures Grid -->
        <div class="measures-grid">
          <!-- Health Effects -->
          <div class="measure-card glass-card hover-scale fade-in" style="animation-delay: 0.3s">
            <div class="measure-header warning">
              <span class="measure-icon">⚠️</span>
              <h3>健康影响</h3>
            </div>
            <div class="measure-content">
              <div class="effect-list">
                <div v-for="(effect, index) in guideData.health_effects" :key="index" class="effect-item">
                  <span class="effect-dot"></span>
                  <span>{{ effect }}</span>
                </div>
                <p v-if="!guideData.health_effects || guideData.health_effects.length === 0" class="empty-text">暂无数据</p>
              </div>
            </div>
          </div>

          <!-- Sensitive Groups -->
          <div class="measure-card glass-card hover-scale fade-in" style="animation-delay: 0.4s">
            <div class="measure-header sensitive">
              <span class="measure-icon">👥</span>
              <h3>敏感人群</h3>
            </div>
            <div class="measure-content">
              <div class="group-tags">
                <span v-for="group in guideData.sensitive_groups" :key="group" class="group-tag">
                  {{ group }}
                </span>
                <span v-if="!guideData.sensitive_groups || guideData.sensitive_groups.length === 0" class="empty-text">暂无数据</span>
              </div>
              <div v-if="guideData.sensitive_advice" class="advice-box sensitive-advice">
                <p>{{ guideData.sensitive_advice }}</p>
              </div>
            </div>
          </div>

          <!-- General Advice -->
          <div class="measure-card glass-card hover-scale fade-in" style="animation-delay: 0.5s">
            <div class="measure-header general">
              <span class="measure-icon">👤</span>
              <h3>一般人群</h3>
            </div>
            <div class="measure-content">
              <div class="advice-list">
                <div v-for="(advice, index) in guideData.general_advice" :key="index" class="advice-item">
                  <span class="advice-icon">✓</span>
                  <span>{{ advice }}</span>
                </div>
                <p v-if="!guideData.general_advice || guideData.general_advice.length === 0" class="empty-text">暂无数据</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actionable Measures -->
        <div class="action-measures glass-card fade-in" style="animation-delay: 0.6s">
          <h3 class="section-title">
            <span class="title-icon">🎯</span>
            推荐防护措施
          </h3>
          <div class="actions-grid">
            <div v-for="action in guideData.actions" :key="action.name" class="action-item">
              <div class="action-icon-wrapper" :class="{ 'pulse-glow': action.recommended }">
                <span class="action-icon">{{ action.icon }}</span>
              </div>
              <div class="action-content">
                <h4>{{ action.name }}</h4>
                <p>{{ action.description }}</p>
              </div>
              <div v-if="action.recommended" class="action-badge">推荐</div>
            </div>
            <p v-if="!guideData.actions || guideData.actions.length === 0" class="empty-text">暂无数据</p>
          </div>
        </div>

        <!-- Outdoor Activity Advice -->
        <div v-if="guideData.outdoor_advice" class="outdoor-advice glass-card fade-in" style="animation-delay: 0.7s">
          <h3 class="section-title">
            <span class="title-icon">🏃</span>
            户外活动建议
          </h3>
          <div class="advice-slider">
            <div class="advice-scale">
              <div class="scale-bar">
                <div class="scale-fill" :style="{ width: getOutdoorActivityWidth() + '%', background: currentAQIInfo.color }"></div>
              </div>
              <div class="scale-labels">
                <span>适宜</span>
                <span>适度</span>
                <span>避免</span>
              </div>
            </div>
            <p class="advice-text">{{ guideData.outdoor_advice }}</p>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="error-container glass-card">
        <span class="error-icon">⚠️</span>
        <h3>加载失败</h3>
        <p>{{ error }}</p>
        <button class="retry-btn" @click="fetchGuide">重新加载</button>
      </div>

      <!-- Quick Reference Card -->
      <div class="quick-reference glass-card fade-in" style="animation-delay: 0.8s">
        <h3 class="section-title">
          <span class="title-icon">📊</span>
          AQI 等级速查
        </h3>
        <div class="reference-table">
          <div v-for="level in aqiLevels" :key="level.value" class="reference-row" :style="{ '--level-color': level.color }">
            <span class="ref-level">{{ level.value }}</span>
            <span class="ref-name">{{ level.name }}</span>
            <span class="ref-range">{{ level.range }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getProtectionGuide } from '@/api/airquality'

// AQI Levels Data
const aqiLevels = [
  { value: 1, name: '优', range: '0-50', color: '#00e400', bgColor: 'rgba(0, 228, 0, 0.1)' },
  { value: 2, name: '良', range: '51-100', color: '#ffff00', bgColor: 'rgba(255, 255, 0, 0.1)' },
  { value: 3, name: '轻度污染', range: '101-150', color: '#ff7e00', bgColor: 'rgba(255, 126, 0, 0.1)' },
  { value: 4, name: '中度污染', range: '151-200', color: '#ff0000', bgColor: 'rgba(255, 0, 0, 0.1)' },
  { value: 5, name: '重度污染', range: '201-300', color: '#99004c', bgColor: 'rgba(153, 0, 76, 0.1)' },
  { value: 6, name: '严重污染', range: '>300', color: '#7e0023', bgColor: 'rgba(126, 0, 35, 0.1)' }
]

const selectedLevel = ref(2) // Default to level 2 (Good)
const loading = ref(false)
const error = ref('')
const guideData = ref(null)

const currentAQIInfo = computed(() => {
  return aqiLevels.find(l => l.value === selectedLevel.value) || aqiLevels[1]
})

const selectLevel = (level) => {
  selectedLevel.value = level
}

const fetchGuide = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getProtectionGuide(selectedLevel.value)
    guideData.value = response.data
  } catch (err) {
    console.error('Failed to fetch protection guide:', err)
    error.value = '加载防护指南失败，请稍后重试'
    guideData.value = null
  } finally {
    loading.value = false
  }
}

const getOutdoorActivityWidth = () => {
  const levelScores = { 1: 95, 2: 75, 3: 50, 4: 30, 5: 15, 6: 5 }
  return levelScores[selectedLevel.value] || 50
}

watch(selectedLevel, () => {
  fetchGuide()
})

onMounted(() => {
  fetchGuide()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

.protection-guide-page {
  min-height: 100vh;
  padding: 2rem;
  position: relative;
  overflow-x: hidden;
  font-family: 'IBM Plex Sans', sans-serif;
  color: #e2e8f0;
}

.grid-background {
  background-color: #020617;
  background-image:
    linear-gradient(rgba(30, 41, 59, 0.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30, 41, 59, 0.3) 1px, transparent 1px);
  background-size: 50px 50px;
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(148, 163, 184, 0.3);
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
  animation-delay: var(--delay);
  left: var(--x);
  top: var(--y);
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100vh) translateX(50px); opacity: 0; }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-icon {
  font-size: 2.5rem;
  -webkit-text-fill-color: initial;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #94a3b8;
  font-weight: 300;
}

/* AQI Selector */
.aqi-selector-wrapper {
  margin-bottom: 2rem;
}

.aqi-selector {
  padding: 1.5rem;
}

.selector-header {
  margin-bottom: 1rem;
}

.selector-header h3 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.25rem;
}

.selector-hint {
  color: #94a3b8;
  font-size: 0.9rem;
}

.aqi-levels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.level-btn {
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  overflow: hidden;
}

.level-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--level-bg);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.level-btn:hover {
  transform: translateY(-2px);
  border-color: var(--level-color);
}

.level-btn:hover::before {
  opacity: 1;
}

.level-btn.active {
  border-color: var(--level-color);
  background: var(--level-bg);
  box-shadow: 0 0 20px var(--level-bg), inset 0 0 20px var(--level-bg);
}

.level-badge {
  font-family: 'Rajdhani', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--level-color);
}

.level-name {
  font-weight: 600;
  color: #f1f5f9;
}

.level-range {
  font-size: 0.85rem;
  color: #94a3b8;
  font-family: 'JetBrains Mono', monospace;
}

/* Level Info Card */
.level-info-card {
  margin-bottom: 2rem;
  padding: 2rem;
  border-left: 4px solid var(--accent-color);
  box-shadow: -5px 0 30px -10px var(--accent-color);
}

.level-info-header {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.level-badge-large {
  width: 100px;
  height: 100px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Rajdhani', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 10px 40px -10px currentColor;
}

.level-info-text h2 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 2rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.25rem;
}

.level-range-text {
  font-family: 'JetBrains Mono', monospace;
  color: #94a3b8;
  margin-bottom: 0.75rem;
}

.level-description {
  color: #cbd5e1;
  line-height: 1.6;
}

/* Measures Grid */
.measures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.measure-card {
  padding: 1.5rem;
  border-top: 3px solid;
}

.measure-card .glass-card:hover {
  transform: translateY(-4px);
}

.measure-card.warning {
  border-color: #f59e0b;
}

.measure-card.sensitive {
  border-color: #ec4899;
}

.measure-card.general {
  border-color: #10b981;
}

.measure-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.measure-icon {
  font-size: 1.5rem;
}

.measure-header h3 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #f1f5f9;
}

.measure-content {
  color: #cbd5e1;
}

.effect-list, .advice-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.effect-item, .advice-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.effect-dot {
  width: 6px;
  height: 6px;
  background: #f59e0b;
  border-radius: 50%;
  margin-top: 8px;
  flex-shrink: 0;
}

.advice-icon {
  width: 20px;
  height: 20px;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.group-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.group-tag {
  background: rgba(236, 72, 153, 0.15);
  color: #f472b6;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  border: 1px solid rgba(236, 72, 153, 0.3);
}

.sensitive-advice {
  background: rgba(236, 72, 153, 0.1);
  border-left: 3px solid #ec4899;
  padding: 1rem;
  border-radius: 0 8px 8px 0;
}

.sensitive-advice p {
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Action Measures */
.action-measures {
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.title-icon {
  font-size: 1.5rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.action-item {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  gap: 1rem;
  position: relative;
  transition: all 0.3s ease;
}

.action-item:hover {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(96, 165, 250, 0.4);
}

.action-icon-wrapper {
  width: 48px;
  height: 48px;
  background: rgba(96, 165, 250, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-icon-wrapper.pulse-glow {
  animation: pulse-glow 2s infinite;
  background: rgba(16, 185, 129, 0.15);
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  50% { box-shadow: 0 0 20px 5px rgba(16, 185, 129, 0.2); }
}

.action-icon {
  font-size: 1.5rem;
}

.action-content {
  flex: 1;
}

.action-content h4 {
  color: #f1f5f9;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.action-content p {
  color: #94a3b8;
  font-size: 0.9rem;
  line-height: 1.4;
}

.action-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
}

/* Outdoor Activity Advice */
.outdoor-advice {
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.advice-slider {
  text-align: center;
}

.advice-scale {
  margin-bottom: 1rem;
}

.scale-bar {
  height: 20px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.5rem;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.scale-fill {
  height: 100%;
  transition: width 0.5s ease, background 0.5s ease;
  border-radius: 10px;
}

.scale-labels {
  display: flex;
  justify-content: space-between;
  color: #94a3b8;
  font-size: 0.85rem;
}

.advice-text {
  color: #cbd5e1;
  line-height: 1.6;
}

/* Quick Reference */
.quick-reference {
  padding: 1.5rem;
}

.reference-table {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reference-row {
  display: grid;
  grid-template-columns: 50px 1fr 100px;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 8px;
  border-left: 3px solid var(--level-color);
  transition: transform 0.2s ease;
}

.reference-row:hover {
  transform: translateX(5px);
}

.ref-level {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--level-color);
}

.ref-name {
  font-weight: 500;
  color: #f1f5f9;
}

.ref-range {
  font-family: 'JetBrains Mono', monospace;
  color: #94a3b8;
  font-size: 0.9rem;
  text-align: right;
}

/* Glass Card */
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  transition: all 0.3s ease;
}

/* Loading & Error */
.loading-container, .error-container {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1.5rem;
  border: 3px solid rgba(96, 165, 250, 0.2);
  border-top-color: #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.error-container h3 {
  color: #f1f5f9;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: #94a3b8;
  margin-bottom: 1rem;
}

.retry-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
}

/* Empty State */
.empty-text {
  color: #64748b;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}

/* Animations */
.fade-in {
  animation: fade-in 0.5s ease forwards;
  opacity: 0;
}

@keyframes fade-in {
  to { opacity: 1; }
}

.fade-in-down {
  animation: fade-in-down 0.6s ease forwards;
  opacity: 0;
}

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hover-scale {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-scale:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .protection-guide-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .aqi-levels {
    grid-template-columns: repeat(2, 1fr);
  }

  .level-info-header {
    flex-direction: column;
    text-align: center;
  }

  .measures-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .reference-row {
    grid-template-columns: 40px 1fr 80px;
  }
}
</style>
