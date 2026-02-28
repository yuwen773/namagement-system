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
      color: '#2D6A4F',
      metrics: [
        { label: '商品总数', value: formatNumber(data.market_size?.total_products || 0) },
        { label: '店铺总数', value: formatNumber(data.market_size?.total_shops || 0) },
        { label: '总销量', value: formatNumber(data.market_size?.total_sales || 0) }
      ]
    },
    {
      title: '价格定位',
      icon: TrendCharts,
      color: '#00B4D8',
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
      color: '#52B788',
      metrics: [
        { label: 'Top品牌', value: data.brand_insights?.top_brand || 'N/A' },
        { label: '品牌数量', value: formatNumber(data.brand_insights?.total_brands || 0) },
        { label: 'Top品牌均价', value: formatPrice(data.brand_insights?.top_brand_avg_price || 0) }
      ]
    },
    {
      title: '数据质量',
      icon: DataAnalysis,
      color: '#74C69D',
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
        <div class="header-icon-wrapper">
          <DataAnalysis class="header-icon" />
        </div>
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
        <div class="card-background">
          <div class="leaf-decoration">
            <svg viewBox="0 0 40 55" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 3C20 3 35 15 35 28C35 42 28 50 20 50C12 50 5 42 5 28C5 15 20 3 20 3Z" fill="currentColor" opacity="0.1"/>
            </svg>
          </div>
        </div>

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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Base Section - 清新自然风格
   ============================================ */
.market-insights {
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

.header-badge {
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.08));
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: var(--primary-green);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Insights Grid
   ============================================ */
.insights-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  padding: 18px 22px;
}

.insight-card {
  position: relative;
  padding: 18px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: insightFadeIn 0.5s ease-out both;
  box-shadow: 0 2px 8px rgba(45, 106, 79, 0.04);
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
  box-shadow: 0 12px 30px rgba(45, 106, 79, 0.15);
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
  opacity: 0.2;
}

.card-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.leaf-decoration {
  position: absolute;
  bottom: -8px;
  right: -8px;
  width: 45px;
  height: 60px;
  color: var(--card-color);
  opacity: 0.12;
  transition: all 0.3s ease;
}

.insight-card:hover .leaf-decoration {
  transform: scale(1.1) rotate(5deg);
  opacity: 0.2;
}

/* ============================================
   Card Header
   ============================================ */
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  position: relative;
  z-index: 1;
}

.icon-wrapper {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.08), rgba(116, 198, 157, 0.05));
  border-radius: 10px;
  border: 1px solid rgba(116, 198, 157, 0.2);
  transition: all 0.3s ease;
}

.insight-card:hover .icon-wrapper {
  background: linear-gradient(135deg, var(--card-color) 15%, rgba(116, 198, 157, 0.1) 100%);
  border-color: var(--card-color);
  box-shadow: 0 6px 20px rgba(45, 106, 79, 0.15);
}

.card-icon {
  width: 18px;
  height: 18px;
  transition: color 0.3s ease;
}

.insight-card:hover .card-icon {
  color: white;
}

.card-title {
  font-family: 'Noto Serif SC', serif;
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
  background: #F5F5F4;
  border-radius: 8px;
  border: 1px solid var(--border-light);
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
  background: white;
  border-color: rgba(116, 198, 157, 0.3);
}

.metric-label {
  font-family: 'Noto Serif SC', serif;
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
  border-radius: 16px;
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
  opacity: 0.3;
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
    padding: 16px 18px;
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
}
</style>
