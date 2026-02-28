<template>
  <div class="feedback-management-page" :class="{ 'user-view': !isAdmin }">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon" :class="{ 'user-icon': !isAdmin }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              <path d="M8 10h.01M12 10h.01M16 10h.01"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">{{ isAdmin ? '反馈管理' : '反馈建议' }}</h1>
            <p class="page-subtitle">{{ isAdmin ? '处理用户反馈建议' : '提交您的建议或问题' }}</p>
          </div>
        </div>
        <div class="header-stats" v-if="isAdmin">
          <div class="stat-pill pending">
            <span class="stat-dot"></span>
            <span class="stat-value">{{ stats.pending }}</span>
            <span class="stat-label">待处理</span>
          </div>
          <div class="stat-pill">
            <span class="stat-value">{{ total.toLocaleString() }}</span>
            <span class="stat-label">反馈总数</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Admin Control Bar -->
    <section class="control-bar" v-if="isAdmin">
      <div class="search-container">
        <div class="search-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            v-model="searchKeyword"
            type="text"
            class="search-input"
            placeholder="搜索反馈标题..."
            @keyup.enter="handleSearch"
            @input="handleSearchInput"
          />
          <button v-if="searchKeyword" class="clear-btn" @click="clearSearch">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
          <button class="search-btn" :disabled="tableLoading" @click="handleSearch">
            <svg v-if="!tableLoading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <span v-else class="loading-spinner-small"></span>
          </button>
        </div>
      </div>

      <!-- 筛选组件 -->
      <div class="filter-container">
        <!-- 类型筛选 -->
        <el-select
          v-model="filters.feedback_type"
          placeholder="反馈类型"
          clearable
          class="filter-select"
          @change="handleFilterChange"
        >
          <el-option label="全部" value="" />
          <el-option
            v-for="type in filterOptions.feedback_types"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>

        <!-- 状态筛选 -->
        <el-select
          v-model="filters.status"
          placeholder="处理状态"
          clearable
          class="filter-select"
          @change="handleFilterChange"
        >
          <el-option label="全部" value="" />
          <el-option
            v-for="status in filterOptions.statuses"
            :key="status.value"
            :label="status.label"
            :value="status.value"
          />
        </el-select>

        <!-- 时间范围筛选 -->
        <el-date-picker
          v-model="filters.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          class="filter-date-range"
          @change="handleFilterChange"
        />
      </div>

      <div class="control-actions">
        <button class="refresh-btn" :disabled="tableLoading" @click="fetchData">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
            <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
            <path d="M16 21h5v-5"/>
          </svg>
          <span>刷新</span>
        </button>
      </div>
    </section>

    <!-- Admin Table View -->
    <section class="table-section" v-if="isAdmin">
      <div class="table-container">
        <!-- Table Header -->
        <div class="table-header">
          <div class="header-row">
            <div class="header-cell col-id">ID</div>
            <div class="header-cell col-title">标题</div>
            <div class="header-cell col-user">提交用户</div>
            <div class="header-cell col-type">类型</div>
            <div class="header-cell col-status">状态</div>
            <div class="header-cell col-created">提交时间</div>
            <div class="header-cell col-actions">操作</div>
          </div>
        </div>

        <!-- Table Body -->
        <div class="table-body" v-loading="tableLoading" element-loading-text="加载中...">
          <!-- Loading Skeleton -->
          <template v-if="tableLoading">
            <div v-for="n in 8" :key="n" class="skeleton-row">
              <div class="skeleton-cell col-id"><div class="skeleton-block" style="width: 30px;"></div></div>
              <div class="skeleton-cell col-title"><div class="skeleton-block" style="width: 150px;"></div></div>
              <div class="skeleton-cell col-user"><div class="skeleton-block" style="width: 80px;"></div></div>
              <div class="skeleton-cell col-type"><div class="skeleton-block" style="width: 60px;"></div></div>
              <div class="skeleton-cell col-status"><div class="skeleton-block" style="width: 60px;"></div></div>
              <div class="skeleton-cell col-created"><div class="skeleton-block" style="width: 120px;"></div></div>
              <div class="skeleton-cell col-actions"><div class="skeleton-block" style="width: 100px;"></div></div>
            </div>
          </template>

          <!-- Data Rows -->
          <template v-else>
            <div
              v-for="(row, index) in tableData"
              :key="row.id"
              class="data-row"
              :style="{ animationDelay: `${index * 0.04}s` }"
            >
              <div class="data-cell col-id">
                <span class="row-id">{{ String(row.id).padStart(4, '0') }}</span>
              </div>
              <div class="data-cell col-title">
                <span class="title-text">{{ row.title }}</span>
              </div>
              <div class="data-cell col-user">
                <span class="user-text">{{ row.username }}</span>
              </div>
              <div class="data-cell col-type">
                <span class="type-badge" :class="getTypeClass(row.feedback_type)">
                  {{ row.feedback_type_display }}
                </span>
              </div>
              <div class="data-cell col-status">
                <span class="status-badge" :class="getStatusClass(row.status)">
                  <span class="status-dot"></span>
                  {{ row.status_display }}
                </span>
              </div>
              <div class="data-cell col-created">
                <span class="time-text">{{ formatDate(row.created_at) }}</span>
              </div>
              <div class="data-cell col-actions">
                <button class="action-btn view" @click="openViewDialog(row)" title="查看/回复">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
                <button
                  class="action-btn delete"
                  @click="handleDelete(row)"
                  title="删除"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="!tableData.length" class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                  <path d="M8 10h.01M12 10h.01M16 10h.01"/>
                </svg>
              </div>
              <h3 class="empty-title">暂无反馈</h3>
              <p class="empty-desc">暂无用户反馈记录</p>
            </div>
          </template>
        </div>
      </div>

      <!-- Pagination -->
      <div class="pagination-wrapper" v-if="total > 0">
        <div class="pagination-info">
          显示第 <span class="info-highlight">{{ (currentPage - 1) * pageSize + 1 }}</span> 到
          <span class="info-highlight">{{ Math.min(currentPage * pageSize, total) }}</span> 条，
          共 <span class="info-highlight">{{ total }}</span> 条
        </div>
        <div class="pagination-controls">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            :total="total"
            layout="prev, pager, next, sizes, jumper"
            background
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </section>

    <!-- User View -->
    <section class="user-feedback-section" v-else>
      <div class="user-layout">
        <!-- Submit Form -->
        <div class="submit-form-card">
          <h2 class="form-title">提交反馈</h2>
          <el-form
            ref="submitFormRef"
            :model="submitForm"
            :rules="submitRules"
            label-position="top"
            class="feedback-submit-form"
          >
            <el-form-item label="标题" prop="title">
              <el-input
                v-model="submitForm.title"
                placeholder="请输入反馈标题"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="反馈类型" prop="feedback_type">
              <el-select v-model="submitForm.feedback_type" placeholder="请选择反馈类型" class="full-width">
                <el-option
                  v-for="type in filterOptions.feedback_types"
                  :key="type.value"
                  :label="type.label"
                  :value="type.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="详细描述" prop="content">
              <el-input
                v-model="submitForm.content"
                type="textarea"
                :rows="6"
                placeholder="请详细描述您的建议或问题..."
                maxlength="2000"
                show-word-limit
              />
            </el-form-item>

            <el-form-item>
              <button
                class="submit-btn"
                :disabled="submitLoading"
                @click="handleSubmit"
              >
                <span v-if="!submitLoading">提交反馈</span>
                <span v-else class="btn-loading">
                  <span class="spinner"></span>
                  提交中...
                </span>
              </button>
            </el-form-item>
          </el-form>
        </div>

        <!-- My Feedback List -->
        <div class="my-feedback-list">
          <h3 class="list-title">我的反馈</h3>

          <div v-if="tableLoading" class="loading-container">
            <div v-for="n in 3" :key="n" class="feedback-card-skeleton">
              <div class="skeleton-title"><div class="skeleton-block"></div></div>
              <div class="skeleton-content"><div class="skeleton-block"></div></div>
              <div class="skeleton-meta"><div class="skeleton-block"></div></div>
            </div>
          </div>

          <div v-else-if="tableData.length" class="feedback-cards">
            <div
              v-for="(feedback, index) in tableData"
              :key="feedback.id"
              class="feedback-card"
              :style="{ animationDelay: `${index * 0.08}s` }"
            >
              <div class="feedback-card-header">
                <div class="header-left">
                  <h4 class="feedback-title">{{ feedback.title }}</h4>
                  <div class="feedback-badges">
                    <span class="type-badge" :class="getTypeClass(feedback.feedback_type)">
                      {{ feedback.feedback_type_display }}
                    </span>
                    <span class="status-badge" :class="getStatusClass(feedback.status)">
                      <span class="status-dot"></span>
                      {{ feedback.status_display }}
                    </span>
                  </div>
                </div>
                <div class="header-actions">
                  <button
                    class="card-action-btn delete"
                    @click="handleDelete(feedback)"
                    title="删除"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                  </button>
                </div>
              </div>
              <p class="feedback-content">{{ feedback.content }}</p>

              <!-- Admin Reply -->
              <div v-if="feedback.admin_reply" class="admin-reply-section">
                <div class="reply-header">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                  </svg>
                  <span class="reply-title">管理员回复</span>
                  <span class="reply-time">{{ formatDate(feedback.replied_at) }}</span>
                </div>
                <p class="reply-content">{{ feedback.admin_reply }}</p>
              </div>

              <div class="feedback-footer">
                <span class="feedback-date">{{ formatUserDate(feedback.created_at) }}</span>
              </div>
            </div>
          </div>

          <div v-else class="empty-user">
            <div class="empty-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                <path d="M8 10h.01M12 10h.01M16 10h.01"/>
              </svg>
            </div>
            <p class="empty-text">暂无反馈记录</p>
          </div>

          <!-- User Pagination -->
          <div class="user-pagination" v-if="total > pageSize">
            <el-pagination
              v-model:current-page="currentPage"
              :page-size="pageSize"
              :total="total"
              layout="prev, pager, next"
              background
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Admin View/Reply Dialog -->
    <el-dialog
      v-model="dialogVisible"
      title="反馈详情与处理"
      width="700px"
      class="feedback-dialog"
      :show-close="true"
      :close-on-click-modal="false"
    >
      <div class="feedback-detail" v-if="currentFeedback">
        <div class="detail-section">
          <h3 class="section-title">反馈信息</h3>
          <div class="detail-row">
            <span class="detail-label">标题：</span>
            <span class="detail-value">{{ currentFeedback.title }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">类型：</span>
            <span class="detail-value">
              <span class="type-badge" :class="getTypeClass(currentFeedback.feedback_type)">
                {{ currentFeedback.feedback_type_display }}
              </span>
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">提交用户：</span>
            <span class="detail-value">{{ currentFeedback.username }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">提交时间：</span>
            <span class="detail-value">{{ formatDate(currentFeedback.created_at) }}</span>
          </div>
          <div class="detail-content">
            <span class="detail-label">详细描述：</span>
            <p class="content-text">{{ currentFeedback.content }}</p>
          </div>

          <!-- Existing Reply -->
          <div v-if="currentFeedback.admin_reply" class="existing-reply">
            <div class="reply-header">
              <span class="reply-label">已回复：</span>
              <span class="reply-info">
                {{ currentFeedback.replied_by_username }} · {{ formatDate(currentFeedback.replied_at) }}
              </span>
            </div>
            <p class="reply-text">{{ currentFeedback.admin_reply }}</p>
          </div>
        </div>

        <div class="detail-section">
          <h3 class="section-title">处理反馈</h3>
          <el-form
            ref="handleFormRef"
            :model="handleForm"
            label-position="top"
            class="feedback-handle-form"
          >
            <el-form-item label="状态">
              <el-select v-model="handleForm.status" placeholder="选择处理状态" class="full-width">
                <el-option
                  v-for="status in filterOptions.statuses"
                  :key="status.value"
                  :label="status.label"
                  :value="status.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="管理员回复">
              <el-input
                v-model="handleForm.admin_reply"
                type="textarea"
                :rows="5"
                placeholder="输入回复内容（可选）..."
                maxlength="2000"
                show-word-limit
              />
            </el-form-item>
          </el-form>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="dialogVisible = false">关闭</button>
          <button class="confirm-btn" :disabled="handleLoading" @click="handleDialogSubmit">
            <span v-if="!handleLoading">保存处理</span>
            <span v-else class="btn-loading">
              <span class="spinner"></span>
              处理中...
            </span>
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { getFeedbackList, createFeedback, updateFeedback, deleteFeedback, getFeedbackFilterOptions } from '@/api/feedbacks'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

// Table state
const tableData = ref([])
const tableLoading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const searchTimer = ref(null)

// Stats
const stats = reactive({
  pending: 0
})

// 筛选状态
const filters = reactive({
  feedback_type: '',
  status: '',
  dateRange: null
})

// Filter options
const filterOptions = reactive({
  feedback_types: [],
  statuses: []
})

// Dialog state
const dialogVisible = ref(false)
const handleLoading = ref(false)
const currentFeedback = ref(null)

const handleForm = reactive({
  status: 'pending',
  admin_reply: ''
})

// User submit form
const submitFormRef = ref(null)
const submitLoading = ref(false)
const submitForm = reactive({
  title: '',
  feedback_type: 'other',
  content: ''
})

const submitRules = {
  title: [
    { required: true, message: '请输入反馈标题', trigger: 'blur' },
    { min: 1, max: 200, message: '标题长度在 1 到 200 个字符', trigger: 'blur' }
  ],
  feedback_type: [
    { required: true, message: '请选择反馈类型', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入详细描述', trigger: 'blur' }
  ]
}

// Fetch filter options
const fetchFilterOptions = async () => {
  try {
    const res = await getFeedbackFilterOptions()
    if (res.code === 0) {
      filterOptions.feedback_types = res.data.feedback_types || []
      filterOptions.statuses = res.data.statuses || []
    }
  } catch (e) {
    console.error('Failed to fetch filter options:', e)
  }
}

// Methods
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

const formatUserDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now - date
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (days === 0) {
      return '今天'
    } else if (days === 1) {
      return '昨天'
    } else if (days < 7) {
      return `${days}天前`
    } else {
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }
  } catch {
    return dateStr
  }
}

const getTypeClass = (type) => {
  const classMap = {
    'feature': 'feature',
    'bug': 'bug',
    'other': 'other'
  }
  return classMap[type] || 'other'
}

const getStatusClass = (status) => {
  const classMap = {
    'pending': 'pending',
    'processing': 'processing',
    'resolved': 'resolved',
    'ignored': 'ignored'
  }
  return classMap[status] || 'pending'
}

const fetchData = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined,
      feedback_type: filters.feedback_type || undefined,
      status: filters.status || undefined,
      created_at_after: filters.dateRange?.[0] || undefined,
      created_at_before: filters.dateRange?.[1] || undefined
    }
    const res = await getFeedbackList(params)
    if (res.code === 0 || res.code === 200) {
      tableData.value = res.data || []
      total.value = res.total || 0
      // Calculate pending count for admin
      if (isAdmin.value) {
        stats.pending = (res.data || []).filter(item => item.status === 'pending').length
      }
    }
  } catch (e) {
    console.error('Failed to fetch feedbacks:', e)
    ElMessage.error('获取反馈列表失败')
  } finally {
    tableLoading.value = false
  }
}

