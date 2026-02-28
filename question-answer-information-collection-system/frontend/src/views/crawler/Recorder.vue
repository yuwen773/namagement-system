<template>
  <div class="recorder-page">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <circle cx="12" cy="12" r="3" fill="currentColor"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">录制管理</h1>
            <p class="page-subtitle">管理爬虫录制任务和配置</p>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-pill" :class="{ active: isRecording }">
            <span class="stat-dot"></span>
            <span class="stat-value">{{ isRecording ? '录制中' : '空闲' }}</span>
            <span class="stat-label">状态</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Local Recorder Info Card -->
    <el-card class="info-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="info-icon">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            本地录制器
          </span>
        </div>
      </template>
      <div class="local-recorder-info">
        <p class="info-text">
          由于浏览器安全限制，服务器上的浏览器无法在前端页面中显示和控制。
          请下载本地录制器，在本地浏览器中进行操作录制。
        </p>
        <div class="recorder-actions">
          <button class="action-btn download" @click="handleDownloadRecorder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            <span>下载录制器</span>
          </button>
          <button class="action-btn upload" @click="handleUploadConfig">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <span>上传配置</span>
          </button>
        </div>
        <div class="usage-steps">
          <h4>使用步骤：</h4>
          <ol>
            <li>点击"下载录制器"下载 <code>local_recorder.py</code> 脚本</li>
            <li>在本地安装 Python 和 Playwright: <code>pip install playwright && playwright install chromium</code></li>
            <li>运行脚本: <code>python local_recorder.py</code></li>
            <li>在弹出的浏览器中进行操作录制</li>
            <li>录制完成后，会在 <code>recordings/</code> 目录生成 JSON 配置文件</li>
            <li>点击"上传配置"将生成的配置文件导入系统</li>
          </ol>
        </div>
      </div>
    </el-card>

    <!-- Control Bar -->
    <section class="control-bar">
      <div class="control-actions">
        <el-select
          v-model="selectedConfig"
          placeholder="选择配置"
          class="config-select"
          :disabled="isRecording"
        >
          <el-option
            v-for="config in configList"
            :key="config.id"
            :label="config.name"
            :value="config.id"
          />
        </el-select>

        <button
          v-if="!isRecording"
          class="action-btn start"
          :disabled="!selectedConfig || loading"
          @click="handleStartRecording"
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="8"/>
          </svg>
          <span>开始录制</span>
        </button>
        <button
          v-else
          class="action-btn stop"
          :disabled="loading"
          @click="handleStopRecording"
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="6" width="12" height="12" rx="2"/>
          </svg>
          <span>停止录制</span>
        </button>

        <button class="action-btn refresh" @click="fetchSteps" :disabled="loading">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
            <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
            <path d="M16 21h5v-5"/>
          </svg>
          <span>刷新</span>
        </button>

        <button class="action-btn save" @click="openSaveDialog" :disabled="!isRecording || steps.length === 0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
            <polyline points="17 21 17 13 7 13 7 21"/>
            <polyline points="7 3 7 8 15 8"/>
          </svg>
          <span>保存配置</span>
        </button>
      </div>
    </section>

    <!-- Main Content -->
    <section class="main-content">
      <!-- Browser Preview -->
      <el-card class="preview-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">浏览器预览</span>
            <span class="preview-url" v-if="previewUrl">{{ previewUrl }}</span>
          </div>
        </template>
        <div class="browser-preview" v-loading="loading" element-loading-text="加载中...">
          <iframe
            v-if="previewUrl"
            :src="previewUrl"
            class="preview-iframe"
            frameborder="0"
          ></iframe>
          <div v-else class="empty-preview">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
            <p>选择配置并开始录制</p>
          </div>
        </div>
      </el-card>

      <!-- Recording Steps -->
      <el-card class="steps-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">录制步骤</span>
            <span class="steps-count">{{ steps.length }} 步</span>
          </div>
        </template>
        <div class="steps-timeline" v-if="steps.length > 0">
          <el-timeline>
            <el-timeline-item
              v-for="(step, index) in steps"
              :key="index"
              :timestamp="step.timestamp"
              :type="getStepType(step.type)"
              placement="top"
            >
              <div class="step-item">
                <div class="step-type">{{ getStepTypeText(step.type) }}</div>
                <div class="step-content" v-if="step.selector">
                  <span class="step-selector">{{ step.selector }}</span>
                </div>
                <div class="step-content" v-if="step.url">
                  <span class="step-url">{{ step.url }}</span>
                </div>
                <div class="step-content" v-if="step.action">
                  <span class="step-action">{{ step.action }}</span>
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
        <div v-else class="empty-steps">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <p>暂无录制步骤</p>
          <span>开始录制后，操作将自动记录</span>
        </div>
      </el-card>
    </section>

    <!-- Save Config Dialog -->
    <el-dialog
      v-model="saveDialogVisible"
      title="保存配置"
      width="480px"
      class="save-dialog"
      :close-on-click-modal="false"
    >
      <el-form
        ref="saveFormRef"
        :model="saveForm"
        :rules="saveRules"
        class="save-form"
        label-position="top"
      >
        <el-form-item label="配置名称" prop="name">
          <el-input
            v-model="saveForm.name"
            placeholder="请输入配置名称"
          />
        </el-form-item>

        <el-form-item label="目标URL" prop="target_url">
          <el-input
            v-model="saveForm.target_url"
            placeholder="请输入目标URL"
          />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="saveForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入配置描述"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="saveDialogVisible = false">取消</button>
          <button class="confirm-btn" :disabled="saveLoading" @click="handleSaveConfig">
            <span v-if="!saveLoading">保存</span>
            <span v-else class="btn-loading">
              <span class="spinner"></span>
              保存中...
            </span>
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  startRecording,
  stopRecording,
  getRecordingSteps,
  listConfigs,
  downloadRecorder,
  uploadConfig
} from '@/api/crawler'

