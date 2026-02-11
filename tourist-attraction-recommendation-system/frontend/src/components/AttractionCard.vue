<template>
  <div
    class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden cursor-pointer border border-gray-100"
    @click="handleClick"
  >
    <!-- 封面图片 -->
    <div class="relative h-48 overflow-hidden">
      <img
        :src="attraction.coverImage || defaultImage"
        :alt="attraction.name"
        class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        @error="handleImageError"
      />
      <!-- 分类标签 -->
      <div class="absolute top-3 left-3">
        <span class="px-2 py-1 bg-blue-600 text-white text-xs rounded-full">
          {{ attraction.category || '景点' }}
        </span>
      </div>
      <!-- 评分标签 -->
      <div class="absolute top-3 right-3 flex items-center bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full shadow-sm">
        <el-icon class="text-yellow-500 mr-1"><Star /></el-icon>
        <span class="text-sm font-medium text-gray-700">{{ attraction.rating?.toFixed(1) || '0.0' }}</span>
      </div>
    </div>

    <!-- 景点信息 -->
    <div class="p-4">
      <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-1">
        {{ attraction.name }}
      </h3>
      <p class="text-gray-500 text-sm mb-3 line-clamp-2">
        {{ attraction.description || '暂无简介' }}
      </p>

      <!-- 地址和查看详情 -->
      <div class="flex items-center justify-between">
        <div class="flex items-center text-gray-400 text-sm">
          <el-icon class="mr-1"><Location /></el-icon>
          <span class="truncate max-w-[150px]">{{ attraction.address || '地址未知' }}</span>
        </div>
        <span class="text-blue-600 text-sm font-medium hover:text-blue-700 flex items-center">
          查看详情
          <el-icon class="ml-1"><ArrowRight /></el-icon>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Star, Location, ArrowRight } from '@element-plus/icons-vue'

const props = defineProps({
  attraction: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const router = useRouter()
const defaultImage = 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop'

// 计算属性：处理显示数据
const displayData = computed(() => ({
  ...props.attraction
}))

function handleClick() {
  router.push(`/attractions/${props.attraction.id}`)
}

function handleImageError(e) {
  e.target.src = defaultImage
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
