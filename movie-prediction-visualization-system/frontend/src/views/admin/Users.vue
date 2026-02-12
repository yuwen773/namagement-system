<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
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
  Search,
  Edit,
  Delete,
  Lock,
  Unlock,
  Refresh,
  Filter,
  Check,
  Close,
  Message,
  Phone,
  Key,
  Clock
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const tableLoading = ref(false)

const tableData = ref([])
const total = ref(0)

const queryParams = reactive({
  page: 1,
  pageSize: 10,
  username: '',
  role: '',
  is_active: ''
})

const dialogVisible = ref(false)
const dialogTitle = ref('编辑用户')
const formLoading = ref(false)

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

const resetPwdDialogVisible = ref(false)
const resetPwdForm = reactive({
  userId: null,
  username: '',
  new_password: ''
})

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

const roleOptions = [
  { label: '管理员', value: 'ADMIN' },
  { label: '普通用户', value: 'USER' }
]

const statusOptions = [
  { label: '全部', value: '' },
  { label: '正常', value: 'true' },
  { label: '已禁用', value: 'false' }
]

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

const handleSearch = () => {
  queryParams.page = 1
  loadData()
}

const handleReset = () => {
  queryParams.username = ''
  queryParams.role = ''
  queryParams.is_active = ''
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
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

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
      ElMessage.success({
        message: '禁用成功',
        icon: Check
      })
      loadData()
    } catch (error) {
      console.error('禁用失败:', error)
    }
  }).catch(() => {})
}

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
      ElMessage.success({
        message: '启用成功',
        icon: Check
      })
      loadData()
    } catch (error) {
      console.error('启用失败:', error)
    }
  }).catch(() => {})
}

const handleResetPassword = (row) => {
  resetPwdForm.userId = row.id
  resetPwdForm.username = row.username
  resetPwdForm.new_password = ''
  resetPwdDialogVisible.value = true
}

const submitResetPassword = async () => {
  if (!resetPwdFormRef.value) return

  try {
    await resetPwdFormRef.value.validate()
    await resetUserPassword(resetPwdForm.userId, {
      new_password: resetPwdForm.new_password
    })
    ElMessage.success({
      message: `用户"${resetPwdForm.username}"密码已重置为: ${resetPwdForm.new_password}`,
      icon: Check
    })
    resetPwdDialogVisible.value = false
  } catch (error) {
    console.error('重置密码失败:', error)
  }
}

