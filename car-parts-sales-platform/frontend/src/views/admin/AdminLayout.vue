<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <AdminSidebar />

    <!-- 主内容区域 -->
    <div class="main-wrapper" :class="{ collapsed: isCollapsed }">
      <!-- 顶部导航栏 -->
      <header class="top-header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">
              <el-icon><HomeFilled /></el-icon>
              <span>管理后台</span>
            </el-breadcrumb-item>
            <el-breadcrumb-item v-for="item in breadcrumbList" :key="item.path">
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <!-- 全局搜索 -->
          <el-input
            v-model="searchKeyword"
            placeholder="搜索..."
            class="search-input"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <!-- 消息通知 -->
          <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="notification-badge">
            <el-button :icon="Bell" circle @click="handleMessageClick" />
          </el-badge>

          <!-- 用户下拉菜单 -->
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" :src="userAvatar">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
              <span class="user-name">{{ authStore.user?.nickname || '管理员' }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人资料
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
      </header>

      <!-- 面包屑导航（可选） -->
      <div v-if="showBreadcrumb" class="breadcrumb-bar">
        <Breadcrumb />
      </div>

      <!-- 页面内容 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  HomeFilled, Search, Bell, UserFilled, ArrowDown, User, Setting, SwitchButton
} from '@element-plus/icons-vue'
import AdminSidebar from '@/components/common/AdminSidebar.vue'
import Breadcrumb from '@/components/common/Breadcrumb.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 侧边栏折叠状态（从 localStorage 读取）
const isCollapsed = ref(false)

// 搜索关键词
const searchKeyword = ref('')

// 未读消息数量（模拟数据）
const unreadCount = ref(0)

// 用户头像
const userAvatar = computed(() => authStore.user?.avatar || '')

// 是否显示面包屑
const showBreadcrumb = computed(() => {
  return route.path !== '/admin/dashboard'
})

// 面包屑列表
const breadcrumbList = computed(() => {
  const path = route.path
  const segments = path.split('/').filter(Boolean)

  if (segments.length <= 2) return []

  const routeMap = {
    products: { title: '商品管理' },
    categories: { title: '分类管理' },
    orders: { title: '订单管理' },
    users: { title: '用户管理' },
    marketing: { title: '营销管理' },
    content: { title: '内容管理' },
    system: { title: '系统管理' }
  }

  const breadcrumbs = []
  segments.slice(2).forEach(segment => {
    const info = routeMap[segment]
    if (info) {
      breadcrumbs.push({ title: info.title, path: path })
    }
  })

  return breadcrumbs
})

// 初始化时读取折叠状态
const loadCollapsedState = () => {
  isCollapsed.value = localStorage.getItem('sidebar-collapsed') === 'true'
}

// 监听 localStorage 变化（当侧边栏折叠状态变化时同步）
const handleStorageChange = (e) => {
  if (e.key === 'sidebar-collapsed') {
    isCollapsed.value = e.newValue === 'true'
  }
}

onMounted(() => {
  loadCollapsedState()
  window.addEventListener('storage', handleStorageChange)
})

// 搜索
const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  ElMessage.info('搜索功能开发中...')
}

// 消息中心点击
const handleMessageClick = () => {
  router.push('/admin/system/messages')
}

// 下拉菜单命令处理
const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      router.push('/admin/profile')
      break
    case 'settings':
      router.push('/admin/system/config')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        authStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 取消退出
      }
      break
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f0f2f5;
}

/* 主内容区域 */
.main-wrapper {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left 0.3s;
}

.main-wrapper.collapsed {
  margin-left: 64px;
}

/* 顶部导航栏 */
.top-header {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 999;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-input {
  width: 200px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 20px;
}

.notification-badge {
  display: inline-flex;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 12px;
  border-radius: 20px;
  transition: background 0.3s;
}

.user-info:hover {
  background: #f5f5f5;
}

.user-name {
  font-size: 14px;
  color: #333;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  color: #909399;
}

/* 面包屑栏 */
.breadcrumb-bar {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 24px;
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

/* 响应式 */
@media (max-width: 768px) {
  .main-wrapper {
    margin-left: 0;
  }

  .main-wrapper.collapsed {
    margin-left: 0;
  }

  .top-header {
    padding: 0 16px;
  }

  .search-input {
    width: 150px;
  }

  .user-name {
    display: none;
  }

  .main-content {
    padding: 16px;
  }
}
</style>
