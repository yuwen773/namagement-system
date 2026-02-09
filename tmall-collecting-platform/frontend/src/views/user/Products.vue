<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '@/api'
import { Search, Filter, Grid, List, ArrowUp, ArrowDown, Star } from '@element-plus/icons-vue'

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
  const shops = ['泡泡玛特旗舰店', '万代官方旗舰店', '宝可梦官方', '原神旗舰店', '鹰角网络', '萌趣旗舰店']
  const categories = ['盲盒', '手办', '毛绒', '模型', '挂件']

  for (let i = 1; i <= 24; i++) {
    const price = Math.floor(Math.random() * 500) + 20
    const sales = Math.floor(Math.random() * 50000) + 100
    mockProducts.push({
      id: i,
      title: `${shops[i % shops.length]} ${categories[i % categories.length]} ${['潮玩', '限定', '经典', '萌系', '酷玩'][i % 5]}系列`,
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
  <div class="products-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="main-title">
          <span class="title-icon">🎨</span>
          商品资源库
        </h1>
        <p class="subtitle">探索海量潮玩商品，发现心仪好物</p>
      </div>
      <div class="header-stats">
        <span class="stat-item">共 {{ formatSales(total) }} 件商品</span>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="filter-section">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <div class="search-input-wrapper">
          <Search class="search-icon" />
          <input
            v-model="searchForm.keyword"
            type="text"
            placeholder="搜索商品名称、店铺..."
            class="search-input"
          />
        </div>
        <button class="search-btn" @click="fetchProducts">搜索</button>
      </div>

      <!-- 筛选工具栏 -->
      <div class="filter-toolbar">
        <div class="filter-left">
          <!-- 价格区间 -->
          <div class="filter-group">
            <label class="filter-label">价格区间</label>
            <el-select
              v-model="selectedPriceRange"
              placeholder="选择价格区间"
              clearable
              class="price-select"
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

          <!-- 店铺筛选 -->
          <div class="filter-group">
            <label class="filter-label">店铺</label>
            <input
              v-model="searchForm.shop"
              type="text"
              placeholder="输入店铺名称"
              class="filter-input"
            />
          </div>

          <button class="reset-btn" @click="resetFilters">
            <span>🔄</span> 重置
          </button>
        </div>

        <div class="filter-right">
          <!-- 排序 -->
          <div class="sort-options">
            <span class="sort-label">排序:</span>
            <button
              class="sort-btn"
              :class="{ active: searchForm.sortBy === 'sales' }"
              @click="searchForm.sortBy = 'sales'; fetchProducts()"
            >
              销量
              <ArrowUp v-if="searchForm.sortBy === 'sales' && searchForm.sortOrder === 'desc'" class="sort-icon" />
              <ArrowDown v-else-if="searchForm.sortBy === 'sales' && searchForm.sortOrder === 'asc'" class="sort-icon" />
            </button>
            <button
              class="sort-btn"
              :class="{ active: searchForm.sortBy === 'price' }"
              @click="searchForm.sortBy = 'price'; fetchProducts()"
            >
              价格
              <ArrowUp v-if="searchForm.sortBy === 'price' && searchForm.sortOrder === 'asc'" class="sort-icon" />
              <ArrowDown v-else-if="searchForm.sortBy === 'price' && searchForm.sortOrder === 'desc'" class="sort-icon" />
            </button>
          </div>

          <!-- 视图切换 -->
          <div class="view-toggle">
            <button
              class="view-btn"
              :class="{ active: viewMode === 'grid' }"
              @click="viewMode = 'grid'"
            >
              <Grid />
            </button>
            <button
              class="view-btn"
              :class="{ active: viewMode === 'list' }"
              @click="viewMode = 'list'"
            >
              <List />
            </button>
          </div>
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
          <div class="card-image">
            <img :src="product.image_url || 'https://picsum.photos/seed/' + product.id + '/300/300'" :alt="product.title" />
            <div class="card-badge" v-if="product.sales > 10000">🔥 热销</div>
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ product.title }}</h3>
            <div class="card-meta">
              <span class="shop-tag">{{ product.shop }}</span>
              <div class="rating">
                <Star class="star-icon" />
                <span>{{ product.rating || '4.8' }}</span>
              </div>
            </div>
            <div class="card-footer">
              <div class="price-info">
                <span class="price-label">价格</span>
                <span class="price-value">{{ formatPrice(product.price) }}</span>
              </div>
              <div class="sales-info">
                销量 {{ formatSales(product.sales) }}
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
              <span class="category-tag">{{ product.category || '潮玩' }}</span>
            </div>
          </div>
          <div class="row-price">
            <span class="price-value">{{ formatPrice(product.price) }}</span>
          </div>
          <div class="row-sales">
            <span class="sales-value">{{ formatSales(product.sales) }}</span>
            <span class="sales-label">销量</span>
          </div>
          <div class="row-action">
            <button class="view-btn-detail">查看详情</button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && products.length === 0" class="empty-state">
        <div class="empty-icon">📦</div>
        <h3>暂无商品</h3>
        <p>调整筛选条件试试看</p>
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

.products-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 28px;
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.1) 0%, rgba(255, 107, 53, 0.08) 100%);
  border: 1px solid rgba(255, 107, 53, 0.15);
  border-radius: 20px;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.main-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Orbitron', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.title-icon {
  font-size: 28px;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.stat-item {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  padding: 8px 16px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
}

