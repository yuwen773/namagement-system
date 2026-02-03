import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/recipes',
    name: 'recipe-list',
    component: () => import('../views/RecipeList.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/recipes/:id',
    name: 'recipe-detail',
    component: () => import('../views/RecipeDetail.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/category/:type?/:value?',
    name: 'recipe-category',
    component: () => import('../views/RecipeCategory.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/hot',
    name: 'recipe-hot',
    component: () => import('../views/RecipeHot.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: () => import('../views/MyFavorites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/change-password',
    name: 'change-password',
    component: () => import('../views/ChangePassword.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analytics',
    name: 'analytics',
    component: () => import('../views/RecipeAnalytics.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/ingredients-frequency',
    name: 'ingredients-frequency',
    component: () => import('../views/IngredientFrequency.vue'),
    meta: { requiresAuth: false }
  },
  // ========== 管理员路由（使用 AdminLayout） ==========
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'admin',
        component: () => import('../views/UserManagement.vue')
      },
      {
        path: 'recipes',
        name: 'admin-recipes',
        component: () => import('../views/RecipeManagement.vue')
      },
      {
        path: 'ingredients',
        name: 'admin-ingredients',
        component: () => import('../views/IngredientManagement.vue')
      },
      {
        path: 'categories',
        name: 'admin-categories',
        component: () => import('../views/CategoryManagement.vue')
      },
      {
        path: 'analytics',
        name: 'admin-analytics',
        component: () => import('../views/AdminAnalytics.vue')
      },
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        component: () => import('../views/AdminDashboard.vue')
      },
      {
        path: 'behavior',
        name: 'admin-behavior',
        component: () => import('../views/UserBehaviorAnalytics.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 用于标记是否已经验证过 token
let hasValidatedToken = false

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 如果本地有 token 且还没有验证过，先验证 token
  if (userStore.token && !hasValidatedToken) {
    hasValidatedToken = true
    const isValid = await userStore.validateToken()
    if (!isValid && to.meta.requiresAuth) {
      // token 无效且目标页面需要认证，跳转到登录页
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
  }

  // 如果页面需要认证但用户未登录，跳转到登录页
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && !userStore.isAdmin) {
    // 如果页面需要管理员权限但用户不是管理员，跳转到首页
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
