<template>
  <div class="alarms-page">
    <!-- Top Stats Cards -->
    <div class="stats-row">
      <div v-for="(stat, index) in alarmStats" :key="index" class="stat-card" :class="`stat-${index}`">
        <div class="stat-background">
          <div class="grid-pattern"></div>
          <div class="glow-effect" :style="{ background: stat.color }"></div>
        </div>
        <div class="stat-content">
          <div class="stat-icon" :style="{ color: stat.color, background: `${stat.color}15` }">
            <component :is="stat.icon" />
          </div>
          <div class="stat-info">
            <div class="stat-label">{{ stat.label }}</div>
            <div class="stat-value">
              <span class="value-number">{{ stat.value }}</span>
              <span class="stat-unit">{{ stat.unit }}</span>
            </div>
            <div class="stat-trend" :class="stat.trendClass" v-if="stat.change">
              <el-icon><icon-ep-caret-top v-if="stat.trend === 'up'" /><icon-ep-caret-bottom v-else /></el-icon>
              <span>{{ stat.change }}</span>
            </div>
          </div>
        </div>
        <div class="stat-pulse" v-if="stat.pulse" :style="{ borderColor: stat.color }"></div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Left: Alarm List -->
      <div class="alarms-section">
        <div class="section-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-warning /></span>
              告警列表
              <span class="live-indicator" v-if="hasPendingAlarms">
                <span class="live-dot"></span>
                实时监控
              </span>
            </h3>
            <div class="header-actions">
              <el-button type="primary" @click="refreshAlarms" :loading="loading">
                刷新
              </el-button>
            </div>
          </div>

          <!-- Filters -->
          <div class="filter-bar">
            <div class="filter-group">
              <el-select v-model="filters.status" placeholder="告警状态" clearable @change="applyFilters">
                <el-option label="待处理" value="PENDING" />
                <el-option label="已处理" value="PROCESSED" />
                <el-option label="已忽略" value="IGNORED" />
              </el-select>
            </div>
            <div class="filter-group">
              <el-select v-model="filters.type" placeholder="告警类型" clearable @change="applyFilters">
                <el-option label="超限告警" value="THRESHOLD" />
                <el-option label="突变告警" value="SUDDEN_CHANGE" />
                <el-option label="离线告警" value="OFFLINE" />
              </el-select>
            </div>
            <div class="filter-group">
              <el-select v-model="filters.energyType" placeholder="能源类型" clearable @change="applyFilters">
                <el-option label="电" value="ELECTRICITY" />
                <el-option label="水" value="WATER" />
                <el-option label="气" value="GAS" />
              </el-select>
            </div>
            <div class="filter-group">
              <el-date-picker
                v-model="filters.dateRange"
                type="datetimerange"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
                @change="applyFilters"
              />
            </div>
            <div class="filter-group">
              <el-input
                v-model="filters.search"
                placeholder="搜索设备或位置"
                prefix-icon="Search"
                clearable
                @input="debounceSearch"
              />
            </div>
          </div>

          <!-- Alarm Table -->
          <div class="table-wrapper">
            <el-table
              :data="filteredAlarms"
              v-loading="loading"
              stripe
              class="alarms-table"
              :empty-text="emptyText"
            >
              <el-table-column type="index" label="#" width="50" />
              <el-table-column prop="alarm_type" label="类型" width="100">
                <template #default="{ row }">
                  <el-tag :type="getAlarmTypeTag(row.alarm_type)" size="small">
                    {{ getAlarmTypeLabel(row.alarm_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="级别" width="80">
                <template #default="{ row }">
                  <div class="severity-indicator" :class="`severity-${getSeverity(row)}`">
                    <span class="severity-dot"></span>
                    <span>{{ getSeverityLabel(row) }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="device_name" label="设备" width="150">
                <template #default="{ row }">
                  <div class="device-cell">
                    <span class="device-name">{{ row.device_name || row.device || '--' }}</span>
                    <span class="device-location">{{ row.location || '' }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="alarm_value" label="告警值" width="100" align="right">
                <template #default="{ row }">
                  <span class="alarm-value">{{ formatAlarmValue(row) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="threshold_value" label="阈值" width="100" align="right">
                <template #default="{ row }">
                  <span class="threshold-value">{{ row.threshold_value || '--' }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="alarm_time" label="告警时间" width="170">
                <template #default="{ row }">
                  <span class="alarm-time">{{ formatTime(row.alarm_time) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="90">
                <template #default="{ row }">
                  <el-tag :type="getStatusTag(row.status)" size="small" effect="plain">
                    {{ getStatusLabel(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="160" fixed="right">
                <template #default="{ row }">
                  <el-button-group>
                    <el-button size="small" text @click="viewDetail(row)">
                      <el-icon><icon-ep-view /></el-icon>
                      详情
                    </el-button>
                    <el-button
                      size="small"
                      text
                      type="primary"
                      @click="openHandleDialog(row)"
                      :disabled="row.status !== 'PENDING'"
                    >
                      <el-icon><icon-ep-check /></el-icon>
                      处理
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>

            <!-- Pagination -->
            <div class="pagination-wrapper">
              <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="pagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handlePageChange"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Alarm Rules -->
      <div class="rules-section">
        <div class="section-card rules-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-setting /></span>
              告警规则
            </h3>
            <el-button type="primary" size="small" @click="openRuleDialog()">
              新增规则
            </el-button>
          </div>

          <!-- Rules List -->
          <div class="rules-list">
            <div
              v-for="rule in alarmRules"
              :key="rule.id"
              class="rule-item"
              :class="{ 'rule-inactive': !rule.is_active }"
            >
              <div class="rule-header">
                <div class="rule-title">
                  <span class="rule-name">{{ rule.name }}</span>
                  <el-tag v-if="rule.is_active" type="success" size="small" effect="plain">启用</el-tag>
                  <el-tag v-else type="info" size="small" effect="plain">禁用</el-tag>
                </div>
                <div class="rule-actions">
                  <el-button size="small" text @click="openRuleDialog(rule)">
                    <el-icon><icon-ep-edit /></el-icon>
                  </el-button>
                  <el-button size="small" text type="danger" @click="deleteRule(rule)">
                    <el-icon><icon-ep-delete /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="rule-detail">
                <span class="rule-energy">{{ getEnergyTypeLabel(rule.energy_type) }}</span>
                <span class="rule-separator">→</span>
                <span class="rule-condition">{{ getConditionLabel(rule.condition_type) }}</span>
                <span class="rule-separator">→</span>
                <span class="rule-threshold">{{ rule.threshold_value }}</span>
              </div>
            </div>

            <el-empty v-if="alarmRules.length === 0" description="暂无告警规则" :image-size="80" />
          </div>
        </div>
      </div>
    </div>

    <!-- Alarm Detail Dialog -->
    <el-dialog
      v-model="detailDialog.visible"
      title="告警详情"
      width="600px"
      :close-on-click-modal="false"
      class="alarm-detail-dialog"
    >
      <div v-if="detailDialog.data" class="detail-content">
        <div class="detail-header">
          <div class="detail-severity" :class="`severity-${getSeverity(detailDialog.data)}`">
            <el-icon><icon-ep-warning /></el-icon>
            <span>{{ getSeverityLabel(detailDialog.data) }}</span>
          </div>
          <el-tag :type="getStatusTag(detailDialog.data.status)" effect="plain">
            {{ getStatusLabel(detailDialog.data.status) }}
          </el-tag>
        </div>

        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">告警类型</span>
            <span class="detail-value">{{ getAlarmTypeLabel(detailDialog.data.alarm_type) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">能源类型</span>
            <span class="detail-value">{{ getEnergyTypeLabel(detailDialog.data.energy_type) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">设备名称</span>
            <span class="detail-value">{{ detailDialog.data.device_name || '--' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">设备位置</span>
            <span class="detail-value">{{ detailDialog.data.location || '--' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">告警时间</span>
            <span class="detail-value">{{ formatFullTime(detailDialog.data.alarm_time) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">告警数值</span>
            <span class="detail-value alarm-highlight">{{ formatAlarmValue(detailDialog.data) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">设定阈值</span>
            <span class="detail-value">{{ detailDialog.data.threshold_value || '--' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">规则名称</span>
            <span class="detail-value">{{ detailDialog.data.rule_name || '--' }}</span>
          </div>
        </div>

        <div v-if="detailDialog.data.description" class="detail-description">
          <span class="detail-label">告警描述</span>
          <p>{{ detailDialog.data.description }}</p>
        </div>

        <div v-if="detailDialog.data.status !== 'PENDING'" class="detail-handle">
          <span class="detail-label">处理信息</span>
          <div class="handle-info">
            <div class="handle-item">
              <span class="handle-label">处理人：</span>
              <span>{{ detailDialog.data.handler || '--' }}</span>
            </div>
            <div class="handle-item">
              <span class="handle-label">处理时间：</span>
              <span>{{ formatFullTime(detailDialog.data.handle_time) }}</span>
            </div>
            <div v-if="detailDialog.data.remark" class="handle-item full">
              <span class="handle-label">处理备注：</span>
              <p>{{ detailDialog.data.remark }}</p>
            </div>
          </div>
        </div>
      </div>

      <template #footer v-if="detailDialog.data?.status === 'PENDING'">
        <el-button @click="detailDialog.visible = false">关闭</el-button>
        <el-button type="primary" @click="openHandleDialog(detailDialog.data)">处理告警</el-button>
      </template>
    </el-dialog>

    <!-- Handle Alarm Dialog -->
    <el-dialog
      v-model="handleDialog.visible"
      title="处理告警"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="handleDialog.form" label-width="80px">
        <el-form-item label="处理状态">
          <el-radio-group v-model="handleDialog.form.status">
            <el-radio value="PROCESSED">已处理</el-radio>
            <el-radio value="IGNORED">已忽略</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="处理备注">
          <el-input
            v-model="handleDialog.form.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入处理说明或备注信息..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitHandle" :loading="handleDialog.loading">
          确认处理
        </el-button>
      </template>
    </el-dialog>

    <!-- Rule Form Dialog -->
    <el-dialog
      v-model="ruleDialog.visible"
      :title="ruleDialog.isEdit ? '编辑告警规则' : '新增告警规则'"
      width="550px"
      :close-on-click-modal="false"
    >
      <el-form :model="ruleDialog.form" :rules="ruleDialog.rules" ref="ruleFormRef" label-width="100px">
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="ruleDialog.form.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="能源类型" prop="energy_type">
          <el-select v-model="ruleDialog.form.energy_type" placeholder="请选择能源类型" style="width: 100%">
            <el-option label="电" value="ELECTRICITY" />
            <el-option label="水" value="WATER" />
            <el-option label="气" value="GAS" />
          </el-select>
        </el-form-item>
        <el-form-item label="条件类型" prop="condition_type">
          <el-select v-model="ruleDialog.form.condition_type" placeholder="请选择条件类型" style="width: 100%">
            <el-option label="超限告警" value="THRESHOLD" />
            <el-option label="突变告警" value="SUDDEN_CHANGE" />
            <el-option label="离线告警" value="OFFLINE" />
          </el-select>
        </el-form-item>
        <el-form-item label="阈值设定" prop="threshold_value">
          <el-input-number
            v-model="ruleDialog.form.threshold_value"
            :min="0"
            :precision="2"
            :step="10"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="ruleDialog.form.is_active" />
          <span class="form-tip">启用后将自动检测并生成告警</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ruleDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitRule" :loading="ruleDialog.loading">
          {{ ruleDialog.isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getAlarms,
  getAlarm,
  handleAlarm,
  getAlarmRules,
  createAlarmRule,
  updateAlarmRule,
  deleteAlarmRule,
  getAlarmStatistics,
} from '@/api/alarm'

// Auto refresh timer
let refreshTimer = null

// Loading state
const loading = ref(false)
const emptyText = ref('暂无告警数据')

// Alarm list data
const alarms = ref([])

// Alarm rules data
const alarmRules = ref([])

// Statistics
const alarmStats = ref([
  {
    label: '待处理',
    value: 0,
    unit: '条',
    change: null,
    color: '#ef4444',
    icon: 'icon-ep-warning',
    pulse: true,
  },
  {
    label: '已处理',
    value: 0,
    unit: '条',
    change: null,
    color: '#22c55e',
    icon: 'icon-ep-circle-check',
    pulse: false,
  },
  {
    label: '已忽略',
    value: 0,
    unit: '条',
    change: null,
    color: '#94a3b8',
    icon: 'icon-ep-remove',
    pulse: false,
  },
  {
    label: '今日告警',
    value: 0,
    unit: '条',
    change: null,
    color: '#f97316',
    icon: 'icon-ep-bell',
    pulse: true,
  },
])

// Filters
const filters = reactive({
  status: '',
  type: '',
  energyType: '',
  dateRange: null,
  search: '',
})

// Pagination
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// Detail dialog
const detailDialog = reactive({
  visible: false,
  data: null,
})

// Handle dialog
const handleDialog = reactive({
  visible: false,
  loading: false,
  form: {
    status: 'PROCESSED',
    remark: '',
  },
})

// Rule dialog
const ruleDialog = reactive({
  visible: false,
  loading: false,
  isEdit: false,
  form: {
    name: '',
    energy_type: '',
    condition_type: 'THRESHOLD',
    threshold_value: 100,
    is_active: true,
  },
  rules: {
    name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
    energy_type: [{ required: true, message: '请选择能源类型', trigger: 'change' }],
    condition_type: [{ required: true, message: '请选择条件类型', trigger: 'change' }],
    threshold_value: [{ required: true, message: '请输入阈值', trigger: 'blur' }],
  },
})

const ruleFormRef = ref(null)

// Computed
const hasPendingAlarms = computed(() => {
  return alarms.value.some(a => a.status === 'PENDING')
})

const filteredAlarms = computed(() => {
  let result = [...alarms.value]

  // Apply filters
  if (filters.status) {
    result = result.filter(a => a.status === filters.status)
  }
  if (filters.type) {
    result = result.filter(a => a.alarm_type === filters.type)
  }
  if (filters.energyType) {
    result = result.filter(a => a.energy_type === filters.energyType)
  }
  if (filters.search) {
    const search = filters.search.toLowerCase()
    result = result.filter(a =>
      (a.device_name && a.device_name.toLowerCase().includes(search)) ||
      (a.location && a.location.toLowerCase().includes(search))
    )
  }
  if (filters.dateRange && filters.dateRange.length === 2) {
    const [start, end] = filters.dateRange
    result = result.filter(a => {
      const time = new Date(a.alarm_time).getTime()
      return time >= new Date(start).getTime() && time <= new Date(end).getTime()
    })
  }

  // Update pagination total
  pagination.total = result.length

  // Apply pagination
  const start = (pagination.page - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return result.slice(start, end)
})

// Helper functions
function getAlarmTypeLabel(type) {
  const labels = {
    THRESHOLD: '超限',
    SUDDEN_CHANGE: '突变',
    OFFLINE: '离线',
  }
  return labels[type] || type
}

function getAlarmTypeTag(type) {
  const tags = {
    THRESHOLD: 'danger',
    SUDDEN_CHANGE: 'warning',
    OFFLINE: 'info',
  }
  return tags[type] || ''
}

function getSeverity(alarm) {
  if (alarm.alarm_type === 'OFFLINE') return 'high'
  if (alarm.alarm_value && alarm.threshold_value) {
    const ratio = alarm.alarm_value / alarm.threshold_value
    if (ratio > 1.5) return 'high'
    if (ratio > 1.2) return 'medium'
  }
  return 'low'
}

function getSeverityLabel(alarm) {
  const severity = getSeverity(alarm)
  return { high: '紧急', medium: '重要', low: '一般' }[severity]
}

function getSeverityClass(severity) {
  return `severity-${severity}`
}

function getStatusLabel(status) {
  return { PENDING: '待处理', PROCESSED: '已处理', IGNORED: '已忽略' }[status] || status
}

function getStatusTag(status) {
  return { PENDING: 'danger', PROCESSED: 'success', IGNORED: 'info' }[status] || ''
}

function getEnergyTypeLabel(type) {
  return { ELECTRICITY: '电', WATER: '水', GAS: '气' }[type] || type
}

function getConditionLabel(type) {
  return { THRESHOLD: '超限', SUDDEN_CHANGE: '突变', OFFLINE: '离线' }[type] || type
}

function formatAlarmValue(alarm) {
  if (!alarm.alarm_value && alarm.alarm_value !== 0) return '--'
  const numValue = Number(alarm.alarm_value)
  if (isNaN(numValue)) return alarm.alarm_value
  const value = numValue.toFixed(2)
  const units = { ELECTRICITY: 'kWh', WATER: 'm³', GAS: 'm³' }
  return `${value} ${units[alarm.energy_type] || ''}`
}

function formatTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)

  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  return date.toLocaleDateString('zh-CN')
}

function formatFullTime(timeStr) {
  if (!timeStr) return '--'
  return new Date(timeStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// Data loading
async function loadAlarms() {
  loading.value = true
  try {
    const response = await getAlarms()
    if (response.code === 0) {
      alarms.value = response.data || []
      pagination.total = alarms.value.length
    }
  } catch (error) {
    console.error('Failed to load alarms:', error)
    ElMessage.error('加载告警数据失败，请稍后重试')
    alarms.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

async function loadAlarmRules() {
  try {
    const response = await getAlarmRules()
    if (response.code === 0) {
      alarmRules.value = response.data || []
    }
  } catch (error) {
    console.error('Failed to load alarm rules:', error)
    alarmRules.value = []
  }
}

async function loadStatistics() {
  try {
    const response = await getAlarmStatistics()
    if (response.code === 0 && response.data) {
      alarmStats.value[0].value = response.data.pending || 0
      alarmStats.value[1].value = response.data.processed || 0
      alarmStats.value[2].value = response.data.ignored || 0
      alarmStats.value[3].value = response.data.today || 0
    }
  } catch (error) {
    console.error('Failed to load statistics:', error)
  }

  // Calculate from current data
  alarmStats.value[0].value = alarms.value.filter(a => a.status === 'PENDING').length
  alarmStats.value[1].value = alarms.value.filter(a => a.status === 'PROCESSED').length
  alarmStats.value[2].value = alarms.value.filter(a => a.status === 'IGNORED').length

  const today = new Date()
  today.setHours(0, 0, 0, 0)
  alarmStats.value[3].value = alarms.value.filter(a => new Date(a.alarm_time) >= today).length
}

// Mock function removed - using real API

// Actions
function refreshAlarms() {
  loadAlarms()
  loadStatistics()
}

function applyFilters() {
  pagination.page = 1
}

let searchTimeout = null
function debounceSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 300)
}

function handleSizeChange() {
  pagination.page = 1
}

function handlePageChange() {
  // Page change is handled by computed property
}

function viewDetail(alarm) {
  detailDialog.data = alarm
  detailDialog.visible = true
}

function openHandleDialog(alarm) {
  handleDialog.form = {
    status: 'PROCESSED',
    remark: '',
  }
  handleDialog.alarm = alarm
  handleDialog.visible = true
  // Close detail dialog if open
  if (detailDialog.visible) {
    detailDialog.visible = false
  }
}

async function submitHandle() {
  if (!handleDialog.form.remark) {
    ElMessage.warning('请填写处理备注')
    return
  }

  handleDialog.loading = true
  try {
    const response = await handleAlarm(handleDialog.alarm.id, handleDialog.form)
    if (response.code === 0) {
      ElMessage.success('告警处理成功')
      handleDialog.visible = false

      // Update local data
      const index = alarms.value.findIndex(a => a.id === handleDialog.alarm.id)
      if (index !== -1) {
        alarms.value[index] = {
          ...alarms.value[index],
          status: handleDialog.form.status,
          remark: handleDialog.form.remark,
          handler: '当前用户',
          handle_time: new Date().toISOString(),
        }
      }

      loadStatistics()
    } else {
      ElMessage.error(response.message || '处理失败')
    }
  } catch (error) {
    console.error('Failed to handle alarm:', error)
    ElMessage.error('告警处理失败，请稍后重试')
  } finally {
    handleDialog.loading = false
  }
}

function openRuleDialog(rule = null) {
  if (rule) {
    ruleDialog.isEdit = true
    ruleDialog.form = { ...rule }
  } else {
    ruleDialog.isEdit = false
    ruleDialog.form = {
      name: '',
      energy_type: '',
      condition_type: 'THRESHOLD',
      threshold_value: 100,
      is_active: true,
    }
  }
  ruleDialog.visible = true
}

async function submitRule() {
  await ruleFormRef.value.validate()

  ruleDialog.loading = true
  try {
    let response
    if (ruleDialog.isEdit) {
      response = await updateAlarmRule(ruleDialog.form.id, ruleDialog.form)
    } else {
      response = await createAlarmRule(ruleDialog.form)
    }

    if (response.code === 0) {
      ElMessage.success(ruleDialog.isEdit ? '规则更新成功' : '规则创建成功')
      ruleDialog.visible = false
      loadAlarmRules()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('Failed to save rule:', error)
    ElMessage.error('规则保存失败，请稍后重试')
  } finally {
    ruleDialog.loading = false
  }
}

async function deleteRule(rule) {
  try {
    await ElMessageBox.confirm('确定要删除这条告警规则吗？', '确认删除', {
      type: 'warning',
    })

    const response = await deleteAlarmRule(rule.id)
    if (response.code === 0) {
      ElMessage.success('规则删除成功')
      loadAlarmRules()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete rule:', error)
      ElMessage.error('规则删除失败，请稍后重试')
    }
  }
}

// Auto refresh
function setupAutoRefresh() {
  refreshTimer = setInterval(() => {
    loadAlarms()
    loadStatistics()
  }, 30000) // 30 seconds
}

// Lifecycle
onMounted(() => {
  loadAlarms()
  loadAlarmRules()
  loadStatistics()
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.alarms-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   STATS ROW
   ======================================== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  position: relative;
  height: 110px;
  background: linear-gradient(135deg, #fff 0%, #f8fafc 100%);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e5e7eb;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(249, 115, 22, 0.15);
  border-color: #f97316;
}

.stat-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
}

.glow-effect {
  position: absolute;
  top: -50%;
  right: -30%;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.4;
}

.stat-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 14px;
  height: 100%;
  padding: 18px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  font-size: 22px;
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 4px;
}

.value-number {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

.stat-unit {
  font-size: 12px;
  color: #94a3b8;
}

.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 500;
}

.stat-pulse {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse-ring 2s ease-out infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

/* ========================================
   MAIN CONTENT
   ======================================== */
.main-content {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 16px;
}

.section-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.title-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 18px;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 3px 8px;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-radius: 10px;
  font-weight: 500;
  margin-left: 8px;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ef4444;
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* ========================================
   ALARMS SECTION
   ======================================== */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 16px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.filter-group {
  display: flex;
  align-items: center;
}

.filter-group :deep(.el-select),
.filter-group :deep(.el-input),
.filter-group :deep(.el-date-editor) {
  width: 160px;
}

.filter-group :deep(.el-input__wrapper) {
  border-radius: 8px;
}

.table-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.alarms-table {
  flex: 1;
}

.alarms-table :deep(.el-table__row) {
  cursor: pointer;
}

.alarms-table :deep(.el-table__row:hover) {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.03) 0%, #f8fafc 100%);
}

.device-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.device-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.device-location {
  font-size: 11px;
  color: #94a3b8;
}

.alarm-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #ef4444;
}

.threshold-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
}

.alarm-time {
  font-size: 12px;
  color: #64748b;
}

.severity-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 500;
}

.severity-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.severity-high {
  color: #ef4444;
}

.severity-high .severity-dot {
  background: #ef4444;
  box-shadow: 0 0 6px rgba(239, 68, 68, 0.5);
}

.severity-medium {
  color: #eab308;
}

.severity-medium .severity-dot {
  background: #eab308;
}

.severity-low {
  color: #64748b;
}

.severity-low .severity-dot {
  background: #64748b;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   RULES SECTION
   ======================================== */
.rules-card {
  max-height: calc(100vh - 200px);
}

.rules-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: calc(100vh - 300px);
}

.rule-item {
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
  padding: 12px;
  transition: all 0.2s ease;
}

.rule-item:hover {
  background: #fff;
  border-color: #f97316;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

.rule-item.rule-inactive {
  opacity: 0.6;
}

.rule-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.rule-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rule-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.rule-actions {
  display: flex;
  gap: 4px;
}

.rule-detail {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
}

.rule-separator {
  color: #cbd5e1;
}

.rule-energy {
  padding: 2px 6px;
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
  border-radius: 4px;
  font-weight: 500;
}

.rule-condition {
  font-weight: 500;
}

.rule-threshold {
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  color: #1f2937;
}

/* ========================================
   DIALOG STYLES
   ======================================== */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.detail-severity {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 500;
}

.detail-severity.severity-high {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.detail-severity.severity-medium {
  background: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.detail-severity.severity-low {
  background: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  color: #64748b;
}

.detail-value {
  font-size: 14px;
  color: #1f2937;
  font-weight: 500;
}

.alarm-highlight {
  font-family: 'Orbitron', sans-serif;
  color: #ef4444;
  font-size: 16px;
}

.detail-description,
.detail-handle {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
}

.detail-description p {
  font-size: 13px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.handle-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.handle-item {
  display: flex;
  font-size: 13px;
}

.handle-item.full {
  flex-direction: column;
  gap: 4px;
}

.handle-label {
  color: #64748b;
  min-width: 80px;
}

.handle-item.full p {
  margin: 0;
  padding: 8px 12px;
  background: #fff;
  border-radius: 6px;
  font-size: 12px;
  color: #475569;
}

.form-tip {
  margin-left: 12px;
  font-size: 12px;
  color: #94a3b8;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1400px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .rules-card {
    max-height: none;
  }

  .rules-list {
    max-height: 300px;
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-group :deep(.el-select),
  .filter-group :deep(.el-input),
  .filter-group :deep(.el-date-editor) {
    width: 100%;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
