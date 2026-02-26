<template>
  <div class="heritage-dashboard">
    <!-- 水墨晕染背景 - 多层次流动 -->
    <div class="ink-background">
      <div class="ink-layer layer-1"></div>
      <div class="ink-layer layer-2"></div>
      <div class="ink-layer layer-3"></div>
      <div class="floating-particles">
        <div v-for="i in 20" :key="i" class="particle" :style="{ '--delay': `${i * 0.5}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
      </div>
    </div>

    <!-- 页面头部 - 印章式 -->
    <header class="dashboard-header">
      <div class="header-decoration">
        <div class="decoration-line"></div>
        <div class="seal-group">
          <div class="main-seal">
            <div class="seal-inner">
              <span class="seal-text-vertical">御览</span>
            </div>
          </div>
          <div class="seal-shadow"></div>
        </div>
        <div class="decoration-line"></div>
      </div>
      <div class="header-content">
        <h1 class="page-title">非遗数字驾驶舱</h1>
        <p class="page-subtitle">Intangible Cultural Heritage Global Overview</p>
      </div>
    </header>

    <!-- 统计卡片 - 竹简式 -->
    <div class="stats-section">
      <div
        v-for="(stat, index) in statsData"
        :key="stat.key"
        class="stat-card"
        :class="`stat-${stat.variant}`"
        :style="{ '--delay': `${index * 0.1}s` }"
      >
        <div class="card-bg-pattern"></div>
        <div class="card-border-left"></div>
        <div class="card-seal" :class="`seal-${stat.variant}`">
          {{ stat.sealChar }}
        </div>
        <div class="card-icon" :class="`icon-${stat.variant}`">
          <component :is="stat.icon" />
        </div>
        <div class="card-value">
          <span class="value-number">{{ animatedStats[stat.key] }}</span>
          <span class="value-unit">{{ stat.unit }}</span>
        </div>
        <div class="card-label">{{ stat.label }}</div>
        <div class="card-ripple" :class="`ripple-${stat.variant}`"></div>
      </div>
    </div>

    <!-- 图表区域 - 宣纸画卷 -->
    <div class="charts-section">
      <!-- 世界分布图 -->
      <div class="chart-card map-chart">
        <div class="chart-frame">
          <div class="frame-corner top-left"></div>
          <div class="frame-corner top-right"></div>
          <div class="frame-corner bottom-left"></div>
          <div class="frame-corner bottom-right"></div>
          <div class="chart-header">
            <div class="header-title-group">
              <span class="title-seal">寰</span>
              <h3 class="chart-title">寰宇分布图</h3>
            </div>
            <el-select
              v-model="selectedCategory"
              placeholder="筛选类别"
              clearable
              size="small"
              class="heritage-select"
              @change="handleCategoryChange"
            >
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.name"
                :value="cat.id"
              />
            </el-select>
          </div>
          <div ref="mapChartRef" class="chart-body"></div>
        </div>
      </div>

      <!-- 类别玉璧图 -->
      <div class="chart-card pie-chart">
        <div class="chart-frame">
          <div class="frame-corner top-left"></div>
          <div class="frame-corner top-right"></div>
          <div class="frame-corner bottom-left"></div>
          <div class="frame-corner bottom-right"></div>
          <div class="chart-header">
            <div class="header-title-group">
              <span class="title-seal">类</span>
              <h3 class="chart-title">类别玉璧图</h3>
            </div>
          </div>
          <div ref="pieChartRef" class="chart-body"></div>
        </div>
      </div>

      <!-- 国家排行 - 卷轴式 -->
      <div class="chart-card bar-chart">
        <div class="chart-frame">
          <div class="frame-corner top-left"></div>
          <div class="frame-corner top-right"></div>
          <div class="frame-corner bottom-left"></div>
          <div class="frame-corner bottom-right"></div>
          <div class="chart-header">
            <div class="header-title-group">
              <span class="title-seal">邦</span>
              <h3 class="chart-title">各国项目排行</h3>
            </div>
          </div>
          <div ref="barChartRef" class="chart-body"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import { ElMessage } from 'element-plus'
