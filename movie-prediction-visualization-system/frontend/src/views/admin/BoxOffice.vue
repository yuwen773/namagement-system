<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  Edit,
  Delete,
  Refresh,
  Ticket,
  Film,
  Building,
  Calendar,
  Money,
  DataLine,
  Filter,
  Check,
  Close
} from '@element-plus/icons-vue'
import {
  getBoxOfficeRecords,
  createBoxOfficeRecord,
  updateBoxOfficeRecord,
  deleteBoxOfficeRecord
} from '@/api/boxoffice'
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
const formMode = ref('add')
const formRef = ref(null)
const submitLoading = ref(false)
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
    tableData.value = res.data || []
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
    formRef.value.clearValidate()
  }
}

// 打开编辑对话框
const handleEdit = (row) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑票房记录'
  Object.assign(formData, {
    id: row.id,
    movie: row.movie || row.movie_id,
    cinema: row.cinema || row.cinema_id,
    record_date: row.record_date || row.date,
    daily_box_office: parseFloat(row.daily_box_office || row.box_office || 0),
    screening_count: row.screening_count || row.show_times || 0,
    audience_count: row.audience_count || row.viewer_count || 0
  })
  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitLoading.value = true

    const submitData = {
      movie: formData.movie,
      cinema: formData.cinema,
      record_date: formData.record_date,
      daily_box_office: formData.daily_box_office,
      screening_count: formData.screening_count,
      audience_count: formData.audience_count
    }

    if (formMode.value === 'add') {
      await createBoxOfficeRecord(submitData)
      ElMessage.success({
        message: '票房录入成功',
        icon: Check,
        customClass: 'success-message'
      })
    } else {
      await updateBoxOfficeRecord(formData.id, submitData)
      ElMessage.success({
        message: '票房更新成功',
        icon: Check,
        customClass: 'success-message'
      })
    }

    dialogVisible.value = false
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error({
        message: formMode.value === 'add' ? '票房录入失败' : '票房更新失败',
        icon: Close
      })
    }
  } finally {
    submitLoading.value = false
  }
}

