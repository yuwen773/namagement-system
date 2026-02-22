<template>
  <div class="rules-manage-container">
    <!-- Header Section -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-indicator"></div>
          <div class="header-title-group">
            <h1 class="header-title">防护规则管理</h1>
            <span class="header-subtitle">PROTECTION RULES</span>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-badge">
            <span class="stat-value">{{ rulesList.length }}</span>
            <span class="stat-label">规则总数</span>
          </div>
          <div class="stat-badge active">
            <span class="stat-value">{{ enabledRulesCount }}</span>
            <span class="stat-label">已启用</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Toolbar Section -->
    <section class="toolbar-section">
      <div class="toolbar-left">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 20 20" fill="none">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索规则名称或建议内容"
            class="search-input"
            @input="handleSearch"
          />
          <button v-if="searchKeyword" @click="clearSearch" class="clear-btn">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <div class="filter-group">
          <select v-model="populationFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部人群</option>
            <option value="GENERAL">普通人群</option>
            <option value="CHILDREN">儿童</option>
            <option value="ELDERLY">老年人</option>
            <option value="PATIENTS">患者</option>
            <option value="SENSITIVE">敏感人群</option>
          </select>
          <select v-model="statusFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部状态</option>
            <option value="true">已启用</option>
            <option value="false">已禁用</option>
          </select>
        </div>
      </div>
      <div class="toolbar-right">
        <button
          v-if="selectedIds.length > 0"
          @click="batchEnable"
          class="action-btn batch-enable"
        >
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>批量启用 ({{ selectedIds.length }})</span>
        </button>
        <button
          v-if="selectedIds.length > 0"
          @click="batchDisable"
          class="action-btn batch-disable"
        >
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M6 18L18 6M6 6l12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>批量禁用</span>
        </button>
        <button @click="openCreateDialog" class="primary-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M10 5v10M5 10h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>新增规则</span>
        </button>
      </div>
    </section>

    <!-- Rules Table -->
    <section class="table-section">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载规则数据...</p>
      </div>
      <div v-else-if="filteredRules.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 20 20" fill="none">
          <path d="M10 2L2 7L10 12L18 7L10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L10 22L18 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L10 17L18 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p class="empty-text">暂无规则数据</p>
        <button @click="openCreateDialog" class="empty-action">创建第一条规则</button>
      </div>
      <div v-else class="table-wrapper">
        <table class="rules-table">
          <thead>
            <tr>
              <th class="checkbox-col">
                <input
                  type="checkbox"
                  :checked="isAllSelected"
                  @change="toggleSelectAll"
                  class="checkbox-input"
                />
              </th>
              <th>规则名称</th>
              <th>AQI 范围</th>
              <th>人群类型</th>
              <th>防护建议</th>
              <th>状态</th>
              <th class="actions-col">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="rule in filteredRules"
              :key="rule.id"
              :class="{ selected: selectedIds.includes(rule.id) }"
            >
              <td class="checkbox-col">
                <input
                  type="checkbox"
                  :checked="selectedIds.includes(rule.id)"
                  @change="toggleSelect(rule.id)"
                  class="checkbox-input"
                />
              </td>
              <td class="rule-name">
                <span class="name-text">{{ rule.rule_name }}</span>
              </td>
              <td class="aqi-range">
                <span class="range-display">
                  <span class="range-value">{{ rule.min_aqi }}</span>
                  <span class="range-separator">~</span>
                  <span class="range-value">{{ rule.max_aqi }}</span>
                </span>
              </td>
              <td class="population-type">
                <span class="type-badge" :class="getPopulationClass(rule.population_type)">
                  {{ getPopulationLabel(rule.population_type) }}
                </span>
              </td>
              <td class="advice-text">
                <span class="advice-preview">{{ truncateText(rule.advice, 50) }}</span>
              </td>
              <td class="status-col">
                <span class="status-badge" :class="{ enabled: rule.is_enabled }">
                  <span class="status-dot"></span>
                  <span class="status-text">{{ rule.is_enabled ? '已启用' : '已禁用' }}</span>
                </span>
              </td>
              <td class="actions-col">
                <div class="action-buttons">
                  <button @click="openEditDialog(rule)" class="icon-btn edit-btn" title="编辑">
                    <svg viewBox="0 0 20 20" fill="none">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                  <button @click="handleDelete(rule)" class="icon-btn delete-btn" title="删除">
                    <svg viewBox="0 0 20 20" fill="none">
                      <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Create/Edit Dialog -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="dialogVisible" class="modal-overlay" @click="closeDialog">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ isEditMode ? '编辑规则' : '新增规则' }}</h2>
              <button @click="closeDialog" class="modal-close">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <form @submit.prevent="handleSubmit" class="modal-form">
              <div class="form-group">
                <label class="form-label">规则名称</label>
                <input
                  v-model="formData.rule_name"
                  type="text"
                  class="form-input"
                  placeholder="例如：儿童-轻度污染防护"
                  required
                />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">AQI 最小值</label>
                  <input
                    v-model.number="formData.min_aqi"
                    type="number"
                    min="0"
                    max="500"
                    class="form-input"
                    placeholder="0"
                    required
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">AQI 最大值</label>
                  <input
                    v-model.number="formData.max_aqi"
                    type="number"
                    min="0"
                    max="500"
                    class="form-input"
                    placeholder="500"
                    required
                  />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">人群类型</label>
                <select v-model="formData.population_type" class="form-select" required>
                  <option value="">请选择人群类型</option>
                  <option value="GENERAL">普通人群</option>
                  <option value="CHILDREN">儿童</option>
                  <option value="ELDERLY">老年人</option>
                  <option value="PATIENTS">患者</option>
                  <option value="SENSITIVE">敏感人群</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">防护建议</label>
                <textarea
                  v-model="formData.advice"
                  class="form-textarea"
                  rows="4"
                  placeholder="请输入针对该人群的防护建议..."
                  required
                ></textarea>
                <span class="char-count">{{ formData.advice.length }} 字符</span>
              </div>
              <div class="form-group switch-group">
                <label class="form-label">启用状态</label>
                <label class="switch">
                  <input v-model="formData.is_enabled" type="checkbox" class="switch-input" />
                  <span class="switch-slider"></span>
                </label>
              </div>
              <div class="modal-footer">
                <button type="button" @click="closeDialog" class="cancel-btn">取消</button>
                <button type="submit" class="submit-btn" :disabled="submitting">
                  <span v-if="submitting">保存中...</span>
                  <span v-else>{{ isEditMode ? '保存修改' : '创建规则' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Delete Confirmation -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="deleteDialogVisible" class="modal-overlay" @click="closeDeleteDialog">
          <div class="modal-container delete-modal" @click.stop>
            <div class="delete-icon-wrapper">
              <svg class="delete-icon" viewBox="0 0 20 20" fill="none">
                <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="delete-title">确认删除规则</h3>
            <p class="delete-message">
              您确定要删除规则 "{{ deleteTarget?.rule_name }}" 吗？此操作无法撤销。
            </p>
            <div class="delete-actions">
              <button @click="closeDeleteDialog" class="cancel-btn">取消</button>
              <button @click="confirmDelete" class="delete-btn" :disabled="deleting">
                {{ deleting ? '删除中...' : '确认删除' }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  getRulesList,
  createRule,
  updateRule,
  deleteRuleById,
  batchUpdateRules
} from '@/api/admin'

// State
const loading = ref(false)
const rulesList = ref([])
const searchKeyword = ref('')
const populationFilter = ref('')
const statusFilter = ref('')
const selectedIds = ref([])

// Dialog state
const dialogVisible = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)
const editingId = ref(null)
const formData = ref({
  rule_name: '',
  min_aqi: 0,
  max_aqi: 500,
  population_type: '',
  advice: '',
  is_enabled: true
})

// Delete dialog state
const deleteDialogVisible = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

// Computed
const filteredRules = computed(() => {
  let rules = rulesList.value

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    rules = rules.filter(rule =>
      rule.rule_name.toLowerCase().includes(keyword) ||
      rule.advice.toLowerCase().includes(keyword)
    )
  }

  if (populationFilter.value) {
    rules = rules.filter(rule => rule.population_type === populationFilter.value)
  }

  if (statusFilter.value !== '') {
    const isEnabled = statusFilter.value === 'true'
    rules = rules.filter(rule => rule.is_enabled === isEnabled)
  }

  return rules
})

