import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi } from '../api/auth'
import { ElMessage } from 'element-plus'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)

  async function login(username, password) {
    loading.value = true
    try {
      const res = await loginApi(username, password)
      const { access, refresh, user_id, username: userName, real_name: realName, role } = res.data

      token.value = access
      user.value = { user_id, username: userName, real_name: realName, role }

      // 持久化存储
      localStorage.setItem('token', access)
      localStorage.setItem('refresh', refresh)
      localStorage.setItem('user', JSON.stringify(user.value))

      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
      throw error
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
    localStorage.removeItem('user')
    router.push('/login')
  }

  function isAuthenticated() {
    return !!token.value
  }

  return {
    token,
    user,
    loading,
    login,
    logout,
    isAuthenticated
  }
})
