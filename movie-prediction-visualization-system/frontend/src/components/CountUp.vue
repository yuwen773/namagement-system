<template>
  <span>{{ displayValue.toFixed(decimalPlaces) }}</span>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'

const props = defineProps({
  endValue: {
    type: [Number, String],
    required: true
  },
  duration: {
    type: Number,
    default: 1500
  }
})

const displayValue = ref(0)
const numValue = computed(() => {
  if (typeof props.endValue === 'string') {
    return parseFloat(props.endValue) || 0
  }
  return props.endValue
})

const decimalPlaces = computed(() => {
  if (typeof props.endValue === 'string' && props.endValue.includes('.')) {
    return props.endValue.split('.')[1].length
  }
  return 0
})

let animationFrame
let startTime

const animate = (timestamp) => {
  if (!startTime) startTime = timestamp
  const progress = timestamp - startTime
  const percentage = Math.min(progress / props.duration, 1)

  // 使用缓动函数 (easeOutQuart)
  const easeOut = 1 - Math.pow(1 - percentage, 4)
  displayValue.value = numValue.value * easeOut

  if (percentage < 1) {
    animationFrame = requestAnimationFrame(animate)
  } else {
    displayValue.value = numValue.value
  }
}

watch(() => props.endValue, () => {
  if (animationFrame) cancelAnimationFrame(animationFrame)
  startTime = null
  animationFrame = requestAnimationFrame(animate)
}, { immediate: true })

onUnmounted(() => {
  if (animationFrame) cancelAnimationFrame(animationFrame)
})
</script>
