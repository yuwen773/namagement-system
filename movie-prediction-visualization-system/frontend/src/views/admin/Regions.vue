<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  Edit,
  Delete,
  Refresh,
  Grid,
  Location,
  Check,
  Close,
  Filter
} from '@element-plus/icons-vue'
import {
  getRegions,
  createRegion,
  updateRegion,
  deleteRegion
} from '@/api/cinema'

const loading = ref(false)
const tableLoading = ref(false)

const tableData = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  search: '',
  parent: null
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增地域')
const formLoading = ref(false)

const form = reactive({
  id: null,
  name: '',
  parent: null,
  code: ''
})

const rules = {
  name: [{ required: true, message: '请输入地域名称', trigger: 'blur' }]
}

const formRef = ref(null)

const allRegions = ref([])
const regionLoading = ref(false)

const loadRegions = async () => {
  regionLoading.value = true
  try {
    const res = await getRegions()
    allRegions.value = res.data || []
  } catch (error) {
    console.error('加载地域失败:', error)
  } finally {
    regionLoading.value = false
  }
}

const loadData = async () => {
  tableLoading.value = true
  try {
    const res = await getRegions(queryParams)
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
  queryParams.parent = null
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
  dialogTitle.value = '新增地域'
  resetForm()
  loadRegions()
  dialogVisible.value = true
}

const handleEdit = async (row) => {
  dialogTitle.value = '编辑地域'
  Object.assign(form, {
    id: row.id,
    name: row.name,
    parent: row.parent?.id || row.parent || null,
    code: row.code || ''
  })
  await loadRegions()
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除地域"${row.name}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(async () => {
    try {
      await deleteRegion(row.id)
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
  form.parent = null
  form.code = ''
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
      await updateRegion(form.id, form)
      ElMessage.success({
        message: '更新成功',
        icon: Check
      })
    } else {
      await createRegion(form)
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

const getRegionColor = (index) => {
  const colors = [
    'from-indigo-500 to-violet-500',
    'from-purple-500 to-fuchsia-500',
    'from-violet-500 to-purple-500',
    'from-blue-500 to-indigo-500',
    'from-cyan-500 to-blue-500',
    'from-teal-500 to-cyan-500'
  ]
  return colors[index % colors.length]
}

onMounted(() => {
  loadData()
  loadRegions()
})
</script>

<template>
  <div class="min-h-screen relative overflow-hidden regions-page">
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
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <Grid class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">地域管理</h1>
            <p class="text-slate-400 text-sm">管理行政区域与地域层级</p>
          </div>
        </div>
      </div>

      <!-- 筛选控制栏 -->
      <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.1s">
        <div class="flex items-center gap-2 mb-4">
          <Filter class="w-4 h-4 text-indigo-400" />
          <span class="text-sm font-medium text-slate-300">筛选搜索</span>
        </div>

        <div class="flex items-center gap-4 flex-wrap">
          <div class="flex-1 min-w-[200px]">
            <div class="relative">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                v-model="queryParams.search"
                type="text"
                placeholder="搜索地域名称..."
                class="search-input"
                @keyup.enter="handleSearch"
                style="width: 80%"
              />
            </div>
          </div>

          <div class="min-w-[180px]">
            <el-select
              v-model="queryParams.parent"
              placeholder="上级地域"
              clearable
              filterable
              class="filter-select"
              popper-class="region-select-dropdown"
              style="width: 100%"
            >
              <el-option
                v-for="region in allRegions"
                :key="region.id"
                :label="region.name"
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
          <div class="flex-1"></div>
          <button @click="handleAdd" class="add-btn from-indigo-500 to-violet-500">
            <Plus class="w-4 h-4 mr-1.5" />
            新增地域
          </button>
        </div>
      </div>

      <!-- 数据表格区域 -->
      <div class="glass-card rounded-2xl border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
        <!-- 表格头部信息 -->
        <div class="px-6 py-4 border-b border-white/10 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center">
              <Grid class="w-4 h-4 text-indigo-400" />
            </div>
            <div>
              <h3 class="text-white font-medium">地域列表</h3>
              <p class="text-xs text-slate-400 mt-0.5">共 <span class="text-indigo-400 font-medium">{{ total }}</span> 个地域</p>
            </div>
          </div>
        </div>

        <!-- 表格 -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">地域</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">名称</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">上级地域</th>
                <th class="text-left py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">编码</th>
                <th class="text-center py-4 px-6 text-xs font-semibold text-slate-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading && tableData.length === 0">
                <td colspan="5" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-12 h-12 rounded-full border-2 border-indigo-500/30 border-t-indigo-500 animate-spin mb-4"></div>
                    <p class="text-slate-400">加载中...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="tableData.length === 0">
                <td colspan="5" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                      <Grid class="w-8 h-8 text-slate-600" />
                    </div>
                    <p class="text-slate-500 mb-1">暂无地域数据</p>
                    <p class="text-slate-600 text-sm">点击上方「新增地域」开始添加</p>
                  </div>
                </td>
              </tr>
              <tr
                v-for="(record, index) in tableData"
                :key="record.id"
                class="border-b border-white/5 hover:bg-white/5 transition-colors group"
                :style="{ animationDelay: `${0.3 + index * 0.03}s` }"
              >
                <td class="py-4 px-6">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center">
                      <Location class="w-5 h-5 text-indigo-400" />
                    </div>
                    <span class="text-slate-500 text-xs">ID: {{ record.id }}</span>
                  </div>
                </td>
                <td class="py-4 px-6">
                  <span class="region-badge" :class="getRegionColor(index)">
                    {{ record.name }}
                  </span>
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm">
                  {{ record.parent?.name || record.parent_name || '-' }}
                </td>
                <td class="py-4 px-6 text-slate-300 text-sm">
                  <code class="code-badge">{{ record.code || '-' }}</code>
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
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
            v-model="form.name"
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
            v-model="form.parent"
            placeholder="请选择上级地域（可选）"
            clearable
            filterable
            loading="regionLoading"
            class="form-input"
            popper-class="region-select-dropdown"
            style="width: 100%"
          >
            <el-option
              v-for="region in allRegions"
              :key="region.id"
              :label="region.name"
              :value="region.id"
            />
          </el-select>
        </div>

        <div class="form-group">
          <label class="form-label">
            <Grid class="w-4 h-4" />
            编码
          </label>
          <el-input
            v-model="form.code"
            placeholder="请输入地域编码（可选）"
            class="form-input"
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
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #8b5cf6, #a855f7);
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
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* 筛选选择器 */
.filter-select {
  --el-input-bg-color: rgba(255, 255, 255, 0.05);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-input-hover-border-color: rgba(99, 102, 241, 0.5);
  --el-input-focus-border-color: #6366f1;
  --el-text-color-placeholder: rgba(255, 255, 255, 0.3);
}

:deep(.filter-select .el-input__wrapper),
:deep(.filter-select .el-select__wrapper) {
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  border-radius: 12px;
}

:deep(.filter-select .el-input__wrapper:hover),
:deep(.filter-select .el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.5) inset;
  background-color: rgba(255, 255, 255, 0.06);
}

:deep(.filter-select .el-input__wrapper.is-focus),
:deep(.filter-select .el-select__wrapper.is-focused) {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px #6366f1 inset !important;
}

:deep(.filter-select .el-input__inner) {
  color: #fff;
}

:deep(.filter-select .el-select__caret),
:deep(.filter-select .el-select__icon) {
  color: rgba(255, 255, 255, 0.5);
}

/* 按钮样式 */
.action-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
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
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

/* 地域标签 */
.region-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: linear-gradient(135deg, var(--tw-gradient-from), var(--tw-gradient-to));
  color: #fff;
}

/* 编码标签 */
.code-badge {
  display: inline-block;
  padding: 2px 8px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 6px;
  font-size: 11px;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #a5b4fc;
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
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
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
  border-color: rgba(99, 102, 241, 0.5);
}

/* 对话框样式 */
:deep(.region-dialog) {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.region-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 24px;
}

:deep(.region-dialog .el-dialog__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.region-dialog .el-dialog__body) {
  padding: 24px;
  background: #0f172a;
}

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
  --el-input-hover-border-color: rgba(99, 102, 241, 0.5);
  --el-input-focus-border-color: #6366f1;
}

