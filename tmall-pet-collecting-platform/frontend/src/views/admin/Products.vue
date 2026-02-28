<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productApi } from '@/api'
import Pagination from '@/components/common/Pagination.vue'
import {
  ShoppingCart, Search, Download, Refresh, Edit, Delete,
  Picture, Filter, TrendCharts
} from '@element-plus/icons-vue'

// 数据状态
const products = ref([])
const loading = ref(false)
const total = ref(0)

// 搜索筛选
const searchForm = ref({
  search: '',
  min_price: null,
  max_price: null,
  shop: '',
  brand: '',
  region: '',
  category: '',
  tags: '',
  batch_no: '',
  ordering: '-crawl_time'
})

const showFilters = ref(false)

// 分页
const pagination = ref({
  page: 1,
  page_size: 20
})

// 排序选项
const sortOptions = [
  { label: '最新采集', value: '-crawl_time' },
  { label: '价格从低到高', value: 'price' },
  { label: '价格从高到低', value: '-price' },
  { label: '销量从高到低', value: '-sales' },
  { label: '销量从低到高', value: 'sales' }
]

// 选中项
const selectedIds = ref([])

// 计算属性：是否有激活的筛选条件
const hasActiveFilters = computed(() => {
  return searchForm.value.search ||
    searchForm.value.min_price ||
    searchForm.value.max_price ||
    searchForm.value.shop ||
    searchForm.value.brand ||
    searchForm.value.region ||
    searchForm.value.category ||
    searchForm.value.tags ||
    searchForm.value.batch_no
})

// 全选/取消全选
const toggleSelectAll = () => {
  if (selectedIds.value.length === products.value.length) {
    selectedIds.value = []
  } else {
    selectedIds.value = products.value.map(p => p.id)
  }
}

// 切换单个选择
const toggleSelect = (id) => {
  const index = selectedIds.value.indexOf(id)
  if (index > -1) {
    selectedIds.value.splice(index, 1)
  } else {
    selectedIds.value.push(id)
  }
}

// 图片加载失败处理
const handleImageError = (e) => {
  e.target.style.display = 'none'
}

// 编辑商品
const handleEdit = (product) => {
  ElMessage.info('编辑功能开发中')
}

// 加载数据
const loadProducts = async () => {
  try {
    loading.value = true
    const params = {
      ...pagination.value,
      ...searchForm.value
    }

    // 清理空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })

    const res = await productApi.getList(params)
    if (res.code === 0) {
      products.value = res.data || []
      total.value = res.total || 0
    }
  } catch (error) {
    ElMessage.error('加载商品数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.value.page = 1
  loadProducts()
}

// 重置筛选
const handleReset = () => {
  searchForm.value = {
    search: '',
    min_price: null,
    max_price: null,
    shop: '',
    brand: '',
    region: '',
    category: '',
    tags: '',
    batch_no: '',
    ordering: '-crawl_time'
  }
  pagination.value.page = 1
  loadProducts()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.value.page = page
  loadProducts()
}

const handlePageSizeChange = (size) => {
  pagination.value.page_size = size
  pagination.value.page = 1
  loadProducts()
}

// 排序变化
const handleSortChange = (value) => {
  searchForm.value.ordering = value
  loadProducts()
}

// 删除商品
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除商品 "${row.title}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const res = await productApi.delete(row.id)
    if (res.code === 0) {
      ElMessage.success('删除成功')
      loadProducts()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要删除的商品')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedIds.value.length} 个商品吗？`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 批量删除
    for (const id of selectedIds.value) {
      await productApi.delete(id)
    }

    ElMessage.success(`成功删除 ${selectedIds.value.length} 个商品`)
    selectedIds.value = []
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// 导出CSV
const handleExport = async () => {
  try {
    const params = {
      ...searchForm.value,
      format: 'csv'
    }

    // 清理空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) {
        delete params[key]
      }
    })

    ElMessage.info('正在导出数据...')

    const blob = await productApi.export(params)
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `products_${new Date().toISOString().slice(0, 10)}.csv`
    link.click()
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
    console.error(error)
  }
}

