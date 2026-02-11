<template>
  <div v-if="attraction">
    <!-- 景点图片 -->
    <div class="bg-white rounded-xl shadow-md overflow-hidden mb-6">
      <el-image :src="attraction.coverImage" fit="cover" class="w-full h-96" />
    </div>

    <el-row :gutter="20">
      <!-- 左侧信息 -->
      <el-col :xs="24" :lg="16">
        <div class="bg-white rounded-xl shadow-md p-6 mb-6">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h1 class="text-3xl font-bold mb-2">{{ attraction.name }}</h1>
              <p class="text-gray-500 flex items-center">
                <el-icon class="mr-1"><Location /></el-icon>
                {{ attraction.address }}
              </p>
            </div>
            <div class="text-right">
              <el-button type="primary" :icon="isFavorite ? 'Star' : 'StarFilled'" @click="toggleFavorite">
                {{ isFavorite ? '取消收藏' : '收藏' }}
              </el-button>
            </div>
          </div>

          <el-row class="mb-6 text-center">
            <el-col :span="8">
              <p class="text-gray-500 text-sm">开放时间</p>
              <p class="font-medium">{{ attraction.openingHours || '待定' }}</p>
            </el-col>
            <el-col :span="8">
              <p class="text-gray-500 text-sm">景点类别</p>
              <el-tag>{{ attraction.category }}</el-tag>
            </el-col>
            <el-col :span="8">
              <p class="text-gray-500 text-sm">浏览量</p>
              <p class="font-medium">{{ attraction.viewCount || 0 }}</p>
            </el-col>
          </el-row>

          <el-divider content-position="center">景点介绍</el-divider>
          <div class="prose max-w-none">{{ attraction.description }}</div>
        </div>

        <!-- 评论区域 -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-bold mb-4 flex items-center">
            <el-icon class="mr-2"><ChatLineRound /></el-icon>
            用户评论 ({{ totalComments }})
          </h2>

          <!-- 发表评论 -->
          <div v-if="userStore.isLoggedIn" class="mb-6 p-4 bg-gray-50 rounded-lg">
            <el-rate v-model="newComment.rating" class="mb-2" />
            <el-input v-model="newComment.content" type="textarea" :rows="3" placeholder="分享您的体验..." />
            <div class="mt-2 flex justify-end">
              <el-button type="primary" @click="submitComment">发表评论</el-button>
            </div>
          </div>

          <!-- 评论列表 -->
          <div v-for="comment in comments" :key="comment.id" class="border-b py-4">
            <div class="flex items-start">
              <el-avatar :size="40">{{ comment.user?.realName?.charAt(0) || 'U' }}</el-avatar>
              <div class="ml-3 flex-1">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-medium">{{ comment.user?.realName }}</span>
                  <el-rate v-model="comment.rating" disabled size="small" />
                </div>
                <p class="text-gray-600">{{ comment.content }}</p>
                <p class="text-gray-400 text-sm mt-1">{{ formatDate(comment.createdAt) }}</p>
              </div>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 右侧推荐 -->
      <el-col :xs="24" :lg="8">
        <div class="bg-white rounded-xl shadow-md p-6">
          <h3 class="text-lg font-bold mb-4 flex items-center">
            <el-icon class="mr-2"><Star /></el-icon>
            相似推荐
          </h3>
          <div v-for="item in similarAttractions" :key="item.id" class="flex items-center py-3 border-b cursor-pointer hover:bg-gray-50" @click="$router.push(`/attractions/${item.id}`)">
            <el-image :src="item.coverImage" fit="cover" class="w-16 h-16 rounded-lg" />
            <div class="ml-3 flex-1">
              <p class="font-medium text-sm">{{ item.name }}</p>
              <el-rate v-model="item.rating" disabled size="small" />
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'
import { ElMessage } from 'element-plus'
import { Location, ChatLineRound, Star, StarFilled } from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()
const attraction = ref(null)
const comments = ref([])
const similarAttractions = ref([])
const isFavorite = ref(false)
const totalComments = ref(0)
const newComment = reactive({ rating: 5, content: '' })

async function fetchDetail() {
  try {
    const res = await request.get(`/attractions/${route.params.id}/`)
    attraction.value = res.data
    const commentsRes = await request.get(`/comments/attraction/${route.params.id}/`)
    comments.value = commentsRes.data || []
    totalComments.value = commentsRes.total || 0
    const similarRes = await request.get(`/recommendations/similar/${route.params.id}/`)
    similarAttractions.value = similarRes.data || []
  } catch (error) {
    console.error(error)
  }
}

async function toggleFavorite() {
  try {
    if (isFavorite.value) {
      await request.delete(`/comments/favorites/${attraction.value.id}/`)
      isFavorite.value = false
    } else {
      await request.post('/comments/favorites/', { attraction_id: attraction.value.id })
      isFavorite.value = true
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

async function submitComment() {
  try {
    await request.post('/comments/', {
      attraction_id: attraction.value.id,
      rating: newComment.rating,
      content: newComment.content
    })
    ElMessage.success('评论成功')
    newComment.content = ''
    newComment.rating = 5
    fetchDetail()
  } catch (error) {
    console.error(error)
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchDetail)
</script>
