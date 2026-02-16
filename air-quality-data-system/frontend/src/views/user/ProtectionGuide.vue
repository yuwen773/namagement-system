<template>
  <div class="protection-guide-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回概览
        </el-button>
        <div class="header-info">
          <h1 class="page-title">个人防护指南</h1>
          <p class="page-subtitle">根据空气质量等级，科学防护，守护健康</p>
        </div>
      </div>
    </div>

    <!-- AQI Level Selector -->
    <div class="card selector-card">
      <div class="selector-header">
        <h3 class="selector-title">选择 AQI 等级</h3>
        <p class="selector-hint">点击查看对应等级的防护建议</p>
      </div>
      <div class="aqi-levels">
        <div
          v-for="level in aqiLevels"
          :key="level.value"
          :class="['level-btn', { active: selectedLevel === level.value }]"
          :style="{ '--level-color': level.color }"
          @click="selectLevel(level.value)"
        >
          <div class="level-badge" :style="{ background: level.color }">
            {{ level.value }}
          </div>
          <div class="level-info">
            <span class="level-name">{{ level.name }}</span>
            <span class="level-range">{{ level.range }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Protection Guide Content -->
    <div v-else-if="guideData" class="guide-content">
      <!-- Level Info Card -->
      <div class="card level-info-card">
        <div class="level-info-header">
          <div class="level-badge-large" :style="{ background: currentAQIInfo.color }">
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
        <div class="card measure-card">
          <div class="measure-header warning">
            <el-icon class="measure-icon"><Warning /></el-icon>
            <h3>健康影响</h3>
          </div>
          <div class="measure-content">
            <div v-if="guideData.health_effects && guideData.health_effects.length > 0" class="effect-list">
              <div v-for="(effect, index) in guideData.health_effects" :key="index" class="effect-item">
                <span class="effect-dot"></span>
                <span>{{ effect }}</span>
              </div>
            </div>
            <el-empty v-else description="暂无数据" :image-size="80" />
          </div>
        </div>

        <!-- Sensitive Groups -->
        <div class="card measure-card">
          <div class="measure-header sensitive">
            <el-icon class="measure-icon"><User /></el-icon>
            <h3>敏感人群</h3>
          </div>
          <div class="measure-content">
            <div v-if="guideData.sensitive_groups && guideData.sensitive_groups.length > 0" class="group-tags">
              <el-tag v-for="group in guideData.sensitive_groups" :key="group" type="danger" effect="light">
                {{ group }}
              </el-tag>
            </div>
            <el-empty v-else description="暂无数据" :image-size="80" />
            <div v-if="guideData.sensitive_advice" class="advice-box">
              <p>{{ guideData.sensitive_advice }}</p>
            </div>
          </div>
        </div>

        <!-- General Advice -->
        <div class="card measure-card">
          <div class="measure-header general">
            <el-icon class="measure-icon"><CircleCheck /></el-icon>
            <h3>一般人群</h3>
          </div>
          <div class="measure-content">
            <div v-if="guideData.general_advice && guideData.general_advice.length > 0" class="advice-list">
              <div v-for="(advice, index) in guideData.general_advice" :key="index" class="advice-item">
                <el-icon class="advice-icon" color="#10B981"><Check /></el-icon>
                <span>{{ advice }}</span>
              </div>
            </div>
            <el-empty v-else description="暂无数据" :image-size="80" />
          </div>
        </div>
      </div>

      <!-- Actionable Measures -->
      <div v-if="guideData.actions && guideData.actions.length > 0" class="card actions-card">
        <h3 class="section-title">
          <el-icon><Document /></el-icon>
          推荐防护措施
        </h3>
        <div class="actions-grid">
          <div v-for="action in guideData.actions" :key="action.name" class="action-item">
            <div class="action-icon" :style="{ background: action.recommended ? 'rgba(16, 185, 129, 0.1)' : 'var(--bg-hover)' }">
              <span class="action-emoji">{{ action.icon }}</span>
            </div>
            <div class="action-content">
              <h4>{{ action.name }}</h4>
              <p>{{ action.description }}</p>
            </div>
            <el-tag v-if="action.recommended" type="success" size="small">推荐</el-tag>
          </div>
        </div>
      </div>

      <!-- Outdoor Activity Advice -->
      <div v-if="guideData.outdoor_advice" class="card outdoor-card">
        <h3 class="section-title">
          <el-icon><Star /></el-icon>
          户外活动建议
        </h3>
        <div class="advice-content">
          <div class="advice-bar-wrapper">
            <div class="advice-bar">
              <div class="advice-fill" :style="{ width: getOutdoorActivityWidth() + '%', background: currentAQIInfo.color }"></div>
            </div>
            <div class="advice-labels">
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
    <div v-else class="card error-card">
      <el-result icon="error" title="加载失败" :sub-title="error">
        <template #extra>
          <el-button type="primary" @click="fetchGuide">重新加载</el-button>
        </template>
      </el-result>
    </div>

    <!-- Quick Reference Card -->
    <div class="card reference-card">
      <h3 class="section-title">
        <el-icon><List /></el-icon>
        AQI 等级速查
      </h3>
      <div class="reference-table">
        <div v-for="level in aqiLevels" :key="level.value" class="reference-row">
          <span class="ref-level" :style="{ background: level.color }">{{ level.value }}</span>
          <span class="ref-name">{{ level.name }}</span>
          <span class="ref-range">{{ level.range }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Warning, User, CircleCheck, Check, Document, Star, List } from '@element-plus/icons-vue'
import { getProtectionGuide } from '@/api/airquality'

const router = useRouter()

// AQI Levels Data
const aqiLevels = [
  { value: 1, name: '优', range: '0-50', color: '#10B981' },
  { value: 2, name: '良', range: '51-100', color: '#FBBF24' },
  { value: 3, name: '轻度污染', range: '101-150', color: '#F97316' },
  { value: 4, name: '中度污染', range: '151-200', color: '#EF4444' },
  { value: 5, name: '重度污染', range: '201-300', color: '#A855F7' },
  { value: 6, name: '严重污染', range: '>300', color: '#7F1D1D' }
]

const selectedLevel = ref(2)
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

const goBack = () => {
  router.back()
}

watch(selectedLevel, () => {
  fetchGuide()
})

onMounted(() => {
  fetchGuide()
})
</script>

<style scoped>
.protection-guide-page {
  padding: var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: var(--spacing-xl);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.back-button {
  font-size: 14px;
  color: var(--text-secondary);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-lg);
}

.card:last-child {
  margin-bottom: 0;
}

/* Selector Card */
.selector-card {
  padding: var(--spacing-lg);
}

.selector-header {
  margin-bottom: var(--spacing-md);
}

.selector-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-xs) 0;
}

