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
      <!-- City Selector -->
      <div class="header-right">
        <div class="city-selector-wrapper">
          <span class="city-label">当前城市:</span>
          <el-select
            v-model="selectedCityCode"
            placeholder="选择城市"
            filterable
            @change="handleCityChange"
            :loading="citiesLoading"
            style="width: 180px"
          >
            <el-option
              v-for="city in availableCities"
              :key="city.city_code"
              :label="city.city_name"
              :value="city.city_code"
            />
          </el-select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Protection Guide Content -->
    <div v-else-if="guideData" class="guide-content">
      <!-- Current AQI Card -->
      <div class="card level-info-card">
        <div class="level-info-header">
          <div class="level-badge-large" :style="{ background: getAQIColor(guideData.current.aqi) }">
            {{ guideData.current.aqi }}
          </div>
          <div class="level-info-text">
            <h2>{{ guideData.city.city_name }}</h2>
            <p class="level-range-text">当前 AQI: {{ guideData.current.aqi }} | {{ getQualityLevelText(guideData.current.quality_level) }}</p>
            <p class="level-description">{{ getHealthImpact(guideData.current.aqi) }}</p>
          </div>
        </div>
      </div>

      <!-- Forecast Card -->
      <div v-if="guideData.forecast" class="card forecast-card">
        <h3 class="section-title">
          <el-icon><TrendCharts /></el-icon>
          空气质量趋势预测
        </h3>
        <div class="forecast-content">
          <div class="forecast-items">
            <div class="forecast-item">
              <span class="forecast-label">趋势</span>
              <span class="forecast-value" :class="getTrendClass(guideData.forecast.trend)">
                {{ getTrendText(guideData.forecast.trend) }}
              </span>
            </div>
            <div class="forecast-item">
              <span class="forecast-label">6小时后预测</span>
              <span class="forecast-value">{{ guideData.forecast.predicted_aqi_6h }} ({{ getQualityLevelText(guideData.forecast.predicted_quality_level_6h) }})</span>
            </div>
            <div class="forecast-item">
              <span class="forecast-label">12小时后预测</span>
              <span class="forecast-value">{{ guideData.forecast.predicted_aqi_12h }} ({{ getQualityLevelText(guideData.forecast.predicted_quality_level_12h) }})</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Protection Measures Grid -->
      <div class="measures-grid">
        <!-- General Advice -->
        <div class="card measure-card">
          <div class="measure-header general">
            <el-icon class="measure-icon"><CircleCheck /></el-icon>
            <h3>一般人群</h3>
          </div>
          <div class="measure-content">
            <p v-if="guideData.advice.general" class="advice-text">{{ guideData.advice.general }}</p>
            <el-empty v-else description="暂无数据" :image-size="60" />
          </div>
        </div>

        <!-- Sensitive Groups -->
        <div class="card measure-card">
          <div class="measure-header sensitive">
            <el-icon class="measure-icon"><User /></el-icon>
            <h3>敏感人群</h3>
          </div>
          <div class="measure-content">
            <p v-if="guideData.advice.sensitive" class="advice-text">{{ guideData.advice.sensitive }}</p>
            <el-empty v-else description="暂无数据" :image-size="60" />
          </div>
        </div>

        <!-- Children -->
        <div class="card measure-card">
          <div class="measure-header children">
            <el-icon class="measure-icon"><User /></el-icon>
            <h3>儿童</h3>
          </div>
          <div class="measure-content">
            <p v-if="guideData.advice.children" class="advice-text">{{ guideData.advice.children }}</p>
            <el-empty v-else description="暂无数据" :image-size="60" />
          </div>
        </div>

        <!-- Elderly -->
        <div class="card measure-card">
          <div class="measure-header elderly">
            <el-icon class="measure-icon"><User /></el-icon>
            <h3>老年人</h3>
          </div>
          <div class="measure-content">
            <p v-if="guideData.advice.elderly" class="advice-text">{{ guideData.advice.elderly }}</p>
            <el-empty v-else description="暂无数据" :image-size="60" />
          </div>
        </div>

        <!-- Patients -->
        <div class="card measure-card">
          <div class="measure-header patients">
            <el-icon class="measure-icon"><User /></el-icon>
            <h3>病患者</h3>
          </div>
          <div class="measure-content">
            <p v-if="guideData.advice.patients" class="advice-text">{{ guideData.advice.patients }}</p>
            <el-empty v-else description="暂无数据" :image-size="60" />
          </div>
        </div>
      </div>

      <!-- Warning Advice -->
      <div v-if="guideData.forecast.warning_advice" class="card warning-card">
        <h3 class="section-title warning">
          <el-icon><Warning /></el-icon>
          预警提示
        </h3>
        <div class="warning-content">
          <p>{{ guideData.forecast.warning_advice }}</p>
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
          <span class="ref-level" :style="{ background: level.color }">{{ level.name }}</span>
          <span class="ref-range">{{ level.range }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Warning, User, CircleCheck, Document, Star, List, TrendCharts } from '@element-plus/icons-vue'
