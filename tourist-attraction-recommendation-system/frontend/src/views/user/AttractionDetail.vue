<template>
  <div v-if="attraction" class="attraction-detail-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <el-image :src="attraction.cover_image" fit="cover" class="hero-image" />
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-badges">
          <span class="badge-category">{{ getCategoryLabel(attraction.category) }}</span>
          <div class="badge-rating">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            <span>{{ attraction.rating_percentage ? (attraction.rating_percentage * 100).toFixed(0) + '%' : '暂无评分' }}</span>
          </div>
        </div>
        <button :class="['favorite-btn', { active: isFavorite }]" @click="toggleFavorite">
          <svg class="heart-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
          <span>{{ isFavorite ? '已收藏' : '收藏' }}</span>
        </button>
      </div>
      <button class="back-btn" @click="$router.back()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="main-column">
        <!-- Title Section -->
        <div class="title-section">
          <h1 class="attraction-title">{{ attraction.name }}</h1>
          <div class="attraction-meta">
            <div class="meta-item">
              <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              <span>{{ attraction.address }}</span>
            </div>
            <div class="meta-item">
              <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <span>{{ formatNumber(attraction.view_count || 0) }} 浏览</span>
            </div>
            <!-- Removed price tag as it is not in the model -->
          </div>
        </div>

        <!-- Info Cards -->
        <div class="info-cards-grid">
          <div class="info-card">
            <div class="info-icon-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div class="info-content">
              <h3>开放时间</h3>
              <p>{{ attraction.opening_hours || '请以景区公告为准' }}</p>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
              </svg>
            </div>
            <div class="info-content">
              <h3>咨询电话</h3>
              <p>暂无</p>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
            </div>
            <div class="info-content">
              <h3>最佳季节</h3>
              <p>四季皆宜</p>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <div class="info-content">
              <h3>建议游玩</h3>
              <p>3-4 小时</p>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="description-section">
          <h2 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
            景点介绍
          </h2>
          <div class="description-content">
            {{ attraction.description }}
          </div>
        </div>

        <!-- Comments Section -->
        <div class="comments-section">
          <h2 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            游客评价
            <span class="comment-count">({{ totalComments }})</span>
          </h2>

          <!-- Comment Form -->
          <div v-if="userStore.isLoggedIn" class="comment-form-card">
            <div class="form-header">
              <h3>分享您的体验</h3>
            </div>
            <div class="form-content">
              <div class="rating-input">
                <span class="rating-label">评分</span>
                <el-rate v-model="newComment.rating" :colors="['#f59e0b', '#f59e0b', '#f59e0b']" size="large" />
              </div>
              <el-input
                v-model="newComment.content"
                type="textarea"
                :rows="4"
                placeholder="说说您的游览体验..."
                class="comment-textarea"
                maxlength="500"
                show-word-limit
              />
              <button class="submit-btn" @click="submitComment">
                <span>发表评价</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
            </div>
          </div>

          <div v-else class="login-prompt">
            <p>登录后参与评论</p>
            <router-link to="/login" class="login-link">立即登录</router-link>
          </div>

          <!-- Comments List -->
          <div class="comments-list">
            <div v-if="comments.length === 0" class="no-comments">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                <line x1="9" y1="9" x2="9.01" y2="9"/>
                <line x1="15" y1="9" x2="15.01" y2="9"/>
              </svg>
              <p>暂无评论，快来抢沙发吧~</p>
            </div>
            <div v-for="comment in comments" :key="comment.id" class="comment-card">
              <div class="comment-avatar">
                {{ comment.user?.realName?.charAt(0) || 'U' }}
              </div>
              <div class="comment-body">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.user?.realName }}</span>
                  <div class="comment-rating">
                    <svg v-for="n in 5" :key="n" viewBox="0 0 24 24" fill="currentColor" class="star-icon">
                      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                  </div>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
                <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- Map Card -->
        <div class="sidebar-card map-card">
          <div class="map-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/>
              <line x1="8" y1="2" x2="8" y2="18"/>
              <line x1="16" y1="6" x2="16" y2="22"/>
            </svg>
            <p>地图位置</p>
          </div>
          <div class="map-address">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            <span>{{ attraction.address }}</span>
          </div>
        </div>

        <!-- Similar Attractions -->
        <div class="sidebar-card recommendations-card">
          <h3 class="sidebar-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M16 12a4 4 0 0 1-8 0"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            相似推荐
          </h3>
          <div v-if="similarAttractions.length === 0" class="no-recommendations">
            <p>暂无推荐</p>
          </div>
          <div v-else class="recommendations-list">
            <div
              v-for="item in similarAttractions"
              :key="item.id"
              class="recommendation-item"
              @click="$router.push(`/attractions/${item.id}`)"
            >
              <el-image :src="item.cover_image" fit="cover" class="recommendation-image" />
              <div class="recommendation-info">
                <h4>{{ item.name }}</h4>
                <div class="recommendation-meta">
                  <el-rate :model-value="(item.rating_percentage || 0) * 5" disabled size="small" show-score text-color="#ff9900" score-template="{value}" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- Loading State -->
    <div v-if="!attraction" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在加载景点详情...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const attraction = ref(null)
