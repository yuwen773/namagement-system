<template>
  <div class="ingredient-frequency-page">
    <!-- Page Header -->
    <div class="page-header">
      <h1 class="page-title">食材频率分析</h1>
      <p class="page-subtitle">探索最受欢迎的食材使用数据</p>
    </div>

    <!-- Controls Bar -->
    <div class="controls-bar">
      <!-- Category Filter -->
      <div class="filter-group">
        <label class="filter-label">分类筛选</label>
        <div class="category-tabs">
          <button
            v-for="cat in categories"
            :key="cat.value"
            class="category-tab"
            :class="{ active: selectedCategory === cat.value }"
            @click="selectCategory(cat.value)"
          >
            <span class="tab-icon">{{ cat.icon }}</span>
            <span class="tab-text">{{ cat.label }}</span>
          </button>
        </div>
      </div>

      <!-- Limit Selector -->
      <div class="filter-group">
        <label class="filter-label">显示数量</label>
        <div class="limit-selector">
          <button
            v-for="limit in limitOptions"
            :key="limit"
            class="limit-btn"
            :class="{ active: selectedLimit === limit }"
            @click="selectLimit(limit)"
          >
            Top {{ limit }}
          </button>
        </div>
      </div>

      <!-- Search -->
      <div class="filter-group search-group">
        <label class="filter-label">搜索食材</label>
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 20 20" fill="none">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l-4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="输入食材名称..."
            @keyup.enter="handleSearch"
          >
          <button v-if="searchQuery" class="clear-btn" @click="clearSearch">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M15 5l-10 10M5 5l10 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Refresh Button -->
      <button class="refresh-btn" @click="fetchData" :disabled="loading">
        <svg class="refresh-icon" :class="{ spinning: loading }" viewBox="0 0 20 20" fill="none">
          <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>刷新</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !ingredients.length" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">加载数据中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">!</div>
      <h3 class="error-title">数据加载失败</h3>
      <p class="error-message">{{ error }}</p>
      <button @click="fetchData" class="retry-button">重试</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!ingredients.length && !loading" class="empty-container">
      <svg class="empty-icon" viewBox="0 0 80 80" fill="none">
        <circle cx="40" cy="40" r="32" stroke="#e5ddd3" stroke-width="2" stroke-dasharray="4 4"/>
        <path d="M28 40h24M40 28v24" stroke="#c2622e" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <h3 class="empty-title">暂无数据</h3>
      <p class="empty-message">未找到符合条件的食材，请尝试调整筛选条件</p>
    </div>

    <!-- Results Display -->
    <div v-else class="results-container">
      <!-- Summary Stats -->
      <div class="stats-row">
        <div class="stat-card" v-for="(stat, index) in stats" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
          <div class="stat-icon" :style="{ background: stat.color }">
            <svg viewBox="0 0 20 20" fill="none" v-html="stat.iconSvg"></svg>
          </div>
          <div class="stat-content">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>

      <!-- Ingredients Ranking List -->
      <div class="ranking-section">
        <h3 class="section-title">
          <span class="title-icon">🏆</span>
          食材使用频率排行
        </h3>
        <div class="ranking-list">
          <div
            v-for="(item, index) in ingredients"
            :key="item.id"
            class="ranking-item"
            :style="{ animationDelay: `${index * 0.03}s` }"
            :class="{ 'top-three': index < 3 }"
          >
            <!-- Rank Badge -->
            <div class="rank-badge" :class="`rank-${index + 1}`">
              <span v-if="index < 3" class="medal">{{ ['🥇', '🥈', '🥉'][index] }}</span>
              <span v-else class="number">{{ index + 1 }}</span>
            </div>

            <!-- Ingredient Info -->
            <div class="ingredient-info">
              <span class="ingredient-name">{{ item.name }}</span>
              <span class="ingredient-category">{{ getCategoryLabel(item.category) }}</span>
            </div>

            <!-- Usage Count & Bar -->
            <div class="usage-section">
              <span class="usage-count">{{ item.count.toLocaleString() }}</span>
              <div class="usage-bar-bg">
                <div
                  class="usage-bar-fill"
                  :style="{
                    width: `${(item.count / maxCount) * 100}%`,
                    background: getBarColor(index)
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Section -->
      <div class="chart-section">
        <h3 class="section-title">
          <span class="title-icon">📊</span>
          可视化图表
        </h3>
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { getIngredientsAnalytics } from '../api/analytics'

