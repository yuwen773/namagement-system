<template>
  <div class="recipe-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton animated>
        <template #template>
          <el-skeleton-item variant="image" style="width: 100%; height: 400px; border-radius: 16px;" />
          <div style="margin-top: 2rem;">
            <el-skeleton-item variant="h1" style="width: 60%; margin-bottom: 1rem;" />
            <el-skeleton-item variant="text" style="width: 40%;" />
          </div>
        </template>
      </el-skeleton>
    </div>

    <!-- 404 状态 -->
    <div v-else-if="notFound" class="not-found-container">
      <div class="not-found-content">
        <div class="not-found-icon">
          <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" stroke="currentColor" stroke-width="2" opacity="0.2"/>
            <path d="M35 35 L65 65 M65 35 L35 65" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
          </svg>
        </div>
        <h1>菜谱不存在</h1>
        <p>抱歉，您查找的菜谱已被删除或不存在</p>
        <el-button type="primary" size="large" @click="goBack">
          浏览其他菜谱
        </el-button>
      </div>
    </div>

    <!-- 菜谱详情内容 -->
    <div v-else-if="recipe" class="detail-container">
      <!-- 顶部图片区 -->
      <div class="hero-section">
        <div class="hero-image">
          <img :src="recipe.image_url || '/placeholder-food.jpg'" :alt="recipe.name" />
          <div class="image-overlay">
            <!-- 难度徽章 -->
            <span :class="['difficulty-badge', recipe.difficulty]">
              {{ difficultyText(recipe.difficulty) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 主内容区 -->
      <div class="content-wrapper">
        <!-- 左侧主内容 -->
        <main class="main-content">
          <!-- 标题区 -->
          <div class="title-section">
            <h1 class="recipe-title">{{ recipe.name }}</h1>
            <div class="recipe-meta">
              <span class="meta-item">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                </svg>
                {{ recipe.cooking_time }} 分钟
              </span>
              <span class="meta-item cuisine-tag">{{ recipe.cuisine_type }}</span>
            </div>
          </div>

          <!-- 统计信息 -->
          <div class="stats-bar">
            <div class="stat-item">
              <svg viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 12c-.3 0-.5-.1-.7-.3l-4-4c-.4-.4-.4-1 0-1.4s1-.4 1.4 0L8 10.2l3.3-3.3c.4-.4 1-.4 1.4 0s.4 1 0 1.4l-4 4c-.2.2-.4.3-.7.3z"/>
              </svg>
              <span class="stat-label">浏览</span>
              <span class="stat-value">{{ formatNumber(recipe.view_count) }}</span>
            </div>
            <div class="stat-item">
              <svg viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
              </svg>
              <span class="stat-label">收藏</span>
              <span class="stat-value">{{ formatNumber(recipe.favorite_count) }}</span>
            </div>
          </div>

          <!-- 食材列表 -->
          <section class="ingredients-section">
            <h2 class="section-title">
              <svg viewBox="0 0 16 16" fill="currentColor">
                <path d="M2 2a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V2z"/>
              </svg>
              食材清单
            </h2>
            <div v-if="recipe.ingredients && recipe.ingredients.length > 0" class="ingredients-grid">
              <div
                v-for="ingredient in recipe.ingredients"
                :key="ingredient.id"
                class="ingredient-item"
              >
                <span class="ingredient-name">{{ ingredient.name }}</span>
                <span class="ingredient-amount">{{ ingredient.amount }}</span>
              </div>
            </div>
            <div v-else class="empty-ingredients">
              <p>暂无食材信息</p>
            </div>
          </section>

          <!-- 制作步骤 -->
          <section class="steps-section">
            <h2 class="section-title">
              <svg viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zM4.5 7.5a.5.5 0 0 1 0-1h5.793l-2.147-2.146a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 7.5H4.5z"/>
              </svg>
              制作步骤
            </h2>
            <div v-if="recipe.steps" class="steps-content">
              <!-- 如果 steps 是字符串，直接显示 -->
              <div v-if="typeof recipe.steps === 'string'" class="steps-text">
                {{ recipe.steps }}
              </div>
              <!-- 如果 steps 是数组，显示列表 -->
              <div v-else-if="Array.isArray(recipe.steps)" class="steps-list">
                <div v-for="(step, index) in recipe.steps" :key="index" class="step-item">
                  <div class="step-number">{{ index + 1 }}</div>
                  <div class="step-content">{{ step }}</div>
                </div>
              </div>
            </div>
            <div v-else class="empty-steps">
              <p>暂无制作步骤</p>
            </div>
          </section>

          <!-- 口味标签 -->
          <section v-if="recipe.flavor_list && recipe.flavor_list.length > 0" class="flavors-section">
            <h2 class="section-title">
              <svg viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V7h1a1 1 0 0 1 1 1v3a3 3 0 0 1-3 3H5.5a3 3 0 0 1-3-3V8a1 1 0 0 1 1-1h1V3.5A2.5 2.5 0 0 1 8 1z"/>
              </svg>
              口味特色
            </h2>
            <div class="flavor-tags">
              <span v-for="flavor in recipe.flavor_list" :key="flavor" class="flavor-tag">
                {{ flavor }}
              </span>
            </div>
          </section>
        </main>

        <!-- 右侧操作栏 -->
        <aside class="action-sidebar">
          <!-- 收藏卡片 -->
          <div class="action-card">
            <div class="action-header">
              <h3>喜欢这个菜谱？</h3>
            </div>
            <div class="action-content">
              <el-button
                :type="isFavorited ? 'primary' : 'default'"
                :icon="isFavorited ? StarFilled : Star"
                size="large"
                class="favorite-button"
                :loading="favoriteLoading"
                @click="toggleFavorite"
              >
                {{ isFavorited ? '已收藏' : '收藏菜谱' }}
              </el-button>
              <p class="action-tip">
                {{ recipe.favorite_count }} 人已收藏这道菜
              </p>
            </div>
          </div>

          <!-- 分享卡片 -->
          <div class="action-card">
            <div class="action-header">
              <h3>分享菜谱</h3>
            </div>
            <div class="action-content">
              <el-button :icon="Share" class="share-button" @click="shareRecipe">
                分享给朋友
              </el-button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, StarFilled, Share } from '@element-plus/icons-vue'
import { getRecipeDetail, checkFavoriteStatus, addFavorite, removeFavorite } from '@/api/recipes'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 状态
const loading = ref(true)
const notFound = ref(false)
const recipe = ref(null)
const isFavorited = ref(false)
const favoriteLoading = ref(false)

// 获取菜谱详情
const loadRecipeDetail = async () => {
  loading.value = true
  notFound.value = false
  try {
    const recipeId = route.params.id
    const response = await getRecipeDetail(recipeId)
    if (response.code === 200) {
      recipe.value = response.data
      // 加载收藏状态（仅登录用户）
      if (userStore.isLoggedIn) {
        await loadFavoriteStatus()
      }
    } else if (response.code === 404) {
      notFound.value = true
    }
  } catch (error) {
    if (error.message?.includes('不存在') || error.message?.includes('404')) {
      notFound.value = true
    } else {
      ElMessage.error(error.message || '加载菜谱详情失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取收藏状态
const loadFavoriteStatus = async () => {
  try {
    const recipeId = route.params.id
    const response = await checkFavoriteStatus(recipeId)
    if (response.code === 200) {
      isFavorited.value = response.data.is_favorited
    }
  } catch (error) {
    // 静默处理，不影响页面显示
    console.error('获取收藏状态失败:', error)
  }
}

// 切换收藏状态
const toggleFavorite = async () => {
  // 未登录用户提示登录
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再收藏菜谱')
    router.push({
      name: 'login',
      query: { redirect: route.fullPath }
    })
    return
  }

  favoriteLoading.value = true
  try {
    const recipeId = route.params.id
    if (isFavorited.value) {
      // 取消收藏
      await removeFavorite(recipeId)
      isFavorited.value = false
      recipe.value.favorite_count--
      ElMessage.success('已取消收藏')
    } else {
      // 添加收藏
      await addFavorite(recipeId)
      isFavorited.value = true
      recipe.value.favorite_count++
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    favoriteLoading.value = false
  }
}

// 分享菜谱
const shareRecipe = async () => {
  const url = window.location.href
  const title = recipe.value?.name || '美味菜谱'

  if (navigator.share) {
    try {
      await navigator.share({
        title: title,
        url: url
      })
    } catch (err) {
      // 用户取消分享
    }
  } else {
    // 复制链接到剪贴板
    try {
      await navigator.clipboard.writeText(url)
      ElMessage.success('链接已复制到剪贴板')
    } catch (err) {
      ElMessage.error('复制失败，请手动复制链接')
    }
  }
}

// 返回上一页
const goBack = () => {
  if (window.history.state && window.history.state.back) {
    router.back()
  } else {
    router.push({ name: 'recipe-list' })
  }
}

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

// 组件挂载
onMounted(() => {
  loadRecipeDetail()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.recipe-detail-page {
  min-height: 100vh;
  background: #faf8f5;
  font-family: 'DM Sans', sans-serif;
  padding-top: 1rem;
}

/* ========== 加载状态 ========== */
.loading-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 2rem 0;
}

/* ========== 404 状态 ========== */
.not-found-container {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 400px;
}

.not-found-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 2rem;
  color: #b8a99a;
}

.not-found-icon svg {
  width: 100%;
  height: 100%;
}

.not-found-content h1 {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  color: #3d2914;
  margin: 0 0 1rem 0;
}

.not-found-content p {
  color: #8b7355;
  margin: 0 0 2rem 0;
}

/* ========== 详情容器 ========== */
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== 顶部图片区 ========== */
.hero-section {
  padding: 2rem 2rem 0;
}

.hero-image {
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 16px;
  overflow: hidden;
  background: #f5f0e8;
  box-shadow: 0 4px 20px rgba(61, 41, 20, 0.1);
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.3) 100%
  );
}

.difficulty-badge {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  padding: 0.5rem 1rem;
  border-radius: 24px;
  font-size: 0.9rem;
  font-weight: 600;
  backdrop-filter: blur(8px);
}

.difficulty-badge.easy {
  background: rgba(52, 168, 83, 0.95);
  color: white;
}

.difficulty-badge.medium {
  background: rgba(240, 173, 78, 0.95);
  color: white;
}

.difficulty-badge.hard {
  background: rgba(217, 83, 79, 0.95);
  color: white;
}

/* ========== 内容包装 ========== */
.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  padding: 2rem;
}

/* ========== 主内容区 ========== */
.main-content {
  min-width: 0;
}

/* 标题区 */
.title-section {
  margin-bottom: 2rem;
}

.recipe-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 1rem 0;
  line-height: 1.2;
}

.recipe-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #8b7355;
  font-size: 0.95rem;
}

