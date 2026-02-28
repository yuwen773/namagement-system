<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '@/api'
import { Search, Filter, Grid, List, ArrowUp, ArrowDown, Star, TrendCharts, Shop, ArrowRight, ShoppingCart } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const products = ref([])
const total = ref(0)
const viewMode = ref('grid') // grid or list

// 搜索和筛选条件
const searchForm = reactive({
  keyword: '',
  minPrice: null,
  maxPrice: null,
  shop: '',
  sortBy: 'sales', // sales, price, created
  sortOrder: 'desc' // asc, desc
})

const pagination = reactive({
  page: 1,
  pageSize: 12
})

// 价格区间选项
const priceRanges = [
  { label: '全部', value: null },
  { label: '0-50元', min: 0, max: 50 },
  { label: '50-100元', min: 50, max: 100 },
  { label: '100-200元', min: 100, max: 200 },
  { label: '200-500元', min: 200, max: 500 },
  { label: '500元以上', min: 500, max: null }
]

const selectedPriceRange = ref(null)

// 加载商品数据
const fetchProducts = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.keyword || undefined,
      min_price: searchForm.minPrice || undefined,
      max_price: searchForm.maxPrice || undefined,
      shop: searchForm.shop || undefined,
      ordering: searchForm.sortBy === 'price'
        ? (searchForm.sortOrder === 'desc' ? '-price' : 'price')
        : searchForm.sortBy === 'sales'
          ? (searchForm.sortOrder === 'desc' ? '-sales' : 'sales')
        : undefined
    }

    const res = await productApi.getList(params)
    if (res.code === 0) {
      products.value = res.data
      total.value = res.total
    }
  } catch (error) {
    console.error('Failed to fetch products:', error)
    // 使用模拟数据
    products.value = generateMockProducts()
    total.value = 10000
  } finally {
    loading.value = false
  }
}

// 生成模拟商品数据
const generateMockProducts = () => {
  const mockProducts = []
  const shops = ['皇家宠物旗舰店', '渴望官方旗舰店', '冠能官方店', '耐威克旗舰店', '疯狂小狗官方', 'pidan官方店']
  const categories = ['猫粮', '狗粮', '猫砂', '零食', '玩具']

  for (let i = 1; i <= 24; i++) {
    const price = Math.floor(Math.random() * 500) + 20
    const sales = Math.floor(Math.random() * 50000) + 100
    mockProducts.push({
      id: i,
      title: `${shops[i % shops.length]} ${categories[i % categories.length]} ${['成猫专用', '幼犬配方', '混合型', '全期通用', '营养均衡'][i % 5]}系列`,
      price: price,
      sales: sales,
      shop: shops[i % shops.length],
      image_url: `https://picsum.photos/seed/${i}/300/300`,
      category: categories[i % categories.length],
      rating: (Math.random() * 2 + 3).toFixed(1)
    })
  }
  return mockProducts
}

// 跳转到商品详情
const goToDetail = (id) => {
  router.push(`/user/products/${id}`)
}

// 处理价格区间选择
const handlePriceRangeChange = (range) => {
  if (range) {
    searchForm.minPrice = range.min || undefined
    searchForm.maxPrice = range.max || undefined
  } else {
    searchForm.minPrice = null
    searchForm.maxPrice = null
  }
  pagination.page = 1
  fetchProducts()
}

// 重置筛选
const resetFilters = () => {
  searchForm.keyword = ''
  searchForm.minPrice = null
  searchForm.maxPrice = null
  searchForm.shop = ''
  searchForm.sortBy = 'sales'
  searchForm.sortOrder = 'desc'
  selectedPriceRange.value = null
  pagination.page = 1
  fetchProducts()
}

// 排序变化
const handleSortChange = (sort) => {
  searchForm.sortBy = sort.prop
  searchForm.sortOrder = sort.order === 'ascending' ? 'asc' : 'desc'
  fetchProducts()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchProducts()
}

// 格式化价格
const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2
  }).format(price)
}

// 格式化销量
const formatSales = (sales) => {
  if (sales >= 10000) {
    return (sales / 10000).toFixed(1) + '万+'
  }
  return sales + '+'
}

// 格式化数字
const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

// 监听筛选变化
watch([() => searchForm.keyword, () => searchForm.shop], () => {
  pagination.page = 1
  // 防抖搜索
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchProducts()
  }, 300)
})

let searchTimeout = null

onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="products-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-badge">
          <Filter class="badge-icon" />
          <span>商品库</span>
        </div>
        <h1 class="page-title">
          <span class="title-gradient">商品资源库</span>
        </h1>
        <p class="page-subtitle">探索海量宠物用品，发现心仪好物</p>
      </div>
      <div class="header-stats">
        <div class="stat-mini">
          <span class="stat-value">{{ formatNumber(total) }}</span>
          <span class="stat-label">商品总数</span>
        </div>
      </div>
    </div>

    <!-- 筛选控制面板 -->
    <div class="filter-panel">
      <div class="filter-bar">
        <div class="search-group">
          <Search class="search-icon" />
          <input
            v-model="searchForm.keyword"
            type="text"
            placeholder="搜索商品名称、店铺..."
            class="search-input"
            @keyup.enter="fetchProducts"
          />
        </div>

        <div class="filter-group-inline">
          <label class="filter-label">价格</label>
          <el-select
            v-model="selectedPriceRange"
            placeholder="选择区间"
            clearable
            class="filter-select"
            @change="handlePriceRangeChange"
          >
            <el-option
              v-for="range in priceRanges"
              :key="range.label"
              :label="range.label"
              :value="range"
            />
          </el-select>
        </div>

        <div class="filter-group-inline">
          <label class="filter-label">店铺</label>
          <input
            v-model="searchForm.shop"
            type="text"
            placeholder="店铺名称"
            class="filter-input-inline"
          />
        </div>

        <div class="action-buttons">
          <button class="search-btn" @click="fetchProducts">
            <Search class="btn-icon-sm" />
            <span>搜索</span>
          </button>
          <button class="reset-btn" @click="resetFilters">
            <span>重置</span>
          </button>
        </div>
      </div>

      <!-- 排序和视图切换 -->
      <div class="toolbar-row">
        <div class="sort-options">
          <span class="sort-label">排序方式</span>
          <button
            class="sort-btn"
            :class="{ active: searchForm.sortBy === 'sales' }"
            @click="searchForm.sortBy = 'sales'; fetchProducts()"
          >
            <TrendCharts class="sort-icon" />
            <span>销量</span>
            <ArrowUp v-if="searchForm.sortBy === 'sales' && searchForm.sortOrder === 'desc'" class="order-icon" />
            <ArrowDown v-else-if="searchForm.sortBy === 'sales' && searchForm.sortOrder === 'asc'" class="order-icon" />
          </button>
          <button
            class="sort-btn"
            :class="{ active: searchForm.sortBy === 'price' }"
            @click="searchForm.sortBy = 'price'; fetchProducts()"
          >
            <span>¥</span>
            <span>价格</span>
            <ArrowUp v-if="searchForm.sortBy === 'price' && searchForm.sortOrder === 'asc'" class="order-icon" />
            <ArrowDown v-else-if="searchForm.sortBy === 'price' && searchForm.sortOrder === 'desc'" class="order-icon" />
          </button>
        </div>

        <div class="view-toggle">
          <button
            class="view-btn"
            :class="{ active: viewMode === 'grid' }"
            @click="viewMode = 'grid'"
          >
            <Grid class="view-icon" />
            <span>网格</span>
          </button>
          <button
            class="view-btn"
            :class="{ active: viewMode === 'list' }"
            @click="viewMode = 'list'"
          >
            <List class="view-icon" />
            <span>列表</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 商品展示区域 -->
    <div class="products-section">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载商品数据...</p>
      </div>

      <!-- 网格视图 -->
      <div v-else-if="viewMode === 'grid'" class="products-grid">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-card"
          @click="goToDetail(product.id)"
        >
          <div class="card-image-wrapper">
            <img :src="product.image_url || 'https://picsum.photos/seed/' + product.id + '/300/300'" :alt="product.title" />
            <div class="card-badges">
              <div v-if="product.sales > 10000" class="card-badge card-badge--hot">
                🔥 热销
              </div>
              <div v-if="product.sales > 50000" class="card-badge card-badge--top">
                TOP
              </div>
            </div>
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ product.title }}</h3>
            <div class="card-meta">
              <span class="shop-tag">
                <Shop class="shop-icon" />
                {{ product.shop }}
              </span>
              <div class="rating" v-if="product.rating">
                <Star class="star-icon" />
                <span>{{ product.rating }}</span>
              </div>
            </div>
            <div class="card-footer">
              <div class="price-info">
                <span class="price-label">¥</span>
                <span class="price-value">{{ Math.floor(product.price) }}</span>
                <span class="price-decimal">.{{ (product.price % 1).toFixed(2).substring(2) }}</span>
              </div>
              <div class="sales-info">
                <TrendCharts class="sales-icon" />
                <span>{{ formatSales(product.sales) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 列表视图 -->
      <div v-else class="products-list">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-row"
          @click="goToDetail(product.id)"
        >
          <div class="row-image">
            <img :src="product.image_url || 'https://picsum.photos/seed/' + product.id + '/300/300'" :alt="product.title" />
          </div>
          <div class="row-content">
            <h3 class="row-title">{{ product.title }}</h3>
            <div class="row-meta">
              <span class="shop-tag">{{ product.shop }}</span>
              <span v-if="product.category" class="category-tag">{{ product.category }}</span>
            </div>
          </div>
          <div class="row-price">
            <span class="price-symbol">¥</span>
            <span class="price-value">{{ Math.floor(product.price) }}</span>
          </div>
          <div class="row-sales">
            <TrendCharts class="sales-icon" />
            <span class="sales-value">{{ formatSales(product.sales) }}</span>
          </div>
          <div class="row-action">
            <button class="view-detail-btn">
              <span>查看详情</span>
              <ArrowRight class="arrow-icon" />
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && products.length === 0" class="empty-state">
        <div class="empty-icon-wrapper">
          <ShoppingCart class="empty-icon" />
        </div>
        <h3 class="empty-title">暂无商品</h3>
        <p class="empty-hint">调整筛选条件试试看</p>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > pagination.pageSize" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="pagination.page"
        :page-size="pagination.pageSize"
        :total="total"
        layout="prev, pager, next, jumper"
        background
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.products-page {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(255, 255, 255, 0.15);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  animation: pageFadeIn 0.4s ease;
}

@keyframes pageFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ============================================
   Page Header
   ============================================ */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  padding: 8px 0;
}

.header-content {
  flex: 1;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  margin-bottom: 12px;
}

.header-badge .badge-icon {
  width: 14px;
  height: 14px;
  color: var(--primary-orange);
}

.header-badge span {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--primary-orange);
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.title-gradient {
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 400;
}

.header-stats {
  display: flex;
  gap: 12px;
}

.stat-mini {
  text-align: center;
  padding: 12px 16px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 14px;
  min-width: 80px;
}

.stat-mini .stat-value {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-orange);
}