// Categories config
const categories = [
  { value: '', label: '全部', icon: '🌟' },
  { value: 'vegetable', label: '蔬菜', icon: '🥬' },
  { value: 'meat', label: '肉类', icon: '🥩' },
  { value: 'seafood', label: '海鲜', icon: '🦐' },
  { value: 'seasoning', label: '调料', icon: '🧂' },
  { value: 'fruit', label: '水果', icon: '🍎' },
  { value: 'grain', label: '谷物', icon: '🌾' },
  { value: 'dairy', label: '乳制品', icon: '🧈' },
  { value: 'other', label: '其他', icon: '📦' }
]

const limitOptions = [20, 50, 100]

// State
const loading = ref(false)
const error = ref(null)
const ingredients = ref([])
const selectedCategory = ref('')
const selectedLimit = ref(20)
const searchQuery = ref('')
const chartRef = ref(null)
let chartInstance = null

// Colors for bars
const barColors = [
  'linear-gradient(135deg, #d4773a 0%, #c2622e 100%)',
  'linear-gradient(135deg, #e8a87c 0%, #d4773a 100%)',
  'linear-gradient(135deg, #c9976b 0%, #a35220 100%)',
  'linear-gradient(135deg, #f4c89a 0%, #c9976b 100%)',
  'linear-gradient(135deg, #8b5a2b 0%, #6b4423 100%)'
]

// Computed
const maxCount = computed(() => {
  return ingredients.value.length > 0 ? Math.max(...ingredients.value.map(i => i.count)) : 0
})

const totalCount = computed(() => {
  return ingredients.value.reduce((sum, item) => sum + item.count, 0)
})

const topIngredient = computed(() => {
  return ingredients.value.length > 0 ? ingredients.value[0] : null
})

const categoryCount = computed(() => {
  const uniqueCategories = new Set(ingredients.value.map(i => i.category))
  return uniqueCategories.size
})

const stats = computed(() => [
  {
    label: '食材总数',
    value: ingredients.value.length,
    color: 'linear-gradient(135deg, #d4773a 0%, #c2622e 100%)',
    iconSvg: '<path d="M4 4h16v16H4z" stroke="white" stroke-width="1.5"/>'
  },
  {
    label: '总使用次数',
    value: totalCount.value.toLocaleString(),
    color: 'linear-gradient(135deg, #e8a87c 0%, #d4773a 100%)',
    iconSvg: '<path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
  },
  {
    label: '最高频食材',
    value: topIngredient.value ? topIngredient.value.name : '-',
    color: 'linear-gradient(135deg, #f4c89a 0%, #c9976b 100%)',
    iconSvg: '<path d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
  },
  {
    label: '覆盖分类',
    value: categoryCount.value,
    color: 'linear-gradient(135deg, #c9976b 0%, #8b5a2b 100%)',
    iconSvg: '<circle cx="8" cy="8" r="6" stroke="white" stroke-width="1.5"/><path d="M8 4v4m0 0h4" stroke="white" stroke-width="1.5" stroke-linecap="round"/>'
  }
])

// Methods
function getCategoryLabel(category) {
  const cat = categories.find(c => c.value === category)
  return cat ? cat.label : category
}

function getBarColor(index) {
  return barColors[index % barColors.length]
}

function selectCategory(value) {
  selectedCategory.value = value
  fetchData()
}

function selectLimit(value) {
  selectedLimit.value = value
  fetchData()
}

function handleSearch() {
  fetchData()
}

function clearSearch() {
  searchQuery.value = ''
  fetchData()
}

