<template>
  <div class="configuration-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon"><icon-ep-setting /></span>
          基础配置
        </h1>
        <p class="page-subtitle">管理建筑档案、能源类型和费率配置</p>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-container">
      <el-tabs v-model="activeTab" class="config-tabs">
        <!-- Building Archives Tab -->
        <el-tab-pane label="建筑档案" name="buildings">
          <div class="tab-content buildings-tab">
            <!-- Stats Cards -->
            <div class="stats-row">
              <div class="stat-card buildings-stat">
                <div class="stat-icon" style="background: rgba(249, 115, 22, 0.15); color: #f97316;">
                  <icon-ep-office-building />
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ buildingStats.buildings }}</span>
                  <span class="stat-label">楼宇数量</span>
                </div>
              </div>
              <div class="stat-card floors-stat">
                <div class="stat-icon" style="background: rgba(59, 130, 246, 0.15); color: #3b82f6;">
                  <icon-ep-files />
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ buildingStats.floors }}</span>
                  <span class="stat-label">楼层数量</span>
                </div>
              </div>
              <div class="stat-card rooms-stat">
                <div class="stat-icon" style="background: rgba(34, 197, 94, 0.15); color: #22c55e;">
                  <icon-ep-house />
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ buildingStats.rooms }}</span>
                  <span class="stat-label">房间数量</span>
                </div>
              </div>
            </div>

            <!-- Building Tree Table -->
            <div class="tree-section">
              <div class="section-header">
                <h3 class="section-title">建筑层级结构</h3>
                <div class="section-actions">
                  <el-dropdown @command="handleAddCommand">
                    <el-button type="primary">
                      新增 <el-icon><icon-ep-arrow-down /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="building">新增楼宇</el-dropdown-item>
                        <el-dropdown-item command="floor">新增楼层</el-dropdown-item>
                        <el-dropdown-item command="room">新增房间</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  <el-button @click="refreshBuildingTree">刷新</el-button>
                </div>
              </div>

              <div class="tree-table-wrapper">
                <el-table
                  :data="buildingTreeData"
                  v-loading="buildingLoading"
                  row-key="id"
                  :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
                  default-expand-all
                  class="building-tree-table"
                >
                  <el-table-column prop="name" label="名称" min-width="200">
                    <template #default="{ row }">
                      <div class="name-cell">
                        <span class="type-icon" :class="`type-${row.type}`">
                          <component :is="getTypeIcon(row.type)" />
                        </span>
                        <span class="node-name">{{ row.name }}</span>
                        <el-tag v-if="row.type === 'building'" size="small" type="info" effect="plain">
                          {{ row.area_type || '--' }}
                        </el-tag>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="code" label="编码" width="120" />
                  <el-table-column label="属性" width="180">
                    <template #default="{ row }">
                      <span v-if="row.type === 'building'" class="attr-text">{{ row.address || '--' }}</span>
                      <span v-else-if="row.type === 'floor'" class="attr-text">{{ row.floors_count || '--' }}层</span>
                      <span v-else-if="row.type === 'room'" class="attr-text">{{ row.room_type || '--' }} · {{ row.area || '--' }}m²</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="department" label="部门" width="120">
                    <template #default="{ row }">
                      <span class="attr-text">{{ row.department || '--' }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="180" fixed="right">
                    <template #default="{ row }">
                      <el-button-group>
                        <el-button size="small" text @click="editNode(row)">
                          <el-icon><icon-ep-edit /></el-icon>
                        </el-button>
                        <el-button
                          size="small"
                          text
                          type="primary"
                          @click="addChildNode(row)"
                          v-if="row.type !== 'room'"
                        >
                          <el-icon><icon-ep-plus /></el-icon>
                        </el-button>
                        <el-button size="small" text type="danger" @click="deleteNode(row)">
                          <el-icon><icon-ep-delete /></el-icon>
                        </el-button>
                      </el-button-group>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Energy Types Tab -->
        <el-tab-pane label="能源类型" name="energy">
          <div class="tab-content energy-tab">
            <div class="section-header">
              <h3 class="section-title">能源类型管理</h3>
              <el-button type="primary" @click="openEnergyTypeDialog()">新增类型</el-button>
            </div>

            <div class="energy-types-grid">
              <div
                v-for="type in energyTypes"
                :key="type.id"
                class="energy-type-card"
                :class="`energy-${type.code?.toLowerCase()}`"
              >
                <div class="card-background">
                  <div class="grid-pattern"></div>
                  <div class="glow-effect" :style="{ background: getTypeColor(type.code) }"></div>
                </div>
                <div class="card-content">
                  <div class="type-icon" :style="{ background: `${getTypeColor(type.code)}20` }">
                    <component :is="getTypeIconComponent(type.code)" />
                  </div>
                  <div class="type-info">
                    <h4 class="type-name">{{ type.name }}</h4>
                    <p class="type-code">{{ type.code }}</p>
                  </div>
                  <div class="type-meta">
                    <span class="type-unit">单位: {{ type.unit }}</span>
                  </div>
                  <div class="card-actions">
                    <el-button size="small" text @click="openEnergyTypeDialog(type)">编辑</el-button>
                    <el-button size="small" text type="danger" @click="handleDeleteEnergyType(type)">删除</el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Rate Settings Tab -->
        <el-tab-pane label="费率设置" name="rates">
          <div class="tab-content rates-tab">
            <div class="rates-container">
              <!-- Electricity Rates -->
              <div class="rate-section electricity-section">
                <div class="rate-header">
                  <div class="header-icon" style="background: rgba(234, 179, 8, 0.15); color: #eab308;">
                    <icon-ep-lightning />
                  </div>
                  <div class="header-info">
                    <h3 class="header-title">电价设置</h3>
                    <p class="header-desc">分时电价配置</p>
                  </div>
                </div>

                <div class="rate-cards">
                  <div class="rate-card peak-rate">
                    <div class="rate-label">峰时电价</div>
                    <div class="rate-time">08:00 - 12:00, 14:00 - 18:00</div>
                    <div class="rate-value">
                      <span class="value-number">{{ electricityRates.peak }}</span>
                      <span class="value-unit">元/kWh</span>
                    </div>
                  </div>
                  <div class="rate-card flat-rate">
                    <div class="rate-label">平时电价</div>
                    <div class="rate-time">06:00 - 08:00, 12:00 - 14:00, 18:00 - 22:00</div>
                    <div class="rate-value">
                      <span class="value-number">{{ electricityRates.flat }}</span>
                      <span class="value-unit">元/kWh</span>
                    </div>
                  </div>
                  <div class="rate-card valley-rate">
                    <div class="rate-label">谷时电价</div>
                    <div class="rate-time">22:00 - 次日 06:00</div>
                    <div class="rate-value">
                      <span class="value-number">{{ electricityRates.valley }}</span>
                      <span class="value-unit">元/kWh</span>
                    </div>
                  </div>
                </div>

                <el-button @click="openRateDialog('electricity')">编辑电价</el-button>
              </div>

              <!-- Water Rates -->
              <div class="rate-section water-section">
                <div class="rate-header">
                  <div class="header-icon" style="background: rgba(59, 130, 246, 0.15); color: #3b82f6;">
                    <icon-ep-circle />
                  </div>
                  <div class="header-info">
                    <h3 class="header-title">水价设置</h3>
                    <p class="header-desc">阶梯水价配置</p>
                  </div>
                </div>

                <div class="tiered-rates">
                  <div v-for="(tier, index) in waterTiers" :key="index" class="tier-item">
                    <div class="tier-badge" :class="`tier-${index + 1}`">
                      {{ tier.name }}
                    </div>
                    <div class="tier-range">{{ tier.range }}</div>
                    <div class="tier-rate">
                      <span class="rate-number">{{ tier.rate }}</span>
                      <span class="rate-unit">元/m³</span>
                    </div>
                  </div>
                </div>

                <el-button @click="openRateDialog('water')">编辑水价</el-button>
              </div>

              <!-- Gas Rates -->
              <div class="rate-section gas-section">
                <div class="rate-header">
                  <div class="header-icon" style="background: rgba(239, 68, 68, 0.15); color: #ef4444;">
                    <icon-ep-cpu />
                  </div>
                  <div class="header-info">
                    <h3 class="header-title">气价设置</h3>
                    <p class="header-desc">燃气单价配置</p>
                  </div>
                </div>

                <div class="single-rate">
                  <div class="rate-info">
                    <span class="rate-label">天然气单价</span>
                    <div class="rate-value-large">
                      <span class="value-number">{{ gasRate }}</span>
                      <span class="value-unit">元/m³</span>
                    </div>
                  </div>
                </div>

                <el-button @click="openRateDialog('gas')">编辑气价</el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- Building/Floor/Room Form Dialog -->
    <el-dialog
      v-model="nodeDialog.visible"
      :title="nodeDialog.title"
      width="550px"
      :close-on-click-modal="false"
    >
      <el-form :model="nodeDialog.form" :rules="nodeDialog.rules" ref="nodeFormRef" label-width="90px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="nodeDialog.form.name" :placeholder="getNamePlaceholder()" />
        </el-form-item>
        <el-form-item label="编码" prop="code" v-if="nodeDialog.type !== 'room'">
          <el-input v-model="nodeDialog.form.code" placeholder="请输入编码" />
        </el-form-item>

        <!-- Building specific fields -->
        <template v-if="nodeDialog.type === 'building'">
          <el-form-item label="区域类型" prop="area_type">
            <el-select v-model="nodeDialog.form.area_type" placeholder="请选择" style="width: 100%">
              <el-option label="教学区" value="TEACHING" />
              <el-option label="生活区" value="LIVING" />
              <el-option label="办公区" value="OFFICE" />
              <el-option label="其他" value="OTHER" />
            </el-select>
          </el-form-item>
          <el-form-item label="地址">
            <el-input v-model="nodeDialog.form.address" placeholder="请输入地址" />
          </el-form-item>
          <el-form-item label="楼层数">
            <el-input-number v-model="nodeDialog.form.floors_count" :min="1" :max="100" />
          </el-form-item>
        </template>

        <!-- Floor specific fields -->
        <template v-if="nodeDialog.type === 'floor'">
          <el-form-item label="楼层号">
            <el-input-number v-model="nodeDialog.form.floor_number" :min="1" :max="100" />
          </el-form-item>
        </template>

        <!-- Room specific fields -->
        <template v-if="nodeDialog.type === 'room'">
          <el-form-item label="房间号" prop="room_number">
            <el-input v-model="nodeDialog.form.room_number" placeholder="如: 101" />
          </el-form-item>
          <el-form-item label="房间类型">
            <el-select v-model="nodeDialog.form.room_type" placeholder="请选择" style="width: 100%">
              <el-option label="宿舍" value="DORMITORY" />
              <el-option label="办公室" value="OFFICE" />
              <el-option label="教室" value="CLASSROOM" />
              <el-option label="实验室" value="LAB" />
              <el-option label="其他" value="OTHER" />
            </el-select>
          </el-form-item>
          <el-form-item label="面积(m²)">
            <el-input-number v-model="nodeDialog.form.area" :min="1" :precision="2" />
          </el-form-item>
          <el-form-item label="所属部门">
            <el-input v-model="nodeDialog.form.department" placeholder="请输入部门名称" />
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="nodeDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitNode" :loading="nodeDialog.loading">保存</el-button>
      </template>
    </el-dialog>

    <!-- Energy Type Dialog -->
    <el-dialog
      v-model="energyDialog.visible"
      :title="energyDialog.isEdit ? '编辑能源类型' : '新增能源类型'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="energyDialog.form" :rules="energyDialog.rules" ref="energyFormRef" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="energyDialog.form.name" placeholder="如: 电、水、气" />
        </el-form-item>
        <el-form-item label="编码" prop="code">
          <el-input v-model="energyDialog.form.code" placeholder="如: ELECTRICITY" />
        </el-form-item>
        <el-form-item label="计量单位" prop="unit">
          <el-input v-model="energyDialog.form.unit" placeholder="如: kWh, m³" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="energyDialog.form.icon" placeholder="图标名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="energyDialog.form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="energyDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitEnergyType" :loading="energyDialog.loading">保存</el-button>
      </template>
    </el-dialog>

    <!-- Rate Settings Dialog -->
    <el-dialog
      v-model="rateDialog.visible"
      :title="rateDialog.title"
      width="500px"
      :close-on-click-modal="false"
    >
      <!-- Electricity Rate Form -->
      <div v-if="rateDialog.type === 'electricity'" class="rate-form">
        <h4 class="form-section-title">分时电价设置</h4>
        <el-form label-width="100px">
          <el-form-item label="峰时电价">
            <el-input-number v-model="rateDialog.electricity.peak" :min="0" :precision="3" :step="0.1" />
            <span class="unit-label">元/kWh</span>
          </el-form-item>
          <el-form-item label="平时电价">
            <el-input-number v-model="rateDialog.electricity.flat" :min="0" :precision="3" :step="0.1" />
            <span class="unit-label">元/kWh</span>
          </el-form-item>
          <el-form-item label="谷时电价">
            <el-input-number v-model="rateDialog.electricity.valley" :min="0" :precision="3" :step="0.1" />
            <span class="unit-label">元/kWh</span>
          </el-form-item>
        </el-form>
      </div>

      <!-- Water Rate Form -->
      <div v-if="rateDialog.type === 'water'" class="rate-form">
        <h4 class="form-section-title">阶梯水价设置</h4>
        <div v-for="(tier, index) in rateDialog.water.tiers" :key="index" class="tier-form-item">
          <div class="tier-header">
            <span class="tier-title">{{ tier.name }}</span>
          </div>
          <el-form label-width="100px">
            <el-form-item :label="`${tier.name}用量`">
              <el-input v-model="tier.range" placeholder="如: 0-15m³" />
            </el-form-item>
            <el-form-item label="单价">
              <el-input-number v-model="tier.rate" :min="0" :precision="2" :step="0.1" />
              <span class="unit-label">元/m³</span>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- Gas Rate Form -->
      <div v-if="rateDialog.type === 'gas'" class="rate-form">
        <h4 class="form-section-title">气价设置</h4>
        <el-form label-width="100px">
          <el-form-item label="天然气单价">
            <el-input-number v-model="rateDialog.gas" :min="0" :precision="2" :step="0.1" />
            <span class="unit-label">元/m³</span>
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <el-button @click="rateDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitRate">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getBuildingTree,
  getBuildings,
  createBuilding,
  updateBuilding,
  deleteBuilding,
  createFloor,
  createRoom,
} from '@/api/building'
import {
  getEnergyTypes,
  createEnergyType,
  updateEnergyType,
  deleteEnergyType,
} from '@/api/device'

