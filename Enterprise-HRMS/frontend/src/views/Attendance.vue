<template>
  <div class="attendance-page">
    <h2>考勤管理</h2>

    <!-- 今日考勤卡片 -->
    <el-card class="today-card">
      <template #header>
        <div class="card-header">
          <span>今日考勤</span>
          <el-tag :type="todayStatusTag">{{ todayData.status_text }}</el-tag>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <el-icon size="24"><Clock /></el-icon>
            <div class="stat-info">
              <span class="stat-label">签到时间</span>
              <span class="stat-value">{{ todayData.check_in_time || '--:--:--' }}</span>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <el-icon size="24"><Timer /></el-icon>
            <div class="stat-info">
              <span class="stat-label">签退时间</span>
              <span class="stat-value">{{ todayData.check_out_time || '--:--:--' }}</span>
            </div>
          </div>
        </el-col>
        <el-col :span="8" style="text-align: right;">
          <el-button
            type="primary"
            :loading="loading.checkIn"
            :disabled="todayData.has_check_in"
            @click="handleCheckIn"
          >
            <el-icon><Top /></el-icon>
            签到
          </el-button>
          <el-button
            type="success"
            :loading="loading.checkOut"
            :disabled="!todayData.has_check_in || todayData.has_check_out"
            @click="handleCheckOut"
          >
            <el-icon><Bottom /></el-icon>
            签退
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 月度统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <span>月度统计</span>
          <el-date-picker
            v-model="selectedMonth"
            type="month"
            placeholder="选择月份"
            format="YYYY年MM月"
            value-format="YYYY-MM"
            @change="fetchStats"
            size="small"
          />
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="4">
          <div class="stat-box normal">
            <span class="stat-number">{{ stats.normal_days }}</span>
            <span class="stat-text">正常</span>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-box late">
            <span class="stat-number">{{ stats.late_days }}</span>
            <span class="stat-text">迟到</span>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-box early">
            <span class="stat-number">{{ stats.early_days }}</span>
            <span class="stat-text">早退</span>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-box absent">
            <span class="stat-number">{{ stats.absent_days }}</span>
            <span class="stat-text">缺勤</span>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-box leave">
            <span class="stat-number">{{ stats.leave_days }}</span>
            <span class="stat-text">请假</span>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-box total">
            <span class="stat-number">{{ stats.total_days }}</span>
            <span class="stat-text">出勤天数</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 考勤记录列表 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考勤记录</span>
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
              style="width: 260px;"
            />
            <el-select
              v-model="filterForm.status"
              placeholder="状态筛选"
              clearable
              @change="handleFilterChange"
              size="small"
              style="width: 120px; margin-left: 10px;"
            >
              <el-option label="正常" value="normal" />
              <el-option label="迟到" value="late" />
              <el-option label="早退" value="early" />
              <el-option label="缺勤" value="absent" />
              <el-option label="请假" value="leave" />
            </el-select>
          </div>
        </div>
      </template>
      <el-table :data="records" v-loading="loading.records" stripe>
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="check_in_time" label="签到时间" width="120">
          <template #default="{ row }">
            <span :class="{ 'text-danger': row.status === 'late' }">
              {{ row.check_in_time || '--:--:--' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="check_out_time" label="签退时间" width="120">
          <template #default="{ row }">
            <span :class="{ 'text-warning': row.status === 'early' }">
              {{ row.check_out_time || '--:--:--' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <div class="pagination-container">
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
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Clock, Timer, Top, Bottom } from '@element-plus/icons-vue'
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

    // 计算今日状态
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

    // 日期范围
    if (filterForm.dateRange && filterForm.dateRange.length === 2) {
      params.date_start = filterForm.dateRange[0]
      params.date_end = filterForm.dateRange[1]
    }

    // 状态筛选
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

// 今日状态标签颜色
const todayStatusTag = computed(() => {
  return getStatusType(todayData.status)
})

// 初始化
onMounted(() => {
  fetchTodayAttendance()
  fetchStats()
  fetchRecords()
})
</script>

<style scoped>
.attendance-page {
  padding: 20px;
}

.attendance-page h2 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #303133;
}

.today-card,
.stats-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.stat-box {
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.stat-box.normal { background: #f0f9eb; }
.stat-box.late { background: #fef0f0; }
.stat-box.early { background: #fdf6ec; }
.stat-box.absent { background: #f4f4f5; }
.stat-box.leave { background: #ecf5ff; }
.stat-box.total { background: #ecf5ff; }

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-text {
  font-size: 14px;
  color: #606266;
}

.text-danger {
  color: #f56c6c;
}

.text-warning {
  color: #e6a23c;
}

.filter-group {
  display: flex;
  align-items: center;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
