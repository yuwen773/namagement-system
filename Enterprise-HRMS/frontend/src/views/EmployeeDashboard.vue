<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'
import { getTodayAttendance, checkIn, checkOut } from '../api/attendance'
import { getLatestNotices } from '../api/notice'

const authStore = useAuthStore()

// 用户信息
const userDisplayName = computed(() => {
  return authStore.user?.real_name || authStore.user?.username || '用户'
})

// 今日考勤状态
const todayAttendance = ref(null)
const attendanceLoading = ref(false)

// 最新公告
const notices = ref([])
const noticesLoading = ref(false)

// 本月考勤统计
const monthlyStats = ref({
  normalDays: 0,
  lateDays: 0,
  earlyDays: 0,
  leaveDays: 0,
  absentDays: 0
})

// 快捷操作加载状态
const quickActionLoading = ref(false)

// 获取今日考勤状态
const fetchTodayAttendance = async () => {
  attendanceLoading.value = true
  try {
    const res = await getTodayAttendance()
    if (res.code === 0) {
      todayAttendance.value = res.data
    }
  } catch (error) {
    console.error('获取今日考勤失败:', error)
  } finally {
    attendanceLoading.value = false
  }
}

// 获取最新公告
const fetchNotices = async () => {
  noticesLoading.value = true
  try {
    const res = await getLatestNotices(5)
    if (res.code === 0) {
      notices.value = res.data
    }
  } catch (error) {
    console.error('获取公告失败:', error)
  } finally {
    noticesLoading.value = false
  }
}

// 签到
const handleClockIn = async () => {
  quickActionLoading.value = true
  try {
    const res = await checkIn()
    if (res.code === 0) {
      ElMessage.success('签到成功')
      fetchTodayAttendance()
    } else {
      ElMessage.error(res.message || '签到失败')
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '签到失败')
  } finally {
    quickActionLoading.value = false
  }
}

// 签退
const handleClockOut = async () => {
  quickActionLoading.value = true
  try {
    const res = await checkOut()
    if (res.code === 0) {
      ElMessage.success('签退成功')
      fetchTodayAttendance()
    } else {
      ElMessage.error(res.message || '签退失败')
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '签退失败')
  } finally {
    quickActionLoading.value = false
  }
}

// 考勤状态文本
const attendanceStatusText = computed(() => {
  if (!todayAttendance.value) return '未知'
  const statusMap = {
    normal: '正常',
    late: '迟到',
    early: '早退',
    leave: '休假',
    absent: '缺勤'
  }
  return statusMap[todayAttendance.value.status] || '未知'
})

// 考勤状态类型
const attendanceStatusType = computed(() => {
  if (!todayAttendance.value) return 'info'
  const typeMap = {
    normal: 'success',
    late: 'warning',
    early: 'warning',
    leave: 'info',
    absent: 'danger'
  }
  return typeMap[todayAttendance.value.status] || 'info'
})

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

onMounted(async () => {
  // 获取权限配置
  if (authStore.token && !authStore.rolePermissions) {
    await authStore.fetchRolePermissions()
  }
  fetchTodayAttendance()
  fetchNotices()
})
</script>

