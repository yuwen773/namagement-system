<template>
  <div class="user-management-page">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">用户管理</h1>
            <p class="page-subtitle">管理系统用户账户</p>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-pill">
            <span class="stat-dot"></span>
            <span class="stat-value">{{ total.toLocaleString() }}</span>
            <span class="stat-label">用户总数</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Control Bar -->
    <section class="control-bar">
      <div class="search-container">
        <div class="search-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            v-model="searchKeyword"
            type="text"
            class="search-input"
            placeholder="搜索用户名..."
            @keyup.enter="handleSearch"
            @input="handleSearchInput"
          />
          <button v-if="searchKeyword" class="clear-btn" @click="clearSearch">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
          <button class="search-btn" :disabled="tableLoading" @click="handleSearch">
            <svg v-if="!tableLoading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <span v-else class="loading-spinner-small"></span>
          </button>
        </div>
      </div>

      <div class="control-actions">
        <button class="refresh-btn" :disabled="tableLoading" @click="fetchData">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
            <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
            <path d="M16 21h5v-5"/>
          </svg>
          <span>刷新</span>
        </button>
        <button class="add-btn" @click="openAddDialog">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>添加用户</span>
        </button>
      </div>
    </section>

    <!-- User Table -->
    <section class="table-section">
      <div class="table-container">
        <!-- Table Header -->
        <div class="table-header">
          <div class="header-row">
            <div class="header-cell col-id">ID</div>
            <div class="header-cell col-username">用户名</div>
            <div class="header-cell col-role">角色</div>
            <div class="header-cell col-status">状态</div>
            <div class="header-cell col-created">创建时间</div>
            <div class="header-cell col-actions">操作</div>
          </div>
        </div>

        <!-- Table Body -->
        <div class="table-body" v-loading="tableLoading" element-loading-text="加载中...">
          <!-- Loading Skeleton -->
          <template v-if="tableLoading">
            <div v-for="n in 8" :key="n" class="skeleton-row">
              <div class="skeleton-cell col-id"><div class="skeleton-block" style="width: 30px;"></div></div>
              <div class="skeleton-cell col-username"><div class="skeleton-block" style="width: 100px;"></div></div>
              <div class="skeleton-cell col-role"><div class="skeleton-block" style="width: 60px;"></div></div>
              <div class="skeleton-cell col-status"><div class="skeleton-block" style="width: 50px;"></div></div>
              <div class="skeleton-cell col-created"><div class="skeleton-block" style="width: 120px;"></div></div>
              <div class="skeleton-cell col-actions"><div class="skeleton-block" style="width: 100px;"></div></div>
            </div>
          </template>

          <!-- Data Rows -->
          <template v-else>
            <div
              v-for="(row, index) in tableData"
              :key="row.id"
              class="data-row"
              :style="{ animationDelay: `${index * 0.04}s` }"
            >
              <div class="data-cell col-id">
                <span class="row-id">{{ String(row.id).padStart(4, '0') }}</span>
              </div>
              <div class="data-cell col-username">
                <div class="username-cell">
                  <div class="user-avatar-small">{{ row.username.charAt(0).toUpperCase() }}</div>
                  <span class="username-text">{{ row.username }}</span>
                </div>
              </div>
              <div class="data-cell col-role">
                <span class="role-badge" :class="row.role">
                  {{ row.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </div>
              <div class="data-cell col-status">
                <span class="status-badge" :class="row.is_active ? 'active' : 'inactive'">
                  <span class="status-dot"></span>
                  {{ row.is_active ? '正常' : '禁用' }}
                </span>
              </div>
              <div class="data-cell col-created">
                <span class="time-text">{{ formatDate(row.created_at) }}</span>
              </div>
              <div class="data-cell col-actions">
                <button class="action-btn edit" @click="openEditDialog(row)" title="编辑">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                </button>
                <button
                  class="action-btn delete"
                  @click="handleDelete(row)"
                  :disabled="row.id === authStore.userInfo?.id"
                  title="删除"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="!tableData.length" class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <h3 class="empty-title">暂无用户</h3>
              <p class="empty-desc">点击"添加用户"创建新账户</p>
            </div>
          </template>
        </div>
      </div>

      <!-- Pagination -->
      <div class="pagination-wrapper" v-if="total > 0">
        <div class="pagination-info">
          显示第 <span class="info-highlight">{{ (currentPage - 1) * pageSize + 1 }}</span> 到
          <span class="info-highlight">{{ Math.min(currentPage * pageSize, total) }}</span> 条，
          共 <span class="info-highlight">{{ total }}</span> 条
        </div>
        <div class="pagination-controls">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            :total="total"
            layout="prev, pager, next, sizes, jumper"
            background
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </section>

    <!-- Add/Edit User Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '添加用户'"
      width="480px"
      class="user-dialog"
      :show-close="true"
      :close-on-click-modal="false"
    >
      <el-form
        ref="dialogFormRef"
        :model="dialogForm"
        :rules="dialogRules"
        class="user-form"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="dialogForm.username"
            placeholder="请输入用户名"
            :disabled="isEdit"
          />
        </el-form-item>

        <el-form-item label="密码" :prop="isEdit ? '' : 'password'">
          <el-input
            v-model="dialogForm.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="请输入密码"
          >
            <template #suffix>
              <button type="button" class="toggle-btn" @click="showPassword = !showPassword">
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </button>
            </template>
          </el-input>
          <div class="form-tip" v-if="isEdit">留空则不修改密码</div>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="dialogForm.role" placeholder="选择角色" class="role-select">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>

        <el-form-item label="状态" prop="is_active" v-if="isEdit">
          <el-switch
            v-model="dialogForm.is_active"
            active-text="正常"
            inactive-text="禁用"
            class="status-switch"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="dialogVisible = false">取消</button>
          <button class="confirm-btn" :disabled="dialogLoading" @click="handleDialogSubmit">
            <span v-if="!dialogLoading">{{ isEdit ? '保存' : '添加' }}</span>
            <span v-else class="btn-loading">
              <span class="spinner"></span>
              处理中...
            </span>
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessageBox, ElMessage } from 'element-plus'
import request from '@/utils/request'

const authStore = useAuthStore()

// Table state
const tableData = ref([])
const tableLoading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const searchTimer = ref(null)

// Dialog state
const dialogVisible = ref(false)
const dialogFormRef = ref(null)
const dialogLoading = ref(false)
const isEdit = ref(false)
const showPassword = ref(false)
const editingId = ref(null)

const dialogForm = reactive({
  username: '',
  password: '',
  role: 'user',
  is_active: true
})

// Dialog validation rules
const validateUsername = (rule, value, callback) => {
  if (!value || value.length < 3) {
    callback(new Error('用户名至少3个字符'))
  } else {
    callback()
  }
}

const validatePassword = (rule, value, callback) => {
  if (!isEdit.value && (!value || value.length < 6)) {
    callback(new Error('密码至少6个字符'))
  } else {
    callback()
  }
}

const dialogRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { validator: validateUsername, trigger: 'blur' }
  ],
  password: [
    { validator: validatePassword, trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

// Methods
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

const fetchData = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined
    }
    const res = await request.get('/api/auth/users/', { params })
    if (res.code === 0 || res.code === 200) {
      tableData.value = res.data || []
      total.value = res.total || 0
    }
  } catch (e) {
    console.error('Failed to fetch users:', e)
    ElMessage.error('获取用户列表失败')
  } finally {
    tableLoading.value = false
  }
}

