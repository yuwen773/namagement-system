<template>
  <div class="attendance-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon :size="28" class="title-icon"><DocumentChecked /></el-icon>
        考勤记录查询
      </h1>
      <p class="page-subtitle">查看您的考勤记录和统计数据</p>
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
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <div class="statistics-cards">
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon present-icon">
            <el-icon :size="32"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.present_days || 0 }}</div>
            <div class="stat-label">出勤天数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon late-icon">
            <el-icon :size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.late_count || 0 }}</div>
            <div class="stat-label">迟到次数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon missing-icon">
            <el-icon :size="32"><CircleClose /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.missing_count || 0 }}</div>
            <div class="stat-label">缺卡次数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon overtime-icon">
            <el-icon :size="32"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.overtime_hours?.toFixed(1) || '0.0' }}</div>
            <div class="stat-label">加班时长</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 考勤记录列表 -->
    <el-card class="records-card" shadow="hover">
      <template #header>
        <div class="records-header">
          <span class="records-title">考勤记录明细</span>
          <el-tag type="info" size="large">共 {{ attendanceList.length }} 条记录</el-tag>
        </div>
      </template>

      <div v-loading="loading" class="records-table-container">
        <el-table
          :data="attendanceList"
          stripe
          :row-class-name="getRowClassName"
          class="attendance-table"
        >
          <el-table-column prop="date" label="日期" width="120" align="center">
            <template #default="{ row }">
              <div class="date-cell">
                <div class="date-day">{{ getDay(row.date) }}</div>
                <div class="date-month">{{ getMonth(row.date) }}</div>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="clock_in_time" label="签到时间" width="160" align="center">
            <template #default="{ row }">
              <div v-if="row.clock_in_time" class="time-cell">
                <el-icon class="time-icon"><Clock /></el-icon>
                <span>{{ formatTime(row.clock_in_time) }}</span>
              </div>
              <span v-else class="no-data">-</span>
            </template>
          </el-table-column>

          <el-table-column prop="clock_out_time" label="签退时间" width="160" align="center">
            <template #default="{ row }">
              <div v-if="row.clock_out_time" class="time-cell">
                <el-icon class="time-icon"><Clock /></el-icon>
                <span>{{ formatTime(row.clock_out_time) }}</span>
              </div>
              <span v-else class="no-data">-</span>
            </template>
          </el-table-column>

          <el-table-column prop="status" label="状态" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusTagType(row.status)" effect="dark">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="clock_in_location" label="签到地点" min-width="150" show-overflow-tooltip>
            <template #default="{ row }">
              <div v-if="row.clock_in_location" class="location-cell">
                <el-icon class="location-icon"><Location /></el-icon>
                <span>{{ row.clock_in_location }}</span>
              </div>
              <span v-else class="no-data">-</span>
            </template>
          </el-table-column>

          <el-table-column label="加班时长" width="100" align="center">
            <template #default="{ row }">
              <span v-if="row.overtime_hours > 0" class="overtime-text">
                {{ row.overtime_hours.toFixed(1) }}h
              </span>
              <span v-else class="no-data">-</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="100" align="center" fixed="right">
            <template #default="{ row }">
              <el-button
                v-if="isAbnormal(row.status)"
                type="warning"
                size="small"
                plain
                @click="handleAppeal(row)"
              >
                <el-icon><EditPen /></el-icon>
                异常上报
              </el-button>
              <span v-else class="no-action">-</span>
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-if="!loading && attendanceList.length === 0" description="暂无考勤记录" />
      </div>
    </el-card>

    <!-- 异常上报对话框 -->
    <el-dialog
      v-model="appealDialogVisible"
      title="考勤异常上报"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="appealForm" :rules="appealRules" ref="appealFormRef" label-width="100px">
        <el-form-item label="异常日期">
          <el-input :value="formatDate(currentAppealRecord?.date)" disabled />
        </el-form-item>

        <el-form-item label="当前状态">
          <el-tag :type="getStatusTagType(currentAppealRecord?.status)" effect="dark">
            {{ getStatusText(currentAppealRecord?.status) }}
          </el-tag>
        </el-form-item>

        <el-form-item label="签到时间" v-if="currentAppealRecord?.clock_in_time">
          <el-input :value="formatTime(currentAppealRecord.clock_in_time)" disabled />
        </el-form-item>

        <el-form-item label="签退时间" v-if="currentAppealRecord?.clock_out_time">
          <el-input :value="formatTime(currentAppealRecord.clock_out_time)" disabled />
        </el-form-item>

        <el-form-item label="异常说明" prop="reason">
          <el-input
            v-model="appealForm.reason"
            type="textarea"
            :rows="4"
            placeholder="请详细说明异常情况，如：实际已按时签到但系统误判、忘记打卡等"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="appealDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAppeal" :loading="submitting">
            提交上报
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
  DocumentChecked,
  Calendar,
  CircleCheck,
  Warning,
  CircleClose,
  Clock,
  Location,
  EditPen
} from '@element-plus/icons-vue'
import { getMyAttendance, getAttendanceStatistics } from '../../api/attendance'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()

