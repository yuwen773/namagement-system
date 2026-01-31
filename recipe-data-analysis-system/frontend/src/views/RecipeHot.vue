<template>
  <div class="recipe-hot-page">
    <!-- 顶部导航栏 -->
    <header class="page-header">
      <div class="header-content">
        <!-- 返回按钮 -->
        <el-button class="back-button" :icon="ArrowLeft" @click="goBack" circle />
        <div class="header-left">
          <div class="title-row">
            <!-- 火焰图标 -->
            <div class="fire-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 23c-3.866 0-7-3.134-7-7 0-2.5 1.5-5 2.5-7.5.833-2 1.5-3.5 1.5-5.5 0 2 1.5 3.5 3 5.5s2.5 5 2.5 7.5c0 3.866-3.134 7-7 7zm0-2c2.761 0 5-2.239 5-5 0-1.5-.5-3-1.5-5-1-2-1.5-3.5-1.5-4.5 0 1-.5 2.5-1.5 4.5s-1.5 3.5-1.5 5c0 2.761 2.239 5 5 5z"/>
              </svg>
            </div>
            <h1 class="page-title">热门菜谱</h1>
          </div>
          <p class="page-subtitle">最受欢迎的美味菜谱，精选推荐</p>
        </div>
        <!-- 排序选择 -->
        <div class="sort-section">
          <el-radio-group v-model="sortBy" @change="handleSortChange" class="sort-group">
            <el-radio-button value="view_count">
              <span class="sort-option">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 12c-.3 0-.5-.1-.7-.3l-4-4c-.4-.4-.4-1 0-1.4s1-.4 1.4 0L8 10.2l3.3-3.3c.4-.4 1-.4 1.4 0s.4 1 0 1.4l-4 4c-.2.2-.4.3-.7.3z"/>
                </svg>
                按点击量
              </span>
            </el-radio-button>
            <el-radio-button value="favorite_count">
              <span class="sort-option">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                </svg>
                按收藏量
              </span>
            </el-radio-button>
          </el-radio-group>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="6" animated />
      </div>

      <!-- 空状态 -->
      <div v-else-if="recipeList.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M30 70 Q50 80, 70 70 L70 55 Q50 45, 30 55 Z" stroke="currentColor" stroke-width="2" fill="none"/>
            <text x="50" y="65" text-anchor="middle" font-size="16" fill="currentColor">?</text>
          </svg>
        </div>
        <h3>暂无热门菜谱</h3>
        <p>快来探索更多美味菜谱吧</p>
        <el-button type="primary" @click="goToList">浏览菜谱</el-button>
      </div>

      <!-- 菜谱卡片网格 -->
      <div v-else>
        <!-- 排序说明 -->
        <div class="sort-notice">
          <svg viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 16A8 8 0 1 1 8 0a8 8 0 0 1 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
          </svg>
          <span>当前按 <strong>{{ sortBy === 'view_count' ? '点击量' : '收藏量' }}</strong> 排序，展示 Top {{ recipeList.length }} 菜谱</span>
        </div>

        <!-- 排行榜样式卡片 -->
        <div class="recipe-grid-hot">
          <div
            v-for="(recipe, index) in recipeList"
            :key="recipe.id"
            :class="['recipe-card-hot', `rank-${index + 1}`]"
            @click="goToDetail(recipe.id)"
          >
            <!-- 排名徽章 -->
            <div v-if="index < 10" :class="['rank-badge', `rank-${index + 1}`]">
              <span v-if="index === 0" class="rank-icon">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M2.5.5A.5.5 0 0 1 3 0h10a.5.5 0 0 1 .5.5c0 .538-.012 1.05-.034 1.536a3 3 0 1 1-1.133 5.89c-.79 1.865-1.878 2.777-2.833 3.011v2.173l1.425.356c.194.048.377.135.537.255L13.3 15.1a.5.5 0 0 1-.3.9H3a.5.5 0 0 1-.3-.9l1.838-1.379c.16-.12.343-.207.537-.255L6.5 13.11v-2.173c-.955-.234-2.043-1.146-2.833-3.012a3 3 0 1 1-1.132-5.89A33.076 33.076 0 0 1 2.5.5zm.099 2.54a2 2 0 0 0 .72 3.935c-.333-1.05-.588-2.346-.72-3.935zm10.083 3.935a2 2 0 0 0 .72-3.935c-.133 1.59-.388 2.885-.72 3.935z"/>
                </svg>
              </span>
              <span v-else-if="index === 1" class="rank-icon">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/>
                </svg>
              </span>
              <span v-else-if="index === 2" class="rank-icon">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M4 11.793V.5H3v11.293l-.854-.853L1.293 12l2 2 2-2-.146-.147-.146.147H4zm8-9.293V.5H7v2h5v9.293l-.854-.853L10.293 12l2 2 2-2-.146-.147-.146.147H13V2.5h-1z"/>
                </svg>
              </span>
              <span v-else class="rank-number">{{ index + 1 }}</span>
            </div>

            <!-- 菜谱图片 -->
            <div class="recipe-image">
              <img :src="recipe.image_url || '/placeholder-food.jpg'" :alt="recipe.name" />
              <!-- 难度标签 -->
              <span :class="['difficulty-badge', recipe.difficulty]">
                {{ difficultyText(recipe.difficulty) }}
              </span>
            </div>

            <!-- 菜谱信息 -->
            <div class="recipe-info">
              <h3 class="recipe-name">{{ recipe.name }}</h3>
              <div class="recipe-meta">
                <span class="cuisine-tag">{{ recipe.cuisine_type }}</span>
                <span class="cooking-time">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                  </svg>
                  {{ recipe.cooking_time }} 分钟
                </span>
              </div>

              <!-- 统计信息 -->
              <div class="recipe-stats">
                <span class="stat-item view-count">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 12c-.3 0-.5-.1-.7-.3l-4-4c-.4-.4-.4-1 0-1.4s1-.4 1.4 0L8 10.2l3.3-3.3c.4-.4 1-.4 1.4 0s.4 1 0 1.4l-4 4c-.2.2-.4.3-.7.3z"/>
                  </svg>
                  {{ formatNumber(recipe.view_count) }}
                </span>
                <span class="stat-item favorite-count">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                  </svg>
                  {{ formatNumber(recipe.favorite_count) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getHotRecipes } from '@/api/recipes'

const router = useRouter()

// 数据状态
const loading = ref(false)
const recipeList = ref([])
const sortBy = ref('view_count') // view_count 或 favorite_count

// 难度文本映射
const difficultyText = (difficulty) => {
  const map = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return map[difficulty] || '未知'
}

// 格式化数字
const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

// 加载热门菜谱
const loadHotRecipes = async () => {
  loading.value = true
  try {
    const params = {
      sort_by: sortBy.value,
      limit: 50 // 获取 Top 50
    }

    const response = await getHotRecipes(params)
    if (response.code === 200) {
      recipeList.value = response.data.results || []
    }
  } catch (error) {
    ElMessage.error(error.message || '加载热门菜谱失败')
  } finally {
    loading.value = false
  }
}

// 排序变化
const handleSortChange = () => {
  loadHotRecipes()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push({ name: 'recipe-detail', params: { id } })
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 跳转到列表页
const goToList = () => {
  router.push({ name: 'recipe-list' })
}

// 组件挂载
onMounted(() => {
  loadHotRecipes()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.recipe-hot-page {
  min-height: 100vh;
  background: #faf8f5;
  font-family: 'DM Sans', sans-serif;
}

/* ========== 顶部导航栏 ========== */
.page-header {
  background: white;
  border-bottom: 1px solid #f0ebe3;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.04);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.back-button {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  background: #f5f0e8;
  border: 1px solid #e5ddd3;
  color: #6b5c4d;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: #c2622e;
  border-color: #c2622e;
  color: white;
  transform: translateX(-2px);
}

.header-left {
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.fire-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s ease-in-out infinite;
}

.fire-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 8px rgba(255, 107, 53, 0);
  }
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: #8b7355;
  font-size: 0.95rem;
  margin: 0.25rem 0 0 0;
  margin-left: 3.25rem;
}

/* 排序选择 */
.sort-section {
  flex-shrink: 0;
}

.sort-group :deep(.el-radio-button__inner) {
  border-radius: 24px;
  border: 1.5px solid #e5ddd3;
  background: white;
  color: #6b5c4d;
  padding: 0.6rem 1.25rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.sort-group :deep(.el-radio-button:first-child .el-radio-button__inner) {
  border-radius: 24px 0 0 24px;
}

.sort-group :deep(.el-radio-button:last-child .el-radio-button__inner) {
  border-radius: 0 24px 24px 0;
}

.sort-group :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
  color: white;
  box-shadow: 0 4px 12px rgba(194, 98, 46, 0.3);
}

.sort-option {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.sort-option svg {
  width: 16px;
  height: 16px;
}

/* ========== 主内容区 ========== */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  animation: fadeInUp 0.4s ease-out;
}

/* 加载状态 */
.loading-container {
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
}

.empty-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 1.5rem;
  color: #b8a99a;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #8b7355;
  margin: 0 0 1.5rem 0;
}

/* 排序说明 */
.sort-notice {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(212, 119, 58, 0.08) 0%, rgba(194, 98, 46, 0.05) 100%);
  border-radius: 12px;
  color: #8b7355;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.sort-notice svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.sort-notice strong {
  color: #c2622e;
  font-weight: 600;
}

