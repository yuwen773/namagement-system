<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { crawlerApi, productApi } from '@/api'
import {
  VideoPlay, VideoPause, Refresh, Clock, Check, Close, Warning,
  Document, Loading, Setting, Download
} from '@element-plus/icons-vue'

const router = useRouter()

// 状态管理
const currentTask = ref(null)
const pollTimer = ref(null)
const isLoading = ref(false)
const keywords = ref('')
const pageCount = ref(1)
const lastBatchNo = ref('')  // 保存最后一次采集的批次号

// 日志相关
const logs = ref([])
const autoScroll = ref(true)
const logContainer = ref(null)

// 历史记录
const recentLogs = ref([])
const logsLoading = ref(false)

// 计算属性
const taskStatus = computed(() => {
  if (!currentTask.value) return 'idle'
  const status = currentTask.value.status?.toUpperCase()
  if (status === 'PENDING' || status === 'PROGRESS') return 'running'
  if (status === 'SUCCESS') return 'success'
  if (status === 'FAILURE') return 'failed'
  return 'idle'
})

const progressPercent = computed(() => {
  if (!currentTask.value?.progress) return 0
  const match = currentTask.value.progress.match(/(\d+)%/)
  return match ? parseInt(match[1]) : 0
})

const statusConfig = computed(() => {
  const configs = {
    idle: {
      label: '空闲',
      color: '#A8A29E',
      bg: 'rgba(168, 162, 158, 0.12)',
      border: 'rgba(168, 162, 158, 0.2)',
      icon: Clock
    },
    running: {
      label: '运行中',
      color: '#52B788',
      bg: 'rgba(82, 183, 136, 0.15)',
      border: 'rgba(82, 183, 136, 0.3)',
      icon: Loading
    },
    success: {
      label: '已完成',
      color: '#52B788',
      bg: 'rgba(82, 183, 136, 0.15)',
      border: 'rgba(82, 183, 136, 0.3)',
      icon: Check
    },
    failed: {
      label: '失败',
      color: '#DC2626',
      bg: 'rgba(220, 38, 38, 0.12)',
      border: 'rgba(220, 38, 38, 0.2)',
      icon: Close
    }
  }
  return configs[taskStatus.value] || configs.idle
})

// 方法
const startCrawl = async () => {
  // 验证页数限制
  if (!pageCount.value || pageCount.value < 1) {
    ElMessage.warning('请输入有效的页数')
    return
  }
  if (pageCount.value > 3) {
    ElMessage.warning('采集页数不能超过3页')
    return
  }

  try {
    isLoading.value = true
    const keyword = keywords.value.trim() || '猫粮'

    const res = await crawlerApi.start({
      mode: 'normal',
      keywords: keyword,
      max_pages: pageCount.value
    })

    if (res.code === 0) {
      currentTask.value = res.data
      logs.value = [
        '任务已启动...',
        `关键词: ${keyword}`,
        `页数限制: ${pageCount.value} 页`
      ]
      ElMessage.success('采集任务已启动')
      startPolling(res.data.task_id)
      await loadRecentLogs()
    } else {
      ElMessage.error(res.message || '启动失败')
    }
  } catch (error) {
    ElMessage.error('启动任务失败: ' + (error.response?.data?.message || error.message))
  } finally {
    isLoading.value = false
  }
}

