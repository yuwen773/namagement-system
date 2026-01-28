<template>
  <div class="admin-dashboard">
    <!-- 顶部导航栏 -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">🍳</div>
          <h1 class="logo-title">食堂管理系统</h1>
        </div>
        <div class="header-actions">
          <div class="date-display">{{ currentDate }}</div>
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            <span class="user-role">管理员</span>
          </div>
          <el-button type="danger" plain @click="handleLogout" class="logout-btn">
            <span class="logout-icon">🚪</span>
            退出登录
          </el-button>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="dashboard-main">
      <!-- 欢迎语 -->
      <div class="welcome-section">
        <h2 class="welcome-title">
          <span class="wave-icon">👋</span>
          欢迎回来，{{ userName }}！
        </h2>
        <p class="welcome-subtitle">今天是 {{ currentDateDisplay }}，祝您工作愉快！</p>
      </div>

      <!-- 快捷入口区域 -->
      <section class="quick-access-section">
        <h3 class="section-title">
          <span class="title-icon">⚡</span>
          快捷入口
        </h3>
        <div class="quick-access-grid">
          <div
            v-for="item in quickAccessItems"
            :key="item.name"
            class="quick-access-card"
            @click="handleQuickAccess(item.route)"
          >
            <div class="card-icon">{{ item.icon }}</div>
            <div class="card-content">
              <h4 class="card-title">{{ item.name }}</h4>
              <p class="card-description">{{ item.description }}</p>
            </div>
            <div class="card-arrow">→</div>
          </div>
        </div>
      </section>

      <!-- 今日概览区域 -->
      <section class="overview-section">
        <h3 class="section-title">
          <span class="title-icon">📊</span>
          今日概览
        </h3>
        <div class="overview-cards" v-loading="overviewLoading">
          <div class="overview-card attendance-card">
            <div class="card-header">
              <div class="card-icon-small">📋</div>
              <span class="card-label">出勤情况</span>
            </div>
            <div class="card-stats">
              <div class="stat-item">
                <span class="stat-value">{{ overviewData.expected_attendance || 0 }}</span>
                <span class="stat-label">应到</span>
              </div>
              <div class="stat-divider">/</div>
              <div class="stat-item">
                <span class="stat-value stat-highlight">{{ overviewData.actual_attendance || 0 }}</span>
                <span class="stat-label">实到</span>
              </div>
            </div>
          </div>

          <div class="overview-card leave-card">
            <div class="card-header">
              <div class="card-icon-small">🏖️</div>
              <span class="card-label">今日请假</span>
            </div>
            <div class="card-stats">
              <div class="stat-item-full">
                <span class="stat-value-large">{{ overviewData.today_leaves || 0 }}</span>
                <span class="stat-label">人</span>
              </div>
            </div>
          </div>

          <div class="overview-card abnormal-card">
            <div class="card-header">
              <div class="card-icon-small">⚠️</div>
              <span class="card-label">今日异常</span>
            </div>
            <div class="card-stats">
              <div class="stat-item-full">
                <span class="stat-value-large stat-warning">{{ overviewData.today_abnormal || 0 }}</span>
                <span class="stat-label">条</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 待办事项区域 -->
      <section class="todo-section">
        <h3 class="section-title">
          <span class="title-icon">📝</span>
          待办事项
        </h3>
        <div class="todo-list" v-loading="overviewLoading">
          <div v-if="todoItems.length === 0" class="empty-state">
            <div class="empty-icon">🎉</div>
            <p class="empty-text">暂无待办事项</p>
          </div>
          <div
            v-for="item in todoItems"
            :key="item.id"
            class="todo-item"
            @click="handleTodoClick(item)"
          >
            <div class="todo-icon" :class="`todo-${item.type}`">
              {{ getTodoIcon(item.type) }}
            </div>
            <div class="todo-content">
              <div class="todo-title">{{ item.title }}</div>
              <div class="todo-meta">
                <span class="todo-type">{{ item.typeName }}</span>
                <span class="todo-time">{{ item.time }}</span>
              </div>
            </div>
            <div class="todo-arrow">→</div>
          </div>
        </div>
      </section>

      <!-- 本月统计区域 -->
      <section class="monthly-section">
        <h3 class="section-title">
          <span class="title-icon">📈</span>
          本月统计
        </h3>
        <div class="monthly-cards" v-loading="overviewLoading">
          <div class="monthly-card">
            <div class="monthly-icon">👥</div>
            <div class="monthly-content">
              <div class="monthly-value">{{ overviewData.total_employees || 0 }}</div>
              <div class="monthly-label">员工总数</div>
            </div>
          </div>
          <div class="monthly-card">
            <div class="monthly-icon">⏰</div>
            <div class="monthly-content">
              <div class="monthly-value">{{ overviewData.monthly_late || 0 }}</div>
              <div class="monthly-label">迟到次数</div>
            </div>
          </div>
          <div class="monthly-card">
            <div class="monthly-icon">💰</div>
            <div class="monthly-content">
              <div class="monthly-value">{{ formatSalary(overviewData.monthly_salary) }}</div>
              <div class="monthly-label">薪资支出</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { getOverviewStatistics } from '../../api/analytics'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

