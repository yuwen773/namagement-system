<template>
  <div class="dashboard-container">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-title-group">
            <div class="header-indicator"></div>
            <h1 class="header-title">系统监控台</h1>
            <span class="header-subtitle">SYSTEM MONITOR</span>
          </div>
        </div>
        <div class="header-right">
          <div class="status-badge" :class="{ active: isSystemOnline }">
            <span class="status-dot"></span>
            <span class="status-text">{{ isSystemOnline ? '运行中' : '离线' }}</span>
          </div>
          <button class="refresh-btn" @click="fetchDashboardData" :disabled="loading">
            <svg class="refresh-icon" :class="{ spinning: loading }" viewBox="0 0 20 20" fill="none">
              <path d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content Grid -->
    <main class="dashboard-main" v-if="!loading && dashboardData">
      <!-- System Status Row -->
      <section class="status-row">
        <!-- Uptime Card -->
        <div class="status-card uptime-card">
          <div class="card-header">
            <div class="card-icon uptime-icon">
              <svg viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/>
                <path d="M10 4v6l4 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="card-label">系统运行时间</span>
          </div>
          <div class="card-content">
            <div class="uptime-display">
              <span class="uptime-value">{{ formattedUptime }}</span>
              <span class="uptime-unit">小时</span>
            </div>
            <div class="uptime-detail">
              启动于: {{ formatDateTime(dashboardData.system?.service_start_time) }}
            </div>
          </div>
          <div class="card-chart">
            <div class="uptime-bar">
              <div class="uptime-progress" :style="{ width: '100%' }"></div>
            </div>
          </div>
        </div>

        <!-- Last Import Card -->
        <div class="status-card import-card">
          <div class="card-header">
            <div class="card-icon import-icon">
              <svg viewBox="0 0 20 20" fill="none">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="card-label">最近数据导入</span>
          </div>
          <div class="card-content">
            <div class="import-time">{{ formatDateTime(dashboardData.system?.latest_import_time) || '暂无导入' }}</div>
            <div class="import-status" v-if="dashboardData.latest_import_task">
              <span class="import-file">{{ dashboardData.latest_import_task.file_name }}</span>
              <span class="import-result" :class="getStatusClass(dashboardData.latest_import_task.status)">
                {{ getStatusText(dashboardData.latest_import_task.status) }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Statistics Grid -->
      <section class="stats-grid">
        <!-- Total Data Card -->
        <div class="stat-card data-card">
          <div class="stat-header">
            <span class="stat-label">数据总量</span>
            <div class="stat-trend up">
              <svg viewBox="0 0 12 12" fill="none">
                <path d="M2 8l4-4 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ formatNumber(dashboardData.data_summary?.total_data_count) }}</div>
          <div class="stat-footer">
            <span class="stat-change">+{{ formatNumber(dashboardData.data_summary?.today_new_count) }}</span>
            <span class="stat-label-text">今日新增</span>
          </div>
          <div class="stat-bg-number">DATA</div>
        </div>

        <!-- Cities Covered Card -->
        <div class="stat-card city-card">
          <div class="stat-header">
            <span class="stat-label">覆盖城市</span>
            <div class="stat-icon">
              <svg viewBox="0 0 20 20" fill="none">
                <path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V15a2 2 0 01-2 2h-1C9.716 17 2 9.284 2 1V5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ formatNumber(dashboardData.data_summary?.covered_city_count) }}</div>
          <div class="stat-footer">
            <span class="stat-label-text">监测站点</span>
            <span class="stat-detail">全国范围</span>
          </div>
          <div class="stat-bg-number">CITY</div>
        </div>

        <!-- Total Users Card -->
        <div class="stat-card user-card">
          <div class="stat-header">
            <span class="stat-label">注册用户</span>
            <div class="stat-icon">
              <svg viewBox="0 0 20 20" fill="none">
                <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </div>
          </div>
          <div class="stat-value">{{ formatNumber(dashboardData.user_summary?.total_user_count) }}</div>
          <div class="stat-footer">
            <span class="stat-change active-count">{{ formatNumber(dashboardData.user_summary?.today_active_user_count) }}</span>
            <span class="stat-label-text">今日活跃</span>
          </div>
          <div class="stat-bg-number">USER</div>
        </div>

        <!-- Active Users Card -->
        <div class="stat-card active-card">
          <div class="stat-header">
            <span class="stat-label">活跃率</span>
            <div class="stat-badge">
              {{ activeRate }}%
            </div>
          </div>
          <div class="stat-value-large">{{ activeRate }}<span class="percent">%</span></div>
          <div class="stat-footer">
            <div class="active-bar">
              <div class="active-fill" :style="{ width: activeRate + '%' }"></div>
            </div>
            <span class="stat-label-text">日活跃占比</span>
          </div>
          <div class="stat-bg-number">RATE</div>
        </div>
      </section>

      <!-- Latest Import Task Section -->
      <section class="task-section" v-if="dashboardData.latest_import_task">
        <div class="section-header">
          <h3 class="section-title">最新导入任务</h3>
          <div class="section-actions">
            <router-link to="/admin/data-import" class="view-all-btn">
              查看全部
              <svg viewBox="0 0 16 16" fill="none">
                <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </router-link>
          </div>
        </div>

        <div class="task-card" :class="`task-${getTaskStatusClass(dashboardData.latest_import_task.status)}`">
          <div class="task-header">
            <div class="task-info">
              <div class="task-title">{{ dashboardData.latest_import_task.file_name }}</div>
              <div class="task-id">ID: {{ dashboardData.latest_import_task.task_id }}</div>
            </div>
            <div class="task-status-badge" :class="`status-${getTaskStatusClass(dashboardData.latest_import_task.status)}`">
              {{ getStatusText(dashboardData.latest_import_task.status) }}
            </div>
          </div>

          <div class="task-stats">
            <div class="task-stat">
              <span class="task-stat-label">总条数</span>
              <span class="task-stat-value">{{ dashboardData.latest_import_task.total_count }}</span>
            </div>
            <div class="task-stat">
              <span class="task-stat-label">成功</span>
              <span class="task-stat-value success">{{ dashboardData.latest_import_task.success_count }}</span>
            </div>
            <div class="task-stat" v-if="dashboardData.latest_import_task.failed_count > 0">
              <span class="task-stat-label">失败</span>
              <span class="task-stat-value error">{{ dashboardData.latest_import_task.failed_count }}</span>
            </div>
          </div>

          <div class="task-progress" v-if="dashboardData.latest_import_task.status === 'RUNNING' || dashboardData.latest_import_task.status === 'PENDING'">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculateProgress(dashboardData.latest_import_task) + '%' }"></div>
            </div>
            <span class="progress-text">{{ calculateProgress(dashboardData.latest_import_task) }}%</span>
          </div>
        </div>
      </section>

      <!-- Quick Actions Grid -->
      <section class="actions-grid">
        <router-link to="/admin/data-import" class="action-card import-action">
          <div class="action-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="action-content">
            <h4 class="action-title">数据导入</h4>
            <p class="action-desc">上传新的监测数据文件</p>
          </div>
          <div class="action-arrow">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </router-link>

        <router-link to="/admin/rules" class="action-card rules-action">
          <div class="action-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="action-content">
            <h4 class="action-title">防护规则</h4>
            <p class="action-desc">配置防护指南规则</p>
          </div>
          <div class="action-arrow">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </router-link>

        <router-link to="/admin/users" class="action-card users-action">
          <div class="action-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="action-content">
            <h4 class="action-title">用户管理</h4>
            <p class="action-desc">管理系统用户权限</p>
          </div>
          <div class="action-arrow">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </router-link>

        <router-link to="/admin/articles" class="action-card articles-action">
          <div class="action-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="action-content">
            <h4 class="action-title">文章管理</h4>
            <p class="action-desc">发布科普文章与公告</p>
          </div>
          <div class="action-arrow">
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </router-link>
      </section>
    </main>

    <!-- Loading State -->
    <main class="dashboard-main loading" v-else-if="loading">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载数据中...</p>
      </div>
    </main>

    <!-- Error State -->
    <main class="dashboard-main error" v-else>
      <div class="error-container">
        <div class="error-icon">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3 class="error-title">加载失败</h3>
        <p class="error-desc">无法获取仪表盘数据，请稍后重试</p>
        <button class="retry-btn" @click="fetchDashboardData">
          <svg viewBox="0 0 16 16" fill="none">
            <path d="M8 2v6l4 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          重试
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getDashboardData } from '@/api/admin'
import { ElMessage } from 'element-plus'

