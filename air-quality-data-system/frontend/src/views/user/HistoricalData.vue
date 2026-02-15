<template>
  <div class="historical-data-container min-h-screen bg-slate-950 relative overflow-hidden">
    <!-- Background grid -->
    <div class="grid-background absolute inset-0 opacity-10 pointer-events-none"></div>

    <!-- Main content -->
    <div class="relative z-10 p-6 lg:p-8">
      <!-- Header -->
      <header class="mb-6 animate-fade-in-down">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl lg:text-3xl font-bold text-white mb-1" style="font-family: 'Rajdhani', sans-serif;">
              历史数据查询
            </h1>
            <p class="text-slate-400 text-sm">检索与回溯历史空气质量监测数据</p>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="goBack"
              class="w-10 h-10 rounded-xl glass-card flex items-center justify-center hover-scale group"
            >
              <svg class="w-5 h-5 text-slate-400 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Query form -->
      <div class="glass-card rounded-2xl p-6 mb-6 animate-fade-in" style="animation-delay: 0.1s;">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- City selector -->
          <div class="md:col-span-1">
            <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
              城市
            </label>
            <el-select
              v-model="queryForm.city"
              filterable
              placeholder="选择城市"
              clearable
              class="w-full custom-select"
              :popper-class="'dark-select-dropdown'"
            >
              <el-option
                v-for="city in availableCities"
                :key="city.code"
                :label="city.name"
                :value="city.code"
              />
            </el-select>
          </div>

          <!-- Date range -->
          <div class="md:col-span-2">
            <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
              日期范围
            </label>
            <el-date-picker
              v-model="queryForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              class="w-full custom-date-picker"
              :popper-class="'dark-date-picker'"
              unlink-panels
            />
          </div>

          <!-- Action buttons -->
          <div class="flex items-end gap-2">
            <button
              @click="handleQuery"
              :disabled="loading"
              class="flex-1 px-4 py-2.5 rounded-xl bg-cyan-500 text-white font-medium hover:bg-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover-scale"
              style="font-family: 'Rajdhani', sans-serif;"
            >
              <span v-if="!loading">查询</span>
              <span v-else class="flex items-center justify-center gap-2">
                <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                查询中
              </span>
            </button>
            <button
              @click="handleReset"
              class="px-4 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white hover-scale"
              style="font-family: 'Rajdhani', sans-serif;"
            >
              重置
            </button>
          </div>
        </div>
      </div>

      <!-- Statistics summary -->
      <div v-if="statistics" class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6 animate-fade-in" style="animation-delay: 0.15s;">
        <div class="glass-card rounded-xl p-4">
          <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">数据总量</div>
          <div class="text-2xl font-bold font-mono text-cyan-400">{{ statistics.total }}</div>
        </div>
        <div class="glass-card rounded-xl p-4">
          <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">平均 AQI</div>
          <div class="text-2xl font-bold font-mono" :style="{ color: getAQIColor(statistics.avgAQI) }">
            {{ statistics.avgAQI?.toFixed(0) || '--' }}
          </div>
        </div>
        <div class="glass-card rounded-xl p-4">
          <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">最高 AQI</div>
          <div class="text-2xl font-bold font-mono text-red-400">{{ statistics.maxAQI || '--' }}</div>
        </div>
        <div class="glass-card rounded-xl p-4">
          <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">最低 AQI</div>
          <div class="text-2xl font-bold font-mono text-emerald-400">{{ statistics.minAQI || '--' }}</div>
        </div>
        <div class="glass-card rounded-xl p-4">
          <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">优占比</div>
          <div class="text-2xl font-bold font-mono text-green-400">{{ statistics.excellentRate }}%</div>
        </div>
      </div>

      <!-- Data table with export -->
      <div class="glass-card rounded-2xl animate-fade-in" style="animation-delay: 0.2s;">
        <div class="p-6 border-b border-slate-800/50">
          <div class="flex items-center justify-between">
            <h2 class="text-sm text-slate-400 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
              查询结果 <span class="text-slate-500">({{ tableData.length }} 条)</span>
            </h2>
            <div class="flex items-center gap-2">
              <button
                @click="handleExport"
                :disabled="loading || tableData.length === 0"
                class="px-4 py-2 rounded-lg bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                style="font-family: 'Rajdhani', sans-serif; font-size: 13px;"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                导出数据
              </button>
            </div>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-800/50">
                <th class="px-6 py-4 text-left text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  监测时间
                </th>
                <th class="px-6 py-4 text-left text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  城市
                </th>
                <th class="px-6 py-4 text-left text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  站点
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  AQI
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  等级
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  PM2.5
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  PM10
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  SO₂
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  NO₂
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  CO
                </th>
                <th class="px-6 py-4 text-center text-xs text-slate-500 uppercase tracking-wider font-medium" style="font-family: 'Rajdhani', sans-serif;">
                  O₃
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading && tableData.length === 0">
                <td colspan="11" class="px-6 py-12 text-center">
                  <div class="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin mx-auto mb-4"></div>
                  <p class="text-slate-500 text-sm">数据加载中...</p>
                </td>
              </tr>
              <tr v-else-if="tableData.length === 0">
                <td colspan="11" class="px-6 py-12 text-center">
                  <svg class="w-16 h-16 mx-auto mb-4 text-slate-600 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
                  </svg>
                  <p class="text-slate-500">暂无数据，请调整查询条件</p>
                </td>
              </tr>
              <tr
                v-for="row in tableData"
                :key="row.id"
                class="border-b border-slate-800/30 hover:bg-slate-900/30 transition-colors group"
              >
                <td class="px-6 py-4 text-sm text-slate-300 font-mono">
                  {{ formatDateTime(row.monitor_time) }}
                </td>
                <td class="px-6 py-4 text-sm text-slate-300">
                  {{ row.city_name }}
                </td>
                <td class="px-6 py-4 text-sm text-slate-400">
                  {{ row.station_name }}
                </td>
                <td class="px-6 py-4 text-sm font-mono text-center font-bold" :style="{ color: getAQIColor(row.aqi) }">
                  {{ row.aqi }}
                </td>
                <td class="px-6 py-4 text-center">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :style="{ background: `${getAQIColor(row.aqi)}20`, color: getAQIColor(row.aqi) }"
                    style="font-family: 'Rajdhani', sans-serif;"
                  >
                    {{ getAQILevelText(row.aqi) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-center text-slate-400 font-mono">
                  {{ row.pm25?.toFixed(1) || '--' }}
                </td>
                <td class="px-6 py-4 text-sm text-center text-slate-400 font-mono">
                  {{ row.pm10?.toFixed(1) || '--' }}
                </td>
                <td class="px-6 py-4 text-sm text-center text-slate-400 font-mono">
                  {{ row.so2?.toFixed(1) || '--' }}
                </td>
                <td class="px-6 py-4 text-sm text-center text-slate-400 font-mono">
                  {{ row.no2?.toFixed(1) || '--' }}
                </td>
                <td class="px-6 py-4 text-sm text-center text-slate-400 font-mono">
                  {{ row.co?.toFixed(2) || '--' }}
                </td>
                <td class="px-6 py-4 text-sm text-center text-slate-400 font-mono">
                  {{ row.o3?.toFixed(1) || '--' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="total > 0" class="p-6 border-t border-slate-800/50">
          <div class="flex items-center justify-between">
            <div class="text-sm text-slate-500">
              共 {{ total }} 条记录，第 {{ pagination.page }} / {{ Math.ceil(total / pagination.pageSize) }} 页
            </div>
            <div class="flex items-center gap-2">
              <button
                @click="handlePageChange(pagination.page - 1)"
                :disabled="pagination.page === 1"
                class="px-3 py-1.5 rounded-lg bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                上一页
              </button>
              <div class="flex items-center gap-1">
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="handlePageChange(page)"
                  class="w-8 h-8 rounded-lg text-sm transition-all"
                  :class="page === pagination.page
                    ? 'bg-cyan-500 text-white'
                    : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50'"
                >
                  {{ page }}
                </button>
              </div>
              <button
                @click="handlePageChange(pagination.page + 1)"
                :disabled="pagination.page >= Math.ceil(total / pagination.pageSize)"
                class="px-3 py-1.5 rounded-lg bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                下一页
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getHistoricalData, exportHistoricalData } from '@/api/airquality'

const router = useRouter()

// State
const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const statistics = ref(null)

// Query form
const queryForm = ref({
  city: '',
  dateRange: []
})

// Pagination
const pagination = ref({
  page: 1,
  pageSize: 20
})

// Available cities (mock data - should come from API)
const availableCities = ref([
  { code: '110101', name: '东城区' },
  { code: '110102', name: '西城区' },
  { code: '310101', name: '黄浦区' },
  { code: '310104', name: '徐汇区' },
  { code: '440101', name: '市辖区' },
  { code: '440103', name: '荔湾区' }
])

// Computed
const visiblePages = computed(() => {
  const totalPages = Math.ceil(total.value / pagination.value.pageSize)
  const current = pagination.value.page
  const pages = []

  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(totalPages)
    } else if (current >= totalPages - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = totalPages - 4; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(totalPages)
    }
  }

  return pages
})

// Methods
const getAQIColor = (aqi) => {
  if (!aqi) return '#64748b'
  if (aqi <= 50) return '#00e400'
  if (aqi <= 100) return '#ffff00'
  if (aqi <= 150) return '#ff7e00'
  if (aqi <= 200) return '#ff0000'
  if (aqi <= 300) return '#99004c'
  return '#7e0023'
}

const getAQILevelText = (aqi) => {
  if (!aqi) return '--'
  if (aqi <= 50) return '优'
  if (aqi <= 100) return '良'
  if (aqi <= 150) return '轻度'
  if (aqi <= 200) return '中度'
  if (aqi <= 300) return '重度'
  return '严重'
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const goBack = () => {
  router.back()
}

const handleQuery = async () => {
  loading.value = true
  pagination.value.page = 1
  await fetchData()
}

const handleReset = () => {
  queryForm.value = {
    city: '',
    dateRange: []
  }
  pagination.value.page = 1
  tableData.value = []
  total.value = 0
  statistics.value = null
}

const handlePageChange = async (page) => {
  if (page === '...' || page < 1 || page > Math.ceil(total.value / pagination.value.pageSize)) {
    return
  }
  pagination.value.page = page
  await fetchData()
}

const handleExport = async () => {
  try {
    const params = {
      city_code: queryForm.value.city,
      start_date: queryForm.value.dateRange?.[0] || '',
      end_date: queryForm.value.dateRange?.[1] || '',
      format: 'xlsx'
    }

    const blob = await exportHistoricalData(params)

    // Create download link
    const url = window.URL.createObjectURL(new Blob([blob]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `历史数据_${new Date().getTime()}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功')
  } catch (error) {
    console.error('Export failed:', error)
    ElMessage.error('导出失败')
  }
}

const calculateStatistics = (data) => {
  if (!data || data.length === 0) return null

  const aqiValues = data.map(d => d.aqi)
  const sum = aqiValues.reduce((acc, val) => acc + val, 0)
  const avg = sum / aqiValues.length
  const max = Math.max(...aqiValues)
  const min = Math.min(...aqiValues)
  const excellentCount = aqiValues.filter(v => v <= 50).length
  const excellentRate = ((excellentCount / aqiValues.length) * 100).toFixed(1)

  return {
    total: data.length,
    avgAQI: avg,
    maxAQI: max,
    minAQI: min,
    excellentRate
  }
}

const fetchData = async () => {
  loading.value = true

  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
      city_code: queryForm.value.city || undefined,
      start_date: queryForm.value.dateRange?.[0] || undefined,
      end_date: queryForm.value.dateRange?.[1] || undefined
    }

    // Remove undefined values
    Object.keys(params).forEach(key => {
      if (params[key] === undefined) {
        delete params[key]
      }
    })

    const response = await getHistoricalData(params)

    if (response.code === 0) {
      tableData.value = response.data || []
      total.value = response.total || 0

      // Calculate statistics for current page
      if (tableData.value.length > 0) {
        statistics.value = calculateStatistics(tableData.value)
      } else {
        statistics.value = null
      }
    } else {
      ElMessage.error(response.message || '查询失败')
    }
  } catch (error) {
    console.error('Failed to fetch historical data:', error)
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Load initial data
  fetchData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  border-color: rgba(148, 163, 184, 0.2);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
}

.grid-background {
  background-image: linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.hover-scale {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-scale:hover {
  transform: translateY(-1px);
}

.animate-fade-in {
  animation: fade-in 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

.animate-fade-in-down {
  animation: fade-in-down 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

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

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Custom Element Plus overrides */
:deep(.custom-select .el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: none;
  transition: all 0.3s;
}

:deep(.custom-select .el-input__wrapper:hover) {
  border-color: rgba(148, 163, 184, 0.3);
}

:deep(.custom-select .el-input__wrapper.is-focus) {
  border-color: rgba(6, 182, 212, 0.5);
}

:deep(.custom-select .el-input__inner) {
  color: #e2e8f0;
  font-family: 'IBM Plex Sans', sans-serif;
}

:deep(.custom-date-picker .el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: none;
}

:deep(.custom-date-picker .el-input__wrapper:hover) {
  border-color: rgba(148, 163, 184, 0.3);
}

:deep(.custom-date-picker .el-input__wrapper.is-focus) {
  border-color: rgba(6, 182, 212, 0.5);
}

:deep(.custom-date-picker .el-input__inner) {
  color: #e2e8f0;
  font-family: 'IBM Plex Sans', sans-serif;
}

:deep(.custom-date-picker .el-input__prefix) {
  color: #64748b;
}

:deep(.dark-select-dropdown) {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(12px);
}

:deep(.dark-select-dropdown .el-select-dropdown__item) {
  color: #e2e8f0;
  font-family: 'IBM Plex Sans', sans-serif;
}

:deep(.dark-select-dropdown .el-select-dropdown__item.hover) {
  background: rgba(6, 182, 212, 0.1);
}

:deep(.dark-select-dropdown .el-select-dropdown__item.selected) {
  color: #06b6d4;
  background: rgba(6, 182, 212, 0.15);
}

:deep(.dark-date-picker) {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(12px);
}

:deep(.dark-date-picker .el-date-table th) {
  color: #64748b;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

:deep(.dark-date-picker .el-date-table td) {
  color: #e2e8f0;
}

:deep(.dark-date-picker .el-date-table td.in-range div) {
  background: rgba(6, 182, 212, 0.2);
}

:deep(.dark-date-picker .el-date-table td.start-date div,
  .dark-date-picker .el-date-table td.end-date div) {
  background: rgba(6, 182, 212, 0.5);
}

:deep(.dark-date-picker .el-date-table td.today div) {
  color: #06b6d4;
}

:deep(.dark-date-picker .el-picker-panel__content .cell:hover) {
  color: #06b6d4;
}
</style>