/* 菜谱网格 - 热门排行榜样式 */
.recipe-grid-hot {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* 菜谱卡片 */
.recipe-card-hot {
  position: relative;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeInUp 0.4s ease-out;
  animation-delay: calc(var(--index, 0) * 0.05s);
}

.recipe-card-hot:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(61, 41, 20, 0.18);
}

/* 排名徽章 */
.rank-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  font-weight: 700;
  font-size: 0.85rem;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.rank-badge.rank-1 {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #8b6914;
}

.rank-badge.rank-2 {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
  color: #5a5a5a;
}

.rank-badge.rank-3 {
  background: linear-gradient(135deg, #cd7f32 0%, #e59a48 100%);
  color: #6b4423;
}

.rank-badge.rank-4,
.rank-badge.rank-5,
.rank-badge.rank-6,
.rank-badge.rank-7,
.rank-badge.rank-8,
.rank-badge.rank-9,
.rank-badge.rank-10 {
  background: rgba(61, 41, 20, 0.7);
  color: white;
}

.rank-icon {
  width: 20px;
  height: 20px;
}

.rank-icon svg {
  width: 100%;
  height: 100%;
}

.rank-number {
  font-size: 0.9rem;
}

/* Top 3 卡片特殊样式 */
.recipe-card-hot.rank-1 {
  border: 2px solid #ffd700;
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.25);
}