const handleSearchInput = () => {
  if (searchTimer.value) clearTimeout(searchTimer.value)
  searchTimer.value = setTimeout(() => {
    currentPage.value = 1
    fetchData()
  }, 300)
}

const handleSearch = () => {
  if (searchTimer.value) clearTimeout(searchTimer.value)
  currentPage.value = 1
  fetchData()
}

const clearSearch = () => {
  searchKeyword.value = ''
  currentPage.value = 1
  fetchData()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchData()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchData()
}

const openAddDialog = () => {
  isEdit.value = false
  editingId.value = null
  dialogForm.username = ''
  dialogForm.password = ''
  dialogForm.role = 'user'
  dialogForm.is_active = true
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  editingId.value = row.id
  dialogForm.username = row.username
  dialogForm.password = ''
  dialogForm.role = row.role
  dialogForm.is_active = row.is_active
  dialogVisible.value = true
}

const handleDialogSubmit = async () => {
  if (!dialogFormRef.value) return

  try {
    await dialogFormRef.value.validate()
  } catch {
    return
  }

  dialogLoading.value = true

  try {
    if (isEdit.value) {
      // Update user
      const updateData = {
        username: dialogForm.username,
        role: dialogForm.role,
        is_active: dialogForm.is_active
      }
      if (dialogForm.password) {
        updateData.password = dialogForm.password
      }
      const res = await request.patch(`/api/auth/users/${editingId.value}/`, updateData)
      if (res.code === 0 || res.code === 200) {
        ElMessage.success('用户更新成功')
        dialogVisible.value = false
        fetchData()
      } else {
        ElMessage.error(res.message || '更新失败')
      }
    } else {
      // Create user
      const res = await request.post('/api/auth/register/', {
        username: dialogForm.username,
        password: dialogForm.password,
        role: dialogForm.role
      })
      if (res.code === 0 || res.code === 200) {
        ElMessage.success('用户创建成功')
        dialogVisible.value = false
        if (tableData.value.length === 0 && currentPage.value > 1) {
          currentPage.value = 1
        }
        fetchData()
      } else {
        ElMessage.error(res.message || '创建失败')
      }
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.message || '操作失败，请稍后重试')
  } finally {
    dialogLoading.value = false
  }
}

