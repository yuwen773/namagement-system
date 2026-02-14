<template>
  <div class="my-comments-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-decoration"></div>
      <div class="header-content">
        <div class="header-icon-wrapper">
          <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            <path d="M8 10h.01M12 10h.01M16 10h.01"/>
          </svg>
        </div>
        <h1 class="page-title">我的评论</h1>
        <p class="page-subtitle">
          共 <span class="count-badge">{{ comments.length }}</span> 条评论记录
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Empty State -->
      <div v-if="comments.length === 0 && !loading" class="empty-state">
        <div class="empty-illustration">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            <path d="M9 10h.01M15 10h.01"/>
          </svg>
        </div>
        <h2>还没有发表任何评论</h2>
        <p>分享您的游览体验，帮助更多游客</p>
        <router-link to="/attractions" class="explore-btn">
          <span>去景点逛逛</span>
          <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </router-link>
      </div>

      <!-- Comments List -->
      <div v-else class="comments-list">
        <div
          v-for="(item, index) in comments"
          :key="item.id"
          class="comment-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="card-header">
            <div class="attraction-info" @click="goToDetail(item.attraction_id)">
              <el-image :src="item.cover_image || getDefaultImage()" fit="cover" class="attraction-thumb" />
              <div class="attraction-details">
                <h3 class="attraction-name">{{ item.attraction_name }}</h3>
                <p class="comment-date">
                  <svg class="date-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  {{ formatDate(item.created_at) }}
                </p>
              </div>
            </div>

            <div class="card-actions">
              <span :class="['status-badge', `status-${item.status.toLowerCase()}`]">
                {{ getStatusLabel(item.status) }}
              </span>
              <button class="delete-btn" @click="confirmDelete(item)" title="删除评论">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="card-rating">
            <svg
              v-for="n in 5"
              :key="n"
              class="star-icon"
              :class="{ filled: n <= item.rating }"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            <span class="rating-text">{{ item.rating }} 分</span>
          </div>

          <div class="card-content">
            <p class="comment-text" :class="{ expanded: item.expanded }">
              {{ item.content }}
            </p>
            <button
              v-if="item.content.length > 100"
              class="expand-btn"
              @click="item.expanded = !item.expanded"
            >
              {{ item.expanded ? '收起' : '展开全部' }}
              <svg class="expand-icon" :class="{ rotated: item.expanded }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </button>
          </div>

          <!-- Status Message for Rejected Comments -->
          <div v-if="item.status === 'REJECTED'" class="status-message">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>您的评论未通过审核，请遵守社区规范</span>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>正在加载评论记录...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'
import commentsAPI from '@/api/comments'

const router = useRouter()
const comments = ref([])
const loading = ref(true)

const statusMap = {
  'PENDING': '待审核',
  'APPROVED': '已通过',
  'REJECTED': '已驳回'
}

function getStatusLabel(status) {
  return statusMap[status] || status
}

function formatDate(date) {
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}月前`
  return d.toLocaleDateString('zh-CN')
}

function goToDetail(id) {
  router.push(`/attractions/${id}`)
}

function getDefaultImage() {
  return 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=200&fit=crop'
}

async function fetchComments() {
  loading.value = true
  try {
    const res = await request.get('/comments/my/')
    comments.value = (res.data || []).map(item => ({ ...item, expanded: false }))
  } catch (error) {
    console.error('Failed to fetch comments:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

async function confirmDelete(item) {
  try {
    await ElMessageBox.confirm(
      `确定要删除这条评论吗？删除后无法恢复。`,
      '删除评论',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await commentsAPI.delete(item.id)
    ElMessage.success('评论已删除')
    await fetchComments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(fetchComments)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.my-comments-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  padding-bottom: 60px;
}

/* Header Section */
.page-header {
  position: relative;
  padding: 60px 20px 40px;
  text-align: center;
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 300px;
  background: radial-gradient(ellipse at center, rgba(30, 58, 95, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.header-content {
  position: relative;
  z-index: 2;
  animation: fadeInUp 0.6s ease;
}

.header-icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(30, 58, 95, 0.2);
}

.header-icon {
  width: 40px;
  height: 40px;
  color: white;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e3a5f;
  margin-bottom: 12px;
}

.page-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.1rem;
  color: #64748b;
}

.count-badge {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  margin: 0 4px;
}

/* Content Wrapper */
.content-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  animation: fadeIn 0.6s ease;
}

.empty-illustration {
  width: 140px;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.08) 0%, rgba(245, 158, 11, 0.05) 100%);
  border-radius: 50%;
  margin-bottom: 32px;
}

.empty-illustration svg {
  width: 70px;
  height: 70px;
  color: #94a3b8;
}

.empty-state h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 12px;
}

.empty-state p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  font-size: 1rem;
  margin-bottom: 32px;
}

.explore-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 36px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s ease;
}

.explore-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(30, 58, 95, 0.25);
}

.btn-arrow {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.explore-btn:hover .btn-arrow {
  transform: translateX(4px);
}

/* Comments List */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeInUp 0.6s ease;
}

.comment-card {
  background: white;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(30, 58, 95, 0.08);
  transition: all 0.3s ease;
  animation: fadeInUp 0.5s ease both;
}

.comment-card:hover {
  box-shadow: 0 8px 24px rgba(30, 58, 95, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 16px;
}

.attraction-info {
  display: flex;
  gap: 16px;
  flex: 1;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.attraction-info:hover {
  opacity: 0.8;
}

.attraction-thumb {
  width: 72px;
  height: 72px;
  border-radius: 14px;
  flex-shrink: 0;
}

.attraction-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.attraction-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 6px;
}

.comment-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #94a3b8;
}

.date-icon {
  width: 14px;
  height: 14px;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-approved {
  background: #d1fae5;
  color: #065f46;
}

.status-rejected {
  background: #fee2e2;
  color: #991b1b;
}

.delete-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fef2f2;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #ef4444;
}

.delete-btn:hover {
  background: #ef4444;
  color: white;
}

.delete-btn svg {
  width: 18px;
  height: 18px;
}

/* Rating */
.card-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(30, 58, 95, 0.05) 100%);
  border-radius: 12px;
  width: fit-content;
}

.star-icon {
  width: 18px;
  height: 18px;
  color: #e5e7eb;
  transition: color 0.3s ease;
}

.star-icon.filled {
  color: #f59e0b;
}

.rating-text {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  color: #64748b;
}

/* Content */
.card-content {
  position: relative;
}

.comment-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  line-height: 1.7;
  color: #475569;
  margin-bottom: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.comment-text.expanded {
  -webkit-line-clamp: unset;
  display: block;
}

.expand-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 12px;
  padding: 0;
  background: none;
  border: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e3a5f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.expand-btn:hover {
  color: #f59e0b;
}

.expand-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}

/* Status Message */
.status-message {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
}

.status-message svg {
  width: 18px;
  height: 18px;
  color: #ef4444;
  flex-shrink: 0;
}

.status-message span {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #991b1b;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #1e3a5f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: stretch;
  }

  .card-actions {
    justify-content: space-between;
  }

  .attraction-thumb {
    width: 60px;
    height: 60px;
  }

  .attraction-name {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 40px 20px 24px;
  }

  .page-title {
    font-size: 2rem;
  }

  .header-icon-wrapper {
    width: 64px;
    height: 64px;
  }

  .header-icon {
    width: 32px;
    height: 32px;
  }

  .comment-card {
    padding: 20px;
  }

  .attraction-thumb {
    width: 56px;
    height: 56px;
  }
}
</style>
