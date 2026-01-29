<template>
  <div class="employee-home">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-card">
        <div class="welcome-content">
          <div class="greeting">
            <h2>{{ greetingText }}，{{ employeeName }}！</h2>
            <p>{{ currentDate }}</p>
          </div>
          <div class="position-info">
            <el-tag type="warning" size="large">{{ positionText }}</el-tag>
          </div>
        </div>
        <div class="welcome-decoration">
          <svg class="food-icon" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path fill="currentColor" d="M128 256h768a32 32 0 0 1 32 32v640a32 32 0 0 1-32 32H128a32 32 0 0 1-32-32V288a32 32 0 0 1 32-32z m0-64a96 96 0 0 0-96 96v640a96 96 0 0 0 96 96h768a96 96 0 0 0 96-96V288a96 96 0 0 0-96-96H128z"/>
            <path fill="currentColor" d="M416 512h192a32 32 0 0 1 32 32v192a32 32 0 0 1-32 32H416a32 32 0 0 1-32-32V544a32 32 0 0 1 32-32z m32 64v128h128V576H448z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 排班卡片区域 -->
    <div class="schedule-section">
      <h3 class="section-title">
        <el-icon><Calendar /></el-icon>
        我的排班
      </h3>
      <div class="schedule-cards">
        <!-- 今日排班 -->
        <div class="schedule-card today-card" :class="{ 'rest-day': !todaySchedule }">
          <div class="card-header">
            <span class="card-day">今日排班</span>
            <el-tag :type="todaySchedule ? 'success' : 'info'" size="small">
              {{ todaySchedule ? '上班' : '休息' }}
            </el-tag>
          </div>
          <div class="card-body">
            <template v-if="todaySchedule">
              <div class="shift-name">{{ todaySchedule.shift_name }}</div>
              <div class="shift-time">
                <el-icon><Clock /></el-icon>
                {{ todaySchedule.start_time }} - {{ todaySchedule.end_time }}
              </div>
            </template>
            <template v-else>
              <div class="rest-text">
                <el-icon :size="48"><Sunny /></el-icon>
                <p>今日休息</p>
              </div>
            </template>
          </div>
        </div>

        <!-- 明日排班 -->
        <div class="schedule-card tomorrow-card" :class="{ 'rest-day': !tomorrowSchedule }">
          <div class="card-header">
            <span class="card-day">明日排班</span>
            <el-tag :type="tomorrowSchedule ? 'warning' : 'info'" size="small">
              {{ tomorrowSchedule ? '上班' : '休息' }}
            </el-tag>
          </div>
          <div class="card-body">
            <template v-if="tomorrowSchedule">
              <div class="shift-name">{{ tomorrowSchedule.shift_name }}</div>
              <div class="shift-time">
                <el-icon><Clock /></el-icon>
                {{ tomorrowSchedule.start_time }} - {{ tomorrowSchedule.end_time }}
              </div>
            </template>
            <template v-else>
              <div class="rest-text">
                <el-icon :size="48"><Moon /></el-icon>
                <p>明日休息</p>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷入口区域 -->
    <div class="quick-access-section">
      <h3 class="section-title">
        <el-icon><Grid /></el-icon>
        快捷入口
      </h3>
      <div class="quick-access-grid">
        <div class="quick-button" @click="handleQuickAccess('checkin')">
          <div class="button-icon checkin-icon">
            <el-icon :size="32"><CircleCheck /></el-icon>
          </div>
          <span>签到签退</span>
        </div>
        <div class="quick-button" @click="handleQuickAccess('leave')">
          <div class="button-icon leave-icon">
            <el-icon :size="32"><DocumentAdd /></el-icon>
          </div>
          <span>请假申请</span>
        </div>
        <div class="quick-button" @click="handleQuickAccess('swap')">
          <div class="button-icon swap-icon">
            <el-icon :size="32"><Switch /></el-icon>
          </div>
          <span>调班申请</span>
        </div>
        <div class="quick-button" @click="handleQuickAccess('salary')">
          <div class="button-icon salary-icon">
            <el-icon :size="32"><Wallet /></el-icon>
          </div>
          <span>工资条</span>
        </div>
      </div>
    </div>

    <!-- 通知公告区域 -->
    <div class="notification-section" v-if="notifications.length > 0">
      <h3 class="section-title">
        <el-icon><Bell /></el-icon>
        通知公告
        <el-badge :value="unreadCount" class="notification-badge" />
      </h3>
      <div class="notification-list">
        <div
          v-for="item in notifications"
          :key="item.id"
          class="notification-item"
          :class="{ 'unread': !item.read }"
          @click="handleNotificationClick(item)"
        >
          <div class="notification-icon">
            <el-icon :size="24">
              <component :is="getNotificationIcon(item.type)" />
            </el-icon>
          </div>
          <div class="notification-content">
            <div class="notification-title">{{ item.title }}</div>
            <div class="notification-desc">{{ item.description }}</div>
            <div class="notification-time">{{ item.time }}</div>
          </div>
          <div class="notification-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { getEmployeeSchedules } from '../../api/schedule'
