<template>
  <div class="statistics-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">📊</span>
        综合统计分析
      </h1>
      <div class="page-subtitle">数据驱动决策，洞察食堂运营全貌</div>
    </div>

    <!-- 顶部统计卡片 -->
    <section class="top-cards-section">
      <div class="stat-card stat-primary" v-loading="overviewLoading">
        <div class="card-bg-pattern"></div>
        <div class="card-icon">👥</div>
        <div class="card-content">
          <div class="card-label">员工总数</div>
          <div class="card-value">{{ overviewData.total_count || 0 }}</div>
          <div class="card-trend">
            <span class="trend-up">在职 {{ overviewData.active_count || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="stat-card stat-success" v-loading="overviewLoading">
        <div class="card-bg-pattern"></div>
        <div class="card-icon">📈</div>
        <div class="card-content">
          <div class="card-label">今日出勤率</div>
          <div class="card-value">{{ overviewData.attendance_rate || 0 }}%</div>
          <div class="card-trend">
            <span v-if="overviewData.late_count > 0" class="trend-warning">迟到 {{ overviewData.late_count }} 人</span>
            <span v-else class="trend-good">全员准时</span>
          </div>
        </div>
      </div>

      <div class="stat-card stat-warning" v-loading="overviewLoading">
        <div class="card-bg-pattern"></div>
        <div class="card-icon">💰</div>
        <div class="card-content">
          <div class="card-label">本月薪资支出</div>
          <div class="card-value">¥{{ formatSalary(overviewData.monthly_salary) }}</div>
          <div class="card-trend">
            <span class="trend-neutral">含岗位津贴</span>
          </div>
        </div>
      </div>

      <div class="stat-card stat-danger" v-loading="overviewLoading">
        <div class="card-bg-pattern"></div>
        <div class="card-icon">📋</div>
        <div class="card-content">
          <div class="card-label">待处理事项</div>
          <div class="card-value">{{ overviewData.pending_count || 0 }}</div>
          <div class="card-trend">
            <span v-if="overviewData.pending_count > 0" class="trend-urgent">需要处理</span>
            <span v-else class="trend-good">全部完成</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 人员统计区域 -->
    <section class="employee-section">
      <h2 class="section-title">
        <span class="title-icon">👤</span>
        人员结构分析
      </h2>
      <div class="employee-grid">
        <!-- 岗位分布饼图 -->
        <div class="chart-card position-card" v-loading="employeeLoading">
          <div class="chart-header">
            <h3 class="chart-title">岗位分布</h3>
            <div class="chart-subtitle">各岗位人员占比</div>
          </div>
          <div ref="positionChartRef" class="chart-container position-chart"></div>
          <div class="chart-legend">
            <div
              v-for="(item, index) in employeeData.position_distribution?.labels"
              :key="index"
              class="legend-item"
            >
              <span class="legend-dot" :style="{ backgroundColor: getPositionColor(index) }"></span>
              <span class="legend-label">{{ item }}</span>
              <span class="legend-value">{{ employeeData.position_distribution?.data[index] }}人</span>
            </div>
          </div>
        </div>

        <!-- 持证率统计 -->
        <div class="cert-stats" v-loading="employeeLoading">
          <div class="cert-card cert-health">
            <div class="cert-icon">🏥</div>
            <div class="cert-content">
              <div class="cert-label">健康证持证率</div>
              <div class="cert-value">{{ employeeData.overview?.health_cert_rate || 0 }}%</div>
              <div class="cert-detail">
                已持证 {{ employeeData.certificates?.health_cert_count || 0 }} /
                {{ employeeData.overview?.total_count || 0 }} 人
              </div>
            </div>
            <div class="cert-progress">
              <div
                class="cert-progress-bar"
                :style="{ width: (employeeData.overview?.health_cert_rate || 0) + '%' }"
              ></div>
            </div>
          </div>

          <div class="cert-card cert-chef">
            <div class="cert-icon">👨‍🍳</div>
            <div class="cert-content">
              <div class="cert-label">厨师证持证率</div>
              <div class="cert-value">{{ employeeData.overview?.chef_cert_rate || 0 }}%</div>
              <div class="cert-detail">
                已持证 {{ employeeData.certificates?.chef_cert_count || 0 }} /
                {{ getChefCount() }} 人
              </div>
            </div>
            <div class="cert-progress">
              <div
                class="cert-progress-bar chef-bar"
                :style="{ width: (employeeData.overview?.chef_cert_rate || 0) + '%' }"
              ></div>
            </div>
          </div>

          <!-- 状态分布 -->
          <div class="status-distribution">
            <div class="status-title">在职状态分布</div>
            <div class="status-list">
              <div
                v-for="(item, index) in employeeData.status_distribution?.labels"
                :key="index"
                class="status-item"
              >
                <span class="status-label">{{ item }}</span>
                <div class="status-bar-wrapper">
                  <div
                    class="status-bar"
                    :style="{
                      width: getStatusBarWidth(index),
                      backgroundColor: getStatusColor(index)
                    }"
                  ></div>
                </div>
                <span class="status-value">{{ employeeData.status_distribution?.data[index] }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 考勤统计区域 -->
    <section class="attendance-section">
      <h2 class="section-title">
        <span class="title-icon">⏰</span>
        考勤趋势分析
      </h2>
      <div class="attendance-grid">
        <!-- 出勤率折线图 -->
        <div class="chart-card trend-card" v-loading="attendanceLoading">
          <div class="chart-header">
            <h3 class="chart-title">出勤率趋势</h3>
            <div class="chart-subtitle">最近 7 天出勤情况</div>
          </div>
          <div ref="attendanceTrendChartRef" class="chart-container trend-chart"></div>
        </div>

        <!-- 岗位缺勤排行 -->
        <div class="chart-card ranking-card" v-loading="attendanceLoading">
          <div class="chart-header">
            <h3 class="chart-title">岗位考勤排行</h3>
            <div class="chart-subtitle">迟到/缺卡统计</div>
          </div>
          <div ref="positionRankingChartRef" class="chart-container ranking-chart"></div>
        </div>
      </div>

      <!-- 考勤状态分布 -->
      <div class="chart-card status-dist-card" v-loading="attendanceLoading">
        <div class="chart-header">
          <h3 class="chart-title">考勤状态分布</h3>
          <div class="chart-subtitle">本月考勤情况统计</div>
        </div>
        <div class="status-overview">
          <div
            v-for="(item, index) in attendanceData.status_distribution?.labels"
            :key="index"
            class="status-overview-item"
          >
            <div class="status-icon" :style="{ backgroundColor: getAttendanceStatusColor(item) }">
              {{ getAttendanceStatusIcon(item) }}
            </div>
            <div class="status-info">
              <div class="status-name">{{ item }}</div>
              <div class="status-count">{{ attendanceData.status_distribution?.data[index] }} 次</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 薪资统计区域 -->
    <section class="salary-section">
      <h2 class="section-title">
        <span class="title-icon">💰</span>
        薪资支出分析
      </h2>
      <div class="salary-grid">
        <!-- 月度薪资支出趋势 -->
        <div class="chart-card salary-trend-card" v-loading="salaryLoading">
          <div class="chart-header">
            <h3 class="chart-title">薪资支出趋势</h3>
            <div class="chart-subtitle">最近 12 个月薪资支出</div>
          </div>
          <div ref="salaryTrendChartRef" class="chart-container salary-trend-chart"></div>
        </div>

        <!-- 薪资构成 -->
        <div class="chart-card salary-comp-card" v-loading="salaryLoading">
          <div class="chart-header">
            <h3 class="chart-title">薪资构成分析</h3>
            <div class="chart-subtitle">本月薪资组成占比</div>
          </div>
          <div ref="salaryCompChartRef" class="chart-container salary-comp-chart"></div>
        </div>
      </div>

      <!-- 岗位薪资对比 -->
      <div class="chart-card position-salary-card" v-loading="salaryLoading">
        <div class="chart-header">
          <h3 class="chart-title">岗位薪资对比</h3>
          <div class="chart-subtitle">各岗位平均薪资水平</div>
        </div>
        <div ref="positionSalaryChartRef" class="chart-container position-salary-chart"></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import {
  getEmployeeStatistics,
  getAttendanceStatistics,
  getSalaryStatistics,
  getOverviewStatistics
} from '../../api/analytics'
import { ElMessage } from 'element-plus'

// 数据状态
const overviewLoading = ref(false)
const employeeLoading = ref(false)
const attendanceLoading = ref(false)
const salaryLoading = ref(false)

const overviewData = ref({})
const employeeData = ref({ position_distribution: { labels: [], data: [] }, status_distribution: { labels: [], data: [] } })
const attendanceData = ref({ status_distribution: { labels: [], data: [] } })
const salaryData = ref({})

// 图表实例
const positionChartRef = ref(null)
const attendanceTrendChartRef = ref(null)
const positionRankingChartRef = ref(null)
const salaryTrendChartRef = ref(null)
const salaryCompChartRef = ref(null)
const positionSalaryChartRef = ref(null)

let charts = []

// 岗位颜色配置
const positionColors = ['#FF6B35', '#F7C52D', '#4CAF50', '#2196F3', '#9C27B0', '#795548']

// 获取岗位颜色
const getPositionColor = (index) => {
  return positionColors[index % positionColors.length]
}

// 获取状态颜色
const getStatusColor = (index) => {
  const colors = ['#4CAF50', '#FF6B35', '#9E9E9E']
  return colors[index % colors.length]
}

// 获取考勤状态颜色
const getAttendanceStatusColor = (status) => {
  const colorMap = {
    '正常': '#4CAF50',
    '迟到': '#FF6B35',
    '早退': '#F44336',
    '缺卡': '#9E9E9E',
    '异常': '#E91E63'
  }
  return colorMap[status] || '#999'
}

// 获取考勤状态图标
const getAttendanceStatusIcon = (status) => {
  const iconMap = {
    '正常': '✓',
    '迟到': '⏰',
    '早退': '⇠',
    '缺卡': '?',
    '异常': '!'
  }
  return iconMap[status] || '•'
}

// 获取状态条宽度
const getStatusBarWidth = (index) => {
  if (!employeeData.value.status_distribution?.data) return '0%'
  const total = employeeData.value.status_distribution.data.reduce((a, b) => a + b, 0)
  const value = employeeData.value.status_distribution.data[index]
  return total > 0 ? (value / total * 100) + '%' : '0%'
}

// 获取厨师数量
const getChefCount = () => {
  const positionIndex = employeeData.value.position_distribution?.labels?.indexOf('厨师')
  return positionIndex >= 0 ? employeeData.value.position_distribution.data[positionIndex] || 0 : 0
}

// 格式化薪资
const formatSalary = (salary) => {
  if (!salary) return '0'
  return Number(salary).toLocaleString()
}

// 加载总览数据
const loadOverviewData = async () => {
  overviewLoading.value = true
  try {
    const [overviewResp, salaryResp] = await Promise.all([
      getOverviewStatistics(),
      getSalaryStatistics({ months: 1 })
    ])

    if (overviewResp.code === 200) {
      const data = overviewResp.data

      // 计算本月薪资总额（从最近一个月的薪资数据中获取）
      let monthlySalary = 0
      if (salaryResp.code === 200 && salaryResp.data?.monthly_trend?.length > 0) {
        // 获取最近一个月的薪资总额
        const latestMonth = salaryResp.data.monthly_trend[salaryResp.data.monthly_trend.length - 1]
        monthlySalary = latestMonth.total_salary || 0
      }

      overviewData.value = {
        total_count: data.overview?.total_employees || 0,
        active_count: data.overview?.total_employees || 0,
        attendance_rate: data.today?.attendance_rate || 0,
        late_count: data.today?.late || 0,
        monthly_salary: monthlySalary,
        pending_count: (data.pending?.leaves || 0) + (data.pending?.attendance_corrections || 0) + (data.pending?.salary_generation || 0)
      }
    }
  } catch (error) {
    console.error('加载总览数据失败:', error)
  } finally {
    overviewLoading.value = false
  }
}

// 加载人员统计数据
const loadEmployeeData = async () => {
  employeeLoading.value = true
  try {
    const response = await getEmployeeStatistics()
    if (response.code === 200) {
      employeeData.value = response.data
      initPositionChart()
    }
  } catch (error) {
    console.error('加载人员统计失败:', error)
  } finally {
    employeeLoading.value = false
  }
}

// 加载考勤统计数据
const loadAttendanceData = async () => {
  attendanceLoading.value = true
  try {
    const response = await getAttendanceStatistics({ days: 7 })
    if (response.code === 200) {
      attendanceData.value = response.data
      initAttendanceTrendChart()
      initPositionRankingChart()
    }
  } catch (error) {
    console.error('加载考勤统计失败:', error)
  } finally {
    attendanceLoading.value = false
  }
}

// 加载薪资统计数据
const loadSalaryData = async () => {
  salaryLoading.value = true
  try {
    const response = await getSalaryStatistics({ months: 12 })
    if (response.code === 200) {
      salaryData.value = response.data
      initSalaryTrendChart()
      initSalaryCompChart()
      initPositionSalaryChart()
    }
  } catch (error) {
    console.error('加载薪资统计失败:', error)
  } finally {
    salaryLoading.value = false
  }
}

// 初始化岗位分布饼图
const initPositionChart = () => {
  if (!positionChartRef.value) return

  const chart = echarts.init(positionChartRef.value)
  charts.push(chart)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#FF6B35',
      borderWidth: 1,
      textStyle: { color: '#333' },
      formatter: '{b}: {c}人 ({d}%)'
    },
    legend: { show: false },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: { show: false },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold',
          color: '#333'
        },
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.3)'
        }
      },
      labelLine: { show: false },
      data: (employeeData.value.position_distribution?.labels || []).map((label, index) => ({
        name: label,
        value: employeeData.value.position_distribution?.data?.[index] || 0,
        itemStyle: { color: positionColors[index] }
      }))
    }]
  }

  chart.setOption(option)
}

