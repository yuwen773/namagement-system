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
   Dashboard - Refined Corporate Design
   ======================================== */
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 28px;
  position: relative;
}

/* 背景装饰 */
.dashboard-page::before {
  content: '';
  position: absolute;
  top: -100px;
  right: -50px;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* KPI 卡片 */
.kpi-section {
  position: relative;
  z-index: 1;
}

.kpi-section::after {
  content: '';
  position: absolute;
  bottom: -14px;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--color-border-light) 0%, transparent 100%);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.kpi-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease forwards;
}

.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.kpi-card:nth-child(3) { animation-delay: 0.3s; }
.kpi-card:nth-child(4) { animation-delay: 0.4s; }
.kpi-card:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.kpi-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.12);
  border-color: var(--color-primary);
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.kpi-card:hover::before {
  opacity: 1;
}

.kpi-accent {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.employee-accent {
  background: linear-gradient(90deg, #4f46e5 0%, #818cf8 50%, #4f46e5 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.hire-accent {
  background: linear-gradient(90deg, #10b981 0%, #34d399 50%, #10b981 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
  animation-delay: 0.5s;
}

.resign-accent {
  background: linear-gradient(90deg, #ef4444 0%, #f87171 50%, #ef4444 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
  animation-delay: 1s;
}

.salary-accent {
  background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 50%, #f59e0b 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
  animation-delay: 1.5s;
}

.retention-accent {
  background: linear-gradient(90deg, #8b5cf6 0%, #a78bfa 50%, #8b5cf6 100%);
  background-size: 200% 100%;
  animation: shimmer 3s ease infinite;
  animation-delay: 2s;
}

.kpi-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.kpi-icon-wrapper::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: calc(var(--radius-lg) + 2px);
  padding: 2px;
  background: linear-gradient(135deg, currentColor, transparent 50%, currentColor);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.kpi-card:hover .kpi-icon-wrapper::before {
  opacity: 0.3;
}

.kpi-icon-wrapper svg {
  width: 24px;
  height: 24px;
  position: relative;
  z-index: 1;
}

.kpi-icon-wrapper.employee {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.12) 0%, rgba(79, 70, 229, 0.04) 100%);
  color: #4f46e5;
}

.kpi-icon-wrapper.hire {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.04) 100%);
  color: #10b981;
}

.kpi-icon-wrapper.resign {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(239, 68, 68, 0.04) 100%);
  color: #ef4444;
}

.kpi-icon-wrapper.salary {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(245, 158, 11, 0.04) 100%);
  color: #f59e0b;
}

.kpi-icon-wrapper.retention {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(139, 92, 246, 0.04) 100%);
  color: #8b5cf6;
}

.kpi-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.1;
  letter-spacing: -1px;
  font-feature-settings: 'tnum' on, 'lnum' on;
}

.kpi-label {
  font-size: 13px;
  color: var(--color-text-tertiary);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.kpi-label::before {
  content: '';
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.5;
}

/* 图表区域 */
.chart-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-row:last-child {
  margin-top: 0;
}

.chart-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  padding: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateY(30px);
  animation: fadeInUp 0.8s ease forwards;
  animation-delay: 0.6s;
  overflow: hidden;
}

.chart-card.full-width {
  grid-column: 1 / -1;
  animation-delay: 0.7s;
}

.chart-card:hover {
  box-shadow: 0 8px 32px -8px rgba(0, 0, 0, 0.1);
  border-color: var(--color-primary-light);
}

.chart-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(135deg, var(--color-gray-50) 0%, var(--color-bg-secondary) 100%);
  position: relative;
}

.chart-card .card-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, var(--color-primary) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.chart-card:hover .card-header::after {
  opacity: 0.3;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
}

.card-icon svg {
  width: 18px;
  height: 18px;
  color: white;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.3px;
}

.card-subtitle {
  font-size: 12px;
  color: var(--color-text-tertiary);
  font-weight: 400;
}

.chart-container {
  height: 280px;
  width: 100%;
  padding: 12px 16px;
}

.chart-container-wide {
  height: 300px;
  width: 100%;
  padding: 12px 16px;
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

  .chart-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .kpi-card {
    padding: 20px;
    flex-direction: row;
    align-items: center;
  }

  .kpi-value {
    font-size: 26px;
  }

  .chart-card .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .chart-container,
  .chart-container-wide {
    height: 260px;
  }
}
</style>