import { Collection, User, Menu, Location } from '@element-plus/icons-vue'
import {
  getOverview,
  getMapDistribution,
  getCategoryDistribution,
  getCountryRanking
} from '@/api/dashboard'
import { getCategoryList } from '@/api/category'
import type {
  DashboardOverview,
  MapPoint,
  CategoryDistribution,
  CountryRanking,
  Category
} from '@/types'

// 数据状态
const overview = ref<DashboardOverview>({
  heritage_count: 0,
  inheritor_count: 0,
  category_count: 0,
  country_count: 0
})
const mapData = ref<MapPoint[]>([])
const categoryData = ref<CategoryDistribution[]>([])
const rankingData = ref<CountryRanking[]>([])
const categories = ref<Category[]>([])
const selectedCategory = ref<number | undefined>(undefined)

// 动画数据
const animatedStats = ref({
  heritage: 0,
  inheritor: 0,
  category: 0,
  country: 0
})

// 统计卡片配置
const statsData = computed(() => [
  {
    key: 'heritage',
    label: '非遗项目',
    value: overview.value.heritage_count,
    unit: '项',
    icon: Collection,
    variant: 'vermilion',
    sealChar: '宝'
  },
  {
    key: 'inheritor',
    label: '传承人',
    value: overview.value.inheritor_count,
    unit: '人',
    icon: User,
    variant: 'ink',
    sealChar: '匠'
  },
  {
    key: 'category',
    label: '分类',
    value: overview.value.category_count,
    unit: '类',
    icon: Menu,
    variant: 'gold',
    sealChar: '门'
  },
  {
    key: 'country',
    label: '覆盖国家',
    value: overview.value.country_count,
    unit: '个',
    icon: Location,
    variant: 'jade',
    sealChar: '宇'
  }
])

// 数字滚动动画 - 带缓动效果
const animateNumber = (key: string, target: number) => {
  const duration = 2000
  const start = Date.now()
  const startValue = animatedStats.value[key as keyof typeof animatedStats]

  const animate = () => {
    const now = Date.now()
    const progress = Math.min((now - start) / duration, 1)
    // 使用easeOutQuart缓动函数
    const easeOut = 1 - Math.pow(1 - progress, 4)
    animatedStats.value[key as keyof typeof animatedStats] = Math.floor(
      startValue + (target - startValue) * easeOut
    )

    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }
  animate()
}

// 图表实例
const mapChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()
const barChartRef = ref<HTMLElement>()
let mapChart: ECharts | null = null
let pieChart: ECharts | null = null
let barChart: ECharts | null = null

// 中国传统色彩 - 优化后的色彩序列
const traditionalColors = [
  '#C23531', // 朱砂红
  '#D4AF37', // 金色
  '#2F3640', // 墨黑
  '#5D8AA8', // 青瓷
  '#3B7A57', // 黛绿
  '#8B4513', // 赭石
  '#CD7F32', // 青铜
  '#DC143C', // 胭脂
  '#4A6741', // 竹青
  '#B8860B'  // 暗金
]

// 加载数据
const loadData = async () => {
  try {
    const [overviewRes, mapRes, categoryRes, rankingRes, categoriesRes] = await Promise.all([
      getOverview(),
      getMapDistribution(),
      getCategoryDistribution(),
      getCountryRanking({ limit: 20 }),
      getCategoryList()
    ])

    overview.value = overviewRes.data.data
    mapData.value = mapRes.data.data
    categoryData.value = categoryRes.data.data
    rankingData.value = rankingRes.data.data
    categories.value = categoriesRes.data.data

    // 触发数字动画
    setTimeout(() => {
      Object.keys(overview.value).forEach(key => {
        const statKey = key === 'heritage_count' ? 'heritage' :
                       key === 'inheritor_count' ? 'inheritor' :
                       key === 'category_count' ? 'category' : 'country'
        animateNumber(statKey, overview.value[key as keyof DashboardOverview])
      })
    }, 300)

    // 延迟初始化图表以确保动画效果
    setTimeout(initCharts, 500)
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    ElMessage.error('加载数据失败')
  }
}

