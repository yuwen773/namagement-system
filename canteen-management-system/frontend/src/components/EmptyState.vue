<template>
  <div class="empty-state">
    <el-empty :description="description">
      <template #image>
        <el-icon :size="80" :color="iconColor">
          <component :is="iconComponent" />
        </el-icon>
      </template>
      <template v-if="showButton">
        <el-button type="primary" @click="$emit('action')" :size="buttonSize">
          {{ buttonText }}
        </el-button>
      </template>
    </el-empty>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Document, Picture, User, Calendar, Box, Warning } from '@element-plus/icons-vue'

/**
 * 空状态组件
 * 用于在列表或页面无数据时显示友好的空状态提示
 */

// 定义 props
const props = defineProps({
  /** 描述文字 */
  description: {
    type: String,
    default: '暂无数据'
  },
  /** 图标类型 */
  icon: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'document', 'picture', 'user', 'calendar', 'box', 'warning'].includes(value)
  },
  /** 是否显示操作按钮 */
  showButton: {
    type: Boolean,
    default: false
  },
  /** 按钮文字 */
  buttonText: {
    type: String,
    default: '立即创建'
  },
  /** 按钮尺寸 */
  buttonSize: {
    type: String,
    default: 'default',
    validator: (value) => ['large', 'default', 'small'].includes(value)
  },
  /** 图标颜色 */
  iconColor: {
    type: String,
    default: '#CCCCCC'
  }
})

// 定义事件
defineEmits(['action'])

// 根据图标类型返回对应的图标组件
const iconComponent = computed(() => {
  const iconMap = {
    default: Box,
    document: Document,
    picture: Picture,
    user: User,
    calendar: Calendar,
    box: Box,
    warning: Warning
  }
  return iconMap[props.icon] || Box
})
</script>

<style scoped>
.empty-state {
  padding: var(--canteen-spacing-xl) 0;
  text-align: center;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 响应式：小屏幕下减少内边距 */
@media (max-width: 768px) {
  .empty-state {
    padding: var(--canteen-spacing-lg) 0;
    min-height: 200px;
  }
}
</style>