const enabledRulesCount = computed(() => {
  return rulesList.value.filter(rule => rule.is_enabled).length
})

const isAllSelected = computed(() => {
  return filteredRules.value.length > 0 &&
    selectedIds.value.length === filteredRules.value.length
})

// Methods
const fetchRules = async () => {
  loading.value = true
  try {
    const response = await getRulesList({
      keyword: searchKeyword.value || undefined,
      population_type: populationFilter.value || undefined,
      is_enabled: statusFilter.value !== '' ? statusFilter.value === 'true' : undefined
    })
    if (response.code === 0) {
      rulesList.value = response.data || []
    }
  } catch (error) {
    ElMessage.error('加载规则失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = debounce(() => {
  fetchRules()
}, 300)

const handleFilterChange = () => {
  fetchRules()
}

const clearSearch = () => {
  searchKeyword.value = ''
  fetchRules()
}

const toggleSelect = (id) => {
  const index = selectedIds.value.indexOf(id)
  if (index > -1) {
    selectedIds.value.splice(index, 1)
  } else {
    selectedIds.value.push(id)
  }
}

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedIds.value = []
  } else {
    selectedIds.value = filteredRules.value.map(rule => rule.id)
  }
}

const openCreateDialog = () => {
  isEditMode.value = false
  editingId.value = null
  formData.value = {
    rule_name: '',
    min_aqi: 0,
    max_aqi: 500,
    population_type: '',
    advice: '',
    is_enabled: true
  }
  dialogVisible.value = true
}

