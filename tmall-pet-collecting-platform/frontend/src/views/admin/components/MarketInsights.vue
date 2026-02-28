<script setup>
import { computed } from 'vue'
import { DataAnalysis, TrendCharts, Collection, Location, ShoppingCart } from '@element-plus/icons-vue'

const props = defineProps({
  insights: {
    type: Object,
    default: () => ({})
  }
})

const formatPrice = (price) => {
  if (!price) return '¥0'
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2
  }).format(price)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}

const insightCards = computed(() => {
  const data = props.insights
  if (!data) return []

  return [
    {
      title: '市场规模',
      icon: ShoppingCart,
      color: '#FF6B35',
      metrics: [
        { label: '商品总数', value: formatNumber(data.market_size?.total_products || 0) },
        { label: '店铺总数', value: formatNumber(data.market_size?.total_shops || 0) },
        { label: '总销量', value: formatNumber(data.market_size?.total_sales || 0) }
      ]
    },
    {
      title: '价格定位',
      icon: TrendCharts,
      color: '#FFD700',
      metrics: [
        { label: '平均价格', value: formatPrice(data.price_positioning?.avg_price || 0) },
        { label: '主力区间', value: data.price_positioning?.main_range || 'N/A' },
        { label: '区间占比', value: `${data.price_positioning?.main_range_pct?.toFixed(1) || 0}%` },
        { label: '高端占比', value: `${data.price_positioning?.high_end_pct?.toFixed(1) || 0}%` }
      ]
    },
    {
      title: '品牌洞察',
      icon: Collection,
      color: '#7B2CBF',
      metrics: [
        { label: 'Top品牌', value: data.brand_insights?.top_brand || 'N/A' },
        { label: '品牌数量', value: formatNumber(data.brand_insights?.total_brands || 0) },
        { label: 'Top品牌均价', value: formatPrice(data.brand_insights?.top_brand_avg_price || 0) }
      ]
    },
    {
      title: '数据质量',
      icon: DataAnalysis,
      color: '#06FFA5',
      metrics: [
        { label: '品牌覆盖', value: `${data.data_quality?.brand_coverage || 0}%` },
        { label: '地区覆盖', value: `${data.data_quality?.region_coverage || 0}%` },
        { label: '销量覆盖', value: `${data.data_quality?.sales_coverage || 0}%` }
      ]
    }
  ]
})
</script>

<template>
  <div class="market-insights">
    <div class="section-header">
      <div class="header-left">
        <DataAnalysis class="header-icon" />
        <div class="header-text">
          <h3 class="section-title">市场洞察</h3>
          <p class="section-subtitle">数据驱动的市场分析与趋势洞察</p>
        </div>
      </div>
      <div class="header-badge">综合分析</div>
    </div>

    <div class="insights-grid">
      <div
        v-for="(insight, index) in insightCards"
        :key="insight.title"
        class="insight-card"
        :style="{
          '--card-color': insight.color,
          'animation-delay': `${index * 0.1}s`
        }"
      >
        <div class="card-glow"></div>
        <div class="card-background"></div>

        <div class="card-header">
          <div class="icon-wrapper" :style="{ color: insight.color }">
            <component :is="insight.icon" class="card-icon" />
          </div>
          <h4 class="card-title">{{ insight.title }}</h4>
        </div>

        <div class="card-metrics">
          <div
            v-for="(metric, idx) in insight.metrics"
            :key="metric.label"
            class="metric-row"
            :style="{ 'animation-delay': `${index * 0.1 + idx * 0.05}s` }"
          >
            <span class="metric-label">{{ metric.label }}</span>
            <span class="metric-value">{{ metric.value }}</span>
          </div>
        </div>

        <div class="card-decoration"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Base Section
   ============================================ */
.market-insights {
  --primary-cyan: #4CC9F0;
  --primary-purple: #7B2CBF;
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);

  background: rgba(20, 20, 32, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 24px;
  overflow: hidden;
}

/* ============================================
   Section Header
   ============================================ */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  width: 22px;
  height: 22px;
  color: var(--primary-cyan);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.section-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-subtitle {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-badge {
  padding: 6px 14px;
  background: rgba(76, 201, 240, 0.1);
  border: 1px solid rgba(76, 201, 240, 0.2);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
  color: var(--primary-cyan);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Insights Grid
   ============================================ */
.insights-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  padding: 20px 24px;
}

.insight-card {
  position: relative;
  padding: 20px;
  background: rgba(20, 20, 32, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: insightFadeIn 0.5s ease-out both;
}

@keyframes insightFadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.insight-card:hover {
  transform: translateY(-4px);
  border-color: var(--card-color);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
}

.card-glow {
  position: absolute;
  bottom: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 100%;
  background: radial-gradient(ellipse at center,
    var(--card-color) 0%,
    transparent 70%);
  opacity: 0;
  filter: blur(40px);
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.insight-card:hover .card-glow {
  opacity: 0.25;
}

.card-background {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 80%, var(--card-color) 0%, transparent 50%);
  opacity: 0.04;
  pointer-events: none;
}

/* ============================================
   Card Header
   ============================================ */
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}

.icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s ease;
}

.insight-card:hover .icon-wrapper {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--card-color);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.card-icon {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 2px 6px var(--card-color));
}

.card-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* ============================================
   Card Metrics
   ============================================ */
.card-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  transition: all 0.3s ease;
  animation: metricSlideIn 0.4s ease-out both;
}

@keyframes metricSlideIn {
  from {
    opacity: 0;
    transform: translateX(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.insight-card:hover .metric-row {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.08);
}

.metric-label {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  color: var(--card-color);
}

.card-decoration {
  position: absolute;
  inset: 0;
  border-radius: 18px;
  padding: 1px;
  background: linear-gradient(135deg,
    var(--card-color) 0%,
    transparent 50%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.insight-card:hover .card-decoration {
  opacity: 0.2;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1400px) {
  .insights-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .insights-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    padding: 18px 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
}
</style>
