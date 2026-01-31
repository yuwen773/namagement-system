<template>
  <div class="ingredient-management-page">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a2 2 0 01-2-2V6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          食材管理
        </h1>
        <p class="page-subtitle">管理系统食材数据</p>
      </div>
      <div class="header-actions">
        <button @click="openCreateDialog" class="action-btn create-btn">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 6v6m0 0v6m0-6h6m-6 0H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          新增食材
        </button>
      </div>
    </div>

    <div class="content-wrapper">
      <!-- 搜索和筛选栏 -->
      <div class="toolbar">
        <div class="search-box">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l-4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索食材名称..."
            @keyup.enter="handleSearch"
          >
        </div>

        <div class="filter-group">
          <select v-model="selectedCategory" @change="handleSearch" class="filter-select">
            <option value="">全部分类</option>
            <option v-for="cat in categoryOptions" :key="cat.value" :value="cat.value">
              {{ cat.label }}
            </option>
          </select>
        </div>
      </div>

      <!-- 食材列表 -->
      <div v-loading="loading" class="ingredient-list-container">
        <div v-if="ingredientList.length === 0 && !loading" class="empty-state">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a2 2 0 01-2-2V6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>暂无食材数据</p>
        </div>

        <div v-else class="ingredient-table-wrapper">
          <table class="ingredient-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>食材名称</th>
                <th>分类</th>
                <th>创建时间</th>
                <th>更新时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ingredient in ingredientList" :key="ingredient.id">
                <td class="id-cell">{{ ingredient.id }}</td>
                <td class="name-cell">{{ ingredient.name }}</td>
                <td class="category-cell">
                  <span class="category-badge" :class="ingredient.category">
                    {{ ingredient.category_display || getCategoryLabel(ingredient.category) }}
                  </span>
                </td>
                <td class="time-cell">{{ formatDate(ingredient.created_at) }}</td>
                <td class="time-cell">{{ formatDate(ingredient.updated_at) }}</td>
                <td class="action-cell">
                  <button @click="openEditDialog(ingredient)" class="icon-btn edit-btn" title="编辑">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                  <button @click="handleDelete(ingredient)" class="icon-btn delete-btn" title="删除">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalCount > 0" class="pagination">
        <button @click="handlePrevPage" :disabled="currentPage === 1" class="pagination-btn">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 15l-4-4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          上一页
        </button>
        <span class="pagination-info">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="handleNextPage" :disabled="currentPage >= totalPages" class="pagination-btn">
          下一页
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 15l4-4-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="showEditDialog"
      :title="isEditMode ? '编辑食材' : '新增食材'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="食材名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入食材名称" />
        </el-form-item>
        <el-form-item label="食材分类" prop="category">
          <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%;">
            <el-option
              v-for="cat in categoryOptions"
              :key="cat.value"
              :label="cat.label"
              :value="cat.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminIngredientList, createIngredient, updateIngredient, deleteIngredient, INGREDIENT_CATEGORIES } from '@/api/ingredients'

// 状态
const loading = ref(false)
const ingredientList = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const totalCount = ref(0)

// 对话框状态
const showEditDialog = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentId = ref(null)

// 分类选项
const categoryOptions = INGREDIENT_CATEGORIES

// 表单数据
const formData = ref({
  name: '',
  category: ''
})

// 表单验证规则
const formRules = {
  name: [{ required: true, message: '请输入食材名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择食材分类', trigger: 'change' }]
}

// 计算属性
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))

// 获取分类标签
const getCategoryLabel = (value) => {
  const cat = categoryOptions.find(c => c.value === value)
  return cat ? cat.label : value
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取食材列表
const fetchIngredientList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value || undefined,
      category: selectedCategory.value || undefined
    }
    const res = await getAdminIngredientList(params)
    if (res.code === 200) {
      ingredientList.value = res.data.results || []
      totalCount.value = res.data.count || 0
    }
  } catch (error) {
    console.error('获取食材列表失败:', error)
    ElMessage.error('获取食材列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchIngredientList()
}

// 分页
const handlePrevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchIngredientList()
  }
}

const handleNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchIngredientList()
  }
}

// 打开新增对话框
const openCreateDialog = () => {
  isEditMode.value = false
  currentId.value = null
  formData.value = {
    name: '',
    category: ''
  }
  showEditDialog.value = true
}

