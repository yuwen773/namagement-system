<template>
  <div class="employee-home">
    <div class="home-container">
      <h1>员工首页</h1>
      <p>欢迎，{{ userStore.userInfo?.username || '员工' }}！</p>
      <p class="placeholder-info">这是阶段五第1步的内容</p>
      <el-button type="warning" @click="handleLogout">退出登录</el-button>
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
.employee-home {
  min-height: 100vh;
  background: linear-gradient(135deg, #FFF8F0, #ffffff);
}

.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.home-container h1 {
  color: #FF6B35;
  margin-bottom: 16px;
}

.home-container p {
  color: #666;
  margin-bottom: 24px;
}

.placeholder-info {
  color: #F7C52D;
  font-weight: 600;
}
</style>