// State
const loading = ref(true)
const dashboardData = ref(null)
const isSystemOnline = ref(true)
const uptimeInterval = ref(null)

// Computed
const formattedUptime = computed(() => {
  if (!dashboardData.value?.system?.uptime_seconds) return '0'
  const hours = Math.floor(dashboardData.value.system.uptime_seconds / 3600)
  return hours.toLocaleString()
})

const activeRate = computed(() => {
  const total = dashboardData.value?.user_summary?.total_user_count || 0
  const active = dashboardData.value?.user_summary?.today_active_user_count || 0
  if (total === 0) return 0
  return Math.round((active / total) * 100)
})

// Methods
const fetchDashboardData = async () => {
  loading.value = true
  try {
    const response = await getDashboardData()
    if (response.code === 0) {
      dashboardData.value = response.data
      isSystemOnline.value = true
    } else {
      throw new Error(response.message)
    }
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    ElMessage.error('加载仪表盘数据失败')
    isSystemOnline.value = false
  } finally {
    loading.value = false
  }
}

const formatNumber = (num) => {
  if (!num) return '0'
  return num.toLocaleString()
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date

  // Less than 1 minute
  if (diff < 60000) {
    return '刚刚'
  }
  // Less than 1 hour
  if (diff < 3600000) {
    return `${Math.floor(diff / 60000)} 分钟前`
  }
  // Less than 1 day
  if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)} 小时前`
  }
  // Format date
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusClass = (status) => {
  const statusMap = {
    'SUCCESS': 'success',
    'FAILED': 'error',
    'RUNNING': 'running',
    'PENDING': 'pending'
  }
  return statusMap[status] || 'pending'
}

const getTaskStatusClass = (status) => {
  const statusMap = {
    'SUCCESS': 'success',
    'FAILED': 'failed',
    'RUNNING': 'running',
    'PENDING': 'pending'
  }
  return statusMap[status] || 'pending'
}

const getStatusText = (status) => {
  const statusMap = {
    'SUCCESS': '成功',
    'FAILED': '失败',
    'RUNNING': '执行中',
    'PENDING': '等待中'
  }
  return statusMap[status] || '未知'
}

const calculateProgress = (task) => {
  if (task.status === 'SUCCESS') return 100
  if (task.total_count === 0) return 0
  return Math.round((task.success_count + task.failed_count) / task.total_count * 100)
}

// Lifecycle
onMounted(() => {
  fetchDashboardData()
  // Refresh data every 30 seconds
  uptimeInterval.value = setInterval(fetchDashboardData, 30000)
})

onUnmounted(() => {
  if (uptimeInterval.value) {
    clearInterval(uptimeInterval.value)
  }
})
</script>

<style scoped>
/* Base Container */
.dashboard-container {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Header */
.dashboard-header {
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-indicator {
  width: 4px;
  height: 32px;
  background: linear-gradient(180deg, #22d3ee 0%, #0891b2 100%);
  border-radius: 2px;
}

.header-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}

.status-badge.active {
  border-color: rgba(34, 211, 238, 0.3);
  background: rgba(34, 211, 238, 0.05);
}

.status-badge.active .status-text {
  color: #22d3ee;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: all 0.3s ease;
}

.status-badge.active .status-dot {
  background: #22d3ee;
  box-shadow: 0 0 8px rgba(34, 211, 238, 0.6);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.refresh-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.refresh-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.5s ease;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Status Row */
.status-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.status-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.3s ease;
}

.status-card:hover {
  border-color: var(--border-hover);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-soft);
  border-radius: 8px;
  color: var(--text-secondary);
}

.uptime-icon {
  background: rgba(34, 211, 238, 0.1);
  color: #22d3ee;
}

.import-icon {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.card-icon svg {
  width: 18px;
  height: 18px;
}

.card-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.uptime-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.uptime-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--text);
  font-feature-settings: 'tnum';
}

.uptime-unit {
  font-size: 14px;
  color: var(--text-secondary);
}

.uptime-detail {
  font-size: 12px;
  color: var(--text-muted);
}

.uptime-bar {
  height: 4px;
  background: var(--bg-soft);
  border-radius: 2px;
  overflow: hidden;
}

.uptime-progress {
  height: 100%;
  background: linear-gradient(90deg, #22d3ee 0%, #0891b2 100%);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.import-time {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.import-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.import-file {
  font-size: 13px;
  color: var(--text-secondary);
  max-width: 70%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.import-result {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.import-result.success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.import-result.error {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.import-result.running {
  background: rgba(34, 211, 238, 0.15);
  color: #22d3ee;
}

.import-result.pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: var(--border-hover);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.stat-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-trend {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 197, 94, 0.15);
  border-radius: 6px;
  color: #22c55e;
}

.stat-trend.up svg {
  width: 12px;
  height: 12px;
}

.stat-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-soft);
  border-radius: 6px;
  color: var(--text-secondary);
}

.stat-icon svg {
  width: 13px;
  height: 13px;
}

.stat-badge {
  padding: 4px 10px;
  background: rgba(34, 211, 238, 0.15);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #22d3ee;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text);
  font-feature-settings: 'tnum';
  letter-spacing: -0.02em;
}

.stat-value-large {
  font-size: 42px;
  font-weight: 700;
  color: var(--text);
  font-feature-settings: 'tnum';
  letter-spacing: -0.02em;
}

.percent {
  font-size: 20px;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-footer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-change {
  font-size: 14px;
  font-weight: 600;
  color: #22c55e;
}

.stat-change.active-count {
  color: #22d3ee;
}

.stat-label-text {
  font-size: 12px;
  color: var(--text-muted);
}

.stat-detail {
  margin-left: auto;
  font-size: 12px;
  color: var(--text-muted);
}

.active-bar {
  flex: 1;
  height: 4px;
  background: var(--bg-soft);
  border-radius: 2px;
  overflow: hidden;
}

.active-fill {
  height: 100%;
  background: linear-gradient(90deg, #22d3ee 0%, #0891b2 100%);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.stat-bg-number {
  position: absolute;
  right: -8px;
  bottom: -12px;
  font-size: 64px;
  font-weight: 900;
  color: var(--text-muted);
  opacity: 0.03;
  letter-spacing: -0.02em;
  pointer-events: none;
}

/* Task Section */
.task-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.section-actions {
  display: flex;
  gap: 8px;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 13px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.view-all-btn svg {
  width: 14px;
  height: 14px;
}

.task-card {
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
}

.task-card.task-success {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.03);
}

.task-card.task-failed {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.03);
}

.task-card.task-running {
  border-color: rgba(34, 211, 238, 0.3);
  background: rgba(34, 211, 238, 0.03);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.task-info {
  flex: 1;
}

.task-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 4px;
}

.task-id {
  font-size: 12px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.task-status-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.task-status-badge.status-success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.task-status-badge.status-failed {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.task-status-badge.status-running {
  background: rgba(34, 211, 238, 0.15);
  color: #22d3ee;
}

.task-status-badge.status-pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.task-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.task-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.task-stat-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.task-stat-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  font-feature-settings: 'tnum';
}

.task-stat-value.success {
  color: #22c55e;
}

.task-stat-value.error {
  color: #ef4444;
}

.task-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: var(--bg-card);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #22d3ee 0%, #0891b2 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 40px;
  text-align: right;
}

/* Actions Grid */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-card:hover {
  border-color: var(--border-hover);
  background: var(--bg-hover);
  transform: translateX(4px);
}

.action-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-soft);
  border-radius: 10px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.action-icon svg {
  width: 20px;
  height: 20px;
}

.import-action .action-icon {
  background: rgba(34, 211, 238, 0.1);
  color: #22d3ee;
}

.rules-action .action-icon {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.users-action .action-icon {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.articles-action .action-icon {
  background: rgba(251, 191, 36, 0.1);
  color: #fbbf24;
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 2px;
}

.action-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.action-arrow {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-soft);
  border-radius: 8px;
  color: var(--text-muted);
  flex-shrink: 0;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
}

.action-card:hover .action-arrow {
  opacity: 1;
  transform: translateX(0);
}

.action-arrow svg {
  width: 14px;
  height: 14px;
}

/* Loading State */
.dashboard-main.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Error State */
.dashboard-main.error {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.error-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 16px;
  color: #ef4444;
}

.error-icon svg {
  width: 28px;
  height: 28px;
}

.error-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
}

.error-desc {
  font-size: 14px;
  color: var(--text-muted);
  max-width: 300px;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.retry-btn svg {
  width: 14px;
  height: 14px;
}

/* Responsive */
@media (max-width: 1280px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .status-row {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
