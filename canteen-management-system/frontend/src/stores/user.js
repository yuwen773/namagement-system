import { defineStore } from 'pinia'
import { login } from '../api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null')
  }),

  getters: {
    // 是否已登录
    isLoggedIn: (state) => !!state.token,
    // 获取用户角色
    userRole: (state) => state.userInfo?.role || null,
    // 是否是管理员
    isAdmin: (state) => state.userInfo?.role === 'ADMIN',
    // 是否是员工
    isEmployee: (state) => state.userInfo?.role === 'EMPLOYEE'
  },

  actions: {
    // 登录
    async login(username, password) {
      try {
        const res = await login(username, password)
        if (res.code === 200) {
          this.token = res.data.id || res.data.username // 使用用户ID或用户名作为token
          this.userInfo = res.data

          // 保存到 localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))

          return { success: true, data: res.data }
        }
        return { success: false, message: res.message || '登录失败' }
      } catch (error) {
        console.error('登录错误:', error)
        return { success: false, message: error.message || '登录失败，请检查网络连接' }
      }
    },

    // 退出登录
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    },

    // 更新用户信息
    updateUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    }
  }
})
