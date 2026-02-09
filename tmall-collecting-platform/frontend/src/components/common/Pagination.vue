<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 20
  },
  total: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:currentPage', 'update:pageSize', 'page-change', 'page-size-change'])

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const startRecord = computed(() => {
  if (props.total === 0) return 0
  return (props.currentPage - 1) * props.pageSize + 1
})

const endRecord = computed(() => {
  const end = props.currentPage * props.pageSize
  return end > props.total ? props.total : end
})

const handleCurrentChange = (page) => {
  emit('update:currentPage', page)
  emit('page-change', page)
}

const handleSizeChange = (size) => {
  emit('update:pageSize', size)
  emit('page-size-change', size)
}
</script>

<template>
  <div class="pagination-wrapper">
    <div class="pagination-info">
      <span class="info-text">
        显示 <strong>{{ startRecord }}</strong> - <strong>{{ endRecord }}</strong>
        条，共 <strong>{{ total }}</strong> 条
      </span>
    </div>

    <el-pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :total="total"
      layout="sizes, prev, pager, next, jumper"
      background
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<style scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  margin-top: 24px;
}

.pagination-info {
  display: flex;
  align-items: center;
}

.info-text {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.info-text strong {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 700;
}

:deep(.el-pagination) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-pagination.is-background .el-pager li) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  font-weight: 600;
  min-width: 32px;
  height: 32px;
  line-height: 32px;
}

:deep(.el-pagination.is-background .el-pager li:hover) {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.3);
  color: #FF6B35;
}

:deep(.el-pagination.is-background .el-pager li.is-active) {
  background: linear-gradient(135deg, #FF6B35, #7B2CBF);
  border-color: transparent;
  color: white;
}

:deep(.el-pagination.is-background .btn-prev),
:deep(.el-pagination.is-background .btn-next) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  min-width: 32px;
  height: 32px;
}

:deep(.el-pagination.is-background .btn-prev:hover),
:deep(.el-pagination.is-background .btn-next:hover) {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.3);
  color: #FF6B35;
}

:deep(.el-pagination.is-background .el-pagination__sizes .el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  box-shadow: none;
}

:deep(.el-pagination.is-background .el-pagination__jump) {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

:deep(.el-pagination.is-background .el-pagination__jump .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  box-shadow: none;
}

@media (max-width: 768px) {
  .pagination-wrapper {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }

  .pagination-info {
    width: 100%;
    justify-content: center;
  }
}
</style>
