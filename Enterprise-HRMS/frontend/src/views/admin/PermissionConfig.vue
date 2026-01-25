<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getRolePermissionList,
  getRolePermissionDetail,
  updateRolePermission,
  initializePermissions
} from '../../api/permission'
import { useAuthStore } from '../../stores/auth'

// 响应式状态
const loading = ref(false)
const permissionList = ref([])
const selectedPermission = ref(null)
const activeRole = ref(null)
const authStore = useAuthStore()
const saving = ref(false)

// 角色选项
const roleOptions = [
  { value: 'employee', label: '普通员工' },
  { value: 'hr', label: '人事专员' },
  { value: 'admin', label: '系统管理员' }
]

// 角色颜色
const roleColors = {
  employee: 'info',
  hr: 'warning',
  admin: 'danger'
}

// 菜单选项
const menuOptions = [
  { value: 'dashboard', label: '数据概览', icon: 'Dashboard' },
  { value: 'employeeDashboard', label: '员工首页', icon: 'HomeFilled' },
  { value: 'dataCenter', label: '数据中心', icon: 'DataAnalysis' },
  { value: 'employees', label: '员工管理', icon: 'User' },
  { value: 'departments', label: '部门管理', icon: 'OfficeBuilding' },
  { value: 'attendance', label: '考勤管理', icon: 'Clock' },
  { value: 'salary', label: '薪资管理', icon: 'Money' },
  { value: 'approval', label: '审批中心', icon: 'Tickets' },
  { value: 'onboarding', label: '入职管理', icon: 'UserFilled' },
  { value: 'users', label: '账号管理', icon: 'Lock' },
  { value: 'notices', label: '系统公告', icon: 'Bell' },
  { value: 'noticeManagement', label: '公告管理', icon: 'EditPen' },
  { value: 'performanceReview', label: '绩效评估', icon: 'TrendCharts' },
  { value: 'myPerformance', label: '我的绩效', icon: 'Odometer' },
  { value: 'profile', label: '个人信息', icon: 'User' },
  { value: 'permissionConfig', label: '权限配置', icon: 'Setting' }
]

// 按钮权限选项
const buttonOptions = [
  { value: 'checkIn', label: '签到', description: '考勤签到按钮' },
  { value: 'checkOut', label: '签退', description: '考勤签退按钮' },
  { value: 'applyLeave', label: '请假申请', description: '提交请假申请按钮' },
  { value: 'applyOvertime', label: '加班申请', description: '提交加班申请按钮' },
  { value: 'viewSalary', label: '查看薪资', description: '查看薪资记录按钮' },
  { value: 'createEmployee', label: '创建员工', description: '新增员工按钮' },
  { value: 'editEmployee', label: '编辑员工', description: '编辑员工按钮' },
  { value: 'deleteEmployee', label: '删除员工', description: '删除员工按钮' },
  { value: 'approveLeave', label: '审批请假', description: '审批请假申请按钮' },
  { value: 'approveOvertime', label: '审批加班', description: '审批加班申请按钮' },
  { value: 'calculateSalary', label: '计算薪资', description: '薪资计算按钮' },
  { value: 'publishSalary', label: '发布薪资', description: '薪资发布按钮' },
  { value: 'createNotice', label: '创建公告', description: '创建公告按钮' },
  { value: 'manageUsers', label: '管理用户', description: '用户管理按钮' },
  { value: 'resetPassword', label: '重置密码', description: '密码重置按钮' },
  { value: 'configurePermissions', label: '配置权限', description: '权限配置按钮' }
]

// 数据权限选项
const dataPermissionOptions = [
  { value: 'all', label: '全部数据', description: '可以访问所有数据' },
  { value: 'department', label: '本部门数据', description: '只能访问本部门数据' },
  { value: 'self', label: '仅本人', description: '只能访问自己的数据' }
]

// 编辑表单
const editForm = reactive({
  menu_permissions: [],
  button_permissions: [],
  data_permission: 'self',
  attendance_permission: 'self',
  salary_permission: 'self',
  can_access_datacenter: false,
  can_access_performance: false
})

// 获取权限配置列表
const fetchPermissionList = async () => {
  loading.value = true
  try {
    const res = await getRolePermissionList()
    permissionList.value = res.data?.data || res.data?.results || []
  } catch (error) {
    console.error('获取权限配置列表失败:', error)
    ElMessage.error('获取权限配置列表失败')
  } finally {
    loading.value = false
  }
}

