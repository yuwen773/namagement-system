import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainLayout from '@/layouts/MainLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false, title: '注册' }
  },
  // 用户端布局 - 顶部导航
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      },
      {
        path: 'heritage',
        name: 'HeritageList',
        component: () => import('@/views/HeritageList.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      },
      {
        path: 'heritage/:id',
        name: 'HeritageDetail',
        component: () => import('@/views/HeritageDetail.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      },
      {
        path: 'inheritors',
        name: 'InheritorList',
        component: () => import('@/views/InheritorList.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      },
      {
        path: 'announcements',
        name: 'AnnouncementList',
        component: () => import('@/views/AnnouncementList.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      },
      {
        path: 'announcements/:id',
        name: 'AnnouncementDetail',
        component: () => import('@/views/AnnouncementDetail.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue'),
        meta: { requiresAuth: true, layout: 'main' }
      }
    ]
  },
  // 管理端布局 - 侧边栏导航
  {
    path: '/admin',
    component: AdminLayout,
    redirect: '/admin/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      },
      {
        path: 'heritage',
        name: 'AdminHeritage',
        component: () => import('@/views/admin/HeritageManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      },
      {
        path: 'inheritors',
        name: 'AdminInheritors',
        component: () => import('@/views/admin/InheritorManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      },
      {
        path: 'categories',
        name: 'AdminCategories',
        component: () => import('@/views/admin/CategoryManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      },
      {
        path: 'import',
        name: 'AdminImport',
        component: () => import('@/views/admin/DataImport.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      },
      {
        path: 'announcements',
        name: 'AdminAnnouncements',
        component: () => import('@/views/admin/AnnouncementManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/UserManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, layout: 'admin' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()

  // 检查是否需要认证
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }

  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/dashboard')
    return
  }

  // 已登录用户访问登录页，重定向到首页
  if (to.path === '/login' && userStore.isLoggedIn) {
    next('/dashboard')
    return
  }

  next()
})

export default router
