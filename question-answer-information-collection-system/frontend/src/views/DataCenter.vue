<template>
  <div class="data-center-page">
    <!-- Header Section -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M4 7V4h16v3M9 20h6M12 4v16"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">{{ pageTitle }}</h1>
            <p class="page-subtitle">智能问答数据管理平台</p>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-pill">
            <span class="stat-dot"></span>
            <span class="stat-value">{{ total.toLocaleString() }}</span>
            <span class="stat-label">总记录</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Control Bar -->
    <section class="control-bar">
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
            placeholder="搜索问答标题..."
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
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <span v-else class="loading-spinner-small"></span>
          </button>
        </div>
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

    <!-- Data Table -->
    <section class="table-section">
      <div class="table-container">
        <!-- Table Header -->
        <div class="table-header">
          <div class="header-row">
            <div class="header-cell col-id">ID</div>
            <div class="header-cell col-title">问题标题</div>
            <div class="header-cell col-answerer">分类</div>
            <div class="header-cell col-time">回答时间</div>
            <div class="header-cell col-tags">位置</div>
            <div class="header-cell col-actions" v-if="authStore.isAdmin">操作</div>
          </div>
        </div>

        <!-- Table Body -->
        <div class="table-body" v-loading="tableLoading" :element-loading-text="'数据加载中...'">
          <!-- Loading Slot -->
          <template v-if="tableLoading">
            <div v-for="n in 10" :key="n" class="skeleton-row">
              <div class="skeleton-cell col-id"><div class="skeleton-block" style="width: 30px;"></div></div>
              <div class="skeleton-cell col-title"><div class="skeleton-block" style="width: 80%;"></div></div>
              <div class="skeleton-cell col-answerer"><div class="skeleton-block" style="width: 60px;"></div></div>
              <div class="skeleton-cell col-time"><div class="skeleton-block" style="width: 100px;"></div></div>
              <div class="skeleton-cell col-tags"><div class="skeleton-block" style="width: 120px;"></div></div>
              <div class="skeleton-cell col-actions" v-if="authStore.isAdmin"><div class="skeleton-block" style="width: 80px;"></div></div>
            </div>
          </template>

          <!-- Data Rows -->
          <template v-else>
            <div
              v-for="(row, index) in tableData"
              :key="row.id"
              class="data-row"
              :style="{ animationDelay: `${index * 0.03}s` }"
              @click="openDetail(row)"
            >
              <div class="data-cell col-id">
                <span class="row-id">{{ String(row.id).padStart(4, '0') }}</span>
              </div>
              <div class="data-cell col-title">
                <div class="title-content">
                  <span class="title-text">{{ row.title }}</span>
                  <span class="source-hint" v-if="row.source_url">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                    </svg>
                  </span>
                </div>
              </div>
              <div class="data-cell col-answerer">
                <div class="answerer-badge" v-if="row.category">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
                    <line x1="7" y1="7" x2="7.01" y2="7"/>
                  </svg>
                  <span>{{ row.category }}</span>
                </div>
                <span v-else class="empty-text">-</span>
              </div>
              <div class="data-cell col-time">
                <span class="time-text">{{ formatDate(row.publish_time) }}</span>
              </div>
              <div class="data-cell col-tags">
                <div class="tags-wrapper" v-if="row.location">
                  <span class="tag-badge">
                    {{ row.location }}
                  </span>
                </div>
                <span v-else class="empty-text">-</span>
              </div>
              <div class="data-cell col-actions" v-if="authStore.isAdmin" @click.stop>
                <button class="action-btn view" @click="openDetail(row)" title="查看详情">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
                <button class="action-btn delete" @click="handleDelete(row)" title="删除">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="!tableData.length" class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <h3 class="empty-title">暂无数据</h3>
              <p class="empty-desc">没有找到匹配的问答记录</p>
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
            :page-sizes="[20, 50, 100]"
            :total="total"
            layout="prev, pager, next, sizes, jumper"
            background
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </section>

    <!-- Detail Dialog -->
    <el-dialog
      v-model="detailVisible"
      :title="selectedQuestion?.title"
      width="720px"
      class="detail-dialog"
      :show-close="true"
      :close-on-click-modal="true"
    >
      <div class="detail-content" v-if="selectedQuestion">
        <div class="detail-header">
          <div class="detail-meta">
            <span class="meta-item" v-if="selectedQuestion.category">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
                <line x1="7" y1="7" x2="7.01" y2="7"/>
              </svg>
              {{ selectedQuestion.category }}
            </span>
            <span class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              {{ formatDate(selectedQuestion.publish_time) }}
            </span>
            <span class="meta-item" v-if="selectedQuestion.location">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              {{ selectedQuestion.location }}
            </span>
          </div>
        </div>

        <div class="detail-section" v-if="selectedQuestion.description">
          <h4 class="section-title">问题描述</h4>
          <div class="section-content">
            <p>{{ selectedQuestion.description }}</p>
          </div>
        </div>

        <div class="detail-section" v-if="selectedQuestion.answers && selectedQuestion.answers.length">
          <h4 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            回答内容
          </h4>
          <div class="section-content answer">
            <div v-for="(answer, index) in selectedQuestion.answers" :key="index" class="answer-item">
              <div class="answer-meta" v-if="answer.answerer">
                <span class="answerer-name">{{ answer.answerer }}</span>
                <span class="answer-time">{{ formatDate(answer.answer_time) }}</span>
              </div>
              <p>{{ answer.content }}</p>
            </div>
          </div>
        </div>

        <div class="detail-footer" v-if="selectedQuestion.source_url">
          <a :href="selectedQuestion.source_url" target="_blank" class="source-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            查看原文
          </a>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessageBox, ElMessage } from 'element-plus'
