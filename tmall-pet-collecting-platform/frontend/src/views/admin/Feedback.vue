<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { feedbackApi } from '@/api'
import {
  Message, Search, Refresh, Delete, View, Check, Filter, Lock, CircleCheck
} from '@element-plus/icons-vue'

const feedbacks = ref([])
const loading = ref(false)
const total = ref(0)
const detailVisible = ref(false)
const currentFeedback = ref(null)

// 确认弹窗
const showConfirmDialog = ref(false)
const confirmConfig = ref({
  title: '',
  message: '',
  type: 'warning',
  onConfirm: null
})

const handleConfirmAction = async () => {
  if (confirmConfig.value.onConfirm) {
    await confirmConfig.value.onConfirm()
  }
  showConfirmDialog.value = false
}

const searchForm = ref({
  status: ''
})

const showFilters = ref(false)

const pagination = ref({
  page: 1,
  page_size: 20
})

const statusOptions = [
  { label: '全部', value: '' },
  { label: '待处理', value: 'pending' },
  { label: '已处理', value: 'processed' }
]

const loadFeedbacks = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: searchForm.value.status || undefined
    }

    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })

    const res = await feedbackApi.getList(params)
    if (res.code === 0) {
      feedbacks.value = res.data || []
      total.value = res.total || 0
    }
  } catch (error) {
    ElMessage.error('加载反馈数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  loadFeedbacks()
}

const handleReset = () => {
  searchForm.value = { status: '' }
  showFilters.value = false
  pagination.value.page = 1
  loadFeedbacks()
}

const handlePageChange = (page) => {
  pagination.value.page = page
  loadFeedbacks()
}

const handlePageSizeChange = (size) => {
  pagination.value.page_size = size
  pagination.value.page = 1
  loadFeedbacks()
}

const handleView = async (feedback) => {
  try {
    const res = await feedbackApi.getDetail(feedback.id)
    if (res.code === 0) {
      currentFeedback.value = res.data
      detailVisible.value = true
    }
  } catch (error) {
    ElMessage.error('加载反馈详情失败')
  }
}

const handleProcess = (feedback) => {
  const title = feedback?.title || '此反馈'
  confirmConfig.value = {
    title: '确认处理',
    message: `确定要将反馈 "${title}" 标记为已处理吗？`,
    type: 'info',
    onConfirm: async () => {
      try {
        const res = await feedbackApi.process(feedback.id)
        if (res.code === 0) {
          ElMessage.success('处理成功')
          loadFeedbacks()
        }
      } catch (error) {
        ElMessage.error('处理失败')
      }
    }
  }
  showConfirmDialog.value = true
}

const handleDelete = (feedback) => {
  const title = feedback?.title || '此反馈'
  confirmConfig.value = {
    title: '确认删除',
    message: `确定要删除反馈 "${title}" 吗？此操作不可恢复。`,
    type: 'danger',
    onConfirm: async () => {
      try {
        const res = await feedbackApi.delete(feedback.id)
        if (res.code === 0) {
          ElMessage.success('删除成功')
          loadFeedbacks()
        }
      } catch (error) {
        ElMessage.error('删除失败')
      }
    }
  }
  showConfirmDialog.value = true
}

const getStatusConfig = (status) => {
  const configs = {
    pending: { color: '#FFB800', bg: 'rgba(255, 184, 0, 0.12)', text: '待处理' },
    processed: { color: '#52B788', bg: 'rgba(82, 183, 136, 0.12)', text: '已处理' }
  }
  return configs[status] || configs.pending
}

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

onMounted(() => {
  loadFeedbacks()
})
</script>

<template>
  <div class="feedback-container">
    <!-- 装饰叶子 -->
    <div class="leaf-decoration leaf-decoration--1">
      <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
        <path d="M50 5C50 5 85 25 85 55C85 85 65 95 50 95C35 95 15 85 15 55C15 25 50 5 50 5Z" fill="currentColor" opacity="0.04"/>
      </svg>
    </div>

    <!-- 顶部欢迎区 -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-icon-wrapper">
          <Message class="header-icon" />
        </div>
        <div>
          <h1 class="header-title">反馈管理</h1>
          <p class="header-subtitle">查看和处理用户提交的反馈意见</p>
        </div>
      </div>
      <div class="header-actions">
        <button class="action-btn action-btn--secondary" @click="loadFeedbacks" :class="{ loading }">
          <Refresh class="icon" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <!-- 搜索和筛选区 -->
    <div class="filter-section">
      <div class="search-box">
        <el-select
          v-model="searchForm.status"
          placeholder="状态筛选"
          class="status-select"
          @change="handleSearch"
        >
          <el-option
            v-for="item in statusOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <button class="filter-btn" @click="showFilters = !showFilters">
          <Filter class="icon" />
          <span>{{ showFilters ? '收起' : '更多' }}</span>
        </button>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="data-table-wrapper">
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th class="th-user">用户</th>
              <th class="th-title">反馈标题</th>
              <th class="th-status">状态</th>
              <th class="th-time">提交时间</th>
              <th class="th-actions">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="loading-row">
              <td colspan="5" class="loading-cell">
                <div class="loading-spinner"></div>
                <span>加载中...</span>
              </td>
            </tr>
            <tr v-else-if="feedbacks.length === 0" class="empty-row">
              <td colspan="5" class="empty-cell">
                <div class="empty-state">
                  <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                    <circle cx="32" cy="32" r="24" fill="url(#emptyGradAdmin)" fill-opacity="0.08"/>
                    <path d="M20 28C20 24 23 21 27 21H37C41 21 44 24 44 28V40C44 42 42 44 40 44H24C22 44 20 42 20 40V28Z" stroke="url(#emptyPathAdmin)" stroke-width="2" stroke-linecap="round"/>
                    <path d="M32 30V36M32 40V40.5" stroke="url(#emptyPathAdmin)" stroke-width="2" stroke-linecap="round"/>
                    <defs>
                      <linearGradient id="emptyGradAdmin" x1="8" y1="8" x2="56" y2="56">
                        <stop offset="0%" stop-color="#74C69D"/>
                        <stop offset="100%" stop-color="#40916C"/>
                      </linearGradient>
                      <linearGradient id="emptyPathAdmin" x1="20" y1="21" x2="44" y2="44">
                        <stop offset="0%" stop-color="#74C69D"/>
                        <stop offset="100%" stop-color="#52B788"/>
                      </linearGradient>
                    </defs>
                  </svg>
                  <p>暂无反馈数据</p>
                </div>
              </td>
            </tr>
            <tr v-else v-for="item in feedbacks" :key="item.id" class="data-row">
              <td class="td-user">
                <div class="user-cell">
                  <div class="user-avatar">
                    {{ item.user_username?.charAt(0)?.toUpperCase() || 'U' }}
                  </div>
                  <span class="user-name">{{ item.user_username || '未知用户' }}</span>
                </div>
              </td>
              <td class="td-title">
                <span class="title-text">{{ item.title }}</span>
              </td>
              <td class="td-status">
                <span
                  class="status-badge"
                  :style="{
                    color: getStatusConfig(item.status).color,
                    background: getStatusConfig(item.status).bg
                  }"
                >
                  {{ getStatusConfig(item.status).text }}
                </span>
              </td>
              <td class="td-time">
                {{ formatTime(item.created_at) }}
              </td>
              <td class="td-actions">
                <div class="action-buttons">
                  <button class="icon-btn" title="查看详情" @click="handleView(item)">
                    <View class="icon" />
                  </button>
                  <button
                    v-if="item.status === 'pending'"
                    class="icon-btn icon-btn--success"
                    title="标记已处理"
                    @click="handleProcess(item)"
                  >
                    <Check class="icon" />
                  </button>
                  <button
                    class="icon-btn icon-btn--danger"
                    title="删除"
                    @click="handleDelete(item)"
                  >
                    <Delete class="icon" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <div class="pagination-info">
          共 <span class="highlight">{{ total }}</span> 条记录
        </div>
        <div class="pagination-controls">
          <button
            class="page-btn"
            :disabled="pagination.page === 1"
            @click="handlePageChange(pagination.page - 1)"
          >
            上一页
          </button>
          <span class="page-indicator">{{ pagination.page }}</span>
          <button
            class="page-btn"
            :disabled="pagination.page * pagination.page_size >= total"
            @click="handlePageChange(pagination.page + 1)"
          >
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- 确认弹窗 -->
    <div v-if="showConfirmDialog" class="modal-overlay" @click.self="showConfirmDialog = false">
      <div class="modal-dialog modal-dialog--confirm" :class="`modal-dialog--${confirmConfig.type}`">
        <div class="confirm-body">
          <div class="confirm-icon-wrapper" :class="`confirm-icon-wrapper--${confirmConfig.type}`">
            <component
              :is="confirmConfig.type === 'danger' ? Delete : (confirmConfig.type === 'warning' ? Lock : CircleCheck)"
              class="confirm-icon"
            />
          </div>
          <h3 class="confirm-title">{{ confirmConfig.title }}</h3>
          <p class="confirm-message">{{ confirmConfig.message }}</p>
        </div>
        <div class="modal-footer modal-footer--confirm">
          <button class="modal-btn modal-btn--cancel" @click="showConfirmDialog = false">
            <span>取消</span>
          </button>
          <button
            class="modal-btn modal-btn--confirm"
            :class="`modal-btn--${confirmConfig.type}`"
            @click="handleConfirmAction"
          >
            <span>确认操作</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="反馈详情"
      width="600px"
      class="detail-dialog"
    >
      <div v-if="currentFeedback" class="detail-content">
        <div class="detail-item">
          <span class="detail-label">用户</span>
          <span class="detail-value">{{ currentFeedback.user_username }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">反馈标题</span>
          <span class="detail-value">{{ currentFeedback.title }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">状态</span>
          <span
            class="status-badge"
            :style="{
              color: getStatusConfig(currentFeedback.status).color,
              background: getStatusConfig(currentFeedback.status).bg
            }"
          >
            {{ getStatusConfig(currentFeedback.status).text }}
          </span>
        </div>
        <div class="detail-item">
          <span class="detail-label">联系方式</span>
          <span class="detail-value">{{ currentFeedback.contact || '未填写' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">提交时间</span>
          <span class="detail-value">{{ formatTime(currentFeedback.created_at) }}</span>
        </div>
        <div class="detail-item detail-item--full">
          <span class="detail-label">反馈内容</span>
          <div class="detail-content-box">{{ currentFeedback.content }}</div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
          <el-button
            v-if="currentFeedback?.status === 'pending'"
            type="primary"
            @click="handleProcess(currentFeedback); detailVisible = false"
          >
            标记已处理
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

.feedback-container {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;

  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
  animation: pageFadeIn 0.4s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.leaf-decoration {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  color: var(--primary-green);
}

.leaf-decoration--1 {
  top: -20px;
  right: 10%;
  opacity: 0.3;
}

/* Header */
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.08);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon-wrapper {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(116, 198, 157, 0.15), rgba(116, 198, 157, 0.05));
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 14px;
}

.header-icon {
  width: 26px;
  height: 26px;
  color: var(--primary-green);
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 4px 0 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn .icon {
  width: 16px;
  height: 16px;
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-green), var(--primary-light));
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(45, 106, 79, 0.2);
}

.action-btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 106, 79, 0.3);
}

