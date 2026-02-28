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
      color: '#FFD700',
      bg: 'rgba(255, 215, 0, 0.15)',
      border: 'rgba(255, 215, 0, 0.3)',
      icon: Clock
    },
    running: {
      label: '运行中',
      color: '#06FFA5',
      bg: 'rgba(6, 255, 165, 0.15)',
      border: 'rgba(6, 255, 165, 0.3)',
      icon: Loading
    },
    success: {
      label: '已完成',
      color: '#06FFA5',
      bg: 'rgba(6, 255, 165, 0.15)',
      border: 'rgba(6, 255, 165, 0.3)',
      icon: Check
    },
    failed: {
      label: '失败',
      color: '#FF6B6B',
      bg: 'rgba(255, 107, 107, 0.15)',
      border: 'rgba(255, 107, 107, 0.3)',
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
          <div class="param-header-icon">⚙</div>
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
            <div class="terminal-controls">
              <span class="terminal-control terminal-control--close"></span>
              <span class="terminal-control terminal-control--minimize"></span>
              <span class="terminal-control terminal-control--maximize"></span>
            </div>
            <div class="terminal-title">
              <Document class="terminal-icon" />
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Variables
   ============================================ */
.crawler-console {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --primary-red: #FF6B6B;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --bg-terminal: rgba(10, 10, 16, 0.8);
  --console-grid: rgba(255, 107, 53, 0.03);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  position: relative;
}

/* Circuit Pattern Background */
.crawler-console::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(var(--console-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--console-grid) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: -1;
}

/* ============================================
   Console Header
   ============================================ */
.console-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 4px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon-wrapper {
  position: relative;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(123, 44, 191, 0.15));
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 16px;
}

.header-icon {
  width: 26px;
  height: 26px;
  color: var(--primary-orange);
  position: relative;
  z-index: 1;
}

.icon-pulse {
  position: absolute;
  inset: 8px;
  background: radial-gradient(circle, var(--primary-orange) 0%, transparent 70%);
  border-radius: 50%;
  opacity: 0;
  animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { opacity: 0; transform: scale(0.8); }
  50% { opacity: 0.3; transform: scale(1); }
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 2px 0 0 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 500;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.control-btn--config {
  background: rgba(123, 44, 191, 0.1);
  border-color: rgba(123, 44, 191, 0.3);
  color: #B983FF;
}

.control-btn--config:hover {
  background: rgba(123, 44, 191, 0.2);
  border-color: rgba(123, 44, 191, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(123, 44, 191, 0.3);
}

.control-btn-icon {
  width: 16px;
  height: 16px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.3s ease;
}

.status-indicator--idle {
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
  color: var(--primary-gold);
}

.status-indicator--running {
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.3);
  color: var(--primary-cyan);
}

.status-indicator--success {
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.3);
  color: var(--primary-cyan);
}

.status-indicator--failed {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: var(--primary-red);
}

.status-dot-wrapper {
  position: relative;
  width: 12px;
  height: 12px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: currentColor;
  box-shadow: 0 0 12px currentColor;
}

.status-pulse-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid currentColor;
  opacity: 0;
}

.status-indicator--running .status-pulse-ring {
  animation: statusPulse 2s ease-out infinite;
}

@keyframes statusPulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}

/* ============================================
   Control Dashboard
   ============================================ */
.control-dashboard {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  align-items: start;
}

.param-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  padding: 24px;
  animation: panelSlideIn 0.5s ease backwards;
  animation-delay: 0.1s;
}

@keyframes panelSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.param-panel-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.param-header-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(123, 44, 191, 0.15));
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 12px;
  font-size: 20px;
}

