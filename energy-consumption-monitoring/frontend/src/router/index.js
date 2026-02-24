import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

/**
 * Vue Router configuration
 * - Route guards for authentication
 * - Route guards for role-based access
 */

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: 'Login - Energy Monitoring',
      requiresAuth: false,
    },
  },
  {
    path: '/admin',
    name: 'AdminLayout',
    component: () => import('@/layouts/AdminLayout.vue'),
    redirect: '/admin/dashboard',
    meta: {
      requiresAuth: true,
      roles: ['ADMIN'],
    },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: {
          title: 'Dashboard - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
      {
        path: 'monitoring',
        name: 'Monitoring',
        component: () => import('@/views/admin/Monitoring.vue'),
        meta: {
          title: 'Monitoring Center - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('@/views/admin/Analysis.vue'),
        meta: {
          title: 'Data Analysis - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
      {
        path: 'alarms',
        name: 'Alarms',
        component: () => import('@/views/admin/Alarms.vue'),
        meta: {
          title: 'Alarm Management - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
      {
        path: 'devices',
        name: 'Devices',
        component: () => import('@/views/admin/Devices.vue'),
        meta: {
          title: 'Device Management - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
      {
        path: 'configuration',
        name: 'Configuration',
        component: () => import('@/views/admin/Configuration.vue'),
        meta: {
          title: 'Configuration - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
      {
        path: 'system',
        name: 'System',
        component: () => import('@/views/admin/System.vue'),
        meta: {
          title: 'System Management - Energy Monitoring',
          requiresAuth: true,
          roles: ['ADMIN'],
        },
      },
    ],
  },
  {
    path: '/user',
    name: 'UserLayout',
    component: () => import('@/layouts/UserLayout.vue'),
    redirect: '/user/dashboard',
    meta: {
      requiresAuth: true,
      roles: ['USER', 'ADMIN'],
    },
    children: [
      {
        path: 'dashboard',
        name: 'UserDashboard',
        component: () => import('@/views/user/Dashboard.vue'),
        meta: {
          title: 'My Dashboard - Energy Monitoring',
          requiresAuth: true,
          roles: ['USER', 'ADMIN'],
        },
      },
      {
        path: 'usage',
        name: 'UsageHistory',
        component: () => import('@/views/user/UsageHistory.vue'),
        meta: {
          title: 'Usage History - Energy Monitoring',
          requiresAuth: true,
          roles: ['USER', 'ADMIN'],
        },
      },
      {
        path: 'cost',
        name: 'CostPayment',
        component: () => import('@/views/user/CostPayment.vue'),
        meta: {
          title: 'Cost & Payment - Energy Monitoring',
          requiresAuth: true,
          roles: ['USER', 'ADMIN'],
        },
      },
      {
        path: 'comparison',
        name: 'Comparison',
        component: () => import('@/views/user/Comparison.vue'),
        meta: {
          title: 'Comparison & Ranking - Energy Monitoring',
          requiresAuth: true,
          roles: ['USER', 'ADMIN'],
        },
      },
      {
        path: 'notices',
        name: 'Notices',
        component: () => import('@/views/user/Notices.vue'),
        meta: {
          title: 'Notices - Energy Monitoring',
          requiresAuth: true,
          roles: ['USER', 'ADMIN'],
        },
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/user/Profile.vue'),
        meta: {
          title: 'Profile - Energy Monitoring',
          requiresAuth: true,
          roles: ['USER', 'ADMIN'],
        },
      },
    ],
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/Forbidden.vue'),
    meta: {
      title: 'Access Denied - Energy Monitoring',
      requiresAuth: false,
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: 'Page Not Found - Energy Monitoring',
      requiresAuth: false,
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

/**
 * Navigation guard: Check authentication
 */
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = !!userStore.token
  const requiresAuth = to.meta.requiresAuth !== false
  const allowedRoles = to.meta.roles || []

  // Update page title
  document.title = to.meta.title || 'Energy Monitoring System'

  // Check if route requires authentication
  if (requiresAuth && !isAuthenticated) {
    // Redirect to login with return URL
    next({
      path: '/login',
      query: { redirect: to.fullPath },
    })
    return
  }

  // Check if already on login page and authenticated
  if (to.path === '/login' && isAuthenticated) {
    // Redirect based on role
    const userRole = userStore.role
    if (userRole === 'ADMIN') {
      next('/admin/dashboard')
    } else {
      next('/user/dashboard')
    }
    return
  }

  // Check role-based access
  if (requiresAuth && isAuthenticated && allowedRoles.length > 0) {
    const userRole = userStore.role
    if (!allowedRoles.includes(userRole)) {
      // User doesn't have required role
      next('/403')
      return
    }
  }

  next()
})

/**
 * Navigation guard: Update page title and handle errors
 */
router.afterEach((to, from) => {
  // Log navigation for debugging
  if (import.meta.env.DEV) {
    console.log(`Navigated from ${from.path} to ${to.path}`)
  }
})

export default router
