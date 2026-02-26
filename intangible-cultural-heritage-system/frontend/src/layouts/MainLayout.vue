<template>
  <div class="heritage-layout">
    <!-- 顶部导航栏 - 卷轴风格 -->
    <header class="layout-header">
      <div class="scroll-decoration left"></div>
      <div class="header-content">
        <!-- Logo 印章区域 -->
        <div class="logo-seal">
          <div class="seal-outer">
            <div class="seal-inner">
              <el-icon :size="32" class="seal-icon">
                <Collection />
              </el-icon>
            </div>
          </div>
          <div class="logo-texts">
            <h1 class="logo-title">非遗数据平台</h1>
            <span class="logo-subtitle">Cultural Heritage System</span>
          </div>
        </div>

        <!-- 用户信息区域 -->
        <div class="user-region">
          <div class="user-card">
            <div class="user-avatar">
              <el-icon :size="18">
                <User />
              </el-icon>
            </div>
            <div class="user-details">
              <span class="user-name">{{ userStore.username }}</span>
              <span
                class="user-role"
                :class="userStore.isAdmin ? 'role-admin' : 'role-user'"
              >
                {{ userStore.isAdmin ? '管理员' : '用户' }}
              </span>
            </div>
          </div>
          <el-button
            class="logout-btn"
            :icon="SwitchButton"
            @click="handleLogout"
          >
            退出
          </el-button>
        </div>
      </div>
      <div class="scroll-decoration right"></div>
    </header>

    <!-- 主体内容区域 -->
    <div class="layout-body">
      <!-- 侧边栏 - 书架风格 -->
      <aside class="layout-sidebar">
        <div class="sidebar-mount">
          <div class="mount-top"></div>
          <div class="mount-bottom"></div>
        </div>
        <nav class="sidebar-nav">
          <!-- 通用菜单 -->
          <div class="menu-shelf">
            <div class="shelf-title">数据查看</div>
            <router-link
              v-for="item in viewMenus"
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

          <!-- 管理员菜单 -->
          <div v-if="userStore.isAdmin" class="menu-shelf">
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
      </aside>

      <!-- 内容区域 - 宣纸风格 -->
      <main class="layout-content">
        <div class="content-scroll">
          <router-view v-slot="{ Component }">
            <transition name="scroll-unfold" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
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
  Upload,
  Lock
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 菜单配置
const viewMenus = [
  { path: '/dashboard', title: '驾驶舱', icon: DataAnalysis, seal: '览' },
  { path: '/heritage', title: '非遗项目', icon: Collection, seal: '宝' },
  { path: '/inheritors', title: '传承人', icon: User, seal: '传' }
]

const adminMenus = [
  { path: '/admin/heritage', title: '项目管理', icon: Edit, seal: '管' },
  { path: '/admin/inheritors', title: '传承人管理', icon: UserFilled, seal: '理' },
  { path: '/admin/categories', title: '分类管理', icon: Menu, seal: '类' },
  { path: '/admin/import', title: '数据导入', icon: Upload, seal: '入' },
  { path: '/admin/users', title: '用户管理', icon: Lock, seal: '用' }
]

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
.heritage-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F7F4ED;
}

