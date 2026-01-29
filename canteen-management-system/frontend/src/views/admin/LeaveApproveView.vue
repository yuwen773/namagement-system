<template>
  <div class="leave-approve-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon :size="24"><DocumentChecked /></el-icon>
        请假审批
      </h2>
      <p class="page-desc">审批员工的请假申请，管理请假记录</p>
    </div>

    <!-- 状态 Tab 切换 -->
    <div class="status-tabs">
      <el-radio-group v-model="activeTab" size="large" @change="handleTabChange">
        <el-radio-button value="all">
          <el-icon><List /></el-icon>
          <span>全部</span>
          <el-badge v-if="tabCounts.all > 0" :value="tabCounts.all" class="tab-badge" />
        </el-radio-button>
        <el-radio-button value="PENDING">
          <el-icon><Clock /></el-icon>
          <span>待审批</span>
          <el-badge v-if="tabCounts.pending > 0" :value="tabCounts.pending" class="tab-badge" />
        </el-radio-button>
        <el-radio-button value="APPROVED">
          <el-icon><Select /></el-icon>
          <span>已通过</span>
        </el-radio-button>
        <el-radio-button value="REJECTED">
          <el-icon><Close /></el-icon>
          <span>已驳回</span>
        </el-radio-button>
      </el-radio-group>

      <div class="filter-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索姓名、电话、原因"
          :prefix-icon="Search"
          clearable
          style="width: 280px"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        />
        <el-button :icon="Search" @click="handleSearch">查询</el-button>
        <el-button :icon="Refresh" @click="handleRefresh">刷新</el-button>
      </div>
    </div>

    <!-- 请假申请列表 -->
    <el-table
      v-loading="loading"
      :data="leaveList"
      stripe
      class="data-table"
      :header-cell-style="{ background: '#FFF8F0', color: '#333' }"
      :row-class-name="getRowClassName"
    >
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="employee_name" label="员工姓名" min-width="100" />
      <el-table-column prop="employee_position" label="岗位" width="100" align="center">
        <template #default="{ row }">
          <el-tag v-if="row.employee_position" :type="getPositionTagType(row.employee_position)" size="small">
            {{ row.employee_position_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="leave_type_display" label="请假类型" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="getLeaveTypeTagType(row.leave_type)" size="small">
            {{ row.leave_type_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="请假时间" min-width="220">
        <template #default="{ row }">
          <div class="leave-time">
            <div>{{ formatDate(row.start_time) }} 至</div>
            <div>{{ formatDate(row.end_time) }}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="leave_duration_days" label="天数" width="80" align="center">
        <template #default="{ row }">
          <span class="duration-text">{{ row.leave_duration_days }} 天</span>
        </template>
      </el-table-column>
      <el-table-column prop="reason" label="请假原因" min-width="150" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="90" align="center">
        <template #default="{ row }">
          <el-tag :type="getStatusTagType(row.status)" size="small">
            {{ row.status_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="160" align="center" />
      <el-table-column label="操作" width="200" fixed="right" align="center">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleView(row)">
            查看
          </el-button>
          <el-button
            v-if="row.status === 'PENDING'"
            link
            type="success"
            size="small"
            @click="handleApprove(row)"
          >
            审批
          </el-button>
          <el-button
            v-if="row.status === 'PENDING'"
            link
            type="danger"
            size="small"
            @click="handleReject(row)"
          >
            驳回
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="请假申请详情"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-descriptions v-if="currentRecord" :column="2" border>
        <el-descriptions-item label="员工姓名">
          {{ currentRecord.employee_name }}
        </el-descriptions-item>
        <el-descriptions-item label="岗位">
          <el-tag :type="getPositionTagType(currentRecord.employee_position)" size="small">
            {{ currentRecord.employee_position_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="请假类型">
          <el-tag :type="getLeaveTypeTagType(currentRecord.leave_type)" size="small">
            {{ currentRecord.leave_type_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="请假天数">
          {{ currentRecord.leave_duration_days }} 天
        </el-descriptions-item>
        <el-descriptions-item label="开始时间" :span="2">
          {{ formatDateTime(currentRecord.start_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="结束时间" :span="2">
          {{ formatDateTime(currentRecord.end_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="申请状态">
          <el-tag :type="getStatusTagType(currentRecord.status)" size="small">
            {{ currentRecord.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">
          {{ formatDateTime(currentRecord.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="请假原因" :span="2">
          {{ currentRecord.reason }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.approver" label="审批人">
          {{ currentRecord.approver_name }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.approval_time" label="审批时间">
          {{ formatDateTime(currentRecord.approval_time) }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.approval_remark" label="审批意见" :span="2">
          {{ currentRecord.approval_remark }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button
          v-if="currentRecord?.status === 'PENDING'"
          type="success"
          @click="handleApprove(currentRecord)"
        >
          批准
        </el-button>
        <el-button
          v-if="currentRecord?.status === 'PENDING'"
          type="danger"
          @click="handleReject(currentRecord)"
        >
          驳回
        </el-button>
      </template>
    </el-dialog>

    <!-- 审批对话框 -->
    <el-dialog
      v-model="approveDialogVisible"
      :title="approveDialogTitle"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-alert
        v-if="approveType === 'approve'"
        title="批准操作"
        type="success"
        :closable="false"
        style="margin-bottom: 16px"
      >
        确认批准此请假申请吗？
      </el-alert>
      <el-alert
        v-else
        title="驳回操作"
        type="error"
        :closable="false"
        style="margin-bottom: 16px"
      >
        确认驳回此请假申请吗？驳回后员工需重新提交申请。
      </el-alert>

      <el-descriptions v-if="currentRecord" :column="1" border style="margin-bottom: 16px">
        <el-descriptions-item label="员工姓名">
          {{ currentRecord.employee_name }}
        </el-descriptions-item>
        <el-descriptions-item label="请假类型">
          <el-tag :type="getLeaveTypeTagType(currentRecord.leave_type)" size="small">
            {{ currentRecord.leave_type_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="请假时间">
          {{ formatDate(currentRecord.start_time) }} 至 {{ formatDate(currentRecord.end_time) }}
          （{{ currentRecord.leave_duration_days }} 天）
        </el-descriptions-item>
        <el-descriptions-item label="请假原因">
          {{ currentRecord.reason }}
        </el-descriptions-item>
      </el-descriptions>

      <el-form
        ref="approveFormRef"
        :model="approveForm"
        :rules="approveRules"
        label-width="100px"
      >
        <el-form-item label="审批意见" prop="approval_remark">
          <el-input
            v-model="approveForm.approval_remark"
            type="textarea"
            :rows="3"
            :placeholder="approveType === 'approve' ? '请输入批准意见（选填）' : '请输入驳回原因（必填）'"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="approveDialogVisible = false">取消</el-button>
        <el-button
          :type="approveType === 'approve' ? 'success' : 'danger'"
          :loading="approveLoading"
          @click="handleConfirmApprove"
        >
          {{ approveType === 'approve' ? '批准' : '驳回' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, DocumentChecked, List, Clock, Select, Close
} from '@element-plus/icons-vue'
import {
  getLeaveList,
  getPendingLeaves,
  approveLeave
} from '@/api/leave'

// 响应式数据
const loading = ref(false)
const leaveList = ref([])
const searchKeyword = ref('')
const activeTab = ref('all')
const tabCounts = reactive({
  all: 0,
  pending: 0
})

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框状态
const detailDialogVisible = ref(false)
const approveDialogVisible = ref(false)
const currentRecord = ref(null)
const approveType = ref('approve') // 'approve' 或 'reject'
const approveLoading = ref(false)

// 审批表单
const approveFormRef = ref()
const approveForm = reactive({
  approval_remark: ''
})

// 表单验证规则
const approveRules = computed(() => ({
  approval_remark: approveType.value === 'reject'
    ? [{ required: true, message: '请输入驳回原因', trigger: 'blur' }]
    : []
}))

// 审批对话框标题
const approveDialogTitle = computed(() => {
  return approveType.value === 'approve' ? '批准请假申请' : '驳回请假申请'
})

// 获取请假列表
const fetchLeaveList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }

    // 根据当前 Tab 添加筛选条件
    if (activeTab.value !== 'all') {
      params.status = activeTab.value
    }

    // 搜索关键词
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }

    const response = await getLeaveList(params)
    leaveList.value = response.data.results || []
    pagination.total = response.data.count || 0
    tabCounts.all = response.data.count || 0

    // 如果是待审批 Tab，更新待审批数量
    if (activeTab.value === 'all' || activeTab.value === 'PENDING') {
      fetchPendingCount()
    }
  } catch (error) {
    ElMessage.error('获取请假列表失败')
    console.error('Error fetching leave list:', error)
  } finally {
    loading.value = false
  }
}

// 获取待审批数量
const fetchPendingCount = async () => {
  try {
    const response = await getPendingLeaves()
    tabCounts.pending = response.data.count || 0
  } catch (error) {
    console.error('Error fetching pending count:', error)
  }
}

// 处理搜索
const handleSearch = () => {
  pagination.page = 1
  fetchLeaveList()
}

// 处理刷新
const handleRefresh = () => {
  searchKeyword.value = ''
  activeTab.value = 'all'
  pagination.page = 1
  fetchLeaveList()
}

// 处理 Tab 切换
const handleTabChange = () => {
  pagination.page = 1
  fetchLeaveList()
}

// 处理分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchLeaveList()
}

// 处理页码变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchLeaveList()
}

// 查看详情
const handleView = (row) => {
  currentRecord.value = row
  detailDialogVisible.value = true
}

// 批准请假
const handleApprove = (row) => {
  currentRecord.value = row
  approveType.value = 'approve'
  approveForm.approval_remark = ''
  approveDialogVisible.value = true
}

// 驳回请假
const handleReject = (row) => {
  currentRecord.value = row
  approveType.value = 'reject'
  approveForm.approval_remark = ''
  approveDialogVisible.value = true
}

// 确认审批
const handleConfirmApprove = async () => {
  // 验证表单
  try {
    await approveFormRef.value.validate()
  } catch (error) {
    return
  }

  approveLoading.value = true
  try {
    const data = {
      approve: approveType.value === 'approve',
      approval_remark: approveForm.approval_remark
    }

    await approveLeave(currentRecord.value.id, data)
    ElMessage.success(approveType.value === 'approve' ? '已批准请假申请' : '已驳回请假申请')
    approveDialogVisible.value = false
    detailDialogVisible.value = false
    fetchLeaveList()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error('Error approving leave:', error)
  } finally {
    approveLoading.value = false
  }
}

// 获取行样式类名
const getRowClassName = ({ row }) => {
  if (row.status === 'PENDING') {
    return 'pending-row'
  }
  return ''
}

// 获取岗位标签类型
const getPositionTagType = (position) => {
  const typeMap = {
    'CHEF': 'warning',
    'PASTRY': 'danger',
    'PREP': 'info',
    'CLEANER': 'success',
    'SERVER': '',
    'MANAGER': 'primary'
  }
  return typeMap[position] || ''
}

// 获取请假类型标签类型
const getLeaveTypeTagType = (leaveType) => {
  const typeMap = {
    'SICK': 'danger',
    'PERSONAL': 'warning',
    'COMPENSATORY': 'success'
  }
  return typeMap[leaveType] || ''
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    'PENDING': 'warning',
    'APPROVED': 'success',
    'REJECTED': 'danger'
  }
  return typeMap[status] || ''
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

// 格式化日期时间
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

// 组件挂载时获取数据
onMounted(() => {
  fetchLeaveList()
})
</script>

<style scoped>
.leave-approve-view {
  background-color: transparent;
}

/* 页面标题 */
.page-header {
  margin-bottom: 20px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #FF6B35;
}

.page-desc {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

/* 状态 Tab */
.status-tabs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
  flex-wrap: wrap;
}

.filter-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* 数据表格 */
.data-table {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

.status-tabs {
  margin-bottom: 20px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

.status-tabs :deep(.el-radio-group) {
  display: flex;
  gap: 12px;
}

.status-tabs :deep(.el-radio-button) {
  flex: 1;
}

.status-tabs :deep(.el-radio-button__inner) {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  height: 48px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s;
}

.status-tabs :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  border-color: #FF6B35;
  color: white;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.tab-badge {
  margin-left: 4px;
}

.tab-badge :deep(.el-badge__content) {
  background-color: #F7C52D;
  border-color: #F7C52D;
}

.leave-time {
  line-height: 1.6;
  font-size: 14px;
}

.duration-text {
  font-weight: 600;
  color: #FF6B35;
}

.text-muted {
  color: #999;
}

.text-success {
  color: #4CAF50;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

/* 待审批行高亮样式 */
:deep(.el-table .pending-row) {
  background-color: #fff7e6;
}

:deep(.el-table .pending-row:hover > td) {
  background-color: #ffeecf !important;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

:deep(.el-table th.el-table__cell) {
  background: linear-gradient(135deg, #FFF8F0, #FFE8D6);
  color: #333;
  font-weight: 600;
}

:deep(.el-table__row) {
  transition: background-color 0.2s;
}

:deep(.el-button--text) {
  transition: all 0.3s;
}

:deep(.el-button--text:hover) {
  transform: translateY(-2px);
}

/* 对话框样式 */
:deep(.el-dialog) {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(255, 107, 53, 0.2);
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  color: white;
  border-radius: 16px 16px 0 0;
  padding: 20px 24px;
}

:deep(.el-dialog__title) {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 20px;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #FFE8D6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .filter-actions {
    flex-wrap: wrap;
  }

  .status-tabs :deep(.el-radio-button__inner) {
    height: 40px;
    font-size: 14px;
  }
}
</style>
