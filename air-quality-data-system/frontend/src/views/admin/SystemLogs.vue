<template>
  <div class="logs-manage-container">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-indicator"></div>
          <div class="header-title-group">
            <h1 class="header-title">系统日志</h1>
            <span class="header-subtitle">SYSTEM LOGS</span>
          </div>
        </div>
        <div class="header-actions">
          <button @click="exportLogs" class="secondary-btn">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>导出日志</span>
          </button>
          <button @click="refreshLogs" class="refresh-btn" :class="{ spinning: refreshing }">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Filters -->
    <section class="filters-section">
      <div class="filter-row">
        <div class="filter-group">
          <label class="filter-label">级别</label>
          <select v-model="levelFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部级别</option>
            <option value="DEBUG">调试</option>
            <option value="INFO">信息</option>
            <option value="WARNING">警告</option>
            <option value="ERROR">错误</option>
            <option value="CRITICAL">严重</option>
          </select>
        </div>
        <div class="filter-group">
          <label class="filter-label">模块</label>
          <select v-model="moduleFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部模块</option>
            <option value="accounts">账户</option>
            <option value="airquality">空气质量</option>
            <option value="articles">文章</option>
            <option value="system">系统</option>
            <option value="auth">认证</option>
          </select>
        </div>
        <div class="filter-group">
          <label class="filter-label">时间范围</label>
          <select v-model="timeFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部时间</option>
            <option value="1h">最近1小时</option>
            <option value="24h">最近24小时</option>
            <option value="7d">最近7天</option>
            <option value="30d">最近30天</option>
          </select>
        </div>
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 20 20" fill="none">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索日志内容..."
            class="search-input"
            @input="handleSearch"
          />
        </div>
      </div>
    </section>

    <!-- Stats Bar -->
    <section class="stats-section">
      <div class="stat-item" :class="{ active: levelFilter === '' }" @click="levelFilter = ''; handleFilterChange()">
        <span class="stat-value">{{ logsList.length }}</span>
        <span class="stat-label">全部</span>
      </div>
      <div class="stat-item error" :class="{ active: levelFilter === 'ERROR' }" @click="levelFilter = 'ERROR'; handleFilterChange()">
        <span class="stat-value">{{ errorCount }}</span>
        <span class="stat-label">错误</span>
      </div>
      <div class="stat-item warning" :class="{ active: levelFilter === 'WARNING' }" @click="levelFilter = 'WARNING'; handleFilterChange()">
        <span class="stat-value">{{ warningCount }}</span>
        <span class="stat-label">警告</span>
      </div>
      <div class="stat-item info" :class="{ active: levelFilter === 'INFO' }" @click="levelFilter = 'INFO'; handleFilterChange()">
        <span class="stat-value">{{ infoCount }}</span>
        <span class="stat-label">信息</span>
      </div>
      <div class="stat-item debug" :class="{ active: levelFilter === 'DEBUG' }" @click="levelFilter = 'DEBUG'; handleFilterChange()">
        <span class="stat-value">{{ debugCount }}</span>
        <span class="stat-label">调试</span>
      </div>
    </section>

    <!-- Logs Table -->
    <section class="logs-section">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载日志数据...</p>
      </div>
      <div v-else-if="filteredLogs.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 20 20" fill="none">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p class="empty-text">暂无日志数据</p>
      </div>
      <div v-else class="logs-table-wrapper">
        <table class="logs-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>级别</th>
              <th>模块</th>
              <th>消息</th>
              <th>用户</th>
              <th>IP</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in paginatedLogs" :key="log.id" :class="`level-${log.level.toLowerCase()}`">
              <td class="timestamp-cell">
                <span class="timestamp-text">{{ formatTimestamp(log.timestamp) }}</span>
              </td>
              <td class="level-cell">
                <span class="level-badge" :class="log.level.toLowerCase()">
                  {{ log.level }}
                </span>
              </td>
              <td class="module-cell">
                <span class="module-text">{{ log.module }}</span>
              </td>
              <td class="message-cell">
                <span class="message-text" :title="log.message" @click="openDetailModal(log)">{{ truncateMessage(log.message) }}</span>
              </td>
              <td class="user-cell">
                <span class="user-text">{{ log.username || '-' }}</span>
              </td>
              <td class="ip-cell">
                <span class="ip-text">{{ log.ip_address || '-' }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Pagination -->
    <section v-if="filteredLogs.length > pageSize" class="pagination-section">
      <div class="pagination-info">
        <span class="pagination-text">显示 {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, filteredLogs.length) }} 条，共 {{ filteredLogs.length }} 条</span>
      </div>
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1" class="page-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="{ active: page === currentPage }"
            class="page-number"
          >
            {{ page }}
          </button>
        </div>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="page-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </section>

    <!-- Log Detail Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="detailModalVisible" class="modal-overlay" @click="closeDetailModal">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">日志详情</h2>
              <button @click="closeDetailModal" class="modal-close">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <div class="modal-body" v-if="selectedLog">
              <div class="detail-grid">
                <div class="detail-item">
                  <span class="detail-label">时间戳</span>
                  <span class="detail-value">{{ formatFullTimestamp(selectedLog.timestamp) }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">级别</span>
                  <span class="level-badge detail" :class="selectedLog.level.toLowerCase()">
                    {{ selectedLog.level }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">模块</span>
                  <span class="detail-value">{{ selectedLog.module }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">用户</span>
                  <span class="detail-value">{{ selectedLog.username || '-' }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">IP地址</span>
                  <span class="detail-value">{{ selectedLog.ip_address || '-' }}</span>
                </div>
                <div class="detail-item full">
                  <span class="detail-label">消息</span>
                  <pre class="detail-message">{{ selectedLog.message }}</pre>
                </div>
                <div v-if="selectedLog.extra_data" class="detail-item full">
                  <span class="detail-label">额外数据</span>
                  <pre class="detail-extra">{{ JSON.stringify(selectedLog.extra_data, null, 2) }}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSystemLogs } from '@/api/admin'

const loading = ref(false)
const refreshing = ref(false)
const logsList = ref([])
const levelFilter = ref('')
const moduleFilter = ref('')
const timeFilter = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = 50

const detailModalVisible = ref(false)
const selectedLog = ref(null)

const filteredLogs = computed(() => {
  let logs = logsList.value

  if (levelFilter.value) {
    logs = logs.filter(log => log.level === levelFilter.value)
  }

  if (moduleFilter.value) {
    logs = logs.filter(log => log.module === moduleFilter.value)
  }

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    logs = logs.filter(log =>
      log.message.toLowerCase().includes(keyword) ||
      (log.username && log.username.toLowerCase().includes(keyword))
    )
  }

  if (timeFilter.value) {
    const now = new Date()
    let cutoff
    switch (timeFilter.value) {
      case '1h': cutoff = new Date(now - 60 * 60 * 1000); break
      case '24h': cutoff = new Date(now - 24 * 60 * 60 * 1000); break
      case '7d': cutoff = new Date(now - 7 * 24 * 60 * 60 * 1000); break
      case '30d': cutoff = new Date(now - 30 * 24 * 60 * 60 * 1000); break
    }
    if (cutoff) {
      logs = logs.filter(log => new Date(log.timestamp) >= cutoff)
    }
  }

  return logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})

const totalPages = computed(() => Math.ceil(filteredLogs.value.length / pageSize))

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredLogs.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    }
  }
  return pages
})