const handleSearchInput = () => {
  if (searchTimer.value) clearTimeout(searchTimer.value)
  searchTimer.value = setTimeout(() => {
    currentPage.value = 1
    fetchData()
  }, 300)
}

const handleSearch = () => {
  if (searchTimer.value) clearTimeout(searchTimer.value)
  currentPage.value = 1
  fetchData()
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchData()
}

const clearSearch = () => {
  searchKeyword.value = ''
  currentPage.value = 1
  fetchData()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchData()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchData()
}

// User submit feedback
const handleSubmit = async () => {
  if (!submitFormRef.value) return

  try {
    await submitFormRef.value.validate()
  } catch {
    return
  }

  submitLoading.value = true

  try {
    const res = await createFeedback({
      title: submitForm.title,
      feedback_type: submitForm.feedback_type,
      content: submitForm.content
    })
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('反馈提交成功')
      submitForm.title = ''
      submitForm.feedback_type = 'other'
      submitForm.content = ''
      submitFormRef.value.resetFields()
      currentPage.value = 1
      fetchData()
    } else {
      ElMessage.error(res.message || '提交失败')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.message || '提交失败，请稍后重试')
  } finally {
    submitLoading.value = false
  }
}

// Admin view/reply dialog
const openViewDialog = (row) => {
  currentFeedback.value = row
  handleForm.status = row.status
  handleForm.admin_reply = row.admin_reply || ''
  dialogVisible.value = true
}

