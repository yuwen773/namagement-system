<template>
  <div class="analysis-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回概览
        </el-button>
        <div class="header-info">
          <h1 class="page-title">数据分析</h1>
          <p class="page-subtitle">城市对比、相关性分析与数据可视化</p>
        </div>
      </div>
    </div>

    <!-- Analysis Tabs -->
    <el-tabs v-model="activeTab" class="analysis-tabs">
      <!-- City Comparison Tab -->
      <el-tab-pane label="城市对比" name="compare">
        <div class="tab-content">
          <!-- City Selector -->
          <div class="card selector-card">
            <div class="selector-form">
              <div class="form-row">
                <div class="form-item">
                  <label class="form-label">选择城市 (最多10个)</label>
                  <el-select
                    v-model="selectedCities"
                    multiple
                    filterable
                    placeholder="选择要对比的城市"
                    style="width: 100%"
                    @change="handleCityChange"
                  >
                    <el-option
                      v-for="city in availableCities"
                      :key="city.code"
                      :label="city.name"
                      :value="city.code"
                    />
                  </el-select>
                </div>
                <div class="form-item form-item-actions">
                  <el-button
                    type="primary"
                    @click="handleCompare"
                    :disabled="selectedCities.length < 2 || loading"
                    :loading="loading"
                  >
                    开始对比
                  </el-button>
                  <el-button
                    @click="handleReset"
                    :disabled="loading"
                  >
                    重置
                  </el-button>
                </div>
              </div>

              <!-- Selected cities tags -->
              <div v-if="selectedCities.length > 0" class="selected-tags">
                <el-tag
                  v-for="code in selectedCities"
                  :key="code"
                  closable
                  @close="removeCity(code)"
                >
                  {{ getCityName(code) }}
                </el-tag>
              </div>
            </div>
          </div>

          <!-- Comparison Chart -->
          <div v-if="comparisonData" class="card chart-card">
            <div class="chart-header">
              <h3 class="chart-title">城市AQI趋势对比</h3>
              <div class="chart-legend">
                <span
                  v-for="city in comparisonData.series"
                  :key="city.city_code"
                  class="legend-item"
                >
                  <span class="legend-color" :style="{ background: city.color || '#06B6D4' }"></span>
                  <span class="legend-label">{{ city.city_name }}</span>
                </span>
              </div>
            </div>
            <div class="chart-container">
              <LineChart
                :data="comparisonData.series"
                :x-axis="comparisonData.xAxis"
                :smooth="true"
                :area-style="false"
                :show-data-zoom="true"
                height="400px"
              />
            </div>
          </div>

          <el-empty v-else description="请选择至少2个城市进行对比分析" :image-size="100" />
        </div>
      </el-tab-pane>

      <!-- Correlation Analysis Tab -->
      <el-tab-pane label="相关性分析" name="correlation">
        <div class="tab-content">
          <!-- Correlation Controls -->
          <div class="card selector-card">
            <div class="selector-form">
              <div class="form-row">
                <div class="form-item">
                  <label class="form-label">X轴污染物</label>
                  <el-select v-model="correlationForm.pollutantX" style="width: 100%">
                    <el-option label="PM2.5" value="pm25" />
                    <el-option label="PM10" value="pm10" />
                    <el-option label="SO₂" value="so2" />
                    <el-option label="NO₂" value="no2" />
                    <el-option label="CO" value="co" />
                    <el-option label="O₃" value="o3" />
                  </el-select>
                </div>
                <div class="form-item">
                  <label class="form-label">Y轴污染物</label>
                  <el-select v-model="correlationForm.pollutantY" style="width: 100%">
                    <el-option label="PM2.5" value="pm25" />
                    <el-option label="PM10" value="pm10" />
                    <el-option label="SO₂" value="so2" />
                    <el-option label="NO₂" value="no2" />
                    <el-option label="CO" value="co" />
                    <el-option label="O₃" value="o3" />
                  </el-select>
                </div>
                <div class="form-item">
                  <label class="form-label">数据点数量</label>
                  <el-select v-model="correlationForm.maxPoints" style="width: 100%">
                    <el-option label="500" :value="500" />
                    <el-option label="1000" :value="1000" />
                    <el-option label="2000" :value="2000" />
                    <el-option label="5000" :value="5000" />
                  </el-select>
                </div>
                <div class="form-item form-item-actions">
                  <el-button
                    type="primary"
                    @click="handleCorrelation"
                    :loading="loading"
                  >
                    分析相关性
                  </el-button>
                  <el-button
                    @click="handleCorrelationReset"
                    :disabled="loading"
                  >
                    重置
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- Correlation Results -->
          <div v-if="correlationData" class="correlation-results">
            <div class="results-grid">
              <!-- Scatter Chart -->
              <div class="card chart-card">
                <h3 class="chart-title">相关性散点图</h3>
                <div class="chart-container">
                  <ScatterChart
                    :data="correlationData.scatterData"
                    :x-axis-name="getPollutantLabel(correlationForm.pollutantX)"
                    :y-axis-name="getPollutantLabel(correlationForm.pollutantY)"
                    :show-regression="true"
                    :regression-data="correlationData.regressionData"
                    height="400px"
                  />
                </div>
              </div>

              <!-- Statistics -->
              <div class="stats-column">
                <div class="card stat-card">
                  <div class="stat-label">相关系数</div>
                  <div class="stat-value" :style="{ color: getCorrelationColor(correlationData.correlation) }">
                    {{ formatDecimal(correlationData.correlation, 4) }}
                  </div>
                  <div class="stat-desc">{{ getCorrelationLabel(correlationData.correlation) }}</div>
                </div>

                <div class="card stat-card">
                  <div class="stat-label">样本数量</div>
                  <div class="stat-value stat-primary">{{ correlationData.sampleCount || '--' }}</div>
                </div>

                <div class="card stat-card">
                  <div class="stat-label">回归方程</div>
                  <div class="stat-equation">
                    y = {{ formatDecimal(correlationData.slope, 4) }}x + {{ formatDecimal(correlationData.intercept, 4) }}
                  </div>
                </div>

                <!-- Correlation Guide -->
                <div class="card guide-card">
                  <h4 class="guide-title">相关系数解释</h4>
                  <div class="guide-list">
                    <div class="guide-item">
                      <span class="guide-range">0.9 - 1.0</span>
                      <span class="guide-label guide-strong">极强相关</span>
                    </div>
                    <div class="guide-item">
                      <span class="guide-range">0.7 - 0.9</span>
                      <span class="guide-label guide-good">强相关</span>
                    </div>
                    <div class="guide-item">
                      <span class="guide-range">0.4 - 0.7</span>
                      <span class="guide-label guide-medium">中等相关</span>
                    </div>
                    <div class="guide-item">
                      <span class="guide-range">0.2 - 0.4</span>
                      <span class="guide-label guide-weak">弱相关</span>
                    </div>
                    <div class="guide-item">
                      <span class="guide-range">0 - 0.2</span>
                      <span class="guide-label guide-poor">极弱相关</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- AQI Distribution Tab -->
      <el-tab-pane label=" AQI分布" name="distribution">
        <div class="tab-content">
          <!-- Distribution Controls -->
          <div class="card selector-card">
            <div class="selector-form">
              <div class="form-row">
                <div class="form-item">
                  <label class="form-label">城市</label>
                  <el-select
                    v-model="distributionForm.city"
                    filterable
                    clearable
                    placeholder="选择城市（可选）"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="city in availableCities"
                      :key="city.code"
                      :label="city.name"
                      :value="city.code"
                    />
                  </el-select>
                </div>
                <div class="form-item form-item-actions">
                  <el-button
                    type="primary"
                    @click="handleDistribution"
                    :loading="loading"
                  >
                    统计分布
                  </el-button>
                  <el-button @click="handleDistributionReset" :disabled="loading">
                    全国数据
                  </el-button>
                  <el-button @click="handleDistributionClear" :disabled="loading">
                    重置
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- Distribution Results -->
          <div v-if="distributionData && distributionData.distribution && distributionData.distribution.length > 0" class="distribution-results">
            <div class="results-grid">
              <!-- Pie Chart -->
              <div class="card chart-card">
                <h3 class="chart-title">空气质量等级分布</h3>
                <div class="chart-container">
                  <PieChart
                    :data="distributionData.distribution"
                    :donut="true"
                    :radius="['40%', '70%']"
                    :show-percentage="true"
                    height="350px"
                  />
                </div>
              </div>

              <!-- Statistics Table -->
              <div class="card table-card">
                <h3 class="chart-title">详细统计</h3>
                <div class="distribution-list">
                  <div
                    v-for="item in distributionData.distribution"
                    :key="item.qualityLevel"
                    class="distribution-item"
                  >
                    <div class="dist-info">
                      <span class="dist-dot" :style="{ background: getAQIColorByLevel(item.qualityLevel) }"></span>
                      <span class="dist-label">{{ item.qualityLabel }}</span>
                    </div>
                    <div class="dist-stats">
                      <div class="dist-value" :style="{ color: getAQIColorByLevel(item.qualityLevel) }">
                        {{ item.count }}
                      </div>
                      <div class="dist-percent">{{ item.percentage }}%</div>
                    </div>
                  </div>
                </div>
                <div class="dist-total">
                  <span>总样本数</span>
                  <span class="dist-total-value">{{ distributionData.total }}</span>
                </div>
              </div>
            </div>
          </div>

          <el-empty v-else description="暂无分布数据，请点击统计按钮获取数据" :image-size="100" />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { LineChart, ScatterChart, PieChart } from '@/components/charts'