// 格式化价格
const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY'
  }).format(price)
}

// 格式化销量
const formatSales = (sales) => {
  return new Intl.NumberFormat('zh-CN').format(sales)
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  return new Date(timeStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化数字（千分位）
const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num || 0)
}

onMounted(() => {
  loadProducts()
})
</script>

<template>
  <div class="products-container">
    <!-- 装饰叶子图案 -->
    <div class="leaf-decoration leaf-decoration--1">
      <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
        <path d="M60 10C60 10 100 30 100 60C100 90 80 110 60 110C40 110 20 90 20 60C20 30 60 10 60 10Z" fill="currentColor" opacity="0.03"/>
        <path d="M60 10L60 110" stroke="currentColor" stroke-width="1" opacity="0.05"/>
      </svg>
    </div>
    <div class="leaf-decoration leaf-decoration--2">
      <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
        <path d="M40 5C40 5 70 20 70 40C70 60 55 75 40 75C25 75 10 60 10 40C10 20 40 5 40 5Z" fill="currentColor" opacity="0.04"/>
      </svg>
    </div>

    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="title-group">
          <div class="title-icon-wrapper">
            <ShoppingCart class="title-icon" />
          </div>
          <div class="title-text">
            <h1 class="page-title">宠物商品管理</h1>
            <p class="page-subtitle">采集数据浏览与管理</p>
          </div>
        </div>
        <div class="stats-badges">
          <div class="stat-badge">
            <span class="stat-label">商品总数</span>
            <span class="stat-value">{{ formatNumber(total) }}</span>
          </div>
          <div v-if="selectedIds.length > 0" class="stat-badge stat-badge--active">
            <span class="stat-label">已选择</span>
            <span class="stat-value">{{ selectedIds.length }}</span>
          </div>
        </div>
      </div>
      <div class="header-actions">
        <button
          v-if="selectedIds.length > 0"
          class="action-btn action-btn--danger"
          @click="handleBatchDelete"
        >
          <Delete class="btn-icon" />
          <span>批量删除</span>
        </button>
        <button class="action-btn action-btn--secondary" @click="loadProducts" :class="{ loading }">
          <Refresh class="btn-icon" :class="{ spinning: loading }" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <!-- 筛选控制面板 -->
    <div class="filter-panel">
      <div class="filter-bar">
        <div class="search-group">
          <Search class="search-icon" />
          <input
            v-model="searchForm.search"
            type="text"
            placeholder="搜索商品标题、品牌..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>

        <button
          class="filter-toggle"
          :class="{ active: showFilters || hasActiveFilters }"
          @click="showFilters = !showFilters"
        >
          <Filter class="filter-icon" />
          <span>高级筛选</span>
          <span v-if="hasActiveFilters" class="active-badge"></span>
        </button>

        <div class="sort-group">
          <select
            v-model="searchForm.ordering"
            class="sort-select"
            @change="handleSortChange"
          >
            <option
              v-for="option in sortOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <div class="action-buttons">
          <button class="search-btn" @click="handleSearch">
            <Search class="btn-icon-sm" />
            <span>搜索</span>
          </button>
          <button class="reset-btn" @click="handleReset">
            <span>重置</span>
          </button>
        </div>
      </div>

      <!-- 展开的筛选条件 -->
      <div v-if="showFilters" class="filter-grid">
        <div class="filter-item">
          <label class="filter-label">价格区间</label>
          <div class="price-range-inputs">
            <input
              v-model.number="searchForm.min_price"
              type="number"
              placeholder="最低价"
              class="range-input"
            />
            <span class="range-divider">至</span>
            <input
              v-model.number="searchForm.max_price"
              type="number"
              placeholder="最高价"
              class="range-input"
            />
          </div>
        </div>

        <div class="filter-item">
          <label class="filter-label">店铺名称</label>
          <input
            v-model="searchForm.shop"
            type="text"
            placeholder="输入店铺名"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">品牌</label>
          <input
            v-model="searchForm.brand"
            type="text"
            placeholder="输入品牌名"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">地区</label>
          <input
            v-model="searchForm.region"
            type="text"
            placeholder="如：广东、上海"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">类目</label>
          <input
            v-model="searchForm.category"
            type="text"
            placeholder="如：狗粮、猫砂"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">标签</label>
          <input
            v-model="searchForm.tags"
            type="text"
            placeholder="商品标签"
            class="filter-input"
          />
        </div>

        <div class="filter-item">
          <label class="filter-label">批次号</label>
          <input
            v-model="searchForm.batch_no"
            type="text"
            placeholder="采集批次号"
            class="filter-input"
          />
        </div>
      </div>
    </div>

    <!-- 商品数据表格 -->
    <div class="table-card">
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-checkbox">
                <input
                  type="checkbox"
                  :checked="selectedIds.length > 0 && selectedIds.length === products.length"
                  @change="toggleSelectAll"
                  class="checkbox-input"
                />
              </th>
              <th class="col-product">商品信息</th>
              <th class="col-price">价格</th>
              <th class="col-sales">销量</th>
              <th class="col-shop">店铺</th>
              <th class="col-brand">品牌</th>
              <th class="col-region">地区</th>
              <th class="col-time">采集时间</th>
              <th class="col-actions">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="products.length === 0 && !loading" class="empty-row">
              <td colspan="9">
                <div class="empty-container">
                  <div class="empty-icon-wrapper">
                    <ShoppingCart class="empty-icon" />
                  </div>
                  <p class="empty-title">暂无商品数据</p>
                  <p class="empty-hint">点击刷新按钮加载最新数据</p>
                </div>
              </td>
            </tr>
            <tr
              v-for="product in products"
              :key="product.id"
              class="data-row"
              :class="{ 'row-selected': selectedIds.includes(product.id) }"
            >
              <td class="col-checkbox">
                <input
                  type="checkbox"
                  :checked="selectedIds.includes(product.id)"
                  @change="toggleSelect(product.id)"
                  class="checkbox-input"
                />
              </td>
              <td class="col-product">
                <div class="product-wrapper">
                  <div class="product-thumb">
                    <img
                      v-if="product.image_url"
                      :src="product.image_url"
                      :alt="product.title"
                      @error="handleImageError"
                    />
                    <Picture v-else class="thumb-placeholder" />
                  </div>
                  <div class="product-details">
                    <h4 class="product-name">{{ product.title }}</h4>
                    <div class="product-tags-row" v-if="product.brand || product.tags">
                      <span v-if="product.brand" class="tag tag--brand">{{ product.brand }}</span>
                      <span v-if="product.tags" class="tag tag--tag">{{ product.tags }}</span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="col-price">
                <span class="price-display">{{ formatPrice(product.price) }}</span>
              </td>
              <td class="col-sales">
                <div class="sales-display">
                  <TrendCharts class="sales-icon" />
                  <span>{{ formatSales(product.sales) }}</span>
                </div>
              </td>
              <td class="col-shop">
                <span class="shop-display" :title="product.shop">{{ product.shop || '-' }}</span>
              </td>
              <td class="col-brand">
                <span class="brand-display">{{ product.brand || '-' }}</span>
              </td>
              <td class="col-region">
                <span class="region-display">{{ product.region || '-' }}</span>
              </td>
              <td class="col-time">
                <span class="time-display">{{ formatTime(product.crawl_time) }}</span>
              </td>
              <td class="col-actions">
                <button class="delete-btn" title="删除" @click="handleDelete(product)">
                  <Delete class="delete-icon" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-overlay">
          <div class="loading-content">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>
        </div>
      </div>

      <!-- 分页组件 -->
      <div class="table-pagination">
        <Pagination
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="total"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.products-container {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  animation: pageFadeIn 0.5s ease;
  position: relative;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  color: var(--primary-green);
}

