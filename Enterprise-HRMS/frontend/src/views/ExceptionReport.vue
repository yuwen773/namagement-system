<template>
  <div class="exception-report-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <span class="page-title">异常上报</span>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="showReportDialog = true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;margin-right:4px;">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          上报异常
        </el-button>
      </div>
    </div>

    <!-- 异常列表 -->
    <div class="table-section" v-loading="loading">
      <el-table :data="exceptionList" stripe class="custom-table">
        <el-table-column prop="id" label="ID" width="80"/>
        <el-table-column label="员工" min-width="120">
          <template #default="{ row }">
            <div class="employee-cell">
              <div class="avatar-small">{{ row.employee_name?.charAt(0) }}</div>
              <span>{{ row.employee_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="month" label="薪资月份" width="100"/>
        <el-table-column label="异常类型" min-width="140">
          <template #default="{ row }">
            <el-tag :type="getExceptionTypeTag(row.exception_type)" size="small">
              {{ row.exception_type_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="处理状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)" size="small">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="adjustment_amount" label="调整金额" width="120" align="right">
          <template #default="{ row }">
            <span :class="row.adjustment_amount > 0 ? 'amount-positive' : row.adjustment_amount < 0 ? 'amount-negative' : ''">
              {{ row.adjustment_amount ? (row.adjustment_amount > 0 ? '+' : '') + row.adjustment_amount.toLocaleString() : '-' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="上报时间" width="170">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)" class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              查看
            </el-button>
            <el-button
              v-if="isHR && row.status !== 'resolved' && row.status !== 'closed'"
              type="success"
              link
              size="small"
              @click="openResolveDialog(row)"
              class="action-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchExceptions"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <el-empty v-if="!loading && exceptionList.length === 0" description="暂无异常记录"/>

    <!-- 异常详情抽屉 -->
    <el-drawer v-model="detailDrawerVisible" title="异常详情" size="480px">
      <div v-if="currentException" class="drawer-content">
        <div class="detail-header">
          <div class="header-info">
            <h3>{{ currentException.exception_type_display }}</h3>
            <p>{{ currentException.employee_name }} - {{ currentException.month }} 月薪资</p>
          </div>
          <el-tag :type="getStatusTag(currentException.status)" class="status-badge">
            {{ currentException.status_display }}
          </el-tag>
        </div>

        <el-descriptions :column="1" border class="info-descriptions">
          <el-descriptions-item label="异常类型">
            <el-tag :type="getExceptionTypeTag(currentException.exception_type)" size="small">
              {{ currentException.exception_type_display }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="上报人">{{ currentException.reported_by_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="处理人">{{ currentException.assigned_to_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="上报时间">{{ formatDate(currentException.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="解决时间">{{ currentException.resolved_at ? formatDate(currentException.resolved_at) : '-' }}</el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>异常描述</h4>
          <p class="description-text">{{ currentException.description }}</p>
        </div>

        <div class="detail-section" v-if="currentException.resolution">
          <h4>处理方案</h4>
          <p class="description-text">{{ currentException.resolution }}</p>
        </div>

        <div class="adjustment-amount" v-if="currentException.adjustment_amount != 0">
          <span>调整金额</span>
          <span :class="currentException.adjustment_amount > 0 ? 'amount-positive' : 'amount-negative'">
            {{ currentException.adjustment_amount > 0 ? '+' : '' }}{{ currentException.adjustment_amount.toLocaleString() }} 元
          </span>
        </div>
      </div>
    </el-drawer>

    <!-- 上报异常对话框 -->
    <el-dialog v-model="showReportDialog" title="上报薪资异常" width="500px">
      <el-form ref="reportFormRef" :model="reportForm" :rules="reportRules" label-width="100px" class="custom-form">
        <el-form-item label="薪资记录" prop="salary_record">
          <el-select v-model="reportForm.salary_record" placeholder="选择薪资记录" filterable class="form-input">
            <el-option
              v-for="record in salaryRecords"
              :key="record.id"
              :label="`${record.real_name} - ${record.month} (¥${record.final_salary?.toLocaleString()})`"
              :value="record.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="异常类型" prop="exception_type">
          <el-select v-model="reportForm.exception_type" placeholder="选择异常类型" class="form-input">
            <el-option label="薪资计算错误" value="salary_error"/>
            <el-option label="考勤数据错误" value="attendance_error"/>
            <el-option label="加班记录缺失" value="overtime_missing"/>
            <el-option label="扣款异常" value="deduction_error"/>
            <el-option label="员工申诉" value="employee_appeal"/>
            <el-option label="其他" value="other"/>
          </el-select>
        </el-form-item>
        <el-form-item label="异常描述" prop="description">
          <el-input
            v-model="reportForm.description"
            type="textarea"
            :rows="4"
            placeholder="请详细描述异常情况..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showReportDialog = false">取消</el-button>
        <el-button type="primary" :loading="reporting" @click="handleReport">
          提交
        </el-button>
      </template>
    </el-dialog>

    <!-- 处理异常对话框 -->
    <el-dialog v-model="showResolveDialog" title="处理薪资异常" width="500px">
      <el-form ref="resolveFormRef" :model="resolveForm" :rules="resolveRules" label-width="100px" class="custom-form">
        <el-form-item label="处理状态" prop="status">
          <el-select v-model="resolveForm.status" placeholder="选择处理状态" class="form-input">
            <el-option label="处理中" value="processing"/>
            <el-option label="已解决" value="resolved"/>
            <el-option label="已关闭" value="closed"/>
          </el-select>
        </el-form-item>
        <el-form-item label="调整金额" prop="adjustment_amount">
          <el-input-number
            v-model="resolveForm.adjustment_amount"
            :precision="2"
            :step="100"
            :min="-100000"
            :max="100000"
            class="form-input"
          />
          <span class="form-tip">（正数为补发，负数为扣回）</span>
        </el-form-item>
        <el-form-item label="处理方案" prop="resolution">
          <el-input
            v-model="resolveForm.resolution"
            type="textarea"
            :rows="4"
            placeholder="请填写处理方案..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showResolveDialog = false">取消</el-button>
        <el-button type="primary" :loading="resolving" @click="handleResolve">
          确认处理
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import {
  getExceptionList,
  getExceptionDetail,
  reportException,
  resolveException,
  getExceptionStatistics,
  getSalaryRecordsForException
} from '@/api/salary'
import { getEmployeeOptions } from '@/api/employee'

// 状态
const loading = ref(false)
const reporting = ref(false)
const resolving = ref(false)
const exceptionList = ref([])
const currentException = ref(null)
const detailDrawerVisible = ref(false)
const showReportDialog = ref(false)
const showResolveDialog = ref(false)
const reportFormRef = ref(null)
const resolveFormRef = ref(null)
const salaryRecords = ref([])
const employeeOptions = ref([])
const statistics = reactive({
  pending: 0,
  resolved: 0,
  total: 0
})

// 筛选表单
const filterForm = reactive({
  status: '',
  exception_type: '',
  user_id: '',
  dateRange: [],
  month: ''
})

// 分页状态
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 上报表单
const reportForm = ref({
  salary_record: null,
  exception_type: '',
  description: ''
})

const reportRules = {
  salary_record: [{ required: true, message: '请选择薪资记录', trigger: 'change' }],
  exception_type: [{ required: true, message: '请选择异常类型', trigger: 'change' }],
  description: [{ required: true, message: '请填写异常描述', trigger: 'blur' }]
}

// 处理表单
const resolveForm = ref({
  status: 'resolved',
  adjustment_amount: 0,
  resolution: ''
})

const resolveRules = {
  status: [{ required: true, message: '请选择处理状态', trigger: 'change' }],
  resolution: [{ required: true, message: '请填写处理方案', trigger: 'blur' }]
}

// 权限判断
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const isHR = computed(() => ['hr', 'admin'].includes(user.value?.role))

// 获取异常列表
const fetchExceptions = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }

    // 员工只能查看自己的异常记录
    if (user.value?.role === 'employee') {
      params.user_id = user.value.user_id
    } else if (filterForm.user_id) {
      params.user_id = filterForm.user_id
    }

    if (filterForm.status) {
      params.status = filterForm.status
    }
    if (filterForm.exception_type) {
      params.exception_type = filterForm.exception_type
    }
    if (filterForm.dateRange && filterForm.dateRange.length === 2) {
      params.date_start = filterForm.dateRange[0]
      params.date_end = filterForm.dateRange[1]
    }
    if (filterForm.month) {
      params.month = filterForm.month
    }

    const res = await getExceptionList(params)
    if (res.data?.code === 0) {
      exceptionList.value = res.data.data || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取异常列表失败:', error)
    ElMessage.error('获取异常列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计数据
const fetchStatistics = async () => {
  if (!isHR.value) return

  try {
    const res = await getExceptionStatistics()
    if (res.data?.code === 0) {
      Object.assign(statistics, res.data.data)
    }
  } catch (error) {
    console.error('获取统计信息失败:', error)
  }
}

// 获取薪资记录列表
const fetchSalaryRecords = async () => {
  try {
    // 只获取已发布的薪资记录
    const params = { page_size: 100 }
    if (user.value?.role === 'employee') {
      params.month = new Date().toISOString().slice(0, 7)
    }
    const res = await getSalaryRecordsForException(params)
    if (res.data?.code === 0) {
      salaryRecords.value = res.data.data || []
    }
  } catch (error) {
    console.error('获取薪资记录失败:', error)
  }
}

// 获取员工选项
const fetchEmployeeOptions = async () => {
  try {
    const res = await getEmployeeOptions({})
    if (res.data?.code === 0) {
      employeeOptions.value = res.data.data || []
    }
  } catch (error) {
    console.error('获取员工列表失败:', error)
  }
}

// 筛选变化
const handleFilterChange = () => {
  pagination.page = 1
  fetchExceptions()
}

// 页码变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchExceptions()
}

// 查看详情
const viewDetail = async (row) => {
  try {
    const res = await getExceptionDetail(row.id)
    if (res.data?.code === 0) {
      currentException.value = res.data.data
      detailDrawerVisible.value = true
    }
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败')
  }
}

// 打开处理对话框
const openResolveDialog = (row) => {
  currentException.value = row
  resolveForm.value = {
    status: 'resolved',
    adjustment_amount: 0,
    resolution: ''
  }
  showResolveDialog.value = true
}

// 上报异常
const handleReport = async () => {
  if (!reportFormRef.value) return

  try {
    await reportFormRef.value.validate()
    reporting.value = true

    const res = await reportException(reportForm.value)
    if (res.data?.code === 0) {
      ElMessage.success('异常已上报')
      showReportDialog.value = false
      reportForm.value = { salary_record: null, exception_type: '', description: '' }
      fetchExceptions()
      fetchStatistics()
    } else {
      ElMessage.error(res.data?.message || '上报失败')
    }
  } catch (error) {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error('上报失败')
    }
  } finally {
    reporting.value = false
  }
}

// 处理异常
const handleResolve = async () => {
  if (!resolveFormRef.value || !currentException.value) return

  try {
    await resolveFormRef.value.validate()
    resolving.value = true

    const res = await resolveException(currentException.value.id, resolveForm.value)
    if (res.data?.code === 0) {
      ElMessage.success('异常已处理')
      showResolveDialog.value = false
      fetchExceptions()
      fetchStatistics()
    } else {
      ElMessage.error(res.data?.message || '处理失败')
    }
  } catch (error) {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error('处理失败')
    }
  } finally {
    resolving.value = false
  }
}

// 获取状态标签类型
const getStatusTag = (status) => {
  const map = {
    pending: 'warning',
    processing: 'info',
    resolved: 'success',
    closed: 'info'
  }
  return map[status] || 'info'
}

// 获取异常类型标签类型
const getExceptionTypeTag = (type) => {
  const map = {
    salary_error: 'danger',
    attendance_error: 'warning',
    overtime_missing: 'info',
    deduction_error: 'danger',
    employee_appeal: 'primary',
    other: 'info'
  }
  return map[type] || 'info'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return dateStr.replace('T', ' ').substring(0, 19)
}

// 初始化
onMounted(() => {
  fetchExceptions()
  if (isHR.value) {
    fetchStatistics()
    fetchSalaryRecords()
    fetchEmployeeOptions()
  }
})
</script>

<style scoped>
/* ========================================
   Salary Exception - Modern Corporate Design
   ======================================== */

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-warning) 0%, var(--color-warning-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow-warning);
}

.header-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-icon.pending {
  background: rgba(230, 162, 60, 0.1);
  color: var(--color-warning);
}

.stat-icon.resolved {
  background: rgba(103, 194, 58, 0.1);
  color: var(--color-success);
}

.stat-icon.total {
  background: rgba(64, 158, 255, 0.1);
  color: var(--color-primary);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

/* 筛选区域 */
.filter-section {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.filter-select {
  width: 160px;
}

/* 表格区域 */
.table-section {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.custom-table {
  border-radius: 0;
}

/* 员工单元格 */
.employee-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-small {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

/* 金额样式 */
.amount-positive {
  color: var(--color-success);
  font-weight: 600;
}

.amount-negative {
  color: var(--color-danger);
  font-weight: 600;
}

/* 操作按钮 */
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 20px;
  background: var(--color-gray-50);
  border-top: 1px solid var(--color-border-light);
}

/* 抽屉样式 */
.drawer-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border-light);
}

.header-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
}

.header-info p {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin: 0;
}

.status-badge {
  font-weight: 500;
}

.info-descriptions {
  border-radius: var(--radius-md);
  overflow: hidden;
}

.detail-section {
  margin-top: 8px;
}

.detail-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.description-text {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
  padding: 12px;
  background: var(--color-gray-50);
  border-radius: var(--radius-md);
}

.adjustment-amount {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--color-success-subtle) 0%, var(--color-bg-secondary) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-success-subtle);
  font-size: 14px;
  color: var(--color-text-secondary);
}

.adjustment-amount .amount-positive,
.adjustment-amount .amount-negative {
  font-size: 20px;
  font-weight: 700;
}

/* 表单样式 */
.custom-form .form-input {
  width: 100%;
}

.form-tip {
  margin-left: 8px;
  font-size: 12px;
  color: var(--color-text-tertiary);
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .stats-cards {
    grid-template-columns: 1fr;
  }

  .filter-section {
    flex-wrap: wrap;
  }
}
</style>
