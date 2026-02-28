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
        <div class="header-icon-wrapper">
          <Trophy class="header-icon" />
        </div>
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
            <div class="metric-value primary">
              {{ activeSort === 'sales' ? formatNumber(product.sales) : formatPrice(product.price) }}
            </div>
          </div>
          <div v-if="activeSort === 'sales'" class="metric-group">
            <div class="metric-label">价格</div>
            <div class="metric-value secondary">{{ formatPrice(product.price) }}</div>
          </div>
          <div v-else class="metric-group">
            <div class="metric-label">销量</div>
            <div class="metric-value secondary">{{ formatNumber(product.sales) }}</div>
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Base Section - 清新自然风格
   ============================================ */
.top-products {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;

  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(45, 106, 79, 0.06);
}

/* ============================================
   Section Header
   ============================================ */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, #F5F5F4 0%, transparent 100%);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon-wrapper {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.08));
  border-radius: 10px;
  border: 1px solid rgba(116, 198, 157, 0.2);
}

.header-icon {
  width: 18px;
  height: 18px;
  color: var(--primary-green);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.section-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-subtitle {
  font-family: 'Nunito', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
}

/* ============================================
   Sort Tabs
   ============================================ */
.sort-tabs {
  display: flex;
  gap: 8px;
}

.sort-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.sort-tab:hover {
  background: #F5F5F4;
  border-color: var(--accent-green);
  color: var(--primary-green);
}

.sort-tab--active {
  background: linear-gradient(135deg,
    rgba(45, 106, 79, 0.1),
    rgba(116, 198, 157, 0.08));
  border-color: var(--accent-green);
  color: var(--primary-green);
  box-shadow: 0 4px 15px rgba(116, 198, 157, 0.2);
}

.tab-icon {
  width: 15px;
  height: 15px;
}

/* ============================================
   Products List
   ============================================ */
.products-list {
  padding: 18px 22px;
  display: grid;
  gap: 12px;
}

.product-card {
  display: grid;
  grid-template-columns: auto 68px 1fr auto;
  gap: 14px;
  align-items: center;
  padding: 14px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(45, 106, 79, 0.04);
}

.product-card:hover {
  background: #F5F5F4;
  border-color: var(--accent-green);
  transform: translateX(4px);
  box-shadow: 0 6px 20px rgba(45, 106, 79, 0.1);
}

.product-card--top {
  background: linear-gradient(135deg,
    rgba(45, 106, 79, 0.04) 0%,
    rgba(116, 198, 157, 0.02) 100%);
  border-color: rgba(116, 198, 157, 0.3);
}

.product-rank {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  border-radius: 10px;
  background: #F5F5F4;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3);
}

.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A8A8A8);
  color: #000;
  box-shadow: 0 6px 20px rgba(192, 192, 192, 0.3);
}

.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #B87333);
  color: #000;
  box-shadow: 0 6px 20px rgba(205, 127, 50, 0.3);
}

.rank-icon {
  font-size: 20px;
}

.rank-number {
  color: var(--text-tertiary);
}

.product-image {
  width: 68px;
  height: 68px;
  flex-shrink: 0;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid var(--border-light);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F5F5F4;
  border-radius: 10px;
  border: 1px solid var(--border-light);
}

.placeholder-icon {
  width: 28px;
  height: 28px;
  color: var(--text-tertiary);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.product-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-meta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  gap: 3px;
  font-size: 10px;
}

.meta-label {
  color: var(--text-tertiary);
}

.meta-value {
  color: var(--text-secondary);
  font-weight: 500;
}

.product-metrics {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-end;
}

.metric-group {
  text-align: right;
}

.metric-label {
  font-size: 10px;
  color: var(--text-tertiary);
  margin-bottom: 2px;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
}

.metric-value.primary {
  color: var(--primary-green);
}

.metric-value.secondary {
  color: var(--text-secondary);
}

.product-card--top .metric-value.primary {
  color: var(--accent-green);
}

.product-decoration {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg,
    var(--primary-green) 0%,
    var(--accent-green) 100%);
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
  min-height: 180px;
  color: var(--text-tertiary);
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 13px;
  margin: 0;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }

  .product-card {
    grid-template-columns: auto 56px 1fr;
    gap: 10px;
  }

  .product-image {
    width: 56px;
    height: 56px;
  }

  .product-metrics {
    grid-column: 2 / -1;
    flex-direction: row;
    justify-content: flex-start;
    gap: 18px;
  }

  .product-rank {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }

  .rank-icon {
    font-size: 16px;
  }
}
</style>