.leaf-decoration--1 {
  top: -20px;
  right: -20px;
  opacity: 0.5;
}

.leaf-decoration--2 {
  bottom: 100px;
  left: -30px;
  opacity: 0.4;
}

/* ============================================
   Page Header
   ============================================ */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.header-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon-wrapper {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(82, 183, 136, 0.08));
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 18px;
  position: relative;
  overflow: hidden;
}

.title-icon-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent, rgba(116, 198, 157, 0.15));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.title-icon-wrapper:hover::before {
  opacity: 1;
}

.title-icon {
  width: 26px;
  height: 26px;
  color: var(--primary-green);
  position: relative;
  z-index: 1;
}

.title-text {
  flex: 1;
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 400;
}

.stats-badges {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.stat-badge {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 22px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.stat-badge:hover {
  border-color: var(--accent-green);
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

.stat-badge--active {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.08), rgba(116, 198, 157, 0.06));
  border-color: var(--primary-green);
}

.stat-label {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.stat-value {
  font-family: 'Nunito', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-badge--active .stat-value {
  color: var(--primary-green);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 22px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.action-btn:hover {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
  transform: translateY(-2px);
}

.action-btn--danger {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(220, 38, 38, 0.05));
  border-color: rgba(239, 68, 68, 0.2);
  color: #DC2626;
}

.action-btn--danger:hover {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1));
  border-color: #DC2626;
  box-shadow: 0 8px 25px rgba(220, 38, 38, 0.2);
}

.action-btn.loading {
  opacity: 0.7;
  pointer-events: none;
}

.action-btn .btn-icon {
  width: 17px;
  height: 17px;
  transition: transform 0.3s ease;
}

.action-btn .btn-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============================================
   Filter Panel
   ============================================ */
.filter-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.5s ease 0.1s backwards;
  box-shadow: var(--shadow-soft);
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
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s ease;
}

