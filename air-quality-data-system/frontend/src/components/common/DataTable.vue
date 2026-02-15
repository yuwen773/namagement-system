<template>
  <div class="data-table-wrapper" :class="{ 'is-dark': theme === 'dark' }">
    <el-table
      ref="tableRef"
      v-loading="loading"
      :data="data"
      :height="height"
      :max-height="maxHeight"
      :stripe="stripe"
      :border="border"
      :show-header="showHeader"
      :highlight-current-row="highlightCurrentRow"
      :row-class-name="rowClassName"
      :cell-class-name="cellClassName"
      :empty-text="emptyText"
      :default-sort="defaultSort"
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
      @current-change="handleCurrentChange"
      @row-click="handleRowClick"
      class="glass-table"
    >
      <!-- Selection column -->
      <el-table-column
        v-if="selectable"
        type="selection"
        width="55"
        :selectable="selectableFn"
        fixed="left"
      />

      <!-- Index column -->
      <el-table-column
        v-if="showIndex"
        type="index"
        label="序号"
        width="70"
        :index="indexMethod"
        fixed="left"
      />

      <!-- Dynamic columns -->
      <template v-for="column in columns" :key="column.prop">
        <el-table-column
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          :min-width="column.minWidth"
          :fixed="column.fixed"
          :sortable="column.sortable"
          :align="column.align || 'left'"
          :show-overflow-tooltip="column.showOverflowTooltip !== false"
        >
          <template #default="scope">
            <slot
              :name="column.prop"
              :row="scope.row"
              :column="column"
              :$index="scope.$index"
            >
              <span v-if="column.formatter">
                {{ column.formatter(scope.row, scope.row[column.prop], scope.$index) }}
              </span>
              <span v-else>
                {{ scope.row[column.prop] }}
              </span>
            </slot>
          </template>

          <!-- Column header slot -->
          <template #header="scope">
            <slot
              :name="`${column.prop}-header`"
              :column="scope.column"
              :$index="scope.$index"
            >
              {{ column.label }}
            </slot>
          </template>
        </el-table-column>
      </template>

      <!-- Action column -->
      <el-table-column
        v-if="$slots.actions"
        label="操作"
        :width="actionWidth"
        :fixed="actionFixed"
        align="center"
      >
        <template #default="scope">
          <slot name="actions" :row="scope.row" :$index="scope.$index" />
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
    <div v-if="pagination && total > 0" class="pagination-wrapper">
      <el-pagination
        :current-page="internalCurrentPage"
        :page-size="internalPageSize"
        :page-sizes="pageSizes"
        :total="total"
        :layout="paginationLayout"
        :background="true"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- Empty state with illustration -->
    <div v-if="!loading && data.length === 0" class="empty-state">
      <slot name="empty">
        <div class="empty-content">
          <svg class="empty-icon" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="80" :stroke="theme === 'dark' ? '#374151' : '#e5e7eb'" stroke-width="8" stroke-dasharray="12 12"/>
            <path d="M100 60V100M100 140V100" :stroke="theme === 'dark' ? '#4b5563' : '#9ca3af'" stroke-width="8" stroke-linecap="round"/>
          </svg>
          <p class="empty-text">{{ emptyText }}</p>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  columns: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(col => col.prop && col.label)
    }
  },
  height: {
    type: [String, Number],
    default: null
  },
  maxHeight: {
    type: [String, Number],
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  stripe: {
    type: Boolean,
    default: true
  },
  border: {
    type: Boolean,
    default: false
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  highlightCurrentRow: {
    type: Boolean,
    default: false
  },
  selectable: {
    type: Boolean,
    default: false
  },
  selectableFn: {
    type: Function,
    default: () => true
  },
  showIndex: {
    type: Boolean,
    default: false
  },
  emptyText: {
    type: String,
    default: '暂无数据'
  },
  pagination: {
    type: Boolean,
    default: true
  },
  total: {
    type: Number,
    default: 0
  },
  pageSize: {
    type: Number,
    default: 20
  },
  currentPage: {
    type: Number,
    default: 1
  },
  pageSizes: {
    type: Array,
    default: () => [10, 20, 50, 100]
  },
  paginationLayout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  },
  defaultSort: {
    type: Object,
    default: () => ({ prop: '', order: '' })
  },
  actionWidth: {
    type: [String, Number],
    default: 200
  },
  actionFixed: {
    type: String,
    default: 'right'
  },
  theme: {
    type: String,
    default: 'light'
  }
})

const emit = defineEmits([
  'sort-change',
  'selection-change',
  'current-change',
  'row-click',
  'page-change',
  'size-change'
])

const tableRef = ref(null)
const internalCurrentPage = ref(props.currentPage)
const internalPageSize = ref(props.pageSize)

watch(() => props.currentPage, (val) => {
  internalCurrentPage.value = val
})

watch(() => props.pageSize, (val) => {
  internalPageSize.value = val
})

const indexMethod = (index) => {
  return (internalCurrentPage.value - 1) * internalPageSize.value + index + 1
}

const handleSortChange = (sort) => {
  emit('sort-change', sort)
}

const handleSelectionChange = (selection) => {
  emit('selection-change', selection)
}

const handleCurrentChange = (currentRow, oldCurrentRow) => {
  emit('current-change', currentRow, oldCurrentRow)
}

const handleRowClick = (row, column, event) => {
  emit('row-click', row, column, event)
}

const handlePageChange = (page) => {
  internalCurrentPage.value = page
  emit('page-change', page)
}

const handleSizeChange = (size) => {
  internalPageSize.value = size
  internalCurrentPage.value = 1
  emit('size-change', size)
}

const rowClassName = ({ row, rowIndex }) => {
  return `table-row-${rowIndex % 2 === 0 ? 'even' : 'odd'}`
}

