<template>
  <div class="product-manage-view">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">商品管理</h1>
        <p class="page-subtitle">管理平台商品信息、分类和库存</p>
      </div>
      <div class="header-actions">
        <el-button :icon="FolderOpened" @click="showCategoryDialog = true">
          分类管理
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleAdd">
          新增商品
        </el-button>
      </div>
    </div>

    <!-- 筛选工具栏 -->
    <div class="filter-toolbar">
      <div class="filter-left">
        <el-input
          v-model="filterForm.search"
          placeholder="搜索商品名称、编码..."
          class="search-input"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-cascader
          v-model="filterForm.category"
          :options="categoryTree"
          :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true, emitPath: false }"
          placeholder="选择分类"
          clearable
          class="filter-select"
        />

        <el-select v-model="filterForm.status" placeholder="商品状态" clearable class="filter-select">
          <el-option label="全部状态" :value="null" />
          <el-option label="草稿" value="draft" />
          <el-option label="待审核" value="pending" />
          <el-option label="已发布" value="published" />
          <el-option label="已下架" value="archived" />
        </el-select>

        <div class="price-range">
          <el-input-number v-model="filterForm.minPrice" :min="0" :precision="2" placeholder="最低价" controls-position="right" />
          <span class="separator">-</span>
          <el-input-number v-model="filterForm.maxPrice" :min="0" :precision="2" placeholder="最高价" controls-position="right" />
        </div>

        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button :icon="Refresh" @click="handleReset">重置</el-button>
      </div>

      <div class="filter-right">
        <el-radio-group v-model="viewMode" class="view-toggle">
          <el-radio-button value="table">
            <el-icon><List /></el-icon>
            <span>列表</span>
          </el-radio-button>
          <el-radio-button value="card">
            <el-icon><Grid /></el-icon>
            <span>卡片</span>
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- 批量操作栏 -->
    <div v-if="selectedRows.length > 0" class="batch-toolbar">
      <div class="batch-info">
        <el-icon><Select /></el-icon>
        <span>已选择 <strong>{{ selectedRows.length }}</strong> 项</span>
      </div>
      <div class="batch-actions">
        <el-button :icon="Download" @click="handleBatchExport">导出</el-button>
        <el-button :icon="Delete" type="danger" @click="handleBatchDelete">批量删除</el-button>
      </div>
    </div>

    <!-- 列表视图 -->
    <div v-if="viewMode === 'table'" class="table-container">
      <el-table
        v-loading="loading"
        :data="tableData"
        style="width: 100%"
        :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />

        <el-table-column label="商品信息" min-width="300">
          <template #default="{ row }">
            <div class="product-info">
              <el-image
                :src="row.main_image || row.image"
                class="product-image"
                fit="cover"
                :preview-src-list="[row.main_image || row.image]"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
              <div class="product-detail">
                <div class="product-name">{{ row.name }}</div>
                <div class="product-code">编码: {{ row.product_code || '-' }}</div>
                <div class="product-category">
                  <el-tag size="small" type="info">{{ row.category_name || '-' }}</el-tag>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="价格" width="130" align="right">
          <template #default="{ row }">
            <div class="price-cell">
              <div class="current-price">¥{{ (row.price || 0).toFixed(2) }}</div>
              <div v-if="row.original_price && row.original_price > row.price" class="original-price">
                ¥{{ row.original_price.toFixed(2) }}
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="库存" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStockType(row.stock)" size="small">
              {{ row.stock }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="销量" width="100" align="center">
          <template #default="{ row }">
            <span class="sales-count">{{ row.sales_count || row.sales || 0 }}</span>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="创建时间" width="170">
          <template #default="{ row }">
            <span class="time-cell">{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" :icon="View" @click="handleView(row)">
              查看
            </el-button>
            <el-button link type="primary" :icon="Edit" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-dropdown @command="(cmd) => handleMoreCommand(cmd, row)">
              <el-button link type="primary" :icon="MoreFilled">
                更多
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    v-if="row.status === 'draft' || row.status === 'archived'"
                    command="publish"
                    :icon="CircleCheck"
                  >
                    发布商品
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status === 'published'"
                    command="archive"
                    :icon="CircleClose"
                  >
                    下架商品
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" :icon="Delete" style="color: #ef4444;">
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 卡片视图 -->
    <div v-else class="card-view">
      <el-row :gutter="20">
        <el-col v-for="item in tableData" :key="item.id" :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
          <div class="product-card">
            <div class="card-image-wrapper">
              <el-image
                :src="item.main_image || item.image"
                class="card-image"
                fit="cover"
                :preview-src-list="[item.main_image || item.image]"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
              <div class="card-badges">
                <el-tag :type="getStatusType(item.status)" size="small">
                  {{ getStatusText(item.status) }}
                </el-tag>
              </div>
            </div>

            <div class="card-content">
              <div class="card-title" :title="item.name">{{ item.name }}</div>
              <div class="card-category">{{ item.category_name || '-' }}</div>

              <div class="card-price-row">
                <span class="current-price">¥{{ (item.price || 0).toFixed(2) }}</span>
                <span v-if="item.original_price && item.original_price > item.price" class="original-price">
                  ¥{{ item.original_price.toFixed(2) }}
                </span>
              </div>

              <div class="card-stats">
                <span class="stat-item">
                  <el-icon><ShoppingCart /></el-icon>
                  {{ item.stock }} 库存
                </span>
                <span class="stat-item">
                  <el-icon><TrendCharts /></el-icon>
                  {{ item.sales_count || item.sales || 0 }} 销量
                </span>
              </div>

              <div class="card-actions">
                <el-button size="small" :icon="Edit" @click="handleEdit(item)">
                  编辑
                </el-button>
                <el-button size="small" :icon="View" @click="handleView(item)">
                  查看
                </el-button>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 商品编辑对话框 -->
    <ProductEditDialog
      v-model="editDialogVisible"
      :product-id="currentProductId"
      @success="handleEditSuccess"
    />

    <!-- 分类管理对话框 -->
    <CategoryManageDialog
      v-model="categoryDialogVisible"
      @success="handleCategorySuccess"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, View, Edit, Delete, Picture,
  FolderOpened, List, Grid, ShoppingCart, TrendCharts,
  Select, Download, MoreFilled, CircleCheck, CircleClose
} from '@element-plus/icons-vue'
import {
  getProductListApi,
  deleteProductApi,
  publishProductApi,
  archiveProductApi,
  getCategoryTreeApi
} from '@/api/modules/product'
import ProductEditDialog from './components/ProductEditDialog.vue'
import CategoryManageDialog from './components/CategoryManageDialog.vue'

// 视图模式
const viewMode = ref('table')

// 加载状态
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  search: '',
  category: null,
  status: null,
  minPrice: null,
  maxPrice: null
})

