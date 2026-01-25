<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getUserList,
  updateUserRole,
  updateUserStatus,
  resetUserPassword,
  ROLE_OPTIONS,
  ROLE_COLORS
} from '../api/user'

// 响应式状态
const loading = ref(false)
const userList = ref([])
const total = ref(0)
const pagination = reactive({
  page: 1,
  page_size: 10
})

// 筛选条件
const filters = reactive({
  status: 'all'
})

// 密码重置对话框
const resetPasswordDialog = reactive({
  visible: false,
  loading: false,
  userId: null,
  userName: '',
  newPassword: ''
})

// 角色选择对话框
const roleDialog = reactive({
  visible: false,
  loading: false,
  userId: null,
  userName: '',
  currentRole: '',
  newRole: ''
})

// 状态切换确认对话框
const statusDialog = reactive({
  visible: false,
  loading: false,
  userId: null,
  userName: '',
  currentStatus: true,
  targetStatus: true
})

// 获取用户列表
const fetchUserList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (filters.status !== 'all') {
      params.status = filters.status
    }

    const res = await getUserList(params)
    // DRF 默认分页格式：{count, next, previous, results}
    const responseData = res.data
    const data = responseData?.results || responseData?.data || []
    const totalCount = responseData?.count || responseData?.total || 0

    userList.value = data.map(user => ({
      ...user,
      status_text: user.is_active ? '已启用' : '已禁用',
      status_type: user.is_active ? 'success' : 'danger'
    }))
    total.value = totalCount
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 筛选变更处理
const handleFilterChange = () => {
  pagination.page = 1
  fetchUserList()
}

// 分页变更处理
const handlePageChange = (page) => {
  pagination.page = page
  fetchUserList()
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  fetchUserList()
}

// 打开角色修改对话框
const openRoleDialog = (user) => {
  roleDialog.visible = true
  roleDialog.userId = user.id
  roleDialog.userName = user.real_name || user.username
  roleDialog.currentRole = user.role
  roleDialog.newRole = user.role
}

// 确认修改角色
const confirmRoleChange = async () => {
  if (roleDialog.currentRole === roleDialog.newRole) {
    ElMessage.warning('角色未变更')
    return
  }

  roleDialog.loading = true
  try {
    await updateUserRole(roleDialog.userId, roleDialog.newRole)
    ElMessage.success('角色修改成功')
    roleDialog.visible = false
    fetchUserList()
  } catch (error) {
    console.error('角色修改失败:', error)
    ElMessage.error(error.response?.data?.message || '角色修改失败')
  } finally {
    roleDialog.loading = false
  }
}

// 打开状态切换对话框
const openStatusDialog = (user) => {
  statusDialog.visible = true
  statusDialog.userId = user.id
  statusDialog.userName = user.real_name || user.username
  statusDialog.currentStatus = user.is_active
  statusDialog.targetStatus = !user.is_active
}

// 确认状态切换
const confirmStatusChange = async () => {
  statusDialog.loading = true
  try {
    await updateUserStatus(statusDialog.userId, statusDialog.targetStatus)
    const actionText = statusDialog.targetStatus ? '启用' : '禁用'
    ElMessage.success(`用户已${actionText}`)
    statusDialog.visible = false
    fetchUserList()
  } catch (error) {
    console.error('状态切换失败:', error)
    ElMessage.error(error.response?.data?.message || '状态切换失败')
  } finally {
    statusDialog.loading = false
  }
}

// 打开密码重置对话框
const openResetPasswordDialog = (user) => {
  resetPasswordDialog.visible = true
  resetPasswordDialog.userId = user.id
  resetPasswordDialog.userName = user.real_name || user.username
  resetPasswordDialog.newPassword = ''
}

// 确认密码重置
const confirmResetPassword = async () => {
  if (!resetPasswordDialog.newPassword || resetPasswordDialog.newPassword.length < 6) {
    ElMessage.warning('密码长度至少6位')
    return
  }

  resetPasswordDialog.loading = true
  try {
    await resetUserPassword(resetPasswordDialog.userId, resetPasswordDialog.newPassword)
    ElMessage.success('密码重置成功')
    resetPasswordDialog.visible = false
  } catch (error) {
    console.error('密码重置失败:', error)
    ElMessage.error(error.response?.data?.message || '密码重置失败')
  } finally {
    resetPasswordDialog.loading = false
  }
}