const handleDelete = async (row) => {
  if (row.id === authStore.userInfo?.id) {
    ElMessage.warning('不能删除当前登录的用户')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }
    )
    tableLoading.value = true
    const res = await request.delete(`/api/auth/users/${row.id}/`)
    if (res.code === 0 || res.code === 200) {
      ElMessage.success('删除成功')
      if (tableData.value.length === 1 && currentPage.value > 1) {
        currentPage.value -= 1
      }
      fetchData()
    } else {
      ElMessage.error(res.message || '删除失败')
    }
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    tableLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* Page Layout */
.user-management-page {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  position: relative;
}

.user-management-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 30%, rgba(139, 92, 246, 0.03) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(13, 148, 136, 0.03) 0%, transparent 40%);
  pointer-events: none;
}

/* Header */
.page-header {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(167, 139, 250, 0.12) 100%);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 16px;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: #8b5cf6;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.page-title {
  font-family: 'Outfit', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 1rem;
  position: relative;
  z-index: 1;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.9); }
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #8b5cf6;
  font-family: 'Outfit', 'SF Mono', 'Fira Code', monospace;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
}

/* Control Bar */
.control-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.search-container {
  flex: 1;
  max-width: 360px;
  min-width: 240px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 1rem;
  width: 20px;
  height: 20px;
  color: #94a3b8;
  pointer-events: none;
  transition: color 0.2s ease;
}

