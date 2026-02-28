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
    <!-- 头部操作区 -->
    <div class="header-section">
      <div class="header-left">
        <div class="header-title">
          <ShoppingCart class="title-icon" />
          <h2>宠物商品管理</h2>
        </div>
        <div class="header-stats">
          <span class="stat">共 <strong>{{ total }}</strong> 件商品</span>
          <span v-if="selectedIds.length > 0" class="stat selected">
            已选 <strong>{{ selectedIds.length }}</strong> 项
          </span>
        </div>
      </div>
      <div class="header-actions">
        <button
          v-if="selectedIds.length > 0"
          class="btn btn-danger"
          @click="handleBatchDelete"
        >
          <Delete class="btn-icon" />
          <span>批量删除</span>
        </button>
        <!-- <button class="btn btn-primary" @click="handleExport">
          <Download class="btn-icon" />
          <span>导出CSV</span>
        </button> -->
        <button class="btn btn-secondary" @click="loadProducts">
          <Refresh class="btn-icon" :class="{ spinning: loading }" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <!-- 搜索筛选区 -->
    <div class="filter-section">
      <div class="filter-bar">
        <div class="search-input-wrapper">
          <Search class="search-icon" />
          <input
            v-model="searchForm.search"
            type="text"
            placeholder="搜索商品标题..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>

        <button
          class="filter-toggle"
          :class="{ active: showFilters }"
          @click="showFilters = !showFilters"
        >
          <Filter class="filter-icon" />
          <span>筛选</span>
          <span v-if="hasActiveFilters" class="filter-badge"></span>
        </button>

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

        <button class="btn btn-search" @click="handleSearch">
          <Search class="btn-icon" />
          <span>搜索</span>
        </button>

        <button class="btn btn-reset" @click="handleReset">
          <span>重置</span>
        </button>
      </div>

      <!-- 展开的筛选条件 -->
      <div v-if="showFilters" class="filter-panel">
        <div class="filter-row">
          <div class="filter-group">
            <label>价格区间</label>
            <div class="price-range">
              <input
                v-model.number="searchForm.min_price"
                type="number"
                placeholder="最低价"
                class="filter-input"
              />
              <span class="range-separator">-</span>
              <input
                v-model.number="searchForm.max_price"
                type="number"
                placeholder="最高价"
                class="filter-input"
              />
            </div>
          </div>

          <div class="filter-group">
            <label>店铺名称</label>
            <input
              v-model="searchForm.shop"
              type="text"
              placeholder="输入店铺名"
              class="filter-input"
            />
          </div>

          <div class="filter-group">
            <label>品牌</label>
            <input
              v-model="searchForm.brand"
              type="text"
              placeholder="输入品牌名"
              class="filter-input"
            />
          </div>
        </div>

        <div class="filter-row">
          <div class="filter-group">
            <label>地区</label>
            <input
              v-model="searchForm.region"
              type="text"
              placeholder="如：广东、上海"
              class="filter-input"
            />
          </div>

          <div class="filter-group">
            <label>类目</label>
            <input
              v-model="searchForm.category"
              type="text"
              placeholder="如：狗粮、猫砂"
              class="filter-input"
            />
          </div>

          <div class="filter-group">
            <label>标签</label>
            <input
              v-model="searchForm.tags"
              type="text"
              placeholder="商品标签"
              class="filter-input"
            />
          </div>
        </div>

        <div class="filter-row">
          <div class="filter-group">
            <label>批次号</label>
            <input
              v-model="searchForm.batch_no"
              type="text"
              placeholder="采集批次号"
              class="filter-input"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 商品表格 -->
    <div class="table-section">
      <div class="table-container">
        <table class="product-table">
          <thead>
            <tr>
              <th class="col-check">
                <input
                  type="checkbox"
                  :checked="selectedIds.length > 0 && selectedIds.length === products.length"
                  @change="toggleSelectAll"
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
                <div class="empty-state">
                  <ShoppingCart class="empty-icon" />
                  <p>暂无商品数据</p>
                  <small>点击"刷新"按钮加载数据</small>
                </div>
              </td>
            </tr>
            <tr
              v-for="product in products"
              :key="product.id"
              class="product-row"
              :class="{ selected: selectedIds.includes(product.id) }"
            >
              <td class="col-check">
                <input
                  type="checkbox"
                  :checked="selectedIds.includes(product.id)"
                  @change="toggleSelect(product.id)"
                />
              </td>
              <td class="col-product">
                <div class="product-cell">
                  <div class="product-image">
                    <img
                      v-if="product.image_url"
                      :src="product.image_url"
                      :alt="product.title"
                      @error="handleImageError"
                    />
                    <Picture v-else class="image-placeholder" />
                  </div>
                  <div class="product-info">
                    <h4 class="product-title">{{ product.title }}</h4>
                    <div class="product-meta">
                      <span v-if="product.brand" class="product-brand">{{ product.brand }}</span>
                      <span v-if="product.tags" class="product-tags">{{ product.tags }}</span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="col-price">
                <span class="price-value">{{ formatPrice(product.price) }}</span>
                <span v-if="product.price_unit" class="price-unit">{{ product.price_unit }}</span>
              </td>
              <td class="col-sales">
                <div class="sales-value">
                  <TrendCharts class="sales-icon" />
                  <span>{{ formatSales(product.sales) }}</span>
                </div>
              </td>
              <td class="col-shop">
                <span class="shop-name" :title="product.shop">{{ product.shop || '-' }}</span>
                <span v-if="product.seller_nick" class="seller-nick">{{ product.seller_nick }}</span>
              </td>
              <td class="col-brand">
                <span class="brand-value">{{ product.brand || '-' }}</span>
              </td>
              <td class="col-region">
                <span class="region-value">{{ product.region || '-' }}</span>
              </td>
              <td class="col-time">
                <span class="time-value">{{ formatTime(product.crawl_time) }}</span>
                <span v-if="product.batch_no" class="batch-no" :title="'批次: ' + product.batch_no">📦</span>
              </td>
              <td class="col-actions">
                <div class="action-buttons">
                  <!-- <button class="action-btn btn-edit" title="编辑" @click="handleEdit(product)">
                    <Edit class="action-icon" />
                  </button> -->
                  <button class="action-btn btn-delete" title="删除" @click="handleDelete(product)">
                    <Delete class="action-icon" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 加载中遮罩 -->
        <div v-if="loading" class="table-loading">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