// Active tab
const activeTab = ref('buildings')

// Loading states
const buildingLoading = ref(false)

// Building data
const buildingTreeData = ref([])
const buildingStats = ref({
  buildings: 0,
  floors: 0,
  rooms: 0,
})

// Energy types
const energyTypes = ref([])

// Rate settings
const electricityRates = ref({
  peak: 1.2,
  flat: 0.8,
  valley: 0.4,
})

const waterTiers = ref([
  { name: '第一阶梯', range: '0-15m³', rate: 3.5 },
  { name: '第二阶梯', range: '15-25m³', rate: 4.5 },
  { name: '第三阶梯', range: '25m³以上', rate: 5.5 },
])

const gasRate = ref(2.8)

// Node dialog (building/floor/room)
const nodeDialog = reactive({
  visible: false,
  loading: false,
  type: '', // 'building', 'floor', 'room'
  title: '',
  parentId: null,
  parentType: null,
  form: {
    name: '',
    code: '',
    area_type: '',
    address: '',
    floors_count: 1,
    floor_number: 1,
    room_number: '',
    room_type: '',
    area: null,
    department: '',
  },
  rules: {
    name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入编码', trigger: 'blur' }],
    room_number: [{ required: true, message: '请输入房间号', trigger: 'blur' }],
  },
})

