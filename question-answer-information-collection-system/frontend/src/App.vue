<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const route = useRoute()

// Login page should not have layout
const showLayout = computed(() => {
  return route.name !== 'Login'
})
</script>

<template>
  <div id="qa-app">
    <AppLayout v-if="showLayout">
      <router-view />
    </AppLayout>
    <router-view v-else />
  </div>
</template>

<style scoped>
#qa-app {
  width: 100%;
  min-height: 100vh;
}
</style>
