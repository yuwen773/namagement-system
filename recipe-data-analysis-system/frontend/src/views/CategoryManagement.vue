
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">分类管理</h1>
        <p class="text-gray-500 mt-1 text-sm">管理系统中的所有分类标签，包括菜系、场景、人群等</p>
      </div>
      <el-button type="primary" size="large" @click="handleAdd" class="!px-6">
        <el-icon class="mr-2"><Plus /></el-icon>
        新增分类
      </el-button>
    </div>

    <!-- Main Content -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
      <!-- Tabs & Search -->
      <div class="p-4 border-b border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
        <el-tabs v-model="activeTab" class="w-full md:w-auto">
          <el-tab-pane label="全部" name="all" />
          <el-tab-pane 
            v-for="item in categoryTypes" 
            :key="item.value" 
            :label="item.label" 
            :name="item.value" 
          />
        </el-tabs>
        
        <div class="w-full md:w-64">
          <el-input
            v-model="searchQuery"
            placeholder="搜索分类名称..."
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon class="text-gray-400"><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>

      <!-- Table -->
      <el-table 
        v-loading="loading"
        :data="categoryList" 
        style="width: 100%"
        :header-cell-style="{ background: '#f9fafb', color: '#374151', fontWeight: '600' }"
      >
        <el-table-column prop="id" label="ID" width="80" align="center" />
        
        <el-table-column prop="name" label="分类名称" min-width="150">
          <template #default="{ row }">
            <span class="font-medium text-gray-900">{{ row.name }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="type_display" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeTagEffect(row.type)" effect="light" round size="small">
              {{ row.type_display }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="sort_order" label="排序" width="100" align="center">
          <template #default="{ row }">
            <span class="text-gray-500 font-mono">{{ row.sort_order }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>

        <template #empty>
          <el-empty description="暂无分类数据" />
        </template>
      </el-table>

      <!-- Pagination -->
      <div class="p-4 border-t border-gray-100 flex justify-end">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
        />
      </div>
    </div>

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑分类' : '新增分类'"
      width="500px"
      destroy-on-close
      class="rounded-lg"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
        class="mt-4"
        status-icon
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择分类类型" class="w-full">
            <el-option
              v-for="item in categoryTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" :max="9999" controls-position="right" class="!w-full" />
          <div class="text-xs text-gray-400 mt-1">数值越小越靠前 (0-9999)</div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api/categories'

// Constants
const categoryTypes = api.CATEGORY_TYPES

// State
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const activeTab = ref('all')
const searchQuery = ref('')
const categoryList = ref([])
const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

// Form
const formRef = ref(null)
const form = reactive({
  id: null,
  name: '',
  type: '',
  sort_order: 0
})

const rules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择分类类型', trigger: 'change' }
  ],
  sort_order: [
    { required: true, message: '请输入排序序号', trigger: 'blur' }
  ]
}

// Helper: Get tag type based on category type
const getTypeTagEffect = (type) => {
  const map = {
    'cuisine': 'danger',
    'scene': 'success',
    'crowd': 'warning',
    'taste': 'info',
    'difficulty': ''
  }
  return map[type] || ''
}

// API: Fetch List
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      search: searchQuery.value
    }
    
    if (activeTab.value !== 'all') {
      params.type = activeTab.value
    }
    
    const res = await api.getAdminCategoryList(params)
    if (res.code === 200) {
      categoryList.value = res.data.results
      pagination.total = res.data.count
    }
  } catch (error) {
    console.error('Failed to fetch categories:', error)
    ElMessage.error('获取分类列表失败')
  } finally {
    loading.value = false
  }
}

// Handlers
const handleSearch = () => {
  pagination.currentPage = 1
  fetchData()
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
  fetchData()
}

const handleCurrentChange = (val) => {
  pagination.currentPage = val
  fetchData()
}

const handleAdd = () => {
  isEdit.value = false
  form.id = null
  form.name = ''
  form.type = activeTab.value !== 'all' ? activeTab.value : ''
  form.sort_order = 0
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.id = row.id
  form.name = row.name
  form.type = row.type
  form.sort_order = row.sort_order
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除分类 "${row.name}" 吗？此操作不可恢复。`,
    '警告',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const res = await api.deleteCategory(row.id)
      if (res.code === 200) {
        ElMessage.success('删除成功')
        fetchData()
      } else {
        ElMessage.error(res.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除操作失败')
    }
  }).catch(() => {})
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        let res
        if (isEdit.value) {
          res = await api.updateCategory(form.id, form)
        } else {
          res = await api.createCategory(form)
        }
        
        if (res.code === 200 || res.code === 201) {
          ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
          dialogVisible.value = false
          fetchData()
        } else {
          ElMessage.error(res.message || (isEdit.value ? '更新失败' : '创建失败'))
        }
      } catch (error) {
        ElMessage.error('提交失败，请稍后重试')
      } finally {
        submitting.value = false
      }
    }
  })
}

// Watchers
watch(activeTab, () => {
  pagination.currentPage = 1
  fetchData()
})

watch(searchQuery, (newVal) => {
  if (newVal === '') {
    handleSearch()
  }
})

// Lifecycle
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.el-table {
  --el-table-header-bg-color: #f9fafb;
}
</style>