import { compareCities, getCorrelationAnalysis, getAQIDistribution, getOverview } from '@/api/airquality'

const router = useRouter()

// State
const loading = ref(false)
const activeTab = ref('compare')

// City comparison
const selectedCities = ref([])
const comparisonData = ref(null)

// Correlation
const correlationForm = ref({
  pollutantX: 'pm25',
  pollutantY: 'pm10',
  maxPoints: 2000
})
const correlationData = ref(null)

// Distribution
const distributionForm = ref({
  city: ''
})
const distributionData = ref(null)

// Available cities - loaded from API
const availableCities = ref([])

// Fetch available cities from API
const fetchAvailableCities = async () => {
  try {
    const response = await getOverview()
    console.log('Overview response:', response)
    if (response.code === 0 && response.data.map_data) {
      availableCities.value = response.data.map_data.map(city => ({
        code: city.city_code,
        name: city.city_name
      }))
      console.log('Loaded cities:', availableCities.value)
    }
  } catch (error) {
    console.error('Failed to fetch cities:', error)
  }
}

// Colors for city comparison
const cityColors = [
  '#06B6D4', '#8B5CF6', '#EC4899', '#F97316', '#14B8A6',
  '#3B82F6', '#6366F1', '#A855F7', '#F43F5E', '#0EA5E9'
]

