import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * User store for authentication and user state management
 */
export const useUserStore = defineStore(
  'user',
  () => {
    // State
    const token = ref('')
    const userInfo = ref(null)
    const role = ref('') // 'ADMIN' or 'USER'

    // Actions
    function setToken(newToken) {
      token.value = newToken
    }

    function setUserInfo(info) {
      userInfo.value = info
      if (info && info.role) {
        role.value = info.role
      }
    }

    function logout() {
      token.value = ''
      userInfo.value = null
      role.value = ''
    }

    // Getters
    const isAdmin = () => role.value === 'ADMIN'

    return {
      token,
      userInfo,
      role,
      setToken,
      setUserInfo,
      logout,
      isAdmin,
    }
  },
  {
    persist: {
      key: 'energy-user-store',
      storage: localStorage,
      pick: ['token', 'userInfo', 'role'],
    },
  }
)
