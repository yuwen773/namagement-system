<template>
  <div class="analytics-page">
    <!-- Page Header -->
    <div class="page-header">
      <h1 class="page-title">数据分析</h1>
      <p class="page-subtitle">探索菜谱数据的深层洞察</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
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

    <!-- Charts Grid -->
    <div v-else class="charts-grid">
      <!-- Cuisine Distribution Chart -->
      <div class="chart-card" style="animation-delay: 0.1s">
        <div class="chart-header">
          <h3 class="chart-title">菜系分布</h3>
          <span class="chart-subtitle">各菜系占比分析</span>
        </div>
        <div ref="cuisineChart" class="chart-container"></div>
      </div>

      <!-- Difficulty Level Chart -->
      <div class="chart-card" style="animation-delay: 0.2s">
        <div class="chart-header">
          <h3 class="chart-title">难度统计</h3>
          <span class="chart-subtitle">难度等级分布</span>
        </div>
        <div ref="difficultyChart" class="chart-container"></div>
      </div>

      <!-- Flavor Preference Chart -->
      <div class="chart-card" style="animation-delay: 0.3s">
        <div class="chart-header">
          <h3 class="chart-title">口味偏好</h3>
          <span class="chart-subtitle">口味标签分析</span>
        </div>
        <div ref="flavorChart" class="chart-container"></div>
      </div>

      <!-- Top Ingredients Chart -->
      <div class="chart-card" style="animation-delay: 0.4s">
        <div class="chart-header">
          <h3 class="chart-title">高频食材</h3>
          <span class="chart-subtitle">Top 15 使用食材</span>
        </div>
        <div ref="ingredientChart" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import {
  getCuisinesAnalytics,
  getDifficultyAnalytics,
  getFlavorsAnalytics,
  getIngredientsAnalytics
} from '../api/analytics'

// Chart refs
const cuisineChart = ref(null)
const difficultyChart = ref(null)
const flavorChart = ref(null)
const ingredientChart = ref(null)

// Chart instances
let cuisineChartInstance = null
let difficultyChartInstance = null
let flavorChartInstance = null
let ingredientChartInstance = null

// State
const loading = ref(true)
const error = ref(null)

// Color palette - warm amber tones
const colors = {
  primary: ['#d4773a', '#c2622e', '#a35220', '#e8a87c', '#c9976b', '#8b5a2b', '#f4c89a', '#d4a574'],
  difficulty: ['#4caf50', '#ff9800', '#f44336'],
  flavors: ['#d4773a', '#e8a87c', '#c2622e', '#f4c89a', '#a35220', '#c9976b', '#8b5a2b', '#d4a574']
}

/**
 * Fetch all analytics data
 */
async function fetchData() {
  loading.value = true
  error.value = null

  try {
    const [cuisines, difficulty, flavors, ingredients] = await Promise.all([
      getCuisinesAnalytics(),
      getDifficultyAnalytics(),
      getFlavorsAnalytics(),
      getIngredientsAnalytics({ limit: 15 })
    ])

    // Set loading to false first so DOM elements are rendered
    loading.value = false

    // Wait for DOM to be ready then render charts
    await nextTick()

    renderCuisineChart(cuisines?.data || [])
    renderDifficultyChart(difficulty?.data || [])
    renderFlavorChart(flavors?.data || [])
    renderIngredientChart(ingredients?.data || [])
  } catch (err) {
    error.value = err.message || '数据加载失败，请稍后重试'
    loading.value = false
  }
}

/**
 * Render cuisine distribution pie chart
 */
function renderCuisineChart(data) {
  if (!cuisineChart.value || !data || data.length === 0) return

  if (cuisineChartInstance) {
    cuisineChartInstance.dispose()
  }

  cuisineChartInstance = echarts.init(cuisineChart.value)

  const option = {
    color: colors.primary,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: {
        color: '#3d2914',
        fontFamily: 'DM Sans'
      }
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 20,
      bottom: 20,
      textStyle: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 12
      },
      pageIconColor: '#c2622e',
      pageTextStyle: {
        color: '#c2622e'
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 600,
            color: '#3d2914',
            fontFamily: 'DM Sans'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(194, 98, 46, 0.3)'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map(item => ({
          name: item.name,
          value: item.count
        }))
      }
    ]
  }

  cuisineChartInstance.setOption(option)
}

/**
 * Render difficulty level bar chart
 */
function renderDifficultyChart(data) {
  if (!difficultyChart.value || !data || data.length === 0) return

  if (difficultyChartInstance) {
    difficultyChartInstance.dispose()
  }

  difficultyChartInstance = echarts.init(difficultyChart.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: {
        color: '#3d2914',
        fontFamily: 'DM Sans'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLine: {
        lineStyle: {
          color: '#e5ddd3'
        }
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      splitLine: {
        lineStyle: {
          color: '#f0ebe3',
          type: 'dashed'
        }
      },
      axisLabel: {
        color: '#8b7355',
        fontFamily: 'DM Sans',
        fontSize: 11
      }
    },
    series: [
      {
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.count,
          itemStyle: {
            color: colors.difficulty[index],
            borderRadius: [6, 6, 0, 0]
          }
        })),
        barWidth: '50%',
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(194, 98, 46, 0.3)'
          }
        }
      }
    ]
  }

  difficultyChartInstance.setOption(option)
}