const openEditDialog = (rule) => {
  isEditMode.value = true
  editingId.value = rule.id
  formData.value = {
    rule_name: rule.rule_name,
    min_aqi: rule.min_aqi,
    max_aqi: rule.max_aqi,
    population_type: rule.population_type,
    advice: rule.advice,
    is_enabled: rule.is_enabled
  }
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
  setTimeout(() => {
    formData.value = {
      rule_name: '',
      min_aqi: 0,
      max_aqi: 500,
      population_type: '',
      advice: '',
      is_enabled: true
    }
  }, 300)
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (isEditMode.value) {
      await updateRule(editingId.value, formData.value)
      ElMessage.success('规则更新成功')
    } else {
      await createRule(formData.value)
      ElMessage.success('规则创建成功')
    }
    closeDialog()
    await fetchRules()
  } catch (error) {
    ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = (rule) => {
  deleteTarget.value = rule
  deleteDialogVisible.value = true
}

const closeDeleteDialog = () => {
  deleteDialogVisible.value = false
  deleteTarget.value = null
}

const confirmDelete = async () => {
  deleting.value = true
  try {
    await deleteRuleById(deleteTarget.value.id)
    ElMessage.success('规则删除成功')
    closeDeleteDialog()
    await fetchRules()
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    deleting.value = false
  }
}

const batchEnable = async () => {
  try {
    await batchUpdateRules({
      ids: selectedIds.value,
      is_enabled: true
    })
    ElMessage.success(`已启用 ${selectedIds.value.length} 条规则`)
    selectedIds.value = []
    await fetchRules()
  } catch (error) {
    ElMessage.error('批量启用失败')
  }
}

const batchDisable = async () => {
  try {
    await batchUpdateRules({
      ids: selectedIds.value,
      is_enabled: false
    })
    ElMessage.success(`已禁用 ${selectedIds.value.length} 条规则`)
    selectedIds.value = []
    await fetchRules()
  } catch (error) {
    ElMessage.error('批量禁用失败')
  }
}

const getPopulationLabel = (type) => {
  const labels = {
    GENERAL: '普通人群',
    CHILDREN: '儿童',
    ELDERLY: '老年人',
    PATIENTS: '患者',
    SENSITIVE: '敏感人群'
  }
  return labels[type] || type
}

const getPopulationClass = (type) => {
  const classes = {
    GENERAL: 'general',
    CHILDREN: 'children',
    ELDERLY: 'elderly',
    PATIENTS: 'patients',
    SENSITIVE: 'sensitive'
  }
  return classes[type] || ''
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

onMounted(() => {
  fetchRules()
})
</script>

<style scoped>
/* Import JetBrains Mono for data display */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* CSS Variables */
:root {
  --bg-primary: #0a0e1a;
  --bg-secondary: #0d121d;
  --bg-card: #111827;
  --bg-hover: #1a2332;
  --border-color: #1e293b;
  --border-focus: #22d3ee;
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-cyan: #22d3ee;
  --accent-cyan-dim: rgba(34, 211, 238, 0.1);
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #fbbf24;
}

/* Base Container */
.rules-manage-container {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Noto Sans SC', sans-serif;
}

/* Header Section */
.page-header {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px 28px;
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

.header-indicator {
  width: 4px;
  height: 32px;
  background: linear-gradient(180deg, var(--accent-cyan) 0%, rgba(34, 211, 238, 0.3) 100%);
  border-radius: 2px;
}

.header-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.header-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.header-stats {
  display: flex;
  gap: 16px;
}

.stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  min-width: 100px;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.stat-badge.active .stat-value {
  color: var(--success);
}

/* Toolbar Section */
.toolbar-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.toolbar-left {
  display: flex;
  gap: 16px;
  flex: 1;
  min-width: 0;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  max-width: 400px;
  min-width: 200px;
}

.search-icon {
  position: absolute;
  left: 14px;
  width: 18px;
  height: 18px;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 42px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.clear-btn {
  position: absolute;
  right: 10px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s;
}

.clear-btn:hover {
  background: var(--border-color);
  color: var(--text-primary);
}

.clear-btn svg {
  width: 14px;
  height: 14px;
}

.filter-group {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 12px 36px 12px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  transition: all 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.toolbar-right {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--bg-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.batch-enable {
  border-color: rgba(34, 211, 238, 0.3);
}

.batch-enable:hover {
  background: rgba(34, 211, 238, 0.1);
  border-color: var(--accent-cyan);
}

.batch-disable:hover {
  border-color: var(--danger);
  color: var(--danger);
}

.primary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--accent-cyan);
  border: none;
  border-radius: 12px;
  color: var(--bg-primary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.primary-btn:hover {
  background: #1ed5f3;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(34, 211, 238, 0.3);
}

.primary-btn svg {
  width: 18px;
  height: 18px;
}

/* Table Section */
.table-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  overflow: hidden;
  min-height: 400px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 20px;
  color: var(--text-muted);
  font-size: 14px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.empty-text {
  color: var(--text-muted);
  font-size: 16px;
  margin-bottom: 20px;
}

.empty-action {
  padding: 10px 20px;
  background: var(--accent-cyan);
  border: none;
  border-radius: 10px;
  color: var(--bg-primary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.empty-action:hover {
  background: #1ed5f3;
  transform: translateY(-1px);
}

.table-wrapper {
  overflow-x: auto;
}

.rules-table {
  width: 100%;
  border-collapse: collapse;
}

.rules-table thead {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.rules-table th {
  padding: 16px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rules-table tbody tr {
  border-bottom: 1px solid var(--border-color);
  transition: background 0.15s;
}

.rules-table tbody tr:hover {
  background: var(--bg-hover);
}

.rules-table tbody tr.selected {
  background: var(--accent-cyan-dim);
}

.rules-table td {
  padding: 16px 20px;
  color: var(--text-primary);
  font-size: 14px;
}

.checkbox-col {
  width: 48px;
  padding: 16px 20px !important;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  accent-color: var(--accent-cyan);
  cursor: pointer;
}

.rule-name {
  font-weight: 500;
}

.name-text {
  color: var(--text-primary);
}

.aqi-range {
  font-family: 'JetBrains Mono', monospace;
}

.range-display {
  display: flex;
  align-items: center;
  gap: 6px;
}

.range-value {
  font-weight: 600;
  color: var(--accent-cyan);
}

.range-separator {
  color: var(--text-muted);
}

.population-type {
  padding: 4px 0;
}

.type-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.type-badge.general {
  background: rgba(34, 211, 238, 0.1);
  color: var(--accent-cyan);
}

.type-badge.children {
  background: rgba(251, 191, 36, 0.1);
  color: var(--warning);
}

.type-badge.elderly {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
}

.type-badge.patients {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.type-badge.sensitive {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.advice-preview {
  color: var(--text-secondary);
  line-height: 1.5;
}

.status-col {
  width: 120px;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: 8px;
  font-size: 12px;
  color: var(--text-muted);
}

.status-badge.enabled {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.actions-col {
  width: 100px;
  padding: 16px 20px !important;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-muted);
}

.icon-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.edit-btn:hover {
  color: var(--accent-cyan);
  background: var(--accent-cyan-dim);
}

.delete-btn:hover {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
}

.icon-btn svg {
  width: 16px;
  height: 16px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 14, 26, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 100%;
  max-width: 540px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s;
}

.modal-close:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.modal-close svg {
  width: 18px;
  height: 18px;
}

.modal-form {
  padding: 28px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.2s;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  transition: all 0.2s;
}

.form-textarea:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.char-count {
  position: absolute;
  bottom: 10px;
  right: 16px;
  font-size: 11px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.switch-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
}

.switch-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-hover);
  border-radius: 26px;
  transition: all 0.3s;
}

.switch-slider::before {
  content: '';
  position: absolute;
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s;
}

.switch-input:checked + .switch-slider {
  background: var(--accent-cyan);
}

.switch-input:checked + .switch-slider::before {
  transform: translateX(22px);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 8px;
}

.cancel-btn,
.submit-btn {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.cancel-btn:hover {
  background: var(--bg-hover);
  border-color: var(--text-muted);
}

.submit-btn {
  background: var(--accent-cyan);
  border: none;
  color: var(--bg-primary);
}

.submit-btn:hover:not(:disabled) {
  background: #1ed5f3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Delete Modal */
.delete-modal {
  max-width: 400px;
  text-align: center;
}

.delete-icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.delete-icon {
  width: 56px;
  height: 56px;
  color: var(--danger);
}

.delete-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.delete-message {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 24px;
}

.delete-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.delete-btn {
  padding: 12px 24px;
  background: var(--danger);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover:not(:disabled) {
  background: #f87171;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

/* Scrollbar */
.table-wrapper::-webkit-scrollbar,
.modal-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track,
.modal-container::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.table-wrapper::-webkit-scrollbar-thumb,
.modal-container::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover,
.modal-container::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}

/* Responsive */
@media (max-width: 1024px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .toolbar-section {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-left {
    flex-direction: column;
  }

  .search-box {
    max-width: 100%;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select {
    flex: 1;
  }

  .toolbar-right {
    justify-content: stretch;
  }

  .action-btn,
  .primary-btn {
    flex: 1;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-stats {
    width: 100%;
    justify-content: space-between;
  }

  .stat-badge {
    flex: 1;
  }
}
</style>
