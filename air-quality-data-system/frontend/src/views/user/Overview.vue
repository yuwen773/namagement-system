<template>
  <div class="overview-container min-h-screen bg-slate-950 relative overflow-hidden">
    <!-- Animated background grid -->
    <div class="grid-background absolute inset-0 opacity-20 pointer-events-none"></div>

    <!-- Floating particles for air flow effect -->
    <div class="particles-container absolute inset-0 overflow-hidden pointer-events-none">
      <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>

    <!-- Main content -->
    <div class="relative z-10 p-6 lg:p-8">
      <!-- Header section -->
      <header class="mb-8 animate-fade-in-down">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 class="text-3xl lg:text-4xl font-bold text-white mb-2" style="font-family: 'Rajdhani', sans-serif;">
              全国空气质量监测
            </h1>
            <p class="text-slate-400 text-sm" style="font-family: 'IBM Plex Sans', sans-serif;">
              实时数据 · 精准监测 · 科学防护
            </p>
          </div>
          <div class="flex items-center gap-3">
            <div class="status-indicator flex items-center gap-2 px-4 py-2 bg-slate-900/50 backdrop-blur-sm rounded-lg border border-slate-700/50">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span class="text-slate-300 text-xs font-mono">LIVE</span>
            </div>
            <div class="text-slate-400 text-xs font-mono" style="font-family: 'JetBrains Mono', monospace;">
              {{ currentTime }}
            </div>
          </div>
        </div>
      </header>

      <!-- Core metrics cards row -->
      <section class="mb-8 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
        <!-- Main AQI card - larger -->
        <div class="lg:col-span-2 glass-card rounded-2xl p-6 relative overflow-hidden group hover-scale cursor-pointer animate-fade-in" style="animation-delay: 0.1s;">
          <div class="absolute top-0 right-0 w-32 h-32 rounded-full opacity-10 blur-3xl group-hover:opacity-20 transition-opacity" :style="{ background: aqiColor }"></div>
          <div class="relative z-10">
            <div class="text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">全国平均 AQI</div>
            <div class="flex items-baseline gap-3">
              <span class="text-5xl lg:text-6xl font-bold" :style="{ color: aqiColor, fontFamily: 'JetBrains Mono, monospace' }">
                {{ overviewData?.national?.aqi || '--' }}
              </span>
              <span class="text-lg px-3 py-1 rounded-full text-sm font-medium" :style="{ background: `${aqiColor}20`, color: aqiColor, fontFamily: 'Rajdhani, sans-serif' }">
                {{ aqiLevelText }}
              </span>
            </div>
            <div class="mt-4 grid grid-cols-3 gap-2 text-xs">
              <div class="text-slate-500">PM2.5: <span class="text-slate-300 font-mono">{{ overviewData?.national?.pm25?.toFixed(1) || '--' }}</span></div>
              <div class="text-slate-500">PM10: <span class="text-slate-300 font-mono">{{ overviewData?.national?.pm10?.toFixed(1) || '--' }}</span></div>
              <div class="text-slate-500">O3: <span class="text-slate-300 font-mono">{{ overviewData?.national?.o3?.toFixed(1) || '--' }}</span></div>
            </div>
          </div>
        </div>

        <!-- Pollutant cards -->
        <div v-for="pollutant in pollutants" :key="pollutant.key"
             class="glass-card rounded-xl p-4 relative overflow-hidden group hover-scale cursor-pointer animate-fade-in"
             :style="{ animationDelay: `${0.15 + pollutant.index * 0.05}s` }">
          <div class="absolute top-0 right-0 w-20 h-20 rounded-full opacity-5 blur-2xl group-hover:opacity-10 transition-opacity" :style="{ background: pollutant.color }"></div>
          <div class="relative z-10">
            <div class="text-slate-400 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">{{ pollutant.label }}</div>
            <div class="text-2xl font-bold font-mono" :style="{ color: pollutant.color }">
              {{ overviewData?.national?.[pollutant.key]?.toFixed(1) || '--' }}
            </div>
            <div class="text-slate-500 text-xs mt-1">{{ pollutant.unit }}</div>
          </div>
        </div>

        <!-- City count card -->
        <div class="glass-card rounded-xl p-4 relative overflow-hidden group hover-scale cursor-pointer animate-fade-in" style="animation-delay: 0.45s;">
          <div class="relative z-10">
            <div class="text-slate-400 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">覆盖城市</div>
            <div class="text-2xl font-bold font-mono text-cyan-400">
              {{ overviewData?.city_count || '--' }}
            </div>
            <div class="text-slate-500 text-xs mt-1">个监测点</div>
          </div>
        </div>
      </section>

      <!-- Main content grid -->
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <!-- Map section - takes 2 columns -->
        <div class="xl:col-span-2 space-y-6">
          <!-- Map card -->
          <div class="glass-card rounded-2xl p-6 animate-fade-in" style="animation-delay: 0.5s;">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-white flex items-center gap-2" style="font-family: 'Rajdhani', sans-serif;">
                <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path>
                </svg>
                全国 AQI 分布
              </h2>
              <div class="flex items-center gap-2">
                <div class="flex items-center gap-1 text-xs text-slate-400">
                  <span class="w-3 h-3 rounded-sm" style="background: #00e400;"></span>
                  <span>优</span>
                </div>
                <div class="flex items-center gap-1 text-xs text-slate-400">
                  <span class="w-3 h-3 rounded-sm" style="background: #ffff00;"></span>
                  <span>良</span>
                </div>
                <div class="flex items-center gap-1 text-xs text-slate-400">
                  <span class="w-3 h-3 rounded-sm" style="background: #ff7e00;"></span>
                  <span>轻度</span>
                </div>
                <div class="flex items-center gap-1 text-xs text-slate-400">
                  <span class="w-3 h-3 rounded-sm" style="background: #ff0000;"></span>
                  <span>中度</span>
                </div>
              </div>
            </div>
            <div class="relative h-[400px] lg:h-[500px] rounded-xl overflow-hidden bg-slate-900/50">
              <MapChart
                v-if="overviewData?.map_data?.length"
                :data="overviewData.map_data"
                :roam="true"
                :zoom="1.2"
                @city-click="handleCityClick"
              />
              <div v-else class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="w-16 h-16 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mb-4 mx-auto"></div>
                  <p class="text-slate-400">地图加载中...</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick navigation -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <router-link
              v-for="nav in quickNav"
              :key="nav.path"
              :to="nav.path"
              class="glass-card rounded-xl p-4 group hover-scale cursor-pointer animate-fade-in"
              style="animation-delay: 0.55s;"
            >
              <div class="flex flex-col items-center text-center">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform" :style="{ background: `${nav.color}20` }">
                  <svg class="w-6 h-6" :style="{ color: nav.color }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="nav.icon"></path>
                  </svg>
                </div>
                <span class="text-white text-sm font-medium" style="font-family: 'Rajdhani', sans-serif;">{{ nav.label }}</span>
                <span class="text-slate-500 text-xs mt-1">{{ nav.desc }}</span>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Right sidebar -->
        <div class="space-y-6">
          <!-- Top cities ranking -->
          <div class="glass-card rounded-2xl p-6 animate-fade-in" style="animation-delay: 0.6s;">
            <h2 class="text-lg font-semibold text-white mb-4 flex items-center gap-2" style="font-family: 'Rajdhani', sans-serif;">
              <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              城市排行榜
            </h2>

            <!-- Best cities -->
            <div class="mb-6">
              <div class="flex items-center gap-2 mb-3">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span class="text-slate-400 text-xs uppercase tracking-wider">空气质量最佳</span>
              </div>
              <div class="space-y-2">
                <div
                  v-for="(city, index) in topCities?.best?.slice(0, 5)"
                  :key="city.city_code"
                  class="flex items-center justify-between p-3 rounded-lg bg-slate-900/30 hover:bg-slate-900/50 cursor-pointer transition-colors group"
                  @click="goToCity(city.city_code)"
                >
                  <div class="flex items-center gap-3">
                    <span class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-slate-800" :class="getRankBadgeClass(index)">
                      {{ index + 1 }}
                    </span>
                    <span class="text-slate-300 text-sm group-hover:text-white transition-colors">{{ city.city_name }}</span>
                  </div>
                  <span class="text-lg font-bold font-mono text-emerald-400">{{ city.aqi }}</span>
                </div>
              </div>
            </div>

            <!-- Worst cities -->
            <div>
              <div class="flex items-center gap-2 mb-3">
                <span class="w-2 h-2 rounded-full bg-red-400"></span>
                <span class="text-slate-400 text-xs uppercase tracking-wider">空气质量较差</span>
              </div>
              <div class="space-y-2">
                <div
                  v-for="(city, index) in topCities?.worst?.slice(0, 5)"
                  :key="city.city_code"
                  class="flex items-center justify-between p-3 rounded-lg bg-slate-900/30 hover:bg-slate-900/50 cursor-pointer transition-colors group"
                  @click="goToCity(city.city_code)"
                >
                  <div class="flex items-center gap-3">
                    <span class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white" :class="getRankBadgeClass(index, true)">
                      {{ index + 1 }}
                    </span>
                    <span class="text-slate-300 text-sm group-hover:text-white transition-colors">{{ city.city_name }}</span>
                  </div>
                  <span class="text-lg font-bold font-mono" :style="{ color: getAQIColor(city.aqi) }">{{ city.aqi }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Announcements -->
          <div class="glass-card rounded-2xl p-6 animate-fade-in" style="animation-delay: 0.65s;">
            <h2 class="text-lg font-semibold text-white mb-4 flex items-center gap-2" style="font-family: 'Rajdhani', sans-serif;">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"></path>
              </svg>
              系统公告
            </h2>
            <div v-if="announcements?.length" class="space-y-3">
              <div
                v-for="announcement in announcements"
                :key="announcement.id"
                class="p-3 rounded-lg bg-slate-900/30 hover:bg-slate-900/50 cursor-pointer transition-colors group"
                @click="goToArticle(announcement.id)"
              >
                <div class="flex items-start gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-blue-400 mt-2 flex-shrink-0"></span>
                  <div class="flex-1 min-w-0">
                    <p class="text-slate-300 text-sm group-hover:text-white transition-colors line-clamp-2">
                      {{ announcement.title }}
                    </p>
                    <p class="text-slate-500 text-xs mt-1 font-mono">{{ formatDate(announcement.created_at) }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-slate-500 text-sm">
              <svg class="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
              </svg>
              暂无公告
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading overlay -->
    <div v-if="loading" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="text-center">
        <div class="w-20 h-20 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mb-6 mx-auto"></div>
        <p class="text-slate-400 text-lg" style="font-family: 'Rajdhani', sans-serif;">数据加载中...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { MapChart } from '@/components/charts'
import { getOverview, getTopCities, getAnnouncements } from '@/api/airquality'

const router = useRouter()

// State
const loading = ref(true)
const overviewData = ref(null)
const topCities = ref(null)
const announcements = ref(null)
const currentTime = ref('')
let timeInterval = null

// Pollutants configuration
const pollutants = [
  { key: 'pm25', label: 'PM2.5', unit: 'μg/m³', color: '#f97316', index: 0 },
  { key: 'pm10', label: 'PM10', unit: 'μg/m³', color: '#ef4444', index: 1 },
  { key: 'so2', label: 'SO₂', unit: 'μg/m³', color: '#8b5cf6', index: 2 },
  { key: 'no2', label: 'NO₂', unit: 'μg/m³', color: '#06b6d4', index: 3 },
  { key: 'co', label: 'CO', unit: 'mg/m³', color: '#ec4899', index: 4 },
  { key: 'o3', label: 'O₃', unit: 'μg/m³', color: '#14b8a6', index: 5 }
]

// Quick navigation items
const quickNav = [
  {
    path: '/historical',
    label: '历史查询',
    desc: '查看历史数据',
    color: '#3b82f6',
    icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
  },
  {
    path: '/analysis',
    label: '数据分析',
    desc: '城市对比分析',
    color: '#8b5cf6',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  },
  {
    path: '/protection',
    label: '防护指南',
    desc: '健康防护建议',
    color: '#10b981',
    icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z'
  },
  {
    path: '/knowledge',
    label: '科普知识',
    desc: '了解空气质量',
    color: '#f59e0b',
    icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'
  }
]

// Computed
const aqiColor = computed(() => {
  const aqi = overviewData.value?.national?.aqi
  if (!aqi) return '#64748b'
  return getAQIColor(aqi)
})

const aqiLevelText = computed(() => {
  const aqi = overviewData.value?.national?.aqi
  if (!aqi) return '--'
  return getAQILevelText(aqi)
})

// Methods
const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#00e400'
  if (aqi <= 100) return '#ffff00'
  if (aqi <= 150) return '#ff7e00'
  if (aqi <= 200) return '#ff0000'
  if (aqi <= 300) return '#99004c'
  return '#7e0023'
}

const getAQILevelText = (aqi) => {
  if (aqi <= 50) return '优'
  if (aqi <= 100) return '良'
  if (aqi <= 150) return '轻度污染'
  if (aqi <= 200) return '中度污染'
  if (aqi <= 300) return '重度污染'
  return '严重污染'
}

const getRankBadgeClass = (index, isWorst = false) => {
  if (index === 0) return isWorst ? 'bg-red-500' : 'bg-yellow-400'
  if (index === 1) return isWorst ? 'bg-orange-500' : 'bg-slate-300'
  if (index === 2) return isWorst ? 'bg-amber-600' : 'bg-amber-600'
  return 'bg-slate-600'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
}

const getParticleStyle = (i) => {
  const size = Math.random() * 3 + 1
  const left = Math.random() * 100
  const delay = Math.random() * 5
  const duration = 15 + Math.random() * 10
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}

const handleCityClick = (cityCode) => {
  goToCity(cityCode)
}

const goToCity = (cityCode) => {
  router.push({ path: '/city', query: { code: cityCode } })
}

const goToArticle = (articleId) => {
  router.push({ path: '/article', query: { id: articleId } })
}

const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
}

