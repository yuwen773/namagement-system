<template>
  <div class="user-layout">
    <!-- Header -->
    <header class="header">
      <div class="header-container">
        <div class="logo" @click="router.push('/')">
          <el-icon :size="24"><Cloudy /></el-icon>
          <span>空气质量监测平台</span>
        </div>
        <nav class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/historical" class="nav-item">历史数据</router-link>
          <router-link to="/analysis" class="nav-item">数据分析</router-link>
          <router-link to="/protection" class="nav-item">防护指南</router-link>
          <router-link to="/knowledge" class="nav-item">科普知识</router-link>
        </nav>
        <div class="header-actions">
          <el-button v-if="!userStore.isLoggedIn" type="primary" @click="router.push('/login')">
            登录
          </el-button>
          <el-dropdown v-else @command="handleCommand">
            <span class="user-name">
              <el-icon><User /></el-icon>
              {{ userStore.username }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-if="userStore.isAdmin" command="admin">管理后台</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <p>&copy; 2026 全国空气质量数据监测与居民个人防护指南平台</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Cloudy, User } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

function handleCommand(command) {
  if (command === 'admin') {
    router.push('/admin')
  } else if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.clearUser()
      router.push('/')
    })
  }
}
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}

.nav-menu {
  display: flex;
  gap: 24px;
}

.nav-item {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
  position: relative;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: white;
}

.nav-item.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -18px;
  left: 0;
  right: 0;
  height: 2px;
  background: white;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: white;
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.footer {
  background: #f5f7fa;
  padding: 20px;
  text-align: center;
  color: #606266;
  font-size: 14px;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
