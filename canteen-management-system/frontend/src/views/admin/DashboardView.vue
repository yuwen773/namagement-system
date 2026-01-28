<template>
  <div class="admin-dashboard">
    <div class="dashboard-container">
      <h1>管理员首页（Dashboard）</h1>
      <p>欢迎，管理员！</p>
      <p class="placeholder-info">这是阶段四第1步的内容</p>
      <el-button type="danger" @click="handleLogout">退出登录</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: #f5f5f5;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.dashboard-container h1 {
  color: #333;
  margin-bottom: 16px;
}

.dashboard-container p {
  color: #666;
  margin-bottom: 24px;
}

.placeholder-info {
  color: #FF6B35;
  font-weight: 600;
}
</style>
