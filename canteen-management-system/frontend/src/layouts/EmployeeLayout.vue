<template>
  <el-container class="employee-layout">
    <!-- 顶部导航栏 -->
    <el-header class="top-header">
      <div class="header-left">
        <div class="logo-area">
          <el-icon :size="32" class="logo-icon"><FoodIcon /></el-icon>
          <span class="logo-text">食堂管理系统</span>
        </div>
      </div>

      <div class="header-center">
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          :ellipsis="false"
          router
          class="top-menu"
          background-color="transparent"
          text-color="#333333"
          active-text-color="#FF6B35"
        >
          <el-menu-item index="/employee">首页</el-menu-item>
          <el-menu-item index="/employee/checkin">签到签退</el-menu-item>
          <el-menu-item index="/employee/schedule">我的排班</el-menu-item>
          <el-menu-item index="/employee/attendance">考勤记录</el-menu-item>
          <el-menu-item index="/employee/leave">请假申请</el-menu-item>
          <el-menu-item index="/employee/swap">调班申请</el-menu-item>
          <el-menu-item index="/employee/salary">薪资查询</el-menu-item>
        </el-menu>
      </div>

      <div class="header-right">
        <div class="date-info">
          <el-icon><Calendar /></el-icon>
          <span>{{ currentDate }}</span>
        </div>

        <el-dropdown @command="handleUserAction">
          <div class="user-dropdown">
            <el-avatar :size="36" class="user-avatar">
              <el-icon><UserFilled /></el-icon>
            </el-avatar>
            <span class="user-name">{{ userName }}</span>
            <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>
                个人信息
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="main-content">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../stores/user'
import {
  Calendar,
  UserFilled,
  ArrowDown,
  User,
  SwitchButton
} from '@element-plus/icons-vue'

// 自定义食物图标组件
const FoodIcon = {
  template: `
    <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
      <path fill="currentColor" d="M128 256h768a32 32 0 0 1 32 32v640a32 32 0 0 1-32 32H128a32 32 0 0 1-32-32V288a32 32 0 0 1 32-32z m0-64a96 96 0 0 0-96 96v640a96 96 0 0 0 96 96h768a96 96 0 0 0 96-96V288a96 96 0 0 0-96-96H128z"/>
      <path fill="currentColor" d="M416 512h192a32 32 0 0 1 32 32v192a32 32 0 0 1-32 32H416a32 32 0 0 1-32-32V544a32 32 0 0 1 32-32z m32 64v128h128V576H448z"/>
    </svg>
  `
}

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 用户名
const userName = computed(() => userStore.userInfo?.username || '员工')

// 当前日期
const currentDate = ref('')
let dateTimer = null

// 更新日期
const updateDate = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const weekDays = ['日', '一', '二', '三', '四', '五', '六']
  const weekDay = weekDays[now.getDay()]
  currentDate.value = `${year}年${month}月${day}日 星期${weekDay}`
}

// 处理用户操作
const handleUserAction = (command) => {
  switch (command) {
    case 'profile':
      router.push('/employee/profile')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }).catch(() => {})
}

onMounted(() => {
  updateDate()
  // 每秒更新时间
  dateTimer = setInterval(updateDate, 1000)
})

onUnmounted(() => {
  if (dateTimer) {
    clearInterval(dateTimer)
  }
})
</script>

<style scoped>
.employee-layout {
  height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏 */
.top-header {
  background: #ffffff;
  border-bottom: 2px solid #FF6B35;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.15);
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  color: #FF6B35;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  color: #FF6B35;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.top-menu {
  border: none;
  flex: 1;
  max-width: 600px;
}

.top-menu :deep(.el-menu-item) {
  height: 64px;
  line-height: 64px;
  font-size: 16px;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.top-menu :deep(.el-menu-item:hover) {
  background-color: #FFF8F0;
  color: #FF6B35;
}

.top-menu :deep(.el-menu-item.is-active) {
  border-bottom-color: #FF6B35;
  background-color: #FFF8F0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.date-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.date-info .el-icon {
  color: #FF6B35;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.user-avatar {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
}

.user-name {
  font-size: 14px;
  color: #303133;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  color: #909399;
}

/* 主内容区 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #FFF8F0;
}

/* 滚动条样式 */
:deep(.main-content::-webkit-scrollbar) {
  width: 6px;
}

:deep(.main-content::-webkit-scrollbar-thumb) {
  background-color: rgba(255, 107, 53, 0.3);
  border-radius: 3px;
}

:deep(.main-content::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(255, 107, 53, 0.5);
}

/* 响应式设计 */
/* 小屏幕（笔记本） < 1200px */
@media (max-width: 1199px) {
  .top-header {
    padding: 0 20px;
  }

  .header-right {
    gap: 16px;
  }

  .user-name {
    max-width: 80px;
  }

  .main-content {
    padding: 16px;
  }

  .logo-text {
    font-size: 18px;
  }

  .top-menu :deep(.el-menu-item) {
    font-size: 15px;
    padding: 0 14px;
  }

  .top-menu {
    max-width: 500px;
  }
}

/* 中等屏幕 1200px - 1439px */
@media (min-width: 1200px) and (max-width: 1439px) {
  .main-content {
    padding: 18px;
  }

  .top-menu {
    /* max-width removed */
  }
}

/* 超小屏幕（特殊优化） < 768px */
@media (max-width: 767px) {
  .top-header {
    padding: 0 12px;
    height: 56px;
  }

  .logo-text {
    display: none;
  }

  .date-info {
    display: none;
  }

  .user-name {
    display: none;
  }

  .main-content {
    padding: 12px;
  }

  .top-menu :deep(.el-menu-item) {
    font-size: 14px;
    padding: 0 8px;
    height: 56px;
    line-height: 56px;
  }

  .user-dropdown {
    padding: 6px 8px;
  }

  /* 更大的点击区域 */
  .user-dropdown,
  .top-menu :deep(.el-menu-item) {
    min-height: 44px;
  }
}
</style>
