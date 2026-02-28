<template>
  <div class="task-manager-page">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/>
              <rect x="9" y="3" width="6" height="4" rx="1"/>
              <path d="M9 14l2 2 4-4"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">任务管理</h1>
            <p class="page-subtitle">管理爬虫采集任务</p>
          </div>
        </div>
        <div class="header-actions">
          <button class="action-btn primary" @click="openCreateDialog">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            <span>创建任务</span>
          </button>
          <button class="action-btn refresh" @click="fetchTasks" :disabled="loading">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
              <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
              <path d="M16 21h5v-5"/>
            </svg>
            <span>刷新</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Task Stats -->
    <section class="stats-bar">
      <div class="stat-card">
        <div class="stat-icon pending">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ taskStats.pending }}</span>
          <span class="stat-label">待执行</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon running">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ taskStats.running }}</span>
          <span class="stat-label">执行中</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon paused">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="6" y="4" width="4" height="16"/>
            <rect x="14" y="4" width="4" height="16"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ taskStats.paused }}</span>
          <span class="stat-label">已暂停</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon completed">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ taskStats.completed }}</span>
          <span class="stat-label">已完成</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon failed">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ taskStats.failed }}</span>
          <span class="stat-label">失败</span>
        </div>
      </div>
    </section>

    <!-- Task Table -->
    <section class="task-table-section">
      <el-card class="task-table-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">任务列表</span>
            <span class="task-count">{{ tasks.length }} 个任务</span>
          </div>
        </template>

        <el-table
          v-loading="loading"
          :data="tasks"
          style="width: 100%"
          :row-key="row => row.id"
          empty-text="暂无任务"
        >
          <el-table-column prop="id" label="任务ID" width="80" align="center" />

          <el-table-column prop="name" label="任务名称" min-width="180">
            <template #default="{ row }">
              <div class="task-name-cell">
                <span class="task-name">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="config_name" label="配置文件" min-width="150">
            <template #default="{ row }">
              <span class="config-name">{{ row.config_name || row.config_name || '-' }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="status" label="状态" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" effect="light" round>
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="progress" label="进度" min-width="200" align="center">
            <template #default="{ row }">
              <div class="progress-cell">
                <el-progress
                  :percentage="calculateProgress(row)"
                  :status="getProgressStatus(row.status)"
                  :stroke-width="8"
                  :show-text="false"
                />
                <span class="progress-text">
                  {{ row.collected_count || 0 }} / {{ row.target_count || 0 }} 条
                </span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="created_at" label="创建时间" width="180" align="center">
            <template #default="{ row }">
              <span class="time-cell">{{ formatTime(row.created_at) }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="200" align="center" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <!-- 开始按钮 - pending 状态 -->
                <el-button
                  v-if="row.status === 'pending'"
                  type="primary"
                  size="small"
                  :loading="actionLoading[row.id]"
                  @click="handleStart(row.id)"
                >
                  开始
                </el-button>

                <!-- 暂停按钮 - running 状态 -->
                <el-button
                  v-if="row.status === 'running'"
                  type="warning"
                  size="small"
                  :loading="actionLoading[row.id]"
                  @click="handlePause(row.id)"
                >
                  暂停
                </el-button>

                <!-- 继续按钮 - paused 状态 -->
                <el-button
                  v-if="row.status === 'paused'"
                  type="success"
                  size="small"
                  :loading="actionLoading[row.id]"
                  @click="handleResume(row.id)"
                >
                  继续
                </el-button>

                <!-- 停止按钮 - running/paused 状态 -->
                <el-button
                  v-if="row.status === 'running' || row.status === 'paused'"
                  type="danger"
                  size="small"
                  :loading="actionLoading[row.id]"
                  @click="handleStop(row.id)"
                >
                  停止
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </section>

    <!-- Create Task Dialog -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建任务"
      width="500px"
      class="create-dialog"
      :close-on-click-modal="false"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        class="create-form"
        label-position="top"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input
            v-model="createForm.name"
            placeholder="请输入任务名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="选择配置文件" prop="config_id">
          <el-select
            v-model="createForm.config_id"
            placeholder="请选择配置文件"
            style="width: 100%"
          >
            <el-option
              v-for="config in configList"
              :key="config.id"
              :label="config.name"
              :value="config.id"
            >
              <div class="config-option">
                <span class="config-option-name">{{ config.name }}</span>
                <span class="config-option-desc">{{ config.description || '无描述' }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="createDialogVisible = false">取消</button>
          <button class="confirm-btn" :disabled="createLoading" @click="handleCreateTask">
            <span v-if="!createLoading">创建</span>
            <span v-else class="btn-loading">
              <span class="spinner"></span>
              创建中...
            </span>
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  listTasks,
  createTask,
  startTask,
  pauseTask,
  resumeTask,
  stopTask,
  listConfigs
} from '@/api/crawler'

// State
const loading = ref(false)
const createLoading = ref(false)
const createDialogVisible = ref(false)
const createFormRef = ref(null)
const tasks = ref([])
const configList = ref([])
const actionLoading = ref({})

const createForm = reactive({
  name: '',
  config_id: null
})

const createRules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 2, max: 50, message: '任务名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  config_id: [
    { required: true, message: '请选择配置文件', trigger: 'change' }
  ]
}

