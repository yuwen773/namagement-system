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

// 表格列配置
const columns = [
  {
    type: 'selection',
    width: 50
  },
  {
    label: '商品信息',
    prop: 'title',
    minWidth: 280
  },
  {
    label: '价格',
    prop: 'price',
    width: 100,
    sortable: true
  },
  {
    label: '销量',
    prop: 'sales',
    width: 90,
    sortable: true
  },
  {
    label: '店铺',
    prop: 'shop',
    width: 150
  },
  {
    label: '品牌',
    prop: 'brand',
    width: 100
  },
  {
    label: '地区',
    prop: 'region',
    width: 90
  },
  {
    label: '采集时间',
    prop: 'crawl_time',
    width: 150
  },
  {
    label: '操作',
    prop: 'actions',
    width: 120,
    fixed: 'right'
  }
]

onMounted(() => {
  loadProducts()
})
</script>

<template>
  <div class="products-container">
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.products-container {
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
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(123, 44, 191, 0.1));
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}

.title-icon-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent, rgba(255, 107, 53, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.title-icon-wrapper:hover::before {
  opacity: 1;
}

.title-icon {
  width: 24px;
  height: 24px;
  color: var(--primary-orange);
  position: relative;
  z-index: 1;
}

.title-text {
  flex: 1;
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
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
  gap: 12px;
  flex-wrap: wrap;
}

.stat-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  transition: all 0.3s ease;
}

.stat-badge:hover {
  border-color: var(--border-default);
  transform: translateY(-2px);
}

.stat-badge--active {
  background: rgba(255, 107, 53, 0.08);
  border-color: rgba(255, 107, 53, 0.2);
}

.stat-label {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-badge--active .stat-value {
  color: var(--primary-orange);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
  transform: translateY(-2px);
}

.action-btn--danger {
  background: rgba(255, 107, 107, 0.1);
  border-color: rgba(255, 107, 107, 0.2);
  color: #FF6B6B;
}

.action-btn--danger:hover {
  background: rgba(255, 107, 107, 0.2);
  border-color: rgba(255, 107, 107, 0.4);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.2);
}

.action-btn.loading {
  opacity: 0.7;
  pointer-events: none;
}

.action-btn .btn-icon {
  width: 16px;
  height: 16px;
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
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s ease;
}

.filter-bar + .filter-grid {
  border-top: 1px solid var(--border-subtle);
}

.search-group {
  position: relative;
  flex: 1;
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

.search-input:focus + .search-icon {
  color: var(--primary-orange);
}

.filter-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 13px 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.filter-toggle.active {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.2);
  color: var(--primary-orange);
}

.filter-icon {
  width: 16px;
  height: 16px;
}

.active-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 6px;
  height: 6px;
  background: var(--primary-orange);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--primary-orange);
}

.sort-group {
  position: relative;
}

.sort-select {
  appearance: none;
  padding: 13px 40px 13px 18px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23ffffff40' d='M2 4l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
}

.sort-select:hover {
  border-color: var(--border-hover);
}

.sort-select:focus {
  outline: none;
  border-color: var(--primary-orange);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
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

/* Filter Grid */
.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 24px;
  animation: filterExpand 0.3s ease;
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
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-input {
  padding: 11px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 10px;
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
  border-color: var(--primary-orange);
  background: rgba(0, 0, 0, 0.4);
}

.price-range-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.range-input {
  flex: 1;
  padding: 11px 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  text-align: center;
  transition: all 0.3s ease;
}

.range-input:focus {
  outline: none;
  border-color: var(--primary-orange);
}

.range-divider {
  color: var(--text-tertiary);
  font-size: 12px;
  font-weight: 500;
}

/* ============================================
   Table Card
   ============================================ */
.table-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.4s ease;
  animation-delay: 0.2s;
  animation-fill-mode: both;
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
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid var(--border-subtle);
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
  border-bottom: 1px solid var(--border-subtle);
  transition: all 0.2s ease;
}

.data-table tbody tr:hover {
  background: rgba(255, 107, 53, 0.03);
}

.data-table tbody tr.row-selected {
  background: rgba(255, 107, 53, 0.08);
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
  accent-color: var(--primary-orange);
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
  width: 56px;
  height: 56px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
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
  width: 24px;
  height: 24px;
  color: var(--text-tertiary);
}

.product-details {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.product-tags-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 4px;
  white-space: nowrap;
}

.tag--brand {
  background: rgba(123, 44, 191, 0.15);
  color: #9D4EDD;
}

.tag--tag {
  background: rgba(255, 107, 53, 0.1);
  color: var(--primary-orange);
}

.col-price {
  width: 110px;
}

.price-display {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  font-weight: 700;
  color: var(--primary-orange);
  display: block;
}

.col-sales {
  width: 100px;
}

.sales-display {
  display: flex;
  align-items: center;
  gap: 6px;
}

.sales-icon {
  width: 14px;
  height: 14px;
  color: var(--primary-cyan);
}

.sales-display span {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
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
  font-size: 11px;
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
  display: block;
}

.col-actions {
  width: 80px;
  text-align: center;
}

.delete-btn {
  width: 36px;
  height: 36px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.2);
  border-radius: 10px;
  color: #FF6B6B;
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  background: rgba(255, 107, 107, 0.2);
  border-color: rgba(255, 107, 107, 0.4);
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
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 13px;
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
  background: rgba(13, 13, 20, 0.85);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--primary-orange);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

/* Table Pagination */
.table-pagination {
  padding: 20px 24px;
  border-top: 1px solid var(--border-subtle);
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
}
</style>
