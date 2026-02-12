<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  Edit,
  Delete,
  Refresh,
  Film,
  Calendar,
  Clock,
  Money,
  Ticket,
  User,
  Check,
  Close,
  Filter,
  VideoCamera
} from '@element-plus/icons-vue'
import {
  getMovies,
  createMovie,
  updateMovie,
  deleteMovie,
  getMovieTypes
} from '@/api/movie'

const loading = ref(false)
const tableLoading = ref(false)

const tableData = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  search: ''
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增影片')
const formLoading = ref(false)

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

const rules = {
  title: [{ required: true, message: '请输入影片名称', trigger: 'blur' }],
  director: [{ required: true, message: '请输入导演', trigger: 'blur' }],
  release_date: [{ required: true, message: '请选择上映日期', trigger: 'change' }],
  duration: [{ required: true, message: '请输入时长', trigger: 'blur' }]
}

const formRef = ref(null)
const movieTypes = ref([])
const typeLoading = ref(false)

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

const handleSearch = () => {
  queryParams.page = 1
  loadData()
}

const handleReset = () => {
  queryParams.search = ''
  queryParams.page = 1
  loadData()
}

const handleSizeChange = (val) => {
  queryParams.pageSize = val
  loadData()
}

const handleCurrentChange = (val) => {
  queryParams.page = val
  loadData()
}

