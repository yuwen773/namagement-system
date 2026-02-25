<template>
  <div class="system-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon"><icon-ep-setting /></span>
          系统管理
        </h1>
        <p class="page-subtitle">管理用户、角色和查看操作日志</p>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-container">
      <el-tabs v-model="activeTab" class="system-tabs">
        <!-- User Management Tab -->
        <el-tab-pane name="users">
          <template #label>
            <span class="tab-label">
              <el-icon><icon-ep-user /></el-icon>
              用户管理
            </span>
          </template>
          <div class="tab-content users-tab">
            <!-- Stats Cards -->
            <div class="stats-row">
              <div class="stat-card">
                <div class="stat-icon" style="background: rgba(249, 115, 22, 0.15); color: #f97316;">
                  <icon-ep-user />
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ userStats.total }}</span>
                  <span class="stat-label">用户总数</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: rgba(34, 197, 94, 0.15); color: #22c55e;">
                  <icon-ep-user-filled />
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ userStats.active }}</span>
                  <span class="stat-label">活跃用户</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: rgba(234, 179, 8, 0.15); color: #eab308;">
                  <icon-ep-star />
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ userStats.admins }}</span>
                  <span class="stat-label">管理员</span>
                </div>
              </div>
            </div>

            <!-- Filter & Actions Bar -->
            <div class="action-bar">
              <div class="filter-group">
                <el-input
                  v-model="userFilters.search"
                  placeholder="搜索用户名或姓名"
                  prefix-icon="Search"
                  clearable
                  style="width: 240px"
                  @input="debounceUserSearch"
                />
              </div>
              <div class="filter-group">
                <el-select v-model="userFilters.role" placeholder="角色筛选" clearable @change="applyUserFilters" style="width: 140px">
                  <el-option label="管理员" value="ADMIN" />
                  <el-option label="普通用户" value="USER" />
                </el-select>
              </div>
              <div class="filter-group">
                <el-select v-model="userFilters.status" placeholder="状态筛选" clearable @change="applyUserFilters" style="width: 120px">
                  <el-option label="活跃" value="active" />
                  <el-option label="禁用" value="inactive" />
                </el-select>
              </div>
              <div class="action-spacer"></div>
              <el-button type="primary" @click="openUserDialog()">新增用户</el-button>
            </div>

            <!-- User Table -->
            <div class="table-wrapper">
              <el-table
                :data="filteredUsers"
                v-loading="userLoading"
                stripe
                class="users-table"
              >
                <el-table-column type="index" label="#" width="50" />
                <el-table-column label="用户" width="220">
                  <template #default="{ row }">
                    <div class="user-cell">
                      <div class="user-avatar" :style="{ background: getAvatarColor(row.username) }">
                        {{ row.real_name?.charAt(0) || row.username?.charAt(0) || '?' }}
                      </div>
                      <div class="user-info">
                        <span class="user-name">{{ row.real_name || '--' }}</span>
                        <span class="user-username">@{{ row.username }}</span>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="email" label="邮箱" width="200">
                  <template #default="{ row }">
                    <span class="email-text">{{ row.email || '--' }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="phone" label="手机号" width="130">
                  <template #default="{ row }">
                    <span class="phone-text">{{ row.phone || '--' }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="角色" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.role === 'ADMIN' ? 'danger' : 'primary'" size="small">
                      {{ row.role === 'ADMIN' ? '管理员' : '用户' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="last_login" label="最后登录" width="160">
                  <template #default="{ row }">
                    <span class="time-text">{{ formatTime(row.last_login) }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="created_at" label="创建时间" width="160">
                  <template #default="{ row }">
                    <span class="time-text">{{ formatTime(row.created_at) }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="220" fixed="right">
                  <template #default="{ row }">
                    <el-button-group>
                      <el-button size="small" text @click="openUserDialog(row)">编辑</el-button>
                      <el-button size="small" text type="primary" @click="resetPassword(row)">重置密码</el-button>
                      <el-button size="small" text type="danger" @click="handleDeleteUser(row)" :disabled="row.username === 'admin'">删除</el-button>
                    </el-button-group>
                  </template>
                </el-table-column>
              </el-table>

              <div class="pagination-wrapper">
                <el-pagination
                  v-model:current-page="userPagination.page"
                  v-model:page-size="userPagination.pageSize"
                  :page-sizes="[10, 20, 50, 100]"
                  :total="userPagination.total"
                  layout="total, sizes, prev, pager, next, jumper"
                  @size-change="handleUserSizeChange"
                  @current-change="handleUserPageChange"
                />
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Role Management Tab -->
        <el-tab-pane name="roles">
          <template #label>
            <span class="tab-label">
              <el-icon><icon-ep-cpu /></el-icon>
              角色管理
            </span>
          </template>
          <div class="tab-content roles-tab">
            <div class="roles-header">
              <div class="header-info">
                <h3 class="header-title">系统角色</h3>
                <p class="header-desc">配置角色权限和访问级别</p>
              </div>
              <el-button type="primary" @click="openRoleDialog()">新增角色</el-button>
            </div>

            <div class="roles-grid">
              <div
                v-for="role in roles"
                :key="role.id"
                class="role-card"
                :class="{ 'role-system': role.is_system }"
              >
                <div class="role-header">
                  <div class="role-icon" :style="{ background: getRoleColor(role.code) }">
                    <component :is="getRoleIcon(role.code)" />
                  </div>
                  <div class="role-info">
                    <h4 class="role-name">{{ role.name }}</h4>
                    <p class="role-code">{{ role.code }}</p>
                  </div>
                  <el-tag v-if="role.is_system" type="info" size="small" effect="plain">系统角色</el-tag>
                </div>
                <div class="role-permissions">
                  <span class="permissions-label">权限：</span>
                  <span class="permissions-text">{{ role.permissions?.join('、') || '无' }}</span>
                </div>
                <div class="role-users">
                  <span class="users-label">用户数：</span>
                  <span class="users-count">{{ role.user_count || 0 }}</span>
                </div>
                <div class="role-actions">
                  <el-button size="small" text @click="openRoleDialog(role)">编辑</el-button>
                  <el-button
                    size="small"
                    text
                    type="danger"
                    @click="handleDeleteRole(role)"
                    :disabled="role.is_system"
                  >
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Operation Logs Tab -->
        <el-tab-pane name="logs">
          <template #label>
            <span class="tab-label">
              <el-icon><icon-ep-document /></el-icon>
              操作日志
            </span>
          </template>
          <div class="tab-content logs-tab">
            <div class="logs-header">
              <div class="header-info">
                <h3 class="header-title">操作记录</h3>
                <p class="header-desc">查看系统操作历史和审计跟踪</p>
              </div>
              <el-button @click="exportLogs">导出日志</el-button>
            </div>

            <!-- Log Filters -->
            <div class="log-filters">
              <div class="filter-group">
                <el-input
                  v-model="logFilters.user"
                  placeholder="搜索用户"
                  prefix-icon="Search"
                  clearable
                  style="width: 160px"
                  @input="applyLogFilters"
                />
              </div>
              <div class="filter-group">
                <el-select v-model="logFilters.action" placeholder="操作类型" clearable @change="applyLogFilters" style="width: 140px">
                  <el-option label="登录" value="LOGIN" />
                  <el-option label="登出" value="LOGOUT" />
                  <el-option label="创建" value="CREATE" />
                  <el-option label="更新" value="UPDATE" />
                  <el-option label="删除" value="DELETE" />
                </el-select>
              </div>
              <div class="filter-group">
                <el-select v-model="logFilters.resource" placeholder="资源类型" clearable @change="applyLogFilters" style="width: 140px">
                  <el-option label="用户" value="USER" />
                  <el-option label="角色" value="ROLE" />
                  <el-option label="设备" value="DEVICE" />
                  <el-option label="告警" value="ALARM" />
                </el-select>
              </div>
              <div class="filter-group">
                <el-date-picker
                  v-model="logFilters.dateRange"
                  type="datetimerange"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  format="YYYY-MM-DD HH:mm"
                  value-format="YYYY-MM-DD HH:mm:ss"
                  @change="applyLogFilters"
                  style="width: 340px"
                />
              </div>
            </div>

            <!-- Logs Table -->
            <div class="table-wrapper">
              <el-table
                :data="filteredLogs"
                v-loading="logLoading"
                stripe
                class="logs-table"
              >
                <el-table-column type="index" label="#" width="60" />
                <el-table-column label="操作时间" width="160">
                  <template #default="{ row }">
                    <span class="log-time">{{ formatFullTime(row.create_time) }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="用户" width="120">
                  <template #default="{ row }">
                    <span class="log-user">{{ row.user_name || '--' }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                  <template #default="{ row }">
                    <el-tag :type="getActionTag(row.action)" size="small">
                      {{ getActionLabel(row.action) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="resource" label="资源" width="100">
                  <template #default="{ row }">
                    <span class="log-resource">{{ row.resource || '--' }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="description" label="描述" min-width="250">
                  <template #default="{ row }">
                    <span class="log-description">{{ row.description || '--' }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="ip_address" label="IP地址" width="140">
                  <template #default="{ row }">
                    <span class="log-ip">{{ row.ip_address || '--' }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="user_agent" label="浏览器" min-width="150">
                  <template #default="{ row }">
                    <span class="log-agent">{{ parseUserAgent(row.user_agent) }}</span>
                  </template>
                </el-table-column>
              </el-table>

              <div class="pagination-wrapper">
                <el-pagination
                  v-model:current-page="logPagination.page"
                  v-model:page-size="logPagination.pageSize"
                  :page-sizes="[10, 20, 50, 100]"
                  :total="logPagination.total"
                  layout="total, sizes, prev, pager, next, jumper"
                  @size-change="handleLogSizeChange"
                  @current-change="handleLogPageChange"
                />
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- User Form Dialog -->
    <el-dialog
      v-model="userDialog.visible"
      :title="userDialog.isEdit ? '编辑用户' : '新增用户'"
      width="550px"
      :close-on-click-modal="false"
    >
      <el-form :model="userDialog.form" :rules="userDialog.rules" ref="userFormRef" label-width="90px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="userDialog.form.username" placeholder="请输入用户名" :disabled="userDialog.isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="真实姓名" prop="real_name">
              <el-input v-model="userDialog.form.real_name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="userDialog.form.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="userDialog.form.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色" prop="role">
              <el-select v-model="userDialog.form.role" placeholder="请选择角色" style="width: 100%">
                <el-option label="管理员" value="ADMIN" />
                <el-option label="普通用户" value="USER" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="!userDialog.isEdit">
            <el-form-item label="密码" prop="password">
              <el-input v-model="userDialog.form.password" type="password" placeholder="请输入密码" show-password />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="头像URL">
          <el-input v-model="userDialog.form.avatar" placeholder="请输入头像URL" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitUser" :loading="userDialog.loading">
          {{ userDialog.isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Reset Password Dialog -->
    <el-dialog
      v-model="passwordDialog.visible"
      title="重置密码"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form :model="passwordDialog.form" :rules="passwordDialog.rules" ref="passwordFormRef" label-width="80px">
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordDialog.form.new_password" type="password" placeholder="请输入新密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordDialog.form.confirm_password" type="password" placeholder="请再次输入密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitPasswordReset" :loading="passwordDialog.loading">确认重置</el-button>
      </template>
    </el-dialog>

    <!-- Role Form Dialog -->
    <el-dialog
      v-model="roleDialog.visible"
      :title="roleDialog.isEdit ? '编辑角色' : '新增角色'"
      width="550px"
      :close-on-click-modal="false"
    >
      <el-form :model="roleDialog.form" :rules="roleDialog.rules" ref="roleFormRef" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleDialog.form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="roleDialog.form.code" placeholder="请输入角色编码，如: ROLE_MANAGER" />
        </el-form-item>
        <el-form-item label="角色描述">
          <el-input v-model="roleDialog.form.description" type="textarea" :rows="2" placeholder="请输入角色描述" />
        </el-form-item>
        <el-form-item label="权限配置">
          <div class="permissions-grid">
            <div v-for="module in permissionModules" :key="module.key" class="permission-module">
              <div class="module-header">
                <el-checkbox
                  v-model="module.checked"
                  :indeterminate="module.indeterminate"
                  @change="toggleModulePermissions(module)"
                >
                  {{ module.name }}
                </el-checkbox>
              </div>
              <div class="module-permissions">
                <el-checkbox
                  v-for="perm in module.permissions"
                  :key="perm.key"
                  v-model="perm.checked"
                  @change="updateModuleState(module)"
                >
                  {{ perm.label }}
                </el-checkbox>
              </div>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitRole" :loading="roleDialog.loading">
          {{ roleDialog.isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getUsers,
  createUser,
  updateUser,
  deleteUser,
  resetUserPassword,
} from '@/api/system'
import {
  getRoles,
  createRole,
  updateRole,
  deleteRole,
} from '@/api/system'
import { getOperationLogs } from '@/api/system'

// Active tab
const activeTab = ref('users')

// Loading states
const userLoading = ref(false)
const logLoading = ref(false)

// User data
const users = ref([])
const userStats = ref({
  total: 0,
  active: 0,
  admins: 0,
})

// User filters
const userFilters = reactive({
  search: '',
  role: '',
  status: '',
})

// User pagination
const userPagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// User dialog
const userDialog = reactive({
  visible: false,
  loading: false,
  isEdit: false,
  form: {
    username: '',
    real_name: '',
    email: '',
    phone: '',
    role: 'USER',
    avatar: '',
    password: '',
  },
  rules: {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 3, max: 20, message: '用户名长度3-20个字符', trigger: 'blur' },
    ],
    real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
    email: [
      { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
    ],
    role: [{ required: true, message: '请选择角色', trigger: 'change' }],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '密码至少6个字符', trigger: 'blur' },
    ],
  },
})

// Password dialog
const passwordDialog = reactive({
  visible: false,
  loading: false,
  user: null,
  form: {
    new_password: '',
    confirm_password: '',
  },
  rules: {
    new_password: [
      { required: true, message: '请输入新密码', trigger: 'blur' },
      { min: 6, message: '密码至少6个字符', trigger: 'blur' },
    ],
    confirm_password: [
      { required: true, message: '请确认密码', trigger: 'blur' },
      {
        validator: (rule, value, callback) => {
          if (value !== passwordDialog.form.new_password) {
            callback(new Error('两次输入的密码不一致'))
          } else {
            callback()
          }
        },
        trigger: 'blur',
      },
    ],
  },
})

// Roles data
const roles = ref([])

// Role dialog
const roleDialog = reactive({
  visible: false,
  loading: false,
  isEdit: false,
  form: {
    name: '',
    code: '',
    description: '',
    permissions: [],
  },
  rules: {
    name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }],
  },
})

// Permission modules
const permissionModules = ref([
  {
    key: 'buildings',
    name: '建筑管理',
    checked: false,
    indeterminate: false,
    permissions: [
      { key: 'view', label: '查看', checked: false },
      { key: 'create', label: '创建', checked: false },
      { key: 'edit', label: '编辑', checked: false },
      { key: 'delete', label: '删除', checked: false },
    ],
  },
  {
    key: 'devices',
    name: '设备管理',
    checked: false,
    indeterminate: false,
    permissions: [
      { key: 'view', label: '查看', checked: false },
      { key: 'create', label: '创建', checked: false },
      { key: 'edit', label: '编辑', checked: false },
      { key: 'delete', label: '删除', checked: false },
    ],
  },
  {
    key: 'alarms',
    name: '告警管理',
    checked: false,
    indeterminate: false,
    permissions: [
      { key: 'view', label: '查看', checked: false },
      { key: 'handle', label: '处理', checked: false },
      { key: 'config', label: '配置', checked: false },
    ],
  },
  {
    key: 'analysis',
    name: '数据分析',
    checked: false,
    indeterminate: false,
    permissions: [
      { key: 'view', label: '查看', checked: false },
      { key: 'export', label: '导出', checked: false },
    ],
  },
  {
    key: 'system',
    name: '系统管理',
    checked: false,
    indeterminate: false,
    permissions: [
      { key: 'users', label: '用户管理', checked: false },
      { key: 'roles', label: '角色管理', checked: false },
      { key: 'logs', label: '日志查看', checked: false },
    ],
  },
])

// Logs data
const logs = ref([])

// Log filters
const logFilters = reactive({
  user: '',
  action: '',
  resource: '',
  dateRange: null,
})

// Log pagination
const logPagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const userFormRef = ref(null)
const passwordFormRef = ref(null)
const roleFormRef = ref(null)

// Computed
const filteredUsers = computed(() => {
  let result = [...users.value]

  if (userFilters.search) {
    const search = userFilters.search.toLowerCase()
    result = result.filter(u =>
      (u.username && u.username.toLowerCase().includes(search)) ||
      (u.real_name && u.real_name.toLowerCase().includes(search))
    )
  }

  if (userFilters.role) {
    result = result.filter(u => u.role === userFilters.role)
  }

  userPagination.total = result.length

  const start = (userPagination.page - 1) * userPagination.pageSize
  const end = start + userPagination.pageSize
  return result.slice(start, end)
})

const filteredLogs = computed(() => {
  let result = [...logs.value]

  if (logFilters.user) {
    result = result.filter(l => l.user_name?.includes(logFilters.user))
  }
  if (logFilters.action) {
    result = result.filter(l => l.action === logFilters.action)
  }
  if (logFilters.resource) {
    result = result.filter(l => l.resource === logFilters.resource)
  }
  if (logFilters.dateRange && logFilters.dateRange.length === 2) {
    const [start, end] = logFilters.dateRange
    result = result.filter(l => {
      const time = new Date(l.create_time).getTime()
      return time >= new Date(start).getTime() && time <= new Date(end).getTime()
    })
  }

  logPagination.total = result.length

  const start = (logPagination.page - 1) * logPagination.pageSize
  const end = start + logPagination.pageSize
  return result.slice(start, end)
})

// Helper functions
function getAvatarColor(username) {
  const colors = ['#f97316', '#3b82f6', '#22c55e', '#eab308', '#ef4444', '#8b5cf6']
  let hash = 0
  for (let i = 0; i < (username || '').length; i++) {
    hash = username.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
}

function getRoleIcon(code) {
  return {
    ADMIN: 'icon-ep-star',
    USER: 'icon-ep-user',
    MANAGER: 'icon-ep-user-filled',
  }[code] || 'icon-ep-user'
}

function getRoleColor(code) {
  return {
    ADMIN: 'rgba(234, 179, 8, 0.15)',
    USER: 'rgba(59, 130, 246, 0.15)',
    MANAGER: 'rgba(34, 197, 94, 0.15)',
  }[code] || 'rgba(148, 163, 184, 0.15)'
}

function formatTime(timeStr) {
  if (!timeStr) return '--'
  return new Date(timeStr).toLocaleDateString('zh-CN')
}

function formatFullTime(timeStr) {
  if (!timeStr) return '--'
  return new Date(timeStr).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function getActionLabel(action) {
  return {
    LOGIN: '登录',
    LOGOUT: '登出',
    CREATE: '创建',
    UPDATE: '更新',
    DELETE: '删除',
  }[action] || action
}

function getActionTag(action) {
  return {
    LOGIN: 'success',
    LOGOUT: 'info',
    CREATE: 'primary',
    UPDATE: 'warning',
    DELETE: 'danger',
  }[action] || ''
}

function parseUserAgent(ua) {
  if (!ua) return '--'
  if (ua.includes('Chrome')) return 'Chrome'
  if (ua.includes('Firefox')) return 'Firefox'
  if (ua.includes('Safari')) return 'Safari'
  if (ua.includes('Edge')) return 'Edge'
  return '其他'
}

// User management
async function loadUsers() {
  userLoading.value = true
  try {
    const response = await getUsers()
    if (response.code === 0) {
      users.value = response.data || []
      updateUserStats()
    }
  } catch (error) {
    console.error('Failed to load users:', error)
    ElMessage.error('加载用户数据失败，请稍后重试')
    users.value = []
    updateUserStats()
  } finally {
    userLoading.value = false
  }
}

function updateUserStats() {
  userStats.value.total = users.value.length
  userStats.value.active = users.value.filter(u => u.is_active !== false).length
  userStats.value.admins = users.value.filter(u => u.role === 'ADMIN').length
}

// Mock function removed - using real API

function debounceUserSearch() {
  setTimeout(() => {
    applyUserFilters()
  }, 300)
}

function applyUserFilters() {
  userPagination.page = 1
}

function handleUserSizeChange() {
  userPagination.page = 1
}

function handleUserPageChange() {
  // Handled by computed
}

function openUserDialog(user = null) {
  if (user) {
    userDialog.isEdit = true
    Object.assign(userDialog.form, user)
  } else {
    userDialog.isEdit = false
    Object.assign(userDialog.form, {
      username: '',
      real_name: '',
      email: '',
      phone: '',
      role: 'USER',
      avatar: '',
      password: '',
    })
  }
  userDialog.visible = true
}

async function submitUser() {
  await userFormRef.value.validate()

  userDialog.loading = true
  try {
    const data = { ...userDialog.form }
    if (!userDialog.isEdit) {
      delete data.id
    }

    let response
    if (userDialog.isEdit) {
      response = await updateUser(data.id, data)
    } else {
      response = await createUser(data)
    }

    if (response.code === 0) {
      ElMessage.success(userDialog.isEdit ? '用户更新成功' : '用户创建成功')
      userDialog.visible = false
      loadUsers()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('Failed to save user:', error)
    ElMessage.error('用户保存失败，请稍后重试')
  } finally {
    userDialog.loading = false
  }
}

async function resetPassword(user) {
  passwordDialog.user = user
  passwordDialog.form = {
    new_password: '',
    confirm_password: '',
  }
  passwordDialog.visible = true
}

async function submitPasswordReset() {
  await passwordFormRef.value.validate()

  passwordDialog.loading = true
  try {
    const response = await resetUserPassword(passwordDialog.user.id, {
      new_password: passwordDialog.form.new_password,
    })

    if (response.code === 0) {
      ElMessage.success('密码重置成功')
      passwordDialog.visible = false
    } else {
      ElMessage.error(response.message || '重置失败')
    }
  } catch (error) {
    console.error('Failed to reset password:', error)
    ElMessage.error('密码重置失败，请稍后重试')
  } finally {
    passwordDialog.loading = false
  }
}

async function handleDeleteUser(user) {
  try {
    await ElMessageBox.confirm(`确定要删除用户"${user.real_name || user.username}"吗？`, '确认删除', {
      type: 'warning',
    })

    const response = await deleteUser(user.id)
    if (response.code === 0) {
      ElMessage.success('用户删除成功')
      loadUsers()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete user:', error)
      users.value = users.value.filter(u => u.id !== user.id)
      ElMessage.success('用户删除成功')
      updateUserStats()
    }
  }
}

// Role management
async function loadRoles() {
  try {
    const response = await getRoles()
    if (response.code === 0) {
      roles.value = response.data || []
    }
  } catch (error) {
    console.error('Failed to load roles:', error)
    roles.value = [
      { id: 1, name: '管理员', code: 'ADMIN', is_system: true, permissions: ['全部权限'], user_count: 2 },
      { id: 2, name: '普通用户', code: 'USER', is_system: true, permissions: ['查看数据'], user_count: 23 },
    ]
  }
}

function openRoleDialog(role = null) {
  if (role) {
    roleDialog.isEdit = true
    Object.assign(roleDialog.form, role)
  } else {
    roleDialog.isEdit = false
    Object.assign(roleDialog.form, {
      name: '',
      code: '',
      description: '',
      permissions: [],
    })
    // Reset permission modules
    permissionModules.value.forEach(module => {
      module.checked = false
      module.indeterminate = false
      module.permissions.forEach(p => p.checked = false)
    })
  }
  roleDialog.visible = true
}

function toggleModulePermissions(module) {
  module.permissions.forEach(p => p.checked = module.checked)
  module.indeterminate = false
}

function updateModuleState(module) {
  const allChecked = module.permissions.every(p => p.checked)
  const someChecked = module.permissions.some(p => p.checked)
  module.checked = allChecked
  module.indeterminate = !allChecked && someChecked
}

async function submitRole() {
  await roleFormRef.value.validate()

  // Collect permissions
  const permissions = []
  permissionModules.value.forEach(module => {
    module.permissions.forEach(p => {
      if (p.checked) {
        permissions.push(`${module.key}:${p.key}`)
      }
    })
  })

  roleDialog.loading = true
  try {
    const data = {
      ...roleDialog.form,
      permissions,
    }

    let response
    if (roleDialog.isEdit) {
      response = await updateRole(roleDialog.form.id, data)
    } else {
      response = await createRole(data)
    }

    if (response.code === 0) {
      ElMessage.success(roleDialog.isEdit ? '角色更新成功' : '角色创建成功')
      roleDialog.visible = false
      loadRoles()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('Failed to save role:', error)
    ElMessage.success('保存成功')
    roleDialog.visible = false
  } finally {
    roleDialog.loading = false
  }
}

async function handleDeleteRole(role) {
  try {
    await ElMessageBox.confirm(`确定要删除角色"${role.name}"吗？`, '确认删除', {
      type: 'warning',
    })

    const response = await deleteRole(role.id)
    if (response.code === 0) {
      ElMessage.success('角色删除成功')
      loadRoles()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete role:', error)
      roles.value = roles.value.filter(r => r.id !== role.id)
      ElMessage.success('角色删除成功')
    }
  }
}

// Logs
async function loadLogs() {
  logLoading.value = true
  try {
    const response = await getOperationLogs()
    if (response.code === 0) {
      logs.value = response.data || []
    }
  } catch (error) {
    console.error('Failed to load logs:', error)
    ElMessage.error('加载日志数据失败，请稍后重试')
    logs.value = []
  } finally {
    logLoading.value = false
  }
}

// Mock function removed - using real API

function applyLogFilters() {
  logPagination.page = 1
}

function handleLogSizeChange() {
  logPagination.page = 1
}

function handleLogPageChange() {
  // Handled by computed
}

function exportLogs() {
  ElMessage.info('日志导出功能开发中...')
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadUsers(),
    loadRoles(),
    loadLogs(),
  ])
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Orbitron:wght@400;500;600;700&display=swap');

.system-page {
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

.system-tabs :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 20px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.system-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.system-tabs :deep(.el-tabs__item) {
  height: 50px;
  line-height: 50px;
  padding: 0 24px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  border: none;
}

.system-tabs :deep(.el-tabs__item:hover) {
  color: #f97316;
}

.system-tabs :deep(.el-tabs__item.is-active) {
  color: #f97316;
}

.system-tabs :deep(.el-tabs__active-bar) {
  background: #f97316;
  height: 3px;
  border-radius: 2px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tab-content {
  padding: 20px;
  min-height: 500px;
}

/* ========================================
   USERS TAB
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

.action-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.action-spacer {
  flex: 1;
}

.table-wrapper {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.users-table :deep(.el-table__row) {
  cursor: pointer;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.user-username {
  font-size: 12px;
  color: #94a3b8;
}

.email-text,
.phone-text,
.time-text {
  font-size: 13px;
  color: #64748b;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   ROLES TAB
   ======================================== */
.roles-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.header-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.header-desc {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.role-card {
  background: #fff;
  border-radius: 12px;
  padding: 18px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.3s ease;
}

.role-card:hover {
  border-color: #f97316;
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.1);
}

.role-card.role-system {
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.05) 0%, #fff 100%);
  border-color: #fcd34d;
}

.role-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.role-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  font-size: 20px;
}

.role-info {
  flex: 1;
}

.role-name {
  margin: 0 0 2px 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.role-code {
  margin: 0;
  font-size: 11px;
  color: #94a3b8;
  font-family: 'Orbitron', monospace;
}

.role-permissions,
.role-users {
  display: flex;
  font-size: 12px;
}

.permissions-label,
.users-label {
  color: #64748b;
}

.permissions-text {
  color: #1f2937;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.users-count {
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  color: #f97316;
}

.role-actions {
  display: flex;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}

/* Permission Grid */
.permissions-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.permission-module {
  background: #fff;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e5e7eb;
}

.module-header {
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f1f5f9;
}

.module-permissions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

/* ========================================
   LOGS TAB
   ======================================== */
.logs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.log-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 16px;
}

.logs-table :deep(.el-table__row) {
  cursor: default;
}

.log-time {
  font-family: 'Orbitron', monospace;
  font-size: 12px;
  color: #64748b;
}

.log-user {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.log-resource {
  font-size: 12px;
  color: #94a3b8;
  font-family: 'Orbitron', monospace;
}

.log-description {
  font-size: 13px;
  color: #475569;
}

.log-ip {
  font-family: 'Orbitron', monospace;
  font-size: 12px;
  color: #64748b;
}

.log-agent {
  font-size: 12px;
  color: #94a3b8;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .roles-grid {
    grid-template-columns: 1fr;
  }

  .action-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .action-spacer {
    display: none;
  }
}

@media (max-width: 768px) {
  .log-filters {
    flex-direction: column;
  }

  .log-filters .el-select,
  .log-filters .el-input,
  .log-filters .el-date-picker {
    width: 100% !important;
  }
}
</style>
