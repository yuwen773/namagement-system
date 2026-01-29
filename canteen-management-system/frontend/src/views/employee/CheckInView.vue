<template>
  <div class="checkin-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>签到签退</h2>
      <p>点击下方按钮进行签到或签退操作</p>
    </div>

    <!-- 主要内容区 -->
    <div class="content-section">
      <!-- 左侧：签到签退卡片 -->
      <div class="left-section">
        <!-- 当前时间卡片 -->
        <div class="time-card">
          <div class="time-display">
            <div class="current-time">{{ currentTime }}</div>
            <div class="current-date">{{ currentDate }}</div>
          </div>
          <div class="time-icon">
            <el-icon :size="48"><Clock /></el-icon>
          </div>
        </div>

        <!-- 签到签退按钮 -->
        <div class="action-card">
          <div class="action-header">
            <h3>{{ isCompleted ? '今日考勤已完成' : (canClockIn ? '签到' : '签退') }}</h3>
            <el-tag :type="actionStatus.type" size="large">{{ actionStatus.text }}</el-tag>
          </div>

          <div class="location-info" v-if="location">
            <el-icon><Location /></el-icon>
            <span>{{ location }}</span>
          </div>

          <div class="action-button-wrapper">
            <button
              class="action-button"
              :class="{ 'clock-out': canClockOut, 'completed': isCompleted }"
              @click="handleClockAction"
              :disabled="loading || isCompleted"
            >
              <span v-if="!loading">
                {{ isCompleted ? '今日已结束' : (canClockIn ? '立即签到' : '立即签退') }}
              </span>
              <span v-else>
                <el-icon class="is-loading"><Loading /></el-icon>
                处理中...
              </span>
            </button>
          </div>

          <!-- 今日记录 -->
          <div class="today-record" v-if="todayRecord">
            <div class="record-item" v-if="todayRecord.clock_in_time">
              <span class="record-label">签到时间</span>
              <span class="record-value success">{{ formatTime(todayRecord.clock_in_time) }}</span>
            </div>
            <div class="record-item" v-if="todayRecord.clock_out_time">
              <span class="record-label">签退时间</span>
              <span class="record-value success">{{ formatTime(todayRecord.clock_out_time) }}</span>
            </div>
            <div class="record-item">
              <span class="record-label">考勤状态</span>
              <el-tag :type="getStatusTagType(todayRecord.status)">
                {{ getStatusText(todayRecord.status) }}
              </el-tag>
            </div>
            <div class="record-item" v-if="todayRecord.overtime_hours > 0">
              <span class="record-label">加班时长</span>
              <span class="record-value highlight">{{ todayRecord.overtime_hours }} 小时</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：日历视图 -->
      <div class="right-section">
        <div class="calendar-card">
          <div class="calendar-header">
            <h3>本月打卡记录</h3>
            <el-button-group size="small">
              <el-button @click="changeMonth(-1)">
                <el-icon><ArrowLeft /></el-icon>
              </el-button>
              <el-button disabled>{{ currentYear }}年{{ currentMonth }}月</el-button>
              <el-button @click="changeMonth(1)">
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </el-button-group>
          </div>

          <!-- 日历 -->
          <div class="calendar-wrapper">
            <el-calendar v-model="calendarDate">
              <template #date-cell="{ data }">
                <div class="calendar-cell">
                  <span class="date-number">{{ data.day.split('-')[2] }}</span>
                  <div class="attendance-indicators" v-if="getAttendanceStatus(data.day)">
                    <div
                      class="indicator"
                      :class="getAttendanceStatus(data.day)"
                      :title="getStatusText(getAttendanceStatus(data.day))"
                    ></div>
                  </div>
                </div>
              </template>
            </el-calendar>
          </div>

          <!-- 图例说明 -->
          <div class="calendar-legend">
            <div class="legend-item">
              <div class="legend-dot normal"></div>
              <span>正常</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot late"></div>
              <span>迟到</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot early-leave"></div>
              <span>早退</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot missing"></div>
              <span>缺卡</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot abnormal"></div>
              <span>异常</span>
            </div>
          </div>
        </div>

        <!-- 本月统计 -->
        <div class="stats-card">
          <h3>本月统计</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ monthStats.present_days || 0 }}</div>
              <div class="stat-label">出勤天数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value warning">{{ monthStats.late_count || 0 }}</div>
              <div class="stat-label">迟到次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value danger">{{ monthStats.missing_count || 0 }}</div>
              <div class="stat-label">缺卡次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value info">{{ monthStats.overtime_hours?.toFixed(1) || '0.0' }}</div>
              <div class="stat-label">加班时长</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { clockIn, clockOut, getMyAttendance, getAttendanceStatistics } from '../../api/attendance'
