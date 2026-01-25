import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi } from '../api/auth'
import { ElMessage } from 'element-plus'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)

  // 角色常量
  const ROLE_ADMIN = 'admin'
  const ROLE_HR = 'hr'
  const ROLE_EMPLOYEE = 'employee'

  // 角色判断 computed 属性
  const isAdmin = computed(() => user.value?.role === ROLE_ADMIN)
  const isHR = computed(() => user.value?.role === ROLE_HR)
  const isEmployee = computed(() => user.value?.role === ROLE_EMPLOYEE)

  // 菜单权限配置（路由名称 -> 角色访问权限）
  const menuPermissions = {
    dashboard: [ROLE_ADMIN, ROLE_HR],
    employees: [ROLE_ADMIN, ROLE_HR],
    departments: [ROLE_ADMIN, ROLE_HR],
    attendance: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    salary: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    approval: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    onboarding: [ROLE_ADMIN, ROLE_HR],
    users: [ROLE_ADMIN],
    notices: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    noticeManagement: [ROLE_ADMIN],
    performanceReview: [ROLE_ADMIN, ROLE_HR],
    myPerformance: [ROLE_ADMIN, ROLE_HR, ROLE_EMPLOYEE],
    dataCenter: [ROLE_ADMIN, ROLE_HR]
  }

  // 检查是否有权限访问指定路由
  function hasPermission(routeName) {
    if (!user.value?.role) return false
    const allowedRoles = menuPermissions[routeName]
    if (!allowedRoles) return true // 未配置的路由默认允许访问
    return allowedRoles.includes(user.value.role)
  }

  // 获取当前用户可访问的菜单列表
  function getAccessibleMenus() {
    const allMenus = [
      { name: 'dashboard', label: '数据概览', path: '/', icon: 'dashboard' },
      { name: 'dataCenter', label: '数据中心', path: '/data-center', icon: 'dashboard' },
      { name: 'employees', label: '员工管理', path: '/employees', icon: 'employees' },
      { name: 'departments', label: '部门管理', path: '/departments', icon: 'departments' },
      { name: 'attendance', label: '考勤管理', path: '/attendance', icon: 'attendance' },
      { name: 'salary', label: '薪资管理', path: '/salary', icon: 'salary' },
      { name: 'approval', label: '审批中心', path: '/approval', icon: 'approval' },
      { name: 'onboarding', label: '入职管理', path: '/onboarding', icon: 'onboarding' },
      { name: 'performanceReview', label: '绩效评估', path: '/performance-review', icon: 'performance' },
      { name: 'myPerformance', label: '我的绩效', path: '/my-performance', icon: 'performance' },
      { name: 'notices', label: '系统公告', path: '/notices', icon: 'notices' },
      { name: 'noticeManagement', label: '公告管理', path: '/notice-management', icon: 'notices' },
      { name: 'users', label: '账号管理', path: '/users', icon: 'users' }
    ]
    return allMenus.filter(menu => hasPermission(menu.name))
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

      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
      throw error
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = ''
    user.value = null
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
    ROLE_ADMIN,
    ROLE_HR,
    ROLE_EMPLOYEE,
    isAdmin,
    isHR,
    isEmployee,
    hasPermission,
    getAccessibleMenus,
    login,
    logout,
    isAuthenticated
  }
})
