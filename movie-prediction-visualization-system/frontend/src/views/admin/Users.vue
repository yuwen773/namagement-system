<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deleteUser,
  disableUser,
  enableUser,
  resetUserPassword
} from '@/api/user'
import {
  User,
  Plus,
  Edit,
  Delete,
  Lock,
  Unlock,
  Refresh
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const tableLoading = ref(false)

// 表格数据
const tableData = ref([])
const total = ref(0)

// 查询参数
const queryParams = reactive({
  page: 1,
  pageSize: 10,
  username: '',
  role: '',
  is_active: ''
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('编辑用户')
const formLoading = ref(false)

// 表单数据
const form = reactive({
  id: null,
  username: '',
  password: '',
  real_name: '',
  email: '',
  phone: '',
  role: 'USER',
  is_active: true
})

// 重置密码对话框
const resetPwdDialogVisible = ref(false)
const resetPwdForm = reactive({
  userId: null,
  username: '',
  new_password: ''
})

// 表单验证规则
const rules = computed(() => ({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在3-50个字符', trigger: 'blur' }
  ],
  password: form.id ? [] : [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}))

const resetPwdRules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const resetPwdFormRef = ref(null)

// 角色选项
const roleOptions = [
  { label: '管理员', value: 'ADMIN' },
  { label: '普通用户', value: 'USER' }
]

// 状态选项
const statusOptions = [
  { label: '全部', value: '' },
  { label: '正常', value: 'true' },
  { label: '已禁用', value: 'false' }
]

// 加载用户列表
const loadData = async () => {
  tableLoading.value = true
  try {
    const res = await getUsers(queryParams)
    tableData.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  } finally {
    tableLoading.value = false
  }
}

// 查询
const handleSearch = () => {
  queryParams.page = 1
  loadData()
}

// 重置
const handleReset = () => {
  queryParams.username = ''
  queryParams.role = ''
  queryParams.is_active = ''
  queryParams.page = 1
  loadData()
}

// 分页
const handleSizeChange = (val) => {
  queryParams.pageSize = val
  loadData()
}

const handleCurrentChange = (val) => {
  queryParams.page = val
  loadData()
}

// 打开新增对话框
const handleAdd = () => {
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

// 打开编辑对话框
const handleEdit = async (row) => {
  dialogTitle.value = '编辑用户'
  formLoading.value = true
  try {
    const res = await getUser(row.id)
    const userData = res.data
    Object.assign(form, {
      id: userData.id,
      username: userData.username,
      password: '',
      real_name: userData.real_name || '',
      email: userData.email || '',
      phone: userData.phone || '',
      role: userData.role,
      is_active: userData.is_active
    })
  } catch (error) {
    ElMessage.error('获取用户信息失败')
    console.error(error)
  } finally {
    formLoading.value = false
  }
  dialogVisible.value = true
}

// 禁用用户
const handleDisable = (row) => {
  ElMessageBox.confirm(
    `确定要禁用用户"${row.username}"吗？禁用后用户将无法登录系统。`,
    '禁用确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await disableUser(row.id)
      ElMessage.success('禁用成功')
      loadData()
    } catch (error) {
      console.error('禁用失败:', error)
    }
  }).catch(() => {})
}

// 启用用户
const handleEnable = (row) => {
  ElMessageBox.confirm(
    `确定要启用用户"${row.username}"吗？`,
    '启用确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'success'
    }
  ).then(async () => {
    try {
      await enableUser(row.id)
      ElMessage.success('启用成功')
      loadData()
    } catch (error) {
      console.error('启用失败:', error)
    }
  }).catch(() => {})
}

// 重置密码
const handleResetPassword = (row) => {
  resetPwdForm.userId = row.id
  resetPwdForm.username = row.username
  resetPwdForm.new_password = ''
  resetPwdDialogVisible.value = true
}

// 提交重置密码
const submitResetPassword = async () => {
  if (!resetPwdFormRef.value) return

  await resetPwdFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      await resetUserPassword(resetPwdForm.userId, {
        new_password: resetPwdForm.new_password
      })
      ElMessage.success(`用户"${resetPwdForm.username}"密码已重置为: ${resetPwdForm.new_password}`)
      resetPwdDialogVisible.value = false
    } catch (error) {
      console.error('重置密码失败:', error)
    }
  })
}