// 初始化出勤率折线图
const initAttendanceTrendChart = () => {
  if (!attendanceTrendChartRef.value) return

  const chart = echarts.init(attendanceTrendChartRef.value)
  charts.push(chart)

  const dates = (attendanceData.value.daily_trend || []).map(item => {
    const d = new Date(item.date)
    return `${d.getMonth() + 1}/${d.getDate()}`
  })
  const normalData = (attendanceData.value.daily_trend || []).map(item => item.normal || 0)
  const lateData = (attendanceData.value.daily_trend || []).map(item => item.late || 0)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#FF6B35',
      borderWidth: 1,
      textStyle: { color: '#333' }
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
      data: dates,
      axisLine: { lineStyle: { color: '#ddd' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } }
    },
    series: [
      {
        name: '正常',
        type: 'line',
        smooth: true,
        data: normalData,
        itemStyle: { color: '#4CAF50' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(76, 175, 80, 0.3)' },
            { offset: 1, color: 'rgba(76, 175, 80, 0.05)' }
          ])
        }
      },
      {
        name: '迟到',
        type: 'line',
        smooth: true,
        data: lateData,
        itemStyle: { color: '#FF6B35' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 107, 53, 0.3)' },
            { offset: 1, color: 'rgba(255, 107, 53, 0.05)' }
          ])
        }
      }
    ]
  }

  chart.setOption(option)
}

