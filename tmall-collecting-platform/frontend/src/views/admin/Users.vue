<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userApi } from '@/api'
import Pagination from '@/components/common/Pagination.vue'
import {
  User, UserFilled, Search, Plus, Refresh, Lock, Unlock,
  Delete, Tools, Filter, CircleCheck, CircleClose
} from '@element-plus/icons-vue'

// 数据状态
const users = ref([])
const loading = ref(false)
const total = ref(0)

// 搜索筛选
const searchForm = ref({
  search: '',
  role: '',
  status: ''
})

const showFilters = ref(false)

// 分页
const pagination = ref({
  page: 1,
  page_size: 20
})

// 对话框状态
const showPasswordDialog = ref(false)
const showEditDialog = ref(false)
const showConfirmDialog = ref(false)
const confirmConfig = ref({
  title: '',
  message: '',
  type: 'warning',
  onConfirm: null
})

const passwordForm = ref({
  userId: '',
  username: '',
  newPassword: ''
})
const editForm = ref({
  id: '',
  username: '',
  email: '',
  role: 'user'
})

// 加载数据
const loadUsers = async () => {
  try {
    loading.value = true
    const params = {
      ...pagination.value,
      ...searchForm.value
    }

    // 清理空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })

    const res = await userApi.getList(params)
    if (res.code === 0) {
      users.value = res.data || []
      total.value = res.total || 0
    }
  } catch (error) {
    ElMessage.error('加载用户数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.value.page = 1
  loadUsers()
}

// 重置筛选
const handleReset = () => {
  searchForm.value = {
    search: '',
    role: '',
    status: ''
  }
  pagination.value.page = 1
  loadUsers()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.value.page = page
  loadUsers()
}

const handlePageSizeChange = (size) => {
  pagination.value.page_size = size
  pagination.value.page = 1
  loadUsers()
}

// 确认操作
const handleConfirmAction = async () => {
  if (confirmConfig.value.onConfirm) {
    await confirmConfig.value.onConfirm()
  }
  showConfirmDialog.value = false
}

// 冻结/解冻用户
const handleToggleStatus = (user) => {
  const newStatus = user.status === 'active' ? 'frozen' : 'active'
  const actionText = newStatus === 'frozen' ? '冻结' : '解冻'

  confirmConfig.value = {
    title: `确认${actionText}`,
    message: `确定要${actionText}用户 "${user.username}" 吗？`,
    type: newStatus === 'frozen' ? 'warning' : 'info',
    onConfirm: async () => {
      try {
        const res = await userApi.updateStatus(user.id, newStatus)
        if (res.code === 0) {
          ElMessage.success(`${actionText}成功`)
          loadUsers()
        }
      } catch (error) {
        ElMessage.error(`${actionText}失败`)
      }
    }
  }
  showConfirmDialog.value = true
}

// 重置密码
const openPasswordDialog = (user) => {
  passwordForm.value = {
    userId: user.id,
    username: user.username,
    newPassword: ''
  }
  showPasswordDialog.value = true
}

const handleResetPassword = async () => {
  if (!passwordForm.value.newPassword) {
    ElMessage.warning('请输入新密码')
    return
  }

  if (passwordForm.value.newPassword.length < 6) {
    ElMessage.warning('密码长度不能少于6位')
    return
  }

  try {
    const res = await userApi.resetPassword(passwordForm.value.userId, passwordForm.value.newPassword)
    if (res.code === 0) {
      ElMessage.success('密码重置成功')
      showPasswordDialog.value = false
    }
  } catch (error) {
    ElMessage.error('密码重置失败')
  }
}

// 编辑用户
const openEditDialog = (user) => {
  editForm.value = {
    id: user.id,
    username: user.username,
    email: user.email || '',
    role: user.role
  }
  showEditDialog.value = true
}

const handleUpdateUser = async () => {
  try {
    const res = await userApi.update(editForm.value.id, {
      email: editForm.value.email,
      role: editForm.value.role
    })
    if (res.code === 0) {
      ElMessage.success('用户信息更新成功')
      showEditDialog.value = false
      loadUsers()
    }
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 删除用户
const handleDelete = (user) => {
  confirmConfig.value = {
    title: '确认删除',
    message: `确定要删除用户 "${user.username}" 吗？此操作不可恢复！`,
    type: 'danger',
    onConfirm: async () => {
      try {
        const res = await userApi.delete(user.id)
        if (res.code === 0) {
          ElMessage.success('删除成功')
          loadUsers()
        }
      } catch (error) {
        ElMessage.error('删除失败')
      }
    }
  }
  showConfirmDialog.value = true
}

// 新增用户
const openAddDialog = () => {
  editForm.value = {
    id: '',
    username: '',
    email: '',
    role: 'user'
  }
  showEditDialog.value = true
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  return new Date(timeStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 获取角色显示
const getRoleDisplay = (role) => {
  const roleMap = {
    'admin': { label: '管理员', color: '#FF6B35', bg: 'rgba(255, 107, 53, 0.15)' },
    'user': { label: '普通用户', color: '#9D4EDD', bg: 'rgba(157, 78, 221, 0.15)' }
  }
  return roleMap[role] || { label: role, color: '#888', bg: 'rgba(136, 136, 136, 0.15)' }
}

// 获取状态显示
const getStatusDisplay = (status) => {
  const statusMap = {
    'active': { label: '正常', icon: CircleCheck, color: '#06FFA5' },
    'frozen': { label: '已冻结', icon: CircleClose, color: '#FF6B6B' }
  }
  return statusMap[status] || { label: status, icon: CircleClose, color: '#888' }
}

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <div class="users-container">
    <!-- 头部操作区 -->
    <div class="header-section">
      <div class="header-left">
        <div class="header-title">
          <User class="title-icon" />
          <h2>用户管理</h2>
        </div>
        <div class="header-stats">
          <span class="stat">共 <strong>{{ total }}</strong> 位用户</span>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="openAddDialog">
          <Plus class="btn-icon" />
          <span>新增用户</span>
        </button>
        <button class="btn btn-secondary" @click="loadUsers">
          <Refresh class="btn-icon" :class="{ spinning: loading }" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <!-- 搜索筛选区 -->
    <div class="filter-section">
      <div class="filter-bar">
        <div class="search-input-wrapper">
          <Search class="search-icon" />
          <input
            v-model="searchForm.search"
            type="text"
            placeholder="搜索用户名或邮箱..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>

        <button
          class="filter-toggle"
          :class="{ active: showFilters || searchForm.role || searchForm.status }"
          @click="showFilters = !showFilters"
        >
          <Filter class="filter-icon" />
          <span>筛选</span>
        </button>

        <button class="btn btn-search" @click="handleSearch">
          <Search class="btn-icon" />
          <span>搜索</span>
        </button>

        <button class="btn btn-reset" @click="handleReset">
          <span>重置</span>
        </button>
      </div>

      <!-- 展开的筛选条件 -->
      <div v-if="showFilters" class="filter-panel">
        <div class="filter-row">
          <div class="filter-group">
            <label>角色</label>
            <select v-model="searchForm.role" class="filter-select">
              <option value="">全部</option>
              <option value="admin">管理员</option>
              <option value="user">普通用户</option>
            </select>
          </div>

          <div class="filter-group">
            <label>状态</label>
            <select v-model="searchForm.status" class="filter-select">
              <option value="">全部</option>
              <option value="active">正常</option>
              <option value="frozen">已冻结</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="table-section">
      <div class="table-container">
        <table class="user-table">
          <thead>
            <tr>
              <th class="col-user">用户</th>
              <th class="col-email">邮箱</th>
              <th class="col-role">角色</th>
              <th class="col-status">状态</th>
              <th class="col-time">注册时间</th>
              <th class="col-actions">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="users.length === 0 && !loading" class="empty-row">
              <td colspan="6">
                <div class="empty-state">
                  <User class="empty-icon" />
                  <p>暂无用户数据</p>
                  <small>点击"新增用户"按钮添加用户</small>
                </div>
              </td>
            </tr>
            <tr
              v-for="user in users"
              :key="user.id"
              class="user-row"
            >
              <td class="col-user">
                <div class="user-cell">
                  <div class="user-avatar">
                    <UserFilled v-if="!user.avatar" class="avatar-placeholder" />
                    <img v-else :src="user.avatar" :alt="user.username" />
                  </div>
                  <div class="user-info">
                    <h4 class="user-name">{{ user.username }}</h4>
                  </div>
                </div>
              </td>
              <td class="col-email">
                <span class="email-value">{{ user.email || '-' }}</span>
              </td>
              <td class="col-role">
                <span
                  class="role-badge"
                  :style="{
                    background: getRoleDisplay(user.role).bg,
                    color: getRoleDisplay(user.role).color
                  }"
                >
                  {{ getRoleDisplay(user.role).label }}
                </span>
              </td>
              <td class="col-status">
                <div class="status-indicator" :style="{ color: getStatusDisplay(user.status).color }">
                  <component :is="getStatusDisplay(user.status).icon" class="status-icon" />
                  <span>{{ getStatusDisplay(user.status).label }}</span>
                </div>
              </td>
              <td class="col-time">
                <span class="time-value">{{ formatTime(user.created_at) }}</span>
              </td>
              <td class="col-actions">
                <div class="action-buttons">
                  <button
                    class="action-btn"
                    :class="user.status === 'active' ? 'btn-freeze' : 'btn-unfreeze'"
                    :title="user.status === 'active' ? '冻结用户' : '解冻用户'"
                    @click="handleToggleStatus(user)"
                  >
                    <component :is="user.status === 'active' ? Lock : Unlock" class="action-icon" />
                  </button>
                  <button class="action-btn btn-password" title="重置密码" @click="openPasswordDialog(user)">
                    <Tools class="action-icon" />
                  </button>
                  <button class="action-btn btn-edit" title="编辑" @click="openEditDialog(user)">
                    <Tools class="action-icon" />
                  </button>
                  <button class="action-btn btn-delete" title="删除" @click="handleDelete(user)">
                    <Delete class="action-icon" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 加载中遮罩 -->
        <div v-if="loading" class="table-loading">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
        <Pagination
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="total"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </div>
    </div>

    <!-- 重置密码对话框 -->
    <div v-if="showPasswordDialog" class="dialog-overlay" @click.self="showPasswordDialog = false">
      <div class="dialog">
        <div class="dialog-header">
          <h3>重置密码</h3>
          <button class="dialog-close" @click="showPasswordDialog = false">×</button>
        </div>
        <div class="dialog-body">
          <p class="dialog-desc">为用户 <strong>{{ passwordForm.username }}</strong> 设置新密码</p>
          <div class="form-group">
            <label>新密码</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码（至少6位）"
              class="form-input"
            />
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="showPasswordDialog = false">取消</button>
          <button class="btn btn-primary" @click="handleResetPassword">确定</button>
        </div>
      </div>
    </div>

    <!-- 编辑用户对话框 -->
    <div v-if="showEditDialog" class="dialog-overlay" @click.self="showEditDialog = false">
      <div class="dialog">
        <div class="dialog-header">
          <h3>{{ editForm.id ? '编辑用户' : '新增用户' }}</h3>
          <button class="dialog-close" @click="showEditDialog = false">×</button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>用户名</label>
            <input
              v-model="editForm.username"
              type="text"
              placeholder="请输入用户名"
              class="form-input"
              :disabled="!!editForm.id"
            />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input
              v-model="editForm.email"
              type="email"
              placeholder="请输入邮箱"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="editForm.role" class="form-select">
              <option value="user">普通用户</option>
              <option value="admin">管理员</option>
            </select>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="showEditDialog = false">取消</button>
          <button class="btn btn-primary" @click="handleUpdateUser">确定</button>
        </div>
      </div>
    </div>

    <!-- 通用确认对话框 -->
    <div v-if="showConfirmDialog" class="dialog-overlay" @click.self="showConfirmDialog = false">
      <div class="dialog confirm-dialog">
        <div class="dialog-header">
          <h3>{{ confirmConfig.title }}</h3>
          <button class="dialog-close" @click="showConfirmDialog = false">×</button>
        </div>
        <div class="dialog-body">
          <div class="confirm-content">
            <div class="confirm-icon-wrapper" :class="confirmConfig.type">
              <component 
                :is="confirmConfig.type === 'danger' ? Delete : (confirmConfig.type === 'warning' ? Lock : User)" 
                class="confirm-icon" 
              />
            </div>
            <p class="confirm-message">{{ confirmConfig.message }}</p>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="showConfirmDialog = false">取消</button>
          <button 
            class="btn" 
            :class="confirmConfig.type === 'danger' ? 'btn-danger' : 'btn-primary'"
            @click="handleConfirmAction"
          >
            确定
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

.confirm-dialog {
  max-width: 400px;
}

.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  padding: 10px 0;
}

.confirm-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
}

.confirm-icon-wrapper.warning {
  background: rgba(255, 107, 53, 0.1);
  color: #FF6B35;
}

.confirm-icon-wrapper.danger {
  background: rgba(255, 59, 48, 0.1);
  color: #FF3B30;
}

.confirm-icon-wrapper.info {
  background: rgba(6, 255, 165, 0.1);
  color: #06FFA5;
}

.confirm-icon {
  width: 30px;
  height: 30px;
}

.confirm-message {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  line-height: 1.5;
}

.btn-danger {
  background: linear-gradient(135deg, #FF3B30, #FF6B6B);
  color: white;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 59, 48, 0.4);
}

.users-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 头部区域 */
.header-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-title .title-icon {
  width: 28px;
  height: 28px;
  color: #FF6B35;
}

.header-title h2 {
  font-size: 20px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 20px;
}

.header-stats .stat {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.header-stats .stat strong {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 按钮样式 */
.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.btn-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.btn-primary {
  background: linear-gradient(135deg, #FF6B35, #FF8C5A);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-search {
  background: linear-gradient(135deg, #7B2CBF, #9D4EDD);
  color: white;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(123, 44, 191, 0.4);
}

.btn-reset {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
}

.btn-reset:hover {
  border-color: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
}

/* 筛选区域 */
.filter-section {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.4);
}

.search-input {
  width: 100%;
  padding: 12px 14px 12px 44px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-family: 'Noto Sans SC', sans-serif;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.search-input:focus {
  outline: none;
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.filter-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.filter-toggle.active {
  background: rgba(255, 107, 53, 0.1);
  border-color: #FF6B35;
  color: #FF6B35;
}

.filter-icon {
  width: 16px;
  height: 16px;
}

.filter-panel {
  padding: 0 20px 20px;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-row {
  display: flex;
  gap: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.filter-group label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.filter-select,
.form-select {
  padding: 10px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23ffffff40' d='M2 4l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

.filter-select:focus,
.form-select:focus {
  outline: none;
  border-color: #FF6B35;
}

/* 表格区域 */
.table-section {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.table-container {
  position: relative;
  overflow-x: auto;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table thead {
  background: rgba(0, 0, 0, 0.3);
}

.user-table th {
  padding: 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.user-table tbody tr {
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  transition: all 0.2s ease;
}

.user-table tbody tr:hover {
  background: rgba(255, 107, 53, 0.03);
}

.user-table td {
  padding: 16px;
}

.col-user {
  min-width: 200px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.user-avatar {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, #7B2CBF, #FF6B35);
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.5);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.col-email {
  min-width: 200px;
}

.email-value {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.col-role {
  width: 120px;
}

.role-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.col-status {
  width: 120px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
}

.status-icon {
  width: 16px;
  height: 16px;
}

.col-time {
  width: 140px;
}

.time-value {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  font-family: 'JetBrains Mono', monospace;
}

.col-actions {
  width: 180px;
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 6px;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-icon {
  width: 16px;
  height: 16px;
}

.btn-freeze {
  background: rgba(255, 215, 0, 0.15);
  color: #FFD700;
}

.btn-freeze:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: scale(1.05);
}

.btn-unfreeze {
  background: rgba(6, 255, 165, 0.15);
  color: #06FFA5;
}

.btn-unfreeze:hover {
  background: rgba(6, 255, 165, 0.3);
  transform: scale(1.05);
}

.btn-password {
  background: rgba(123, 44, 191, 0.15);
  color: #9D4EDD;
}

.btn-password:hover {
  background: rgba(123, 44, 191, 0.3);
  transform: scale(1.05);
}

.btn-edit {
  background: rgba(255, 107, 53, 0.15);
  color: #FF6B35;
}

.btn-edit:hover {
  background: rgba(255, 107, 53, 0.3);
  transform: scale(1.05);
}

.btn-delete {
  background: rgba(255, 107, 107, 0.15);
  color: #FF6B6B;
}

.btn-delete:hover {
  background: rgba(255, 107, 107, 0.3);
  transform: scale(1.05);
}

/* 空状态 */
.empty-row td {
  padding: 80px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.3);
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  margin: 0 0 8px 0;
}

.empty-state small {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.2);
}

/* 加载遮罩 */
.table-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(15, 15, 26, 0.8);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #FF6B35;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.table-loading p {
  margin-top: 16px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

/* 分页 */
.pagination-section {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
}

/* 对话框 */
.dialog-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  z-index: 1000;
  padding: 20px;
}

.dialog {
  width: 100%;
  max-width: 480px;
  background: linear-gradient(135deg,
    rgba(30, 30, 46, 0.95) 0%,
    rgba(20, 20, 32, 0.98) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  animation: dialogIn 0.3s ease;
}

@keyframes dialogIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.dialog-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.dialog-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dialog-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.dialog-body {
  padding: 24px;
}

.dialog-desc {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0 0 20px 0;
}

.dialog-desc strong {
  color: #FF6B35;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 8px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-family: 'Noto Sans SC', sans-serif;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.dialog-footer .btn {
  min-width: 80px;
}

/* 响应式 */
@media (max-width: 1200px) {
  .filter-row {
    flex-direction: column;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .filter-bar {
    flex-wrap: wrap;
  }

  .search-input-wrapper {
    max-width: 100%;
    order: 1;
  }

  .filter-toggle {
    order: 2;
  }

  .btn-search,
  .btn-reset {
    order: 3;
  }

  .header-actions {
    flex-wrap: wrap;
  }

  .btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>
