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
    <!-- 顶部欢迎区 -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">用户管理</h1>
        <p class="header-subtitle">管理系统用户账户与权限配置</p>
      </div>
      <div class="header-actions">
        <button class="action-btn action-btn--primary" @click="openAddDialog">
          <Plus class="icon" />
          <span>新增用户</span>
        </button>
        <button class="action-btn action-btn--secondary" @click="loadUsers" :class="{ loading }">
          <Refresh class="icon" :class="{ spinning: loading }" />
          <span>刷新数据</span>
        </button>
      </div>
    </div>

    <!-- 统计指标卡片 -->
    <div class="metrics-grid">
      <div class="metric-card metric-card--orange" style="--i: 0">
        <div class="metric-header">
          <div class="metric-icon">
            <User class="icon" />
          </div>
          <span class="metric-badge">总计</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">用户总数</p>
          <p class="metric-value">{{ total }}</p>
        </div>
        <div class="metric-bg">👥</div>
      </div>

      <div class="metric-card metric-card--cyan" style="--i: 1">
        <div class="metric-header">
          <div class="metric-icon">
            <CircleCheck class="icon" />
          </div>
          <span class="metric-badge metric-badge--success">活跃</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">正常用户</p>
          <p class="metric-value">{{ users.filter(u => u.status === 'active').length }}</p>
        </div>
        <div class="metric-bg">✓</div>
      </div>

      <div class="metric-card metric-card--purple" style="--i: 2">
        <div class="metric-header">
          <div class="metric-icon">
            <Tools class="icon" />
          </div>
          <span class="metric-badge metric-badge--admin">管理</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">管理员</p>
          <p class="metric-value">{{ users.filter(u => u.role === 'admin').length }}</p>
        </div>
        <div class="metric-bg">🔧</div>
      </div>

      <div class="metric-card metric-card--gold" style="--i: 3">
        <div class="metric-header">
          <div class="metric-icon">
            <Lock class="icon" />
          </div>
          <span class="metric-badge metric-badge--warning">冻结</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">已冻结</p>
          <p class="metric-value">{{ users.filter(u => u.status === 'frozen').length }}</p>
        </div>
        <div class="metric-bg">🔒</div>
      </div>
    </div>

    <!-- 搜索筛选区 -->
    <div class="filter-panel" style="--i: 0">
      <div class="filter-header">
        <div class="filter-search">
          <Search class="search-icon" />
          <input
            v-model="searchForm.search"
            type="text"
            placeholder="搜索用户名或邮箱..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>
        <div class="filter-actions">
          <button
            class="filter-toggle"
            :class="{ active: showFilters || searchForm.role || searchForm.status }"
            @click="showFilters = !showFilters"
          >
            <Filter class="icon" />
            <span>筛选条件</span>
            <span v-if="searchForm.role || searchForm.status" class="filter-count">
              {{ [searchForm.role, searchForm.status].filter(Boolean).length }}
            </span>
          </button>
          <button class="filter-btn filter-btn--search" @click="handleSearch">
            <Search class="icon" />
          </button>
          <button class="filter-btn filter-btn--reset" @click="handleReset">
            <span>重置</span>
          </button>
        </div>
      </div>

      <!-- 展开的筛选条件 -->
      <div v-if="showFilters" class="filter-body">
        <div class="filter-group">
          <label class="filter-label">
            <UserFilled class="label-icon" />
            <span>用户角色</span>
          </label>
          <div class="filter-options">
            <button
              v-for="option in [{value: '', label: '全部'}, {value: 'admin', label: '管理员'}, {value: 'user', label: '普通用户'}]"
              :key="option.value"
              class="filter-option"
              :class="{ active: searchForm.role === option.value }"
              @click="searchForm.role = option.value"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <div class="filter-divider"></div>

        <div class="filter-group">
          <label class="filter-label">
            <CircleCheck class="label-icon" />
            <span>账户状态</span>
          </label>
          <div class="filter-options">
            <button
              v-for="option in [{value: '', label: '全部'}, {value: 'active', label: '正常'}, {value: 'frozen', label: '已冻结'}]"
              :key="option.value"
              class="filter-option"
              :class="{ active: searchForm.status === option.value }"
              @click="searchForm.status = option.value"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="users-panel" style="--i: 1">
      <div class="users-panel-header">
        <div class="panel-title-group">
          <div class="panel-icon-wrapper panel-icon-wrapper--orange">
            <UserFilled class="icon" />
          </div>
          <div>
            <h3 class="panel-title">用户列表</h3>
            <p class="panel-subtitle">管理系统中的所有用户账户</p>
          </div>
        </div>
        <div class="panel-badge">列表</div>
      </div>

      <div class="users-table-wrapper">
        <table class="users-table">
          <thead>
            <tr>
              <th class="col-user">用户信息</th>
              <th class="col-email">邮箱地址</th>
              <th class="col-role">角色权限</th>
              <th class="col-status">账户状态</th>
              <th class="col-time">注册时间</th>
              <th class="col-actions">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="users.length === 0 && !loading" class="empty-row">
              <td colspan="6">
                <div class="empty-state">
                  <div class="empty-icon-wrapper">
                    <User class="empty-icon" />
                  </div>
                  <p class="empty-title">暂无用户数据</p>
                  <p class="empty-desc">点击"新增用户"按钮添加第一个用户</p>
                </div>
              </td>
            </tr>
            <tr
              v-for="(user, index) in users"
              :key="user.id"
              class="user-row"
              :style="{ '--i': index }"
            >
              <td class="col-user">
                <div class="user-profile">
                  <div class="user-avatar" :class="`avatar-${user.role}`">
                    <UserFilled v-if="!user.avatar" class="avatar-icon" />
                    <img v-else :src="user.avatar" :alt="user.username" />
                  </div>
                  <div class="user-details">
                    <h4 class="user-name">{{ user.username }}</h4>
                    <span class="user-id">ID: {{ user.id }}</span>
                  </div>
                </div>
              </td>
              <td class="col-email">
                <span class="email-text">{{ user.email || '-' }}</span>
              </td>
              <td class="col-role">
                <span
                  class="role-tag"
                  :class="`role-tag--${user.role}`"
                >
                  {{ getRoleDisplay(user.role).label }}
                </span>
              </td>
              <td class="col-status">
                <div class="status-badge" :class="`status-badge--${user.status}`">
                  <div class="status-dot"></div>
                  <component :is="getStatusDisplay(user.status).icon" class="status-icon" />
                  <span>{{ getStatusDisplay(user.status).label }}</span>
                </div>
              </td>
              <td class="col-time">
                <span class="time-text">{{ formatTime(user.created_at) }}</span>
              </td>
              <td class="col-actions">
                <div class="row-actions">
                  <button
                    class="row-action-btn"
                    :class="user.status === 'active' ? 'row-action-btn--freeze' : 'row-action-btn--unfreeze'"
                    :title="user.status === 'active' ? '冻结用户' : '解冻用户'"
                    @click="handleToggleStatus(user)"
                  >
                    <component :is="user.status === 'active' ? Lock : Unlock" class="action-icon" />
                  </button>
                  <button
                    class="row-action-btn row-action-btn--password"
                    title="重置密码"
                    @click="openPasswordDialog(user)"
                  >
                    <Tools class="action-icon" />
                  </button>
                  <button
                    class="row-action-btn row-action-btn--edit"
                    title="编辑用户"
                    @click="openEditDialog(user)"
                  >
                    <Tools class="action-icon" />
                  </button>
                  <button
                    class="row-action-btn row-action-btn--delete"
                    title="删除用户"
                    @click="handleDelete(user)"
                  >
                    <Delete class="action-icon" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 加载中遮罩 -->
        <div v-if="loading" class="table-loading-overlay">
          <div class="loading-content">
            <div class="loading-spinner"></div>
            <p>正在加载用户数据...</p>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="users-pagination">
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
    <div v-if="showPasswordDialog" class="modal-overlay" @click.self="showPasswordDialog = false">
      <div class="modal-dialog modal-dialog--password">
        <div class="modal-header">
          <div class="modal-header-left">
            <div class="modal-icon-wrapper modal-icon-wrapper--password">
              <Tools class="modal-icon" />
            </div>
            <div>
              <h3 class="modal-title">重置密码</h3>
              <p class="modal-subtitle">为用户设置新的登录密码</p>
            </div>
          </div>
          <button class="modal-close" @click="showPasswordDialog = false">
            <span>✕</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="password-user-info">
            <div class="password-user-avatar">
              <UserFilled class="avatar-icon" />
            </div>
            <div class="password-user-details">
              <p class="password-user-label">目标用户</p>
              <p class="password-user-name">{{ passwordForm.username }}</p>
            </div>
          </div>
          <div class="form-field">
            <label class="form-label">
              <Lock class="label-icon" />
              <span>新密码</span>
            </label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码（至少6位）"
              class="form-input"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn--cancel" @click="showPasswordDialog = false">
            <span>取消</span>
          </button>
          <button class="modal-btn modal-btn--confirm" @click="handleResetPassword">
            <span>确认重置</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑/新增用户对话框 -->
    <div v-if="showEditDialog" class="modal-overlay" @click.self="showEditDialog = false">
      <div class="modal-dialog modal-dialog--user">
        <div class="modal-header">
          <div class="modal-header-left">
            <div class="modal-icon-wrapper" :class="editForm.id ? 'modal-icon-wrapper--edit' : 'modal-icon-wrapper--add'">
              <component :is="editForm.id ? Tools : Plus" class="modal-icon" />
            </div>
            <div>
              <h3 class="modal-title">{{ editForm.id ? '编辑用户' : '新增用户' }}</h3>
              <p class="modal-subtitle">{{ editForm.id ? '修改用户信息和权限' : '创建新的系统用户' }}</p>
            </div>
          </div>
          <button class="modal-close" @click="showEditDialog = false">
            <span>✕</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-field">
            <label class="form-label">
              <UserFilled class="label-icon" />
              <span>用户名</span>
            </label>
            <input
              v-model="editForm.username"
              type="text"
              placeholder="请输入用户名"
              class="form-input"
              :disabled="!!editForm.id"
            />
          </div>
          <div class="form-field">
            <label class="form-label">
              <span class="label-icon">@</span>
              <span>邮箱地址</span>
            </label>
            <input
              v-model="editForm.email"
              type="email"
              placeholder="请输入邮箱"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">
              <Tools class="label-icon" />
              <span>用户角色</span>
            </label>
            <div class="role-selector">
              <button
                v-for="role in [{value: 'user', label: '普通用户', icon: User}, {value: 'admin', label: '管理员', icon: Tools}]"
                :key="role.value"
                class="role-option"
                :class="{ active: editForm.role === role.value }"
                @click="editForm.role = role.value"
              >
                <component :is="role.icon" class="role-icon" />
                <span>{{ role.label }}</span>
                <div v-if="editForm.role === role.value" class="role-check">
                  <CircleCheck class="check-icon" />
                </div>
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn modal-btn--cancel" @click="showEditDialog = false">
            <span>取消</span>
          </button>
          <button class="modal-btn modal-btn--confirm" @click="handleUpdateUser">
            <span>{{ editForm.id ? '保存修改' : '创建用户' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 确认操作对话框 -->
    <div v-if="showConfirmDialog" class="modal-overlay" @click.self="showConfirmDialog = false">
      <div class="modal-dialog modal-dialog--confirm" :class="`modal-dialog--${confirmConfig.type}`">
        <div class="confirm-body">
          <div class="confirm-icon-wrapper" :class="`confirm-icon-wrapper--${confirmConfig.type}`">
            <component
              :is="confirmConfig.type === 'danger' ? Delete : (confirmConfig.type === 'warning' ? Lock : CircleCheck)"
              class="confirm-icon"
            />
          </div>
          <h3 class="confirm-title">{{ confirmConfig.title }}</h3>
          <p class="confirm-message">{{ confirmConfig.message }}</p>
        </div>
        <div class="modal-footer modal-footer--confirm">
          <button class="modal-btn modal-btn--cancel" @click="showConfirmDialog = false">
            <span>取消</span>
          </button>
          <button
            class="modal-btn modal-btn--confirm"
            :class="`modal-btn--${confirmConfig.type}`"
            @click="handleConfirmAction"
          >
            <span>确认操作</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.users-container {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
}

/* ============================================
   Dashboard Header
   ============================================ */
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  animation: fadeInDown 0.5s ease;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-content {
  flex: 1;
}

.header-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-btn .icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.action-btn .icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-orange), #FF8C5A);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.action-btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
}