const errorCount = computed(() => logsList.value.filter(l => l.level === 'ERROR').length)
const warningCount = computed(() => logsList.value.filter(l => l.level === 'WARNING').length)
const infoCount = computed(() => logsList.value.filter(l => l.level === 'INFO').length)
const debugCount = computed(() => logsList.value.filter(l => l.level === 'DEBUG').length)

const fetchLogs = async () => {
  loading.value = true
  try {
    const response = await getSystemLogs({
      level: levelFilter.value || undefined,
      module: moduleFilter.value || undefined,
      search: searchKeyword.value || undefined
    })
    if (response.code === 0) {
      logsList.value = response.data || []
    }
  } catch (error) {
    ElMessage.error('加载日志失败')
  } finally {
    loading.value = false
  }
}

const refreshLogs = async () => {
  refreshing.value = true
  await fetchLogs()
  setTimeout(() => { refreshing.value = false }, 500)
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchLogs()
}

const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const goToPage = (page) => { if (typeof page === 'number') currentPage.value = page }

const openDetailModal = (log) => {
  selectedLog.value = log
  detailModalVisible.value = true
}

const closeDetailModal = () => {
  detailModalVisible.value = false
  selectedLog.value = null
}

const exportLogs = () => {
  const data = filteredLogs.value.map(log => ({
    时间: formatFullTimestamp(log.timestamp),
    级别: log.level,
    模块: log.module,
    用户: log.username || '',
    IP: log.ip_address || '',
    消息: log.message
  }))
  const csv = [
    Object.keys(data[0] || {}).join(','),
    ...data.map(row => Object.values(row).map(v => `"${v}"`).join(','))
  ].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `system-logs-${new Date().toISOString().split('T')[0]}.csv`
  link.click()
  ElMessage.success('日志导出成功')
}

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN')
}

const formatFullTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN')
}

const truncateMessage = (message) => {
  if (!message) return '-'
  return message.length > 80 ? message.substring(0, 80) + '...' : message
}

onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

:root {
  --bg-primary: #0a0e1a;
  --bg-secondary: #0d121d;
  --bg-card: #111827;
  --bg-hover: #1a2332;
  --border-color: #1e293b;
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-cyan: #22d3ee;
  --accent-cyan-dim: rgba(34, 211, 238, 0.1);
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #fbbf24;
  --info: #3b82f6;
  --debug: #8b5cf6;
}

.logs-manage-container {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: 'Noto Sans SC', sans-serif;
}

