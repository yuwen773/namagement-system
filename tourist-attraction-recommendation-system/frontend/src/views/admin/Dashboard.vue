<template>
  <div class="dashboard-page">
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.title" class="stat-card" :class="stat.colorClass">
        <div class="stat-icon">
          <component :is="stat.icon" />
        </div>
        <div class="stat-content">
          <p class="stat-label">{{ stat.title }}</p>
          <p class="stat-value">{{ stat.value }}</p>
          <div class="stat-trend" v-if="stat.trend">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12 7l-5 5 1.41 1.41L12 9.83l3.59 3.58L17 12l-5-5zm-5 2l5-5 5 5-5-5-5-5z" clip-rule="evenodd"/>
            </svg>
            <span>{{ stat.trend }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <!-- Monthly Trend Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title-wrapper">
            <div class="chart-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3v18h18"/>
                <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
              </svg>
            </div>
            <div>
              <h3 class="chart-title">月度数据趋势</h3>
              <p class="chart-subtitle">过去6个月的数据统计</p>
            </div>
          </div>
        </div>
        <div ref="chartRef" class="chart-container"></div>
      </div>

      <!-- Hot Attractions Chart -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title-wrapper">
            <div class="chart-icon hot">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
              </svg>
            </div>
            <div>
              <h3 class="chart-title">热门景点 TOP 10</h3>
              <p class="chart-subtitle">基于热度值排序</p>
            </div>
          </div>
        </div>
        <div ref="hotChartRef" class="chart-container"></div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h3 class="section-title">快捷操作</h3>
      <div class="actions-grid">
        <router-link to="/admin/users" class="action-card">
          <div class="action-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <span>用户管理</span>
        </router-link>
        <router-link to="/admin/attractions" class="action-card">
          <div class="action-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <circle cx="8.5" cy="8.5" r="1.5"/>
              <polyline points="21 15 16 10 5 21"/>
            </svg>
          </div>
          <span>景点管理</span>
        </router-link>
        <router-link to="/admin/comments" class="action-card">
          <div class="action-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <span>评论审核</span>
        </router-link>
        <router-link to="/admin/announcements" class="action-card">
          <div class="action-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </div>
          <span>发布公告</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, markRaw } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import request from '@/api/request'
import { User, View, ChatDotRound, Star } from '@element-plus/icons-vue'

const chartRef = ref(null)
const hotChartRef = ref(null)
let chartInstance = null
let hotChartInstance = null

const stats = ref([
  { title: '用户总数', value: '0', icon: markRaw(User), colorClass: 'blue', trend: '+12%' },
  { title: '浏览量', value: '0', icon: markRaw(View), colorClass: 'green', trend: '+23%' },
  { title: '评论数', value: '0', icon: markRaw(ChatDotRound), colorClass: 'orange', trend: '+8%' },
  { title: '景点数', value: '0', icon: markRaw(Star), colorClass: 'purple' }
])

async function fetchDashboard() {
  try {
    const res = await request.get('/statistics/dashboard/')
    // request.js 拦截器已提取 data 字段: res.data = { total_users, total_attractions, ... }
    if (res.data) {
      const data = res.data
      stats.value[0].value = data.total_users?.toLocaleString() || '0'
      stats.value[1].value = data.total_views?.toLocaleString() || '0'
      stats.value[2].value = data.total_comments?.toLocaleString() || '0'
      stats.value[3].value = data.total_attractions?.toLocaleString() || '0'
    }
    // 获取图表数据
    try {
      const chartsRes = await request.get('/statistics/monthly/')
      // 拦截器已提取 data: chartsRes.data = [{month, new_users, ...}, ...]
      if (chartsRes.data && Array.isArray(chartsRes.data)) {
        initCharts(chartsRes.data)
      }
    } catch (chartsError) {
      console.warn('获取图表数据失败', chartsError)
      initCharts([])
    }
  } catch (error) {
    console.error('获取看板数据失败', error)
    ElMessage.error('获取看板数据失败')
  }
}