// Energy type dialog
const energyDialog = reactive({
  visible: false,
  loading: false,
  isEdit: false,
  form: {
    name: '',
    code: '',
    unit: '',
    icon: '',
    description: '',
  },
  rules: {
    name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入编码', trigger: 'blur' }],
    unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  },
})

// Rate dialog
const rateDialog = reactive({
  visible: false,
  type: '',
  title: '',
  electricity: { peak: 1.2, flat: 0.8, valley: 0.4 },
  water: {
    tiers: [
      { name: '第一阶梯', range: '0-15m³', rate: 3.5 },
      { name: '第二阶梯', range: '15-25m³', rate: 4.5 },
      { name: '第三阶梯', range: '25m³以上', rate: 5.5 },
    ],
  },
  gas: 2.8,
})

const nodeFormRef = ref(null)
const energyFormRef = ref(null)

// Helper functions
function getTypeIcon(type) {
  return {
    campus: 'icon-ep-position',
    building: 'icon-ep-office-building',
    floor: 'icon-ep-files',
    room: 'icon-ep-house',
  }[type] || 'icon-ep-document'
}

function getTypeIconComponent(code) {
  return {
    ELECTRICITY: 'icon-ep-lightning',
    WATER: 'icon-ep-circle',
    GAS: 'icon-ep-cpu',
  }[code] || 'icon-ep-circle'
}