.action-btn--secondary {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
}

.action-btn--secondary:hover {
  background: var(--bg-card-hover);
  border-color: var(--primary-orange);
  color: var(--primary-orange);
}

/* ============================================
   Metrics Grid
   ============================================ */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.metric-card {
  position: relative;
  padding: 24px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  animation: metricSlideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: calc(var(--i) * 0.1s);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes metricSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card--orange::before { background: linear-gradient(90deg, var(--primary-orange), transparent); }
.metric-card--purple::before { background: linear-gradient(90deg, var(--primary-purple), transparent); }
.metric-card--gold::before { background: linear-gradient(90deg, var(--primary-gold), transparent); }
.metric-card--cyan::before { background: linear-gradient(90deg, var(--primary-cyan), transparent); }

.metric-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-default);
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.metric-card--orange .metric-icon { background: rgba(255, 107, 53, 0.15); }
.metric-card--purple .metric-icon { background: rgba(123, 44, 191, 0.15); }
.metric-card--gold .metric-icon { background: rgba(255, 215, 0, 0.15); }
.metric-card--cyan .metric-icon { background: rgba(6, 255, 165, 0.15); }

.metric-icon .icon {
  width: 22px;
  height: 22px;
}

.metric-card--orange .metric-icon .icon { color: var(--primary-orange); }
.metric-card--purple .metric-icon .icon { color: var(--primary-purple); }
.metric-card--gold .metric-icon .icon { color: var(--primary-gold); }
.metric-card--cyan .metric-icon .icon { color: var(--primary-cyan); }

