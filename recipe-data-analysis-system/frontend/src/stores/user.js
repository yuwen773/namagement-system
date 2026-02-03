import { defineStore } from 'pinia'
import { getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null'),
    isTokenValidating: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.userInfo?.role === 'admin'
  },

  actions: {
    setToken(token) {
      this.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },

    setUserInfo(userInfo) {
      this.userInfo = userInfo
      if (userInfo) {
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
      } else {
        localStorage.removeItem('userInfo')
      }
    },

    logout() {
      this.setToken(null)
      this.setUserInfo(null)
    },

    /**
     * 验证当前 token 是否有效
     * @returns {Promise<boolean>} token 是否有效
     */
    async validateToken() {
      // 如果没有 token，直接返回 false
      if (!this.token) {
        return false
      }

      // 防止重复验证
      if (this.isTokenValidating) {
        return true
      }

      this.isTokenValidating = true

      try {
        const response = await getCurrentUser()
        if (response.code === 200 && response.data) {
          // token 有效，更新用户信息
          this.setUserInfo(response.data)
          return true
        }
        // token 无效
        this.logout()
        return false
      } catch (error) {
        // token 无效或请求失败
        this.logout()
        return false
      } finally {
        this.isTokenValidating = false
      }
    }
  }
})
