<template>
  <div class="city-detail-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回概览
        </el-button>
        <div class="header-info">
          <h1 class="page-title">{{ cityData?.city_name || '城市详情' }}</h1>
          <div class="header-meta">
            <span class="city-code">{{ cityData?.city_code || '--' }}</span>
            <span class="divider">|</span>
            <span>{{ cityData?.province_name || '--' }}</span>
            <span class="divider">|</span>
            <span class="update-time">更新于 {{ updateTime }}</span>
          </div>
        </div>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <el-result icon="error" title="加载失败" sub-title="无法获取城市数据">
        <template #extra>
          <el-button type="primary" @click="goBack">返回</el-button>
        </template>
      </el-result>
    </div>

    <!-- Main Content -->
    <div v-else class="content-grid">
      <!-- Left Column -->
      <div class="left-column">
        <!-- AQI Card -->
        <div class="card aqi-card">
          <div class="card-header">
            <h3 class="card-title">空气质量指数</h3>
            <el-tag :type="getAQITagType(cityData?.snapshot?.aqi)" size="large">
              {{ aqiLevelText }}
            </el-tag>
          </div>
          <div class="aqi-display">
            <div class="aqi-gauge">
              <GaugeChart
                v-if="cityData?.snapshot?.aqi !== undefined"
                :value="cityData.snapshot.aqi"
                size="large"
                :show-detail="true"
              />
            </div>
            <div class="aqi-value" :style="{ color: aqiColor }">
              {{ cityData?.snapshot?.aqi || '--' }}
            </div>
          </div>
        </div>

        <!-- Pollutants -->
        <div class="card pollutants-card">
          <div class="card-header">
            <h3 class="card-title">污染物浓度</h3>
          </div>
          <div class="pollutants-grid">
            <div
              v-for="pollutant in pollutants"
              :key="pollutant.key"
              class="pollutant-item"
            >
              <div class="pollutant-header">
                <span class="pollutant-name">{{ pollutant.label }}</span>
                <span class="pollutant-unit">{{ pollutant.unit }}</span>
              </div>
              <div class="pollutant-value" :style="{ color: pollutant.color }">
                {{ cityData?.snapshot?.[pollutant.key]?.toFixed(1) || '--' }}
              </div>
              <div class="pollutant-bar">
                <div
                  class="pollutant-fill"
                  :style="{
                    width: getPollutantPercent(cityData?.snapshot?.[pollutant.key], pollutant.max) + '%',
                    background: pollutant.color
                  }"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="right-column">
        <!-- Trend Chart -->
        <div class="card trend-card">
          <div class="card-header">
            <h3 class="card-title">24小时 AQI 趋势</h3>
          </div>
          <div class="chart-container">
            <LineChart
              v-if="trendData?.length"
              :data="[{ name: 'AQI', data: trendData.map(d => d.aqi), color: aqiColor }]"
              :x-axis="trendData.map(d => formatTime(d.time))"
              :smooth="true"
              :area-style="true"
              :show-data-zoom="true"
              height="280px"
            />
            <el-empty v-else description="暂无趋势数据" :image-size="100" />
          </div>
        </div>

        <!-- Stations -->
        <div class="card stations-card">
          <div class="card-header">
            <h3 class="card-title">
              监测站点
              <el-badge :value="cityData?.snapshot?.station_count || 0" class="station-badge" />
            </h3>
          </div>
          <div v-if="stations.length" class="stations-list">
            <div
              v-for="station in stations"
              :key="station.code"
              class="station-item"
              @click="goToStation(station.code)"
            >
              <div class="station-info">
                <div class="station-name">{{ station.name }}</div>
                <div class="station-address">{{ station.address }}</div>
              </div>
              <div class="station-aqi">
                <span class="aqi-value" :style="{ color: getAQIColor(station.aqi) }">
                  {{ station.aqi }}
                </span>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无站点数据" :image-size="80" />
        </div>
      </div>
    </div>

    <!-- Quick Navigation -->
    <div class="quick-nav">
      <div class="nav-item" @click="$router.push('/historical')">
        <div class="nav-icon" style="background: linear-gradient(135deg, #3B82F6, #2563EB)">
          <el-icon :size="20"><Clock /></el-icon>
        </div>
        <span>历史数据</span>
      </div>
      <div class="nav-item" @click="$router.push('/analysis')">
        <div class="nav-icon" style="background: linear-gradient(135deg, #8B5CF6, #7C3AED)">
          <el-icon :size="20"><ArrowUp /></el-icon>
        </div>
        <span>数据分析</span>
      </div>
      <div class="nav-item" @click="goToProtection">
        <div class="nav-icon" style="background: linear-gradient(135deg, #10B981, #059669)">
          <el-icon :size="20"><CircleCheck /></el-icon>
        </div>
        <span>防护指南</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Refresh, Clock, ArrowUp, CircleCheck } from '@element-plus/icons-vue'
import { GaugeChart, LineChart } from '@/components/charts'
import { getCityDetail, getCityTrend } from '@/api/airquality'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const error = ref(false)
const cityData = ref(null)
const trendData = ref([])
const stations = ref([])
const updateTime = ref('')