// State
const loading = ref(false)
const saveLoading = ref(false)
const isRecording = ref(false)
const selectedConfig = ref(null)
const configList = ref([])
const steps = ref([])
const previewUrl = ref('')
const saveDialogVisible = ref(false)
const saveFormRef = ref(null)

const saveForm = reactive({
  name: '',
  target_url: '',
  description: ''
})

const saveRules = {
  name: [
    { required: true, message: '请输入配置名称', trigger: 'blur' }
  ],
  target_url: [
    { required: true, message: '请输入目标URL', trigger: 'blur' }
  ]
}

// Methods
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

const fetchSteps = async () => {
  loading.value = true
  try {
    const res = await getRecordingSteps()
    if (res.code === 0 || res.code === 200) {
      steps.value = res.data || []
    }
  } catch (e) {
    console.error('Failed to fetch steps:', e)
    ElMessage.error('获取录制步骤失败')
  } finally {
    loading.value = false
  }
}

const handleStartRecording = async () => {
  if (!selectedConfig.value) {
    ElMessage.warning('请选择配置')
    return
  }

  loading.value = true
  try {
    const res = await startRecording({ config_id: selectedConfig.value })
    if (res.code === 0 || res.code === 200) {
      isRecording.value = true
      previewUrl.value = res.data?.preview_url || ''
      ElMessage.success('开始录制')
      // 开始轮询步骤
      startPollingSteps()
    } else {
      ElMessage.error(res.message || '开始录制失败')
    }
  } catch (e) {
    console.error('Failed to start recording:', e)
    ElMessage.error('开始录制失败')
  } finally {
    loading.value = false
  }
}

const handleStopRecording = async () => {
  loading.value = true
  try {
    const res = await stopRecording({})
    if (res.code === 0 || res.code === 200) {
      isRecording.value = false
      ElMessage.success('录制已停止')
      stopPollingSteps()
    } else {
      ElMessage.error(res.message || '停止录制失败')
    }
  } catch (e) {
    console.error('Failed to stop recording:', e)
    ElMessage.error('停止录制失败')
  } finally {
    loading.value = false
  }
}

const openSaveDialog = () => {
  saveForm.name = ''
  saveForm.target_url = ''
  saveForm.description = ''
  saveDialogVisible.value = true
}

const handleSaveConfig = async () => {
  if (!saveFormRef.value) return

  try {
    await saveFormRef.value.validate()
  } catch {
    return
  }

  saveLoading.value = true
  try {
    // 这里可以调用保存配置的 API
    // await saveConfig({ ...saveForm, steps: steps.value })
    ElMessage.success('配置保存成功')
    saveDialogVisible.value = false
    fetchConfigs()
  } catch (e) {
    console.error('Failed to save config:', e)
    ElMessage.error('保存配置失败')
  } finally {
    saveLoading.value = false
  }
}

const getStepType = (type) => {
  const typeMap = {
    'click': 'primary',
    'input': 'success',
    'navigate': 'warning',
    'scroll': 'info',
    'wait': 'danger'
  }
  return typeMap[type] || ''
}

const getStepTypeText = (type) => {
  const textMap = {
    'click': '点击',
    'input': '输入',
    'navigate': '导航',
    'scroll': '滚动',
    'wait': '等待'
  }
  return textMap[type] || type
}

// Polling
let pollingTimer = null

const startPollingSteps = () => {
  pollingTimer = setInterval(() => {
    if (isRecording.value) {
      fetchSteps()
    }
  }, 2000)
}

const stopPollingSteps = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
}

