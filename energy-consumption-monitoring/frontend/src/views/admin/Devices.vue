<template>
  <div class="devices-page">
    <!-- Top Stats Cards -->
    <div class="stats-row">
      <div v-for="(stat, index) in deviceStats" :key="index" class="stat-card" :class="`stat-${index}`">
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
            <div class="stat-percent" v-if="stat.percent !== undefined">
              <div class="percent-bar">
                <div class="percent-fill" :style="{ width: stat.percent + '%', background: stat.color }"></div>
              </div>
              <span class="percent-text">{{ stat.percent }}%</span>
            </div>
          </div>
        </div>
        <div class="stat-pulse" v-if="stat.pulse" :style="{ borderColor: stat.color }"></div>
      </div>
    </div>

    <!-- Main Content Card -->
    <div class="main-card">
      <div class="card-header">
        <h3 class="card-title">
          <span class="title-icon"><icon-ep-cpu /></span>
          设备管理
        </h3>
        <div class="header-actions">
          <el-button @click="refreshDevices" :loading="loading">刷新</el-button>
          <el-button type="primary" @click="openDeviceDialog()">新增设备</el-button>
        </div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <div class="filter-group">
          <el-select v-model="filters.building" placeholder="选择建筑" clearable @change="applyFilters">
            <el-option
              v-for="building in buildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
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
          <el-select v-model="filters.status" placeholder="设备状态" clearable @change="applyFilters">
            <el-option label="在线" value="ONLINE" />
            <el-option label="离线" value="OFFLINE" />
            <el-option label="故障" value="FAULT" />
          </el-select>
        </div>
        <div class="filter-group">
          <el-select v-model="filters.hasData" placeholder="数据状态" clearable @change="applyFilters">
            <el-option label="有数据" :value="true" />
            <el-option label="无数据" :value="false" />
          </el-select>
        </div>
        <div class="filter-group search-group">
          <el-input
            v-model="filters.search"
            placeholder="搜索设备名称或ID"
            prefix-icon="Search"
            clearable
            @input="debounceSearch"
          />
        </div>
      </div>

      <!-- Device Table -->
      <div class="table-wrapper">
        <el-table
          :data="filteredDevices"
          v-loading="loading"
          stripe
          class="devices-table"
          :empty-text="emptyText"
        >
          <el-table-column type="index" label="#" width="50" />
          <el-table-column label="状态" width="70">
            <template #default="{ row }">
              <div class="status-indicator" :class="`status-${row.status?.toLowerCase()}`">
                <span class="status-dot"></span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="能源类型" width="80">
            <template #default="{ row }">
              <el-tag :type="getEnergyTypeTag(row.energy_type)" size="small" effect="plain">
                {{ getEnergyTypeLabel(row.energy_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="设备名称" width="160">
            <template #default="{ row }">
              <div class="device-name-cell">
                <span class="device-name">{{ row.name }}</span>
                <span class="device-id">{{ row.device_id || '--' }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="model" label="型号" width="120">
            <template #default="{ row }">
              <span class="device-model">{{ row.model || '--' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="位置" width="200">
            <template #default="{ row }">
              <div class="location-cell">
                <span class="location-icon"><icon-ep-location /></span>
                <div class="location-info">
                  <span class="building-name">{{ row.building_name || '--' }}</span>
                  <span class="room-info">{{ row.floor_name || '' }} {{ row.room_name || '未绑定' }}</span>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="最新数据" width="140">
            <template #default="{ row }">
              <div class="data-cell">
                <span v-if="row.latest_data" class="data-value">
                  {{ formatDataValue(row.latest_data.value, row.energy_type) }}
                </span>
                <span v-else class="no-data">--</span>
                <span v-if="row.last_data_time" class="data-time">{{ formatRelativeTime(row.last_data_time) }}</span>
                <span v-else class="no-data-time">从未上报</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="添加时间" width="160">
            <template #default="{ row }">
              <span class="created-time">{{ formatTime(row.created_at) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button size="small" text @click="openDeviceDialog(row)">
                  <el-icon><icon-ep-edit /></el-icon>
                  编辑
                </el-button>
                <el-button size="small" text type="primary" @click="openBindDialog(row)">
                  <el-icon><icon-ep-link /></el-icon>
                  绑定
                </el-button>
                <el-button size="small" text type="danger" @click="handleDeleteDevice(row)">
                  <el-icon><icon-ep-delete /></el-icon>
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

    <!-- Device Form Dialog -->
    <el-dialog
      v-model="deviceDialog.visible"
      :title="deviceDialog.isEdit ? '编辑设备' : '新增设备'"
      width="600px"
      :close-on-click-modal="false"
      class="device-dialog"
    >
      <el-form :model="deviceDialog.form" :rules="deviceDialog.rules" ref="deviceFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="设备名称" prop="name">
              <el-input v-model="deviceDialog.form.name" placeholder="请输入设备名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备ID" prop="device_id">
              <el-input v-model="deviceDialog.form.device_id" placeholder="请输入设备ID" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="能源类型" prop="energy_type">
              <el-select v-model="deviceDialog.form.energy_type" placeholder="请选择" style="width: 100%">
                <el-option label="电" value="ELECTRICITY" />
                <el-option label="水" value="WATER" />
                <el-option label="气" value="GAS" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备型号" prop="model">
              <el-input v-model="deviceDialog.form.model" placeholder="请输入型号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属建筑" prop="building_id">
              <el-select v-model="deviceDialog.form.building_id" placeholder="请选择" style="width: 100%" @change="onBuildingChange">
                <el-option
                  v-for="building in buildings"
                  :key="building.id"
                  :label="building.name"
                  :value="building.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备状态" prop="status">
              <el-select v-model="deviceDialog.form.status" placeholder="请选择" style="width: 100%">
                <el-option label="在线" value="ONLINE" />
                <el-option label="离线" value="OFFLINE" />
                <el-option label="故障" value="FAULT" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="绑定房间" prop="room_id">
          <el-cascader
            v-model="deviceDialog.form.room_cascade"
            :options="roomTreeOptions"
            :props="{ value: 'id', label: 'name', children: 'children' }"
            placeholder="请选择楼层-房间"
            clearable
            style="width: 100%"
            @change="onRoomChange"
          />
          <span class="form-tip">留空则为室外设备</span>
        </el-form-item>
        <el-form-item label="备注说明">
          <el-input
            v-model="deviceDialog.form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入设备描述或备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="deviceDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitDevice" :loading="deviceDialog.loading">
          {{ deviceDialog.isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Bind Room Dialog -->
    <el-dialog
      v-model="bindDialog.visible"
      title="绑定房间"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="bind-content">
        <div class="current-device" v-if="bindDialog.device">
          <span class="device-label">当前设备：</span>
          <span class="device-name">{{ bindDialog.device.name }}</span>
          <el-tag :type="getEnergyTypeTag(bindDialog.device.energy_type)" size="small" effect="plain">
            {{ getEnergyTypeLabel(bindDialog.device.energy_type) }}
          </el-tag>
        </div>

        <div class="current-binding" v-if="bindDialog.device?.room_name">
          <span class="binding-label">当前绑定：</span>
          <span class="binding-value">{{ bindDialog.device.building_name }} - {{ bindDialog.device.floor_name }} - {{ bindDialog.device.room_name }}</span>
        </div>
        <div class="current-binding unbound" v-else>
          <span class="binding-label">当前绑定：</span>
          <span class="binding-value">未绑定</span>
        </div>

        <el-divider />

        <el-form label-width="80px">
          <el-form-item label="选择位置">
            <el-cascader
              v-model="bindDialog.room_cascade"
              :options="roomTreeOptions"
              :props="{ value: 'id', label: 'name', children: 'children' }"
              placeholder="请选择建筑-楼层-房间"
              clearable
              style="width: 100%"
            />
          </el-form-item>
        </el-form>

        <el-alert
          title="提示"
          type="info"
          :closable="false"
          show-icon
        >
          选择房间可绑定设备，清空选择可解除绑定。设备绑定后可按位置查询能耗数据。
        </el-alert>
      </div>
      <template #footer>
        <el-button @click="bindDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitBind" :loading="bindDialog.loading">
          确认绑定
        </el-button>
      </template>
    </el-dialog>

    <!-- Device Detail Drawer -->
    <el-drawer
      v-model="detailDrawer.visible"
      title="设备详情"
      direction="rtl"
      size="450px"
    >
      <div v-if="detailDrawer.data" class="detail-content">
        <div class="detail-header">
          <div class="detail-status" :class="`status-${detailDrawer.data.status?.toLowerCase()}`">
            <span class="status-dot"></span>
            <span>{{ getStatusLabel(detailDrawer.data.status) }}</span>
          </div>
          <el-tag :type="getEnergyTypeTag(detailDrawer.data.energy_type)" effect="plain">
            {{ getEnergyTypeLabel(detailDrawer.data.energy_type) }}
          </el-tag>
        </div>

        <div class="detail-section">
          <h4 class="section-title">基本信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label">设备名称</span>
              <span class="detail-value">{{ detailDrawer.data.name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">设备ID</span>
              <span class="detail-value mono">{{ detailDrawer.data.device_id || '--' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">设备型号</span>
              <span class="detail-value">{{ detailDrawer.data.model || '--' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">能源类型</span>
              <span class="detail-value">{{ getEnergyTypeLabel(detailDrawer.data.energy_type) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-title">位置信息</h4>
          <div class="detail-grid">
            <div class="detail-item full">
              <span class="detail-label">所属建筑</span>
              <span class="detail-value">{{ detailDrawer.data.building_name || '--' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">楼层</span>
              <span class="detail-value">{{ detailDrawer.data.floor_name || '--' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">房间</span>
              <span class="detail-value">{{ detailDrawer.data.room_name || '未绑定' }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-title">数据状态</h4>
          <div class="data-status-card">
            <div v-if="detailDrawer.data.latest_data" class="data-current">
              <span class="data-label">最新读数</span>
              <span class="data-value">{{ formatDataValue(detailDrawer.data.latest_data.value, detailDrawer.data.energy_type) }}</span>
            </div>
            <div v-else class="data-current empty">
              <span class="data-label">暂无数据</span>
            </div>
            <div class="data-meta">
              <div class="meta-item">
                <span class="meta-label">最后上报</span>
                <span class="meta-value">{{ formatRelativeTime(detailDrawer.data.last_data_time) }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">添加时间</span>
                <span class="meta-value">{{ formatTime(detailDrawer.data.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="detailDrawer.data.description" class="detail-section">
          <h4 class="section-title">备注说明</h4>
          <p class="description-text">{{ detailDrawer.data.description }}</p>
        </div>

        <div class="detail-actions">
          <el-button type="primary" @click="openDeviceDialog(detailDrawer.data)">
            <el-icon><icon-ep-edit /></el-icon>
            编辑设备
          </el-button>
          <el-button @click="openBindDialog(detailDrawer.data)">
            <el-icon><icon-ep-link /></el-icon>
            绑定房间
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getDevices,
  getDevice,
  createDevice,
  updateDevice,
  deleteDevice,
  bindDeviceRoom,
  getEnergyTypes,
  getDeviceDataStatus,
} from '@/api/device'
import { getBuildingTree, getBuildings } from '@/api/building'

// Loading state
const loading = ref(false)
const emptyText = ref('暂无设备数据')

// Data
const devices = ref([])
const buildings = ref([])
const roomTreeOptions = ref([])

// Statistics
const deviceStats = ref([
  { label: '设备总数', value: 0, unit: '台', color: '#f97316', icon: 'icon-ep-cpu', pulse: false },
  { label: '在线设备', value: 0, unit: '台', color: '#22c55e', icon: 'icon-ep-circle-check', pulse: true },
  { label: '离线设备', value: 0, unit: '台', color: '#94a3b8', icon: 'icon-ep-video-pause', pulse: false },
  { label: '故障设备', value: 0, unit: '台', color: '#ef4444', icon: 'icon-ep-warning', pulse: true },
])

// Filters
const filters = reactive({
  building: '',
  energyType: '',
  status: '',
  hasData: '',
  search: '',
})

// Pagination
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// Device dialog
const deviceDialog = reactive({
  visible: false,
  loading: false,
  isEdit: false,
  form: {
    name: '',
    device_id: '',
    energy_type: '',
    model: '',
    building_id: '',
    room_id: null,
    room_cascade: [],
    status: 'ONLINE',
    description: '',
  },
  rules: {
    name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
    device_id: [{ required: true, message: '请输入设备ID', trigger: 'blur' }],
    energy_type: [{ required: true, message: '请选择能源类型', trigger: 'change' }],
    building_id: [{ required: true, message: '请选择所属建筑', trigger: 'change' }],
  },
})

// Bind dialog
const bindDialog = reactive({
  visible: false,
  loading: false,
  device: null,
  room_cascade: [],
})

// Detail drawer
const detailDrawer = reactive({
  visible: false,
  data: null,
})

const deviceFormRef = ref(null)

// Computed
const filteredDevices = computed(() => {
  let result = [...devices.value]

  if (filters.building) {
    result = result.filter(d => d.building_id === filters.building)
  }
  if (filters.energyType) {
    result = result.filter(d => d.energy_type === filters.energyType)
  }
  if (filters.status) {
    result = result.filter(d => d.status === filters.status)
  }
  if (filters.hasData !== '') {
    if (filters.hasData) {
      result = result.filter(d => d.latest_data && d.latest_data.value !== undefined)
    } else {
      result = result.filter(d => !d.latest_data || d.latest_data.value === undefined)
    }
  }
  if (filters.search) {
    const search = filters.search.toLowerCase()
    result = result.filter(d =>
      (d.name && d.name.toLowerCase().includes(search)) ||
      (d.device_id && d.device_id.toLowerCase().includes(search))
    )
  }

  pagination.total = result.length

  const start = (pagination.page - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return result.slice(start, end)
})

// Helper functions
function getEnergyTypeLabel(type) {
  return { ELECTRICITY: '电', WATER: '水', GAS: '气' }[type] || type
}

function getEnergyTypeTag(type) {
  return { ELECTRICITY: 'warning', WATER: 'primary', GAS: 'danger' }[type] || 'info'
}

function getStatusLabel(status) {
  return { ONLINE: '在线', OFFLINE: '离线', FAULT: '故障' }[status] || status
}

function formatDataValue(value, energyType) {
  if (value === undefined || value === null) return '--'
  const units = { ELECTRICITY: 'kWh', WATER: 'm³', GAS: 'm³' }
  return `${Number(value).toFixed(2)} ${units[energyType] || ''}`
}

function formatTime(timeStr) {
  if (!timeStr) return '--'
  return new Date(timeStr).toLocaleDateString('zh-CN')
}

function formatRelativeTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)

  if (diff < 5) return '刚刚'
  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  if (diff < 43200) return `${Math.floor(diff / 1440)}天前`
  return date.toLocaleDateString('zh-CN')
}

// Data loading
async function loadDevices() {
  loading.value = true
  try {
    const response = await getDevices()
    if (response.code === 0) {
      devices.value = response.data || []
      pagination.total = devices.value.length
      updateStats()
    }
  } catch (error) {
    console.error('Failed to load devices:', error)
    ElMessage.error('加载设备数据失败，请稍后重试')
    devices.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

async function loadBuildings() {
  try {
    const response = await getBuildings()
    if (response.code === 0) {
      buildings.value = response.data || []
    }
  } catch (error) {
    console.error('Failed to load buildings:', error)
    // Mock buildings
    buildings.value = [
      { id: 1, name: '教学楼A' },
      { id: 2, name: '实验楼' },
      { id: 3, name: '图书馆' },
    ]
  }
}

async function loadBuildingTree() {
  try {
    const response = await getBuildingTree()
    if (response.code === 0 && response.data) {
      roomTreeOptions.value = buildRoomTree(response.data)
    }
  } catch (error) {
    console.error('Failed to load building tree:', error)
    // Mock tree
    roomTreeOptions.value = [
      {
        id: 1, name: '教学楼A', children: [
          { id: 1, name: '1层', children: [
            { id: 1, name: '101室' },
            { id: 2, name: '102室' },
          ]},
          { id: 2, name: '2层', children: [
            { id: 3, name: '201室' },
            { id: 4, name: '202室' },
          ]},
        ],
      },
    ]
  }
}

function buildRoomTree(tree) {
  if (!tree) return []
  return tree.map(building => ({
    id: building.id,
    name: building.name,
    children: (building.floors || []).map(floor => ({
      id: floor.id,
      name: `${floor.floor_number}层`,
      children: (floor.rooms || []).map(room => ({
        id: room.id,
        name: room.room_number,
      })),
    })),
  }))
}

function updateStats() {
  const total = devices.value.length
  const online = devices.value.filter(d => d.status === 'ONLINE').length
  const offline = devices.value.filter(d => d.status === 'OFFLINE').length
  const fault = devices.value.filter(d => d.status === 'FAULT').length

  deviceStats.value[0].value = total
  deviceStats.value[1].value = online
  deviceStats.value[1].percent = total > 0 ? Math.round((online / total) * 100) : 0
  deviceStats.value[2].value = offline
  deviceStats.value[2].percent = total > 0 ? Math.round((offline / total) * 100) : 0
  deviceStats.value[3].value = fault
  deviceStats.value[3].percent = total > 0 ? Math.round((fault / total) * 100) : 0
}

// Mock function removed - using real API

// Actions
function refreshDevices() {
  loadDevices()
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
  // Handled by computed
}

function openDeviceDialog(device = null) {
  if (device) {
    deviceDialog.isEdit = true
    deviceDialog.form = {
      ...device,
      room_cascade: device.room_id ? [device.building_id, device.floor_id, device.room_id] : [],
    }
  } else {
    deviceDialog.isEdit = false
    deviceDialog.form = {
      name: '',
      device_id: '',
      energy_type: '',
      model: '',
      building_id: '',
      room_id: null,
      room_cascade: [],
      status: 'ONLINE',
      description: '',
    }
  }
  deviceDialog.visible = true

  // Close drawer if open
  if (detailDrawer.visible) {
    detailDrawer.visible = false
  }
}

function onBuildingChange() {
  deviceDialog.form.room_cascade = []
  deviceDialog.form.room_id = null
}

function onRoomChange(value) {
  if (value && value.length === 3) {
    deviceDialog.form.room_id = value[2]
    deviceDialog.form.floor_id = value[1]
  } else {
    deviceDialog.form.room_id = null
    deviceDialog.form.floor_id = null
  }
}

async function submitDevice() {
  await deviceFormRef.value.validate()

  deviceDialog.loading = true
  try {
    const data = { ...deviceDialog.form }
    delete data.room_cascade

    let response
    if (deviceDialog.isEdit) {
      response = await updateDevice(data.id, data)
    } else {
      response = await createDevice(data)
    }

    if (response.code === 0) {
      ElMessage.success(deviceDialog.isEdit ? '设备更新成功' : '设备创建成功')
      deviceDialog.visible = false
      loadDevices()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('Failed to save device:', error)
    ElMessage.error('操作失败，请稍后重试')
  } finally {
    deviceDialog.loading = false
  }
}

async function handleDeleteDevice(device) {
  try {
    await ElMessageBox.confirm('确定要删除这个设备吗？此操作不可恢复。', '确认删除', {
      type: 'warning',
    })

    const response = await deleteDevice(device.id)
    if (response.code === 0) {
      ElMessage.success('设备删除成功')
      loadDevices()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete device:', error)
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}

function openBindDialog(device) {
  bindDialog.device = device
  bindDialog.room_cascade = device.room_id ? [device.building_id, device.floor_id, device.room_id] : []
  bindDialog.visible = false
  bindDialog.visible = true

  // Close drawer if open
  if (detailDrawer.visible) {
    detailDrawer.visible = false
  }
}

async function submitBind() {
  bindDialog.loading = true
  try {
    const data = { room_id: null }
    if (bindDialog.room_cascade && bindDialog.room_cascade.length === 3) {
      data.room_id = bindDialog.room_cascade[2]
    }

    const response = await bindDeviceRoom(bindDialog.device.id, data)
    if (response.code === 0) {
      ElMessage.success('绑定成功')
      bindDialog.visible = false
      loadDevices()
    } else {
      ElMessage.error(response.message || '绑定失败')
    }
  } catch (error) {
    console.error('Failed to bind room:', error)
    ElMessage.error('绑定失败，请稍后重试')
  } finally {
    bindDialog.loading = false
  }
}

function viewDetail(device) {
  detailDrawer.data = device
  detailDrawer.visible = true
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadDevices(),
    loadBuildings(),
    loadBuildingTree(),
  ])
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.devices-page {
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
  margin-bottom: 6px;
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

.stat-percent {
  display: flex;
  align-items: center;
  gap: 8px;
}

.percent-bar {
  flex: 1;
  height: 4px;
  background: #f1f5f9;
  border-radius: 2px;
  overflow: hidden;
}

.percent-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.6s ease;
}

.percent-text {
  font-size: 11px;
  font-weight: 500;
  color: #64748b;
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
   MAIN CARD
   ======================================== */
.main-card {
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

.header-actions {
  display: flex;
  gap: 10px;
}

/* ========================================
   FILTER BAR
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

.filter-group :deep(.el-select) {
  width: 140px;
}

.search-group :deep(.el-input) {
  width: 200px;
}

.filter-group :deep(.el-input__wrapper) {
  border-radius: 8px;
}

/* ========================================
   TABLE
   ======================================== */
.table-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 500px;
}

.devices-table {
  flex: 1;
}

.devices-table :deep(.el-table__row) {
  cursor: pointer;
}

.devices-table :deep(.el-table__row:hover) {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.03) 0%, #f8fafc 100%);
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-online .status-dot {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.status-offline .status-dot {
  background: #94a3b8;
}

.status-fault .status-dot {
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
  animation: fault-pulse 1.5s ease-in-out infinite;
}

@keyframes fault-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.device-name-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.device-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.device-id {
  font-size: 11px;
  color: #94a3b8;
  font-family: 'Orbitron', monospace;
}

.device-model {
  font-size: 12px;
  color: #64748b;
}

.location-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.location-icon {
  display: flex;
  color: #f97316;
  font-size: 14px;
}

.location-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.building-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.room-info {
  font-size: 11px;
  color: #94a3b8;
}

.data-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.data-value {
  font-family: 'Orbitron', monospace;
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.no-data {
  font-size: 13px;
  color: #cbd5e1;
}

.data-time {
  font-size: 11px;
  color: #22c55e;
}

.no-data-time {
  font-size: 11px;
  color: #cbd5e1;
}

.created-time {
  font-size: 12px;
  color: #64748b;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   DIALOG STYLES
   ======================================== */
.form-tip {
  margin-left: 12px;
  font-size: 12px;
  color: #94a3b8;
}

/* Bind Dialog */
.bind-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.current-device {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
}

.device-label {
  font-size: 12px;
  color: #64748b;
}

.current-binding {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.current-binding.unbound {
  color: #94a3b8;
}

.binding-label {
  color: #64748b;
}

.binding-value {
  color: #1f2937;
  font-weight: 500;
}

/* Detail Drawer */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.detail-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.detail-status.status-online {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.detail-status.status-offline {
  background: rgba(148, 163, 184, 0.1);
  color: #64748b;
}

.detail-status.status-fault {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  padding-bottom: 8px;
  border-bottom: 2px solid #f97316;
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

.detail-item.full {
  grid-column: 1 / -1;
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

.detail-value.mono {
  font-family: 'Orbitron', monospace;
  font-size: 13px;
}

/* Data Status Card */
.data-status-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.data-current {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.data-current.empty {
  justify-content: center;
}

.data-label {
  font-size: 12px;
  color: #64748b;
}

.data-value {
  font-family: 'Orbitron', monospace;
  font-size: 20px;
  font-weight: 700;
  color: #f97316;
}

.data-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.meta-label {
  color: #64748b;
}

.meta-value {
  color: #1f2937;
  font-weight: 500;
}

.description-text {
  margin: 0;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
  font-size: 13px;
  color: #475569;
  line-height: 1.6;
}

.detail-actions {
  display: flex;
  gap: 10px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.detail-actions .el-button {
  flex: 1;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-group :deep(.el-select),
  .search-group :deep(.el-input) {
    width: 100%;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
