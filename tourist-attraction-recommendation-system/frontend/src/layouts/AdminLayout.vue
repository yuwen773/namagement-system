<template>
  <div class="min-h-screen bg-gray-100">
    <!-- 侧边栏 -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-gray-800 text-white">
      <div class="flex items-center h-16 px-6 border-b border-gray-700">
        <el-icon class="text-2xl"><MapLocation /></el-icon>
        <span class="ml-2 text-lg font-bold">旅游推荐管理后台</span>
      </div>
      <nav class="mt-6 px-3">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-4 py-3 mb-2 rounded-lg transition-colors"
          :class="$route.path === item.path || ($route.path.startsWith(item.path) && item.path !== '/admin') ? 'bg-blue-600' : 'text-gray-300 hover:bg-gray-700'"
        >
          <el-icon class="mr-3"><component :is="item.icon" /></el-icon>
          <span>{{ item.title }}</span>
        </router-link>
      </nav>
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700">
        <div class="flex items-center">
          <el-avatar :size="36" class="bg-blue-500">
            {{ userStore.user?.realName?.charAt(0) || 'A' }}
          </el-avatar>
          <div class="ml-3 flex-1">
            <p class="text-sm font-medium">{{ userStore.user?.realName || '管理员' }}</p>
            <p class="text-xs text-gray-400">管理员</p>
          </div>
          <el-dropdown trigger="click" @command="handleCommand">
            <el-icon class="cursor-pointer text-gray-400 hover:text-white"><Setting /></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="settings">
                  <el-icon><User /></el-icon>个人设置
                </el-dropdown-item>
                <el-dropdown-item command="home">
                  <el-icon><HomeFilled /></el-icon>返回前台
                </el-dropdown-item>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="ml-64 min-h-screen">
      <!-- 顶部栏 -->
      <header class="bg-white shadow-sm h-16 flex items-center justify-between px-6">
        <h1 class="text-xl font-semibold text-gray-800">{{ currentPageTitle }}</h1>
        <div class="flex items-center space-x-4">
          <router-link to="/" class="text-gray-500 hover:text-blue-600">
            <el-icon :size="20"><HomeFilled /></el-icon>
          </router-link>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'
import {
  MapLocation, DataBoard, User, Ticket, ChatDotSquare, Bell, Setting,
  SwitchButton, HomeFilled
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const menuItems = [
  { path: '/admin', title: '数据看板', icon: DataBoard },
  { path: '/admin/users', title: '用户管理', icon: User },
  { path: '/admin/attractions', title: '景点管理', icon: Ticket },
  { path: '/admin/comments', title: '评论审核', icon: ChatDotSquare },
  { path: '/admin/announcements', title: '公告管理', icon: Bell },
  { path: '/admin/settings', title: '个人设置', icon: Setting }
]

const currentPageTitle = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item?.title || route.meta?.title || '管理后台'
})

function handleCommand(command) {
  switch (command) {
    case 'settings':
      router.push('/admin/settings')
      break
    case 'home':
      router.push('/')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        userStore.logout()
        router.push('/admin/login')
      })
      break
  }
}
</script>
