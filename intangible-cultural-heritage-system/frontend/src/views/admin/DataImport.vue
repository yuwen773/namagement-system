<template>
  <div class="data-import">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-seal">
          <span class="seal-text">导入</span>
        </div>
        <div class="header-texts">
          <h1 class="page-title">数据导入</h1>
          <p class="page-subtitle">批量导入非物质文化遗产数据</p>
        </div>
      </div>
    </header>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab" class="import-tabs">
      <!-- 上传标签页 -->
      <el-tab-pane label="文件上传" name="upload">
        <div class="upload-section">
          <!-- 说明区域 -->
          <div class="instruction-scroll">
            <div class="scroll-header">
              <span class="scroll-title">导入说明</span>
            </div>
            <div class="scroll-body">
              <ul class="instruction-list">
                <li>支持 Excel (.xlsx) 和 CSV (.csv) 格式文件</li>
                <li>文件大小不超过 10MB</li>
                <li>必需字段：项目名称、分类、级别、国家</li>
                <li>系统将自动清洗数据、标准化国家名称、补全经纬度</li>
                <li>导入失败的数据可在导入记录中下载错误报告</li>
              </ul>
            </div>
          </div>

          <!-- 上传区域 -->
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
              <div class="upload-icon">
                <el-icon><UploadFilled /></el-icon>
              </div>
              <div class="upload-text">
                <p class="upload-title">点击或拖拽文件到此处上传</p>
                <p class="upload-hint">支持 .xlsx 和 .csv 格式</p>
              </div>
            </el-upload>
          </div>

          <!-- 文件信息 -->
          <div v-if="selectedFile" class="file-info">
            <div class="file-card">
              <div class="file-seal">档</div>
              <div class="file-details">
                <p class="file-name">{{ selectedFile.name }}</p>
                <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <button class="file-clear" @click="clearFile">
                <el-icon><Close /></el-icon>
              </button>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-buttons">
            <button
              class="import-btn"
              :disabled="!selectedFile || importing"
              :class="{ loading: importing }"
              @click="handleImport"
            >
              <span v-if="!importing">开始导入</span>
              <span v-else class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </span>
            </button>
            <button class="clear-btn" @click="clearFile" :disabled="importing">
              清空
            </button>
          </div>

          <!-- 进度 -->
          <div v-if="importing" class="progress-section">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: importProgress + '%' }"></div>
            </div>
            <p class="progress-text">{{ progressText }}</p>
          </div>

          <!-- 结果 -->
          <div v-if="importResult" class="result-section">
            <div class="result-icon" :class="{ success: importResult.success }">
              <span>{{ importResult.success ? '成' : '败' }}</span>
            </div>
            <h3 class="result-title">{{ importResult.title }}</h3>
            <p class="result-subtitle">{{ importResult.subtitle }}</p>
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
            <div class="result-actions">
              <button class="result-btn primary" @click="resetImport">继续导入</button>
              <button class="result-btn" @click="activeTab = 'history'">查看导入记录</button>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- 历史记录标签页 -->
      <el-tab-pane label="导入记录" name="history">
        <div class="history-section">
          <!-- 筛选栏 -->
          <div class="filter-bar">
            <el-select v-model="historyFilter" placeholder="筛选状态" clearable class="filter-select">
              <el-option label="全部" value="" />
              <el-option label="处理中" value="processing" />
              <el-option label="已完成" value="completed" />
              <el-option label="失败" value="failed" />
            </el-select>
            <button class="refresh-btn" @click="fetchHistory">
              <el-icon><Refresh /></el-icon>
              <span>刷新</span>
            </button>
          </div>

          <!-- 历史表格 -->
          <el-table :data="historyData" v-loading="historyLoading" class="history-table">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="file_name" label="文件名" min-width="200" />
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <span class="status-badge" :class="getStatusClass(row.status)">
                  {{ getStatusText(row.status) }}
                </span>
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
                <button
                  class="table-download-btn"
                  :disabled="!row.error_count || row.error_count === 0"
                  @click="downloadErrors(row)"
                >
                  下载错误
                </button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
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
import { UploadFilled, Document, Close, Upload, Refresh } from '@element-plus/icons-vue'