.param-panel-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.param-panel-subtitle {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.param-inputs {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label-text {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.label-hint {
  font-size: 10px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
}

.console-input {
  width: 100%;
  padding: 14px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
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
  border-color: var(--primary-orange);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.input-focus-line {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-orange), var(--primary-purple));
  width: 0;
  transition: width 0.3s ease;
}

.console-input:focus ~ .input-focus-line {
  width: 100%;
}

/* Page Stepper */
.page-stepper {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  overflow: hidden;
}

.stepper-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.stepper-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 107, 53, 0.1);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.stepper-btn:hover:not(:disabled)::before {
  opacity: 1;
}

.stepper-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.stepper-btn span {
  width: 12px;
  height: 12px;
  background: currentColor;
  clip-path: polygon(50% 0%, 0% 50%, 50% 100%, 50% 65%, 85% 50%, 50% 35%);
  color: var(--text-secondary);
}

.stepper-btn--decrement span {
  transform: rotate(180deg);
}

.stepper-value {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
}

.value-number {
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.value-unit {
  font-size: 10px;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

/* Action Panel */
.action-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: panelSlideIn 0.5s ease backwards;
  animation-delay: 0.2s;
}

.action-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  overflow: hidden;
  transition: all 0.3s ease;
  font-family: inherit;
}

.action-btn-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.action-btn--primary .action-btn-bg {
  background: linear-gradient(135deg, var(--primary-orange), #FF8C5A);
}

.action-btn--danger .action-btn-bg {
  background: linear-gradient(135deg, var(--primary-red), #FF8E8E);
}

.action-btn--success .action-btn-bg {
  background: linear-gradient(135deg, var(--primary-cyan), #06D4A5);
}

.action-btn--secondary .action-btn-bg {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-default);
}

.action-btn-icon,
.action-btn-text {
  position: relative;
  z-index: 1;
}

.action-btn--primary,
.action-btn--danger,
.action-btn--success {
  color: white;
}

.action-btn--secondary {
  color: var(--text-secondary);
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

.action-btn--primary:hover:not(:disabled) .action-btn-glow,
.action-btn--danger:hover:not(:disabled) .action-btn-glow,
.action-btn--success:hover:not(:disabled) .action-btn-glow {
  opacity: 1;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn--loading {
  pointer-events: none;
}

.action-btn-icon {
  width: 16px;
  height: 16px;
}

.action-btn-icon--spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.action-btn-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.3), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}

/* ============================================
   Progress Monitor
   ============================================ */
.progress-monitor {
  background: linear-gradient(135deg, rgba(6, 255, 165, 0.05), rgba(123, 44, 191, 0.03));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(6, 255, 165, 0.15);
  border-radius: 20px;
  padding: 24px;
  animation: panelSlideIn 0.5s ease backwards;
  animation-delay: 0.3s;
}

.progress-monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  background: rgba(6, 255, 165, 0.15);
  border-radius: 12px;
  color: var(--primary-cyan);
}

.spinning-icon {
  width: 20px;
  height: 20px;
  animation: spin 2s linear infinite;
}

.progress-stage-info {
  display: flex;
  flex-direction: column;
}

.progress-stage-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.progress-stage-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.progress-percentage {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-cyan);
}

.progress-track {
  margin-bottom: 20px;
}

.progress-bar-wrapper {
  height: 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-purple), var(--primary-orange), var(--primary-cyan));
  border-radius: 10px;
  position: relative;
  transition: width 0.5s ease;
}

.progress-shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-metrics {
  display: flex;
  gap: 16px;
}

.metric-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.metric-chip-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

.metric-chip-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 700;
}

.metric-chip-value--primary { color: var(--primary-orange); }
.metric-chip-value--success { color: var(--primary-cyan); }
.metric-chip-value--error { color: var(--primary-red); }

/* ============================================
   Console Grid
   ============================================ */
.console-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
}

.console-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: panelSlideIn 0.5s ease backwards;
  animation-delay: 0.4s;
}

/* ============================================
   Terminal Panel
   ============================================ */
.console-panel--terminal {
  animation-delay: 0.4s;
}

.console-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.3);
}

.terminal-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.terminal-controls {
  display: flex;
  gap: 8px;
}

.terminal-control {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.terminal-control--close { background: #FF5F57; }
.terminal-control--minimize { background: #FFBD2E; }
.terminal-control--maximize { background: #28CA42; }

.terminal-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
}

.terminal-icon {
  width: 14px;
  height: 14px;
  color: var(--primary-orange);
}

.scroll-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 12px;
  color: var(--text-secondary);
}

.toggle-checkbox {
  display: none;
}

.toggle-slider {
  width: 36px;
  height: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  border: 1px solid var(--border-default);
  position: relative;
  transition: all 0.3s ease;
}

.toggle-slider::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  background: var(--text-tertiary);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.toggle-checkbox:checked + .toggle-slider {
  background: rgba(255, 107, 53, 0.2);
  border-color: var(--primary-orange);
}

.toggle-checkbox:checked + .toggle-slider::after {
  left: 18px;
  background: var(--primary-orange);
  box-shadow: 0 0 10px var(--primary-orange);
}

.terminal-content {
  flex: 1;
  background: var(--bg-terminal);
  padding: 16px;
  overflow-y: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  min-height: 320px;
}

.terminal-content--empty {
  display: flex;
  align-items: center;
  justify-content: center;
}

.terminal-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--text-tertiary);
}

