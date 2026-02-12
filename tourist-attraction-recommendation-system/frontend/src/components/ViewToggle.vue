<template>
  <div class="view-toggle">
    <button
      v-for="mode in modes"
      :key="mode.value"
      :class="['toggle-button', { active: modelValue === mode.value }]"
      @click="$emit('update:modelValue', mode.value)"
    >
      <svg viewBox="0 0 20 20" v-html="mode.icon"></svg>
      <span>{{ mode.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String
})

defineEmits(['update:modelValue'])

const modes = [
  {
    value: 'list',
    label: '列表',
    icon: '<path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>'
  },
  {
    value: 'card',
    label: '卡片',
    icon: '<path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>'
  }
]
</script>

<style scoped>
.view-toggle {
  display: flex;
  gap: 8px;
  padding: 4px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
}

.toggle-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-button svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.toggle-button:hover {
  background: #f9fafb;
}

.toggle-button.active {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
}
</style>