// 初始化水墨散点地图
const initMapChart = () => {
  if (!mapChartRef.value) return

  mapChart = echarts.init(mapChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: (params: any) => `
        <div style="padding: 8px;">
          <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color: #D4AF37;">
            ${params.data[2]}
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin: 4px 0;">
            <span style="color: #909399;">非遗项目：</span>
            <span style="font-weight: 600;">${params.data[3]} 项</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #909399;">传承人：</span>
            <span style="font-weight: 600;">${params.data[4]} 人</span>
          </div>
        </div>
      `
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '5%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '经度',
      min: -180,
      max: 180,
      axisLine: { lineStyle: { color: '#D4AF37', opacity: 0.4 } },
      axisLabel: { color: '#606266', fontSize: 11 },
      splitLine: { lineStyle: { color: '#E4E7ED', type: 'dashed', opacity: 0.4 } },
      nameTextStyle: { color: '#606266' }
    },
    yAxis: {
      type: 'value',
      name: '纬度',
      min: -90,
      max: 90,
      axisLine: { lineStyle: { color: '#D4AF37', opacity: 0.4 } },
      axisLabel: { color: '#606266', fontSize: 11 },
      splitLine: { lineStyle: { color: '#E4E7ED', type: 'dashed', opacity: 0.4 } },
      nameTextStyle: { color: '#606266' }
    },
    series: [
      {
        type: 'scatter',
        data: mapData.value.map(item => [
          item.longitude,
          item.latitude,
          item.country_name,
          item.heritage_count,
          item.inheritor_count
        ]),
        symbolSize: (val: any) => Math.max(Math.sqrt(val[3]) * 6, 14),
        itemStyle: {
          color: '#C23531',
          opacity: 0.8,
          borderColor: '#D4AF37',
          borderWidth: 2
        },
        emphasis: {
          itemStyle: {
            color: '#DC143C',
            opacity: 1,
            borderWidth: 3,
            shadowBlur: 25,
            shadowColor: 'rgba(194, 35, 49, 0.7)'
          },
          scale: 1.2
        }
      }
    ]
  }

  mapChart.setOption(option)
}

// 初始化玉璧饼图
const initPieChart = () => {
  if (!pieChartRef.value) return

  pieChart = echarts.init(pieChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: '{b}: {c} 项 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: {
        color: '#2F3640',
        fontSize: 13,
        fontWeight: 500
      },
      itemGap: 16,
      itemWidth: 18,
      itemHeight: 18,
      formatter: (name: string) => {
        const item = categoryData.value.find(d => d.category_name === name)
        if (item) {
          return `${name}  ${item.heritage_count}项`
        }
        return name
      }
    },
    series: [
      {
        name: '类别分布',
        type: 'pie',
        radius: ['40%', '75%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: '#F7F4ED',
          borderWidth: 4
        },
        label: {
          show: true,
          position: 'outside',
          formatter: (params: any) => {
            if (params.percent >= 5) {
              return `${params.name}\n${params.percent.toFixed(1)}%`
            }
            return ''
          },
          color: '#2F3640',
          fontSize: 12,
          fontWeight: 500
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 20,
          smooth: true,
          lineStyle: { color: '#D4AF37', width: 1.5 }
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 20,
            shadowOffsetX: 0,
            shadowColor: 'rgba(212, 175, 55, 0.5)'
          }
        },
        data: categoryData.value.map((item, index) => ({
          name: item.category_name,
          value: item.heritage_count,
          itemStyle: {
            color: traditionalColors[index % traditionalColors.length]
          }
        }))
      }
    ]
  }

  pieChart.setOption(option)
}