// 获取角色显示文本
const getRoleText = (role) => {
  const option = ROLE_OPTIONS.find(opt => opt.value === role)
  return option ? option.label : role
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 初始化
onMounted(() => {
  fetchUserList()
})
</script>

<template>
  <div class="user-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h2 class="page-title">用户账号管理</h2>
        <p class="page-desc">管理系统用户账号、角色和权限</p>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-card class="filter-card">
        <el-form :inline="true" class="filter-form">
          <el-form-item label="账号状态">
            <el-select
              v-model="filters.status"
              placeholder="全部状态"
              @change="handleFilterChange"
              style="width: 140px"
            >
              <el-option label="全部" value="all" />
              <el-option label="已启用" value="active" />
              <el-option label="已禁用" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchUserList">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              查询
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 用户列表 -->
    <el-card class="data-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">用户列表</span>
          <span class="card-count">共 {{ total }} 个用户</span>
        </div>
      </template>

      <el-table
        :data="userList"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="用户ID" width="80" />

        <el-table-column label="账号信息" min-width="180">
          <template #default="{ row }">
            <div class="user-info-cell">
              <div class="user-name">{{ row.real_name || row.username }}</div>
              <div class="user-account">@{{ row.username }}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="手机号" width="140">
          <template #default="{ row }">
            {{ row.phone || '-' }}
          </template>
        </el-table-column>

        <el-table-column label="邮箱" min-width="180">
          <template #default="{ row }">
            {{ row.email || '-' }}
          </template>
        </el-table-column>

        <el-table-column label="角色" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="ROLE_COLORS[row.role]" size="small">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status_type" size="small">
              {{ row.status_text }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="注册时间" width="160" align="center">
          <template #default="{ row }">
            {{ formatDate(row.date_joined) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                type="primary"
                link
                size="small"
                @click="openRoleDialog(row)"
              >
                角色
              </el-button>
              <el-button
                :type="row.is_active ? 'danger' : 'success'"
                link
                size="small"
                @click="openStatusDialog(row)"
              >
                {{ row.is_active ? '禁用' : '启用' }}
              </el-button>
              <el-button
                type="warning"
                link
                size="small"
                @click="openResetPasswordDialog(row)"
              >
                重置密码
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="total > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 角色修改对话框 -->
    <el-dialog
      v-model="roleDialog.visible"
      title="修改用户角色"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="dialog-content">
        <p class="dialog-message">
          将用户 <strong>{{ roleDialog.userName }}</strong> 的角色修改为：
        </p>
        <el-radio-group v-model="roleDialog.newRole" class="role-radio-group">
          <el-radio-button
            v-for="option in ROLE_OPTIONS"
            :key="option.value"
            :label="option.value"
          >
            {{ option.label }}
          </el-radio-button>
        </el-radio-group>
      </div>
      <template #footer>
        <el-button @click="roleDialog.visible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="roleDialog.loading"
          @click="confirmRoleChange"
        >
          确认修改
        </el-button>
      </template>
    </el-dialog>

    <!-- 状态切换对话框 -->
    <el-dialog
      v-model="statusDialog.visible"
      :title="statusDialog.targetStatus ? '启用用户' : '禁用用户'"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="dialog-content">
        <p class="dialog-message">
          确认{{ statusDialog.targetStatus ? '启用' : '禁用' }}用户
          <strong>{{ statusDialog.userName }}</strong> 吗？
        </p>
        <div class="warning-tip">
          <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <span>{{ statusDialog.targetStatus ? '启用后用户可以正常登录系统' : '禁用后用户将无法登录系统' }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="statusDialog.visible = false">取消</el-button>
        <el-button
          :type="statusDialog.targetStatus ? 'success' : 'danger'"
          :loading="statusDialog.loading"
          @click="confirmStatusChange"
        >
          确认{{ statusDialog.targetStatus ? '启用' : '禁用' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 密码重置对话框 -->
    <el-dialog
      v-model="resetPasswordDialog.visible"
      title="重置用户密码"
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="dialog-content">
        <p class="dialog-message">
          为用户 <strong>{{ resetPasswordDialog.userName }}</strong> 重置密码：
        </p>
        <el-form label-position="top">
          <el-form-item label="新密码">
            <el-input
              v-model="resetPasswordDialog.newPassword"
              type="password"
              placeholder="请输入新密码（至少6位）"
              show-password
              clearable
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="resetPasswordDialog.visible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="resetPasswordDialog.loading"
          @click="confirmResetPassword"
        >
          确认重置
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.user-management {
  padding: 0;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.page-desc {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

/* 筛选区域 */
.filter-section {
  margin-bottom: 20px;
}

.filter-card {
  border-radius: var(--radius-lg);
}

.filter-form {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

/* 数据卡片 */
.data-card {
  border-radius: var(--radius-lg);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.card-count {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

/* 用户信息单元格 */
.user-info-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 500;
  color: var(--color-text-primary);
}

.user-account {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border-light);
}

/* 对话框 */
.dialog-content {
  padding: 8px 0;
}

.dialog-message {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 20px;
}

.dialog-message strong {
  color: var(--color-text-primary);
}

.role-radio-group {
  display: flex;
  width: 100%;
}

.role-radio-group .el-radio-button {
  flex: 1;
}

.role-radio-group .el-radio-button__inner {
  width: 100%;
}

.warning-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: var(--color-warning-subtle);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--color-warning);
}

.warning-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

/* 响应式 */
@media (max-width: 1024px) {
  .filter-row {
    flex-wrap: wrap;
    gap: 16px;
  }

  .filter-item {
    flex: 1;
    min-width: 150px;
  }

  .search-btn {
    margin-left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .filter-row {
    flex-direction: column;
  }

  .filter-item {
    width: 100%;
    min-width: unset;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .stat-item {
    padding: 16px;
  }

  .stat-value {
    font-size: 20px;
  }

  .user-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .user-detail {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
    gap: 8px;
  }

  .action-buttons .el-button {
    width: 100%;
  }

  .role-tag {
    font-size: 12px;
  }
}
</style>