// 初始化岗位考勤排行柱状图
const initPositionRankingChart = () => {
  if (!positionRankingChartRef.value) return

  const chart = echarts.init(positionRankingChartRef.value)
  charts.push(chart)

  const positions = (attendanceData.value.position_stats || []).map(item => item.position)
  const lateData = (attendanceData.value.position_stats || []).map(item => item.late_count || 0)
  const missingData = (attendanceData.value.position_stats || []).map(item => item.missing_count || 0)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#FF6B35',
      borderWidth: 1
    },
    legend: {
      data: ['迟到', '缺卡'],
      top: 0,
      textStyle: { color: '#666' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: positions,
      axisLine: { lineStyle: { color: '#ddd' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#666' },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } }
    },
    series: [
      {
        name: '迟到',
        type: 'bar',
        data: lateData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#FF8C42' },
            { offset: 1, color: '#FF6B35' }
          ]),
          borderRadius: [4, 4, 0, 0]
        }
      },
      {
        name: '缺卡',
        type: 'bar',
        data: missingData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#BDBDBD' },
            { offset: 1, color: '#9E9E9E' }
          ]),
          borderRadius: [4, 4, 0, 0]
        }
      }
    ]
  }

  chart.setOption(option)
}

// 初始化薪资趋势图
const initSalaryTrendChart = () => {
  if (!salaryTrendChartRef.value) return

  const chart = echarts.init(salaryTrendChartRef.value)
  charts.push(chart)

  const months = (salaryData.value.monthly_trend || []).map(item => {
    const [year, month] = item.year_month.split('-')
    return `${month}月`
  })
  const salaryAmounts = (salaryData.value.monthly_trend || []).map(item => item.total_salary)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#FF6B35',
      borderWidth: 1,
      formatter: (params) => {
        const item = salaryData.value.monthly_trend?.[params[0].dataIndex]
        return `${params[0].name}<br/>总支出: ¥${Number(params[0].value).toLocaleString()}<br/>平均: ¥${Number(item?.avg_salary || 0).toLocaleString()}`
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
      data: months,
      axisLine: { lineStyle: { color: '#ddd' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: {
        color: '#666',
        formatter: (value) => '¥' + (value / 10000).toFixed(1) + '万'
      },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } }
    },
    series: [{
      name: '薪资支出',
      type: 'line',
      smooth: true,
      data: salaryAmounts,
      itemStyle: { color: '#FF6B35' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(255, 107, 53, 0.4)' },
          { offset: 1, color: 'rgba(255, 107, 53, 0.05)' }
        ])
      },
      lineStyle: { width: 3 }
    }]
  }

  chart.setOption(option)
}

