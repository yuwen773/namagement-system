<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

// 菜单数据
const menuItems = [
  { path: '/admin', name: '系统概览', icon: 'Odometer' },
  { path: '/admin/movies', name: '影片管理', icon: 'VideoCamera' },
  { path: '/admin/movie-types', name: '影片类型', icon: 'CollectionTag' },
  { path: '/admin/cinemas', name: '影院管理', icon: 'Location' },
  { path: '/admin/regions', name: '地域管理', icon: 'Grid' },
  { path: '/admin/boxoffice', name: '票房数据', icon: 'Money' },
  { path: '/admin/prediction', name: '预测分析', icon: 'DataAnalysis' },
  { path: '/admin/users', name: '用户管理', icon: 'User' }
]

// 当前激活菜单
const activeMenu = computed(() => route.path)

// 退出登录
const handleLogout = async () => {
  await userStore.doLogout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-layout flex h-screen bg-gray-100">
    <!-- 侧边栏 -->
    <aside
      class="sidebar bg-white shadow-sm transition-all duration-300"
      :class="{ 'w-64': !appStore.sidebarCollapsed, 'w-16': appStore.sidebarCollapsed }"
    >
      <!-- Logo -->
      <div class="h-16 flex items-center justify-center border-b border-gray-200">
        <h1 class="text-lg font-bold text-gray-800 whitespace-nowrap">
          {{ appStore.sidebarCollapsed ? '票房' : '电影票房预测系统' }}
        </h1>
      </div>

      <!-- 菜单 -->
      <el-menu
        :default-active="activeMenu"
        :collapse="appStore.sidebarCollapsed"
        class="sidebar-menu border-r-0"
      >
        <el-menu-item
          v-for="item in menuItems"
          :key="item.path"
          :index="item.path"
          @click="router.push(item.path)"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.name }}</template>
        </el-menu-item>
      </el-menu>
    </aside>

    <!-- 主内容区 -->
    <div class="main-content flex-1 flex flex-col overflow-hidden">
      <!-- 顶部栏 -->
      <header class="h-16 bg-white shadow-sm flex items-center justify-between px-4">
        <div class="flex items-center">
          <el-button
            :icon="appStore.sidebarCollapsed ? 'Expand' : 'Fold'"
            text
            @click="appStore.toggleSidebar"
          />
          <span class="ml-2 text-gray-600">{{ route.meta.title }}</span>
        </div>

        <div class="flex items-center gap-4">
          <!-- 用户信息 -->
          <el-dropdown trigger="click" @command="handleLogout">
            <div class="flex items-center cursor-pointer">
              <el-avatar :size="32" :src="userStore.user?.avatar">
                {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
              </el-avatar>
              <span class="ml-2 text-gray-700">{{ userStore.user?.real_name || userStore.user?.username }}</span>
              <el-icon class="ml-1"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon> 个人中心
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="flex-1 overflow-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.sidebar {
  width: 256px;
  flex-shrink: 0;
}

.sidebar-menu {
  height: calc(100vh - 64px);
  overflow-y: auto;
}

.main-content {
  min-width: 0;
}
</style>