/* ========== 顶部导航栏 - 卷轴风格 ========== */
.layout-header {
  position: relative;
  height: 72px;
  background: linear-gradient(135deg, #2F3640 0%, #1a2026 100%);
  display: flex;
  align-items: stretch;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.scroll-decoration {
  width: 40px;
  background: linear-gradient(180deg,
    #D4AF37 0%,
    #B8860B 15%,
    #8B6914 30%,
    #B8860B 50%,
    #D4AF37 70%,
    #B8860B 85%,
    #8B6914 100%
  );
  position: relative;
  flex-shrink: 0;
}

.scroll-decoration::before {
  content: '';
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 100%;
  background: repeating-linear-gradient(
    180deg,
    transparent 0px,
    transparent 8px,
    rgba(0, 0, 0, 0.2) 8px,
    rgba(0, 0, 0, 0.2) 10px
  );
  border-radius: 2px;
}

.scroll-decoration.left {
  border-radius: 0 8px 8px 0;
}

.scroll-decoration.right {
  border-radius: 8px 0 0 8px;
}

.header-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.logo-seal {
  display: flex;
  align-items: center;
  gap: 20px;
}

.seal-outer {
  width: 56px;
  height: 56px;
  background: #C23531;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 4px 16px rgba(194, 35, 49, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  flex-shrink: 0;
}

.seal-outer::before {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  right: 4px;
  bottom: 4px;
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-radius: 2px;
}

.seal-inner {
  width: 44px;
  height: 44px;
  background: rgba(194, 35, 49, 0.9);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seal-icon {
  color: #F7F4ED;
}

.logo-texts {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.logo-title {
  font-size: 22px;
  font-weight: 700;
  color: #F7F4ED;
  margin: 0;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.logo-subtitle {
  font-size: 11px;
  color: rgba(247, 244, 237, 0.7);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 500;
}

.user-region {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  background: rgba(247, 244, 237, 0.1);
  border-radius: 30px;
  border: 1px solid rgba(212, 175, 55, 0.3);
  backdrop-filter: blur(10px);
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

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #F7F4ED;
}

.user-role {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.role-admin {
  background: #C23531;
  color: white;
}

.role-user {
  background: rgba(93, 138, 168, 0.8);
  color: white;
}

.logout-btn {
  background: rgba(194, 35, 49, 0.9) !important;
  border: 1px solid rgba(194, 35, 49, 0.5) !important;
  color: #F7F4ED !important;
  border-radius: 20px !important;
  padding: 10px 20px !important;
  font-weight: 600 !important;
  transition: all 0.3s !important;
}

.logout-btn:hover {
  background: #DC143C !important;
  border-color: #DC143C !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 20, 60, 0.4) !important;
}

/* ========== 主体内容区域 ========== */
.layout-body {
  flex: 1;
  display: flex;
  max-width: 1920px;
  width: 100%;
  margin: 0 auto;
}

/* ========== 侧边栏 - 书架风格 ========== */
.layout-sidebar {
  width: 260px;
  background: linear-gradient(180deg, #FFFBF5 0%, #F7F4ED 100%);
  position: relative;
  box-shadow:
    2px 0 20px rgba(47, 54, 64, 0.1),
    inset 0 0 0 1px rgba(212, 175, 55, 0.1);
}

.sidebar-mount {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 24px 0;
  background: linear-gradient(180deg,
    rgba(212, 175, 55, 0.4) 0%,
    rgba(212, 175, 55, 0.2) 50%,
    rgba(212, 175, 55, 0.4) 100%
  );
}

.mount-top,
.mount-bottom {
  width: 16px;
  height: 16px;
  background: #D4AF37;
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.3);
}

.sidebar-nav {
  padding: 24px 0 24px 24px;
  overflow-y: auto;
  max-height: calc(100vh - 72px);
}

.menu-shelf {
  margin-bottom: 32px;
}

.shelf-title {
  padding: 8px 16px;
  margin-bottom: 12px;
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-left: 3px solid #D4AF37;
  padding-left: 12px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
  margin: 4px 0;
  border-radius: 8px 0 0 8px;
  color: #606266;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #D4AF37;
  transform: scaleY(0);
  transition: transform 0.3s;
}

.nav-item:hover {
  background: rgba(212, 175, 55, 0.1);
  color: #2F3640;
  transform: translateX(4px);
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(194, 35, 49, 0.1) 0%, transparent 100%);
  color: #C23531;
}

.nav-item.active::before {
  transform: scaleY(1);
}

.nav-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.nav-text {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.nav-seal {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #D4AF37;
  color: #2F3640;
  font-size: 12px;
  font-weight: 600;
  border-radius: 2px;
  font-family: "STSong", "SimSun", serif;
  flex-shrink: 0;
  opacity: 0.6;
}

.nav-item.active .nav-seal {
  background: #C23531;
  color: white;
  opacity: 1;
}

/* ========== 内容区域 ========== */
.layout-content {
  flex: 1;
  overflow: hidden;
  background: #F7F4ED;
  position: relative;
}

.layout-content::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background: radial-gradient(ellipse at center, rgba(212, 175, 55, 0.05) 0%, transparent 70%);
  pointer-events: none;
}

.content-scroll {
  height: 100%;
  overflow-y: auto;
  padding: 0;
}

/* ========== 页面切换动画 ========== */
.scroll-unfold-enter-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.scroll-unfold-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.scroll-unfold-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.98);
}

.scroll-unfold-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ========== 滚动条样式 ========== */
.sidebar-nav::-webkit-scrollbar,
.content-scroll::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track,
.content-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb,
.content-scroll::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #D4AF37, #CD7F32);
  border-radius: 3px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover,
.content-scroll::-webkit-scrollbar-thumb:hover {
  background: #C23531;
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .layout-sidebar {
    width: 80px;
  }

  .sidebar-mount {
    width: 8px;
  }

  .mount-top,
  .mount-bottom {
    width: 12px;
    height: 12px;
  }

  .sidebar-nav {
    padding: 24px 0 24px 12px;
  }

  .shelf-title {
    display: none;
  }

  .nav-text,
  .nav-seal {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 14px;
  }

  .nav-icon {
    margin: 0;
  }
}

@media (max-width: 768px) {
  .layout-header {
    height: auto;
    flex-direction: column;
  }

  .scroll-decoration {
    display: none;
  }

  .header-content {
    flex-direction: column;
    padding: 16px;
    gap: 16px;
  }

  .logo-seal {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }

  .layout-sidebar {
    display: none;
  }
}
</style>