// 初始化薪资构成饼图
const initSalaryCompChart = () => {
  if (!salaryCompChartRef.value) return

  const chart = echarts.init(salaryCompChartRef.value)
  charts.push(chart)

  const labels = salaryData.value.composition?.distribution?.labels || []
  const data = salaryData.value.composition?.distribution?.data || []
  const colors = ['#FF6B35', '#F7C52D', '#4CAF50', '#F44336']

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#FF6B35',
      borderWidth: 1,
      formatter: (params) => {
        return `${params.name}: ¥${Number(params.value).toLocaleString()} (${params.percent}%)`
      }
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center',
      textStyle: { color: '#666' }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{d}%',
        color: '#666'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.3)'
        }
      },
      data: labels.map((label, index) => ({
        name: label,
        value: data[index],
        itemStyle: { color: colors[index] }
      }))
    }]
  }

  chart.setOption(option)
}

// 初始化岗位薪资对比图
const initPositionSalaryChart = () => {
  if (!positionSalaryChartRef.value) return

  const chart = echarts.init(positionSalaryChartRef.value)
  charts.push(chart)

  const positions = (salaryData.value.position_comparison || []).map(item => item.position)
  const avgSalaries = (salaryData.value.position_comparison || []).map(item => item.avg_salary)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#FF6B35',
      borderWidth: 1,
      formatter: (params) => {
        return `${params[0].name}<br/>平均薪资: ¥${Number(params[0].value).toLocaleString()}`
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
      data: positions,
      axisLine: { lineStyle: { color: '#ddd' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: {
        color: '#666',
        formatter: (value) => '¥' + (value / 1000).toFixed(0) + 'k'
      },
      splitLine: { lineStyle: { color: '#f0f0f0', type: 'dashed' } }
    },
    series: [{
      name: '平均薪资',
      type: 'bar',
      data: avgSalaries,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#FF8C42' },
          { offset: 1, color: '#FF6B35' }
        ]),
        borderRadius: [4, 4, 0, 0]
      },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => '¥' + (params.value / 1000).toFixed(1) + 'k',
        color: '#FF6B35'
      }
    }]
  }

  chart.setOption(option)
}

