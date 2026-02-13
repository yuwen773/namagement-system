<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  Edit,
  Delete,
  Refresh,
  Film,
  Phone,
  Check,
  Close,
  Filter,
  Location,
  Grid
} from '@element-plus/icons-vue'
import {
  getCinemas,
  createCinema,
  updateCinema,
  deleteCinema,
  getRegions,
  createRegion,
  updateRegion,
  deleteRegion
} from '@/api/cinema'

const loading = ref(false)
const tableLoading = ref(false)
const regionTreeLoading = ref(false)

const tableData = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  search: '',
  region: null
})

// 地域数据
const regionTreeData = ref([])
const flatRegionList = ref([])
const selectedRegionId = ref(null)
const selectedRegionNode = ref(null)
const regionTreeRef = ref(null)

// 地域面板展开状态
const regionPanelCollapsed = ref(false)

// ============================================
// 影院对话框
// ============================================
const dialogVisible = ref(false)
const dialogTitle = ref('新增影院')
const formLoading = ref(false)

const form = reactive({
  id: null,
  name: '',
  address: '',
  phone: '',
  region: null,
  region_name: '',
  parent_region_name: ''
})

const rules = {
  name: [{ required: true, message: '请输入影院名称', trigger: 'blur' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }],
  region: [{ required: true, message: '请选择所属地域', trigger: 'change' }]
}

const formRef = ref(null)

// ============================================
// 地域对话框
// ============================================
const regionDialogVisible = ref(false)
const regionDialogTitle = ref('')
const regionDialogMode = ref('add')

const regionForm = reactive({
  id: null,
  name: '',
  parent: null,
  code: ''
})

const regionRules = {
  name: [{ required: true, message: '请输入地域名称', trigger: 'blur' }]
}

const regionFormRef = ref(null)

// ============================================
// 地域树相关
// ============================================
const buildRegionTree = (regions) => {
  const regionMap = new Map()
  const roots = []

  regions.forEach(region => {
    regionMap.set(region.id, { ...region, children: [] })
  })

  regions.forEach(region => {
    const node = regionMap.get(region.id)
    if (region.parent) {
      const parent = regionMap.get(region.parent)
      if (parent) {
        parent.children.push(node)
      } else {
        roots.push(node)
      }
    } else {
      roots.push(node)
    }
  })

  const cleanEmptyChildren = (nodes) => {
    nodes.forEach(node => {
      if (node.children.length === 0) {
        delete node.children
      } else {
        cleanEmptyChildren(node.children)
      }
    })
  }
  cleanEmptyChildren(roots)

  return roots
}

const loadRegions = async () => {
  regionTreeLoading.value = true
  try {
    const res = await getRegions()
    flatRegionList.value = res.data || []
    regionTreeData.value = buildRegionTree(flatRegionList.value)
  } catch (error) {
    ElMessage.error('加载地域数据失败')
    console.error(error)
  } finally {
    regionTreeLoading.value = false
  }
}

const handleRegionNodeClick = (data) => {
  selectedRegionId.value = data.id
  selectedRegionNode.value = data
  queryParams.region = data.id
  queryParams.page = 1
  loadData()
}

const handleClearRegion = () => {
  selectedRegionId.value = null
  selectedRegionNode.value = null
  queryParams.region = null
  queryParams.page = 1
  if (regionTreeRef.value) {
    regionTreeRef.value.setCurrentKey(null)
  }
  loadData()
}

// ============================================
// 地域操作
// ============================================
const handleAddRootRegion = () => {
  regionDialogTitle.value = '新增根地域'
  regionDialogMode.value = 'add'
  resetRegionForm()
  regionDialogVisible.value = true
}

const handleAddChildRegion = (node) => {
  regionDialogTitle.value = `新增子地域 - ${node.name}`
  regionDialogMode.value = 'add-child'
  resetRegionForm()
  regionForm.parent = node.id
  regionDialogVisible.value = true
}

const handleEditRegion = (node) => {
  regionDialogTitle.value = '编辑地域'
  regionDialogMode.value = 'edit'
  Object.assign(regionForm, {
    id: node.id,
    name: node.name,
    parent: node.parent?.id || node.parent || null,
    code: node.code || ''
  })
  regionDialogVisible.value = true
}

