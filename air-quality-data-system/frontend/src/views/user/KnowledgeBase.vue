<template>
  <div class="knowledge-base-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回概览
        </el-button>
        <div class="header-info">
          <h1 class="page-title">科普知识库</h1>
          <p class="page-subtitle">了解空气质量知识，科学守护呼吸健康</p>
        </div>
      </div>
    </div>

    <!-- Search and Filter Bar -->
    <div class="card search-card">
      <div class="search-form">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文章..."
          @keyup.enter="handleSearch"
          clearable
          @clear="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
          <template #append>
            <el-button @click="handleSearch">搜索</el-button>
          </template>
        </el-input>
        <div class="category-filter">
          <el-radio-group v-model="selectedCategory" @change="selectCategory">
            <el-radio-button
              v-for="category in categories"
              :key="category.id"
              :label="category.id"
            >
              {{ category.name }}
            </el-radio-button>
          </el-radio-group>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Articles Grid -->
    <div v-else-if="articles.length > 0" class="articles-grid">
      <div
        v-for="article in articles"
        :key="article.id"
        class="card article-card"
        @click="goToArticle(article.id)"
      >
        <div class="article-image">
          <div class="image-placeholder" :style="{ background: getCategoryGradient(article.category) }">
            <span class="placeholder-icon">{{ getCategoryIcon(article.category_name) }}</span>
          </div>
          <el-tag size="small" :style="{ background: getCategoryColor(article.category), border: 'none' }">
            {{ article.category_name || '未分类' }}
          </el-tag>
        </div>
        <div class="article-content">
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-summary">{{ article.summary || '暂无摘要' }}</p>
          <div class="article-meta">
            <span class="meta-item">
              <el-icon><Calendar /></el-icon>
              {{ formatDate(article.created_at) }}
            </span>
            <span v-if="article.view_count" class="meta-item">
              <el-icon><View /></el-icon>
              {{ article.view_count }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="card empty-card">
      <el-empty
        :description="searchQuery ? '未找到匹配的文章，请尝试其他关键词' : '该分类下暂无文章'"
        :image-size="120"
      >
        <el-button v-if="searchQuery || selectedCategory !== 'all'" type="primary" @click="resetFilters">
          清除筛选条件
        </el-button>
      </el-empty>
    </div>

    <!-- Error State -->
    <div v-if="error" class="card error-card">
      <el-result icon="error" title="加载失败" :sub-title="error">
        <template #extra>
          <el-button type="primary" @click="fetchArticles">重新加载</el-button>
        </template>
      </el-result>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1 && articles.length > 0" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 48]"
        :total="totalItems"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="goToPage"
      />
    </div>

    <!-- Quick Categories -->
    <div class="card categories-card">
      <h3 class="section-title">
        <el-icon><Folder /></el-icon>
        快速导航
      </h3>
      <div class="category-cards">
        <div
          v-for="category in categories.filter(c => c.id !== 'all')"
          :key="category.id"
          class="category-card"
          @click="selectCategory(category.id)"
        >
          <div class="category-icon" :style="{ background: category.color + '20', color: category.color }">
            {{ getCategoryIcon(category.name) }}
          </div>
          <div class="category-info">
            <h4>{{ category.name }}</h4>
            <p>{{ category.description || category.article_count || 0 }} 篇文章</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Search, Calendar, View, Folder } from '@element-plus/icons-vue'
import { getArticles, getCategories } from '@/api/airquality'

const router = useRouter()

const articles = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const selectedCategory = ref('all')
const currentPage = ref(1)
const pageSize = ref(12)
const totalItems = ref(0)

const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value))

const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = [
      { id: 'all', name: '全部', color: '#0066CC', description: '所有文章' },
      ...(response.data || [])
    ]
  } catch (err) {
    console.error('Failed to fetch categories:', err)
    categories.value = [
      { id: 'all', name: '全部', color: '#0066CC', description: '所有文章' },
      { id: 'pollution', name: '污染原理', color: '#F59E0B', icon: '🏭' },
      { id: 'health', name: '健康知识', color: '#EC4899', icon: '🏥' },
      { id: 'protection', name: '防护指南', color: '#10B981', icon: '🛡️' },
      { id: 'policy', name: '政策法规', color: '#8B5CF6', icon: '⚖️' }
    ]
  }
}

const fetchArticles = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (selectedCategory.value !== 'all') {
      params.category = selectedCategory.value
    }
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }

    const response = await getArticles(params)
    articles.value = response.data.results || response.data || []
    totalItems.value = response.data.count || articles.value.length
  } catch (err) {
    console.error('Failed to fetch articles:', err)
    error.value = '加载文章失败，请稍后重试'
    articles.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchArticles()
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  currentPage.value = 1
  fetchArticles()
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  currentPage.value = 1
  fetchArticles()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchArticles()
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchArticles()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToArticle = (articleId) => {
  router.push({ name: 'ArticleDetail', params: { id: articleId } })
}

const goBack = () => {
  router.back()
}

const formatDate = (dateString) => {
  if (!dateString) return '未知日期'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const getCategoryColor = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.color || '#0066CC'
}

const getCategoryIcon = (categoryName) => {
  const icons = {
    '污染原理': '🏭',
    '健康知识': '🏥',
    '防护指南': '🛡️',
    '政策法规': '⚖️',
    '全部': '📚'
  }
  return icons[categoryName] || '📄'
}

const getCategoryGradient = (categoryId) => {
  const gradients = {
    'pollution': 'linear-gradient(135deg, #F59E0B, #D97706)',
    'health': 'linear-gradient(135deg, #EC4899, #DB2777)',
    'protection': 'linear-gradient(135deg, #10B981, #059669)',
    'policy': 'linear-gradient(135deg, #8B5CF6, #7C3AED)',
    'all': 'linear-gradient(135deg, #0066CC, #0052A3)'
  }
  return gradients[categoryId] || 'linear-gradient(135deg, #0066CC, #0052A3)'
}

onMounted(() => {
  fetchCategories()
  fetchArticles()
})
</script>

<style scoped>
.knowledge-base-page {
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: var(--spacing-xl);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.back-button {
  font-size: 14px;
  color: var(--text-secondary);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-lg);
}

.card:last-child {
  margin-bottom: 0;
}

/* Search Card */
.search-card {
  padding: var(--spacing-lg);
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

/* Articles Grid */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.article-card {
  padding: 0;
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-base);
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.article-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 48px;
  opacity: 0.8;
}

.article-image .el-tag {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-md);
  color: white;
}

.article-content {
  padding: var(--spacing-lg);
}

.article-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-sm) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: var(--spacing-md);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-secondary);
  font-size: 13px;
}

/* Empty & Error Cards */
.empty-card,
.error-card {
  padding: var(--spacing-2xl);
  margin-bottom: var(--spacing-lg);
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  margin-bottom: var(--spacing-lg);
}

/* Categories Card */
.categories-card {
  padding: var(--spacing-lg);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-md) 0;
}

.category-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.category-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  border-left: 3px solid transparent;
}

.category-card:hover {
  background: var(--border);
  transform: translateX(4px);
}

.category-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.category-info h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-xs) 0;
}

.category-info p {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

/* Loading */
.loading-container {
  padding: var(--spacing-2xl);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
}

/* Responsive */
@media (max-width: 768px) {
  .knowledge-base-page {
    padding: var(--spacing-md);
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }

  .category-filter {
    justify-content: center;
  }

  .category-cards {
    grid-template-columns: 1fr;
  }
}
</style>