/* 筛选区域 */
.filter-section {
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-input-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.4);
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 44px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 14px;
  color: #fff;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: rgba(255, 107, 53, 0.5);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.search-btn {
  padding: 14px 32px;
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
}

.filter-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.price-select {
  width: 140px;
}

.price-select :deep(.el-input__wrapper) {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.filter-input {
  width: 140px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 13px;
  color: #fff;
  outline: none;
}

.filter-input:focus {
  border-color: rgba(255, 107, 53, 0.5);
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  border-color: rgba(255, 107, 53, 0.5);
  color: #FF6B35;
}

.filter-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-btn.active {
  background: rgba(255, 107, 53, 0.15);
  border-color: rgba(255, 107, 53, 0.3);
  color: #FF6B35;
}

.sort-icon {
  width: 12px;
  height: 12px;
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
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn.active {
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  color: #000;
}

.view-btn:hover:not(.active) {
  color: rgba(255, 255, 255, 0.8);
}

.view-btn :deep(svg) {
  width: 18px;
  height: 18px;
}

/* 商品展示 */
.products-section {
  min-height: 400px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: rgba(255, 255, 255, 0.4);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 107, 53, 0.2);
  border-top-color: #FF6B35;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 网格视图 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.product-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 107, 53, 0.3);
  box-shadow: 0 20px 40px rgba(255, 107, 53, 0.15);
}

.card-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .card-image img {
  transform: scale(1.05);
}

.card-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: #000;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.shop-tag {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  padding: 3px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.rating {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #FFD700;
}

.star-icon {
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
  flex-direction: column;
}

.price-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

.price-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #FF6B35;
}

.sales-info {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

/* 列表视图 */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-row {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-row:hover {
  border-color: rgba(255, 107, 53, 0.3);
  background: rgba(255, 107, 53, 0.05);
}

.row-image {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
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
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-meta {
  display: flex;
  gap: 8px;
}

.shop-tag, .category-tag {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  padding: 3px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.row-price {
  width: 100px;
  text-align: right;
}

.row-price .price-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #FF6B35;
}

.row-sales {
  width: 80px;
  text-align: center;
}

.sales-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.sales-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

.row-action {
  width: 100px;
}

.view-btn-detail {
  width: 100%;
  padding: 10px 16px;
  background: transparent;
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 8px;
  font-size: 12px;
  color: #FF6B35;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn-detail:hover {
  background: rgba(255, 107, 53, 0.15);
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: rgba(255, 255, 255, 0.4);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

.pagination-wrapper :deep(.el-pagination) {
  --el-pagination-bg-color: rgba(255, 255, 255, 0.05);
  --el-pagination-text-color: rgba(255, 255, 255, 0.7);
  --el-pagination-button-bg-color: rgba(255, 255, 255, 0.05);
  --el-pagination-hover-color: #FF6B35;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 8px 16px;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li) {
  background: transparent;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  color: #000;
}

/* 响应式 */
@media (max-width: 1400px) {
  .products-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
  }

  .filter-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-left {
    width: 100%;
    flex-wrap: wrap;
  }

  .product-row {
    flex-wrap: wrap;
  }

  .row-price, .row-sales, .row-action {
    width: auto;
    flex: 1;
    text-align: left;
  }
}
</style>
