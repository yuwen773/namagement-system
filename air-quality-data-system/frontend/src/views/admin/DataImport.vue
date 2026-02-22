<template>
  <div class="data-import-container">
    <!-- Header -->
    <header class="import-header">
      <div class="header-content">
        <h1 class="page-title">数据导入中心</h1>
        <p class="page-subtitle">DATA IMPORT CENTER</p>
      </div>
    </header>

    <!-- Upload Section -->
    <section class="upload-section">
      <div class="section-header">
        <h2 class="section-title">
          <span class="section-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          文件上传
        </h2>
        <div class="dataset-type-selector">
          <el-select v-model="selectedDatasetType" placeholder="选择数据集类型" size="large">
            <el-option label="空气质量监测数据" value="air_quality_data" />
            <el-option label="省份数据" value="provinces" />
            <el-option label="城市数据" value="cities" />
            <el-option label="监测站点数据" value="stations" />
          </el-select>
        </div>
      </div>

      <div class="upload-area" :class="{ 'drag-over': isDragOver, 'uploading': uploading }"
           @drop.prevent="handleDrop"
           @dragover.prevent="isDragOver = true"
           @dragleave.prevent="isDragOver = false"
           @click="selectFile">
        <input ref="fileInputRef" type="file" accept=".csv,.xlsx,.xls" @change="handleFileSelect" style="display: none">

        <div class="upload-content" v-if="!selectedFile">
          <div class="upload-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3 class="upload-title">拖放文件到此处</h3>
          <p class="upload-desc">或点击选择文件（支持 CSV、Excel 格式）</p>
          <div class="upload-formats">
            <span class="format-tag">.CSV</span>
            <span class="format-tag">.XLSX</span>
            <span class="format-tag">.XLS</span>
          </div>
        </div>

        <div class="upload-preview" v-else>
          <div class="file-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="file-info">
            <div class="file-name">{{ selectedFile.name }}</div>
            <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
          </div>
          <button class="remove-file-btn" @click.stop="removeFile" :disabled="uploading">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M6 18L18 6M6 6l12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="upload-progress" v-if="uploading">
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
          </div>
          <span class="progress-text">{{ uploadProgress }}%</span>
        </div>
      </div>

      <div class="upload-actions">
        <button class="upload-btn" @click="handleUpload" :disabled="!selectedFile || uploading || !selectedDatasetType">
          <svg v-if="!uploading" viewBox="0 0 20 20" fill="none">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="uploading-icon" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/>
            <path d="M10 4v6l4 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          {{ uploading ? '导入中...' : '开始导入' }}
        </button>
      </div>
    </section>

    <!-- Import Tasks Section -->
    <section class="tasks-section">
      <div class="section-header">
        <h2 class="section-title">
          <span class="section-icon">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          导入任务历史
        </h2>
        <div class="section-actions">
          <el-button @click="fetchTasks" :icon="RefreshIcon" circle />
        </div>
      </div>

      <div class="tasks-table-container">
        <el-table :data="tasks" v-loading="tasksLoading" class="tasks-table" stripe>
          <el-table-column prop="task_id" label="任务ID" min-width="180">
            <template #default="{ row }">
              <span class="task-id">{{ row.task_id }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="file_name" label="文件名" min-width="200" />

          <el-table-column prop="file_type" label="类型" width="80">
            <template #default="{ row }">
              <span class="file-type-badge">{{ row.file_type.toUpperCase() }}</span>
            </template>
          </el-table-column>

          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <span class="status-badge" :class="getTaskStatusClass(row.status)">
                {{ getTaskStatusText(row.status) }}
              </span>
            </template>
          </el-table-column>

          <el-table-column label="统计" width="200">
            <template #default="{ row }">
              <div class="task-stats">
                <span class="stat-item total">{{ row.total_count }}</span>
                <span class="stat-item success">{{ row.success_count }}</span>
                <span class="stat-item failed" v-if="row.failed_count > 0">{{ row.failed_count }}</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="start_time" label="开始时间" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.start_time) }}
            </template>
          </el-table-column>

          <el-table-column label="用时" width="100">
            <template #default="{ row }">
              {{ calculateDuration(row) }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" link @click="viewTaskDetail(row)" size="small">
                详情
              </el-button>
              <el-button type="primary" link @click="viewTaskLogs(row)" size="small"
                         v-if="row.failed_count > 0">
                日志
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container" v-if="tasksTotal > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="tasksTotal"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="fetchTasks"
            @current-change="fetchTasks"
          />
        </div>
      </div>
    </section>

    <!-- Task Detail Dialog -->
    <el-dialog v-model="detailDialogVisible" title="导入任务详情" width="600px" class="detail-dialog">
      <div class="task-detail" v-if="selectedTask">
        <div class="detail-row">
          <span class="detail-label">任务ID</span>
          <span class="detail-value task-id-value">{{ selectedTask.task_id }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">文件名</span>
          <span class="detail-value">{{ selectedTask.file_name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">状态</span>
          <span class="status-badge detail-status" :class="getTaskStatusClass(selectedTask.status)">
            {{ getTaskStatusText(selectedTask.status) }}
          </span>
        </div>
        <div class="detail-stats">
          <div class="detail-stat-card">
            <span class="stat-label">总条数</span>
            <span class="stat-value">{{ selectedTask.total_count }}</span>
          </div>
          <div class="detail-stat-card success">
            <span class="stat-label">成功</span>
            <span class="stat-value">{{ selectedTask.success_count }}</span>
          </div>
          <div class="detail-stat-card error" v-if="selectedTask.failed_count > 0">
            <span class="stat-label">失败</span>
            <span class="stat-value">{{ selectedTask.failed_count }}</span>
          </div>
        </div>
        <div class="detail-row" v-if="selectedTask.start_time">
          <span class="detail-label">开始时间</span>
          <span class="detail-value">{{ formatDateTime(selectedTask.start_time) }}</span>
        </div>
        <div class="detail-row" v-if="selectedTask.end_time">
          <span class="detail-label">结束时间</span>
          <span class="detail-value">{{ formatDateTime(selectedTask.end_time) }}</span>
        </div>
        <div class="detail-row" v-if="selectedTask.end_time">
          <span class="detail-label">总耗时</span>
          <span class="detail-value">{{ calculateDuration(selectedTask) }}</span>
        </div>
      </div>
    </el-dialog>

    <!-- Task Logs Dialog -->
    <el-dialog v-model="logsDialogVisible" title="导入失败日志" width="800px" class="logs-dialog">
      <div class="logs-container" v-if="taskLogs.length > 0">
        <div class="logs-header">
          <span class="logs-count">共 {{ logsTotal }} 条失败记录</span>
          <el-button @click="exportLogs" size="small" :icon="DownloadIcon">导出日志</el-button>
        </div>
        <div class="logs-table">
          <div class="logs-table-header">
            <span class="log-col row-num">行号</span>
            <span class="log-col error">错误原因</span>
            <span class="log-col raw-data">原始数据</span>
          </div>
          <div class="logs-list">
            <div class="log-item" v-for="log in taskLogs" :key="log.id">
              <span class="log-col row-num">{{ log.row_number }}</span>
              <span class="log-col error">{{ log.error_reason }}</span>
              <span class="log-col raw-data">{{ log.raw_data_snippet }}</span>
            </div>
          </div>
        </div>
        <div class="logs-pagination" v-if="logsTotal > logsPageSize">
          <el-pagination
            v-model:current-page="logsCurrentPage"
            v-model:page-size="logsPageSize"
            :total="logsTotal"
            :page-sizes="[20, 50, 100]"
            layout="total, sizes, prev, pager, next"
            small
            @size-change="fetchTaskLogs"
            @current-change="fetchTaskLogs"
          />
        </div>
      </div>
      <el-empty v-else description="暂无失败日志" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh as RefreshIcon, Download as DownloadIcon } from '@element-plus/icons-vue'
import { uploadDataFile, getImportTasks, getImportTaskDetail, getImportTaskLogs } from '@/api/admin'

// State
const isDragOver = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const selectedFile = ref(null)
const selectedDatasetType = ref('air_quality_data')
const fileInputRef = ref(null)

const tasks = ref([])
const tasksLoading = ref(false)
const tasksTotal = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const detailDialogVisible = ref(false)
const logsDialogVisible = ref(false)
const selectedTask = ref(null)
const taskLogs = ref([])
const logsTotal = ref(0)
const logsCurrentPage = ref(1)
const logsPageSize = ref(50)

// Methods
const selectFile = () => {
  fileInputRef.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleDrop = (event) => {
  isDragOver.value = false
  const file = event.dataTransfer.files?.[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const validateAndSetFile = (file) => {
  const validTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
  const validExtensions = ['.csv', '.xlsx', '.xls']

  const fileExtension = '.' + file.name.split('.').pop().toLowerCase()

  if (!validExtensions.includes(fileExtension)) {
    ElMessage.error('仅支持 CSV、Excel 格式的文件')
    return
  }

  selectedFile.value = file
}

const removeFile = () => {
  selectedFile.value = null
  uploadProgress.value = 0
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const handleUpload = async () => {
  if (!selectedFile.value || !selectedDatasetType.value) {
    ElMessage.warning('请选择文件和数据集类型')
    return
  }

  uploading.value = true
  uploadProgress.value = 0

  // Simulate progress
  const progressInterval = setInterval(() => {
    if (uploadProgress.value < 90) {
      uploadProgress.value += Math.random() * 10
    }
  }, 200)

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await uploadDataFile(formData, selectedDatasetType.value)

    clearInterval(progressInterval)
    uploadProgress.value = 100

    if (response.code === 0) {
      ElMessage.success('文件上传成功，导入任务已创建')
      removeFile()
      fetchTasks()
    } else {
      throw new Error(response.message)
    }
  } catch (error) {
    clearInterval(progressInterval)
    ElMessage.error(error.message || '文件上传失败')
  } finally {
    uploading.value = false
    uploadProgress.value = 0
  }
}

const fetchTasks = async () => {
  tasksLoading.value = true
  try {
    const response = await getImportTasks({
      page: currentPage.value,
      page_size: pageSize.value
    })

    if (response.code === 0) {
      tasks.value = response.data
      tasksTotal.value = response.total
    }
  } catch (error) {
    ElMessage.error('获取任务列表失败')
  } finally {
    tasksLoading.value = false
  }
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

const getTaskStatusText = (status) => {
  const statusMap = {
    'SUCCESS': '成功',
    'FAILED': '失败',
    'RUNNING': '执行中',
    'PENDING': '等待中'
  }
  return statusMap[status] || '未知'
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const calculateDuration = (task) => {
  if (!task.start_time || !task.end_time) return '-'
  const start = new Date(task.start_time)
  const end = new Date(task.end_time)
  const diff = (end - start) / 1000
  if (diff < 60) return `${Math.round(diff)}秒`
  if (diff < 3600) return `${Math.round(diff / 60)}分钟`
  return `${Math.round(diff / 3600)}小时`
}

const viewTaskDetail = async (task) => {
  selectedTask.value = task
  detailDialogVisible.value = true
}

const viewTaskLogs = async (task) => {
  selectedTask.value = task
  logsDialogVisible.value = true
  logsCurrentPage.value = 1
  await fetchTaskLogs()
}

const fetchTaskLogs = async () => {
  if (!selectedTask.value) return

  try {
    const response = await getImportTaskLogs(selectedTask.value.task_id, {
      page: logsCurrentPage.value,
      page_size: logsPageSize.value
    })

    if (response.code === 0) {
      taskLogs.value = response.data
      logsTotal.value = response.total
    }
  } catch (error) {
    ElMessage.error('获取日志失败')
  }
}

const exportLogs = () => {
  // Export logs to CSV
  const headers = ['行号', '错误原因', '原始数据']
  const rows = taskLogs.value.map(log => [
    log.row_number,
    log.error_reason,
    log.raw_data_snippet || ''
  ])

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')

  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `import_logs_${selectedTask.value.task_id}.csv`
  link.click()
  URL.revokeObjectURL(url)

  ElMessage.success('日志导出成功')
}

// Lifecycle
onMounted(() => {
  fetchTasks()
  // Auto refresh tasks every 10 seconds
  setInterval(() => {
    if (!tasksLoading.value) {
      fetchTasks()
    }
  }, 10000)
})
</script>

<style scoped>
/* Container */
.data-import-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Header */
.import-header {
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 4px;
}

/* Section Common */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.section-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 211, 238, 0.1);
  border-radius: 8px;
  color: #22d3ee;
}

.section-icon svg {
  width: 14px;
  height: 14px;
}

.section-actions {
  display: flex;
  gap: 8px;
}

/* Upload Section */
.upload-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
}

.dataset-type-selector {
  width: 200px;
}

.upload-area {
  background: var(--bg-soft);
  border: 2px dashed var(--border);
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.upload-area:hover {
  border-color: var(--primary);
  background: rgba(34, 211, 238, 0.02);
}

.upload-area.drag-over {
  border-color: #22d3ee;
  background: rgba(34, 211, 238, 0.05);
}

.upload-area.uploading {
  pointer-events: none;
}

.upload-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border-radius: 16px;
  color: var(--text-muted);
}

.upload-icon svg {
  width: 28px;
  height: 28px;
}

.upload-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.upload-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.upload-formats {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.format-tag {
  padding: 4px 10px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  font-family: 'JetBrains Mono', monospace;
}

.upload-preview {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
}

.file-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 211, 238, 0.1);
  border-radius: 10px;
  color: #22d3ee;
  flex-shrink: 0;
}

.file-icon svg {
  width: 22px;
  height: 22px;
}

.file-info {
  flex: 1;
  text-align: left;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 4px;
  word-break: break-all;
}

.file-size {
  font-size: 12px;
  color: var(--text-muted);
}

.remove-file-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-soft);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s ease;
}

.remove-file-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.remove-file-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.remove-file-btn svg {
  width: 14px;
  height: 14px;
}

.upload-progress {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.progress-track {
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
  min-width: 45px;
  text-align: right;
}

.upload-actions {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: linear-gradient(135deg, #22d3ee 0%, #0891b2 100%);
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(34, 211, 238, 0.3);
}

.upload-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.upload-btn svg {
  width: 18px;
  height: 18px;
}

.uploading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Tasks Section */
.tasks-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
}

.tasks-table-container {
  min-height: 400px;
}

.tasks-table {
  width: 100%;
}

:deep(.el-table) {
  background: transparent;
  color: var(--text);
}

:deep(.el-table th.el-table__cell) {
  background: var(--bg-soft);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border);
}

:deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid var(--border);
}

:deep(.el-table tr:hover > td) {
  background: var(--bg-hover);
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: rgba(0, 0, 0, 0.02);
}

.task-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--text-secondary);
}

