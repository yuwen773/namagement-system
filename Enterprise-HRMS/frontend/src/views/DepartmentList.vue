<template>
  <div class="department-list">
    <div class="page-header">
      <h2>部门管理</h2>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon> 新增部门
      </el-button>
    </div>

    <!-- 部门树 -->
    <el-table :data="departmentTree" v-loading="loading" row-key="id" default-expand-all>
      <el-table-column prop="name" label="部门名称" min-width="200">
        <template #default="{ row }">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="code" label="部门编码" width="150" />
      <el-table-column label="上级部门" width="150">
        <template #default="{ row }">
          {{ row.parent ? getParentName(row.parent) : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="sort_order" label="排序" width="100" align="center" />
      <el-table-column prop="is_active" label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div class="pagination-container">
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

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑部门' : '新增部门'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="部门编码" prop="code">
          <el-input v-model="form.code" placeholder="请输入部门编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent">
          <el-tree-select
            v-model="form.parent"
            :data="treeSelectData"
            :props="{ label: 'name', value: 'id' }"
            placeholder="请选择上级部门（留空为顶级）"
            check-strictly
            clearable
          />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getDepartmentList, getDepartmentTree, createDepartment, updateDepartment, deleteDepartment } from '@/api/department'

const loading = ref(false)
const departmentList = ref([])
const departmentTree = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const submitting = ref(false)

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

const fetchDepartments = async () => {
  loading.value = true
  try {
    const res = await getDepartmentList({
      page: pagination.page,
      page_size: pagination.pageSize,
      only_root: 'true'  // 获取根部门构建树
    })
    const data = res.data.data || []
    pagination.total = res.data.total || 0

    // 获取完整列表用于查找父部门名称
    const allRes = await getDepartmentList({ page: 1, page_size: 9999 })
    departmentList.value = allRes.data.data || []

    // 构建树形结构（使用完整列表）
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
  form.sort_order = 0
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
    await ElMessageBox.confirm(`确定要删除部门"${row.name}"吗？`, '提示', {
      type: 'warning'
    })
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
.department-list {
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
  color: #303133;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