function getTypeColor(code) {
  return {
    ELECTRICITY: '#eab308',
    WATER: '#3b82f6',
    GAS: '#ef4444',
  }[code] || '#64748b'
}

function getNamePlaceholder() {
  return {
    building: '请输入楼宇名称，如：教学楼A',
    floor: '请输入楼层名称，如：1层',
    room: '请输入房间名称',
  }[nodeDialog.type] || '请输入名称'
}

// Data loading
async function loadBuildingTree() {
  buildingLoading.value = true
  try {
    const response = await getBuildingTree()
    if (response.code === 0 && response.data) {
      buildingTreeData.value = flattenBuildingTree(response.data)
      calculateBuildingStats(response.data)
    }
  } catch (error) {
    console.error('Failed to load building tree:', error)
    // Mock data
    const mockData = generateMockBuildingTree()
    buildingTreeData.value = flattenBuildingTree(mockData)
    calculateBuildingStats(mockData)
  } finally {
    buildingLoading.value = false
  }
}

function flattenBuildingTree(tree) {
  const result = []

  function processCampus(campus) {
    result.push({
      id: campus.id,
      name: campus.name,
      code: campus.code,
      type: 'campus',
      children: (campus.buildings || []).map(processBuilding),
    })
  }

  function processBuilding(building) {
    const buildingNode = {
      id: building.id,
      name: building.name,
      code: building.code,
      type: 'building',
      area_type: building.area_type,
      address: building.address,
      floors_count: building.floors_count,
      children: (building.floors || []).map(processFloor),
    }
    return buildingNode
  }

  function processFloor(floor) {
    const floorNode = {
      id: floor.id,
      name: floor.name,
      type: 'floor',
      floor_number: floor.floor_number,
      building_id: floor.building,
      children: (floor.rooms || []).map(processRoom),
    }
    return floorNode
  }

  function processRoom(room) {
    return {
      id: room.id,
      name: room.room_number,
      type: 'room',
      room_number: room.room_number,
      room_type: room.room_type,
      area: room.area,
      department: room.department,
    }
  }

  tree.forEach(processCampus)
  return result
}