const stopCrawl = async () => {
  if (!currentTask.value?.task_id) return

  try {
    await ElMessageBox.confirm('确定要停止当前采集任务吗？', '确认停止', {
      confirmButtonText: '停止',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await crawlerApi.stop(currentTask.value.task_id)
    ElMessage.info('任务停止请求已发送')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('停止任务失败')
    }
  }
}

const pollTaskStatus = async () => {
  if (!currentTask.value?.task_id) return

  try {
    const res = await crawlerApi.getStatus(currentTask.value.task_id)
    if (res.code === 0) {
      currentTask.value = res.data

      // 更新日志
      if (res.data.logs && res.data.logs.length > 0) {
        const newLogs = res.data.logs.filter(log => !logs.value.includes(log))
        if (newLogs.length > 0) {
          logs.value.push(...newLogs)
          scrollToBottom()
        }
      }

      // 任务完成或失败时停止轮询
      const status = res.data.status?.toUpperCase()
      if (status === 'SUCCESS' || status === 'FAILURE') {
        stopPolling()
        if (status === 'SUCCESS') {
          logs.value.push('=== 采集完成 ===')
          ElMessage.success(`采集完成！共获取 ${res.data.items_collected} 条数据`)

          // 自动导出CSV
          if (res.data.batch_no && res.data.items_collected > 0) {
            lastBatchNo.value = res.data.batch_no
            await exportCrawlData(res.data.batch_no)
          } else {
            // 采集失败但没有数据时，提供导出已有数据的选项
            logs.value.push('提示: 本次采集未获取到数据，可点击"导出已有数据"查看现有数据')
          }
        } else {
          logs.value.push('=== 采集失败 ===')
          ElMessage.error(`采集任务失败: ${res.data.error_message || '请检查Cookie配置'}`)
        }
        await loadRecentLogs()
      }
    }
  } catch (error) {
    console.error('Poll error:', error)
  }
}

// 导出采集数据
const exportCrawlData = async (batchNo) => {
  try {
    logs.value.push('正在导出数据...')
    const response = await productApi.export({ batch_no: batchNo })

    // 创建下载链接
    const blob = new Blob([response], { type: 'text/csv;charset=utf-8-sig' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url

    // 从响应头获取文件名或生成默认文件名
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5)
    link.download = `采集数据_${batchNo}_${timestamp}.csv`

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    logs.value.push(`✓ 数据已导出: 采集数据_${batchNo}.csv`)
    ElMessage.success('CSV文件已自动下载')
  } catch (error) {
    console.error('Export error:', error)
    logs.value.push('✗ 导出失败: ' + (error.message || '未知错误'))
    ElMessage.warning('数据已保存，但自动导出失败')
  }
}

// 手动导出最后一次采集的数据
const manualExport = async () => {
  if (!lastBatchNo.value) {
    // 如果没有批次号，导出最近100条数据作为演示
    ElMessage.info('正在导出最近100条数据...')
    await exportRecentData()
    return
  }
  await exportCrawlData(lastBatchNo.value)
}

// 导出最近的数据（当采集失败时使用）
const exportRecentData = async () => {
  try {
    logs.value.push('正在导出最近数据...')
    // 不传batch_no参数，后端会返回所有数据（或可以用limit参数限制数量）
    const response = await productApi.export({})

    // 创建下载链接
    const blob = new Blob([response], { type: 'text/csv;charset=utf-8-sig' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5)
    link.download = `商品数据_${timestamp}.csv`

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    logs.value.push(`✓ 数据已导出: 商品数据_${timestamp}.csv`)
    ElMessage.success('CSV文件已下载')
  } catch (error) {
    console.error('Export error:', error)
    logs.value.push('✗ 导出失败: ' + (error.message || '未知错误'))
  }
}

const startPolling = (taskId) => {
  stopPolling()
  pollTimer.value = setInterval(pollTaskStatus, 3000)
}

const stopPolling = () => {
  if (pollTimer.value) {
    clearInterval(pollTimer.value)
    pollTimer.value = null
  }
}

const scrollToBottom = () => {
  if (autoScroll.value && logContainer.value) {
    setTimeout(() => {
      if (logContainer.value) {
        logContainer.value.scrollTop = logContainer.value.scrollHeight
      }
    }, 50)
  }
}

const loadRecentLogs = async () => {
  try {
    logsLoading.value = true
    const res = await crawlerApi.getLogs({ page: 1, page_size: 10 })
    if (res.code === 0) {
      recentLogs.value = res.data || []
    }
  } catch (error) {
    console.error('Load logs error:', error)
  } finally {
    logsLoading.value = false
  }
}

const getStatusClass = (status) => {
  const statusMap = {
    'pending': 'status-pending',
    'running': 'status-running',
    'success': 'status-success',
    'failed': 'status-failed',
    'cancelled': 'status-cancelled'
  }
  return statusMap[status] || ''
}

const getStatusDisplay = (status) => {
  const displayMap = {
    'pending': '等待中',
    'running': '运行中',
    'success': '成功',
    'failed': '失败',
    'cancelled': '已取消'
  }
  return displayMap[status] || status
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatLogTimestamp = () => {
  const now = new Date()
  return now.toLocaleTimeString('zh-CN', { hour12: false })
}

const getLogLineClass = (log) => {
  if (log.includes('失败') || log.includes('错误') || log.includes('✗')) return 'terminal-line--error'
  if (log.includes('成功') || log.includes('完成') || log.includes('✓')) return 'terminal-line--success'
  if (log.includes('警告') || log.includes('提示')) return 'terminal-line--warning'
  if (log.includes('启动') || log.includes('开始')) return 'terminal-line--info'
  return ''
}

// 生命周期
onMounted(() => {
  loadRecentLogs()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="crawler-console">
    <!-- 装饰叶子图案 -->
    <div class="leaf-decoration leaf-decoration--top-left">
      <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
        <path d="M50 5C50 5 85 25 85 55C85 85 65 95 50 95C35 95 15 85 15 55C15 25 50 5 50 5Z" fill="currentColor" opacity="0.04"/>
        <path d="M50 5L50 95" stroke="currentColor" stroke-width="1" opacity="0.06"/>
      </svg>
    </div>
    <div class="leaf-decoration leaf-decoration--bottom-right">
      <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
        <path d="M40 5C40 5 70 18 70 40C70 62 55 75 40 75C25 75 10 62 10 40C10 18 40 5 40 5Z" fill="currentColor" opacity="0.05"/>
      </svg>
    </div>

    <!-- Console Header -->
    <div class="console-header">
      <div class="header-content">
        <div class="header-icon-wrapper">
          <VideoPlay class="header-icon" />
          <div class="icon-pulse"></div>
        </div>
        <div class="header-text">
          <h1 class="header-title">数据采集控制台</h1>
          <p class="header-subtitle">Data Collection Console</p>
        </div>
      </div>
      <div class="header-controls">
        <button class="control-btn control-btn--config" @click="router.push('/admin/crawler/config')">
          <Setting class="control-btn-icon" />
          <span>配置</span>
        </button>
        <div class="status-indicator" :class="`status-indicator--${taskStatus}`">
          <div class="status-dot-wrapper">
            <div class="status-dot"></div>
            <div class="status-pulse-ring"></div>
          </div>
          <span class="status-text">{{ statusConfig.label }}</span>
        </div>
      </div>
    </div>

    <!-- Control Dashboard -->
    <div class="control-dashboard">
      <!-- Parameter Input Panel -->
      <div class="param-panel">
        <div class="param-panel-header">
          <div class="param-header-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M12 1v6m0 6v6"></path>
              <path d="m4.93 4.93 4.24 4.24M19.07 19.07l-4.24-4.24"></path>
            </svg>
          </div>
          <div>
            <h3 class="param-panel-title">采集参数</h3>
            <p class="param-panel-subtitle">Collection Parameters</p>
          </div>
        </div>

        <div class="param-inputs">
          <!-- Keyword Input -->
          <div class="input-group">
            <label class="input-label">
              <span class="label-text">搜索关键词</span>
              <span class="label-hint">Keywords</span>
            </label>
            <div class="input-wrapper">
              <input
                v-model="keywords"
                type="text"
                placeholder="例如: 狗粮、猫砂、玩具"
                class="console-input"
              />
              <div class="input-focus-line"></div>
            </div>
          </div>

          <!-- Page Count Control -->
          <div class="input-group input-group--compact">
            <label class="input-label">
              <span class="label-text">采集页数</span>
              <span class="label-hint">Max Pages: 3</span>
            </label>
            <div class="page-stepper">
              <button
                class="stepper-btn stepper-btn--decrement"
                :disabled="pageCount <= 1"
                @click="pageCount--"
              >
                <span></span>
              </button>
              <div class="stepper-value">
                <span class="value-number">{{ pageCount }}</span>
                <span class="value-unit">页</span>
              </div>
              <button
                class="stepper-btn stepper-btn--increment"
                :disabled="pageCount >= 3"
                @click="pageCount++"
              >
                <span></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-panel">
        <button
          v-if="taskStatus === 'idle' || taskStatus === 'success' || taskStatus === 'failed'"
          class="action-btn action-btn--primary"
          :class="{ 'action-btn--loading': isLoading }"
          :disabled="isLoading"
          @click="startCrawl"
        >
          <span class="action-btn-bg"></span>
          <VideoPlay class="action-btn-icon" />
          <span class="action-btn-text">{{ isLoading ? '启动中...' : '开始采集' }}</span>
          <div class="action-btn-glow"></div>
        </button>

        <button
          v-if="taskStatus === 'running'"
          class="action-btn action-btn--danger"
          @click="stopCrawl"
        >
          <span class="action-btn-bg"></span>
          <VideoPause class="action-btn-icon" />
          <span class="action-btn-text">停止任务</span>
          <div class="action-btn-glow"></div>
        </button>

        <button
          class="action-btn action-btn--success"
          @click="manualExport"
        >
          <span class="action-btn-bg"></span>
          <Download class="action-btn-icon" />
          <span class="action-btn-text">{{ lastBatchNo ? '导出CSV' : '导出数据' }}</span>
          <div class="action-btn-glow"></div>
        </button>

        <button
          class="action-btn action-btn--secondary"
          @click="loadRecentLogs"
        >
          <span class="action-btn-bg"></span>
          <Refresh class="action-btn-icon" :class="{ 'action-btn-icon--spinning': logsLoading }" />
          <span class="action-btn-text">刷新</span>
          <div class="action-btn-glow"></div>
        </button>
      </div>
    </div>

    <!-- Progress Monitor (shown when running) -->
    <div v-if="taskStatus === 'running'" class="progress-monitor">
      <div class="progress-monitor-header">
        <div class="progress-stage-wrapper">
          <div class="progress-stage-icon">
            <Loading class="spinning-icon" />
          </div>
          <div class="progress-stage-info">
            <span class="progress-stage-label">当前阶段</span>
            <span class="progress-stage-value">{{ currentTask?.current_stage || '采集中...' }}</span>
          </div>
        </div>
        <div class="progress-percentage">{{ progressPercent }}%</div>
      </div>

      <div class="progress-track">
        <div class="progress-bar-wrapper">
          <div
            class="progress-bar-fill"
            :style="{ width: progressPercent + '%' }"
          >
            <div class="progress-shimmer"></div>
          </div>
        </div>
      </div>

      <div class="progress-metrics">
        <div class="metric-chip">
          <span class="metric-chip-label">已采集</span>
          <span class="metric-chip-value metric-chip-value--primary">{{ currentTask?.items_collected || 0 }}</span>
        </div>
        <div class="metric-chip">
          <span class="metric-chip-label">成功</span>
          <span class="metric-chip-value metric-chip-value--success">{{ currentTask?.items_success || 0 }}</span>
        </div>
        <div class="metric-chip">
          <span class="metric-chip-label">失败</span>
          <span class="metric-chip-value metric-chip-value--error">{{ currentTask?.items_failed || 0 }}</span>
        </div>
      </div>
    </div>

    <!-- Console Panels Grid -->
    <div class="console-grid">
      <!-- Terminal Log Panel -->
      <div class="console-panel console-panel--terminal">
        <div class="console-panel-header">
          <div class="terminal-header-left">
            <div class="terminal-icon-wrapper">
              <Document class="terminal-icon" />
            </div>
            <div class="terminal-title">
              <span>实时日志 / Real-time Logs</span>
            </div>
          </div>
          <label class="scroll-toggle">
            <input type="checkbox" v-model="autoScroll" class="toggle-checkbox" />
            <span class="toggle-slider"></span>
            <span class="toggle-label">自动滚动</span>
          </label>
        </div>

        <div
          ref="logContainer"
          class="terminal-content"
          :class="{ 'terminal-content--empty': logs.length === 0 }"
        >
          <div v-if="logs.length === 0" class="terminal-empty">
            <div class="empty-terminal-icon">
              <Document class="icon" />
            </div>
            <p class="empty-text">等待采集任务启动...</p>
            <p class="empty-hint">Logs will appear here when crawling starts</p>
          </div>
          <div v-else class="terminal-lines">
            <div
              v-for="(log, index) in logs"
              :key="index"
              class="terminal-line"
              :class="getLogLineClass(log)"
            >
              <span class="line-timestamp">{{ formatLogTimestamp() }}</span>
              <span class="line-prompt">›</span>
              <span class="line-content">{{ log }}</span>
            </div>
          </div>
        </div>

        <div class="terminal-footer">
          <div class="terminal-prompt-line">
            <span class="prompt-user">root@crawler</span>
            <span class="prompt-separator">:</span>
            <span class="prompt-path">~</span>
            <span class="prompt-indicator">$</span>
            <span class="prompt-cursor"></span>
          </div>
        </div>
      </div>

      <!-- History Records Panel -->
      <div class="console-panel console-panel--history">
        <div class="console-panel-header">
          <div class="history-header-left">
            <div class="history-icon-wrapper">
              <Clock class="history-icon" />
            </div>
            <div class="history-title-group">
              <h3 class="history-title">历史记录</h3>
              <p class="history-subtitle">Collection History</p>
            </div>
          </div>
          <div class="history-count">{{ recentLogs.length }} 条记录</div>
        </div>

        <div class="history-content">
          <div v-if="recentLogs.length === 0" class="history-empty">
            <Clock class="empty-icon" />
            <p class="empty-text">暂无采集记录</p>
            <p class="empty-hint">Start a collection task to see history</p>
          </div>
          <div v-else class="history-list">
            <div
              v-for="log in recentLogs"
              :key="log.id"
              class="history-card"
              :class="`history-card--${log.status}`"
            >
              <div class="history-card-left">
                <div class="history-status-indicator" :class="`history-status-indicator--${log.status}`">
                  <div class="status-dot-inner"></div>
                </div>
                <div class="history-card-info">
                  <p class="history-keyword">{{ log.keywords || '未指定' }}</p>
                  <p class="history-datetime">{{ formatDateTime(log.created_at) }}</p>
                </div>
              </div>
              <div class="history-card-metrics">
                <div class="history-metric">
                  <span class="metric-label">采集</span>
                  <span class="metric-value">{{ log.items_collected || 0 }}</span>
                </div>
                <div class="history-metric history-metric--success">
                  <span class="metric-label">成功</span>
                  <span class="metric-value">{{ log.items_success || 0 }}</span>
                </div>
                <div v-if="log.items_failed > 0" class="history-metric history-metric--failed">
                  <span class="metric-label">失败</span>
                  <span class="metric-value">{{ log.items_failed }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.crawler-console {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  --status-idle: #A8A29E;
  --status-running: #52B788;
  --status-success: #52B788;
  --status-failed: #DC2626;

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
  animation: pageFadeIn 0.5s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  color: var(--primary-green);
}

.leaf-decoration--top-left {
  top: -20px;
  left: -20px;
  opacity: 0.5;
}

.leaf-decoration--bottom-right {
  bottom: 80px;
  right: -30px;
  opacity: 0.4;
}

/* ============================================
   Console Header
   ============================================ */
.console-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 18px;
}

.header-icon-wrapper {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(82, 183, 136, 0.08));
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 20px;
  position: relative;
}

.icon-pulse {
  position: absolute;
  inset: -4px;
  border-radius: 24px;
  background: var(--primary-light);
  opacity: 0;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0; }
  50% { opacity: 0.2; }
}

.header-icon {
  width: 26px;
  height: 26px;
  color: var(--primary-green);
  position: relative;
  z-index: 1;
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.01em;
}

.header-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'Nunito', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 14px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.control-btn:hover {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
}

.control-btn-icon {
  width: 17px;
  height: 17px;
}

/* Status Indicator */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  font-size: 13px;
  font-weight: 600;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s ease;
}

.status-indicator--idle {
  color: var(--status-idle);
  background: linear-gradient(135deg, rgba(168, 162, 158, 0.1), rgba(168, 162, 158, 0.05));
  border-color: rgba(168, 162, 158, 0.2);
}

.status-indicator--running {
  color: var(--status-running);
  background: linear-gradient(135deg, rgba(82, 183, 136, 0.15), rgba(116, 198, 157, 0.08));
  border-color: rgba(82, 183, 136, 0.3);
}

.status-indicator--success {
  color: var(--status-success);
  background: linear-gradient(135deg, rgba(82, 183, 136, 0.15), rgba(116, 198, 157, 0.08));
  border-color: rgba(82, 183, 136, 0.3);
}

.status-indicator--failed {
  color: var(--status-failed);
  background: linear-gradient(135deg, rgba(220, 38, 38, 0.12), rgba(239, 68, 68, 0.06));
  border-color: rgba(220, 38, 38, 0.2);
}

.status-dot-wrapper {
  position: relative;
  width: 14px;
  height: 14px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: currentColor;
  position: relative;
}

.status-indicator--running .status-dot {
  animation: statusDotPulse 1.5s ease-in-out infinite;
}

@keyframes statusDotPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.status-pulse-ring {
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid currentColor;
  opacity: 0;
}

.status-indicator--running .status-pulse-ring {
  animation: pulseRing 2s ease-out infinite;
}

@keyframes pulseRing {
  0% { transform: scale(0.8); opacity: 0.5; }
  100% { transform: scale(2); opacity: 0; }
}

/* ============================================
   Control Dashboard
   ============================================ */
.control-dashboard {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  position: relative;
  z-index: 1;
}

@media (max-width: 1000px) {
  .control-dashboard {
    grid-template-columns: 1fr;
  }
}

/* Parameter Panel */
.param-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
  animation: panelSlideIn 0.5s ease 0.1s backwards;
}

@keyframes panelSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.param-panel-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px 24px;
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
  border-bottom: 1px solid var(--border-light);
}

.param-header-icon {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.12), rgba(82, 183, 136, 0.08));
  border-radius: 12px;
  color: var(--primary-green);
}