.search-input {
  flex: 1;
  height: 44px;
  padding: 0 3.5rem 0 3rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #1e293b;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  outline: none;
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.clear-btn {
  position: absolute;
  right: 3.5rem;
  width: 20px;
  height: 20px;
  padding: 0;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.2s ease;
}

.clear-btn:hover {
  color: #1e293b;
}

.clear-btn svg {
  width: 16px;
  height: 16px;
}

.search-btn {
  position: absolute;
  right: 0.5rem;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border: none;
  border-radius: 10px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.search-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-btn svg {
  width: 16px;
  height: 16px;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.control-actions {
  display: flex;
  gap: 0.75rem;
}

.refresh-btn,
.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  font-size: 0.875rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #475569;
}

.refresh-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.add-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border: none;
  color: #fff;
  font-weight: 600;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.refresh-btn svg,
.add-btn svg {
  width: 18px;
  height: 18px;
}

/* Table Section */
.table-section {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.table-container {
  overflow-x: auto;
}

.table-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.header-row {
  display: flex;
  min-width: 900px;
}

.header-cell {
  padding: 1rem 1.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.col-id { width: 80px; flex-shrink: 0; text-align: center; }
.col-username { width: 180px; flex-shrink: 0; }
.col-role { width: 120px; flex-shrink: 0; }
.col-status { width: 100px; flex-shrink: 0; }
.col-created { width: 160px; flex-shrink: 0; }
.col-actions { width: 120px; flex-shrink: 0; text-align: center; }

.table-body {
  min-height: 320px;
}

.data-row {
  display: flex;
  min-width: 900px;
  border-bottom: 1px solid #f1f5f9;
  animation: rowFadeIn 0.4s ease-out forwards;
  opacity: 0;
  transition: background 0.15s ease;
}

@keyframes rowFadeIn {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}

.data-row:hover {
  background: rgba(139, 92, 246, 0.03);
}

.data-row:last-child {
  border-bottom: none;
}

.data-cell {
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #334155;
}

.col-id { justify-content: center; }
.col-username { justify-content: flex-start; gap: 0.75rem; }
.col-role { justify-content: flex-start; }
.col-status { justify-content: flex-start; }
.col-created { justify-content: flex-start; }
.col-actions { justify-content: center; gap: 0.5rem; }

.row-id {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.username-cell {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
}

.username-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.role-badge.admin {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.role-badge.user {
  background: rgba(13, 148, 136, 0.1);
  color: #0d9488;
  border: 1px solid rgba(13, 148, 136, 0.2);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8rem;
}

.status-badge .status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: none;
}

.status-badge.active .status-dot {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
}

.status-badge.inactive .status-dot {
  background: #94a3b8;
}

.status-badge.active {
  color: #10b981;
}

.status-badge.inactive {
  color: #94a3b8;
}

.time-text {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.8rem;
  color: #64748b;
}

/* Action Buttons */
.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.action-btn.edit:hover {
  background: rgba(13, 148, 136, 0.08);
  border-color: rgba(13, 148, 136, 0.2);
  color: #0d9488;
}

.action-btn.delete:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

/* Skeleton Loading */
.skeleton-row {
  display: flex;
  min-width: 900px;
  border-bottom: 1px solid #f1f5f9;
}

.skeleton-cell {
  padding: 1rem 1.25rem;
}

.skeleton-block {
  height: 16px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.col-id { width: 80px; flex-shrink: 0; }
.col-username { width: 180px; flex-shrink: 0; }
.col-role { width: 120px; flex-shrink: 0; }
.col-status { width: 100px; flex-shrink: 0; }
.col-created { width: 160px; flex-shrink: 0; }
.col-actions { width: 120px; flex-shrink: 0; }

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  min-height: 240px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  margin-bottom: 1.5rem;
}

.empty-icon svg {
  width: 36px;
  height: 36px;
  color: #cbd5e1;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem;
}

.empty-desc {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  flex-wrap: wrap;
  gap: 1rem;
}

.pagination-info {
  font-size: 0.8rem;
  color: #64748b;
}

.info-highlight {
  font-weight: 500;
  color: #8b5cf6;
  font-family: 'Outfit', 'SF Mono', 'Fira Code', monospace;
}

.pagination-controls {
  display: flex;
  justify-content: flex-end;
}

/* Dialog Styles */
.user-dialog :deep(.el-dialog) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.12);
}

.user-dialog :deep(.el-dialog__header) {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.user-dialog :deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.user-dialog :deep(.el-dialog__headerbtn) {
  top: 1rem;
  right: 1rem;
  width: 32px;
  height: 32px;
  background: #f8fafc;
  border-radius: 8px;
}

.user-dialog :deep(.el-dialog__body) {
  padding: 1.5rem;
}

.user-form :deep(.el-form-item__label) {
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
}

.user-form :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
}

.user-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(139, 92, 246, 0.5);
}

.user-form :deep(.el-input__wrapper.is-focus) {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.user-form :deep(.el-input__inner) {
  color: #1e293b;
  height: 44px;
}

.user-form :deep(.el-select .el-input__inner) {
  height: 44px;
}

.toggle-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
}

.toggle-btn:hover {
  color: #8b5cf6;
}

.toggle-btn svg {
  width: 18px;
  height: 18px;
}

.form-tip {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.375rem;
}

.role-select {
  width: 100%;
}

.status-switch :deep(.el-switch__label) {
  color: #64748b;
}

.status-switch :deep(.el-switch__label.is-active) {
  color: #8b5cf6;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
}

.cancel-btn,
.confirm-btn {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #475569;
}

.cancel-btn:hover {
  background: #f8fafc;
}

.confirm-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border: none;
  color: #fff;
  font-weight: 600;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Element Plus Pagination Override */
.pagination-controls :deep(.el-pagination) {
  --el-pagination-bg-color: #ffffff;
  --el-pagination-text-color: #475569;
  --el-pagination-hover-color: #8b5cf6;
  --el-pagination-font-size: 0.8rem;
}

.pagination-controls :deep(.el-pagination .el-pager li) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin: 0 0.25rem;
  min-width: 32px;
  height: 32px;
  line-height: 32px;
}

.pagination-controls :deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  color: #fff;
  border-color: #8b5cf6;
}

/* Responsive */
@media (max-width: 1024px) {
  .user-management-page {
    padding: 1.5rem;
  }

  .control-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-container {
    max-width: 100%;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .pagination-wrapper {
    flex-direction: column;
    align-items: stretch;
  }

  .pagination-controls {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .user-management-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .header-icon {
    width: 48px;
    height: 48px;
  }

  .header-icon svg {
    width: 24px;
    height: 24px;
  }

  .control-actions {
    flex-direction: column;
  }

  .refresh-btn,
  .add-btn {
    justify-content: center;
  }
}
</style>