.stat-mini .stat-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ============================================
   Filter Panel
   ============================================ */
.filter-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.4s ease;
  animation-delay: 0.1s;
  animation-fill-mode: both;
}

@keyframes panelSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
  flex-wrap: wrap;
}

.search-group {
  position: relative;
  flex: 1;
  min-width: 200px;
  max-width: 420px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--text-tertiary);
  pointer-events: none;
  transition: color 0.3s ease;
}

.search-input {
  width: 100%;
  padding: 13px 16px 13px 48px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-orange);
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.filter-group-inline {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.filter-select {
  width: 120px;
}

.filter-select :deep(.el-input__wrapper) {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 10px;
  box-shadow: none;
}

.filter-select :deep(.el-input__inner) {
  color: var(--text-primary);
}

.filter-input-inline {
  width: 120px;
  padding: 11px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.filter-input-inline::placeholder {
  color: var(--text-tertiary);
}

.filter-input-inline:focus {
  outline: none;
  border-color: var(--primary-orange);
  background: rgba(0, 0, 0, 0.4);
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.search-btn,
.reset-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 13px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.search-btn {
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-orange));
  color: white;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

.reset-btn {
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-tertiary);
}

.reset-btn:hover {
  border-color: var(--border-default);
  color: var(--text-secondary);
}

.btn-icon-sm {
  width: 14px;
  height: 14px;
}

/* Toolbar Row */
.toolbar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  flex-wrap: wrap;
  gap: 12px;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sort-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-btn:hover {
  border-color: var(--border-default);
  color: var(--text-primary);
}

.sort-btn.active {
  background: rgba(255, 107, 53, 0.15);
  border-color: rgba(255, 107, 53, 0.3);
  color: var(--primary-orange);
}

.sort-btn .sort-icon {
  width: 14px;
  height: 14px;
}

.order-icon {
  width: 12px;
  height: 12px;
  margin-left: 2px;
}

.view-toggle {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 4px;
}

.view-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 14px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
  font-weight: 500;
}

.view-btn .view-icon {
  width: 16px;
  height: 16px;
}

.view-btn.active {
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-gold));
  color: #000;
}

