<script setup>
import { ref, onMounted, reactive, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
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

// ============================================
// 数据状态
// ============================================
const tableLoading = ref(false)
const regionTreeLoading = ref(false)
const formLoading = ref(false)

// 影院表格数据
const tableData = ref([])
const total = ref(0)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  search: '',
  region: null
})

// 地域树数据
const regionTreeData = ref([])
const flatRegionList = ref([]) // 扁平化地域列表，用于下拉选择

// 当前选中的地域节点
const selectedRegionId = ref(null)
const selectedRegionNode = ref(null)

// ============================================
// 影院对话框
// ============================================
const cinemaDialogVisible = ref(false)
const cinemaDialogTitle = ref('')

const cinemaForm = reactive({
  id: null,
  name: '',
  address: '',
  phone: '',
  region: null
})

const cinemaRules = {
  name: [{ required: true, message: '请输入影院名称', trigger: 'blur' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }],
  region: [{ required: true, message: '请选择所属地域', trigger: 'change' }]
}

const cinemaFormRef = ref(null)

// ============================================
// 地域对话框
// ============================================
const regionDialogVisible = ref(false)
const regionDialogTitle = ref('')
const regionDialogMode = ref('add') // add | edit
const regionTargetNode = ref(null) // 用于添加子节点时的父节点

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
const regionTreeRef = ref(null)

// 将扁平数据转换为树形结构
const buildRegionTree = (regions) => {
  const regionMap = new Map()
  const roots = []

  // 先创建所有节点的副本
  regions.forEach(region => {
    regionMap.set(region.id, { ...region, children: [] })
  })

  // 建立父子关系
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

  // 清理空children
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

// 加载地域数据
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

// 地域树节点点击
const handleRegionNodeClick = (data) => {
  selectedRegionId.value = data.id
  selectedRegionNode.value = data
  queryParams.region = data.id
  queryParams.page = 1
  loadCinemas()
}

// 清除地域选择
const handleClearRegion = () => {
  selectedRegionId.value = null
  selectedRegionNode.value = null
  queryParams.region = null
  queryParams.page = 1
  if (regionTreeRef.value) {
    regionTreeRef.value.setCurrentKey(null)
  }
  loadCinemas()
}

// ============================================
// 地域操作
// ============================================
// 添加根地域
const handleAddRootRegion = () => {
  regionDialogTitle.value = '新增根地域'
  regionDialogMode.value = 'add'
  regionTargetNode.value = null
  resetRegionForm()
  regionDialogVisible.value = true
}

// 添加子地域
const handleAddChildRegion = (node) => {
  regionDialogTitle.value = `新增子地域 - ${node.name}`
  regionDialogMode.value = 'add-child'
  regionTargetNode.value = node
  resetRegionForm()
  regionForm.parent = node.id
  regionDialogVisible.value = true
}

// 编辑地域
const handleEditRegion = (node) => {
  regionDialogTitle.value = '编辑地域'
  regionDialogMode.value = 'edit'
  regionTargetNode.value = node
  Object.assign(regionForm, {
    id: node.id,
    name: node.name,
    parent: node.parent?.id || node.parent || null,
    code: node.code || ''
  })
  regionDialogVisible.value = true
}

// 删除地域
const handleDeleteRegion = (node) => {
  const hasChildren = node.children && node.children.length > 0
  const message = hasChildren
    ? `该地域下有 ${node.children.length} 个子地域，确定要删除地域"${node.name}"吗？删除后子地域也将被删除。`
    : `确定要删除地域"${node.name}"吗？`

  ElMessageBox.confirm(message, '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteRegion(node.id)
      ElMessage.success('删除成功')
      await loadRegions()
      // 如果删除的是当前选中的地域，清除选择
      if (selectedRegionId.value === node.id) {
        handleClearRegion()
      }
    } catch (error) {
      console.error('删除地域失败:', error)
    }
  }).catch(() => {})
}

// 重置地域表单
const resetRegionForm = () => {
  regionForm.id = null
  regionForm.name = ''
  regionForm.parent = null
  regionForm.code = ''
  if (regionFormRef.value) {
    regionFormRef.value.resetFields()
  }
}

