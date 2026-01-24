<template>
  <div class="salary-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="4" width="20" height="16" rx="2"/>
            <path d="M12 12h.01"/>
            <path d="M6 12h.01"/>
            <path d="M18 12h.01"/>
          </svg>
        </div>
        <span class="page-title">薪资管理</span>
      </div>
      <div class="header-right">
        <el-date-picker
          v-model="filterForm.monthRange"
          type="monthrange"
          range-separator="至"
          start-placeholder="开始月份"
          end-placeholder="结束月份"
          format="YYYY-MM"
          value-format="YYYY-MM"
          :disabled-date="disabledDate"
          @change="handleFilterChange"
          class="month-range-picker"
        />
      </div>
    </div>

    <!-- 薪资记录列表 -->
    <div class="table-section" v-loading="loading">
      <el-table :data="salaryRecords" stripe class="custom-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="员工" min-width="140">
          <template #default="{ row }">
            <div class="employee-cell">
              <div class="avatar-small">{{ row.real_name?.charAt(0) }}</div>
              <div class="info">
                <span class="name">{{ row.real_name }}</span>
                <span class="dept">{{ row.department_name }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="month" label="月份" width="100" />
        <el-table-column prop="base_salary" label="基本工资" width="120" align="right">
          <template #default="{ row }">
            <span class="salary-amount">¥{{ row.base_salary?.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="final_salary" label="实发工资" width="140" align="right">
          <template #default="{ row }">
            <span class="salary-amount final">¥{{ row.final_salary?.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'info'" size="small" class="status-tag">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            {{ row.create_time?.replace('T', ' ').substring(0, 19) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)" class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              查看详情
            </el-button>
            <el-button
              v-if="isHR && row.status === 'draft'"
              type="success"
              link
              size="small"
              @click="publishSalary(row)"
              class="action-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              发布
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchSalaryRecords"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <el-empty v-if="!loading && salaryRecords.length === 0" description="暂无薪资记录" />

    <!-- 薪资详情抽屉 -->
    <el-drawer v-model="detailDrawerVisible" title="薪资详情" size="420px">
      <div v-if="currentRecord" class="drawer-content">
        <div class="detail-header">
          <div class="header-info">
            <h3>{{ currentRecord.real_name }}</h3>
            <p>{{ currentRecord.month }} 月薪资单</p>
          </div>
          <el-tag :type="currentRecord.status === 'published' ? 'success' : 'info'" class="status-badge">
            {{ currentRecord.status === 'published' ? '已发布' : '草稿' }}
          </el-tag>
        </div>

        <el-descriptions :column="1" border class="info-descriptions">
          <el-descriptions-item label="部门">{{ currentRecord.department_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="基本工资">
            <span class="amount">¥{{ currentRecord.base_salary?.toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="加班费">
            <span class="amount add">+¥{{ currentRecord.overtime_pay?.toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="考勤扣款">
            <span class="amount minus">-¥{{ currentRecord.attendance_deduction?.toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="迟到次数">{{ currentRecord.late_count || 0 }} 次</el-descriptions-item>
          <el-descriptions-item label="早退次数">{{ currentRecord.early_count || 0 }} 次</el-descriptions-item>
        </el-descriptions>

        <div class="final-salary">
          <span>实发工资</span>
          <span class="amount-total">¥{{ currentRecord.final_salary?.toLocaleString() }}</span>
        </div>
      </div>
    </el-drawer>

    <!-- HR/管理员：薪资计算对话框 -->
    <el-dialog v-model="calculateDialogVisible" title="薪资计算" width="500px">
      <el-form ref="calculateFormRef" :model="calculateForm" :rules="calculateRules" label-width="100px" class="custom-form">
        <el-form-item label="员工" prop="user_id">
          <el-select v-model="calculateForm.user_id" placeholder="选择员工" filterable class="form-input">
            <el-option
              v-for="emp in employeeList"
              :key="emp.id"
              :label="`${emp.real_name} (${emp.employee_no})`"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="月份" prop="month">
          <el-date-picker
            v-model="calculateForm.month"
            type="month"
            placeholder="选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM"
            class="form-input"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="calculateDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="calculating" @click="handleCalculate">
          计算并保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { getSalaryRecords, getSalaryRecordDetail, saveSalaryRecord, publishSalaryRecords } from '@/api/salary'
import { getEmployeeList } from '@/api/employee'

// 状态
const loading = ref(false)
const calculating = ref(false)
const salaryRecords = ref([])
const detailDrawerVisible = ref(false)
const currentRecord = ref(null)
const calculateDialogVisible = ref(false)
const calculateFormRef = ref(null)
const employeeList = ref([])

// 筛选表单
const filterForm = reactive({
  monthRange: null
})

// 分页状态
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 计算表单
const calculateForm = ref({
  user_id: null,
  month: ''
})

const calculateRules = {
  user_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  month: [{ required: true, message: '请选择月份', trigger: 'change' }]
}

// 权限判断
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const isHR = computed(() => ['hr', 'admin'].includes(user.value?.role))

// 禁用未来月份
const disabledDate = (time) => {
  return time.getTime() > Date.now()
}

// 获取薪资记录列表
const fetchSalaryRecords = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }

    if (filterForm.monthRange && filterForm.monthRange.length === 2) {
      params.month_start = filterForm.monthRange[0]
      params.month_end = filterForm.monthRange[1]
    } else if (selectedMonth.value) {
      params.month = selectedMonth.value
    }

    const res = await getSalaryRecords(params)
    if (res.data?.code === 0) {
      salaryRecords.value = res.data.data || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取薪资记录失败:', error)
    ElMessage.error('获取薪资记录失败')
  } finally {
    loading.value = false
  }
}

// 筛选条件变化
const handleFilterChange = () => {
  pagination.page = 1
  fetchSalaryRecords()
}

// 页码变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchSalaryRecords()
}

// 单月选择（兼容旧版本）
const selectedMonth = ref(null)
const handleMonthChange = () => {
  if (selectedMonth.value) {
    filterForm.monthRange = null
  }
  handleFilterChange()
}

// 查看详情
const viewDetail = async (row) => {
  try {
    const res = await getSalaryRecordDetail(row.id)
    if (res.data?.code === 0) {
      currentRecord.value = res.data.data
      detailDrawerVisible.value = true
    }
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败')
  }
}

// 发布薪资
const publishSalary = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认发布 ${row.real_name} 的 ${row.month} 月薪资？`,
      '发布确认',
      { type: 'warning' }
    )

    const res = await publishSalaryRecords([row.id])
    if (res.data?.code === 0) {
      ElMessage.success('薪资已发布')
      fetchSalaryRecords()
    } else {
      ElMessage.error(res.data?.message || '发布失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发布失败:', error)
      ElMessage.error(error.response?.data?.message || '发布失败')
    }
  }
}

// 获取员工列表（用于计算薪资）
const fetchEmployeeList = async () => {
  try {
    const res = await getEmployeeList({ status: 'active' })
    if (res.data?.code === 0) {
      employeeList.value = res.data.data || []
    }
  } catch (error) {
    console.error('获取员工列表失败:', error)
  }
}

// 打开计算对话框
const openCalculateDialog = () => {
  calculateForm.value = {
    user_id: null,
    month: selectedMonth.value || new Date().toISOString().slice(0, 7)
  }
  calculateDialogVisible.value = true
}

// 计算并保存薪资
const handleCalculate = async () => {
  if (!calculateFormRef.value) return

  try {
    await calculateFormRef.value.validate()
    calculating.value = true

    const res = await saveSalaryRecord(calculateForm.value)
    if (res.data?.code === 0) {
      ElMessage.success('薪资计算并保存成功')
      calculateDialogVisible.value = false
      fetchSalaryRecords()
    } else {
      ElMessage.error(res.data?.message || '保存失败')
    }
  } catch (error) {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error !== 'cancel') {
      ElMessage.error('保存失败')
    }
  } finally {
    calculating.value = false
  }
}

// 初始化
onMounted(() => {
  fetchSalaryRecords()
  if (isHR.value) {
    fetchEmployeeList()
  }
})
</script>

<style scoped>
/* ========================================
   Salary - Modern Corporate Design
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
  background: linear-gradient(135deg, var(--color-success) 0%, var(--color-success-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow-success);
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

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.month-range-picker {
  width: 280px;
}

/* 表格区域 */
.table-section {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--color-shadow-sm);
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
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.employee-cell .info {
  display: flex;
  flex-direction: column;
}

.employee-cell .name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.employee-cell .dept {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.salary-amount {
  font-weight: 500;
  color: var(--color-text-primary);
}

.salary-amount.final {
  font-weight: 600;
  color: var(--color-success);
}

.status-tag {
  font-weight: 500;
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
  gap: 24px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border-light);
}

.header-info h3 {
  font-size: 20px;
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

.amount {
  font-weight: 500;
  color: var(--color-text-primary);
}

.amount.add {
  color: var(--color-success);
  font-weight: 600;
}

.amount.minus {
  color: var(--color-danger);
  font-weight: 600;
}

.final-salary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, var(--color-success-subtle) 0%, var(--color-bg-secondary) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-success-subtle);
}

.final-salary span:first-child {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.amount-total {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-success);
}

/* 表单样式 */
.custom-form .form-input {
  width: 100%;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-right {
    width: 100%;
  }

  .month-range-picker {
    width: 100%;
  }
}
</style>
