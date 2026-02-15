<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: adminStore.isCollapsed }">
      <div class="sidebar-header">
        <el-icon :size="24" v-if="!adminStore.isCollapsed"><DataAnalysis /></el-icon>
        <span v-if="!adminStore.isCollapsed">管理后台</span>
      </div>
      <el-menu
        :default-active="adminStore.activeMenu"
        :collapse="adminStore.isCollapsed"
        @select="handleMenuSelect"
        class="sidebar-menu"
      >
        <el-menu-item index="dashboard">
          <el-icon><Odometer /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="data-import">
          <el-icon><Upload /></el-icon>
          <span>数据导入</span>
        </el-menu-item>
        <el-menu-item index="air-quality">
          <el-icon><DataLine /></el-icon>
          <span>数据管理</span>
        </el-menu-item>
        <el-menu-item index="rules">
          <el-icon><Document /></el-icon>
          <span>规则管理</span>
        </el-menu-item>
        <el-menu-item index="users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="articles">
          <el-icon><Document /></el-icon>
          <span>文章管理</span>
        </el-menu-item>
        <el-menu-item index="logs">
          <el-icon><Notebook /></el-icon>
          <span>系统日志</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <!-- Main Content -->
    <div class="main-wrapper">
      <!-- Top Bar -->
      <header class="top-bar">
        <div class="top-bar-left">
          <el-button :icon="Fold" @click="adminStore.toggleSidebar" text />
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin' }">管理后台</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentTitle">{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="top-bar-right">
          <el-button @click="goToUserSite">用户端</el-button>
          <el-dropdown @command="handleCommand">
            <span class="user-name">
              <el-icon><User /></el-icon>
              {{ userStore.username }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- Page Content -->
      <main class="main-content">
        <router-view @update-title="updateTitle" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAdminStore } from '@/stores/admin'
import {
  DataAnalysis, Odometer, Upload, DataLine, Document,
  User, Notebook, Fold
} from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const adminStore = useAdminStore()

const currentTitle = computed(() => route.meta.title || '')

function handleMenuSelect(index) {
  adminStore.setActiveMenu(index)
  const routeMap = {
    dashboard: '/admin',
    'data-import': '/admin/data-import',
    'air-quality': '/admin/air-quality',
    rules: '/admin/rules',
    users: '/admin/users',
    articles: '/admin/articles',
    logs: '/admin/logs'
  }
  router.push(routeMap[index] || '/admin')
}

function handleCommand(command) {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.clearUser()
      router.push('/login')
    })
  }
}

function goToUserSite() {
  router.push('/')
}

function updateTitle(title) {
  // Can be used to update title dynamically
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background: #304156;
  transition: width 0.3s;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  border: none;
  background: transparent;
}

.sidebar-menu :deep(.el-menu-item) {
  color: #bfcbd9;
}

.sidebar-menu :deep(.el-menu-item:hover),
.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #263445;
  color: #409eff;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  height: 60px;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: #606266;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f5f7fa;
}
</style>
