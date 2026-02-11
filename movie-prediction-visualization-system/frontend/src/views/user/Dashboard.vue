<script setup>
import { ref, onMounted, computed, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getTop10Movies, getDashboardData, getTypeDistribution, getTodayBoxOffice, getWeeklyChampion } from '@/api/visualization'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  VideoCamera,
  Money,
  Calendar,
  TrendCharts,
  Trophy
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const topMovies = ref([])
const dashboardStats = ref({
  todayBoxOffice: 0,
  weeklyChampion: null,
  totalMovies: 0,
  totalCinemas: 0
})
const genreData = ref([])

// Chart references
const genreChartRef = ref(null)
const top10ChartRef = ref(null)
let genreChart = null
let top10Chart = null

// Current time and greeting
const currentTime = ref('')
const currentGreeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  if (hour < 22) return '晚上好'
  return '夜深了'
})

// Quick actions for user
const quickActions = [
  {
    title: '票房查询',
    subtitle: '查询历史票房数据',
    icon: Money,
    route: '/user/boxoffice',
    gradient: 'from-blue-500 to-blue-600',
    glowColor: 'rgba(59, 130, 246, 0.5)'
  },
  {
    title: '可视化图表',
    subtitle: '查看数据分析',
    icon: TrendCharts,
    route: '/user/visualization',
    gradient: 'from-emerald-500 to-emerald-600',
    glowColor: 'rgba(16, 185, 129, 0.5)'
  },
  {
    title: '未来预测',
    subtitle: '预测票房趋势',
    icon: VideoCamera,
    route: '/user/prediction',
    gradient: 'from-violet-500 to-violet-600',
    glowColor: 'rgba(139, 92, 246, 0.5)'
  },
  {
    title: '个人中心',
    subtitle: '管理个人信息',
    icon: Calendar,
    route: '/user/profile',
    gradient: 'from-amber-500 to-amber-600',
    glowColor: 'rgba(245, 158, 11, 0.5)'
  }
]

// Stat cards configuration
const statCards = [
  {
    key: 'todayBoxOffice',
    title: '今日大盘票房（万元）',
    icon: Money,
    gradient: 'from-blue-500/20 to-cyan-500/20',
    borderColor: 'from-blue-500 to-cyan-500',
    textColor: 'text-cyan-400',
    format: (value) => ((value || 0) / 10000).toFixed(2)
  },
  {
    key: 'totalMovies',
    title: '影片总数',
    icon: VideoCamera,
    gradient: 'from-emerald-500/20 to-green-500/20',
    borderColor: 'from-emerald-500 to-green-500',
    textColor: 'text-emerald-400'
  },
  {
    key: 'totalCinemas',
    title: '影院总数',
    icon: Calendar,
    gradient: 'from-violet-500/20 to-purple-500/20',
    borderColor: 'from-violet-500 to-purple-500',
    textColor: 'text-violet-400'
  },
  {
    key: 'weeklyChampion',
    title: '本周票房冠军',
    icon: Trophy,
    gradient: 'from-amber-500/20 to-orange-500/20',
    borderColor: 'from-amber-500 to-orange-500',
    textColor: 'text-amber-400',
    format: (value) => value?.movie_title || '-'
  }
]

// Load top 10 movies
const loadTopMovies = async () => {
  try {
    const res = await getTop10Movies()
    topMovies.value = res.data || []
  } catch (error) {
    console.error('加载Top10失败:', error)
  }
}

// Load dashboard stats
const loadDashboardStats = async () => {
  try {
    loading.value = true
    const [dashboardRes, genreRes] = await Promise.all([
      getDashboardData(),
      getTypeDistribution()
    ])

    dashboardStats.value = {
      todayBoxOffice: dashboardRes.data?.today_box_office || 0,
      weeklyChampion: dashboardRes.data?.week_champion || null,
      totalMovies: dashboardRes.data?.total_movies || 0,
      totalCinemas: dashboardRes.data?.total_cinemas || 0
    }

    genreData.value = genreRes.data || []
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

// Initialize genre chart (pie chart)
const initGenreChart = () => {
  if (!genreChartRef.value || genreData.value.length === 0) return

  if (genreChart) {
    genreChart.dispose()
  }

  genreChart = echarts.init(genreChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}万元 ({d}%)',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: 'rgba(59, 130, 246, 0.3)',
      textStyle: { color: '#e2e8f0' }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#94a3b8', fontSize: 12 },
      itemGap: 12
    },
    series: [
      {
        type: 'pie',
        radius: ['45%', '75%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#0f172a',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold',
            color: '#f8fafc'
          }
        },
        labelLine: {
          show: false
        },
        data: genreData.value.map(item => ({
          value: (item.box_office || 0) / 10000,
          name: item.type_name || '未知'
        }))
      }
    ]
  }

  genreChart.setOption(option)
}

// Initialize Top 10 bar chart
const initTop10Chart = () => {
  if (!top10ChartRef.value || topMovies.value.length === 0) return

  if (top10Chart) {
    top10Chart.dispose()
  }

  top10Chart = echarts.init(top10ChartRef.value)

  const movieNames = topMovies.value.map(m => m.title || m.movie_title)
  const boxOfficeData = topMovies.value.map(m => (m.box_office_total || m.box_office || 0) / 10000)

  const option = {
    grid: {
      left: '5%',
      right: '8%',
      top: '5%',
      bottom: '5%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: 'rgba(59, 130, 246, 0.3)',
      textStyle: { color: '#e2e8f0' },
      formatter: (params) => {
        const item = params[0]
        return `${item.name}<br/>总票房: ${item.value.toFixed(2)} 万元`
      }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.2)' } },
      axisLabel: { color: '#94a3b8', formatter: '{value}万' },
      splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.1)' } }
    },
    yAxis: {
      type: 'category',
      data: movieNames,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#e2e8f0',
        fontSize: 13,
        width: 100,
        overflow: 'truncate'
      }
    },
    series: [
      {
        type: 'bar',
        data: boxOfficeData,
        itemStyle: {
          borderRadius: [0, 8, 8, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#3b82f6' },
            { offset: 1, color: '#06b6d4' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#60a5fa' },
              { offset: 1, color: '#22d3ee' }
            ])
          }
        },
        label: {
          show: true,
          position: 'right',
          color: '#e2e8f0',
          fontSize: 12,
          formatter: '{c}万'
        },
        barWidth: '60%'
      }
    ]
  }

  top10Chart.setOption(option)
}

