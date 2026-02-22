<template>
  <div class="air-quality-manage-container">
    <!-- Header Section -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="page-indicator"></div>
          <div class="title-group">
            <h1 class="page-title">空气质量数据管理</h1>
            <p class="page-subtitle">AIR QUALITY DATA MANAGEMENT</p>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-chip">
            <span class="stat-label">记录总数</span>
            <span class="stat-value">{{ formatNumber(total) }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Filter Section -->
    <section class="filter-section">
      <div class="filter-header" @click="toggleFilterCollapse">
        <div class="filter-title">
          <svg class="filter-icon" viewBox="0 0 20 20" fill="none">
            <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>数据过滤器</span>
          <span class="filter-count" v-if="hasActiveFilters">{{ activeFilterCount }}</span>
        </div>
        <svg class="collapse-icon" :class="{ collapsed: isFilterCollapsed }" viewBox="0 0 20 20" fill="none">
          <path d="M5 15l7-7 7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>

      <div class="filter-content" :class="{ collapsed: isFilterCollapsed }">
        <div class="filter-grid">
          <div class="filter-item">
            <label class="filter-label">城市</label>
            <el-select v-model="filters.city_code" placeholder="全部城市" clearable filterable>
              <el-option v-for="city in cities" :key="city.code" :label="city.name" :value="city.code" />
            </el-select>
          </div>

          <div class="filter-item">
            <label class="filter-label">监测站点</label>
            <el-select v-model="filters.station_code" placeholder="全部站点" clearable filterable>
              <el-option v-for="station in stations" :key="station.code" :label="station.name" :value="station.code" />
            </el-select>
          </div>

          <div class="filter-item">
            <label class="filter-label">空气质量等级</label>
            <el-select v-model="filters.quality_level" placeholder="全部等级" clearable>
              <el-option v-for="level in qualityLevels" :key="level.value" :label="level.label" :value="level.value">
                <span class="level-option">
                  <span class="level-dot" :style="{ background: level.color }"></span>
                  {{ level.label }}
                </span>
              </el-option>
            </el-select>
          </div>

          <div class="filter-item">
            <label class="filter-label">监测时间</label>
            <el-date-picker
              v-model="filters.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
          </div>
        </div>

        <div class="filter-actions">
          <button class="filter-btn secondary" @click="resetFilters">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            重置
          </button>
          <button class="filter-btn primary" @click="applyFilters">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            搜索
          </button>
        </div>
      </div>
    </section>

    <!-- Data Table Section -->
    <section class="table-section">
      <!-- Toolbar -->
      <div class="table-toolbar">
        <div class="selection-info" v-if="selectedRows.length > 0">
          <span class="selection-count">{{ selectedRows.length }}</span>
          <span class="selection-text">项已选择</span>
        </div>
        <div class="toolbar-actions">
          <button class="toolbar-btn danger" :disabled="selectedRows.length === 0" @click="handleBatchDelete">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            批量删除
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="table-container">
        <el-table
          ref="tableRef"
          :data="tableData"
          v-loading="loading"
          class="data-table"
          stripe
          @selection-change="handleSelectionChange"
          @sort-change="handleSortChange"
        >
          <el-table-column type="selection" width="50" fixed />

          <el-table-column prop="monitor_time" label="监测时间" width="180" sortable>
            <template #default="{ row }">
              <span class="time-cell">{{ formatDateTime(row.monitor_time) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="province_name" label="省份" width="120" />

          <el-table-column prop="city_name" label="城市" width="120" />

          <el-table-column prop="station_name" label="监测站点" width="180" />

          <el-table-column prop="aqi" label="AQI" width="100" sortable>
            <template #default="{ row }">
              <span class="aqi-cell" :style="{ color: getAQIColor(row.aqi) }">{{ row.aqi }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="pm25" label="PM2.5" width="100" sortable>
            <template #default="{ row }">
              <span class="value-cell">{{ formatValue(row.pm25) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="pm10" label="PM10" width="100" sortable>
            <template #default="{ row }">
              <span class="value-cell">{{ formatValue(row.pm10) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="so2" label="SO₂" width="100" sortable>
            <template #default="{ row }">
              <span class="value-cell">{{ formatValue(row.so2) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="no2" label="NO₂" width="100" sortable>
            <template #default="{ row }">
              <span class="value-cell">{{ formatValue(row.no2) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="co" label="CO" width="100" sortable>
            <template #default="{ row }">
              <span class="value-cell">{{ formatValue(row.co) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="o3" label="O₃" width="100" sortable>
            <template #default="{ row }">
              <span class="value-cell">{{ formatValue(row.o3) }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="quality_level" label="质量等级" width="120" sortable>
            <template #default="{ row }">
              <span class="level-badge" :style="getLevelStyle(row.quality_level)">
                {{ getLevelLabel(row.quality_level) }}
              </span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="140" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <button class="action-btn edit" @click="handleEdit(row)">
                  <svg viewBox="0 0 20 20" fill="none">
                    <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button class="action-btn delete" @click="handleDelete(row)">
                  <svg viewBox="0 0 20 20" fill="none">
                    <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Pagination -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchData"
          @current-change="fetchData"
        />
      </div>
    </section>

    <!-- Edit Dialog -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑监测数据"
      width="600px"
      class="edit-dialog"
      :close-on-click-modal="false"
    >
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="120px" class="edit-form">
        <el-form-item label="监测时间">
          <el-input
            :model-value="formatDateTime(editForm.monitor_time)"
            disabled
            style="width: 100%"
          >
            <template #prefix>
              <svg style="width: 16px; height: 16px; color: var(--text-muted)" viewBox="0 0 20 20" fill="none">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M10 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 10h4m12 0h4M4.93 15.07l2.83-2.83m8.48-8.48l2.83-2.83" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="监测站点">
          <el-input
            :model-value="editForm.station_name || stations.find(s => s.id === editForm.station_id)?.name || ''"
            disabled
            style="width: 100%"
          >
            <template #prefix>
              <svg style="width: 16px; height: 16px; color: var(--text-muted)" viewBox="0 0 20 20" fill="none">
                <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </template>
          </el-input>
        </el-form-item>

        <div class="form-section-title">污染物浓度</div>

        <el-form-item label="AQI" prop="aqi">
          <el-input-number v-model="editForm.aqi" :min="0" :max="500" :precision="0" controls-position="right" style="width: 100%" />
        </el-form-item>

        <el-form-item label="PM2.5 (μg/m³)" prop="pm25">
          <el-input-number v-model="editForm.pm25" :min="0" :precision="1" controls-position="right" style="width: 100%" />
        </el-form-item>

        <el-form-item label="PM10 (μg/m³)" prop="pm10">
          <el-input-number v-model="editForm.pm10" :min="0" :precision="1" controls-position="right" style="width: 100%" />
        </el-form-item>

        <el-form-item label="SO₂ (μg/m³)" prop="so2">
          <el-input-number v-model="editForm.so2" :min="0" :precision="1" controls-position="right" style="width: 100%" />
        </el-form-item>

        <el-form-item label="NO₂ (μg/m³)" prop="no2">
          <el-input-number v-model="editForm.no2" :min="0" :precision="1" controls-position="right" style="width: 100%" />
        </el-form-item>

        <el-form-item label="CO (mg/m³)" prop="co">
          <el-input-number v-model="editForm.co" :min="0" :precision="2" controls-position="right" style="width: 100%" />
        </el-form-item>

        <el-form-item label="O₃ (μg/m³)" prop="o3">
          <el-input-number v-model="editForm.o3" :min="0" :precision="1" controls-position="right" style="width: 100%" />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <button class="dialog-btn secondary" @click="editDialogVisible = false">取消</button>
          <button class="dialog-btn primary" @click="handleSaveEdit">保存</button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getAirQualityDataList,
  updateAirQualityData,
  deleteAirQualityDataById,
  deleteAirQualityDataByIds
} from '@/api/admin'

// State
const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const selectedRows = ref([])
const tableRef = ref(null)

const isFilterCollapsed = ref(false)

// Dynamic cities and stations (extracted from data)
const cities = ref([])
const stations = ref([])
const allDataCache = ref([])

const filters = reactive({
  city_code: '',
  station_code: '',
  quality_level: '',
  dateRange: null
})

const pagination = reactive({
  page: 1,
  pageSize: 20
})

const sortInfo = reactive({
  prop: 'monitor_time',
  order: 'descending'
})

const qualityLevels = [
  { value: 'EXCELLENT', label: '优', color: '#00e400' },
  { value: 'GOOD', label: '良', color: '#ffff00' },
  { value: 'LIGHT_POLLUTION', label: '轻度污染', color: '#ff7e00' },
  { value: 'MODERATE_POLLUTION', label: '中度污染', color: '#ff0000' },
  { value: 'HEAVY_POLLUTION', label: '重度污染', color: '#99004c' },
  { value: 'SEVERE_POLLUTION', label: '严重污染', color: '#7e0023' }
]

// Edit dialog
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const editForm = reactive({
  id: null,
  station_id: null,
  station_code: '',
  station_name: '',
  monitor_time: '',
  aqi: 0,
  pm25: 0,
  pm10: 0,
  so2: 0,
  no2: 0,
  co: 0,
  o3: 0
})

const editRules = {
  aqi: [
    { required: true, message: '请输入AQI值', trigger: 'blur' },
    { type: 'number', min: 0, max: 500, message: 'AQI值范围0-500', trigger: 'blur' }
  ],
  pm25: [{ type: 'number', min: 0, message: 'PM2.5不能为负数', trigger: 'blur' }],
  pm10: [{ type: 'number', min: 0, message: 'PM10不能为负数', trigger: 'blur' }],
  so2: [{ type: 'number', min: 0, message: 'SO2不能为负数', trigger: 'blur' }],
  no2: [{ type: 'number', min: 0, message: 'NO2不能为负数', trigger: 'blur' }],
  co: [{ type: 'number', min: 0, message: 'CO不能为负数', trigger: 'blur' }],
  o3: [{ type: 'number', min: 0, message: 'O3不能为负数', trigger: 'blur' }]
}

// Computed
const hasActiveFilters = computed(() => {
  return filters.city_code || filters.station_code || filters.quality_level || filters.dateRange
})

const activeFilterCount = computed(() => {
  let count = 0
  if (filters.city_code) count++
  if (filters.station_code) count++
  if (filters.quality_level) count++
  if (filters.dateRange) count++
  return count
})

// Methods
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ordering: sortInfo.order === 'descending' ? `-${sortInfo.prop}` : sortInfo.prop
    }

    if (filters.city_code) params.city_code = filters.city_code
    if (filters.station_code) params.station_code = filters.station_code
    if (filters.quality_level) params.quality_level = filters.quality_level
    if (filters.dateRange) {
      params.start_date = filters.dateRange[0]
      params.end_date = filters.dateRange[1]
    }

    const response = await getAirQualityDataList(params)
    if (response.code === 0) {
      tableData.value = response.data
      total.value = response.total

      // Extract unique cities and stations for filter dropdowns
      extractFiltersFromData(response.data)
    }
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// Extract unique cities and stations from loaded data
const extractFiltersFromData = (data) => {
  const cityMap = new Map()
  const stationMap = new Map()

  data.forEach(row => {
    if (row.city_code && row.city_name) {
      cityMap.set(row.city_code, row.city_name)
    }
    if (row.station_code && row.station_name) {
      stationMap.set(row.station_code, {
        code: row.station_code,
        name: row.station_name,
        id: row.station_id
      })
    }
  })

  // Update ref values
  cities.value = Array.from(cityMap.entries()).map(([code, name]) => ({ code, name }))
  stations.value = Array.from(stationMap.values())
}

// Fetch all data without pagination to build filter options
const fetchFilterOptions = async () => {
  try {
    // Use maximum page_size (200) to get enough data for filter options
    const response = await getAirQualityDataList({ page: 1, page_size: 200 })
    if (response.code === 0 && response.data.length > 0) {
      extractFiltersFromData(response.data)
    }
  } catch (error) {
    console.error('Failed to fetch filter options:', error)
  }
}

const toggleFilterCollapse = () => {
  isFilterCollapsed.value = !isFilterCollapsed.value
}

const resetFilters = () => {
  filters.city_code = ''
  filters.station_code = ''
  filters.quality_level = ''
  filters.dateRange = null
  pagination.page = 1
  fetchData()
}

const applyFilters = () => {
  pagination.page = 1
  fetchData()
}

const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

const handleSortChange = ({ prop, order }) => {
  sortInfo.prop = prop
  sortInfo.order = order
  fetchData()
}

const handleEdit = (row) => {
  Object.assign(editForm, {
    id: row.id,
    station_id: Number(row.station_id),
    station_code: row.station_code,
    station_name: row.station_name,
    monitor_time: row.monitor_time,
    aqi: Number(row.aqi) || 0,
    pm25: Number(row.pm25) || 0,
    pm10: Number(row.pm10) || 0,
    so2: Number(row.so2) || 0,
    no2: Number(row.no2) || 0,
    co: Number(row.co) || 0,
    o3: Number(row.o3) || 0
  })
  editDialogVisible.value = true
}

const handleSaveEdit = async () => {
  try {
    await editFormRef.value.validate()
    const response = await updateAirQualityData(editForm)
    if (response.code === 0) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      fetchData()
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('更新失败')
    }
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这条数据吗？', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const response = await deleteAirQualityDataById(row.id)
    if (response.code === 0) {
      ElMessage.success('删除成功')
      fetchData()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条数据吗？`, '确认批量删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const ids = selectedRows.value.map(row => row.id)
    const response = await deleteAirQualityDataByIds(ids)
    if (response.code === 0) {
      ElMessage.success('批量删除成功')
      tableRef.value?.clearSelection()
      fetchData()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// Utility functions
const formatNumber = (num) => {
  if (!num) return '0'
  return num.toLocaleString()
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatValue = (val) => {
  if (val === null || val === undefined || val === '') return '-'
  const num = typeof val === 'string' ? parseFloat(val) : val
  if (isNaN(num)) return '-'
  return num.toFixed(1)
}

const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#00e400'
  if (aqi <= 100) return '#ffff00'
  if (aqi <= 150) return '#ff7e00'
  if (aqi <= 200) return '#ff0000'
  if (aqi <= 300) return '#99004c'
  return '#7e0023'
}

const getLevelLabel = (level) => {
  const levelMap = {
    'EXCELLENT': '优',
    'GOOD': '良',
    'LIGHT_POLLUTION': '轻度污染',
    'MODERATE_POLLUTION': '中度污染',
    'HEAVY_POLLUTION': '重度污染',
    'SEVERE_POLLUTION': '严重污染'
  }
  return levelMap[level] || level
}

const getLevelStyle = (level) => {
  const color = getAQIColor(level?.aqi || 0)
  return {
    background: `rgba(${hexToRgb(color)}, 0.15)`,
    color: color
  }
}

const hexToRgb = (hex) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result
    ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}`
    : '0, 0, 0'
}

// Lifecycle
onMounted(() => {
  fetchFilterOptions() // Load filter options first
  fetchData()
})
</script>

<style scoped>
/* Base Variables */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
  --bg-primary: #0a0e1a;
  --bg-card: #111827;
  --bg-hover: #1f2937;
  --bg-soft: rgba(255, 255, 255, 0.03);
  --border: rgba(34, 211, 238, 0.1);
  --border-hover: rgba(34, 211, 238, 0.2);
  --text: #f3f4f6;
  --text-secondary: #9ca3af;
  --text-muted: #6b7280;
  --primary: #22d3ee;
  --primary-dark: #0891b2;
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #fbbf24;
  --purple: #a855f7;
}

/* Container */
.air-quality-manage-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.page-header {
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-indicator {
  width: 4px;
  height: 36px;
  background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 2px;
  box-shadow: 0 0 12px rgba(34, 211, 238, 0.4);
}

.title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

.header-stats {
  display: flex;
  gap: 12px;
}

.stat-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary);
}

/* Filter Section */
.filter-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.filter-section:hover {
  border-color: var(--border-hover);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s ease;
}

.filter-header:hover {
  background: var(--bg-soft);
}

.filter-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}

.filter-icon {
  width: 18px;
  height: 18px;
  color: var(--primary);
}

.filter-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: var(--primary);
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--bg-primary);
}

.collapse-icon {
  width: 16px;
  height: 16px;
  color: var(--text-muted);
  transition: transform 0.3s ease;
}

.collapse-icon.collapsed {
  transform: rotate(180deg);
}

.filter-content {
  padding: 20px;
  border-top: 1px solid var(--border);
  transition: all 0.3s ease;
}

.filter-content.collapsed {
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
  overflow: hidden;
  border-top-color: transparent;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.filter-btn svg {
  width: 16px;
  height: 16px;
}

.filter-btn.secondary {
  background: var(--bg-hover);
  color: var(--text-secondary);
}

.filter-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text);
}

.filter-btn.primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: var(--bg-primary);
}

.filter-btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
}

/* Level Option */
.level-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.level-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Table Section */
.table-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.selection-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.selection-count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary);
}

.selection-text {
  font-size: 13px;
  color: var(--text-secondary);
}

.toolbar-actions {
  display: flex;
  gap: 12px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.toolbar-btn svg {
  width: 16px;
  height: 16px;
}

.toolbar-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.toolbar-btn.danger {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.toolbar-btn.danger:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
}

/* Table Container */
.table-container {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
}

.data-table {
  width: 100%;
}

:deep(.el-table) {
  background: transparent;
  color: var(--text);
}

:deep(.el-table th.el-table__cell) {
  background: var(--bg-soft);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border);
  padding: 14px 12px;
}

:deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid var(--border);
  padding: 12px;
}

:deep(.el-table tr:hover > td) {
  background: var(--bg-hover);
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: rgba(255, 255, 255, 0.01);
}

:deep(.el-table__empty-block) {
  background: transparent;
  color: var(--text-muted);
}

/* Table Cells */
.time-cell {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--text-secondary);
}

.aqi-cell {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 14px;
}

.value-cell {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--text-secondary);
}

.level-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.action-btn.edit:hover {
  background: rgba(34, 211, 238, 0.1);
  border-color: var(--primary);
  color: var(--primary);
}

.action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: var(--danger);
  color: var(--danger);
}