const handleDialogSubmit = async () => {
  if (!currentFeedback.value) return

  handleLoading.value = true

  try {
    const res = await updateFeedback(currentFeedback.value.id, {
      status: handleForm.status,
      admin_reply: handleForm.admin_reply
    })
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('处理成功')
      dialogVisible.value = false
      fetchData()
    } else {
      ElMessage.error(res.message || '处理失败')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.message || '处理失败，请稍后重试')
  } finally {
    handleLoading.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      isAdmin.value
        ? `确定要删除来自 "${row.username}" 的反馈 "${row.title}" 吗？此操作不可恢复。`
        : `确定要删除您的反馈 "${row.title}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }
    )
    tableLoading.value = true
    const res = await deleteFeedback(row.id)
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('删除成功')
      if (tableData.value.length === 1 && currentPage.value > 1) {
        currentPage.value -= 1
      }
      fetchData()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    tableLoading.value = false
  }
}

onMounted(async () => {
  await fetchFilterOptions()
  fetchData()
})
</script>

<style scoped>
/* Page Layout */
.feedback-management-page {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  position: relative;
}

.feedback-management-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 300px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  opacity: 0.05;
  border-radius: 0 0 50% 50% / 0 0 100px 100px;
}

.user-view.feedback-management-page::before {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

/* Page Header */
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
  gap: 1.5rem;
}

.header-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 24px -8px rgba(99, 102, 241, 0.4);
}

.user-view .header-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 8px 24px -8px rgba(16, 185, 129, 0.4);
}

.header-icon svg {
  width: 32px;
  height: 32px;
}

.header-text {
  color: #1e293b;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.page-subtitle {
  color: #64748b;
  font-size: 0.95rem;
}

.header-stats {
  display: flex;
  gap: 1rem;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-pill.pending {
  border-left: 4px solid #f59e0b;
}

.stat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6366f1;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  color: #64748b;
  font-size: 0.85rem;
}

/* Control Bar */
.control-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 16px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.search-container {
  flex: 1;
  min-width: 280px;
}

.search-wrapper {
  display: flex;
  align-items: center;
  padding: 0.625rem 1rem;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.search-wrapper:focus-within {
  background: white;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #94a3b8;
  margin-right: 0.75rem;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.9rem;
  color: #1e293b;
}

.clear-btn {
  background: none;
  border: none;
  padding: 0.25rem;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-btn:hover {
  color: #64748b;
}

.clear-btn svg {
  width: 16px;
  height: 16px;
}

.search-btn {
  margin-left: 0.75rem;
  background: #6366f1;
  border: none;
  padding: 0.5rem;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.search-btn:hover:not(:disabled) {
  background: #5558e6;
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-btn svg {
  width: 16px;
  height: 16px;
}

.filter-container {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-select {
  width: 140px;
}

.filter-date-range {
  width: 280px;
}

.control-actions {
  display: flex;
  gap: 0.75rem;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn svg {
  width: 16px;
  height: 16px;
}

/* Table Section */
.table-section {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.table-container {
  overflow-x: auto;
}

/* Table Header */
.table-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.header-row {
  display: flex;
  min-width: 1000px;
}

.header-cell {
  padding: 1rem 1.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.col-id { width: 80px; flex-shrink: 0; }
.col-title { flex: 1; min-width: 200px; }
.col-user { width: 120px; flex-shrink: 0; }
.col-type { width: 120px; flex-shrink: 0; }
.col-status { width: 120px; flex-shrink: 0; }
.col-created { width: 180px; flex-shrink: 0; }
.col-actions { width: 140px; flex-shrink: 0; text-align: center; }

/* Table Body */
.table-body {
  min-width: 1000px;
}

.data-row {
  display: flex;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s;
  animation: fadeInUp 0.4s ease-out;
}

.data-row:hover {
  background: #f8fafc;
}

.data-cell {
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.row-id {
  color: #94a3b8;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
}

.title-text {
  color: #1e293b;
  font-weight: 500;
}

.user-text {
  color: #64748b;
}

.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
}

.type-badge.feature {
  background: #dbeafe;
  color: #1d4ed8;
}

.type-badge.bug {
  background: #fee2e2;
  color: #dc2626;
}

.type-badge.other {
  background: #f1f5f9;
  color: #475569;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.pending {
  background: #fef3c7;
  color: #d97706;
}

.status-badge.processing {
  background: #dbeafe;
  color: #2563eb;
}

.status-badge.resolved {
  background: #d1fae5;
  color: #059669;
}

.status-badge.ignored {
  background: #f1f5f9;
  color: #64748b;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.time-text {
  color: #64748b;
  font-size: 0.85rem;
}

/* Actions */
.data-cell.col-actions {
  justify-content: center;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn.view {
  background: #dbeafe;
  color: #2563eb;
}

.action-btn.view:hover {
  background: #2563eb;
  color: white;
}

.action-btn.delete {
  background: #fee2e2;
  color: #dc2626;
}

.action-btn.delete:hover {
  background: #dc2626;
  color: white;
}

/* Skeleton Loading */
.skeleton-row {
  display: flex;
  border-bottom: 1px solid #f1f5f9;
}

.skeleton-cell {
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
}

.skeleton-block {
  height: 16px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  display: inline-flex;
  width: 80px;
  height: 80px;
  background: #f8fafc;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  color: #cbd5e1;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.empty-desc {
  color: #94a3b8;
  font-size: 0.9rem;
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.pagination-info {
  color: #64748b;
  font-size: 0.9rem;
}

.info-highlight {
  color: #1e293b;
  font-weight: 600;
}

/* User View */
.user-feedback-section {
  max-width: 1200px;
  margin: 0 auto;
}

.user-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 2rem;
  align-items: start;
}

.submit-form-card {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 2rem;
}

.form-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.feedback-submit-form {
  margin-top: 1rem;
}

.full-width {
  width: 100%;
}

.submit-btn {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px -8px rgba(16, 185, 129, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.my-feedback-list {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.list-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.feedback-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-card {
  padding: 1.25rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
  animation: fadeInUp 0.4s ease-out;
}

.feedback-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.feedback-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.header-left {
  flex: 1;
}

.feedback-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.feedback-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.card-action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  background: #f1f5f9;
  color: #64748b;
}

.card-action-btn:hover {
  background: #e2e8f0;
  color: #475569;
}

.card-action-btn.delete:hover {
  background: #fee2e2;
  color: #dc2626;
}

.card-action-btn svg {
  width: 16px;
  height: 16px;
}

.feedback-content {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.admin-reply-section {
  padding: 0.875rem 1rem;
  background: #f0fdf4;
  border-radius: 8px;
  margin-bottom: 1rem;
  border-left: 3px solid #10b981;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.reply-header svg {
  width: 16px;
  height: 16px;
  color: #10b981;
}

.reply-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #059669;
}

.reply-time {
  margin-left: auto;
  font-size: 0.75rem;
  color: #64748b;
}

.reply-content {
  color: #475569;
  font-size: 0.85rem;
  line-height: 1.5;
}

.feedback-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.feedback-date {
  font-size: 0.8rem;
  color: #94a3b8;
}

.user-pagination {
  display: flex;
  justify-content: center;
  padding: 1.5rem 0 0;
}

.empty-user {
  text-align: center;
  padding: 3rem 2rem;
}

.empty-user .empty-icon {
  width: 60px;
  height: 60px;
}

.empty-user .empty-icon svg {
  width: 30px;
  height: 30px;
}

.empty-text {
  color: #94a3b8;
  font-size: 0.9rem;
}

/* Loading states */
.loading-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-card-skeleton,
.notice-card-skeleton {
  padding: 1.25rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.skeleton-title .skeleton-block {
  width: 60%;
  height: 20px;
  margin-bottom: 0.75rem;
}

.skeleton-content .skeleton-block {
  width: 100%;
  height: 48px;
  margin-bottom: 0.75rem;
}

.skeleton-date .skeleton-block {
  width: 30%;
  height: 14px;
}

.skeleton-meta .skeleton-block {
  width: 40%;
  height: 14px;
}

/* Dialog Styles */
.feedback-dialog .feedback-detail {
  max-height: 500px;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.detail-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  margin-bottom: 0.75rem;
}

.detail-label {
  width: 100px;
  flex-shrink: 0;
  color: #64748b;
  font-size: 0.9rem;
}

.detail-value {
  color: #1e293b;
  font-size: 0.9rem;
}

.detail-content {
  margin-top: 1rem;
}

.detail-content .detail-label {
  display: block;
  width: auto;
  margin-bottom: 0.5rem;
}

.content-text {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.6;
  white-space: pre-wrap;
  margin: 0;
}

.existing-reply {
  margin-top: 1rem;
  padding: 1rem;
  background: #f0fdf4;
  border-radius: 8px;
  border-left: 3px solid #10b981;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.reply-label {
  font-weight: 600;
  color: #059669;
  font-size: 0.9rem;
}

.reply-info {
  margin-left: auto;
  font-size: 0.8rem;
  color: #64748b;
}

.reply-text {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

.feedback-handle-form {
  margin-top: 1rem;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.confirm-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px -4px rgba(99, 102, 241, 0.4);
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Loading Spinner */
.btn-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 1024px) {
  .user-layout {
    grid-template-columns: 1fr;
  }

  .submit-form-card {
    position: static;
  }
}

@media (max-width: 768px) {
  .feedback-management-page {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-stats {
    width: 100%;
    justify-content: space-between;
  }

  .control-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-container {
    flex-direction: column;
  }

  .filter-select,
  .filter-date-range {
    width: 100%;
  }
}
</style>
