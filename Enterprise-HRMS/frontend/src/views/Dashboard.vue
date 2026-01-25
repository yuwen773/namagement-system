<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats } from '@/api/dashboard'

// 统计数据
const stats = ref({
  total_employees: 0,
  new_hires_this_month: 0,
  resigned_this_month: 0,
  total_salary_this_month: 0,
  department_distribution: [],
  salary_trend: [],
  attendance_anomalies: [],
  hire_resign_trend: [],
  overtime_by_department: [],
  leave_by_department: [],
  retention_rate: 0
})

// 图表引用
const departmentChartRef = ref(null)
const salaryChartRef = ref(null)
const attendanceChartRef = ref(null)
const hireResignChartRef = ref(null)
const overtimeChartRef = ref(null)
const leaveChartRef = ref(null)

// 图表实例
let departmentChart = null
let salaryChart = null
let attendanceChart = null
let hireResignChart = null
let overtimeChart = null
let leaveChart = null

// 格式化数字
const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

// 初始化图表
const initCharts = () => {
  // 部门分布饼图
  if (departmentChartRef.value) {
    departmentChart = echarts.init(departmentChartRef.value)
    const departmentData = stats.value.department_distribution.map(item => ({
      name: item.department_name,
      value: item.employee_count
    }))

    const colorPalette = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899']

    departmentChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}人 ({d}%)',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16]
      },
      legend: {
        orient: 'vertical',
        right: '5%',
        top: 'middle',
        itemWidth: 12,
        itemHeight: 12,
        itemGap: 12,
        textStyle: { color: '#6b7280', fontSize: 13 }
      },
      series: [{
        type: 'pie',
        radius: ['35%', '60%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 6,
          borderColor: '#ffffff',
          borderWidth: 3
        },
        label: { show: false },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: '500'
          },
          itemStyle: {
            shadowBlur: 20,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.15)'
          }
        },
        data: departmentData,
        color: colorPalette
      }]
    })
  }

  // 薪资趋势折线图
  if (salaryChartRef.value) {
    salaryChart = echarts.init(salaryChartRef.value)
    const months = stats.value.salary_trend.map(item => item.month)
    const amounts = stats.value.salary_trend.map(item => item.total_amount)
    const counts = stats.value.salary_trend.map(item => item.count)

    salaryChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16]
      },
      legend: {
        data: ['薪资总额', '人数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 12 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: months,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#6b7280', fontSize: 12 }
      },
      yAxis: [{
        type: 'value',
        name: '金额(元)',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: {
          color: '#9ca3af',
          fontSize: 12,
          formatter: (value) => {
            if (value >= 10000) return (value / 10000) + '万'
            return value
          }
        },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      }, {
        type: 'value',
        name: '人数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      }],
      series: [{
        name: '薪资总额',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        data: amounts,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.15)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0)' }
            ]
          }
        },
        lineStyle: { width: 3, color: '#10b981' },
        itemStyle: { color: '#10b981', borderColor: '#fff', borderWidth: 2 }
      }, {
        name: '人数',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        yAxisIndex: 1,
        data: counts,
        lineStyle: { width: 3, color: '#4f46e5' },
        itemStyle: { color: '#4f46e5', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 考勤异常柱状图
  if (attendanceChartRef.value) {
    attendanceChart = echarts.init(attendanceChartRef.value)
    const anomalyData = stats.value.attendance_anomalies
    const departments = anomalyData.map(item => item.department)
    const lateData = anomalyData.map(item => item.late)
    const earlyData = anomalyData.map(item => item.early)
    const absentData = anomalyData.map(item => item.absent)

    attendanceChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16]
      },
      legend: {
        data: ['迟到', '早退', '缺勤'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 12 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        splitLine: { lineStyle: { color: '#f3f4f6' } }
      },
      yAxis: {
        type: 'category',
        data: departments,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#4b5563', fontSize: 12 }
      },
      series: [{
        name: '迟到',
        type: 'bar',
        stack: 'total',
        data: lateData,
        barWidth: 24,
        itemStyle: {
          color: '#f59e0b',
          borderRadius: [0, 0, 0, 0]
        }
      }, {
        name: '早退',
        type: 'bar',
        stack: 'total',
        data: earlyData,
        barWidth: 24,
        itemStyle: {
          color: '#ef4444',
          borderRadius: [0, 0, 0, 0]
        }
      }, {
        name: '缺勤',
        type: 'bar',
        stack: 'total',
        data: absentData,
        barWidth: 24,
        itemStyle: {
          color: '#9ca3af',
          borderRadius: [4, 4, 0, 0]
        }
      }]
    })
  }

  // 入离职趋势折线图
  if (hireResignChartRef.value) {
    hireResignChart = echarts.init(hireResignChartRef.value)
    const months = stats.value.hire_resign_trend.map(item => item.month)
    const hireData = stats.value.hire_resign_trend.map(item => item.hire_count)
    const resignData = stats.value.hire_resign_trend.map(item => item.resign_count)

    hireResignChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16]
      },
      legend: {
        data: ['入职人数', '离职人数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 12 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: months,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#6b7280', fontSize: 12 }
      },
      yAxis: {
        type: 'value',
        name: '人数',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      },
      series: [{
        name: '入职人数',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        data: hireData,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.15)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0)' }
            ]
          }
        },
        lineStyle: { width: 3, color: '#10b981' },
        itemStyle: { color: '#10b981', borderColor: '#fff', borderWidth: 2 }
      }, {
        name: '离职人数',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        data: resignData,
        lineStyle: { width: 3, color: '#ef4444' },
        itemStyle: { color: '#ef4444', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 部门加班统计柱状图
  if (overtimeChartRef.value) {
    overtimeChart = echarts.init(overtimeChartRef.value)
    const overtimeData = stats.value.overtime_by_department
    const departments = overtimeData.map(item => item.department)
    const hoursData = overtimeData.map(item => item.overtime_hours)
    const countData = overtimeData.map(item => item.overtime_count)

    overtimeChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16],
        formatter: function(params) {
          const dept = params[0].name
          const hours = params[0].value
          const count = params[1].value
          return `<div style="font-weight: 600; margin-bottom: 8px;">${dept}</div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #f59e0b; border-radius: 2px;"></span>
                    <span>加班时长: <b style="color: #f59e0b;">${hours} 小时</b></span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #4f46e5; border-radius: 2px;"></span>
                    <span>加班次数: <b style="color: #4f46e5;">${count} 次</b></span>
                  </div>`
        }
      },
      legend: {
        data: ['加班时长', '加班次数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 12 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: departments,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#4b5563', fontSize: 12, rotate: 30 }
      },
      yAxis: [{
        type: 'value',
        name: '时长(小时)',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      }, {
        type: 'value',
        name: '次数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      }],
      series: [{
        name: '加班时长',
        type: 'bar',
        data: hoursData,
        barWidth: 24,
        itemStyle: {
          color: '#f59e0b',
          borderRadius: [4, 4, 0, 0]
        },
        label: {
          show: true,
          position: 'top',
          color: '#9ca3af',
          fontSize: 11,
          formatter: (params) => params.value + 'h'
        }
      }, {
        name: '加班次数',
        type: 'line',
        yAxisIndex: 1,
        data: countData,
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { width: 3, color: '#4f46e5' },
        itemStyle: { color: '#4f46e5', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 部门请假统计柱状图
  if (leaveChartRef.value) {
    leaveChart = echarts.init(leaveChartRef.value)
    const leaveData = stats.value.leave_by_department
    const departments = leaveData.map(item => item.department)
    const daysData = leaveData.map(item => item.leave_days)
    const countData = leaveData.map(item => item.leave_count)

    leaveChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16],
        formatter: function(params) {
          const dept = params[0].name
          const days = params[0].value
          const count = params[1].value
          return `<div style="font-weight: 600; margin-bottom: 8px;">${dept}</div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #10b981; border-radius: 2px;"></span>
                    <span>请假天数: <b style="color: #10b981;">${days} 天</b></span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #06b6d4; border-radius: 2px;"></span>
                    <span>请假次数: <b style="color: #06b6d4;">${count} 次</b></span>
                  </div>`
        }
      },
      legend: {
        data: ['请假天数', '请假次数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 12 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '12%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: departments,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#4b5563', fontSize: 12, rotate: 30 }
      },
      yAxis: [{
        type: 'value',
        name: '天数',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      }, {
        type: 'value',
        name: '次数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 12 },
        nameTextStyle: { color: '#9ca3af', fontSize: 12 }
      }],
      series: [{
        name: '请假天数',
        type: 'bar',
        data: daysData,
        barWidth: 24,
        itemStyle: {
          color: '#10b981',
          borderRadius: [4, 4, 0, 0]
        },
        label: {
          show: true,
          position: 'top',
          color: '#9ca3af',
          fontSize: 11,
          formatter: (params) => params.value + 'd'
        }
      }, {
        name: '请假次数',
        type: 'line',
        yAxisIndex: 1,
        data: countData,
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { width: 3, color: '#06b6d4' },
        itemStyle: { color: '#06b6d4', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  departmentChart?.resize()
  salaryChart?.resize()
  attendanceChart?.resize()
  hireResignChart?.resize()
  overtimeChart?.resize()
  leaveChart?.resize()
}

// 获取数据
const fetchData = async () => {
  try {
    const res = await getDashboardStats()
    const data = res.data?.data || {}
    stats.value = {
      total_employees: data.total_employees || 0,
      new_hires_this_month: data.new_hires_this_month || 0,
      resigned_this_month: data.resigned_this_month || 0,
      total_salary_this_month: data.total_salary_this_month || 0,
      department_distribution: data.department_distribution || [],
      salary_trend: data.salary_trend || [],
      attendance_anomalies: data.attendance_anomalies || [],
      hire_resign_trend: data.hire_resign_trend || [],
      overtime_by_department: data.overtime_by_department || [],
      leave_by_department: data.leave_by_department || [],
      retention_rate: data.retention_rate || 0
    }

    // 数据更新后重新渲染图表
    setTimeout(() => {
      initCharts()
    }, 100)
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  departmentChart?.dispose()
  salaryChart?.dispose()
  attendanceChart?.dispose()
  hireResignChart?.dispose()
  overtimeChart?.dispose()
  leaveChart?.dispose()
})
</script>

<template>
  <div class="dashboard-page">
    <!-- KPI 卡片区域 -->
    <div class="kpi-section">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-icon-wrapper employee">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ stats.total_employees }}</div>
            <div class="kpi-label">在职员工</div>
          </div>
          <div class="kpi-accent employee-accent"></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon-wrapper hire">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ stats.new_hires_this_month }}</div>
            <div class="kpi-label">本月入职</div>
          </div>
          <div class="kpi-accent hire-accent"></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon-wrapper resign">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ stats.resigned_this_month }}</div>
            <div class="kpi-label">本月离职</div>
          </div>
          <div class="kpi-accent resign-accent"></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon-wrapper salary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">¥{{ formatNumber(stats.total_salary_this_month) }}</div>
            <div class="kpi-label">本月薪资总额</div>
          </div>
          <div class="kpi-accent salary-accent"></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon-wrapper retention">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ stats.retention_rate }}%</div>
            <div class="kpi-label">员工留存率</div>
          </div>
          <div class="kpi-accent retention-accent"></div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="chart-section">
      <div class="chart-row">
        <div class="chart-card">
          <div class="card-header">
            <div class="header-content">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 2a10 10 0 0 1 10 10"/>
                  <path d="M12 12L16 12"/>
                </svg>
              </span>
              <span class="card-title">部门人数分布</span>
            </div>
          </div>
          <div ref="departmentChartRef" class="chart-container"></div>
        </div>

        <div class="chart-card">
          <div class="card-header">
            <div class="header-content">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
              </span>
              <span class="card-title">近6月薪资趋势</span>
            </div>
          </div>
          <div ref="salaryChartRef" class="chart-container"></div>
        </div>
      </div>

      <div class="chart-row">
        <div class="chart-card full-width">
          <div class="card-header">
            <div class="header-content">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </span>
              <span class="card-title">本月考勤异常统计</span>
            </div>
            <span class="card-subtitle">按部门分组统计迟到、早退、缺勤次数</span>
          </div>
          <div ref="attendanceChartRef" class="chart-container-wide"></div>
        </div>
      </div>

      <!-- 入离职趋势图表 -->
      <div class="chart-row">
        <div class="chart-card full-width">
          <div class="card-header">
            <div class="header-content">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
              </span>
              <span class="card-title">近6月入离职趋势</span>
            </div>
            <span class="card-subtitle">按月份统计入职和离职人数变化</span>
          </div>
          <div ref="hireResignChartRef" class="chart-container-wide"></div>
        </div>
      </div>

      <!-- 加班统计和请假统计图表 -->
      <div class="chart-row">
        <div class="chart-card">
          <div class="card-header">
            <div class="header-content">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </span>
              <span class="card-title">本月部门加班统计</span>
            </div>
            <span class="card-subtitle">按部门统计已审批加班时长和次数</span>
          </div>
          <div ref="overtimeChartRef" class="chart-container"></div>
        </div>

        <div class="chart-card">
          <div class="card-header">
            <div class="header-content">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </span>
              <span class="card-title">本月部门请假统计</span>
            </div>
            <span class="card-subtitle">按部门统计已审批请假天数和次数</span>
          </div>
          <div ref="leaveChartRef" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Dashboard - Modern Corporate Design
   ======================================== */
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* KPI 卡片 */
.kpi-section {
  margin-bottom: 4px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.kpi-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.kpi-accent {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
}

.employee-accent {
  background: linear-gradient(180deg, #4f46e5 0%, #6366f1 100%);
}

.hire-accent {
  background: linear-gradient(180deg, #10b981 0%, #34d399 100%);
}

.resign-accent {
  background: linear-gradient(180deg, #ef4444 0%, #f87171 100%);
}

.salary-accent {
  background: linear-gradient(180deg, #f59e0b 0%, #fbbf24 100%);
}

.retention-accent {
  background: linear-gradient(180deg, #8b5cf6 0%, #a78bfa 100%);
}

.kpi-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
}

.kpi-icon-wrapper::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-lg);
  opacity: 0.15;
}

.kpi-icon-wrapper.employee {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
}

.kpi-icon-wrapper.employee::after {
  background: #4f46e5;
}

.kpi-icon-wrapper.hire {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.05) 100%);
}

.kpi-icon-wrapper.hire::after {
  background: #10b981;
}

.kpi-icon-wrapper.resign {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%);
}

.kpi-icon-wrapper.resign::after {
  background: #ef4444;
}

.kpi-icon-wrapper.salary {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 191, 36, 0.05) 100%);
}

.kpi-icon-wrapper.salary::after {
  background: #f59e0b;
}

.kpi-icon-wrapper.retention {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(167, 139, 250, 0.05) 100%);
}

.kpi-icon-wrapper.retention::after {
  background: #8b5cf6;
}

.kpi-icon-wrapper svg {
  width: 24px;
  height: 24px;
  position: relative;
  z-index: 1;
}

.kpi-icon-wrapper.employee svg {
  color: #4f46e5;
}

.kpi-icon-wrapper.hire svg {
  color: #10b981;
}

.kpi-icon-wrapper.resign svg {
  color: #ef4444;
}

.kpi-icon-wrapper.salary svg {
  color: #f59e0b;
}

.kpi-icon-wrapper.retention svg {
  color: #8b5cf6;
}

.kpi-content {
  flex: 1;
  min-width: 0;
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}

.kpi-label {
  font-size: 13px;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

/* 图表区域 */
.chart-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-row:last-child {
  margin-top: 0;
}

.chart-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 0;
  transition: all var(--transition-base);
}

.chart-card:hover {
  box-shadow: var(--shadow-md);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(to bottom, var(--color-gray-50), var(--color-bg-secondary));
}

.header-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--color-primary-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon svg {
  width: 16px;
  height: 16px;
  color: var(--color-primary);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.card-subtitle {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.chart-container {
  height: 300px;
  width: 100%;
  padding: 16px;
}

.chart-container-wide {
  height: 320px;
  width: 100%;
  padding: 16px;
}

/* 响应式 */
@media (max-width: 1400px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .chart-row {
    grid-template-columns: 1fr;
  }

  .kpi-card {
    padding: 20px;
  }

  .kpi-value {
    font-size: 24px;
  }

  .chart-card .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
