<template>
  <div class="users-manage-container">
    <!-- Header Section -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-indicator"></div>
          <div class="header-title-group">
            <h1 class="header-title">用户管理</h1>
            <span class="header-subtitle">USER MANAGEMENT</span>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-badge">
            <span class="stat-value">{{ usersList.length }}</span>
            <span class="stat-label">总用户数</span>
          </div>
          <div class="stat-badge admin">
            <span class="stat-value">{{ adminCount }}</span>
            <span class="stat-label">管理员</span>
          </div>
          <div class="stat-badge active">
            <span class="stat-value">{{ activeUsersCount }}</span>
            <span class="stat-label">已激活</span>
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
            placeholder="搜索用户名、邮箱或手机号"
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
          <select v-model="roleFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部角色</option>
            <option value="USER">普通用户</option>
            <option value="ADMIN">管理员</option>
          </select>
          <select v-model="statusFilter" @change="handleFilterChange" class="filter-select">
            <option value="">全部状态</option>
            <option value="true">已激活</option>
            <option value="false">已禁用</option>
          </select>
        </div>
      </div>
      <div class="toolbar-right">
        <button @click="openCreateDialog" class="primary-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M10 5v10M5 10h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>新增用户</span>
        </button>
      </div>
    </section>

    <!-- Users Table -->
    <section class="table-section">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载用户数据...</p>
      </div>
      <div v-else-if="filteredUsers.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 20 20" fill="none">
          <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="7" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <p class="empty-text">暂无用户数据</p>
        <button @click="openCreateDialog" class="empty-action">创建第一个用户</button>
      </div>
      <div v-else class="table-wrapper">
        <table class="users-table">
          <thead>
            <tr>
              <th>用户名</th>
              <th>邮箱</th>
              <th>手机号</th>
              <th>角色</th>
              <th>状态</th>
              <th>注册时间</th>
              <th>最后登录</th>
              <th class="actions-col">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td class="username-cell">
                <div class="user-avatar">
                  {{ user.username?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <span class="username-text">{{ user.username }}</span>
              </td>
              <td class="email-cell">
                <span class="email-text">{{ user.email || '-' }}</span>
              </td>
              <td class="phone-cell">
                <span class="phone-text">{{ user.phone || '-' }}</span>
              </td>
              <td class="role-cell">
                <span class="role-badge" :class="{ admin: user.role === 'ADMIN' }">
                  <svg v-if="user.role === 'ADMIN'" class="role-icon" viewBox="0 0 20 20" fill="none">
                    <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-else class="role-icon" viewBox="0 0 20 20" fill="none">
                    <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  {{ user.role === 'ADMIN' ? '管理员' : '普通用户' }}
                </span>
              </td>
              <td class="status-cell">
                <span class="status-badge" :class="{ enabled: user.status }">
                  <span class="status-dot"></span>
                  <span class="status-text">{{ user.status ? '已激活' : '已禁用' }}</span>
                </span>
              </td>
              <td class="date-cell">
                <span class="date-text">{{ formatDate(user.date_joined) }}</span>
              </td>
              <td class="date-cell">
                <span class="date-text">{{ formatDate(user.last_login) }}</span>
              </td>
              <td class="actions-col">
                <div class="action-buttons">
                  <button @click="openEditDialog(user)" class="icon-btn edit-btn" title="编辑">
                    <svg viewBox="0 0 20 20" fill="none">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                  <button @click="handleDelete(user)" class="icon-btn delete-btn" title="删除">
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

    <!-- Pagination -->
    <section v-if="filteredUsers.length > pageSize" class="pagination-section">
      <div class="pagination-info">
        <span class="pagination-text">显示 {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, filteredUsers.length) }} 条，共 {{ filteredUsers.length }} 条</span>
      </div>
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1" class="page-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="{ active: page === currentPage }"
            class="page-number"
          >
            {{ page }}
          </button>
        </div>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="page-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </section>

    <!-- Create/Edit Dialog -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="dialogVisible" class="modal-overlay" @click="closeDialog">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ isEditMode ? '编辑用户' : '新增用户' }}</h2>
              <button @click="closeDialog" class="modal-close">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <form @submit.prevent="handleSubmit" class="modal-form">
              <div v-if="!isEditMode" class="form-group">
                <label class="form-label">用户名</label>
                <input
                  v-model="formData.username"
                  type="text"
                  class="form-input"
                  placeholder="请输入用户名"
                  required
                  minlength="3"
                  maxlength="20"
                />
              </div>
              <div v-if="!isEditMode" class="form-group">
                <label class="form-label">密码</label>
                <input
                  v-model="formData.password"
                  type="password"
                  class="form-input"
                  placeholder="请输入密码"
                  required
                  minlength="6"
                />
              </div>
              <div class="form-group">
                <label class="form-label">邮箱</label>
                <input
                  v-model="formData.email"
                  type="email"
                  class="form-input"
                  placeholder="请输入邮箱地址"
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">手机号</label>
                <input
                  v-model="formData.phone"
                  type="tel"
                  class="form-input"
                  placeholder="请输入手机号（可选）"
                  pattern="[0-9]*"
                />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">角色</label>
                  <select v-model="formData.role" class="form-select" required>
                    <option value="USER">普通用户</option>
                    <option value="ADMIN">管理员</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">状态</label>
                  <select v-model="formData.status" class="form-select" required>
                    <option :value="true">已激活</option>
                    <option :value="false">已禁用</option>
                  </select>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" @click="closeDialog" class="cancel-btn">取消</button>
                <button type="submit" class="submit-btn" :disabled="submitting">
                  <span v-if="submitting">保存中...</span>
                  <span v-else>{{ isEditMode ? '保存修改' : '创建用户' }}</span>
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
            <h3 class="delete-title">确认删除用户</h3>
            <p class="delete-message">
              您确定要删除用户 "{{ deleteTarget?.username }}" 吗？此操作将软删除该用户，数据将被保留但无法登录。
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
import { getUsersList, updateUser, deleteUserById } from '@/api/admin'
import { register } from '@/api/auth'

