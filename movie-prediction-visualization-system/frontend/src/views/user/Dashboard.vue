<script setup>
import { ref, onMounted, computed, nextTick, onUnmounted } from 'vue'
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
    route: '/boxoffice',
    gradient: 'from-amber-500/20 to-amber-600/20',
    borderColor: 'border-amber-500/30',
    textColor: 'text-amber-400',
    iconBg: 'bg-amber-500/20'
  },
  {
    title: '可视化图表',
    subtitle: '查看数据分析',
    icon: TrendCharts,
    route: '/visualization',
    gradient: 'from-cyan-500/20 to-cyan-600/20',
    borderColor: 'border-cyan-500/30',
    textColor: 'text-cyan-400',
    iconBg: 'bg-cyan-500/20'
  },
  {
    title: '未来预测',
    subtitle: '预测票房趋势',
    icon: VideoCamera,
    route: '/prediction',
    gradient: 'from-red-500/20 to-red-600/20',
    borderColor: 'border-red-500/30',
    textColor: 'text-red-400',
    iconBg: 'bg-red-500/20'
  },
  {
    title: '个人中心',
    subtitle: '管理个人信息',
    icon: Calendar,
    route: '/profile',
    gradient: 'from-emerald-500/20 to-emerald-600/20',
    borderColor: 'border-emerald-500/30',
    textColor: 'text-emerald-400',
    iconBg: 'bg-emerald-500/20'
  }
]

