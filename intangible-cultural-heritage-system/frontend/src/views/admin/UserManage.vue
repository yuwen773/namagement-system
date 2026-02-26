<template>
  <div class="user-manage">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-seal">
          <span class="seal-text">管理</span>
        </div>
        <div class="header-texts">
          <h1 class="page-title">用户管理</h1>
          <p class="page-subtitle">管理系统用户和权限</p>
        </div>
      </div>
      <button class="add-btn" @click="handleAdd">
        <span class="btn-seal">增</span>
        <span>新增用户</span>
      </button>
    </header>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="用户名">
          <el-input v-model="filters.username" placeholder="搜索用户名" clearable @clear="handleSearch" class="user-input" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="filters.role" placeholder="选择角色" clearable class="user-select">
            <el-option label="管理员" value="admin" />
            <el-option label="用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.is_active" placeholder="选择状态" clearable class="user-select">
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <button class="action-btn search-btn" @click="handleSearch">搜索</button>
          <button class="action-btn reset-btn" @click="handleReset">重置</button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 表格区域 -->
    <div class="table-frame">
      <el-table :data="tableData" v-loading="loading" class="data-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="150" />
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <span class="role-badge" :class="row.role === 'admin' ? 'role-admin' : 'role-user'">
              {{ row.role === 'admin' ? '管理员' : '用户' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <span class="status-badge" :class="row.is_active ? 'status-active' : 'status-inactive'">
              {{ row.is_active ? '启用' : '禁用' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.last_login_time ? formatDate(row.last_login_time) : '从未登录' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <button class="table-action-btn edit-btn" @click="handleEdit(row)">编辑</button>
            <el-dropdown trigger="click" @command="(cmd) => handleMoreAction(cmd, row)">
              <button class="table-action-btn more-btn">更多</button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="'change-role'">
                    {{ row.role === 'admin' ? '设为用户' : '设为管理员' }}
                  </el-dropdown-item>
                  <el-dropdown-item :command="'change-status'">
                    {{ row.is_active ? '禁用用户' : '启用用户' }}
                  </el-dropdown-item>
                  <el-dropdown-item :command="'reset-password'">重置密码</el-dropdown-item>
                  <el-dropdown-item :command="'delete'" divided>删除用户</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="20"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 新增/编辑用户弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      class="user-dialog"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" :disabled="!!editingId" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item v-if="!editingId" label="密码" prop="password">
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="dialog-btn cancel-btn" @click="dialogVisible = false">取消</button>
        <button class="dialog-btn confirm-btn" @click="handleSubmit" :disabled="submitting">
          {{ submitting ? '提交中...' : '确定' }}
        </button>
      </template>
    </el-dialog>

    <!-- 重置密码弹窗 -->
    <el-dialog
      v-model="resetPasswordVisible"
      title="重置密码"
      width="400px"
      :close-on-click-modal="false"
      class="user-dialog"
    >
      <el-form :model="resetPasswordForm" :rules="resetPasswordRules" ref="resetPasswordFormRef" label-width="80px">
        <el-form-item label="用户">
          <el-input v-model="resetPasswordForm.username" disabled />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="resetPasswordForm.new_password" type="password" placeholder="请输入新密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="resetPasswordForm.confirm_password" type="password" placeholder="请再次输入新密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="dialog-btn cancel-btn" @click="resetPasswordVisible = false">取消</button>
        <button class="dialog-btn confirm-btn" @click="handleResetPasswordSubmit" :disabled="submitting">
          {{ submitting ? '提交中...' : '确定' }}
        </button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  getUserList,
  createUser,
  updateUser,
  updateUserStatus,
  updateUserRole,
  resetUserPassword,
  deleteUser
} from '@/api/user'
import type { UserDetail, CreateUserRequest, UpdateUserRequest } from '@/types'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// State
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const resetPasswordVisible = ref(false)
const dialogTitle = ref('新增用户')
const currentPage = ref(1)
const total = ref(0)
const tableData = ref<UserDetail[]>([])
const formRef = ref<FormInstance>()
const resetPasswordFormRef = ref<FormInstance>()
const editingId = ref<number | null>(null)
const resetPasswordUserId = ref<number | null>(null)

// Filters
const filters = reactive({
  username: '',
  role: undefined as 'admin' | 'user' | undefined,
  is_active: undefined as boolean | undefined
})

// Form data
const formData = reactive<CreateUserRequest & { username?: string }>({
  username: '',
  password: '',
  email: '',
  role: 'user'
})

// Reset password form data
const resetPasswordForm = reactive({
  username: '',
  new_password: '',
  confirm_password: ''
})

// Form rules
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

// Reset password form rules
const resetPasswordRules: FormRules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== resetPasswordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// Methods
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      username: filters.username || undefined,
      role: filters.role,
      is_active: filters.is_active
    }
    const res = await getUserList(params)
    if (res.data.code === 0) {
      tableData.value = res.data.data
      total.value = res.data.total || 0
    } else {
      ElMessage.error(res.data.message || '获取用户列表失败')
    }
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const handleReset = () => {
  filters.username = ''
  filters.role = undefined
  filters.is_active = undefined
  handleSearch()
}

const handlePageChange = () => {
  fetchData()
}

const handleAdd = () => {
  dialogTitle.value = '新增用户'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: UserDetail) => {
  dialogTitle.value = '编辑用户'
  editingId.value = row.id
  formData.username = row.username
  formData.email = row.email
  formData.role = row.role
  formData.password = ''
  dialogVisible.value = true
}

const handleMoreAction = async (command: string, row: UserDetail) => {
  switch (command) {
    case 'change-role':
      await handleChangeRole(row)
      break
    case 'change-status':
      await handleChangeStatus(row)
      break
    case 'reset-password':
      handleOpenResetPassword(row)
      break
    case 'delete':
      await handleDelete(row)
      break
  }
}

const handleChangeRole = async (row: UserDetail) => {
  const newRole = row.role === 'admin' ? 'user' : 'admin'
  const actionText = newRole === 'admin' ? '设为管理员' : '设为用户'
  try {
    await ElMessageBox.confirm(
      `确定要将用户 "${row.username}" ${actionText}吗？`,
      '更改角色',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await updateUserRole({ user_ids: [row.id], role: newRole })
    if (res.data.code === 0) {
      ElMessage.success('角色更改成功')
      fetchData()
    } else {
      ElMessage.error(res.data.message || '角色更改失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('角色更改失败')
    }
  }
}

const handleChangeStatus = async (row: UserDetail) => {
  const newStatus = !row.is_active
  const actionText = newStatus ? '启用' : '禁用'
  try {
    await ElMessageBox.confirm(
      `确定要${actionText}用户 "${row.username}"吗？`,
      `${actionText}用户`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await updateUserStatus({ user_ids: [row.id], is_active: newStatus })
    if (res.data.code === 0) {
      ElMessage.success(`用户已${actionText}`)
      fetchData()
    } else {
      ElMessage.error(res.data.message || '状态更改失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('状态更改失败')
    }
  }
}

const handleOpenResetPassword = (row: UserDetail) => {
  resetPasswordUserId.value = row.id
  resetPasswordForm.username = row.username
  resetPasswordForm.new_password = ''
  resetPasswordForm.confirm_password = ''
  resetPasswordVisible.value = true
}

const handleResetPasswordSubmit = async () => {
  if (!resetPasswordFormRef.value || resetPasswordUserId.value === null) return

  await resetPasswordFormRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      const res = await resetUserPassword({
        user_id: resetPasswordUserId.value!,
        new_password: resetPasswordForm.new_password
      })
      if (res.data.code === 0) {
        ElMessage.success('密码重置成功')
        resetPasswordVisible.value = false
      } else {
        ElMessage.error(res.data.message || '密码重置失败')
      }
    } catch (error) {
      ElMessage.error('密码重置失败')
    } finally {
      submitting.value = false
    }
  })
}

const handleDelete = async (row: UserDetail) => {
  // 不允许删除自己
  if (row.id === userStore.userId) {
    ElMessage.warning('不能删除自己的账号')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}"吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await deleteUser(row.id)
    if (res.data.code === 0) {
      ElMessage.success('删除成功')
      fetchData()
    } else {
      ElMessage.error(res.data.message || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      if (editingId.value) {
        // 编辑用户
        const updateData: UpdateUserRequest = {
          email: formData.email,
          role: formData.role
        }
        const res = await updateUser(editingId.value, updateData)
        if (res.data.code === 0) {
          ElMessage.success('更新成功')
          dialogVisible.value = false
          fetchData()
        } else {
          ElMessage.error(res.data.message || '更新失败')
        }
      } else {
        // 新增用户
        const createData: CreateUserRequest = {
          username: formData.username!,
          password: formData.password!,
          email: formData.email,
          role: formData.role
        }
        const res = await createUser(createData)
        if (res.data.code === 0) {
          ElMessage.success('创建成功')
          dialogVisible.value = false
          fetchData()
        } else {
          ElMessage.error(res.data.message || '创建失败')
        }
      }
    } catch (error) {
      ElMessage.error('操作失败')
    } finally {
      submitting.value = false
    }
  })
}

const resetForm = () => {
  formData.username = ''
  formData.password = ''
  formData.email = ''
  formData.role = 'user'
  formRef.value?.clearValidate()
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.user-manage {
  padding: 24px;
  background: #F7F4ED;
  min-height: calc(100vh - 60px);
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(194, 35, 49, 0.3);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-seal {
  width: 56px;
  height: 56px;
  background: #D4AF37;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.seal-text {
  font-size: 20px;
  font-weight: 700;
  color: #2F3640;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 2px;
}

.header-texts {
  color: white;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
}

.page-subtitle {
  font-size: 13px;
  margin: 0;
  opacity: 0.9;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #C23531;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.btn-seal {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #C23531;
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 2px;
  font-family: "STSong", "SimSun", serif;
}

/* ========== 筛选区域 ========== */
.filter-section {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.filter-form {
  margin: 0;
}

:deep(.user-input .el-input__wrapper),
:deep(.user-select .el-select__wrapper) {
  background: #F7F4ED;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
}

.action-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn {
  background: #C23531;
  color: white;
}

.search-btn:hover {
  background: #A93226;
}

.reset-btn {
  background: #F7F4ED;
  color: #606266;
  margin-left: 8px;
}

.reset-btn:hover {
  background: #EDF2ED;
}

/* ========== 表格区域 ========== */
.table-frame {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.data-table {
  margin-bottom: 24px;
}

:deep(.data-table th) {
  background: #F7F4ED !important;
  color: #2F3640 !important;
  font-weight: 600 !important;
}

:deep(.data-table tr:hover) {
  background: rgba(212, 175, 55, 0.05) !important;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.role-admin {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
}

.role-badge.role-user {
  background: rgba(93, 138, 168, 0.15);
  color: #5D8AA8;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.status-active {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.status-badge.status-inactive {
  background: rgba(156, 163, 175, 0.1);
  color: #9ca3af;
}

.table-action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-btn {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  margin-right: 8px;
}

.edit-btn:hover {
  background: #D4AF37;
  color: white;
}

.more-btn {
  background: rgba(47, 54, 64, 0.1);
  color: #606266;
}

.more-btn:hover {
  background: #2F3640;
  color: white;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

:deep(.el-pagination .el-pager li.is-active) {
  background: #C23531 !important;
  border-color: #C23531 !important;
}

/* ========== 弹窗 ========== */
:deep(.user-dialog .el-dialog__header) {
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  color: white;
  padding: 20px 24px;
  border-radius: 8px 8px 0 0;
}

:deep(.user-dialog .el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 2px;
  font-family: "STSong", "SimSun", serif;
}

.dialog-btn {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: #F7F4ED;
  color: #606266;
  margin-right: 12px;
}

.cancel-btn:hover {
  background: #EDF2ED;
}

.confirm-btn {
  background: #C23531;
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background: #A93226;
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