const handleDelete = (row) => {
  if (row.id === userStore.user?.id) {
    ElMessage.warning('不能删除当前登录的账号')
    return
  }

  ElMessageBox.confirm(
    `确定要删除用户"${row.username}"吗？此操作不可恢复！`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(async () => {
    try {
      await deleteUser(row.id)
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

const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    formLoading.value = true

    const data = {
      username: form.username,
      real_name: form.real_name,
      email: form.email,
      phone: form.phone,
      role: form.role,
      is_active: form.is_active
    }

    if (!form.id) {
      data.password = form.password
      await createUser(data)
      ElMessage.success({
        message: '创建成功',
        icon: Check
      })
    } else {
      await updateUser(form.id, data)
      ElMessage.success({
        message: '更新成功',
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

const handleCancelResetPassword = () => {
  resetPwdDialogVisible.value = false
  resetPwdForm.userId = null
  resetPwdForm.username = ''
  resetPwdForm.new_password = ''
  if (resetPwdFormRef.value) {
    resetPwdFormRef.value.resetFields()
  }
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const getRoleType = (role) => {
  return role === 'ADMIN' ? 'danger' : 'primary'
}

const getRoleText = (role) => {
  return role === 'ADMIN' ? '管理员' : '普通用户'
}

const getRoleBadgeClass = (role) => {
  return role === 'ADMIN'
    ? 'bg-gradient-to-r from-red-500/20 to-pink-500/20 border-red-500/30 text-red-400'
    : 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border-blue-500/30 text-blue-400'
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="min-h-screen relative overflow-hidden users-page">
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
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
              <User class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-white">用户管理</h1>
              <p class="text-slate-400 text-sm">管理系统用户账号和权限</p>
            </div>
          </div>
          <button @click="handleAdd" class="add-btn from-violet-500 to-purple-600">
            <Plus class="w-4 h-4 mr-1.5" />
            新增用户
          </button>
        </div>
      </div>

      <!-- 筛选控制栏 -->
      <div class="glass-card rounded-2xl p-5 border border-white/10 mb-6 animate-slide-up" style="animation-delay: 0.1s">
        <div class="flex items-center gap-2 mb-4">
          <Filter class="w-4 h-4 text-violet-400" />
          <span class="text-sm font-medium text-slate-300">筛选搜索</span>
        </div>

        <div class="flex items-center gap-4 flex-wrap">
          <div class="flex-1 min-w-[200px] relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              v-model="queryParams.username"
              type="text"
              placeholder="搜索用户名..."
              class="search-input"
              @keyup.enter="handleSearch"
            />
          </div>

          <div class="min-w-[140px]">
            <el-select
              v-model="queryParams.role"
              placeholder="选择角色"
              clearable
              class="filter-select"
              popper-class="user-select-dropdown"
              style="width: 100%"
              @change="handleSearch"
            >
              <el-option label="全部" value="" />
              <el-option
                v-for="opt in roleOptions"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
          </div>

          <div class="min-w-[140px]">
            <el-select
              v-model="queryParams.is_active"
              placeholder="选择状态"
              clearable
              class="filter-select"
              popper-class="user-select-dropdown"
              style="width: 100%"
              @change="handleSearch"
            >
              <el-option
                v-for="opt in statusOptions"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
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
        </div>
      </div>

      <!-- 数据表格区域 -->
      <div class="glass-card rounded-2xl border border-white/10 animate-slide-up" style="animation-delay: 0.2s">
        <!-- 表格头部信息 -->
        <div class="px-6 py-4 border-b border-white/10 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
              <User class="w-4 h-4 text-violet-400" />
            </div>
            <div>
              <h3 class="text-white font-medium">用户列表</h3>
              <p class="text-xs text-slate-400 mt-0.5">共 <span class="text-violet-400 font-medium">{{ total }}</span> 个用户</p>
            </div>
          </div>
        </div>

        <!-- 表格 -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">用户</th>
                <th class="text-left py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">用户名</th>
                <th class="text-left py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">真实姓名</th>
                <th class="text-left py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">邮箱</th>
                <th class="text-left py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">手机号</th>
                <th class="text-center py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">角色</th>
                <th class="text-center py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">状态</th>
                <th class="text-left py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">创建时间</th>
                <th class="text-center py-4 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading && tableData.length === 0">
                <td colspan="9" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-12 h-12 rounded-full border-2 border-violet-500/30 border-t-violet-500 animate-spin mb-4"></div>
                    <p class="text-slate-400">加载中...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="tableData.length === 0">
                <td colspan="9" class="py-20 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                      <User class="w-8 h-8 text-slate-600" />
                    </div>
                    <p class="text-slate-500 mb-1">暂无用户数据</p>
                    <p class="text-slate-600 text-sm">点击上方「新增用户」开始添加</p>
                  </div>
                </td>
              </tr>
              <tr
                v-for="(record, index) in tableData"
                :key="record.id"
                class="border-b border-white/5 hover:bg-white/5 transition-colors group"
                :style="{ animationDelay: `${0.3 + index * 0.03}s` }"
              >
                <td class="py-4 px-4">
                  <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
                    <User class="w-5 h-5 text-violet-400" />
                  </div>
                </td>
                <td class="py-4 px-6">
                  <div class="flex items-center gap-2">
                    <span class="text-white text-sm font-medium">{{ record.username }}</span>
                    <span class="text-xs text-slate-500">ID: {{ record.id }}</span>
                  </div>
                </td>
                <td class="py-4 px-4 text-slate-300 text-sm">{{ record.real_name || '-' }}</td>
                <td class="py-4 px-4">
                  <div v-if="record.email" class="flex items-center gap-2 text-slate-300 text-sm">
                    <Message class="w-4 h-4 text-slate-500" />
                    <span class="truncate max-w-[150px] inline-block">{{ record.email }}</span>
                  </div>
                  <span v-else class="text-slate-500">-</span>
                </td>
                <td class="py-4 px-4 text-slate-300 text-sm">
                  <div v-if="record.phone" class="flex items-center gap-2">
                    <Phone class="w-4 h-4 text-slate-500" />
                    <span>{{ record.phone }}</span>
                  </div>
                  <span v-else class="text-slate-500">-</span>
                </td>
                <td class="py-4 px-4 text-center">
                  <span class="role-badge" :class="getRoleBadgeClass(record.role)">
                    <Key class="w-3.5 h-3.5 mr-1" />
                    {{ getRoleText(record.role) }}
                  </span>
                </td>
                <td class="py-4 px-4 text-center">
                  <span
                    class="status-badge"
                    :class="record.is_active ? 'status-active' : 'status-inactive'"
                  >
                    <span class="status-dot" :class="record.is_active ? 'dot-active' : 'dot-inactive'"></span>
                    {{ record.is_active ? '正常' : '已禁用' }}
                  </span>
                </td>
                <td class="py-4 px-4 text-slate-400 text-sm">
                  <div class="flex items-center gap-2">
                    <Clock class="w-4 h-4 text-slate-500" />
                    <span>{{ formatDate(record.created_at) }}</span>
                  </div>
                </td>
                <td class="py-4 px-4 text-center">
                  <div class="flex items-center justify-center gap-1 flex-wrap">
                    <button
                      @click="handleEdit(record)"
                      class="action-icon-btn"
                      title="编辑"
                    >
                      <Edit class="w-4 h-4" />
                    </button>
                    <button
                      @click="record.is_active ? handleDisable(record) : handleEnable(record)"
                      class="action-icon-btn"
                      :class="record.is_active ? 'text-amber-400' : 'text-emerald-400'"
                      :title="record.is_active ? '禁用' : '启用'"
                    >
                      <component :is="record.is_active ? Lock : Unlock" class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleResetPassword(record)"
                      class="action-icon-btn text-cyan-400"
                      title="重置密码"
                    >
                      <Refresh class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(record)"
                      class="action-icon-btn text-red-400 hover:text-red-300"
                      title="删除"
                      :disabled="record.id === userStore.user?.id"
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

    <!-- 编辑/新增对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      @close="handleCancel"
      class="user-dialog"
      destroy-on-close
    >
      <div class="space-y-5">
        <div class="form-group">
          <label class="form-label">
            <User class="w-4 h-4" />
            用户名 <span class="text-red-400">*</span>
          </label>
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :disabled="!!form.id"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Lock class="w-4 h-4" />
            密码 <span v-if="!form.id" class="text-red-400">*</span>
          </label>
          <el-input
            v-model="form.password"
            type="password"
            :placeholder="form.id ? '留空则不修改' : '请输入密码'"
            show-password
            class="form-input"
          />
          <p class="text-xs text-slate-400 mt-1">密码长度不少于6位</p>
        </div>

        <div class="form-group">
          <label class="form-label">
            <User class="w-4 h-4" />
            真实姓名
          </label>
          <el-input
            v-model="form.real_name"
            placeholder="请输入真实姓名"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Message class="w-4 h-4" />
            邮箱
          </label>
          <el-input
            v-model="form.email"
            placeholder="请输入邮箱"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Phone class="w-4 h-4" />
            手机号
          </label>
          <el-input
            v-model="form.phone"
            placeholder="请输入手机号"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Key class="w-4 h-4" />
            角色 <span class="text-red-400">*</span>
          </label>
          <el-select
            v-model="form.role"
            placeholder="请选择角色"
            class="form-input"
            popper-class="user-select-dropdown"
            style="width: 100%"
          >
            <el-option
              v-for="opt in roleOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </div>

        <div class="form-group">
          <label class="form-label">
            <Key class="w-4 h-4" />
            状态
          </label>
          <div class="flex items-center gap-3">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                v-model="form.is_active"
                :value="true"
                class="status-radio"
              />
              <span class="text-sm text-slate-300">正常</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                v-model="form.is_active"
                :value="false"
                class="status-radio"
              />
              <span class="text-sm text-slate-300">禁用</span>
            </label>
          </div>
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
            {{ form.id ? '保存修改' : '确认创建' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPwdDialogVisible"
      title="重置密码"
      width="420px"
      :close-on-click-modal="false"
      @close="handleCancelResetPassword"
      class="user-dialog"
      destroy-on-close
    >
      <div class="space-y-5">
        <div class="form-group">
          <label class="form-label">
            <User class="w-4 h-4" />
            用户名
          </label>
          <el-input
            v-model="resetPwdForm.username"
            disabled
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">
            <Lock class="w-4 h-4" />
            新密码 <span class="text-red-400">*</span>
          </label>
          <el-input
            v-model="resetPwdForm.new_password"
            type="password"
            placeholder="请输入新密码"
            show-password
            class="form-input"
          />
          <p class="text-xs text-slate-400 mt-1">密码长度不少于6位</p>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3 pt-2">
          <el-button @click="handleCancelResetPassword" size="large">取消</el-button>
          <el-button
            type="primary"
            @click="submitResetPassword"
            size="large"
            class="submit-btn"
          >
            确认重置
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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #a78bfa, #c084fc);
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
  border-color: #8b5cf6;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
}

/* ============================================
   筛选区域样式
   ============================================ */
.filter-select {
  --el-input-bg-color: rgba(255, 255, 255, 0.05);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-input-hover-border-color: rgba(139, 92, 246, 0.5);
  --el-input-focus-border-color: #8b5cf6;
  --el-text-color-placeholder: rgba(255, 255, 255, 0.3);
  --el-fill-color-blank: rgba(255, 255, 255, 0.05);
  --el-bg-color: rgba(15, 23, 42, 0.95);
  --el-text-color-regular: rgba(255, 255, 255, 0.85);
  --el-text-color-secondary: rgba(255, 255, 255, 0.65);
  --el-border-color: rgba(255, 255, 255, 0.1);
}

:deep(.filter-select .el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  border-radius: 12px;
  transition: all 0.3s ease;
}

:deep(.filter-select .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.5) inset;
  background-color: rgba(255, 255, 255, 0.06);
}

:deep(.filter-select .el-input__wrapper.is-focus) {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px #8b5cf6 inset !important;
}

:deep(.filter-select .el-input__inner) {
  color: #fff;
}

:deep(.filter-select .el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

/* 筛选下拉面板样式 */
:deep(.el-select-dropdown) {
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
}

:deep(.el-select-dropdown__item) {
  color: rgba(255, 255, 255, 0.85);
  background: transparent;
  transition: all 0.2s;
}

:deep(.el-select-dropdown__item:hover) {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

:deep(.el-select-dropdown__item.is-selected) {
  background: rgba(139, 92, 246, 0.25);
  color: #a78bfa;
}

/* 按钮样式 */
.action-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
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
  background: linear-gradient(135deg, #8b5cf6, #a855f7);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

/* 角色徽章 */
.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  border-width: 1px;
  border-style: solid;
}

/* 状态徽章 */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-inactive {
  background: rgba(156, 163, 175, 0.15);
  color: #9ca3af;
  border: 1px solid rgba(156, 163, 175, 0.3);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 6px;
}

.dot-active {
  background: #34d399;
  box-shadow: 0 0 6px rgba(52, 211, 153, 0.5);
}

.dot-inactive {
  background: #9ca3af;
}

/* 操作图标按钮 */
.action-icon-btn {
  padding: 6px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.5);
  transition: all 0.2s;
}

.action-icon-btn:hover:not(:disabled) {
  background: rgba(139, 92, 246, 0.15);
  color: #c4b5fd;
}

.action-icon-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
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
  border-color: rgba(139, 92, 246, 0.5);
}

/* 对话框样式 */
:deep(.user-dialog) {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.user-dialog .el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 24px;
}

:deep(.user-dialog .el-dialog__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.user-dialog .el-dialog__body) {
  padding: 24px;
  background: #0f172a;
}

:deep(.user-dialog .el-dialog__footer) {
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

.form-input :deep(.el-input__wrapper),
.form-input :deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  transition: all 0.3s ease;
}

.form-input :deep(.el-input__wrapper:hover),
.form-input :deep(.el-select .el-input__wrapper:hover) {
  border-color: rgba(139, 92, 246, 0.5);
}

.form-input :deep(.el-input__wrapper.is-focus),
.form-input :deep(.el-select .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: #8b5cf6;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
}

.form-input :deep(.el-input__inner),
.form-input :deep(.el-select__selected-item) {
  color: #fff;
}

.form-input :deep(.el-input__inner::placeholder),
.form-input :deep(.el-select__placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.form-input :deep(.el-input__disabled .el-input__inner) {
  color: #64748b;
  background: rgba(255, 255, 255, 0.02);
}

.form-input :deep(.el-select__caret) {
  color: rgba(255, 255, 255, 0.5);
}

/* 单选按钮样式 */
.status-radio {
  appearance: none;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(139, 92, 246, 0.4);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.status-radio:checked {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border-color: #8b5cf6;
}

.status-radio:checked::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #fff;
  border-radius: 50%;
}

/* 提交按钮 */
.submit-btn {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border: none;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}
</style>

<style>
/* ============================================
   用户管理 - 下拉选项面板全局样式
   ============================================ */
/* 筛选下拉面板 - 紫色系 */
.user-select-dropdown.el-select-dropdown {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.user-select-dropdown .el-select-dropdown__item {
  color: rgba(255, 255, 255, 0.85) !important;
  background: transparent !important;
  transition: all 0.2s;
}

.user-select-dropdown .el-select-dropdown__item:hover {
  background: rgba(139, 92, 246, 0.15) !important;
  color: #c4b5fd !important;
}

.user-select-dropdown .el-select-dropdown__item.is-selected {
  background: rgba(139, 92, 246, 0.25) !important;
  color: #c4b5fd !important;
}

.user-select-dropdown .el-select-dropdown__item.is-disabled {
  color: rgba(255, 255, 255, 0.25) !important;
}

/* 滚动条样式 */
.user-select-dropdown .el-scrollbar__bar {
  background: rgba(255, 255, 255, 0.1);
}

.user-select-dropdown .el-scrollbar__thumb {
  background: rgba(139, 92, 246, 0.5);
  border-radius: 3px;
}

.user-select-dropdown .el-scrollbar__thumb:hover {
  background: rgba(139, 92, 246, 0.7);
}

/* 空状态 */
.user-select-dropdown .el-select-dropdown__empty {
  color: rgba(255, 255, 255, 0.4) !important;
}
</style>
