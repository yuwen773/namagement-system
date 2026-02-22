<template>
  <div class="station-detail-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回城市
        </el-button>
        <div class="header-info">
          <h1 class="page-title">{{ stationData?.station_name || '站点详情' }}</h1>
          <div class="header-meta">
            <el-tag size="small">{{ stationData?.station_type || '--' }}</el-tag>
            <span class="divider">|</span>
            <span>{{ stationData?.city_name || '--' }}</span>
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
      <el-result icon="error" title="加载失败" sub-title="无法获取站点数据">
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
            <el-tag :type="getAQITagType(stationData?.snapshot?.aqi)" size="large">
              {{ aqiLevelText }}
            </el-tag>
          </div>
          <div class="aqi-display">
            <div class="aqi-gauge">
              <GaugeChart
                v-if="stationData?.snapshot?.aqi !== undefined"
                :value="stationData.snapshot.aqi"
                size="large"
                :show-detail="true"
              />
            </div>
            <div class="aqi-value" :style="{ color: aqiColor }">
              {{ stationData?.snapshot?.aqi || '--' }}
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
                {{ formatPollutantValue(stationData?.snapshot?.[pollutant.key]) }}
              </div>
              <div class="pollutant-bar">
                <div
                  class="pollutant-fill"
                  :style="{
                    width: getPollutantPercent(stationData?.snapshot?.[pollutant.key], pollutant.max) + '%',
                    background: pollutant.color
                  }"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Station Info -->
        <div class="card info-card">
          <div class="card-header">
            <h3 class="card-title">站点信息</h3>
          </div>
          <div class="info-list">
            <div class="info-row">
              <span class="info-label">站点编码</span>
              <span class="info-value">{{ stationData?.station_code || '--' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">站点类型</span>
              <span class="info-value">{{ stationData?.station_type || '--' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">所属城市</span>
              <span class="info-value">{{ stationData?.city_name || '--' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">监测时间</span>
              <span class="info-value">{{ formatMonitorTime }}</span>
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
              :data="[
                { name: 'AQI', data: trendData.map(d => d.aqi), color: aqiColor },
                { name: 'PM2.5', data: trendData.map(d => d.pm25), color: '#F97316' }
              ]"
              :x-axis="trendData.map(d => formatTime(d.time))"
              :smooth="true"
              :area-style="false"
              :show-data-zoom="true"
              height="320px"
            />
            <el-empty v-else description="暂无趋势数据" :image-size="100" />
          </div>
        </div>

        <!-- Statistics -->
        <div class="stats-grid">
          <div class="stat-item stat-danger">
            <div class="stat-label">24h 最高</div>
            <div class="stat-value">{{ maxAQI || '--' }}</div>
          </div>
          <div class="stat-item stat-success">
            <div class="stat-label">24h 最低</div>
            <div class="stat-value">{{ minAQI || '--' }}</div>
          </div>
          <div class="stat-item" :style="{ '--stat-color': aqiColor }">
            <div class="stat-label">24h 平均</div>
            <div class="stat-value">{{ avgAQI || '--' }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">数据点数</div>
            <div class="stat-value">{{ trendData?.length || 0 }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Refresh } from '@element-plus/icons-vue'
import { GaugeChart, LineChart } from '@/components/charts'
import { getStationDetail, getStationTrend } from '@/api/airquality'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const error = ref(false)
const stationData = ref(null)
const trendData = ref([])
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
  const aqi = stationData.value?.snapshot?.aqi
  if (!aqi) return '#94A3B8'
  return getAQIColor(aqi)
})

const aqiLevelText = computed(() => {
  const aqi = stationData.value?.snapshot?.aqi
  if (!aqi) return '--'
  return getAQILevelText(aqi)
})

const formatMonitorTime = computed(() => {
  const time = stationData.value?.snapshot?.monitor_time
  if (!time) return '--'
  return new Date(time).toLocaleString('zh-CN')
})

const maxAQI = computed(() => {
  if (!trendData.value?.length) return null
  return Math.max(...trendData.value.map(d => d.aqi))
})

const minAQI = computed(() => {
  if (!trendData.value?.length) return null
  return Math.min(...trendData.value.map(d => d.aqi))
})

const avgAQI = computed(() => {
  if (!trendData.value?.length) return null
  const sum = trendData.value.reduce((acc, d) => acc + d.aqi, 0)
  return Math.round(sum / trendData.value.length)
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

const formatPollutantValue = (value) => {
  if (value === null || value === undefined || value === '') return '--'
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return '--'
  return num.toFixed(1)
}

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const goBack = () => {
  router.back()
}

const goToCity = () => {
  const cityCode = stationData.value?.city_code
  if (cityCode) {
    router.push({ path: '/city', query: { code: cityCode } })
  }
}

const refreshData = () => {
  fetchData()
}

const fetchData = async () => {
  const stationCode = route.query.code
  if (!stationCode) {
    error.value = true
    loading.value = false
    return
  }

  loading.value = true
  error.value = false

  try {
    const [detailRes, trendRes] = await Promise.all([
      getStationDetail(stationCode),
      getStationTrend(stationCode)
    ])

    if (detailRes.code === 0) {
      stationData.value = detailRes.data
      updateTime.value = new Date(detailRes.data?.snapshot?.monitor_time).toLocaleString('zh-CN')
    } else {
      error.value = true
    }

    if (trendRes.code === 0) {
      trendData.value = trendRes.data?.trend || []
    }
  } catch (err) {
    console.error('Failed to fetch station detail:', err)
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
.station-detail-page {
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

.divider {
  color: var(--border);
}

.update-time {
  font-family: var(--font-mono);
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: var(--spacing-lg);
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

/* Info Card */
.info-list {
  padding: var(--spacing-lg);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
  font-size: 14px;
}

.info-row:not(:last-child) {
  border-bottom: 1px solid var(--border);
}

.info-label {
  color: var(--text-secondary);
}

.info-value {
  font-weight: 500;
  color: var(--text);
  font-family: var(--font-mono);
}

/* Chart Container */
.chart-container {
  padding: var(--spacing-lg);
  min-height: 380px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  padding: 0 var(--spacing-lg) var(--spacing-lg);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.stat-item {
  text-align: center;
  padding: var(--spacing-md);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  font-family: var(--font-mono);
}

.stat-item.stat-danger .stat-value { color: var(--error); }
.stat-item.stat-success .stat-value { color: var(--success); }
.stat-item .stat-value { color: var(--stat-color, #94A3B8); }

/* Loading & Error */
.loading-container {
  padding: var(--spacing-2xl);
}

.error-container {
  padding: var(--spacing-2xl);
}

/* Responsive */
@media (max-width: 768px) {
  .station-detail-page {
    padding: var(--spacing-md);
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .pollutants-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
