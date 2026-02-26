<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">数据驾驶舱</h1>
      <p class="dashboard-subtitle">非物质文化遗产全球分布概览</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <StatCard
        label="非遗项目总数"
        :value="overview.heritage_count"
        :icon="Collection"
        variant="primary"
        unit="项"
      />
      <StatCard
        label="传承人总数"
        :value="overview.inheritor_count"
        :icon="User"
        variant="success"
        unit="人"
      />
      <StatCard
        label="分类总数"
        :value="overview.category_count"
        :icon="Menu"
        variant="warning"
        unit="类"
      />
      <StatCard
        label="覆盖国家"
        :value="overview.country_count"
        :icon="Location"
        variant="danger"
        unit="个"
      />
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 世界地图 -->
      <div class="chart-card chart-map">
        <div class="chart-header">
          <h3 class="chart-title">全球分布地图</h3>
          <el-select
            v-model="selectedCategory"
            placeholder="选择分类"
            clearable
            size="small"
            style="width: 180px"
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
        <div ref="mapChartRef" class="chart-content"></div>
      </div>

      <!-- 类别占比饼图 -->
      <div class="chart-card chart-pie">
        <div class="chart-header">
          <h3 class="chart-title">类别占比分布</h3>
        </div>
        <div ref="pieChartRef" class="chart-content"></div>
      </div>

      <!-- 国家排行条形图 -->
      <div class="chart-card chart-bar">
        <div class="chart-header">
          <h3 class="chart-title">国家项目排行 TOP 20</h3>
        </div>
        <div ref="barChartRef" class="chart-content"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import { ElMessage } from 'element-plus'
import { Collection, User, Menu, Location } from '@element-plus/icons-vue'
import StatCard from '@/components/StatCard.vue'
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

// 图表实例
const mapChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()
const barChartRef = ref<HTMLElement>()
let mapChart: ECharts | null = null
let pieChart: ECharts | null = null
let barChart: ECharts | null = null

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

    // 初始化图表
    initCharts()
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    ElMessage.error('加载数据失败')
  }
}

// 初始化地图（使用散点图展示全球分布）
const initMapChart = () => {
  if (!mapChartRef.value) return

  mapChart = echarts.init(mapChartRef.value)

  // 使用散点图展示全球分布
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `
          <div style="padding: 8px;">
            <div style="font-weight: 600; margin-bottom: 4px;">${params.data[2]}</div>
            <div>非遗项目: ${params.data[3]} 项</div>
            <div>传承人: ${params.data[4]} 人</div>
          </div>
        `
      }
    },
    grid: {
      left: '3%',
      right: '3%',
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '经度',
      min: -180,
      max: 180,
      axisLabel: {
        color: '#606266'
      },
      splitLine: {
        lineStyle: {
          color: '#e4e7ed'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '纬度',
      min: -90,
      max: 90,
      axisLabel: {
        color: '#606266'
      },
      splitLine: {
        lineStyle: {
          color: '#e4e7ed'
        }
      }
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
        symbolSize: (val: any) => Math.max(Math.sqrt(val[3]) * 4, 10),
        itemStyle: {
          color: '#8b4513',
          opacity: 0.7,
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          itemStyle: {
            color: '#a0522d',
            opacity: 1,
            borderWidth: 2,
            shadowBlur: 10,
            shadowColor: 'rgba(139, 69, 19, 0.5)'
          }
        }
      }
    ]
  }

  mapChart.setOption(option)
}

// 初始化饼图
const initPieChart = () => {
  if (!pieChartRef.value) return

  pieChart = echarts.init(pieChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} 项 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center',
      textStyle: {
        color: '#606266'
      }
    },
    series: [
      {
        name: '类别占比',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%',
          color: '#606266'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        data: categoryData.value.map((item, index) => ({
          name: item.category_name,
          value: item.heritage_count,
          itemStyle: {
            color: [
              '#8b4513',
              '#a0522d',
              '#cd853f',
              '#daa520',
              '#f0b659',
              '#e6a23c',
              '#67c23a',
              '#409eff',
              '#f56c6c',
              '#909399'
            ][index % 10]
          }
        }))
      }
    ]
  }

  pieChart.setOption(option)
}

// 初始化条形图
const initBarChart = () => {
  if (!barChartRef.value) return

  barChart = echarts.init(barChartRef.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: '{b}: {c} 项'
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
      axisLabel: {
        color: '#606266'
      },
      splitLine: {
        lineStyle: {
          color: '#e4e7ed'
        }
      }
    },
    yAxis: {
      type: 'category',
      data: rankingData.value.map(item => item.country_name).reverse(),
      axisLabel: {
        color: '#606266'
      },
      axisTick: {
        show: false
      },
      axisLine: {
        show: false
      }
    },
    series: [
      {
        name: '项目数量',
        type: 'bar',
        data: rankingData.value.map(item => item.heritage_count).reverse(),
        barWidth: '60%',
        itemStyle: {
          borderRadius: [0, 4, 4, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#8b4513' },
            { offset: 1, color: '#cd853f' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#a0522d' },
              { offset: 1, color: '#daa520' }
            ])
          }
        },
        label: {
          show: true,
          position: 'right',
          color: '#606266',
          formatter: '{c}'
        }
      }
    ]
  }

  barChart.setOption(option)
}

// 初始化所有图表
const initCharts = () => {
  initMapChart()
  initPieChart()
  initBarChart()
}

// 处理分类筛选
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

// 窗口大小变化时重新渲染图表
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
.dashboard-container {
  min-height: 100%;
}

.dashboard-header {
  margin-bottom: 24px;
}

.dashboard-title {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
}

.dashboard-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-map {
  grid-column: span 12;
  min-height: 500px;
}

.chart-pie {
  grid-column: span 6;
  min-height: 400px;
}

.chart-bar {
  grid-column: span 6;
  min-height: 400px;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.chart-content {
  width: 100%;
  height: calc(100% - 50px);
  min-height: 300px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .chart-pie,
  .chart-bar {
    grid-column: span 12;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard-title {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
