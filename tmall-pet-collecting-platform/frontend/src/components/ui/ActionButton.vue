<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'ghost', 'danger', 'success'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  icon: {
    type: [String, Object],
    default: null
  },
  iconPosition: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  },
  glow: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (e) => {
  if (!props.loading && !props.disabled) {
    emit('click', e)
  }
}

const buttonClasses = computed(() => [
  `action-btn`,
  `action-btn--${props.variant}`,
  `action-btn--${props.size}`,
  {
    'action-btn--loading': props.loading,
    'action-btn--disabled': props.disabled,
    'action-btn--block': props.block,
    'action-btn--glow': props.glow
  }
])
</script>

<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="action-btn__spinner"></span>
    <span v-if="icon && iconPosition === 'left' && !loading" class="action-btn__icon action-btn__icon--left">
      <component :is="icon" />
    </span>
    <span class="action-btn__content">
      <slot />
    </span>
    <span v-if="icon && iconPosition === 'right' && !loading" class="action-btn__icon action-btn__icon--right">
      <component :is="icon" />
    </span>
    <span v-if="glow" class="action-btn__glow"></span>
  </button>
</template>

<style scoped>
.action-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-family: var(--font-display);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  overflow: hidden;
}

/* Variants */
.action-btn--primary {
  background: var(--gradient-primary);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.action-btn--primary:hover {
  box-shadow: 0 6px 25px rgba(255, 107, 53, 0.5);
  transform: translateY(-2px);
}

.action-btn--primary.action-btn--glow:hover {
  box-shadow: 0 0 30px rgba(255, 107, 53, 0.6);
}

.action-btn--secondary {
  background: var(--bg-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

.action-btn--secondary:hover {
  background: var(--bg-tertiary);
  border-color: var(--neon-cyan);
  box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
}

.action-btn--ghost {
  background: transparent;
  color: var(--text-secondary);
}

.action-btn--ghost:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.action-btn--danger {
  background: linear-gradient(135deg, #FF3B30 0%, #FF6B6B 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 59, 48, 0.3);
}

.action-btn--danger:hover {
  box-shadow: 0 6px 25px rgba(255, 59, 48, 0.5);
  transform: translateY(-2px);
}

.action-btn--success {
  background: linear-gradient(135deg, #06FFA5 0%, #39FF14 100%);
  color: var(--bg-primary);
  box-shadow: 0 4px 15px rgba(6, 255, 165, 0.3);
}

.action-btn--success:hover {
  box-shadow: 0 6px 25px rgba(6, 255, 165, 0.5);
  transform: translateY(-2px);
}

/* Sizes */
.action-btn--small {
  padding: var(--space-xs) var(--space-md);
  font-size: 0.75rem;
  gap: var(--space-xs);
}

.action-btn--medium {
  padding: var(--space-sm) var(--space-lg);
}

.action-btn--large {
  padding: var(--space-md) var(--space-xl);
  font-size: 1rem;
  gap: var(--space-md);
}

/* States */
.action-btn--loading,
.action-btn--disabled {
  pointer-events: none;
  opacity: 0.7;
}

.action-btn--block {
  width: 100%;
}

/* Icon */
.action-btn__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.action-btn--small .action-btn__icon {
  width: 14px;
  height: 14px;
}

.action-btn--large .action-btn__icon {
  width: 20px;
  height: 20px;
}

/* Spinner */
.action-btn__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.action-btn--small .action-btn__spinner {
  width: 12px;
  height: 12px;
  border-width: 1.5px;
}

.action-btn--large .action-btn__spinner {
  width: 16px;
  height: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Glow effect */
.action-btn__glow {
  position: absolute;
  inset: -2px;
  background: inherit;
  filter: blur(10px);
  opacity: 0;
  transition: opacity var(--transition-base);
  z-index: -1;
  border-radius: inherit;
}

.action-btn--glow:hover .action-btn__glow {
  opacity: 0.5;
}

/* Content */
.action-btn__content {
  position: relative;
  z-index: 1;
}
</style>