import { ElMessage } from 'element-plus'
import {
  Calendar,
  Clock,
  Sunny,
  Moon,
  Grid,
  CircleCheck,
  DocumentAdd,
  Switch,
  Wallet,
  Bell,
  ArrowRight,
  Select,
  SuccessFilled,
  Warning
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 状态数据
const todaySchedule = ref(null)
const tomorrowSchedule = ref(null)
const employeeName = ref('')
const positionText = ref('')
const notifications = ref([])

// 获取员工ID
const employeeId = computed(() => userStore.userInfo?.employee)

// 当前日期
const currentDate = computed(() => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const weekDay = weekDays[now.getDay()]
  return `${year}年${month}月${day}日 ${weekDay}`
})

// 问候语
const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  if (hour < 22) return '晚上好'
  return '夜深了'
})

// 未读通知数量
const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

// 获取通知图标
const getNotificationIcon = (type) => {
  const iconMap = {
    'leave_approved': SuccessFilled,
    'leave_rejected': Warning,
    'swap_approved': SuccessFilled,
    'swap_rejected': Warning,
    'appeal_result': Select
  }
  return iconMap[type] || Bell
}

// 加载排班数据
const loadSchedules = async () => {
  if (!employeeId.value) {
    // 如果没有关联员工档案，显示提示
    ElMessage.warning('未关联员工档案，请联系管理员')
    return
  }

  try {
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    const formatDate = (date) => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }

    const startDate = formatDate(today)
    const endDate = formatDate(tomorrow)

    const res = await getEmployeeSchedules(employeeId.value, startDate, endDate)
    if (res.code === 200) {
      const schedules = res.data.results || res.data || []

      // 今日排班
      const todayStr = formatDate(today)
      const todayData = schedules.find(s => s.work_date === todayStr)
      if (todayData) {
        todaySchedule.value = {
          shift_name: todayData.shift_name,
          start_time: todayData.start_time?.substring(0, 5),
          end_time: todayData.end_time?.substring(0, 5)
        }
      }

      // 明日排班
      const tomorrowStr = formatDate(tomorrow)
      const tomorrowData = schedules.find(s => s.work_date === tomorrowStr)
      if (tomorrowData) {
        tomorrowSchedule.value = {
          shift_name: tomorrowData.shift_name,
          start_time: tomorrowData.start_time?.substring(0, 5),
          end_time: tomorrowData.end_time?.substring(0, 5)
        }
      }
    }
  } catch (error) {
    console.error('加载排班数据失败:', error)
  }
}

// 加载员工信息
const loadEmployeeInfo = async () => {
  // 从用户信息中获取员工姓名和岗位
  if (userStore.userInfo?.employee_name) {
    employeeName.value = userStore.userInfo.employee_name
  } else {
    employeeName.value = userStore.userInfo?.username || '员工'
  }

  // 岗位文本映射
  const positionMap = {
    'CHEF': '厨师',
    'PASTRY': '面点',
    'PREP': '切配',
    'CLEANER': '保洁',
    'SERVER': '服务员',
    'MANAGER': '经理'
  }
  positionText.value = positionMap[userStore.userInfo?.employee_position] || '员工'
}

