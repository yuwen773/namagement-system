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
    const keyword = keywords.value.trim() || '高达'

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

// 生命周期
onMounted(() => {
  loadRecentLogs()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="crawler-container">
    <!-- 控制面板 -->
    <div class="control-panel">
      <div class="control-header">
        <div class="header-title">
          <VideoPlay class="title-icon" />
          <h2>宠物数据采集</h2>
        </div>
        <div class="header-actions">
          <el-button
            type="primary"
            :icon="Setting"
            @click="router.push('/admin/crawler/config')"
            class="config-btn"
          >
            爬虫配置
          </el-button>
          <div class="status-badge" :style="{
            background: statusConfig.bg,
            borderColor: statusConfig.border,
            color: statusConfig.color
          }">
            <component :is="statusConfig.icon" class="status-icon" :class="{ spinning: taskStatus === 'running' }" />
            <span>{{ statusConfig.label }}</span>
          </div>
        </div>
      </div>

      <div class="control-content">
        <!-- 采集参数 -->
        <div class="params-section">
          <!-- 关键词输入 -->
          <div class="keywords-input">
            <label>搜索关键词</label>
            <input
              v-model="keywords"
              type="text"
              placeholder="例如: 高达、手办、模型"
              class="input-field"
            />
          </div>

          <!-- 页数限制 -->
          <div class="page-count-input">
            <label>采集页数（最多3页）</label>
            <div class="page-control">
              <button
                class="page-btn"
                :disabled="pageCount <= 1"
                @click="pageCount--"
              >-</button>
              <span class="page-value">{{ pageCount }}</span>
              <button
                class="page-btn"
                :disabled="pageCount >= 3"
                @click="pageCount++"
              >+</button>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button
            v-if="taskStatus === 'idle' || taskStatus === 'success' || taskStatus === 'failed'"
            class="btn btn-primary"
            :disabled="isLoading"
            @click="startCrawl"
          >
            <VideoPlay class="btn-icon" />
            <span>{{ isLoading ? '启动中...' : '开始采集' }}</span>
          </button>

          <button
            v-if="taskStatus === 'running'"
            class="btn btn-danger"
            @click="stopCrawl"
          >
            <VideoPause class="btn-icon" />
            <span>停止任务</span>
          </button>

          <button
            class="btn btn-success"
            @click="manualExport"
          >
            <Download class="btn-icon" />
            <span>{{ lastBatchNo ? '导出CSV' : '导出已有数据' }}</span>
          </button>

          <button
            class="btn btn-secondary"
            @click="loadRecentLogs"
          >
            <Refresh class="btn-icon" :class="{ spinning: logsLoading }" />
            <span>刷新记录</span>
          </button>
        </div>
      </div>

      <!-- 进度条 -->
      <div v-if="taskStatus === 'running'" class="progress-section">
        <div class="progress-header">
          <span class="progress-label">{{ currentTask?.current_stage || '采集中...' }}</span>
          <span class="progress-value">{{ progressPercent }}%</span>
        </div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: progressPercent + '%' }"
          >
            <div class="progress-glow"></div>
          </div>
        </div>
        <div class="progress-stats">
          <span>已采集: <strong>{{ currentTask?.items_collected || 0 }}</strong></span>
          <span>成功: <strong>{{ currentTask?.items_success || 0 }}</strong></span>
          <span>失败: <strong>{{ currentTask?.items_failed || 0 }}</strong></span>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="content-row">
      <!-- 实时日志 -->
      <div class="log-panel">
        <div class="panel-header">
          <div class="panel-title">
            <Document class="title-icon" />
            <h3>实时日志</h3>
          </div>
          <label class="auto-scroll-toggle">
            <input type="checkbox" v-model="autoScroll" />
            <span>自动滚动</span>
          </label>
        </div>
        <div
          ref="logContainer"
          class="log-content"
          :class="{ 'empty-logs': logs.length === 0 }"
        >
          <div v-if="logs.length === 0" class="log-empty">
            <Document class="empty-icon" />
            <p>暂无日志记录</p>
            <small>启动采集任务后，日志将实时显示在这里</small>
          </div>
          <div
            v-for="(log, index) in logs"
            :key="index"
            class="log-line"
          >
            <span class="log-time">{{ formatDateTime(new Date()) }}</span>
            <span class="log-text">{{ log }}</span>
          </div>
        </div>
      </div>

      <!-- 历史记录 -->
      <div class="history-panel">
        <div class="panel-header">
          <div class="panel-title">
            <Clock class="title-icon" />
            <h3>最近记录</h3>
          </div>
        </div>
        <div class="history-content">
          <div v-if="recentLogs.length === 0" class="history-empty">
            <Clock class="empty-icon" />
            <p>暂无历史记录</p>
          </div>
          <div v-else class="history-list">
            <div
              v-for="log in recentLogs"
              :key="log.id"
              class="history-item"
            >
              <div class="history-main">
                <div class="history-status" :class="getStatusClass(log.status)">
                  <span class="status-dot"></span>
                </div>
                <div class="history-info">
                  <p class="history-keywords">{{ log.keywords || '未指定' }}</p>
                  <p class="history-time">{{ formatDateTime(log.created_at) }}</p>
                </div>
              </div>
              <div class="history-stats">
                <span class="stat-item">
                  <span class="stat-label">采集</span>
                  <strong>{{ log.items_collected || 0 }}</strong>
                </span>
                <span class="stat-item success">
                  <span class="stat-label">成功</span>
                  <strong>{{ log.items_success || 0 }}</strong>
                </span>
                <span class="stat-item failed" v-if="log.items_failed > 0">
                  <span class="stat-label">失败</span>
                  <strong>{{ log.items_failed }}</strong>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

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