import { getProtectionGuide, getTopCities } from '@/api/airquality'
import { useCityStore } from '@/stores/city'

const router = useRouter()
const route = useRoute()
const cityStore = useCityStore()

// Default city: Beijing
const DEFAULT_CITY_CODE = '110100'
const DEFAULT_CITY_NAME = '北京市'

// AQI Levels Data
const aqiLevels = [
  { value: 1, name: '优', range: '0-50', color: '#10B981' },
  { value: 2, name: '良', range: '51-100', color: '#FBBF24' },
  { value: 3, name: '轻度污染', range: '101-150', color: '#F97316' },
  { value: 4, name: '中度污染', range: '151-200', color: '#EF4444' },
  { value: 5, name: '重度污染', range: '201-300', color: '#A855F7' },
  { value: 6, name: '严重污染', range: '>300', color: '#7F1D1D' }
]

const loading = ref(false)
const citiesLoading = ref(false)
const error = ref('')
const guideData = ref(null)

// City management
const availableCities = ref([])
const selectedCityCode = ref('')

// Initialize city code with priority: URL param > store > default
const initializeCityCode = () => {
  const urlCityCode = route.query.city_code
  if (urlCityCode) {
    return urlCityCode
  }
  if (cityStore.selectedCityCode) {
    return cityStore.selectedCityCode
  }
  return DEFAULT_CITY_CODE
}

// Fetch available cities list
const fetchCities = async () => {
  citiesLoading.value = true
  try {
    const response = await getTopCities({ limit: 50 })
    // Get cities from both best and worst lists, deduplicate
    const bestCities = response.data.best || []
    const worstCities = response.data.worst || []
    const allCities = [...bestCities, ...worstCities]

    // Deduplicate by city_code
    const cityMap = new Map()
    allCities.forEach(city => {
      if (!cityMap.has(city.city_code)) {
        cityMap.set(city.city_code, city)
      }
    })

    // Add default city if not in list
    if (!cityMap.has(DEFAULT_CITY_CODE)) {
      cityMap.set(DEFAULT_CITY_CODE, { city_code: DEFAULT_CITY_CODE, city_name: DEFAULT_CITY_NAME })
    }

    availableCities.value = Array.from(cityMap.values())
  } catch (err) {
    console.error('Failed to fetch cities:', err)
    // Fallback to default city
    availableCities.value = [{ city_code: DEFAULT_CITY_CODE, city_name: DEFAULT_CITY_NAME }]
  } finally {
    citiesLoading.value = false
  }
}

const fetchGuide = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getProtectionGuide({ city_code: selectedCityCode.value })
    guideData.value = response.data
  } catch (err) {
    console.error('Failed to fetch protection guide:', err)
    error.value = '加载防护指南失败，请稍后重试'
    guideData.value = null
  } finally {
    loading.value = false
  }
}

const handleCityChange = (cityCode) => {
  // Update store
  const city = availableCities.value.find(c => c.city_code === cityCode)
  if (city) {
    cityStore.setCity(city.city_name, city.city_code)
  }
  // Refetch guide data
  fetchGuide()
}

const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#10B981'
  if (aqi <= 100) return '#FBBF24'
  if (aqi <= 150) return '#F97316'
  if (aqi <= 200) return '#EF4444'
  if (aqi <= 300) return '#A855F7'
  return '#7F1D1D'
}

