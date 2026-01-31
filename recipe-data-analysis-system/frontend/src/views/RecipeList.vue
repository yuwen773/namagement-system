<template>
  <div class="recipe-list-page">
    <!-- 页面标题区 -->
    <div class="page-header-section">
      <div class="page-header-content">
        <h1 class="page-title">探索菜谱</h1>
        <p class="page-subtitle">发现 20,000+ 精选菜谱，开启美味之旅</p>
      </div>
      <!-- 搜索框 -->
      <div class="search-section">
        <el-popover
          :visible="searchHistoryVisible && searchHistory.length > 0"
          placement="bottom"
          :width="300"
          trigger="click"
          popper-class="search-history-popover"
        >
          <template #reference>
            <el-input
              v-model="searchKeyword"
              placeholder="搜索菜谱名称或食材..."
              size="large"
              :prefix-icon="Search"
              clearable
              class="search-input"
              @focus="searchHistoryVisible = true"
              @blur="handleSearchBlur"
              @keyup.enter="handleSearch"
              @clear="handleClearSearch"
            >
              <template #append>
                <el-button :icon="Search" @click="handleSearch" />
              </template>
            </el-input>
          </template>
          <div class="search-history">
            <div class="history-header">
              <span>搜索历史</span>
              <el-button text size="small" @click="clearSearchHistory">清空</el-button>
            </div>
            <div class="history-list">
              <div
                v-for="(item, index) in searchHistory"
                :key="index"
                class="history-item"
                @click="useSearchHistory(item)"
              >
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 12c-.3 0-.5-.1-.7-.3l-4-4c-.4-.4-.4-1 0-1.4s1-.4 1.4 0L8 10.2l3.3-3.3c.4-.4 1-.4 1.4 0s.4 1 0 1.4l-4 4c-.2.2-.4.3-.7.3z"/>
                </svg>
                <span>{{ item }}</span>
                <el-button
                  text
                  size="small"
                  :icon="Close"
                  @click.stop="removeSearchHistory(index)"
                />
              </div>
            </div>
          </div>
        </el-popover>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 侧边栏筛选区 -->
      <aside class="filter-sidebar">
        <div class="filter-section">
          <div class="filter-header">
            <h3>菜系</h3>
          </div>
          <div class="filter-options">
            <el-radio-group v-model="filters.cuisine_type" @change="handleFilterChange">
              <el-radio-button label="">全部</el-radio-button>
              <el-radio-button v-for="cuisine in cuisineList" :key="cuisine.id" :label="cuisine.name">
                {{ cuisine.name }}
              </el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <div class="filter-section">
          <div class="filter-header">
            <h3>难度</h3>
          </div>
          <div class="filter-options">
            <el-radio-group v-model="filters.difficulty" @change="handleFilterChange">
              <el-radio-button label="">全部</el-radio-button>
              <el-radio-button label="easy">简单</el-radio-button>
              <el-radio-button label="medium">中等</el-radio-button>
              <el-radio-button label="hard">困难</el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <div class="filter-section">
          <div class="filter-header">
            <h3>排序</h3>
          </div>
          <div class="filter-options">
            <el-select v-model="filters.ordering" @change="handleFilterChange" class="sort-select">
              <el-option label="最新发布" value="-created_at" />
              <el-option label="点击量高到低" value="-view_count" />
              <el-option label="点击量低到高" value="view_count" />
              <el-option label="收藏量高到低" value="-favorite_count" />
              <el-option label="收藏量低到高" value="favorite_count" />
            </el-select>
          </div>
        </div>

        <!-- 浏览分类入口 -->
        <div class="filter-section category-entry">
          <div class="category-link" @click="goToCategory">
            <svg viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
              <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
            </svg>
            <span>浏览分类</span>
          </div>
        </div>

        <!-- 热门菜谱入口 -->
        <div class="filter-section hot-entry">
          <div class="hot-link" @click="goToHot">
            <svg viewBox="0 0 16 16" fill="currentColor">
              <path d="M12 1.5c-1.5 0-2.5 1-3 2.5-.5-1.5-1.5-2.5-3-2.5-2 0-3.5 2-3.5 4 0 3 4 6 6.5 8.5C10.5 10.5 14.5 7.5 14.5 4.5c0-2-1.5-4-3.5-3l1.5 2.5-2.5-1-1.5 2.5z"/>
            </svg>
            <span>热门菜谱</span>
          </div>
        </div>
      </aside>

      <!-- 菜谱列表区 -->
      <main class="recipe-list-section">
        <!-- 搜索状态提示 -->
        <div v-if="isSearching" class="search-status-bar">
          <div class="search-status-content">
            <span class="search-status-text">
              搜索结果：<strong>"{{ searchKeyword }}"</strong>
            </span>
            <span class="search-status-count">
              找到 {{ pagination.total }} 个相关菜谱
            </span>
          </div>
          <el-button size="small" @click="handleClearSearch">
            清除搜索
          </el-button>
        </div>

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
          <h3>{{ isSearching ? '未找到相关菜谱' : '暂无菜谱' }}</h3>
          <p>{{ isSearching ? `没有找到与"${searchKeyword}"相关的菜谱，试试其他关键词吧` : '试试调整筛选条件或搜索其他关键词' }}</p>
          <el-button type="primary" @click="resetFilters">
            {{ isSearching ? '清除搜索' : '重置筛选' }}
          </el-button>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Close } from '@element-plus/icons-vue'
