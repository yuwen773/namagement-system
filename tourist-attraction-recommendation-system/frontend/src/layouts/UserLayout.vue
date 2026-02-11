<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <el-icon class="text-2xl text-blue-600"><MapLocation /></el-icon>
              <span class="ml-2 text-xl font-bold text-gray-900">旅游推荐</span>
            </router-link>
            <div class="hidden md:flex ml-10 space-x-8">
              <router-link
                to="/"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="$route.name === 'Home' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'"
              >
                首页
              </router-link>
              <router-link
                to="/attractions"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="$route.name === 'AttractionList' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'"
              >
                景点列表
              </router-link>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <template v-if="userStore.isLoggedIn">
              <el-dropdown trigger="click" @command="handleCommand">
                <div class="flex items-center cursor-pointer">
                  <el-avatar :size="32" :src="userStore.user?.avatar">
                    {{ userStore.user?.realName?.charAt(0) || 'U' }}
                  </el-avatar>
                  <span class="ml-2 text-sm text-gray-700 hidden sm:block">{{ userStore.user?.realName }}</span>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="usercenter">
                      <el-icon><User /></el-icon>个人中心
                    </el-dropdown-item>
                    <el-dropdown-item command="favorites">
                      <el-icon><Star /></el-icon>我的收藏
                    </el-dropdown-item>
                    <el-dropdown-item command="comments">
                      <el-icon><ChatLineRound /></el-icon>我的评论
                    </el-dropdown-item>
                    <el-dropdown-item command="notifications">
                      <el-icon><Bell /></el-icon>消息中心
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <router-link to="/login" class="text-sm text-gray-700 hover:text-blue-600">登录</router-link>
              <router-link to="/register" class="ml-4 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700">注册</router-link>
            </template>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主内容 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <!-- 底部 -->
    <footer class="bg-white border-t mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <p class="text-center text-sm text-gray-500">旅游景点推荐系统 &copy; 2026</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { MapLocation, User, Star, ChatLineRound, Bell, SwitchButton } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()

function handleCommand(command) {
  switch (command) {
    case 'usercenter':
      router.push('/usercenter')
      break
    case 'favorites':
      router.push('/favorites')
      break
    case 'comments':
      router.push('/comments')
      break
    case 'notifications':
      router.push('/notifications')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        userStore.logout()
        router.push('/')
      })
      break
  }
}
</script>