// 初始化卷轴条形图
const initBarChart = () => {
  if (!barChartRef.value) return

  barChart = echarts.init(barChartRef.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(47, 54, 64, 0.95)',
      borderColor: '#D4AF37',
      borderWidth: 2,
      textStyle: { color: '#F7F4ED', fontSize: 14 },
      formatter: (params: any) => {
        const data = params[0]
        return `<span style="color: #D4AF37; font-weight: 600;">${data.name}</span>: ${data.value} 项`
      }
    },
    grid: {
      left: '18%',
      right: '12%',
      bottom: '8%',
      top: '5%',
      containLabel: false
    },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#606266', fontSize: 11 },
      splitLine: {
        lineStyle: { color: '#D4AF37', type: 'dashed', opacity: 0.15 }
      }
    },
    yAxis: {
      type: 'category',
      data: rankingData.value.map(item => item.country_name).reverse(),
      axisLabel: {
        color: '#2F3640',
        fontSize: 13,
        width: 100,
        overflow: 'truncate',
        ellipsis: '...',
        fontWeight: 500
      },
      axisTick: { show: false },
      axisLine: { show: false }
    },
    series: [
      {
        name: '项目数量',
        type: 'bar',
        data: rankingData.value.map(item => item.heritage_count).reverse(),
        barWidth: '65%',
        itemStyle: {
          borderRadius: [0, 8, 8, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#C23531' },
            { offset: 0.5, color: '#D4AF37' },
            { offset: 1, color: '#CD7F32' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#DC143C' },
              { offset: 1, color: '#D4AF37' }
            ]),
            shadowBlur: 15,
            shadowColor: 'rgba(212, 175, 55, 0.4)'
          }
        },
        label: {
          show: true,
          position: 'right',
          color: '#C23531',
          fontSize: 13,
          fontWeight: 600,
          formatter: '{c}'
        }
      }
    ]
  }

  barChart.setOption(option)
}

const initCharts = () => {
  initMapChart()
  initPieChart()
  initBarChart()
}

const handleCategoryChange = async () => {
  try {
    const res = await getMapDistribution(
      selectedCategory.value ? { category: selectedCategory.value } : undefined
    )
    mapData.value = res.data.data
    initMapChart()
  } catch (error) {
    console.error('Failed to filter map data:', error)
    ElMessage.error('筛选失败')
  }
}

const handleResize = () => {
  mapChart?.resize()
  pieChart?.resize()
  barChart?.resize()
}

onMounted(() => {
  loadData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  mapChart?.dispose()
  pieChart?.dispose()
  barChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* ========== 全局样式 ========== */
.heritage-dashboard {
  min-height: 100%;
  position: relative;
  padding: 40px 32px;
  background: #F7F4ED;
  overflow-x: hidden;
}

/* ========== 水墨晕染背景 ========== */
.ink-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.ink-layer {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.08;
  animation: inkDrift 40s ease-in-out infinite;
}

.ink-layer.layer-1 {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle at center, #C23531 0%, transparent 70%);
  top: -200px;
  right: -200px;
  animation-delay: 0s;
}

.ink-layer.layer-2 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle at center, #D4AF37 0%, transparent 70%);
  bottom: -150px;
  left: -150px;
  animation-delay: -15s;
}

.ink-layer.layer-3 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle at center, #2F3640 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -30s;
}

@keyframes inkDrift {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(40px, -30px) scale(1.05);
  }
  50% {
    transform: translate(-30px, 40px) scale(0.95);
  }
  75% {
    transform: translate(-40px, -40px) scale(1.02);
  }
}

.floating-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.6) 0%, transparent 70%);
  border-radius: 50%;
  left: var(--x);
  top: var(--y);
  animation: particleFloat 20s ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes particleFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translate(30px, -50px) scale(1.5);
    opacity: 0.8;
  }
}

/* ========== 页面头部 ========== */
.dashboard-header {
  position: relative;
  z-index: 1;
  text-align: center;
  margin-bottom: 48px;
}

.header-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  margin-bottom: 24px;
}

.decoration-line {
  width: 120px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #D4AF37, transparent);
  position: relative;
}

.decoration-line::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #C23531;
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(194, 35, 49, 0.2);
}

.seal-group {
  position: relative;
}

.main-seal {
  width: 88px;
  height: 88px;
  background: #C23531;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 8px 32px rgba(194, 35, 49, 0.5),
    inset 0 2px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  animation: sealFloat 6s ease-in-out infinite;
}

@keyframes sealFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-8px) rotate(2deg);
  }
}

.main-seal::before {
  content: '';
  position: absolute;
  top: 6px;
  left: 6px;
  right: 6px;
  bottom: 6px;
  border: 2px solid rgba(212, 175, 55, 0.5);
  border-radius: 4px;
}