.file-type-badge {
  padding: 4px 8px;
  background: var(--bg-soft);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-secondary);
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-badge.failed {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.status-badge.running {
  background: rgba(34, 211, 238, 0.15);
  color: #22d3ee;
}

.status-badge.pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.task-stats {
  display: flex;
  gap: 8px;
}

.stat-item {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  font-feature-settings: 'tnum';
}

.stat-item.total {
  background: var(--bg-soft);
  color: var(--text-secondary);
}

.stat-item.success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.stat-item.failed {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

:deep(.el-pagination) {
  color: var(--text-secondary);
}

:deep(.el-pagination button) {
  background: var(--bg-card);
  color: var(--text-secondary);
  border-color: var(--border);
}

:deep(.el-pagination button:hover) {
  color: var(--primary);
}

:deep(.el-pagination .el-pager li) {
  background: var(--bg-card);
  color: var(--text-secondary);
  border-color: var(--border);
}

:deep(.el-pagination .el-pager li.is-active) {
  background: var(--primary);
  color: white;
}

/* Detail Dialog */
.task-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  color: var(--text-muted);
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}

.task-id-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin: 8px 0;
}

.detail-stat-card {
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
}

.detail-stat-card.success {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.03);
}

.detail-stat-card.error {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.03);
}

.detail-stat-card .stat-label {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.detail-stat-card .stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: var(--text);
  font-feature-settings: 'tnum';
}