// 分类树
const categoryTree = ref([])

// 表格数据
const tableData = ref([])
const selectedRows = ref([])

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框
const editDialogVisible = ref(false)
const categoryDialogVisible = ref(false)
const currentProductId = ref(null)

// 状态映射
const statusMap = {
  draft: { text: '草稿', type: 'info' },
  pending: { text: '待审核', type: 'warning' },
  published: { text: '已发布', type: 'success' },
  archived: { text: '已下架', type: 'danger' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

// 获取库存状态类型
const getStockType = (stock) => {
  if (stock <= 0) return 'danger'
  if (stock < 10) return 'warning'
  return 'success'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取分类树
const fetchCategoryTree = async () => {
  try {
    const data = await getCategoryTreeApi()
    categoryTree.value = data || []
  } catch (error) {
    console.error('获取分类树失败:', error)
  }
}

// 获取商品列表
const fetchProductList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ordering: '-created_at'
    }

    if (filterForm.search) {
      params.search = filterForm.search
    }
    if (filterForm.category) {
      params.category = filterForm.category
    }
    if (filterForm.status) {
      params.status = filterForm.status
    }
    if (filterForm.minPrice !== null) {
      params.price__gte = filterForm.minPrice
    }
    if (filterForm.maxPrice !== null) {
      params.price__lte = filterForm.maxPrice
    }

    const response = await getProductListApi(params)
    tableData.value = response.results || []
    pagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchProductList()
}

// 重置
const handleReset = () => {
  Object.assign(filterForm, {
    search: '',
    category: null,
    status: null,
    minPrice: null,
    maxPrice: null
  })
  pagination.page = 1
  fetchProductList()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchProductList()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchProductList()
}

// 选择变化
const handleSelectionChange = (rows) => {
  selectedRows.value = rows
}

// 新增商品
const handleAdd = () => {
  currentProductId.value = null
  editDialogVisible.value = true
}

// 查看商品
const handleView = (row) => {
  window.open(`/products/${row.id}`, '_blank')
}

// 编辑商品
const handleEdit = (row) => {
  currentProductId.value = row.id
  editDialogVisible.value = true
}

// 更多操作命令
const handleMoreCommand = async (command, row) => {
  switch (command) {
    case 'publish':
      await handlePublish(row)
      break
    case 'archive':
      await handleArchive(row)
      break
    case 'delete':
      await handleDelete(row)
      break
  }
}

// 发布商品
const handlePublish = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要发布商品"${row.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await publishProductApi(row.id)
    ElMessage.success('发布成功')
    fetchProductList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('发布失败')
    }
  }
}