const cellClassName = ({ column, columnIndex }) => {
  return `table-cell-${columnIndex}`
}

// Expose methods
const clearSelection = () => {
  tableRef.value?.clearSelection()
}

const toggleRowSelection = (row, selected) => {
  tableRef.value?.toggleRowSelection(row, selected)
}

const setCurrentRow = (row) => {
  tableRef.value?.setCurrentRow(row)
}

defineExpose({
  clearSelection,
  toggleRowSelection,
  setCurrentRow,
  tableRef
})
</script>

<style scoped>
.data-table-wrapper {
  width: 100%;
  position: relative;
}

.glass-table {
  background: transparent;
  border-radius: 12px;
  overflow: hidden;
}

.glass-table :deep(.el-table__header-wrapper) {
  background: transparent;
}

.glass-table :deep(.el-table__header) {
  background: transparent;
}

.glass-table :deep(th.el-table__cell) {
  background: transparent;
  border-bottom: 2px solid;
  border-color: v-bind(theme === 'dark' ? '#374151' : '#e5e7eb');
  color: v-bind(theme === 'dark' ? '#9ca3af' : '#6b7280');
  font-weight: 600;
  font-size: 13px;
  padding: 14px 0;
}

.glass-table :deep(td.el-table__cell) {
  border-bottom: 1px solid;
  border-color: v-bind(theme === 'dark' ? '#1f2937' : '#f3f4f6');
  color: v-bind(theme === 'dark' ? '#e5e7eb' : '#1f2937');
  padding: 12px 0;
  transition: all 0.25s ease;
}

.glass-table :deep(tr:hover td) {
  background: v-bind(theme === 'dark' ? 'rgba(59, 130, 246, 0.08)' : 'rgba(59, 130, 246, 0.04)');
}

.glass-table :deep(.el-table__body tr.current-row td) {
  background: v-bind(theme === 'dark' ? 'rgba(59, 130, 246, 0.15)' : 'rgba(59, 130, 246, 0.08)');
}

.glass-table :deep(.el-table__empty-block) {
  background: transparent;
  min-height: 200px;
}

.glass-table :deep(.el-table__empty-text) {
  color: v-bind(theme === 'dark' ? '#6b7280' : '#9ca3af');
}

/* Stripe effect */
.glass-table :deep(.table-row-even) {
  background: v-bind(theme === 'dark' ? 'rgba(255, 255, 255, 0.01)' : 'rgba(0, 0, 0, 0.01)');
}

.glass-table :deep(.table-row-odd) {
  background: transparent;
}

/* Custom scrollbar */
.glass-table :deep(.el-table__body-wrapper) {
  scrollbar-width: thin;
  scrollbar-color: v-bind(theme === 'dark' ? '#4b5563' : '#d1d5db') transparent;
}

.glass-table :deep(.el-table__body-wrapper::-webkit-scrollbar) {
  width: 8px;
  height: 8px;
}

.glass-table :deep(.el-table__body-wrapper::-webkit-scrollbar-track) {
  background: transparent;
}

.glass-table :deep(.el-table__body-wrapper::-webkit-scrollbar-thumb) {
  background: v-bind(theme === 'dark' ? '#4b5563' : '#d1d5db');
  border-radius: 4px;
}

.glass-table :deep(.el-table__body-wrapper::-webkit-scrollbar-thumb:hover) {
  background: v-bind(theme === 'dark' ? '#6b7280' : '#9ca3af');
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px 0;
  margin-top: 16px;
}

.pagination-wrapper :deep(.el-pagination) {
  display: flex;
  gap: 8px;
  align-items: center;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li) {
  background: v-bind(theme === 'dark' ? '#1f2937' : '#f3f4f6');
  color: v-bind(theme === 'dark' ? '#9ca3af' : '#6b7280');
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.25s ease;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li:hover) {
  background: v-bind(theme === 'dark' ? '#374151' : '#e5e7eb');
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.pagination-wrapper :deep(.el-pagination.is-background button) {
  background: v-bind(theme === 'dark' ? '#1f2937' : '#f3f4f6');
  color: v-bind(theme === 'dark' ? '#9ca3af' : '#6b7280');
  border-radius: 8px;
  transition: all 0.25s ease;
}

.pagination-wrapper :deep(.el-pagination.is-background button:hover) {
  background: v-bind(theme === 'dark' ? '#374151' : '#e5e7eb');
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pagination__sizes .el-select .el-input__wrapper) {
  background: v-bind(theme === 'dark' ? '#1f2937' : '#f3f4f6');
  border-radius: 8px;
}

.pagination-wrapper :deep(.el-pagination__total) {
  color: v-bind(theme === 'dark' ? '#9ca3af' : '#6b7280');
  font-weight: 500;
}

.pagination-wrapper :deep(.btn-prev),
.pagination-wrapper :deep(.btn-next) {
  border-radius: 8px;
}

/* Empty state */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.empty-content {
  text-align: center;
}

.empty-icon {
  width: 120px;
  height: 120px;
  opacity: 0.5;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.empty-text {
  margin-top: 16px;
  font-size: 14px;
  color: v-bind(theme === 'dark' ? '#6b7280' : '#9ca3af');
  font-weight: 500;
}

/* Loading overlay */
:deep(.el-loading-mask) {
  background: v-bind(theme === 'dark' ? 'rgba(17, 24, 39, 0.8)' : 'rgba(255, 255, 255, 0.8)');
  backdrop-filter: blur(8px);
  border-radius: 12px;
}

:deep(.el-loading-spinner .circular) {
  stroke: v-bind(theme === 'dark' ? '#60a5fa' : '#3b82f6');
}
</style>
