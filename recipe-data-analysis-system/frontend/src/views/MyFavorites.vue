<template>
  <div class="favorites-page">
    <!-- 页面标题区 -->
    <div class="page-header-section">
      <div class="page-header-content">
        <h1 class="page-title">我的收藏</h1>
        <p class="page-subtitle">收藏 {{ favoriteCount }} 个美味菜谱</p>
      </div>
      <!-- 排序选项 -->
      <div class="sort-options">
        <span class="sort-label">排序：</span>
        <el-radio-group v-model="ordering" @change="handleOrderChange" size="small">
          <el-radio-button value="-created_at">最新收藏</el-radio-button>
          <el-radio-button value="created_at">最早收藏</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="4" animated />
      </div>

      <!-- 空状态 -->
      <div v-else-if="favoriteList.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 92.5C74.4 92.5 94.5 72.4 94.5 48C94.5 23.6 74.4 3.5 50 3.5C25.6 3.5 5.5 23.6 5.5 48C5.5 72.4 25.6 92.5 50 92.5Z" stroke="currentColor" stroke-width="2" opacity="0.2"/>
            <path d="M35 35C35 27.3 41.3 21 49 21H51C58.7 21 65 27.3 65 35V45H35V35Z" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M50 65L58 55H42L50 65Z" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M30 70L70 70" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M35 78H65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="50" cy="48" r="8" stroke="currentColor" stroke-width="2"/>
            <path d="M47 48L49 50L53 46" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3>还没有收藏任何菜谱</h3>
        <p>去发现更多美味菜谱吧</p>
        <el-button type="primary" @click="goToRecipes">
          去浏览菜谱
        </el-button>
      </div>

      <!-- 收藏菜谱列表 -->
      <div v-else class="favorites-grid">
        <template v-for="(item, index) in favoriteList" :key="item.id">
          <div
            class="favorite-card"
            :style="{ animationDelay: `${index * 0.05}s` }"
          >
            <!-- 菜谱图片 -->
            <div class="recipe-image" @click="goToDetail(item.recipe_id)">
              <img :src="item.recipe_image || '/placeholder-food.jpg'" :alt="item.recipe_name" />
              <!-- 难度标签 -->
              <span :class="['difficulty-badge', item.difficulty]">
                {{ difficultyText(item.difficulty) }}
              </span>
              <!-- 收藏时间 -->
              <span class="collect-time">
                {{ formatCollectTime(item.created_at) }}
              </span>
            </div>

            <!-- 菜谱信息 -->
            <div class="recipe-info">
              <h3 class="recipe-name" @click="goToDetail(item.recipe_id)">{{ item.recipe_name }}</h3>
              <div class="recipe-meta">
                <span class="cuisine-tag">{{ item.cuisine_type }}</span>
                <span class="cooking-time">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                  </svg>
                  {{ item.cooking_time }} 分钟
                </span>
              </div>

              <!-- 统计信息 -->
              <div class="recipe-stats">
                <span class="stat-item">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 12c-.3 0-.5-.1-.7-.3l-4-4c-.4-.4-.4-1 0-1.4s1-.4 1.4 0L8 10.2l3.3-3.3c.4-.4 1-.4 1.4 0s.4 1 0 1.4l-4 4c-.2.2-.4.3-.7.3z"/>
                  </svg>
                  {{ formatNumber(item.view_count) }}
                </span>
                <span class="stat-item">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                  </svg>
                  {{ formatNumber(item.favorite_count) }}
                </span>
              </div>

              <!-- 操作按钮 -->
              <div class="action-buttons">
                <el-button type="primary" size="small" @click="goToDetail(item.recipe_id)">
                  查看详情
                </el-button>
                <el-button size="small" @click="handleRemoveFavorite(item.recipe_id)">
                  取消收藏
                </el-button>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- 分页组件 -->
      <div v-if="pagination.total > 0 && favoriteList.length > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[12, 24, 48]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </div>

    <!-- 取消收藏确认对话框 -->
    <el-dialog
      v-model="confirmDialogVisible"
      title="取消收藏"
      width="360px"
      center
    >
      <span>确定要取消收藏「{{ removingRecipeName }}」吗？</span>
      <template #footer>
        <el-button @click="confirmDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmRemoveFavorite">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getFavoriteList, removeFavorite } from '@/api/recipes'
import { getErrorTip } from '@/utils/errorHandler'

const router = useRouter()

// 数据状态
const loading = ref(false)
const favoriteList = ref([])
const favoriteCount = ref(0)
const ordering = ref('-created_at')
const removingRecipeId = ref(null)
const removingRecipeName = ref('')
const confirmDialogVisible = ref(false)

// 分页信息
const pagination = reactive({
  page: 1,
  pageSize: 12,
  total: 0
})

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