// Methods
const goBack = () => {
  router.back()
}

const getCityName = (code) => {
  const city = availableCities.value.find(c => c.code === code)
  return city ? city.name : code
}

const removeCity = (code) => {
  const index = selectedCities.value.indexOf(code)
  if (index > -1) {
    selectedCities.value.splice(index, 1)
  }
}

const handleCityChange = () => {
  // Remove duplicates and empty values
  const unique = [...new Set(selectedCities.value.filter(c => c && c.trim()))]
  selectedCities.value = unique

  if (selectedCities.value.length > 10) {
    selectedCities.value = selectedCities.value.slice(0, 10)
    ElMessage.warning('最多选择10个城市进行对比')
  }
}

const handleReset = () => {
  selectedCities.value = []
  comparisonData.value = null
  ElMessage.success('已重置')
}

const handleCompare = async () => {
  // Normalize and validate selected cities
  const normalizedCodes = selectedCities.value
    .map(code => String(code).trim())
    .filter(code => code.length > 0)

  // Remove duplicates
  const uniqueCodes = [...new Set(normalizedCodes)]

  if (uniqueCodes.length < 2) {
    ElMessage.warning('请至少选择2个城市进行对比')
    return
  }

  // Debug: log selected cities
  console.log('Selected cities:', selectedCities.value)
  console.log('Normalized codes:', normalizedCodes)
  console.log('Unique codes:', uniqueCodes)
  console.log('Available cities:', availableCities.value)

  loading.value = true

  try {
    const requestData = {
      city_codes: uniqueCodes,
      hours: 24
    }
    console.log('Request data:', requestData)

    const response = await compareCities(requestData)

    if (response.code === 0) {
      const data = response.data
      // hours is a number (like 24), convert to array for xAxis
      const hoursCount = data.hours || 0
      const xAxis = Array.from({ length: hoursCount }, (_, i) => hoursCount - 1 - i)

      // Find the maximum data length across all series
      const maxDataLength = Math.max(...data.series.map(s => s.trend.length))

      // Build xAxis from the first series with most data, or generate time labels
      let xAxisLabels
      let referenceSeries = data.series.find(s => s.trend.length === maxDataLength)

      if (referenceSeries && referenceSeries.trend.length > 0) {
        // Use actual time from the series with most data
        xAxisLabels = referenceSeries.trend.map(d => {
          const date = new Date(d.time)
          return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        })
      } else {
        // Fallback to generated time labels
        xAxisLabels = xAxis.map(h => {
          const date = new Date()
          date.setHours(date.getHours() - h)
          return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        })
      }

      comparisonData.value = {
        xAxis: xAxisLabels,
        series: data.series.map((series, index) => {
          const values = series.trend.map(d => d.aqi)
          console.log('Series ' + index + ' (' + series.city_name + '): ' + values.length + ' data points')

          // If this series has fewer data points, pad with null at the beginning
          let paddedValues = values
          if (values.length < maxDataLength) {
            const padding = Array(maxDataLength - values.length).fill(null)
            paddedValues = [...padding, ...values]
          }

          return {
            name: series.city_name,
            city_code: series.city_code,
            city_name: series.city_name,
            values: paddedValues,
            color: cityColors[index % cityColors.length]
          }
        })
      }

      console.log('Comparison data:', comparisonData.value)
    } else {
      ElMessage.error(response.message || '对比分析失败')
    }
  } catch (error) {
    console.error('Comparison failed:', error)
    ElMessage.error('对比分析失败')
  } finally {
    loading.value = false
  }
}

