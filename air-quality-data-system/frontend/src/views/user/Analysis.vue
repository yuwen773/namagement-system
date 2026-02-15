<template>
  <div class="analysis-container min-h-screen bg-slate-950 relative overflow-hidden">
    <!-- Background grid -->
    <div class="grid-background absolute inset-0 opacity-10 pointer-events-none"></div>

    <!-- Main content -->
    <div class="relative z-10 p-6 lg:p-8">
      <!-- Header -->
      <header class="mb-6 animate-fade-in-down">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl lg:text-3xl font-bold text-white mb-1" style="font-family: 'Rajdhani', sans-serif;">
              数据分析
            </h1>
            <p class="text-slate-400 text-sm">城市对比、相关性分析与数据可视化</p>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="goBack"
              class="w-10 h-10 rounded-xl glass-card flex items-center justify-center hover-scale group"
            >
              <svg class="w-5 h-5 text-slate-400 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Analysis tabs -->
      <div class="glass-card rounded-2xl mb-6 animate-fade-in" style="animation-delay: 0.1s;">
        <div class="flex border-b border-slate-800/50">
          <button
            v-for="tab in analysisTabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            class="px-6 py-4 text-sm font-medium transition-all relative"
            :class="activeTab === tab.key ? 'text-cyan-400' : 'text-slate-400 hover:text-slate-300'"
            style="font-family: 'Rajdhani', sans-serif;"
          >
            {{ tab.label }}
            <span
              v-if="activeTab === tab.key"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-400"
            ></span>
          </button>
        </div>
      </div>

      <!-- Tab content -->
      <div class="animate-fade-in" style="animation-delay: 0.15s;">
        <!-- City comparison tab -->
        <div v-show="activeTab === 'compare'" class="space-y-6">
          <!-- City selector -->
          <div class="glass-card rounded-xl p-6">
            <div class="flex flex-wrap items-center gap-4">
              <div class="flex-1 min-w-[300px]">
                <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                  选择城市 (最多10个)
                </label>
                <el-select
                  v-model="selectedCities"
                  multiple
                  filterable
                  placeholder="选择要对比的城市"
                  class="w-full custom-select"
                  :popper-class="'dark-select-dropdown'"
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
              <div class="flex items-end">
                <button
                  @click="handleCompare"
                  :disabled="selectedCities.length < 2 || loading"
                  class="px-6 py-2.5 rounded-xl bg-cyan-500 text-white font-medium hover:bg-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover-scale"
                  style="font-family: 'Rajdhani', sans-serif;"
                >
                  <span v-if="!loading">开始对比</span>
                  <span v-else>分析中...</span>
                </button>
              </div>
            </div>

            <!-- Selected cities tags -->
            <div v-if="selectedCities.length > 0" class="mt-4 flex flex-wrap gap-2">
              <span
                v-for="code in selectedCities"
                :key="code"
                class="px-3 py-1.5 rounded-lg bg-slate-800/50 text-slate-300 text-sm flex items-center gap-2"
              >
                {{ getCityName(code) }}
                <button @click="removeCity(code)" class="hover:text-red-400 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
            </div>
          </div>

          <!-- Comparison chart -->
          <div v-if="comparisonData" class="glass-card rounded-2xl p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm text-slate-400 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                城市AQI趋势对比
              </h2>
              <div class="flex items-center gap-4 text-xs">
                <div v-for="city in comparisonData.series" :key="city.city_code" class="flex items-center gap-2">
                  <span class="w-3 h-3 rounded-sm" :style="{ background: city.color || '#06b6d4' }"></span>
                  <span class="text-slate-400">{{ city.city_name }}</span>
                </div>
              </div>
            </div>
            <div class="h-[400px]">
              <LineChart
                :data="comparisonData.series"
                :x-axis="comparisonData.xAxis"
                :smooth="true"
                :area-style="false"
                :show-data-zoom="true"
              />
            </div>
          </div>
        </div>

        <!-- Correlation analysis tab -->
        <div v-show="activeTab === 'correlation'" class="space-y-6">
          <!-- Correlation controls -->
          <div class="glass-card rounded-xl p-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                  X轴污染物
                </label>
                <el-select v-model="correlationForm.pollutantX" class="w-full custom-select" :popper-class="'dark-select-dropdown'">
                  <el-option label="PM2.5" value="pm25" />
                  <el-option label="PM10" value="pm10" />
                  <el-option label="SO₂" value="so2" />
                  <el-option label="NO₂" value="no2" />
                  <el-option label="CO" value="co" />
                  <el-option label="O₃" value="o3" />
                </el-select>
              </div>
              <div>
                <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                  Y轴污染物
                </label>
                <el-select v-model="correlationForm.pollutantY" class="w-full custom-select" :popper-class="'dark-select-dropdown'">
                  <el-option label="PM2.5" value="pm25" />
                  <el-option label="PM10" value="pm10" />
                  <el-option label="SO₂" value="so2" />
                  <el-option label="NO₂" value="no2" />
                  <el-option label="CO" value="co" />
                  <el-option label="O₃" value="o3" />
                </el-select>
              </div>
              <div>
                <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                  数据点数量
                </label>
                <el-select v-model="correlationForm.maxPoints" class="w-full custom-select" :popper-class="'dark-select-dropdown'">
                  <el-option label="500" :value="500" />
                  <el-option label="1000" :value="1000" />
                  <el-option label="2000" :value="2000" />
                  <el-option label="5000" :value="5000" />
                </el-select>
              </div>
              <div class="flex items-end">
                <button
                  @click="handleCorrelation"
                  :disabled="loading"
                  class="w-full px-6 py-2.5 rounded-xl bg-cyan-500 text-white font-medium hover:bg-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover-scale"
                  style="font-family: 'Rajdhani', sans-serif;"
                >
                  <span v-if="!loading">分析相关性</span>
                  <span v-else">分析中...</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Correlation results -->
          <div v-if="correlationData" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Scatter chart -->
            <div class="lg:col-span-2 glass-card rounded-2xl p-6">
              <h2 class="text-sm text-slate-400 uppercase tracking-wider mb-4" style="font-family: 'Rajdhani', sans-serif;">
                相关性散点图
              </h2>
              <div class="h-[400px]">
                <ScatterChart
                  :data="correlationData.scatterData"
                  :x-axis-name="getPollutantLabel(correlationForm.pollutantX)"
                  :y-axis-name="getPollutantLabel(correlationForm.pollutantY)"
                  :show-regression="true"
                  :regression-data="correlationData.regressionData"
                />
              </div>
            </div>

            <!-- Statistics -->
            <div class="space-y-4">
              <div class="glass-card rounded-xl p-4">
                <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">
                  相关系数
                </div>
                <div class="text-3xl font-bold font-mono" :style="{ color: getCorrelationColor(correlationData.correlation) }">
                  {{ correlationData.correlation?.toFixed(4) || '--' }}
                </div>
                <div class="text-xs text-slate-500 mt-1">
                  {{ getCorrelationLabel(correlationData.correlation) }}
                </div>
              </div>

              <div class="glass-card rounded-xl p-4">
                <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">
                  样本数量
                </div>
                <div class="text-2xl font-bold font-mono text-cyan-400">
                  {{ correlationData.sampleCount || '--' }}
                </div>
              </div>

              <div class="glass-card rounded-xl p-4">
                <div class="text-slate-500 text-xs mb-1" style="font-family: 'Rajdhani', sans-serif;">
                  回归方程
                </div>
                <div class="text-sm font-mono text-slate-300 break-all">
                  y = {{ correlationData.slope?.toFixed(4) || '--' }}x + {{ correlationData.intercept?.toFixed(4) || '--' }}
                </div>
              </div>

              <!-- Correlation guide -->
              <div class="glass-card rounded-xl p-4">
                <div class="text-slate-500 text-xs mb-2" style="font-family: 'Rajdhani', sans-serif;">
                  相关系数解释
                </div>
                <div class="space-y-2 text-xs text-slate-400">
                  <div class="flex justify-between">
                    <span>0.9 - 1.0</span>
                    <span class="text-emerald-400">极强相关</span>
                  </div>
                  <div class="flex justify-between">
                    <span>0.7 - 0.9</span>
                    <span class="text-green-400">强相关</span>
                  </div>
                  <div class="flex justify-between">
                    <span>0.4 - 0.7</span>
                    <span class="text-yellow-400">中等相关</span>
                  </div>
                  <div class="flex justify-between">
                    <span>0.2 - 0.4</span>
                    <span class="text-orange-400">弱相关</span>
                  </div>
                  <div class="flex justify-between">
                    <span>0 - 0.2</span>
                    <span class="text-red-400">极弱相关</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Distribution tab -->
        <div v-show="activeTab === 'distribution'" class="space-y-6">
          <!-- Distribution controls -->
          <div class="glass-card rounded-xl p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-slate-400 text-xs mb-2 uppercase tracking-wider" style="font-family: 'Rajdhani', sans-serif;">
                  城市
                </label>
                <el-select
                  v-model="distributionForm.city"
                  filterable
                  clearable
                  placeholder="选择城市（可选）"
                  class="w-full custom-select"
                  :popper-class="'dark-select-dropdown'"
                >
                  <el-option
                    v-for="city in availableCities"
                    :key="city.code"
                    :label="city.name"
                    :value="city.code"
                  />
                </el-select>
              </div>
              <div class="flex items-end gap-2">
                <button
                  @click="handleDistribution"
                  :disabled="loading"
                  class="flex-1 px-6 py-2.5 rounded-xl bg-cyan-500 text-white font-medium hover:bg-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover-scale"
                  style="font-family: 'Rajdhani', sans-serif;"
                >
                  <span v-if="!loading">统计分布</span>
                  <span v-else">统计中...</span>
                </button>
                <button
                  @click="distributionForm.city = ''; handleDistribution()"
                  class="px-6 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white hover-scale"
                  style="font-family: 'Rajdhani', sans-serif;"
                >
                  全国数据
                </button>
              </div>
            </div>
          </div>

          <!-- Distribution results -->
          <div v-if="distributionData" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Pie chart -->
            <div class="glass-card rounded-2xl p-6">
              <h2 class="text-sm text-slate-400 uppercase tracking-wider mb-4" style="font-family: 'Rajdhani', sans-serif;">
                空气质量等级分布
              </h2>
              <div class="h-[350px] flex items-center justify-center">
                <PieChart
                  :data="distributionData.distribution"
                  :donut="true"
                  :radius="['40%', '70%']"
                  :show-percentage="true"
                />
              </div>
            </div>

            <!-- Statistics table -->
            <div class="glass-card rounded-2xl p-6">
              <h2 class="text-sm text-slate-400 uppercase tracking-wider mb-4" style="font-family: 'Rajdhani', sans-serif;">
                详细统计
              </h2>
              <div class="space-y-3">
                <div
                  v-for="item in distributionData.distribution"
                  :key="item.qualityLevel"
                  class="flex items-center justify-between p-4 rounded-xl bg-slate-900/30"
                >
                  <div class="flex items-center gap-3">
                    <span
                      class="w-4 h-4 rounded-full"
                      :style="{ background: getAQIColorByLevel(item.qualityLevel) }"
                    ></span>
                    <span class="text-slate-300">{{ item.qualityLabel }}</span>
                  </div>
                  <div class="flex items-center gap-6">
                    <div class="text-right">
                      <div class="text-lg font-bold font-mono" :style="{ color: getAQIColorByLevel(item.qualityLevel) }">
                        {{ item.count }}
                      </div>
                      <div class="text-xs text-slate-500">数量</div>
                    </div>
                    <div class="text-right w-20">
                      <div class="text-lg font-bold font-mono text-cyan-400">
                        {{ item.percentage }}%
                      </div>
                      <div class="text-xs text-slate-500">占比</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Total -->
              <div class="mt-4 pt-4 border-t border-slate-800/50 flex items-center justify-between">
                <span class="text-slate-400 text-sm">总样本数</span>
                <span class="text-xl font-bold font-mono text-white">{{ distributionData.total }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { LineChart, ScatterChart, PieChart } from '@/components/charts'
import { compareCities, getCorrelationAnalysis, getAQIDistribution } from '@/api/airquality'

const router = useRouter()

// State
const loading = ref(false)
const activeTab = ref('compare')

// Tabs
const analysisTabs = [
  { key: 'compare', label: '城市对比' },
  { key: 'correlation', label: '相关性分析' },
  { key: 'distribution', label: 'AQI分布' }
]

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

// Available cities (mock data - should come from API)
const availableCities = ref([
  { code: '110101', name: '东城区' },
  { code: '110102', name: '西城区' },
  { code: '310101', name: '黄浦区' },
  { code: '310104', name: '徐汇区' },
  { code: '310105', name: '长宁区' },
  { code: '310106', name: '静安区' },
  { code: '440101', name: '市辖区' },
  { code: '440103', name: '荔湾区' },
  { code: '440104', name: '越秀区' },
  { code: '440106', name: '天河区' }
])

// Colors for city comparison
const cityColors = [
  '#06b6d4', '#8b5cf6', '#ec4899', '#f97316', '#14b8a6',
  '#3b82f6', '#6366f1', '#a855f7', '#f43f5e', '#0ea5e9'
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
  // Limit to 10 cities
  if (selectedCities.value.length > 10) {
    selectedCities.value = selectedCities.value.slice(0, 10)
    ElMessage.warning('最多选择10个城市进行对比')
  }
}

const handleCompare = async () => {
  if (selectedCities.value.length < 2) {
    ElMessage.warning('请至少选择2个城市进行对比')
    return
  }

  loading.value = true

  try {
    const response = await compareCities({
      city_codes: selectedCities.value,
      hours: 24
    })

    if (response.code === 0) {
      const data = response.data
      const xAxis = data.hours || []

      // Transform data for LineChart
      comparisonData.value = {
        xAxis: xAxis.map(h => {
          const date = new Date()
          date.setHours(date.getHours() - h)
          return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }),
        series: data.series.map((series, index) => ({
          name: series.city_name,
          city_code: series.city_code,
          city_name: series.city_name,
          data: series.trend.map(d => d.aqi),
          color: cityColors[index % cityColors.length]
        }))
      }
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
  if (!correlation) return '#64748b'
  const abs = Math.abs(correlation)
  if (abs >= 0.9) return '#10b981'
  if (abs >= 0.7) return '#22c55e'
  if (abs >= 0.4) return '#eab308'
  if (abs >= 0.2) return '#f97316'
  return '#ef4444'
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

      // Calculate regression line
      const scatterData = data.scatterData || []
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

      correlationData.value = {
        scatterData: scatterData,
        correlation: data.correlation,
        sampleCount: data.sampleCount,
        slope,
        intercept,
        regressionData: scatterData.length > 0
          ? [
            { x: Math.min(...scatterData.map(p => p.x)), y: intercept + slope * Math.min(...scatterData.map(p => p.x)) },
            { x: Math.max(...scatterData.map(p => p.x)), y: intercept + slope * Math.max(...scatterData.map(p => p.x)) }
          ]
          : []
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

const getAQIColorByLevel = (level) => {
  const colors = {
    EXCELLENT: '#00e400',
    Good: '#ffff00',
    'Light pollution': '#ff7e00',
    'Moderate pollution': '#ff0000',
    'Heavy pollution': '#99004c',
    'Severe pollution': '#7e0023'
  }
  return colors[level] || '#64748b'
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
      distributionData.value = {
        total: response.data.total,
        distribution: response.data.distribution.map(d => ({
          qualityLevel: d.quality_level,
          qualityLabel: d.quality_label,
          count: d.count,
          percentage: d.percentage
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

onMounted(() => {
  // Load initial data
  handleDistribution()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  border-color: rgba(148, 163, 184, 0.2);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
}

.grid-background {
  background-image: linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.hover-scale {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-scale:hover {
  transform: translateY(-1px);
}

.animate-fade-in {
  animation: fade-in 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

.animate-fade-in-down {
  animation: fade-in-down 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  opacity: 0;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Custom Element Plus overrides */
:deep(.custom-select .el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: none;
}

:deep(.custom-select .el-input__wrapper:hover) {
  border-color: rgba(148, 163, 184, 0.3);
}

:deep(.custom-select .el-input__wrapper.is-focus) {
  border-color: rgba(6, 182, 212, 0.5);
}

:deep(.custom-select .el-input__inner) {
  color: #e2e8f0;
  font-family: 'IBM Plex Sans', sans-serif;
}

:deep(.dark-select-dropdown) {
  background: rgba(15, 23, 42, 0.95) !important;
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(12px);
}

:deep(.dark-select-dropdown .el-select-dropdown__item) {
  color: #e2e8f0;
  font-family: 'IBM Plex Sans', sans-serif;
}

:deep(.dark-select-dropdown .el-select-dropdown__item.hover) {
  background: rgba(6, 182, 212, 0.1);
}

:deep(.dark-select-dropdown .el-select-dropdown__item.selected) {
  color: #06b6d4;
  background: rgba(6, 182, 212, 0.15);
}
</style>