.action-btn--secondary {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
}

.action-btn--secondary:hover {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.action-btn.loading .icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Filter Section */
.filter-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-select {
  width: 140px;
}

.status-select :deep(.el-input__wrapper) {
  border-radius: 10px;
  background: var(--bg-sand);
  box-shadow: none;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.filter-btn .icon {
  width: 14px;
  height: 14px;
}

/* Table */
.data-table-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.08);
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 16px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--bg-sand);
  border-bottom: 1px solid var(--border-light);
}

.data-table td {
  padding: 16px 20px;
  font-size: 14px;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-light);
}

.data-row:hover {
  background: rgba(116, 198, 157, 0.03);
}

.loading-row .loading-cell,
.empty-row .empty-cell {
  padding: 60px 20px;
  text-align: center;
  color: var(--text-tertiary);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  margin: 0 auto 12px;
  border: 3px solid var(--border-light);
  border-top-color: var(--primary-green);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.empty-state p {
  margin: 12px 0 0;
  font-size: 14px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-green), var(--accent-green));
  border-radius: 50%;
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.user-name {
  font-weight: 500;
}

.title-text {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 20px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-btn:hover {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.icon-btn .icon {
  width: 14px;
  height: 14px;
}

.icon-btn--success:hover {
  border-color: var(--primary-light);
  color: var(--primary-light);
  background: rgba(82, 183, 136, 0.1);
}

.icon-btn--danger:hover {
  border-color: #DC2626;
  color: #DC2626;
  background: rgba(220, 38, 38, 0.1);
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
  background: var(--bg-sand);
}

.pagination-info {
  font-size: 13px;
  color: var(--text-secondary);
}

.pagination-info .highlight {
  color: var(--primary-green);
  font-weight: 600;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-btn {
  padding: 8px 16px;
  font-size: 13px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-indicator {
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-green);
}

/* Detail Dialog */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-item--full {
  flex-direction: column;
  align-items: flex-start;
}

.detail-label {
  flex-shrink: 0;
  width: 80px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-tertiary);
}

.detail-value {
  font-size: 14px;
  color: var(--text-primary);
}

.detail-content-box {
  width: 100%;
  padding: 16px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
  }

  .header-actions {
    width: 100%;
  }

  .action-btn {
    flex: 1;
    justify-content: center;
  }

  .filter-section {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }

  .search-box {
    width: 100%;
    flex-wrap: wrap;
  }

  .status-select {
    flex: 1;
  }

  .data-table th,
  .data-table td {
    padding: 12px;
  }

  .title-text {
    max-width: 150px;
  }

  .pagination-wrapper {
    flex-direction: column;
    gap: 12px;
  }
}

/* Dialog Styles */
:deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
}

