<template>
  <div class="marketing-manage-view">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">营销管理</h1>
        <p class="page-subtitle">管理平台优惠券、促销活动和营销素材</p>
      </div>
      <div class="header-actions">
        <el-button :icon="DataAnalysis" @click="showStatsDialog = true">
          数据统计
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleAddCoupon">
          新增优惠券
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);">
          <el-icon :size="24"><Ticket /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalCoupons }}</div>
          <div class="stat-label">优惠券总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);">
          <el-icon :size="24"><SuccessFilled /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.activeCoupons }}</div>
          <div class="stat-label">启用中</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
          <el-icon :size="24"><UserFilled /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalIssued }}</div>
          <div class="stat-label">已发放</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
          <el-icon :size="24"><CircleCheck /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalUsed }}</div>
          <div class="stat-label">已使用</div>
        </div>
      </div>
    </div>

    <!-- 选项卡 -->
    <el-tabs v-model="activeTab" class="content-tabs">
      <!-- 优惠券管理 -->
      <el-tab-pane label="优惠券管理" name="coupons">
        <!-- 筛选工具栏 -->
        <div class="filter-toolbar">
          <div class="filter-left">
            <el-input
              v-model="couponFilter.search"
              placeholder="搜索优惠券名称..."
              class="search-input"
              clearable
              @clear="handleCouponSearch"
              @keyup.enter="handleCouponSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>

            <el-select v-model="couponFilter.type" placeholder="优惠类型" clearable class="filter-select">
              <el-option label="全部类型" value="" />
              <el-option label="满减券" value="full_reduction" />
              <el-option label="折扣券" value="discount" />
            </el-select>

            <el-select v-model="couponFilter.status" placeholder="状态" clearable class="filter-select">
              <el-option label="全部状态" value="" />
              <el-option label="启用" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>

            <el-button type="primary" :icon="Search" @click="handleCouponSearch">搜索</el-button>
            <el-button :icon="Refresh" @click="handleCouponReset">重置</el-button>
          </div>
        </div>

        <!-- 优惠券列表 -->
        <div class="table-container">
          <el-table
            v-loading="couponLoading"
            :data="couponList"
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
          >
            <el-table-column label="优惠券信息" min-width="280">
              <template #default="{ row }">
                <div class="coupon-info">
                  <div class="coupon-badge" :class="`type-${row.discount_type}`">
                    <span v-if="row.discount_type === 'full_reduction'">满减</span>
                    <span v-else>折扣</span>
                  </div>
                  <div class="coupon-detail">
                    <div class="coupon-name">{{ row.name }}</div>
                    <div class="coupon-desc">{{ row.description || '暂无描述' }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="优惠内容" width="180">
              <template #default="{ row }">
                <div class="discount-content">
                  <span v-if="row.discount_type === 'full_reduction'" class="discount-value">
                    ¥{{ row.discount_amount }}
                  </span>
                  <span v-else class="discount-value">
                    {{ row.discount_rate }}折
                  </span>
                  <span v-if="parseFloat(row.min_amount) > 0" class="discount-condition">
                    满¥{{ row.min_amount }}
                  </span>
                  <span v-else class="discount-condition">
                    无门槛
                  </span>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="有效期" width="200">
              <template #default="{ row }">
                <div class="validity-period">
                  <div class="date-row">{{ formatDate(row.valid_from) }}</div>
                  <div class="date-row">{{ formatDate(row.valid_until) }}</div>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="发放情况" width="150" align="center">
              <template #default="{ row }">
                <div class="issue-stats">
                  <el-progress
                    :percentage="getIssuePercentage(row)"
                    :color="getIssueColor(row)"
                    :stroke-width="8"
                    :show-text="false"
                  />
                  <div class="issue-text">
                    <span>{{ row.issued_quantity || 0 }}</span>
                    <span v-if="row.total_quantity > 0"> / {{ row.total_quantity }}</span>
                    <span v-else> / 不限量</span>
                  </div>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="限领" width="100" align="center">
              <template #default="{ row }">
                <span class="limit-text">{{ row.per_user_limit }}张/人</span>
              </template>
            </el-table-column>

            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-switch
                  v-model="row.is_active"
                  @change="handleStatusChange(row)"
                />
              </template>
            </el-table-column>

            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="Edit" @click="handleEditCoupon(row)">
                  编辑
                </el-button>
                <el-button link type="primary" :icon="View" @click="handleViewUserCoupons(row)">
                  领取记录
                </el-button>
                <el-button link type="danger" :icon="Delete" @click="handleDeleteCoupon(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="couponPagination.page"
              v-model:page-size="couponPagination.pageSize"
              :page-sizes="[10, 30, 50]"
              :total="couponPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleCouponSizeChange"
              @current-change="handleCouponPageChange"
            />
          </div>
        </div>
      </el-tab-pane>

      <!-- 用户优惠券记录 -->
      <el-tab-pane label="领取记录" name="user-coupons">
        <div class="filter-toolbar">
          <div class="filter-left">
            <el-select v-model="userCouponFilter.status" placeholder="状态" clearable class="filter-select">
              <el-option label="全部状态" value="" />
              <el-option label="未使用" value="unused" />
              <el-option label="已使用" value="used" />
              <el-option label="已过期" value="expired" />
            </el-select>

            <el-button type="primary" :icon="Search" @click="handleUserCouponSearch">搜索</el-button>
            <el-button :icon="Refresh" @click="handleUserCouponReset">重置</el-button>
          </div>
        </div>

        <div class="table-container">
          <el-table
            v-loading="userCouponLoading"
            :data="userCouponList"
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
          >
            <el-table-column label="优惠券" min-width="200">
              <template #default="{ row }">
                <div class="coupon-name">{{ row.coupon?.name || '-' }}</div>
              </template>
            </el-table-column>

            <el-table-column label="用户" width="120">
              <template #default="{ row }">
                <span>{{ row.user_phone || '-' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="优惠类型" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.coupon?.discount_type === 'full_reduction'" size="small" type="warning">
                  满减
                </el-tag>
                <el-tag v-else size="small" type="success">
                  折扣
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="优惠内容" width="150">
              <template #default="{ row }">
                <div class="discount-content">
                  <span v-if="row.coupon?.discount_type === 'full_reduction'">
                    ¥{{ row.coupon.discount_amount }}
                  </span>
                  <span v-else>{{ row.coupon?.discount_rate }}折</span>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getUserCouponStatusType(row.status)" size="small">
                  {{ getUserCouponStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="领取时间" width="170">
              <template #default="{ row }">
                <span>{{ formatDateTime(row.obtained_at) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="使用时间" width="170">
              <template #default="{ row }">
                <span>{{ row.used_at ? formatDateTime(row.used_at) : '-' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button
                  v-if="row.used_order"
                  link
                  type="primary"
                  :icon="View"
                  @click="handleViewOrder(row.used_order)"
                >
                  查看订单
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="userCouponPagination.page"
              v-model:page-size="userCouponPagination.pageSize"
              :page-sizes="[10, 30, 50]"
              :total="userCouponPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleUserCouponSizeChange"
              @current-change="handleUserCouponPageChange"
            />
          </div>
        </div>
      </el-tab-pane>

      <!-- 促销活动 -->
      <el-tab-pane label="促销活动" name="promotions">
        <div class="empty-state">
          <el-icon :size="64" color="#94a3b8"><Promotion /></el-icon>
          <p>促销活动功能开发中...</p>
        </div>
      </el-tab-pane>

      <!-- 营销素材 -->
      <el-tab-pane label="营销素材" name="materials">
        <div class="empty-state">
          <el-icon :size="64" color="#94a3b8"><Picture /></el-icon>
          <p>Banner/海报管理功能开发中...</p>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 优惠券编辑对话框 -->
    <CouponEditDialog
      v-model="editDialogVisible"
      :coupon-id="currentCouponId"
      @success="handleCouponEditSuccess"
    />

    <!-- 用户优惠券领取记录对话框 -->
    <el-dialog
      v-model="userCouponListDialogVisible"
      title="领取记录"
      width="900px"
    >
      <el-table
        v-loading="userCouponListLoading"
        :data="currentUserCouponList"
        style="width: 100%"
      >
        <el-table-column label="用户" prop="user_phone" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getUserCouponStatusType(row.status)" size="small">
              {{ getUserCouponStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="领取时间" width="170">
          <template #default="{ row }">
            {{ formatDateTime(row.obtained_at) }}
          </template>
        </el-table-column>
        <el-table-column label="使用时间" width="170">
          <template #default="{ row }">
            {{ row.used_at ? formatDateTime(row.used_at) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="订单号" prop="used_order" />
      </el-table>
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="userCouponListPagination.page"
          v-model:page-size="userCouponListPagination.pageSize"
          :total="userCouponListPagination.total"
          layout="total, prev, pager, next"
          @current-change="loadUserCouponList"
        />
      </div>
    </el-dialog>

    <!-- 统计数据对话框 -->
    <el-dialog
      v-model="showStatsDialog"
      title="营销数据统计"
      width="600px"
    >
      <div class="stats-dialog-content">
        <h3>优惠券发放统计</h3>
        <div class="stats-list">
          <div class="stats-item">
            <span class="stats-label">总优惠券数：</span>
            <span class="stats-value">{{ statsDetail.totalCoupons }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">启用中：</span>
            <span class="stats-value">{{ statsDetail.activeCoupons }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">禁用中：</span>
            <span class="stats-value">{{ statsDetail.inactiveCoupons }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">已发放总量：</span>
            <span class="stats-value">{{ statsDetail.totalIssued }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">已使用：</span>
            <span class="stats-value">{{ statsDetail.totalUsed }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">未使用：</span>
            <span class="stats-value">{{ statsDetail.totalUnused }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">使用率：</span>
            <span class="stats-value">{{ statsDetail.usageRate }}%</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, View, Edit, Delete, Ticket, SuccessFilled,
  UserFilled, CircleCheck, DataAnalysis, Promotion, Picture
} from '@element-plus/icons-vue'
import {
  getCouponListApi,
  deleteCouponApi,
  patchCouponApi,
  getUserCouponsApi
} from '@/api/modules/marketing'
import CouponEditDialog from './components/CouponEditDialog.vue'

// 当前选项卡
const activeTab = ref('coupons')

// 统计数据
const stats = reactive({
  totalCoupons: 0,
  activeCoupons: 0,
  totalIssued: 0,
  totalUsed: 0
})

const statsDetail = reactive({
  totalCoupons: 0,
  activeCoupons: 0,
  inactiveCoupons: 0,
  totalIssued: 0,
  totalUsed: 0,
  totalUnused: 0,
  usageRate: 0
})

const showStatsDialog = ref(false)

// 优惠券列表
const couponLoading = ref(false)
const couponList = ref([])
const couponFilter = reactive({
  search: '',
  type: '',
  status: ''
})
const couponPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 用户优惠券列表
const userCouponLoading = ref(false)
const userCouponList = ref([])
const userCouponFilter = reactive({
  status: ''
})
const userCouponPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 对话框
const editDialogVisible = ref(false)
const currentCouponId = ref(null)
const userCouponListDialogVisible = ref(false)
const currentUserCouponList = ref([])
const userCouponListLoading = ref(false)
const userCouponListPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})
const currentCouponForUserList = ref(null)

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const formatDateTime = (dateStr) => {
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

// 计算发放进度百分比
const getIssuePercentage = (row) => {
  if (!row.total_quantity || row.total_quantity === 0) return 0
  return Math.min(100, Math.round((row.issued_quantity / row.total_quantity) * 100))
}

// 获取进度条颜色
const getIssueColor = (row) => {
  const percentage = getIssuePercentage(row)
  if (percentage >= 90) return '#ef4444'
  if (percentage >= 70) return '#f97316'
  return '#22c55e'
}

// 用户优惠券状态映射
const getUserCouponStatusText = (status) => {
  const statusMap = {
    unused: '未使用',
    used: '已使用',
    expired: '已过期'
  }
  return statusMap[status] || status
}

const getUserCouponStatusType = (status) => {
  const typeMap = {
    unused: 'success',
    used: 'info',
    expired: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取优惠券列表
const fetchCouponList = async () => {
  couponLoading.value = true
  try {
    const params = {
      page: couponPagination.page,
      page_size: couponPagination.pageSize
    }

    const response = await getCouponListApi(params)
    couponList.value = response.results || []
    couponPagination.total = response.count || 0

    // 更新统计数据
    updateStats(response.results || [])
  } catch (error) {
    ElMessage.error('获取优惠券列表失败')
  } finally {
    couponLoading.value = false
  }
}

// 更新统计数据
const updateStats = (coupons) => {
  stats.totalCoupons = coupons.length
  stats.activeCoupons = coupons.filter(c => c.is_active).length
  stats.totalIssued = coupons.reduce((sum, c) => sum + (c.issued_quantity || 0), 0)
  // 统计已使用数量（从用户优惠券数据获取）
}

// 获取用户优惠券列表
const fetchUserCouponList = async () => {
  userCouponLoading.value = true
  try {
    const params = {
      page: userCouponPagination.page,
      page_size: userCouponPagination.pageSize
    }

    const response = await getUserCouponsApi(params)
    userCouponList.value = response.results || []
    userCouponPagination.total = response.count || 0

    // 更新已使用统计
    stats.totalUsed = userCouponList.value.filter(c => c.status === 'used').length
  } catch (error) {
    ElMessage.error('获取领取记录失败')
  } finally {
    userCouponLoading.value = false
  }
}

// 优惠券搜索
const handleCouponSearch = () => {
  couponPagination.page = 1
  fetchCouponList()
}

const handleCouponReset = () => {
  Object.assign(couponFilter, {
    search: '',
    type: '',
    status: ''
  })
  couponPagination.page = 1
  fetchCouponList()
}

const handleCouponPageChange = (page) => {
  couponPagination.page = page
  fetchCouponList()
}

const handleCouponSizeChange = (size) => {
  couponPagination.pageSize = size
  couponPagination.page = 1
  fetchCouponList()
}

// 用户优惠券搜索
const handleUserCouponSearch = () => {
  userCouponPagination.page = 1
  fetchUserCouponList()
}

const handleUserCouponReset = () => {
  userCouponFilter.status = ''
  userCouponPagination.page = 1
  fetchUserCouponList()
}

const handleUserCouponPageChange = (page) => {
  userCouponPagination.page = page
  fetchUserCouponList()
}

const handleUserCouponSizeChange = (size) => {
  userCouponPagination.pageSize = size
  userCouponPagination.page = 1
  fetchUserCouponList()
}

// 新增优惠券
const handleAddCoupon = () => {
  currentCouponId.value = null
  editDialogVisible.value = true
}

// 编辑优惠券
const handleEditCoupon = (row) => {
  currentCouponId.value = row.id
  editDialogVisible.value = true
}

// 删除优惠券
const handleDeleteCoupon = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除优惠券"${row.name}"吗？此操作不可恢复！`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteCouponApi(row.id)
    ElMessage.success('删除成功')
    fetchCouponList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 状态切换
const handleStatusChange = async (row) => {
  try {
    await patchCouponApi(row.id, { is_active: row.is_active })
    ElMessage.success(row.is_active ? '已启用' : '已禁用')
    fetchCouponList()
  } catch (error) {
    row.is_active = !row.is_active // 回滚状态
    ElMessage.error('状态更新失败')
  }
}

// 查看用户领取记录
const handleViewUserCoupons = async (row) => {
  currentCouponForUserList.value = row.id
  userCouponListDialogVisible.value = true
  userCouponListPagination.page = 1
  await loadUserCouponList()
}

// 加载指定优惠券的用户领取记录
const loadUserCouponList = async () => {
  userCouponListLoading.value = true
  try {
    const params = {
      page: userCouponListPagination.page,
      page_size: userCouponListPagination.pageSize,
      coupon: currentCouponForUserList.value
    }

    const response = await getUserCouponsApi(params)
    currentUserCouponList.value = response.results || []
    userCouponListPagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('获取领取记录失败')
  } finally {
    userCouponListLoading.value = false
  }
}

// 查看订单
const handleViewOrder = (orderId) => {
  window.open(`/admin/orders?order_id=${orderId}`, '_blank')
}

// 编辑成功
const handleCouponEditSuccess = () => {
  fetchCouponList()
}

// 加载统计详情
const loadStatsDetail = async () => {
  try {
    const [couponRes, userCouponRes] = await Promise.all([
      getCouponListApi({ page: 1, page_size: 1000 }),
      getUserCouponsApi({ page: 1, page_size: 1000 })
    ])

    const allCoupons = couponRes.results || []
    const allUserCoupons = userCouponRes.results || []

    statsDetail.totalCoupons = allCoupons.length
    statsDetail.activeCoupons = allCoupons.filter(c => c.is_active).length
    statsDetail.inactiveCoupons = allCoupons.filter(c => !c.is_active).length
    statsDetail.totalIssued = allUserCoupons.length
    statsDetail.totalUsed = allUserCoupons.filter(c => c.status === 'used').length
    statsDetail.totalUnused = allUserCoupons.filter(c => c.status === 'unused').length
    statsDetail.usageRate = statsDetail.totalIssued > 0
      ? ((statsDetail.totalUsed / statsDetail.totalIssued) * 100).toFixed(1)
      : 0
  } catch (error) {
    console.error('加载统计详情失败', error)
  }
}

// 监听统计对话框打开
watch(showStatsDialog, (val) => {
  if (val) {
    loadStatsDetail()
  }
})

// 初始化
onMounted(() => {
  fetchCouponList()
  fetchUserCouponList()
})
</script>

<style scoped>
.marketing-manage-view {
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
   统计卡片
   ======================================== */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

/* ========================================
   选项卡
   ======================================== */
.content-tabs {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.content-tabs :deep(.el-tabs__header) {
  margin-bottom: 20px;
}

/* ========================================
   筛选工具栏
   ======================================== */
.filter-toolbar {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
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
  width: 140px;
}

/* ========================================
   表格容器
   ======================================== */
.table-container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

/* ========================================
   优惠券信息
   ======================================== */
.coupon-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.coupon-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.coupon-badge.type-full_reduction {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #fff;
}

.coupon-badge.type-discount {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: #fff;
}

.coupon-detail {
  flex: 1;
  min-width: 0;
}

.coupon-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.coupon-desc {
  font-size: 12px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ========================================
   优惠内容
   ======================================== */
.discount-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.discount-value {
  font-size: 18px;
  font-weight: 700;
  color: #f97316;
}

.discount-condition {
  font-size: 12px;
  color: #64748b;
}

/* ========================================
   有效期
   ======================================== */
.validity-period {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.date-row {
  font-size: 13px;
  color: #64748b;
}

/* ========================================
   发放统计
   ======================================== */
.issue-stats {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.issue-text {
  font-size: 12px;
  color: #64748b;
}

.issue-text span:first-child {
  font-weight: 600;
  color: #1e293b;
}

/* ========================================
   限领文本
   ======================================== */
.limit-text {
  font-size: 13px;
  color: #64748b;
}

/* ========================================
   分页
   ======================================== */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px;
}

/* ========================================
   空状态
   ======================================== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #94a3b8;
}

.empty-state p {
  margin-top: 16px;
  font-size: 14px;
}

/* ========================================
   统计对话框
   ======================================== */
.stats-dialog-content h3 {
  margin: 0 0 20px;
  font-size: 16px;
  color: #1e293b;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.stats-label {
  color: #64748b;
}

.stats-value {
  font-weight: 600;
  color: #1e293b;
}

/* ========================================
   响应式设计
   ======================================== */
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

  .stats-cards {
    grid-template-columns: 1fr;
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
  .filter-select {
    width: 100%;
  }
}
</style>