<template>
  <div class="employee-dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">你好，{{ userDisplayName }}</h1>
        <p class="welcome-subtitle">{{ formatDate(new Date()) }} · 祝你工作顺利</p>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <h3 class="section-title">快捷操作</h3>
      <div class="action-cards">
        <el-card class="action-card" shadow="hover">
          <div class="action-content">
            <div class="action-icon clock-in">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div class="action-info">
              <span class="action-label">签到</span>
              <span class="action-desc">每日09:00前</span>
            </div>
            <el-button
              type="primary"
              :loading="quickActionLoading"
              :disabled="todayAttendance?.check_in_time"
              @click="handleClockIn"
            >
              {{ todayAttendance?.check_in_time ? '已签到' : '立即签到' }}
            </el-button>
          </div>
        </el-card>

        <el-card class="action-card" shadow="hover">
          <div class="action-content">
            <div class="action-icon clock-out">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div class="action-info">
              <span class="action-label">签退</span>
              <span class="action-desc">每日18:00后</span>
            </div>
            <el-button
              type="success"
              :loading="quickActionLoading"
              :disabled="!todayAttendance?.check_in_time || todayAttendance?.check_out_time"
              @click="handleClockOut"
            >
              {{ todayAttendance?.check_out_time ? '已签退' : '立即签退' }}
            </el-button>
          </div>
        </el-card>

        <el-card class="action-card" shadow="hover" @click="$router.push('/approval')">
          <div class="action-content clickable">
            <div class="action-icon leave">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </div>
            <div class="action-info">
              <span class="action-label">请假申请</span>
              <span class="action-desc">提交请假请求</span>
            </div>
            <el-button text type="primary">去申请</el-button>
          </div>
        </el-card>

        <el-card class="action-card" shadow="hover" @click="$router.push('/approval')">
          <div class="action-content clickable">
            <div class="action-icon overtime">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2v4"/>
                <path d="M12 18v4"/>
                <path d="M4.93 4.93l2.83 2.83"/>
                <path d="M16.24 16.24l2.83 2.83"/>
                <path d="M2 12h4"/>
                <path d="M18 12h4"/>
                <path d="M4.93 19.07l2.83-2.83"/>
                <path d="M16.24 7.76l2.83-2.83"/>
              </svg>
            </div>
            <div class="action-info">
              <span class="action-label">加班申请</span>
              <span class="action-desc">记录加班工时</span>
            </div>
            <el-button text type="primary">去申请</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <div class="dashboard-grid">
      <!-- 今日考勤状态 -->
      <div class="grid-item attendance-status">
        <el-card shadow="never" class="status-card">
          <template #header>
            <div class="card-header">
              <span>今日考勤</span>
              <el-tag :type="attendanceStatusType" size="small">{{ attendanceStatusText }}</el-tag>
            </div>
          </template>
          <div v-loading="attendanceLoading" class="status-content">
            <div v-if="todayAttendance" class="attendance-details">
              <div class="detail-item">
                <span class="label">考勤日期</span>
                <span class="value">{{ todayAttendance.date }}</span>
              </div>
              <div class="detail-item">
                <span class="label">签到时间</span>
                <span class="value">{{ todayAttendance.check_in_time || '未签到' }}</span>
              </div>
              <div class="detail-item">
                <span class="label">签退时间</span>
                <span class="value">{{ todayAttendance.check_out_time || '未签退' }}</span>
              </div>
            </div>
            <el-empty v-else description="今日暂无考勤记录" :image-size="60" />
          </div>
        </el-card>
      </div>

      <!-- 最新公告 -->
      <div class="grid-item latest-notices">
        <el-card shadow="never" class="notices-card">
          <template #header>
            <div class="card-header">
              <span>最新公告</span>
              <el-link type="primary" :underline="false" @click="$router.push('/notices')">
                查看全部 →
              </el-link>
            </div>
          </template>
          <div v-loading="noticesLoading" class="notices-content">
            <div v-if="notices.length > 0" class="notice-list">
              <div
                v-for="notice in notices"
                :key="notice.id"
                class="notice-item"
                @click="$router.push(`/notices/${notice.id}`)"
              >
                <div class="notice-header">
                  <el-tag
                    v-if="notice.is_pinned"
                    type="warning"
                    size="small"
                    effect="plain"
                  >
                    置顶
                  </el-tag>
                  <span class="notice-title">{{ notice.title }}</span>
                </div>
                <div class="notice-meta">
                  <span>{{ notice.published_at?.slice(0, 10) || notice.created_at?.slice(0, 10) }}</span>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无公告" :image-size="60" />
          </div>
        </el-card>
      </div>

      <!-- 本月考勤统计 -->
      <div class="grid-item monthly-stats">
        <el-card shadow="never" class="stats-card">
          <template #header>
            <div class="card-header">
              <span>本月考勤概览</span>
            </div>
          </template>
          <div class="stats-content">
            <div class="stats-summary">
              <div class="stat-item normal">
                <span class="stat-value">{{ monthlyStats.normalDays }}</span>
                <span class="stat-label">正常</span>
              </div>
              <div class="stat-item warning">
                <span class="stat-value">{{ monthlyStats.lateDays + monthlyStats.earlyDays }}</span>
                <span class="stat-label">异常</span>
              </div>
              <div class="stat-item info">
                <span class="stat-value">{{ monthlyStats.leaveDays }}</span>
                <span class="stat-label">休假</span>
              </div>
            </div>
            <div class="stats-detail">
              <div class="detail-row">
                <span>迟到次数</span>
                <span class="value warning">{{ monthlyStats.lateDays }} 次</span>
              </div>
              <div class="detail-row">
                <span>早退次数</span>
                <span class="value warning">{{ monthlyStats.earlyDays }} 次</span>
              </div>
              <div class="detail-row">
                <span>请假天数</span>
                <span class="value info">{{ monthlyStats.leaveDays }} 天</span>
              </div>
              <div class="detail-row">
                <span>缺勤天数</span>
                <span class="value danger">{{ monthlyStats.absentDays }} 天</span>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.employee-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

