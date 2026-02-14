<template>
  <div class="flex justify-center py-6">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="pageSizes"
      :total="total"
      :layout="layout"
      :background="background"
      :small="small"
      :disabled="disabled"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // 当前页码
  modelValue: {
    type: Number,
    default: 1
  },
  // 每页条数
  pageSize: {
    type: Number,
    default: 10
  },
  // 总数据条数
  total: {
    type: Number,
    default: 0
  },
  // 每页条数选项
  pageSizes: {
    type: Array,
    default: () => [10, 20, 50, 100]
  },
  // 分页布局
  layout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  },
  // 是否使用背景色
  background: {
    type: Boolean,
    default: true
  },
  // 是否使用小尺寸
  small: {
    type: Boolean,
    default: false
  },
  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'update:pageSize', 'size-change', 'current-change'])

// 双向绑定当前页码
const currentPage = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 处理每页条数变化
function handleSizeChange(size) {
  emit('update:pageSize', size)
  emit('size-change', size)
  // 切换每页条数时，重置到第一页
  currentPage.value = 1
}

// 处理页码变化
function handleCurrentChange(page) {
  emit('update:modelValue', page)
  emit('current-change', page)
}
</script>

<style scoped>
/* 自定义分页样式 */
:deep(.el-pagination) {
  --el-pagination-bg-color: #f5f7fa;
  --el-pagination-button-bg-color: #fff;
  --el-pagination-hover-color: #409eff;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #409eff;
}
</style>
