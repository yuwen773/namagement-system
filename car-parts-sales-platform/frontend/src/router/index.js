import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 用户端布局路由（需要头部和底部）
    {
      path: '/',
      component: () => import('@/components/layouts/UserLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
          meta: { title: '首页' }
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/views/ProductListView.vue'),
          meta: { title: '商品列表' }
        },
        {
          path: 'products/:id',
          name: 'product-detail',
          component: () => import('@/views/ProductDetailView.vue'),
          meta: { title: '商品详情' }
        },
        {
          path: 'cart',
          name: 'cart',
          component: () => import('@/views/CartView.vue'),
          meta: { title: '购物车', requiresAuth: true }
        },
        {
          path: 'orders',
          name: 'orders',
          component: () => import('@/views/OrderListView.vue'),
          meta: { title: '我的订单', requiresAuth: true }
        },
        {
          path: 'orders/:id',
          name: 'order-detail',
          component: () => import('@/views/OrderDetailView.vue'),
          meta: { title: '订单详情', requiresAuth: true }
        },
        {
          path: 'user',
          name: 'user-center',
          component: () => import('@/views/UserCenterView.vue'),
          meta: { title: '个人中心', requiresAuth: true }
        },
        // 用户中心子路由（可在 UserCenterView 中使用嵌套路由或标签页）
        {
          path: 'user/profile',
          name: 'user-profile',
          component: () => import('@/views/UserCenterView.vue'),
          meta: { title: '个人资料', requiresAuth: true }
        },
        {
          path: 'user/addresses',
          name: 'user-addresses',
          component: () => import('@/views/UserCenterView.vue'),
          meta: { title: '收货地址', requiresAuth: true }
        },
        {
          path: 'user/orders',
          name: 'user-orders',
          component: () => import('@/views/UserCenterView.vue'),
          meta: { title: '我的订单', requiresAuth: true }
        },
        {
          path: 'user/coupons',
          name: 'user-coupons',
          component: () => import('@/views/UserCenterView.vue'),
          meta: { title: '我的优惠券', requiresAuth: true }
        },
        {
          path: 'user/messages',
          name: 'user-messages',
          component: () => import('@/views/UserCenterView.vue'),
          meta: { title: '消息中心', requiresAuth: true }
        }
      ]
    },
    // 登录/注册页面（无布局）
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: '登录', hideInMenu: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { title: '注册', hideInMenu: true }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/ForgotPasswordView.vue'),
      meta: { title: '忘记密码', hideInMenu: true }
    },
    // 管理端布局路由
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true },
      redirect: '/admin/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/DashboardView.vue'),
          meta: { title: '数据统计' }
        },
        {
          path: 'products',
          name: 'admin-products',
          component: () => import('@/views/admin/ProductManageView.vue'),
          meta: { title: '商品管理' }
        },
        {
          path: 'categories',
          name: 'admin-categories',
          component: () => import('@/views/admin/ProductManageView.vue'),
          meta: { title: '分类管理' }
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: () => import('@/views/admin/OrderManageView.vue'),
          meta: { title: '订单管理' }
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/UserManageView.vue'),
          meta: { title: '用户管理' }
        },
        {
          path: 'marketing',
          name: 'admin-marketing',
          component: () => import('@/views/admin/MarketingManageView.vue'),
          meta: { title: '营销管理' }
        },
        {
          path: 'content',
          name: 'admin-content',
          component: () => import('@/views/admin/ContentManageView.vue'),
          meta: { title: '内容管理' }
        },
        {
          path: 'system',
          name: 'admin-system',
          component: () => import('@/views/admin/SystemManageView.vue'),
          meta: { title: '系统管理' }
        },
        {
          path: 'system/config',
          name: 'admin-config',
          component: () => import('@/views/admin/SystemManageView.vue'),
          meta: { title: '系统配置' }
        },
        {
          path: 'system/messages',
          name: 'admin-messages',
          component: () => import('@/views/admin/SystemManageView.vue'),
          meta: { title: '消息管理' }
        }
      ]
    },
    // 404 页面
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
      meta: { title: '页面不存在' }
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 汽车改装件销售平台` : '汽车改装件销售平台'

  const authStore = useAuthStore()

  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    // 如果有 token 但没有用户信息，尝试获取用户信息
    if (authStore.token && !authStore.user) {
      try {
        await authStore.getCurrentUser()
      } catch (error) {
        // Token 可能过期，清除登录状态
        authStore.logout()
        next({ name: 'login', query: { redirect: to.fullPath } })
        return
      }
    }

    // 检查是否已登录
    if (!authStore.isAuthenticated) {
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }

    // 检查是否需要管理员权限
    if (to.meta.requiresAdmin && !authStore.user?.is_admin) {
      next({ name: 'home' })
      return
    }
  }

  next()
})

export default router
