<template>
  <div class="city-detail-container min-h-screen bg-slate-950 relative overflow-hidden">
    <!-- Background grid -->
    <div class="grid-background absolute inset-0 opacity-10 pointer-events-none"></div>

    <!-- Main content -->
    <div class="relative z-10 p-6 lg:p-8">
      <!-- Header with back button -->
      <header class="mb-6 animate-fade-in-down">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div class="flex items-center gap-4">
            <button
              @click="goBack"
              class="w-10 h-10 rounded-xl glass-card flex items-center justify-center hover-scale group"
            >
              <svg class="w-5 h-5 text-slate-400 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <div>
              <div class="flex items-center gap-3">
                <h1 class="text-2xl lg:text-3xl font-bold text-white" style="font-family: 'Rajdhani', sans-serif;">
                  {{ cityData?.city_name || '城市详情' }}
                </h1>
                <span class="px-3 py-1 rounded-full text-xs font-medium bg-slate-800/50 text-slate-300" style="font-family: 'JetBrains Mono', monospace;">
                  {{ cityData?.city_code || '--' }}
                </span>
              </div>
              <div class="flex items-center gap-4 mt-1 text-sm text-slate-400">
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  {{ cityData?.province_name || '--' }}
                </span>
                <span class="flex items-center gap-1" style="font-family: 'JetBrains Mono', monospace;">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  {{ cityData?.latitude?.toFixed(4) || '--' }}, {{ cityData?.longitude?.toFixed(4) || '--' }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-slate-400 text-xs">更新时间</span>
            <span class="text-slate-300 text-xs font-mono">{{ updateTime }}</span>
          </div>
        </div>
      </header>

      <!-- Main grid -->
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <!-- Left column - AQI gauge and pollutants -->
        <div class="space-y-6">
          <!-- AQI Gauge card -->
          <div class="glass-card rounded-2xl p-6 animate-fade-in" style="animation-delay: 0.1s;">
            <h2 class="text-sm text-slate-400 mb-4 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
              空气质量指数
            </h2>
            <div class="flex justify-center">
              <GaugeChart
                v-if="cityData?.snapshot?.aqi !== undefined"
                :value="cityData.snapshot.aqi"
                :size="'large'"
                :show-detail="true"
              />
              <div v-else class="w-64 h-32 flex items-center justify-center">
                <div class="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
              </div>
            </div>
            <div class="mt-4 text-center">
              <div class="text-3xl font-bold font-mono" :style="{ color: aqiColor }">
                {{ cityData?.snapshot?.aqi || '--' }}
              </div>
              <div class="text-sm mt-1" :style="{ color: aqiColor }">
                {{ aqiLevelText }}
              </div>
            </div>
          </div>

          <!-- Pollutants grid -->
          <div class="grid grid-cols-2 gap-4">
            <div
              v-for="pollutant in pollutants"
              :key="pollutant.key"
              class="glass-card rounded-xl p-4 animate-fade-in hover-scale"
              :style="{ animationDelay: `${0.15 + pollutant.index * 0.05}s` }"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="text-slate-400 text-xs" style="font-family: 'Rajdhani', sans-serif;">{{ pollutant.label }}</span>
                <span class="w-2 h-2 rounded-full" :style="{ background: pollutant.color }"></span>
              </div>
              <div class="text-2xl font-bold font-mono" :style="{ color: pollutant.color }">
                {{ cityData?.snapshot?.[pollutant.key]?.toFixed(1) || '--' }}
              </div>
              <div class="text-slate-500 text-xs mt-1">{{ pollutant.unit }}</div>
            </div>
          </div>
        </div>

        <!-- Right column - Trend and stations -->
        <div class="xl:col-span-2 space-y-6">
          <!-- Trend chart -->
          <div class="glass-card rounded-2xl p-6 animate-fade-in" style="animation-delay: 0.4s;">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm text-slate-400 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                24小时 AQI 趋势
              </h2>
              <div class="flex items-center gap-2 text-xs text-slate-500">
                <span class="w-3 h-3 rounded-sm" :style="{ background: aqiColor }"></span>
                <span>AQI</span>
              </div>
            </div>
            <div class="h-[280px]">
              <LineChart
                v-if="trendData?.length"
                :data="[{ name: 'AQI', data: trendData.map(d => d.aqi), color: aqiColor }]"
                :x-axis="trendData.map(d => formatTime(d.time))"
                :smooth="true"
                :area-style="true"
                :show-data-zoom="true"
              />
              <div v-else class="h-full flex items-center justify-center">
                <div class="text-center">
                  <div class="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mb-3 mx-auto"></div>
                  <p class="text-slate-500 text-sm">趋势数据加载中...</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Monitoring stations list -->
          <div class="glass-card rounded-2xl p-6 animate-fade-in" style="animation-delay: 0.5s;">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm text-slate-400 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                监测站点 <span class="text-slate-500">({{ cityData?.snapshot?.station_count || 0 }})</span>
              </h2>
            </div>
            <div v-if="stations.length" class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="station in stations"
                :key="station.code"
                @click="goToStation(station.code)"
                class="p-4 rounded-xl bg-slate-900/30 hover:bg-slate-900/50 cursor-pointer transition-all group"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2">
                      <span class="text-white font-medium group-hover:text-cyan-400 transition-colors truncate">
                        {{ station.name }}
                      </span>
                      <span class="px-2 py-0.5 rounded text-xs bg-slate-800 text-slate-400 flex-shrink-0">
                        {{ station.type }}
                      </span>
                    </div>
                    <p class="text-slate-500 text-xs mt-1 truncate">{{ station.address }}</p>
                  </div>
                  <div class="flex-shrink-0 ml-3">
                    <div class="text-lg font-bold font-mono" :style="{ color: getAQIColor(station.aqi) }">
                      {{ station.aqi }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-slate-500 text-sm">
              <svg class="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              暂无站点数据
            </div>
          </div>

          <!-- Quick navigation -->
          <div class="grid grid-cols-3 gap-4 animate-fade-in" style="animation-delay: 0.55s;">
            <router-link
              to="/historical"
              class="glass-card rounded-xl p-4 text-center hover-scale group"
            >
              <div class="w-10 h-10 rounded-lg flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform" style="background: rgba(59, 130, 246, 0.2);">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-white text-sm" style="font-family: 'Rajdhani', sans-serif;">历史数据</span>
            </router-link>
            <router-link
              to="/analysis"
              class="glass-card rounded-xl p-4 text-center hover-scale group"
            >
              <div class="w-10 h-10 rounded-lg flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform" style="background: rgba(139, 92, 246, 0.2);">
                <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <span class="text-white text-sm" style="font-family: 'Rajdhani', sans-serif;">数据分析</span>
            </router-link>
            <button
              @click="goToProtection"
              class="glass-card rounded-xl p-4 text-center hover-scale group w-full"
            >
              <div class="w-10 h-10 rounded-lg flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform" style="background: rgba(16, 185, 129, 0.2);">
                <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
              <span class="text-white text-sm" style="font-family: 'Rajdhani', sans-serif;">防护指南</span>
            </button>
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

    <!-- Error state -->
    <div v-if="error" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="text-center">
        <svg class="w-20 h-20 mx-auto mb-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <p class="text-slate-400 text-lg mb-4">加载失败</p>
        <button @click="goBack" class="px-6 py-2 rounded-lg bg-cyan-500 text-white hover:bg-cyan-600 transition-colors">
          返回上一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { GaugeChart, LineChart } from '@/components/charts'
import { getCityDetail, getCityTrend } from '@/api/airquality'

const router = useRouter()
const route = useRoute()

// State
const loading = ref(true)
const error = ref(false)
const cityData = ref(null)
const trendData = ref([])
const stations = ref([])
const updateTime = ref('')

// Pollutants configuration
const pollutants = [
  { key: 'pm25', label: 'PM2.5', unit: 'μg/m³', color: '#f97316', index: 0 },
  { key: 'pm10', label: 'PM10', unit: 'μg/m³', color: '#ef4444', index: 1 },
  { key: 'so2', label: 'SO₂', unit: 'μg/m³', color: '#8b5cf6', index: 2 },
  { key: 'no2', label: 'NO₂', unit: 'μg/m³', color: '#06b6d4', index: 3 },
  { key: 'co', label: 'CO', unit: 'mg/m³', color: '#ec4899', index: 4 },
  { key: 'o3', label: 'O₃', unit: 'μg/m³', color: '#14b8a6', index: 5 }
]

// Computed
const aqiColor = computed(() => {
  const aqi = cityData.value?.snapshot?.aqi
  if (!aqi) return '#64748b'
  return getAQIColor(aqi)
})

const aqiLevelText = computed(() => {
  const aqi = cityData.value?.snapshot?.aqi
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
      // Mock stations data based on station_count
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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  border-color: rgba(148, 163, 184, 0.2);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
}

.grid-background {
  background-image: linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.hover-scale {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-scale:hover {
  transform: translateY(-2px);
}

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
</style>
