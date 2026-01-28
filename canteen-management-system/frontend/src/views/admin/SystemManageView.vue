<template>
  <div class="system-manage-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon :size="24"><Setting /></el-icon>
        系统管理
      </h2>
      <p class="page-desc">管理用户账号、角色权限和系统基础配置</p>
    </div>

    <!-- 主容器：左侧导航 + 右侧内容 -->
    <div class="main-container">
      <!-- 左侧导航 -->
      <div class="side-nav">
        <div
          v-for="tab in tabs"
          :key="tab.key"
          :class="['nav-item', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          <el-icon :size="20">
            <component :is="tab.icon" />
          </el-icon>
          <span>{{ tab.label }}</span>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="content-area">
        <!-- 用户账号管理 -->
        <div v-show="activeTab === 'users'" class="tab-content">
          <!-- 操作栏 -->
          <div class="action-bar">
            <el-button type="primary" :icon="Plus" @click="handleAddUser">
              新增账号
            </el-button>
            <div class="search-area">
              <el-select
                v-model="userFilters.role"
                placeholder="角色筛选"
                clearable
                style="width: 120px"
                @change="loadUserList"
              >
                <el-option label="管理员" value="ADMIN" />
                <el-option label="员工" value="EMPLOYEE" />
              </el-select>
              <el-select
                v-model="userFilters.status"
                placeholder="状态筛选"
                clearable
                style="width: 120px"
                @change="loadUserList"
              >
                <el-option label="启用" value="ENABLED" />
                <el-option label="禁用" value="DISABLED" />
              </el-select>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索用户名"
                :prefix-icon="Search"
                clearable
                style="width: 200px"
                @clear="handleSearch"
                @keyup.enter="handleSearch"
              />
              <el-button :icon="Search" @click="handleSearch">查询</el-button>
            </div>
          </div>

          <!-- 用户列表表格 -->
          <el-table
            v-loading="userLoading"
            :data="userList"
            stripe
            class="data-table"
            :header-cell-style="{ background: '#FFF8F0', color: '#333' }"
          >
            <el-table-column prop="id" label="ID" width="70" align="center" />
            <el-table-column prop="username" label="用户名" min-width="140" />
            <el-table-column prop="role" label="角色" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="row.role === 'ADMIN' ? 'warning' : 'primary'" size="small">
                  {{ row.role === 'ADMIN' ? '管理员' : '员工' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="employee_name" label="关联员工" min-width="120">
              <template #default="{ row }">
                {{ row.employee_name || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="90" align="center">
              <template #default="{ row }">
                <el-tag :type="row.status === 'ENABLED' ? 'success' : 'info'" size="small">
                  {{ row.status === 'ENABLED' ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="170" align="center" />
            <el-table-column label="操作" width="180" fixed="right" align="center">
              <template #default="{ row }">
                <el-button link type="primary" size="small" @click="handleEditUser(row)">
                  编辑
                </el-button>
                <el-button link type="danger" size="small" @click="handleDeleteUser(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="userPagination.page"
              v-model:page-size="userPagination.pageSize"
              :page-sizes="[10, 20, 50]"
              :total="userPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadUserList"
              @current-change="loadUserList"
            />
          </div>
        </div>

        <!-- 角色权限管理 -->
        <div v-show="activeTab === 'roles'" class="tab-content">
          <div class="roles-container">
            <div
              v-for="role in roleList"
              :key="role.value"
              class="role-card"
            >
              <div class="role-icon" :class="`role-${role.value.toLowerCase()}`">
                <el-icon :size="32">
                  <component :is="role.icon" />
                </el-icon>
              </div>
              <h3 class="role-name">{{ role.label }}</h3>
              <p class="role-desc">{{ role.description }}</p>
              <div class="role-permissions">
                <span class="perm-title">权限范围：</span>
                <ul>
                  <li v-for="perm in role.permissions" :key="perm">{{ perm }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统设置 -->
        <div v-show="activeTab === 'settings'" class="tab-content">
          <el-form
            ref="settingsFormRef"
            :model="settingsForm"
            label-width="140px"
            class="settings-form"
          >
            <div class="form-section">
              <h4 class="section-title">
                <el-icon><Clock /></el-icon>
                考勤规则设置
              </h4>

              <el-form-item label="迟到宽限时间">
                <el-input-number
                  v-model="settingsForm.grace_period_minutes"
                  :min="0"
                  :max="60"
                  :step="1"
                  controls-position="right"
                />
                <span class="unit-text">分钟</span>
                <span class="help-text">
                  签到时间在班次开始后此时间内不算迟到
                </span>
              </el-form-item>

              <el-form-item label="早退宽限时间">
                <el-input-number
                  v-model="settingsForm.early_leave_grace_minutes"
                  :min="0"
                  :max="60"
                  :step="1"
                  controls-position="right"
                />
                <span class="unit-text">分钟</span>
                <span class="help-text">
                  签退时间在班次结束前此时间内不算早退
                </span>
              </el-form-item>

              <el-form-item label="迟到扣款金额">
                <el-input-number
                  v-model="settingsForm.late_deduction"
                  :min="0"
                  :max="500"
                  :step="10"
                  controls-position="right"
                />
                <span class="unit-text">元/次</span>
              </el-form-item>

              <el-form-item label="缺卡扣款金额">
                <el-input-number
                  v-model="settingsForm.missing_deduction"
                  :min="0"
                  :max="500"
                  :step="10"
                  controls-position="right"
                />
                <span class="unit-text">元/次</span>
              </el-form-item>
            </div>

            <div class="form-section">
              <h4 class="section-title">
                <el-icon><Calendar /></el-icon>
                薪资计算设置
              </h4>

              <el-form-item label="月计薪天数">
                <el-input-number
                  v-model="settingsForm.days_per_month"
                  :min="20"
                  :max="23"
                  :step="0.25"
                  :precision="2"
                  controls-position="right"
                />
                <span class="unit-text">天</span>
                <span class="help-text">用于计算日工资</span>
              </el-form-item>

              <el-form-item label="日工作小时数">
                <el-input-number
                  v-model="settingsForm.hours_per_day"
                  :min="4"
                  :max="12"
                  :step="0.5"
                  controls-position="right"
                />
                <span class="unit-text">小时</span>
                <span class="help-text">用于计算时薪</span>
              </el-form-item>

              <el-form-item label="加班工资倍率">
                <el-input-number
                  v-model="settingsForm.overtime_rate"
                  :min="1"
                  :max="3"
                  :step="0.5"
                  controls-position="right"
                />
                <span class="unit-text">倍</span>
                <span class="help-text">加班费 = 时薪 × 倍率 × 加班小时数</span>
              </el-form-item>
            </div>

            <div class="form-actions">
              <el-button type="primary" :loading="settingsSaving" @click="handleSaveSettings">
                保存设置
              </el-button>
              <el-button @click="handleResetSettings">重置默认</el-button>
            </div>
          </el-form>
>
        </div>
      </div>
    </div>

    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      v-model="userDialogVisible"
      :title="userDialogTitle"
      width="550px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="userFormRef"
        :model="userFormData"
        :rules="userFormRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="userFormData.username"
            placeholder="请输入用户名"
            :disabled="isEditUser"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="userFormData.password"
            type="password"
            :placeholder="isEditUser ? '留空则不修改密码' : '请输入密码'"
            show-password
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userFormData.role" placeholder="请选择角色">
            <el-option label="管理员" value="ADMIN" />
            <el-option label="员工" value="EMPLOYEE" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联员工" prop="employee">
          <el-select
            v-model="userFormData.employee"
            placeholder="请选择关联员工（可选）"
            clearable
            filterable
          >
            <el-option
              v-for="emp in employeeOptions"
              :key="emp.id"
              :label="`${emp.name} - ${emp.position_display}`"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="userFormData.status">
            <el-radio value="ENABLED">启用</el-radio>
            <el-radio value="DISABLED">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="userSubmitting" @click="handleSubmitUser">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  User,
  Lock,
  Tools,
  Plus,
  Search,
  Clock,
  Calendar,
  Avatar,
  Key
} from '@element-plus/icons-vue'
import {
  getUserList,
  createUser,
  updateUser,
  deleteUser,
  getSystemSettings,
  updateSystemSettings
} from '@/api/accounts'
import { getEmployeeList } from '@/api/employee'

// 标签页
const tabs = [
  { key: 'users', label: '用户账号', icon: User },
  { key: 'roles', label: '角色权限', icon: Lock },
  { key: 'settings', label: '系统设置', icon: Tools }
]

const activeTab = ref('users')

// ===== 用户账号管理 =====
const userLoading = ref(false)
const userList = ref([])
const searchKeyword = ref('')
const userFilters = reactive({
  role: '',
  status: ''
})
const userPagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 用户对话框
const userDialogVisible = ref(false)
const isEditUser = ref(false)
const userSubmitting = ref(false)
const userDialogTitle = computed(() => (isEditUser.value ? '编辑用户账号' : '新增用户账号'))
const userFormRef = ref(null)
const userFormData = reactive({
  username: '',
  password: '',
  role: 'EMPLOYEE',
  employee: null,
  status: 'ENABLED'
})
const userFormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: !isEditUser.value, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}
const employeeOptions = ref([])

// 加载用户列表
const loadUserList = async () => {
  userLoading.value = true
  try {
    const params = {
      page: userPagination.page,
      page_size: userPagination.pageSize,
      ordering: '-created_at'
    }
    if (userFilters.role) params.role = userFilters.role
    if (userFilters.status) params.status = userFilters.status
    if (searchKeyword.value) params.search = searchKeyword.value

    const res = await getUserList(params)
    if (res.code === 200) {
      userList.value = res.data.results || res.data
      userPagination.total = res.data.count || res.data.length
    } else {
      ElMessage.error(res.message || '加载用户列表失败')
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
  } finally {
    userLoading.value = false
  }
}

// 加载员工选项
const loadEmployeeOptions = async () => {
  try {
    const res = await getEmployeeList({ page_size: 1000, status: 'ACTIVE' })
    if (res.code === 200) {
      employeeOptions.value = res.data.results || res.data
    }
  } catch (error) {
    console.error('加载员工列表失败:', error)
  }
}

// 搜索用户
const handleSearch = () => {
  userPagination.page = 1
  loadUserList()
}

// 新增用户
const handleAddUser = () => {
  isEditUser.value = false
  resetUserForm()
  userDialogVisible.value = true
}

// 编辑用户
const handleEditUser = (row) => {
  isEditUser.value = true
  Object.assign(userFormData, {
    id: row.id,
    username: row.username,
    password: '',
    role: row.role,
    employee: row.employee,
    status: row.status
  })
  userDialogVisible.value = true
}

// 删除用户
const handleDeleteUser = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户账号 "${row.username}" 吗？删除后该用户将无法登录系统。`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
    .then(async () => {
      try {
        const res = await deleteUser(row.id)
        if (res.code === 200) {
          ElMessage.success('删除成功')
          loadUserList()
        } else {
          ElMessage.error(res.message || '删除失败')
        }
      } catch (error) {
        console.error('删除用户失败:', error)
        ElMessage.error('删除用户失败')
      }
    })
    .catch(() => {})
}

// 提交用户表单
const handleSubmitUser = () => {
  userFormRef.value.validate(async (valid) => {
    if (!valid) return

    userSubmitting.value = true
    try {
      const data = { ...userFormData }
      delete data.id

      // 编辑模式下如果密码为空则不传递密码字段
      if (isEditUser.value && !data.password) {
        delete data.password
      }

      let res
      if (isEditUser.value) {
        res = await updateUser(userFormData.id, data)
      } else {
        res = await createUser(data)
      }

      if (res.code === 200 || res.code === 201) {
        ElMessage.success(isEditUser.value ? '更新成功' : '创建成功')
        userDialogVisible.value = false
        loadUserList()
      } else {
        ElMessage.error(res.message || '操作失败')
      }
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    } finally {
      userSubmitting.value = false
    }
  })
}

// 重置用户表单
const resetUserForm = () => {
  Object.assign(userFormData, {
    username: '',
    password: '',
    role: 'EMPLOYEE',
    employee: null,
    status: 'ENABLED'
  })
  userFormRef.value?.clearValidate()
}

// ===== 角色权限管理 =====
const roleList = ref([
  {
    value: 'ADMIN',
    label: '管理员',
    icon: Avatar,
    description: '拥有系统全部管理权限，可进行所有操作',
    permissions: [
      '员工档案管理',
      '排班计划制定',
      '考勤记录查看与修正',
      '请假申请审批',
      '薪资计算与发放',
      '数据统计分析',
      '系统配置管理'
    ]
  },
  {
    value: 'EMPLOYEE',
    label: '普通员工',
    icon: User,
    description: '仅可查看和操作个人相关功能',
    permissions: [
      '查看个人信息',
      '每日签到签退',
      '查看个人排班',
      '提交请假申请',
      '提交调班申请',
      '查看个人薪资',
      '提交申诉'
    ]
  }
])

// ===== 系统设置 =====
const settingsFormRef = ref(null)
const settingsSaving = ref(false)
const settingsForm = reactive({
  grace_period_minutes: 5,
  early_leave_grace_minutes: 5,
  late_deduction: 20,
  missing_deduction: 50,
  days_per_month: 21.75,
  hours_per_day: 8,
  overtime_rate: 1.5
})

// 加载系统设置
const loadSystemSettings = async () => {
  try {
    const res = await getSystemSettings()
    if (res.code === 200 && res.data) {
      Object.assign(settingsForm, res.data)
    }
  } catch (error) {
    console.error('加载系统设置失败:', error)
  }
}

// 保存系统设置
const handleSaveSettings = () => {
  settingsSaving.value = true
  updateSystemSettings(settingsForm)
    .then((res) => {
      if (res.code === 200) {
        ElMessage.success('设置保存成功')
      } else {
        ElMessage.error(res.message || '保存失败')
      }
    })
    .catch((error) => {
      console.error('保存设置失败:', error)
      ElMessage.error('保存设置失败')
    })
    .finally(() => {
      settingsSaving.value = false
    })
}

// 重置系统设置
const handleResetSettings = () => {
  ElMessageBox.confirm('确定要重置为默认设置吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      Object.assign(settingsForm, {
        grace_period_minutes: 5,
        early_leave_grace_minutes: 5,
        late_deduction: 20,
        missing_deduction: 50,
        days_per_month: 21.75,
        hours_per_day: 8,
        overtime_rate: 1.5
      })
      ElMessage.success('已重置为默认设置')
    })
    .catch(() => {})
}

// 初始化
onMounted(() => {
  loadUserList()
  loadEmployeeOptions()
  loadSystemSettings()
})
</script>

<style scoped>
.system-manage-view {
  background-color: transparent;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px 0;
  font-size: 26px;
  font-weight: 700;
  background: linear-gradient(135deg, #FF6B35 0%, #F7C52D 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-desc {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

/* 主容器 */
.main-container {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

/* 左侧导航 */
.side-nav {
  width: 160px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.12);
  overflow: hidden;
  flex-shrink: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #606266;
  font-weight: 500;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: linear-gradient(90deg, rgba(255, 107, 53, 0.08) 0%, transparent 100%);
  color: #FF6B35;
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(255, 107, 53, 0.15) 0%, transparent 100%);
  color: #FF6B35;
  border-left-color: #FF6B35;
}

.nav-item .el-icon {
  flex-shrink: 0;
}

/* 右侧内容区 */
.content-area {
  flex: 1;
  min-height: 500px;
}

.tab-content {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.12);
}

/* 操作栏 */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-area {
  display: flex;
  gap: 10px;
}

/* 数据表格 */
.data-table {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 角色卡片 */
.roles-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.role-card {
  position: relative;
  padding: 28px;
  background: linear-gradient(145deg, #ffffff 0%, #fff9f5 100%);
  border-radius: 20px;
  border: 2px solid transparent;
  background-clip: padding-box;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.role-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 20px;
  padding: 2px;
  background: linear-gradient(135deg, #FF6B35, #F7C52D, #4CAF50);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.role-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(255, 107, 53, 0.2);
}

.role-card:hover::before {
  opacity: 1;
}

.role-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  margin-bottom: 16px;
  color: white;
}

.role-admin {
  background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
}

.role-employee {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
}

.role-name {
  margin: 0 0 10px 0;
  font-size: 20px;
  font-weight: 700;
  color: #303133;
}

.role-desc {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #909399;
  line-height: 1.6;
}

.role-permissions {
  padding-top: 16px;
  border-top: 1px dashed #e4e7ed;
}

.perm-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 10px;
}

.role-permissions ul {
  margin: 0;
  padding-left: 18px;
  list-style: none;
}

.role-permissions li {
  position: relative;
  padding-left: 12px;
  margin-bottom: 6px;
  font-size: 13px;
  color: #606266;
}

.role-permissions li::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 8px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #FF6B35;
}

/* 系统设置表单 */
.settings-form {
  max-width: 650px;
}

.form-section {
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
  border-radius: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px 0;
  font-size: 17px;
  font-weight: 700;
  color: #FF6B35;
  padding-bottom: 12px;
  border-bottom: 2px solid rgba(255, 107, 53, 0.2);
}

.unit-text {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}

.help-text {
  margin-left: 16px;
  color: #9ca3af;
  font-size: 13px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding: 24px;
  background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
  border-radius: 16px;
}

/* 主题样式 */
:deep(.el-button--primary) {
  background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 107, 53, 0.4);
}

:deep(.el-button--primary:active) {
  transform: translateY(0);
}

:deep(.el-input-number) {
  border-radius: 8px;
}

:deep(.el-input-number .el-input__inner) {
  border-radius: 8px;
  border-color: #e4e7ed;
  transition: all 0.3s ease;
}

:deep(.el-input-number .el-input__inner:focus) {
  border-color: #FF6B35;
}

:deep(.el-table) {
  border-radius: 12px;
}

:deep(.el-table th) {
  font-weight: 600;
}

:deep(.el-tag--warning) {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border-color: #FFB74D;
  color: #E65100;
}

:deep(.el-tag--success) {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border-color: #81C784;
  color: #2E7D32;
}

:deep(.el-tag--primary) {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-color: #64B5F6;
  color: #1565C0;
}

:deep(.el-tag--info) {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  border-color: #BDBDBD;
  color: #616161;
}

:deep(.el-dialog) {
  border-radius: 20px;
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #FF6B35 0%, #F7C52D 100%);
  border-radius: 20px 20px 0 0;
  padding: 24px;
}

:deep(.el-dialog__title) {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 20px;
}

:deep(.el-dialog__body) {
  padding: 28px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }

  .side-nav {
    width: 100%;
    display: flex;
    overflow-x: auto;
  }

  .nav-item {
    flex-shrink: 0;
    border-left: none;
    border-bottom: 3px solid transparent;
  }

  .nav-item.active {
    border-left: none;
    border-bottom-color: #FF6B35;
  }
}
</style>
