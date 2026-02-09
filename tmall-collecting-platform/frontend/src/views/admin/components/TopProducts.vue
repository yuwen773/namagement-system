<script setup>
import { ref, computed } from 'vue'
import { TrendCharts, Trophy, ShoppingBag } from '@element-plus/icons-vue'

const props = defineProps({
  salesProducts: {
    type: Array,
    default: () => []
  },
  priceProducts: {
    type: Array,
    default: () => []
  },
  activeSort: {
    type: String,
    default: 'sales'
  }
})

const emit = defineEmits(['sort-change'])

const sortOptions = [
  { key: 'sales', label: '按销量', icon: TrendCharts },
  { key: 'price', label: '按价格', icon: ShoppingBag }
]

const displayProducts = computed(() => {
  if (props.activeSort === 'sales') {
    return props.salesProducts?.slice(0, 10) || []
  }
  return props.priceProducts?.slice(0, 10) || []
})

const formatPrice = (price) => {
  if (!price) return '¥0'
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0
  }).format(price)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}
</script>

<template>
  <div class="top-products">
    <div class="section-header">
      <div class="header-left">
        <Trophy class="header-icon" />
        <div class="header-text">
          <h3 class="section-title">热门商品排行</h3>
          <p class="section-subtitle">市场热门商品追踪与对比</p>
        </div>
      </div>
      <div class="sort-tabs">
        <button
          v-for="option in sortOptions"
          :key="option.key"
          :class="['sort-tab', { 'sort-tab--active': activeSort === option.key }]"
          @click="emit('sort-change', option.key)"
        >
          <component :is="option.icon" class="tab-icon" />
          {{ option.label }}
        </button>
      </div>
    </div>

    <div class="products-list">
      <div
        v-for="(product, index) in displayProducts"
        :key="product.id"
        class="product-card"
        :class="{ 'product-card--top': index < 3 }"
      >
        <div class="product-rank" :class="`rank-${index + 1}`">
          <span v-if="index < 3" class="rank-icon">🏆</span>
          <span v-else class="rank-number">{{ index + 1 }}</span>
        </div>

        <div class="product-image">
          <img
            v-if="product.image_url"
            :src="product.image_url"
            :alt="product.title"
            class="image"
          />
          <div v-else class="image-placeholder">
            <ShoppingBag class="placeholder-icon" />
          </div>
        </div>

        <div class="product-info">
          <h4 class="product-title" :title="product.title">
            {{ product.title }}
          </h4>
          <div class="product-meta">
            <span class="meta-item">
              <span class="meta-label">店铺</span>
              <span class="meta-value">{{ product.shop || '未知' }}</span>
            </span>
            <span class="meta-item" v-if="product.brand">
              <span class="meta-label">品牌</span>
              <span class="meta-value">{{ product.brand }}</span>
            </span>
            <span class="meta-item" v-if="product.region">
              <span class="meta-label">地区</span>
              <span class="meta-value">{{ product.region }}</span>
            </span>
          </div>
        </div>

        <div class="product-metrics">
          <div class="metric-group">
            <div class="metric-label">{{ activeSort === 'sales' ? '销量' : '价格' }}</div>
            <div class="metric-value">
              {{ activeSort === 'sales' ? formatNumber(product.sales) : formatPrice(product.price) }}
            </div>
          </div>
          <div v-if="activeSort === 'sales'" class="metric-group">
            <div class="metric-label">价格</div>
            <div class="metric-value">{{ formatPrice(product.price) }}</div>
          </div>
          <div v-else class="metric-group">
            <div class="metric-label">销量</div>
            <div class="metric-value">{{ formatNumber(product.sales) }}</div>
          </div>
        </div>

        <div class="product-decoration"></div>
      </div>

      <div v-if="displayProducts.length === 0" class="products-empty">
        <div class="empty-icon">📦</div>
        <p class="empty-text">暂无商品数据</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.top-products {
  background: linear-gradient(135deg,
    rgba(255, 107, 53, 0.05) 0%,
    rgba(123, 44, 191, 0.05) 100%);
  border: 1px solid rgba(255, 107, 53, 0.1);
  border-radius: 24px;
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #FFD700;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-family: 'Exo 2', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
}

.section-subtitle {
  font-family: 'Exo 2', sans-serif;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.sort-tabs {
  display: flex;
  gap: 8px;
}

.sort-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  font-family: 'Exo 2', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s ease;
}

.sort-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 107, 53, 0.3);
  color: rgba(255, 255, 255, 0.9);
}

.sort-tab--active {
  background: linear-gradient(135deg,
    rgba(255, 107, 53, 0.2),
    rgba(123, 44, 191, 0.2));
  border-color: rgba(255, 107, 53, 0.4);
  color: #FF6B35;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.2);
}

.tab-icon {
  width: 16px;
  height: 16px;
}

.products-list {
  padding: 24px;
  display: grid;
  gap: 16px;
}

.product-card {
  display: grid;
  grid-template-columns: auto 80px 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.product-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 107, 53, 0.2);
  transform: translateX(4px);
}

.product-card--top {
  background: linear-gradient(135deg,
    rgba(255, 215, 0, 0.08) 0%,
    rgba(255, 107, 53, 0.05) 100%);
  border-color: rgba(255, 215, 0, 0.2);
}

.product-rank {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', monospace;
  font-size: 20px;
  font-weight: 700;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
}

.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A8A8A8);
  color: #000;
  box-shadow: 0 8px 25px rgba(192, 192, 192, 0.4);
}

.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #B87333);
  color: #000;
  box-shadow: 0 8px 25px rgba(205, 127, 50, 0.4);
}

.rank-icon {
  font-size: 24px;
}

.rank-number {
  color: rgba(255, 255, 255, 0.5);
}

.product-image {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.placeholder-icon {
  width: 32px;
  height: 32px;
  color: rgba(255, 255, 255, 0.2);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.product-title {
  font-family: 'Exo 2', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  gap: 4px;
  font-size: 11px;
}

.meta-label {
  color: rgba(255, 255, 255, 0.4);
}

.meta-value {
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.product-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.metric-group {
  text-align: right;
}

.metric-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 2px;
}

.metric-value {
  font-family: 'Orbitron', monospace;
  font-size: 18px;
  font-weight: 700;
  color: #FF6B35;
}

.product-card--top .metric-value {
  color: #FFD700;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

.product-decoration {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg,
    rgba(255, 107, 53, 0.6) 0%,
    rgba(123, 44, 191, 0.6) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-decoration {
  opacity: 1;
}

.products-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: rgba(255, 255, 255, 0.3);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-family: 'Exo 2', sans-serif;
  font-size: 14px;
  margin: 0;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .product-card {
    grid-template-columns: auto 60px 1fr;
    gap: 12px;
  }

  .product-image {
    width: 60px;
    height: 60px;
  }

  .product-metrics {
    grid-column: 2 / -1;
    flex-direction: row;
    justify-content: flex-start;
    gap: 24px;
  }

  .product-rank {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }

  .rank-icon {
    font-size: 20px;
  }
}
</style>
