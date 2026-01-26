import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/',
      component: Home,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/Dashboard.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'employee',
          name: 'employee-dashboard',
          component: () => import('../views/EmployeeDashboard.vue'),
          meta: { roles: ['employee'] }
        },
        {
          path: 'employees',
          name: 'employees',
          component: () => import('../views/EmployeeList.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'departments',
          name: 'departments',
          component: () => import('../views/DepartmentList.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'posts',
          name: 'posts',
          component: () => import('../views/PostList.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'attendance',
          name: 'attendance',
          component: () => import('../views/Attendance.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'attendance-center',
          name: 'attendance-center',
          component: () => import('../views/AttendanceCenter.vue'),
          meta: { roles: ['employee'] }
        },
        {
          path: 'attendance-statistics',
          name: 'attendance-statistics',
          component: () => import('../views/AttendanceStatistics.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'salary',
          name: 'salary',
          component: () => import('../views/Salary.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'approval',
          name: 'approval',
          component: () => import('../views/ApprovalCenter.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'application-center',
          name: 'application-center',
          component: () => import('../views/ApplicationCenter.vue'),
          meta: { roles: ['employee'] }
        },
        {
          path: 'onboarding',
          name: 'onboarding',
          component: () => import('../views/Onboarding.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'resignation',
          name: 'resignation',
          component: () => import('../views/Resignation.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('../views/UserManagement.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'notices',
          name: 'notices',
          component: () => import('../views/NoticeList.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'notices/:id',
          name: 'notice-detail',
          component: () => import('../views/NoticeDetail.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'notice-management',
          name: 'notice-management',
          component: () => import('../views/NoticeManagement.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'performance-review',
          name: 'performance-review',
          component: () => import('../views/PerformanceReview.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'my-performance',
          name: 'my-performance',
          component: () => import('../views/MyPerformance.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'performance-template',
          name: 'performance-template',
          component: () => import('../views/performance/PerformanceTemplate.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'data-center',
          name: 'data-center',
          component: () => import('../views/DataCenter.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/ProfileCenter.vue'),
          meta: { title: '个人中心', roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'permission-config',
          name: 'permission-config',
          component: () => import('../views/admin/PermissionConfig.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'security-config',
          name: 'security-config',
          component: () => import('../views/admin/SecurityConfig.vue'),
          meta: { roles: ['admin'] }
        },
        {
          path: 'salary-exception',
          name: 'salary-exception',
          component: () => import('../views/SalaryException.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
        }
      ]
    },
    // 404 路由
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue')
    }
  ]
})

// 路由守卫：检查登录状态和角色权限
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('token')
  const user = authStore.user

  // 1. 检查是否需要登录
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  // 2. 如果已登录，尝试访问登录页或注册页，跳转到首页
  if ((to.path === '/login' || to.path === '/register') && token) {
    next('/')
    return
  }

  // 3. 检查角色权限（优先使用动态权限）
  if (user?.role) {
    // 如果权限数据还没加载，先加载
    if (!authStore.rolePermissions && to.meta.requiresAuth) {
      await authStore.fetchRolePermissions()
    }

    // 先检查动态权限配置（从后端获取）
    const hasDynamicPermission = authStore.hasPermission(to.name)
    // 再检查路由的 meta.roles 配置
    const routeAllowedRoles = to.meta.roles

    // 如果动态权限允许访问，直接放行
    if (hasDynamicPermission) {
      next()
      return
    }

    // 如果动态权限不允许，检查静态 meta.roles 作为兜底
    if (routeAllowedRoles && !routeAllowedRoles.includes(user.role)) {
      // 无权限访问
      ElMessage.warning('您没有权限访问该页面')
      // 跳转到该角色可访问的第一个页面
      const accessibleMenus = authStore.getAccessibleMenus()
      // 过滤掉当前要访问的路径，避免无限重定向
      const validMenus = accessibleMenus.filter(menu => menu.path !== to.path)
      if (validMenus.length > 0) {
        next(validMenus[0].path)
      } else {
        // 如果没有任何可访问的菜单，跳转到登录页
        authStore.logout()
        next('/login')
      }
      return
    }
  }

  next()
})

export default router
