<template>
  <div class="salary-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon :size="28" class="title-icon"><Wallet /></el-icon>
        薪资查询
      </h1>
      <p class="page-subtitle">查看您的工资条和薪资明细</p>
    </div>

    <!-- 月份选择器 -->
    <el-card class="month-selector-card" shadow="hover">
      <div class="month-selector">
        <el-icon class="selector-icon"><Calendar /></el-icon>
        <span class="selector-label">选择月份：</span>
        <el-date-picker
          v-model="selectedMonth"
          type="month"
          placeholder="选择月份"
          format="YYYY年MM月"
          value-format="YYYY-MM"
          :clearable="false"
          @change="handleMonthChange"
          class="month-picker"
        />
        <el-button
          type="primary"
          :icon="Tickets"
          @click="showAppealDialog"
          class="appeal-btn"
        >
          薪资申诉
        </el-button>
      </div>
    </el-card>

    <!-- 薪资详情卡片 -->
    <div v-if="currentSalary" v-loading="loading" class="salary-content">
      <!-- 当月工资总览 -->
      <el-card class="salary-overview-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-title">{{ formatMonth(selectedMonth) }} 工资条</span>
            <el-button
              :icon="isShowDetail ? Hide : View"
              @click="toggleDetail"
              type="primary"
              plain
              size="small"
            >
              {{ isShowDetail ? '隐藏详情' : '查看详情' }}
            </el-button>
          </div>
        </template>

        <!-- 实发工资大字显示 -->
        <div class="total-salary-section">
          <div class="total-salary-label">实发工资</div>
          <div class="total-salary-value">
            <span v-if="!isShowDetail" class="masked">****</span>
            <span v-else class="amount">¥{{ formatMoney(currentSalary.total_salary) }}</span>
          </div>
          <el-tag :type="getStatusTagType(currentSalary.status)" effect="dark" size="large">
            {{ getStatusText(currentSalary.status) }}
          </el-tag>
        </div>
      </el-card>

      <!-- 工资明细 -->
      <el-row :gutter="16" class="salary-details-row">
        <!-- 基本工资 -->
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="salary-detail-card" shadow="hover">
            <div class="detail-content">
              <div class="detail-icon base-icon">
                <el-icon :size="24"><Money /></el-icon>
              </div>
              <div class="detail-info">
                <div class="detail-label">基本工资</div>
                <div class="detail-value">
                  <span v-if="!isShowDetail" class="masked">****</span>
                  <span v-else>¥{{ formatMoney(currentSalary.base_salary) }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 岗位津贴 -->
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="salary-detail-card" shadow="hover">
            <div class="detail-content">
              <div class="detail-icon allowance-icon">
                <el-icon :size="24"><Medal /></el-icon>
              </div>
              <div class="detail-info">
                <div class="detail-label">岗位津贴</div>
                <div class="detail-value">
                  <span v-if="!isShowDetail" class="masked">****</span>
                  <span v-else>¥{{ formatMoney(currentSalary.position_allowance) }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 加班费 -->
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="salary-detail-card" shadow="hover">
            <div class="detail-content">
              <div class="detail-icon overtime-icon">
                <el-icon :size="24"><Clock /></el-icon>
              </div>
              <div class="detail-info">
                <div class="detail-label">加班费</div>
                <div class="detail-value">
                  <span v-if="!isShowDetail" class="masked">****</span>
                  <span v-else class="overtime-value">¥{{ formatMoney(currentSalary.overtime_pay) }}</span>
                </div>
                <div class="detail-hint">{{ currentSalary.overtime_hours || 0 }} 小时</div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 扣款 -->
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="salary-detail-card deduction-card" shadow="hover">
            <div class="detail-content">
              <div class="detail-icon deduction-icon">
                <el-icon :size="24"><Minus /></el-icon>
              </div>
              <div class="detail-info">
                <div class="detail-label">扣款</div>
                <div class="detail-value deduction-value">
                  <span v-if="!isShowDetail" class="masked">****</span>
                  <span v-else>- ¥{{ formatMoney(currentSalary.deductions) }}</span>
                </div>
                <div class="detail-hint" v-if="currentSalary.late_count > 0 || currentSalary.missing_count > 0">
                  迟到{{ currentSalary.late_count }}次 缺卡{{ currentSalary.missing_count }}次
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 详细说明 -->
      <el-card v-if="isShowDetail" class="salary-breakdown-card" shadow="hover">
        <template #header>
          <span class="card-title">工资明细说明</span>
        </template>

        <el-descriptions :column="1" border>
          <el-descriptions-item label="工资月份">
            {{ formatMonth(selectedMonth) }}
          </el-descriptions-item>
          <el-descriptions-item label="出勤天数">
            {{ currentSalary.work_days || 0 }} 天
          </el-descriptions-item>
          <el-descriptions-item label="迟到次数">
            {{ currentSalary.late_count || 0 }} 次
          </el-descriptions-item>
          <el-descriptions-item label="缺卡次数">
            {{ currentSalary.missing_count || 0 }} 次
          </el-descriptions-item>
          <el-descriptions-item label="加班时长">
            {{ currentSalary.overtime_hours?.toFixed(1) || '0.0' }} 小时
          </el-descriptions-item>
          <el-descriptions-item label="基本工资">
            ¥{{ formatMoney(currentSalary.base_salary) }}
          </el-descriptions-item>
          <el-descriptions-item label="岗位津贴">
            ¥{{ formatMoney(currentSalary.position_allowance) }}
          </el-descriptions-item>
          <el-descriptions-item label="加班费">
            ¥{{ formatMoney(currentSalary.overtime_pay) }}
            <span class="formula-hint">（时薪 × 1.5 × 加班小时数）</span>
          </el-descriptions-item>
          <el-descriptions-item label="扣款">
            ¥{{ formatMoney(currentSalary.deductions) }}
            <span class="formula-hint">（迟到×20 + 缺卡×50）</span>
          </el-descriptions-item>
          <el-descriptions-item label="实发工资" label-class-name="breakdown-total-label">
            <span class="breakdown-total">¥{{ formatMoney(currentSalary.total_salary) }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 历史薪资记录 -->
      <el-card class="salary-history-card" shadow="hover">
        <template #header>
          <span class="card-title">历史薪资记录</span>
        </template>

        <div class="history-list">
          <div
            v-for="record in salaryHistory"
            :key="record.id"
            class="history-item"
            :class="{ active: record.id === currentSalary?.id }"
            @click="selectSalary(record)"
          >
            <div class="history-month">
              <el-icon><Calendar /></el-icon>
              {{ formatMonth(record.year_month) }}
            </div>
            <div class="history-amount">
              ¥{{ formatMoney(record.total_salary) }}
            </div>
            <el-tag :type="getStatusTagType(record.status)" size="small">
              {{ getStatusText(record.status) }}
            </el-tag>
          </div>
        </div>

        <el-empty v-if="salaryHistory.length === 0" description="暂无历史记录" />
      </el-card>
    </div>

    <!-- 无数据提示 -->
    <el-card v-else-if="!loading" class="no-data-card" shadow="hover">
      <el-empty description="该月份暂无薪资数据">
        <el-icon :size="64" color="#FF6B35"><Wallet /></el-icon>
      </el-empty>
    </el-card>

    <!-- 薪资申诉对话框 -->
    <el-dialog
      v-model="appealDialogVisible"
      title="薪资申诉"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="appealForm" :rules="appealRules" ref="appealFormRef" label-width="100px">
        <el-form-item label="申诉月份">
          <el-input :value="formatMonth(selectedMonth)" disabled />
        </el-form-item>

        <el-form-item label="当前金额" v-if="currentSalary">
          <el-input :value="`¥${formatMoney(currentSalary.total_salary)}`" disabled />
        </el-form-item>

        <el-form-item label="申诉原因" prop="reason">
          <el-input
            v-model="appealForm.reason"
            type="textarea"
            :rows="5"
            placeholder="请详细说明申诉原因，如：加班时数统计有误、考勤记录需要更正等"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-alert
          title="提示"
          type="info"
          :closable="false"
          show-icon
        >
          提交后管理员将审核您的申诉，请耐心等待处理结果
        </el-alert>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="appealDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAppeal" :loading="submitting">
            提交申诉
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Wallet,
  Calendar,
  Tickets,
  View,
  Hide,
  Money,
  Medal,
  Clock,
  Minus
} from '@element-plus/icons-vue'
import { getMySalaries, createAppeal } from '../../api/salary'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()

// 数据状态
const loading = ref(false)
const submitting = ref(false)
const selectedMonth = ref('')
const salaryHistory = ref([])
const currentSalary = ref(null)
const isShowDetail = ref(false)

// 申诉对话框
const appealDialogVisible = ref(false)
const appealFormRef = ref(null)
const appealForm = reactive({
  reason: ''
})

const appealRules = {
  reason: [
    { required: true, message: '请填写申诉原因', trigger: 'blur' },
    { min: 5, message: '申诉原因至少5个字符', trigger: 'blur' },
    { max: 200, message: '申诉原因不能超过200个字符', trigger: 'blur' }
  ]
}

// 获取当前月份
const getCurrentMonth = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  return `${year}-${month}`
}

// 月份改变
const handleMonthChange = (value) => {
  isShowDetail.value = false
  loadSalaryData()
}

// 加载薪资数据
const loadSalaryData = async () => {
  loading.value = true
  try {
    const employeeId = userStore.userInfo?.employee

    if (!employeeId) {
      ElMessage.error('未关联员工档案，无法查询薪资')
      return
    }

    // 获取薪资列表
    const res = await getMySalaries({
      employee_id: employeeId,
      year_month: selectedMonth.value
    })

    if (res.code === 200) {
      const salaries = res.data?.results || res.data || []

      // 找到当前月份的薪资
      const current = salaries.find(s => s.year_month === selectedMonth.value)

      if (current) {
        currentSalary.value = current
      } else {
        currentSalary.value = null
      }

      // 历史记录（排除当前选中的月份）
      salaryHistory.value = salaries.filter(s => s.year_month !== selectedMonth.value)
    } else {
      ElMessage.error(res.message || '加载薪资数据失败')
      currentSalary.value = null
      salaryHistory.value = []
    }
  } catch (error) {
    console.error('加载薪资数据失败:', error)
    ElMessage.error('加载薪资数据失败')
    currentSalary.value = null
    salaryHistory.value = []
  } finally {
    loading.value = false
  }
}

// 切换详情显示
const toggleDetail = () => {
  isShowDetail.value = !isShowDetail.value
}

// 选择历史薪资记录
const selectSalary = (record) => {
  selectedMonth.value = record.year_month
  isShowDetail.value = false
  loadSalaryData()
}

// 显示申诉对话框
const showAppealDialog = () => {
  if (!currentSalary.value) {
    ElMessage.warning('请先选择有薪资数据的月份')
    return
  }
  appealForm.reason = ''
  appealDialogVisible.value = true
}

// 提交申诉
const submitAppeal = async () => {
  try {
    await appealFormRef.value.validate()

    if (!currentSalary.value) {
      ElMessage.error('无法提交申诉：未找到薪资记录')
      return
    }

    submitting.value = true

    const res = await createAppeal({
      appeal_type: 'SALARY',
      employee: userStore.userInfo?.employee,
      target_id: currentSalary.value.id,
      reason: appealForm.reason
    })

    if (res.code === 200) {
      ElMessage.success('申诉已提交，请等待管理员审核')
      appealDialogVisible.value = false
    } else {
      ElMessage.error(res.message || '提交申诉失败')
    }
  } catch (error) {
    if (error !== false) {
      console.error('提交申诉失败:', error)
      ElMessage.error('提交申诉失败，请重试')
    }
  } finally {
    submitting.value = false
  }
}

// 格式化金额
const formatMoney = (value) => {
  if (value === null || value === undefined) return '0.00'
  return Number(value).toFixed(2)
}

// 格式化月份
const formatMonth = (monthStr) => {
  if (!monthStr) return '-'
  const [year, month] = monthStr.split('-')
  return `${year}年${month}月`
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    DRAFT: 'info',
    PUBLISHED: 'success',
    ADJUSTED: 'warning',
    APPEALED: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ADJUSTED: '已调整',
    APPEALED: '申诉中'
  }
  return textMap[status] || '未知'
}