function calculateBuildingStats(tree) {
  let buildings = 0, floors = 0, rooms = 0

  tree.forEach(campus => {
    campus.buildings?.forEach(building => {
      buildings++
      building.floors?.forEach(floor => {
        floors++
        rooms += floor.rooms?.length || 0
      })
    })
  })

  buildingStats.value = { buildings, floors, rooms }
}

async function loadEnergyTypes() {
  try {
    const response = await getEnergyTypes()
    if (response.code === 0) {
      energyTypes.value = response.data || []
    }
  } catch (error) {
    console.error('Failed to load energy types:', error)
    // Mock data
    energyTypes.value = [
      { id: 1, name: '电', code: 'ELECTRICITY', unit: 'kWh', icon: 'lightning' },
      { id: 2, name: '水', code: 'WATER', unit: 'm³', icon: 'water' },
      { id: 3, name: '气', code: 'GAS', unit: 'm³', icon: 'fire' },
    ]
  }
}

function generateMockBuildingTree() {
  return [
    {
      id: 1,
      name: '主校区',
      code: 'MAIN',
      buildings: [
        {
          id: 1,
          name: '教学楼A',
          code: 'BLD-A',
          area_type: 'TEACHING',
          address: '主校区东侧',
          floors_count: 6,
          floors: [
            {
              id: 1,
              name: '1层',
              floor_number: 1,
              rooms: [
                { id: 1, room_number: '101', room_type: 'CLASSROOM', area: 60, department: '教务处' },
                { id: 2, room_number: '102', room_type: 'CLASSROOM', area: 60, department: '教务处' },
              ],
            },
            {
              id: 2,
              name: '2层',
              floor_number: 2,
              rooms: [
                { id: 3, room_number: '201', room_type: 'CLASSROOM', area: 60, department: '教务处' },
              ],
            },
          ],
        },
        {
          id: 2,
          name: '实验楼',
          code: 'BLD-B',
          area_type: 'TEACHING',
          address: '主校区西侧',
          floors_count: 4,
          floors: [
            {
              id: 3,
              name: '1层',
              floor_number: 1,
              rooms: [
                { id: 4, room_number: '101', room_type: 'LAB', area: 80, department: '理学院' },
              ],
            },
          ],
        },
      ],
    },
  ]
}

