import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAdminStore = defineStore('admin', () => {
  // State
  const activeMenu = ref('dashboard')
  const isCollapsed = ref(false)
  const importTaskStatus = ref(null)

  // Actions
  function setActiveMenu(menu) {
    activeMenu.value = menu
  }

  function toggleSidebar() {
    isCollapsed.value = !isCollapsed.value
  }

  function setImportTaskStatus(status) {
    importTaskStatus.value = status
  }

  return {
    activeMenu,
    isCollapsed,
    importTaskStatus,
    setActiveMenu,
    toggleSidebar,
    setImportTaskStatus
  }
})
