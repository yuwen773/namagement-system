<template>
  <div class="attendance-page">
    <!-- 今日考勤卡片 -->
    <div class="section-card today-card">
      <div class="card-header">
        <div class="header-left">
          <div class="header-icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <span class="card-title">今日考勤</span>
          <el-tag :type="todayStatusType" size="small" class="status-badge">{{ todayData.status_text }}</el-tag>
        </div>
        <div class="header-right">
          <el-button
            type="primary"
            :loading="loading.checkIn"
            :disabled="todayData.has_check_in"
            @click="handleCheckIn"
            class="action-btn"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="18 15 12 9 6 15"/>
            </svg>
            签到
          </el-button>
          <el-button
            type="success"
            :loading="loading.checkOut"
            :disabled="!todayData.has_check_in || todayData.has_check_out"
            @click="handleCheckOut"
            class="action-btn"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
            签退
          </el-button>
        </div>
      </div>
      <div class="card-body">
        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-icon checkin">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="18 15 12 9 6 15"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-label">签到时间</span>
              <span class="stat-value">{{ todayData.check_in_time || '--:--:--' }}</span>
            </div>
            <div v-if="todayData.check_in_time && todayData.status === 'late'" class="late-indicator">迟到</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon checkout">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-label">签退时间</span>
              <span class="stat-value">{{ todayData.check_out_time || '--:--:--' }}</span>
            </div>
            <div v-if="todayData.check_out_time && todayData.status === 'early'" class="early-indicator">早退</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 月度统计 -->
    <div class="section-card stats-card">
      <div class="card-header">
        <div class="header-left">
          <div class="header-icon-wrapper chart">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
          </div>
          <span class="card-title">月度统计</span>
        </div>
        <el-date-picker
          v-model="selectedMonth"
          type="month"
          placeholder="选择月份"
          format="YYYY年MM月"
          value-format="YYYY-MM"
          @change="fetchStats"
          size="small"
          class="month-picker"
        />
      </div>
      <div class="card-body">
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-box-content normal">
              <div class="stat-icon-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <span class="stat-number">{{ stats.normal_days }}</span>
              <span class="stat-text">正常</span>
            </div>
          </div>
          <div class="stat-box">
            <div class="stat-box-content late">
              <div class="stat-icon-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <span class="stat-number">{{ stats.late_days }}</span>
              <span class="stat-text">迟到</span>
            </div>
          </div>
          <div class="stat-box">
            <div class="stat-box-content early">
              <div class="stat-icon-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </div>
              <span class="stat-number">{{ stats.early_days }}</span>
              <span class="stat-text">早退</span>
            </div>
          </div>
          <div class="stat-box">
            <div class="stat-box-content absent">
              <div class="stat-icon-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="15" y1="9" x2="9" y2="15"/>
                  <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
              </div>
              <span class="stat-number">{{ stats.absent_days }}</span>
              <span class="stat-text">缺勤</span>
            </div>
          </div>
          <div class="stat-box">
            <div class="stat-box-content leave">
              <div class="stat-icon-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <span class="stat-number">{{ stats.leave_days }}</span>
              <span class="stat-text">请假</span>
            </div>
          </div>
          <div class="stat-box">
            <div class="stat-box-content total">
              <div class="stat-icon-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
              </div>
              <span class="stat-number">{{ stats.total_days }}</span>
              <span class="stat-text">出勤天数</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 考勤记录列表 -->
    <div class="section-card">
      <div class="card-header">
        <div class="header-left">
          <div class="header-icon-wrapper list">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"/>
              <line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/>
              <line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/>
              <line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
          </div>
          <span class="card-title">考勤记录</span>
        </div>
        <div class="filter-group">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleFilterChange"
            size="small"
            clearable
            class="date-range-picker"
          />
          <el-select
            v-model="filterForm.status"
            placeholder="状态筛选"
            clearable
            @change="handleFilterChange"
            size="small"
            class="status-filter"
          >
            <el-option label="正常" value="normal" />
            <el-option label="迟到" value="late" />
            <el-option label="早退" value="early" />
            <el-option label="缺勤" value="absent" />
            <el-option label="请假" value="leave" />
          </el-select>
        </div>
      </div>
      <div class="card-body">
        <el-table :data="records" v-loading="loading.records" stripe class="custom-table">
          <el-table-column prop="date" label="日期" width="120" />
          <el-table-column prop="check_in_time" label="签到时间" width="120">
            <template #default="{ row }">
              <span :class="{ 'text-danger': row.status === 'late', 'late-value': row.status === 'late' }">
                {{ row.check_in_time || '--:--:--' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="check_out_time" label="签退时间" width="120">
            <template #default="{ row }">
              <span :class="{ 'text-warning': row.status === 'early', 'early-value': row.status === 'early' }">
                {{ row.check_out_time || '--:--:--' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small" class="status-tag">
                {{ getStatusText(row.status) }}
              </el-tag>
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
            @size-change="fetchRecords"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { checkIn, checkOut, getTodayAttendance, getAttendanceRecords, getAttendanceStats } from '@/api/attendance'

// 加载状态
const loading = reactive({
  checkIn: false,
  checkOut: false,
  records: false
})

// 今日考勤数据
const todayData = reactive({
  has_check_in: false,
  has_check_out: false,
  check_in_time: null,
  check_out_time: null,
  status: null,
  status_text: '未签到'
})

// 月度统计数据
const stats = reactive({
  total_days: 0,
  normal_days: 0,
  late_days: 0,
  early_days: 0,
  absent_days: 0,
  leave_days: 0
})

// 考勤记录列表
const records = ref([])

// 筛选表单
const filterForm = reactive({
  dateRange: null,
  status: ''
})

// 分页状态
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 月份选择
const selectedMonth = ref(new Date().toISOString().slice(0, 7))

// 今日状态标签颜色
const todayStatusType = computed(() => getStatusType(todayData.status))

// 获取今日考勤
async function fetchTodayAttendance() {
  try {
    const res = await getTodayAttendance()
    const data = res.data?.data || {}
    todayData.has_check_in = data.has_check_in || false
    todayData.has_check_out = data.has_check_out || false

    if (data.check_in_time) {
      todayData.check_in_time = data.check_in_time
    }
    if (data.check_out_time) {
      todayData.check_out_time = data.check_out_time
    }

    if (data.status) {
      todayData.status = data.status
      todayData.status_text = getStatusText(data.status)
    } else if (todayData.has_check_in && !todayData.has_check_out) {
      todayData.status_text = '已签到'
    } else if (todayData.has_check_in && todayData.has_check_out) {
      todayData.status_text = '已完成'
    }
  } catch (error) {
    console.error('获取今日考勤失败:', error)
  }
}

// 获取月度统计
async function fetchStats() {
  if (!selectedMonth.value) return

  try {
    const res = await getAttendanceStats(selectedMonth.value)
    const data = res.data?.data || {}
    Object.assign(stats, data)
  } catch (error) {
    console.error('获取月度统计失败:', error)
  }
}

// 获取考勤记录
async function fetchRecords() {
  loading.records = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }

    if (filterForm.dateRange && filterForm.dateRange.length === 2) {
      params.date_start = filterForm.dateRange[0]
      params.date_end = filterForm.dateRange[1]
    }

    if (filterForm.status) {
      params.status = filterForm.status
    }

    const res = await getAttendanceRecords(params)
    if (res.data?.code === 0) {
      records.value = res.data?.data || []
      pagination.total = res.data?.total || 0
    }
  } catch (error) {
    console.error('获取考勤记录失败:', error)
    ElMessage.error('获取考勤记录失败')
  } finally {
    loading.records = false
  }
}

// 筛选条件变化
function handleFilterChange() {
  pagination.page = 1
  fetchRecords()
}

// 页码变化
function handlePageChange(page) {
  pagination.page = page
  fetchRecords()
}

// 签到
async function handleCheckIn() {
  loading.checkIn = true
  try {
    const res = await checkIn()
    ElMessage.success(res.data?.message || '签到成功')
    await fetchTodayAttendance()
  } catch (error) {
    const msg = error.response?.data?.message || '签到失败'
    ElMessage.warning(msg)
  } finally {
    loading.checkIn = false
  }
}

// 签退
async function handleCheckOut() {
  loading.checkOut = true
  try {
    const res = await checkOut()
    ElMessage.success(res.data?.message || '签退成功')
    await fetchTodayAttendance()
  } catch (error) {
    const msg = error.response?.data?.message || '签退失败'
    ElMessage.warning(msg)
  } finally {
    loading.checkOut = false
  }
}

// 状态类型映射
function getStatusType(status) {
  const map = {
    normal: 'success',
    late: 'danger',
    early: 'warning',
    absent: 'info',
    leave: ''
  }
  return map[status] || 'info'
}

// 状态文本映射
function getStatusText(status) {
  const map = {
    normal: '正常',
    late: '迟到',
    early: '早退',
    absent: '缺勤',
    leave: '请假'
  }
  return map[status] || '未知'
}

// 初始化
onMounted(() => {
  fetchTodayAttendance()
  fetchStats()
  fetchRecords()
})
</script>

<style scoped>
/* ========================================
   Attendance - Modern Corporate Design
   ======================================== */
.attendance-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 通用卡片样式 */
.section-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  overflow: hidden;
}

.section-card:hover {
  box-shadow: var(--shadow-md);
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

.header-icon-wrapper.chart {
  background: linear-gradient(135deg, var(--color-success) 0%, var(--color-success-light) 100%);
  box-shadow: var(--shadow-glow-success);
}

.header-icon-wrapper.list {
  background: linear-gradient(135deg, var(--color-warning) 0%, var(--color-warning-light) 100%);
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.15);
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

.status-badge {
  font-weight: 500;
}

.header-right {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.card-body {
  padding: 24px;
}

/* 今日考勤 */
.stat-row {
  display: flex;
  gap: 48px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon.checkin {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
}

.stat-icon.checkin svg {
  color: var(--color-primary);
  width: 24px;
  height: 24px;
}

.stat-icon.checkout {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.05) 100%);
}

.stat-icon.checkout svg {
  color: var(--color-success);
  width: 24px;
  height: 24px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.late-indicator,
.early-indicator {
  position: absolute;
  top: -8px;
  right: -8px;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 600;
}

.late-indicator {
  background: var(--color-danger-subtle);
  color: var(--color-danger);
}

.early-indicator {
  background: var(--color-warning-subtle);
  color: var(--color-warning);
}

/* 月度统计 */
.month-picker {
  width: 180px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.stat-box {
  background: var(--color-gray-50);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--transition-base);
}

.stat-box:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-box-content {
  padding: 20px 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.stat-box-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.stat-box-content.normal::before {
  background: var(--color-success);
}

.stat-box-content.late::before {
  background: var(--color-danger);
}

.stat-box-content.early::before {
  background: var(--color-warning);
}

.stat-box-content.absent::before {
  background: var(--color-info);
}

.stat-box-content.leave::before {
  background: var(--color-primary);
}

.stat-box-content.total::before {
  background: var(--color-primary);
}

.stat-icon-small {
  width: 28px;
  height: 28px;
  margin: 0 auto 8px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-box-content.normal .stat-icon-small {
  background: var(--color-success-subtle);
}

.stat-box-content.normal .stat-icon-small svg {
  color: var(--color-success);
}

.stat-box-content.late .stat-icon-small {
  background: var(--color-danger-subtle);
}

.stat-box-content.late .stat-icon-small svg {
  color: var(--color-danger);
}

.stat-box-content.early .stat-icon-small {
  background: var(--color-warning-subtle);
}

.stat-box-content.early .stat-icon-small svg {
  color: var(--color-warning);
}

.stat-box-content.absent .stat-icon-small {
  background: var(--color-info-subtle);
}

.stat-box-content.absent .stat-icon-small svg {
  color: var(--color-info);
}

.stat-box-content.leave .stat-icon-small {
  background: var(--color-primary-subtle);
}

.stat-box-content.leave .stat-icon-small svg {
  color: var(--color-primary);
}

.stat-box-content.total .stat-icon-small {
  background: var(--color-primary-subtle);
}

.stat-box-content.total .stat-icon-small svg {
  color: var(--color-primary);
}

.stat-icon-small svg {
  width: 14px;
  height: 14px;
}

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 4px;
  line-height: 1.2;
}

.stat-text {
  font-size: 12px;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

/* 筛选组样式 */
.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-range-picker {
  width: 260px;
}

.status-filter {
  width: 100px;
}

/* 表格样式 */
.custom-table {
  border-radius: 0;
}

.status-tag {
  font-weight: 500;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 20px;
  background: var(--color-gray-50);
  border-top: 1px solid var(--color-border-light);
  margin-top: 0;
}

/* 状态文本颜色 */
.text-danger,
.late-value {
  color: var(--color-danger);
  font-weight: 500;
}

.text-warning,
.early-value {
  color: var(--color-warning);
  font-weight: 500;
}

/* 响应式 */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stat-row {
    flex-direction: column;
    gap: 24px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .card-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .filter-group {
    width: 100%;
    flex-wrap: wrap;
  }

  .date-range-picker {
    width: 100%;
  }

  .stat-item {
    width: 100%;
  }
}
</style>