// 删除
const handleDelete = (row) => {
  // 防止删除自己
  if (row.id === userStore.user?.id) {
    ElMessage.warning('不能删除当前登录的账号')
    return
  }

  ElMessageBox.confirm(
    `确定要删除用户"${row.username}"吗？此操作不可恢复！`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'danger'
    }
  ).then(async () => {
    try {
      await deleteUser(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

// 重置表单
const resetForm = () => {
  form.id = null
  form.username = ''
  form.password = ''
  form.real_name = ''
  form.email = ''
  form.phone = ''
  form.role = 'USER'
  form.is_active = true
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    formLoading.value = true
    try {
      const data = {
        username: form.username,
        real_name: form.real_name,
        email: form.email,
        phone: form.phone,
        role: form.role,
        is_active: form.is_active
      }

      // 新增时需要密码
      if (!form.id) {
        data.password = form.password
        await createUser(data)
        ElMessage.success('创建成功')
      } else {
        await updateUser(form.id, data)
        ElMessage.success('更新成功')
      }

      dialogVisible.value = false
      loadData()
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      formLoading.value = false
    }
  })
}

// 取消
const handleCancel = () => {
  dialogVisible.value = false
  resetForm()
}

// 取消重置密码
const handleCancelResetPassword = () => {
  resetPwdDialogVisible.value = false
  resetPwdForm.userId = null
  resetPwdForm.username = ''
  resetPwdForm.new_password = ''
  if (resetPwdFormRef.value) {
    resetPwdFormRef.value.resetFields()
  }
}

// 格式化时间
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

// 获取角色标签类型
const getRoleType = (role) => {
  return role === 'ADMIN' ? 'danger' : 'primary'
}

// 获取角色文本
const getRoleText = (role) => {
  return role === 'ADMIN' ? '管理员' : '普通用户'
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
    <!-- 动画背景网格 -->
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
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500 to-purple-500 flex items-center justify-center shadow-lg shadow-violet-500/30">
              <User class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-white">用户管理</h1>
              <p class="text-slate-400 text-sm mt-0.5">管理系统用户账号和权限</p>
            </div>
          </div>
          <el-button
            type="primary"
            :icon="Plus"
            @click="handleAdd"
            class="!bg-gradient-to-r !from-violet-500 !to-purple-500 !border-0"
          >
            新增用户
          </el-button>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="mb-6 animate-slide-up">
        <div class="glass-card rounded-2xl p-5 border border-white/10">
          <el-form :inline="true" :model="queryParams" class="search-form">
            <el-form-item label="用户名">
              <el-input
                v-model="queryParams.username"
                placeholder="请输入用户名"
                clearable
                @keyup.enter="handleSearch"
                class="!w-48"
              />
            </el-form-item>
            <el-form-item label="角色">
              <el-select v-model="queryParams.role" placeholder="请选择角色" clearable class="!w-40">
                <el-option label="全部" value="" />
                <el-option
                  v-for="opt in roleOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="queryParams.is_active" placeholder="请选择状态" clearable class="!w-40">
                <el-option
                  v-for="opt in statusOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="animate-slide-up" style="animation-delay: 0.1s">
        <div class="glass-card rounded-2xl border border-white/10 overflow-hidden">
          <el-table
            :data="tableData"
            v-loading="tableLoading"
            stripe
            style="width: 100%"
            class="user-table"
          >
            <el-table-column prop="id" label="ID" width="80" align="center" />
            <el-table-column prop="username" label="用户名" width="140" />
            <el-table-column prop="real_name" label="真实姓名" width="120">
              <template #default="{ row }">
                <span class="text-slate-300">{{ row.real_name || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="email" label="邮箱" min-width="200" show-overflow-tooltip>
              <template #default="{ row }">
                <span class="text-slate-400">{{ row.email || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="phone" label="手机号" width="140">
              <template #default="{ row }">
                <span class="text-slate-400">{{ row.phone || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="role" label="角色" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getRoleType(row.role)" size="small">
                  {{ getRoleText(row.role) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                  {{ row.is_active ? '正常' : '已禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template #default="{ row }">
                <span class="text-slate-400 text-sm">{{ formatDate(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="280" fixed="right" align="center">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  size="small"
                  :icon="Edit"
                  @click="handleEdit(row)"
                >
                  编辑
                </el-button>
                <el-button
                  :type="row.is_active ? 'warning' : 'success'"
                  link
                  size="small"
                  @click="row.is_active ? handleDisable(row) : handleEnable(row)"
                >
                  <component :is="row.is_active ? Lock : Unlock" class="w-3.5 h-3.5 mr-0.5" />
                  {{ row.is_active ? '禁用' : '启用' }}
                </el-button>
                <el-button
                  type="info"
                  link
                  size="small"
                  :icon="Refresh"
                  @click="handleResetPassword(row)"
                >
                  重置密码
                </el-button>
                <el-button
                  type="danger"
                  link
                  size="small"
                  :icon="Delete"
                  @click="handleDelete(row)"
                  :disabled="row.id === userStore.user?.id"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="flex justify-end p-4 border-t border-white/10">
            <el-pagination
              v-model:current-page="queryParams.page"
              v-model:page-size="queryParams.pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              background
              class="pagination-dark"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑/新增对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      @close="handleCancel"
      class="user-dialog"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="90px"
        v-loading="formLoading"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :disabled="!!form.id"
          />
        </el-form-item>
        <el-form-item label="密码" :prop="form.id ? '' : 'password'">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
          <div v-if="!form.id" class="text-xs text-slate-400 mt-1">密码长度不少于6位</div>
          <div v-else class="text-xs text-slate-400 mt-1">留空则不修改密码</div>
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" class="!w-full">
            <el-option
              v-for="opt in roleOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="form.is_active"
            active-text="正常"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="formLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPwdDialogVisible"
      title="重置密码"
      width="400px"
      :close-on-click-modal="false"
      @close="handleCancelResetPassword"
    >
      <el-form
        ref="resetPwdFormRef"
        :model="resetPwdForm"
        :rules="resetPwdRules"
        label-width="90px"
      >
        <el-form-item label="用户名">
          <el-input v-model="resetPwdForm.username" disabled />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="resetPwdForm.new_password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
          <div class="text-xs text-slate-400 mt-1">密码长度不少于6位</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleCancelResetPassword">取消</el-button>
        <el-button type="primary" @click="submitResetPassword">
          确定
        </el-button>
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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #ec4899, #f472b6);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
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

/* 淡入动画 */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

/* 滑入动画 */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* 深色主题表格样式 */
:deep(.user-table) {
  background: transparent;
}

:deep(.user-table .el-table__header-wrapper) {
  background: transparent;
}

:deep(.user-table th.el-table__cell) {
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  font-weight: 600;
}

:deep(.user-table td.el-table__cell) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
}

:deep(.user-table tr:hover > td) {
  background: rgba(139, 92, 246, 0.1) !important;
}

:deep(.user-table .el-table__empty-block) {
  background: transparent;
}

:deep(.user-table .el-table__empty-text) {
  color: #64748b;
}

/* 深色主题分页样式 */
:deep(.pagination-dark .el-pagination) {
  color: #94a3b8;
}

:deep(.pagination-dark .el-pagination button) {
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.pagination-dark .el-pagination button:hover) {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.5);
}

:deep(.pagination-dark .el-pagination .el-pager li) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin: 0 2px;
}

:deep(.pagination-dark .el-pagination .el-pager li:hover) {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.5);
}

:deep(.pagination-dark .el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border-color: transparent;
  color: white;
}

/* 搜索表单样式 */
:deep(.search-form .el-form-item__label) {
  color: #94a3b8;
}

:deep(.search-form .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

:deep(.search-form .el-input__wrapper:hover) {
  border-color: rgba(139, 92, 246, 0.5);
}

:deep(.search-form .el-input__wrapper.is-focus) {
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1);
}

:deep(.search-form .el-input__inner) {
  color: #e2e8f0;
}

:deep(.search-form .el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
}

:deep(.search-form .el-select .el-input__inner) {
  color: #e2e8f0;
}

/* 对话框样式 */
:deep(.user-dialog .el-dialog) {
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.user-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.user-dialog .el-dialog__title) {
  color: #f1f5f9;
}

:deep(.user-dialog .el-dialog__body) {
  background: transparent;
}

:deep(.user-dialog .el-form-item__label) {
  color: #94a3b8;
}

:deep(.user-dialog .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

:deep(.user-dialog .el-input__wrapper.is-focus) {
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1);
}

:deep(.user-dialog .el-input__inner) {
  color: #e2e8f0;
}

:deep(.user-dialog .el-input__inner::placeholder) {
  color: #64748b;
}

:deep(.user-dialog .el-input__disabled .el-input__inner) {
  color: #64748b;
  background: rgba(255, 255, 255, 0.02);
}

:deep(.user-dialog .el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
}

:deep(.user-dialog .el-select .el-input__inner) {
  color: #e2e8f0;
}

:deep(.user-dialog .el-dialog__footer) {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