.param-panel-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.param-panel-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'Nunito', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.param-inputs {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group--compact {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
}

.label-hint {
  font-size: 11px;
  color: var(--text-tertiary);
  font-family: 'Nunito', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.input-wrapper {
  position: relative;
}

.console-input {
  width: 100%;
  padding: 14px 18px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.console-input::placeholder {
  color: var(--text-tertiary);
}

.console-input:focus {
  outline: none;
  border-color: var(--border-focus);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.input-focus-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-green), var(--primary-light));
  transition: width 0.3s ease;
}

.console-input:focus ~ .input-focus-line {
  width: 100%;
}

/* Page Stepper */
.page-stepper {
  display: flex;
  align-items: center;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  overflow: hidden;
}

.stepper-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.stepper-btn::before {
  content: '';
  width: 12px;
  height: 12px;
  border-right: 2px solid var(--border-light);
  border-bottom: 2px solid var(--border-light);
  transform: rotate(45deg);
  transition: all 0.2s ease;
}

.stepper-btn--decrement::before {
  transform: rotate(225deg);
  left: 18px;
}

.stepper-btn--increment::before {
  right: 18px;
}

.stepper-btn:hover:not(:disabled) {
  background: rgba(45, 106, 79, 0.08);
}

.stepper-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.stepper-value {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 0 16px;
}

.value-number {
  font-family: 'Nunito', monospace;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.value-unit {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
}

/* Action Panel */
.action-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--bg-sand), var(--bg-card));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.action-btn:hover:not(:disabled) .action-btn-bg {
  opacity: 1;
}