.form-input :deep(.el-input__wrapper),
.form-input :deep(.el-select .el-input__wrapper),
.form-input :deep(.el-select__wrapper) {
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  transition: all 0.3s ease;
}

.form-input :deep(.el-input__wrapper:hover),
.form-input :deep(.el-select .el-input__wrapper:hover),
.form-input :deep(.el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.5) inset;
  background-color: rgba(255, 255, 255, 0.06);
}

.form-input :deep(.el-input__wrapper.is-focus),
.form-input :deep(.el-select .el-input__wrapper.is-focus),
.form-input :deep(.el-select__wrapper.is-focused) {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px #6366f1 inset !important;
}

.form-input :deep(.el-input__inner),
.form-input :deep(.el-select__selected-item) {
  color: #fff;
}

.form-input :deep(.el-input__inner::placeholder),
.form-input :deep(.el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.form-input :deep(.el-select__caret),
.form-input :deep(.el-select__icon) {
  color: rgba(255, 255, 255, 0.5);
}

/* 提交按钮 */
.submit-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}
</style>

<style>
/* ============================================
   地域管理 - 下拉选项面板全局样式
   ============================================ */
/* 筛选下拉面板 - 紫色系 */
.region-select-dropdown.el-select-dropdown {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.region-select-dropdown .el-select-dropdown__item {
  color: rgba(255, 255, 255, 0.85) !important;
  background: transparent !important;
  transition: all 0.2s;
}

.region-select-dropdown .el-select-dropdown__item:hover {
  background: rgba(99, 102, 241, 0.15) !important;
  color: #a5b4fc !important;
}

.region-select-dropdown .el-select-dropdown__item.is-selected {
  background: rgba(99, 102, 241, 0.25) !important;
  color: #a5b4fc !important;
}

.region-select-dropdown .el-select-dropdown__item.is-disabled {
  color: rgba(255, 255, 255, 0.25) !important;
}

/* 滚动条样式 */
.region-select-dropdown .el-scrollbar__bar {
  background: rgba(255, 255, 255, 0.1);
}

.region-select-dropdown .el-scrollbar__thumb {
  background: rgba(99, 102, 241, 0.5);
  border-radius: 3px;
}

.region-select-dropdown .el-scrollbar__thumb:hover {
  background: rgba(99, 102, 241, 0.7);
}

/* 空状态 */
.region-select-dropdown .el-select-dropdown__empty {
  color: rgba(255, 255, 255, 0.4) !important;
}
</style>