const getPollutantLabel = (key) => {
  const labels = {
    pm25: 'PM2.5 (μg/m³)',
    pm10: 'PM10 (μg/m³)',
    so2: 'SO₂ (μg/m³)',
    no2: 'NO₂ (μg/m³)',
    co: 'CO (mg/m³)',
    o3: 'O₃ (μg/m³)'
  }
  return labels[key] || key
}

const getCorrelationColor = (correlation) => {
  if (!correlation) return 'var(--text-secondary)'
  const abs = Math.abs(correlation)
  if (abs >= 0.9) return '#10B981'
  if (abs >= 0.7) return '#22C55E'
  if (abs >= 0.4) return '#EAB308'
  if (abs >= 0.2) return '#F97316'
  return '#EF4444'
}

const getCorrelationLabel = (correlation) => {
  if (!correlation) return '--'
  const abs = Math.abs(correlation)
  if (abs >= 0.9) return '极强相关'
  if (abs >= 0.7) return '强相关'
  if (abs >= 0.4) return '中等相关'
  if (abs >= 0.2) return '弱相关'
  return '极弱相关'
}

const formatDecimal = (value, decimals = 4) => {
  if (value === null || value === undefined || value === '') return '--'
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return '--'
  return num.toFixed(decimals)
}

const handleCorrelation = async () => {
  loading.value = true

  try {
    const response = await getCorrelationAnalysis({
      pollutant_x: correlationForm.value.pollutantX,
      pollutant_y: correlationForm.value.pollutantY,
      max_points: correlationForm.value.maxPoints
    })

    if (response.code === 0) {
      const data = response.data

      // Calculate regression line - handle both snake_case and camelCase
      const scatterData = data.scatter_data || data.scatterData || []
      const sampleCount = data.sample_count || data.sampleCount || 0
      const n = scatterData.length
      let slope = 0, intercept = 0

      if (n > 1) {
        const sumX = scatterData.reduce((sum, p) => sum + p.x, 0)
        const sumY = scatterData.reduce((sum, p) => sum + p.y, 0)
        const sumXY = scatterData.reduce((sum, p) => sum + p.x * p.y, 0)
        const sumXX = scatterData.reduce((sum, p) => sum + p.x * p.x, 0)

        const denominator = n * sumXX - sumX * sumX
        if (denominator !== 0) {
          slope = (n * sumXY - sumX * sumY) / denominator
          intercept = (sumY - slope * sumX) / n
        }
      }

      // Convert scatter data from {x, y} format to [x, y] format for ECharts
      const scatterDataArray = scatterData.map(p => [p.x, p.y])
      const regressionDataArray = scatterData.length > 0
        ? [
            [Math.min(...scatterData.map(p => p.x)), intercept + slope * Math.min(...scatterData.map(p => p.x))],
            [Math.max(...scatterData.map(p => p.x)), intercept + slope * Math.max(...scatterData.map(p => p.x))]
          ]
        : []

      correlationData.value = {
        scatterData: scatterDataArray,
        correlation: data.correlation,
        sampleCount: sampleCount,
        slope,
        intercept,
        regressionData: regressionDataArray
      }
    } else {
      ElMessage.error(response.message || '相关性分析失败')
    }
  } catch (error) {
    console.error('Correlation analysis failed:', error)
    ElMessage.error('相关性分析失败')
  } finally {
    loading.value = false
  }
}

const handleCorrelationReset = () => {
  correlationForm.value.pollutantX = 'pm25'
  correlationForm.value.pollutantY = 'pm10'
  correlationForm.value.maxPoints = 2000
  correlationData.value = null
  ElMessage.success('已重置')
}

const getAQIColorByLevel = (level) => {
  const colors = {
    EXCELLENT: '#10B981',
    Good: '#FBBF24',
    'Light pollution': '#F97316',
    'Moderate pollution': '#EF4444',
    'Heavy pollution': '#A855F7',
    'Severe pollution': '#7F1D1D'
  }
  return colors[level] || 'var(--text-secondary)'
}