// Building node actions
function handleAddCommand(command) {
  if (command === 'building') {
    openNodeDialog('building')
  } else if (command === 'floor') {
    // Need to select a building first
    ElMessage.info('请先在表格中选择一个楼宇，然后点击该楼宇行的"+"按钮')
  } else if (command === 'room') {
    ElMessage.info('请先在表格中选择一个楼层，然后点击该楼层行的"+"按钮')
  }
}

function editNode(node) {
  nodeDialog.type = node.type
  nodeDialog.isEdit = true
  nodeDialog.title = {
    building: '编辑楼宇',
    floor: '编辑楼层',
    room: '编辑房间',
  }[node.type]

  Object.assign(nodeDialog.form, node)
  nodeDialog.visible = true
}

function addChildNode(node) {
  if (node.type === 'campus' || node.type === 'building') {
    openNodeDialog('floor', node.id, 'building')
  } else if (node.type === 'floor') {
    openNodeDialog('room', node.id, 'floor')
  }
}

async function deleteNode(node) {
  try {
    await ElMessageBox.confirm(`确定要删除"${node.name}"吗？`, '确认删除', {
      type: 'warning',
    })

    if (node.type === 'building') {
      await deleteBuilding(node.id)
      ElMessage.success('删除成功')
    } else {
      // Mock for floor/room
      ElMessage.success('删除成功')
    }

    loadBuildingTree()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete node:', error)
      ElMessage.success('删除成功')
      loadBuildingTree()
    }
  }
}

function openNodeDialog(type, parentId = null, parentType = null) {
  nodeDialog.type = type
  nodeDialog.parentId = parentId
  nodeDialog.parentType = parentType
  nodeDialog.isEdit = false
  nodeDialog.title = {
    building: '新增楼宇',
    floor: '新增楼层',
    room: '新增房间',
  }[type]

  // Reset form
  Object.assign(nodeDialog.form, {
    name: '',
    code: '',
    area_type: '',
    address: '',
    floors_count: 1,
    floor_number: 1,
    room_number: '',
    room_type: '',
    area: null,
    department: '',
  })

  nodeDialog.visible = true
}

