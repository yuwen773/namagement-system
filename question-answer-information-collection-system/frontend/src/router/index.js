import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy loading for views
const Login = () => import('@/views/Login.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const DataCenter = () => import('@/views/DataCenter.vue')
const UserManagement = () => import('@/views/UserManagement.vue')
const Profile = () => import('@/views/Profile.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, title: '仪表盘' }
  },
  {
    path: '/data',
    name: 'DataCenter',
    component: DataCenter,
    meta: { requiresAuth: true, title: '数据中心' }
  },
  {
    path: '/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, roles: ['admin'], title: '用户管理' }
  },
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
    next({ name: 'Dashboard' })
    return
  }

  // Check role-based access
  if (requiredRoles && requiredRoles.length > 0) {
    if (!authStore.isAdmin) {
      next({ name: 'Dashboard' })
      return
    }
  }

  next()
})

export default router
