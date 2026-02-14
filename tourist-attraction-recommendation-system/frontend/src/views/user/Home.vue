<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-image"></div>
        <div class="hero-overlay"></div>
      </div>

      <div class="hero-content">
        <div class="hero-badge">
          <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 2C12 2 16 8 16 12C16 15.3137 13.3137 18 10 18C6.68629 18 4 15.3137 4 12C4 8 8 2 8 2"/>
            <path d="M12 22V18"/>
          </svg>
          <span>探索每一个值得去的景点</span>
        </div>

        <h1 class="hero-title">
          <span class="title-line">发现世界的</span>
          <span class="title-highlight">美好</span>
        </h1>

        <p class="hero-subtitle">个性化推荐，让每一次旅行都充满惊喜</p>

        <!-- Search Bar -->
        <div class="search-container">
          <div class="search-wrapper">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21l-4.35-4.35"/>
            </svg>
            <input
              v-model="searchKeyword"
              type="text"
              class="search-input"
              placeholder="搜索景点名称..."
              @keyup.enter="handleSearch"
            />
            <button class="search-button" @click="handleSearch">
              <span>搜索</span>
            </button>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">1000+</span>
            <span class="stat-label">精选景点</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">50K+</span>
            <span class="stat-label">真实评价</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">98%</span>
            <span class="stat-label">满意度</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Personalized Recommendations -->
      <section v-if="userStore.isLoggedIn && recommendations.length > 0" class="section recommendations-section">
        <div class="section-header">
          <div class="section-title-wrapper">
            <div class="title-icon recommendation-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">为您推荐</h2>
              <p class="section-subtitle">基于您的偏好智能推荐</p>
            </div>
          </div>
          <router-link to="/attractions" class="view-all-link">
            查看全部
            <svg class="link-arrow" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </router-link>
        </div>

        <div class="attractions-grid">
          <AttractionCard
            v-for="item in recommendations"
            :key="'rec-' + item.id"
            :attraction="item"
          />
        </div>
        <!-- Fallback empty state -->
        <div v-if="recommendations.length === 0" class="empty-state">
          <p>暂无推荐内容</p>
        </div>
      </section>

      <!-- Hot Attractions -->
      <section class="section hot-section">
        <div class="section-header">
          <div class="section-title-wrapper">
            <div class="title-icon hot-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">热门景点</h2>
              <p class="section-subtitle">大家都在去的精彩地方</p>
            </div>
          </div>
          <router-link to="/attractions" class="view-all-link">
            查看全部
            <svg class="link-arrow" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </router-link>
        </div>

        <div class="attractions-grid">
          <AttractionCard
            v-for="item in hotAttractions"
            :key="'hot-' + item.id"
            :attraction="item"
          />
        </div>
      </section>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && hotAttractions.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 6v6l4 2"/>
        </svg>
        <h3>暂无景点数据</h3>
        <p>请稍后再试</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import AttractionCard from '@/components/AttractionCard.vue'
import request from '@/api/request'

const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')
const recommendations = ref([])
const hotAttractions = ref([])
const loading = ref(true)

async function handleSearch() {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  router.push({ path: '/attractions', query: { keyword: searchKeyword.value } })
}

async function fetchRecommendations() {
  loading.value = true
  try {
    // 获取热门景点
    const hotRes = await request.get('/recommendations/popular/')
    hotAttractions.value = hotRes.data || []

    // 如果已登录，获取个性化推荐
    if (userStore.isLoggedIn) {
      const recRes = await request.get('/recommendations/personalized/')
      recommendations.value = recRes.data || []
    }
  } catch (error) {
    console.error('获取推荐失败', error)
    ElMessage.error('获取推荐失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* Hero Section */
.hero-section {
  position: relative;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-image {
  position: absolute;
  inset: 0;
  background-image: url('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&h=1080&fit=crop');
  background-size: cover;
  background-position: center;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.85) 0%, rgba(15, 23, 42, 0.75) 100%);
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 800px;
  padding: 60px 24px;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 30px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 32px;
}

.badge-icon {
  width: 18px;
  height: 18px;
  color: #fbbf24;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 64px;
  font-weight: 700;
  line-height: 1.1;
  color: white;
  margin-bottom: 24px;
}

.title-line {
  display: block;
}

.title-highlight {
  display: block;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 48px;
  font-weight: 400;
}

/* Search Bar */
.search-container {
  max-width: 600px;
  margin: 0 auto 48px;
}

.search-wrapper {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 16px;
  padding: 8px 8px 8px 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.search-wrapper:focus-within {
  box-shadow: 0 20px 60px rgba(249, 115, 22, 0.3);
  transform: translateY(-2px);
}

.search-icon {
  width: 24px;
  height: 24px;
  color: #9ca3af;
  margin-right: 12px;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  color: #1f2937;
  background: transparent;
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-button {
  padding: 14px 32px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.4);
}

.search-button:active {
  transform: translateY(0);
}

/* Hero Stats */
.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 700;
  color: #fbbf24;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
}

/* Main Content */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 80px 24px;
}

.section {
  margin-bottom: 80px;
}

.section:last-child {
  margin-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40px;
}

.section-title-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-icon svg {
  width: 28px;
  height: 28px;
}

.recommendation-icon {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(249, 115, 22, 0.15) 100%);
}

.recommendation-icon svg {
  color: #fbbf24;
}

.hot-icon {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
}

.hot-icon svg {
  color: #ef4444;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.section-subtitle {
  font-size: 14px;
  color: #6b7280;
}

.view-all-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  font-weight: 600;
  color: #f97316;
  text-decoration: none;
  transition: all 0.3s ease;
}

.view-all-link:hover {
  gap: 10px;
  color: #ea580c;
}

.link-arrow {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.view-all-link:hover .link-arrow {
  transform: translateX(4px);
}

/* Attractions Grid */
.attractions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 32px;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 80px 24px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f3f4f6;
  border-top-color: #f97316;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #6b7280;
  font-size: 16px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 24px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: #d1d5db;
}

.empty-state h3 {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.empty-state p {
  color: #6b7280;
  font-size: 16px;
}

/* Responsive */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 48px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .section-title {
    font-size: 28px;
  }

  .attractions-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 24px;
  }
}

@media (max-width: 640px) {
  .hero-section {
    min-height: 500px;
  }

  .hero-content {
    padding: 40px 20px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 16px;
    margin-bottom: 32px;
  }

  .search-wrapper {
    flex-direction: column;
    padding: 16px;
    gap: 12px;
  }

  .search-icon {
    display: none;
  }

  .search-button {
    width: 100%;
  }

  .hero-stats {
    gap: 16px;
  }

  .stat-number {
    font-size: 28px;
  }

  .stat-divider {
    display: none;
  }

  .main-content {
    padding: 40px 16px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .attractions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