.recipe-card-hot.rank-2 {
  border: 2px solid #d4d4d4;
  box-shadow: 0 4px 20px rgba(192, 192, 192, 0.25);
}

.recipe-card-hot.rank-3 {
  border: 2px solid #cd7f32;
  box-shadow: 0 4px 20px rgba(205, 127, 50, 0.25);
}

/* 菜谱图片 */
.recipe-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f5f0e8;
}

.recipe-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.recipe-card-hot:hover .recipe-image img {
  transform: scale(1.08);
}

.difficulty-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(8px);
}

.difficulty-badge.easy {
  background: rgba(52, 168, 83, 0.9);
  color: white;
}

.difficulty-badge.medium {
  background: rgba(240, 173, 78, 0.9);
  color: white;
}

.difficulty-badge.hard {
  background: rgba(217, 83, 79, 0.9);
  color: white;
}

.recipe-info {
  padding: 1rem;
}

.recipe-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 0.75rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.recipe-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.cuisine-tag {
  padding: 0.25rem 0.5rem;
  background: #f5f0e8;
  color: #8b7355;
  border-radius: 6px;
  font-size: 0.8rem;
}

.cooking-time {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #8b7355;
  font-size: 0.85rem;
}

.cooking-time svg {
  width: 14px;
  height: 14px;
}

.recipe-stats {
  display: flex;
  gap: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f5f0e8;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
}

.stat-item svg {
  width: 14px;
  height: 14px;
}

.stat-item.view-count {
  color: #6b5c4d;
}

.stat-item.favorite-count {
  color: #e74c3c;
}

/* ========== 响应式设计 ========== */
@media (max-width: 968px) {
  .header-content {
    flex-wrap: wrap;
  }

  .back-button {
    order: -1;
  }

  .sort-section {
    width: 100%;
    order: 3;
  }

  .sort-group {
    width: 100%;
  }

  .sort-group :deep(.el-radio-button) {
    flex: 1;
  }

  .page-subtitle {
    margin-left: 0;
  }

  .recipe-grid-hot {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 640px) {
  .header-content {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .main-content {
    padding: 1rem;
  }

  .recipe-grid-hot {
    grid-template-columns: 1fr;
  }

  .fire-icon {
    width: 32px;
    height: 32px;
  }

  .fire-icon svg {
    width: 20px;
    height: 20px;
  }
}

/* ========== 动画 ========== */
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
</style>