onMounted(() => {
  selectedMonth.value = getCurrentMonth()
  loadSalaryData()
})
</script>

<style scoped>
.salary-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 页面标题 */
.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
}

.title-icon {
  color: #FF6B35;
}

.page-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* 月份选择器 */
.month-selector-card {
  margin-bottom: 20px;
}

.month-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.selector-icon {
  font-size: 20px;
  color: #FF6B35;
}

.selector-label {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.month-picker {
  width: 200px;
}

.appeal-btn {
  margin-left: auto;
}

/* 薪资内容区 */
.salary-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 当月工资总览 */
.salary-overview-card {
  border-radius: 12px;
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
}

.salary-overview-card :deep(.el-card__header) {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.salary-overview-card .card-title {
  color: white;
}

.total-salary-section {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 20px 0;
}

.total-salary-label {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
}

.total-salary-value {
  flex: 1;
  text-align: center;
}

.total-salary-value .masked {
  font-size: 48px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 8px;
}

.total-salary-value .amount {
  font-size: 48px;
  font-weight: 700;
  color: white;
}

/* 工资明细卡片 */
.salary-details-row {
  margin-bottom: 0;
}

.salary-detail-card {
  border-radius: 12px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.salary-detail-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.15);
}

.detail-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.base-icon {
  background: linear-gradient(135deg, #42A5F5, #64B5F6);
  color: white;
}

.allowance-icon {
  background: linear-gradient(135deg, #66BB6A, #81C784);
  color: white;
}

.overtime-icon {
  background: linear-gradient(135deg, #FFA726, #FFB74D);
  color: white;
}

.deduction-icon {
  background: linear-gradient(135deg, #EF5350, #E57373);
  color: white;
}

.detail-info {
  flex: 1;
}

.detail-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.detail-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.detail-value .masked {
  letter-spacing: 4px;
  color: #c0c4cc;
}

.overtime-value {
  color: #FF6B35;
}

.deduction-value {
  color: #EF5350;
}

.detail-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

/* 工资明细说明 */
.salary-breakdown-card {
  border-radius: 12px;
}

.formula-hint {
  margin-left: 8px;
  font-size: 12px;
  color: #909399;
}

:deep(.breakdown-total-label) {
  font-weight: 600;
}

.breakdown-total {
  font-size: 20px;
  font-weight: 700;
  color: #FF6B35;
}

/* 历史薪资记录 */
.salary-history-card {
  border-radius: 12px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-radius: 8px;
  border: 2px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-item:hover {
  border-color: #FF6B35;
  background-color: #FFF8F0;
}

.history-item.active {
  border-color: #FF6B35;
  background-color: #FFF8F0;
}

.history-month {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.history-amount {
  font-size: 20px;
  font-weight: 700;
  color: #FF6B35;
}

/* 无数据卡片 */
.no-data-card {
  border-radius: 12px;
  text-align: center;
  padding: 60px 20px;
}

/* 对话框 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .salary-view {
    padding: 12px;
  }

  .page-title {
    font-size: 22px;
  }

  .month-selector {
    flex-wrap: wrap;
  }

  .month-picker {
    width: 100%;
  }

  .appeal-btn {
    width: 100%;
    margin-left: 0;
    margin-top: 12px;
  }

  .total-salary-section {
    flex-direction: column;
    gap: 16px;
  }

  .total-salary-value .masked,
  .total-salary-value .amount {
    font-size: 36px;
  }

  .detail-value {
    font-size: 20px;
  }

  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
