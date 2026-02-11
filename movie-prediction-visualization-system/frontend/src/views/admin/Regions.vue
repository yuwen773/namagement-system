<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getRegions,
  createRegion,
  updateRegion,
  deleteRegion
} from '@/api/cinema'

const loading = ref(false)
const tableLoading = ref(false)

// 表格数据
const tableData = ref([])
const total = ref(0)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  search: '',
  parent: null
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增地域')
const formLoading = ref(false)

// 表单数据
const form = reactive({
  id: null,
  name: '',
  parent: null,
  code: ''
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入地域名称', trigger: 'blur' }]
}

const formRef = ref(null)

// 地域列表（用于上级选择）
const allRegions = ref([])
const regionLoading = ref(false)

// 加载地域列表
const loadRegions = async () => {
  regionLoading.value = true
  try {
    const res = await getRegions()
    allRegions.value = res.data || []
  } catch (error) {
    console.error('加载地域失败:', error)
  } finally {
    regionLoading.value = false
  }
}

// 加载数据
const loadData = async () => {
  tableLoading.value = true
  try {
    const res = await getRegions(queryParams)
    tableData.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  } finally {
    tableLoading.value = false
  }
}

// 查询
const handleSearch = () => {
  queryParams.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  queryParams.search = ''
  queryParams.parent = null
  queryParams.page = 1
  loadData()
}

// 分页
const handleSizeChange = (val) => {
  queryParams.pageSize = val
  loadData()
}

const handleCurrentChange = (val) => {
  queryParams.page = val
  loadData()
}

// 打开新增对话框
const handleAdd = () => {
  dialogTitle.value = '新增地域'
  resetForm()
  loadRegions()
  dialogVisible.value = true
}

// 打开编辑对话框
const handleEdit = async (row) => {
  dialogTitle.value = '编辑地域'
  Object.assign(form, {
    id: row.id,
    name: row.name,
    parent: row.parent?.id || row.parent || null,
    code: row.code || ''
  })
  await loadRegions()
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除地域"${row.name}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteRegion(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

// 重置表单
const resetForm = () => {
  form.id = null
  form.name = ''
  form.parent = null
  form.code = ''
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    formLoading.value = true
    try {
      if (form.id) {
        await updateRegion(form.id, form)
        ElMessage.success('更新成功')
      } else {
        await createRegion(form)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      loadData()
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      formLoading.value = false
    }
  })
}

// 取消
const handleCancel = () => {
  dialogVisible.value = false
  resetForm()
}

onMounted(() => {
  loadData()
  loadRegions()
})
</script>

<template>
  <div class="regions-page">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">地域管理</h2>
    </div>

    <!-- 搜索栏 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="queryParams">
        <el-form-item label="地域名称">
          <el-input
            v-model="queryParams.search"
            placeholder="请输入地域名称"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="上级地域">
          <el-select
            v-model="queryParams.parent"
            placeholder="请选择上级地域"
            clearable
            filterable
          >
            <el-option
              v-for="region in allRegions"
              :key="region.id"
              :label="region.name"
              :value="region.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作栏 -->
    <el-card class="mb-4">
      <div class="flex justify-between items-center">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon> 新增地域
        </el-button>
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card>
      <el-table
        :data="tableData"
        v-loading="tableLoading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="地域名称" min-width="150" />
        <el-table-column prop="parent_name" label="上级地域" width="150">
          <template #default="{ row }">
            {{ row.parent?.name || row.parent_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="code" label="编码" width="120" />
        <el-table-column label="操作" width="150" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      @close="handleCancel"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        v-loading="formLoading"
      >
        <el-form-item label="地域名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入地域名称" />
        </el-form-item>
        <el-form-item label="上级地域">
          <el-select
            v-model="form.parent"
            placeholder="请选择上级地域（可选）"
            clearable
            filterable
            loading="regionLoading"
          >
            <el-option
              v-for="region in allRegions"
              :key="region.id"
              :label="region.name"
              :value="region.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="编码">
          <el-input v-model="form.code" placeholder="请输入编码（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="formLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
