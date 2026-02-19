<template>
  <div class="overview-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">全国空气质量概览</h1>
        <p class="page-subtitle">实时监测全国城市空气质量状况</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.key" class="stat-card" :class="stat.color">
        <div class="stat-icon">
          <el-icon :size="24"><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
        <div class="stat-trend" :class="stat.trendClass">
          <el-icon><component :is="stat.trendIcon" /></el-icon>
          <span>{{ stat.trend }}</span>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Map Chart -->
      <div class="chart-card map-card">
        <div class="card-header">
          <h3 class="card-title">全国 AQI 分布</h3>
          <el-select v-model="selectedMetric" size="small" style="width: 120px">
            <el-option label="AQI" value="aqi" />
            <el-option label="PM2.5" value="pm25" />
            <el-option label="PM10" value="pm10" />
            <el-option label="O3" value="o3" />
          </el-select>
        </div>
        <div class="card-body">
          <MapChart v-if="mapData.length > 0" :data="mapData" height="400px" />
          <div v-else class="chart-loading">
            <el-skeleton :rows="8" animated />
          </div>
        </div>
      </div>

      <!-- Top Cities -->
      <div class="chart-card ranking-card">
        <div class="card-header">
          <h3 class="card-title">城市 AQI 排名</h3>
          <el-radio-group v-model="rankingType" size="small">
            <el-radio-button value="best">最优</el-radio-button>
            <el-radio-button value="worst">最差</el-radio-button>
          </el-radio-group>
        </div>
        <div class="card-body">
          <div v-if="topCities.length > 0" class="ranking-list">
            <div
              v-for="(city, index) in topCities"
              :key="city.city_code"
              class="ranking-item"
              @click="goToCity(city.city_code)"
            >
              <div class="ranking-number" :class="`rank-${index + 1}`">{{ index + 1 }}</div>
              <div class="ranking-info">
                <div class="city-name">{{ city.city_name }}</div>
                <div class="city-location">{{ city.province }}</div>
              </div>
              <div class="ranking-aqi">
                <span class="aqi-value" :style="{ color: getAQIColor(city.aqi) }">{{ city.aqi }}</span>
                <span class="aqi-level" :style="{ background: getAQIBgColor(city.aqi) }">
                  {{ getAQILevel(city.aqi) }}
                </span>
              </div>
            </div>
          </div>
          <div v-else class="chart-loading">
            <el-skeleton :rows="5" animated />
          </div>
        </div>
      </div>
    </div>

    <!-- Pollutants and Announcements -->
    <div class="content-grid">
      <!-- Pollutants Overview -->
      <div class="chart-card pollutants-card">
        <div class="card-header">
          <h3 class="card-title">主要污染物浓度</h3>
          <el-select v-model="pollutantCity" size="small" placeholder="选择城市" style="width: 150px">
            <el-option label="全国平均" value="" />
            <el-option
              v-for="city in majorCities"
              :key="city.city_code"
              :label="city.city_name"
              :value="city.city_code"
            />
          </el-select>
        </div>
        <div class="card-body">
          <div v-if="pollutantData" class="pollutants-grid">
            <div v-for="pollutant in pollutants" :key="pollutant.key" class="pollutant-item">
              <div class="pollutant-header">
                <span class="pollutant-name">{{ pollutant.name }}</span>
                <span class="pollutant-unit">μg/m³</span>
              </div>
              <div class="pollutant-value">{{ pollutantData[pollutant.key] || '-' }}</div>
              <div class="pollutant-bar">
                <div
                  class="pollutant-fill"
                  :style="{
                    width: getPollutantPercent(pollutantData[pollutant.key], pollutant.max) + '%',
                    background: getPollutantColor(pollutantData[pollutant.key], pollutant.max)
                  }"
                />
              </div>
            </div>
          </div>
          <div v-else class="chart-loading">
            <el-skeleton :rows="4" animated />
          </div>
        </div>
      </div>

      <!-- Announcements -->
      <div class="chart-card announcements-card">
        <div class="card-header">
          <h3 class="card-title">最新公告</h3>
          <el-link type="primary" @click="$router.push('/announcements')">查看全部</el-link>
        </div>
        <div class="card-body">
          <div v-if="announcements.length > 0" class="announcements-list">
            <div
              v-for="notice in announcements"
              :key="notice.id"
              class="announcement-item"
              @click="viewAnnouncement(notice.id)"
            >
              <div class="announcement-badge" :class="notice.type">
                <el-icon v-if="notice.type === 'urgent'"><Warning /></el-icon>
                <el-icon v-else><Bell /></el-icon>
              </div>
              <div class="announcement-content">
                <div class="announcement-title">{{ notice.title }}</div>
                <div class="announcement-time">{{ formatDate(notice.created_at) }}</div>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无公告" :image-size="80" />
        </div>
      </div>
    </div>

    <!-- Quick Navigation -->
    <div class="quick-nav">
      <h3 class="section-title">快捷导航</h3>
      <div class="nav-grid">
        <div v-for="nav in quickNav" :key="nav.path" class="nav-item" @click="$router.push(nav.path)">
          <div class="nav-icon" :style="{ background: nav.color }">
            <el-icon :size="24">
              <component :is="nav.icon" />
            </el-icon>
          </div>
          <span class="nav-label">{{ nav.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import { Refresh, Warning, Bell, Location, ArrowUp, ArrowDown, Star, CircleCheck, Document, Search } from '@element-plus/icons-vue'
import { MapChart } from '@/components/charts'
import { getOverview, getTopCities, getAnnouncements } from '@/api/airquality'

const router = useRouter()

const loading = ref(false)
const mapData = ref([])
const rawMapData = ref([]) // Store raw data for metric switching
const topCities = ref([])
const announcements = ref([])
const pollutantData = ref(null)
const selectedMetric = ref('aqi')
const rankingType = ref('best')
const pollutantCity = ref('')

const stats = ref([
  { key: 'cities', label: '监测城市', value: '-', icon: markRaw(Location), trend: '-', trendIcon: markRaw(ArrowUp), trendClass: '', color: 'blue' },
  { key: 'avgAQI', label: '平均 AQI', value: '-', icon: markRaw(Star), trend: '-', trendIcon: markRaw(ArrowDown), trendClass: 'down', color: 'green' },
  { key: 'excellent', label: '优良率', value: '-', icon: markRaw(ArrowUp), trend: '-', trendIcon: markRaw(ArrowUp), trendClass: 'up', color: 'cyan' },
  { key: 'warnings', label: '预警城市', value: '-', icon: markRaw(Warning), trend: '-', trendIcon: markRaw(ArrowDown), trendClass: 'down', color: 'orange' }
])

const pollutants = [
  { key: 'pm25', name: 'PM2.5', max: 100 },
  { key: 'pm10', name: 'PM10', max: 150 },
  { key: 'o3', name: 'O3', max: 200 },
  { key: 'no2', name: 'NO2', max: 80 },
  { key: 'so2', name: 'SO2', max: 50 },
  { key: 'co', name: 'CO', max: 10 }
]

const quickNav = [
  { label: '城市详情', path: '/cities', icon: markRaw(Location), color: 'linear-gradient(135deg, #0066CC, #0052A3)' },
  { label: '历史数据', path: '/historical', icon: markRaw(Search), color: 'linear-gradient(135deg, #0EA5E9, #0284C7)' },
  { label: '数据分析', path: '/analysis', icon: markRaw(Star), color: 'linear-gradient(135deg, #10B981, #059669)' },
  { label: '防护指南', path: '/protection', icon: markRaw(CircleCheck), color: 'linear-gradient(135deg, #10B981, #059669)' },
  { label: '科普知识', path: '/knowledge', icon: markRaw(Document), color: 'linear-gradient(135deg, #8B5CF6, #7C3AED)' }
]

const majorCities = computed(() => {
  return topCities.value.slice(0, 10).map(city => ({
    city_code: city.city_code,
    city_name: city.city_name
  }))
})

const fetchOverview = async () => {
  try {
    const response = await getOverview()
    // Store raw data for metric switching
    rawMapData.value = response.data.map_data || []
    updateMapData()
    // Backend returns national object with pollutant data
    const national = response.data.national || {}
    pollutantData.value = {
      pm25: national.pm25,
      pm10: national.pm10,
      o3: national.o3,
      no2: national.no2,
      so2: national.so2,
      co: national.co
    }

    // Update stats - create new array to trigger reactivity
    const excellentCount = rawMapData.value.filter(city => city.aqi <= 100).length
    const excellentRate = rawMapData.value.length > 0
      ? Math.round((excellentCount / rawMapData.value.length) * 100)
      : 0
    const warningCount = rawMapData.value.filter(city => city.aqi > 150).length

    stats.value = [
      { ...stats.value[0], value: response.data.city_count || '-' },
      { ...stats.value[1], value: national.aqi || '-' },
      { ...stats.value[2], value: excellentRate + '%' },
      { ...stats.value[3], value: warningCount || '-' }
    ]
  } catch (error) {
    console.error('Failed to fetch overview:', error)
  }
}

const fetchTopCities = async () => {
  try {
    const response = await getTopCities({ limit: 10 })
    // Backend returns { best: [...], worst: [...] }
    const key = rankingType.value === 'best' ? 'best' : 'worst'
    topCities.value = response.data[key] || []
  } catch (error) {
    console.error('Failed to fetch top cities:', error)
  }
}

const fetchAnnouncements = async () => {
  try {
    const response = await getAnnouncements({ limit: 5 })
    // API returns data as array directly
    announcements.value = response.data || []
  } catch (error) {
    console.error('Failed to fetch announcements:', error)
  }
}

const refreshData = () => {
  fetchOverview()
  fetchTopCities()
  fetchAnnouncements()
}

// Metric field mapping
const metricFields = {
  aqi: 'aqi',
  pm25: 'pm25',
  pm10: 'pm10',
  o3: 'o3'
}

// Update map data based on selected metric
const updateMapData = () => {
  const field = metricFields[selectedMetric.value] || 'aqi'
  mapData.value = rawMapData.value
    .filter(item => item && item.city_name && item[field] !== null && item[field] !== undefined)
    .map(item => ({
      name: item.city_name,
      value: item[field]
    }))
}

const goToCity = (cityCode) => {
  router.push(`/city/${cityCode}`)
}

const viewAnnouncement = (id) => {
  router.push(`/announcements/${id}`)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  return '刚刚'
}

const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#10B981'
  if (aqi <= 100) return '#FBBF24'
  if (aqi <= 150) return '#F97316'
  if (aqi <= 200) return '#EF4444'
  if (aqi <= 300) return '#A855F7'
  return '#7F1D1D'
}

const getAQIBgColor = (aqi) => {
  const color = getAQIColor(aqi)
  return color + '20'
}

const getAQILevel = (aqi) => {
  if (aqi <= 50) return '优'
  if (aqi <= 100) return '良'
  if (aqi <= 150) return '轻度'
  if (aqi <= 200) return '中度'
  if (aqi <= 300) return '重度'
  return '严重'
}

const getPollutantPercent = (value, max) => {
  if (!value) return 0
  return Math.min((value / max) * 100, 100)
}

const getPollutantColor = (value, max) => {
  if (!value) return '#E2E8F0'
  const percent = value / max
  if (percent <= 0.5) return '#10B981'
  if (percent <= 0.8) return '#FBBF24'
  return '#EF4444'
}

watch(rankingType, () => {
  fetchTopCities()
})

watch(selectedMetric, () => {
  updateMapData()
})

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.overview-page {
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
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
  margin-top: var(--spacing-xs);
}

.header-actions {
  display: flex;
  gap: var(--spacing-md);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: all var(--transition-base);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-card.blue .stat-icon { background: rgba(0, 102, 204, 0.1); color: var(--primary); }
.stat-card.green .stat-icon { background: rgba(16, 185, 129, 0.1); color: var(--success); }
.stat-card.cyan .stat-icon { background: rgba(14, 165, 233, 0.1); color: var(--accent); }
.stat-card.orange .stat-icon { background: rgba(245, 158, 11, 0.1); color: var(--warning); }

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text);
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 12px;
  font-weight: 500;
}