const handleDeleteRegion = (node) => {
  const hasChildren = node.children && node.children.length > 0
  const message = hasChildren
    ? `该地域下有 ${node.children.length} 个子地域，确定要删除地域"${node.name}"吗？`
    : `确定要删除地域"${node.name}"吗？`

  ElMessageBox.confirm(message, '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteRegion(node.id)
      ElMessage.success({
        message: '删除成功',
        icon: Check
      })
      await loadRegions()
      if (selectedRegionId.value === node.id) {
        handleClearRegion()
      }
    } catch (error) {
      console.error('删除地域失败:', error)
    }
  }).catch(() => {})
}

const resetRegionForm = () => {
  regionForm.id = null
  regionForm.name = ''
  regionForm.parent = null
  regionForm.code = ''
  if (regionFormRef.value) {
    regionFormRef.value.clearValidate()
  }
}

const submitRegionForm = async () => {
  if (!regionFormRef.value) return

  try {
    await regionFormRef.value.validate()
    formLoading.value = true

    if (regionForm.id) {
      await updateRegion(regionForm.id, regionForm)
      ElMessage.success({
        message: '更新成功',
        icon: Check
      })
    } else {
      const data = {
        name: regionForm.name,
        code: regionForm.code
      }
      if (regionForm.parent) {
        data.parent = regionForm.parent
      }
      await createRegion(data)
      ElMessage.success({
        message: '创建成功',
        icon: Check
      })
    }

    regionDialogVisible.value = false
    await loadRegions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error({
        message: regionForm.id ? '更新失败' : '创建失败',
        icon: Close
      })
    }
  } finally {
    formLoading.value = false
  }
}

