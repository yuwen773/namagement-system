<template>
  <div>
    <!-- 搜索区域 -->
    <div class="mb-8">
      <div class="max-w-2xl mx-auto">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索景点名称..."
          size="large"
          prefix-icon="Search"
          @keyup.enter="handleSearch"
          class="shadow-lg"
        >
          <template #append>
            <el-button @click="handleSearch">搜索</el-button>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 个性化推荐 -->
    <section v-if="userStore.isLoggedIn && recommendations.length > 0" class="mb-12">
      <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
        <el-icon class="mr-2 text-blue-600"><Star /></el-icon>
        为您推荐
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="item in recommendations" :key="item.id" class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
          <el-image :src="item.coverImage" fit="cover" class="w-full h-48" />
          <div class="p-4">
            <h3 class="font-semibold text-lg mb-2">{{ item.name }}</h3>
            <p class="text-gray-500 text-sm mb-2">{{ item.address }}</p>
            <div class="flex items-center justify-between">
              <el-rate v-model="item.rating" disabled show-score text-color="#ff9900" />
              <span class="text-blue-600 font-medium">¥{{ item.price || '免费' }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 热门景点 -->
    <section class="mb-12">
      <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
        <el-icon class="mr-2 text-red-500"><HotWater /></el-icon>
        热门景点
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="item in hotAttractions" :key="item.id" class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push(`/attractions/${item.id}`)">
          <el-image :src="item.coverImage" fit="cover" class="w-full h-48" />
          <div class="p-4">
            <h3 class="font-semibold text-lg mb-2">{{ item.name }}</h3>
            <p class="text-gray-500 text-sm mb-2">{{ item.address }}</p>
            <div class="flex items-center justify-between">
              <el-rate v-model="item.rating" disabled show-score text-color="#ff9900" />
              <span class="text-blue-600 font-medium">¥{{ item.price || '免费' }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'
import { Star, HotWater, Search } from '@element-plus/icons-vue'

const userStore = useUserStore()
const searchKeyword = ref('')
const recommendations = ref([])
const hotAttractions = ref([])

async function handleSearch() {
  // 搜索功能
}

onMounted(async () => {
  try {
    const hotRes = await request.get('/recommendations/popular/')
    hotAttractions.value = hotRes.data || []
    if (userStore.isLoggedIn) {
      const recRes = await request.get('/recommendations/personalized/')
      recommendations.value = recRes.data || []
    }
  } catch (error) {
    console.error('获取推荐失败', error)
  }
})
</script>