.stat-trend.up { color: var(--success); }
.stat-trend.down { color: var(--warning); }

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

/* Chart Card */
.chart-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
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

.card-body {
  padding: var(--spacing-lg);
  min-height: 400px;
}

.chart-loading {
  padding: var(--spacing-xl);
}

/* Ranking List */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.ranking-item:hover {
  background: var(--border-light);
  transform: translateX(4px);
}

.ranking-number {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  background: var(--bg-card);
  color: var(--text-secondary);
}

.ranking-number.rank-1 {
  background: linear-gradient(135deg, #FBBF24, #F59E0B);
  color: white;
}

.ranking-number.rank-2 {
  background: linear-gradient(135deg, #94A3B8, #64748B);
  color: white;
}

.ranking-number.rank-3 {
  background: linear-gradient(135deg, #F97316, #EA580C);
  color: white;
}

.ranking-info {
  flex: 1;
  min-width: 0;
}

.city-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}

.city-location {
  font-size: 12px;
  color: var(--text-secondary);
}

.ranking-aqi {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.aqi-value {
  font-size: 18px;
  font-weight: 700;
}

.aqi-level {
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
}

/* Pollutants Grid */
.pollutants-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

@media (max-width: 640px) {
  .pollutants-grid {
    grid-template-columns: repeat(2, 1fr);
  }
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
  margin-bottom: var(--spacing-xs);
}

.pollutant-name {
  font-size: 14px;
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
  color: var(--text);
  margin-bottom: var(--spacing-sm);
}

.pollutant-bar {
  height: 6px;
  background: var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.pollutant-fill {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--transition-slow);
}

/* Announcements List */
.announcements-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.announcement-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.announcement-item:hover {
  background: var(--border-light);
}

.announcement-badge {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.announcement-badge.urgent {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.announcement-badge.normal {
  background: rgba(0, 102, 204, 0.1);
  color: var(--primary);
}

.announcement-content {
  flex: 1;
  min-width: 0;
}

.announcement-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.announcement-time {
  font-size: 12px;
  color: var(--text-secondary);
}

/* Quick Navigation */
.quick-nav {
  margin-top: var(--spacing-xl);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-lg) 0;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--spacing-md);
}

.nav-item {
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
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.nav-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

/* Responsive */
@media (max-width: 768px) {
  .overview-page {
    padding: var(--spacing-md);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .nav-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