.metric-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  background: rgba(255, 107, 53, 0.1);
  color: var(--primary-orange);
  border: 1px solid rgba(255, 107, 53, 0.2);
}

.metric-badge--success {
  background: rgba(6, 255, 165, 0.1);
  color: var(--primary-cyan);
  border-color: rgba(6, 255, 165, 0.2);
}

.metric-badge--admin {
  background: rgba(123, 44, 191, 0.1);
  color: var(--primary-purple);
  border-color: rgba(123, 44, 191, 0.2);
}

.metric-badge--warning {
  background: rgba(255, 215, 0, 0.1);
  color: var(--primary-gold);
  border-color: rgba(255, 215, 0, 0.2);
}

.metric-body {
  position: relative;
  z-index: 1;
}

.metric-label {
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
  margin: 0 0 8px 0;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-card--orange .metric-value { color: var(--primary-orange); }
.metric-card--purple .metric-value { color: var(--primary-purple); }
.metric-card--gold .metric-value { color: var(--primary-gold); }
.metric-card--cyan .metric-value { color: var(--primary-cyan); }

.metric-bg {
  position: absolute;
  bottom: -8px;
  right: -8px;
  font-size: 72px;
  opacity: 0.04;
  pointer-events: none;
  filter: blur(1px);
}

/* ============================================
   Filter Panel
   ============================================ */
.filter-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(var(--i) * 0.1s + 0.2s);
}

