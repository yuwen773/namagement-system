<template>
  <div class="admin-analytics-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">数据分析中心</h1>
          <p class="page-subtitle">深度洞察菜谱数据，助力精准决策</p>
        </div>
        <div class="header-actions">
          <button @click="exportData" class="export-btn" :disabled="loading || !currentTabData">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            导出数据
          </button>
        </div>
      </div>
    </div>

    <!-- Analysis Tabs -->
    <div class="tabs-container">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="switchTab(tab.key)"
        class="tab-btn"
        :class="{ active: currentTab === tab.key }"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </button>
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

    <!-- Content Area -->
    <div v-else class="content-area">
      <!-- Cuisine Analysis -->
      <div v-if="currentTab === 'cuisine'" class="analysis-content">
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总菜谱数</span>
            <span class="card-value">{{ formatNumber(cuisineData?.summary?.total_recipes) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">菜系类型</span>
            <span class="card-value">{{ cuisineData?.summary?.total_cuisines || 0 }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均点击量</span>
            <span class="card-value">{{ formatNumber(getAvgCuisineMetric('avg_view_count')) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均收藏量</span>
            <span class="card-value">{{ formatNumber(getAvgCuisineMetric('avg_favorite_count')) }}</span>
          </div>
        </div>
        <div class="chart-section">
          <div ref="cuisineChart" class="chart-container"></div>
        </div>
        <div class="table-section">
          <h3 class="section-title">菜系详细数据</h3>
          <el-table :data="cuisineData?.cuisines || []" stripe style="width: 100%">
            <el-table-column prop="name" label="菜系" width="120" />
            <el-table-column prop="count" label="菜谱数量" sortable width="120">
              <template #default="{ row }">{{ formatNumber(row.count) }}</template>
            </el-table-column>
            <el-table-column prop="percentage" label="占比" width="100">
              <template #default="{ row }">{{ row.percentage.toFixed(2) }}%</template>
            </el-table-column>
            <el-table-column prop="avg_view_count" label="平均点击量" sortable width="130">
              <template #default="{ row }">{{ formatNumber(row.avg_view_count) }}</template>
            </el-table-column>
            <el-table-column prop="avg_favorite_count" label="平均收藏量" sortable width="130">
              <template #default="{ row }">{{ formatNumber(row.avg_favorite_count) }}</template>
            </el-table-column>
            <el-table-column prop="avg_cooking_time" label="平均时长(分钟)" sortable width="150">
              <template #default="{ row }">{{ row.avg_cooking_time.toFixed(1) }}</template>
            </el-table-column>
            <el-table-column label="难度分布" min-width="200">
              <template #default="{ row }">
                <span class="difficulty-badge easy">简单: {{ row.difficulty_distribution.easy }}</span>
                <span class="difficulty-badge medium">中等: {{ row.difficulty_distribution.medium }}</span>
                <span class="difficulty-badge hard">困难: {{ row.difficulty_distribution.hard }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Difficulty Analysis -->
      <div v-else-if="currentTab === 'difficulty'" class="analysis-content">
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总菜谱数</span>
            <span class="card-value">{{ formatNumber(difficultyData?.summary?.total_recipes) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">难度等级</span>
            <span class="card-value">{{ difficultyData?.summary?.total_difficulty_levels || 0 }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均烹饪时长</span>
            <span class="card-value">{{ getAvgCookingTime() }} 分钟</span>
          </div>
        </div>
        <div class="chart-section">
          <div ref="difficultyChart" class="chart-container"></div>
        </div>
        <div class="table-section">
          <h3 class="section-title">难度等级详细数据</h3>
          <el-table :data="difficultyData?.difficulties || []" stripe style="width: 100%">
            <el-table-column prop="name" label="难度等级" width="120" />
            <el-table-column prop="value" label="代码值" width="100" />
            <el-table-column prop="count" label="菜谱数量" sortable width="120">
              <template #default="{ row }">{{ formatNumber(row.count) }}</template>
            </el-table-column>
            <el-table-column prop="percentage" label="占比" width="100">
              <template #default="{ row }">{{ row.percentage.toFixed(2) }}%</template>
            </el-table-column>
            <el-table-column prop="avg_cooking_time" label="平均烹饪时长(分钟)" sortable width="160">
              <template #default="{ row }">{{ row.avg_cooking_time.toFixed(1) }}</template>
            </el-table-column>
            <el-table-column prop="avg_view_count" label="平均点击量" sortable width="130">
              <template #default="{ row }">{{ formatNumber(row.avg_view_count) }}</template>
            </el-table-column>
            <el-table-column prop="avg_favorite_count" label="平均收藏量" sortable width="130">
              <template #default="{ row }">{{ formatNumber(row.avg_favorite_count) }}</template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Hot Recipes Analysis -->
      <div v-else-if="currentTab === 'hot'" class="analysis-content">
        <div class="controls-section">
          <el-select v-model="hotParams.sort_by" @change="fetchHotData" class="control-select">
            <el-option label="按点击量" value="view_count" />
            <el-option label="按收藏量" value="favorite_count" />
          </el-select>
          <el-select v-model="hotParams.limit" @change="fetchHotData" class="control-select">
            <el-option label="Top 20" :value="20" />
            <el-option label="Top 50" :value="50" />
            <el-option label="Top 100" :value="100" />
          </el-select>
        </div>
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总菜谱数</span>
            <span class="card-value">{{ formatNumber(hotData?.summary?.total_recipes) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">排序方式</span>
            <span class="card-value">{{ hotData?.summary?.sort_by_label || '-' }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均点击量</span>
            <span class="card-value">{{ formatNumber(hotData?.trends?.avg_view_count) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均收藏量</span>
            <span class="card-value">{{ formatNumber(hotData?.trends?.avg_favorite_count) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">平均转化率</span>
            <span class="card-value">{{ hotData?.trends?.avg_conversion_rate?.toFixed(2) || 0 }}%</span>
          </div>
        </div>
        <div class="chart-section">
          <div ref="hotChart" class="chart-container"></div>
        </div>
        <div class="table-section">
          <h3 class="section-title">热门菜谱列表</h3>
          <el-table :data="hotData?.recipes || []" stripe style="width: 100%" max-height="400">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="菜谱名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="cuisine_type" label="菜系" width="100" />
            <el-table-column label="难度" width="100">
              <template #default="{ row }">
                <span :class="['difficulty-tag', row.difficulty]">
                  {{ getDifficultyLabel(row.difficulty) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="view_count" label="点击量" sortable width="110">
              <template #default="{ row }">{{ formatNumber(row.view_count) }}</template>
            </el-table-column>
            <el-table-column prop="favorite_count" label="收藏量" sortable width="110">
              <template #default="{ row }">{{ formatNumber(row.favorite_count) }}</template>
            </el-table-column>
            <el-table-column prop="conversion_rate" label="转化率" sortable width="100">
              <template #default="{ row }">{{ row.conversion_rate.toFixed(2) }}%</template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Ingredient Pairs Analysis -->
      <div v-else-if="currentTab === 'pairs'" class="analysis-content">
        <div class="controls-section">
          <el-select v-model="pairsParams.category" @change="fetchPairsData" placeholder="选择食材分类" clearable class="control-select">
            <el-option label="全部" value="" />
            <el-option label="蔬菜" value="vegetable" />
            <el-option label="肉类" value="meat" />
            <el-option label="海鲜" value="seafood" />
            <el-option label="调料" value="seasoning" />
            <el-option label="水果" value="fruit" />
            <el-option label="谷物" value="grain" />
            <el-option label="乳制品" value="dairy" />
            <el-option label="其他" value="other" />
          </el-select>
          <el-select v-model="pairsParams.limit" @change="fetchPairsData" class="control-select">
            <el-option label="Top 20" :value="20" />
            <el-option label="Top 50" :value="50" />
            <el-option label="Top 100" :value="100" />
          </el-select>
        </div>
        <div class="summary-cards">
          <div class="summary-card">
            <span class="card-label">总菜谱数</span>
            <span class="card-value">{{ formatNumber(pairsData?.summary?.total_recipes) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">食材配对数</span>
            <span class="card-value">{{ formatNumber(pairsData?.summary?.total_pairs) }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">最小共现次数</span>
            <span class="card-value">{{ pairsData?.summary?.min_count || 0 }}</span>
          </div>
          <div class="summary-card">
            <span class="card-label">分类筛选</span>
            <span class="card-value">{{ pairsData?.summary?.category_filter || '全部' }}</span>
          </div>
        </div>
        <div class="chart-section">
          <div ref="pairsChart" class="chart-container"></div>
        </div>
        <div class="table-section">
          <h3 class="section-title">食材搭配组合</h3>
          <el-table :data="pairsData?.pairs || []" stripe style="width: 100%" max-height="400">
            <el-table-column label="食材1" min-width="150">
              <template #default="{ row }">
                <span :class="['ingredient-tag', row.ingredient_1.category]">{{ row.ingredient_1.name }}</span>
              </template>
            </el-table-column>
            <el-table-column label="食材2" min-width="150">
              <template #default="{ row }">
                <span :class="['ingredient-tag', row.ingredient_2.category]">{{ row.ingredient_2.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="共现次数" sortable width="130">
              <template #default="{ row }">{{ formatNumber(row.count) }}</template>
            </el-table-column>
            <el-table-column prop="percentage" label="占比" width="100">
              <template #default="{ row }">{{ row.percentage.toFixed(2) }}%</template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  getAdminCuisinesAnalytics,
  getAdminDifficultyAnalytics,
  getAdminHotRecipesAnalytics,
  getAdminIngredientPairsAnalytics
} from '../api/analytics'

// State
const currentTab = ref('cuisine')
const loading = ref(true)
const error = ref(null)
const cuisineData = ref(null)
const difficultyData = ref(null)
const hotData = ref(null)
const pairsData = ref(null)

// Chart refs
const cuisineChart = ref(null)
const difficultyChart = ref(null)
const hotChart = ref(null)
const pairsChart = ref(null)

// Chart instances
let cuisineChartInstance = null
let difficultyChartInstance = null
let hotChartInstance = null
let pairsChartInstance = null

// Tabs
const tabs = [
  { key: 'cuisine', label: '菜系分析', icon: '🍽️' },
  { key: 'difficulty', label: '难度分析', icon: '📊' },
  { key: 'hot', label: '热门菜谱', icon: '🔥' },
  { key: 'pairs', label: '食材关联', icon: '🔗' }
]

// Hot params
const hotParams = ref({
  sort_by: 'view_count',
  limit: 50
})

// Pairs params
const pairsParams = ref({
  category: '',
  limit: 50
})

// Current tab data for export
const currentTabData = computed(() => {
  switch (currentTab.value) {
    case 'cuisine': return cuisineData.value
    case 'difficulty': return difficultyData.value
    case 'hot': return hotData.value
    case 'pairs': return pairsData.value
    default: return null
  }
})

// Difficulty label map
const difficultyLabelMap = {
  easy: '简单',
  medium: '中等',
  hard: '困难'
}

/**
 * Get difficulty label
 */
function getDifficultyLabel(value) {
  return difficultyLabelMap[value] || value
}

/**
 * Get average cuisine metric
 */
function getAvgCuisineMetric(key) {
  if (!cuisineData.value?.cuisines?.length) return 0
  const sum = cuisineData.value.cuisines.reduce((acc, item) => acc + (item[key] || 0), 0)
  return sum / cuisineData.value.cuisines.length
}

/**
 * Get average cooking time across difficulties
 */
function getAvgCookingTime() {
  if (!difficultyData.value?.difficulties?.length) return 0
  const sum = difficultyData.value.difficulties.reduce((acc, item) => acc + (item.avg_cooking_time || 0), 0)
  return (sum / difficultyData.value.difficulties).toFixed(1)
}

/**
 * Format number with commas
 */
function formatNumber(num) {
  if (num === null || num === undefined) return '-'
  return Number(num).toLocaleString('zh-CN')
}

/**
 * Switch tab
 */
function switchTab(tab) {
  currentTab.value = tab
  if (!currentTabData.value) {
    fetchData()
  } else {
    nextTick(() => renderCurrentChart())
  }
}

/**
 * Render current chart
 */
function renderCurrentChart() {
  switch (currentTab.value) {
    case 'cuisine': renderCuisineChart(); break
    case 'difficulty': renderDifficultyChart(); break
    case 'hot': renderHotChart(); break
    case 'pairs': renderPairsChart(); break
  }
}

/**
 * Fetch all data
 */
async function fetchData() {
  loading.value = true
  error.value = null

  try {
    await Promise.all([
      fetchCuisineData(),
      fetchDifficultyData(),
      fetchHotData(),
      fetchPairsData()
    ])

    loading.value = false
    await nextTick()
    renderCurrentChart()
  } catch (err) {
    error.value = err.message || '数据加载失败，请稍后重试'
    loading.value = false
  }
}

/**
 * Fetch cuisine data
 */
async function fetchCuisineData() {
  const response = await getAdminCuisinesAnalytics()
  cuisineData.value = response?.data || null
}

/**
 * Fetch difficulty data
 */
async function fetchDifficultyData() {
  const response = await getAdminDifficultyAnalytics()
  difficultyData.value = response?.data || null
}

/**
 * Fetch hot data
 */
async function fetchHotData() {
  const response = await getAdminHotRecipesAnalytics(hotParams.value)
  hotData.value = response?.data || null
  if (currentTab.value === 'hot') {
    await nextTick()
    renderHotChart()
  }
}

/**
 * Fetch pairs data
 */
async function fetchPairsData() {
  const response = await getAdminIngredientPairsAnalytics(
    Object.fromEntries(Object.entries(pairsParams.value).filter(([_, v]) => v !== ''))
  )
  pairsData.value = response?.data || null
  if (currentTab.value === 'pairs') {
    await nextTick()
    renderPairsChart()
  }
}

/**
 * Render cuisine chart
 */
function renderCuisineChart() {
  if (!cuisineChart.value || !cuisineData.value?.cuisines?.length) return

  if (cuisineChartInstance) {
    cuisineChartInstance.dispose()
  }

  cuisineChartInstance = echarts.init(cuisineChart.value)
  const data = cuisineData.value.cuisines

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' }
    },
    legend: {
      data: ['菜谱数量', '平均点击量', '平均收藏量'],
      bottom: 10,
      textStyle: { color: '#6b5c4d', fontFamily: 'DM Sans' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLine: { lineStyle: { color: '#e5ddd3' } },
      axisTick: { show: false },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 11,
        rotate: 30
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '数量',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } },
        axisLabel: { color: '#8b7355', fontFamily: 'DM Sans' }
      },
      {
        type: 'value',
        name: '点击/收藏量',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#8b7355', fontFamily: 'DM Sans' }
      }
    ],
    series: [
      {
        name: '菜谱数量',
        type: 'bar',
        yAxisIndex: 0,
        data: data.map(item => ({
          value: item.count,
          itemStyle: {
            color: '#c2622e',
            borderRadius: [6, 6, 0, 0]
          }
        })),
        barWidth: '40%'
      },
      {
        name: '平均点击量',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.avg_view_count),
        smooth: true,
        itemStyle: { color: '#d4773a' },
        lineStyle: { width: 2 }
      },
      {
        name: '平均收藏量',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.avg_favorite_count),
        smooth: true,
        itemStyle: { color: '#a35220' },
        lineStyle: { width: 2 }
      }
    ]
  }

  cuisineChartInstance.setOption(option)
}

/**
 * Render difficulty chart
 */
function renderDifficultyChart() {
  if (!difficultyChart.value || !difficultyData.value?.difficulties?.length) return

  if (difficultyChartInstance) {
    difficultyChartInstance.dispose()
  }

  difficultyChartInstance = echarts.init(difficultyChart.value)
  const data = difficultyData.value.difficulties

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' }
    },
    legend: {
      data: ['菜谱数量', '平均烹饪时长'],
      bottom: 10,
      textStyle: { color: '#6b5c4d', fontFamily: 'DM Sans' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLine: { lineStyle: { color: '#e5ddd3' } },
      axisTick: { show: false },
      axisLabel: { color: '#6b5c4d', fontFamily: 'DM Sans', fontSize: 12 }
    },
    yAxis: [
      {
        type: 'value',
        name: '菜谱数量',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } },
        axisLabel: { color: '#8b7355', fontFamily: 'DM Sans' }
      },
      {
        type: 'value',
        name: '烹饪时长(分钟)',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#8b7355', fontFamily: 'DM Sans' }
      }
    ],
    series: [
      {
        name: '菜谱数量',
        type: 'bar',
        yAxisIndex: 0,
        data: data.map((item, index) => ({
          value: item.count,
          itemStyle: {
            color: ['#4caf50', '#ff9800', '#f44336'][index],
            borderRadius: [6, 6, 0, 0]
          }
        })),
        barWidth: '40%'
      },
      {
        name: '平均烹饪时长',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.avg_cooking_time),
        smooth: true,
        itemStyle: { color: '#c2622e' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(194, 98, 46, 0.3)' },
              { offset: 1, color: 'rgba(194, 98, 46, 0.05)' }
            ]
          }
        }
      }
    ]
  }

  difficultyChartInstance.setOption(option)
}

/**
 * Render hot chart
 */
function renderHotChart() {
  if (!hotChart.value || !hotData.value?.recipes?.length) return

  if (hotChartInstance) {
    hotChartInstance.dispose()
  }

  hotChartInstance = echarts.init(hotChart.value)
  const recipes = hotData.value.recipes.slice(0, 20)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' },
      formatter: (params) => {
        const recipe = recipes[params[0].dataIndex]
        return `
          <strong>${recipe.name}</strong><br/>
          点击量: ${formatNumber(recipe.view_count)}<br/>
          收藏量: ${formatNumber(recipe.favorite_count)}<br/>
          转化率: ${recipe.conversion_rate.toFixed(2)}%
        `
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
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } },
      axisLabel: { color: '#8b7355', fontFamily: 'DM Sans', fontSize: 10 }
    },
    yAxis: {
      type: 'category',
      data: recipes.map(item => item.name).reverse(),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 11,
        width: 150,
        overflow: 'truncate'
      }
    },
    series: [
      {
        type: 'bar',
        data: recipes.map((item, index) => ({
          value: hotParams.value.sort_by === 'view_count' ? item.view_count : item.favorite_count,
          itemStyle: {
            color: index < 3 ? '#ff6b35' : '#c2622e',
            borderRadius: [0, 6, 6, 0]
          }
        })).reverse(),
        barWidth: '60%',
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(194, 98, 46, 0.4)'
          }
        }
      }
    ]
  }

  hotChartInstance.setOption(option)
}

/**
 * Render pairs chart
 */
function renderPairsChart() {
  if (!pairsChart.value || !pairsData.value?.pairs?.length) return

  if (pairsChartInstance) {
    pairsChartInstance.dispose()
  }

  pairsChartInstance = echarts.init(pairsChart.value)
  const pairs = pairsData.value.pairs.slice(0, 20)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5ddd3',
      borderWidth: 1,
      textStyle: { color: '#3d2914', fontFamily: 'DM Sans' },
      formatter: (params) => {
        const pair = pairs[params[0].dataIndex]
        return `
          <strong>${pair.ingredient_1.name} + ${pair.ingredient_2.name}</strong><br/>
          共现次数: ${formatNumber(pair.count)}<br/>
          占比: ${pair.percentage.toFixed(2)}%
        `
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
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f0ebe3', type: 'dashed' } },
      axisLabel: { color: '#8b7355', fontFamily: 'DM Sans', fontSize: 10 }
    },
    yAxis: {
      type: 'category',
      data: pairs.map(item => `${item.ingredient_1.name} + ${item.ingredient_2.name}`).reverse(),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#6b5c4d',
        fontFamily: 'DM Sans',
        fontSize: 10,
        width: 180,
        overflow: 'truncate'
      }
    },
    series: [
      {
        type: 'bar',
        data: pairs.map((item, index) => ({
          value: item.count,
          itemStyle: {
            color: ['#c2622e', '#d4773a', '#a35220', '#e8a87c', '#c9976b'][index % 5],
            borderRadius: [0, 6, 6, 0]
          }
        })).reverse(),
        barWidth: '60%',
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(194, 98, 46, 0.4)'
          }
        }
      }
    ]
  }

  pairsChartInstance.setOption(option)
}

