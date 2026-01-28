<template>
  <el-container class="admin-layout">
    <!-- 侧导航栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
      <div class="logo-area">
        <div v-if="!isCollapse" class="logo-full">
          <el-icon :size="32" class="logo-icon"><FoodIcon /></el-icon>
          <span class="logo-text">食堂管理系统</span>
        </div>
        <div v-else class="logo-mini">
          <el-icon :size="28"><FoodIcon /></el-icon>
        </div>
      </div>

      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :unique-opened="true"
        router
        class="sidebar-menu"
        background-color="#FF6B35"
        text-color="#ffffff"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/admin">
          <el-icon><HomeFilled /></el-icon>
          <template #title>工作台</template>
        </el-menu-item>

        <el-menu-item index="/admin/employees">
          <el-icon><User /></el-icon>
          <template #title>员工管理</template>
        </el-menu-item>

        <el-menu-item index="/admin/schedules">
          <el-icon><Calendar /></el-icon>
          <template #title>排班管理</template>
        </el-menu-item>

        <el-menu-item index="/admin/attendance">
          <el-icon><Clock /></el-icon>
          <template #title>考勤管理</template>
        </el-menu-item>

        <el-menu-item index="/admin/leaves">
          <el-icon><DocumentChecked /></el-icon>
          <template #title>请假审批</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="top-header">
        <div class="header-left">
          <el-button
            :icon="isCollapse ? DArrowRight : DArrowLeft"
            circle
            @click="toggleCollapse"
            class="collapse-btn"
          />
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentMenuTitle">{{ currentMenuTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
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
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
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

      <!-- 页面内容区 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../stores/user'
import {
  HomeFilled,
  User,
  Calendar,
  Clock,
  DocumentChecked,
  DArrowLeft,
  DArrowRight,
  UserFilled,
  ArrowDown,
  Setting,
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

// 侧边栏折叠状态
const isCollapse = ref(false)

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 当前菜单标题
const currentMenuTitle = computed(() => {
  const titleMap = {
    '/admin': '',
    '/admin/employees': '员工管理',
    '/admin/schedules': '排班管理',
    '/admin/attendance': '考勤管理',
    '/admin/leaves': '请假审批'
  }
  return titleMap[route.path] || ''
})

// 用户名
const userName = computed(() => userStore.userInfo?.username || '管理员')

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

// 切换侧边栏折叠
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

// 处理用户操作
const handleUserAction = (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人信息功能开发中')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中')
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
.admin-layout {
  height: 100vh;
  background-color: #f5f5f5;
}

/* 侧边栏样式 */
.sidebar {
  background: linear-gradient(180deg, #FF6B35 0%, #FF8C42 100%);
  transition: width 0.3s ease;
  box-shadow: 2px 0 8px rgba(255, 107, 53, 0.2);
  overflow: hidden;
}

.logo-area {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-full {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  color: #ffffff;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
}

.logo-mini {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-menu {
  border: none;
  height: calc(100% - 64px);
  overflow-y: auto;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 56px;
  line-height: 56px;
  margin: 4px 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.2) !important;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  font-size: 20px;
  color: #ffffff;
}

/* 主容器 */
.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* 顶部导航栏 */
.top-header {
  background: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  border-color: #FF6B35;
  color: #FF6B35;
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  background-color: #FF6B35;
  color: #ffffff;
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
:deep(.sidebar-menu::-webkit-scrollbar),
:deep(.main-content::-webkit-scrollbar) {
  width: 6px;
}

:deep(.sidebar-menu::-webkit-scrollbar-thumb),
:deep(.main-content::-webkit-scrollbar-thumb) {
  background-color: rgba(255, 107, 53, 0.3);
  border-radius: 3px;
}

:deep(.sidebar-menu::-webkit-scrollbar-thumb:hover),
:deep(.main-content::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(255, 107, 53, 0.5);
}

/* 面包屑样式 */
:deep(.el-breadcrumb__inner) {
  color: #606266;
  font-weight: 400;
}

:deep(.el-breadcrumb__inner.is-link) {
  color: #FF6B35;
}

:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #303133;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
  }

  .main-container {
    margin-left: 0;
  }

  .user-name {
    display: none;
  }

  .date-info {
    display: none;
  }
}
</style>