function initCharts(data) {
  if (!chartRef.value || !hotChartRef.value) return

  // 转换月度数据格式
  // 后端返回: [{month, new_users, new_attractions, new_comments}, ...]
  const months = data.map(item => item.month) || []
  const users = data.map(item => item.new_users) || []
  // 浏览量暂时使用评论数替代（评论数与浏览量相关）
  const views = data.map(item => item.new_comments * 10) || []
  const comments = data.map(item => item.new_comments) || []

  // Monthly Trend Chart
  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(30, 58, 95, 0.9)',
      borderColor: '#fbbf24',
      textStyle: { color: '#fff' }
    },
    legend: {
      data: ['新增用户', '浏览量', '评论数'],
      textStyle: { color: '#6b7280' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#6b7280' }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#6b7280' },
      splitLine: { lineStyle: { color: '#f3f4f6' } }
    },
    series: [
      {
        name: '新增用户',
        type: 'line',
        data: users,
        smooth: true,
        itemStyle: { color: '#fbbf24' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(251, 191, 36, 0.3)' },
            { offset: 1, color: 'rgba(251, 191, 36, 0)' }
          ])
        }
      },
      {
        name: '浏览量',
        type: 'line',
        data: views,
        smooth: true,
        itemStyle: { color: '#22c55e' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(34, 197, 94, 0.3)' },
            { offset: 1, color: 'rgba(34, 197, 94, 0)' }
          ])
        }
      },
      {
        name: '评论数',
        type: 'line',
        data: comments,
        smooth: true,
        itemStyle: { color: '#f97316' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(249, 115, 22, 0.3)' },
            { offset: 1, color: 'rgba(249, 115, 22, 0)' }
          ])
        }
      }
    ]
  })

  // 尝试获取热门景点数据
  fetchHotAttractions()
}

// 获取热门景点数据
async function fetchHotAttractions() {
  try {
    const res = await request.get('/statistics/hot/')
    if (res.data?.code === 0 && res.data?.data) {
      const hotData = res.data.data
      const hotNames = hotData.map(item => item.name) || []
      const hotValues = hotData.map(item => item.view_count) || []
      initHotChart(hotNames, hotValues)
    }
  } catch (error) {
    console.warn('获取热门景点数据失败', error)
    // 使用空数据初始化
    initHotChart([], [])
  }
}

function initHotChart(hotNames, hotValues) {
  if (!hotChartRef.value) return

  hotChartInstance = echarts.init(hotChartRef.value)
  hotChartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(30, 58, 95, 0.9)',
      borderColor: '#ef4444',
      textStyle: { color: '#fff' }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { show: false },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: hotNames,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#374151', fontSize: 13 }
    },
    series: [{
      type: 'bar',
      data: hotValues,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#ef4444' },
            { offset: 1, color: '#f87171' }
          ]),
        borderRadius: [0, 4, 4, 0]
      },
      barWidth: 16
    }]
  })
}

onMounted(fetchDashboard)
onUnmounted(() => {
  chartInstance?.dispose()
  hotChartInstance?.dispose()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.dashboard-page {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.stat-card.blue { border-left: 4px solid #3b82f6; }
.stat-card.green { border-left: 4px solid #22c55e; }
.stat-card.orange { border-left: 4px solid #f97316; }
.stat-card.purple { border-left: 4px solid #a855f7; }

.stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  flex-shrink: 0;
}

.stat-card.blue .stat-icon { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #3b82f6; }
.stat-card.green .stat-icon { background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); color: #22c55e; }
.stat-card.orange .stat-icon { background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); color: #f97316; }
.stat-card.purple .stat-icon { background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); color: #a855f7; }

.stat-icon svg {
  width: 28px;
  height: 28px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-value {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 600;
}

.stat-card.blue .stat-trend { color: #3b82f6; }
.stat-card.green .stat-trend { color: #22c55e; }
.stat-card.orange .stat-trend { color: #f97316; }
.stat-card.purple .stat-trend { color: #a855f7; }

.stat-trend svg {
  width: 16px;
  height: 16px;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  margin-bottom: 24px;
}

.chart-title-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
}

.chart-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
  border-radius: 12px;
  color: #1e3a5f;
}

.chart-icon.hot {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #ef4444;
}

.chart-icon svg {
  width: 24px;
  height: 24px;
}

.chart-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.chart-subtitle {
  font-size: 14px;
  color: #6b7280;
}

.chart-container {
  height: 320px;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 32px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #374151;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border-color: #fbbf24;
  color: #1e3a5f;
}

.action-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 12px;
  color: #1e3a5f;
}

.action-icon svg {
  width: 24px;
  height: 24px;
}

.action-card span {
  font-weight: 600;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