.action-btn-icon {
  width: 18px;
  height: 18px;
  position: relative;
  z-index: 1;
}

.action-btn-icon--spinning {
  animation: spin 1s linear infinite;
}

.action-btn-text {
  position: relative;
  z-index: 1;
  font-weight: 700;
}

.action-btn-glow {
  position: absolute;
  inset: -2px;
  border-radius: 18px;
  opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(8px);
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-green), var(--primary-teal));
  border: none;
  color: white;
}

.action-btn--primary .action-btn-glow {
  background: var(--primary-green);
  opacity: 0.3;
}

.action-btn--primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(45, 106, 79, 0.35);
}

.action-btn--primary:hover:not(:disabled) .action-btn-glow {
  opacity: 0.5;
}

.action-btn--danger {
  background: linear-gradient(135deg, #DC2626, #EF4444);
  border: none;
  color: white;
}

.action-btn--danger .action-btn-glow {
  background: #DC2626;
  opacity: 0.3;
}

.action-btn--danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3);
}

.action-btn--success {
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-blue-light));
  border: none;
  color: white;
}

.action-btn--success .action-btn-glow {
  background: var(--accent-blue);
  opacity: 0.3;
}

.action-btn--success:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 180, 216, 0.3);
}

.action-btn--secondary {
  background: var(--bg-card);
}

