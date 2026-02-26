<template>
  <div class="category-manage">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">分类字典管理</h1>
        <p class="page-subtitle">管理非物质文化遗产分类体系</p>
      </div>
      <el-button type="primary" size="large" @click="handleAdd" class="add-btn">
        <el-icon><Plus /></el-icon>
        <span>新增分类</span>
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="分类名称">
          <el-input v-model="filters.name" placeholder="搜索分类名称" clearable @clear="handleSearch" />
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="filters.level" placeholder="选择级别" clearable>
            <el-option label="国家级" value="national" />
            <el-option label="省级" value="provincial" />
            <el-option label="市县级" value="city_county" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button @click="toggleTreeView">
            {{ showTree ? '列表视图' : '树形视图' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Tree View -->
    <div v-if="showTree" class="tree-section">
      <el-tree
        :data="treeData"
        :props="treeProps"
        node-key="id"
        default-expand-all
        class="category-tree"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <div class="node-content">
              <span class="node-name">{{ data.name }}</span>
              <el-tag size="small" class="node-code">{{ data.code }}</el-tag>
              <el-tag size="small" :type="getLevelType(data.level)">{{ getLevelText(data.level) }}</el-tag>
            </div>
            <div class="node-actions">
              <el-button link type="primary" size="small" @click.stop="handleEdit(data)">编辑</el-button>
              <el-button link type="danger" size="small" @click.stop="handleDelete(data)">删除</el-button>
            </div>
          </div>
        </template>
      </el-tree>
    </div>

    <!-- Table View -->
    <div v-else class="table-section">
      <el-table :data="tableData" v-loading="loading" stripe class="data-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="分类名称" min-width="200" />
        <el-table-column prop="code" label="分类代码" width="150" />
        <el-table-column label="级别" width="120">
          <template #default="{ row }">
            <el-tag :type="getLevelType(row.level)">{{ getLevelText(row.level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="父分类" width="200">
          <template #default="{ row }">
            <span v-if="row.parent">{{ row.parent.name }}</span>
            <span v-else class="text-gray">根分类</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
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

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
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
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
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

const getLevelType = (level: string) => {
  const types: Record<string, any> = {
    national: 'danger',
    provincial: 'warning',
    city_county: 'info'
  }
  return types[level] || 'info'
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
  background: linear-gradient(135deg, #f5f1ed 0%, #faf8f5 100%);
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 32px;
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(139, 69, 19, 0.2);
}

.header-content {
  color: white;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  letter-spacing: 1px;
}

.page-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
}

.add-btn {
  background: white;
  color: #8b4513;
  border: none;
  font-weight: 600;
  padding: 12px 32px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.filter-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-form {
  margin: 0;
}

.tree-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
  background: #faf8f5;
}

.node-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.node-name {
  font-weight: 500;
  color: #333;
}

.node-code {
  font-family: monospace;
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

.table-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.data-table {
  margin-bottom: 24px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

.text-gray {
  color: #999;
  font-style: italic;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background: #f8f5f2;
  color: #8b4513;
  font-weight: 600;
}

:deep(.el-table__row:hover) {
  background: #faf8f5;
}

:deep(.el-button--primary) {
  background: #8b4513;
  border-color: #8b4513;
}

:deep(.el-button--primary:hover) {
  background: #a0522d;
  border-color: #a0522d;
}

:deep(.el-tree-node__content) {
  height: auto;
  padding: 4px 0;
}
</style>