.page-header {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px 24px;
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

.header-indicator {
  width: 4px;
  height: 32px;
  background: linear-gradient(180deg, var(--accent-cyan) 0%, rgba(34, 211, 238, 0.3) 100%);
  border-radius: 2px;
}

.header-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.header-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.secondary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-btn:hover {
  background: var(--bg-hover);
}

.secondary-btn svg {
  width: 16px;
  height: 16px;
}

.refresh-btn {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.refresh-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.refresh-btn.spinning svg {
  animation: spin 0.8s linear infinite;
}

.refresh-btn svg {
  width: 18px;
  height: 18px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.filters-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px 20px;
}

.filter-row {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select {
  padding: 10px 32px 10px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 13px;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 14px;
  transition: all 0.2s;
  min-width: 140px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.search-box {
  position: relative;
  margin-left: auto;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  padding: 10px 12px 10px 36px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 13px;
  transition: all 0.2s;
  width: 280px;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.stats-section {
  display: flex;
  gap: 12px;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-item.active {
  border-color: var(--accent-cyan);
  background: var(--accent-cyan-dim);
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-item.error .stat-value { color: var(--danger); }
.stat-item.warning .stat-value { color: var(--warning); }
.stat-item.info .stat-value { color: var(--info); }
.stat-item.debug .stat-value { color: var(--debug); }

.stat-item.error.active { border-color: var(--danger); background: rgba(239, 68, 68, 0.1); }
.stat-item.warning.active { border-color: var(--warning); background: rgba(251, 191, 36, 0.1); }
.stat-item.info.active { border-color: var(--info); background: rgba(59, 130, 246, 0.1); }
.stat-item.debug.active { border-color: var(--debug); background: rgba(139, 92, 246, 0.1); }

.logs-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  overflow: hidden;
  min-height: 400px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  margin-top: 20px;
  color: var(--text-muted);
  font-size: 14px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.empty-text {
  color: var(--text-muted);
  font-size: 16px;
}

.logs-table-wrapper {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table thead {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.logs-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logs-table tbody tr {
  border-bottom: 1px solid var(--border-color);
  transition: background 0.15s;
}

.logs-table tbody tr:hover {
  background: var(--bg-hover);
}

.logs-table td {
  padding: 12px 16px;
  color: var(--text-primary);
  font-size: 13px;
}

.logs-table tbody tr.level-error {
  background: rgba(239, 68, 68, 0.05);
}

.logs-table tbody tr.level-critical {
  background: rgba(239, 68, 68, 0.08);
}

.timestamp-cell {
  width: 100px;
}

.timestamp-text {
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-muted);
  font-size: 12px;
}

.level-cell {
  width: 80px;
}

.level-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.level-badge.debug {
  background: rgba(139, 92, 246, 0.1);
  color: var(--debug);
}

.level-badge.info {
  background: rgba(59, 130, 246, 0.1);
  color: var(--info);
}

.level-badge.warning {
  background: rgba(251, 191, 36, 0.1);
  color: var(--warning);
}

.level-badge.error,
.level-badge.critical {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.module-cell {
  width: 100px;
}

.module-text {
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-secondary);
  font-size: 12px;
}

.message-cell {
  min-width: 300px;
  max-width: 500px;
}

.message-text {
  color: var(--text-secondary);
  line-height: 1.5;
  cursor: pointer;
}

.message-text:hover {
  color: var(--text-primary);
}

.user-cell,
.ip-cell {
  width: 100px;
}

.user-text,
.ip-text {
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-muted);
  font-size: 12px;
}

.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.pagination-info {
  color: var(--text-secondary);
  font-size: 13px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.page-btn:hover:not(:disabled) {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-number {
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.page-number:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.page-number.active {
  background: var(--accent-cyan);
  color: var(--bg-primary);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 14, 26, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 100%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s;
}

.modal-close:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.modal-close svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  padding: 24px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item.full {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 14px;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;
}

.level-badge.detail {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  align-self: flex-start;
}

.detail-message,
.detail-extra {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--text-primary);
  line-height: 1.6;
  overflow-x: auto;
  max-height: 300px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

/* Scrollbar */
.logs-table-wrapper::-webkit-scrollbar,
.modal-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.logs-table-wrapper::-webkit-scrollbar-track,
.modal-container::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.logs-table-wrapper::-webkit-scrollbar-thumb,
.modal-container::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.logs-table-wrapper::-webkit-scrollbar-thumb:hover,
.modal-container::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}

/* Responsive */
@media (max-width: 1024px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group,
  .filter-select {
    width: 100%;
  }

  .search-box {
    margin-left: 0;
  }

  .search-input {
    width: 100%;
  }

  .stats-section {
    flex-wrap: wrap;
  }

  .stat-item {
    min-width: calc(50% - 6px);
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }

  .secondary-btn,
  .refresh-btn {
    flex: 1;
  }

  .pagination-section {
    flex-direction: column;
    gap: 16px;
  }

  .stat-item {
    min-width: calc(33.333% - 8px);
  }
}
</style>