.action-btn--secondary:hover:not(:disabled) {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
}

/* ============================================
   Progress Monitor
   ============================================ */
.progress-monitor {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
  animation: panelSlideIn 0.5s ease 0.2s backwards;
}

.progress-monitor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.06), rgba(82, 183, 136, 0.03));
  border-bottom: 1px solid rgba(116, 198, 157, 0.15);
}

.progress-stage-wrapper {
  display: flex;
  align-items: center;
  gap: 14px;
}

.progress-stage-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(82, 183, 136, 0.15);
  border-radius: 12px;
  color: var(--primary-green);
}

.spinning-icon {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.progress-stage-info {
  flex: 1;
}

.progress-stage-label {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
  display: block;
}

.progress-stage-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.progress-percentage {
  font-family: 'Nunito', monospace;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-green);
}

.progress-track {
  padding: 0 24px 20px;
  background: var(--bg-sand);
}

.progress-bar-wrapper {
  height: 8px;
  background: var(--border-light);
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-teal), var(--primary-light));
  border-radius: 10px;
  position: relative;
  transition: width 0.5s ease;
}

.progress-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-metrics {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;
}

.metric-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-sand);
  border-radius: 10px;
}

.metric-chip-label {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.metric-chip-value {
  font-family: 'Nunito', monospace;
  font-size: 14px;
  font-weight: 700;
}

.metric-chip-value--primary {
  color: var(--primary-green);
}

.metric-chip-value--success {
  color: var(--primary-light);
}

.metric-chip-value--error {
  color: #DC2626;
}

/* ============================================
   Console Grid
   ============================================ */
.console-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
  position: relative;
  z-index: 1;
}