// Update time
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

// Handle quick action click
const handleQuickAction = (route) => {
  router.push(route)
}

// Format money
const formatMoney = (amount) => {
  if (!amount && amount !== 0) return '-'
  return (amount / 10000).toFixed(2) + '万'
}

// Handle chart resize
const handleResize = () => {
  genreChart?.resize()
  top10Chart?.resize()
}

// Watch for data changes and reinitialize charts
const initCharts = () => {
  nextTick(() => {
    initGenreChart()
    initTop10Chart()
  })
}

onMounted(async () => {
  await loadDashboardStats()
  await loadTopMovies()
  initCharts()
  updateTime()
  setInterval(updateTime, 1000)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  genreChart?.dispose()
  top10Chart?.dispose()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
    <!-- Animated background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <div class="relative z-10 p-6 lg:p-8">
      <!-- Welcome header -->
      <div class="mb-8 animate-fade-in">
        <div class="glass-card rounded-2xl p-6 border border-white/10">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center shadow-lg shadow-emerald-500/30">
                <span class="text-2xl font-bold text-white">
                  {{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
                </span>
              </div>
              <div>
                <h1 class="text-2xl font-bold text-white">
                  {{ currentGreeting }}，{{ userStore.user?.real_name || userStore.user?.username || '用户' }}
                </h1>
                <p class="text-slate-400 mt-1">欢迎来到电影票房预测系统</p>
              </div>
            </div>
            <div class="flex items-center gap-2 text-slate-400">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span class="font-mono">{{ currentTime }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stat cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div
          v-for="(card, index) in statCards"
          :key="card.key"
          class="stat-card animate-slide-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="glass-card rounded-2xl p-6 border border-white/10 h-full relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                 :class="card.gradient"></div>
            <div class="absolute inset-0 rounded-2xl bg-gradient-to-br opacity-0 group-hover:opacity-20 transition-opacity duration-500"
                 :class="card.borderColor"></div>
            <div class="relative z-10">
              <div class="flex items-start justify-between mb-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center"
                     :class="card.borderColor">
                  <component :is="card.icon" class="w-6 h-6 text-white" />
                </div>
                <span class="text-xs font-medium px-2 py-1 rounded-full bg-white/5 text-slate-400">实时</span>
              </div>
              <div class="mb-1">
                <span class="text-3xl font-bold text-white tracking-tight">
                  {{ card.format ? card.format(dashboardStats[card.key]) : (dashboardStats[card.key] || 0) }}
                </span>
              </div>
              <div class="text-sm text-slate-400">{{ card.title }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick actions -->
      <div class="mb-8 animate-slide-up" style="animation-delay: 0.4s">
        <h2 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          快捷操作
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div
            v-for="(action, index) in quickActions"
            :key="action.title"
            class="action-card cursor-pointer animate-slide-up"
            :style="{ animationDelay: `${0.5 + index * 0.1}s` }"
            @click="handleQuickAction(action.route)"
          >
            <div class="glass-card rounded-xl p-5 border border-white/10 h-full relative overflow-hidden group">
              <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-all duration-300"
                   :class="action.gradient"></div>
              <div class="absolute -inset-4 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-300"
                   :style="{ background: action.glowColor }"></div>
              <div class="relative z-10">
                <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300">
                  <component :is="action.icon" class="w-5 h-5 text-white" />
                </div>
                <h3 class="text-white font-semibold mb-1">{{ action.title }}</h3>
                <p class="text-sm text-slate-400 group-hover:text-white/80 transition-colors">{{ action.subtitle }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts and rankings -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top10 Box Office Chart -->
        <div class="animate-slide-up" style="animation-delay: 0.9s">
          <h2 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            票房总榜 Top10
          </h2>
          <div class="glass-card rounded-2xl border border-white/10 p-6">
            <div v-if="topMovies.length === 0" class="h-64 flex items-center justify-center text-slate-500">
              <p>暂无数据</p>
            </div>
            <div v-else ref="top10ChartRef" class="chart-container"></div>
          </div>
        </div>

        <!-- Genre distribution chart -->
        <div class="animate-slide-up" style="animation-delay: 1s">
          <h2 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"></path>
            </svg>
            类型分布
          </h2>
          <div class="glass-card rounded-2xl border border-white/10 p-6">
            <div ref="genreChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Grid background */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* Gradient orbs */
.gradient-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #10b981, #3b82f6);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -20px) scale(1.05); }
  50% { transform: translate(-10px, 20px) scale(0.95); }
  75% { transform: translate(-20px, -10px) scale(1.02); }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

.stat-card .glass-card { transition: all 0.3s ease; }
.stat-card:hover .glass-card {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(59, 130, 246, 0.1);
}

.action-card .glass-card { transition: all 0.3s ease; }
.action-card:hover .glass-card {
  transform: scale(1.02);
  border-color: rgba(255, 255, 255, 0.2);
}

.chart-container {
  height: 300px;
}
</style>