.meta-item svg {
  width: 16px;
  height: 16px;
}

.cuisine-tag {
  padding: 0.25rem 0.75rem;
  background: #f5f0e8;
  color: #8b7355;
  border-radius: 20px;
  font-size: 0.85rem;
}

/* 统计栏 */
.stats-bar {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-item svg {
  width: 20px;
  height: 20px;
  color: #c2622e;
}

.stat-label {
  color: #8b7355;
  font-size: 0.9rem;
}

.stat-value {
  color: #3d2914;
  font-weight: 600;
  font-size: 1.1rem;
}

/* 通用区块样式 */
section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title svg {
  width: 24px;
  height: 24px;
  color: #c2622e;
}

/* 食材列表 */
.ingredients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.ingredient-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #faf8f5;
  border-radius: 8px;
  border: 1px solid #f0ebe3;
}

.ingredient-name {
  color: #3d2914;
  font-weight: 500;
}

.ingredient-amount {
  color: #8b7355;
  font-size: 0.9rem;
}

.empty-ingredients,
.empty-steps {
  text-align: center;
  padding: 2rem;
  color: #8b7355;
}

/* 制作步骤 */
.steps-text {
  color: #3d2914;
  line-height: 1.8;
  white-space: pre-wrap;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step-item {
  display: flex;
  gap: 1rem;
}

.step-number {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 1rem;
}

.step-content {
  flex: 1;
  color: #3d2914;
  line-height: 1.8;
  padding-top: 0.5rem;
}

/* 口味标签 */
.flavor-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.flavor-tag {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, rgba(212, 119, 58, 0.1) 0%, rgba(194, 98, 46, 0.1) 100%);
  color: #c2622e;
  border-radius: 24px;
  font-weight: 500;
}

