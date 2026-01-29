<template>
  <div class="schedule-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon :size="24"><Calendar /></el-icon>
        我的排班
      </h2>
      <p class="page-desc">查看每月的排班安排和工作时间</p>
    </div>

    <el-card class="schedule-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-date-picker
              v-model="currentMonth"
              type="month"
              placeholder="选择月份"
              format="YYYY年MM月"
              value-format="YYYY-MM"
              :clearable="false"
              @change="handleMonthChange"
            />
            <el-button @click="handleToday">回到今天</el-button>
          </div>
          <div class="header-right">
            <el-radio-group v-model="viewType" size="small">
              <el-radio-button value="calendar">日历视图</el-radio-button>
              <el-radio-button value="list">列表视图</el-radio-button>
            </el-radio-group>
            <el-button :icon="Refresh" circle @click="loadData" />
          </div>
        </div>
      </template>

      <!-- 日历视图 -->
      <div v-if="viewType === 'calendar'" class="calendar-container" v-loading="loading">
        <el-calendar v-model="calendarDate">
          <template #date-cell="{ data }">
            <div class="date-cell-content" :class="{ 'is-today': isToday(data.day) }">
              <div class="day-number">{{ data.day.split('-').slice(2).join('') }}</div>
              
              <div v-if="getScheduleForDate(data.day)" class="schedule-info">
                <el-tag :type="getShiftTagType(getScheduleForDate(data.day).shift_name)" size="small" effect="dark">
                  {{ getScheduleForDate(data.day).shift_name }}
                </el-tag>
                <div class="time-range">{{ getScheduleForDate(data.day).shift_time }}</div>
              </div>
              <div v-else-if="isPast(data.day)" class="no-schedule">
                <!-- 过去的日期如果没有排班，不显示内容或者显示休息 -->
                <!-- <span class="rest-text">休息</span> -->
              </div>
            </div>
          </template>
        </el-calendar>
      </div>

      <!-- 列表视图 -->
      <div v-else class="list-container" v-loading="loading">
        <el-table :data="monthlySchedules" stripe style="width: 100%">
          <el-table-column prop="work_date" label="日期" width="180">
            <template #default="{ row }">
              <div class="date-col">
                <span class="date-text">{{ formatDate(row.work_date) }}</span>
                <el-tag v-if="isToday(row.work_date)" size="small" type="danger" effect="plain">今天</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="shift_name" label="班次" width="120">
            <template #default="{ row }">
              <el-tag :type="getShiftTagType(row.shift_name)">{{ row.shift_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="shift_time" label="工作时间" />
          <el-table-column label="状态" width="100">
             <template #default="{ row }">
               <span v-if="isPast(row.work_date)">已结束</span>
               <span v-else>未开始</span>
             </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="monthlySchedules.length === 0" description="本月暂无排班" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Calendar, Refresh } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getCalendarView } from '@/api/schedule'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const loading = ref(false)
const viewType = ref('calendar')
const currentMonth = ref(new Date().toISOString().slice(0, 7)) // YYYY-MM
const calendarDate = ref(new Date())
const schedulesMap = ref({}) // date -> schedule
const monthlySchedules = ref([])

// 监听日历日期变化，同步更新月份选择器
watch(calendarDate, (newDate) => {
  const newMonth = newDate.toISOString().slice(0, 7)
  if (newMonth !== currentMonth.value) {
    currentMonth.value = newMonth
    loadData()
  }
})

// 监听月份选择器变化，同步更新日历
const handleMonthChange = (val) => {
  calendarDate.value = new Date(val + '-01')
  // loadData will be triggered by watch(calendarDate) if month changed, 
  // but if we just set calendarDate, it might trigger. 
  // However, since handleMonthChange updates currentMonth first (v-model), 
  // the watcher might not trigger if currentMonth is already updated.
  // Actually loadData depends on currentMonth.
  loadData()
}

const handleToday = () => {
  const today = new Date()
  calendarDate.value = today
  currentMonth.value = today.toISOString().slice(0, 7)
  loadData()
}

// 加载数据
const loadData = async () => {
  const employeeId = userStore.userInfo?.employee || userStore.userInfo?.employee_id
  if (!employeeId) {
    ElMessage.warning('未关联员工档案，无法查看排班')
    return
  }

  loading.value = true
  try {
    // 2. 加载当月排班
    // 计算当月第一天和最后一天
    const year = parseInt(currentMonth.value.split('-')[0])
    const month = parseInt(currentMonth.value.split('-')[1])
    const startDate = new Date(year, month - 1, 1)
    const endDate = new Date(year, month, 0) // 下个月第0天即本月最后一天

    const startStr = formatDateToString(startDate)
    const endStr = formatDateToString(endDate)

    const res = await getCalendarView({
      employee_id: employeeId,
      start_date: startStr,
      end_date: endStr
    })
    
    if (res.code === 200) {
      const scheduleData = res.data.schedules || {}
      
      // 处理数据
      const newSchedulesMap = {}
      const newList = []
      
      // schedules 是一个对象，key 是日期，value 是排班数组
      Object.entries(scheduleData).forEach(([date, schedules]) => {
        // 对于员工个人视图，每天应该只有一个排班（或者取第一个）
        if (schedules && schedules.length > 0) {
          const item = schedules[0]
          const schedule = {
            id: item.id,
            work_date: item.work_date,
            shift_name: item.shift_name || '未知班次',
            shift_time: (item.start_time && item.end_time) ? `${item.start_time} - ${item.end_time}` : ''
          }
          newSchedulesMap[date] = schedule
          newList.push(schedule)
        }
      })
      
      schedulesMap.value = newSchedulesMap
      monthlySchedules.value = newList.sort((a, b) => new Date(a.work_date) - new Date(b.work_date))
    }
  } catch (error) {
    console.error('加载排班失败:', error)
    ElMessage.error('加载排班数据失败')
  } finally {
    loading.value = false
  }
}

// 获取指定日期的排班
const getScheduleForDate = (dateStr) => {
  return schedulesMap.value[dateStr]
}

// 判断是否是今天
const isToday = (dateStr) => {
  const today = new Date()
  const d = new Date(dateStr)
  return d.getDate() === today.getDate() && 
         d.getMonth() === today.getMonth() && 
         d.getFullYear() === today.getFullYear()
}

// 判断是否是过去
const isPast = (dateStr) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return new Date(dateStr) < today
}

// 格式化日期 YYYY-MM-DD -> YYYY-MM-DD (Date object)
const formatDateToString = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 格式化日期显示
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return `${dateStr} ${weekdays[date.getDay()]}`
}

// 班次标签颜色
const getShiftTagType = (shiftName) => {
  const map = {
    '早班': 'success',
    '中班': 'warning',
    '晚班': 'danger',
    '全天': 'primary',
    '休息': 'info'
  }
  return map[shiftName] || ''
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.schedule-view {
  max-width: 1200px;
  margin: 0 auto;
}

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

.schedule-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  gap: 12px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 日历样式自定义 */
.calendar-container {
  min-height: 600px;
}

:deep(.el-calendar-table .el-calendar-day) {
  height: 100px;
  padding: 8px;
}

:deep(.el-calendar-table td.is-selected .el-calendar-day) {
  background-color: #FFF8F0;
}

:deep(.el-calendar-table td.is-today .el-calendar-day) {
  background-color: #fffbf6;
}

.date-cell-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.day-number {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.is-today .day-number {
  color: #FF6B35;
  font-weight: bold;
}

.schedule-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-start;
}

.time-range {
  font-size: 12px;
  color: #999;
}

.date-col {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-text {
  font-weight: 500;
}
</style>