// 选择角色查看配置
const selectRole = async (role) => {
  activeRole.value = role
  const permission = permissionList.value.find(p => p.role === role)

  if (permission) {
    selectedPermission.value = permission
    // 初始化编辑表单
    Object.assign(editForm, {
      menu_permissions: [...(permission.menu_permissions || [])],
      button_permissions: [...(permission.button_permissions || [])],
      data_permission: permission.data_permission || 'self',
      attendance_permission: permission.attendance_permission || 'self',
      salary_permission: permission.salary_permission || 'self',
      can_access_datacenter: permission.can_access_datacenter || false,
      can_access_performance: permission.can_access_performance || false
    })
  } else {
    selectedPermission.value = null
  }
}

// 保存权限配置
const savePermission = async () => {
  if (!selectedPermission.value) return

  const id = selectedPermission.value.id
  saving.value = true
  try {
    await updateRolePermission(id, editForm)
    ElMessage.success('权限配置保存成功')
    await fetchPermissionList()
    // 重新加载当前角色的配置
    selectRole(activeRole.value)
    // 如果保存的是当前登录用户的角色，刷新前端权限缓存
    if (authStore.user?.role === activeRole.value) {
      await authStore.fetchRolePermissions()
    }
  } catch (error) {
    console.error('保存权限配置失败:', error)
    ElMessage.error(error.response?.data?.message || '保存权限配置失败')
  } finally {
    saving.value = false
  }
}

// 重置为默认配置
const resetToDefault = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重置当前角色的权限配置为默认值吗？此操作不可撤销。',
      '重置确认',
      {
        confirmButtonText: '确定重置',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    // 重新初始化（通过获取默认值）
    const permission = permissionList.value.find(p => p.role === activeRole.value)
    if (permission) {
      // 获取默认配置
      const defaults = getDefaultConfig(activeRole.value)
      await updateRolePermission(permission.id, defaults)
      ElMessage.success('已重置为默认配置')
      await fetchPermissionList()
      selectRole(activeRole.value)
      // 如果重置的是当前登录用户的角色，刷新前端权限缓存
      if (authStore.user?.role === activeRole.value) {
        await authStore.fetchRolePermissions()
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重置失败:', error)
      ElMessage.error('重置失败')
    }
  }
}

// 获取默认配置
const getDefaultConfig = (role) => {
  const defaults = {
    employee: {
      menu_permissions: ['dashboard', 'attendance', 'salary', 'approval', 'notices', 'myPerformance', 'profile'],
      button_permissions: ['checkIn', 'checkOut', 'applyLeave', 'applyOvertime', 'viewSalary'],
      data_permission: 'self',
      attendance_permission: 'self',
      salary_permission: 'self',
      can_access_datacenter: false,
      can_access_performance: true
    },
    hr: {
      menu_permissions: ['dashboard', 'employees', 'departments', 'attendance', 'salary', 'approval', 'onboarding', 'notices', 'noticeManagement', 'performanceReview', 'dataCenter', 'profile'],
      button_permissions: ['createEmployee', 'editEmployee', 'deleteEmployee', 'approveLeave', 'approveOvertime', 'calculateSalary', 'publishSalary', 'createNotice'],
      data_permission: 'department',
      attendance_permission: 'all',
      salary_permission: 'all',
      can_access_datacenter: true,
      can_access_performance: true
    },
    admin: {
      menu_permissions: ['dashboard', 'employees', 'departments', 'attendance', 'salary', 'approval', 'onboarding', 'users', 'notices', 'noticeManagement', 'performanceReview', 'dataCenter', 'profile', 'permissionConfig'],
      button_permissions: ['createEmployee', 'editEmployee', 'deleteEmployee', 'approveLeave', 'approveOvertime', 'calculateSalary', 'publishSalary', 'createNotice', 'manageUsers', 'resetPassword', 'configurePermissions'],
      data_permission: 'all',
      attendance_permission: 'all',
      salary_permission: 'all',
      can_access_datacenter: true,
      can_access_performance: true
    }
  }
  return defaults[role] || defaults.employee
}

