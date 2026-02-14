<template>
  <div class="my-favorites-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-decoration"></div>
      <div class="header-content">
        <div class="header-icon-wrapper">
          <svg class="header-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </div>
        <h1 class="page-title">我的收藏</h1>
        <p class="page-subtitle">
          已收藏 <span class="count-badge">{{ favorites.length }}</span> 个景点
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Empty State -->
      <div v-if="favorites.length === 0 && !loading" class="empty-state">
        <div class="empty-illustration">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h2>还没有收藏任何景点</h2>
        <p>收藏心仪的景点，规划您的下一次旅程</p>
        <router-link to="/attractions" class="explore-btn">
          <span>去逛逛</span>
          <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </router-link>
      </div>

      <!-- Favorites Grid -->
      <div v-else class="favorites-grid">
        <div
          v-for="(item, index) in favorites"
          :key="item.id"
          class="favorite-card"
          :style="{ animationDelay: `${index * 0.08}s` }"
          :class="{ removing: item.removing }"
        >
          <div class="card-inner" @click="goToDetail(item.attraction.id)">
            <div class="card-image-wrapper">
              <el-image :src="item.attraction.coverImage" fit="cover" class="card-image" />
              <div class="card-overlay">
                <div class="card-rating">
                  <svg class="star-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  <span>{{ item.attraction.rating || 4.5 }}</span>
                </div>
                <div class="card-category">
                  {{ getCategoryLabel(item.attraction.category) }}
                </div>
              </div>
              <button class="favorite-indicator" @click.stop="toggleFavorite(item)">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </button>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ item.attraction.name }}</h3>

              <div class="card-meta">
                <div class="meta-item">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  <span>{{ item.attraction.address }}</span>
                </div>
                <div class="meta-item price">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/>
                    <path d="M12 18V6"/>
                  </svg>
                  <span>{{ item.attraction.price ? `¥${item.attraction.price}` : '免费' }}</span>
                </div>
              </div>

              <div class="card-actions">
                <button class="view-btn">
                  <span>查看详情</span>
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </button>
                <button class="remove-btn" @click.stop="confirmRemove(item)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 6L6 18M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>正在加载收藏列表...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const favorites = ref([])
const loading = ref(true)

const categoryMap = {
  'NATURE': '自然风光',
  'HISTORY': '人文古迹',
  'THEME': '主题乐园',
  'OTHER': '其他'
}

function getCategoryLabel(value) {
  return categoryMap[value] || value
}

function goToDetail(id) {
  router.push(`/attractions/${id}`)
}

async function fetchFavorites() {
  loading.value = true
  try {
    const res = await request.get('/comments/favorites/my/')
    favorites.value = (res.data || []).map(item => ({ ...item, removing: false }))
  } catch (error) {
    console.error('Failed to fetch favorites:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

async function confirmRemove(item) {
  try {
    await ElMessageBox.confirm(
      `确定要取消收藏 "${item.attraction.name}" 吗？`,
      '取消收藏',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await toggleFavorite(item)
  } catch (error) {
    // User cancelled
  }
}

async function toggleFavorite(item) {
  try {
    // Add removing animation
    item.removing = true

    await request.delete(`/comments/favorites/${item.attraction.id}/`)

    // Wait for animation
    await new Promise(resolve => setTimeout(resolve, 300))

    ElMessage.success('已取消收藏')
    await fetchFavorites()
  } catch (error) {
    item.removing = false
    ElMessage.error('操作失败')
  }
}

onMounted(fetchFavorites)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.my-favorites-page {
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
  background: radial-gradient(ellipse at center, rgba(245, 158, 11, 0.15) 0%, transparent 70%);
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.3);
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  margin: 0 4px;
}

/* Content Wrapper */
.content-wrapper {
  max-width: 1200px;
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
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(30, 58, 95, 0.05) 100%);
  border-radius: 50%;
  margin-bottom: 32px;
}

.empty-illustration svg {
  width: 70px;
  height: 70px;
  color: #f59e0b;
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

/* Favorites Grid */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
  animation: fadeInUp 0.6s ease;
}

.favorite-card {
  animation: fadeInUp 0.5s ease both;
}

.favorite-card.removing {
  opacity: 0;
  transform: scale(0.9);
  pointer-events: none;
}

.card-inner {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(30, 58, 95, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.card-inner:hover {
  box-shadow: 0 12px 32px rgba(30, 58, 95, 0.15);
  transform: translateY(-4px);
}

.card-image-wrapper {
  position: relative;
  aspect-ratio: 16/10;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  transition: transform 0.6s ease;
}

.card-inner:hover .card-image {
  transform: scale(1.08);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(30, 58, 95, 0.1) 0%, rgba(30, 58, 95, 0.5) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card-inner:hover .card-overlay {
  opacity: 1;
}

.card-rating {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  color: #1e3a5f;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.star-icon {
  width: 14px;
  height: 14px;
  color: #f59e0b;
}

.card-category {
  position: absolute;
  bottom: 16px;
  left: 16px;
  padding: 6px 14px;
  background: rgba(245, 158, 11, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.75rem;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.favorite-indicator {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.favorite-indicator:hover {
  transform: scale(1.1);
  background: #fef2f2;
}

.favorite-indicator svg {
  width: 22px;
  height: 22px;
  color: #ef4444;
}

.card-content {
  padding: 24px;
}

.card-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 16px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #64748b;
}

.meta-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.meta-item.price {
  color: #f59e0b;
  font-weight: 600;
}

.card-actions {
  display: flex;
  gap: 12px;
}

.view-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn:hover {
  box-shadow: 0 4px 12px rgba(30, 58, 95, 0.25);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.remove-btn {
  width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fef2f2;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #ef4444;
}

.remove-btn:hover {
  background: #ef4444;
  color: white;
}

.remove-btn svg {
  width: 18px;
  height: 18px;
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
  border-top-color: #f59e0b;
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
  .page-title {
    font-size: 2rem;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
  }

  .card-content {
    padding: 20px;
  }

  .card-actions {
    flex-direction: column;
  }

  .view-btn {
    width: 100%;
  }

  .remove-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 40px 20px 24px;
  }

  .page-title {
    font-size: 1.75rem;
  }

  .header-icon-wrapper {
    width: 64px;
    height: 64px;
  }

  .header-icon {
    width: 32px;
    height: 32px;
  }

  .favorites-grid {
    gap: 16px;
  }
}
</style>