// 加载通知数据
const loadNotifications = () => {
  // 模拟通知数据（实际应从后端API获取）
  notifications.value = [
    {
      id: 1,
      type: 'leave_approved',
      title: '请假申请已通过',
      description: '您2024-01-20的请假申请已通过审核',
      time: '2小时前',
      read: false
    },
    {
      id: 2,
      type: 'appeal_result',
      title: '申诉处理结果',
      description: '您提交的考勤申诉已处理完成',
      time: '昨天',
      read: true
    }
  ]
}

// 处理快捷入口点击
const handleQuickAccess = (type) => {
  const routeMap = {
    'checkin': '/employee/checkin',
    'leave': '/employee/leave',
    'swap': '/employee/swap',
    'salary': '/employee/salary'
  }

  const route = routeMap[type]
  if (route) {
    router.push(route)
  } else {
    ElMessage.info('功能开发中，敬请期待')
  }
}

// 处理通知点击
const handleNotificationClick = (item) => {
  item.read = true
  // 根据通知类型跳转到相应页面
  if (item.type.includes('leave')) {
    router.push('/employee/leave')
  } else if (item.type.includes('swap')) {
    router.push('/employee/swap')
  } else if (item.type.includes('appeal')) {
    router.push('/employee/salary')
  }
}

onMounted(() => {
  loadSchedules()
  loadEmployeeInfo()
  loadNotifications()
})
</script>

<style scoped>
.employee-home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 欢迎区域 */
.welcome-section {
  margin-bottom: 24px;
}

.welcome-card {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  border-radius: 16px;
  padding: 32px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
  position: relative;
  overflow: hidden;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.welcome-content {
  flex: 1;
  z-index: 1;
}

.greeting h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.greeting p {
  font-size: 16px;
  opacity: 0.9;
}

.position-info {
  margin-top: 16px;
}

.welcome-decoration {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.food-icon {
  width: 100%;
  height: 100%;
  opacity: 0.3;
}

/* 排班区域 */
.schedule-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.schedule-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.schedule-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid #FF6B35;
}

.schedule-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.schedule-card.rest-day {
  border-left-color: #909399;
  background: linear-gradient(135deg, #f5f7fa, #ffffff);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-day {
  font-size: 16px;
  font-weight: 600;
  color: #606266;
}

.card-body {
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.shift-name {
  font-size: 20px;
  font-weight: 600;
  color: #FF6B35;
  margin-bottom: 8px;
}

.shift-time {
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.rest-text {
  text-align: center;
  color: #909399;
}

.rest-text p {
  margin-top: 8px;
  font-size: 14px;
}

/* 快捷入口区域 */
.quick-access-section {
  margin-bottom: 32px;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.quick-button {
  background: white;
  border-radius: 12px;
  padding: 24px 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.quick-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.2);
}

.button-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.checkin-icon {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
}

.leave-icon {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
}

.swap-icon {
  background: linear-gradient(135deg, #F7C52D, #FDD835);
}

.salary-icon {
  background: linear-gradient(135deg, #42A5F5, #64B5F6);
}

.quick-button span {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

/* 通知区域 */
.notification-section {
  margin-bottom: 32px;
}

.notification-badge {
  margin-left: 8px;
}

.notification-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.notification-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid #f0f0f0;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item:hover {
  background-color: #FFF8F0;
}

.notification-item.unread {
  background-color: #FFF8F0;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.notification-desc {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-time {
  font-size: 12px;
  color: #C0C4CC;
}

.notification-arrow {
  color: #C0C4CC;
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .employee-home {
    padding: 16px;
  }

  .welcome-card {
    padding: 24px;
  }

  .greeting h2 {
    font-size: 22px;
  }

  .schedule-cards {
    grid-template-columns: 1fr;
  }

  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