// 提交地域表单
const submitRegionForm = async () => {
  if (!regionFormRef.value) return

  await regionFormRef.value.validate(async (valid) => {
    if (!valid) return

    formLoading.value = true
    try {
      if (regionForm.id) {
        // 编辑
        await updateRegion(regionForm.id, {
          name: regionForm.name,
          parent: regionForm.parent,
          code: regionForm.code
        })
        ElMessage.success('更新成功')
      } else {
        // 新增
        const data = {
          name: regionForm.name,
          code: regionForm.code
        }
        if (regionForm.parent) {
          data.parent = regionForm.parent
        }
        await createRegion(data)
        ElMessage.success('创建成功')
      }
      regionDialogVisible.value = false
      await loadRegions()
    } catch (error) {
      console.error('提交地域表单失败:', error)
    } finally {
      formLoading.value = false
    }
  })
}

// ============================================
// 影院操作
// ============================================
// 加载影院列表
const loadCinemas = async () => {
  tableLoading.value = true
  try {
    const res = await getCinemas(queryParams)
    tableData.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    ElMessage.error('加载影院数据失败')
    console.error(error)
  } finally {
    tableLoading.value = false
  }
}

// 查询影院
const handleSearch = () => {
  queryParams.page = 1
  loadCinemas()
}

// 重置查询
const handleReset = () => {
  queryParams.search = ''
  queryParams.page = 1
  // 不重置地域选择，保持当前选中的地域
  loadCinemas()
}

// 分页
const handleSizeChange = (val) => {
  queryParams.pageSize = val
  loadCinemas()
}

const handleCurrentChange = (val) => {
  queryParams.page = val
  loadCinemas()
}

// 打开新增影院对话框
const handleAddCinema = () => {
  cinemaDialogTitle.value = '新增影院'
  resetCinemaForm()
  // 如果选中了地域，自动设置
  if (selectedRegionId.value) {
    cinemaForm.region = selectedRegionId.value
  }
  cinemaDialogVisible.value = true
}

// 打开编辑影院对话框
const handleEditCinema = (row) => {
  cinemaDialogTitle.value = '编辑影院'
  Object.assign(cinemaForm, {
    id: row.id,
    name: row.name,
    address: row.address,
    phone: row.phone || '',
    region: row.region?.id || row.region
  })
  cinemaDialogVisible.value = true
}