.selector-hint {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

.aqi-levels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--spacing-md);
}

.level-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.level-btn:hover {
  border-color: var(--level-color);
  background: var(--bg-card);
}

.level-btn.active {
  border-color: var(--level-color);
  background: var(--bg-card);
  box-shadow: 0 0 0 2px var(--level-color);
}

.level-badge {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
  flex-shrink: 0;
}

.level-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.level-name {
  font-weight: 600;
  color: var(--text);
}

.level-range {
  font-size: 12px;
  color: var(--text-secondary);
  font-family: var(--font-mono);
}

/* Level Info Card */
.level-info-card {
  padding: var(--spacing-lg);
}

.level-info-header {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.level-badge-large {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 36px;
  font-weight: 700;
  flex-shrink: 0;
}

.level-info-text h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-xs) 0;
}

.level-range-text {
  font-size: 14px;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  margin-bottom: var(--spacing-sm);
}

.level-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Measures Grid */
.measures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.measure-card {
  padding: var(--spacing-lg);
}

.measure-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border);
}

.measure-header.warning { color: #F59E0B; }
.measure-header.sensitive { color: #EC4899; }
.measure-header.general { color: #10B981; }

.measure-icon {
  font-size: 20px;
}

.measure-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.measure-content {
  color: var(--text-secondary);
}

.effect-list, .advice-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.effect-item, .advice-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
}

.effect-dot {
  width: 6px;
  height: 6px;
  background: #F59E0B;
  border-radius: 50%;
  margin-top: 8px;
  flex-shrink: 0;
}

.advice-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.group-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.advice-box {
  background: var(--bg-hover);
  border-left: 3px solid #EC4899;
  padding: var(--spacing-md);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}

.advice-box p {
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

/* Actions Card */
.actions-card {
  padding: var(--spacing-lg);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-md) 0;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.action-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  position: relative;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-emoji {
  font-size: 24px;
}

.action-content {
  flex: 1;
}

.action-content h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-xs) 0;
}

.action-content p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
}

/* Outdoor Card */
.outdoor-card {
  padding: var(--spacing-lg);
}

.advice-content {
  text-align: center;
}

.advice-bar-wrapper {
  margin-bottom: var(--spacing-md);
}

.advice-bar {
  height: 16px;
  background: var(--bg-hover);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: var(--spacing-sm);
}

.advice-fill {
  height: 100%;
  transition: width 0.5s ease;
}

.advice-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
}

.advice-text {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Reference Card */
.reference-card {
  padding: var(--spacing-lg);
}

.reference-table {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.reference-row {
  display: grid;
  grid-template-columns: 50px 1fr 100px;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.ref-level {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
}

.ref-name {
  font-weight: 500;
  color: var(--text);
}

.ref-range {
  font-family: var(--font-mono);
  color: var(--text-secondary);
  font-size: 13px;
  text-align: right;
}

/* Loading & Error */
.loading-container {
  padding: var(--spacing-2xl);
}

.error-card {
  padding: var(--spacing-2xl);
}

/* Responsive */
@media (max-width: 768px) {
  .protection-guide-page {
    padding: var(--spacing-md);
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
