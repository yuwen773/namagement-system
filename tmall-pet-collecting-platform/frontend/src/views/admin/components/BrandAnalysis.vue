<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { Collection } from '@element-plus/icons-vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const chartRef = ref(null)
let chartInstance = null

const topBrands = computed(() => {
  return props.data?.slice(0, 8) || []
})

// 清新自然风格配色
const natureColors = ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#00B4D8', '#90E0EF']

const initChart = () => {
  if (!chartRef.value || !topBrands.value.length) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E7E5E4',
      borderWidth: 1,
      textStyle: { color: '#1C1917', fontSize: 13 },
      formatter: (params) => {
        const brand = params[0].name
        const item = topBrands.value.find(b => b.brand === brand)
        return `
          <div style="padding: 8px;">
            <div style="font-weight: 600; margin-bottom: 8px; color: #1C1917;">${brand}</div>
            <div style="color: #57534E;">商品数: ${item?.count || 0}</div>
            <div style="color: #57534E;">均价: ¥${item?.price?.avg?.toFixed(2) || '0'}</div>
            <div style="color: #57534E;">均销量: ${Math.round(item?.sales?.avg || 0)}</div>
          </div>
        `
      }
    },
    radar: {
      indicator: topBrands.value.slice(0, 6).map(brand => ({
        name: brand.brand?.length > 8 ? brand.brand.slice(0, 8) + '...' : brand.brand || '未分类',
        max: Math.max(...topBrands.value.map(b => b.count))
      })),
      shape: 'polygon',
      splitNumber: 4,
      axisName: {
        color: '#57534E',
        fontSize: 11,
        fontFamily: 'Noto Serif SC, serif'
      },
      splitLine: {
        lineStyle: { color: '#E7E5E4' }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(45, 106, 79, 0.03)', 'rgba(116, 198, 157, 0.03)']
        }
      },
      axisLine: {
        lineStyle: { color: '#E7E5E4' }
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: topBrands.value.slice(0, 6).map(b => b.count),
        name: '品牌分布',
        areaStyle: {
          color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
            { offset: 0, color: 'rgba(45, 106, 79, 0.4)' },
            { offset: 1, color: 'rgba(116, 198, 157, 0.2)' }
          ])
        },
        lineStyle: {
          width: 2,
          color: '#2D6A4F'
        },
        itemStyle: {
          color: '#2D6A4F'
        },
        symbol: 'circle',
        symbolSize: 6
      }]
    }]
  }

  chartInstance.setOption(option)
}

watch(() => props.data, () => {
  initChart()
}, { deep: true })

onMounted(() => {
  initChart()

  const resizeHandler = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }

  window.addEventListener('resize', resizeHandler)

  onUnmounted(() => {
    window.removeEventListener('resize', resizeHandler)
    if (chartInstance) {
      chartInstance.dispose()
    }
  })
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}
</script>

<template>
  <div class="brand-analysis">
    <div class="section-header">
      <div class="header-left">
        <div class="header-icon-wrapper">
          <Collection class="header-icon" />
        </div>
        <div class="header-text">
          <h3 class="section-title">品牌分析</h3>
          <p class="section-subtitle">品牌分布与市场占有率</p>
        </div>
      </div>
      <div class="header-badge">TOP 8</div>
    </div>

    <div class="analysis-content">
      <div class="radar-chart">
        <div v-if="topBrands.length > 0" ref="chartRef" class="chart-wrapper"></div>
        <div v-else class="chart-empty">
          <div class="empty-icon">📊</div>
          <p class="empty-text">暂无品牌数据</p>
        </div>
      </div>

      <div class="brand-list">
        <div
          v-for="(brand, index) in topBrands"
          :key="brand.brand"
          class="brand-item"
          :class="{ 'brand-item--top': index < 3 }"
        >
          <div class="brand-rank" :class="`rank-${index + 1}`">
            {{ index + 1 }}
          </div>
          <div class="brand-info">
            <div class="brand-name">{{ brand.brand || '未分类' }}</div>
            <div class="brand-metrics">
              <span class="metric">
                <span class="metric-label">商品</span>
                <span class="metric-value">{{ formatNumber(brand.count) }}</span>
              </span>
              <span class="metric">
                <span class="metric-label">均价</span>
                <span class="metric-value">¥{{ brand.price?.avg?.toFixed(0) || '0' }}</span>
              </span>
              <span class="metric">
                <span class="metric-label">均销</span>
                <span class="metric-value">{{ formatNumber(Math.round(brand.sales?.avg || 0)) }}</span>
              </span>
            </div>
          </div>
          <div class="brand-bar">
            <div
              class="bar-fill"
              :style="{
                width: `${(brand.count / topBrands[0].count) * 100}%`,
                background: index < 3
                  ? `linear-gradient(90deg, ${natureColors[index]}, ${natureColors[index + 1]})`
                  : '#E7E5E4'
              }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Base Analysis - 清新自然风格
   ============================================ */
.brand-analysis {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;

  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(45, 106, 79, 0.06);
}

.brand-analysis:hover {
  box-shadow: 0 8px 30px rgba(45, 106, 79, 0.12);
  transform: translateY(-2px);
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
   Analysis Content
   ============================================ */
.analysis-content {
  padding: 18px 22px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.radar-chart {
  min-height: 320px;
}

.chart-wrapper {
  width: 100%;
  height: 320px;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 320px;
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
   Brand List
   ============================================ */
.brand-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 320px;
  overflow-y: auto;
  padding-right: 8px;
}

.brand-list::-webkit-scrollbar {
  width: 5px;
}

.brand-list::-webkit-scrollbar-track {
  background: #F5F5F4;
  border-radius: 3px;
}

.brand-list::-webkit-scrollbar-thumb {
  background: #E7E5E4;
  border-radius: 3px;
}

.brand-list::-webkit-scrollbar-thumb:hover {
  background: #D6D3D1;
}

.brand-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--bg-card);
  border-radius: 12px;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.brand-item:hover {
  background: #F5F5F4;
  border-color: var(--accent-green);
  transform: translateX(3px);
}

.brand-item--top {
  background: linear-gradient(135deg,
    rgba(45, 106, 79, 0.05) 0%,
    rgba(116, 198, 157, 0.03) 100%);
  border-color: rgba(116, 198, 157, 0.3);
}

.brand-rank {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  border-radius: 8px;
  background: #F5F5F4;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  box-shadow: 0 3px 12px rgba(255, 215, 0, 0.25);
}

.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A8A8A8);
  color: #000;
  box-shadow: 0 3px 12px rgba(192, 192, 192, 0.25);
}

.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #B87333);
  color: #000;
  box-shadow: 0 3px 12px rgba(205, 127, 50, 0.25);
}

.brand-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.brand-name {
  font-family: 'Noto Serif SC', serif;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.brand-metrics {
  display: flex;
  gap: 10px;
}

.metric {
  display: flex;
  gap: 3px;
  font-size: 10px;
}

.metric-label {
  color: var(--text-tertiary);
}

.metric-value {
  color: var(--text-secondary);
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

.brand-bar {
  width: 60px;
  height: 3px;
  background: #F5F5F4;
  border-radius: 2px;
  overflow: hidden;
  flex-shrink: 0;
}

.bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1200px) {
  .analysis-content {
    grid-template-columns: 1fr;
  }

  .radar-chart {
    min-height: 280px;
  }

  .chart-wrapper {
    height: 280px;
  }

  .brand-list {
    max-height: 200px;
  }
}
</style>
