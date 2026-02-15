<template>
  <div class="knowledge-base-page grid-background">
    <!-- Floating Particles -->
    <div class="particles">
      <div v-for="i in 12" :key="i" class="particle" :style="{ '--delay': `${i * 0.6}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
    </div>

    <div class="container">
      <!-- Header -->
      <header class="page-header fade-in-down">
        <h1 class="page-title">
          <span class="title-icon">📚</span>
          科普知识库
        </h1>
        <p class="page-subtitle">了解空气质量知识，科学守护呼吸健康</p>
      </header>

      <!-- Search and Filter Bar -->
      <div class="search-filter-bar glass-card fade-in" style="animation-delay: 0.1s">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索文章..."
            @keyup.enter="handleSearch"
            class="search-input"
          />
          <button class="search-btn" @click="handleSearch">搜索</button>
        </div>
        <div class="category-filter">
          <button
            v-for="category in categories"
            :key="category.id"
            :class="['category-btn', { active: selectedCategory === category.id }]"
            :style="{ '--category-color': category.color || '#60a5fa' }"
            @click="selectCategory(category.id)"
          >
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container fade-in">
        <div class="loading-spinner"></div>
        <p>加载文章中...</p>
      </div>

      <!-- Articles Grid -->
      <div v-else-if="articles.length > 0" class="articles-grid">
        <div
          v-for="article in articles"
          :key="article.id"
          class="article-card glass-card hover-scale fade-in"
          :style="{ 'animation-delay': `${Math.min(articles.indexOf(article) * 0.05 + 0.2, 0.8)}s` }"
          @click="goToArticle(article.id)"
        >
          <div class="article-image">
            <div class="image-placeholder" :style="{ background: getArticleGradient(article.category) }">
              <span class="placeholder-icon">{{ getCategoryIcon(article.category_name) }}</span>
            </div>
            <span class="article-category" :style="{ background: getCategoryColor(article.category) }">
              {{ article.category_name || '未分类' }}
            </span>
          </div>
          <div class="article-content">
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-summary">{{ article.summary || '暂无摘要' }}</p>
            <div class="article-meta">
              <span class="meta-item">
                <span class="meta-icon">📅</span>
                {{ formatDate(article.created_at) }}
              </span>
              <span v-if="article.view_count" class="meta-item">
                <span class="meta-icon">👁️</span>
                {{ article.view_count }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-container glass-card fade-in">
        <span class="empty-icon">📭</span>
        <h3>暂无文章</h3>
        <p>{{ searchQuery ? '未找到匹配的文章，请尝试其他关键词' : '该分类下暂无文章' }}</p>
        <button v-if="searchQuery || selectedCategory !== 'all'" class="reset-btn" @click="resetFilters">
          清除筛选条件
        </button>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-container glass-card">
        <span class="error-icon">⚠️</span>
        <h3>加载失败</h3>
        <p>{{ error }}</p>
        <button class="retry-btn" @click="fetchArticles">重新加载</button>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1 && articles.length > 0" class="pagination glass-card fade-in">
        <button
          class="page-btn"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
        >
          <span>‹</span>
        </button>
        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            :class="['page-num', { active: page === currentPage }]"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </div>
        <button
          class="page-btn"
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
        >
          <span>›</span>
        </button>
        <div class="page-info">
          <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
          <span class="total-count">共 {{ totalItems }} 篇</span>
        </div>
      </div>

      <!-- Quick Categories -->
      <div class="quick-categories glass-card fade-in" style="animation-delay: 0.3s">
        <h3 class="section-title">
          <span class="title-icon">🏷️</span>
          快速导航
        </h3>
        <div class="category-cards">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-card"
            :style="{ '--category-color': category.color || '#60a5fa' }"
            @click="selectCategory(category.id)"
          >
            <span class="category-card-icon">{{ getCategoryIcon(category.name) }}</span>
            <div class="category-card-info">
              <h4>{{ category.name }}</h4>
              <p>{{ category.description || category.article_count || 0 }} 篇文章</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
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

const visiblePages = computed(() => {
  const pages = []
  const showPages = 5
  let start = Math.max(1, currentPage.value - Math.floor(showPages / 2))
  let end = Math.min(totalPages.value, start + showPages - 1)

  if (end - start < showPages - 1) {
    start = Math.max(1, end - showPages + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = [
      { id: 'all', name: '全部', color: '#60a5fa', icon: '📚' },
      ...(response.data || [])
    ]
  } catch (err) {
    console.error('Failed to fetch categories:', err)
    categories.value = [
      { id: 'all', name: '全部', color: '#60a5fa', icon: '📚' },
      { id: 'pollution', name: '污染原理', color: '#f59e0b', icon: '🏭' },
      { id: 'health', name: '健康知识', color: '#ec4899', icon: '🏥' },
      { id: 'protection', name: '防护指南', color: '#10b981', icon: '🛡️' },
      { id: 'policy', name: '政策法规', color: '#8b5cf6', icon: '⚖️' }
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
  return category?.color || '#60a5fa'
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

const getArticleGradient = (categoryId) => {
  const gradients = {
    'pollution': 'linear-gradient(135deg, #f59e0b, #d97706)',
    'health': 'linear-gradient(135deg, #ec4899, #db2777)',
    'protection': 'linear-gradient(135deg, #10b981, #059669)',
    'policy': 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
    'all': 'linear-gradient(135deg, #60a5fa, #3b82f6)'
  }
  return gradients[categoryId] || 'linear-gradient(135deg, #60a5fa, #3b82f6)'
}

onMounted(() => {
  fetchCategories()
  fetchArticles()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

.knowledge-base-page {
  min-height: 100vh;
  padding: 2rem;
  position: relative;
  overflow-x: hidden;
  font-family: 'IBM Plex Sans', sans-serif;
  color: #e2e8f0;
}

.grid-background {
  background-color: #020617;
  background-image:
    linear-gradient(rgba(30, 41, 59, 0.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30, 41, 59, 0.3) 1px, transparent 1px);
  background-size: 50px 50px;
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(148, 163, 184, 0.3);
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
  animation-delay: var(--delay);
  left: var(--x);
  top: var(--y);
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100vh) translateX(50px); opacity: 0; }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-icon {
  font-size: 2.5rem;
  -webkit-text-fill-color: initial;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #94a3b8;
  font-weight: 300;
}

/* Search and Filter Bar */
.search-filter-bar {
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  align-items: center;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 12px;
  padding: 0.5rem 1rem;
  margin-bottom: 1rem;
}

.search-icon {
  font-size: 1.2rem;
  margin-right: 0.75rem;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #f1f5f9;
  font-size: 1rem;
  outline: none;
  font-family: 'IBM Plex Sans', sans-serif;
}

.search-input::placeholder {
  color: #64748b;
}

.search-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.category-btn {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #cbd5e1;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn:hover {
  background: rgba(15, 23, 42, 0.6);
  border-color: var(--category-color);
}

.category-btn.active {
  background: var(--category-color);
  border-color: var(--category-color);
  color: white;
  box-shadow: 0 4px 15px var(--category-color);
}

/* Articles Grid */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.article-card {
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.article-image {
  position: relative;
  height: 180px;
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
  font-size: 4rem;
  opacity: 0.8;
}

.article-category {
  position: absolute;
  top: 1rem;
  left: 1rem;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.article-content {
  padding: 1.25rem;
}

.article-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.75rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  color: #94a3b8;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #64748b;
  font-size: 0.85rem;
  font-family: 'JetBrains Mono', monospace;
}

.meta-icon {
  font-size: 1rem;
}

/* Empty State */
.empty-container {
  text-align: center;
  padding: 4rem 2rem;
  margin-bottom: 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-container h3 {
  color: #f1f5f9;
  margin-bottom: 0.5rem;
}

.empty-container p {
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

.reset-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
}

/* Error State */
.error-container {
  text-align: center;
  padding: 4rem 2rem;
  margin-bottom: 2rem;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.error-container h3 {
  color: #f1f5f9;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: #94a3b8;
  margin-bottom: 1rem;
}

.retry-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
}

.page-btn {
  width: 40px;
  height: 40px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
  color: #60a5fa;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-num {
  min-width: 40px;
  height: 40px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', monospace;
}

.page-num:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
  color: #60a5fa;
}

.page-num.active {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-color: #3b82f6;
  color: white;
}

.page-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 1rem;
  padding-left: 1rem;
  border-left: 1px solid rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  font-size: 0.85rem;
}

.total-count {
  font-size: 0.75rem;
  color: #64748b;
}

/* Quick Categories */
.quick-categories {
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.title-icon {
  font-size: 1.5rem;
}

.category-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.category-card {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid var(--category-color);
}

.category-card:hover {
  background: rgba(15, 23, 42, 0.6);
  border-color: var(--category-color);
  transform: translateX(5px);
}

.category-card-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(96, 165, 250, 0.1);
  border-radius: 10px;
}

.category-card-info h4 {
  color: #f1f5f9;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.category-card-info p {
  color: #94a3b8;
  font-size: 0.85rem;
}

/* Loading State */
.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  margin-bottom: 2rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1.5rem;
  border: 3px solid rgba(96, 165, 250, 0.2);
  border-top-color: #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-container p {
  color: #94a3b8;
}

/* Glass Card */
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  transition: all 0.3s ease;
}

/* Animations */
.fade-in {
  animation: fade-in 0.5s ease forwards;
  opacity: 0;
}

@keyframes fade-in {
  to { opacity: 1; }
}

.fade-in-down {
  animation: fade-in-down 0.6s ease forwards;
  opacity: 0;
}

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hover-scale {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-scale:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .knowledge-base-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }

  .search-box {
    flex-direction: column;
    gap: 0.75rem;
  }

  .search-input {
    width: 100%;
  }

  .category-filter {
    justify-content: center;
  }

  .pagination {
    flex-wrap: wrap;
  }

  .page-info {
    width: 100%;
    border-left: none;
    border-top: 1px solid rgba(148, 163, 184, 0.2);
    padding-left: 0;
    padding-top: 0.75rem;
    margin-left: 0;
  }

  .category-cards {
    grid-template-columns: 1fr;
  }
}
</style>