// Task stats computed
const taskStats = computed(() => {
  const stats = {
    pending: 0,
    running: 0,
    paused: 0,
    completed: 0,
    failed: 0
  }
  tasks.value.forEach(task => {
    if (stats.hasOwnProperty(task.status)) {
      stats[task.status]++
    }
  })
  return stats
})

// Methods
const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await listTasks()
    if (res.code === 0 || res.code === 200) {
      tasks.value = res.data || []
    } else {
      ElMessage.error(res.message || '获取任务列表失败')
    }
  } catch (e) {
    console.error('Failed to fetch tasks:', e)
    ElMessage.error('获取任务列表失败')
  } finally {
    loading.value = false
  }
}

const fetchConfigs = async () => {
  try {
    const res = await listConfigs()
    if (res.code === 0 || res.code === 200) {
      configList.value = res.data || []
    }
  } catch (e) {
    console.error('Failed to fetch configs:', e)
  }
}

const openCreateDialog = () => {
  createForm.name = ''
  createForm.config_id = null
  createDialogVisible.value = true
}

const handleCreateTask = async () => {
  if (!createFormRef.value) return

  try {
    await createFormRef.value.validate()
  } catch {
    return
  }

  createLoading.value = true
  try {
    const res = await createTask({
      name: createForm.name,
      config_id: createForm.config_id
    })
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('任务创建成功')
      createDialogVisible.value = false
      fetchTasks()
    } else {
      ElMessage.error(res.message || '创建任务失败')
    }
  } catch (e) {
    console.error('Failed to create task:', e)
    ElMessage.error('创建任务失败')
  } finally {
    createLoading.value = false
  }
}

const handleStart = async (taskId) => {
  actionLoading.value[taskId] = true
  try {
    const res = await startTask(taskId)
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('任务已开始')
      fetchTasks()
    } else {
      ElMessage.error(res.message || '启动任务失败')
    }
  } catch (e) {
    console.error('Failed to start task:', e)
    ElMessage.error('启动任务失败')
  } finally {
    actionLoading.value[taskId] = false
  }
}

const handlePause = async (taskId) => {
  actionLoading.value[taskId] = true
  try {
    const res = await pauseTask(taskId)
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('任务已暂停')
      fetchTasks()
    } else {
      ElMessage.error(res.message || '暂停任务失败')
    }
  } catch (e) {
    console.error('Failed to pause task:', e)
    ElMessage.error('暂停任务失败')
  } finally {
    actionLoading.value[taskId] = false
  }
}