/**
 * Render flavor preference radar chart
 */
function renderFlavorChart(data) {
  if (!flavorChart.value || !data || data.length === 0) return

  if (flavorChartInstance) {
    flavorChartInstance.dispose()
  }

  flavorChartInstance = echarts.init(flavorChart.value)

  // Take top 6 flavors for better radar visualization
  const topFlavors = data.slice(0, 6)
  const maxValue = Math.max(...topFlavors.map(f => f.count))

  const option = {
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: {
        color: '#3d2914',
        fontFamily: 'DM Sans'
      }
    },
    radar: {
      indicator: topFlavors.map(item => ({
        name: item.name,
        max: maxValue * 1.2
      })),
      shape: 'circle',
      splitNumber: 4,
      axisName: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 11
      },
      splitLine: {
        lineStyle: {
          color: '#e5ddd3'
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(194, 98, 46, 0.05)', 'rgba(194, 98, 46, 0.02)']
        }
      },
      axisLine: {
        lineStyle: {
          color: '#e5ddd3'
        }
      }
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: topFlavors.map(item => item.count),
            name: '口味分布',
            areaStyle: {
              color: 'rgba(194, 98, 46, 0.2)'
            },
            lineStyle: {
              color: '#c2622e',
              width: 2
            },
            itemStyle: {
              color: '#c2622e'
            },
            emphasis: {
              lineStyle: {
                width: 3
              },
              areaStyle: {
                color: 'rgba(194, 98, 46, 0.3)'
              }
            }
          }
        ]
      }
    ]
  }

  flavorChartInstance.setOption(option)
}

/**
 * Render top ingredients horizontal bar chart
 */
function renderIngredientChart(data) {
  if (!ingredientChart.value || !data || data.length === 0) return

  if (ingredientChartInstance) {
    ingredientChartInstance.dispose()
  }

  ingredientChartInstance = echarts.init(ingredientChart.value)

  const option = {
    color: colors.primary,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: {
        color: '#3d2914',
        fontFamily: 'DM Sans'
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
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      splitLine: {
        lineStyle: {
          color: '#f0ebe3',
          type: 'dashed'
        }
      },
      axisLabel: {
        color: '#8b7355',
        fontFamily: 'DM Sans',
        fontSize: 10
      }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.name).reverse(),
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 11
      }
    },
    series: [
      {
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.count,
          itemStyle: {
            color: colors.primary[index % colors.primary.length],
            borderRadius: [0, 6, 6, 0]
          }
        })).reverse(),
        barWidth: '60%',
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(194, 98, 46, 0.3)'
          }
        }
      }
    ]
  }

  ingredientChartInstance.setOption(option)
}

/**
 * Handle window resize
 */
function handleResize() {
  cuisineChartInstance?.resize()
  difficultyChartInstance?.resize()
  flavorChartInstance?.resize()
  ingredientChartInstance?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  cuisineChartInstance?.dispose()
  difficultyChartInstance?.dispose()
  flavorChartInstance?.dispose()
  ingredientChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* Google Fonts Import */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

/* CSS Variables */
.analytics-page {
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
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;

  min-height: 100vh;
  background: var(--gradient-bg);
  padding: var(--space-6);
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: var(--space-10);
  animation: fadeInUp 0.6s ease-out;
}

.page-title {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-4) 0;
  line-height: 1.2;
}

.page-subtitle {
  font-family: var(--font-body);
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin: 0;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  margin-top: var(--space-6);
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
  margin-bottom: var(--space-6);
}

.error-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-4) 0;
}

.error-message {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  margin: 0 0 var(--space-8) 0;
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

.retry-button:active {
  transform: translateY(0);
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-8);
  max-width: 1400px;
  margin: 0 auto;
}

/* Chart Card */
.chart-card {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-2xl);
  padding: var(--space-10);
  box-shadow: var(--shadow-card);
  animation: fadeInUp 0.6s ease-out both;
}

.chart-header {
  margin-bottom: var(--space-8);
}

.chart-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 0.25rem 0;
}

.chart-subtitle {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--color-text-tertiary);
}

.chart-container {
  width: 100%;
  height: 320px;
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
  .charts-grid {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }

  .chart-card {
    padding: var(--space-8);
  }

  .chart-container {
    height: 280px;
  }
}

@media (max-width: 768px) {
  .analytics-page {
    padding: var(--space-4);
  }

  .page-title {
    font-size: 1.75rem;
  }

  .page-subtitle {
    font-size: 0.9rem;
  }

  .chart-card {
    padding: var(--space-6);
  }

  .chart-container {
    height: 260px;
  }

  .chart-title {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .charts-grid {
    gap: var(--space-4);
  }

  .chart-card {
    border-radius: var(--radius-lg);
    padding: var(--space-4);
  }

  .chart-container {
    height: 220px;
  }
}
</style>