async function fetchData() {
  loading.value = true
  error.value = null

  try {
    const params = { limit: selectedLimit.value }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }

    const response = await getIngredientsAnalytics(params)
    ingredients.value = response.data || []

    // Render chart after data loads
    if (ingredients.value.length > 0) {
      setTimeout(() => renderChart(), 100)
    }
  } catch (err) {
    error.value = err.message || '数据加载失败，请稍后重试'
    ingredients.value = []
  } finally {
    loading.value = false
  }
}

function renderChart() {
  if (!chartRef.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)

  const data = ingredients.value.slice(0, 15).reverse()
  const maxValue = Math.max(...data.map(d => d.count))

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' },
      formatter: (params) => {
        const item = params[0]
        return `${item.name}<br/>使用次数: <b>${item.value.toLocaleString()}</b>`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      max: maxValue * 1.1,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: {
        lineStyle: { color: '#f0ebe3', type: 'dashed' }
      },
      axisLabel: {
        color: '#8b7355',
        fontFamily: 'DM Sans',
        fontSize: 10
      }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 11
      }
    },
    series: [{
      type: 'bar',
      data: data.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 1, y2: 0,
            colorStops: [
              { offset: 0, color: '#d4773a' },
              { offset: 1, color: '#c2622e' }
            ]
          },
          borderRadius: [0, 6, 6, 0]
        }
      })),
      barWidth: '60%',
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(194, 98, 46, 0.4)'
        }
      },
      animationDelay: (idx) => idx * 50
    }]
  }

  chartInstance.setOption(option)
}

function handleResize() {
  chartInstance?.resize()
}

// Lifecycle
onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  chartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})

// Watch for data changes to re-render chart
watch(ingredients, () => {
  if (ingredients.value.length > 0) {
    renderChart()
  }
}, { deep: true })
</script>

<style scoped>
/* Google Fonts Import */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

/* CSS Variables */
.ingredient-frequency-page {
  --color-primary-light: #d4773a;
  --color-primary: #c2622e;
  --color-primary-dark: #a35220;
  --color-text-primary: #3d2914;
  --color-text-secondary: #6b5c4d;
  --color-text-tertiary: #8b7355;
  --color-text-hint: #b8a99a;
  --color-bg-primary: #faf8f5;
  --color-bg-elevated: #ffffff;
  --color-border-light: #e5ddd3;
  --shadow-card: 0 4px 24px rgba(61, 41, 20, 0.08), 0 0 1px rgba(61, 41, 20, 0.1);
  --shadow-primary: 0 8px 24px rgba(194, 98, 46, 0.35);
  --gradient-primary: linear-gradient(135deg, #d4773a 0%, #c2622e 50%, #a35220 100%);
  --gradient-bg: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
  --radius-2xl: 24px;
  --radius-lg: 16px;
  --radius-md: 12px;
  --font-display: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;

  min-height: 100vh;
  background: var(--gradient-bg);
  padding: 6rem 2rem 2rem;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 2rem;
  animation: fadeInUp 0.6s ease-out;
}

.page-title {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.page-subtitle {
  font-family: var(--font-body);
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* Controls Bar */
.controls-bar {
  max-width: 1200px;
  margin: 0 auto 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-end;
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-family: var(--font-body);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Category Tabs */
.category-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.5rem 0.85rem;
  background: var(--color-bg-elevated);
  border: 1.5px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-tab:hover {
  border-color: var(--color-primary-light);
  color: var(--color-primary);
}

.category-tab.active {
  background: var(--gradient-primary);
  border-color: transparent;
  color: white;
  box-shadow: var(--shadow-primary);
}

.tab-icon {
  font-size: 1rem;
}

/* Limit Selector */
.limit-selector {
  display: flex;
  gap: 0.5rem;
}

.limit-btn {
  padding: 0.5rem 1rem;
  background: var(--color-bg-elevated);
  border: 1.5px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.limit-btn:hover {
  border-color: var(--color-primary-light);
  color: var(--color-primary);
}

.limit-btn.active {
  background: var(--gradient-primary);
  border-color: transparent;
  color: white;
}

/* Search Box */
.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box input {
  width: 220px;
  height: 42px;
  padding: 0 2.5rem 0 2.5rem;
  background: var(--color-bg-elevated);
  border: 1.5px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--color-text-primary);
  outline: none;
  transition: border-color 0.2s ease;
}

.search-box input:focus {
  border-color: var(--color-primary);
}

.search-box input::placeholder {
  color: var(--color-text-hint);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  width: 16px;
  height: 16px;
  color: var(--color-text-hint);
  pointer-events: none;
}

.clear-btn {
  position: absolute;
  right: 0.5rem;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-border-light);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: var(--color-text-hint);
}

.clear-btn svg {
  width: 12px;
  height: 12px;
  color: var(--color-text-secondary);
}

/* Refresh Button */
.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  background: var(--gradient-primary);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-primary);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.refresh-icon.spinning {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  animation: fadeIn 0.4s ease-out;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--color-border-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  margin-top: 1.5rem;
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  animation: fadeIn 0.4s ease-out;
}

.error-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--gradient-primary);
  color: white;
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.error-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 1rem 0;
}

