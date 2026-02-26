import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainLayout from '@/layouts/MainLayout.vue'

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
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'heritage',
        name: 'HeritageList',
        component: () => import('@/views/HeritageList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'heritage/:id',
        name: 'HeritageDetail',
        component: () => import('@/views/HeritageDetail.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'inheritors',
        name: 'InheritorList',
        component: () => import('@/views/InheritorList.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'admin',
        redirect: '/admin/heritage'
      },
      {
        path: 'admin/heritage',
        name: 'AdminHeritage',
        component: () => import('@/views/admin/HeritageManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'admin/inheritors',
        name: 'AdminInheritors',
        component: () => import('@/views/admin/InheritorManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'admin/categories',
        name: 'AdminCategories',
        component: () => import('@/views/admin/CategoryManage.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'admin/import',
        name: 'AdminImport',
        component: () => import('@/views/admin/DataImport.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
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
