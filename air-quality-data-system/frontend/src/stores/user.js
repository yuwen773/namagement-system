import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  // Computed
  const isLoggedIn = computed(() => !!token.value && !!userInfo.value)
  const isAdmin = computed(() => userInfo.value?.role === 'ADMIN')
  const userId = computed(() => userInfo.value?.id)
  const username = computed(() => userInfo.value?.username)

  // Actions
  function setUser(user, newToken) {
    userInfo.value = user
    token.value = newToken
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('token', newToken)
  }

  function clearUser() {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  function updateUser(user) {
    userInfo.value = { ...userInfo.value, ...user }
    localStorage.setItem('user', JSON.stringify(userInfo.value))
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    userId,
    username,
    setUser,
    clearUser,
    updateUser
  }
})
