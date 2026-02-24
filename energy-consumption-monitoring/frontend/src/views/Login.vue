<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Energy Monitoring System</h1>
      <p>Login Page - To be implemented</p>
      <el-button type="primary" @click="handleLogin">Login (Demo)</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

function handleLogin() {
  // Demo login
  userStore.setToken('demo-token')
  userStore.setUserInfo({
    id: 1,
    username: 'admin',
    role: 'ADMIN',
  })
  router.push('/admin/dashboard')
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
}

.login-card {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 300px;
}

h1 {
  margin-bottom: 0.5rem;
  color: #1f2937;
}
</style>