// 数据状态
const loading = ref(false)
const submitting = ref(false)
const selectedMonth = ref('')
const attendanceList = ref([])
const statistics = ref({})

// 异常上报对话框
const appealDialogVisible = ref(false)
const currentAppealRecord = ref(null)
const appealFormRef = ref(null)
const appealForm = reactive({
  reason: ''
})

const appealRules = {
  reason: [
    { required: true, message: '请填写异常说明', trigger: 'blur' },
    { min: 5, message: '异常说明至少5个字符', trigger: 'blur' }
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
  loadData()
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const employeeId = userStore.userInfo?.employee

    if (!employeeId) {
      ElMessage.error('未关联员工档案，无法查询考勤记录')
      return
    }

    // 计算月份的开始和结束日期
    const [year, month] = selectedMonth.value.split('-')
    const startDate = `${year}-${month}-01`
    const endDate = new Date(year, month, 0).toISOString().split('T')[0]

    // 并行加载考勤记录和统计数据
    const [attendanceRes, statsRes] = await Promise.all([
      getMyAttendance({
        employee_id: employeeId,
        start_date: startDate,
        end_date: endDate
      }),
      getAttendanceStatistics({
        employee_id: employeeId,
        start_date: startDate,
        end_date: endDate
      })
    ])

    if (attendanceRes.code === 200) {
      attendanceList.value = attendanceRes.data || []
    } else {
      ElMessage.error(attendanceRes.message || '加载考勤记录失败')
    }

    if (statsRes.code === 200) {
      statistics.value = statsRes.data || {}
    }
  } catch (error) {
    console.error('加载考勤数据失败:', error)
    ElMessage.error('加载考勤数据失败')
  } finally {
    loading.value = false
  }
}

// 判断是否为异常记录
const isAbnormal = (status) => {
  return ['LATE', 'EARLY_LEAVE', 'MISSING', 'ABNORMAL'].includes(status)
}

// 获取表格行的类名
const getRowClassName = ({ row }) => {
  if (isAbnormal(row.status)) {
    return 'abnormal-row'
  }
  return ''
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    NORMAL: 'success',
    LATE: 'warning',
    EARLY_LEAVE: 'danger',
    MISSING: 'info',
    ABNORMAL: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    NORMAL: '正常',
    LATE: '迟到',
    EARLY_LEAVE: '早退',
    MISSING: '缺卡',
    ABNORMAL: '异常'
  }
  return textMap[status] || '未知'
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}年${month}月${day}日`
}

// 获取日期的日
const getDay = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return String(date.getDate()).padStart(2, '0')
}

// 获取日期的月
const getMonth = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  return months[date.getMonth()]
}

// 处理异常上报
const handleAppeal = (record) => {
  currentAppealRecord.value = record
  appealForm.reason = ''
  appealDialogVisible.value = true
}

// 提交异常上报
const submitAppeal = async () => {
  try {
    await appealFormRef.value.validate()

    submitting.value = true

    // TODO: 调用后端 API 提交申诉
    // 目前仅模拟提交成功
    await new Promise(resolve => setTimeout(resolve, 500))

    ElMessage.success('异常上报已提交，等待管理员审核')
    appealDialogVisible.value = false
  } catch (error) {
    if (error !== false) {
      console.error('提交异常上报失败:', error)
      ElMessage.error('提交失败，请重试')
    }
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  selectedMonth.value = getCurrentMonth()
  loadData()
})
</script>

<style scoped>
.attendance-view {
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

/* 统计卡片 */
.statistics-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.2);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.present-icon {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
}

.late-icon {
  background: linear-gradient(135deg, #FF9800, #FFB74D);
  color: white;
}

.missing-icon {
  background: linear-gradient(135deg, #9E9E9E, #BDBDBD);
  color: white;
}

.overtime-icon {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

/* 记录列表 */
.records-card {
  border-radius: 12px;
}

.records-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.records-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.records-table-container {
  min-height: 200px;
}

/* 异常行样式 */
.attendance-table :deep(.abnormal-row) {
  background-color: #fef5e7 !important;
}

.attendance-table :deep(.abnormal-row:hover) {
  background-color: #fdefd2 !important;
}

/* 日期单元格 */
.date-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.date-day {
  font-size: 24px;
  font-weight: 700;
  color: #FF6B35;
  line-height: 1.2;
}

.date-month {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

/* 时间单元格 */
.time-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #333;
}

.time-icon {
  color: #FF6B35;
  font-size: 14px;
}

/* 地点单元格 */
.location-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
}

.location-icon {
  color: #FF6B35;
  font-size: 14px;
}

/* 加班文本 */
.overtime-text {
  color: #FF6B35;
  font-weight: 600;
}

/* 无数据 */
.no-data {
  color: #c0c4cc;
}

.no-action {
  color: #c0c4cc;
  font-size: 14px;
}

/* 对话框 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .attendance-view {
    padding: 12px;
  }

  .page-title {
    font-size: 22px;
  }

  .statistics-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-value {
    font-size: 24px;
  }

  .month-selector {
    flex-direction: column;
    align-items: flex-start;
  }

  .month-picker {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .statistics-cards {
    grid-template-columns: 1fr;
  }
}
</style>