import { ElMessage } from 'element-plus'
import {
  Clock,
  Location,
  Loading,
  ArrowLeft,
  ArrowRight
} from '@element-plus/icons-vue'

const userStore = useUserStore()

// 状态数据
const currentTime = ref('')
const currentDate = ref('')
const location = ref('')
const loading = ref(false)
const todayRecord = ref(null)
const calendarDate = ref(new Date())
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const attendanceMap = ref({})
const monthStats = ref({})

let timeTimer = null

// 获取员工ID
const employeeId = computed(() => userStore.userInfo?.employee_id || userStore.userInfo?.employee)

// 是否可以签到（今日未签到或已签退）
const canClockIn = computed(() => {
  if (!todayRecord.value) return true
  // 如果已签到且未签退，则不能再签到（显示签退）
  if (todayRecord.value.clock_in_time && !todayRecord.value.clock_out_time) return false
  // 如果已签到且已签退，则不能再签到（显示已完成）
  if (todayRecord.value.clock_in_time && todayRecord.value.clock_out_time) return false
  return true
})

// 是否可以签退
const canClockOut = computed(() => {
  if (!todayRecord.value) return false
  // 只有已签到且未签退时，才可以签退
  return !!todayRecord.value.clock_in_time && !todayRecord.value.clock_out_time
})

// 是否已完成今日考勤
const isCompleted = computed(() => {
  if (!todayRecord.value) return false
  return !!todayRecord.value.clock_in_time && !!todayRecord.value.clock_out_time
})

// 操作状态
const actionStatus = computed(() => {
  if (!todayRecord.value) {
    return { type: 'info', text: '未签到' }
  }
  if (!todayRecord.value.clock_in_time) {
    return { type: 'warning', text: '请签到' }
  }
  if (todayRecord.value.clock_out_time) {
    return { type: 'success', text: '已完成' }
  }
  return { type: 'primary', text: '工作中' }
})