// 状态数据
const overviewLoading = ref(false)
const overviewData = ref({})
const todoItems = ref([])

// 计算属性
const userName = computed(() => userStore.userInfo?.username || '管理员')

const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
})

const currentDateDisplay = computed(() => {
  const now = new Date()
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const date = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
  return `${date} ${weekdays[now.getDay()]}`
})

// 快捷入口配置
const quickAccessItems = [
  {
    name: '人员新增',
    description: '添加新员工档案',
    icon: '👤',
    route: '/admin/employees'
  },
  {
    name: '排班制定',
    description: '安排员工班次',
    icon: '📅',
    route: '/admin/schedules'
  },
  {
    name: '考勤异常',
    description: '处理考勤异常',
    icon: '⚠️',
    route: '/admin/attendance'
  },
  {
    name: '薪资生成',
    description: '生成月度薪资',
    icon: '💰',
    route: '/admin/salaries'
  }
]

// 获取待办图标
const getTodoIcon = (type) => {
  const iconMap = {
    leave: '🏖️',
    shift_swap: '🔄',
    appeal: '📝'
  }
  return iconMap[type] || '📋'
}

// 格式化薪资
const formatSalary = (salary) => {
  if (!salary) return '¥0'
  return `¥${Number(salary).toLocaleString()}`
}