/* ========== 侧边栏操作区 ========== */
.action-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
  position: sticky;
  top: 100px;
}

.action-header h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem;
  color: #3d2914;
  margin: 0 0 1rem 0;
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.favorite-button {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.favorite-button:not(.el-button--primary) {
  border: 2px solid #e5ddd3;
  color: #6b5c4d;
}

.favorite-button:not(.el-button--primary):hover {
  border-color: #c2622e;
  color: #c2622e;
  background: rgba(194, 98, 46, 0.05);
}

.favorite-button.el-button--primary {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
}

.action-tip {
  text-align: center;
  color: #8b7355;
  font-size: 0.85rem;
  margin: 0;
}

.share-button {
  width: 100%;
  border: 1px solid #e5ddd3;
  color: #6b5c4d;
  border-radius: 12px;
  height: 44px;
}

.share-button:hover {
  border-color: #c2622e;
  color: #c2622e;
}

/* ========== 响应式设计 ========== */
@media (max-width: 968px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .action-sidebar {
    position: static;
  }

  .action-card {
    position: static;
  }

  .hero-image {
    height: 300px;
  }

  .recipe-title {
    font-size: 2rem;
  }
}

@media (max-width: 640px) {
  .detail-container,
  .content-wrapper {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .hero-section {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .hero-image {
    height: 220px;
    border-radius: 12px;
  }

  .recipe-title {
    font-size: 1.5rem;
  }

  .stats-bar {
    flex-direction: column;
    gap: 1rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .ingredients-grid {
    grid-template-columns: 1fr;
  }
}
</style>