.empty-terminal-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 53, 0.1);
  border-radius: 16px;
  margin-bottom: 16px;
}

.empty-terminal-icon .icon {
  width: 24px;
  height: 24px;
  color: var(--primary-orange);
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 4px 0;
}

.empty-hint {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.terminal-lines {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.terminal-line {
  display: flex;
  gap: 10px;
  padding: 6px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.terminal-line:hover {
  background: rgba(255, 255, 255, 0.03);
}

.line-timestamp {
  color: var(--text-tertiary);
  font-size: 11px;
  opacity: 0.6;
  flex-shrink: 0;
}

.line-prompt {
  color: var(--primary-orange);
  flex-shrink: 0;
  font-weight: 600;
}

.line-content {
  color: var(--text-secondary);
  word-break: break-all;
}

.terminal-line--info .line-content {
  color: #7DD3FC;
}

.terminal-line--success .line-content {
  color: var(--primary-cyan);
}

.terminal-line--warning .line-content {
  color: var(--primary-gold);
}

.terminal-line--error .line-content {
  color: var(--primary-red);
}

.terminal-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.3);
}

.terminal-prompt-line {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}

.prompt-user {
  color: var(--primary-cyan);
  font-weight: 600;
}

.prompt-separator {
  color: var(--text-tertiary);
}

.prompt-path {
  color: var(--primary-purple);
  font-weight: 600;
}

.prompt-indicator {
  color: var(--primary-orange);
  font-weight: 600;
}

.prompt-cursor {
  width: 8px;
  height: 16px;
  background: var(--text-tertiary);
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
  animation-delay: 0.5s;
}

.history-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.history-icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(123, 44, 191, 0.15);
  border-radius: 12px;
}

.history-icon {
  width: 18px;
  height: 18px;
  color: var(--primary-purple);
}

.history-title-group {
  display: flex;
  flex-direction: column;
}

.history-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.history-subtitle {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.history-count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--text-tertiary);
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
}

.history-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 320px;
  text-align: center;
  color: var(--text-tertiary);
}

.history-empty .empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.3;
}

.history-empty .empty-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 4px 0;
}

.history-empty .empty-hint {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
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
  background: rgba(0, 0, 0, 0.2);
  border-radius: 14px;
  border: 1px solid var(--border-subtle);
  transition: all 0.3s ease;
  cursor: pointer;
}

.history-card:hover {
  border-color: rgba(255, 107, 53, 0.3);
  background: rgba(255, 107, 53, 0.05);
  transform: translateX(4px);
}

.history-card-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.history-status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: relative;
  flex-shrink: 0;
}

.history-status-indicator--pending {
  background: var(--primary-gold);
  box-shadow: 0 0 12px var(--primary-gold);
}

.history-status-indicator--running {
  background: var(--primary-cyan);
  box-shadow: 0 0 12px var(--primary-cyan);
  animation: runningPulse 2s ease-in-out infinite;
}

@keyframes runningPulse {
  0%, 100% { box-shadow: 0 0 12px var(--primary-cyan); }
  50% { box-shadow: 0 0 20px var(--primary-cyan); }
}

.history-status-indicator--success {
  background: var(--primary-cyan);
  box-shadow: 0 0 12px var(--primary-cyan);
}

.history-status-indicator--failed {
  background: var(--primary-red);
  box-shadow: 0 0 12px var(--primary-red);
}

.history-status-indicator--cancelled {
  background: var(--text-tertiary);
}

.history-card-info {
  display: flex;
  flex-direction: column;
}

.history-keyword {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.history-datetime {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.history-card-metrics {
  display: flex;
  gap: 12px;
}

.history-metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  min-width: 50px;
}

.history-metric--success {
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.2);
}

.history-metric--failed {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.2);
}

.history-metric .metric-label {
  font-size: 9px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2px;
}

.history-metric .metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.history-metric--success .metric-value {
  color: var(--primary-cyan);
}

.history-metric--failed .metric-value {
  color: var(--primary-red);
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 1400px) {
  .console-grid {
    grid-template-columns: 1fr;
  }

  .control-dashboard {
    grid-template-columns: 1fr;
  }

  .action-panel {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1;
    min-width: 140px;
  }
}

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

  .param-inputs {
    grid-template-columns: 1fr;
  }

  .action-panel {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }

  .console-panel-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .history-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .history-card-metrics {
    width: 100%;
    justify-content: space-between;
  }
}

.crawler-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 控制面板 */
.control-panel {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 24px;
  position: relative;
  overflow: hidden;
}

