<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getMovies } from '@/api/movie'
import { getCinemas } from '@/api/cinema'
import { getBoxOfficeRecords } from '@/api/boxoffice'
import { getUsers } from '@/api/user'
import { ElMessage } from 'element-plus'
import {
  VideoCamera,
  Location,
  Money,
  User,
  Plus,
  DataLine,
  OfficeBuilding,
  UserFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const stats = ref({
  movies: 0,
  cinemas: 0,
  totalBoxOffice: 0,
  users: 0
})
const recentRecords = ref([])
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

// 快捷操作配置
const quickActions = [
  {
    title: '添加影片',
    subtitle: '录入新影片信息',
    icon: VideoCamera,
    route: '/admin/movies',
    gradient: 'from-blue-500 to-blue-600',
    glowColor: 'rgba(59, 130, 246, 0.5)'
  },
  {
    title: '录入票房',
    subtitle: '添加票房数据',
    icon: Money,
    route: '/admin/boxoffice',
    gradient: 'from-emerald-500 to-emerald-600',
    glowColor: 'rgba(16, 185, 129, 0.5)'
  },
  {
    title: '添加影院',
    subtitle: '新增影院信息',
    icon: OfficeBuilding,
    route: '/admin/cinemas',
    gradient: 'from-violet-500 to-violet-600',
    glowColor: 'rgba(139, 92, 246, 0.5)'
  },
  {
    title: '用户管理',
    subtitle: '管理系统用户',
    icon: UserFilled,
    route: '/admin/users',
    gradient: 'from-amber-500 to-amber-600',
    glowColor: 'rgba(245, 158, 11, 0.5)'
  }
]

// 统计卡片配置
const statCards = [
  {
    key: 'movies',
    title: '影片总数',
    icon: VideoCamera,
    gradient: 'from-blue-500/20 to-cyan-500/20',
    borderColor: 'from-blue-500 to-cyan-500',
    textColor: 'text-cyan-400'
  },
  {
    key: 'cinemas',
    title: '影院总数',
    icon: Location,
    gradient: 'from-emerald-500/20 to-green-500/20',
    borderColor: 'from-emerald-500 to-green-500',
    textColor: 'text-emerald-400'
  },
  {
    key: 'totalBoxOffice',
    title: '累计票房（万元）',
    icon: Money,
    gradient: 'from-amber-500/20 to-orange-500/20',
    borderColor: 'from-amber-500 to-orange-500',
    textColor: 'text-amber-400',
    format: (value) => (value / 10000).toFixed(1)
  },
  {
    key: 'users',
    title: '注册用户',
    icon: User,
    gradient: 'from-violet-500/20 to-purple-500/20',
    borderColor: 'from-violet-500 to-purple-500',
    textColor: 'text-violet-400'
  }
]

// 加载统计数据
const loadStats = async () => {
  try {
    loading.value = true
    const [moviesRes, cinemasRes, boxofficeRes, usersRes] = await Promise.all([
      getMovies({ pageSize: 1 }),
      getCinemas({ pageSize: 1 }),
      getBoxOfficeRecords({ pageSize: 1 }),
      getUsers({ pageSize: 1 })
    ])

    // 计算累计票房
    let totalBoxOffice = 0
    if (boxofficeRes.total > 0) {
      const allRecords = await getBoxOfficeRecords({ pageSize: 1000 })
      totalBoxOffice = allRecords.data?.reduce((sum, record) => sum + (record.box_office || 0), 0) || 0
    }

    stats.value = {
      movies: moviesRes.total || 0,
      cinemas: cinemasRes.total || 0,
      totalBoxOffice,
      users: usersRes.total || 0
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

// 加载最近票房记录
const loadRecentRecords = async () => {
  try {
    const res = await getBoxOfficeRecords({ pageSize: 5, ordering: '-date' })
    recentRecords.value = res.data || []
  } catch (error) {
    console.error('加载最近记录失败:', error)
  }
}

// 更新时间
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

// 快捷操作处理
const handleQuickAction = (route) => {
  router.push(route)
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 格式化金额
const formatMoney = (amount) => {
  if (!amount && amount !== 0) return '-'
  return (amount / 10000).toFixed(2) + '万'
}

// 统计数字动画
const animateNumber = (target, duration = 1500) => {
  return { target, duration }
}

onMounted(() => {
  loadStats()
  loadRecentRecords()
  updateTime()
  setInterval(updateTime, 1000)
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
    <!-- 动画背景网格 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <div class="relative z-10 p-6 lg:p-8">
      <!-- 欢迎头部 -->
      <div class="mb-8 animate-fade-in">
        <div class="glass-card rounded-2xl p-6 border border-white/10">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
                <span class="text-2xl font-bold text-white">
                  {{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'A' }}
                </span>
              </div>
              <div>
                <h1 class="text-2xl font-bold text-white">
                  {{ currentGreeting }}，{{ userStore.user?.real_name || userStore.user?.username || '管理员' }}
                </h1>
                <p class="text-slate-400 mt-1">欢迎回到电影票房预测管理系统</p>
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

      <!-- 统计卡片区域 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div
          v-for="(card, index) in statCards"
          :key="card.key"
          class="stat-card animate-slide-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="glass-card rounded-2xl p-6 border border-white/10 h-full relative overflow-hidden group">
            <!-- 背景渐变 -->
            <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                 :class="card.gradient"></div>

            <!-- 边框发光 -->
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
                  <CountUp :end-value="card.format ? card.format(stats[card.key]) : stats[card.key]" />
                </span>
              </div>
              <div class="text-sm text-slate-400">{{ card.title }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作区域 -->
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
              <!-- 背景渐变 -->
              <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-all duration-300"
                   :class="action.gradient"></div>

              <!-- 光晕效果 -->
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

      <!-- 最近票房记录表格 -->
      <div class="animate-slide-up" style="animation-delay: 0.9s">
        <h2 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          最近票房记录
        </h2>
        <div class="glass-card rounded-2xl border border-white/10 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/10">
                  <th class="text-left py-4 px-6 text-sm font-semibold text-slate-400">日期</th>
                  <th class="text-left py-4 px-6 text-sm font-semibold text-slate-400">影片名称</th>
                  <th class="text-left py-4 px-6 text-sm font-semibold text-slate-400">影院</th>
                  <th class="text-right py-4 px-6 text-sm font-semibold text-slate-400">当日票房</th>
                  <th class="text-center py-4 px-6 text-sm font-semibold text-slate-400">场次</th>
                  <th class="text-center py-4 px-6 text-sm font-semibold text-slate-400">人次</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="recentRecords.length === 0">
                  <td colspan="6" class="py-12 text-center text-slate-500">
                    <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
                    </svg>
                    <p>暂无票房记录</p>
                  </td>
                </tr>
                <tr
                  v-for="(record, index) in recentRecords"
                  :key="record.id"
                  class="border-b border-white/5 hover:bg-white/5 transition-colors"
                  :class="{ 'animate-fade-in': true }"
                  :style="{ animationDelay: `${1 + index * 0.05}s` }"
                >
                  <td class="py-4 px-6 text-white text-sm">{{ formatDate(record.date) }}</td>
                  <td class="py-4 px-6 text-white text-sm font-medium">{{ record.movie?.title || record.movie_title || '-' }}</td>
                  <td class="py-4 px-6 text-slate-300 text-sm">{{ record.cinema?.name || record.cinema_name || '-' }}</td>
                  <td class="py-4 px-6 text-emerald-400 text-sm text-right font-semibold">
                    {{ formatMoney(record.box_office) }}
                  </td>
                  <td class="py-4 px-6 text-slate-300 text-sm text-center">{{ record.show_times || 0 }}</td>
                  <td class="py-4 px-6 text-slate-300 text-sm text-center">{{ record.viewer_count || 0 }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 玻璃态卡片 */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* 网格背景 */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* 渐变光球 */
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
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -20px) scale(1.05);
  }
  50% {
    transform: translate(-10px, 20px) scale(0.95);
  }
  75% {
    transform: translate(-20px, -10px) scale(1.02);
  }
}

/* 淡入动画 */
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

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

/* 滑入动画 */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* 统计卡片悬停效果 */
.stat-card .glass-card {
  transition: all 0.3s ease;
}

.stat-card:hover .glass-card {
  transform: translateY(-4px);
  box-shadow:
    0 20px 40px -10px rgba(0, 0, 0, 0.5),
    0 0 20px rgba(59, 130, 246, 0.1);
}

/* 快捷操作卡片悬停效果 */
.action-card .glass-card {
  transition: all 0.3s ease;
}

.action-card:hover .glass-card {
  transform: scale(1.02);
  border-color: rgba(255, 255, 255, 0.2);
}

/* 数字计数动画组件 */
 CountUp {
  display: inline-block;
}
</style>

<!-- CountUp 组件 -->
<script>
export default {
  name: 'CountUp',
  props: {
    endValue: {
      type: [Number, String],
      required: true
    },
    duration: {
      type: Number,
      default: 1500
    }
  },
  setup(props) {
    const displayValue = ref(0)
    const numValue = computed(() => {
      if (typeof props.endValue === 'string') {
        return parseFloat(props.endValue) || 0
      }
      return props.endValue
    })

    let animationFrame
    let startTime

    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp
      const progress = timestamp - startTime
      const percentage = Math.min(progress / props.duration, 1)

      // 使用缓动函数
      const easeOut = 1 - Math.pow(1 - percentage, 3)
      displayValue.value = numValue.value * easeOut

      if (percentage < 1) {
        animationFrame = requestAnimationFrame(animate)
      } else {
        displayValue.value = numValue.value
      }
    }

    watch(() => props.endValue, (newVal) => {
      if (animationFrame) cancelAnimationFrame(animationFrame)
      startTime = null
      animationFrame = requestAnimationFrame(animate)
    }, { immediate: true })

    onUnmounted(() => {
      if (animationFrame) cancelAnimationFrame(animationFrame)
    })

    return { displayValue }
  },
  template: `
    <span>{{ displayValue.toFixed(typeof endValue === 'string' && endValue.includes('.') ? 1 : 0) }}</span>
  `
}
</script>