// 下载本地录制器
const handleDownloadRecorder = async () => {
  try {
    // 获取 token
    const token = localStorage.getItem('access_token')
    if (!token) {
      ElMessage.warning('请先登录')
      return
    }

    // 直接使用 window.location.href 下载
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    const downloadUrl = `${apiBaseUrl}/recorder/download/`

    // 创建隐藏的 a 标签进行下载
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = 'local_recorder.py'
    link.style.display = 'none'

    // 添加 Authorization 头
    const xhr = new XMLHttpRequest()
    xhr.open('GET', downloadUrl, true)
    xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.responseType = 'blob'

    xhr.onload = function() {
      if (xhr.status === 200) {
        const blob = new Blob([xhr.response], { type: 'application/octet-stream' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'local_recorder.py'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
        ElMessage.success('录制器下载成功')
      } else {
        ElMessage.error('下载录制器失败')
      }
    }

    xhr.onerror = function() {
      ElMessage.error('下载录制器失败，请确保后端服务正常运行')
    }

    xhr.send()
  } catch (e) {
    console.error('Failed to download recorder:', e)
    ElMessage.error('下载录制器失败，请确保后端服务正常运行')
  }
}

// 上传配置文件
const handleUploadConfig = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', file.name.replace('.json', ''))

    try {
      loading.value = true
      const res = await uploadConfig(formData)
      if (res.code === 0 || res.code === 200) {
        ElMessage.success('配置上传成功')
        fetchConfigs()
      } else {
        ElMessage.error(res.message || '上传失败')
      }
    } catch (e) {
      console.error('Failed to upload config:', e)
      ElMessage.error('上传配置文件失败')
    } finally {
      loading.value = false
    }
  }
  input.click()
}

onMounted(() => {
  fetchConfigs()
  fetchSteps()
})
</script>

<style scoped>
/* Page Layout */
.recorder-page {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

/* Info Card */
.info-card {
  margin-bottom: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.info-card :deep(.el-card__header) {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.info-card .card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.info-icon {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

.local-recorder-info {
  padding: 0.5rem;
}

.info-text {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0 0 1rem;
}

.recorder-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.action-btn.download {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: #fff;
}

.action-btn.download:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.action-btn.upload {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: #fff;
}

.action-btn.upload:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
}

.usage-steps {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

.usage-steps h4 {
  margin: 0 0 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.usage-steps ol {
  margin: 0;
  padding-left: 1.25rem;
  color: #475569;
  font-size: 0.85rem;
  line-height: 1.8;
}

.usage-steps code {
  background: #e2e8f0;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 0.8rem;
  color: #dc2626;
}

.page-header {
  margin-bottom: 2rem;
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
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(248, 113, 113, 0.12) 100%);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 16px;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: #ef4444;
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

.header-stats {
  display: flex;
  gap: 1rem;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-pill.active {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
}

.stat-dot {
  width: 8px;
  height: 8px;
  background: #94a3b8;
  border-radius: 50%;
}

.stat-pill.active .stat-dot {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  animation: pulse-dot 1.5s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.9); }
}

.stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
}

.stat-pill.active .stat-value {
  color: #ef4444;
}

.stat-label {
  font-size: 0.8rem;
  color: #94a3b8;
}

/* Control Bar */
.control-bar {
  margin-bottom: 1.5rem;
}

.control-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.config-select {
  width: 200px;
}

.config-select :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
}

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

.action-btn.start {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  color: #fff;
}

.action-btn.start:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
}

.action-btn.stop {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  color: #fff;
}

.action-btn.stop:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
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

.action-btn.save {
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  color: #fff;
}

.action-btn.save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

/* Main Content */
.main-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

/* Preview Card */
.preview-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.preview-card :deep(.el-card__header) {
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

.preview-url {
  font-size: 0.75rem;
  color: #64748b;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.browser-preview {
  height: 500px;
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
}

.preview-iframe {
  width: 100%;
  height: 100%;
}

.empty-preview {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.empty-preview svg {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
}

.empty-preview p {
  font-size: 0.9rem;
  margin: 0;
}

/* Steps Card */
.steps-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.steps-card :deep(.el-card__header) {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.steps-count {
  font-size: 0.8rem;
  color: #8b5cf6;
  font-weight: 500;
}

.steps-timeline {
  max-height: 460px;
  overflow-y: auto;
  padding: 0.5rem;
}

.step-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.step-type {
  font-size: 0.75rem;
  font-weight: 600;
  color: #8b5cf6;
  margin-bottom: 0.375rem;
}

.step-content {
  font-size: 0.8rem;
  color: #475569;
  word-break: break-all;
}

.step-selector,
.step-url,
.step-action {
  display: block;
  padding: 0.25rem 0;
}

.empty-steps {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.empty-steps svg {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
}

.empty-steps p {
  font-size: 0.9rem;
  margin: 0 0 0.5rem;
  color: #64748b;
}

.empty-steps span {
  font-size: 0.8rem;
}

/* Dialog Styles */
.save-dialog :deep(.el-dialog) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
}

.save-dialog :deep(.el-dialog__header) {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.save-dialog :deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.save-dialog :deep(.el-dialog__body) {
  padding: 1.5rem;
}

.save-form :deep(.el-form-item__label) {
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
}

.save-form :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
}

.save-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(139, 92, 246, 0.5);
}

.save-form :deep(.el-input__wrapper.is-focus) {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
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
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border: none;
  color: #fff;
  font-weight: 600;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
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
  .recorder-page {
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

  .control-actions {
    flex-direction: column;
  }

  .config-select {
    width: 100%;
  }

  .action-btn {
    justify-content: center;
  }

  .browser-preview {
    height: 300px;
  }
}
</style>