@keyframes panelFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
}

.filter-search {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.filter-search .search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--text-tertiary);
  pointer-events: none;
}

.filter-search .search-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.filter-search .search-input::placeholder {
  color: var(--text-tertiary);
}

.filter-search .search-input:focus {
  outline: none;
  border-color: var(--primary-orange);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
}

.filter-toggle.active {
  background: rgba(255, 107, 53, 0.1);
  border-color: var(--primary-orange);
  color: var(--primary-orange);
}

.filter-toggle .icon {
  width: 16px;
  height: 16px;
}

.filter-toggle .filter-count {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: var(--primary-orange);
  color: white;
  font-size: 11px;
  font-weight: 700;
  border-radius: 10px;
}

.filter-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
}

.filter-btn--search {
  background: linear-gradient(135deg, var(--primary-purple), #9D4EDD);
  border: none;
  color: white;
}

.filter-btn--search:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(123, 44, 191, 0.4);
}

.filter-btn--search .icon {
  width: 18px;
  height: 18px;
}

.filter-btn--reset {
  padding: 0 16px;
  width: auto;
  color: var(--text-tertiary);
  font-size: 14px;
  font-weight: 600;
}

.filter-btn--reset:hover {
  border-color: var(--text-secondary);
  color: var(--text-secondary);
}

