<template>
  <div class="attendance-statistics-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">月度考勤统计</h1>
        <p class="page-subtitle">查看各部门月度考勤汇总数据</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" :loading="loading" @click="handleExport">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          导出报表
        </el-button>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-card">
      <div class="filter-row">
        <div class="filter-item">
          <label class="filter-label">统计月份</label>
          <el-date-picker
            v-model="selectedMonth"
            type="month"
            placeholder="选择月份"
            format="YYYY年MM月"
            value-format="YYYY-MM"
            @change="handleMonthChange"
            size="large"
            class="filter-input"
          />
        </div>
        <div class="filter-item">
          <label class="filter-label">部门筛选</label>
          <el-select
            v-model="selectedDepartment"
            placeholder="全部部门"
            clearable
            @change="handleDepartmentChange"
            size="large"
            class="filter-input"
          >
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </div>
        <div class="filter-item search-btn">
          <el-button type="primary" size="large" :loading="loading" @click="fetchStats">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            查询
          </el-button>
        </div>
      </div>
    </div>

    <!-- 汇总统计卡片 -->
    <div class="stats-summary" v-if="summary">
      <div class="summary-card total">
        <div class="summary-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <div class="summary-content">
          <span class="summary-value">{{ summary.total_employees }}</span>
          <span class="summary-label">在职员工</span>
        </div>
      </div>

      <div class="summary-card normal">
        <div class="summary-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <div class="summary-content">
          <span class="summary-value">{{ summary.normal_days }}</span>
          <span class="summary-label">正常出勤</span>
        </div>
      </div>

      <div class="summary-card rate">
        <div class="summary-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
        </div>
        <div class="summary-content">
          <span class="summary-value">{{ summary.attendance_rate }}%</span>
          <span class="summary-label">出勤率</span>
        </div>
      </div>

      <div class="summary-card late">
        <div class="summary-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <div class="summary-content">
          <span class="summary-value">{{ summary.late_days }}</span>
          <span class="summary-label">迟到次数</span>
        </div>
      </div>

      <div class="summary-card early">
        <div class="summary-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </div>
        <div class="summary-content">
          <span class="summary-value">{{ summary.early_days }}</span>
          <span class="summary-label">早退次数</span>
        </div>
      </div>

      <div class="summary-card absent">
        <div class="summary-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        </div>
        <div class="summary-content">
          <span class="summary-value">{{ summary.absent_days }}</span>
          <span class="summary-label">缺勤次数</span>
        </div>
      </div>
    </div>

    <!-- 部门统计表格 -->
    <div class="section-card">
      <div class="card-header">
        <div class="header-left">
          <div class="header-icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <line x1="3" y1="9" x2="21" y2="9"/>
              <line x1="9" y1="21" x2="9" y2="9"/>
            </svg>
          </div>
          <span class="card-title">部门考勤明细</span>
        </div>
        <div class="header-right">
          <span class="data-tip">数据更新于 {{ currentTime }}</span>
        </div>
      </div>
      <div class="card-body">
        <el-table
          :data="departmentStats"
          v-loading="loading"
          stripe
          class="custom-table"
          :header-cell-style="{ background: 'var(--color-gray-50)', color: 'var(--color-text-secondary)' }"
        >
          <el-table-column prop="department" label="部门" min-width="180">
            <template #default="{ row }">
              <div class="dept-name">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="dept-icon">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                  <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>
                {{ row.department }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="employee_count" label="部门人数" width="100" align="center" />
          <el-table-column prop="total_records" label="考勤记录" width="100" align="center" />
          <el-table-column prop="normal_days" label="正常" width="90" align="center">
            <template #default="{ row }">
              <span class="text-success">{{ row.normal_days }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="late_days" label="迟到" width="90" align="center">
            <template #default="{ row }">
              <span class="text-danger">{{ row.late_days }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="early_days" label="早退" width="90" align="center">
            <template #default="{ row }">
              <span class="text-warning">{{ row.early_days }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="absent_days" label="缺勤" width="90" align="center">
            <template #default="{ row }">
              <span class="text-info">{{ row.absent_days }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="leave_days" label="请假" width="90" align="center">
            <template #default="{ row }">
              <span class="text-primary">{{ row.leave_days }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="attendance_rate" label="出勤率" width="110" align="center">
            <template #default="{ row }">
              <el-progress
                :percentage="row.attendance_rate"
                :color="getRateColor(row.attendance_rate)"
                :stroke-width="8"
                :show-text="false"
              />
              <span class="rate-text" :style="{ color: getRateColor(row.attendance_rate) }">
                {{ row.attendance_rate }}%
              </span>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="!loading && departmentStats.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="empty-icon">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
          <p>暂无考勤数据</p>
          <span>请选择月份后点击查询按钮</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getMonthlyAttendanceStats } from '@/api/attendance'
import { getDepartmentList } from '@/api/department'

// 加载状态
const loading = ref(false)

// 月份选择
const selectedMonth = ref(new Date().toISOString().slice(0, 7))

// 部门筛选
const selectedDepartment = ref(null)
const departments = ref([])

// 统计数据
const summary = ref(null)
const departmentStats = ref([])

// 当前时间
const currentTime = computed(() => {
  const now = new Date()
  return `${now.toLocaleDateString()} ${now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
})

// 获取部门列表
async function fetchDepartments() {
  try {
    const res = await getDepartmentList({ page_size: 100, only_active: true })
    if (res.data?.code === 0) {
      departments.value = res.data?.data || []
    }
  } catch (error) {
    console.error('获取部门列表失败:', error)
  }
}

// 获取月度统计
async function fetchStats() {
  if (!selectedMonth.value) {
    ElMessage.warning('请选择月份')
    return
  }

  loading.value = true
  try {
    const res = await getMonthlyAttendanceStats(selectedMonth.value, selectedDepartment.value)
    if (res.data?.code === 0) {
      const data = res.data?.data || {}
      summary.value = data.summary || {}
      departmentStats.value = data.by_department || []
    } else {
      ElMessage.error(res.data?.message || '获取统计数据失败')
    }
  } catch (error) {
    console.error('获取月度统计失败:', error)
    ElMessage.error('获取统计数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 月份变化
function handleMonthChange() {
  fetchStats()
}

// 部门变化
function handleDepartmentChange() {
  fetchStats()
}

// 导出报表
function handleExport() {
  if (!summary.value) {
    ElMessage.warning('请先查询数据')
    return
  }

  // 生成 CSV 格式的报表
  const month = selectedMonth.value
  const headers = ['部门', '部门人数', '考勤记录', '正常', '迟到', '早退', '缺勤', '请假', '出勤率(%)']
  const rows = departmentStats.value.map(dept => [
    dept.department,
    dept.employee_count,
    dept.total_records,
    dept.normal_days,
    dept.late_days,
    dept.early_days,
    dept.absent_days,
    dept.leave_days,
    dept.attendance_rate
  ])

  // 添加汇总行
  const summaryRow = [
    '汇总',
    summary.value.total_employees,
    summary.value.total_records,
    summary.value.normal_days,
    summary.value.late_days,
    summary.value.early_days,
    summary.value.absent_days,
    summary.value.leave_days,
    summary.value.attendance_rate
  ]
  rows.unshift(summaryRow)

  // 构建 CSV 内容
  const csvContent = [
    `月度考勤统计报表 - ${month}`,
    '',
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n')

  // 下载文件
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `考勤统计_${month}.csv`
  link.click()
  URL.revokeObjectURL(link.href)

  ElMessage.success('报表导出成功')
}

// 出勤率颜色
function getRateColor(rate) {
  if (rate >= 95) return 'var(--color-success)'
  if (rate >= 85) return 'var(--color-warning)'
  return 'var(--color-danger)'
}

// 初始化
onMounted(() => {
  fetchDepartments()
  fetchStats()
})
</script>

<style scoped>
/* ========================================
   Attendance Statistics - Modern Corporate Design
   ======================================== */
.attendance-statistics-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .el-button svg {
  width: 16px;
  height: 16px;
  margin-right: 6px;
}

/* 筛选卡片 */
.filter-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.filter-row {
  display: flex;
  gap: 20px;
  align-items: flex-end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.filter-input {
  width: 220px;
}

.search-btn {
  margin-left: auto;
}

/* 汇总统计卡片 */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.summary-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.summary-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.summary-icon svg {
  width: 24px;
  height: 24px;
}

.summary-card.total .summary-icon {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
}

.summary-card.total .summary-icon svg {
  color: var(--color-primary);
}

.summary-card.normal .summary-icon {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.05) 100%);
}

.summary-card.normal .summary-icon svg {
  color: var(--color-success);
}

.summary-card.rate .summary-icon {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.05) 100%);
}

.summary-card.rate .summary-icon svg {
  color: var(--color-info);
}

.summary-card.late .summary-icon {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%);
}

.summary-card.late .summary-icon svg {
  color: var(--color-danger);
}

.summary-card.early .summary-icon {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 191, 36, 0.05) 100%);
}

.summary-card.early .summary-icon svg {
  color: var(--color-warning);
}

.summary-card.absent .summary-icon {
  background: linear-gradient(135deg, rgba(107, 114, 128, 0.1) 0%, rgba(156, 163, 175, 0.05) 100%);
}

.summary-card.absent .summary-icon svg {
  color: var(--color-text-tertiary);
}

.summary-content {
  display: flex;
  flex-direction: column;
}

.summary-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.summary-label {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin-top: 4px;
}

/* 通用卡片样式 */
.section-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(to bottom, var(--color-gray-50), var(--color-bg-secondary));
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon-wrapper {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow-primary);
}

.header-icon-wrapper svg {
  width: 18px;
  height: 18px;
  color: white;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.data-tip {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.card-body {
  padding: 24px;
}

/* 表格样式 */
.custom-table {
  border-radius: 0;
}

.dept-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.dept-icon {
  width: 16px;
  height: 16px;
  color: var(--color-text-tertiary);
}

.rate-text {
  margin-left: 8px;
  font-weight: 600;
  font-size: 12px;
}

.text-success {
  color: var(--color-success);
  font-weight: 500;
}

.text-danger {
  color: var(--color-danger);
  font-weight: 500;
}

.text-warning {
  color: var(--color-warning);
  font-weight: 500;
}

.text-info {
  color: var(--color-text-tertiary);
  font-weight: 500;
}

.text-primary {
  color: var(--color-primary);
  font-weight: 500;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--color-text-tertiary);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 8px;
  color: var(--color-text-secondary);
}

.empty-state span {
  font-size: 13px;
}

/* 响应式 */
@media (max-width: 1400px) {
  .stats-summary {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-row {
    flex-wrap: wrap;
  }

  .filter-input {
    width: 100%;
  }

  .search-btn {
    margin-left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .summary-card {
    padding: 16px;
  }

  .summary-value {
    font-size: 24px;
  }
}
</style>
