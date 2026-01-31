<template>
  <div class="recipe-category-page">
    <!-- 页面标题区 -->
    <div class="page-header-section">
      <h1 class="page-title">{{ pageTitle }}</h1>
      <p class="page-subtitle">{{ pageSubtitle }}</p>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 分类标签切换区 -->
      <div class="category-tabs-section">
        <div class="tabs-container">
          <el-radio-group v-model="activeCategoryType" @change="handleCategoryTypeChange" class="category-type-tabs">
            <el-radio-button value="cuisine">菜系分类</el-radio-button>
            <el-radio-button value="scene">场景分类</el-radio-button>
            <el-radio-button value="crowd">人群分类</el-radio-button>
          </el-radio-group>
        </div>

        <!-- 具体分类标签 -->
        <div class="category-tags-container">
          <div
            v-for="category in currentCategoryList"
            :key="category.id"
            :class="['category-tag', { active: selectedCategory === category.name }]"
            @click="selectCategory(category.name)"
          >
            {{ category.name }}
          </div>
        </div>
      </div>

      <!-- 筛选条件区 -->
      <div class="filter-section">
        <div class="filter-header">
          <span class="filter-label">难度筛选：</span>
          <el-radio-group v-model="filters.difficulty" @change="handleFilterChange">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="easy">简单</el-radio-button>
            <el-radio-button label="medium">中等</el-radio-button>
            <el-radio-button label="hard">困难</el-radio-button>
          </el-radio-group>
        </div>
        <div class="filter-header">
          <span class="filter-label">排序方式：</span>
          <el-select v-model="filters.ordering" @change="handleFilterChange" class="sort-select">
            <el-option label="最新发布" value="-created_at" />
            <el-option label="点击量高到低" value="-view_count" />
            <el-option label="点击量低到高" value="view_count" />
            <el-option label="收藏量高到低" value="-favorite_count" />
            <el-option label="收藏量低到高" value="favorite_count" />
            <el-option label="烹饪时间短到长" value="cooking_time" />
            <el-option label="烹饪时间长到短" value="-cooking_time" />
          </el-select>
        </div>
      </div>

      <!-- 菜谱列表区 -->
      <main class="recipe-list-section">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="6" animated />
        </div>

        <!-- 空状态 -->
        <div v-else-if="recipeList.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="40" stroke="currentColor" stroke-width="2" opacity="0.2"/>
              <path d="M30 45 Q50 35, 70 45 L70 65 Q50 75, 30 65 Z" stroke="currentColor" stroke-width="2" fill="none"/>
              <text x="50" y="55" text-anchor="middle" font-size="20" fill="currentColor">?</text>
            </svg>
          </div>
          <h3>暂无菜谱</h3>
          <p>该分类下暂无菜谱，试试其他分类吧</p>
        </div>

        <!-- 菜谱卡片网格 -->
        <div v-else class="recipe-grid">
          <div
            v-for="recipe in recipeList"
            :key="recipe.id"
            class="recipe-card"
            @click="goToDetail(recipe.id)"
          >
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
                <span class="stat-item">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 12c-.3 0-.5-.1-.7-.3l-4-4c-.4-.4-.4-1 0-1.4s1-.4 1.4 0L8 10.2l3.3-3.3c.4-.4 1-.4 1.4 0s.4 1 0 1.4l-4 4c-.2.2-.4.3-.7.3z"/>
                  </svg>
                  {{ formatNumber(recipe.view_count) }}
                </span>
                <span class="stat-item">
                  <svg viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                  </svg>
                  {{ formatNumber(recipe.favorite_count) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页组件 -->
        <div v-if="pagination.total > 0" class="pagination-container">
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
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getRecipeList, getCategories } from '@/api/recipes'

const router = useRouter()
const route = useRoute()

// 数据状态
const loading = ref(false)
const recipeList = ref([])

// 分类数据
const categories = ref({
  cuisine: [],
  scene: [],
  crowd: []
})

// 当前分类类型
const activeCategoryType = ref('cuisine')
const selectedCategory = ref('')

// 筛选条件
const filters = reactive({
  difficulty: '',
  ordering: '-created_at'
})

// 分页信息
const pagination = reactive({
  page: 1,
  pageSize: 12,
  total: 0
})

// 当前分类类型对应的分类列表
const currentCategoryList = computed(() => {
  return categories.value[activeCategoryType.value] || []
})

// 页面标题
const pageTitle = computed(() => {
  if (selectedCategory.value) {
    return `${selectedCategory.value}菜谱`
  }
  const typeMap = {
    cuisine: '菜系分类',
    scene: '场景分类',
    crowd: '人群分类'
  }
  return typeMap[activeCategoryType.value] || '分类浏览'
})

// 页面副标题
const pageSubtitle = computed(() => {
  if (selectedCategory.value) {
    const count = pagination.total
    return `共找到 ${count} 道相关菜谱`
  }
  return '选择一个分类开始浏览'
})

// 分类类型对应的参数字段
const categoryTypeParamMap = {
  cuisine: 'cuisine_type',
  scene: 'scene_type',
  crowd: 'target_audience'
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

// 加载所有分类数据
const loadAllCategories = async () => {
  try {
    const [cuisineRes, sceneRes, crowdRes] = await Promise.all([
      getCategories({ type: 'cuisine' }),
      getCategories({ type: 'scene' }),
      getCategories({ type: 'crowd' })
    ])

    if (cuisineRes.code === 200) {
      categories.value.cuisine = cuisineRes.data || []
    }
    if (sceneRes.code === 200) {
      categories.value.scene = sceneRes.data || []
    }
    if (crowdRes.code === 200) {
      categories.value.crowd = crowdRes.data || []
    }
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

// 加载菜谱列表
const loadRecipes = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ordering: filters.ordering
    }

    // 添加分类筛选
    if (selectedCategory.value) {
      const paramField = categoryTypeParamMap[activeCategoryType.value]
      params[paramField] = selectedCategory.value
    }

    // 添加难度筛选
    if (filters.difficulty) {
      params.difficulty = filters.difficulty
    }

    const response = await getRecipeList(params)
    if (response.code === 200) {
      recipeList.value = response.data.results || []
      pagination.total = response.data.count || 0
    }
  } catch (error) {
    ElMessage.error(error.message || '加载菜谱列表失败')
  } finally {
    loading.value = false
  }
}

// 分类类型切换
const handleCategoryTypeChange = () => {
  selectedCategory.value = ''
  pagination.page = 1
  loadRecipes()
}

// 选择分类
const selectCategory = (categoryName) => {
  if (selectedCategory.value === categoryName) {
    // 取消选择
    selectedCategory.value = ''
  } else {
    selectedCategory.value = categoryName
  }
  pagination.page = 1
  loadRecipes()
}

// 筛选条件变化
const handleFilterChange = () => {
  pagination.page = 1
  loadRecipes()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  loadRecipes()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 每页数量变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadRecipes()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push({ name: 'recipe-detail', params: { id } })
}

// 从路由参数初始化分类
const initFromRoute = () => {
  const { type, value } = route.params

  if (type && ['cuisine', 'scene', 'crowd'].includes(type)) {
    activeCategoryType.value = type
  }

  if (value) {
    selectedCategory.value = decodeURIComponent(value)
  }

  // 从查询参数恢复筛选条件
  if (route.query.difficulty) {
    filters.difficulty = route.query.difficulty
  }
  if (route.query.ordering) {
    filters.ordering = route.query.ordering
  }
}

// 组件挂载
onMounted(async () => {
  await loadAllCategories()
  initFromRoute()
  loadRecipes()
})

// 监听路由变化
watch(() => route.params, () => {
  initFromRoute()
  loadRecipes()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.recipe-category-page {
  min-height: 100vh;
  background: #faf8f5;
  font-family: 'DM Sans', sans-serif;
}

/* ========== 页面标题区 ========== */
.page-header-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 2rem 1.5rem;
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

/* ========== 主内容区 ========== */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* ========== 分类标签切换区 ========== */
.category-tabs-section {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
}

.tabs-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0ebe3;
}

.category-type-tabs :deep(.el-radio-button__inner) {
  border-radius: 24px;
  border: 1px solid #e5ddd3;
  background: white;
  color: #6b5c4d;
  padding: 0.5rem 1.5rem;
  transition: all 0.2s ease;
}

.category-type-tabs :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
  color: white;
  box-shadow: 0 2px 8px rgba(194, 98, 46, 0.3);
}

.category-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.category-tag {
  padding: 0.5rem 1.25rem;
  background: #faf8f5;
  border: 1px solid #e5ddd3;
  border-radius: 24px;
  color: #6b5c4d;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.category-tag:hover {
  border-color: #c2622e;
  color: #c2622e;
  background: rgba(194, 98, 46, 0.05);
}

.category-tag.active {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
  color: white;
  box-shadow: 0 2px 8px rgba(194, 98, 46, 0.3);
}

/* ========== 筛选条件区 ========== */
.filter-section {
  background: white;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: center;
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filter-label {
  color: #3d2914;
  font-weight: 500;
  font-size: 0.9rem;
}

.filter-header :deep(.el-radio-group) {
  display: flex;
  gap: 0.5rem;
}

.filter-header :deep(.el-radio-button__inner) {
  border-radius: 8px;
  border: 1px solid #e5ddd3;
  background: white;
  color: #6b5c4d;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.filter-header :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
  color: white;
}

.sort-select {
  width: 180px;
}

.sort-select :deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid #e5ddd3;
}

/* ========== 菜谱列表区 ========== */
.recipe-list-section {
  min-height: 600px;
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
  margin: 0;
}

/* 菜谱网格 */
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* 菜谱卡片 */
.recipe-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeInUp 0.4s ease-out;
}

.recipe-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 28px rgba(61, 41, 20, 0.15);
}

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

.recipe-card:hover .recipe-image img {
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
  margin-bottom: 0.75rem;
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
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .back-button {
    width: 100%;
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-header {
    flex-direction: column;
    align-items: stretch;
  }

  .sort-select {
    width: 100%;
  }

  .recipe-grid {
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

  .category-tabs-section {
    padding: 1rem;
  }

  .filter-section {
    padding: 1rem;
  }

  .recipe-grid {
    grid-template-columns: 1fr;
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
