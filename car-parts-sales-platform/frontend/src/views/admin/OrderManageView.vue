<template>
  <div class="order-manage-view">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">订单管理</h1>
        <p class="page-subtitle">管理平台订单、发货及退换货处理</p>
      </div>
      <div class="header-actions">
        <el-button :icon="Download" @click="handleExport">导出订单</el-button>
        <el-button type="primary" :icon="Refresh" @click="fetchOrderList">刷新</el-button>
      </div>
    </div>

    <!-- 快捷统计 -->
    <div class="stats-tabs">
      <div
        v-for="stat in orderStats"
        :key="stat.key"
        class="stat-tab"
        :class="{ active: filterForm.status === stat.key }"
        @click="handleStatClick(stat.key)"
      >
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>

    <!-- 筛选工具栏 -->
    <div class="filter-toolbar">
      <div class="filter-left">
        <el-input
          v-model="filterForm.search"
          placeholder="搜索订单号、用户手机号..."
          class="search-input"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select v-model="filterForm.status" placeholder="订单状态" clearable class="filter-select">
          <el-option label="待付款" value="pending_payment" />
          <el-option label="待发货" value="pending_shipment" />
          <el-option label="已发货" value="shipped" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>

        <el-date-picker
          v-model="filterForm.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          class="date-picker"
        />

        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button :icon="Refresh" @click="handleReset">重置</el-button>
      </div>
    </div>

    <!-- 订单列表 -->
    <div class="table-container">
      <el-table
        v-loading="loading"
        :data="tableData"
        style="width: 100%"
        :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
      >
        <el-table-column label="订单信息" min-width="280">
          <template #default="{ row }">
            <div class="order-info">
              <div class="order-no">{{ row.order_no }}</div>
              <div class="order-meta">
                <span class="user-info">
                  <el-icon><User /></el-icon>
                  {{ row.user_nickname || row.user_phone }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="商品信息" min-width="200">
          <template #default="{ row }">
            <div class="products-info">
              <div class="product-count">{{ row.items_count || 0 }} 件商品</div>
              <div class="product-preview">
                {{ row.product_names || '-' }}
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="金额" width="160" align="right">
          <template #default="{ row }">
            <div class="amount-cell">
              <div class="pay-amount">¥{{ row.pay_amount }}</div>
              <div v-if="row.discount_amount && row.discount_amount !== '0.00'" class="discount">
                优惠 ¥{{ row.discount_amount }}
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status_display || getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="物流" width="150">
          <template #default="{ row }">
            <div v-if="row.express_company || row.tracking_number" class="logistics-info">
              <div class="company">{{ row.express_company || '-' }}</div>
              <div class="tracking">{{ row.tracking_number || '-' }}</div>
            </div>
            <span v-else class="text-placeholder">-</span>
          </template>
        </el-table-column>

        <el-table-column label="创建时间" width="170">
          <template #default="{ row }">
            <span class="time-cell">{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" :icon="View" @click="handleViewOrder(row)">
              详情
            </el-button>
            <el-button
              v-if="row.status === 'pending_shipment'"
              link
              type="success"
              :icon="Promotion"
              @click="handleShip(row)"
            >
              发货
            </el-button>
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

    <!-- 订单详情对话框 -->
    <OrderDetailDialog
      v-model="orderDetailVisible"
      :order-id="currentOrderId"
      @refresh="fetchOrderList"
    />

    <!-- 发货对话框 -->
    <ShipDialog
      v-model="shipDialogVisible"
      :order="currentShipOrder"
      @success="handleShipSuccess"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Search, Refresh, View, Promotion, Download, User
} from '@element-plus/icons-vue'
import {
  getOrderListApi,
  getReturnListApi
} from '@/api/modules/order'
import OrderDetailDialog from './components/OrderDetailDialog.vue'
import ShipDialog from './components/ShipDialog.vue'

// 筛选表单
const filterForm = reactive({
  search: '',
  status: null,
  dateRange: null
})

// 表格数据
const loading = ref(false)
const tableData = ref([])

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框
const orderDetailVisible = ref(false)
const currentOrderId = ref(null)
const shipDialogVisible = ref(false)
const currentShipOrder = ref(null)

// 订单统计
const orderStats = ref([
  { key: null, label: '全部订单', value: 0 },
  { key: 'pending_payment', label: '待付款', value: 0 },
  { key: 'pending_shipment', label: '待发货', value: 0 },
  { key: 'shipped', label: '已发货', value: 0 },
  { key: 'completed', label: '已完成', value: 0 }
])

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

// 获取订单状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    pending_payment: 'warning',
    pending_shipment: 'info',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取订单状态标签
const getStatusLabel = (status) => {
  const labelMap = {
    pending_payment: '待付款',
    pending_shipment: '待发货',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labelMap[status] || status
}

// 获取订单列表
const fetchOrderList = async () => {
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
    if (filterForm.status) {
      params.status = filterForm.status
    }
    if (filterForm.dateRange && filterForm.dateRange.length === 2) {
      params.created_at__gte = filterForm.dateRange[0]
      params.created_at__lte = filterForm.dateRange[1]
    }

    const response = await getOrderListApi(params)
    tableData.value = response.results || []
    pagination.total = response.count || 0

    // 更新统计数据
    updateOrderStats()
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

// 更新订单统计
const updateOrderStats = async () => {
  try {
    const stats = orderStats.value
    for (const stat of stats) {
      if (stat.key === null) {
        const response = await getOrderListApi({ page: 1, page_size: 1 })
        stat.value = response.count || 0
      } else {
        const response = await getOrderListApi({ page: 1, page_size: 1, status: stat.key })
        stat.value = response.count || 0
      }
    }
  } catch (error) {
    console.error('获取订单统计失败:', error)
  }
}

// 统计标签点击
const handleStatClick = (key) => {
  filterForm.status = key
  pagination.page = 1
  fetchOrderList()
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchOrderList()
}

// 重置
const handleReset = () => {
  Object.assign(filterForm, {
    search: '',
    status: null,
    dateRange: null
  })
  pagination.page = 1
  fetchOrderList()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchOrderList()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchOrderList()
}

// 查看订单详情
const handleViewOrder = (row) => {
  currentOrderId.value = row.id
  orderDetailVisible.value = true
}

// 发货
const handleShip = (row) => {
  currentShipOrder.value = { ...row }
  shipDialogVisible.value = true
}

// 发货成功
const handleShipSuccess = () => {
  fetchOrderList()
}

// 导出订单
const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 初始化
onMounted(() => {
  fetchOrderList()
})
</script>

<style scoped>
.order-manage-view {
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
   统计标签
   ======================================== */
.stats-tabs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-tab {
  flex: 1;
  min-width: 120px;
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-tab:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-tab.active {
  border-color: #06b6d4;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(59, 130, 246, 0.05) 100%);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

/* ========================================
   筛选工具栏
   ======================================== */
.filter-toolbar {
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.search-input {
  width: 280px;
}

.filter-select {
  width: 150px;
}

.date-picker {
  width: 280px;
}

/* ========================================
   表格容器
   ======================================== */
.table-container {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.order-no {
  font-weight: 600;
  color: #1e293b;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
}

.order-meta {
  font-size: 13px;
  color: #64748b;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.products-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-count {
  font-size: 13px;
  color: #64748b;
}

.product-preview {
  font-size: 12px;
  color: #94a3b8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.amount-cell {
  text-align: right;
}

.pay-amount {
  font-size: 16px;
  font-weight: 700;
  color: #ef4444;
}

.discount {
  font-size: 12px;
  color: #10b981;
}

.logistics-info {
  font-size: 12px;
}

.company {
  color: #64748b;
  margin-bottom: 2px;
}

.tracking {
  color: #06b6d4;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
}

.text-placeholder {
  color: #cbd5e1;
}

.time-cell {
  color: #64748b;
  font-size: 13px;
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

  .date-picker {
    width: 240px;
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

  .stats-tabs {
    flex-direction: column;
  }

  .stat-tab {
    min-width: 100%;
  }

  .filter-left {
    flex-direction: column;
    width: 100%;
  }

  .search-input,
  .filter-select,
  .date-picker {
    width: 100%;
  }
}
</style>