@media (max-width: 1200px) {
  .console-grid {
    grid-template-columns: 1fr;
  }
}

/* Console Panel */
.console-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.console-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
}

.terminal-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.terminal-icon-wrapper {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 106, 79, 0.1);
  border-radius: 10px;
  color: var(--primary-green);
}

.terminal-icon {
  width: 16px;
  height: 16px;
}

.terminal-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.terminal-title span {
  font-family: 'Nunito', sans-serif;
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 400;
}

/* Scroll Toggle */
.scroll-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
}

.toggle-checkbox {
  position: relative;
  width: 40px;
  height: 22px;
  appearance: none;
  background: var(--bg-sand);
  border: 2px solid var(--border-light);
  border-radius: 11px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-checkbox:checked {
  background: var(--primary-green);
  border-color: var(--primary-green);
}

.toggle-checkbox:checked + .toggle-slider {
  transform: translateX(18px);
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.toggle-label {
  font-weight: 500;
}

/* Terminal Content */
.terminal-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: linear-gradient(180deg, #1C1917 0%, #0F1720 100%);
  border-radius: 0 0 12px 12px;
  margin: 0 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
}

.terminal-content::-webkit-scrollbar {
  width: 8px;
}

.terminal-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
}

.terminal-content::-webkit-scrollbar-thumb {
  background: rgba(45, 106, 79, 0.3);
  border-radius: 4px;
}

.terminal-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
}