// 响应式图表
const handleResize = () => {
  charts.forEach(chart => chart.resize())
}

// 组件挂载
onMounted(async () => {
  await Promise.all([
    loadOverviewData(),
    loadEmployeeData(),
    loadAttendanceData(),
    loadSalaryData()
  ])
  window.addEventListener('resize', handleResize)
})

// 组件卸载
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(chart => chart.dispose())
  charts = []
})
</script>

<style scoped>
/* 页面容器 */
.statistics-view {
  min-height: 100vh;
  background: linear-gradient(180deg, #FFF8F0 0%, #FFE8D6 100%);
  padding: 0;
}

/* 页面标题 */
.page-header {
  text-align: center;
  padding: 32px 20px 24px;
  background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
  border-radius: 0 0 24px 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
}

.page-title {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.title-icon {
  font-size: 36px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

.page-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 400;
}

/* 通用区块 */
.section-title {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-left: 12px;
  border-left: 4px solid #FF6B35;
}

/* 顶部统计卡片 */
.top-cards-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
  padding: 0 20px;
}

.stat-card {
  position: relative;
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.12);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(255, 107, 53, 0.25);
}

.card-bg-pattern {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle at top right, rgba(255, 107, 53, 0.1), transparent 70%);
  border-radius: 0 16px 0 100%;
}