import { getRecipeList, getCategories, searchRecipes } from '@/api/recipes'

const router = useRouter()

// 数据状态
const loading = ref(false)
const searchKeyword = ref('')
const recipeList = ref([])
const cuisineList = ref([])
const isSearching = ref(false) // 搜索状态标识
const searchHistoryVisible = ref(false) // 搜索历史弹窗显示
const searchHistory = ref([]) // 搜索历史记录

// 搜索历史存储key
const SEARCH_HISTORY_KEY = 'recipe_search_history'

// 筛选条件
const filters = reactive({
  cuisine_type: '',
  difficulty: '',
  ordering: '-created_at'
})

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

// 加载分类列表
const loadCategories = async () => {
  try {
    const response = await getCategories({ type: 'cuisine' })
    if (response.code === 200) {
      cuisineList.value = response.data || []
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
      ...filters
    }

    // 移除空值参数
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })

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

// 搜索
const handleSearch = async () => {
  const keyword = searchKeyword.value.trim()
  if (!keyword) {
    // 清空搜索，返回正常列表
    isSearching.value = false
    pagination.page = 1
    loadRecipes()
    return
  }

  // 保存搜索历史
  saveSearchHistory(keyword)

  isSearching.value = true
  loading.value = true
  pagination.page = 1
  searchHistoryVisible.value = false
  try {
    const params = {
      keyword: keyword,
      search_type: 'name',
      page: 1,
      page_size: pagination.pageSize
    }

    const response = await searchRecipes(params)
    if (response.code === 200) {
      recipeList.value = response.data.results || []
      pagination.total = response.data.count || 0
      if (pagination.total > 0) {
        ElMessage.success(`找到 ${pagination.total} 个相关菜谱`)
      }
    }
  } catch (error) {
    ElMessage.error(error.message || '搜索失败')
  } finally {
    loading.value = false
  }
}

// 执行搜索（用于分页）
const executeSearch = async () => {
  if (!searchKeyword.value.trim()) {
    isSearching.value = false
    loadRecipes()
    return
  }

  isSearching.value = true
  loading.value = true
  try {
    const params = {
      keyword: searchKeyword.value.trim(),
      search_type: 'name',
      page: pagination.page,
      page_size: pagination.pageSize
    }

    const response = await searchRecipes(params)
    if (response.code === 200) {
      recipeList.value = response.data.results || []
      pagination.total = response.data.count || 0
    }
  } catch (error) {
    ElMessage.error(error.message || '搜索失败')
  } finally {
    loading.value = false
  }
}

// 加载搜索历史
const loadSearchHistory = () => {
  try {
    const history = localStorage.getItem(SEARCH_HISTORY_KEY)
    if (history) {
      searchHistory.value = JSON.parse(history)
    }
  } catch (error) {
    console.error('加载搜索历史失败:', error)
    searchHistory.value = []
  }
}

// 保存搜索历史
const saveSearchHistory = (keyword) => {
  // 移除重复项
  const index = searchHistory.value.indexOf(keyword)
  if (index > -1) {
    searchHistory.value.splice(index, 1)
  }
  // 添加到开头
  searchHistory.value.unshift(keyword)
  // 限制历史记录数量为10条
  if (searchHistory.value.length > 10) {
    searchHistory.value = searchHistory.value.slice(0, 10)
  }
  // 保存到localStorage
  try {
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(searchHistory.value))
  } catch (error) {
    console.error('保存搜索历史失败:', error)
  }
}

// 清除搜索
const handleClearSearch = () => {
  searchKeyword.value = ''
  isSearching.value = false
  pagination.page = 1
  loadRecipes()
}

// 搜索输入框失焦处理（延迟隐藏历史）
const handleSearchBlur = () => {
  setTimeout(() => {
    searchHistoryVisible.value = false
  }, 200)
}

// 使用搜索历史
const useSearchHistory = (keyword) => {
  searchKeyword.value = keyword
  searchHistoryVisible.value = false
  handleSearch()
}

// 删除单条搜索历史
const removeSearchHistory = (index) => {
  searchHistory.value.splice(index, 1)
  try {
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(searchHistory.value))
  } catch (error) {
    console.error('更新搜索历史失败:', error)
  }
}

// 清空搜索历史
const clearSearchHistory = () => {
  searchHistory.value = []
  try {
    localStorage.removeItem(SEARCH_HISTORY_KEY)
    ElMessage.success('搜索历史已清空')
  } catch (error) {
    console.error('清空搜索历史失败:', error)
  }
}

