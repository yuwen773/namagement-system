<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { getBoxOfficeRecords } from '@/api/boxoffice'
import { getMovies } from '@/api/movie'
import { getCinemas } from '@/api/cinema'
import { ElMessage } from 'element-plus'
import {
  Search,
  Refresh,
  Download,
  Filter,
  Calendar,
  Film,
  OfficeBuilding,
  DataLine,
  Money,
  Ticket
} from '@element-plus/icons-vue'

// 表格数据
const tableData = ref([])
const loading = ref(false)
const total = ref(0)

// 下拉选项
const movieOptions = ref([])
const cinemaOptions = ref([])

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

// 排序选项
const sortOptions = [
  { label: '按日期降序', value: '-record_date' },
  { label: '按日期升序', value: 'record_date' },
  { label: '按票房降序', value: '-daily_box_office' },
  { label: '按票房升序', value: 'daily_box_office' }
]

// 加载影片选项
const loadMovieOptions = async () => {
  try {
    const res = await getMovies({ pageSize: 1000 })
    movieOptions.value = (res.data || []).map(item => ({
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
    cinemaOptions.value = (res.data || []).map(item => ({
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
      ordering: queryParams.order_by
    }

    if (queryParams.start_date) params.start_date = queryParams.start_date
    if (queryParams.end_date) params.end_date = queryParams.end_date
    if (queryParams.movie_id) params.movie_id = queryParams.movie_id
    if (queryParams.cinema_id) params.cinema_id = queryParams.cinema_id

    const res = await getBoxOfficeRecords(params)
    tableData.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error('加载票房数据失败:', error)
    ElMessage.error('加载票房数据失败')
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

// 导出数据（占位符）
const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

// 监听日期范围变化
watch(dateRange, () => {
  handleSearch()
})

// 挂载时加载
onMounted(() => {
  loadData()
  loadMovieOptions()
  loadCinemaOptions()
})
</script>

<template>
  <div class="page-container">
    <div class="content-wrapper">
      <!-- 页面标题 -->
      <div class="mb-6 animate-fade-in">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
            <Ticket class="w-6 h-6 text-white" />
          </div>
          <div class="flex-1">
            <h1 class="text-2xl font-bold text-white">票房查询中心</h1>
            <p class="text-slate-400 text-sm">查询历史票房数据，支持多维度筛选与排序</p>
          </div>
          <el-button @click="handleExport" class="export-btn">
            <Download class="w-4 h-4 mr-1.5" />
            导出数据
          </el-button>
        </div>
      </div>

      <!-- 筛选控制栏 -->
      <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.1s">
        <div class="flex items-center gap-2 mb-4">
          <Filter class="w-4 h-4 text-blue-400" />
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
              popper-class="dark-select-dropdown"
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
              <OfficeBuilding class="w-3.5 h-3.5" />
              影院
            </label>
            <el-select
              v-model="queryParams.cinema_id"
              placeholder="选择影院"
              clearable
              filterable
              @change="handleSearch"
              class="filter-input"
              popper-class="dark-select-dropdown"
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
              popper-class="dark-select-dropdown"
              style="width: 100%"
            >
              <el-option
                v-for="item in sortOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
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
        </div>
      </div>

      <!-- 数据表格区域 -->
      <div class="glass-card rounded-2xl border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
        <!-- 表格头部信息 -->
        <div class="px-6 py-4 border-b border-white/10 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
              <DataLine class="w-4 h-4 text-blue-400" />
            </div>
            <div>
              <h3 class="text-white font-medium">票房记录列表</h3>
              <p class="text-xs text-slate-400 mt-0.5">共 <span class="text-blue-400 font-medium">{{ total }}</span> 条记录</p>
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
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading && tableData.length === 0">
                <td colspan="6" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-12 h-12 rounded-full border-2 border-blue-500/30 border-t-blue-500 animate-spin mb-4"></div>
                    <p class="text-slate-400">加载中...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="tableData.length === 0">
                <td colspan="6" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                      <Ticket class="w-8 h-8 text-slate-600" />
                    </div>
                    <p class="text-slate-500 mb-1">暂无票房记录</p>
                    <p class="text-slate-600 text-sm">请调整筛选条件重新查询</p>
                  </div>
                </td>
              </tr>
              <tr
                v-else
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
                  <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 text-sm font-semibold">
                    <Money class="w-3.5 h-3.5" />
                    {{ formatMoney(record.daily_box_office || record.box_office) }}
                  </span>
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm text-center">{{ record.screening_count || record.show_times || 0 }}</td>
                <td class="py-4 px-6 text-slate-300 text-sm text-center">{{ record.audience_count || record.viewer_count || 0 }}</td>
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
  </div>
</template>

<style scoped>
/* ========================================
   Page Container
   ======================================== */
.page-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ========================================
   Animations
   ======================================== */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }
.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* ========================================
   Glass Card
   ======================================== */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  transition: all 0.3s ease;
}

.glass-card:hover {
  border-color: rgba(245, 158, 11, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ========================================
   Filter Inputs
   ======================================== */
.filter-input {
  width: 100%;
}

:deep(.filter-input .el-input__wrapper),
:deep(.filter-input.el-range-editor.el-input__wrapper),
:deep(.filter-input .el-select__wrapper) {
  background-color: rgba(255, 255, 255, 0.05) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
  transition: all 0.3s ease;
}

:deep(.filter-input .el-input__wrapper:hover),
:deep(.filter-input.el-range-editor.el-input__wrapper:hover),
:deep(.filter-input .el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.5) inset !important;
}

:deep(.filter-input .el-input__wrapper.is-focus),
:deep(.filter-input.el-range-editor.el-input__wrapper.is-active),
:deep(.filter-input .el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px #f59e0b inset !important;
}

:deep(.filter-input .el-input__inner),
:deep(.filter-input .el-range-input) {
  color: #fff !important;
  background-color: transparent !important;
  font-family: inherit;
}

:deep(.filter-input .el-input__inner::placeholder),
:deep(.filter-input .el-range-input::placeholder) {
  color: rgba(255, 255, 255, 0.3) !important;
}

:deep(.filter-input .el-range-separator) {
  color: rgba(255, 255, 255, 0.5) !important;
}

:deep(.filter-input .el-select__caret) {
  color: rgba(255, 255, 255, 0.5) !important;
}

:deep(.filter-input .el-range__icon),
:deep(.filter-input .el-range__close-icon) {
  color: rgba(255, 255, 255, 0.5) !important;
}

/* ========================================
   Buttons
   ======================================== */
.action-btn {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border: none;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
}

.action-btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  transition: all 0.3s ease;
}

.action-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
}

.export-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
}

/* ========================================
   Pagination
   ======================================== */
:deep(.dark-pagination .el-pagination__total),
:deep(.dark-pagination .el-pager li),
:deep(.dark-pagination .btn-prev),
:deep(.dark-pagination .btn-next),
:deep(.dark-pagination .el-pagination__sizes span) {
  color: rgba(255, 255, 255, 0.7);
  background: transparent;
}

:deep(.dark-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #f59e0b, #d97706);
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
  border-color: rgba(245, 158, 11, 0.3);
}

/* ========================================
   Responsive Design
   ======================================== */
@media (max-width: 768px) {
  .page-container {
    padding: 1rem;
  }
}
</style>

<style>
/* ========================================
   Global Overrides (Poppers)
   ======================================== */

/* Select Dropdown */
.dark-select-dropdown.el-popper {
  background: #12121f !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.dark-select-dropdown .el-popper__arrow::before {
  background: #12121f !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.dark-select-dropdown .el-select-dropdown__item {
  color: #94a3b8;
}

.dark-select-dropdown .el-select-dropdown__item.hover,
.dark-select-dropdown .el-select-dropdown__item:hover {
  background: rgba(245, 158, 11, 0.1);
  color: #fff;
}

.dark-select-dropdown .el-select-dropdown__item.selected {
  color: #f59e0b;
  font-weight: bold;
}

/* Datepicker */
.dark-datepicker.el-picker__popper {
  background: #12121f !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #fff;
}

.dark-datepicker .el-picker-panel {
  background: #12121f;
  color: #fff;
}

.dark-datepicker .el-picker-panel__content {
  background: #0a0a12;
}

.dark-datepicker .el-date-picker__header-label,
.dark-datepicker .el-picker-panel__icon-btn {
  color: #fff !important;
}

.dark-datepicker .el-date-table th {
  color: #94a3b8;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-datepicker .el-date-table td.current:not(.disabled) .el-date-table-cell__text {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #fff;
}

.dark-datepicker .el-date-table td.today .el-date-table-cell__text {
  color: #f59e0b;
  font-weight: bold;
}

.dark-datepicker .el-date-table td.available:hover {
  color: #f59e0b;
}

.dark-datepicker .el-picker-panel__footer {
  background-color: #12121f;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-datepicker .el-button--text {
  color: #94a3b8;
}

.dark-datepicker .el-button--plain {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
}

.dark-datepicker .el-input__wrapper {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

.dark-datepicker .el-input__inner {
  color: #fff;
}
</style>