.stat-card .card-icon {
  font-size: 42px;
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  flex-shrink: 0;
}

.stat-primary .card-icon {
  background: linear-gradient(135deg, #FFE8D6 0%, #FFD8B8 100%);
}

.stat-success .card-icon {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
}

.stat-warning .card-icon {
  background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
}

.stat-danger .card-icon {
  background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 13px;
  color: #888888;
  margin-bottom: 6px;
}

.card-value {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 28px;
  font-weight: 700;
  color: #333333;
  line-height: 1.2;
  margin-bottom: 6px;
}

.card-trend {
  font-size: 12px;
}

.trend-up,
.trend-good {
  color: #4CAF50;
}

.trend-warning {
  color: #FF6B35;
}

.trend-neutral {
  color: #888888;
}

.trend-urgent {
  color: #F44336;
}

/* 人员统计区域 */
.employee-section,
.attendance-section,
.salary-section {
  padding: 0 20px 32px;
}

.employee-grid,
.attendance-grid,
.salary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 20px;
}

/* 图表卡片 */
.chart-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.12);
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.2);
}

.chart-header {
  margin-bottom: 20px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 4px 0;
}

.chart-subtitle {
  font-size: 12px;
  color: #888888;
  margin: 0;
}

.chart-container {
  width: 100%;
  min-height: 300px;
}

/* 岗位分布图 */
.position-chart {
  height: 280px;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #666;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-label {
  font-weight: 500;
}

.legend-value {
  color: #FF6B35;
  font-weight: 600;
}

/* 持证率统计 */
.cert-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cert-card {
  background: linear-gradient(135deg, #ffffff 0%, #FFF8F0 100%);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.1);
  position: relative;
  overflow: hidden;
}

.cert-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #FF6B35, #F7C52D);
}

.cert-health::before {
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
}

.cert-chef::before {
  background: linear-gradient(90deg, #2196F3, #03A9F4);
}

.cert-icon {
  font-size: 36px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  flex-shrink: 0;
}

.cert-content {
  flex: 1;
}

.cert-label {
  font-size: 13px;
  color: #888888;
  margin-bottom: 4px;
}

.cert-value {
  font-size: 28px;
  font-weight: 700;
  color: #FF6B35;
  line-height: 1.2;
  margin-bottom: 4px;
}

.cert-chef .cert-value {
  color: #2196F3;
}

.cert-detail {
  font-size: 12px;
  color: #666666;
}

.cert-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(0, 0, 0, 0.05);
}

.cert-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #FF6B35, #F7C52D);
  border-radius: 0 0 12px 12px;
  transition: width 0.6s ease;
}

.chef-bar {
  background: linear-gradient(90deg, #2196F3, #03A9F4);
}

/* 状态分布 */
.status-distribution {
  background: linear-gradient(135deg, #ffffff 0%, #FFF8F0 100%);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.1);
}

.status-title {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16px;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-label {
  font-size: 13px;
  color: #666;
  min-width: 60px;
}

.status-bar-wrapper {
  flex: 1;
  height: 20px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  overflow: hidden;
}

.status-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.6s ease;
}

.status-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  min-width: 30px;
  text-align: right;
}

/* 考勤状态概览 */
.status-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.status-overview-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #ffffff 0%, #FFF8F0 100%);
  padding: 16px;
  border-radius: 12px;
}

.status-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
}

.status-info {
  flex: 1;
}

.status-name {
  font-size: 12px;
  color: #888888;
  margin-bottom: 2px;
}

.status-count {
  font-size: 20px;
  font-weight: 700;
  color: #333333;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .employee-grid,
  .attendance-grid,
  .salary-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .top-cards-section {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 24px;
  }

  .title-icon {
    font-size: 28px;
  }

  .status-overview {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