.detail-status {
  padding: 6px 12px;
}

/* Logs Dialog */
.logs-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logs-count {
  font-size: 13px;
  color: var(--text-muted);
}

.logs-table {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.logs-table-header {
  display: grid;
  grid-template-columns: 80px 1fr 1fr;
  gap: 16px;
  padding: 12px 16px;
  background: var(--bg-soft);
  border-bottom: 1px solid var(--border);
}

.logs-table-header .log-col {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.logs-list {
  max-height: 400px;
  overflow-y: auto;
}

.log-item {
  display: grid;
  grid-template-columns: 80px 1fr 1fr;
  gap: 16px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  transition: background 0.2s ease;
}

.log-item:hover {
  background: var(--bg-hover);
}

.log-item:last-child {
  border-bottom: none;
}

.log-item .log-col {
  font-size: 13px;
  color: var(--text);
}

.log-item .log-col.row-num {
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-muted);
}

.log-item .log-col.error {
  color: #ef4444;
}

.log-item .log-col.raw-data {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logs-pagination {
  display: flex;
  justify-content: center;
}

/* Scrollbar */
.logs-list::-webkit-scrollbar {
  width: 6px;
}

.logs-list::-webkit-scrollbar-track {
  background: var(--bg-soft);
}

.logs-list::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
}

.logs-list::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}

/* Responsive */
@media (max-width: 768px) {
  .upload-area {
    padding: 32px 16px;
  }

  .upload-formats {
    flex-direction: column;
    align-items: center;
  }

  .detail-stats {
    grid-template-columns: 1fr;
  }

  .logs-table-header,
  .log-item {
    grid-template-columns: 60px 1fr;
  }

  .logs-table-header .log-col.raw-data,
  .log-item .log-col.raw-data {
    display: none;
  }
}
</style>
