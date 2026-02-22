import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '@/utils/request'
import { getToken, setToken, removeToken, getRefreshToken, setRefreshToken, getUserInfo, setUserInfo, clearAuth } from '@/utils/auth'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const userInfo = ref(getUserInfo())
  const token = ref(getToken())
  const loading = ref(false)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')

  async function login(username, password) {
    loading.value = true
    try {
      const response = await request.post('/api/auth/login/', {
        username,
        password
      })
      console.log('Login response:', response)
      // 后端返回格式: { code: 0, data: { access, refresh, user }, message: "..." }
      // request 拦截器返回 response.data，所以 response 就是 { code, data, message }
      if (!response?.data?.access) {
        console.error('Invalid response format:', response)
        throw new Error('登录响应数据格式错误')
      }
      const { access, refresh, user } = response.data
      setToken(access)
      setRefreshToken(refresh)
      setUserInfo(user)
      token.value = access
      userInfo.value = user
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      const message = error.response?.data?.message || error.message || '登录失败，请检查用户名和密码'
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    // JWT 只需要客户端删除 token 即可，后端无需处理
    clearAuth()
    token.value = null
    userInfo.value = null
    router.push('/login')
  }

  async function fetchUserInfo() {
    if (!token.value) return
    try {
      const response = await request.get('/api/auth/me/')
      userInfo.value = response.data
      setUserInfo(response.data)
    } catch (error) {
      console.error('Fetch user info error:', error)
    }
  }

  return {
    userInfo,
    token,
    loading,
    isLoggedIn,
    isAdmin,
    login,
    logout,
    fetchUserInfo
  }
})
