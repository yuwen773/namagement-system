<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getProductListApi, getCategoryListApi } from '@/api'
import { formatCurrency } from '@/utils'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const products = ref([])
const categories = ref([])
const totalCount = ref(0)

// Filters
const selectedCategory = ref(null)
const priceRange = ref([])
const sortBy = ref('default')
const searchQuery = ref('')

// Pagination
const currentPage = ref(1)
const pageSize = ref(12)

// Price options
const priceOptions = [
  { label: '全部价格', value: '' },
  { label: '¥500 以下', value: '0-500' },
  { label: '¥500 - ¥2000', value: '500-2000' },
  { label: '¥2000 - ¥5000', value: '2000-5000' },
  { label: '¥5000 - ¥10000', value: '5000-10000' },
  { label: '¥10000 以上', value: '10000-' }
]

// Sort options
const sortOptions = [
  { label: '默认排序', value: 'default' },
  { label: '价格从低到高', value: 'price_asc' },
  { label: '价格从高到低', value: 'price_desc' },
  { label: '销量优先', value: 'sales' },
  { label: '最新上架', value: 'newest' }
]

onMounted(async () => {
  await fetchCategories()
  await fetchProducts()
})

// Watch route query changes
watch(() => route.query, async () => {
  if (route.query.category_id) {
    selectedCategory.value = parseInt(route.query.category_id)
  }
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
  await fetchProducts()
}, { immediate: true })

async function fetchCategories() {
  try {
    const response = await getCategoryListApi()
    categories.value = response?.data || []
  } catch (error) {
    console.error('Failed to fetch categories:', error)
    categories.value = []
  }
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (selectedCategory.value) {
      params.category_id = selectedCategory.value
    }
    if (priceRange.value[0] !== undefined) {
      params.min_price = priceRange.value[0]
    }
    if (priceRange.value[1] !== undefined) {
      params.max_price = priceRange.value[1]
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (sortBy.value === 'price_asc') {
      params.ordering = 'price'
    } else if (sortBy.value === 'price_desc') {
      params.ordering = '-price'
    } else if (sortBy.value === 'sales') {
      params.ordering = '-sales'
    } else if (sortBy.value === 'newest') {
      params.ordering = '-created_at'
    }

    const data = await getProductListApi(params)
    products.value = data.results || []
    totalCount.value = data.count || 0
  } finally {
    loading.value = false
  }
}

function handleCategoryClick(categoryId) {
  selectedCategory.value = categoryId
  currentPage.value = 1
  fetchProducts()
}

function handlePriceChange() {
  currentPage.value = 1
  fetchProducts()
}

function handleSortChange() {
  currentPage.value = 1
  fetchProducts()
}

function handleSearch() {
  currentPage.value = 1
  fetchProducts()
}