/* Pagination */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

:deep(.el-pagination) {
  color: var(--text-secondary);
}

:deep(.el-pagination button) {
  background: var(--bg-card);
  color: var(--text-secondary);
  border-color: var(--border);
  border-radius: 8px;
}

:deep(.el-pagination button:hover) {
  color: var(--primary);
  border-color: var(--primary);
}

:deep(.el-pagination .el-pager li) {
  background: var(--bg-card);
  color: var(--text-secondary);
  border-radius: 8px;
  margin: 0 2px;
}

:deep(.el-pagination .el-pager li:hover) {
  color: var(--primary);
}

:deep(.el-pagination .el-pager li.is-active) {
  background: var(--primary);
  color: var(--bg-primary);
}

:deep(.el-pagination .el-pager li.is-active:hover) {
  color: var(--bg-primary);
}

/* Edit Dialog */
:deep(.edit-dialog) {
  background: var(--bg-card);
}

:deep(.edit-dialog .el-dialog__header) {
  border-bottom: 1px solid var(--border);
  padding: 20px 24px;
}

:deep(.edit-dialog .el-dialog__title) {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

:deep(.edit-dialog .el-dialog__body) {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

:deep(.edit-dialog .el-dialog__footer) {
  border-top: 1px solid var(--border);
  padding: 16px 24px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 8px;
  margin-bottom: 8px;
}

:deep(.edit-form .el-form-item__label) {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

:deep(.edit-form .el-input__wrapper) {
  background: var(--bg-hover);
  border-color: var(--border);
  box-shadow: none;
}

:deep(.edit-form .el-input__wrapper:hover) {
  border-color: var(--border-hover);
}

:deep(.edit-form .el-input__wrapper.is-focus) {
  border-color: var(--primary);
}

:deep(.edit-form .el-input__inner) {
  color: var(--text);
}

:deep(.edit-form .el-select .el-input__wrapper) {
  background: var(--bg-hover);
}

:deep(.edit-form .el-select-dropdown) {
  background: var(--bg-card);
  border-color: var(--border);
}

:deep(.edit-form .el-select-dropdown__item) {
  color: var(--text);
}

:deep(.edit-form .el-select-dropdown__item:hover) {
  background: var(--bg-hover);
}

:deep(.edit-form .el-select-dropdown__item.is-selected) {
  background: rgba(34, 211, 238, 0.1);
  color: var(--primary);
}

/* Dialog Footer */
.dialog-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.dialog-btn {
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.dialog-btn.secondary {
  background: var(--bg-hover);
  color: var(--text);
}

.dialog-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.dialog-btn.primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: var(--bg-primary);
}

.dialog-btn.primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
}

/* Responsive */
@media (max-width: 1280px) {
  .filter-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    flex-direction: column;
  }

  .filter-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