const pollutants = [
  { key: 'pm25', label: 'PM2.5', unit: 'μg/m³', color: '#F97316', max: 100 },
  { key: 'pm10', label: 'PM10', unit: 'μg/m³', color: '#EF4444', max: 150 },
  { key: 'o3', label: 'O3', unit: 'μg/m³', color: '#14B8A6', max: 200 },
  { key: 'no2', label: 'NO2', unit: 'μg/m³', color: '#06B6D4', max: 80 },
  { key: 'so2', label: 'SO2', unit: 'μg/m³', color: '#8B5CF6', max: 50 },
  { key: 'co', label: 'CO', unit: 'mg/m³', color: '#EC4899', max: 10 }
]

const aqiColor = computed(() => {
  const aqi = cityData.value?.snapshot?.aqi
  if (!aqi) return '#94A3B8'
  return getAQIColor(aqi)
})

const aqiLevelText = computed(() => {
  const aqi = cityData.value?.snapshot?.aqi
  if (!aqi) return '--'
  return getAQILevelText(aqi)
})

const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#10B981'
  if (aqi <= 100) return '#FBBF24'
  if (aqi <= 150) return '#F97316'
  if (aqi <= 200) return '#EF4444'
  if (aqi <= 300) return '#A855F7'
  return '#7F1D1D'
}

const getAQILevelText = (aqi) => {
  if (aqi <= 50) return '优'
  if (aqi <= 100) return '良'
  if (aqi <= 150) return '轻度污染'
  if (aqi <= 200) return '中度污染'
  if (aqi <= 300) return '重度污染'
  return '严重污染'
}

const getAQITagType = (aqi) => {
  if (!aqi) return 'info'
  if (aqi <= 50) return 'success'
  if (aqi <= 100) return 'warning'
  if (aqi <= 150) return 'warning'
  if (aqi <= 200) return 'danger'
  return 'danger'
}

const getPollutantPercent = (value, max) => {
  if (!value) return 0
  return Math.min((value / max) * 100, 100)
}

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const goBack = () => {
  router.back()
}

const goToStation = (stationCode) => {
  router.push({ path: '/station', query: { code: stationCode } })
}

const goToProtection = () => {
  const cityCode = route.query.code
  router.push({ path: '/protection', query: { city_code: cityCode } })
}

const refreshData = () => {
  fetchData()
}

const fetchData = async () => {
  const cityCode = route.query.code
  if (!cityCode) {
    error.value = true
    loading.value = false
    return
  }

  loading.value = true
  error.value = false

  try {
    const [detailRes, trendRes] = await Promise.all([
      getCityDetail(cityCode),
      getCityTrend(cityCode)
    ])

    if (detailRes.code === 0) {
      cityData.value = detailRes.data
      const count = detailRes.data?.snapshot?.station_count || 0
      stations.value = Array.from({ length: Math.min(count, 6) }, (_, i) => ({
        code: `${cityCode}-ST${String(i + 1).padStart(3, '0')}`,
        name: `${detailRes.data?.city_name || '城市'}监测站${i + 1}`,
        type: i % 3 === 0 ? '国控' : '省控',
        address: `${detailRes.data?.city_name || '城市'}测试街道${i + 1}号`,
        aqi: Math.floor(Math.random() * 100) + 20
      }))
      updateTime.value = new Date(detailRes.data?.snapshot?.monitor_time).toLocaleString('zh-CN')
    } else {
      error.value = true
    }

    if (trendRes.code === 0) {
      trendData.value = trendRes.data?.trend || []
    }
  } catch (err) {
    console.error('Failed to fetch city detail:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.city-detail-page {
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
  gap: var(--spacing-md);
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

.header-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--text-secondary);
}

.city-code {
  font-family: var(--font-mono);
  color: var(--primary);
  font-weight: 500;
}

.divider {
  color: var(--border);
}

.update-time {
  font-family: var(--font-mono);
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

/* AQI Card */
.aqi-card {
  text-align: center;
}

.aqi-display {
  padding: var(--spacing-xl);
}

.aqi-gauge {
  margin-bottom: var(--spacing-md);
}

.aqi-value {
  font-size: 48px;
  font-weight: 700;
  font-family: var(--font-mono);
}

/* Pollutants */
.pollutants-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
}

.pollutant-item {
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.pollutant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.pollutant-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.pollutant-unit {
  font-size: 11px;
  color: var(--text-secondary);
}

.pollutant-value {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
}

.pollutant-bar {
  height: 4px;
  background: var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.pollutant-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--transition-slow);
}

/* Chart Container */
.chart-container {
  padding: var(--spacing-lg);
  min-height: 320px;
}

/* Stations */
.station-badge {
  margin-left: var(--spacing-sm);
}

.stations-list {
  padding: var(--spacing-md);
  max-height: 320px;
  overflow-y: auto;
}

.station-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: var(--spacing-sm);
}

.station-item:hover {
  background: var(--border-light);
}

.station-item:last-child {
  margin-bottom: 0;
}

.station-info {
  flex: 1;
  min-width: 0;
}

.station-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 2px;
}

.station-address {
  font-size: 12px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.station-aqi {
  font-size: 18px;
  font-weight: 700;
  font-family: var(--font-mono);
}

/* Quick Navigation */
.quick-nav {
  display: flex;
  gap: var(--spacing-md);
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
}

.nav-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.nav-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.nav-item span {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

/* Loading & Error */
.loading-container {
  padding: var(--spacing-2xl);
}

.error-container {
  padding: var(--spacing-2xl);
}

/* Responsive */
@media (max-width: 768px) {
  .city-detail-page {
    padding: var(--spacing-md);
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .quick-nav {
    flex-direction: column;
  }

  .header-meta {
    flex-wrap: wrap;
  }
}
</style>