// 格式化收藏时间
const formatCollectTime = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date

  // 小于1小时
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes} 分钟前`
  }
  // 小于24小时
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours} 小时前`
  }
  // 小于7天
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days} 天前`
  }
  // 正常日期格式
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 加载收藏列表
const loadFavorites = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ordering: ordering.value
    }

    const response = await getFavoriteList(params)
    if (response.code === 200) {
      favoriteList.value = response.data.results || []
      pagination.total = response.data.count || 0
      favoriteCount.value = response.data.count || 0
    } else {
      ElMessage.error(response.message || '加载收藏列表失败')
    }
  } catch (error) {
    console.error('加载收藏列表失败:', error)
    ElMessage.error(getErrorTip(error).message)
  } finally {
    loading.value = false
  }
}

// 排序变化
const handleOrderChange = () => {
  pagination.page = 1
  loadFavorites()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  loadFavorites()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 每页数量变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadFavorites()
}

// 取消收藏 - 弹出确认框
const handleRemoveFavorite = (recipeId) => {
  const item = favoriteList.value.find(f => f.recipe.id === recipeId)
  if (item) {
    removingRecipeId.value = recipeId
    removingRecipeName.value = item.recipe.name
    confirmDialogVisible.value = true
  }
}

// 确认取消收藏
const confirmRemoveFavorite = async () => {
  if (!removingRecipeId.value) return

  try {
    const response = await removeFavorite(removingRecipeId.value)
    if (response.code === 200) {
      ElMessage.success('已取消收藏')
      // 从列表中移除
      favoriteList.value = favoriteList.value.filter(
        item => item.recipe.id !== removingRecipeId.value
      )
      favoriteCount.value = Math.max(0, favoriteCount.value - 1)
      pagination.total = Math.max(0, pagination.total - 1)
    } else {
      ElMessage.error(response.message || '取消收藏失败')
    }
  } catch (error) {
    console.error('取消收藏失败:', error)
    ElMessage.error(getErrorTip(error).message)
  } finally {
    confirmDialogVisible.value = false
    removingRecipeId.value = null
    removingRecipeName.value = ''
  }
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push({ name: 'recipe-detail', params: { id } })
}

// 跳转到菜谱列表页
const goToRecipes = () => {
  router.push({ name: 'recipe-list' })
}

// 组件挂载
onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.favorites-page {
  min-height: 100vh;
  background: #faf8f5;
  font-family: 'DM Sans', sans-serif;
}

/* ========== 页面标题区 ========== */
.page-header-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 2rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.page-header-content {
  flex: 1;
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
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-label {
  color: #8b7355;
  font-size: 0.9rem;
}

.sort-options :deep(.el-radio-group) {
  display: flex;
}

.sort-options :deep(.el-radio-button__inner) {
  border-radius: 8px;
  border: 1px solid #e5ddd3;
  background: white;
  color: #6b5c4d;
  transition: all 0.2s ease;
}

.sort-options :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
  color: white;
}

/* ========== 主内容区 ========== */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
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
  padding: 6rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
  color: #b8a99a;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #8b7355;
  margin: 0 0 1.5rem 0;
}

/* 收藏菜谱网格 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* 收藏卡片 */
.favorite-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.08);
  transition: all 0.3s ease;
  animation: fadeInUp 0.4s ease-out both;
}

.favorite-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 28px rgba(61, 41, 20, 0.15);
}

.recipe-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f5f0e8;
  cursor: pointer;
}

.recipe-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.favorite-card:hover .recipe-image img {
  transform: scale(1.05);
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

.collect-time {
  position: absolute;
  bottom: 12px;
  left: 12px;
  padding: 0.25rem 0.5rem;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 6px;
  font-size: 0.75rem;
}

.recipe-info {
  padding: 1rem;
}

.recipe-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 0.75rem 0;
  cursor: pointer;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  transition: color 0.2s ease;
}

.recipe-name:hover {
  color: #c2622e;
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
  color: #8b7355;
  font-size: 0.85rem;
}

.stat-item svg {
  width: 14px;
  height: 14px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f5f0e8;
}

.action-buttons .el-button {
  flex: 1;
}

/* ========== 分页 ========== */
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
}

.pagination-container :deep(.el-pagination) {
  --el-pagination-button-bg-color: white;
  --el-pagination-button-color: #6b5c4d;
  --el-pagination-button-border-color: #e5ddd3;
  --el-pagination-hover-color: #c2622e;
}

.pagination-container :deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
}

/* ========== 响应式设计 ========== */
@media (max-width: 968px) {
  .page-header-section {
    flex-direction: column;
    align-items: stretch;
    padding: 1.5rem 1rem 1rem;
  }

  .sort-options {
    justify-content: flex-start;
  }

  .main-content {
    padding: 0 1rem 1rem;
  }

  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.5rem;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
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