.empty-terminal-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 106, 79, 0.1);
  border-radius: 12px;
  margin-bottom: 16px;
  color: var(--primary-green);
}

.empty-terminal-icon .icon {
  width: 20px;
  height: 20px;
}

.empty-text {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0 0 4px 0;
}

.empty-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  opacity: 0.7;
}

.terminal-lines {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.terminal-line {
  display: flex;
  gap: 8px;
  line-height: 1.6;
}

.line-timestamp {
  color: var(--text-tertiary);
  font-size: 11px;
  opacity: 0.7;
  flex-shrink: 0;
}

.line-prompt {
  color: var(--accent-green);
  font-weight: 600;
  flex-shrink: 0;
}

.line-content {
  color: rgba(255, 255, 255, 0.9);
  flex: 1;
}

.terminal-line--error .line-content {
  color: #FF6B6B;
}

.terminal-line--success .line-content {
  color: var(--primary-light);
}

.terminal-line--warning .line-content {
  color: #FFB800;
}

.terminal-line--info .line-content {
  color: var(--accent-blue);
}

/* Terminal Footer */
.terminal-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(45, 106, 79, 0.2);
}

.terminal-prompt-line {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  color: rgba(255, 255, 255, 0.7);
}

.prompt-user {
  color: var(--primary-green);
  font-weight: 600;
}

