<template>
  <div class="performance-template">
    <div class="page-header">
      <h2>绩效考核模板管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建模板
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="状态">
          <el-select v-model="filterForm.is_active" placeholder="全部" clearable style="width: 120px">
            <el-option label="启用" value="true" />
            <el-option label="停用" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="handleResetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 模板列表 -->
    <el-card>
      <el-table
        v-loading="tableLoading"
        :data="templateList"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="name" label="模板名称" min-width="150" />
        <el-table-column prop="description" label="描述" min-width="200">
          <template #default="{ row }">
            <span>{{ row.description || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="items" label="考核项数量" width="120" align="center">
          <template #default="{ row }">
            <el-tag type="info">{{ row.items_count || 0 }} 项</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_weight" label="总权重" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.total_weight === 100 ? 'success' : 'warning'">
              {{ row.total_weight }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.active_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button
              link
              :type="row.is_active ? 'warning' : 'success'"
              @click="handleToggleActive(row)"
            >
              {{ row.is_active ? '停用' : '启用' }}
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建模板' : '编辑模板'"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="模板名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入模板名称" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            placeholder="请输入模板描述"
            :rows="2"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="formData.is_active" active-text="启用" inactive-text="停用" />
        </el-form-item>

        <!-- 考核项设计器 -->
        <el-form-item label="考核项" prop="items">
          <div class="items-designer">
            <div class="items-header">
              <span class="item-name">考核项名称</span>
              <span class="item-weight">权重(%)</span>
              <span class="item-desc">说明</span>
              <span class="item-action">操作</span>
            </div>
            <div
              v-for="(item, index) in formData.items"
              :key="index"
              class="item-row"
            >
              <el-input
                v-model="item.name"
                placeholder="如：工作质量"
                class="item-name-input"
              />
              <el-input-number
                v-model="item.weight"
                :min="0"
                :max="100"
                :step="5"
                controls-position="right"
                class="item-weight-input"
              />
              <el-input
                v-model="item.desc"
                placeholder="考核项说明"
                class="item-desc-input"
              />
              <el-button
                type="danger"
                :icon="Delete"
                circle
                size="small"
                @click="removeItem(index)"
              />
            </div>
            <div class="items-footer">
              <el-button type="primary" plain size="small" @click="addItem">
                <el-icon><Plus /></el-icon>
                添加考核项
              </el-button>
              <span class="weight-summary">
                当前总权重：
                <el-tag :type="currentTotalWeight === 100 ? 'success' : 'warning'">
                  {{ currentTotalWeight }}%
                </el-tag>
                <span v-if="currentTotalWeight !== 100" class="weight-warning">
                  （建议总权重为100%）
                </span>
              </span>
            </div>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 查看详情弹窗 -->
    <el-dialog v-model="viewDialogVisible" title="模板详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="模板名称">
          {{ currentTemplate.name }}
        </el-descriptions-item>
        <el-descriptions-item label="描述">
          {{ currentTemplate.description || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentTemplate.is_active ? 'success' : 'danger'">
            {{ currentTemplate.active_status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="考核项">
          <el-table :data="currentTemplate.items || []" size="small" border>
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="name" label="考核项" />
            <el-table-column prop="weight" label="权重" width="80">
              <template #default="{ row }">
                {{ row.weight }}%
              </template>
            </el-table-column>
            <el-table-column prop="desc" label="说明" />
          </el-table>
        </el-descriptions-item>
        <el-descriptions-item label="总权重">
          <el-tag :type="currentTemplate.total_weight === 100 ? 'success' : 'warning'">
            {{ currentTemplate.total_weight }}%
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDateTime(currentTemplate.created_at) }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'
import {
  getPerformanceTemplateList,
  getPerformanceTemplateDetail,
  createPerformanceTemplate,
  updatePerformanceTemplate,
  deletePerformanceTemplate,
  togglePerformanceTemplateActive
} from '@/api/performance'
import { formatDateTime } from '@/utils/format'

// 筛选表单
const filterForm = ref({
  is_active: ''
})

// 表格数据
const tableLoading = ref(false)
const templateList = ref([])

// 弹窗控制
const dialogVisible = ref(false)
const dialogType = ref('create')
const viewDialogVisible = ref(false)
const submitLoading = ref(false)
const formRef = ref(null)
const currentTemplate = ref({})

// 表单数据
const formData = ref({
  name: '',
  description: '',
  is_active: true,
  items: [
    { name: '', weight: 0, desc: '' }
  ]
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
    { min: 2, max: 100, message: '模板名称长度在 2-100 个字符', trigger: 'blur' }
  ],
  items: [
    {
      validator: (rule, value, callback) => {
        if (!value || value.length === 0) {
          callback(new Error('请至少添加一个考核项'))
        } else if (value.some(item => !item.name)) {
          callback(new Error('请完善所有考核项名称'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算当前总权重
const currentTotalWeight = computed(() => {
  return formData.value.items.reduce((sum, item) => sum + (item.weight || 0), 0)
})

// 获取模板列表
const fetchTemplateList = async () => {
  tableLoading.value = true
  try {
    const params = {}
    if (filterForm.value.is_active) {
      params.is_active = filterForm.value.is_active
    }
    const res = await getPerformanceTemplateList(params)
    console.log('API Response:', res.data)
    // DRF 分页格式: {count, next, previous, results}
    if (res.data && res.data.results) {
      templateList.value = res.data.results
      console.log('Template list:', templateList.value)
    } else {
      templateList.value = []
    }
  } catch (error) {
    console.error('获取模板列表失败:', error)
    ElMessage.error('获取模板列表失败')
    templateList.value = []
  } finally {
    tableLoading.value = false
  }
}

// 筛选
const handleFilter = () => {
  fetchTemplateList()
}

// 重置筛选
const handleResetFilter = () => {
  filterForm.value.is_active = ''
  fetchTemplateList()
}

// 新建模板
const handleCreate = () => {
  dialogType.value = 'create'
  formData.value = {
    name: '',
    description: '',
    is_active: true,
    items: [{ name: '', weight: 0, desc: '' }]
  }
  dialogVisible.value = true
}

// 查看模板详情
const handleView = async (row) => {
  try {
    const res = await getPerformanceTemplateDetail(row.id)
    // 处理 DRF 返回格式（可能是 {code: 0, data: {...}} 或直接数据）
    const data = res.data?.data || res.data
    if (data) {
      currentTemplate.value = data
      viewDialogVisible.value = true
    } else {
      ElMessage.error('获取模板详情失败')
    }
  } catch (error) {
    console.error('获取模板详情失败:', error)
    ElMessage.error('获取模板详情失败')
  }
}

// 编辑模板
const handleEdit = async (row) => {
  dialogType.value = 'edit'
  try {
    const res = await getPerformanceTemplateDetail(row.id)
    // 处理 DRF 返回格式
    const data = res.data?.data || res.data
    if (data) {
      formData.value = {
        id: data.id,
        name: data.name,
        description: data.description,
        is_active: data.is_active,
        items: data.items && data.items.length > 0
          ? [...data.items]
          : [{ name: '', weight: 0, desc: '' }]
      }
      dialogVisible.value = true
    } else {
      ElMessage.error('获取模板详情失败')
    }
  } catch (error) {
    console.error('获取模板详情失败:', error)
    ElMessage.error('获取模板详情失败')
  }
}

// 切换启用/停用
const handleToggleActive = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认${row.is_active ? '停用' : '启用'}模板"${row.name}"？`,
      '操作确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await togglePerformanceTemplateActive(row.id)
    if (res.data && (res.data.code === 0 || res.status === 200)) {
      ElMessage.success(res.data?.message || '操作成功')
      fetchTemplateList()
    } else {
      ElMessage.error(res.data?.message || '操作失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('切换状态失败:', error)
      if (error.response?.data?.message) {
        ElMessage.error(error.response.data.message)
      } else {
        ElMessage.error('操作失败')
      }
    }
  }
}

// 删除模板
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认删除模板"${row.name}"？删除后无法恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'danger'
      }
    )
    await deletePerformanceTemplate(row.id)
    // DELETE 请求成功返回 204 No Content，无 body
    ElMessage.success('删除成功')
    fetchTemplateList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除模板失败:', error)
      if (error.response?.status === 204) {
        ElMessage.success('删除成功')
        fetchTemplateList()
      } else if (error.response?.data?.message) {
        ElMessage.error(error.response.data.message)
      } else {
        ElMessage.error('删除失败')
      }
    }
  }
}

// 添加考核项
const addItem = () => {
  formData.value.items.push({ name: '', weight: 0, desc: '' })
}

// 删除考核项
const removeItem = (index) => {
  if (formData.value.items.length > 1) {
    formData.value.items.splice(index, 1)
  } else {
    ElMessage.warning('至少保留一个考核项')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitLoading.value = true

    // 过滤空考核项
    const items = formData.value.items.filter(item => item.name.trim())

    const data = {
      name: formData.value.name,
      description: formData.value.description,
      is_active: formData.value.is_active,
      items
    }

    let res
    if (dialogType.value === 'create') {
      res = await createPerformanceTemplate(data)
    } else {
      res = await updatePerformanceTemplate(formData.value.id, data)
    }

    console.log('Submit Response:', res.data)
    if (res.data && res.data.code === 0) {
      ElMessage.success(res.data.message || (dialogType.value === 'create' ? '创建成功' : '更新成功'))
      dialogVisible.value = false
      fetchTemplateList()
    } else {
      ElMessage.error(res.data?.message || '操作失败')
    }
  } catch (error) {
    console.error('提交失败:', error)
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error !== false) {
      ElMessage.error('操作失败，请重试')
    }
  } finally {
    submitLoading.value = false
  }
}

// 初始化
onMounted(() => {
  fetchTemplateList()
})
</script>

<style scoped>
.performance-template {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.filter-card {
  margin-bottom: 20px;
}

.items-designer {
  width: 100%;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 12px;
  background: #fafafa;
}

.items-header {
  display: flex;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 8px;
  font-weight: 500;
  color: #606266;
  font-size: 14px;
}

.item-name {
  flex: 2;
  padding-right: 8px;
}

.item-weight {
  width: 100px;
  text-align: center;
}

.item-desc {
  flex: 2;
  padding-left: 8px;
}

.item-action {
  width: 60px;
  text-align: center;
}

.item-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
}

.item-name-input {
  flex: 2;
}

.item-weight-input {
  width: 100px;
}

.item-desc-input {
  flex: 2;
}

.items-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e4e7ed;
}

.weight-summary {
  font-size: 14px;
  color: #606266;
}

.weight-warning {
  color: #e6a23c;
  font-size: 12px;
  margin-left: 4px;
}
</style>
