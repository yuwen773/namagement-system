import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { requiresAuth: false }
  },
  // 管理员端路由
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/admin/DashboardView.vue'),
    meta: { requiresAuth: true, role: 'ADMIN' }
  },
  // 员工端路由
  {
    path: '/employee',
    name: 'EmployeeHome',
    component: () => import('../views/employee/HomeView.vue'),
    meta: { requiresAuth: true, role: 'EMPLOYEE' }
  },
  // 默认重定向到登录页
  {
    path: '/',
    redirect: '/login'
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

// 导航守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 如果路由需要认证
  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      // 未登录，跳转到登录页
      next('/login')
      return
    }

    // 检查角色权限
    if (to.meta.role && to.meta.role !== userStore.userRole) {
      // 角色不匹配，跳转到对应角色的首页
      if (userStore.isAdmin) {
        next('/admin')
      } else if (userStore.isEmployee) {
        next('/employee')
      } else {
        next('/login')
      }
      return
    }
  }

  // 如果已登录用户访问登录页，跳转到对应首页
  if (to.path === '/login' && userStore.isLoggedIn) {
    if (userStore.isAdmin) {
      next('/admin')
    } else if (userStore.isEmployee) {
      next('/employee')
    } else {
      next()
    }
    return
  }

  next()
})

export default router