const fetchData = async () => {
  loading.value = true
  try {
    const [overviewRes, topCitiesRes, announcementsRes] = await Promise.all([
      getOverview(),
      getTopCities(),
      getAnnouncements()
    ])

    if (overviewRes.code === 0) {
      overviewData.value = overviewRes.data
    }
    if (topCitiesRes.code === 0) {
      topCities.value = topCitiesRes.data
    }
    if (announcementsRes.code === 0) {
      announcements.value = announcementsRes.data
    }
  } catch (error) {
    console.error('Failed to fetch overview data:', error)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchData()
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Glass card effect */
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.3),
    0 2px 4px -2px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  border-color: rgba(148, 163, 184, 0.2);
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.4),
    0 4px 6px -4px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
}

/* Grid background */
.grid-background {
  background-image:
    linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* Floating particles */
.particles-container .particle {
  position: absolute;
  bottom: -10px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.6) 0%, transparent 70%);
  border-radius: 50%;
  animation: float-up linear infinite;
}

@keyframes float-up {
  0% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.3;
  }
  100% {
    transform: translateY(-100vh) translateX(calc(var(--tw-x, 0) * 1px)) scale(0.5);
    opacity: 0;
  }
}

/* Status indicator pulse */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(52, 211, 153, 0);
  }
}

.status-indicator .animate-pulse {
  animation: pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Hover scale effect */
.hover-scale {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-scale:hover {
  transform: translateY(-2px) scale(1.01);
}

/* Fade in animations */
.animate-fade-in {
  animation: fade-in 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

.animate-fade-in-down {
  animation: fade-in-down 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

/* Line clamp for text truncation */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar */
.glass-card::-webkit-scrollbar {
  width: 6px;
}

.glass-card::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.5);
  border-radius: 3px;
}

.glass-card::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 3px;
}

.glass-card::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}
</style>