// State
const loading = ref(false)
const usersList = ref([])
const searchKeyword = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = 20

// Dialog state
const dialogVisible = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)
const editingId = ref(null)
const formData = ref({
  username: '',
  password: '',
  email: '',
  phone: '',
  role: 'USER',
  status: true
})

// Delete dialog state
const deleteDialogVisible = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

// Computed
const filteredUsers = computed(() => {
  let users = usersList.value

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    users = users.filter(user =>
      user.username.toLowerCase().includes(keyword) ||
      (user.email && user.email.toLowerCase().includes(keyword)) ||
      (user.phone && user.phone.includes(keyword))
    )
  }

  if (roleFilter.value) {
    users = users.filter(user => user.role === roleFilter.value)
  }

  if (statusFilter.value !== '') {
    const isActive = statusFilter.value === 'true'
    users = users.filter(user => user.status === isActive)
  }

  return users
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / pageSize))

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredUsers.value.slice(start, end)
})

const adminCount = computed(() => usersList.value.filter(u => u.role === 'ADMIN').length)

const activeUsersCount = computed(() => usersList.value.filter(u => u.status).length)

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    }
  }

  return pages
})

// Methods
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await getUsersList({
      keyword: searchKeyword.value || undefined,
      role: roleFilter.value || undefined,
      status: statusFilter.value !== '' ? statusFilter.value === 'true' : undefined
    })
    if (response.code === 0) {
      usersList.value = response.data || []
    }
  } catch (error) {
    ElMessage.error('加载用户失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = debounce(() => {
  currentPage.value = 1
  fetchUsers()
}, 300)

const handleFilterChange = () => {
  currentPage.value = 1
  fetchUsers()
}

const clearSearch = () => {
  searchKeyword.value = ''
  currentPage.value = 1
  fetchUsers()
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page) => {
  if (typeof page === 'number') {
    currentPage.value = page
  }
}

const openCreateDialog = () => {
  isEditMode.value = false
  editingId.value = null
  formData.value = {
    username: '',
    password: '',
    email: '',
    phone: '',
    role: 'USER',
    status: true
  }
  dialogVisible.value = true
}

const openEditDialog = (user) => {
  isEditMode.value = true
  editingId.value = user.id
  formData.value = {
    username: user.username,
    password: '',
    email: user.email || '',
    phone: user.phone || '',
    role: user.role,
    status: user.status
  }
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
  setTimeout(() => {
    formData.value = {
      username: '',
      password: '',
      email: '',
      phone: '',
      role: 'USER',
      status: true
    }
  }, 300)
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (isEditMode.value) {
      await updateUser(editingId.value, {
        email: formData.value.email,
        phone: formData.value.phone || null,
        role: formData.value.role,
        status: formData.value.status
      })
      ElMessage.success('用户更新成功')
    } else {
      await register({
        username: formData.value.username,
        password: formData.value.password,
        email: formData.value.email,
        phone: formData.value.phone || null
      })
      ElMessage.success('用户创建成功')
    }
    closeDialog()
    await fetchUsers()
  } catch (error) {
    ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = (user) => {
  deleteTarget.value = user
  deleteDialogVisible.value = true
}

const closeDeleteDialog = () => {
  deleteDialogVisible.value = false
  deleteTarget.value = null
}

const confirmDelete = async () => {
  deleting.value = true
  try {
    await deleteUserById(deleteTarget.value.id)
    ElMessage.success('用户删除成功')
    closeDeleteDialog()
    await fetchUsers()
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    deleting.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
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
  fetchUsers()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

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

.users-manage-container {
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

.stat-badge.admin .stat-value {
  color: var(--accent-cyan);
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

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.users-table th {
  padding: 16px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table tbody tr {
  border-bottom: 1px solid var(--border-color);
  transition: background 0.15s;
}

.users-table tbody tr:hover {
  background: var(--bg-hover);
}

.users-table td {
  padding: 16px 20px;
  color: var(--text-primary);
  font-size: 14px;
}

.username-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-cyan) 0%, #06b6d4 100%);
  color: var(--bg-primary);
  font-size: 14px;
  font-weight: 600;
  border-radius: 10px;
  flex-shrink: 0;
}

.username-text {
  font-weight: 500;
}

.email-cell,
.phone-cell,
.date-cell {
  min-width: 160px;
}

.email-text,
.phone-text,
.date-text {
  color: var(--text-secondary);
  font-size: 13px;
}

.role-cell {
  min-width: 120px;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
}

.role-badge.admin {
  background: var(--accent-cyan-dim);
  border-color: rgba(34, 211, 238, 0.3);
  color: var(--accent-cyan);
}

.role-icon {
  width: 14px;
  height: 14px;
}

.status-cell {
  min-width: 120px;
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

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.pagination-info {
  color: var(--text-secondary);
  font-size: 13px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.page-btn:hover:not(:disabled) {
  background: var(--bg-hover);
  color: var(--text-primary);
  border-color: var(--text-muted);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-number {
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.page-number:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.page-number.active {
  background: var(--accent-cyan);
  color: var(--bg-primary);
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
  max-width: 500px;
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
  position: relative;
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

  .pagination-section {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
