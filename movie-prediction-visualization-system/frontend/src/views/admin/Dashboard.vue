<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 统计数据
const stats = ref([
  { title: '影片总数', value: 0, icon: 'VideoCamera', color: '#409eff' },
  { title: '影院总数', value: 0, icon: 'Location', color: '#67c23a' },
  { title: '票房记录', value: 0, icon: 'Money', color: '#e6a23c' },
  { title: '用户总数', value: 0, icon: 'User', color: '#909399' }
])

onMounted(() => {
  // TODO: 加载统计数据
})
</script>

<template>
  <div class="dashboard">
    <h2 class="text-2xl font-bold mb-6">系统概览</h2>

    <!-- 欢迎语 -->
    <el-card class="mb-6">
      <div class="flex items-center">
        <el-avatar :size="64" :src="userStore.user?.avatar">
          {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
        </el-avatar>
        <div class="ml-4">
          <h3 class="text-xl font-bold">欢迎回来，{{ userStore.user?.real_name || userStore.user?.username }}</h3>
          <p class="text-gray-500 mt-1">今天是 {{ new Date().toLocaleDateString('zh-CN') }}</p>
        </div>
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col v-for="stat in stats" :key="stat.title" :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="flex items-center">
            <el-icon :size="40" :style="{ color: stat.color }">
              <component :is="stat.icon" />
            </el-icon>
            <div class="ml-4">
              <div class="text-2xl font-bold">{{ stat.value }}</div>
              <div class="text-gray-500">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.stat-card {
  margin-bottom: 20px;
}
</style>