// State
const activeTab = ref('upload')
const uploadRef = ref<UploadInstance>()
const selectedFile = ref<File | null>(null)
const importing = ref(false)
const importProgress = ref(0)
const progressText = ref('')
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
    ElMessage.success('文件已选择')
  }
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

const clearFile = () => {
  selectedFile.value = null
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
  progressText.value = '正在上传文件...'

  try {
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

    await new Promise(resolve => setTimeout(resolve, 5000))

    clearInterval(progressInterval)
    importProgress.value = 100
    progressText.value = '导入完成！'

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
  progressText.value = ''
}

const fetchHistory = async () => {
  historyLoading.value = true
  try {
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
  ElMessage.info(`正在下载 ${row.file_name} 的错误报告...`)
}

const getStatusClass = (status: string) => {
  return `status-${status}`
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
  background: #F7F4ED;
  min-height: calc(100vh - 60px);
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #5D8AA8 0%, #4a7a9e 100%);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(93, 138, 168, 0.3);
}

.header-seal {
  width: 56px;
  height: 56px;
  background: #D4AF37;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.seal-text {
  font-size: 20px;
  font-weight: 700;
  color: #2F3640;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 2px;
}

.header-texts {
  color: white;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
}

.page-subtitle {
  font-size: 13px;
  margin: 0;
  opacity: 0.9;
}

/* ========== 标签页 ========== */
.import-tabs {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

:deep(.import-tabs .el-tabs__item.is-active) {
  color: #5D8AA8;
}

:deep(.import-tabs .el-tabs__active-bar) {
  background-color: #5D8AA8;
}

/* ========== 上传区域 ========== */
.upload-section {
  padding: 24px 0;
}

.instruction-scroll {
  margin-bottom: 32px;
}

.scroll-header {
  background: linear-gradient(135deg, #5D8AA8 0%, #4a7a9e 100%);
  padding: 12px 20px;
  border-radius: 8px 8px 0 0;
}

.scroll-title {
  font-size: 16px;
  font-weight: 600;
  color: white;
  letter-spacing: 2px;
  font-family: "STSong", "SimSun", serif;
}

.scroll-body {
  background: #F7F4ED;
  padding: 20px;
  border-radius: 0 0 8px 8px;
}

.instruction-list {
  margin: 0;
  padding-left: 24px;
  line-height: 2;
}

.instruction-list li {
  color: #606266;
}

.upload-area {
  margin-bottom: 32px;
}

:deep(.upload-dragger) {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 240px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #5D8AA8;
  border-radius: 12px;
  background: #F7F4ED;
  transition: all 0.3s ease;
}

:deep(.el-upload-dragger:hover) {
  border-color: #4a7a9e;
  background: #EDF2ED;
}

.upload-icon {
  font-size: 64px;
  color: #5D8AA8;
  margin-bottom: 16px;
}

.upload-text {
  text-align: center;
}

.upload-title {
  font-size: 18px;
  font-weight: 600;
  color: #2F3640;
  margin: 0 0 8px 0;
}

.upload-hint {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* ========== 文件信息 ========== */
.file-info {
  margin-bottom: 32px;
}

.file-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid rgba(93, 138, 168, 0.2);
  box-shadow: 0 2px 8px rgba(93, 138, 168, 0.1);
}

.file-seal {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #5D8AA8;
  color: white;
  font-size: 18px;
  font-weight: 600;
  border-radius: 4px;
  font-family: "STSong", "SimSun", serif;
  flex-shrink: 0;
}

.file-details {
  flex: 1;
}

.file-name {
  font-size: 16px;
  font-weight: 600;
  color: #2F3640;
  margin: 0 0 4px 0;
}

.file-size {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.file-clear {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
}

.file-clear:hover {
  background: #C23531;
  color: white;
}

/* ========== 操作按钮 ========== */
.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 32px;
}

.import-btn {
  padding: 14px 40px;
  background: linear-gradient(135deg, #5D8AA8 0%, #4a7a9e 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(93, 138, 168, 0.3);
}

.import-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(93, 138, 168, 0.4);
}

.import-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.import-btn.loading .loading-dots {
  display: flex;
  gap: 4px;
}

.import-btn.loading .loading-dots span {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: dotBounce 1.4s ease-in-out infinite;
}

.import-btn.loading .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.import-btn.loading .loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBounce {
  0%, 80%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  40% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.clear-btn {
  padding: 14px 32px;
  background: white;
  color: #606266;
  border: 1px solid #DCDFE6;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.clear-btn:hover:not(:disabled) {
  background: #F7F4ED;
  border-color: #C0C4CC;
}

/* ========== 进度条 ========== */
.progress-section {
  max-width: 600px;
  margin: 0 auto 32px;
}

.progress-bar {
  height: 8px;
  background: #E4E7ED;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #5D8AA8, #4a7a9e);
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  color: #606266;
  font-size: 14px;
  margin: 0;
}

/* ========== 结果区域 ========== */
.result-section {
  text-align: center;
  padding: 40px 20px;
}

.result-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(194, 35, 49, 0.1);
  border-radius: 50%;
}

.result-icon.success {
  background: rgba(103, 194, 58, 0.1);
}

.result-icon span {
  font-size: 36px;
  font-weight: 700;
  font-family: "STSong", "SimSun", serif;
}

.result-icon:not(.success) span {
  color: #C23531;
}

.result-icon.success span {
  color: #67C23A;
}

.result-title {
  font-size: 24px;
  font-weight: 600;
  color: #2F3640;
  margin: 0 0 8px 0;
  font-family: "STSong", "SimSun", serif;
}

.result-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0 0 32px 0;
}

.result-stats {
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-bottom: 32px;
}

.stat-item {
  text-align: center;
  padding: 20px 32px;
  border-radius: 12px;
  min-width: 120px;
}

.stat-item.success {
  background: rgba(103, 194, 58, 0.1);
  border: 2px solid #67C23A;
}

.stat-item.error {
  background: rgba(194, 35, 49, 0.1);
  border: 2px solid #C23531;
}

.stat-item.total {
  background: rgba(144, 147, 153, 0.1);
  border: 2px solid #909399;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #2F3640;
}

.result-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.result-btn {
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.result-btn.primary {
  background: #5D8AA8;
  color: white;
}

.result-btn.primary:hover {
  background: #4a7a9e;
}

.result-btn:not(.primary) {
  background: white;
  color: #606266;
  border: 1px solid #DCDFE6;
}

.result-btn:not(.primary):hover {
  background: #F7F4ED;
}

/* ========== 历史记录 ========== */
.history-section {
  padding: 24px 0;
}

.filter-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.filter-select {
  width: 200px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #5D8AA8;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background: #4a7a9e;
}

.history-table {
  margin-bottom: 24px;
}

:deep(.history-table th) {
  background: #F7F4ED !important;
  color: #2F3640 !important;
  font-weight: 600 !important;
}

:deep(.history-table tr:hover) {
  background: rgba(93, 138, 168, 0.05) !important;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

.status-badge.status-pending {
  background: rgba(144, 147, 153, 0.1);
  color: #909399;
}

.status-badge.status-processing {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
}

.status-badge.status-completed {
  background: rgba(103, 194, 58, 0.1);
  color: #67C23A;
}

.status-badge.status-failed {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
}

.success-text {
  color: #67C23A;
  font-weight: 600;
}

.error-text {
  color: #C23531;
  font-weight: 600;
}

.table-download-btn {
  padding: 6px 12px;
  background: rgba(93, 138, 168, 0.15);
  color: #5D8AA8;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.table-download-btn:hover:not(:disabled) {
  background: #5D8AA8;
  color: white;
}

.table-download-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

:deep(.el-pagination .el-pager li.is-active) {
  background: #5D8AA8 !important;
  border-color: #5D8AA8 !important;
}
</style>
