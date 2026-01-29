<template>
  <div class="salary-manage-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon">💰</span>
          薪资管理
        </h1>
        <p class="page-subtitle">管理员工薪资、处理申诉与调整</p>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <el-date-picker
          v-model="selectedMonth"
          type="month"
          placeholder="选择月份"
          format="YYYY年MM月"
          value-format="YYYY-MM"
          @change="handleMonthChange"
          class="month-picker"
        />
      </div>
      <div class="action-right">
        <el-button type="primary" :icon="Refresh" @click="handleGenerateSalary" :loading="generating">
          <span class="btn-icon">🔄</span>
          生成薪资
        </el-button>
        <el-button :icon="Download" @click="handleExport" class="export-btn">
          <span class="btn-icon">📊</span>
          导出工资表
        </el-button>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-section" v-loading="statsLoading">
      <div class="stat-card total-card">
        <div class="stat-icon-wrapper total-icon">
          <span class="stat-icon">💵</span>
        </div>
        <div class="stat-content">
          <div class="stat-label">本月薪资总额</div>
          <div class="stat-value">{{ formatCurrency(statsData.total_salary) }}</div>
        </div>
      </div>

      <div class="stat-card average-card">
        <div class="stat-icon-wrapper average-icon">
          <span class="stat-icon">📈</span>
        </div>
        <div class="stat-content">
          <div class="stat-label">平均薪资</div>
          <div class="stat-value">{{ formatCurrency(statsData.average_salary) }}</div>
        </div>
      </div>

      <div class="stat-card draft-card">
        <div class="stat-icon-wrapper draft-icon">
          <span class="stat-icon">📝</span>
        </div>
        <div class="stat-content">
          <div class="stat-label">待发布薪资</div>
          <div class="stat-value">{{ statsData.draft_count || 0 }}</div>
          <div class="stat-unit">份</div>
        </div>
      </div>

      <div class="stat-card appeal-card">
        <div class="stat-icon-wrapper appeal-icon">
          <span class="stat-icon">⚠️</span>
        </div>
        <div class="stat-content">
          <div class="stat-label">待处理申诉</div>
          <div class="stat-value">{{ statsData.pending_appeals || 0 }}</div>
          <div class="stat-unit">条</div>
        </div>
      </div>
    </div>

    <!-- 薪资列表 -->
    <div class="table-section">
      <el-table
        :data="salaryList"
        v-loading="tableLoading"
        stripe
        class="salary-table"
        @row-click="handleRowClick"
      >
        <el-table-column type="index" label="#" width="50" align="center" />

        <el-table-column prop="employee_name" label="员工姓名" min-width="100">
          <template #default="{ row }">
            <div class="employee-cell">
              <span class="employee-avatar">{{ row.employee_name?.[0] || '?' }}</span>
              <span class="employee-name">{{ row.employee_name || '-' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="position" label="岗位" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="getPositionTagType(row.position)" size="small">
              {{ getPositionLabel(row.position) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="year_month" label="月份" width="100" align="center">
          <template #default="{ row }">
            <span class="month-text">{{ formatMonth(row.year_month) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="base_salary" label="基本工资" width="110" align="right">
          <template #default="{ row }">
            <span class="amount-cell">{{ formatCurrency(row.base_salary) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="position_allowance" label="岗位津贴" width="100" align="right">
          <template #default="{ row }">
            <span class="amount-cell allowance">+{{ formatCurrency(row.position_allowance) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="overtime_pay" label="加班费" width="100" align="right">
          <template #default="{ row }">
            <span class="amount-cell" :class="{ 'overtime-highlight': row.overtime_pay > 0 }">
              +{{ formatCurrency(row.overtime_pay) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="deductions" label="扣款" width="90" align="right">
          <template #default="{ row }">
            <span class="amount-cell deduction" v-if="row.deductions > 0">
              -{{ formatCurrency(row.deductions) }}
            </span>
            <span class="amount-cell zero" v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column prop="total_salary" label="实发工资" width="120" align="right">
          <template #default="{ row }">
            <span class="amount-cell total-salary">{{ formatCurrency(row.total_salary) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)" size="small" class="status-tag">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button link type="primary" size="small" @click.stop="handleViewDetail(row)">
                详情
              </el-button>
              <el-button
                link
                type="warning"
                size="small"
                @click.stop="handleAdjust(row)"
                :disabled="row.status === 'PUBLISHED'"
              >
                调整
              </el-button>
              <el-button
                link
                type="success"
                size="small"
                @click.stop="handlePublish(row)"
                :disabled="row.status === 'PUBLISHED'"
              >
                发布
              </el-button>
              <el-popconfirm
                title="确认删除此薪资记录？"
                confirm-button-text="确认"
                cancel-button-text="取消"
                @confirm="handleDelete(row)"
              >
                <template #reference>
                  <el-button link type="danger" size="small" @click.stop>删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 调整薪资对话框 -->
    <el-dialog
      v-model="adjustDialogVisible"
      title="调整薪资"
      width="500px"
      class="adjust-dialog"
      :close-on-click-modal="false"
    >
      <div class="adjust-content" v-if="currentSalary">
        <div class="salary-summary">
          <div class="summary-item">
            <span class="summary-label">员工：</span>
            <span class="summary-value">{{ currentSalary.employee_name }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">月份：</span>
            <span class="summary-value">{{ formatMonth(currentSalary.year_month) }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">当前实发：</span>
            <span class="summary-value highlight">{{ formatCurrency(currentSalary.total_salary) }}</span>
          </div>
        </div>

        <el-divider />

        <el-form :model="adjustForm" :rules="adjustRules" ref="adjustFormRef" label-width="100px">
          <el-form-item label="基本工资" prop="base_salary">
            <el-input-number
              v-model="adjustForm.base_salary"
              :min="0"
              :step="100"
              :precision="2"
              controls-position="right"
              class="amount-input"
            />
            <span class="input-suffix">元</span>
          </el-form-item>

          <el-form-item label="加班费" prop="overtime_pay">
            <el-input-number
              v-model="adjustForm.overtime_pay"
              :min="0"
              :step="50"
              :precision="2"
              controls-position="right"
              class="amount-input"
            />
            <span class="input-suffix">元</span>
          </el-form-item>

          <el-form-item label="调整原因" prop="reason">
            <el-input
              v-model="adjustForm.reason"
              type="textarea"
              :rows="3"
              placeholder="请输入调整原因（必填）"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>

          <el-alert
            title="调整后将自动变更状态为'已调整'"
            type="info"
            :closable="false"
            show-icon
            class="adjust-hint"
          />
        </el-form>
      </div>

      <template #footer>
        <el-button @click="adjustDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAdjust" :loading="adjusting">确认调整</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="薪资详情"
      width="600px"
      class="detail-dialog"
    >
      <div class="detail-content" v-if="currentSalary">
        <div class="detail-header">
          <div class="employee-info">
            <span class="detail-avatar">{{ currentSalary.employee_name?.[0] || '?' }}</span>
            <div>
              <div class="detail-name">{{ currentSalary.employee_name }}</div>
              <div class="detail-meta">{{ formatMonth(currentSalary.year_month) }}</div>
            </div>
          </div>
          <el-tag :type="getStatusTagType(currentSalary.status)" size="large">
            {{ getStatusLabel(currentSalary.status) }}
          </el-tag>
        </div>

        <el-divider />

        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">基本工资</span>
            <span class="detail-amount">{{ formatCurrency(currentSalary.base_salary) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">岗位津贴</span>
            <span class="detail-amount positive">+{{ formatCurrency(currentSalary.position_allowance) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">加班费</span>
            <span class="detail-amount positive">+{{ formatCurrency(currentSalary.overtime_pay) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">迟到扣款</span>
            <span class="detail-amount negative">-{{ formatCurrency(currentSalary.late_deduction || 0) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">缺卡扣款</span>
            <span class="detail-amount negative">-{{ formatCurrency(currentSalary.missing_deduction || 0) }}</span>
          </div>
          <div class="detail-item total">
            <span class="detail-label">实发工资</span>
            <span class="detail-amount total">{{ formatCurrency(currentSalary.total_salary) }}</span>
          </div>
        </div>

        <div class="detail-stats" v-if="currentSalary.work_days || currentSalary.late_count">
          <el-tag size="small" type="info">出勤 {{ currentSalary.work_days || 0 }} 天</el-tag>
          <el-tag size="small" type="warning" v-if="currentSalary.late_count">
            迟到 {{ currentSalary.late_count }} 次
          </el-tag>
          <el-tag size="small" type="danger" v-if="currentSalary.missing_count">
            缺卡 {{ currentSalary.missing_count }} 次
          </el-tag>
          <el-tag size="small" type="success" v-if="currentSalary.overtime_hours">
            加班 {{ currentSalary.overtime_hours }} 小时
          </el-tag>
        </div>
      </div>
    </el-dialog>

    <!-- 申诉处理对话框 -->
    <el-dialog
      v-model="appealDialogVisible"
      title="申诉处理"
      width="600px"
      class="appeal-dialog"
      :close-on-click-modal="false"
    >
      <div class="appeal-content" v-if="currentAppeal">
        <div class="appeal-info">
          <el-alert
            :title="`${currentAppeal.employee_name} 的${currentAppeal.appeal_type === 'SALARY' ? '薪资' : '考勤'}申诉`"
            type="warning"
            :closable="false"
            show-icon
          >
            <div class="appeal-reason">
              <strong>申诉原因：</strong>{{ currentAppeal.reason }}
            </div>
          </el-alert>
        </div>

        <el-divider />

        <el-form :model="appealForm" :rules="appealRules" ref="appealFormRef" label-width="100px">
          <el-form-item label="处理结果" prop="approve">
            <el-radio-group v-model="appealForm.approve">
              <el-radio :label="true" size="large">
                <span class="radio-label approve">✅ 批准申诉</span>
              </el-radio>
              <el-radio :label="false" size="large">
                <span class="radio-label reject">❌ 拒绝申诉</span>
              </el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="审批意见" prop="approval_remark">
            <el-input
              v-model="appealForm.approval_remark"
              type="textarea"
              :rows="4"
              :placeholder="appealForm.approve ? '请输入批准原因' : '请输入拒绝原因（必填）'"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <el-button @click="appealDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAppeal" :loading="appealing">确认处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Download } from '@element-plus/icons-vue'
import {
  getSalaryList,
  generateSalary,
  adjustSalary,
  publishSalary,
  deleteSalary,
  getPendingAppeals,
  approveAppeal
} from '../../api/salary'

// ==================== 状态数据 ====================
const selectedMonth = ref('')
const salaryList = ref([])
const tableLoading = ref(false)
const statsLoading = ref(false)
const generating = ref(false)
const adjusting = ref(false)
const appealing = ref(false)

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 统计数据
const statsData = ref({
  total_salary: 0,
  average_salary: 0,
  draft_count: 0,
  pending_appeals: 0
})

// 对话框状态
const adjustDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const appealDialogVisible = ref(false)

// 当前操作对象
const currentSalary = ref(null)
const currentAppeal = ref(null)

// 表单引用
const adjustFormRef = ref(null)
const appealFormRef = ref(null)

// 调整表单
const adjustForm = reactive({
  base_salary: 0,
  overtime_pay: 0,
  reason: ''
})

const adjustRules = {
  base_salary: [{ required: true, message: '请输入基本工资', trigger: 'blur' }],
  overtime_pay: [{ required: true, message: '请输入加班费', trigger: 'blur' }],
  reason: [
    { required: true, message: '请输入调整原因', trigger: 'blur' },
    { min: 5, max: 200, message: '调整原因长度在 5 到 200 个字符', trigger: 'blur' }
  ]
}

// 申诉表单
const appealForm = reactive({
  approve: true,
  approval_remark: ''
})

const appealRules = {
  approval_remark: [
    { required: true, message: '请输入审批意见', trigger: 'blur' },
    { min: 5, max: 200, message: '审批意见长度在 5 到 200 个字符', trigger: 'blur' }
  ]
}

// ==================== 工具函数 ====================
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '¥0.00'
  return `¥${Number(amount).toFixed(2)}`
}

const formatMonth = (yearMonth) => {
  if (!yearMonth) return '-'
  const [year, month] = yearMonth.split('-')
  return `${year}年${month}月`
}

const getPositionLabel = (position) => {
  const map = {
    CHEF: '厨师',
    PASTRY: '面点',
    PREP: '切配',
    CLEANER: '保洁',
    SERVER: '服务员',
    MANAGER: '经理'
  }
  return map[position] || position
}

const getPositionTagType = (position) => {
  const map = {
    CHEF: 'warning',
    PASTRY: 'danger',
    PREP: 'primary',
    CLEANER: 'success',
    SERVER: 'info',
    MANAGER: ''
  }
  return map[position] || ''
}

const getStatusLabel = (status) => {
  const map = {
    DRAFT: '草稿',
    PUBLISHED: '已发布',
    ADJUSTED: '已调整',
    APPEALED: '申诉中'
  }
  return map[status] || status
}

const getStatusTagType = (status) => {
  const map = {
    DRAFT: 'info',
    PUBLISHED: 'success',
    ADJUSTED: 'warning',
    APPEALED: 'danger'
  }
  return map[status] || ''
}

// ==================== 数据加载 ====================
const loadSalaryList = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    if (selectedMonth.value) {
      params.year_month = selectedMonth.value
    }

    const response = await getSalaryList(params)
    if (response.code === 200) {
      salaryList.value = response.data.results || []
      pagination.total = response.data.count || 0

      // 计算统计数据
      updateStats(response.data.results || [])
    }
  } catch (error) {
    console.error('加载薪资列表失败:', error)
    ElMessage.error('加载薪资列表失败')
  } finally {
    tableLoading.value = false
  }
}

const updateStats = (data) => {
  if (!data.length) {
    statsData.value = {
      total_salary: 0,
      average_salary: 0,
      draft_count: 0,
      pending_appeals: 0
    }
    return
  }

  const total = data.reduce((sum, item) => sum + Number(item.total_salary || 0), 0)
  const draftCount = data.filter(item => item.status === 'DRAFT').length

  statsData.value = {
    total_salary: total,
    average_salary: data.length ? total / data.length : 0,
    draft_count: draftCount,
    pending_appeals: statsData.value.pending_appeals || 0 // 保持之前的值
  }

  // 获取待处理申诉数量
  fetchPendingAppealsCount()
}

// 获取待处理申诉数量
const fetchPendingAppealsCount = async () => {
  try {
    const response = await getPendingAppeals()
    // 从返回的数据中获取 count
    const count = response.data?.count || (Array.isArray(response.data) ? response.data.length : 0)
    statsData.value.pending_appeals = count
  } catch (error) {
    console.error('获取待处理申诉数量失败:', error)
  }
}

// ==================== 事件处理 ====================
const handleMonthChange = () => {
  pagination.page = 1
  loadSalaryList()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadSalaryList()
}

const handlePageChange = (page) => {
  pagination.page = page
  loadSalaryList()
}

const handleGenerateSalary = async () => {
  if (!selectedMonth.value) {
    ElMessage.warning('请先选择月份')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确认为 ${formatMonth(selectedMonth.value)} 生成薪资？此操作将根据考勤数据自动计算所有员工的薪资。`,
      '生成薪资确认',
      {
        confirmButtonText: '确认生成',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    generating.value = true
    const response = await generateSalary({ year_month: selectedMonth.value })
    if (response.code === 200) {
      ElMessage.success(`薪资生成成功！创建 ${response.data.created} 条记录`)
      loadSalaryList()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('生成薪资失败:', error)
      ElMessage.error('生成薪资失败')
    }
  } finally {
    generating.value = false
  }
}

const handleExport = async () => {
  if (!selectedMonth.value) {
    ElMessage.warning('请先选择月份')
    return
  }
  ElMessage.info('导出功能即将在后续版本中实现')
}

const handleRowClick = (row) => {
  handleViewDetail(row)
}

const handleViewDetail = (row) => {
  currentSalary.value = { ...row }
  detailDialogVisible.value = true
}

const handleAdjust = (row) => {
  currentSalary.value = { ...row }
  adjustForm.base_salary = row.base_salary
  adjustForm.overtime_pay = row.overtime_pay
  adjustForm.reason = ''
  adjustDialogVisible.value = true
}

const confirmAdjust = async () => {
  try {
    await adjustFormRef.value.validate()

    adjusting.value = true
    const response = await adjustSalary(currentSalary.value.id, {
      base_salary: adjustForm.base_salary,
      overtime_pay: adjustForm.overtime_pay,
      reason: adjustForm.reason
    })

    if (response.code === 200) {
      ElMessage.success('薪资调整成功')
      adjustDialogVisible.value = false
      loadSalaryList()
    }
  } catch (error) {
    if (error !== false) {
      console.error('调整薪资失败:', error)
      ElMessage.error('调整薪资失败')
    }
  } finally {
    adjusting.value = false
  }
}

const handlePublish = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认发布 ${row.employee_name} ${formatMonth(row.year_month)} 的薪资？发布后员工即可查看。`,
      '发布薪资确认',
      {
        confirmButtonText: '确认发布',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await publishSalary(row.id)
    if (response.code === 200) {
      ElMessage.success('薪资发布成功')
      loadSalaryList()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发布薪资失败:', error)
      ElMessage.error('发布薪资失败')
    }
  }
}

const handleDelete = async (row) => {
  try {
    const response = await deleteSalary(row.id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      loadSalaryList()
    }
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

const handleAppealAction = (appeal) => {
  currentAppeal.value = { ...appeal }
  appealForm.approve = true
  appealForm.approval_remark = ''
  appealDialogVisible.value = true
}

const confirmAppeal = async () => {
  try {
    await appealFormRef.value.validate()

    appealing.value = true
    const response = await approveAppeal(currentAppeal.value.id, {
      approve: appealForm.approve,
      approval_remark: appealForm.approval_remark,
      approver_id: 1 // TODO: 从用户信息中获取
    })

    if (response.code === 200) {
      ElMessage.success(appealForm.approve ? '申诉已批准' : '申诉已拒绝')
      appealDialogVisible.value = false
      loadSalaryList()
    }
  } catch (error) {
    if (error !== false) {
      console.error('处理申诉失败:', error)
      ElMessage.error('处理申诉失败')
    }
  } finally {
    appealing.value = false
  }
}

// ==================== 生命周期 ====================
onMounted(() => {
  // 默认选择当前月份
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  selectedMonth.value = `${year}-${month}`

  loadSalaryList()
})
</script>

<style scoped>
/* ==================== 全局样式 ==================== */
.salary-manage-view {
  padding: 0;
  background-color: transparent;
}

/* ==================== 页面标题 ==================== */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  background: linear-gradient(135deg, #ffffff 0%, #FFF8F0 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.1);
  border-left: 4px solid #FF6B35;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #333333;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 28px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.page-subtitle {
  font-size: 14px;
  color: #888888;
  margin: 0;
}

/* ==================== 操作栏 ==================== */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: #ffffff;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.action-left,
.action-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.month-picker :deep(.el-input__wrapper) {
  border-radius: 8px;
  border-color: #FF6B35;
  transition: all 0.3s ease;
}

.month-picker :deep(.el-input__wrapper:hover),
.month-picker :deep(.el-input__wrapper.is-focus) {
  border-color: #FF6B35;
  box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1);
}

.btn-icon {
  margin-right: 4px;
}

.export-btn {
  border-color: #FF6B35;
  color: #FF6B35;
}

.export-btn:hover {
  background-color: #FF6B35;
  color: #ffffff;
}

/* ==================== 统计卡片 ==================== */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.15);
}

.total-card:hover {
  border-color: #FF6B35;
}

.average-card:hover {
  border-color: #F7C52D;
}

.draft-card:hover {
  border-color: #4CAF50;
}

.appeal-card:hover {
  border-color: #F44336;
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.total-icon {
  background: linear-gradient(135deg, #FFE8D6 0%, #FFD8B8 100%);
}

.average-icon {
  background: linear-gradient(135deg, #FFF4D6 0%, #FFE9B8 100%);
}

.draft-icon {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
}

.appeal-icon {
  background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
}

.stat-icon {
  font-size: 28px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 13px;
  color: #888888;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #333333;
  line-height: 1.2;
}

.stat-unit {
  font-size: 12px;
  color: #888888;
  margin-left: 4px;
}

/* ==================== 表格区域 ==================== */
.table-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.salary-table {
  width: 100%;
}

.salary-table :deep(.el-table__row) {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.salary-table :deep(.el-table__row:hover) {
  background-color: #FFF8F0 !important;
}

.employee-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.employee-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B35 0%, #F7C52D 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.employee-name {
  font-weight: 500;
  color: #333333;
}

.month-text {
  color: #666666;
  font-size: 13px;
}

.amount-cell {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-weight: 600;
  color: #333333;
  font-size: 14px;
}

.amount-cell.allowance {
  color: #4CAF50;
}

.amount-cell.overtime-highlight {
  color: #FF6B35;
  font-weight: 700;
}

.amount-cell.deduction {
  color: #F44336;
}

.amount-cell.zero {
  color: #cccccc;
  font-weight: 400;
}

.amount-cell.total-salary {
  color: #FF6B35;
  font-size: 16px;
  font-weight: 700;
}

.status-tag {
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 4px;
  justify-content: center;
}

.action-buttons .el-button {
  padding: 4px 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* ==================== 对话框样式 ==================== */
.adjust-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #FF6B35 0%, #F7C52D 100%);
  color: #ffffff;
  border-radius: 12px 12px 0 0;
  padding: 20px;
}

.adjust-dialog :deep(.el-dialog__title) {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.adjust-content {
  padding: 20px 0;
}

.salary-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.summary-item {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}

.summary-label {
  font-size: 12px;
  color: #888888;
  display: block;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
}

.summary-value.highlight {
  color: #FF6B35;
  font-size: 18px;
}

.amount-input {
  width: 100%;
}

.input-suffix {
  margin-left: 8px;
  color: #888888;
  font-size: 14px;
}

.adjust-hint {
  margin-top: 16px;
}

/* ==================== 详情对话框 ==================== */
.detail-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: #ffffff;
  border-radius: 12px 12px 0 0;
  padding: 20px;
}

.detail-dialog :deep(.el-dialog__title) {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.detail-content {
  padding: 20px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.employee-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B35 0%, #F7C52D 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
}

.detail-name {
  font-size: 18px;
  font-weight: 600;
  color: #333333;
}

.detail-meta {
  font-size: 14px;
  color: #888888;
  margin-top: 4px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.detail-item.total {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, #FFF8F0 0%, #FFE8D6 100%);
  border: 2px solid #FF6B35;
}

.detail-label {
  font-size: 14px;
  color: #666666;
}

.detail-amount {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 16px;
  font-weight: 600;
  color: #333333;
}

.detail-amount.positive {
  color: #4CAF50;
}

.detail-amount.negative {
  color: #F44336;
}

.detail-amount.total {
  font-size: 20px;
  color: #FF6B35;
}

.detail-stats {
  display: flex;
  gap: 8px;
  margin-top: 20px;
  flex-wrap: wrap;
}

/* ==================== 申诉对话框 ==================== */
.appeal-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #F44336 0%, #FF9800 100%);
  color: #ffffff;
  border-radius: 12px 12px 0 0;
  padding: 20px;
}

.appeal-dialog :deep(.el-dialog__title) {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.appeal-content {
  padding: 20px 0;
}

.appeal-reason {
  margin-top: 12px;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 8px;
  white-space: pre-wrap;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.radio-label.approve {
  color: #4CAF50;
  font-weight: 500;
}

.radio-label.reject {
  color: #F44336;
  font-weight: 500;
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 1200px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .action-bar {
    flex-direction: column;
    gap: 12px;
  }

  .action-left,
  .action-right {
    width: 100%;
  }

  .stats-section {
    grid-template-columns: 1fr;
  }

  .salary-summary {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 20px;
  }
}
</style>
