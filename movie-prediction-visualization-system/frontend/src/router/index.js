/**
 * Vue Router 配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 静态导入布局组件
import AdminLayout from '@/views/layouts/AdminLayout.vue'
import UserLayout from '@/views/layouts/UserLayout.vue'

// 静态导入页面组件 (路由懒加载)
const Login = () => import('@/views/Login.vue')
const Register = () => import('@/views/Register.vue')

// Admin Pages
const AdminDashboard = () => import('@/views/admin/Dashboard.vue')
const AdminMovies = () => import('@/views/admin/Movies.vue')
const AdminMovieTypes = () => import('@/views/admin/MovieTypes.vue')
const AdminCinemas = () => import('@/views/admin/Cinemas.vue')
const AdminRegions = () => import('@/views/admin/Regions.vue')
const AdminBoxOffice = () => import('@/views/admin/BoxOffice.vue')
const AdminPrediction = () => import('@/views/admin/Prediction.vue')
const AdminUsers = () => import('@/views/admin/Users.vue')

// User Pages
const UserDashboard = () => import('@/views/user/Dashboard.vue')
const UserBoxOffice = () => import('@/views/user/BoxOffice.vue')
const UserVisualization = () => import('@/views/user/Visualization.vue')
const UserPrediction = () => import('@/views/user/Prediction.vue')
const UserProfile = () => import('@/views/user/Profile.vue')

// 路由配置
const routes = [
  // Auth Routes
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录', public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册', public: true }
  },

  // Admin Routes
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, roles: ['ADMIN'] },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { title: '系统概览' }
      },
      {
        path: 'movies',
        name: 'AdminMovies',
        component: AdminMovies,
        meta: { title: '影片管理' }
      },
      {
        path: 'movie-types',
        name: 'AdminMovieTypes',
        component: AdminMovieTypes,
        meta: { title: '影片类型' }
      },
      {
        path: 'cinemas',
        name: 'AdminCinemas',
        component: AdminCinemas,
        meta: { title: '影院管理' }
      },
      {
        path: 'regions',
        name: 'AdminRegions',
        component: AdminRegions,
        meta: { title: '地域管理' }
      },
      {
        path: 'boxoffice',
        name: 'AdminBoxOffice',
        component: AdminBoxOffice,
        meta: { title: '票房数据' }
      },
      {
        path: 'prediction',
        name: 'AdminPrediction',
        component: AdminPrediction,
        meta: { title: '预测分析' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: { title: '用户管理' }
      }
    ]
  },

  // User Routes
  {
    path: '/',
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'UserDashboard',
        component: UserDashboard,
        meta: { title: '数据看板' }
      },
      {
        path: 'boxoffice',
        name: 'UserBoxOffice',
        component: UserBoxOffice,
        meta: { title: '票房查询' }
      },
      {
        path: 'visualization',
        name: 'UserVisualization',
        component: UserVisualization,
        meta: { title: '可视化图表' }
      },
      {
        path: 'prediction',
        name: 'UserPrediction',
        component: UserPrediction,
        meta: { title: '票房预测' }
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { title: '个人中心' }
      }
    ]
  },

  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到', public: true }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title
    ? `${to.meta.title} - 电影票房预测系统`
    : '电影票房预测系统'

  const userStore = useUserStore()

  // 公开路由直接通过
  if (to.meta.public) {
    // 已登录用户访问登录页则跳转到首页
    if (userStore.isLoggedIn && ['Login', 'Register'].includes(to.name)) {
      return next({ name: userStore.isAdmin ? 'AdminDashboard' : 'UserDashboard' })
    }
    return next()
  }

  // 需要认证的路由
  if (to.meta.requiresAuth) {
    // 未登录跳转到登录页
    if (!userStore.isLoggedIn) {
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }

    // 角色权限检查
    if (to.meta.roles && !to.meta.roles.includes(userStore.user?.role)) {
      return next({ name: userStore.isAdmin ? 'AdminDashboard' : 'UserDashboard' })
    }
  }

  next()
})

export default router