.prompt-separator {
  color: rgba(255, 255, 255, 0.4);
}

.prompt-path {
  color: var(--accent-blue);
}

.prompt-indicator {
  color: var(--primary-light);
}

.prompt-cursor {
  width: 8px;
  height: 16px;
  background: var(--primary-light);
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* ============================================
   History Panel
   ============================================ */
.console-panel--history {
  min-height: 400px;
}

.history-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.history-icon-wrapper {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 180, 216, 0.12);
  border-radius: 10px;
  color: var(--accent-blue);
}

.history-icon {
  width: 16px;
  height: 16px;
}

.history-title-group {
  flex: 1;
}

.history-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.history-subtitle {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.history-count {
  font-size: 12px;
  color: var(--text-tertiary);
  background: var(--bg-sand);
  padding: 4px 12px;
  border-radius: 12px;
}

.history-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.history-content::-webkit-scrollbar {
  width: 6px;
}

.history-content::-webkit-scrollbar-track {
  background: var(--bg-sand);
}

.history-content::-webkit-scrollbar-thumb {
  background: var(--border-light);
  border-radius: 3px;
}

.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
}

.empty-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 106, 79, 0.08);
  border-radius: 12px;
  margin-bottom: 16px;
  color: var(--primary-green);
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0 0 4px 0;
}

.empty-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  opacity: 0.7;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  transition: all 0.3s ease;
}

.history-card:hover {
  background: var(--bg-card);
  border-color: var(--accent-green);
  transform: translateX(4px);
}

.history-card-left {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
}

.history-status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  position: relative;
}

.history-status-indicator::before {
  content: '';
  position: absolute;
  inset: 2px;
  border-radius: 50%;
  background: currentColor;
}

.history-status-indicator--success {
  color: var(--primary-light);
}

.history-status-indicator--failed {
  color: #DC2626;
}

.history-status-indicator--pending {
  color: #FFB800;
}

.status-dot-inner {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: currentColor;
}

.history-card-info {
  flex: 1;
}

.history-keyword {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.history-datetime {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'Nunito', monospace;
}

.history-card-metrics {
  display: flex;
  gap: 16px;
}

.history-metric {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.metric-label {
  font-size: 10px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.metric-value {
  font-family: 'Nunito', monospace;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.history-metric--success .metric-value {
  color: var(--primary-light);
}

.history-metric--failed .metric-value {
  color: #DC2626;
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 768px) {
  .console-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-controls {
    width: 100%;
    justify-content: space-between;
  }

  .control-dashboard {
    grid-template-columns: 1fr;
  }

  .console-grid {
    grid-template-columns: 1fr;
  }

  .action-btn {
    width: 100%;
  }

  .leaf-decoration {
    display: none;
  }
}
</style>
