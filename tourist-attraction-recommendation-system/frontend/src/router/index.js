import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  // 公共页面
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: '注册', public: true }
  },

  // 用户端布局
  {
    path: '/',
    component: () => import('@/layouts/UserLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/user/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'attractions',
        name: 'AttractionList',
        component: () => import('@/views/user/AttractionList.vue'),
        meta: { title: '景点列表' }
      },
      {
        path: 'attractions/:id',
        name: 'AttractionDetail',
        component: () => import('@/views/user/AttractionDetail.vue'),
        meta: { title: '景点详情' }
      },
      {
        path: 'usercenter',
        name: 'UserCenter',
        component: () => import('@/views/user/UserCenter.vue'),
        meta: { title: '个人中心' }
      },
      {
        path: 'favorites',
        name: 'MyFavorites',
        component: () => import('@/views/user/MyFavorites.vue'),
        meta: { title: '我的收藏' }
      },
      {
        path: 'comments',
        name: 'MyComments',
        component: () => import('@/views/user/MyComments.vue'),
        meta: { title: '我的评论' }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: () => import('@/views/user/Notifications.vue'),
        meta: { title: '消息中心' }
      }
    ]
  },

  // 管理端布局
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '数据看板', roles: ['ADMIN'] }
      },
      {
        path: 'users',
        name: 'UserManage',
        component: () => import('@/views/admin/UserManage.vue'),
        meta: { title: '用户管理', roles: ['ADMIN'] }
      },
      {
        path: 'attractions',
        name: 'AttractionManage',
        component: () => import('@/views/admin/AttractionManage.vue'),
        meta: { title: '景点管理', roles: ['ADMIN'] }
      },
      {
        path: 'attractions/:id/edit',
        name: 'AttractionEdit',
        component: () => import('@/views/admin/AttractionEdit.vue'),
        meta: { title: '编辑景点', roles: ['ADMIN'] }
      },
      {
        path: 'attractions/create',
        name: 'AttractionCreate',
        component: () => import('@/views/admin/AttractionEdit.vue'),
        meta: { title: '新增景点', roles: ['ADMIN'] }
      },
      {
        path: 'comments',
        name: 'CommentReview',
        component: () => import('@/views/admin/CommentReview.vue'),
        meta: { title: '评论审核', roles: ['ADMIN'] }
      },
      {
        path: 'announcements',
        name: 'AnnouncementManage',
        component: () => import('@/views/admin/AnnouncementManage.vue'),
        meta: { title: '公告管理', roles: ['ADMIN'] }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/AdminSettings.vue'),
        meta: { title: '个人设置', roles: ['ADMIN'] }
      }
    ]
  },

  // 管理员登录页（独立）
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/admin/AdminLogin.vue'),
    meta: { title: '管理员登录', public: true }
  },

  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到', public: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '页面'} - 旅游景点推荐系统`

  const userStore = useUserStore()

  // 公开页面直接放行
  if (to.meta.public) {
    next()
    return
  }

  // 需要角色权限的页面
  if (to.meta.roles) {
    if (!userStore.isLoggedIn) {
      next({ name: to.path.startsWith('/admin') ? 'AdminLogin' : 'Login', query: { redirect: to.fullPath } })
      return
    }
    if (!to.meta.roles.includes(userStore.user?.role)) {
      next({ name: userStore.user?.role === 'ADMIN' ? 'Dashboard' : 'Home' })
      return
    }
  }

  // 需要登录的页面
  if (!userStore.isLoggedIn) {
    next({ name: to.path.startsWith('/admin') ? 'AdminLogin' : 'Login', query: { redirect: to.fullPath } })
    return
  }

  // 管理员访问用户页面或用户访问管理员页面时跳转
  if (to.path.startsWith('/admin') && userStore.user?.role !== 'ADMIN') {
    next({ name: 'Home' })
    return
  }
  if (!to.path.startsWith('/admin') && userStore.user?.role === 'ADMIN') {
    next({ name: 'Dashboard' })
    return
  }

  next()
})

export default router