// Stat cards configuration
const statCards = [
  {
    key: 'todayBoxOffice',
    title: '今日大盘票房（万元）',
    icon: Money,
    gradient: 'from-amber-500/20 to-amber-600/20',
    borderColor: 'border-amber-500/30',
    textColor: 'text-amber-400',
    iconBg: 'bg-amber-500/20',
    format: (value) => ((value || 0) / 10000).toFixed(2)
  },
  {
    key: 'totalMovies',
    title: '影片总数',
    icon: VideoCamera,
    gradient: 'from-cyan-500/20 to-cyan-600/20',
    borderColor: 'border-cyan-500/30',
    textColor: 'text-cyan-400',
    iconBg: 'bg-cyan-500/20'
  },
  {
    key: 'totalCinemas',
    title: '影院总数',
    icon: Calendar,
    gradient: 'from-emerald-500/20 to-emerald-600/20',
    borderColor: 'border-emerald-500/30',
    textColor: 'text-emerald-400',
    iconBg: 'bg-emerald-500/20'
  },
  {
    key: 'weeklyChampion',
    title: '本周票房冠军',
    icon: Trophy,
    gradient: 'from-red-500/20 to-red-600/20',
    borderColor: 'border-red-500/30',
    textColor: 'text-red-400',
    iconBg: 'bg-red-500/20',
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
      backgroundColor: 'rgba(10, 10, 18, 0.9)',
      borderColor: 'rgba(245, 158, 11, 0.3)',
      textStyle: { color: '#f1f5f9' }
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
          borderColor: '#0a0a12',
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
            color: '#f1f5f9'
          },
          itemStyle: {
            shadowBlur: 15,
            shadowOffsetX: 0,
            shadowColor: 'rgba(245, 158, 11, 0.3)'
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
      backgroundColor: 'rgba(10, 10, 18, 0.9)',
      borderColor: 'rgba(245, 158, 11, 0.3)',
      textStyle: { color: '#f1f5f9' },
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
            { offset: 0, color: '#f59e0b' },
            { offset: 1, color: '#d97706' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#fbbf24' },
              { offset: 1, color: '#f59e0b' }
            ]),
            shadowBlur: 10,
            shadowColor: 'rgba(245, 158, 11, 0.3)'
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
  <div class="dashboard-container">
    <!-- Welcome header -->
    <div class="welcome-section animate-fade-in">
      <div class="glass-card welcome-card">
        <div class="welcome-content">
          <div class="user-greeting">
            <div class="avatar-large">
              <span class="avatar-text">
                {{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
              </span>
            </div>
            <div class="greeting-text">
              <h1 class="greeting-title">{{ currentGreeting }}，{{ userStore.user?.real_name || userStore.user?.username || '用户' }}</h1>
              <p class="greeting-subtitle">欢迎来到电影票房预测系统</p>
            </div>
          </div>
          <div class="time-display">
            <svg class="time-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="time-text">{{ currentTime }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Stat cards -->
    <div class="stats-grid">
      <div
        v-for="(card, index) in statCards"
        :key="card.key"
        class="stat-card animate-slide-up"
        :style="{ animationDelay: `${index * 0.05}s` }"
      >
        <div class="glass-card stat-card-inner" :class="card.borderColor">
          <div class="stat-header">
            <div class="stat-icon" :class="[card.iconBg, card.textColor]">
              <component :is="card.icon" class="w-6 h-6" />
            </div>
            <span class="stat-badge">实时</span>
          </div>
          <div class="stat-value" :class="card.textColor">
            {{ card.format ? card.format(dashboardStats[card.key]) : (dashboardStats[card.key] || 0) }}
          </div>
          <div class="stat-title">{{ card.title }}</div>
        </div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="actions-section animate-slide-up" style="animation-delay: 0.1s">
      <h2 class="section-title">
        <svg class="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
        快捷操作
      </h2>
      <div class="actions-grid">
        <div
          v-for="(action, index) in quickActions"
          :key="action.title"
          class="action-card animate-slide-up"
          :style="{ animationDelay: `${0.15 + index * 0.05}s` }"
          @click="handleQuickAction(action.route)"
        >
          <div class="glass-card action-card-inner" :class="action.borderColor">
            <div class="action-icon" :class="[action.iconBg, action.textColor]">
              <component :is="action.icon" class="w-5 h-5" />
            </div>
            <h3 class="action-title">{{ action.title }}</h3>
            <p class="action-subtitle">{{ action.subtitle }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts and rankings -->
    <div class="charts-grid">
      <!-- Top10 Box Office Chart -->
      <div class="chart-section animate-slide-up" style="animation-delay: 0.2s">
        <h2 class="section-title">
          <svg class="section-icon text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          票房总榜 Top10
        </h2>
        <div class="glass-card chart-card">
          <div v-if="topMovies.length === 0" class="empty-state">
            <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"></path>
            </svg>
            <p>暂无数据</p>
          </div>
          <div v-else ref="top10ChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- Genre distribution chart -->
      <div class="chart-section animate-slide-up" style="animation-delay: 0.25s">
        <h2 class="section-title">
          <svg class="section-icon text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"></path>
          </svg>
          类型分布
        </h2>
        <div class="glass-card chart-card">
          <div ref="genreChartRef" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Dashboard Container
   ======================================== */
.dashboard-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* ========================================
   Animations
   ======================================== */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }
.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* ========================================
   Glass Card
   ======================================== */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  transition: all 0.3s ease;
}

.glass-card:hover {
  border-color: rgba(245, 158, 11, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ========================================
   Welcome Section
   ======================================== */
.welcome-section {
  margin-bottom: 2rem;
}

.welcome-card {
  padding: 1.5rem 2rem;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.user-greeting {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar-large {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.avatar-large::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
}

.avatar-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  position: relative;
  z-index: 1;
}

.greeting-text {
  display: flex;
  flex-direction: column;
}

.greeting-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
}

.greeting-subtitle {
  color: #94a3b8;
  margin-top: 0.25rem;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.time-icon {
  width: 20px;
  height: 20px;
  color: #94a3b8;
}

.time-text {
  font-family: 'Courier New', monospace;
  font-size: 0.9375rem;
  color: #94a3b8;
}

/* ========================================
   Stats Grid
   ======================================== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  opacity: 0;
}

.stat-card-inner {
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card-inner:hover {
  transform: translateY(-4px);
  border-color: rgba(245, 158, 11, 0.3);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.4),
    0 0 20px rgba(245, 158, 11, 0.1);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-badge {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-title {
  font-size: 0.875rem;
  color: #94a3b8;
}

/* ========================================
   Actions Section
   ======================================== */
.actions-section {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 1rem;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: #f59e0b;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.action-card {
  opacity: 0;
  cursor: pointer;
}

.action-card-inner {
  padding: 1.25rem;
  transition: all 0.3s ease;
}

.action-card-inner:hover {
  transform: scale(1.02);
  border-color: rgba(245, 158, 11, 0.4);
}

.action-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.action-title {
  font-size: 1rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.25rem;
}

.action-subtitle {
  font-size: 0.8125rem;
  color: #94a3b8;
}

/* ========================================
   Charts Grid
   ======================================== */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.chart-section {
  opacity: 0;
}

.chart-card {
  padding: 1.5rem;
}

.chart-container {
  height: 300px;
}

.empty-state {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #64748b;
  gap: 1rem;
}

.empty-icon {
  width: 48px;
  height: 48px;
  opacity: 0.5;
}

/* ========================================
   Responsive Design
   ======================================== */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .welcome-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .time-display {
    width: 100%;
    justify-content: center;
  }

  .stats-grid,
  .actions-grid,
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .greeting-title {
    font-size: 1.25rem;
  }
}
</style>