function handlePageChange(page) {
  currentPage.value = page
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function goToProduct(id) {
  router.push({ name: 'product-detail', params: { id } })
}

const filteredCategories = computed(() => {
  // Return only top-level categories
  return categories.value.filter(c => !c.parent)
})

const hasActiveFilters = computed(() => {
  return selectedCategory.value || priceRange.value.length > 0 || searchQuery.value
})

function clearFilters() {
  selectedCategory.value = null
  priceRange.value = []
  searchQuery.value = ''
  currentPage.value = 1
  fetchProducts()
}
</script>

<template>
  <div class="product-list-view">
    <!-- Hero Header with Dynamic Background -->
    <div class="hero-header">
      <div class="hero-mesh"></div>
      <div class="hero-grid"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2"/>
            <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V5H9Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>零件目录</span>
        </div>
        <h1 class="hero-title">探索改装配件</h1>
        <p class="hero-subtitle">为您的座驾找到完美的性能升级组件</p>

        <!-- Quick Stats -->
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">{{ totalCount }}+</span>
            <span class="stat-label">精选配件</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">{{ filteredCategories.length }}</span>
            <span class="stat-label">分类系列</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">100%</span>
            <span class="stat-label">正品保证</span>
          </div>
        </div>
      </div>

      <!-- Decorative Elements -->
      <div class="hero-circle hero-circle-1"></div>
      <div class="hero-circle hero-circle-2"></div>
    </div>

    <!-- Main Content -->
    <div class="main-container">
      <!-- Sidebar Filters -->
      <aside class="filters-sidebar">
        <!-- Active Filters Bar -->
        <div v-if="hasActiveFilters" class="active-filters-bar">
          <div class="active-filters-content">
            <span class="active-label">已选筛选:</span>
            <div class="active-tags">
              <span v-if="selectedCategory" class="filter-tag">
                {{ categories.find(c => c.id === selectedCategory)?.name }}
                <button @click="selectedCategory = null; fetchProducts()" class="tag-close">×</button>
              </span>
              <span v-if="priceRange.length" class="filter-tag">
                价格区间
                <button @click="priceRange = []; fetchProducts()" class="tag-close">×</button>
              </span>
              <span v-if="searchQuery" class="filter-tag">
                "{{ searchQuery }}"
                <button @click="searchQuery = ''; fetchProducts()" class="tag-close">×</button>
              </span>
            </div>
            <button @click="clearFilters" class="clear-all-btn">清除全部</button>
          </div>
        </div>

        <!-- Filter Sections -->
        <div class="filter-sections">
          <!-- Categories -->
          <div class="filter-section">
            <div class="filter-header">
              <svg class="filter-icon" viewBox="0 0 24 24" fill="none">
                <path d="M4 6h16M4 12h16M4 18h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <h3 class="filter-title">商品分类</h3>
            </div>
            <div class="category-list">
              <div
                v-for="category in filteredCategories"
                :key="category.id"
                :class="['category-item', { active: selectedCategory === category.id }]"
                @click="handleCategoryClick(category.id)"
              >
                <span class="category-name">{{ category.name }}</span>
                <div class="category-indicator"></div>
              </div>
            </div>
          </div>

          <!-- Price Range -->
          <div class="filter-section">
            <div class="filter-header">
              <svg class="filter-icon" viewBox="0 0 24 24" fill="none">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <h3 class="filter-title">价格区间</h3>
            </div>
            <div class="price-options">
              <button
                v-for="option in priceOptions"
                :key="option.value"
                :class="['price-option', { active: priceRange.includes(option.value) }]"
                @click="priceRange = priceRange.includes(option.value) ? [] : [option.value]; handlePriceChange()"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="filter-section">
            <div class="filter-header">
              <svg class="filter-icon" viewBox="0 0 24 24" fill="none">
                <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <h3 class="filter-title">快捷入口</h3>
            </div>
            <div class="quick-links">
              <router-link to="/products?type=hot" class="quick-link">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 2c0 0-4 4-4 9 0 2.5 2 4 2 6s-2 3-2 5c0 2.5 2.5 5 6 5s6-2.5 6-5c0-2-2-3-2-5s2-3.5 2-6c0-5-4-9-4-9z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>热销爆款</span>
              </router-link>
              <router-link to="/products?type=new" class="quick-link">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 8v8M8 12h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>新品上市</span>
              </router-link>
            </div>
          </div>
        </div>
      </aside>

      <!-- Product Grid Area -->
      <main class="products-area">
        <!-- Toolbar -->
        <div class="toolbar">
          <div class="search-bar">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
              <path d="M21 21l-6.35-6.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索商品名称、型号..."
              class="search-input"
              @keyup.enter="handleSearch"
            />
            <button @click="handleSearch" class="search-button">搜索</button>
          </div>

          <div class="sort-controls">
            <span class="sort-label">排序:</span>
            <div class="sort-buttons">
              <button
                v-for="option in sortOptions"
                :key="option.value"
                :class="['sort-btn', { active: sortBy === option.value }]"
                @click="sortBy = option.value; handleSortChange()"
              >
                {{ option.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- Results Header -->
        <div class="results-header">
          <span class="results-count">找到 <strong>{{ totalCount }}</strong> 件商品</span>
          <div class="view-toggle">
            <button class="view-btn active">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="7" height="7" stroke="currentColor" stroke-width="2"/>
                <rect x="14" y="3" width="7" height="7" stroke="currentColor" stroke-width="2"/>
                <rect x="3" y="14" width="7" height="7" stroke="currentColor" stroke-width="2"/>
                <rect x="14" y="14" width="7" height="7" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-loading="loading" class="products-grid">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <!-- Product Image -->
            <div class="product-image-box">
              <img :src="product.image" :alt="product.name" class="product-img" />
              <div class="product-overlay">
                <button class="view-detail-btn">查看详情</button>
              </div>

              <!-- Badges -->
              <div class="product-badges">
                <span v-if="product.sales > 100" class="badge badge-hot">HOT</span>
                <span v-if="product.is_new" class="badge badge-new">NEW</span>
              </div>

              <!-- Quick Actions -->
              <div class="quick-actions">
                <button class="action-btn" @click.stop>
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" stroke="currentColor" stroke-width="2"/>
                  </svg>
                </button>
                <button class="action-btn" @click.stop>
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="currentColor" stroke-width="2"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Product Info -->
            <div class="product-details">
              <div class="product-category-tag">
                {{ product.category?.name || '配件' }}
              </div>
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-desc" v-if="product.description">{{ product.description.slice(0, 50) }}...</p>

              <div class="product-meta">
                <div class="price-section">
                  <span class="current-price">{{ formatCurrency(product.price) }}</span>
                  <span v-if="product.original_price && product.original_price > product.price" class="original-price">
                    {{ formatCurrency(product.original_price) }}
                  </span>
                </div>
                <div class="product-stats">
                  <span class="stat-item">
                    <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                      <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                    {{ product.sales }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && products.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h3 class="empty-title">未找到相关商品</h3>
          <p class="empty-desc">尝试调整筛选条件或搜索关键词</p>
          <button @click="clearFilters" class="empty-action">清除所有筛选</button>
        </div>

        <!-- Pagination -->
        <div v-if="totalCount > pageSize" class="pagination-container">
          <el-pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :total="totalCount"
            layout="prev, pager, next"
            @current-change="handlePageChange"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.product-list-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Hero Header */
.hero-header {
  position: relative;
  padding: 80px 40px 60px;
  overflow: hidden;
  background: #0f172a;
}

.hero-mesh {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 40%, rgba(249, 115, 22, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 60%, rgba(59, 130, 246, 0.1), transparent);
  animation: meshMove 15s ease-in-out infinite;
}

@keyframes meshMove {
  0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
  50% { opacity: 0.8; transform: scale(1.1) rotate(3deg); }
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black, transparent);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 100px;
  color: #f97316;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
}

.hero-title {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 16px;
  color: #94a3b8;
  margin-bottom: 40px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #f97316;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(249, 115, 22, 0.2);
}

.hero-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.hero-circle-1 {
  width: 400px;
  height: 400px;
  background: #f97316;
  top: -100px;
  right: -100px;
}

.hero-circle-2 {
  width: 300px;
  height: 300px;
  background: #3b82f6;
  bottom: -50px;
  left: -50px;
}

/* Main Container */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 32px;
}

/* Filters Sidebar */
.filters-sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.active-filters-bar {
  background: rgba(249, 115, 22, 0.05);
  border: 1px solid rgba(249, 115, 22, 0.2);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.active-filters-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.active-label {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
}

.active-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  flex: 1;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(249, 115, 22, 0.15);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 6px;
  color: #f97316;
  font-size: 12px;
  font-weight: 500;
}

.tag-close {
  background: none;
  border: none;
  color: #f97316;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-all-btn {
  background: none;
  border: none;
  color: #f97316;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
}

.clear-all-btn:hover {
  text-decoration: underline;
}

.filter-sections {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.filter-icon {
  width: 20px;
  height: 20px;
  color: #f97316;
}

.filter-title {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #ffffff;
}

/* Category List */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-item:hover {
  background: rgba(249, 115, 22, 0.1);
}

.category-item.active {
  background: rgba(249, 115, 22, 0.15);
}

.category-name {
  font-size: 14px;
  color: #94a3b8;
  transition: color 0.2s ease;
}

.category-item:hover .category-name,
.category-item.active .category-name {
  color: #f97316;
}

.category-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: transparent;
  border: 2px solid #475569;
  transition: all 0.2s ease;
}

.category-item.active .category-indicator {
  background: #f97316;
  border-color: #f97316;
  box-shadow: 0 0 10px rgba(249, 115, 22, 0.5);
}

/* Price Options */
.price-options {
  display: grid;
  gap: 8px;
}

.price-option {
  padding: 10px 14px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 13px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.price-option:hover {
  border-color: rgba(249, 115, 22, 0.5);
  color: #f97316;
}

.price-option.active {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
}

/* Quick Links */
.quick-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.quick-link svg {
  width: 18px;
  height: 18px;
  color: #f97316;
}

.quick-link:hover {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
}

/* Products Area */
.products-area {
  min-width: 0;
}

.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-bar {
  flex: 1;
  min-width: 280px;
  display: flex;
  align-items: center;
  padding: 4px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.search-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
  margin: 0 12px;
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  color: #e2e8f0;
  font-size: 14px;
  outline: none;
}

.search-input::placeholder {
  color: #64748b;
}

.search-button {
  padding: 8px 20px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.4);
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sort-label {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  white-space: nowrap;
}

.sort-buttons {
  display: flex;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  padding: 4px;
}

.sort-btn {
  padding: 8px 16px;
  background: none;
  border: none;
  border-radius: 6px;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.sort-btn:hover {
  color: #e2e8f0;
}

.sort-btn.active {
  background: rgba(249, 115, 22, 0.2);
  color: #f97316;
}

/* Results Header */
.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(71, 85, 105, 0.5);
}

.results-count {
  font-size: 14px;
  color: #94a3b8;
}

.results-count strong {
  color: #f97316;
  font-weight: 700;
}

.view-toggle {
  display: flex;
  gap: 8px;
}

.view-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
}

.view-btn.active {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
}

.view-btn svg {
  width: 18px;
  height: 18px;
}

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.product-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.product-card:hover {
  border-color: rgba(249, 115, 22, 0.5);
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -20px rgba(249, 115, 22, 0.3);
}

.product-image-box {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  background: rgba(15, 23, 42, 0.5);
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.product-card:hover .product-img {
  transform: scale(1.08);
}

.product-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.8);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-overlay {
  opacity: 1;
}

.view-detail-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 100px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.05em;
  cursor: pointer;
  transform: translateY(20px);
  transition: transform 0.3s ease;
}

.product-card:hover .view-detail-btn {
  transform: translateY(0);
}

.product-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 6px;
  z-index: 2;
}

.badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.badge-hot {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
}

.badge-new {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: #ffffff;
}

.quick-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 2;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: #f97316;
  border-color: #f97316;
  color: #ffffff;
}

.product-card:hover .action-btn {
  opacity: 1;
  transform: translateX(0);
}

.action-btn:nth-child(2) {
  transition-delay: 0.05s;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.product-details {
  padding: 16px;
}

.product-category-tag {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(249, 115, 22, 0.1);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #f97316;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 10px;
}

.product-name {
  font-size: 15px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-desc {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.price-section {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.current-price {
  font-size: 20px;
  font-weight: 800;
  color: #f97316;
}

.original-price {
  font-size: 13px;
  color: #64748b;
  text-decoration: line-through;
}

.product-stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #64748b;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: rgba(30, 41, 59, 0.3);
  border: 1px dashed rgba(71, 85, 105, 0.5);
  border-radius: 16px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: #475569;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-size: 20px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
}

.empty-action {
  padding: 12px 28px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 100px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.empty-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

.pagination-container :deep(.el-pagination-item) {
  background: rgba(30, 41, 59, 0.5);
  border-color: rgba(71, 85, 105, 0.5);
  color: #94a3b8;
}

.pagination-container :deep(.el-pagination-item:hover) {
  border-color: #f97316;
  color: #f97316;
}

.pagination-container :deep(.el-pagination-item.is-active) {
  background: #f97316;
  border-color: #f97316;
  color: #ffffff;
}

.pagination-container :deep(.el-pagination button) {
  background: rgba(30, 41, 59, 0.5);
  border-color: rgba(71, 85, 105, 0.5);
  color: #94a3b8;
}

.pagination-container :deep(.el-pagination button:hover) {
  border-color: #f97316;
  color: #f97316;
}

/* Responsive */
@media (max-width: 1024px) {
  .main-container {
    grid-template-columns: 1fr;
  }

  .filters-sidebar {
    position: static;
  }

  .toolbar {
    flex-direction: column;
  }

  .search-bar {
    min-width: 100%;
  }

  .sort-controls {
    width: 100%;
  }

  .sort-buttons {
    flex: 1;
    overflow-x: auto;
  }
}

@media (max-width: 640px) {
  .hero-header {
    padding: 60px 20px 40px;
  }

  .hero-stats {
    gap: 16px;
  }

  .stat-divider {
    display: none;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
  }

  .product-details {
    padding: 12px;
  }

  .product-name {
    font-size: 13px;
  }

  .current-price {
    font-size: 16px;
  }
}
</style>
