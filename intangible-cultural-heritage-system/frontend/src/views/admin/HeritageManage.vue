<template>
  <div class="heritage-manage">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-seal">
          <span class="seal-text">管理</span>
        </div>
        <div class="header-texts">
          <h1 class="page-title">非遗项目管理</h1>
          <p class="page-subtitle">管理和维护非物质文化遗产项目数据</p>
        </div>
      </div>
      <button class="add-btn" @click="handleAdd">
        <span class="btn-seal">增</span>
        <span>新增项目</span>
      </button>
    </header>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="项目名称">
          <el-input v-model="filters.name" placeholder="搜索项目名称" clearable @clear="handleSearch" class="heritage-input" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filters.category" placeholder="选择分类" clearable class="heritage-select" style="width: 120px;">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="filters.level" placeholder="选择级别" clearable class="heritage-select" style="width: 120px;">
            <el-option label="国家级" value="national" />
            <el-option label="省级" value="provincial" />
            <el-option label="市县级" value="city_county" />
          </el-select>
        </el-form-item>
        <el-form-item label="国家">
          <el-select v-model="filters.region" placeholder="选择国家" clearable filterable class="heritage-select">
            <el-option v-for="reg in regions" :key="reg.id" :label="reg.country_name" :value="reg.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <button type="button" class="action-btn search-btn" @click="handleSearch">搜索</button>
          <button type="button" class="action-btn reset-btn" @click="handleReset">重置</button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 表格区域 -->
    <div class="table-frame">
      <el-table :data="tableData" v-loading="loading" class="data-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="项目名称" min-width="200" />
        <el-table-column label="分类" width="150">
          <template #default="{ row }">
            <span class="category-tag">{{ row.category.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="级别" width="120">
          <template #default="{ row }">
            <span class="level-badge" :class="getLevelClass(row.level)">
              {{ getLevelText(row.level) }}
            </span>
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
      width="600px"
      :close-on-click-modal="false"
      class="heritage-dialog"
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
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(194, 35, 49, 0.3);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-seal {
  width: 56px;
  height: 56px;
  background: #D4AF37;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.seal-text {
  font-size: 20px;
  font-weight: 700;
  color: #2F3640;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 2px;
}

.header-texts {
  color: white;
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
  opacity: 0.9;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #C23531;
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
  background: #C23531;
  color: white;
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
  background: #C23531;
  color: white;
}

.search-btn:hover {
  background: #A93226;
}

.reset-btn {
  background: #F7F4ED;
  color: #606266;
  margin-left: 8px;
}

.reset-btn:hover {
  background: #EDF2ED;
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

.category-tag {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  border-radius: 12px;
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
  background: #C23531 !important;
  border-color: #C23531 !important;
}

/* ========== 弹窗 ========== */
:deep(.heritage-dialog .el-dialog__header) {
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  color: white;
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
  background: #C23531;
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background: #A93226;
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