// 更新当前时间
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toTimeString().substring(0, 8)
  const weekDays = ['日', '一', '二', '三', '四', '五', '六']
  currentDate.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 星期${weekDays[now.getDay()]}`
}

// 获取位置
const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        location.value = `纬度: ${position.coords.latitude.toFixed(4)}, 经度: ${position.coords.longitude.toFixed(4)}`
      },
      () => {
        location.value = '无法获取位置信息'
      }
    )
  } else {
    location.value = '浏览器不支持定位'
  }
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  return date.toTimeString().substring(0, 5)
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    'NORMAL': 'success',
    'LATE': 'warning',
    'EARLY_LEAVE': 'danger',
    'MISSING': 'info',
    'ABNORMAL': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    'NORMAL': '正常',
    'LATE': '迟到',
    'EARLY_LEAVE': '早退',
    'MISSING': '缺卡',
    'ABNORMAL': '异常'
  }
  return textMap[status] || '未知'
}

// 处理签到/签退操作
const handleClockAction = async () => {
  if (!employeeId.value) {
    ElMessage.warning('未关联员工档案，请联系管理员')
    return
  }

  loading.value = true
  try {
    if (canClockIn.value) {
      // 签到
      const res = await clockIn({
        employee_id: employeeId.value,
        clock_in_location: location.value || '食堂'
      })
      if (res.code === 200) {
        ElMessage.success('签到成功！')
        await loadTodayRecord()
      }
    } else {
      // 签退
      const res = await clockOut({
        employee_id: employeeId.value,
        clock_out_location: location.value || '食堂'
      })
      if (res.code === 200) {
        ElMessage.success('签退成功！')
        await loadTodayRecord()
      }
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '操作失败，请重试')
  } finally {
    loading.value = false
  }
}

// 加载今日考勤记录
const loadTodayRecord = async () => {
  if (!employeeId.value) return

  try {
    const today = new Date()
    const startDate = formatDate(today)
    const endDate = formatDate(today)

    const res = await getMyAttendance({
      employee_id: employeeId.value,
      start_date: startDate,
      end_date: endDate
    })

    if (res.code === 200) {
      const records = res.data.results || res.data || []
      todayRecord.value = records.length > 0 ? records[0] : null
    }
  } catch (error) {
    console.error('加载今日考勤记录失败:', error)
  }
}

// 格式化日期
const formatDate = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 加载月度考勤数据
const loadMonthAttendance = async () => {
  if (!employeeId.value) return

  try {
    const startDate = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-01`
    const endDate = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-31`

    const res = await getMyAttendance({
      employee_id: employeeId.value,
      start_date: startDate,
      end_date: endDate
    })

    if (res.code === 200) {
      const records = res.data.results || res.data || []
      attendanceMap.value = {}
      records.forEach(record => {
        const date = new Date(record.clock_in_time || record.created_at)
        const dateStr = formatDate(date)
        attendanceMap.value[dateStr] = record.status
      })
    }

    // 同时加载统计
    await loadMonthStatistics()
  } catch (error) {
    console.error('加载月度考勤数据失败:', error)
  }
}

// 加载月度统计
const loadMonthStatistics = async () => {
  if (!employeeId.value) return

  try {
    const startDate = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-01`
    const endDate = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-31`

    const res = await getAttendanceStatistics({
      start_date: startDate,
      end_date: endDate,
      employee_id: employeeId.value
    })

    if (res.code === 200) {
      monthStats.value = res.data || {}
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 获取指定日期的考勤状态
const getAttendanceStatus = (dateStr) => {
  return attendanceMap.value[dateStr] || null
}

// 切换月份
const changeMonth = (delta) => {
  const newDate = new Date(currentYear.value, currentMonth.value - 1 + delta, 1)
  currentYear.value = newDate.getFullYear()
  currentMonth.value = newDate.getMonth() + 1
  calendarDate.value = newDate
  loadMonthAttendance()
}

// 初始化
onMounted(() => {
  updateCurrentTime()
  timeTimer = setInterval(updateCurrentTime, 1000)
  getLocation()
  loadTodayRecord()
  loadMonthAttendance()
})

onUnmounted(() => {
  if (timeTimer) {
    clearInterval(timeTimer)
  }
})
</script>

<style scoped>
.checkin-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.page-header p {
  font-size: 14px;
  color: #909399;
}

/* 内容区 */
.content-section {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
}

/* 左侧区域 */
.left-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 时间卡片 */
.time-card {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  border-radius: 16px;
  padding: 32px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
}

.time-display .current-time {
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 8px;
  font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
}

.time-display .current-date {
  font-size: 14px;
  opacity: 0.9;
}

.time-icon {
  opacity: 0.8;
}

/* 操作卡片 */
.action-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.action-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.location-info .el-icon {
  color: #FF6B35;
}

.action-button-wrapper {
  margin-bottom: 24px;
}

.action-button {
  width: 100%;
  height: 80px;
  border: none;
  border-radius: 16px;
  font-size: 24px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5);
}

.action-button:active:not(:disabled) {
  transform: translateY(0);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-button.clock-out {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.4);
}

.action-button.clock-out:hover:not(:disabled) {
  box-shadow: 0 6px 20px rgba(255, 107, 53, 0.5);
}

.action-button.completed {
  background: #909399;
  box-shadow: none;
  cursor: not-allowed;
}

/* 今日记录 */
.today-record {
  border-top: 1px solid #f0f0f0;
  padding-top: 16px;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.record-label {
  font-size: 14px;
  color: #606266;
}

.record-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.record-value.success {
  color: #67C23A;
}

.record-value.highlight {
  color: #FF6B35;
}

/* 右侧区域 */
.right-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 日历卡片 */
.calendar-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.calendar-wrapper {
  margin-bottom: 20px;
}

.calendar-wrapper :deep(.el-calendar) {
  --el-calendar-cell-width: 60px;
}

.calendar-wrapper :deep(.el-calendar-table .el-calendar-day) {
  height: 60px;
  padding: 4px;
}

.calendar-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.date-number {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.attendance-indicators {
  display: flex;
  gap: 4px;
  margin-top: 4px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.indicator.normal {
  background-color: #67C23A;
}

.indicator.late {
  background-color: #E6A23C;
}

.indicator.early-leave {
  background-color: #F56C6C;
}

.indicator.missing {
  background-color: #909399;
}

.indicator.abnormal {
  background-color: #F56C6C;
}

/* 图例说明 */
.calendar-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-dot.normal {
  background-color: #67C23A;
}

.legend-dot.late {
  background-color: #E6A23C;
}

.legend-dot.early-leave {
  background-color: #F56C6C;
}

.legend-dot.missing {
  background-color: #909399;
}

.legend-dot.abnormal {
  background-color: #F56C6C;
}

/* 统计卡片 */
.stats-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.stats-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 12px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.stat-value.warning {
  color: #E6A23C;
}

.stat-value.danger {
  color: #F56C6C;
}

.stat-value.info {
  color: #409EFF;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .content-section {
    grid-template-columns: 1fr;
  }

  .left-section {
    max-width: 500px;
    margin: 0 auto;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header h2 {
    font-size: 20px;
  }

  .time-display .current-time {
    font-size: 36px;
  }

  .action-button {
    height: 60px;
    font-size: 20px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .calendar-legend {
    justify-content: center;
  }
}
</style>