// 加载总览数据
const loadOverviewData = async () => {
  overviewLoading.value = true
  try {
    const response = await getOverviewStatistics()
    if (response.code === 200) {
      overviewData.value = response.data

      // 构建待办事项列表
      const todos = []
      // 待审批请假
      if (response.data.pending_leaves && response.data.pending_leaves.length > 0) {
        response.data.pending_leaves.forEach(leave => {
          todos.push({
            id: `leave-${leave.id}`,
            type: 'leave',
            typeName: '请假审批',
            title: `${leave.employee_name} 的请假申请`,
            time: formatDate(leave.created_at),
            data: leave
          })
        })
      }
      // 待审批调班
      if (response.data.pending_shift_swaps && response.data.pending_shift_swaps.length > 0) {
        response.data.pending_shift_swaps.forEach(swap => {
          todos.push({
            id: `swap-${swap.id}`,
            type: 'shift_swap',
            typeName: '调班审批',
            title: `${swap.requester_name} 的调班申请`,
            time: formatDate(swap.created_at),
            data: swap
          })
        })
      }
      // 待审批申诉
      if (response.data.pending_appeals && response.data.pending_appeals.length > 0) {
        response.data.pending_appeals.forEach(appeal => {
          todos.push({
            id: `appeal-${appeal.id}`,
            type: 'appeal',
            typeName: '申诉处理',
            title: `${appeal.employee_name} 的${appeal.type === 'SALARY' ? '薪资' : '考勤'}申诉`,
            time: formatDate(appeal.created_at),
            data: appeal
          })
        })
      }
      // 待发布薪资
      if (response.data.draft_salaries > 0) {
        todos.push({
          id: 'draft-salaries',
          type: 'salary',
          typeName: '薪资发布',
          title: `有 ${response.data.draft_salaries} 份薪资待发布`,
          time: '立即处理',
          data: { count: response.data.draft_salaries }
        })
      }

      todoItems.value = todos
    }
  } catch (error) {
    console.error('加载总览数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    overviewLoading.value = false
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

// 快捷入口点击处理
const handleQuickAccess = (route) => {
  if (route === '/admin/employees' || route === '/admin/schedules' || route === '/admin/attendance') {
    router.push(route)
  } else {
    // 其他路由功能在阶段四其他步骤实现
    ElMessage.info(`${route} 页面即将在后续步骤中实现`)
  }
}

// 待办事项点击处理
const handleTodoClick = (item) => {
  // 路由功能在阶段四其他步骤实现
  ElMessage.info(`${item.typeName} 详情页面即将在后续步骤中实现`)
}

// 退出登录
const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

// 组件挂载时加载数据
onMounted(() => {
  loadOverviewData()
})
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #FFF8F0 0%, #FFF0E0 100%);
}

/* 顶部导航栏 */
.dashboard-header {
  background: linear-gradient(90deg, #FF6B35 0%, #FF8C42 50%, #F7C52D 100%);
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 32px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

.logo-title {
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  letter-spacing: 1px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.date-display {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.logout-btn {
  border-color: rgba(255, 255, 255, 0.5);
  color: #ffffff;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logout-icon {
  margin-right: 4px;
}

/* 主内容区域 */
.dashboard-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* 欢迎区域 */
.welcome-section {
  margin-bottom: 32px;
}

.welcome-title {
  font-size: 28px;
  font-weight: 700;
  color: #333333;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.wave-icon {
  animation: wave 2s ease-in-out infinite;
  display: inline-block;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(20deg); }
  75% { transform: rotate(-20deg); }
}

.welcome-subtitle {
  font-size: 16px;
  color: #666666;
  margin: 0;
}

/* 通用区块样式 */
.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 24px;
}

/* 快捷入口区域 */
.quick-access-section {
  margin-bottom: 32px;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.quick-access-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 2px solid transparent;
}

.quick-access-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.2);
  border-color: #FF6B35;
}

.card-icon {
  font-size: 40px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFF8F0 0%, #FFE8D6 100%);
  border-radius: 12px;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 4px 0;
}

.card-description {
  font-size: 14px;
  color: #888888;
  margin: 0;
}

.card-arrow {
  font-size: 20px;
  color: #FF6B35;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
}

.quick-access-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* 今日概览区域 */
.overview-section {
  margin-bottom: 32px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.overview-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border-left: 4px solid;
}

.attendance-card {
  border-left-color: #4CAF50;
}

.leave-card {
  border-left-color: #FF6B35;
}

.abnormal-card {
  border-left-color: #F7C52D;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.card-icon-small {
  font-size: 20px;
}

.card-label {
  font-size: 14px;
  color: #888888;
  font-weight: 500;
}

.card-stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #333333;
  line-height: 1;
}

.stat-highlight {
  color: #4CAF50;
}

.stat-warning {
  color: #FF6B35;
}

.stat-label {
  font-size: 12px;
  color: #888888;
  margin-top: 4px;
}

.stat-divider {
  font-size: 24px;
  color: #cccccc;
}

.stat-item-full {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.stat-value-large {
  font-size: 36px;
  font-weight: 700;
  color: #FF6B35;
  line-height: 1;
}

/* 待办事项区域 */
.todo-section {
  margin-bottom: 32px;
}

.todo-list {
  background: #ffffff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  min-height: 200px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 16px;
  color: #888888;
  margin: 0;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid #f0f0f0;
}

.todo-item:last-child {
  border-bottom: none;
}

.todo-item:hover {
  background: #FFF8F0;
  transform: translateX(4px);
}

.todo-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 12px;
}

.todo-leave {
  background: linear-gradient(135deg, #FFF8F0 0%, #FFE8D6 100%);
}

.todo-shift_swap {
  background: linear-gradient(135deg, #F0F8FF 0%, #E0F0FF 100%);
}

.todo-appeal {
  background: linear-gradient(135deg, #FFF0F0 0%, #FFE0E0 100%);
}

.todo-content {
  flex: 1;
}

.todo-title {
  font-size: 16px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 4px;
}

.todo-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
}

.todo-type {
  color: #FF6B35;
  font-weight: 500;
}

.todo-time {
  color: #888888;
}

.todo-arrow {
  font-size: 18px;
  color: #cccccc;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
}

.todo-item:hover .todo-arrow {
  opacity: 1;
  transform: translateX(0);
  color: #FF6B35;
}

/* 本月统计区域 */
.monthly-section {
  margin-bottom: 32px;
}

.monthly-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.monthly-card {
  background: linear-gradient(135deg, #ffffff 0%, #FFF8F0 100%);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.monthly-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.15);
}

.monthly-icon {
  font-size: 40px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFE8D6 0%, #FFD8B8 100%);
  border-radius: 12px;
}

.monthly-content {
  flex: 1;
}

.monthly-value {
  font-size: 28px;
  font-weight: 700;
  color: #FF6B35;
  line-height: 1.2;
  margin-bottom: 4px;
}

.monthly-label {
  font-size: 14px;
  color: #888888;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .dashboard-main {
    padding: 20px 16px;
  }

  .quick-access-grid {
    grid-template-columns: 1fr;
  }

  .overview-cards {
    grid-template-columns: 1fr;
  }

  .monthly-cards {
    grid-template-columns: 1fr;
  }
}
</style>
