<template>
  <div class="historical-data-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回概览
        </el-button>
        <div class="header-info">
          <h1 class="page-title">历史数据查询</h1>
          <p class="page-subtitle">检索与回溯历史空气质量监测数据</p>
        </div>
      </div>
      <div class="header-actions">
        <el-button
          type="primary"
          @click="handleExport"
          :disabled="loading || tableData.length === 0"
          :loading="exporting"
        >
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- Query Form -->
    <div class="card query-card">
      <div class="query-form">
        <div class="form-row">
          <div class="form-item">
            <label class="form-label">城市</label>
            <el-select
              v-model="queryForm.city"
              filterable
              placeholder="选择城市"
              clearable
              style="width: 100%"
            >
              <el-option
                v-for="city in availableCities"
                :key="city.code"
                :label="city.name"
                :value="city.code"
              />
            </el-select>
          </div>
          <div class="form-item form-item-wide">
            <label class="form-label">日期范围</label>
            <el-date-picker
              v-model="queryForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              style="width: 100%"
              unlink-panels
            />
          </div>
          <div class="form-item form-item-actions">
            <el-button type="primary" @click="handleQuery" :loading="loading">
              查询
            </el-button>
            <el-button @click="handleReset">重置</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Summary -->
    <div v-if="statistics" class="stats-row">
      <div class="stat-card">
        <div class="stat-label">数据总量</div>
        <div class="stat-value">{{ statistics.total }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">平均 AQI</div>
        <div class="stat-value" :style="{ color: getAQIColor(statistics.avgAQI) }">
          {{ statistics.avgAQI ?? '--' }}
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-label">最高 AQI</div>
        <div class="stat-value stat-danger">{{ statistics.maxAQI ?? '--' }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">最低 AQI</div>
        <div class="stat-value stat-success">{{ statistics.minAQI ?? '--' }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">优占比</div>
        <div class="stat-value stat-primary">{{ statistics.excellentRate ?? '--' }}%</div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="card table-card">
      <div class="table-header">
        <h3 class="table-title">
          查询结果
          <span class="record-count">({{ tableData.length }} 条)</span>
        </h3>
      </div>

      <el-table
        :data="tableData"
        v-loading="loading && tableData.length === 0"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="monitor_time" label="监测时间" width="180">
          <template #default="{ row }">
            <span class="mono-text">{{ formatDateTime(row.monitor_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="city_name" label="城市" width="120" />
        <el-table-column prop="station_name" label="站点" width="180" />
        <el-table-column prop="aqi" label="AQI" width="100" align="center">
          <template #default="{ row }">
            <span class="aqi-value" :style="{ color: getAQIColor(row.aqi) }">
              {{ row.aqi }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="等级" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getAQITagType(row.aqi)" size="small">
              {{ getAQILevelText(row.aqi) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pm25" label="PM2.5" width="100" align="center">
          <template #default="{ row }">
            <span class="mono-text">{{ formatNumber(row.pm25, 1) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm10" label="PM10" width="100" align="center">
          <template #default="{ row }">
            <span class="mono-text">{{ formatNumber(row.pm10, 1) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="so2" label="SO₂" width="100" align="center">
          <template #default="{ row }">
            <span class="mono-text">{{ formatNumber(row.so2, 1) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="no2" label="NO₂" width="100" align="center">
          <template #default="{ row }">
            <span class="mono-text">{{ formatNumber(row.no2, 1) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="co" label="CO" width="100" align="center">
          <template #default="{ row }">
            <span class="mono-text">{{ formatNumber(row.co, 2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="o3" label="O₃" width="100" align="center">
          <template #default="{ row }">
            <span class="mono-text">{{ formatNumber(row.o3, 1) }}</span>
          </template>
        </el-table-column>
      </el-table>

      <template v-if="tableData.length === 0 && !loading">
        <el-empty description="暂无数据，请调整查询条件" :image-size="100" />
      </template>

      <!-- Pagination -->
      <div v-if="total > 0" class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getHistoricalData, exportHistoricalData, getHistoricalStatistics, getOverview } from '@/api/airquality'

const router = useRouter()

// State
const loading = ref(false)
const exporting = ref(false)
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

// Available cities (fetched from API)
const availableCities = ref([])

// Fetch available cities from overview API
const fetchAvailableCities = async () => {
  try {
    const response = await getOverview()
    if (response.code === 0 && response.data?.map_data) {
      // Extract unique cities from map_data
      const cityMap = new Map()
      response.data.map_data.forEach(city => {
        if (!cityMap.has(city.city_code)) {
          cityMap.set(city.city_code, {
            code: city.city_code,
            name: city.city_name
          })
        }
      })
      availableCities.value = Array.from(cityMap.values()).sort((a, b) => a.name.localeCompare(b.name, 'zh-CN'))
    }
  } catch (error) {
    console.error('Failed to fetch available cities:', error)
  }
}

// Methods
const getAQIColor = (aqi) => {
  if (!aqi) return 'var(--text-secondary)'
  if (aqi <= 50) return '#10B981'
  if (aqi <= 100) return '#FBBF24'
  if (aqi <= 150) return '#F97316'
  if (aqi <= 200) return '#EF4444'
  if (aqi <= 300) return '#A855F7'
  return '#7F1D1D'
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

const getAQITagType = (aqi) => {
  if (!aqi) return 'info'
  if (aqi <= 50) return 'success'
  if (aqi <= 100) return 'warning'
  if (aqi <= 150) return 'warning'
  if (aqi <= 200) return 'danger'
  return 'danger'
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

const formatNumber = (value, decimals = 1) => {
  if (value === null || value === undefined || value === '') return '--'
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return '--'
  return num.toFixed(decimals)
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
  pagination.value.page = page
  await fetchData()
}

const handleSizeChange = async (size) => {
  pagination.value.pageSize = size
  pagination.value.page = 1
  await fetchData()
}

const handleExport = async () => {
  exporting.value = true
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
  } finally {
    exporting.value = false
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
    } else {
      ElMessage.error(response.message || '查询失败')
    }

    // Fetch statistics separately (based on all filtered data)
    await fetchStatistics()
  } catch (error) {
    console.error('Failed to fetch historical data:', error)
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

const fetchStatistics = async () => {
  try {
    const params = {
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

    const response = await getHistoricalStatistics(params)
    if (response.code === 0) {
      statistics.value = response.data
    }
  } catch (error) {
    console.error('Failed to fetch statistics:', error)
  }
}

onMounted(() => {
  fetchAvailableCities()
  fetchData()
})
</script>

<style scoped>
.historical-data-page {
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.back-button {
  font-size: 14px;
  color: var(--text-secondary);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-lg);
}

.card:last-child {
  margin-bottom: 0;
}

/* Query Form */
.query-card {
  padding: var(--spacing-lg);
}

.query-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-row {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  align-items: flex-end;
}

.form-item {
  flex: 1;
  min-width: 200px;
}

.form-item-wide {
  flex: 2;
  min-width: 300px;
}

.form-item-actions {
  flex: 0;
  display: flex;
  gap: var(--spacing-sm);
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: var(--spacing-xs);
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  padding: var(--spacing-md);
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  font-family: var(--font-mono);
}

.stat-danger { color: var(--error); }
.stat-success { color: var(--success); }
.stat-primary { color: var(--primary); }

/* Table Card */
.table-card {
  overflow: hidden;
}

.table-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.record-count {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 400;
  margin-left: var(--spacing-xs);
}

.aqi-value {
  font-weight: 700;
  font-family: var(--font-mono);
}

.mono-text {
  font-family: var(--font-mono);
}

.pagination-wrapper {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
}

/* Responsive */
@media (max-width: 1024px) {
  .stats-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .historical-data-page {
    padding: var(--spacing-md);
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .form-row {
    flex-direction: column;
  }

  .form-item,
  .form-item-wide {
    min-width: 100%;
  }

  .form-item-actions {
    width: 100%;
  }

  .form-item-actions .el-button {
    flex: 1;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