const handleResume = async (taskId) => {
  actionLoading.value[taskId] = true
  try {
    const res = await resumeTask(taskId)
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('任务已继续')
      fetchTasks()
    } else {
      ElMessage.error(res.message || '继续任务失败')
    }
  } catch (e) {
    console.error('Failed to resume task:', e)
    ElMessage.error('继续任务失败')
  } finally {
    actionLoading.value[taskId] = false
  }
}

const handleStop = async (taskId) => {
  actionLoading.value[taskId] = true
  try {
    const res = await stopTask(taskId)
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('任务已停止')
      fetchTasks()
    } else {
      ElMessage.error(res.message || '停止任务失败')
    }
  } catch (e) {
    console.error('Failed to stop task:', e)
    ElMessage.error('停止任务失败')
  } finally {
    actionLoading.value[taskId] = false
  }
}

// Status helpers
const getStatusType = (status) => {
  const typeMap = {
    'pending': 'info',
    'running': 'primary',
    'paused': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    'pending': '待执行',
    'running': '执行中',
    'paused': '已暂停',
    'completed': '已完成',
    'failed': '失败'
  }
  return textMap[status] || status
}

const calculateProgress = (task) => {
  if (!task.target_count || task.target_count === 0) return 0
  return Math.min(100, Math.round((task.collected_count || 0) / task.target_count * 100))
}

const getProgressStatus = (status) => {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  return undefined
}

const formatTime = (time) => {
  if (!time) return '-'
  const date = new Date(time)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Polling for task status
let pollingTimer = null

const startPolling = () => {
  pollingTimer = setInterval(() => {
    fetchTasks()
  }, 5000)
}

const stopPolling = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
}

onMounted(() => {
  fetchTasks()
  fetchConfigs()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
/* Page Layout */
.task-manager-page {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.page-header {
  margin-bottom: 1.5rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(96, 165, 250, 0.12) 100%);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 16px;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: #3b82f6;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.page-title {
  font-family: 'Outfit', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* Action Buttons */
.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  font-size: 0.875rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-weight: 500;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: #fff;
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.action-btn.refresh {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #475569;
}

.action-btn.refresh:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

/* Stats Bar */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 1024px) {
  .stats-bar {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.stat-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.stat-icon svg {
  width: 22px;
  height: 22px;
}

.stat-icon.pending {
  background: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

.stat-icon.running {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.stat-icon.paused {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.stat-icon.completed {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.stat-icon.failed {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Task Table */
.task-table-section {
  margin-top: 1.5rem;
}

.task-table-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.task-table-card :deep(.el-card__header) {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.task-count {
  font-size: 0.8rem;
  color: #64748b;
}

.task-name-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.task-name {
  font-weight: 500;
  color: #1e293b;
}

.config-name {
  color: #64748b;
}

.progress-cell {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.progress-text {
  font-size: 0.75rem;
  color: #64748b;
}

.time-cell {
  font-size: 0.8rem;
  color: #64748b;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

/* Dialog Styles */
.create-dialog :deep(.el-dialog) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
}

.create-dialog :deep(.el-dialog__header) {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.create-dialog :deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.create-dialog :deep(.el-dialog__body) {
  padding: 1.5rem;
}

.create-form :deep(.el-form-item__label) {
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
}

.create-form :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
}

.create-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(59, 130, 246, 0.5);
}

.create-form :deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.create-form :deep(.el-select .el-input__wrapper) {
  border-radius: 10px;
}

.config-option {
  display: flex;
  flex-direction: column;
}

.config-option-name {
  font-weight: 500;
  color: #1e293b;
}

.config-option-desc {
  font-size: 0.75rem;
  color: #64748b;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
}

.cancel-btn,
.confirm-btn {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #475569;
}

.cancel-btn:hover {
  background: #f8fafc;
}

.confirm-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
  color: #fff;
  font-weight: 600;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 640px) {
  .task-manager-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .header-icon {
    width: 48px;
    height: 48px;
  }

  .header-icon svg {
    width: 24px;
    height: 24px;
  }

  .header-actions {
    flex-direction: column;
  }

  .action-btn {
    justify-content: center;
  }
}
</style>