const getQualityLevelText = (level) => {
  const levelMap = {
    'EXCELLENT': '优',
    'GOOD': '良',
    'LIGHT_POLLUTION': '轻度污染',
    'MODERATE_POLLUTION': '中度污染',
    'HEAVY_POLLUTION': '重度污染',
    'SEVERE_POLLUTION': '严重污染'
  }
  return levelMap[level] || level
}

const getHealthImpact = (aqi) => {
  if (aqi <= 50) return '空气质量令人满意，基本无空气污染。'
  if (aqi <= 100) return '空气质量可接受，极少数异常敏感人群应减少户外活动。'
  if (aqi <= 150) return '易感人群症状轻度加剧，健康人群出现刺激症状。'
  if (aqi <= 200) return '进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响。'
  if (aqi <= 300) return '心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状。'
  return '健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病。'
}

const getTrendText = (trend) => {
  const trendMap = {
    'RISING': '上升',
    'FALLING': '下降',
    'STABLE': '稳定'
  }
  return trendMap[trend] || trend
}

const getTrendClass = (trend) => {
  if (trend === 'RISING') return 'trend-up'
  if (trend === 'FALLING') return 'trend-down'
  return 'trend-stable'
}

const goBack = () => {
  router.back()
}

onMounted(async () => {
  // Initialize city code
  selectedCityCode.value = initializeCityCode()

  // Update store if not already set
  if (!cityStore.selectedCityCode || !cityStore.selectedCity) {
    const initialCity = availableCities.value.find(c => c.city_code === selectedCityCode.value)
    if (initialCity) {
      cityStore.setCity(initialCity.city_name, initialCity.city_code)
    } else {
      // Use default city values
      cityStore.setCity(DEFAULT_CITY_NAME, selectedCityCode.value)
    }
  }

  // Fetch cities and guide data in parallel
  await Promise.all([fetchCities(), fetchGuide()])
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
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-lg);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.city-selector-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
}

.city-label {
  font-size: 13px;
  color: var(--text-secondary);
  white-space: nowrap;
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
  width: 100px;
  height: 100px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 42px;
  font-weight: 700;
  flex-shrink: 0;
}

.level-info-text {
  flex: 1;
}

.level-info-text h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-xs) 0;
}

.level-range-text {
  font-size: 16px;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  margin-bottom: var(--spacing-sm);
}

.level-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Forecast Card */
.forecast-card {
  padding: var(--spacing-lg);
}

.forecast-content {
  margin-top: var(--spacing-md);
}

.forecast-items {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.forecast-item {
  text-align: center;
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  min-width: 140px;
}

.forecast-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
}

.forecast-value {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
}

.trend-up { color: #EF4444; }
.trend-down { color: #10B981; }
.trend-stable { color: #FBBF24; }

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
.measure-header.children { color: #3B82F6; }
.measure-header.elderly { color: #8B5CF6; }
.measure-header.patients { color: #EF4444; }

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

.advice-text {
  line-height: 1.8;
  margin: 0;
}

/* Warning Card */
.warning-card {
  padding: var(--spacing-lg);
  border-left: 4px solid #F59E0B;
}

.section-title.warning {
  color: #F59E0B;
}

.warning-content p {
  color: var(--text-secondary);
  line-height: 1.8;
  margin: 0;
}

/* Section Title */
.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-md) 0;
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
  grid-template-columns: 80px 1fr;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.ref-level {
  padding: 6px 12px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.ref-range {
  font-family: var(--font-mono);
  color: var(--text-secondary);
  font-size: 14px;
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

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .city-selector-wrapper {
    width: 100%;
  }

  .city-selector-wrapper .el-select {
    flex: 1;
  }

  .level-info-header {
    flex-direction: column;
    text-align: center;
  }

  .measures-grid {
    grid-template-columns: 1fr;
  }

  .forecast-items {
    flex-direction: column;
  }

  .forecast-item {
    width: 100%;
  }

  .reference-row {
    grid-template-columns: 60px 1fr;
  }
}
</style>
