<template>
  <div class="forbidden-page">
    <h1>403 - Access Denied</h1>
    <p>You don't have permission to access this page.</p>
    <el-button type="primary" @click="goBack">Go Back</el-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goBack() {
  router.back()
}
</script>

<style scoped>
.forbidden-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
}

h1 {
  font-size: 48px;
  color: #ef4444;
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  color: #6b7280;
  margin-bottom: 20px;
}
</style>