.filter-body {
  padding: 0 24px 20px;
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

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.filter-group:last-of-type {
  margin-bottom: 0;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.filter-label .label-icon {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

.filter-options {
  display: flex;
  gap: 10px;
}

.filter-option {
  padding: 10px 18px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-option:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
}

.filter-option.active {
  background: rgba(255, 107, 53, 0.15);
  border-color: var(--primary-orange);
  color: var(--primary-orange);
}

.filter-divider {
  height: 1px;
  background: var(--border-subtle);
  margin: 20px 0;
}

/* ============================================
   Users Panel
   ============================================ */
.users-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  animation: panelFadeIn 0.5s ease backwards;
  animation-delay: calc(var(--i) * 0.1s + 0.3s);
}

.users-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
}

.panel-title-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.panel-icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.panel-icon-wrapper--orange {
  background: rgba(255, 107, 53, 0.15);
}

.panel-icon-wrapper .icon {
  width: 18px;
  height: 18px;
}

.panel-icon-wrapper--orange .icon {
  color: var(--primary-orange);
}

.panel-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.panel-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.panel-badge {
  padding: 6px 14px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--primary-orange);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Users Table
   ============================================ */
.users-table-wrapper {
  position: relative;
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: rgba(0, 0, 0, 0.3);
}

.users-table th {
  padding: 16px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border-subtle);
}

.users-table tbody tr {
  border-bottom: 1px solid var(--border-subtle);
  transition: all 0.2s ease;
  animation: rowFadeIn 0.4s ease backwards;
  animation-delay: calc(var(--i) * 0.03s);
}

@keyframes rowFadeIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.users-table tbody tr:hover {
  background: rgba(255, 107, 53, 0.03);
}

.users-table td {
  padding: 16px 20px;
}

.col-user {
  min-width: 220px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 14px;
}

.user-avatar {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.user-avatar::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 14px;
  padding: 2px;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.5;
}

.user-avatar.avatar-admin {
  background: linear-gradient(135deg, var(--primary-purple), #9D4EDD);
}

.user-avatar.avatar-user {
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-gold));
}

.user-avatar .avatar-icon {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.7);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.user-id {
  font-size: 12px;
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
}

.col-email {
  min-width: 200px;
}

.email-text {
  font-size: 14px;
  color: var(--text-secondary);
}

.col-role {
  width: 140px;
}