// 筛选条件变化
const handleFilterChange = () => {
  pagination.page = 1
  loadRecipes()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  if (isSearching.value) {
    executeSearch()
  } else {
    loadRecipes()
  }
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 每页数量变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  if (isSearching.value) {
    executeSearch()
  } else {
    loadRecipes()
  }
}

// 重置筛选
const resetFilters = () => {
  filters.cuisine_type = ''
  filters.difficulty = ''
  filters.ordering = '-created_at'
  searchKeyword.value = ''
  isSearching.value = false
  pagination.page = 1
  loadRecipes()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push({ name: 'recipe-detail', params: { id } })
}

// 跳转到分类页面
const goToCategory = () => {
  router.push({ name: 'recipe-category' })
}

// 跳转到热门菜谱页面
const goToHot = () => {
  router.push({ name: 'recipe-hot' })
}

// 组件挂载
onMounted(() => {
  loadCategories()
  loadRecipes()
  loadSearchHistory()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.recipe-list-page {
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

.search-section {
  width: 400px;
}

.search-input {
  width: 100%;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 1.5px solid #e5ddd3;
  box-shadow: none;
  transition: all 0.2s ease;
}

.search-input :deep(.el-input__wrapper:hover),
.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #c2622e;
  box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);
}

.search-input :deep(.el-input-group__append) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
  border-radius: 0 12px 12px 0;
  padding: 0;
}

.search-input :deep(.el-input-group__append .el-button) {
  background: transparent;
  border: none;
  color: white;
}

/* ========== 主内容区 ========== */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2rem;
  align-items: start;
}

/* ========== 侧边栏筛选 ========== */
.filter-sidebar {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(61, 41, 20, 0.06);
  position: sticky;
  top: 100px;
}

.filter-section {
  margin-bottom: 1.5rem;
}

.filter-section:last-child {
  margin-bottom: 0;
}

.filter-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 1rem 0;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-options :deep(.el-radio-group) {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-options :deep(.el-radio-button) {
  width: 100%;
}

.filter-options :deep(.el-radio-button__inner) {
  border-radius: 8px;
  border: 1px solid #e5ddd3;
  background: white;
  color: #6b5c4d;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.filter-options :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: #c2622e;
  color: white;
  box-shadow: 0 2px 8px rgba(194, 98, 46, 0.3);
}

.sort-select {
  width: 100%;
}

.sort-select :deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid #e5ddd3;
}

/* 分类入口 */
.category-entry {
  padding: 0;
  border: 1px dashed #e5ddd3;
  background: transparent;
}

.category-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  color: #c2622e;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
}

.category-link svg {
  width: 18px;
  height: 18px;
}

.category-link:hover {
  background: rgba(194, 98, 46, 0.05);
}

/* 热门菜谱入口 */
.hot-entry {
  padding: 0;
  border: 1px dashed #e5ddd3;
  background: transparent;
}

.hot-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  color: #ff6b35;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
}

.hot-link svg {
  width: 18px;
  height: 18px;
}

.hot-link:hover {
  background: rgba(255, 107, 53, 0.08);
}

/* ========== 菜谱列表区 ========== */
.recipe-list-section {
  min-height: 600px;
}

/* 搜索状态栏 */
.search-status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #fff8f0 0%, #fff 100%);
  border: 1px solid #f0ebe3;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(61, 41, 20, 0.04);
}

.search-status-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-status-text {
  color: #6b5c4d;
  font-size: 0.95rem;
}

.search-status-text strong {
  color: #c2622e;
}

.search-status-count {
  padding: 0.25rem 0.75rem;
  background: rgba(194, 98, 46, 0.1);
  color: #c2622e;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
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
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 220px 1fr;
  }
}

@media (max-width: 968px) {
  .page-header-section {
    flex-direction: column;
    align-items: stretch;
    padding: 1.5rem 1rem 1rem;
  }

  .search-section {
    width: 100%;
  }

  .main-content {
    grid-template-columns: 1fr;
    padding: 0 1rem 1rem;
  }

  .filter-sidebar {
    position: static;
  }

  .recipe-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 640px) {
  .page-title {
    font-size: 1.5rem;
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

<style>
/* 搜索历史弹窗样式（全局样式，因为使用了popper-class） */
.search-history-popover {
  padding: 0 !important;
}

.search-history {
  padding: 0.75rem 0;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem 0.5rem;
  border-bottom: 1px solid #f0ebe3;
}

.history-header span {
  font-size: 0.85rem;
  font-weight: 600;
  color: #8b7355;
}

.history-list {
  max-height: 240px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-item:hover {
  background: rgba(194, 98, 46, 0.05);
}

.history-item svg {
  width: 14px;
  height: 14px;
  color: #b8a99a;
  flex-shrink: 0;
}

.history-item span {
  flex: 1;
  font-size: 0.9rem;
  color: #6b5c4d;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-item .el-button {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.history-item:hover .el-button {
  opacity: 1;
}
</style>