.products-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 头部区域 */
.header-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-title .title-icon {
  width: 28px;
  height: 28px;
  color: #FF6B35;
}

.header-title h2 {
  font-size: 20px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 20px;
}

.header-stats .stat {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.header-stats .stat strong {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
}

.header-stats .stat.selected strong {
  color: #FF6B35;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 按钮样式 */
.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.btn-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.btn-primary {
  background: linear-gradient(135deg, #FF6B35, #FF8C5A);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
}

.btn-danger {
  background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
  color: white;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-search {
  background: linear-gradient(135deg, #7B2CBF, #9D4EDD);
  color: white;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(123, 44, 191, 0.4);
}

.btn-reset {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
}

.btn-reset:hover {
  border-color: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
}

/* 筛选区域 */
.filter-section {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.4);
}

.search-input {
  width: 100%;
  padding: 12px 14px 12px 44px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-family: 'Noto Sans SC', sans-serif;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.search-input:focus {
  outline: none;
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.filter-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.filter-toggle.active {
  background: rgba(255, 107, 53, 0.1);
  border-color: #FF6B35;
  color: #FF6B35;
}

.filter-icon {
  width: 16px;
  height: 16px;
}

.filter-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: #FF6B35;
  border-radius: 50%;
}

.sort-select {
  padding: 12px 16px;
  padding-right: 36px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-family: 'Noto Sans SC', sans-serif;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23ffffff40' d='M2 4l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

.sort-select:focus {
  outline: none;
  border-color: #FF6B35;
}

.filter-panel {
  padding: 0 20px 20px;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-row {
  display: flex;
  gap: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.filter-group label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.filter-input {
  padding: 10px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  transition: all 0.3s ease;
}

.filter-input:focus {
  outline: none;
  border-color: #FF6B35;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.range-separator {
  color: rgba(255, 255, 255, 0.3);
}

/* 表格区域 */
.table-section {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.table-container {
  position: relative;
  overflow-x: auto;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
}

.product-table thead {
  background: rgba(0, 0, 0, 0.3);
}

.product-table th {
  padding: 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.product-table tbody tr {
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  transition: all 0.2s ease;
}

.product-table tbody tr:hover {
  background: rgba(255, 107, 53, 0.03);
}

.product-table tbody tr.selected {
  background: rgba(255, 107, 53, 0.08);
}

.product-table td {
  padding: 16px;
}

.col-check {
  width: 50px;
  text-align: center;
}

.col-check input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #FF6B35;
  cursor: pointer;
}

.col-product {
  min-width: 300px;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.product-image {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.2);
}

.product-info {
  flex: 1;
  min-width: 0;
}

.product-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-meta {
  display: flex;
  gap: 6px;
  align-items: center;
}

.product-brand {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  background: rgba(123, 44, 191, 0.2);
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.product-tags {
  font-size: 11px;
  color: rgba(255, 107, 53, 0.6);
  background: rgba(255, 107, 53, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-price {
  width: 100px;
}

.price-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  font-weight: 600;
  color: #FF6B35;
}

.price-unit {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin-left: 2px;
}

.col-sales {
  width: 90px;
}

.sales-value {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.sales-icon {
  width: 14px;
  height: 14px;
  color: #06FFA5;
}

.col-shop {
  width: 150px;
}

.shop-name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  display: block;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.seller-nick {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  display: block;
  margin-top: 2px;
}

.col-brand {
  width: 100px;
}

.brand-value {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  display: block;
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-region {
  width: 90px;
}

.region-value {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.col-time {
  width: 150px;
}

.time-value {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  font-family: 'JetBrains Mono', monospace;
  display: block;
}

.batch-no {
  font-size: 12px;
  margin-left: 4px;
  cursor: help;
}

.col-actions {
  width: 120px;
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-icon {
  width: 16px;
  height: 16px;
}

.btn-edit {
  background: rgba(123, 44, 191, 0.15);
  color: #9D4EDD;
}

.btn-edit:hover {
  background: rgba(123, 44, 191, 0.3);
  transform: scale(1.05);
}

.btn-delete {
  background: rgba(255, 107, 107, 0.15);
  color: #FF6B6B;
}

.btn-delete:hover {
  background: rgba(255, 107, 107, 0.3);
  transform: scale(1.05);
}

/* 空状态 */
.empty-row td {
  padding: 80px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.3);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  margin: 0 0 8px 0;
}

.empty-state small {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.2);
}

/* 加载遮罩 */
.table-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(15, 15, 26, 0.8);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #FF6B35;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.table-loading p {
  margin-top: 16px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

/* 分页 */
.pagination-section {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
}

/* 响应式 */
@media (max-width: 1200px) {
  .filter-row {
    flex-direction: column;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .filter-bar {
    flex-wrap: wrap;
  }

  .search-input-wrapper {
    max-width: 100%;
    order: 1;
  }

  .filter-toggle {
    order: 2;
  }

  .sort-select {
    order: 3;
  }

  .btn-search,
  .btn-reset {
    order: 4;
  }

  .header-actions {
    flex-wrap: wrap;
  }

  .btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>
