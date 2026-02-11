<template>
  <div class="comment-review-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">评论审核</h1>
          <p class="page-subtitle">管理用户提交的评论内容</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-badge pending">
          <span class="stat-number">{{ comments.length }}</span>
          <span class="stat-label">待审核</span>
        </div>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="filter-tabs">
      <button
        v-for="tab in filterTabs"
        :key="tab.key"
        :class="['filter-tab', { active: activeFilter === tab.key }]"
        @click="activeFilter = tab.key"
      >
        <svg viewBox="0 0 20 20" fill="currentColor">
          <circle cx="10" cy="10" r="6"/>
        </svg>
        <span>{{ tab.label }}</span>
        <span class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Comments List -->
    <div v-loading="loading" class="comments-list">
      <div v-for="comment in filteredComments" :key="comment.id" class="comment-card">
        <div class="card-header">
          <div class="user-info">
            <div class="user-avatar">
              {{ comment.user?.realName?.charAt(0) || comment.user?.username?.charAt(0) || 'U' }}
            </div>
            <div class="user-details">
              <p class="user-name">{{ comment.user?.realName || comment.user?.username || '未知用户' }}</p>
              <p class="comment-date">{{ formatDate(comment.createdAt) }}</p>
            </div>
          </div>
          <div class="comment-rating">
            <svg v-for="i in 5" :key="i" viewBox="0 0 20 20" :class="{ filled: i <= (comment.rating || 0) }">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>
        </div>

        <div class="attraction-info">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
          </svg>
          <router-link :to="`/admin/attractions/${comment.attraction?.id}/edit`" class="attraction-link">
            {{ comment.attraction?.name || '未知景点' }}
          </router-link>
        </div>

        <div class="comment-content">
          <p>{{ comment.content }}</p>
        </div>

        <div class="card-footer">
          <button @click="review(comment, 'APPROVED')" class="action-button approve">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            通过
          </button>
          <button @click="review(comment, 'REJECTED')" class="action-button reject">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            驳回
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredComments.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <p>暂无待审核评论</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="total > 10" class="pagination-section">
      <el-pagination
        v-model:current-page="page"
        :total="total"
        :page-size="10"
        layout="prev, pager, next"
        @current-change="fetchComments"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const comments = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const activeFilter = ref('all')

const filterTabs = [
  { key: 'all', label: '全部', count: 0 },
  { key: 'PENDING', label: '待审核', count: 0 },
  { key: 'APPROVED', label: '已通过', count: 0 },
  { key: 'REJECTED', label: '已驳回', count: 0 }
]

const filteredComments = computed(() => {
  if (activeFilter.value === 'all') {
    return comments.value
  }
  return comments.value.filter(c => c.status === activeFilter.value)
})

async function fetchComments() {
  loading.value = true
  try {
    const res = await request.get('/comments/', {
      params: { page: page.value, page_size: 50, status: activeFilter.value === 'all' ? undefined : activeFilter.value }
    })
    comments.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error(error)
    ElMessage.error('获取评论列表失败')
  } finally {
    loading.value = false
  }
}

async function review(comment, status) {
  try {
    await request.put(`/comments/${comment.id}/review/`, { status })
    ElMessage.success(status === 'APPROVED' ? '评论已通过' : '评论已驳回')

    // Remove from local list
    const index = comments.value.findIndex(c => c.id === comment.id)
    if (index > -1) {
      comments.value.splice(index, 1)
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchComments)

watch(activeFilter, () => {
  page.value = 1
  fetchComments()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.comment-review-page {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
  border-radius: 16px;
  color: #1e3a5f;
}

.header-icon svg {
  width: 28px;
  height: 28px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
}

.header-stats {
  display: flex;
  gap: 12px;
}

.stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-badge.pending .stat-number {
  color: #f97316;
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.filter-tab svg {
  width: 14px;
  height: 14px;
  color: #9ca3af;
}

.filter-tab:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.filter-tab.active {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  border-color: transparent;
  color: white;
}

.filter-tab.active svg {
  color: white;
}

.tab-count {
  font-size: 12px;
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  font-weight: 600;
}

.filter-tab:not(.active) .tab-count {
  background: #f3f4f6;
  color: #6b7280;
}

/* Comments List */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.comment-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.comment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #fbbf24;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  font-size: 18px;
  font-weight: 700;
  border-radius: 12px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.comment-date {
  font-size: 13px;
  color: #9ca3af;
}

.comment-rating {
  display: flex;
  gap: 4px;
}

.comment-rating svg {
  width: 18px;
  height: 18px;
  color: #e5e7eb;
  transition: color 0.3s ease;
}

.comment-rating svg.filled {
  color: #fbbf24;
}

.attraction-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 10px;
}

.attraction-info svg {
  width: 16px;
  height: 16px;
  color: #9ca3af;
  flex-shrink: 0;
}

.attraction-link {
  font-size: 14px;
  color: #1e3a5f;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.attraction-link:hover {
  color: #f97316;
}

.comment-content {
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  margin-bottom: 16px;
}

.comment-content p {
  font-size: 15px;
  color: #374151;
  line-height: 1.6;
  white-space: pre-wrap;
}

.card-footer {
  display: flex;
  gap: 12px;
}

.action-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-button svg {
  width: 18px;
  height: 18px;
}

.action-button.approve {
  background: #dcfce7;
  color: #16a34a;
}

.action-button.approve:hover {
  background: #bbf7d0;
  transform: translateY(-2px);
}

.action-button.reject {
  background: #fee2e2;
  color: #ef4444;
}

.action-button.reject:hover {
  background: #fecaca;
  transform: translateY(-2px);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: #9ca3af;
}

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: center;
  padding: 24px;
  background: white;
  border-radius: 16px;
}

:deep(.el-pagination) {
  display: flex;
  gap: 8px;
}

:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next),
:deep(.el-pagination .el-pager li) {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.3s ease;
}

:deep(.el-pagination .btn-prev:hover),
:deep(.el-pagination .btn-next:hover),
:deep(.el-pagination .el-pager li:hover) {
  background: #f9fafb;
  border-color: #fbbf24;
  color: #1e3a5f;
}

:deep(.el-pagination .el-pager li.active) {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  border-color: transparent;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .card-footer {
    flex-direction: column;
  }
}
</style>
