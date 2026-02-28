import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

// 布局组件
const AdminLayout = () => import('@/components/Layout/AdminLayout.vue')
const UserLayout = () => import('@/components/Layout/UserLayout.vue')

// 页面组件
const Login = () => import('@/views/Login.vue')

// 管理端页面
const AdminDashboard = () => import('@/views/admin/Dashboard.vue')
const StatisticsDashboard = () => import('@/views/admin/StatisticsDashboard.vue')
const AdminCrawler = () => import('@/views/admin/Crawler.vue')
const AdminCrawlerConfig = () => import('@/views/admin/CrawlerConfig.vue')
const AdminProducts = () => import('@/views/admin/Products.vue')
const AdminUsers = () => import('@/views/admin/Users.vue')
const AdminSettings = () => import('@/views/admin/Settings.vue')

// 用户端页面
const UserMarket = () => import('@/views/user/Market.vue')
const UserProducts = () => import('@/views/user/Products.vue')
const UserProductDetail = () => import('@/views/user/ProductDetail.vue')
const UserProfile = () => import('@/views/user/Profile.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/',
    redirect: '/login'
  },
  // 管理端路由
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin', title: '宠物用品数据概览' }
      },
      {
        path: 'statistics',
        name: 'StatisticsDashboard',
        component: StatisticsDashboard,
        meta: { requiresAuth: true, role: 'admin', title: '宠物用品统计分析' }
      },
      {
        path: 'crawler',
        name: 'AdminCrawler',
        component: AdminCrawler,
        meta: { requiresAuth: true, role: 'admin', title: '宠物数据采集' }
      },
      {
        path: 'crawler/config',
        name: 'AdminCrawlerConfig',
        component: AdminCrawlerConfig,
        meta: { requiresAuth: true, role: 'admin', title: '爬虫配置' }
      },
      {
        path: 'products',
        name: 'AdminProducts',
        component: AdminProducts,
        meta: { requiresAuth: true, role: 'admin', title: '宠物商品管理' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: { requiresAuth: true, role: 'admin', title: '用户管理' }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: AdminSettings,
        meta: { requiresAuth: true, role: 'admin', title: '系统设置' }
      }
    ]
  },
  // 用户端路由
  {
    path: '/user',
    component: UserLayout,
    meta: { requiresAuth: true, role: 'user' },
    children: [
      {
        path: '',
        redirect: '/user/market'
      },
      {
        path: 'market',
        name: 'UserMarket',
        component: UserMarket,
        meta: { requiresAuth: true, role: 'user', title: '市场行情' }
      },
      {
        path: 'products',
        name: 'UserProducts',
        component: UserProducts,
        meta: { requiresAuth: true, role: 'user', title: '商品资源库' }
      },
      {
        path: 'products/:id',
        name: 'UserProductDetail',
        component: UserProductDetail,
        meta: { requiresAuth: true, role: 'user', title: '商品详情' }
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { requiresAuth: true, role: 'user', title: '个人中心' }
      }
    ]
  },
  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const token = localStorage.getItem('access_token')
  const userRole = userStore.userInfo?.role

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 宠物用品数据` : '宠物用品数据'

  // 不需要认证的页面直接放行
  if (to.meta.requiresAuth === false) {
    // 如果已登录，访问登录页时重定向到对应首页
    if (token && to.path === '/login') {
      // 如果有 token 但没有用户信息，先让请求继续（会在组件中获取用户信息）
      if (!userRole) {
        next()
        return
      }
      if (userRole === 'admin') {
        next('/admin/dashboard')
      } else {
        next('/user/market')
      }
    } else {
      next()
    }
    return
  }

  // 需要认证但没有 token，重定向到登录页
  if (!token) {
    ElMessage.warning('请先登录')
    next('/login')
    return
  }

  // 检查角色权限（只有当用户角色已加载时才检查）
  if (to.meta.role && userRole && to.meta.role !== userRole) {
    ElMessage.error('无权限访问该页面')
    // 重定向到对应角色的首页
    if (userRole === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/user/market')
    }
    return
  }

  next()
})

export default router
