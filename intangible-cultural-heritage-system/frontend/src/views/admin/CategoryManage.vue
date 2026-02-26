<template>
  <div class="category-manage">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-seal">
          <span class="seal-text">分类</span>
        </div>
        <div class="header-texts">
          <h1 class="page-title">分类字典管理</h1>
          <p class="page-subtitle">管理非物质文化遗产分类体系</p>
        </div>
      </div>
      <button class="add-btn" @click="handleAdd">
        <span class="btn-seal">增</span>
        <span>新增分类</span>
      </button>
    </header>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="分类名称">
          <el-input v-model="filters.name" placeholder="搜索分类名称" clearable @clear="handleSearch" class="heritage-input" />
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="filters.level" placeholder="选择级别" clearable class="heritage-select">
            <el-option label="国家级" value="national" />
            <el-option label="省级" value="provincial" />
            <el-option label="市县级" value="city_county" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <button class="action-btn search-btn" @click="handleSearch">搜索</button>
          <button class="action-btn reset-btn" @click="handleReset">重置</button>
          <button class="action-btn toggle-btn" @click="toggleTreeView">
            {{ showTree ? '列表视图' : '树形视图' }}
          </button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 树形视图 -->
    <div v-if="showTree" class="tree-section">
      <el-tree
        :data="treeData"
        :props="treeProps"
        node-key="id"
        default-expand-all
        class="category-tree"
      >
        <template #default="{ data }">
          <div class="tree-node">
            <div class="node-content">
              <span class="node-name">{{ data.name }}</span>
              <span class="node-code">{{ data.code }}</span>
              <span class="level-badge" :class="getLevelClass(data.level)">
                {{ getLevelText(data.level) }}
              </span>
            </div>
            <div class="node-actions">
              <button class="node-btn edit-btn" @click.stop="handleEdit(data)">编辑</button>
              <button class="node-btn delete-btn" @click.stop="handleDelete(data)">删除</button>
            </div>
          </div>
        </template>
      </el-tree>
    </div>

    <!-- 列表视图 -->
    <div v-else class="table-frame">
      <el-table :data="tableData" v-loading="loading" class="data-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="分类名称" min-width="200" />
        <el-table-column prop="code" label="分类代码" width="150" />
        <el-table-column label="级别" width="120">
          <template #default="{ row }">
            <span class="level-badge" :class="getLevelClass(row.level)">
              {{ getLevelText(row.level) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="父分类" width="200">
          <template #default="{ row }">
            <span v-if="row.parent">{{ row.parent.name }}</span>
            <span v-else class="empty-text">根分类</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <button class="table-action-btn edit-btn" @click="handleEdit(row)">编辑</button>
            <button class="table-action-btn delete-btn" @click="handleDelete(row)">删除</button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="20"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      class="heritage-dialog"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="分类代码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入分类代码（如：CAT001）" />
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="formData.level" placeholder="请选择级别" style="width: 100%">
            <el-option label="国家级" value="national" />
            <el-option label="省级" value="provincial" />
            <el-option label="市县级" value="city_county" />
          </el-select>
        </el-form-item>
        <el-form-item label="父分类">
          <el-select v-model="formData.parent" placeholder="请选择父分类（可选）" clearable filterable style="width: 100%">
            <el-option
              v-for="cat in allCategories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
              :disabled="editingId === cat.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="dialog-btn cancel-btn" @click="dialogVisible = false">取消</button>
        <button class="dialog-btn confirm-btn" @click="handleSubmit" :disabled="submitting">
          {{ submitting ? '提交中...' : '确定' }}
        </button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { getCategoryList, getCategoryTree, createCategory, updateCategory, deleteCategory } from '@/api/category'
import type { Category, CategoryTree } from '@/types'

// State
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增分类')
const showTree = ref(false)
const currentPage = ref(1)
const total = ref(0)
const tableData = ref<Category[]>([])
const treeData = ref<CategoryTree[]>([])
const allCategories = ref<Category[]>([])
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

// Tree props
const treeProps = {
  children: 'children',
  label: 'name'
}

// Filters
const filters = reactive({
  name: '',
  level: ''
})

// Form data
const formData = reactive({
  name: '',
  code: '',
  level: 'national',
  parent: undefined as number | undefined
})

// Form rules
const formRules: FormRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入分类代码', trigger: 'blur' }],
  level: [{ required: true, message: '请选择级别', trigger: 'change' }]
}

// Methods
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      name: filters.name || undefined,
      level: filters.level || undefined
    }
    const res = await getCategoryList(params)
    if (res.data.code === 0) {
      tableData.value = res.data.data
      total.value = res.data.total || 0
    }
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const fetchTreeData = async () => {
  try {
    const res = await getCategoryTree()
    if (res.data.code === 0) {
      treeData.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取树形数据失败')
  }
}

const fetchAllCategories = async () => {
  try {
    const res = await getCategoryList({ page: 1 })
    if (res.data.code === 0) {
      allCategories.value = res.data.data
    }
  } catch (error) {
    console.error('获取分类列表失败', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  if (showTree.value) {
    fetchTreeData()
  } else {
    fetchData()
  }
}

const handleReset = () => {
  filters.name = ''
  filters.level = ''
  handleSearch()
}

const handlePageChange = () => {
  fetchData()
}

const toggleTreeView = () => {
  showTree.value = !showTree.value
  if (showTree.value) {
    fetchTreeData()
  } else {
    fetchData()
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增分类'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: Category) => {
  dialogTitle.value = '编辑分类'
  editingId.value = row.id
  formData.name = row.name
  formData.code = row.code
  formData.level = row.level
  formData.parent = row.parent_id || undefined
  dialogVisible.value = true
}

const handleDelete = async (row: Category) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类"${row.name}"吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await deleteCategory(row.id)
    if (res.data.code === 0) {
      ElMessage.success('删除成功')
      if (showTree.value) {
        fetchTreeData()
      } else {
        fetchData()
      }
    } else {
      ElMessage.error(res.data.message || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      if (editingId.value) {
        const res = await updateCategory(editingId.value, formData)
        if (res.data.code === 0) {
          ElMessage.success('更新成功')
          dialogVisible.value = false
          if (showTree.value) {
            fetchTreeData()
          } else {
            fetchData()
          }
          fetchAllCategories()
        } else {
          ElMessage.error(res.data.message || '更新失败')
        }
      } else {
        const res = await createCategory(formData)
        if (res.data.code === 0) {
          ElMessage.success('创建成功')
          dialogVisible.value = false
          if (showTree.value) {
            fetchTreeData()
          } else {
            fetchData()
          }
          fetchAllCategories()
        } else {
          ElMessage.error(res.data.message || '创建失败')
        }
      }
    } catch (error) {
      ElMessage.error('操作失败')
    } finally {
      submitting.value = false
    }
  })
}

const resetForm = () => {
  formData.name = ''
  formData.code = ''
  formData.level = 'national'
  formData.parent = undefined
  formRef.value?.clearValidate()
}

const getLevelClass = (level: string) => {
  return `level-${level}`
}

const getLevelText = (level: string) => {
  const texts: Record<string, string> = {
    national: '国家级',
    provincial: '省级',
    city_county: '市县级'
  }
  return texts[level] || level
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// Lifecycle
onMounted(() => {
  fetchData()
  fetchAllCategories()
})
</script>

<style scoped>
.category-manage {
  padding: 24px;
  background: #F7F4ED;
  min-height: calc(100vh - 60px);
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #D4AF37 0%, #CD7F32 100%);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-seal {
  width: 56px;
  height: 56px;
  background: #2F3640;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(47, 54, 64, 0.4);
}

.seal-text {
  font-size: 20px;
  font-weight: 700;
  color: #F7F4ED;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 2px;
}

.header-texts {
  color: #2F3640;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
}

.page-subtitle {
  font-size: 13px;
  margin: 0;
  opacity: 0.8;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #CD7F32;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.btn-seal {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #D4AF37;
  color: #2F3640;
  font-size: 12px;
  font-weight: 600;
  border-radius: 2px;
  font-family: "STSong", "SimSun", serif;
}

/* ========== 筛选区域 ========== */
.filter-section {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.filter-form {
  margin: 0;
}

:deep(.heritage-input .el-input__wrapper),
:deep(.heritage-select .el-select__wrapper) {
  background: #F7F4ED;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
}

.action-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn {
  background: #D4AF37;
  color: #2F3640;
}

.search-btn:hover {
  background: #CD7F32;
}

.reset-btn {
  background: #F7F4ED;
  color: #606266;
  margin-left: 8px;
}

.reset-btn:hover {
  background: #EDF2ED;
}

.toggle-btn {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  margin-left: 8px;
}

.toggle-btn:hover {
  background: rgba(212, 175, 55, 0.25);
}

/* ========== 树形视图 ========== */
.tree-section {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.category-tree {
  font-size: 14px;
}

.tree-node {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.tree-node:hover {
  background: rgba(212, 175, 55, 0.08);
}

.node-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.node-name {
  font-weight: 500;
  color: #2F3640;
}

.node-code {
  font-family: monospace;
  color: #909399;
  font-size: 12px;
}

.level-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

.level-badge.level-national {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
}

.level-badge.level-provincial {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
}

.level-badge.level-city_county {
  background: rgba(93, 138, 168, 0.15);
  color: #5D8AA8;
}

.node-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tree-node:hover .node-actions {
  opacity: 1;
}

.node-btn {
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.node-btn.edit-btn {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
}

.node-btn.edit-btn:hover {
  background: #D4AF37;
  color: white;
}

.node-btn.delete-btn {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
}

.node-btn.delete-btn:hover {
  background: #C23531;
  color: white;
}

/* ========== 表格区域 ========== */
.table-frame {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.data-table {
  margin-bottom: 24px;
}

:deep(.data-table th) {
  background: #F7F4ED !important;
  color: #2F3640 !important;
  font-weight: 600 !important;
}

:deep(.data-table tr:hover) {
  background: rgba(212, 175, 55, 0.05) !important;
}

.empty-text {
  color: #C0C4CC;
  font-style: italic;
}

.table-action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-btn {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  margin-right: 8px;
}

.edit-btn:hover {
  background: #D4AF37;
  color: white;
}

.delete-btn {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
}

.delete-btn:hover {
  background: #C23531;
  color: white;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

:deep(.el-pagination .el-pager li.is-active) {
  background: #D4AF37 !important;
  border-color: #D4AF37 !important;
  color: #2F3640 !important;
}

/* ========== 弹窗 ========== */
:deep(.heritage-dialog .el-dialog__header) {
  background: linear-gradient(135deg, #D4AF37 0%, #CD7F32 100%);
  color: #2F3640;
  padding: 20px 24px;
  border-radius: 8px 8px 0 0;
}

:deep(.heritage-dialog .el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 2px;
  font-family: "STSong", "SimSun", serif;
}

.dialog-btn {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: #F7F4ED;
  color: #606266;
  margin-right: 12px;
}

.cancel-btn:hover {
  background: #EDF2ED;
}

.confirm-btn {
  background: #D4AF37;
  color: #2F3640;
}

.confirm-btn:hover:not(:disabled) {
  background: #CD7F32;
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