const handleAdd = () => {
  dialogTitle.value = '新增影片'
  resetForm()
  loadTypes()
  dialogVisible.value = true
}

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

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除影片《${row.title}》吗？`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(async () => {
    try {
      await deleteMovie(row.id)
      ElMessage.success({
        message: '删除成功',
        icon: Check
      })
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

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
    formRef.value.clearValidate()
  }
}

const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    formLoading.value = true

    if (form.id) {
      await updateMovie(form.id, form)
      ElMessage.success({
        message: '更新成功',
        icon: Check
      })
    } else {
      await createMovie(form)
      ElMessage.success({
        message: '创建成功',
        icon: Check
      })
    }

    dialogVisible.value = false
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error({
        message: form.id ? '更新失败' : '创建失败',
        icon: Close
      })
    }
  } finally {
    formLoading.value = false
  }
}

const handleCancel = () => {
  dialogVisible.value = false
  resetForm()
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const getTypeColor = (index) => {
  const colors = [
    'from-rose-500 to-orange-500',
    'from-amber-500 to-yellow-500',
    'from-emerald-500 to-teal-500',
    'from-blue-500 to-cyan-500',
    'from-purple-500 to-pink-500',
    'from-indigo-500 to-violet-500'
  ]
  return colors[index % colors.length]
}

onMounted(() => {
  loadData()
  loadTypes()
})
</script>

<template>
  <div class="min-h-screen relative overflow-hidden movies-page">
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
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-rose-500 to-orange-500 flex items-center justify-center shadow-lg shadow-rose-500/30">
            <VideoCamera class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">影片管理</h1>
            <p class="text-slate-400 text-sm">管理影片信息、类型与上映数据</p>
          </div>
        </div>
      </div>

      <!-- 筛选控制栏 -->
      <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.1s">
        <div class="flex items-center gap-2 mb-4">
          <Filter class="w-4 h-4 text-rose-400" />
          <span class="text-sm font-medium text-slate-300">筛选搜索</span>
        </div>

        <div class="flex items-center gap-4">
          <div class="flex-1">
            <div class="relative">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                v-model="queryParams.search"
                type="text"
                placeholder="搜索影片名称、导演..."
                class="search-input"
                @keyup.enter="handleSearch"
              />
            </div>
          </div>
          <button @click="handleSearch" class="action-btn">
            <Search class="w-4 h-4 mr-1.5" />
            搜索
          </button>
          <button @click="handleReset" class="action-btn-secondary">
            <Refresh class="w-4 h-4 mr-1.5" />
            重置
          </button>
          <div class="flex-1"></div>
          <button @click="handleAdd" class="add-btn from-rose-500 to-orange-500">
            <Plus class="w-4 h-4 mr-1.5" />
            新增影片
          </button>
        </div>
      </div>

      <!-- 数据表格区域 -->
      <div class="glass-card rounded-2xl border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
        <!-- 表格头部信息 -->
        <div class="px-6 py-4 border-b border-white/10 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-rose-500/20 to-orange-500/20 flex items-center justify-center">
              <Film class="w-4 h-4 text-rose-400" />
            </div>
            <div>
              <h3 class="text-white font-medium">影片列表</h3>
              <p class="text-xs text-slate-400 mt-0.5">共 <span class="text-rose-400 font-medium">{{ total }}</span> 部影片</p>
            </div>
          </div>
        </div>

        <!-- 表格 -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">影片</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">导演</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">主演</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">类型</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">上映日期</th>
                <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">时长</th>
                <th class="text-right py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">票房</th>
                <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading && tableData.length === 0">
                <td colspan="8" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-12 h-12 rounded-full border-2 border-rose-500/30 border-t-rose-500 animate-spin mb-4"></div>
                    <p class="text-slate-400">加载中...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="tableData.length === 0">
                <td colspan="8" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                      <Film class="w-8 h-8 text-slate-600" />
                    </div>
                    <p class="text-slate-500 mb-1">暂无影片数据</p>
                    <p class="text-slate-600 text-sm">点击上方「新增影片」开始添加</p>
                  </div>
                </td>
              </tr>
              <tr
                v-for="(record, index) in tableData"
                :key="record.id"
                class="border-b border-white/5 hover:bg-white/5 transition-colors group"
                :style="{ animationDelay: `${0.3 + index * 0.03}s` }"
              >
                <td class="py-4 px-6">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-rose-500/20 to-orange-500/20 flex items-center justify-center">
                      <Film class="w-5 h-5 text-rose-400" />
                    </div>
                    <div>
                      <div class="text-white text-sm font-medium">{{ record.title }}</div>
                      <div class="text-slate-500 text-xs">ID: {{ record.id }}</div>
                    </div>
                  </div>
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm">{{ record.director }}</td>
                <td class="py-4 px-6 text-slate-300 text-sm max-w-[200px] truncate" :title="record.actors">{{ record.actors || '-' }}</td>
                <td class="py-4 px-6">
                  <span v-if="record.type?.name || record.type_name" class="type-badge" :class="getTypeColor(record.id || index)">
                    {{ record.type?.name || record.type_name }}
                  </span>
                  <span v-else class="text-slate-500 text-sm">-</span>
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm">{{ formatDate(record.release_date) }}</td>
                <td class="py-4 px-6 text-center text-slate-300 text-sm">
                  <span class="inline-flex items-center gap-1 text-slate-300">
                    <Clock class="w-3.5 h-3.5" />
                    {{ record.duration }}分钟
                  </span>
                </td>
                <td class="py-4 px-6 text-right">
                  <span v-if="record.box_office" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-sm font-semibold">
                    <Money class="w-3.5 h-3.5" />
                    {{ (record.box_office / 10000).toFixed(2) }}万
                  </span>
                  <span v-else class="text-slate-500 text-sm">-</span>
                </td>
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
            @current-change="handleCurrentChange"
            class="dark-pagination"
          />
        </div>
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="540px"
      :close-on-click-modal="false"
      class="movie-dialog"
      destroy-on-close
    >
      <div class="space-y-5">
        <div class="form-group">
          <label class="form-label">
            <Film class="w-4 h-4" />
            影片名称 <span class="text-red-400">*</span>
          </label>
          <el-input
            v-model="form.title"
            placeholder="请输入影片名称"
            class="form-input"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">
              <User class="w-4 h-4" />
              导演 <span class="text-red-400">*</span>
            </label>
            <el-input
              v-model="form.director"
              placeholder="请输入导演"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label class="form-label">
              <Clock class="w-4 h-4" />
              时长(分钟) <span class="text-red-400">*</span>
            </label>
            <el-input-number
              v-model="form.duration"
              :min="1"
              :max="1000"
              class="form-input"
              style="width: 100%"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <Ticket class="w-4 h-4" />
            主演
          </label>
          <el-input
            v-model="form.actors"
            placeholder="请输入主演，多个用逗号分隔"
            class="form-input"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="form-group">
            <label class="form-label">
              <VideoCamera class="w-4 h-4" />
              影片类型
            </label>
            <el-select
              v-model="form.type"
              placeholder="请选择影片类型"
              clearable
              filterable
              loading="typeLoading"
              class="form-input"
              style="width: 100%"
            >
              <el-option
                v-for="type in movieTypes"
                :key="type.id"
                :label="type.name"
                :value="type.id"
              />
            </el-select>
          </div>
          <div class="form-group">
            <label class="form-label">
              <Calendar class="w-4 h-4" />
              上映日期 <span class="text-red-400">*</span>
            </label>
            <el-date-picker
              v-model="form.release_date"
              type="date"
              placeholder="请选择上映日期"
              value-format="YYYY-MM-DD"
              class="form-input"
              popper-class="dark-datepicker"
              style="width: 100%"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">
            <VideoCamera class="w-4 h-4" />
            简介
          </label>
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入影片简介"
            class="form-input"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3 pt-2">
          <el-button @click="handleCancel" size="large">取消</el-button>
          <el-button
            type="primary"
            @click="submitForm"
            :loading="formLoading"
            size="large"
            class="submit-btn"
          >
            {{ form.id ? '保存修改' : '确认添加' }}
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
  background: linear-gradient(135deg, #f43f5e, #fb923c);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #ec4899, #f97316);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #fb923c, #f43f5e);
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

/* 动画 */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* 搜索输入框 */
.search-input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.search-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #f43f5e;
  box-shadow: 0 0 0 2px rgba(244, 63, 94, 0.2);
}

/* 按钮样式 */
.action-btn {
  margin-left: 52px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #f43f5e, #fb923c);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 63, 94, 0.4);
}

.action-btn-secondary {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
}

.action-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.add-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #f43f5e, #fb923c);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 63, 94, 0.4);
}

/* 类型标签 */
.type-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: linear-gradient(135deg, var(--tw-gradient-from), var(--tw-gradient-to));
  color: #fff;
}

/* 分页样式 */
:deep(.dark-pagination .el-pagination__total),
:deep(.dark-pagination .el-pager li),
:deep(.dark-pagination .btn-prev),
:deep(.dark-pagination .btn-next),
:deep(.dark-pagination .el-pagination__sizes span) {
  color: rgba(255, 255, 255, 0.7);
  background: transparent;
}

:deep(.dark-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #f43f5e, #fb923c);
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
  border-color: rgba(244, 63, 94, 0.5);
}

/* 对话框样式 */
:deep(.movie-dialog) {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.movie-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 24px;
}

:deep(.movie-dialog .el-dialog__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.movie-dialog .el-dialog__body) {
  padding: 24px;
  background: #0f172a;
}

:deep(.movie-dialog .el-dialog__footer) {
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
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form-input :deep(.el-input__wrapper),
.form-input :deep(.el-select .el-input__wrapper),
.form-input :deep(.el-date-editor .el-input__wrapper),
.form-input :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  transition: all 0.3s ease;
}

.form-input :deep(.el-input__wrapper:hover),
.form-input :deep(.el-select .el-input__wrapper:hover) {
  border-color: rgba(244, 63, 94, 0.5);
}

.form-input :deep(.el-input__wrapper.is-focus),
.form-input :deep(.el-select .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #f43f5e;
  box-shadow: 0 0 0 2px rgba(244, 63, 94, 0.2);
}

.form-input :deep(.el-input__inner),
.form-input :deep(.el-select__selected-item),
.form-input :deep(.el-textarea__inner) {
  color: #fff;
}

.form-input :deep(.el-input__inner::placeholder),
.form-input :deep(.el-select__placeholder),
.form-input :deep(.el-textarea__inner::placeholder) {
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
  color: #f43f5e;
}

/* 提交按钮 */
.submit-btn {
  background: linear-gradient(135deg, #f43f5e, #fb923c);
  border: none;
  box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 63, 94, 0.4);
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
  background: linear-gradient(135deg, #f43f5e, #fb923c);
  color: #fff;
}

:deep(.dark-datepicker .el-date-table td.today) {
  color: #f43f5e;
}

:deep(.dark-datepicker .el-date-table td.available:hover) {
  background: rgba(244, 63, 94, 0.2);
}

:deep(.dark-datepicker .el-picker-panel__content) {
  background: #0f172a;
}
</style>

<style>
/* ============================================
   影片管理 - 下拉选项面板全局样式
   ============================================ */
/* 筛选下拉面板 - 橙红色系 */
.movies-page .el-select-dropdown {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.movies-page .el-select-dropdown__item {
  color: rgba(255, 255, 255, 0.85) !important;
  background: transparent !important;
  transition: all 0.2s;
}

.movies-page .el-select-dropdown__item:hover {
  background: rgba(244, 63, 94, 0.15) !important;
  color: #fb7185 !important;
}

.movies-page .el-select-dropdown__item.is-selected {
  background: rgba(244, 63, 94, 0.25) !important;
  color: #fb7185 !important;
}

.movies-page .el-select-dropdown__item.is-disabled {
  color: rgba(255, 255, 255, 0.25) !important;
}

/* 日期选择器下拉面板 - 橙红色系 */
.movies-page .el-picker__popper {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.movies-page .el-picker-panel {
  background: rgba(30, 41, 59, 0.95) !important;
  border: none !important;
}

.movies-page .el-picker-panel__body {
  background: transparent !important;
}

.movies-page .el-date-picker__header {
  color: rgba(255, 255, 255, 0.85) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.movies-page .el-date-picker__header-label {
  color: #fff !important;
  font-weight: 500;
}

.movies-page .el-date-picker__header-label:hover {
  color: #fb7185 !important;
}

.movies-page .el-picker-panel__icon-btn {
  color: rgba(255, 255, 255, 0.5) !important;
  transition: color 0.2s;
}

.movies-page .el-picker-panel__icon-btn:hover {
  color: #fb7185 !important;
}

.movies-page .el-date-table th {
  color: rgba(255, 255, 255, 0.5) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.movies-page .el-date-table td {
  color: rgba(255, 255, 255, 0.85) !important;
}

.movies-page .el-date-table td.today span {
  color: #fb7185 !important;
  font-weight: 500;
}

.movies-page .el-date-table td.current:not(.disabled) span {
  background: linear-gradient(135deg, #f43f5e, #fb923c) !important;
  color: #fff !important;
}

.movies-page .el-date-table td.available:hover {
  background: rgba(244, 63, 94, 0.2) !important;
}

.movies-page .el-date-table td.in-range {
  background: rgba(244, 63, 94, 0.15) !important;
}

.movies-page .el-date-table td.start-date span,
.movies-page .el-date-table td.end-date span {
  background: linear-gradient(135deg, #f43f5e, #fb923c) !important;
  color: #fff !important;
}

.movies-page .el-date-table td.next-month,
.movies-page .el-date-table td.prev-month {
  color: rgba(255, 255, 255, 0.2) !important;
}

.movies-page .el-date-table td.disabled {
  color: rgba(255, 255, 255, 0.15) !important;
}

/* 滚动条样式 */
.movies-page .el-select-dropdown .el-scrollbar__bar {
  background: rgba(255, 255, 255, 0.1);
}

.movies-page .el-select-dropdown .el-scrollbar__thumb {
  background: rgba(244, 63, 94, 0.5);
  border-radius: 3px;
}

.movies-page .el-select-dropdown .el-scrollbar__thumb:hover {
  background: rgba(244, 63, 94, 0.7);
}

.movies-page .el-select-dropdown__empty {
  color: rgba(255, 255, 255, 0.4) !important;
}
</style>
