<template>
  <div class="max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">我的收藏</h2>
    <div v-if="favorites.length === 0" class="text-center py-12 text-gray-500">
      <el-icon :size="48" class="mb-4"><Star /></el-icon>
      <p>暂无收藏的景点</p>
      <router-link to="/attractions" class="text-blue-600">去逛逛</router-link>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="item in favorites" :key="item.attraction.id" class="bg-white rounded-xl shadow-md overflow-hidden">
        <el-image :src="item.attraction.coverImage" fit="cover" class="w-full h-48 cursor-pointer" @click="$router.push(`/attractions/${item.attraction.id}`)" />
        <div class="p-4">
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-semibold">{{ item.attraction.name }}</h3>
            <el-button type="danger" size="small" @click="removeFavorite(item.attraction.id)">取消收藏</el-button>
          </div>
          <el-rate v-model="item.attraction.rating" disabled size="small" show-score />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'
import { Star } from '@element-plus/icons-vue'

const favorites = ref([])

async function fetchFavorites() {
  try {
    const res = await request.get('/comments/favorites/my/')
    favorites.value = res.data || []
  } catch (error) {
    console.error(error)
  }
}

async function removeFavorite(id) {
  await request.delete(`/comments/favorites/${id}/`)
  ElMessage.success('已取消收藏')
  fetchFavorites()
}

onMounted(fetchFavorites)
</script>