// 打开编辑对话框
const openEditDialog = (ingredient) => {
  isEditMode.value = true
  currentId.value = ingredient.id
  formData.value = {
    name: ingredient.name,
    category: ingredient.category
  }
  showEditDialog.value = true
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (isEditMode.value) {
      const res = await updateIngredient(currentId.value, formData.value)
      if (res.code === 200) {
        ElMessage.success('更新成功')
        showEditDialog.value = false
        fetchIngredientList()
      } else {
        ElMessage.error(res.message || '更新失败')
      }
    } else {
      const res = await createIngredient(formData.value)
      if (res.code === 201 || res.code === 200) {
        ElMessage.success('创建成功')
        showEditDialog.value = false
        fetchIngredientList()
      } else {
        ElMessage.error(res.message || '创建失败')
      }
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error(error.response?.data?.message || '操作失败')
  } finally {
    submitting.value = false
  }
}

// 删除食材
const handleDelete = async (ingredient) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除食材 "${ingredient.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const res = await deleteIngredient(ingredient.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      fetchIngredientList()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.message || '删除失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchIngredientList()
})
</script>

<style scoped>
.ingredient-management-page {
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: calc(100vh - 64px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.page-title svg {
  width: 2rem;
  height: 2rem;
  color: #f59e0b;
}

.page-subtitle {
  color: #64748b;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.create-btn {
  background: #f59e0b;
  color: white;
}

.create-btn:hover {
  background: #d97706;
}

.content-wrapper {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.toolbar {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  border-bottom: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  min-width: 250px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f8fafc;
}

.search-box svg {
  width: 1.25rem;
  height: 1.25rem;
  color: #94a3b8;
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.875rem;
  color: #1e293b;
}

.search-box input::placeholder {
  color: #94a3b8;
}

.filter-group {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f8fafc;
  font-size: 0.875rem;
  color: #1e293b;
  cursor: pointer;
  min-width: 140px;
}

.ingredient-list-container {
  padding: 1.25rem;
  min-height: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #94a3b8;
}

.empty-state svg {
  width: 4rem;
  height: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1rem;
}

.ingredient-table-wrapper {
  overflow-x: auto;
}

.ingredient-table {
  width: 100%;
  border-collapse: collapse;
}

.ingredient-table th {
  text-align: left;
  padding: 0.875rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.ingredient-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.875rem;
  color: #334155;
}

.ingredient-table tr:hover td {
  background: #f8fafc;
}

.id-cell {
  font-family: monospace;
  color: #94a3b8;
  font-size: 0.75rem;
}

.name-cell {
  font-weight: 500;
  color: #1e293b;
}

.category-cell {
  text-align: center;
}

.category-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.category-badge.vegetable {
  background: #dcfce7;
  color: #166534;
}

.category-badge.meat {
  background: #fee2e2;
  color: #991b1b;
}

.category-badge.seafood {
  background: #dbeafe;
  color: #1e40af;
}

.category-badge.seasoning {
  background: #fef3c7;
  color: #92400e;
}

.category-badge.fruit {
  background: #fce7f3;
  color: #9d174d;
}

.category-badge.grain {
  background: #f3e8ff;
  color: #6b21a8;
}

.category-badge.dairy {
  background: #cffafe;
  color: #155e75;
}

.category-badge.other {
  background: #f1f5f9;
  color: #475569;
}

.time-cell {
  color: #64748b;
  font-size: 0.75rem;
}

.action-cell {
  text-align: right;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  margin-left: 0.5rem;
}

.icon-btn svg {
  width: 1rem;
  height: 1rem;
}

.edit-btn {
  background: #eff6ff;
  color: #3b82f6;
}

.edit-btn:hover {
  background: #dbeafe;
}

.delete-btn {
  background: #fef2f2;
  color: #ef4444;
}

.delete-btn:hover {
  background: #fee2e2;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  border-top: 1px solid #e2e8f0;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  font-size: 0.875rem;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-btn svg {
  width: 1rem;
  height: 1rem;
}

.pagination-info {
  font-size: 0.875rem;
  color: #64748b;
  min-width: 4rem;
  text-align: center;
}
</style>