// 初始化默认权限
const handleInitialize = async () => {
  try {
    await ElMessageBox.confirm(
      '此操作将初始化所有角色的默认权限配置，已有的配置会被更新。是否继续？',
      '初始化确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    loading.value = true
    await initializePermissions()
    ElMessage.success('权限配置初始化成功')
    await fetchPermissionList()
    if (activeRole.value) {
      selectRole(activeRole.value)
    }
    // 刷新当前用户的权限缓存
    await authStore.fetchRolePermissions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('初始化失败:', error)
      ElMessage.error('初始化失败')
    }
  } finally {
    loading.value = false
  }
}

// 获取角色显示名称
const getRoleLabel = (role) => {
  const option = roleOptions.find(o => o.value === role)
  return option ? option.label : role
}

// 获取菜单显示名称
const getMenuLabel = (menu) => {
  const option = menuOptions.find(o => o.value === menu)
  return option ? option.label : menu
}

// 获取按钮显示名称
const getButtonLabel = (btn) => {
  const option = buttonOptions.find(o => o.value === btn)
  return option ? option.label : btn
}

// 初始化
onMounted(() => {
  fetchPermissionList()
})
</script>

<template>
  <div class="permission-config">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h2 class="page-title">角色权限配置</h2>
        <p class="page-desc">管理系统各角色的菜单权限、按钮权限和数据权限</p>
      </div>
      <div class="header-actions">
        <el-button type="info" @click="handleInitialize">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          初始化默认权限
        </el-button>
      </div>
    </div>

    <div class="config-container">
      <!-- 角色列表 -->
      <div class="role-list-section">
        <el-card class="role-list-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">角色列表</span>
            </div>
          </template>

          <div class="role-list">
            <div
              v-for="permission in permissionList"
              :key="permission.role"
              class="role-item"
              :class="{ active: activeRole === permission.role }"
              @click="selectRole(permission.role)"
            >
              <div class="role-info">
                <el-tag :type="roleColors[permission.role]" size="small">
                  {{ getRoleLabel(permission.role) }}
                </el-tag>
                <span class="role-count">
                  {{ permission.menu_permissions?.length || 0 }} 个菜单
                </span>
              </div>
              <el-icon class="arrow-icon">
                <ArrowRight />
              </el-icon>
            </div>

            <el-empty v-if="permissionList.length === 0 && !loading" description="暂无权限配置">
              <el-button type="primary" size="small" @click="handleInitialize">
                初始化权限配置
              </el-button>
            </el-empty>
          </div>
        </el-card>
      </div>

      <!-- 权限配置详情 -->
      <div class="permission-detail-section">
        <el-card v-if="activeRole" class="permission-detail-card" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                {{ getRoleLabel(activeRole) }} 权限配置
              </span>
              <div class="header-actions">
                <el-button type="warning" size="small" @click="resetToDefault">
                  重置默认
                </el-button>
                <el-button type="primary" size="small" :loading="saving" @click="savePermission">
                  保存配置
                </el-button>
              </div>
            </div>
          </template>

          <div class="permission-form">
            <!-- 菜单权限配置 -->
            <div class="form-section">
              <h4 class="section-title">
                <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
                菜单权限
              </h4>
              <p class="section-desc">选择该角色可以访问的菜单</p>
              <el-checkbox-group v-model="editForm.menu_permissions" class="permission-checkbox-group">
                <div class="menu-grid">
                  <div
                    v-for="menu in menuOptions"
                    :key="menu.value"
                    class="menu-item"
                  >
                    <el-checkbox :label="menu.value" :value="menu.value">
                      <span class="menu-label">{{ menu.label }}</span>
                    </el-checkbox>
                  </div>
                </div>
              </el-checkbox-group>
            </div>

            <!-- 按钮权限配置 -->
            <div class="form-section">
              <h4 class="section-title">
                <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M12 1v6m0 6v10M1 12h6m6 0h10"/>
                </svg>
                按钮权限
              </h4>
              <p class="section-desc">选择该角色可以看到的操作按钮</p>
              <el-checkbox-group v-model="editForm.button_permissions" class="permission-checkbox-group">
                <div class="button-grid">
                  <div
                    v-for="btn in buttonOptions"
                    :key="btn.value"
                    class="button-item"
                  >
                    <el-checkbox :label="btn.value" :value="btn.value">
                      <span class="btn-label">{{ btn.label }}</span>
                      <span class="btn-desc">{{ btn.description }}</span>
                    </el-checkbox>
                  </div>
                </div>
              </el-checkbox-group>
            </div>

            <!-- 数据权限配置 -->
            <div class="form-section">
              <h4 class="section-title">
                <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
                数据权限
              </h4>
              <p class="section-desc">设置该角色可以访问的数据范围</p>

              <div class="data-permission-group">
                <div class="permission-row">
                  <label>通用数据权限</label>
                  <el-radio-group v-model="editForm.data_permission">
                    <el-radio-button
                      v-for="opt in dataPermissionOptions"
                      :key="opt.value"
                      :label="opt.value"
                    >
                      {{ opt.label }}
                    </el-radio-button>
                  </el-radio-group>
                  <span class="permission-hint">
                    {{ dataPermissionOptions.find(o => o.value === editForm.data_permission)?.description }}
                  </span>
                </div>

                <div class="permission-row">
                  <label>考勤数据权限</label>
                  <el-radio-group v-model="editForm.attendance_permission">
                    <el-radio-button
                      v-for="opt in dataPermissionOptions"
                      :key="opt.value"
                      :label="opt.value"
                    >
                      {{ opt.label }}
                    </el-radio-button>
                  </el-radio-group>
                </div>

                <div class="permission-row">
                  <label>薪资数据权限</label>
                  <el-radio-group v-model="editForm.salary_permission">
                    <el-radio-button
                      v-for="opt in dataPermissionOptions"
                      :key="opt.value"
                      :label="opt.value"
                    >
                      {{ opt.label }}
                    </el-radio-button>
                  </el-radio-group>
                </div>
              </div>
            </div>

            <!-- 功能权限配置 -->
            <div class="form-section">
              <h4 class="section-title">
                <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                功能权限
              </h4>
              <p class="section-desc">设置该角色可以使用的高级功能</p>

              <div class="feature-permission-group">
                <div class="feature-item">
                  <div class="feature-info">
                    <span class="feature-name">访问数据中心</span>
                    <span class="feature-desc">查看企业数据统计分析</span>
                  </div>
                  <el-switch v-model="editForm.can_access_datacenter" />
                </div>

                <div class="feature-item">
                  <div class="feature-info">
                    <span class="feature-name">访问绩效管理</span>
                    <span class="feature-desc">查看和参与绩效评估流程</span>
                  </div>
                  <el-switch v-model="editForm.can_access_performance" />
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <el-empty v-else description="请从左侧选择一个角色进行配置" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.permission-config {
  padding: 0;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.btn-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

/* 配置容器 */
.config-container {
  display: flex;
  gap: 20px;
  min-height: 500px;
}

/* 角色列表 */
.role-list-section {
  width: 280px;
  flex-shrink: 0;
}

.role-list-card {
  border-radius: var(--radius-lg);
}

.role-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.role-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
  background: var(--color-background);
}

