import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  // User routes (user-facing pages)
  {
    path: '/',
    component: () => import('@/layouts/UserLayout.vue'),
    children: [
      {
        path: '',
        name: 'Overview',
        component: () => import('@/views/user/Overview.vue'),
        meta: { title: '全国概览' }
      },
      {
        path: 'city/:code',
        name: 'CityDetail',
        component: () => import('@/views/user/CityDetail.vue'),
        meta: { title: '城市详情' }
      },
      {
        path: 'station/:code',
        name: 'StationDetail',
        component: () => import('@/views/user/StationDetail.vue'),
        meta: { title: '站点详情' }
      },
      {
        path: 'historical',
        name: 'HistoricalData',
        component: () => import('@/views/user/HistoricalData.vue'),
        meta: { title: '历史数据' }
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('@/views/user/Analysis.vue'),
        meta: { title: '数据分析' }
      },
      {
        path: 'protection',
        name: 'ProtectionGuide',
        component: () => import('@/views/user/ProtectionGuide.vue'),
        meta: { title: '防护指南' }
      },
      {
        path: 'knowledge',
        name: 'KnowledgeBase',
        component: () => import('@/views/user/KnowledgeBase.vue'),
        meta: { title: '科普知识' }
      },
      {
        path: 'article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/user/ArticleDetail.vue'),
        meta: { title: '文章详情' }
      }
    ]
  },
  // Admin routes
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '管理后台' }
      },
      {
        path: 'data-import',
        name: 'DataImport',
        component: () => import('@/views/admin/DataImport.vue'),
        meta: { title: '数据导入' }
      },
      {
        path: 'air-quality',
        name: 'AirQualityManage',
        component: () => import('@/views/admin/AirQualityManage.vue'),
        meta: { title: '数据管理' }
      },
      {
        path: 'rules',
        name: 'RulesManage',
        component: () => import('@/views/admin/RulesManage.vue'),
        meta: { title: '规则管理' }
      },
      {
        path: 'users',
        name: 'UsersManage',
        component: () => import('@/views/admin/UsersManage.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'articles',
        name: 'ArticlesManage',
        component: () => import('@/views/admin/ArticlesManage.vue'),
        meta: { title: '文章管理' }
      },
      {
        path: 'logs',
        name: 'SystemLogs',
        component: () => import('@/views/admin/SystemLogs.vue'),
        meta: { title: '系统日志' }
      }
    ]
  },
  // Authentication routes
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: '注册' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isLoggedIn
  const isAdmin = userStore.isAdmin

  // Update page title
  document.title = to.meta.title ? `${to.meta.title} - 空气质量监测平台` : '空气质量监测平台'

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  // Check if route requires admin
  if (to.meta.requiresAdmin && !isAdmin) {
    next('/')
    return
  }

  // Redirect authenticated users from login/register to home
  if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next(isAdmin ? '/admin' : '/')
    return
  }

  next()
})

export default router