const handleDistribution = async () => {
  loading.value = true

  try {
    const params = {}
    if (distributionForm.value.city) {
      params.city_code = distributionForm.value.city
    }

    const response = await getAQIDistribution(params)

    if (response.code === 0) {
      const distribution = response.data?.distribution
      if (!distribution || distribution.length === 0) {
        distributionData.value = null
        ElMessage.warning('暂无分布数据')
        return
      }

      distributionData.value = {
        total: response.data.total || 0,
        distribution: distribution.map(d => ({
          qualityLevel: d.quality_level,
          qualityLabel: d.quality_label,
          count: d.count || 0,
          percentage: d.percentage || 0,
          value: d.count || 0
        }))
      }
    } else {
      ElMessage.error(response.message || '统计失败')
    }
  } catch (error) {
    console.error('Distribution analysis failed:', error)
    ElMessage.error('统计失败')
  } finally {
    loading.value = false
  }
}

const handleDistributionReset = () => {
  distributionForm.value.city = ''
  handleDistribution()
}

const handleDistributionClear = () => {
  distributionForm.value.city = ''
  distributionData.value = null
  ElMessage.success('已重置')
}

onMounted(() => {
  // Load available cities on mount
  fetchAvailableCities()
})

// Watch for tab changes to lazy load distribution data
watch(activeTab, async (newTab) => {
  if (newTab === 'distribution' && !distributionData.value) {
    await nextTick()
    handleDistribution()
  }
})
</script>

<style scoped>
.analysis-page {
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: var(--spacing-xl);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.back-button {
  font-size: 14px;
  color: var(--text-secondary);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

/* Tabs */
.analysis-tabs {
  background: transparent;
}

:deep(.el-tabs__header) {
  margin-bottom: var(--spacing-lg);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 0 var(--spacing-md);
  border: 1px solid var(--border);
}

:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.el-tabs__item) {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  border-bottom: 2px solid transparent;
}

:deep(.el-tabs__item:hover) {
  color: var(--primary);
}

:deep(.el-tabs__item.is-active) {
  color: var(--primary);
}

:deep(.el-tabs__active-bar) {
  background: var(--primary);
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.selector-card {
  padding: var(--spacing-lg);
}

.chart-card {
  padding: var(--spacing-lg);
}

/* Selector Form */
.selector-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-row {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  align-items: flex-end;
}

.form-item {
  flex: 1;
  min-width: 200px;
}

.form-item-actions {
  flex: 0;
  display: flex;
  gap: var(--spacing-sm);
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: var(--spacing-xs);
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

/* Chart Card */
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.chart-legend {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 13px;
  color: var(--text-secondary);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.chart-container {
  min-height: 400px;
}

/* Correlation Results */
.correlation-results,
.distribution-results {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.results-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
}

.stats-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.stat-card {
  padding: var(--spacing-md);
  text-align: center;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  font-family: var(--font-mono);
}

.stat-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

.stat-equation {
  font-size: 14px;
  font-family: var(--font-mono);
  color: var(--text);
}

.stat-primary {
  color: var(--primary);
}

/* Guide Card */
.guide-card {
  padding: var(--spacing-md);
}

.guide-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-sm) 0;
}

.guide-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.guide-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.guide-range {
  color: var(--text-secondary);
  font-family: var(--font-mono);
}

.guide-label {
  font-weight: 500;
}

.guide-strong { color: #10B981; }
.guide-good { color: #22C55E; }
.guide-medium { color: #EAB308; }
.guide-weak { color: #F97316; }
.guide-poor { color: #EF4444; }

/* Distribution List */
.distribution-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.distribution-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
}

.dist-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.dist-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dist-label {
  font-size: 14px;
  color: var(--text);
}

.dist-stats {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.dist-value {
  font-size: 18px;
  font-weight: 700;
  font-family: var(--font-mono);
}

.dist-percent {
  font-size: 14px;
  color: var(--text-secondary);
  width: 50px;
  text-align: right;
}

.dist-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
  margin-top: var(--spacing-md);
  border-top: 1px solid var(--border);
  font-size: 14px;
  color: var(--text-secondary);
}

.dist-total-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-mono);
}

/* Responsive */
@media (max-width: 1024px) {
  .results-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .analysis-page {
    padding: var(--spacing-md);
  }

  .form-row {
    flex-direction: column;
  }

  .form-item,
  .form-item-actions {
    width: 100%;
  }

  .form-item-actions {
    display: flex;
  }

  .form-item-actions .el-button {
    flex: 1;
  }
}
</style>