.filter-bar + .filter-grid {
  border-top: 1px solid var(--border-light);
}

.search-group {
  position: relative;
  flex: 1;
  max-width: 440px;
}

.search-icon {
  position: absolute;
  left: 18px;
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
  padding: 14px 18px 14px 50px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
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
  border-color: var(--border-focus);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.search-input:focus ~ .search-icon {
  color: var(--primary-green);
}

.filter-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: var(--bg-card);
  border-color: var(--accent-green);
  color: var(--primary-green);
}

.filter-toggle.active {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.06));
  border-color: var(--primary-green);
  color: var(--primary-green);
}

.filter-icon {
  width: 17px;
  height: 17px;
}

.active-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 7px;
  height: 7px;
  background: var(--primary-green);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--accent-green);
}

.sort-group {
  position: relative;
}

.sort-select {
  appearance: none;
  padding: 14px 42px 14px 18px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2340916C' d='M2 4l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.sort-select:hover {
  border-color: var(--accent-green);
}

.sort-select:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
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
  padding: 14px 22px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.search-btn {
  background: linear-gradient(135deg, var(--primary-green), var(--primary-teal));
  color: white;
  box-shadow: 0 4px 15px rgba(45, 106, 79, 0.25);
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(45, 106, 79, 0.35);
}

.reset-btn {
  background: transparent;
  border: 1px solid var(--border-light);
  color: var(--text-tertiary);
}

.reset-btn:hover {
  border-color: var(--accent-green);
  color: var(--primary-green);
  background: rgba(45, 106, 79, 0.05);
}

.btn-icon-sm {
  width: 15px;
  height: 15px;
}

/* Filter Grid */
.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 24px;
  animation: filterExpand 0.4s ease;
}

@keyframes filterExpand {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.filter-input {
  padding: 12px 16px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.filter-input::placeholder {
  color: var(--text-tertiary);
}

.filter-input:focus {
  outline: none;
  border-color: var(--border-focus);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.1);
}

.price-range-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.range-input {
  flex: 1;
  padding: 12px 14px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  text-align: center;
  transition: all 0.3s ease;
}

.range-input:focus {
  outline: none;
  border-color: var(--border-focus);
}

.range-divider {
  color: var(--text-tertiary);
  font-size: 13px;
  font-weight: 600;
}

/* ============================================
   Table Card
   ============================================ */
.table-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.5s ease 0.2s backwards;
  box-shadow: var(--shadow-soft);
}