.role-item:hover {
  background: var(--color-background-hover);
}

.role-item.active {
  background: var(--color-primary-subtle);
  border: 1px solid var(--color-primary);
}

.role-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.role-count {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.arrow-icon {
  color: var(--color-text-tertiary);
}

.role-item.active .arrow-icon {
  color: var(--color-primary);
}

/* 权限详情 */
.permission-detail-section {
  flex: 1;
}

.permission-detail-card {
  border-radius: var(--radius-lg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-actions {
  display: flex;
  gap: 8px;
}

/* 表单样式 */
.permission-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border-light);
}

.form-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: var(--color-primary);
}

.section-desc {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin: 0 0 16px 0;
}

/* 菜单权限网格 */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.menu-item {
  padding: 8px 12px;
  background: var(--color-background);
  border-radius: var(--radius-md);
}

.menu-label {
  font-size: 14px;
}

/* 按钮权限网格 */
.button-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.button-item {
  padding: 12px;
  background: var(--color-background);
  border-radius: var(--radius-md);
}

.btn-label {
  font-size: 14px;
  font-weight: 500;
  display: block;
}

.btn-desc {
  font-size: 12px;
  color: var(--color-text-tertiary);
  display: block;
  margin-top: 2px;
}

/* 数据权限组 */
.data-permission-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.permission-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.permission-row label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.permission-hint {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.role-radio-group {
  display: flex;
  width: 100%;
}

.role-radio-group .el-radio-button {
  flex: 1;
}

/* 功能权限组 */
.feature-permission-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--color-background);
  border-radius: var(--radius-md);
}

.feature-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.feature-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.feature-desc {
  font-size: 12px;
  color: var(--color-text-tertiary);
}
</style>