.control-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: radial-gradient(ellipse at top right,
    rgba(255, 107, 53, 0.08) 0%,
    transparent 50%);
  pointer-events: none;
}

.control-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-title .title-icon {
  width: 28px;
  height: 28px;
  color: #FF6B35;
}

.header-title h2 {
  font-size: 20px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.config-btn {
  background: rgba(123, 44, 191, 0.2);
  border-color: rgba(123, 44, 191, 0.4);
  color: #B983FF;
}

.config-btn:hover {
  background: rgba(123, 44, 191, 0.3);
  border-color: rgba(123, 44, 191, 0.6);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: 1px solid;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.status-icon {
  width: 18px;
  height: 18px;
}

.status-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.control-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 参数区域 */
.params-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

/* 关键词输入 */
.keywords-input {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.keywords-input label {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

/* 页数限制 */
.page-count-input {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.page-count-input label {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.page-control {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px;
}

.page-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background: rgba(255, 107, 53, 0.2);
  color: #FF6B35;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-value {
  flex: 1;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  font-family: 'JetBrains Mono', monospace;
}

.input-field {
  width: 100%;
  padding: 14px 18px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-family: 'Noto Sans SC', sans-serif;
  transition: all 0.3s ease;
}

.input-field::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.input-field:focus {
  outline: none;
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 12px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.btn-icon.spinning {
  animation: spin 1s linear infinite;
}

.btn-primary {
  background: linear-gradient(135deg, #FF6B35, #FF8C5A);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-danger {
  background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
  color: white;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-success {
  background: linear-gradient(135deg, #06FFA5, #06D4A5);
  color: #1a1a2e;
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(6, 255, 165, 0.4);
}

/* 进度条 */
.progress-section {
  margin-top: 20px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
  border: 1px solid rgba(6, 255, 165, 0.2);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.progress-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.progress-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  color: #06FFA5;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 16px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7B2CBF, #FF6B35, #06FFA5);
  border-radius: 10px;
  position: relative;
  transition: width 0.5s ease;
}

.progress-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-stats {
  display: flex;
  gap: 24px;
  font-size: 13px;
}

.progress-stats span {
  color: rgba(255, 255, 255, 0.5);
}

.progress-stats strong {
  color: rgba(255, 255, 255, 0.9);
  margin-left: 4px;
}

/* 内容行 */
.content-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
}

/* 日志面板 */
.log-panel {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 480px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.panel-title .title-icon {
  width: 20px;
  height: 20px;
  color: #FF6B35;
}

.panel-title h3 {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.auto-scroll-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

.auto-scroll-toggle input {
  width: 16px;
  height: 16px;
  accent-color: #FF6B35;
}

.log-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}

.log-content.empty-logs {
  display: flex;
  align-items: center;
  justify-content: center;
}

.log-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.3);
  text-align: center;
}

.log-empty .empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.log-empty p {
  font-size: 14px;
  margin: 0 0 4px 0;
}

.log-empty small {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.2);
}

.log-line {
  display: flex;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.log-time {
  color: rgba(255, 255, 255, 0.3);
  font-size: 11px;
  white-space: nowrap;
}

.log-text {
  color: rgba(255, 255, 255, 0.7);
}

/* 历史记录面板 */
.history-panel {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 480px;
}

.history-content {
  flex: 1;
  overflow-y: auto;
}

.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.3);
  text-align: center;
  padding: 40px;
}

.history-empty .empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.history-empty p {
  font-size: 14px;
  margin: 0;
}

.history-list {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
}

.history-item:hover {
  border-color: rgba(255, 107, 53, 0.2);
  background: rgba(255, 107, 53, 0.05);
}

.history-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.history-status {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  position: relative;
}

.status-dot {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: currentColor;
}

.history-status.status-pending {
  color: #FFD700;
}

.history-status.status-running {
  color: #06FFA5;
}

.history-status.status-success {
  color: #06FFA5;
}

.history-status.status-failed {
  color: #FF6B6B;
}

.history-status.status-cancelled {
  color: rgba(255, 255, 255, 0.3);
}

.history-info p {
  margin: 0;
}

.history-keywords {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.history-time {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 2px;
}

.history-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 2px;
}

.stat-item strong {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.stat-item.success strong {
  color: #06FFA5;
}

.stat-item.failed strong {
  color: #FF6B6B;
}

/* 响应式 */
@media (max-width: 1200px) {
  .content-row {
    grid-template-columns: 1fr;
  }

  .log-panel,
  .history-panel {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .params-section {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
