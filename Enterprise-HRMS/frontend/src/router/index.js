import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      component: Home,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/Dashboard.vue')
        },
        {
          path: 'employees',
          name: 'employees',
          component: () => import('../views/EmployeeList.vue')
        },
        {
          path: 'departments',
          name: 'departments',
          component: () => import('../views/DepartmentList.vue')
        },
        {
          path: 'attendance',
          name: 'attendance',
          component: () => import('../views/Attendance.vue')
        },
        {
          path: 'salary',
          name: 'salary',
          component: () => import('../views/Salary.vue')
        },
        {
          path: 'approval',
          name: 'approval',
          component: () => import('../views/ApprovalCenter.vue')
        },
        {
          path: 'onboarding',
          name: 'onboarding',
          component: () => import('../views/Onboarding.vue')
        }
      ]
    }
  ]
})

// 路由守卫：检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