.seal-inner {
  width: 76px;
  height: 76px;
  background: rgba(194, 35, 49, 0.9);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.25);
}

.seal-text-vertical {
  writing-mode: vertical-rl;
  color: #F7F4ED;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 12px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  font-family: "STSong", "SimSun", serif;
}

.seal-shadow {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 88px;
  height: 88px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  z-index: -1;
}

.header-content {
  position: relative;
}

.page-title {
  font-size: 42px;
  font-weight: 700;
  color: #2F3640;
  margin: 0 0 12px 0;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
  background: linear-gradient(135deg, #C23531 0%, #2F3640 50%, #D4AF37 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleShimmer 3s ease-in-out infinite;
}

@keyframes titleShimmer {
  0%, 100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.1);
  }
}

.page-subtitle {
  margin: 0;
  font-size: 13px;
  color: #909399;
  letter-spacing: 3px;
  text-transform: uppercase;
  font-weight: 500;
}

/* ========== 统计卡片 ========== */
.stats-section {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  position: relative;
  background: linear-gradient(135deg, #FFFBF7 0%, #F7F4ED 100%);
  border-radius: 12px;
  padding: 28px 24px;
  box-shadow:
    0 2px 0 0 rgba(212, 175, 55, 0.2),
    0 12px 32px rgba(47, 54, 64, 0.1);
  overflow: hidden;
  animation: cardSlideIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
  animation-delay: var(--delay);
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes cardSlideIn {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.stat-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 2px 0 0 rgba(212, 175, 55, 0.3),
    0 20px 48px rgba(47, 54, 64, 0.15);
}

.card-bg-pattern {
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle at top right, rgba(212, 175, 55, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.card-border-left {
  position: absolute;
  left: 0;
  top: 20%;
  bottom: 20%;
  width: 4px;
  background: linear-gradient(180deg, transparent 0%, #D4AF37 50%, transparent 100%);
  border-radius: 2px;
}

.card-seal {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  border-radius: 4px;
  font-family: "STSong", "SimSun", serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.seal-vermilion {
  background: #C23531;
  color: white;
}

.seal-ink {
  background: #2F3640;
  color: white;
}

.seal-gold {
  background: #D4AF37;
  color: #2F3640;
}

.seal-jade {
  background: #5D8AA8;
  color: white;
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin-bottom: 20px;
  color: white;
  position: relative;
}

.card-icon::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 16px;
  padding: 3px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), transparent);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s;
}

.stat-card:hover .card-icon::after {
  opacity: 1;
}

.icon-vermilion {
  background: linear-gradient(135deg, #C23531 0%, #E74C3C 100%);
  box-shadow: 0 8px 20px rgba(194, 35, 49, 0.35);
}

.icon-ink {
  background: linear-gradient(135deg, #2F3640 0%, #4A5568 100%);
  box-shadow: 0 8px 20px rgba(47, 54, 64, 0.35);
}

.icon-gold {
  background: linear-gradient(135deg, #D4AF37 0%, #F4D03F 100%);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.35);
}

.icon-jade {
  background: linear-gradient(135deg, #5D8AA8 0%, #7FB3D5 100%);
  box-shadow: 0 8px 20px rgba(93, 138, 168, 0.35);
}

.card-value {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 10px;
}

.value-number {
  font-size: 42px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  font-family: "STSong", "SimSun", serif;
  line-height: 1;
}

.stat-vermilion .value-number {
  color: #C23531;
  text-shadow: 0 2px 8px rgba(194, 35, 49, 0.2);
}

.stat-ink .value-number {
  color: #2F3640;
  text-shadow: 0 2px 8px rgba(47, 54, 64, 0.2);
}

.stat-gold .value-number {
  color: #D4AF37;
  text-shadow: 0 2px 8px rgba(212, 175, 55, 0.2);
}

.stat-jade .value-number {
  color: #5D8AA8;
  text-shadow: 0 2px 8px rgba(93, 138, 168, 0.2);
}

.value-unit {
  font-size: 15px;
  color: #909399;
  font-weight: 500;
}

.card-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
  letter-spacing: 1px;
}

.card-ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  border-radius: 50%;
  pointer-events: none;
  transition: all 0.6s ease-out;
}

.stat-card:hover .card-ripple {
  width: 300px;
  height: 300px;
}

.ripple-vermilion {
  background: radial-gradient(circle, rgba(194, 35, 49, 0.1) 0%, transparent 70%);
}

.ripple-ink {
  background: radial-gradient(circle, rgba(47, 54, 64, 0.08) 0%, transparent 70%);
}

.ripple-gold {
  background: radial-gradient(circle, rgba(212, 175, 55, 0.12) 0%, transparent 70%);
}

.ripple-jade {
  background: radial-gradient(circle, rgba(93, 138, 168, 0.1) 0%, transparent 70%);
}

/* ========== 图表区域 ========== */
.charts-section {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.chart-card {
  position: relative;
  animation: chartFadeIn 1s ease-out backwards;
  animation-delay: 0.5s;
}

@keyframes chartFadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.map-chart {
  grid-column: span 12;
}

.pie-chart,
.bar-chart {
  grid-column: span 6;
}

.chart-frame {
  position: relative;
  background: white;
  border-radius: 12px;
  padding: 28px;
  box-shadow:
    0 1px 0 0 rgba(212, 175, 55, 0.2) inset,
    0 12px 32px rgba(47, 54, 64, 0.1);
  overflow: hidden;
}

.chart-frame::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
}

.frame-corner {
  position: absolute;
  width: 24px;
  height: 24px;
  border: 2px solid #D4AF37;
  opacity: 0.35;
}

.frame-corner.top-left {
  top: 12px;
  left: 12px;
  border-right: none;
  border-bottom: none;
}

.frame-corner.top-right {
  top: 12px;
  right: 12px;
  border-left: none;
  border-bottom: none;
}

.frame-corner.bottom-left {
  bottom: 12px;
  left: 12px;
  border-right: none;
  border-top: none;
}

.frame-corner.bottom-right {
  bottom: 12px;
  right: 12px;
  border-left: none;
  border-top: none;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-seal {
  width: 36px;
  height: 36px;
  background: #C23531;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  border-radius: 4px;
  font-family: "STSong", "SimSun", serif;
  box-shadow: 0 4px 12px rgba(194, 35, 49, 0.3);
}

.chart-title {
  font-size: 20px;
  font-weight: 600;
  color: #2F3640;
  margin: 0;
  letter-spacing: 3px;
  font-family: "STSong", "SimSun", serif;
}

:deep(.heritage-select) {
  width: 180px;
}

:deep(.heritage-select .el-input__wrapper) {
  background: #F7F4ED;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 8px;
  box-shadow: none;
}

:deep(.heritage-select .el-input__wrapper:hover) {
  border-color: #D4AF37;
}

:deep(.heritage-select .el-input__wrapper.is-focus) {
  border-color: #C23531;
  box-shadow: 0 0 0 3px rgba(194, 35, 49, 0.1);
}

.chart-body {
  width: 100%;
  min-height: 420px;
}

.map-chart .chart-body {
  min-height: 520px;
}

/* ========== 响应式 ========== */
@media (max-width: 1400px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .pie-chart,
  .bar-chart {
    grid-column: span 12;
  }
}

@media (max-width: 768px) {
  .heritage-dashboard {
    padding: 24px 16px;
  }

  .header-decoration {
    flex-direction: column;
    gap: 16px;
  }

  .decoration-line {
    width: 80px;
  }

  .page-title {
    font-size: 32px;
    letter-spacing: 4px;
  }

  .stats-section {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .map-chart,
  .pie-chart,
  .bar-chart {
    grid-column: span 1;
  }

  .chart-frame {
    padding: 20px;
  }

  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  :deep(.heritage-select) {
    width: 100%;
  }
}

/* ========== 滚动条样式 ========== */
:deep(*)::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

:deep(*)::-webkit-scrollbar-track {
  background: rgba(212, 175, 55, 0.1);
  border-radius: 4px;
}

:deep(*)::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #D4AF37, #CD7F32);
  border-radius: 4px;
}

:deep(*)::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #C23531, #D4AF37);
}
</style>
