<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AdminLayout from '@/components/AdminLayout.vue'
import UserLayout from '@/components/UserLayout.vue'

const route = useRoute()
const authStore = useAuthStore()

// Login page should not have layout wrapper
const isLoginPage = computed(() => {
  return route.name === 'Login'
})

// Determine which layout to use based on user role
const currentLayout = computed(() => {
  if (!authStore.isLoggedIn) return null

  // Admin users get the sidebar layout
  if (authStore.isAdmin) {
    return AdminLayout
  }

  // Regular users get the clean top-nav layout
  return UserLayout
})
</script>

<template>
  <div id="qa-app">
    <!-- Login page - no layout wrapper -->
    <router-view v-if="isLoginPage" />

    <!-- Authenticated pages with role-based layout -->
    <component v-else :is="currentLayout">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </component>
  </div>
</template>

<style scoped>
#qa-app {
  width: 100%;
  min-height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
