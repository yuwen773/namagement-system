import { defineStore } from 'pinia'
import { loginApi, registerApi, getCurrentUserApi } from '@/api/modules/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    isLoading: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userInfo: (state) => state.user,
    userRole: (state) => state.user?.is_staff ? 'admin' : 'user'
  },

  actions: {
    // 登录
    async login(phone, password) {
      this.isLoading = true
      try {
        const data = await loginApi({ phone, password })
        this.token = data.token
        this.user = data.user
        localStorage.setItem('token', data.token)
        return data
      } finally {
        this.isLoading = false
      }
    },

    // 注册
    async register(userData) {
      this.isLoading = true
      try {
        const data = await registerApi(userData)
        this.token = data.token
        this.user = data.user
        localStorage.setItem('token', data.token)
        return data
      } finally {
        this.isLoading = false
      }
    },

    // 获取当前用户信息
    async getCurrentUser() {
      if (!this.token) return null

      this.isLoading = true
      try {
        const data = await getCurrentUserApi()
        this.user = data
        return data
      } catch (error) {
        // Token 可能过期，清除登录状态
        this.logout()
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // 退出登录
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },

    // 更新用户信息
    updateUser(userData) {
      this.user = { ...this.user, ...userData }
    }
  }
})
