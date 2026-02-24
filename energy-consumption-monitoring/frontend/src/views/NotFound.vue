<template>
  <div class="not-found-page">
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <el-button type="primary" @click="goHome">Go Home</el-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/login')
}
</script>

<style scoped>
.not-found-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
}

h1 {
  font-size: 48px;
  color: #6b7280;
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  color: #6b7280;
  margin-bottom: 20px;
}
</style>