const comments = ref([])
const similarAttractions = ref([])
const isFavorite = ref(false)
const favoriteId = ref(null)
const totalComments = ref(0)
const loading = ref(true)

const newComment = reactive({
  rating: 5,
  content: ''
})

const categoryMap = {
  'NATURE': '自然风光',
  'HISTORY': '人文古迹',
  'THEME': '主题乐园',
  'OTHER': '其他'
}

function getCategoryLabel(value) {
  return categoryMap[value] || value
}

function formatNumber(num) {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

function formatDate(date) {
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return d.toLocaleDateString('zh-CN')
}

async function fetchDetail() {
  loading.value = true
  try {
    const res = await request.get(`/attractions/${route.params.id}/`)
    attraction.value = res.data

    const commentsRes = await request.get(`/comments/attraction/${route.params.id}/`)
    comments.value = commentsRes.data || []
    totalComments.value = commentsRes.total || 0

    // Fetch similar attractions - handle 404 gracefully
    try {
      const similarRes = await request.get(`/recommendations/similar/${route.params.id}/`)
      similarAttractions.value = similarRes.data || []
    } catch (e) {
      similarAttractions.value = []
    }

    // Check if favorite
    if (userStore.isLoggedIn) {
      try {
        const favRes = await request.get('/comments/favorites/my/')
        const favorites = favRes.data || []
        // Use loose equality to handle string/number mismatch
        const currentFav = favorites.find(f => f.attraction == attraction.value.id)
        console.log('Favorite check:', { attractionId: attraction.value.id, favorites, currentFav })
        if (currentFav) {
          isFavorite.value = true
          favoriteId.value = currentFav.id
        } else {
          isFavorite.value = false
          favoriteId.value = null
        }
      } catch (e) {
        // Ignore error
      }
    }
  } catch (error) {
    ElMessage.error('加载失败')
    router.back()
  } finally {
    loading.value = false
  }
}

async function toggleFavorite() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    const res = await request.post('/comments/favorites/', { attraction: attraction.value.id })
    console.log('Toggle favorite response:', res.data)

    // 根据后端返回的 action 字段更新状态
    if (res.data.action === 'removed') {
      // 取消收藏
      isFavorite.value = false
      favoriteId.value = null
      ElMessage.success('已取消收藏')
    } else {
      // 收藏成功
      isFavorite.value = true
      favoriteId.value = res.data.id
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    console.log('Favorite toggle error:', error.response?.status, error.response?.data)
    ElMessage.error('操作失败')
  }
}

async function submitComment() {
  if (!newComment.content.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  try {
    await request.post('/comments/', {
      attraction: attraction.value.id,
      rating: newComment.rating,
      content: newComment.content
    })
    ElMessage.success('评论提交成功，等待审核')
    newComment.content = ''
    newComment.rating = 5
    // Refresh comments
    const commentsRes = await request.get(`/comments/attraction/${route.params.id}/`)
    comments.value = commentsRes.data || []
    totalComments.value = commentsRes.total || 0
  } catch (error) {
    ElMessage.error('提交失败')
  }
}

onMounted(fetchDetail)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.attraction-detail-page {
  min-height: 100vh;
  background: #f8fafc;
  padding-bottom: 60px;
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 60vh;
  min-height: 400px;
  max-height: 600px;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(30, 58, 95, 0.3) 0%, rgba(30, 58, 95, 0.7) 100%);
}

.hero-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 40px;
  z-index: 2;
}

.hero-badges {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.badge-category {
  padding: 8px 16px;
  background: rgba(245, 158, 11, 0.95);
  backdrop-filter: blur(10px);
  color: white;
  border-radius: 20px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-rating {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  color: #1e3a5f;
}

.badge-rating svg {
  width: 16px;
  height: 16px;
  color: #f59e0b;
}

.favorite-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 30px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.05);
}

.favorite-btn.active {
  background: #f59e0b;
  color: white;
}

.favorite-btn.active .heart-icon {
  fill: white;
}

.heart-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.favorite-btn:hover .heart-icon {
  transform: scale(1.2);
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.back-btn:hover {
  background: white;
  transform: scale(1.1);
}

.back-btn svg {
  width: 24px;
  height: 24px;
  color: #1e3a5f;
}

/* Content Wrapper */
.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 32px;
}

/* Main Column */
.main-column {
  min-width: 0;
}

/* Title Section */
.title-section {
  margin-bottom: 32px;
  animation: fadeInUp 0.6s ease;
}

.attraction-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e3a5f;
  margin-bottom: 20px;
  line-height: 1.3;
}

.attraction-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
}