// ============================================
// 影院操作
// ============================================
const loadData = async () => {
  tableLoading.value = true
  try {
    const res = await getCinemas(queryParams, flatRegionList.value)
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
  dialogTitle.value = '新增影院'
  resetForm()
  if (selectedRegionId.value) {
    form.region = selectedRegionId.value
  }
  dialogVisible.value = true
}

const handleEdit = async (row) => {
  dialogTitle.value = '编辑影院'
  // region 可能是数字ID或对象，统一处理
  const regionId = typeof row.region === 'number' ? row.region : (row.region?.id || row.region)
  Object.assign(form, {
    id: row.id,
    name: row.name,
    address: row.address,
    phone: row.phone || '',
    region: regionId,
    region_name: row.region_name || '',
    parent_region_name: row.parent_region_name || ''
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除影院"${row.name}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(async () => {
    try {
      await deleteCinema(row.id)
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
  form.name = ''
  form.address = ''
  form.phone = ''
  form.region = null
  form.region_name = ''
  form.parent_region_name = ''
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
      await updateCinema(form.id, form)
      ElMessage.success({
        message: '更新成功',
        icon: Check
      })
    } else {
      await createCinema(form)
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

const handleCancelRegion = () => {
  regionDialogVisible.value = false
  resetRegionForm()
}

const getRegionPath = (region) => {
  if (!region) return '-'
  const path = []
  let current = region
  while (current) {
    path.unshift(current.name)
    current = flatRegionList.value.find(r => r.id === current.parent)
  }
  return path.join(' / ')
}

// 获取选中地域的显示名称
const selectedRegionName = computed(() => {
  if (!form.region) return ''
  const region = flatRegionList.value.find(r => r.id === form.region)
  if (region) {
    return getRegionPath(region)
  }
  return ''
})

const getCinemaColor = (index) => {
  const colors = [
    'from-emerald-500 to-teal-500',
    'from-teal-500 to-cyan-500',
    'from-green-500 to-emerald-500',
    'from-cyan-500 to-blue-500',
    'from-lime-500 to-green-500'
  ]
  return colors[index % colors.length]
}

onMounted(() => {
  loadRegions()
  loadData()
})
</script>

<template>
  <div class="min-h-screen relative overflow-hidden cinemas-page">
    <!-- 动画背景 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <div class="relative z-10 p-6 lg:p-8 flex gap-6">
      <!-- 左侧：地域面板 -->
      <div
        class="region-sidebar transition-all duration-300"
        :class="regionPanelCollapsed ? 'w-0 opacity-0 overflow-hidden' : 'w-72 opacity-100'"
      >
        <div class="glass-card rounded-2xl border border-white/10 h-full flex flex-col animate-slide-up">
          <!-- 地域面板头部 -->
          <div class="p-5 border-b border-white/10">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
                  <Location class="w-5 h-5 text-emerald-400" />
                </div>
                <div>
                  <h3 class="text-white font-medium">地域层级</h3>
                  <p class="text-xs text-slate-400 mt-0.5">{{ flatRegionList.length }} 个地域</p>
                </div>
              </div>
            </div>
            <button @click="handleAddRootRegion" class="add-region-btn w-full">
              <Plus class="w-4 h-4 mr-2" />
              新增根地域
            </button>
          </div>

          <!-- 地域树 -->
          <div class="flex-1 overflow-y-auto p-3 custom-scrollbar" v-loading="regionTreeLoading">
            <el-tree
              ref="regionTreeRef"
              :data="regionTreeData"
              :props="{ children: 'children', label: 'name' }"
              node-key="id"
              :highlight-current="true"
              :expand-on-click-node="false"
              @node-click="handleRegionNodeClick"
              class="region-tree"
            >
              <template #default="{ node, data }">
                <div class="tree-node">
                  <span class="tree-node-label">{{ node.label }}</span>
                  <div class="tree-node-actions" @click.stop>
                    <button
                      @click="handleAddChildRegion(data)"
                      class="tree-action-btn"
                      title="添加子地域"
                    >
                      <Plus class="w-3.5 h-3.5" />
                    </button>
                    <button
                      @click="handleEditRegion(data)"
                      class="tree-action-btn"
                      title="编辑"
                    >
                      <Edit class="w-3.5 h-3.5" />
                    </button>
                    <button
                      @click="handleDeleteRegion(data)"
                      class="tree-action-btn text-red-400 hover:text-red-300"
                      title="删除"
                    >
                      <Delete class="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </template>
            </el-tree>
          </div>
        </div>
      </div>

      <!-- 右侧：影院列表 -->
      <div class="flex-1 min-w-0">
        <!-- 页面标题 -->
        <div class="mb-6 animate-fade-in">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button
                @click="regionPanelCollapsed = !regionPanelCollapsed"
                class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center shadow-lg shadow-emerald-500/30 hover:scale-105 transition-transform"
              >
                <Location class="w-6 h-6 text-white" />
              </button>
              <div>
                <h1 class="text-2xl font-bold text-white">影院管理</h1>
                <p class="text-slate-400 text-sm">管理影院信息与地域归属</p>
              </div>
            </div>
            <button @click="handleAdd" class="add-btn from-emerald-500 to-teal-500">
              <Plus class="w-4 h-4 mr-1.5" />
              新增影院
            </button>
          </div>
        </div>

        <!-- 筛选控制栏 -->
        <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.1s">
          <div class="flex items-center gap-2 mb-4">
            <Filter class="w-4 h-4 text-emerald-400" />
            <span class="text-sm font-medium text-slate-300">筛选搜索</span>
          </div>

          <div class="flex items-center gap-4 flex-wrap">
            <div class="flex-1 min-w-[200px]">
              <div class="relative">
                <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  v-model="queryParams.search"
                  type="text"
                  placeholder="搜索影院名称、地址..."
                  class="search-input"
                  @keyup.enter="handleSearch"
                  style="width: 80%"
                />
              </div>
            </div>

            <div class="min-w-[180px]">
              <el-select
                v-model="queryParams.region"
                placeholder="筛选地域"
                clearable
                filterable
                class="filter-select"
                popper-class="cinema-select-dropdown"
                style="width: 100%"
                @change="handleSearch"
              >
                <el-option
                  v-for="region in flatRegionList"
                  :key="region.id"
                  :label="getRegionPath(region)"
                  :value="region.id"
                />
              </el-select>
            </div>

            <button @click="handleSearch" class="action-btn">
              <Search class="w-4 h-4 mr-1.5" />
              搜索
            </button>
            <button @click="handleReset" class="action-btn-secondary">
              <Refresh class="w-4 h-4 mr-1.5" />
              重置
            </button>
          </div>

          <!-- 已选地域提示 -->
          <div v-if="selectedRegionNode" class="mt-4 flex items-center gap-2">
            <span class="text-sm text-slate-400">已选地域:</span>
            <span class="selected-region-tag">
              <Location class="w-3.5 h-3.5 mr-1" />
              {{ selectedRegionNode.name }}
              <button @click="handleClearRegion" class="ml-1 hover:text-white">
                <Close class="w-3 h-3" />
              </button>
            </span>
          </div>
        </div>

        <!-- 数据表格区域 -->
        <div class="glass-card rounded-2xl border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
          <!-- 表格头部信息 -->
          <div class="px-6 py-4 border-b border-white/10 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
                <Film class="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <h3 class="text-white font-medium">影院列表</h3>
                <p class="text-xs text-slate-400 mt-0.5">共 <span class="text-emerald-400 font-medium">{{ total }}</span> 家影院</p>
              </div>
            </div>
          </div>

          <!-- 表格 -->
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/10">
                  <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">影院</th>
                  <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">地址</th>
                  <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">联系电话</th>
                  <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">所属地域</th>
                  <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading && tableData.length === 0">
                  <td colspan="5" class="py-20 text-center">
                    <div class="flex flex-col items-center">
                      <div class="w-12 h-12 rounded-full border-2 border-emerald-500/30 border-t-emerald-500 animate-spin mb-4"></div>
                      <p class="text-slate-400">加载中...</p>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="tableData.length === 0">
                  <td colspan="5" class="py-20 text-center">
                    <div class="flex flex-col items-center">
                      <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                        <Film class="w-8 h-8 text-slate-600" />
                      </div>
                      <p class="text-slate-500 mb-1">暂无影院数据</p>
                      <p class="text-slate-600 text-sm">点击上方「新增影院」开始添加</p>
                    </div>
                  </td>
                </tr>
                <tr
                  v-for="(record, index) in tableData"
                  :key="record.id"
                  class="border-b border-white/5 hover:bg-white/5 transition-colors group"
                >
                  <td class="py-4 px-6">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
                        <Film class="w-5 h-5 text-emerald-400" />
                      </div>
                      <div>
                        <div class="text-white text-sm font-medium">{{ record.name }}</div>
                        <div class="text-slate-500 text-xs">ID: {{ record.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="py-4 px-6">
                    <div class="flex items-center gap-2 text-slate-300 text-sm max-w-[250px]">
                      <Location class="w-4 h-4 text-slate-500 flex-shrink-0" />
                      <span class="truncate" :title="record.address">{{ record.address }}</span>
                    </div>
                  </td>
                  <td class="py-4 px-6">
                    <div v-if="record.phone" class="flex items-center gap-2 text-slate-300 text-sm">
                      <Phone class="w-4 h-4 text-slate-500" />
                      <span>{{ record.phone }}</span>
                    </div>
                    <span v-else class="text-slate-500 text-sm">-</span>
                  </td>
                  <td class="py-4 px-6">
                    <span class="region-badge" :class="getCinemaColor(record.id || index)">
                      <Location class="w-3.5 h-3.5 mr-1" />
                      {{ record.parent_region_name ? record.parent_region_name + ' / ' : '' }}{{ record.region_name || '-' }}
                    </span>
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
    </div>

    <!-- 新增/编辑影院对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      class="cinema-dialog"
      destroy-on-close
    >
      <div class="space-y-5">
        <div class="form-group">
          <label class="form-label">
            <Film class="w-4 h-4" />
            影院名称 <span class="text-red-400">*</span>
          </label>
          <el-input
            v-model="form.name"
            placeholder="请输入影院名称"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Location class="w-4 h-4" />
            地址 <span class="text-red-400">*</span>
          </label>
          <el-input
            v-model="form.address"
            placeholder="请输入影院地址"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Phone class="w-4 h-4" />
            联系电话
          </label>
          <el-input
            v-model="form.phone"
            placeholder="请输入联系电话（可选）"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Location class="w-4 h-4" />
            所属地域 <span class="text-red-400">*</span>
          </label>
          <el-tree-select
            v-model="form.region"
            :data="regionTreeData"
            :props="{ label: 'name', children: 'children' }"
            placeholder="请选择所属地域"
            check-strictly
            filterable
            clearable
            class="form-input"
            popper-class="cinema-select-dropdown"
            style="width: 100%"
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

    <!-- 新增/编辑地域对话框 -->
    <el-dialog
      v-model="regionDialogVisible"
      :title="regionDialogTitle"
      width="480px"
      :close-on-click-modal="false"
      class="region-dialog"
      destroy-on-close
    >
      <div class="space-y-5">
        <div class="form-group">
          <label class="form-label">
            <Location class="w-4 h-4" />
            地域名称 <span class="text-red-400">*</span>
          </label>
          <el-input
            v-model="regionForm.name"
            placeholder="请输入地域名称，如：北京市、朝阳区"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Grid class="w-4 h-4" />
            上级地域
          </label>
          <el-select
            v-model="regionForm.parent"
            placeholder="请选择上级地域（可选）"
            clearable
            filterable
            class="form-input"
            popper-class="cinema-select-dropdown"
            style="width: 100%"
            :disabled="regionDialogMode === 'add-child'"
          >
            <el-option
              v-for="region in flatRegionList"
              :key="region.id"
              :label="region.name"
              :value="region.id"
              :disabled="regionForm.id && region.id === regionForm.id"
            />
          </el-select>
        </div>

        <div class="form-group">
          <label class="form-label">
            <Grid class="w-4 h-4" />
            编码
          </label>
          <el-input
            v-model="regionForm.code"
            placeholder="请输入地域编码（可选）"
            class="form-input"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3 pt-2">
          <el-button @click="handleCancelRegion" size="large">取消</el-button>
          <el-button
            type="primary"
            @click="submitRegionForm"
            :loading="formLoading"
            size="large"
            class="submit-btn"
          >
            {{ regionForm.id ? '保存修改' : '确认添加' }}
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
  background: linear-gradient(135deg, #14b8a6, #10b981);
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

/* ============================================
   左侧地域面板
   ============================================ */
.region-sidebar {
  flex-shrink: 0;
}

.add-region-btn {
  padding: 10px 16px;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.add-region-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 地域树 */
.region-tree {
  background: transparent;
  color: #cbd5e1;
}

:deep(.region-tree .el-tree-node__content) {
  height: 36px;
  border-radius: 8px;
  transition: all 0.2s;
  margin-bottom: 1px;
}

:deep(.region-tree .el-tree-node__content:hover) {
  background: rgba(16, 185, 129, 0.1);
}

:deep(.region-tree .el-tree-node.is-current > .el-tree-node__content) {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(20, 184, 166, 0.2));
  border-left: 3px solid #10b981;
}

:deep(.region-tree .el-tree-node__expand-icon) {
  color: #94a3b8;
}

.tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 4px;
}

.tree-node-label {
  flex: 1;
  font-size: 13px;
}

.tree-node-actions {
  display: flex;
  gap: 1px;
  opacity: 0;
  transition: opacity 0.2s;
}

:deep(.region-tree .el-tree-node__content:hover) .tree-node-actions {
  opacity: 1;
}

.tree-action-btn {
  padding: 4px;
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.4);
  transition: all 0.2s;
}

.tree-action-btn:hover {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

/* ============================================
   主区域样式
   ============================================ */
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
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

/* ============================================
   筛选区域样式
   ============================================ */
.filter-select {
  --el-input-bg-color: rgba(255, 255, 255, 0.05);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-input-hover-border-color: rgba(16, 185, 129, 0.5);
  --el-input-focus-border-color: #10b981;
  --el-text-color-placeholder: rgba(255, 255, 255, 0.3);
  --el-fill-color-blank: rgba(255, 255, 255, 0.05);
  --el-bg-color: rgba(15, 23, 42, 0.95);
  --el-text-color-regular: rgba(255, 255, 255, 0.85);
  --el-text-color-secondary: rgba(255, 255, 255, 0.65);
  --el-border-color: rgba(255, 255, 255, 0.1);
}

:deep(.filter-select .el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  border-radius: 12px;
  transition: all 0.3s ease;
}

:deep(.filter-select .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.5) inset;
}

:deep(.filter-select .el-input__wrapper.is-focus) {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px #10b981 inset !important;
}

:deep(.filter-select .el-input__inner) {
  color: #fff;
}

:deep(.filter-select .el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

/* 筛选下拉面板样式 */
:deep(.el-select-dropdown) {
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
}

:deep(.el-select-dropdown__item) {
  color: rgba(255, 255, 255, 0.85);
  background: transparent;
  transition: all 0.2s;
}

:deep(.el-select-dropdown__item:hover) {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

:deep(.el-select-dropdown__item.is-selected) {
  background: rgba(16, 185, 129, 0.25);
  color: #10b981;
}

/* 已选地域标签 */
.selected-region-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  color: #fff;
  gap: 4px;
}

/* 按钮样式 */
.action-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
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
  background: linear-gradient(135deg, #10b981, #14b8a6);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* 地域徽章 */
.region-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
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

/* ============================================
   对话框样式
   ============================================ */
:deep(.cinema-dialog),
:deep(.region-dialog) {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.cinema-dialog .el-dialog__header),
:deep(.region-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 24px;
}

:deep(.cinema-dialog .el-dialog__title),
:deep(.region-dialog .el-dialog__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.cinema-dialog .el-dialog__body),
:deep(.region-dialog .el-dialog__body) {
  padding: 24px;
  background: #0f172a;
}

:deep(.cinema-dialog .el-dialog__footer),
:deep(.region-dialog .el-dialog__footer) {
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

.form-input {
  --el-input-bg-color: rgba(255, 255, 255, 0.05);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-fill-color-blank: rgba(255, 255, 255, 0.05);
  --el-text-color-regular: #fff;
  --el-text-color-placeholder: rgba(255, 255, 255, 0.3);
}

.form-input :deep(.el-input__wrapper),
.form-input :deep(.el-select .el-input__wrapper),
.form-input :deep(.el-tree-select .el-input__wrapper) {
  background-color: var(--el-input-bg-color);
  border: 1px solid var(--el-input-border-color);
  box-shadow: none;
  transition: all 0.3s ease;
}

.form-input :deep(.el-input__wrapper:hover),
.form-input :deep(.el-select .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.5) inset;
}

.form-input :deep(.el-input__wrapper.is-focus),
.form-input :deep(.el-select .el-input__wrapper.is-focus) {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px #10b981 inset !important;
}

.form-input :deep(.el-input__inner),
.form-input :deep(.el-select__selected-item) {
  color: #fff;
}

.form-input :deep(.el-input__inner::placeholder),
.form-input :deep(.el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.form-input :deep(.el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

.form-input :deep(.el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
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
</style>

<style>
/* ============================================
   影院管理 - 下拉选项面板全局样式
   ============================================ */
/* 筛选下拉面板 - 绿色系 */
.cinema-select-dropdown.el-select-dropdown {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.cinema-select-dropdown .el-select-dropdown__item {
  color: rgba(255, 255, 255, 0.85) !important;
  background: transparent !important;
  transition: all 0.2s;
}

.cinema-select-dropdown .el-select-dropdown__item:hover {
  background: rgba(16, 185, 129, 0.15) !important;
  color: #34d399 !important;
}

.cinema-select-dropdown .el-select-dropdown__item.is-selected {
  background: rgba(16, 185, 129, 0.25) !important;
  color: #34d399 !important;
}

.cinema-select-dropdown .el-select-dropdown__item.is-disabled {
  color: rgba(255, 255, 255, 0.25) !important;
}

/* 滚动条样式 */
.cinema-select-dropdown .el-scrollbar__bar {
  background: rgba(255, 255, 255, 0.1);
}

.cinema-select-dropdown .el-scrollbar__thumb {
  background: rgba(16, 185, 129, 0.5);
  border-radius: 3px;
}

.cinema-select-dropdown .el-scrollbar__thumb:hover {
  background: rgba(16, 185, 129, 0.7);
}

/* 空状态 */
.cinema-select-dropdown .el-select-dropdown__empty {
  color: rgba(255, 255, 255, 0.4) !important;
}

/* 树形选择器样式适配 */
.cinema-select-dropdown .el-tree {
  background: transparent;
  color: rgba(255, 255, 255, 0.85);
}

.cinema-select-dropdown .el-tree-node__content {
  height: 34px;
  border-radius: 4px;
  margin: 2px 4px;
}

.cinema-select-dropdown .el-tree-node__content:hover,
.cinema-select-dropdown .el-tree-node:focus > .el-tree-node__content {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.cinema-select-dropdown .el-tree-node.is-current > .el-tree-node__content {
  background: rgba(16, 185, 129, 0.25);
  color: #34d399;
  font-weight: 500;
}

.cinema-select-dropdown .el-tree-node__expand-icon {
  color: rgba(255, 255, 255, 0.5);
}

.cinema-select-dropdown .el-tree-node__expand-icon.is-leaf {
  color: transparent;
}
</style>