// 删除影院
const handleDeleteCinema = (row) => {
  ElMessageBox.confirm(
    `确定要删除影院"${row.name}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteCinema(row.id)
      ElMessage.success('删除成功')
      loadCinemas()
    } catch (error) {
      console.error('删除影院失败:', error)
    }
  }).catch(() => {})
}

// 重置影院表单
const resetCinemaForm = () => {
  cinemaForm.id = null
  cinemaForm.name = ''
  cinemaForm.address = ''
  cinemaForm.phone = ''
  cinemaForm.region = null
  if (cinemaFormRef.value) {
    cinemaFormRef.value.resetFields()
  }
}

// 提交影院表单
const submitCinemaForm = async () => {
  if (!cinemaFormRef.value) return

  await cinemaFormRef.value.validate(async (valid) => {
    if (!valid) return

    formLoading.value = true
    try {
      if (cinemaForm.id) {
        await updateCinema(cinemaForm.id, {
          name: cinemaForm.name,
          address: cinemaForm.address,
          phone: cinemaForm.phone,
          region: cinemaForm.region
        })
        ElMessage.success('更新成功')
      } else {
        await createCinema({
          name: cinemaForm.name,
          address: cinemaForm.address,
          phone: cinemaForm.phone,
          region: cinemaForm.region
        })
        ElMessage.success('创建成功')
      }
      cinemaDialogVisible.value = false
      loadCinemas()
    } catch (error) {
      console.error('提交影院表单失败:', error)
    } finally {
      formLoading.value = false
    }
  })
}

// ============================================
// 工具函数
// ============================================
// 获取地域名称路径
const getRegionPath = (region) => {
  if (!region) return '-'
  const path = []
  let current = region
  while (current) {
    path.unshift(current.name)
    // 从扁平列表中查找父节点
    current = flatRegionList.value.find(r => r.id === current.parent)
  }
  return path.join(' / ')
}

// ============================================
// 生命周期
// ============================================
onMounted(async () => {
  await loadRegions()
  await loadCinemas()
})
</script>

<template>
  <div class="cinema-region-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">影院与地域管理</h1>
      <p class="page-subtitle">管理影院信息与地域层级结构</p>
    </div>

    <!-- 主布局：左侧地域树 + 右侧影院列表 -->
    <div class="main-layout">
      <!-- 左侧：地域树 -->
      <div class="region-panel">
        <div class="panel-header">
          <div class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="9 22 9 12 15 12 15 22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>地域层级</span>
          </div>
          <div class="panel-actions">
            <el-button type="primary" size="small" @click="handleAddRootRegion">
              <el-icon><Plus /></el-icon> 新增根地域
            </el-button>
          </div>
        </div>

        <div class="region-tree-container" v-loading="regionTreeLoading">
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
                <span class="tree-node-actions" @click.stop>
                  <el-tooltip content="添加子地域" placement="top">
                    <el-button
                      type="primary"
                      link
                      size="small"
                      @click="handleAddChildRegion(data)"
                    >
                      <el-icon><Plus /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <el-tooltip content="编辑" placement="top">
                    <el-button
                      type="primary"
                      link
                      size="small"
                      @click="handleEditRegion(data)"
                    >
                      <el-icon><Edit /></el-icon>
                    </el-button>
                  </el-tooltip>
                  <el-tooltip content="删除" placement="top">
                    <el-button
                      type="danger"
                      link
                      size="small"
                      @click="handleDeleteRegion(data)"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </el-tooltip>
                </span>
              </div>
            </template>
          </el-tree>
        </div>
      </div>

      <!-- 右侧：影院列表 -->
      <div class="cinema-panel">
        <div class="panel-header">
          <div class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="2" y="4" width="20" height="16" rx="2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 8v8" stroke-width="2" stroke-linecap="round"/>
              <path d="M8 12h8" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>影院列表</span>
            <span v-if="selectedRegionNode" class="selected-region-badge">
              {{ selectedRegionNode.name }}
            </span>
          </div>
          <div class="panel-actions">
            <el-button
              v-if="selectedRegionId"
              size="small"
              @click="handleClearRegion"
            >
              显示全部影院
            </el-button>
          </div>
        </div>

        <!-- 搜索栏 -->
        <div class="search-bar">
          <el-input
            v-model="queryParams.search"
            placeholder="搜索影院名称..."
            clearable
            @keyup.enter="handleSearch"
            class="search-input"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </div>

        <!-- 操作栏 -->
        <div class="action-bar">
          <el-button type="primary" @click="handleAddCinema">
            <el-icon><Plus /></el-icon> 新增影院
          </el-button>
        </div>

        <!-- 数据表格 -->
        <div class="table-container">
          <el-table
            :data="tableData"
            v-loading="tableLoading"
            stripe
            class="data-table"
            :empty-text="selectedRegionId ? '该地域下暂无影院' : '暂无影院数据'"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="影院名称" min-width="160" show-overflow-tooltip />
            <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
            <el-table-column prop="phone" label="联系电话" width="130" />
            <el-table-column label="所属地域" min-width="150" show-overflow-tooltip>
              <template #default="{ row }">
                {{ getRegionPath(row.region) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="140" fixed="right" align="center">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditCinema(row)">
                  编辑
                </el-button>
                <el-button type="danger" link size="small" @click="handleDeleteCinema(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="queryParams.page"
              v-model:page-size="queryParams.pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 影院编辑对话框 -->
    <el-dialog
      v-model="cinemaDialogVisible"
      :title="cinemaDialogTitle"
      width="560px"
      :close-on-click-modal="false"
      @close="resetCinemaForm"
      class="cinema-dialog"
    >
      <el-form
        ref="cinemaFormRef"
        :model="cinemaForm"
        :rules="cinemaRules"
        label-width="90px"
        v-loading="formLoading"
      >
        <el-form-item label="影院名称" prop="name">
          <el-input v-model="cinemaForm.name" placeholder="请输入影院名称" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="cinemaForm.address" placeholder="请输入影院地址" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="cinemaForm.phone" placeholder="请输入联系电话（可选）" />
        </el-form-item>
        <el-form-item label="所属地域" prop="region">
          <el-select
            v-model="cinemaForm.region"
            placeholder="请选择所属地域"
            clearable
            filterable
            class="full-width"
          >
            <el-option
              v-for="region in flatRegionList"
              :key="region.id"
              :label="getRegionPath(region)"
              :value="region.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="cinemaDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCinemaForm" :loading="formLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 地域编辑对话框 -->
    <el-dialog
      v-model="regionDialogVisible"
      :title="regionDialogTitle"
      width="480px"
      :close-on-click-modal="false"
      @close="resetRegionForm"
      class="region-dialog"
    >
      <el-form
        ref="regionFormRef"
        :model="regionForm"
        :rules="regionRules"
        label-width="90px"
        v-loading="formLoading"
      >
        <el-form-item label="地域名称" prop="name">
          <el-input v-model="regionForm.name" placeholder="请输入地域名称" />
        </el-form-item>
        <el-form-item label="上级地域">
          <el-select
            v-model="regionForm.parent"
            placeholder="请选择上级地域（可选）"
            clearable
            filterable
            class="full-width"
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
        </el-form-item>
        <el-form-item label="编码">
          <el-input v-model="regionForm.code" placeholder="请输入地域编码（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="regionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRegionForm" :loading="formLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* ============================================
   页面整体样式
   ============================================ */
.cinema-region-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 24px;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-size: 14px;
  color: #94a3b8;
  margin: 0;
}

/* ============================================
   主布局
   ============================================ */
.main-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
  height: calc(100vh - 120px);
}

/* ============================================
   通用面板样式
   ============================================ */
.region-panel,
.cinema-panel {
  background: #1e293b;
  border-radius: 16px;
  border: 1px solid #334155;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #334155;
  background: rgba(15, 23, 42, 0.5);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #f1f5f9;
}

.title-icon {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

.selected-region-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: #ffffff;
  margin-left: 8px;
}

.panel-actions {
  display: flex;
  gap: 8px;
}

/* ============================================
   地域树面板
   ============================================ */
.region-tree-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.region-tree-container::-webkit-scrollbar {
  width: 6px;
}

.region-tree-container::-webkit-scrollbar-track {
  background: transparent;
}

.region-tree-container::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 3px;
}

.region-tree-container::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

.region-tree {
  background: transparent;
  color: #cbd5e1;
}

:deep(.el-tree-node__content) {
  height: 40px;
  border-radius: 8px;
  transition: all 0.2s;
  margin-bottom: 2px;
}

:deep(.el-tree-node__content:hover) {
  background: rgba(59, 130, 246, 0.1);
}

:deep(.el-tree-node.is-current > .el-tree-node__content) {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.2));
  border-left: 3px solid #3b82f6;
}

:deep(.el-tree-node__expand-icon) {
  color: #94a3b8;
}

.tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 8px;
}

.tree-node-label {
  flex: 1;
}

.tree-node-actions {
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.2s;
}

:deep(.el-tree-node__content:hover) .tree-node-actions {
  opacity: 1;
}

/* ============================================
   影院面板
   ============================================ */
.search-bar {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #334155;
  background: rgba(15, 23, 42, 0.3);
}

.search-input {
  max-width: 280px;
}

:deep(.search-input .el-input__wrapper) {
  background: #0f172a;
  border-color: #334155;
}

.action-bar {
  padding: 12px 20px;
  border-bottom: 1px solid #334155;
  background: rgba(15, 23, 42, 0.3);
}

.table-container {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.data-table {
  flex: 1;
}

:deep(.data-table) {
  background: transparent;
  color: #cbd5e1;
}

:deep(.data-table th.el-table__cell) {
  background: #0f172a;
  border-color: #334155;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
  padding: 14px 0;
}

:deep(.data-table td.el-table__cell) {
  border-color: #1e293b;
  padding: 14px 0;
}

:deep(.data-table tr:hover > td) {
  background: rgba(59, 130, 246, 0.05);
}

:deep(.data-table .el-table__empty-block) {
  background: transparent;
}

:deep(.data-table .el-table__empty-text) {
  color: #64748b;
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: flex-end;
  padding: 16px 20px;
  border-top: 1px solid #334155;
  background: rgba(15, 23, 42, 0.3);
}

:deep(.pagination-container .el-pagination) {
  color: #94a3b8;
}

:deep(.pagination-container .el-pagination button) {
  background: #0f172a;
  border-color: #334155;
  color: #cbd5e1;
}

:deep(.pagination-container .el-pagination button:hover) {
  background: #1e293b;
  border-color: #475569;
}

:deep(.pagination-container .el-pagination .el-pager li) {
  background: #0f172a;
  border-color: #334155;
  color: #cbd5e1;
}

:deep(.pagination-container .el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-color: transparent;
  color: #ffffff;
}

/* ============================================
   对话框样式
   ============================================ */
:deep(.cinema-dialog .el-dialog),
:deep(.region-dialog .el-dialog) {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
}

:deep(.cinema-dialog .el-dialog__header),
:deep(.region-dialog .el-dialog__header) {
  border-bottom: 1px solid #334155;
  padding: 20px 24px;
}

:deep(.cinema-dialog .el-dialog__title),
:deep(.region-dialog .el-dialog__title) {
  color: #f1f5f9;
  font-size: 18px;
  font-weight: 600;
}

:deep(.cinema-dialog .el-dialog__body),
:deep(.region-dialog .el-dialog__body) {
  padding: 24px;
}

:deep(.cinema-dialog .el-dialog__footer),
:deep(.region-dialog .el-dialog__footer) {
  border-top: 1px solid #334155;
  padding: 16px 24px;
}

:deep(.cinema-dialog .el-form-item__label),
:deep(.region-dialog .el-form-item__label) {
  color: #94a3b8;
}

:deep(.cinema-dialog .el-input__wrapper),
:deep(.region-dialog .el-input__wrapper) {
  background: #0f172a;
  border-color: #334155;
  box-shadow: none;
}

:deep(.cinema-dialog .el-input__wrapper:hover),
:deep(.region-dialog .el-input__wrapper:hover),
:deep(.cinema-dialog .el-input__wrapper.is-focus),
:deep(.region-dialog .el-input__wrapper.is-focus) {
  border-color: #3b82f6;
}

:deep(.cinema-dialog .el-input__inner),
:deep(.region-dialog .el-input__inner) {
  color: #cbd5e1;
}

:deep(.cinema-dialog .el-select .el-input__wrapper),
:deep(.region-dialog .el-select .el-input__wrapper) {
  background: #0f172a;
}

:deep(.cinema-dialog .el-select__placeholder),
:deep(.region-dialog .el-select__placeholder) {
  color: #64748b;
}

:deep(.cinema-dialog .el-option),
:deep(.region-dialog .el-option) {
  background: #0f172a;
  color: #cbd5e1;
}

:deep(.cinema-dialog .el-option:hover),
:deep(.region-dialog .el-option:hover) {
  background: rgba(59, 130, 246, 0.1);
}

:deep(.cinema-dialog .el-option.is-disabled),
:deep(.region-dialog .el-option.is-disabled) {
  color: #475569;
}

.full-width {
  width: 100%;
}

/* ============================================
   响应式
   ============================================ */
@media (max-width: 1200px) {
  .main-layout {
    grid-template-columns: 280px 1fr;
  }
}

@media (max-width: 900px) {
  .main-layout {
    grid-template-columns: 1fr;
    height: auto;
  }

  .region-panel,
  .cinema-panel {
    height: 500px;
  }
}
</style>