.view-btn:hover:not(.active) {
  color: var(--text-secondary);
}

/* ============================================
   Products Section
   ============================================ */
.products-section {
  min-height: 400px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: var(--text-tertiary);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 107, 53, 0.2);
  border-top-color: var(--primary-orange);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ============================================
   Products Grid
   ============================================ */
.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  animation: gridFadeIn 0.5s ease;
}

@keyframes gridFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.product-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 107, 53, 0.3);
  box-shadow: 0 20px 40px rgba(255, 107, 53, 0.15);
}

.card-image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.card-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.product-card:hover .card-image-wrapper img {
  transform: scale(1.08);
}

.card-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  backdrop-filter: blur(10px);
}

.card-badge--hot {
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-gold));
  color: #000;
}

.card-badge--top {
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-cyan));
  color: #000;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.shop-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
}

.shop-tag .shop-icon {
  width: 12px;
  height: 12px;
}

.rating {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--primary-gold);
  font-weight: 600;
}

.rating .star-icon {
  width: 14px;
  height: 14px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.price-info {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.price-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-orange);
}

.price-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  font-weight: 700;
  color: var(--primary-orange);
  line-height: 1;
}

.price-decimal {
  font-size: 14px;
  color: var(--primary-orange);
  opacity: 0.8;
}

.sales-info {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--text-tertiary);
}

.sales-info .sales-icon {
  width: 12px;
  height: 12px;
  color: var(--primary-cyan);
}

/* ============================================
   Products List
   ============================================ */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: gridFadeIn 0.5s ease;
}

.product-row {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-row:hover {
  border-color: rgba(255, 107, 53, 0.3);
  background: rgba(255, 107, 53, 0.05);
  transform: translateX(4px);
}

.row-image {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.3);
}

.row-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.row-content {
  flex: 1;
  min-width: 0;
}

.row-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.row-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.row-meta .shop-tag {
  background: rgba(123, 44, 191, 0.1);
  color: var(--primary-purple);
}

.row-meta .category-tag {
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
}

.row-price {
  width: 100px;
  text-align: right;
}

.row-price .price-symbol {
  font-size: 14px;
  color: var(--primary-orange);
  font-weight: 600;
}

.row-price .price-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-orange);
}

.row-sales {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.row-sales .sales-icon {
  width: 14px;
  height: 14px;
  color: var(--primary-cyan);
}

.row-sales .sales-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.row-action {
  width: 120px;
}

.view-detail-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px 16px;
  background: transparent;
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-orange);
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-detail-btn:hover {
  background: rgba(255, 107, 53, 0.15);
  border-color: var(--primary-orange);
}

.view-detail-btn .arrow-icon {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
}

.view-detail-btn:hover .arrow-icon {
  transform: translateX(4px);
}

/* ============================================
   Empty State
   ============================================ */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: var(--text-tertiary);
}

.empty-icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  margin-bottom: 24px;
}

.empty-icon {
  width: 36px;
  height: 36px;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 14px;
  margin: 0;
}

/* ============================================
   Pagination
   ============================================ */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

.pagination-wrapper :deep(.el-pagination) {
  --el-pagination-bg-color: rgba(255, 255, 255, 0.05);
  --el-pagination-text-color: rgba(255, 255, 255, 0.7);
  --el-pagination-button-bg-color: rgba(255, 255, 255, 0.05);
  --el-pagination-hover-color: var(--primary-orange);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 8px 16px;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li) {
  background: transparent;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-gold));
  color: #000;
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 1400px) {
  .products-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-stats {
    width: 100%;
    justify-content: flex-start;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-group {
    max-width: 100%;
  }

  .action-buttons {
    margin-left: 0;
    width: 100%;
  }

  .search-btn,
  .reset-btn {
    flex: 1;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .toolbar-row {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .sort-options {
    flex-wrap: wrap;
    justify-content: center;
  }

  .view-toggle {
    justify-content: center;
  }

  .product-row {
    flex-wrap: wrap;
    gap: 12px;
  }

  .row-image {
    width: 60px;
    height: 60px;
  }

  .row-content {
    flex: 1;
    min-width: 120px;
  }

  .row-price,
  .row-sales,
  .row-action {
    width: auto;
    flex: 1;
  }

  .row-price {
    text-align: left;
  }

  .filter-group-inline {
    flex: 1;
    min-width: 140px;
  }

  .filter-select,
  .filter-input-inline {
    width: 100%;
  }
}
</style>