:deep(.el-dialog__title) {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
  background: var(--bg-sand);
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-dialog {
  background: var(--bg-card);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  max-width: 90vw;
}

.modal-dialog--confirm {
  width: 420px;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.confirm-body {
  padding: 32px 24px 24px;
  text-align: center;
}

.confirm-icon-wrapper {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.confirm-icon-wrapper--warning {
  background: rgba(255, 184, 0, 0.12);
  color: #FFB800;
}

.confirm-icon-wrapper--info {
  background: rgba(0, 180, 216, 0.12);
  color: #00B4D8;
}

.confirm-icon-wrapper--danger {
  background: rgba(220, 38, 38, 0.12);
  color: #DC2626;
}

.confirm-icon {
  width: 28px;
  height: 28px;
}

.confirm-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px;
}

.confirm-message {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: var(--bg-sand);
}

.modal-footer--confirm {
  justify-content: center;
}

.modal-btn {
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Nunito', sans-serif;
}

.modal-btn--cancel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
}

.modal-btn--cancel:hover {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.modal-btn--confirm {
  color: white;
}

.modal-btn--warning {
  background: linear-gradient(135deg, #FFB800, #F59E0B);
}

.modal-btn--warning:hover {
  box-shadow: 0 4px 12px rgba(255, 184, 0, 0.3);
}

.modal-btn--info {
  background: linear-gradient(135deg, #00B4D8, #0096C7);
}

.modal-btn--info:hover {
  box-shadow: 0 4px 12px rgba(0, 180, 216, 0.3);
}

.modal-btn--danger {
  background: linear-gradient(135deg, #DC2626, #B91C1C);
}

.modal-btn--danger:hover {
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}
</style>