.role-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.role-tag--admin {
  background: rgba(123, 44, 191, 0.15);
  color: var(--primary-purple);
  border: 1px solid rgba(123, 44, 191, 0.2);
}

.role-tag--user {
  background: rgba(255, 107, 53, 0.15);
  color: var(--primary-orange);
  border: 1px solid rgba(255, 107, 53, 0.2);
}

.col-status {
  width: 140px;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
}

.status-badge--active {
  background: rgba(6, 255, 165, 0.1);
  color: var(--primary-cyan);
  border: 1px solid rgba(6, 255, 165, 0.2);
}

.status-badge--active .status-dot {
  background: var(--primary-cyan);
  box-shadow: 0 0 8px var(--primary-cyan);
}

.status-badge--frozen {
  background: rgba(255, 215, 0, 0.1);
  color: var(--primary-gold);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.status-badge--frozen .status-dot {
  background: var(--primary-gold);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-badge .status-icon {
  width: 14px;
  height: 14px;
}

.col-time {
  width: 140px;
}

.time-text {
  font-size: 13px;
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
}

.col-actions {
  width: 180px;
  text-align: center;
}

.row-actions {
  display: flex;
  justify-content: center;
  gap: 6px;
}

.row-action-btn {
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

.row-action-btn .action-icon {
  width: 16px;
  height: 16px;
}

.row-action-btn--freeze {
  background: rgba(255, 215, 0, 0.15);
  color: var(--primary-gold);
}

.row-action-btn--freeze:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: scale(1.1);
}

.row-action-btn--unfreeze {
  background: rgba(6, 255, 165, 0.15);
  color: var(--primary-cyan);
}

.row-action-btn--unfreeze:hover {
  background: rgba(6, 255, 165, 0.3);
  transform: scale(1.1);
}

.row-action-btn--password {
  background: rgba(123, 44, 191, 0.15);
  color: var(--primary-purple);
}

.row-action-btn--password:hover {
  background: rgba(123, 44, 191, 0.3);
  transform: scale(1.1);
}

.row-action-btn--edit {
  background: rgba(255, 107, 53, 0.15);
  color: var(--primary-orange);
}

.row-action-btn--edit:hover {
  background: rgba(255, 107, 53, 0.3);
  transform: scale(1.1);
}

.row-action-btn--delete {
  background: rgba(255, 107, 107, 0.15);
  color: #FF6B6B;
}

.row-action-btn--delete:hover {
  background: rgba(255, 107, 107, 0.3);
  transform: scale(1.1);
}

/* Empty State */
.empty-row td {
  padding: 80px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
}

.empty-icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 53, 0.05);
  border-radius: 20px;
  margin-bottom: 20px;
}

.empty-icon {
  width: 40px;
  height: 40px;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-desc {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

/* Loading Overlay */
.table-loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(13, 13, 20, 0.8);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--primary-orange);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-content p {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* Pagination */
.users-pagination {
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  justify-content: center;
}

/* ============================================
   Modal Dialog
   ============================================ */
.modal-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-dialog {
  width: 100%;
  max-width: 480px;
  background: linear-gradient(135deg, rgba(30, 30, 46, 0.95), rgba(20, 20, 32, 0.98));
  border: 1px solid var(--border-default);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  animation: modalIn 0.3s ease;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.modal-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.modal-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.modal-icon-wrapper--add {
  background: rgba(6, 255, 165, 0.15);
}

.modal-icon-wrapper--add .modal-icon {
  color: var(--primary-cyan);
}

.modal-icon-wrapper--edit {
  background: rgba(255, 107, 53, 0.15);
}

.modal-icon-wrapper--edit .modal-icon {
  color: var(--primary-orange);
}

.modal-icon-wrapper--password {
  background: rgba(123, 44, 191, 0.15);
}

.modal-icon-wrapper--password .modal-icon {
  color: var(--primary-purple);
}

.modal-icon {
  width: 20px;
  height: 20px;
}

.modal-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.modal-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 8px;
  color: var(--text-tertiary);
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.modal-body {
  padding: 24px;
}

.password-user-info {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 14px;
  margin-bottom: 20px;
}

.password-user-avatar {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-orange));
  border-radius: 12px;
}

.password-user-avatar .avatar-icon {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.7);
}