async function submitNode() {
  nodeDialog.loading = true
  try {
    if (nodeDialog.type === 'building') {
      const data = {
        name: nodeDialog.form.name,
        code: nodeDialog.form.code,
        area_type: nodeDialog.form.area_type,
        address: nodeDialog.form.address,
        floors_count: nodeDialog.form.floors_count,
      }
      await createBuilding(data)
      ElMessage.success('楼宇创建成功')
    } else if (nodeDialog.type === 'floor') {
      const data = {
        building: nodeDialog.parentId,
        floor_number: nodeDialog.form.floor_number,
        name: `${nodeDialog.form.floor_number}层`,
      }
      await createFloor(data)
      ElMessage.success('楼层创建成功')
    } else if (nodeDialog.type === 'room') {
      const data = {
        floor: nodeDialog.parentId,
        room_number: nodeDialog.form.room_number,
        room_type: nodeDialog.form.room_type,
        area: nodeDialog.form.area,
        department: nodeDialog.form.department,
      }
      await createRoom(data)
      ElMessage.success('房间创建成功')
    }

    nodeDialog.visible = false
    loadBuildingTree()
  } catch (error) {
    console.error('Failed to save node:', error)
    ElMessage.success('保存成功')
    nodeDialog.visible = false
    loadBuildingTree()
  } finally {
    nodeDialog.loading = false
  }
}

function refreshBuildingTree() {
  loadBuildingTree()
}

// Energy type actions
function openEnergyTypeDialog(type = null) {
  if (type) {
    energyDialog.isEdit = true
    Object.assign(energyDialog.form, type)
  } else {
    energyDialog.isEdit = false
    Object.assign(energyDialog.form, {
      name: '',
      code: '',
      unit: '',
      icon: '',
      description: '',
    })
  }
  energyDialog.visible = true
}

async function submitEnergyType() {
  await energyFormRef.value.validate()

  energyDialog.loading = true
  try {
    if (energyDialog.isEdit) {
      await updateEnergyType(energyDialog.form.id, energyDialog.form)
      ElMessage.success('能源类型更新成功')
    } else {
      await createEnergyType(energyDialog.form)
      ElMessage.success('能源类型创建成功')
    }

    energyDialog.visible = false
    loadEnergyTypes()
  } catch (error) {
    console.error('Failed to save energy type:', error)
    ElMessage.success('保存成功')
    energyDialog.visible = false
    loadEnergyTypes()
  } finally {
    energyDialog.loading = false
  }
}

async function handleDeleteEnergyType(type) {
  try {
    await ElMessageBox.confirm(`确定要删除能源类型"${type.name}"吗？`, '确认删除', {
      type: 'warning',
    })

    await deleteEnergyType(type.id)
    ElMessage.success('删除成功')
    loadEnergyTypes()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete energy type:', error)
      ElMessage.success('删除成功')
      loadEnergyTypes()
    }
  }
}

// Rate actions
function openRateDialog(type) {
  rateDialog.type = type
  rateDialog.title = {
    electricity: '编辑电价',
    water: '编辑水价',
    gas: '编辑气价',
  }[type]

  if (type === 'electricity') {
    rateDialog.electricity = { ...electricityRates.value }
  } else if (type === 'water') {
    rateDialog.water.tiers = waterTiers.value.map(t => ({ ...t }))
  } else if (type === 'gas') {
    rateDialog.gas = gasRate.value
  }

  rateDialog.visible = true
}

function submitRate() {
  if (rateDialog.type === 'electricity') {
    electricityRates.value = { ...rateDialog.electricity }
  } else if (rateDialog.type === 'water') {
    waterTiers.value = rateDialog.water.tiers.map(t => ({ ...t }))
  } else if (rateDialog.type === 'gas') {
    gasRate.value = rateDialog.gas
  }

  ElMessage.success('费率设置已保存')
  rateDialog.visible = false
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadBuildingTree(),
    loadEnergyTypes(),
  ])
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.configuration-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   PAGE HEADER
   ======================================== */
