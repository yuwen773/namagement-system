<template>
  <div class="bg-white rounded-lg p-4 border border-gray-100 hover:shadow-sm transition-shadow">
    <div class="flex items-start justify-between">
      <!-- 用户信息 -->
      <div class="flex items-center">
        <el-avatar :size="48" :src="comment.user?.avatar" class="bg-blue-500">
          {{ comment.user?.realName?.charAt(0) || comment.user?.username?.charAt(0) || 'U' }}
        </el-avatar>
        <div class="ml-3">
          <div class="flex items-center gap-2">
            <span class="font-medium text-gray-900">
              {{ comment.user?.realName || comment.user?.username || '匿名用户' }}
            </span>
            <!-- 评分星星 -->
            <div class="flex items-center" v-if="comment.rating">
              <el-icon
                v-for="n in 5"
                :key="n"
                :size="14"
                :class="n <= comment.rating ? 'text-yellow-400' : 'text-gray-200'"
              >
                <Star />
              </el-icon>
            </div>
          </div>
          <span class="text-sm text-gray-400">{{ formatDate(comment.createdAt) }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex items-center gap-2" v-if="showDelete">
        <el-button
          type="danger"
          size="small"
          text
          @click="$emit('delete', comment.id)"
        >
          删除
        </el-button>
      </div>
    </div>

    <!-- 评论内容 -->
    <div class="mt-3">
      <p class="text-gray-700 leading-relaxed">{{ comment.content }}</p>
    </div>

    <!-- 景点信息（可选） -->
    <div v-if="comment.attraction" class="mt-3 pt-3 border-t border-gray-100">
      <router-link
        :to="`/attractions/${comment.attraction.id}`"
        class="inline-flex items-center text-sm text-blue-600 hover:text-blue-700"
      >
        <el-icon class="mr-1"><Location /></el-icon>
        {{ comment.attraction.name }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Star, Location } from '@element-plus/icons-vue'
import { formatDate } from '@/utils/date'

const props = defineProps({
  comment: {
    type: Object,
    required: true,
    default: () => ({
      user: {},
      rating: 0
    })
  },
  // 是否显示删除按钮（只显示自己的评论）
  showDelete: {
    type: Boolean,
    default: false
  },
  // 当前登录用户ID，用于判断是否是自己的评论
  currentUserId: {
    type: [Number, String],
    default: null
  }
})

const emit = defineEmits(['delete'])

// 自动判断是否显示删除按钮
const canDelete = computed(() => {
  return props.currentUserId && props.comment.user?.id === props.currentUserId
})

// 暴露 canDelete 给父组件使用
defineExpose({ canDelete })
</script>