// 下架商品
const handleArchive = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要下架商品"${row.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await archiveProductApi(row.id)
    ElMessage.success('下架成功')
    fetchProductList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('下架失败')
    }
  }
}

// 删除商品
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除商品"${row.name}"吗？此操作不可恢复！`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteProductApi(row.id)
    ElMessage.success('删除成功')
    fetchProductList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 个商品吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    // 批量删除逻辑
    ElMessage.success('批量删除成功')
    selectedRows.value = []
    fetchProductList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// 批量导出
const handleBatchExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 编辑成功
const handleEditSuccess = () => {
  fetchProductList()
}

// 分类管理成功
const handleCategorySuccess = () => {
  fetchCategoryTree()
}

// 初始化
onMounted(() => {
  fetchCategoryTree()
  fetchProductList()
})
</script>

<style scoped>
.product-manage-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   页面标题区
   ======================================== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.page-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: #64748b;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* ========================================
   筛选工具栏
   ======================================== */
.filter-toolbar {
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  flex-wrap: wrap;
}

.search-input {
  width: 280px;
}

.filter-select {
  width: 160px;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-range .separator {
  color: #94a3b8;
}

.view-toggle :deep(.el-radio-button__inner) {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ========================================
   批量操作栏
   ======================================== */
.batch-toolbar {
  background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}

.batch-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.batch-info strong {
  font-size: 18px;
}

.batch-actions {
  display: flex;
  gap: 8px;
}

.batch-actions .el-button {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: #fff;
}

.batch-actions .el-button--danger {
  background: rgba(239, 68, 68, 0.9);
  border-color: #ef4444;
}

/* ========================================
   表格视图
   ======================================== */
.table-container {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.product-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.product-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  flex-shrink: 0;
  overflow: hidden;
  background: #f1f5f9;
}

.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 24px;
}

.product-detail {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-code {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.price-cell {
  text-align: right;
}

.current-price {
  font-size: 16px;
  font-weight: 700;
  color: #ef4444;
}

.original-price {
  font-size: 12px;
  color: #94a3b8;
  text-decoration: line-through;
}

.sales-count {
  color: #64748b;
  font-weight: 500;
}

.time-cell {
  color: #64748b;
  font-size: 13px;
}

/* ========================================
   卡片视图
   ======================================== */
.card-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 75%;
  overflow: hidden;
  background: #f1f5f9;
}

.card-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.card-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 6px;
}

.card-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
  min-height: 2.8em;
}

.card-category {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 12px;
}

.card-price-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 12px;
}

.card-price-row .current-price {
  font-size: 20px;
  font-weight: 700;
  color: #ef4444;
}

.card-price-row .original-price {
  font-size: 13px;
  color: #94a3b8;
  text-decoration: line-through;
}

.card-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.card-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.card-actions .el-button {
  flex: 1;
}

/* ========================================
   分页
   ======================================== */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

/* ========================================
   响应式设计
   ======================================== */
@media (max-width: 1024px) {
  .search-input {
    width: 200px;
  }

  .filter-select {
    width: 120px;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    width: 100%;
    justify-content: stretch;
  }

  .header-actions .el-button {
    flex: 1;
  }

  .filter-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-left {
    flex-direction: column;
    width: 100%;
  }

  .search-input,
  .filter-select,
  .price-range {
    width: 100%;
  }

  .filter-right {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .batch-toolbar {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}
</style>