.table-wrapper {
  position: relative;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: linear-gradient(180deg, var(--bg-sand) 0%, var(--bg-card) 100%);
  border-bottom: 1px solid var(--border-light);
}

.data-table th {
  padding: 18px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  white-space: nowrap;
}

.data-table tbody tr {
  border-bottom: 1px solid rgba(231, 229, 228, 0.6);
  transition: all 0.2s ease;
}

.data-table tbody tr:hover {
  background: rgba(116, 198, 157, 0.05);
}

.data-table tbody tr.row-selected {
  background: linear-gradient(90deg, rgba(45, 106, 79, 0.08), rgba(116, 198, 157, 0.04));
}

.data-table td {
  padding: 18px 20px;
}

.col-checkbox {
  width: 50px;
  text-align: center;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  accent-color: var(--primary-green);
  cursor: pointer;
}

.col-product {
  min-width: 320px;
}

.product-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
}

.product-thumb {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border-radius: 14px;
  overflow: hidden;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-placeholder {
  width: 26px;
  height: 26px;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.product-details {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.product-tags-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

.tag--brand {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.12), rgba(82, 183, 136, 0.08));
  color: var(--primary-green);
  border: 1px solid rgba(45, 106, 79, 0.15);
}

.tag--tag {
  background: rgba(0, 180, 216, 0.1);
  color: var(--accent-blue);
  border: 1px solid rgba(0, 180, 216, 0.15);
}

.col-price {
  width: 110px;
}

.price-display {
  font-family: 'Nunito', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-green);
  display: block;
}

.col-sales {
  width: 100px;
}

.sales-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sales-icon {
  width: 15px;
  height: 15px;
  color: var(--accent-blue);
}

.sales-display span {
  font-family: 'Nunito', sans-serif;
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 600;
}

.col-shop {
  width: 160px;
}

.shop-display {
  font-size: 13px;
  color: var(--text-secondary);
  display: block;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-brand {
  width: 100px;
}

.brand-display {
  font-size: 13px;
  color: var(--text-secondary);
  display: block;
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-region {
  width: 90px;
}

.region-display {
  font-size: 13px;
  color: var(--text-tertiary);
}

.col-time {
  width: 150px;
}

.time-display {
  font-size: 12px;
  color: var(--text-tertiary);
  font-family: 'Nunito', sans-serif;
  display: block;
}

.col-actions {
  width: 80px;
  text-align: center;
}

.delete-btn {
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.15);
  border-radius: 12px;
  color: #DC2626;
  cursor: pointer;
  transition: all 0.25s ease;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: #DC2626;
  transform: scale(1.05);
}

.delete-icon {
  width: 16px;
  height: 16px;
}

/* Empty State */
.empty-row td {
  padding: 0;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.empty-icon-wrapper {
  width: 88px;
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.05), rgba(116, 198, 157, 0.03));
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 24px;
  margin-bottom: 24px;
}

.empty-icon {
  width: 38px;
  height: 38px;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.empty-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* Loading Overlay */
.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  z-index: 10;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 44px;
  height: 44px;
  border: 4px solid var(--border-light);
  border-top-color: var(--primary-green);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

/* Table Pagination */
.table-pagination {
  padding: 20px 24px;
  border-top: 1px solid var(--border-light);
  background: linear-gradient(180deg, transparent, var(--bg-sand) 100%);
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 1400px) {
  .filter-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1200px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .filter-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .filter-bar {
    flex-wrap: wrap;
  }

  .search-group {
    max-width: 100%;
    order: 1;
    flex-basis: 100%;
  }

  .filter-toggle {
    order: 2;
  }

  .sort-group {
    order: 3;
  }

  .action-buttons {
    order: 4;
    width: 100%;
    margin-left: 0;
  }

  .search-btn,
  .reset-btn {
    flex: 1;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .title-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .header-actions {
    flex-wrap: wrap;
  }

  .stats-badges {
    width: 100%;
  }

  .stat-badge {
    flex: 1;
    min-width: 140px;
  }

  .leaf-decoration {
    display: none;
  }
}
</style>
