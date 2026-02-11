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
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
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
  border-color: rgba(59, 130, 246, 0.5);
}

:deep(.filter-input .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
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
  background: linear-gradient(135deg, #3b82f6, #0ea5e9);
  border: none;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
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

.export-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
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
  background: linear-gradient(135deg, #3b82f6, #0ea5e9);
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
  border-color: rgba(59, 130, 246, 0.5);
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
  background: linear-gradient(135deg, #3b82f6, #0ea5e9);
  color: #fff;
}

:deep(.dark-datepicker .el-date-table td.today) {
  color: #3b82f6;
}

:deep(.dark-datepicker .el-date-table td.available:hover) {
  background: rgba(59, 130, 246, 0.2);
}

:deep(.dark-datepicker .el-picker-panel__content) {
  background: #0f172a;
}
</style>
