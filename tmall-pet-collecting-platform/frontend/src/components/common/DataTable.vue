<script setup>
import { ref, computed, watch } from 'vue'
import { Search, Refresh, Download } from '@element-plus/icons-vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  columns: {
    type: Array,
    default: () => []
  },
  total: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  },
  searchable: {
    type: Boolean,
    default: true
  },
  exportable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['refresh', 'search', 'export', 'selection-change'])

const searchKeyword = ref('')
const tableRef = ref(null)

const hasSelection = computed(() => {
  return props.columns.some(col => col.type === 'selection')
})

const handleSearch = () => {
  emit('search', searchKeyword.value)
}

const handleRefresh = () => {
  searchKeyword.value = ''
  emit('refresh')
}

const handleExport = () => {
  emit('export')
}

const handleSelectionChange = (selection) => {
  emit('selection-change', selection)
}
</script>

<template>
  <div class="data-table-container">
    <!-- 工具栏 -->
    <div class="table-toolbar">
      <div class="toolbar-left">
        <div v-if="searchable" class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索..."
            :prefix-icon="Search"
            clearable
            class="search-input"
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          />
          <button class="action-btn search-btn" @click="handleSearch">
            <Search class="icon" />
          </button>
        </div>
      </div>

      <div class="toolbar-right">
        <button class="action-btn" @click="handleRefresh">
          <Refresh class="icon" />
          <span>刷新</span>
        </button>

        <button v-if="exportable" class="action-btn export-btn" @click="handleExport">
          <Download class="icon" />
          <span>导出</span>
        </button>
      </div>
    </div>

    <!-- 表格 -->
    <div class="table-wrapper">
      <el-table
        ref="tableRef"
        :data="data"
        :loading="loading"
        stripe
        class="custom-table"
        @selection-change="handleSelectionChange"
      >
        <template v-for="column in columns" :key="column.prop">
          <el-table-column
            v-if="column.type === 'selection'"
            type="selection"
            width="55"
          />
          <el-table-column
            v-else-if="column.type === 'index'"
            type="index"
            label="#"
            width="60"
            :index="index => (props.page - 1) * props.pageSize + index + 1"
          />
          <el-table-column
            v-else
            :prop="column.prop"
            :label="column.label"
            :width="column.width"
            :min-width="column.minWidth"
            :sortable="column.sortable"
          >
            <template #default="{ row }">
              <slot v-if="column.slot" :name="column.slot" :row="row" />
              <span v-else>{{ row[column.prop] }}</span>
            </template>
          </el-table-column>
        </template>

        <template #empty>
          <div class="empty-state">
            <div class="empty-icon">📦</div>
            <p class="empty-text">暂无数据</p>
          </div>
        </template>
      </el-table>
    </div>

    <!-- 分页 -->
    <Pagination
      v-if="total > 0"
      :page="page"
      :page-size="pageSize"
      :total="total"
      @update:page="$emit('update:page', $event)"
      @update:page-size="$emit('update:pageSize', $event)"
      @change="$emit('change', $event)"
    />
  </div>
</template>

<style scoped>
.data-table-container {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

/* 工具栏 */
.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  gap: 16px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-box {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.search-box:focus-within {
  border-color: rgba(255, 107, 53, 0.3);
  box-shadow: 0 0 20px rgba(255, 107, 53, 0.1);
}

.search-input {
  flex: 1;
}

.search-input :deep(.el-input__wrapper) {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 10px 16px;
}

.search-input :deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.search-input :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.search-input :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.4);
}

.search-btn {
  padding: 10px 16px;
  background: rgba(255, 107, 53, 0.1);
  border-left: 1px solid rgba(255, 255, 255, 0.08);
}

.search-btn:hover {
  background: rgba(255, 107, 53, 0.2);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.9);
}

.export-btn:hover {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.3);
  color: #FF6B35;
}

.action-btn .icon {
  width: 16px;
  height: 16px;
}

/* 表格包装器 */
.table-wrapper {
  padding: 0 24px;
}

.custom-table {
  background: transparent;
}

:deep(.el-table__inner-wrapper) {
  background: transparent;
}

:deep(.el-table) {
  background: transparent;
  color: rgba(255, 255, 255, 0.9);
}

:deep(.el-table tr) {
  background: transparent;
}

:deep(.el-table th.el-table__cell) {
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.5);
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 16px 12px;
}

:deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  padding: 16px 12px;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: rgba(255, 255, 255, 0.02);
}

:deep(.el-table__body tr:hover > td) {
  background: rgba(255, 107, 53, 0.05) !important;
}

:deep(.el-table__empty-text) {
  color: rgba(255, 255, 255, 0.4);
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .table-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-left,
  .toolbar-right {
    width: 100%;
    justify-content: space-between;
  }

  .search-box {
    flex: 1;
  }
}
</style>
