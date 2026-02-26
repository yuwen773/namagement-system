import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, logout as logoutApi, getCurrentUser, register as registerApi } from '@/api/auth'
import type { User, LoginRequest, RegisterRequest } from '@/types'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>(localStorage.getItem('access_token') || '')
  const refreshToken = ref<string>(localStorage.getItem('refresh_token') || '')
  const userInfo = ref<User | null>(null)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const username = computed(() => userInfo.value?.username || '')

  // Actions
  const login = async (loginData: LoginRequest) => {
    try {
      const response = await loginApi(loginData)
      const { access, refresh, user } = response.data.data

      // 保存 token
      token.value = access
      refreshToken.value = refresh
      userInfo.value = user

      // 持久化到 localStorage
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user_info', JSON.stringify(user))

      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await logoutApi(refreshToken.value)
      }
    } catch (error) {
      console.error('Logout API failed:', error)
    } finally {
      // 清除状态
      token.value = ''
      refreshToken.value = ''
      userInfo.value = null

      // 清除 localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_info')
    }
  }

  const fetchUserInfo = async () => {
    try {
      const response = await getCurrentUser()
      userInfo.value = response.data.data
      localStorage.setItem('user_info', JSON.stringify(response.data.data))
    } catch (error) {
      console.error('Fetch user info failed:', error)
      // 如果获取用户信息失败，清除登录状态
      await logout()
    }
  }

  const initFromStorage = () => {
    const storedUser = localStorage.getItem('user_info')
    if (storedUser) {
      try {
        userInfo.value = JSON.parse(storedUser)
      } catch (error) {
        console.error('Parse user info failed:', error)
      }
    }
  }

  const register = async (registerData: RegisterRequest) => {
    try {
      const response = await registerApi(registerData)
      const { access, refresh, user } = response.data.data

      // 保存 token
      token.value = access
      refreshToken.value = refresh
      userInfo.value = user

      // 持久化到 localStorage
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user_info', JSON.stringify(user))

      return true
    } catch (error) {
      console.error('Register failed:', error)
      return false
    }
  }

  // 初始化时从 localStorage 恢复用户信息
  initFromStorage()

  return {
    token,
    refreshToken,
    userInfo,
    isLoggedIn,
    isAdmin,
    username,
    login,
    logout,
    register,
    fetchUserInfo
  }
})