import { getQuestions, deleteQuestion } from '@/api/questions'

const route = useRoute()
const authStore = useAuthStore()

// State
const tableData = ref([])
const tableLoading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const detailVisible = ref(false)
const selectedQuestion = ref(null)
const searchTimer = ref(null)

// Computed
const isAdmin = computed(() => authStore.isAdmin)
const pageTitle = computed(() => route.meta?.title || '数据中心')

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

const fetchData = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined
    }
    const res = await getQuestions(params)
    if (res.code === 0 || res.code === 200) {
      tableData.value = res.data || []
      total.value = res.total || 0
    }
  } catch (e) {
    console.error('Failed to fetch questions:', e)
    ElMessage.error('获取数据失败')
  } finally {
    tableLoading.value = false
  }
}

const handleSearchInput = () => {
  if (searchTimer.value) {
    clearTimeout(searchTimer.value)
  }
  searchTimer.value = setTimeout(() => {
    currentPage.value = 1
    fetchData()
  }, 300)
}

const handleSearch = () => {
  if (searchTimer.value) {
    clearTimeout(searchTimer.value)
  }
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

const openDetail = (row) => {
  selectedQuestion.value = row
  detailVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除这条问答记录吗？\n"${row.title.substring(0, 50)}..."`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }
    )
    tableLoading.value = true
    const res = await deleteQuestion(row.id)
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

// Lifecycle
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* Page Layout */
.data-center-page {
  min-height: 100%;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  position: relative;
}

.data-center-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 10% 20%, rgba(13, 148, 136, 0.03) 0%, transparent 40%),
    radial-gradient(circle at 90% 90%, rgba(139, 92, 246, 0.03) 0%, transparent 40%);
  pointer-events: none;
}

/* Header */
.page-header {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
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
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.12) 0%, rgba(20, 184, 166, 0.12) 100%);
  border: 1px solid rgba(13, 148, 136, 0.2);
  border-radius: 16px;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: #0d9488;
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
  position: relative;
  z-index: 1;
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

.stat-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #0d9488;
  font-family: 'Outfit', 'SF Mono', 'Fira Code', monospace;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
}

/* Control Bar */
.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.search-container {
  flex: 1;
  max-width: 480px;
  min-width: 280px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 1rem;
  width: 20px;
  height: 20px;
  color: #94a3b8;
  pointer-events: none;
  transition: color 0.2s ease;
}

.search-input {
  flex: 1;
  height: 48px;
  padding: 0 3.5rem 0 3rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #1e293b;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  outline: none;
  border-color: rgba(13, 148, 136, 0.5);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.search-input:focus + .search-icon {
  color: #0d9488;
}

.clear-btn {
  position: absolute;
  right: 3.5rem;
  width: 20px;
  height: 20px;
  padding: 0;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.2s ease;
}

.clear-btn:hover {
  color: #1e293b;
}

.clear-btn svg {
  width: 16px;
  height: 16px;
}

.search-btn {
  position: absolute;
  right: 0.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  border: none;
  border-radius: 10px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(13, 148, 136, 0.3);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-btn svg {
  width: 18px;
  height: 18px;
}

.loading-spinner-small {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.control-actions {
  display: flex;
  gap: 0.75rem;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #475569;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
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
  width: 18px;
  height: 18px;
}

/* Table Section */
.table-section {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.table-container {
  overflow-x: auto;
}

.table-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.header-row {
  display: flex;
  min-width: 900px;
}

.header-cell {
  padding: 1rem 1.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.col-id { width: 80px; flex-shrink: 0; text-align: center; }
.col-title { flex: 1; min-width: 300px; }
.col-answerer { width: 140px; flex-shrink: 0; }
.col-time { width: 160px; flex-shrink: 0; }
.col-tags { width: 180px; flex-shrink: 0; }
.col-actions { width: 120px; flex-shrink: 0; text-align: center; }

/* Table Body */
.table-body {
  min-height: 400px;
}

.data-row {
  display: flex;
  min-width: 900px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  animation: rowFadeIn 0.4s ease-out forwards;
  opacity: 0;
  transition: background 0.15s ease;
}

@keyframes rowFadeIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.data-row:hover {
  background: rgba(13, 148, 136, 0.03);
}

.data-row:last-child {
  border-bottom: none;
}

.data-cell {
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #334155;
}

.col-id { justify-content: center; }
.col-title { justify-content: flex-start; }
.col-answerer { justify-content: flex-start; }
.col-time { justify-content: flex-start; }
.col-tags { justify-content: flex-start; }
.col-actions { justify-content: center; gap: 0.5rem; }

.row-id {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.title-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  max-width: 100%;
}

.title-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.source-hint {
  flex-shrink: 0;
  color: #94a3b8;
}

.source-hint svg {
  width: 14px;
  height: 14px;
}

.answerer-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: #64748b;
}

.answerer-badge svg {
  width: 14px;
  height: 14px;
}

.time-text {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.8rem;
  color: #64748b;
}

.empty-text {
  color: #cbd5e1;
}

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.tag-badge {
  padding: 0.25rem 0.625rem;
  background: rgba(13, 148, 136, 0.08);
  border: 1px solid rgba(13, 148, 136, 0.15);
  border-radius: 9999px;
  font-size: 0.7rem;
  color: #0d9488;
}

.tag-more {
  padding: 0.25rem 0.5rem;
  background: #f1f5f9;
  border-radius: 9999px;
  font-size: 0.7rem;
  color: #94a3b8;
}

/* Action Buttons */
.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.05);
}

.action-btn.view:hover {
  background: rgba(13, 148, 136, 0.08);
  border-color: rgba(13, 148, 136, 0.2);
  color: #0d9488;
}

.action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

/* Skeleton Loading */
.skeleton-row {
  display: flex;
  min-width: 900px;
  border-bottom: 1px solid #f1f5f9;
}

.skeleton-cell {
  padding: 1rem 1.25rem;
}

.skeleton-block {
  height: 16px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.col-id { width: 80px; flex-shrink: 0; }
.col-title { flex: 1; min-width: 300px; }
.col-answerer { width: 140px; flex-shrink: 0; }
.col-time { width: 160px; flex-shrink: 0; }
.col-tags { width: 180px; flex-shrink: 0; }
.col-actions { width: 120px; flex-shrink: 0; }

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  min-height: 300px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  margin-bottom: 1.5rem;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #cbd5e1;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem;
}

.empty-desc {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
  gap: 1rem;
}

.pagination-info {
  font-size: 0.8rem;
  color: #64748b;
}

.info-highlight {
  font-weight: 500;
  color: #0d9488;
  font-family: 'Outfit', 'SF Mono', 'Fira Code', monospace;
}

.pagination-controls {
  display: flex;
  justify-content: flex-end;
}

/* Element Plus Pagination Override */
.pagination-controls :deep(.el-pagination) {
  --el-pagination-bg-color: #ffffff;
  --el-pagination-text-color: #475569;
  --el-pagination-button-bg-color: #ffffff;
  --el-pagination-hover-color: #0d9488;
  --el-pagination-font-size: 0.8rem;
}

.pagination-controls :deep(.el-pagination .el-pager li) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin: 0 0.25rem;
  min-width: 32px;
  height: 32px;
  line-height: 32px;
}

.pagination-controls :deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  color: #fff;
  border-color: #0d9488;
}

.pagination-controls :deep(.el-pagination .el-pager li:hover) {
  border-color: #0d9488;
}

.pagination-controls :deep(.el-pagination .btn-prev),
.pagination-controls :deep(.el-pagination .btn-next) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #475569;
  min-width: 32px;
  height: 32px;
}

.pagination-controls :deep(.el-pagination .el-select .el-input__wrapper) {
  background: #ffffff;
  border-radius: 8px;
}

.pagination-controls :deep(.el-pagination .el-input__inner) {
  color: #475569;
}

/* Detail Dialog */
.detail-dialog :deep(.el-dialog) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.12);
}

.detail-dialog :deep(.el-dialog__header) {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.detail-dialog :deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.detail-dialog :deep(.el-dialog__headerbtn) {
  top: 1rem;
  right: 1rem;
  width: 32px;
  height: 32px;
  background: #f8fafc;
  border-radius: 8px;
}

.detail-dialog :deep(.el-dialog__headerbtn:hover) {
  background: rgba(239, 68, 68, 0.1);
}

.detail-dialog :deep(.el-dialog__headerbtn .el-icon) {
  color: #64748b;
  font-size: 1.25rem;
}

.detail-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.detail-content {
  padding: 1.5rem;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
  flex-wrap: wrap;
  gap: 1rem;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
}

.meta-item svg {
  width: 16px;
  height: 16px;
  color: #0d9488;
}

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.detail-tag {
  padding: 0.375rem 0.75rem;
  background: rgba(13, 148, 136, 0.08);
  border: 1px solid rgba(13, 148, 136, 0.15);
  border-radius: 9999px;
  font-size: 0.75rem;
  color: #0d9488;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.75rem;
}

.section-title svg {
  width: 18px;
  height: 18px;
  color: #0d9488;
}

.section-content {
  padding: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.7;
  color: #475569;
}

.section-content.answer {
  background: rgba(13, 148, 136, 0.03);
  border-color: rgba(13, 148, 136, 0.15);
}

.section-content p {
  margin: 0;
  white-space: pre-wrap;
}

.detail-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.source-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #0d9488;
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.source-link:hover {
  color: #14b8a6;
}

.source-link svg {
  width: 16px;
  height: 16px;
}

/* Responsive */
@media (max-width: 1024px) {
  .data-center-page {
    padding: 1.5rem;
  }

  .control-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-container {
    max-width: 100%;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .pagination-wrapper {
    flex-direction: column;
    align-items: stretch;
  }

  .pagination-controls {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .data-center-page {
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

  .pagination-controls :deep(.el-pagination) {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