/* 欢迎区域 */
.welcome-section {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 24px;
  color: white;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.welcome-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

/* 快捷操作 */
.quick-actions {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 16px 0;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.action-card {
  border-radius: 12px;
  transition: transform var(--transition-fast);
}

.action-card:hover {
  transform: translateY(-2px);
}

.action-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-content.clickable {
  cursor: pointer;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-icon svg {
  width: 24px;
  height: 24px;
}

.action-icon.clock-in {
  background: rgba(79, 70, 229, 0.1);
  color: #4f46e5;
}

.action-icon.clock-out {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.action-icon.leave {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.action-icon.overtime {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.action-info {
  flex: 1;
}

.action-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.action-desc {
  display: block;
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
}

/* 仪表盘网格 */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 24px;
}

.grid-item {
  min-height: 280px;
}

.attendance-status {
  grid-column: 1;
  grid-row: 1;
}

.latest-notices {
  grid-column: 2;
  grid-row: 1;
}

.monthly-stats {
  grid-column: 1 / span 2;
  grid-row: 2;
}

/* 卡片样式 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 500;
}

.status-card,
.notices-card,
.stats-card {
  height: 100%;
  border-radius: 12px;
}

/* 考勤状态 */
.status-content {
  min-height: 150px;
}

.attendance-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--color-gray-50);
  border-radius: 8px;
}

.detail-item .label {
  color: var(--color-text-secondary);
  font-size: 14px;
}

.detail-item .value {
  font-weight: 500;
  color: var(--color-text-primary);
}

/* 公告列表 */
.notices-content {
  min-height: 180px;
}

.notice-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notice-item {
  padding: 12px 16px;
  background: var(--color-gray-50);
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.notice-item:hover {
  background: var(--color-gray-100);
}

.notice-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.notice-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-meta {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

/* 统计卡片 */
.stats-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-summary {
  display: flex;
  justify-content: space-around;
  padding: 16px 0;
  background: var(--color-gray-50);
  border-radius: 12px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 600;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

.stat-item.normal .stat-value {
  color: #10b981;
}

.stat-item.warning .stat-value {
  color: #f59e0b;
}

.stat-item.info .stat-value {
  color: #6366f1;
}

.stats-detail {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--color-gray-50);
  border-radius: 8px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.detail-row .value {
  font-weight: 500;
}

.detail-row .value.warning {
  color: #f59e0b;
}

.detail-row .value.info {
  color: #6366f1;
}

.detail-row .value.danger {
  color: #ef4444;
}

/* 响应式 */
@media (max-width: 1200px) {
  .action-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .grid-item {
    grid-column: 1;
    grid-row: auto;
  }

  .monthly-stats {
    grid-column: 1;
    grid-row: auto;
  }
}

@media (max-width: 768px) {
  .action-cards {
    grid-template-columns: 1fr;
  }

  .stats-summary {
    flex-wrap: wrap;
    gap: 16px;
  }

  .stat-item {
    flex: 1;
    min-width: 80px;
  }

  .stats-detail {
    grid-template-columns: 1fr;
  }
}
</style>
