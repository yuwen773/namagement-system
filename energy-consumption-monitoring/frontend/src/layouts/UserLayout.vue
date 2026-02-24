<template>
  <div class="user-layout">
    <header class="header">
      <div class="logo">
        <h2>Energy Monitor - User Portal</h2>
      </div>
      <nav class="nav">
        <router-link to="/user/dashboard">Dashboard</router-link>
        <router-link to="/user/usage">Usage</router-link>
        <router-link to="/user/cost">Cost</router-link>
        <router-link to="/user/comparison">Comparison</router-link>
        <router-link to="/user/notices">Notices</router-link>
        <router-link to="/user/profile">Profile</router-link>
      </nav>
      <div class="user-menu">
        <el-button @click="handleLogout">Logout</el-button>
      </div>
    </header>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.user-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e5e7eb;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  color: #f97316;
}

.nav {
  display: flex;
  gap: 20px;
}

.nav a {
  color: #374151;
  text-decoration: none;
}

.nav a.router-link-active {
  color: #f97316;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f3f4f6;
}
</style>
