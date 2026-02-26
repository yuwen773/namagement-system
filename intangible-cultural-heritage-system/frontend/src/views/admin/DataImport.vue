<template>
  <div class="data-import">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">数据导入</h1>
        <p class="page-subtitle">批量导入非物质文化遗产数据</p>
      </div>
    </div>

    <!-- Tabs -->
    <el-tabs v-model="activeTab" class="import-tabs">
      <!-- Upload Tab -->
      <el-tab-pane label="文件上传" name="upload">
        <div class="upload-section">
          <!-- Instructions -->
          <el-alert
            title="导入说明"
            type="info"
            :closable="false"
            class="import-alert"
          >
            <template #default>
              <ul class="instruction-list">
                <li>支持 Excel (.xlsx) 和 CSV (.csv) 格式文件</li>
                <li>文件大小不超过 10MB</li>
                <li>必需字段：项目名称、分类、级别、国家</li>
                <li>系统将自动清洗数据、标准化国家名称、补全经纬度</li>
                <li>导入失败的数据可在导入记录中下载错误报告</li>
              </ul>
            </template>
          </el-alert>

          <!-- Upload Area -->
          <div class="upload-area">
            <el-upload
              ref="uploadRef"
              class="upload-dragger"
              drag
              :auto-upload="false"
              :limit="1"
              :on-change="handleFileChange"
              :on-exceed="handleExceed"
              accept=".xlsx,.csv"
            >
              <el-icon class="upload-icon"><UploadFilled /></el-icon>
              <div class="upload-text">
                <p class="upload-title">点击或拖拽文件到此处上传</p>
                <p class="upload-hint">支持 .xlsx 和 .csv 格式</p>
              </div>
            </el-upload>
          </div>

          <!-- File Info -->
          <div v-if="selectedFile" class="file-info">
            <div class="file-card">
              <el-icon class="file-icon"><Document /></el-icon>
              <div class="file-details">
                <p class="file-name">{{ selectedFile.name }}</p>
                <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <el-button link type="danger" @click="clearFile">
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
          </div>

          <!-- Preview (placeholder for future enhancement) -->
          <div v-if="previewData.length > 0" class="preview-section">
            <h3 class="preview-title">数据预览（前10行）</h3>
            <el-table :data="previewData" stripe max-height="400">
              <el-table-column
                v-for="(col, index) in previewColumns"
                :key="index"
                :prop="col"
                :label="col"
                min-width="150"
              />
            </el-table>
          </div>

          <!-- Actions -->
          <div class="action-buttons">
            <el-button
              type="primary"
              size="large"
              :disabled="!selectedFile"
              :loading="importing"
              @click="handleImport"
            >
              <el-icon><Upload /></el-icon>
              <span>{{ importing ? '导入中...' : '开始导入' }}</span>
            </el-button>
            <el-button size="large" @click="clearFile" :disabled="importing">
              清空
            </el-button>
          </div>

          <!-- Progress -->
          <div v-if="importing" class="progress-section">
            <el-progress :percentage="importProgress" :status="progressStatus" />
            <p class="progress-text">{{ progressText }}</p>
          </div>

          <!-- Result -->
          <div v-if="importResult" class="result-section">
            <el-result
              :icon="importResult.success ? 'success' : 'warning'"
              :title="importResult.title"
              :sub-title="importResult.subtitle"
            >
              <template #extra>
                <div class="result-stats">
                  <div class="stat-item success">
                    <span class="stat-label">成功</span>
                    <span class="stat-value">{{ importResult.successCount }}</span>
                  </div>
                  <div class="stat-item error">
                    <span class="stat-label">失败</span>
                    <span class="stat-value">{{ importResult.errorCount }}</span>
                  </div>
                  <div class="stat-item total">
                    <span class="stat-label">总计</span>
                    <span class="stat-value">{{ importResult.totalCount }}</span>
                  </div>
                </div>
                <el-button type="primary" @click="resetImport">继续导入</el-button>
                <el-button @click="activeTab = 'history'">查看导入记录</el-button>
              </template>
            </el-result>
          </div>
        </div>
      </el-tab-pane>

      <!-- History Tab -->
      <el-tab-pane label="导入记录" name="history">
        <div class="history-section">
          <!-- Filters -->
          <div class="filter-bar">
            <el-select v-model="historyFilter" placeholder="筛选状态" clearable style="width: 200px">
              <el-option label="全部" value="" />
              <el-option label="处理中" value="processing" />
              <el-option label="已完成" value="completed" />
              <el-option label="失败" value="failed" />
            </el-select>
            <el-button type="primary" @click="fetchHistory">刷新</el-button>
          </div>

          <!-- History Table -->
          <el-table :data="historyData" v-loading="historyLoading" stripe class="history-table">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="file_name" label="文件名" min-width="200" />
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="总行数" width="100">
              <template #default="{ row }">
                {{ row.total_rows || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="成功" width="100">
              <template #default="{ row }">
                <span class="success-text">{{ row.success_count || 0 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="失败" width="100">
              <template #default="{ row }">
                <span class="error-text">{{ row.error_count || 0 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button
                  link
                  type="primary"
                  :disabled="!row.error_count || row.error_count === 0"
                  @click="downloadErrors(row)"
                >
                  下载错误
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Pagination -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="historyPage"
              :page-size="20"
              :total="historyTotal"
              layout="total, prev, pager, next, jumper"
              @current-change="fetchHistory"
            />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, type UploadInstance, type UploadFile } from 'element-plus'
import { UploadFilled, Document, Close, Upload } from '@element-plus/icons-vue'

// Note: Import APIs would be implemented when backend endpoints are ready
// For now, this is a complete UI implementation

// State
const activeTab = ref('upload')
const uploadRef = ref<UploadInstance>()
const selectedFile = ref<File | null>(null)
const importing = ref(false)
const importProgress = ref(0)
const progressStatus = ref<'success' | 'exception' | 'warning' | undefined>(undefined)
const progressText = ref('')
const previewData = ref<any[]>([])
const previewColumns = ref<string[]>([])
const historyLoading = ref(false)
const historyPage = ref(1)
const historyTotal = ref(0)
const historyFilter = ref('')
const historyData = ref<any[]>([])

// Import result
const importResult = ref<{
  success: boolean
  title: string
  subtitle: string
  successCount: number
  errorCount: number
  totalCount: number
} | null>(null)

// Methods
const handleFileChange = (file: UploadFile) => {
  if (file.raw) {
    selectedFile.value = file.raw
    // In real implementation, parse and preview file here
    ElMessage.success('文件已选择')
  }
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

const clearFile = () => {
  selectedFile.value = null
  previewData.value = []
  previewColumns.value = []
  uploadRef.value?.clearFiles()
  importResult.value = null
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const handleImport = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  importing.value = true
  importProgress.value = 0
  progressStatus.value = undefined
  progressText.value = '正在上传文件...'

  try {
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      if (importProgress.value < 30) {
        importProgress.value += 10
        progressText.value = '正在上传文件...'
      } else if (importProgress.value < 60) {
        importProgress.value += 5
        progressText.value = '正在解析数据...'
      } else if (importProgress.value < 90) {
        importProgress.value += 5
        progressText.value = '正在导入数据...'
      }
    }, 500)

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 5000))
    
    clearInterval(progressInterval)
    importProgress.value = 100
    progressStatus.value = 'success'
    progressText.value = '导入完成！'

    // Mock result
    importResult.value = {
      success: true,
      title: '导入完成',
      subtitle: '数据已成功导入系统',
      successCount: 950,
      errorCount: 50,
      totalCount: 1000
    }

    ElMessage.success('导入成功')
  } catch (error) {
    importProgress.value = 100
    progressStatus.value = 'exception'
    progressText.value = '导入失败'
    
    importResult.value = {
      success: false,
      title: '导入失败',
      subtitle: '请检查文件格式或联系管理员',
      successCount: 0,
      errorCount: 0,
      totalCount: 0
    }
    
    ElMessage.error('导入失败')
  } finally {
    importing.value = false
  }
}

const resetImport = () => {
  clearFile()
  importProgress.value = 0
  progressStatus.value = undefined
  progressText.value = ''
}

const fetchHistory = async () => {
  historyLoading.value = true
  try {
    // Mock data - replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    historyData.value = [
      {
        id: 1,
        file_name: 'heritage_data_2026.xlsx',
        status: 'completed',
        total_rows: 1000,
        success_count: 950,
        error_count: 50,
        created_at: '2026-02-26T10:00:00Z'
      },
      {
        id: 2,
        file_name: 'inheritors_data.csv',
        status: 'completed',
        total_rows: 500,
        success_count: 500,
        error_count: 0,
        created_at: '2026-02-25T15:30:00Z'
      },
      {
        id: 3,
        file_name: 'test_import.xlsx',
        status: 'failed',
        total_rows: 100,
        success_count: 0,
        error_count: 100,
        created_at: '2026-02-24T09:15:00Z'
      }
    ]
    
    historyTotal.value = 3
  } catch (error) {
    ElMessage.error('获取导入记录失败')
  } finally {
    historyLoading.value = false
  }
}

const downloadErrors = (row: any) => {
  // Mock download - replace with actual API call
  ElMessage.info(`正在下载 ${row.file_name} 的错误报告...`)
  
  // In real implementation:
  // const url = `/api/v1/importer/jobs/${row.id}/errors/`
  // window.open(url, '_blank')
}

const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    pending: 'info',
    processing: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// Lifecycle
onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.data-import {
  padding: 24px;
  background: linear-gradient(135deg, #f5f1ed 0%, #faf8f5 100%);
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 32px;
  padding: 32px;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(139, 69, 19, 0.2);
}

.header-content {
  color: white;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  letter-spacing: 1px;
}

.page-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
}

.import-tabs {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.upload-section {
  padding: 24px 0;
}

.import-alert {
  margin-bottom: 32px;
}

.instruction-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
  line-height: 1.8;
}

.upload-area {
  margin-bottom: 32px;
}

.upload-dragger {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 240px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #d4a574;
  border-radius: 12px;
  background: #faf8f5;
  transition: all 0.3s ease;
}

:deep(.el-upload-dragger:hover) {
  border-color: #8b4513;
  background: #f5f1ed;
}

.upload-icon {
  font-size: 64px;
  color: #8b4513;
  margin-bottom: 16px;
}

.upload-text {
  text-align: center;
}

.upload-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.upload-hint {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.file-info {
  margin-bottom: 32px;
}

.file-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f5f2;
  border-radius: 12px;
  border: 1px solid #e8e3dd;
}

.file-icon {
  font-size: 32px;
  color: #8b4513;
}

.file-details {
  flex: 1;
}

.file-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.file-size {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.preview-section {
  margin-bottom: 32px;
}

.preview-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 32px;
}

.progress-section {
  max-width: 600px;
  margin: 0 auto 32px;
}

.progress-text {
  text-align: center;
  margin-top: 12px;
  color: #666;
  font-size: 14px;
}

.result-section {
  margin-top: 32px;
}

.result-stats {
  display: flex;
  gap: 32px;
  justify-content: center;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
  padding: 20px 32px;
  border-radius: 12px;
  background: #f8f5f2;
}

.stat-item.success {
  background: #f0f9ff;
  border: 2px solid #67c23a;
}

.stat-item.error {
  background: #fef0f0;
  border: 2px solid #f56c6c;
}

.stat-item.total {
  background: #f4f4f5;
  border: 2px solid #909399;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #333;
}

.history-section {
  padding: 24px 0;
}

.filter-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.history-table {
  margin-bottom: 24px;
}

.success-text {
  color: #67c23a;
  font-weight: 600;
}

.error-text {
  color: #f56c6c;
  font-weight: 600;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

:deep(.el-table th) {
  background: #f8f5f2;
  color: #8b4513;
  font-weight: 600;
}

:deep(.el-table__row:hover) {
  background: #faf8f5;
}

:deep(.el-button--primary) {
  background: #8b4513;
  border-color: #8b4513;
}

:deep(.el-button--primary:hover) {
  background: #a0522d;
  border-color: #a0522d;
}

:deep(.el-tabs__item.is-active) {
  color: #8b4513;
}

:deep(.el-tabs__active-bar) {
  background-color: #8b4513;
}
</style>
