<template>
  <div class="main-layout">
    <!-- 顶部导航栏 -->
    <header class="layout-header">
      <div class="header-content">
        <!-- Logo 区域 -->
        <div class="logo-section">
          <div class="logo-icon">
            <el-icon :size="28">
              <Collection />
            </el-icon>
          </div>
          <div class="logo-text">
            <h1 class="logo-title">非遗数据平台</h1>
            <span class="logo-subtitle">Cultural Heritage</span>
          </div>
        </div>

        <!-- 用户信息区域 -->
        <div class="user-section">
          <div class="user-info">
            <el-icon :size="20" class="user-icon">
              <User />
            </el-icon>
            <span class="username">{{ userStore.username }}</span>
            <el-tag :type="userStore.isAdmin ? 'danger' : 'info'" size="small" class="role-tag">
              {{ userStore.isAdmin ? '管理员' : '用户' }}
            </el-tag>
          </div>
          <el-button
            type="danger"
            size="small"
            :icon="SwitchButton"
            @click="handleLogout"
            class="logout-btn"
          >
            退出
          </el-button>
        </div>
      </div>
    </header>

    <!-- 主体内容区域 -->
    <div class="layout-body">
      <!-- 侧边栏 -->
      <aside class="layout-sidebar">
        <el-menu
          :default-active="activeMenu"
          :router="true"
          class="sidebar-menu"
        >
          <!-- 通用菜单 -->
          <div class="menu-section">
            <div class="menu-section-title">数据查看</div>
            <el-menu-item index="/dashboard">
              <el-icon><DataAnalysis /></el-icon>
              <span>驾驶舱</span>
            </el-menu-item>
            <el-menu-item index="/heritage">
              <el-icon><Collection /></el-icon>
              <span>非遗项目</span>
            </el-menu-item>
            <el-menu-item index="/inheritors">
              <el-icon><User /></el-icon>
              <span>传承人</span>
            </el-menu-item>
          </div>

          <!-- 管理员菜单 -->
          <div v-if="userStore.isAdmin" class="menu-section">
            <div class="menu-section-title">数据管理</div>
            <el-menu-item index="/admin/heritage">
              <el-icon><Edit /></el-icon>
              <span>项目管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/inheritors">
              <el-icon><UserFilled /></el-icon>
              <span>传承人管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/categories">
              <el-icon><Menu /></el-icon>
              <span>分类管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/import">
              <el-icon><Upload /></el-icon>
              <span>数据导入</span>
            </el-menu-item>
          </div>
        </el-menu>
      </aside>

      <!-- 内容区域 -->
      <main class="layout-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Collection,
  User,
  UserFilled,
  SwitchButton,
  DataAnalysis,
  Edit,
  Menu,
  Upload
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

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
  } catch (error) {
    // 用户取消
  }
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

/* 顶部导航栏 */
.layout-header {
  height: 64px;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1920px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  backdrop-filter: blur(10px);
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-title {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0;
  letter-spacing: 0.5px;
}

.logo-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.user-icon {
  color: white;
}

.username {
  color: white;
  font-weight: 500;
  font-size: 14px;
}

.role-tag {
  font-size: 11px;
  font-weight: 600;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
}

/* 主体内容区域 */
.layout-body {
  flex: 1;
  display: flex;
  max-width: 1920px;
  width: 100%;
  margin: 0 auto;
}

/* 侧边栏 */
.layout-sidebar {
  width: 240px;
  background: white;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.sidebar-menu {
  border-right: none;
  padding: 16px 0;
}

.menu-section {
  margin-bottom: 24px;
}

.menu-section-title {
  padding: 8px 24px;
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

:deep(.el-menu-item) {
  margin: 4px 12px;
  border-radius: 8px;
  transition: all 0.3s;
}

:deep(.el-menu-item:hover) {
  background: #f5f7fa;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  color: white;
}

:deep(.el-menu-item.is-active .el-icon) {
  color: white;
}

/* 内容区域 */
.layout-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: #f5f7fa;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 滚动条样式 */
.layout-sidebar::-webkit-scrollbar,
.layout-content::-webkit-scrollbar {
  width: 6px;
}

.layout-sidebar::-webkit-scrollbar-thumb,
.layout-content::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 3px;
}

.layout-sidebar::-webkit-scrollbar-thumb:hover,
.layout-content::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}
</style>
