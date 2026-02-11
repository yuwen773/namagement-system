<template>
  <div class="max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">我的评论</h2>
    <div v-if="comments.length === 0" class="text-center py-12 text-gray-500">
      <el-icon :size="48" class="mb-4"><ChatLineRound /></el-icon>
      <p>暂无评论记录</p>
    </div>
    <div v-else class="space-y-4">
      <div v-for="item in comments" :key="item.id" class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-start justify-between">
          <div class="flex items-center">
            <el-image :src="item.attraction.coverImage" fit="cover" class="w-20 h-20 rounded-lg" />
            <div class="ml-4">
              <router-link :to="`/attractions/${item.attraction.id}`" class="font-semibold text-blue-600 hover:underline">
                {{ item.attraction.name }}
              </router-link>
              <div class="mt-1">
                <el-rate v-model="item.rating" disabled size="small" />
              </div>
            </div>
          </div>
          <span class="text-gray-400 text-sm">{{ formatDate(item.createdAt) }}</span>
        </div>
        <p class="mt-4 text-gray-600">{{ item.content }}</p>
        <div class="mt-3">
          <el-tag v-if="item.status === 'PENDING'" type="warning">待审核</el-tag>
          <el-tag v-else-if="item.status === 'APPROVED'" type="success">已通过</el-tag>
          <el-tag v-else type="danger">已驳回</el-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ChatLineRound } from '@element-plus/icons-vue'

const comments = ref([])

async function fetchComments() {
  try {
    const res = await request.get('/comments/my/')
    comments.value = res.data || []
  } catch (error) {
    console.error(error)
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchComments)
</script>
