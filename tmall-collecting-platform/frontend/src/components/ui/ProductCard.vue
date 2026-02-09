<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  rank: {
    type: Number,
    default: null
  },
  compact: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()

const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0
  }).format(price)
}

const formatSales = (sales) => {
  if (sales >= 10000) {
    return `${(sales / 10000).toFixed(1)}万`
  }
  return new Intl.NumberFormat('zh-CN').format(sales)
}

const rankClass = computed(() => {
  if (!props.rank) return ''
  if (props.rank <= 3) return `rank-${props.rank}`
  return 'rank-other'
})

const rankColor = computed(() => {
  if (!props.rank) return null
  const colors = {
    1: 'var(--neon-yellow)',
    2: '#C0C0C0',
    3: '#CD7F32'
  }
  return colors[props.rank] || null
})

const handleClick = () => {
  router.push(`/user/products/${props.product.id}`)
}
</script>

<template>
  <div
    :class="['product-card', { compact, 'has-rank': rank }]"
    @click="handleClick"
  >
    <div v-if="rank" :class="['product-rank', rankClass]" :style="{ color: rankColor }">
      {{ rank }}
    </div>

    <div class="product-image-wrapper">
      <img
        :src="product.image_url || '/placeholder-product.png'"
        :alt="product.title"
        class="product-image"
        loading="lazy"
      />
      <div class="product-overlay">
        <div class="product-overlay-content">
          <span class="view-detail">查看详情</span>
        </div>
      </div>
      <div v-if="product.discount" class="discount-badge">
        -{{ product.discount }}%
      </div>
    </div>

    <div class="product-info">
      <h3 class="product-title" :title="product.title">
        {{ product.title }}
      </h3>

      <div class="product-meta">
        <span class="product-shop">{{ product.shop }}</span>
      </div>

      <div class="product-footer">
        <div class="product-price-group">
          <span class="product-price">{{ formatPrice(product.price) }}</span>
          <span v-if="product.originalPrice && product.originalPrice > product.price" class="product-original-price">
            {{ formatPrice(product.originalPrice) }}
          </span>
        </div>
        <div class="product-sales">
          <span>已售</span>
          <span class="sales-count">{{ formatSales(product.sales) }}</span>
        </div>
      </div>
    </div>

    <div class="card-shine"></div>
  </div>
</template>

<style scoped>
.product-card {
  background: var(--gradient-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
  border-color: var(--neon-orange);
}

.product-card.compact {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
}

.product-card.compact .product-image-wrapper {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
}

.product-card.compact .product-info {
  flex: 1;
}

.product-rank {
  position: absolute;
  top: var(--space-sm);
  left: var(--space-sm);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-elevated);
  border: 2px solid currentColor;
  border-radius: var(--radius-md);
  font-family: var(--font-display);
  font-size: 0.875rem;
  font-weight: 800;
  z-index: 10;
  box-shadow: 0 0 10px currentColor;
}

.product-rank.rank-1,
.product-rank.rank-2,
.product-rank.rank-3 {
  background: linear-gradient(135deg, currentColor 0%, rgba(0, 0, 0, 0.3) 100%);
}

.product-image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  overflow: hidden;
  background: var(--bg-tertiary);
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(10, 10, 18, 0.9) 0%,
    rgba(10, 10, 18, 0.5) 50%,
    transparent 100%
  );
  opacity: 0;
  transition: opacity var(--transition-base);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: var(--space-md);
}

.product-card:hover .product-overlay {
  opacity: 1;
}

.product-overlay-content {
  transform: translateY(10px);
  transition: transform var(--transition-base);
}

.product-card:hover .product-overlay-content {
  transform: translateY(0);
}

.view-detail {
  padding: var(--space-sm) var(--space-lg);
  background: var(--gradient-primary);
  color: white;
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: var(--radius-full);
}

.discount-badge {
  position: absolute;
  top: var(--space-sm);
  right: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  background: var(--status-error);
  color: white;
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 8px rgba(255, 59, 48, 0.4);
}

.product-info {
  padding: var(--space-md);
}

.product-title {
  font-family: var(--font-display);
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 var(--space-sm) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.8em;
}

.product-meta {
  margin-bottom: var(--space-sm);
}

.product-shop {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
}

.product-price-group {
  display: flex;
  align-items: baseline;
  gap: var(--space-xs);
}

.product-price {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--neon-orange);
}

.product-original-price {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.product-sales {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

.sales-count {
  font-weight: 600;
  color: var(--text-secondary);
}

.card-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.03) 50%,
    transparent 100%
  );
  transform: skewX(-20deg);
  transition: left 0.6s ease;
}

.product-card:hover .card-shine {
  left: 150%;
}

@media (max-width: 640px) {
  .product-card.compact {
    flex-direction: column;
  }

  .product-card.compact .product-image-wrapper {
    width: 100%;
    height: auto;
    aspect-ratio: 1;
  }
}
</style>
