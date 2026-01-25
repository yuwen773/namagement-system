<template>
  <div class="department-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 21h18"/>
            <path d="M9 8h1"/>
            <path d="M9 12h1"/>
            <path d="M9 16h1"/>
            <path d="M14 8h1"/>
            <path d="M14 12h1"/>
            <path d="M14 16h1"/>
            <path d="M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"/>
          </svg>
        </div>
        <span class="page-title">部门管理</span>
      </div>
      <div class="header-right">
        <el-button v-if="!isReadOnly" type="primary" @click="handleAdd">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          新增部门
        </el-button>
      </div>
    </div>

    <!-- 部门表格 -->
    <div class="table-section" v-loading="loading">
      <el-table :data="departmentTree" row-key="id" default-expand-all stripe class="custom-table">
        <el-table-column prop="name" label="部门名称" min-width="200">
          <template #default="{ row }">
            <div class="department-name">
              <div class="dept-avatar" :style="{ background: getDeptColor(row.id) }">
                {{ row.name?.charAt(0) }}
              </div>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="部门编码" width="150" />
        <el-table-column label="上级部门" width="150">
          <template #default="{ row }">
            <span class="parent-dept">{{ row.parent ? getParentName(row.parent) : '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="100" align="center" />
        <el-table-column prop="is_active" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'" size="small" class="status-tag">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="!isReadOnly" label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)" class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)" class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchDepartments"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑部门' : '新增部门'" width="500px" :close-on-click-modal="false">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" class="custom-form">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" class="form-input" />
        </el-form-item>
        <el-form-item label="部门编码" prop="code">
          <el-input v-model="form.code" placeholder="请输入部门编码" :disabled="isEdit" class="form-input" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent">
          <el-tree-select
            v-model="form.parent"
            :data="treeSelectData"
            :props="{ label: 'name', value: 'id' }"
            placeholder="请选择上级部门（留空为顶级）"
            check-strictly
            clearable
            class="form-input"
          />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" class="form-input" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDepartmentList, createDepartment, updateDepartment, deleteDepartment } from '@/api/department'
import { useAuthStore } from '@/stores/auth'

const loading = ref(false)
const departmentList = ref([])
const departmentTree = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const submitting = ref(false)
const authStore = useAuthStore()

// 只读模式（员工角色无法操作）
const isReadOnly = computed(() => authStore.user?.role === 'employee')

// 分页状态
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const form = reactive({
  id: null,
  name: '',
  code: '',
  parent: null,
  sort_order: 0,
  is_active: true
})

const rules = {
  name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入部门编码', trigger: 'blur' }]
}

// 用于树选择器的扁平数据
const treeSelectData = computed(() => {
  const result = [{ id: null, name: '无（顶级部门）' }]
  const buildTree = (list, parentId = null) => {
    return list
      .filter(item => item.parent === parentId)
      .map(item => ({
        ...item,
        children: buildTree(list, item.id)
      }))
  }
  result[0].children = buildTree(departmentList.value)
  return result
})

// 获取父部门名称
const getParentName = (parentId) => {
  const parent = departmentList.value.find(d => d.id === parentId)
  return parent?.name || '-'
}

// 获取部门颜色
const getDeptColor = (id) => {
  const colors = [
    'linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)',
    'linear-gradient(135deg, #10b981 0%, #34d399 100%)',
    'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)',
    'linear-gradient(135deg, #ef4444 0%, #f87171 100%)',
    'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
    'linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%)',
    'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)'
  ]
  return colors[id % colors.length]
}

const fetchDepartments = async () => {
  loading.value = true
  try {
    const res = await getDepartmentList({
      page: pagination.page,
      page_size: pagination.pageSize,
      only_root: 'true'
    })
    const data = res.data.data || []
    pagination.total = res.data.total || 0

    const allRes = await getDepartmentList({ page: 1, page_size: 9999 })
    departmentList.value = allRes.data.data || []

    const buildTree = (list, parentId = null) => {
      return list
        .filter(item => item.parent === parentId)
        .map(item => ({
          ...item,
          children: buildTree(list, item.id)
        }))
    }
    departmentTree.value = buildTree(departmentList.value)
  } catch (error) {
    console.error('获取部门列表失败:', error)
    ElMessage.error('获取部门列表失败')
  } finally {
    loading.value = false
  }
}

// 页码变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchDepartments()
}

const handleAdd = () => {
  isEdit.value = false
  form.id = null
  form.name = ''
  form.code = ''
  form.parent = null
  form.sort_order = departmentList.value.length + 1
  form.is_active = true
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.id = row.id
  form.name = row.name
  form.code = row.code
  form.parent = row.parent
  form.sort_order = row.sort_order
  form.is_active = row.is_active
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除部门"${row.name}"吗？`,
      '删除确认',
      { confirmButtonText: '确定删除', cancelButtonText: '取消', type: 'warning' }
    )
    await deleteDepartment(row.id)
    ElMessage.success('删除成功')
    fetchDepartments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitting.value = true
    if (isEdit.value) {
      await updateDepartment(form.id, {
        name: form.name,
        code: form.code,
        parent: form.parent,
        sort_order: form.sort_order,
        is_active: form.is_active
      })
      ElMessage.success('更新成功')
    } else {
      await createDepartment({
        name: form.name,
        code: form.code,
        parent: form.parent,
        sort_order: form.sort_order,
        is_active: form.is_active
      })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchDepartments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('保存失败:', error)
      ElMessage.error(error.response?.data?.detail || '保存失败')
    }
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchDepartments()
})
</script>

<style scoped>
/* ========================================
   Department List - Modern Corporate Design
   ======================================== */

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-glow-primary);
}

.header-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-right .el-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
}

.header-right svg {
  width: 16px;
  height: 16px;
}

/* 表格区域 */
.table-section {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.custom-table {
  border-radius: 0;
}

/* 部门名称列样式 */
.department-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dept-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.parent-dept {
  color: var(--color-text-secondary);
}

.status-tag {
  font-weight: 500;
}

/* 操作按钮 */
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 20px;
  background: var(--color-gray-50);
  border-top: 1px solid var(--color-border-light);
}

/* 表单样式 */
.custom-form .form-input {
  width: 100%;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>