.meta-icon {
  width: 18px;
  height: 18px;
  color: #f59e0b;
}

.price-tag {
  padding: 8px 16px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border-radius: 20px;
  font-weight: 600;
}

.price-tag .meta-icon {
  color: rgba(255, 255, 255, 0.7);
}

/* Info Cards Grid */
.info-cards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 40px;
  animation: fadeInUp 0.6s ease 0.1s both;
}

.info-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
  transition: all 0.3s ease;
}

.info-card:hover {
  box-shadow: 0 8px 24px rgba(30, 58, 95, 0.12);
  transform: translateY(-2px);
}

.info-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.1) 0%, rgba(45, 74, 111, 0.1) 100%);
  border-radius: 12px;
  flex-shrink: 0;
}

.info-icon-wrapper svg {
  width: 24px;
  height: 24px;
  color: #1e3a5f;
}

.info-content h3 {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-content p {
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  color: #1e3a5f;
  font-weight: 500;
}

/* Description Section */
.description-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 40px;
  box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
  animation: fadeInUp 0.6s ease 0.2s both;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 24px;
}

.section-title svg {
  width: 24px;
  height: 24px;
  color: #f59e0b;
}

.comment-count {
  font-size: 1rem;
  color: #94a3b8;
  font-weight: 400;
}

.description-content {
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  line-height: 1.8;
  color: #475569;
}

/* Comments Section */
.comments-section {
  animation: fadeInUp 0.6s ease 0.3s both;
}

.comment-form-card {
  background: white;
  border-radius: 20px;
  padding: 28px;
  margin-bottom: 32px;
  box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
}

.form-header h3 {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 20px;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rating-input {
  display: flex;
  align-items: center;
  gap: 16px;
}

.rating-label {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #475569;
}

.comment-textarea :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  line-height: 1.6;
  transition: all 0.3s ease;
}

.comment-textarea :deep(.el-textarea__inner:focus) {
  border-color: #1e3a5f;
  box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.1);
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-end;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(30, 58, 95, 0.25);
}

.submit-btn svg {
  width: 18px;
  height: 18px;
}

.login-prompt {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  margin-bottom: 32px;
  box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
}

.login-prompt p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
}

.login-link {
  padding: 10px 24px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.login-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 58, 95, 0.2);
}

/* Comments List */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.no-comments {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 60px 20px;
  text-align: center;
}

.no-comments svg {
  width: 80px;
  height: 80px;
  color: #cbd5e1;
}

.no-comments p {
  font-family: 'DM Sans', sans-serif;
  color: #94a3b8;
}

.comment-card {
  display: flex;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
  transition: all 0.3s ease;
}

.comment-card:hover {
  box-shadow: 0 6px 20px rgba(30, 58, 95, 0.1);
}

.comment-avatar {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 1.25rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.comment-author {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #1e3a5f;
}

.comment-rating {
  display: flex;
  gap: 2px;
}

.star-icon {
  width: 14px;
  height: 14px;
  color: #f59e0b;
}

.comment-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #475569;
  margin-bottom: 12px;
}

.comment-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #94a3b8;
}

/* Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
}

/* Map Card */
.map-card {
  animation: fadeInLeft 0.6s ease 0.4s both;
}

.map-placeholder {
  aspect-ratio: 16/9;
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.map-placeholder svg {
  width: 48px;
  height: 48px;
  color: #94a3b8;
}

.map-placeholder p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  font-weight: 500;
}

.map-address {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  border-top: 1px solid #e2e8f0;
}

.map-address svg {
  width: 18px;
  height: 18px;
  color: #f59e0b;
  flex-shrink: 0;
}

.map-address span {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #475569;
}

/* Recommendations Card */
.recommendations-card {
  padding: 24px;
  animation: fadeInLeft 0.6s ease 0.5s both;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 20px;
}

.sidebar-title svg {
  width: 20px;
  height: 20px;
  color: #f59e0b;
}

.no-recommendations p {
  font-family: 'DM Sans', sans-serif;
  color: #94a3b8;
  text-align: center;
  padding: 20px 0;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.recommendation-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recommendation-item:hover {
  background: #f8fafc;
}

.recommendation-image {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  flex-shrink: 0;
}

.recommendation-info {
  flex: 1;
  min-width: 0;
}

.recommendation-info h4 {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommendation-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.recommendation-price {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #f59e0b;
  font-size: 0.9rem;
  flex-shrink: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #1e3a5f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive */
@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-content {
    padding: 24px;
  }

  .attraction-title {
    font-size: 1.75rem;
  }

  .info-cards-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    grid-template-columns: 1fr;
  }

  .attraction-meta {
    flex-direction: column;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    height: 50vh;
    min-height: 300px;
  }

  .attraction-title {
    font-size: 1.5rem;
  }

  .description-section,
  .comment-form-card {
    padding: 20px;
  }

  .comment-card {
    padding: 16px;
  }

  .comment-avatar {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>
