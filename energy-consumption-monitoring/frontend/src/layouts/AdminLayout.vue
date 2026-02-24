<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">
        <h2>Energy Monitor</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#001529"
        text-color="#fff"
        active-text-color="#f97316"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><icon-ep-monitor /></el-icon>
          <span>Dashboard</span>
        </el-menu-item>
        <el-menu-item index="/admin/monitoring">
          <el-icon><icon-ep-data-analysis /></el-icon>
          <span>Monitoring</span>
        </el-menu-item>
        <el-menu-item index="/admin/analysis">
          <el-icon><icon-ep-trend-charts /></el-icon>
          <span>Analysis</span>
        </el-menu-item>
        <el-menu-item index="/admin/alarms">
          <el-icon><icon-ep-warning /></el-icon>
          <span>Alarms</span>
        </el-menu-item>
        <el-menu-item index="/admin/devices">
          <el-icon><icon-ep-cpu /></el-icon>
          <span>Devices</span>
        </el-menu-item>
        <el-menu-item index="/admin/configuration">
          <el-icon><icon-ep-setting /></el-icon>
          <span>Configuration</span>
        </el-menu-item>
        <el-menu-item index="/admin/system">
          <el-icon><icon-ep-tools /></el-icon>
          <span>System</span>
        </el-menu-item>
      </el-menu>
    </aside>
    <div class="main-container">
      <header class="header">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/admin' }">Admin</el-breadcrumb-item>
          <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
        </el-breadcrumb>
        <div class="user-menu">
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-icon><icon-ep-user /></el-icon>
              Admin
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)
const currentPageTitle = computed(() => route.name?.replace('Admin', '') || 'Home')

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 240px;
  background-color: #001529;
  overflow-y: auto;
}

.logo {
  padding: 20px;
  color: white;
  text-align: center;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e5e7eb;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f3f4f6;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
