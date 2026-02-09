import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function setRefreshToken(newToken) {
    refreshToken.value = newToken
    localStorage.setItem('refresh_token', newToken)
  }

  function setUserInfo(info) {
    userInfo.value = info
    localStorage.setItem('user', JSON.stringify(info))
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = {}
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  function isAdmin() {
    return userInfo.value?.role === 'admin'
  }

  return {
    token,
    refreshToken,
    userInfo,
    setToken,
    setRefreshToken,
    setUserInfo,
    logout,
    isAdmin
  }
})
