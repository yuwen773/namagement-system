<template>
  <div class="max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">消息中心</h2>
    <div class="bg-white rounded-xl shadow-md">
      <div v-if="notifications.length === 0" class="text-center py-12 text-gray-500">
        <el-icon :size="48" class="mb-4"><Bell /></el-icon>
        <p>暂无消息</p>
      </div>
      <div v-else>
        <div v-for="item in notifications" :key="item.id" class="p-4 border-b hover:bg-gray-50 cursor-pointer" :class="{ 'bg-blue-50': !item.isRead }" @click="handleNotification(item)">
          <div class="flex items-start">
            <el-icon :size="20" class="mt-1 mr-3" :class="item.isRead ? 'text-gray-400' : 'text-blue-600'">
              <Bell v-if="item.type === 'SYSTEM'" />
              <ChatDotSquare v-else-if="item.type === 'COMMENT'" />
              <Postcard v-else />
            </el-icon>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-medium">{{ item.title }}</span>
                <span class="text-gray-400 text-sm">{{ formatDate(item.createdAt) }}</span>
              </div>
              <p class="text-gray-600 mt-1">{{ item.content }}</p>
            </div>
            <el-tag v-if="!item.isRead" type="danger" size="small" class="ml-2">未读</el-tag>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { Bell, ChatDotSquare, Postcard } from '@element-plus/icons-vue'

const notifications = ref([])

async function fetchNotifications() {
  try {
    const res = await request.get('/notifications/')
    notifications.value = res.data || []
  } catch (error) {
    console.error(error)
  }
}

async function handleNotification(item) {
  if (!item.isRead) {
    await request.post(`/notifications/${item.id}/mark_read/`)
    item.isRead = true
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchNotifications)
</script>