.error-message {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  margin: 0 0 2rem 0;
  text-align: center;
  max-width: 400px;
}

.retry-button {
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 600;
  color: white;
  background: var(--gradient-primary);
  border: none;
  border-radius: var(--radius-md);
  padding: 0.75rem 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-primary);
}

/* Empty State */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  animation: fadeIn 0.4s ease-out;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 1.5rem;
}

.empty-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 0.75rem 0;
}

.empty-message {
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* Results Container */
.results-container {
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  animation: fadeInUp 0.5s ease-out both;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.stat-value {
  font-family: var(--font-body);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.stat-label {
  font-family: var(--font-body);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Ranking Section */
.ranking-section {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-2xl);
  padding: 2rem;
  box-shadow: var(--shadow-card);
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 1.5rem 0;
}

.title-icon {
  font-size: 1.5rem;
}

/* Ranking List */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  transition: all 0.2s ease;
  animation: fadeInUp 0.4s ease-out both;
}

.ranking-item:hover {
  background: #f5efe6;
  transform: translateX(4px);
}

.ranking-item.top-three {
  background: linear-gradient(135deg, rgba(212, 119, 58, 0.08) 0%, rgba(194, 98, 46, 0.08) 100%);
  border: 1px solid rgba(194, 98, 46, 0.15);
}

.rank-badge {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rank-badge .medal {
  font-size: 1.5rem;
}

.rank-badge .number {
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text-hint);
}

.ingredient-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.ingredient-name {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.ingredient-category {
  font-family: var(--font-body);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-tertiary);
}

.usage-section {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.4rem;
  min-width: 120px;
}

.usage-count {
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-primary);
}

.usage-bar-bg {
  width: 100%;
  height: 8px;
  background: var(--color-border-light);
  border-radius: 4px;
  overflow: hidden;
}

.usage-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease-out;
}

/* Chart Section */
.chart-section {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-2xl);
  padding: 2rem;
  box-shadow: var(--shadow-card);
}

.chart-container {
  width: 100%;
  height: 400px;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .ranking-item {
    flex-wrap: wrap;
  }

  .usage-section {
    width: 100%;
    min-width: auto;
  }
}

@media (max-width: 768px) {
  .ingredient-frequency-page {
    padding: 5rem 1rem 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .controls-bar {
    gap: 1rem;
  }

  .filter-group {
    width: 100%;
  }

  .category-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.25rem;
  }

  .search-box input {
    width: 100%;
  }

  .stats-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .ranking-section,
  .chart-section {
    padding: 1.5rem;
  }

  .chart-container {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .rank-badge {
    width: 36px;
    height: 36px;
  }

  .rank-badge .medal {
    font-size: 1.25rem;
  }

  .ingredient-name {
    font-size: 0.9rem;
  }
}
</style>