.password-user-details {
  flex: 1;
}

.password-user-label {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0 0 4px 0;
}

.password-user-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--primary-orange);
  margin: 0;
}

.form-field {
  margin-bottom: 16px;
}

.form-field:last-child {
  margin-bottom: 0;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.form-label .label-icon {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: var(--text-tertiary);
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-orange);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.role-selector {
  display: flex;
  gap: 12px;
}

.role-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.role-option:hover {
  background: rgba(255, 255, 255, 0.03);
  border-color: var(--border-default);
}

.role-option.active {
  background: rgba(255, 107, 53, 0.08);
  border-color: var(--primary-orange);
}

.role-option .role-icon {
  width: 24px;
  height: 24px;
  color: var(--text-tertiary);
  transition: color 0.3s ease;
}

.role-option.active .role-icon {
  color: var(--primary-orange);
}

.role-option span {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.role-option.active span {
  color: var(--primary-orange);
}

.role-check {
  position: absolute;
  top: 8px;
  right: 8px;
}

.role-check .check-icon {
  width: 16px;
  height: 16px;
  color: var(--primary-orange);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
}

.modal-footer--confirm {
  justify-content: center;
  padding: 0 24px 24px;
  border-top: none;
}

.modal-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  min-width: 100px;
}

.modal-btn--cancel {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
}

.modal-btn--cancel:hover {
  background: rgba(255, 255, 255, 0.1);
}

.modal-btn--confirm {
  background: linear-gradient(135deg, var(--primary-orange), #FF8C5A);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.modal-btn--confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
}

.modal-btn--warning {
  background: linear-gradient(135deg, var(--primary-gold), #FFA500);
  color: #1a1a1a;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.modal-btn--warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
}

.modal-btn--danger {
  background: linear-gradient(135deg, #FF3B30, #FF6B6B);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 59, 48, 0.3);
}

.modal-btn--danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 59, 48, 0.4);
}

/* Confirm Dialog */
.modal-dialog--confirm {
  max-width: 420px;
}

.modal-dialog--confirm .modal-header {
  display: none;
}

.confirm-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 32px 24px;
}

.confirm-icon-wrapper {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 20px;
}

.confirm-icon-wrapper--warning {
  background: rgba(255, 215, 0, 0.15);
  border: 2px solid rgba(255, 215, 0, 0.3);
}

.confirm-icon-wrapper--warning .confirm-icon {
  color: var(--primary-gold);
}

.confirm-icon-wrapper--danger {
  background: rgba(255, 59, 48, 0.15);
  border: 2px solid rgba(255, 59, 48, 0.3);
}

.confirm-icon-wrapper--danger .confirm-icon {
  color: #FF3B30;
}

.confirm-icon-wrapper--info {
  background: rgba(6, 255, 165, 0.15);
  border: 2px solid rgba(6, 255, 165, 0.3);
}

.confirm-icon-wrapper--info .confirm-icon {
  color: var(--primary-cyan);
}

.confirm-icon {
  width: 36px;
  height: 36px;
}

.confirm-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.confirm-message {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1400px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .dashboard-header {
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
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .filter-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-search {
    max-width: 100%;
  }

  .filter-actions {
    justify-content: space-between;
  }

  .filter-toggle {
    flex: 1;
    justify-content: center;
  }

  .filter-options {
    flex-wrap: wrap;
  }

  .users-table {
    font-size: 14px;
  }

  .users-table th,
  .users-table td {
    padding: 12px 16px;
  }

  .role-selector {
    flex-direction: column;
  }

  .modal-dialog {
    max-width: 100%;
    margin: 20px;
  }
}
</style>
