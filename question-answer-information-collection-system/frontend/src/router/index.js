import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import DataCenter from '@/views/DataCenter.vue'
import UserManagement from '@/views/UserManagement.vue'
import NoticeManagement from '@/views/NoticeManagement.vue'
import Profile from '@/views/Profile.vue'

// Routes with lazy loading
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: (to) => {
      // 根据用户角色重定向
      const isLoggedIn = useAuthStore().isLoggedIn
      if (!isLoggedIn) return '/login'
      return useAuthStore().isAdmin ? '/dashboard' : '/overview'
    }
  },
  // Dashboard - accessible to all authenticated users
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, layout: 'admin', title: '仪表盘' }
  },
  // User Overview - accessible to regular users (simplified dashboard)
  {
    path: '/overview',
    name: 'Overview',
    component: Dashboard,
    meta: { requiresAuth: true, layout: 'user', title: '数据概览' }
  },
  // Data Center - different titles for admin vs regular user
  {
    path: '/data',
    name: 'DataCenter',
    component: DataCenter,
    meta: { requiresAuth: true, layout: 'admin', title: '数据中心' }
  },
  {
    path: '/my-data',
    name: 'MyData',
    component: DataCenter,
    meta: { requiresAuth: true, layout: 'user', title: '我的数据' }
  },
  // User Management - admin only
  {
    path: '/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, roles: ['admin'], layout: 'admin', title: '用户管理' }
  },
  // Notice Management - admin for management, regular users for viewing
  {
    path: '/notices',
    name: 'NoticeManagement',
    component: NoticeManagement,
    meta: { requiresAuth: true, layout: 'user', title: '通知公告' }
  },
  // Profile - accessible to all
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true, title: '个人中心' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = authStore.isLoggedIn
  const requiresAuth = to.meta.requiresAuth !== false
  const requiredRoles = to.meta.roles

  // Redirect to login if not authenticated
  if (requiresAuth && !isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // Redirect to dashboard if already logged in and trying to access login
  if (to.name === 'Login' && isLoggedIn) {
    next({ name: authStore.isAdmin ? 'Dashboard' : 'Overview' })
    return
  }

  // Check role-based access for admin routes
  if (requiredRoles && requiredRoles.length > 0) {
    if (!authStore.isAdmin) {
      next({ name: 'Overview' })
      return
    }
  }

  // Redirect admin users away from user-only routes
  if (to.meta.layout === 'user' && authStore.isAdmin) {
    next({ name: 'Dashboard' })
    return
  }

  // Redirect regular users away from admin-only routes
  if (to.meta.layout === 'admin' && !authStore.isAdmin) {
    next({ name: 'Overview' })
    return
  }

  next()
})

export default router