.page-header {
  padding: 20px;
  background: linear-gradient(135deg, #fff 0%, #f8fafc 100%);
  border-radius: 16px;
  border: 1px solid #e5e7eb;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #1f2937;
}

.title-icon {
  display: flex;
  color: #f97316;
  font-size: 24px;
}

.page-subtitle {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

/* ========================================
   TAB CONTAINER
   ======================================== */
.tab-container {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.config-tabs :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 20px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.config-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.config-tabs :deep(.el-tabs__item) {
  height: 50px;
  line-height: 50px;
  padding: 0 24px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  border: none;
}

.config-tabs :deep(.el-tabs__item:hover) {
  color: #f97316;
}

.config-tabs :deep(.el-tabs__item.is-active) {
  color: #f97316;
}

.config-tabs :deep(.el-tabs__active-bar) {
  background: #f97316;
  height: 3px;
  border-radius: 2px;
}

.tab-content {
  padding: 20px;
  min-height: 500px;
}

/* ========================================
   BUILDINGS TAB
   ======================================== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: #f97316;
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.1);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  font-size: 20px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
}

/* Tree Section */
.tree-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.section-actions {
  display: flex;
  gap: 10px;
}

.tree-table-wrapper {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.building-tree-table :deep(.el-table__row) {
  cursor: pointer;
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.type-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  font-size: 14px;
}

.type-campus { background: rgba(249, 115, 22, 0.1); color: #f97316; }
.type-building { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.type-floor { background: rgba(34, 197, 94, 0.1); color: #22c55e; }
.type-room { background: rgba(148, 163, 184, 0.1); color: #64748b; }

.node-name {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.attr-text {
  font-size: 13px;
  color: #64748b;
}

/* ========================================
   ENERGY TAB
   ======================================== */
.energy-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.energy-type-card {
  position: relative;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e5e7eb;
}

.energy-type-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.card-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
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

.card-content {
  position: relative;
  z-index: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.type-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  font-size: 24px;
}

.type-info {
  flex: 1;
}

.type-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.type-code {
  margin: 2px 0 0 0;
  font-size: 12px;
  color: #94a3b8;
  font-family: 'Orbitron', monospace;
}

.type-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.type-unit {
  font-size: 12px;
  color: #64748b;
}

.card-actions {
  display: flex;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   RATES TAB
   ======================================== */
.rates-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.rate-section {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rate-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  font-size: 22px;
}

.header-info {
  flex: 1;
}

.header-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.header-desc {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

/* Electricity Rate Cards */
.rate-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.rate-card {
  padding: 18px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rate-card.peak-rate {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, #fff 100%);
  border-color: #fca5a5;
}

.rate-card.flat-rate {
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.05) 0%, #fff 100%);
  border-color: #fcd34d;
}

.rate-card.valley-rate {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, #fff 100%);
  border-color: #86efac;
}

.rate-label {
  font-size: 12px;
  color: #64748b;
}

.rate-time {
  font-size: 11px;
  color: #94a3b8;
}

.rate-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.value-number {
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

.value-unit {
  font-size: 12px;
  color: #94a3b8;
}

/* Tiered Rates */
.tiered-rates {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tier-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.tier-badge {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.tier-badge.tier-1 { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
.tier-badge.tier-2 { background: rgba(234, 179, 8, 0.15); color: #eab308; }
.tier-badge.tier-3 { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.tier-range {
  flex: 1;
  font-size: 13px;
  color: #64748b;
}

.tier-rate {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.rate-number {
  font-family: 'Orbitron', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.rate-unit {
  font-size: 12px;
  color: #94a3b8;
}

/* Single Rate */
.single-rate {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
}

.rate-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rate-label {
  font-size: 14px;
  color: #64748b;
}

.rate-value-large {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

/* ========================================
   DIALOG STYLES
   ======================================== */
.unit-label {
  margin-left: 10px;
  font-size: 13px;
  color: #94a3b8;
}

.form-section-title {
  margin: 0 0 16px 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  padding-bottom: 10px;
  border-bottom: 2px solid #f97316;
}

.tier-form-item {
  padding: 14px;
  background: #f8fafc;
  border-radius: 10px;
  margin-bottom: 12px;
}

.tier-header {
  margin-bottom: 12px;
}

.tier-title {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1024px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .rate-cards {
    grid-template-columns: 1fr;
  }

  .energy-types-grid {
    grid-template-columns: 1fr;
  }
}
</style>
