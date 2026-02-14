import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '@/api/request'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('accessToken') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const initialized = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  // 方法
  async function login(username, password) {
    const response = await request.post('/accounts/login/', { username, password })
    const { access_token, refresh_token, user: userInfo } = response.data

    accessToken.value = access_token
    refreshToken.value = refresh_token
    user.value = userInfo

    localStorage.setItem('accessToken', access_token)
    localStorage.setItem('refreshToken', refresh_token)

    return userInfo
  }

  async function register(username, password, confirmPassword, email) {
    const response = await request.post('/accounts/register/', {
      username,
      password,
      password_confirm: confirmPassword,
      email
    })
    return response.data
  }

  async function getUserInfo() {
    const response = await request.get('/accounts/profile/')
    user.value = response.data
    return response.data
  }

  async function updateProfile(data) {
    const response = await request.put('/accounts/profile/', data)
    user.value = response.data
    return response.data
  }

  async function changePassword(oldPassword, newPassword) {
    return await request.put('/accounts/profile/password/', {
      old_password: oldPassword,
      new_password: newPassword
    })
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    initialized.value = false
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  async function initialize() {
    if (initialized.value) return
    if (accessToken.value && !user.value) {
      try {
        await getUserInfo()
      } catch (error) {
        // Token 无效，清除登录状态
        logout()
      }
    }
    initialized.value = true
  }

  return {
    user,
    accessToken,
    refreshToken,
    initialized,
    isLoggedIn,
    isAdmin,
    login,
    register,
    getUserInfo,
    updateProfile,
    changePassword,
    logout,
    initialize
  }
})
