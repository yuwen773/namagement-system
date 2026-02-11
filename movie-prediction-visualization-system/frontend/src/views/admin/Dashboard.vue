<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getDashboardData } from '@/api/visualization'
import { getMovies } from '@/api/movie'
import { getCinemas } from '@/api/cinema'
import { getBoxOfficeRecords } from '@/api/boxoffice'
import { getUsers } from '@/api/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

const loading = ref(false)
const stats = ref({
  movies: 0,
  cinemas: 0,
  boxoffice: 0,
  users: 0
})
const recentRecords = ref([])
const recentLoading = ref(false)

// 快捷入口
const quickActions = [
  { title: '添加影片', icon: 'Plus', action: 'addMovie', type: 'primary' },
  { title: '录入票房', icon: 'Money', action: 'addBoxOffice', type: 'success' },
  { title: '添加影院', icon: 'Location', action: 'addCinema', type: 'warning' },
  { title: '用户管理', icon: 'User', action: 'manageUsers', type: 'info' }
]

// 加载统计数据
const loadStats = async () => {
  try {
    // 并行获取各类数据
    const [moviesRes, cinemasRes, boxofficeRes, usersRes] = await Promise.all([
      getMovies({ pageSize: 1 }),
      getCinemas({ pageSize: 1 }),
      getBoxOfficeRecords({ pageSize: 1 }),
      getUsers({ pageSize: 1 })
    ])

    stats.value = {
      movies: moviesRes.total || 0,
      cinemas: cinemasRes.total || 0,
      boxoffice: boxofficeRes.total || 0,
      users: usersRes.total || 0
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  }
}

// 加载最近票房记录
const loadRecentRecords = async () => {
  recentLoading.value = true
  try {
    const res = await getBoxOfficeRecords({ pageSize: 5, ordering: '-date' })
    recentRecords.value = res.data || []
  } catch (error) {
    console.error('加载最近记录失败:', error)
  } finally {
    recentLoading.value = false
  }
}

// 快捷操作处理
const handleQuickAction = (action) => {
  const router = useRouter()
  switch (action) {
    case 'addMovie':
      router.push('/admin/movies')
      break
    case 'addBoxOffice':
      router.push('/admin/boxoffice')
      break
    case 'addCinema':
      router.push('/admin/cinemas')
      break
    case 'manageUsers':
      router.push('/admin/users')
      break
  }
}

// 日期格式化
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadStats()
  loadRecentRecords()
})
</script>

<template>
  <div class="dashboard">
    <h2 class="text-2xl font-bold mb-6">系统概览</h2>

    <!-- 欢迎语 -->
    <el-card class="mb-6">
      <div class="flex items-center">
        <el-avatar :size="64" :src="userStore.user?.avatar">
          {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
        </el-avatar>
        <div class="ml-4">
          <h3 class="text-xl font-bold">欢迎回来，{{ userStore.user?.real_name || userStore.user?.username }}</h3>
          <p class="text-gray-500 mt-1">今天是 {{ new Date().toLocaleDateString('zh-CN') }}</p>
        </div>
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb-6">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon :size="40" class="stat-icon movies"><VideoCamera /></el-icon>
            <div class="ml-4">
              <div class="text-3xl font-bold">{{ stats.movies }}</div>
              <div class="text-gray-500">影片总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon :size="40" class="stat-icon cinemas"><Location /></el-icon>
            <div class="ml-4">
              <div class="text-3xl font-bold">{{ stats.cinemas }}</div>
              <div class="text-gray-500">影院总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon :size="40" class="stat-icon boxoffice"><Money /></el-icon>
            <div class="ml-4">
              <div class="text-3xl font-bold">{{ stats.boxoffice }}</div>
              <div class="text-gray-500">票房记录</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon :size="40" class="stat-icon users"><User /></el-icon>
            <div class="ml-4">
              <div class="text-3xl font-bold">{{ stats.users }}</div>
              <div class="text-gray-500">用户总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷入口 -->
    <el-card class="mb-6">
      <div class="card-header">
        <h3 class="text-lg font-bold">快捷操作</h3>
      </div>
      <div class="flex gap-4 mt-4">
        <el-button
          v-for="action in quickActions"
          :key="action.action"
          :type="action.type"
          size="large"
          @click="handleQuickAction(action.action)"
        >
          <el-icon class="mr-1"><component :is="action.icon" /></el-icon>
          {{ action.title }}
        </el-button>
      </div>
    </el-card>

    <!-- 最近票房记录 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <h3 class="text-lg font-bold">最近票房记录</h3>
        </div>
      </template>
      <el-table :data="recentRecords" v-loading="recentLoading" stripe>
        <el-table-column prop="date" label="日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="movie_title" label="影片名称" min-width="150">
          <template #default="{ row }">
            {{ row.movie?.title || row.movie_title || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="cinema_name" label="影院" min-width="150">
          <template #default="{ row }">
            {{ row.cinema?.name || row.cinema_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="box_office" label="当日票房(万)" width="120">
          <template #default="{ row }">
            {{ row.box_office?.toLocaleString() || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="show_times" label="排片场次" width="100" align="center" />
        <el-table-column prop="viewer_count" label="观影人次" width="100" align="center" />
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  padding: 12px;
  border-radius: 8px;
}

.stat-icon.movies {
  background: rgba(64, 158, 255, 0.1);
  color: #409eff;
}

.stat-icon.cinemas {
  background: rgba(103, 194, 58, 0.1);
  color: #67c23a;
}

.stat-icon.boxoffice {
  background: rgba(230, 162, 60, 0.1);
  color: #e6a23c;
}

.stat-icon.users {
  background: rgba(144, 147, 153, 0.1);
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
