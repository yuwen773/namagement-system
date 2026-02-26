<template>
  <div class="heritage-manage">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">非遗项目管理</h1>
        <p class="page-subtitle">管理和维护非物质文化遗产项目数据</p>
      </div>
      <el-button type="primary" size="large" @click="handleAdd" class="add-btn">
        <el-icon><Plus /></el-icon>
        <span>新增项目</span>
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="项目名称">
          <el-input v-model="filters.name" placeholder="搜索项目名称" clearable @clear="handleSearch" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filters.category" placeholder="选择分类" clearable>
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="filters.level" placeholder="选择级别" clearable>
            <el-option label="国家级" value="national" />
            <el-option label="省级" value="provincial" />
            <el-option label="市县级" value="city_county" />
          </el-select>
        </el-form-item>
        <el-form-item label="国家">
          <el-select v-model="filters.region" placeholder="选择国家" clearable filterable>
            <el-option v-for="reg in regions" :key="reg.id" :label="reg.country_name" :value="reg.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Table -->
    <div class="table-section">
      <el-table :data="tableData" v-loading="loading" stripe class="data-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="项目名称" min-width="200" />
        <el-table-column label="分类" width="150">
          <template #default="{ row }">
            <el-tag>{{ row.category.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="级别" width="120">
          <template #default="{ row }">
            <el-tag :type="getLevelType(row.level)">{{ getLevelText(row.level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="国家" width="120">
          <template #default="{ row }">
            {{ row.region.country_name }}
          </template>
        </el-table-column>
        <el-table-column prop="area" label="地区" width="150" />
        <el-table-column prop="protection_unit" label="保护单位" min-width="180" show-overflow-tooltip />
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
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="formData.level" placeholder="请选择级别" style="width: 100%">
            <el-option label="国家级" value="national" />
            <el-option label="省级" value="provincial" />
            <el-option label="市县级" value="city_county" />
          </el-select>
        </el-form-item>
        <el-form-item label="国家" prop="region">
          <el-select v-model="formData.region" placeholder="请选择国家" filterable style="width: 100%">
            <el-option v-for="reg in regions" :key="reg.id" :label="reg.country_name" :value="reg.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="地区">
          <el-input v-model="formData.area" placeholder="请输入地区（可选）" />
        </el-form-item>
        <el-form-item label="保护单位">
          <el-input v-model="formData.protection_unit" placeholder="请输入保护单位（可选）" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目简介（可选）"
          />
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
import { getHeritageList, createHeritage, updateHeritage, deleteHeritage } from '@/api/heritage'
import { getCategoryList } from '@/api/category'
import { getRegionList } from '@/api/region'
import type { HeritageItem, HeritageItemCreate, Category, Region } from '@/types'

// State
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增项目')
const currentPage = ref(1)
const total = ref(0)
const tableData = ref<HeritageItem[]>([])
const categories = ref<Category[]>([])
const regions = ref<Region[]>([])
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

// Filters
const filters = reactive({
  name: '',
  category: undefined as number | undefined,
  level: '',
  region: undefined as number | undefined
})

// Form data
const formData = reactive<HeritageItemCreate>({
  name: '',
  category: 0,
  level: 'national',
  region: 0,
  area: '',
  protection_unit: '',
  description: ''
})

// Form rules
const formRules: FormRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  level: [{ required: true, message: '请选择级别', trigger: 'change' }],
  region: [{ required: true, message: '请选择国家', trigger: 'change' }]
}

// Methods
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      name: filters.name || undefined,
      category: filters.category,
      level: filters.level || undefined,
      region: filters.region
    }
    const res = await getHeritageList(params)
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

const fetchCategories = async () => {
  try {
    const res = await getCategoryList({ page: 1 })
    if (res.data.code === 0) {
      categories.value = res.data.data
    }
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

const fetchRegions = async () => {
  try {
    const res = await getRegionList({ page: 1 })
    if (res.data.code === 0) {
      regions.value = res.data.data
    }
  } catch (error) {
    console.error('获取地区失败', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const handleReset = () => {
  filters.name = ''
  filters.category = undefined
  filters.level = ''
  filters.region = undefined
  handleSearch()
}

const handlePageChange = () => {
  fetchData()
}

const handleAdd = () => {
  dialogTitle.value = '新增项目'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: HeritageItem) => {
  dialogTitle.value = '编辑项目'
  editingId.value = row.id
  formData.name = row.name
  formData.category = row.category.id
  formData.level = row.level
  formData.region = row.region.id
  formData.area = row.area || ''
  formData.protection_unit = row.protection_unit || ''
  formData.description = row.description || ''
  dialogVisible.value = true
}

const handleDelete = async (row: HeritageItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目"${row.name}"吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await deleteHeritage(row.id)
    if (res.data.code === 0) {
      ElMessage.success('删除成功')
      fetchData()
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
        const res = await updateHeritage(editingId.value, formData)
        if (res.data.code === 0) {
          ElMessage.success('更新成功')
          dialogVisible.value = false
          fetchData()
        } else {
          ElMessage.error(res.data.message || '更新失败')
        }
      } else {
        const res = await createHeritage(formData)
        if (res.data.code === 0) {
          ElMessage.success('创建成功')
          dialogVisible.value = false
          fetchData()
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
  formData.category = 0
  formData.level = 'national'
  formData.region = 0
  formData.area = ''
  formData.protection_unit = ''
  formData.description = ''
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

// Lifecycle
onMounted(() => {
  fetchData()
  fetchCategories()
  fetchRegions()
})
</script>

<style scoped>
.heritage-manage {
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
</style>
