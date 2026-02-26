<template>
  <div class="admin-layout">
    <!-- 侧边栏 - 书架风格 -->
    <aside class="layout-sidebar">
      <div class="sidebar-header">
        <div class="logo-seal">
          <div class="seal-outer">
            <div class="seal-inner">
              <el-icon :size="24" class="seal-icon">
                <Setting />
              </el-icon>
            </div>
          </div>
          <div class="logo-text">
            <h1>管理后台</h1>
            <span>Admin Panel</span>
          </div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="menu-shelf">
          <div class="shelf-title">数据管理</div>
          <router-link
            v-for="item in adminMenus"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="nav-icon">
              <component :is="item.icon" />
            </span>
            <span class="nav-text">{{ item.title }}</span>
            <span class="nav-seal">{{ item.seal }}</span>
          </router-link>
        </div>

      </nav>

      <div class="sidebar-footer">
        <div class="user-card">
          <div class="user-avatar">
            <el-icon :size="16">
              <User />
            </el-icon>
          </div>
          <div class="user-info">
            <span class="user-name">{{ userStore.username }}</span>
            <span class="user-role">管理员</span>
          </div>
        </div>
        <el-button
          class="logout-btn"
          :icon="SwitchButton"
          @click="handleLogout"
          size="small"
        >
          退出
        </el-button>
      </div>
    </aside>

    <!-- 主体内容区域 -->
    <main class="layout-main">
      <!-- 顶部工具栏 -->
      <header class="main-header">
        <div class="header-title">
          <h2>{{ currentPageTitle }}</h2>
        </div>
        <div class="header-actions">
          <span class="welcome-text">欢迎，{{ userStore.username }}</span>
        </div>
      </header>

      <!-- 内容区域 -->
      <div class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  User,
  SwitchButton,
  Back,
  Edit,
  UserFilled,
  Menu,
  Upload,
  Bell,
  Lock,
  DataAnalysis
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 菜单配置
const adminMenus = [
  { path: '/admin/dashboard', title: '驾驶舱', icon: DataAnalysis, seal: '览' },
  { path: '/admin/heritage', title: '项目管理', icon: Edit, seal: '管' },
  { path: '/admin/inheritors', title: '传承人管理', icon: UserFilled, seal: '理' },
  { path: '/admin/categories', title: '分类管理', icon: Menu, seal: '类' },
  // { path: '/admin/import', title: '数据导入', icon: Upload, seal: '入' },
  { path: '/admin/announcements', title: '公告管理', icon: Bell, seal: '告' },
  { path: '/admin/users', title: '用户管理', icon: Lock, seal: '用' }
]

// 当前页面标题
const currentPageTitle = computed(() => {
  const menu = adminMenus.find(m => isActive(m.path))
  if (menu) return menu.title
  // 检查是否是驾驶舱
  if (isActive('/dashboard')) return '驾驶舱'
  return '管理后台'
})

const isActive = (path: string) => {
  return route.path === path || route.path.startsWith(path + '/')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
/* ========== 全局布局 ========== */
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #F7F4ED;
}

/* ========== 侧边栏 ========== */
.layout-sidebar {
  width: 260px;
  background: linear-gradient(180deg, #2F3640 0%, #1a2026 100%);
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 1000;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-seal {
  display: flex;
  align-items: center;
  gap: 16px;
}

.seal-outer {
  width: 48px;
  height: 48px;
  background: #C23531;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(194, 35, 49, 0.4);
}

.seal-inner {
  width: 38px;
  height: 38px;
  background: rgba(194, 35, 49, 0.9);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seal-icon {
  color: #F7F4ED;
}

.logo-text h1 {
  font-size: 18px;
  font-weight: 700;
  color: #F7F4ED;
  margin: 0;
  letter-spacing: 2px;
  font-family: "STSong", "SimSun", serif;
}

.logo-text span {
  font-size: 10px;
  color: rgba(247, 244, 237, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* ========== 导航菜单 ========== */
.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.menu-shelf {
  margin-bottom: 24px;
}

.shelf-title {
  padding: 8px 24px;
  font-size: 11px;
  font-weight: 600;
  color: rgba(247, 244, 237, 0.5);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 24px;
  color: rgba(247, 244, 237, 0.7);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(247, 244, 237, 0.05);
  color: #F7F4ED;
  padding-left: 28px;
}

.nav-item.active {
  background: rgba(194, 35, 49, 0.2);
  color: #F7F4ED;
  border-left-color: #C23531;
}

.nav-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.nav-text {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
}

.nav-seal {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(212, 175, 55, 0.2);
  color: #D4AF37;
  font-size: 11px;
  font-weight: 600;
  border-radius: 2px;
  font-family: "STSong", "SimSun", serif;
}

.nav-item.active .nav-seal {
  background: #C23531;
  color: white;
}

/* ========== 侧边栏底部 ========== */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(247, 244, 237, 0.05);
  border-radius: 8px;
  margin-bottom: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #D4AF37, #CD7F32);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2F3640;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow: hidden;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #F7F4ED;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 11px;
  color: #C23531;
}

.logout-btn {
  width: 100%;
  background: rgba(194, 35, 49, 0.8) !important;
  border: none !important;
  color: #F7F4ED !important;
  border-radius: 6px !important;
  font-weight: 500 !important;
}

.logout-btn:hover {
  background: #DC143C !important;
}

/* ========== 主内容区 ========== */
.layout-main {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0; /* 防止子元素撑开容器导致溢出 */
}

.main-header {
  height: 64px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-title h2 {
  font-size: 18px;
  font-weight: 600;
  color: #2F3640;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.welcome-text {
  font-size: 14px;
  color: #606266;
}

.main-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}

/* ========== 页面切换动画 ========== */
.fade-slide-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* ========== 滚动条样式 ========== */
.sidebar-nav::-webkit-scrollbar,
.main-content::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track,
.main-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(212, 175, 55, 0.3);
  border-radius: 3px;
}

.main-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .layout-sidebar {
    width: 80px;
  }

  .logo-text,
  .nav-text,
  .nav-seal,
  .shelf-title {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 14px;
  }

  .sidebar-header {
    padding: 16px;
    justify-content: center;
  }

  .logo-seal {
    justify-content: center;
  }

  .user-info,
  .logout-btn span {
    display: none;
  }

  .user-card {
    justify-content: center;
    padding: 8px;
  }

  .logout-btn {
    padding: 8px !important;
  }

  .layout-main {
    margin-left: 80px;
  }
}
</style>
