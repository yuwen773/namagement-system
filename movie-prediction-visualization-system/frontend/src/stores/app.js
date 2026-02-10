/**
 * Pinia Store - 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 状态
  const sidebarCollapsed = ref(false)
  const theme = ref(localStorage.getItem('theme') || 'light')
  const pageTitle = ref('')

  // Actions
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setSidebarCollapsed(collapsed) {
    sidebarCollapsed.value = collapsed
  }

  function setTheme(newTheme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    document.documentElement.className = newTheme
  }

  function setPageTitle(title) {
    pageTitle.value = title
  }

  return {
    // 状态
    sidebarCollapsed,
    theme,
    pageTitle,
    // Actions
    toggleSidebar,
    setSidebarCollapsed,
    setTheme,
    setPageTitle
  }
})
