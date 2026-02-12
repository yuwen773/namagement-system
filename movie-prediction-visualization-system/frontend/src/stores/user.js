/**
 * Pinia Store - 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, logout, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('access_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'ADMIN' || user.value?.role === 'admin')
  const isEmployee = computed(() => user.value?.role === 'USER' || user.value?.role === 'user')

  // Actions
  async function doLogin(credentials) {
    loading.value = true
    try {
      const response = await login(credentials)
      const { access_token, refresh_token, user: userInfo } = response.data

      // 保存到本地存储
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify(userInfo))

      // 更新状态
      token.value = access_token
      user.value = userInfo

      return { success: true }
    } catch (error) {
      return { success: false, message: error.message }
    } finally {
      loading.value = false
    }
  }

  async function doLogout() {
    try {
      await logout()
    } catch (error) {
      // 即使请求失败也清除本地状态
    } finally {
      // 清除本地存储
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')

      // 重置状态
      token.value = ''
      user.value = null
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return

    loading.value = true
    try {
      const response = await getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      // Token 失效时清除状态
      if (error.response?.status === 401) {
        doLogout()
      }
    } finally {
      loading.value = false
    }
  }

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function setUser(userData) {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  return {
    // 状态
    token,
    user,
    loading,
    // 计算属性
    isLoggedIn,
    isAdmin,
    isEmployee,
    // Actions
    doLogin,
    doLogout,
    fetchCurrentUser,
    setToken,
    setUser
  }
})