// 删除单条记录
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除「${row.movie_title || row.movie?.title || '-'}」在「${row.cinema_name || row.cinema?.name || '-'}」的票房记录吗？`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger',
      customClass: 'delete-confirm-box'
    }
  ).then(async () => {
    try {
      await deleteBoxOfficeRecord(row.id)
      ElMessage.success({
        message: '删除成功',
        icon: Check,
        customClass: 'success-message'
      })
      loadData()
    } catch (error) {
      ElMessage.error({
        message: '删除失败',
        icon: Close
      })
    }
  }).catch(() => {})
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 格式化金额
const formatMoney = (value) => {
  if (!value && value !== 0) return '-'
  const v = parseFloat(value)
  if (v >= 10000) {
    return (v / 10000).toFixed(2) + '万'
  }
  return v.toFixed(2)
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 挂载时加载
onMounted(() => {
  loadData()
  loadMovieOptions()
  loadCinemaOptions()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
    <!-- 动画背景 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <div class="relative z-10 p-6 lg:p-8">
      <!-- 页面标题 -->
      <div class="mb-6 animate-fade-in">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/30">
            <Ticket class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">票房数据录入</h1>
            <p class="text-slate-400 text-sm">管理每日票房记录、排片场次与观影数据</p>
          </div>
        </div>
      </div>

      <!-- 筛选控制栏 -->
      <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.1s">
        <div class="flex items-center gap-2 mb-4">
          <Filter class="w-4 h-4 text-emerald-400" />
          <span class="text-sm font-medium text-slate-300">筛选条件</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <!-- 日期范围 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <Calendar class="w-3.5 h-3.5" />
              日期范围
            </label>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
              @change="handleSearch"
              class="filter-input"
              popper-class="dark-datepicker"
              style="width: 100%"
            />
          </div>

          <!-- 影片选择 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <Film class="w-3.5 h-3.5" />
              影片
            </label>
            <el-select
              v-model="queryParams.movie_id"
              placeholder="选择影片"
              clearable
              filterable
              @change="handleSearch"
              class="filter-input"
              style="width: 100%"
            >
              <el-option
                v-for="item in movieOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <!-- 影院选择 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <Building class="w-3.5 h-3.5" />
              影院
            </label>
            <el-select
              v-model="queryParams.cinema_id"
              placeholder="选择影院"
              clearable
              filterable
              @change="handleSearch"
              class="filter-input"
              style="width: 100%"
            >
              <el-option
                v-for="item in cinemaOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>

          <!-- 排序方式 -->
          <div class="space-y-1.5">
            <label class="text-xs text-slate-400 flex items-center gap-1.5">
              <DataLine class="w-3.5 h-3.5" />
              排序方式
            </label>
            <el-select
              v-model="queryParams.order_by"
              @change="handleSearch"
              class="filter-input"
              style="width: 100%"
            >
              <el-option label="按日期降序" value="-record_date" />
              <el-option label="按日期升序" value="record_date" />
              <el-option label="按票房降序" value="-daily_box_office" />
              <el-option label="按票房升序" value="daily_box_office" />
            </el-select>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex items-center gap-3">
          <el-button type="primary" @click="handleSearch" class="action-btn">
            <Search class="w-4 h-4 mr-1.5" />
            搜索
          </el-button>
          <el-button @click="resetQuery" class="action-btn-secondary">
            <Refresh class="w-4 h-4 mr-1.5" />
            重置筛选
          </el-button>
          <div class="flex-1"></div>
          <el-button type="primary" @click="handleAdd" class="add-btn">
            <Plus class="w-4 h-4 mr-1.5" />
            新增票房记录
          </el-button>
        </div>
      </div>

      <!-- 数据表格区域 -->
      <div class="glass-card rounded-2xl border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
        <!-- 表格头部信息 -->
        <div class="px-6 py-4 border-b border-white/10 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
              <DataLine class="w-4 h-4 text-emerald-400" />
            </div>
            <div>
              <h3 class="text-white font-medium">票房记录列表</h3>
              <p class="text-xs text-slate-400 mt-0.5">共 <span class="text-emerald-400 font-medium">{{ total }}</span> 条记录</p>
            </div>
          </div>
        </div>

        <!-- 表格 -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">日期</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">影片名称</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">影院</th>
                <th class="text-right py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">当日票房</th>
                <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">排片场次</th>
                <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">观影人次</th>
                <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading && tableData.length === 0">
                <td colspan="7" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-12 h-12 rounded-full border-2 border-emerald-500/30 border-t-emerald-500 animate-spin mb-4"></div>
                    <p class="text-slate-400">加载中...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="tableData.length === 0">
                <td colspan="7" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                      <Ticket class="w-8 h-8 text-slate-600" />
                    </div>
                    <p class="text-slate-500 mb-1">暂无票房记录</p>
                    <p class="text-slate-600 text-sm">点击上方「新增票房记录」开始录入</p>
                  </div>
                </td>
              </tr>
              <tr
                v-for="(record, index) in tableData"
                :key="record.id"
                class="border-b border-white/5 hover:bg-white/5 transition-colors group"
                :style="{ animationDelay: `${0.3 + index * 0.03}s` }"
              >
                <td class="py-4 px-6 text-white text-sm">{{ formatDate(record.record_date || record.date) }}</td>
                <td class="py-4 px-6">
                  <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
                      <Film class="w-4 h-4 text-blue-400" />
                    </div>
                    <span class="text-white text-sm font-medium">{{ record.movie_title || record.movie?.title || '-' }}</span>
                  </div>
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm">{{ record.cinema_name || record.cinema?.name || '-' }}</td>
                <td class="py-4 px-6 text-right">
                  <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-sm font-semibold">
                    <Money class="w-3.5 h-3.5" />
                    {{ formatMoney(record.daily_box_office || record.box_office) }}
                  </span>
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm text-center">{{ record.screening_count || record.show_times || 0 }}</td>
                <td class="py-4 px-6 text-slate-300 text-sm text-center">{{ record.audience_count || record.viewer_count || 0 }}</td>
                <td class="py-4 px-6 text-center">
                  <div class="flex items-center justify-center gap-1">
                    <button
                      @click="handleEdit(record)"
                      class="p-2 rounded-lg hover:bg-blue-500/20 text-slate-400 hover:text-blue-400 transition-all"
                      title="编辑"
                    >
                      <Edit class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(record)"
                      class="p-2 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-all"
                      title="删除"
                    >
                      <Delete class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页 -->
        <div class="px-6 py-4 border-t border-white/10 flex items-center justify-between">
          <div class="text-sm text-slate-400">
            显示第 <span class="text-white font-medium">{{ (queryParams.page - 1) * queryParams.pageSize + 1 }}</span>
            至 <span class="text-white font-medium">{{ Math.min(queryParams.page * queryParams.pageSize, total) }}</span>
            条，共 <span class="text-white font-medium">{{ total }}</span> 条
          </div>
          <el-pagination
            v-model:current-page="queryParams.page"
            v-model:page-size="queryParams.pageSize"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            layout="sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
            class="dark-pagination"
          />
        </div>
      </div>
    </div>

    <!-- 录入/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      class="boxoffice-dialog"
      destroy-on-close
    >
      <div class="space-y-5">
        <!-- 影片选择 -->
        <div class="form-group">
          <label class="form-label">
            <Film class="w-4 h-4" />
            影片 <span class="text-red-400">*</span>
          </label>
          <el-select
            v-model="formData.movie"
            placeholder="请选择影片"
            filterable
            class="form-input"
            style="width: 100%"
          >
            <el-option
              v-for="item in movieOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>

        <!-- 影院选择 -->
        <div class="form-group">
          <label class="form-label">
            <Building class="w-4 h-4" />
            影院 <span class="text-red-400">*</span>
          </label>
          <el-select
            v-model="formData.cinema"
            placeholder="请选择影院"
            filterable
            class="form-input"
            style="width: 100%"
          >
            <el-option
              v-for="item in cinemaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>

        <!-- 日期选择 -->
        <div class="form-group">
          <label class="form-label">
            <Calendar class="w-4 h-4" />
            日期 <span class="text-red-400">*</span>
          </label>
          <el-date-picker
            v-model="formData.record_date"
            type="date"
            placeholder="请选择日期"
            value-format="YYYY-MM-DD"
            class="form-input"
            popper-class="dark-datepicker"
            style="width: 100%"
          />
        </div>

        <!-- 票房金额 -->
        <div class="form-group">
          <label class="form-label">
            <Money class="w-4 h-4" />
            当日票房（元） <span class="text-red-400">*</span>
          </label>
          <el-input-number
            v-model="formData.daily_box_office"
            :min="0"
            :precision="2"
            :step="100"
            :controls="true"
            class="form-input"
            style="width: 100%"
          />
        </div>

        <!-- 排片场次与观影人次 -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">
              <DataLine class="w-4 h-4" />
              排片场次 <span class="text-red-400">*</span>
            </label>
            <el-input-number
              v-model="formData.screening_count"
              :min="0"
              :step="1"
              :controls="true"
              class="form-input"
              style="width: 100%"
            />
          </div>
          <div class="form-group">
            <label class="form-label">
              <Ticket class="w-4 h-4" />
              观影人次 <span class="text-red-400">*</span>
            </label>
            <el-input-number
              v-model="formData.audience_count"
              :min="0"
              :step="1"
              :controls="true"
              class="form-input"
              style="width: 100%"
            />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3 pt-2">
          <el-button @click="dialogVisible = false" size="large">取消</el-button>
          <el-button
            type="primary"
            @click="submitForm"
            :loading="submitLoading"
            size="large"
            class="submit-btn"
          >
            {{ formMode === 'add' ? '确认录入' : '保存修改' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* 玻璃态卡片 */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* 网格背景 */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* 渐变光球 */
.gradient-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #059669, #0d9488);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #14b8a6, #0ea5e9);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -20px) scale(1.05);
  }
  50% {
    transform: translate(-10px, 20px) scale(0.95);
  }
  75% {
    transform: translate(-20px, -10px) scale(1.02);
  }
}

/* 淡入动画 */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

/* 滑入动画 */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* 筛选输入框样式 */
:deep(.filter-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  transition: all 0.3s ease;
}

:deep(.filter-input .el-input__wrapper:hover) {
  border-color: rgba(16, 185, 129, 0.5);
}

:deep(.filter-input .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

:deep(.filter-input .el-input__inner) {
  color: #fff;
}

:deep(.filter-input .el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

:deep(.filter-input .el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

:deep(.filter-input .el-select__selected-item) {
  color: #fff;
}

:deep(.filter-input .el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

/* 按钮样式 */
.action-btn {
  background: linear-gradient(135deg, #10b981, #0d9488);
  border: none;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.action-btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  transition: all 0.3s ease;
}

.action-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.add-btn {
  background: linear-gradient(135deg, #10b981, #14b8a6);
  border: none;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* 分页样式 - 深色主题 */
:deep(.dark-pagination .el-pagination__total),
:deep(.dark-pagination .el-pager li),
:deep(.dark-pagination .btn-prev),
:deep(.dark-pagination .btn-next),
:deep(.dark-pagination .el-pagination__sizes span) {
  color: rgba(255, 255, 255, 0.7);
  background: transparent;
}

:deep(.dark-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #10b981, #14b8a6);
  color: #fff;
}

:deep(.dark-pagination .el-pager li:hover),
:deep(.dark-pagination .btn-prev:hover),
:deep(.dark-pagination .btn-next:hover) {
  background: rgba(255, 255, 255, 0.1);
}

:deep(.dark-pagination .el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

:deep(.dark-pagination .el-select .el-input__wrapper:hover) {
  border-color: rgba(16, 185, 129, 0.5);
}

/* 对话框样式 */
:deep(.boxoffice-dialog) {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.boxoffice-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 24px;
}

:deep(.boxoffice-dialog .el-dialog__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.boxoffice-dialog .el-dialog__body) {
  padding: 24px;
  background: #0f172a;
}

:deep(.boxoffice-dialog .el-dialog__footer) {
  padding: 16px 24px;
  background: #1e293b;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* 表单组样式 */
.form-group {
  position: relative;
}

.form-label {
  display: flex;
  items-center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form-input :deep(.el-input__wrapper),
.form-input :deep(.el-select .el-input__wrapper),
.form-input :deep(.el-date-editor .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  transition: all 0.3s ease;
}

.form-input :deep(.el-input__wrapper:hover),
.form-input :deep(.el-select .el-input__wrapper:hover) {
  border-color: rgba(16, 185, 129, 0.5);
}

.form-input :deep(.el-input__wrapper.is-focus),
.form-input :deep(.el-select .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.form-input :deep(.el-input__inner),
.form-input :deep(.el-select__selected-item) {
  color: #fff;
}

.form-input :deep(.el-input__inner::placeholder),
.form-input :deep(.el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.form-input :deep(.el-input-number__decrease),
.form-input :deep(.el-input-number__increase) {
  background: rgba(255, 255, 255, 0.05);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
}

.form-input :deep(.el-input-number__decrease:hover),
.form-input :deep(.el-input-number__increase:hover) {
  color: #10b981;
}

/* 提交按钮 */
.submit-btn {
  background: linear-gradient(135deg, #10b981, #14b8a6);
  border: none;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* 深色日期选择器下拉 */
:deep(.dark-datepicker.el-picker__popper) {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.dark-datepicker .el-date-picker__header-label) {
  color: #fff;
}

:deep(.dark-datepicker .el-picker-panel__icon-btn) {
  color: rgba(255, 255, 255, 0.5);
}

:deep(.dark-datepicker .el-date-table th) {
  color: rgba(255, 255, 255, 0.5);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.dark-datepicker .el-date-table td.current:not(.disabled)) {
  background: linear-gradient(135deg, #10b981, #14b8a6);
  color: #fff;
}

:deep(.dark-datepicker .el-date-table td.today) {
  color: #10b981;
}

:deep(.dark-datepicker .el-date-table td.available:hover) {
  background: rgba(16, 185, 129, 0.2);
}

:deep(.dark-datepicker .el-picker-panel__content) {
  background: #0f172a;
}
</style>