/**
 * Export data as JSON
 */
function exportData() {
  const data = currentTabData.value
  if (!data) return

  const tabNames = {
    cuisine: '菜系分析',
    difficulty: '难度分析',
    hot: '热门菜谱',
    pairs: '食材关联'
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `admin-analytics-${currentTab.value}-${new Date().toISOString().slice(0, 10)}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)

  ElMessage.success(`${tabNames[currentTab.value]}数据已导出`)
}

/**
 * Handle window resize
 */
function handleResize() {
  cuisineChartInstance?.resize()
  difficultyChartInstance?.resize()
  hotChartInstance?.resize()
  pairsChartInstance?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  cuisineChartInstance?.dispose()
  difficultyChartInstance?.dispose()
  hotChartInstance?.dispose()
  pairsChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* Base Styles */
.admin-analytics-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
  padding: 2rem;
  font-family: 'DM Sans', 'Noto Sans SC', sans-serif;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
}

.header-left {
  text-align: left;
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  font-size: 1rem;
  color: #8b7355;
  margin: 0;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

.export-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.export-btn svg {
  width: 18px;
  height: 18px;
}

/* Tabs Container */
.tabs-container {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  max-width: 1600px;
  margin-left: auto;
  margin-right: auto;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.5rem;
  background: white;
  border: 2px solid #e5ddd3;
  border-radius: 14px;
  font-size: 0.95rem;
  font-weight: 500;
  color: #6b5c4d;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  border-color: #c2622e;
  color: #c2622e;
}

.tab-btn.active {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 4px 16px rgba(194, 98, 46, 0.3);
}

.tab-icon {
  font-size: 1.1rem;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e5ddd3;
  border-top-color: #c2622e;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #8b7355;
  margin-top: 1rem;
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.error-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  font-size: 2rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.error-message {
  color: #8b7355;
  margin: 0 0 1.5rem 0;
}

.retry-button {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

/* Content Area */
.content-area {
  max-width: 1600px;
  margin: 0 auto;
}

/* Summary Cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-label {
  font-size: 0.85rem;
  color: #8b7355;
}

.card-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #c2622e;
}

/* Controls Section */
.controls-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.control-select {
  min-width: 150px;
}

/* Chart Section */
.chart-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
  margin-bottom: 2rem;
}

.chart-container {
  width: 100%;
  height: 400px;
}

/* Table Section */
.table-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08);
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 1.5rem 0;
}

/* Badges */
.difficulty-badge {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  margin-right: 0.5rem;
}

.difficulty-badge.easy {
  background: #e8f5e9;
  color: #2e7d32;
}

.difficulty-badge.medium {
  background: #fff3e0;
  color: #e65100;
}

.difficulty-badge.hard {
  background: #ffebee;
  color: #c62828;
}

.difficulty-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 500;
}

.difficulty-tag.easy {
  background: #e8f5e9;
  color: #2e7d32;
}

.difficulty-tag.medium {
  background: #fff3e0;
  color: #e65100;
}

.difficulty-tag.hard {
  background: #ffebee;
  color: #c62828;
}

.ingredient-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
}

.ingredient-tag.vegetable { background: #e8f5e9; color: #2e7d32; }
.ingredient-tag.meat { background: #ffebee; color: #c62828; }
.ingredient-tag.seafood { background: #e3f2fd; color: #1565c0; }
.ingredient-tag.seasoning { background: #fff3e0; color: #e65100; }
.ingredient-tag.fruit { background: #fce4ec; color: #c2185b; }
.ingredient-tag.grain { background: #fff8e1; color: #f57f17; }
.ingredient-tag.dairy { background: #f3e5f5; color: #6a1b9a; }
.ingredient-tag.other { background: #f5f5f5; color: #616161; }

/* Responsive */
@media (max-width: 1024px) {
  .admin-analytics-page {
    padding: 1rem;
  }

  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-container {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 250px;
  }
}
</style>
