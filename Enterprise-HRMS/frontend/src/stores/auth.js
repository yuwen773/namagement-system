import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi } from '../api/auth'
import { getPermissionByRole } from '../api/permission'
import { ElMessage } from 'element-plus'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const rolePermissions = ref(null) // 从后端动态获取的权限配置

  // 角色常量
  const ROLE_ADMIN = 'admin'
  const ROLE_HR = 'hr'
  const ROLE_EMPLOYEE = 'employee'

  // 角色判断 computed 属性
  const isAdmin = computed(() => user.value?.role === ROLE_ADMIN)
  const isHR = computed(() => user.value?.role === ROLE_HR)
  const isEmployee = computed(() => user.value?.role === ROLE_EMPLOYEE)

  // 菜单权限配置（路由名称 -> 角色访问权限）- 作为默认配置
  const defaultMenuPermissions = {
    dashboard: [ROLE_ADMIN, ROLE_HR],
    employeeDashboard: [ROLE_EMPLOYEE],
    employees: [ROLE_ADMIN, ROLE_HR],
    departments: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    posts: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    attendance: [ROLE_ADMIN, ROLE_HR],
    attendanceCenter: [ROLE_EMPLOYEE],
    attendanceStatistics: [ROLE_ADMIN, ROLE_HR],
    salary: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    salaryException: [ROLE_ADMIN, ROLE_HR],
    exceptionReport: [ROLE_EMPLOYEE],
    applicationCenter: [ROLE_EMPLOYEE],
    onboarding: [ROLE_ADMIN, ROLE_HR],
    resignation: [ROLE_ADMIN, ROLE_HR],
    users: [ROLE_ADMIN],
    notices: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    noticeManagement: [ROLE_ADMIN],
    performanceReview: [ROLE_ADMIN, ROLE_HR],
    myPerformance: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    performanceTemplate: [ROLE_ADMIN, ROLE_HR],
    dataCenter: [ROLE_ADMIN, ROLE_HR],
    profile: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    permissionConfig: [ROLE_ADMIN],
    securityConfig: [ROLE_ADMIN]
  }

  // 从后端获取角色权限配置
  async function fetchRolePermissions() {
    if (!user.value?.role) return null

    try {
      const res = await getPermissionByRole(user.value.role)
      if (res.data?.code === 0 && res.data?.data) {
        rolePermissions.value = res.data.data
        return rolePermissions.value
      }
    } catch (error) {
      console.error('获取角色权限配置失败:', error)
    }
    return null
  }

  // 检查是否有权限访问指定菜单
  function hasPermission(routeName) {
    if (!user.value?.role) return false

    // 如果有后端动态权限配置，优先使用
    if (rolePermissions.value?.menu_permissions) {
      // 如果后端配置包含该路由，允许访问
      return rolePermissions.value.menu_permissions.includes(routeName)
    }

    // 否则使用默认配置兜底（仅用于初始化时）
    const allowedRoles = defaultMenuPermissions[routeName]
    if (!allowedRoles) return true // 未配置的路由默认允许访问
    return allowedRoles.includes(user.value.role)
  }

  // 检查是否有按钮权限
  function hasButtonPermission(buttonName) {
    if (!user.value?.role) return false

    // 如果有后端动态权限配置，优先使用
    if (rolePermissions.value?.button_permissions) {
      return rolePermissions.value.button_permissions.includes(buttonName)
    }

    // 默认所有角色都可以查看自己的薪资
    if (buttonName === 'viewSalary') {
      return true
    }

    return false
  }

  // 检查是否可以访问数据中心
  function canAccessDataCenter() {
    if (!user.value?.role) return false

    if (rolePermissions.value?.can_access_datacenter !== undefined) {
      return rolePermissions.value.can_access_datacenter
    }

    // 默认配置
    return [ROLE_ADMIN, ROLE_HR].includes(user.value.role)
  }

  // 检查是否可以访问绩效管理
  function canAccessPerformance() {
    if (!user.value?.role) return false

    if (rolePermissions.value?.can_access_performance !== undefined) {
      return rolePermissions.value.can_access_performance
    }

    // 默认配置
    return true
  }

  // 获取当前用户可访问的菜单列表
  function getAccessibleMenus() {
    const allMenus = [
      { 
        name: 'dashboard', 
        label: isAdmin.value ? '系统运营看板' : (isHR.value ? '人事工作台' : '系统运营看板'), 
        path: '/', 
        icon: 'dashboard' 
      },
      { name: 'employeeDashboard', label: '首页', path: '/employee', icon: 'dashboard' },
      { name: 'dataCenter', label: '数据中心', path: '/data-center', icon: 'dashboard' },
      { name: 'employees', label: isHR.value ? '员工档案管理' : '员工管理', path: '/employees', icon: 'employees' },
      { name: 'departments', label: '部门管理', path: '/departments', icon: 'departments' },
      { name: 'posts', label: '岗位管理', path: '/posts', icon: 'posts' },
      { name: 'attendance', label: '考勤管理', path: '/attendance', icon: 'attendance' },
      { name: 'attendanceCenter', label: '考勤中心', path: '/attendance-center', icon: 'attendance' },
      { name: 'attendanceStatistics', label: '考勤统计', path: '/attendance-statistics', icon: 'attendance' },
      { name: 'salary', label: '薪资管理', path: '/salary', icon: 'salary' },
      { name: 'salaryException', label: '异常处理', path: '/salary-exception', icon: 'salary' },
      { name: 'exceptionReport', label: '异常上报', path: '/exception-report', icon: 'salary' },
      { name: 'approval', label: '审批中心', path: '/approval', icon: 'approval' },
      { name: 'applicationCenter', label: '申请中心', path: '/application-center', icon: 'approval' },
      { name: 'onboarding', label: '入职管理', path: '/onboarding', icon: 'onboarding' },
      { name: 'resignation', label: '离职管理', path: '/resignation', icon: 'onboarding' },
      { name: 'performanceReview', label: '绩效评估', path: '/performance-review', icon: 'performance' },
      { name: 'myPerformance', label: '我的绩效', path: '/my-performance', icon: 'performance' },
      { name: 'performanceTemplate', label: '绩效模板', path: '/performance-template', icon: 'performance' },
      { name: 'notices', label: '系统公告', path: '/notices', icon: 'notices' },
      { name: 'noticeManagement', label: '公告管理', path: '/notice-management', icon: 'notices' },
      { name: 'users', label: '账号管理', path: '/users', icon: 'users' },
      { name: 'permissionConfig', label: '权限配置', path: '/permission-config', icon: 'setting' },
      { name: 'securityConfig', label: '安全配置', path: '/security-config', icon: 'setting' },
      { name: 'profile', label: '个人中心', path: '/profile', icon: 'profile' }
    ]
    return allMenus.filter(menu => hasPermission(menu.name))
  }

  // 获取数据权限
  function getDataPermission(type = 'general') {
    if (!rolePermissions.value) {
      // 默认配置
      if (type === 'attendance') {
        return user.value?.role === ROLE_EMPLOYEE ? 'self' : 'all'
      }
      if (type === 'salary') {
        return user.value?.role === ROLE_EMPLOYEE ? 'self' : 'all'
      }
      return user.value?.role === ROLE_EMPLOYEE ? 'self' : 'all'
    }

    if (type === 'attendance') {
      return rolePermissions.value.attendance_permission || 'self'
    }
    if (type === 'salary') {
      return rolePermissions.value.salary_permission || 'self'
    }
    return rolePermissions.value.data_permission || 'self'
  }

  async function login(username, password) {
    loading.value = true
    try {
      const res = await loginApi(username, password)
      const { access, refresh, user_id, username: userName, real_name: realName, role } = res.data

      token.value = access
      user.value = { user_id, username: userName, real_name: realName, role }

      // 持久化存储
      localStorage.setItem('token', access)
      localStorage.setItem('refresh', refresh)
      localStorage.setItem('user', JSON.stringify(user.value))

      // 获取角色权限配置
      await fetchRolePermissions()

      ElMessage.success('登录成功')
      // 根据角色跳转到不同首页
      if (role === 'employee') {
        router.push('/employee')
      } else {
        router.push('/')
      }
    } catch (error) {
      let errorMessage = '登录失败，请检查用户名和密码'
      const errorData = error.response?.data
      
      if (errorData) {
        if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail
        } else if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail[0]
        } else if (errorData.non_field_errors) {
          errorMessage = Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors[0] : errorData.non_field_errors
        }
      }
      
      ElMessage.error(errorMessage)
      throw error
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    rolePermissions.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
    localStorage.removeItem('user')
    router.push('/login')
  }

  function isAuthenticated() {
    return !!token.value
  }

  return {
    token,
    user,
    loading,
    rolePermissions,
    ROLE_ADMIN,
    ROLE_HR,
    ROLE_EMPLOYEE,
    isAdmin,
    isHR,
    isEmployee,
    hasPermission,
    hasButtonPermission,
    canAccessDataCenter,
    canAccessPerformance,
    getDataPermission,
    fetchRolePermissions,
    getAccessibleMenus,
    login,
    logout,
    isAuthenticated
  }
})
