import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
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
          path: 'employees',
          name: 'employees',
          component: () => import('../views/EmployeeList.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'departments',
          name: 'departments',
          component: () => import('../views/DepartmentList.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'attendance',
          name: 'attendance',
          component: () => import('../views/Attendance.vue'),
          meta: { roles: ['admin', 'hr', 'employee'] }
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
          meta: { roles: ['admin', 'hr', 'employee'] }
        },
        {
          path: 'onboarding',
          name: 'onboarding',
          component: () => import('../views/Onboarding.vue'),
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
          path: 'data-center',
          name: 'data-center',
          component: () => import('../views/DataCenter.vue'),
          meta: { roles: ['admin', 'hr'] }
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/ProfileEdit.vue'),
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
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('token')
  const user = authStore.user

  // 1. 检查是否需要登录
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  // 2. 如果已登录，尝试访问登录页，跳转到首页
  if (to.path === '/login' && token) {
    next('/')
    return
  }

  // 3. 检查角色权限
  if (to.meta.roles && user?.role) {
    const allowedRoles = to.meta.roles
    if (!allowedRoles.includes(user.role)) {
      // 无权限访问
      ElMessage.warning('您没有权限访问该页面')
      // 跳转到该角色可访问的第一个页面
      const accessibleMenus = authStore.getAccessibleMenus()
      if (accessibleMenus.length > 0) {
        next(accessibleMenus[0].path)
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
