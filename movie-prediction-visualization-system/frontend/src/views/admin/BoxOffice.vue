<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Edit, Delete, Refresh
} from '@element-plus/icons-vue'
import { getBoxOfficeRecords, createBoxOfficeRecord, updateBoxOfficeRecord, deleteBoxOfficeRecord, batchDeleteBoxOfficeRecords } from '@/api/boxoffice'
import { getMovies } from '@/api/movie'
import { getCinemas } from '@/api/cinema'

// 表格数据
const tableData = ref([])
const loading = ref(false)
const total = ref(0)
const selectedRows = ref([])

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  start_date: '',
  end_date: '',
  movie_id: '',
  cinema_id: '',
  order_by: '-record_date'
})

// 日期范围计算属性
const dateRange = computed({
  get: () => {
    return queryParams.start_date && queryParams.end_date
      ? [queryParams.start_date, queryParams.end_date]
      : []
  },
  set: (val) => {
    if (val && val.length === 2) {
      queryParams.start_date = val[0]
      queryParams.end_date = val[1]
    } else {
      queryParams.start_date = ''
      queryParams.end_date = ''
    }
  }
})

// 录入表单
const dialogVisible = ref(false)
const dialogTitle = ref('录入票房')
const formMode = ref('add') // 'add' | 'edit'
const formRef = ref(null)
const formData = reactive({
  id: null,
  movie: null,
  cinema: null,
  record_date: '',
  daily_box_office: 0,
  screening_count: 0,
  audience_count: 0
})

// 表单验证规则
const formRules = {
  movie: [{ required: true, message: '请选择影片', trigger: 'change' }],
  cinema: [{ required: true, message: '请选择影院', trigger: 'change' }],
  record_date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  daily_box_office: [
    { required: true, message: '请输入票房金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '票房金额必须大于0', trigger: 'blur' }
  ],
  screening_count: [
    { required: true, message: '请输入排片场次', trigger: 'blur' },
    { type: 'number', min: 0, message: '排片场次必须大于0', trigger: 'blur' }
  ],
  audience_count: [
    { required: true, message: '请输入观影人次', trigger: 'blur' },
    { type: 'number', min: 0, message: '观影人次必须大于0', trigger: 'blur' }
  ]
}

// 下拉选项
const movieOptions = ref([])
const cinemaOptions = ref([])

// 加载影片选项
const loadMovieOptions = async () => {
  try {
    const res = await getMovies({ pageSize: 1000 })
    movieOptions.value = res.data.map(item => ({
      label: item.title,
      value: item.id
    }))
  } catch (e) {
    console.error('加载影片选项失败', e)
  }
}

// 加载影院选项
const loadCinemaOptions = async () => {
  try {
    const res = await getCinemas({ pageSize: 1000 })
    cinemaOptions.value = res.data.map(item => ({
      label: item.name,
      value: item.id
    }))
  } catch (e) {
    console.error('加载影院选项失败', e)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: queryParams.page,
      pageSize: queryParams.pageSize,
      order_by: queryParams.order_by
    }
    if (queryParams.start_date) params.start_date = queryParams.start_date
    if (queryParams.end_date) params.end_date = queryParams.end_date
    if (queryParams.movie_id) params.movie_id = queryParams.movie_id
    if (queryParams.cinema_id) params.cinema_id = queryParams.cinema_id

    const res = await getBoxOfficeRecords(params)
    tableData.value = res.data
    total.value = res.total || 0
  } catch (error) {
    ElMessage.error('加载票房数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  queryParams.page = 1
  loadData()
}

// 重置筛选
const resetQuery = () => {
  queryParams.start_date = ''
  queryParams.end_date = ''
  queryParams.movie_id = ''
  queryParams.cinema_id = ''
  queryParams.order_by = '-record_date'
  queryParams.page = 1
  loadData()
}

// 分页变化
const handlePageChange = (page) => {
  queryParams.page = page
  loadData()
}

// 每页条数变化
const handleSizeChange = (size) => {
  queryParams.pageSize = size
  queryParams.page = 1
  loadData()
}

// 打开录入对话框
const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '录入票房'
  resetForm()
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  formData.id = null
  formData.movie = null
  formData.cinema = null
  formData.record_date = ''
  formData.daily_box_office = 0
  formData.screening_count = 0
  formData.audience_count = 0
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 打开编辑对话框
const handleEdit = (row) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑票房'
  Object.assign(formData, {
    id: row.id,
    movie: row.movie,
    cinema: row.cinema,
    record_date: row.record_date,
    daily_box_office: parseFloat(row.daily_box_office),
    screening_count: row.screening_count,
    audience_count: row.audience_count
  })
  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    if (formMode.value === 'add') {
      await createBoxOfficeRecord(formData)
      ElMessage.success('票房录入成功')
    } else {
      await updateBoxOfficeRecord(formData.id, formData)
      ElMessage.success('票房更新成功')
    }

    dialogVisible.value = false
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(formMode.value === 'add' ? '票房录入失败' : '票房更新失败')
    }
  }
}

