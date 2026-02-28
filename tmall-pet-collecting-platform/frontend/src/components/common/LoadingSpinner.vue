<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  text: {
    type: String,
    default: ''
  }
})

const sizeClass = computed(() => `spinner-${props.size}`)
</script>

<template>
  <div class="loading-spinner">
    <div :class="['spinner', sizeClass]">
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
    <p v-if="text" class="spinner-text">{{ text }}</p>
  </div>
</template>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 40px;
}

.spinner {
  position: relative;
  display: inline-block;
}

.spinner-small {
  width: 32px;
  height: 32px;
}

.spinner-medium {
  width: 48px;
  height: 48px;
}

.spinner-large {
  width: 64px;
  height: 64px;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-radius: 50%;
  animation: spinner-spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.spinner-ring:nth-child(1) {
  border-top-color: #FF6B35;
  animation-delay: -0.45s;
}

.spinner-ring:nth-child(2) {
  border-top-color: #7B2CBF;
  animation-delay: -0.3s;
}

.spinner-ring:nth-child(3) {
  border-top-color: #00D9FF;
  animation-delay: -0.15s;
}

.spinner-ring:nth-child(4) {
  border-top-color: #FFD700;
}

@keyframes spinner-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.spinner-text {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}
</style>
