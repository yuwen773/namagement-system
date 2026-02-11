<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getMovies,
  createMovie,
  updateMovie,
  deleteMovie,
  getMovieTypes
} from '@/api/movie'

const loading = ref(false)
const tableLoading = ref(false)

// 表格数据
const tableData = ref([])
const total = ref(0)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  search: ''
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增影片')
const formLoading = ref(false)

// 表单数据
const form = reactive({
  id: null,
  title: '',
  director: '',
  actors: '',
  type: null,
  release_date: '',
  duration: 90,
  description: ''
})

// 表单验证规则
const rules = {
  title: [{ required: true, message: '请输入影片名称', trigger: 'blur' }],
  director: [{ required: true, message: '请输入导演', trigger: 'blur' }],
  release_date: [{ required: true, message: '请选择上映日期', trigger: 'change' }],
  duration: [{ required: true, message: '请输入时长', trigger: 'blur' }]
}

const formRef = ref(null)

// 类型列表
const movieTypes = ref([])
const typeLoading = ref(false)

// 获取类型列表
const loadTypes = async () => {
  typeLoading.value = true
  try {
    const res = await getMovieTypes()
    movieTypes.value = res.data || []
  } catch (error) {
    console.error('加载类型失败:', error)
  } finally {
    typeLoading.value = false
  }
}

// 加载影片列表
const loadData = async () => {
  tableLoading.value = true
  try {
    const res = await getMovies(queryParams)
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
  dialogTitle.value = '新增影片'
  resetForm()
  loadTypes()
  dialogVisible.value = true
}

// 打开编辑对话框
const handleEdit = async (row) => {
  dialogTitle.value = '编辑影片'
  Object.assign(form, {
    id: row.id,
    title: row.title,
    director: row.director,
    actors: row.actors || '',
    type: row.type?.id || row.type,
    release_date: row.release_date,
    duration: row.duration,
    description: row.description || ''
  })
  await loadTypes()
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除影片《${row.title}》吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteMovie(row.id)
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
  form.title = ''
  form.director = ''
  form.actors = ''
  form.type = null
  form.release_date = ''
  form.duration = 90
  form.description = ''
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
        // 编辑
        await updateMovie(form.id, form)
        ElMessage.success('更新成功')
      } else {
        // 新增
        await createMovie(form)
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

// 日期格式化
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadData()
  loadTypes()
})
</script>

<template>
  <div class="movies-page">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">影片管理</h2>
    </div>

    <!-- 搜索栏 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="queryParams">
        <el-form-item label="影片名称">
          <el-input
            v-model="queryParams.search"
            placeholder="请输入影片名称"
            clearable
            @keyup.enter="handleSearch"
          />
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
          <el-icon><Plus /></el-icon> 新增影片
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
        <el-table-column prop="title" label="影片名称" min-width="150" />
        <el-table-column prop="director" label="导演" width="120" />
        <el-table-column prop="actors" label="主演" min-width="150" show-overflow-tooltip />
        <el-table-column prop="type_name" label="类型" width="100">
          <template #default="{ row }">
            {{ row.type?.name || row.type_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="release_date" label="上映日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.release_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="时长(分钟)" width="100" align="center" />
        <el-table-column prop="box_office" label="票房(万)" width="100" align="right">
          <template #default="{ row }">
            {{ row.box_office?.toLocaleString() || '-' }}
          </template>
        </el-table-column>
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
      width="600px"
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
        <el-form-item label="影片名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入影片名称" />
        </el-form-item>
        <el-form-item label="导演" prop="director">
          <el-input v-model="form.director" placeholder="请输入导演" />
        </el-form-item>
        <el-form-item label="主演">
          <el-input v-model="form.actors" placeholder="请输入主演，多个用逗号分隔" />
        </el-form-item>
        <el-form-item label="影片类型" prop="type">
          <el-select
            v-model="form.type"
            placeholder="请选择影片类型"
            clearable
            filterable
            loading="typeLoading"
          >
            <el-option
              v-for="type in movieTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="上映日期" prop="release_date">
          <el-date-picker
            v-model="form.release_date"
            type="date"
            placeholder="请选择上映日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="时长(分钟)" prop="duration">
          <el-input-number v-model="form.duration" :min="1" :max="1000" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入影片简介"
          />
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