// 删除单条记录
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除「${row.movie_title}」在「${row.cinema_name}」的票房记录吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteBoxOfficeRecord(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 批量删除
const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的记录')
    return
  }

  ElMessageBox.confirm(
    `确定要删除选中的 ${selectedRows.value.length} 条票房记录吗？`,
    '批量删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const ids = selectedRows.value.map(row => row.id)
      await batchDeleteBoxOfficeRecords({ ids })
      ElMessage.success(`成功删除 ${ids.length} 条记录`)
      loadData()
    } catch (error) {
      ElMessage.error('批量删除失败')
    }
  }).catch(() => {})
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 格式化金额
const formatMoney = (value) => {
  if (!value) return '¥0.00'
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY'
  }).format(value)
}

// 挂载时加载
onMounted(() => {
  loadData()
  loadMovieOptions()
  loadCinemaOptions()
})
</script>

<template>
  <div class="boxoffice-page">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">票房数据管理</h2>
      <div class="flex gap-3">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon> 录入票房
        </el-button>
      </div>
    </div>

    <!-- 筛选区域 -->
    <el-card class="mb-6 filter-card">
      <el-form :inline="true" :model="queryParams" class="filter-form">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            @change="handleSearch"
            style="width: 260px"
          />
        </el-form-item>
        <el-form-item label="影片">
          <el-select
            v-model="queryParams.movie_id"
            placeholder="选择影片"
            clearable
            filterable
            @change="handleSearch"
            style="width: 180px"
          >
            <el-option
              v-for="item in movieOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="影院">
          <el-select
            v-model="queryParams.cinema_id"
            placeholder="选择影院"
            clearable
            filterable
            @change="handleSearch"
            style="width: 180px"
          >
            <el-option
              v-for="item in cinemaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-select
            v-model="queryParams.order_by"
            @change="handleSearch"
            style="width: 150px"
          >
            <el-option label="按日期降序" value="-record_date" />
            <el-option label="按日期升序" value="record_date" />
            <el-option label="按票房降序" value="-daily_box_office" />
            <el-option label="按票房升序" value="daily_box_office" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon> 搜索
          </el-button>
          <el-button @click="resetQuery">
            <el-icon><Refresh /></el-icon> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card>
      <div class="flex justify-between items-center mb-4">
        <span class="text-gray-600">共 {{ total }} 条记录</span>
        <el-button
          v-if="selectedRows.length > 0"
          type="danger"
          size="small"
          @click="handleBatchDelete"
        >
          <el-icon><Delete /></el-icon> 批量删除 ({{ selectedRows.length }})
        </el-button>
      </div>

      <el-table
        :data="tableData"
        v-loading="loading"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="movie_title" label="影片名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="cinema_name" label="影院" min-width="150" show-overflow-tooltip />
        <el-table-column prop="region_name" label="地区" width="120" />
        <el-table-column prop="record_date" label="日期" width="120" />
        <el-table-column prop="daily_box_office" label="票房收入" width="120">
          <template #default="{ row }">
            <span class="text-orange-600 font-medium">{{ formatMoney(row.daily_box_office) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="screening_count" label="排片场次" width="100" align="center" />
        <el-table-column prop="audience_count" label="观影人次" width="100" align="center" />
        <el-table-column label="操作" width="150" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 录入/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="影片" prop="movie">
          <el-select
            v-model="formData.movie"
            placeholder="请选择影片"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="item in movieOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="影院" prop="cinema">
          <el-select
            v-model="formData.cinema"
            placeholder="请选择影院"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="item in cinemaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="日期" prop="record_date">
          <el-date-picker
            v-model="formData.record_date"
            type="date"
            placeholder="请选择日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="票房收入" prop="daily_box_office">
          <el-input-number
            v-model="formData.daily_box_office"
            :min="0"
            :precision="2"
            :step="100"
            style="width: 100%"
          >
            <template #prefix>¥</template>
          </el-input-number>
        </el-form-item>
        <el-form-item label="排片场次" prop="screening_count">
          <el-input-number
            v-model="formData.screening_count"
            :min="0"
            :step="1"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="观影人次" prop="audience_count">
          <el-input-number
            v-model="formData.audience_count"
            :min="0"
            :step="1"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">
            {{ formMode === 'add' ? '录入' : '保存' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.boxoffice-page {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-form .el-form-item {
  margin-bottom: 0;
  margin-right: 0;
}
</style>
