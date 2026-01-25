<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats } from '@/api/dashboard'
import { formatDateTime, formatCurrency } from '@/utils/format'

// 统计数据
const stats = ref({
  total_employees: 0,
  new_hires_this_month: 0,
  resigned_this_month: 0,
  total_salary_this_month: 0,
  avg_salary: 0,
  attendance_anomaly_rate: 0,
  total_overtime_hours: 0,
  retention_rate: 0,
  department_distribution: [],
  salary_trend: [],
  attendance_anomalies: [],
  hire_resign_trend: [],
  overtime_by_department: [],
  leave_by_department: []
})

const loading = ref(true)

// 图表引用
const departmentChartRef = ref(null)
const salaryTrendChartRef = ref(null)
const attendanceChartRef = ref(null)
const hireResignChartRef = ref(null)
const overtimeChartRef = ref(null)
const leaveChartRef = ref(null)
const salaryStructureChartRef = ref(null)
const salaryAvgTrendChartRef = ref(null)

// 图表实例
let departmentChart = null
let salaryTrendChart = null
let attendanceChart = null
let hireResignChart = null
let overtimeChart = null
let leaveChart = null
let salaryStructureChart = null
let salaryAvgTrendChart = null

// 格式化数字
const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

// 计算平均薪资
const avgSalary = computed(() => {
  if (stats.value.total_employees > 0 && stats.value.total_salary_this_month > 0) {
    return Math.round(stats.value.total_salary_this_month / stats.value.total_employees)
  }
  return 0
})

// 计算考勤异常率
const attendanceAnomalyRate = computed(() => {
  const anomalies = stats.value.attendance_anomalies.reduce((sum, item) => sum + item.total, 0)
  const total = stats.value.total_employees * 22 // 假设每月22个工作日
  if (total > 0) {
    return ((anomalies / total) * 100).toFixed(1)
  }
  return 0
})

// 计算总加班时长
const totalOvertimeHours = computed(() => {
  return stats.value.overtime_by_department.reduce((sum, item) => sum + item.overtime_hours, 0).toFixed(1)
})

// 初始化所有图表
const initCharts = () => {
  // 1. 部门人数分布饼图
  if (departmentChartRef.value) {
    departmentChart = echarts.init(departmentChartRef.value)
    const departmentData = stats.value.department_distribution.map(item => ({
      name: item.department_name,
      value: item.employee_count
    }))

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
        orient: 'horizontal',
        bottom: 0,
        itemWidth: 12,
        itemHeight: 12,
        itemGap: 8,
        textStyle: { color: '#6b7280', fontSize: 12 }
      },
      series: [{
        type: 'pie',
        radius: ['35%', '60%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 6,
          borderColor: '#ffffff',
          borderWidth: 2
        },
        label: { show: false },
        emphasis: {
          label: {
            show: true,
            fontSize: 13,
            fontWeight: '500'
          },
          itemStyle: {
            shadowBlur: 15,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.12)'
          }
        },
        data: departmentData,
        color: ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#14b8a6']
      }]
    })
  }

  // 2. 薪资趋势折线图
  if (salaryTrendChartRef.value) {
    salaryTrendChart = echarts.init(salaryTrendChartRef.value)
    const months = stats.value.salary_trend.map(item => item.month)
    const amounts = stats.value.salary_trend.map(item => item.total_amount)
    const counts = stats.value.salary_trend.map(item => item.count)

    salaryTrendChart.setOption({
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
        data: ['薪资总额', '发放人数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 12 }
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
        boundaryGap: false,
        data: months,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#6b7280', fontSize: 11 }
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
          fontSize: 11,
          formatter: (value) => value >= 10000 ? (value / 10000) + '万' : value
        },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      }, {
        type: 'value',
        name: '人数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      }],
      series: [{
        name: '薪资总额',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 6,
        data: amounts,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.12)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0)' }
            ]
          }
        },
        lineStyle: { width: 2.5, color: '#10b981' },
        itemStyle: { color: '#10b981', borderColor: '#fff', borderWidth: 2 }
      }, {
        name: '发放人数',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 6,
        yAxisIndex: 1,
        data: counts,
        lineStyle: { width: 2.5, color: '#4f46e5' },
        itemStyle: { color: '#4f46e5', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 3. 考勤异常统计柱状图
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
        textStyle: { color: '#6b7280', fontSize: 11 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '8%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        splitLine: { lineStyle: { color: '#f3f4f6' } }
      },
      yAxis: {
        type: 'category',
        data: departments,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#4b5563', fontSize: 11 }
      },
      series: [{
        name: '迟到',
        type: 'bar',
        stack: 'total',
        data: lateData,
        barWidth: 20,
        itemStyle: { color: '#f59e0b', borderRadius: [0, 0, 0, 0] }
      }, {
        name: '早退',
        type: 'bar',
        stack: 'total',
        data: earlyData,
        barWidth: 20,
        itemStyle: { color: '#ef4444', borderRadius: [0, 0, 0, 0] }
      }, {
        name: '缺勤',
        type: 'bar',
        stack: 'total',
        data: absentData,
        barWidth: 20,
        itemStyle: { color: '#9ca3af', borderRadius: [4, 4, 0, 0] }
      }]
    })
  }

  // 4. 入离职趋势折线图
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
        textStyle: { color: '#6b7280', fontSize: 11 }
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
        boundaryGap: false,
        data: months,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#6b7280', fontSize: 11 }
      },
      yAxis: {
        type: 'value',
        name: '人数',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      },
      series: [{
        name: '入职人数',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 6,
        data: hireData,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.12)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0)' }
            ]
          }
        },
        lineStyle: { width: 2.5, color: '#10b981' },
        itemStyle: { color: '#10b981', borderColor: '#fff', borderWidth: 2 }
      }, {
        name: '离职人数',
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 6,
        data: resignData,
        lineStyle: { width: 2.5, color: '#ef4444' },
        itemStyle: { color: '#ef4444', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 5. 部门加班统计柱状图
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
        padding: [12, 16]
      },
      legend: {
        data: ['加班时长', '加班次数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 11 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '8%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: departments,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#4b5563', fontSize: 11, rotate: 15 }
      },
      yAxis: [{
        type: 'value',
        name: '时长(h)',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      }, {
        type: 'value',
        name: '次数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      }],
      series: [{
        name: '加班时长',
        type: 'bar',
        data: hoursData,
        barWidth: 20,
        itemStyle: { color: '#f59e0b', borderRadius: [4, 4, 0, 0] },
        label: {
          show: true,
          position: 'top',
          color: '#9ca3af',
          fontSize: 10,
          formatter: (params) => params.value + 'h'
        }
      }, {
        name: '加班次数',
        type: 'line',
        yAxisIndex: 1,
        data: countData,
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { width: 2.5, color: '#4f46e5' },
        itemStyle: { color: '#4f46e5', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 6. 部门请假统计柱状图
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
        padding: [12, 16]
      },
      legend: {
        data: ['请假天数', '请假次数'],
        bottom: 0,
        textStyle: { color: '#6b7280', fontSize: 11 }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '18%',
        top: '8%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: departments,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#4b5563', fontSize: 11, rotate: 15 }
      },
      yAxis: [{
        type: 'value',
        name: '天数',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      }, {
        type: 'value',
        name: '次数',
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 }
      }],
      series: [{
        name: '请假天数',
        type: 'bar',
        data: daysData,
        barWidth: 20,
        itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] },
        label: {
          show: true,
          position: 'top',
          color: '#9ca3af',
          fontSize: 10,
          formatter: (params) => params.value + 'd'
        }
      }, {
        name: '请假次数',
        type: 'line',
        yAxisIndex: 1,
        data: countData,
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { width: 2.5, color: '#06b6d4' },
        itemStyle: { color: '#06b6d4', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }

  // 7. 薪资结构饼图（模拟数据）
  if (salaryStructureChartRef.value) {
    salaryStructureChart = echarts.init(salaryStructureChartRef.value)
    salaryStructureChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16]
      },
      legend: {
        orient: 'horizontal',
        bottom: 0,
        itemWidth: 10,
        itemHeight: 10,
        itemGap: 6,
        textStyle: { color: '#6b7280', fontSize: 11 }
      },
      series: [{
        type: 'pie',
        radius: ['30%', '55%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 4,
          borderColor: '#ffffff',
          borderWidth: 2
        },
        label: { show: false },
        data: [
          { value: 65, name: '基本工资', itemStyle: { color: '#4f46e5' } },
          { value: 15, name: '加班费', itemStyle: { color: '#f59e0b' } },
          { value: 12, name: '绩效奖金', itemStyle: { color: '#10b981' } },
          { value: 5, name: '补贴', itemStyle: { color: '#06b6d4' } },
          { value: 3, name: '其他', itemStyle: { color: '#9ca3af' } }
        ]
      }]
    })
  }

  // 8. 薪资平均趋势（模拟数据）
  if (salaryAvgTrendChartRef.value) {
    salaryAvgTrendChart = echarts.init(salaryAvgTrendChartRef.value)
    const months = stats.value.salary_trend.map(item => item.month)
    const avgData = months.map((_, i) => {
      const total = stats.value.salary_trend[i]?.total_amount || 0
      const count = stats.value.salary_trend[i]?.count || 1
      return Math.round(total / count / 1000)
    })

    salaryAvgTrendChart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e5e5e5',
        borderWidth: 1,
        textStyle: { color: '#1f2937' },
        padding: [12, 16],
        formatter: (params) => {
          const value = params[0].value
          return `${params[0].axisValue}<br/>平均薪资: <b style="color: #8b5cf6;">${value}K</b>`
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '12%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: months,
        axisLine: { lineStyle: { color: '#d4d4d4' } },
        axisLabel: { color: '#6b7280', fontSize: 11 }
      },
      yAxis: {
        type: 'value',
        name: 'K',
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f3f4f6' } },
        axisLabel: { color: '#9ca3af', fontSize: 11 },
        nameTextStyle: { color: '#9ca3af', fontSize: 11 },
        min: (value) => Math.floor(value.min * 0.9)
      },
      series: [{
        type: 'line',
        smooth: 0.3,
        symbol: 'circle',
        symbolSize: 8,
        data: avgData,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(139, 92, 246, 0.2)' },
              { offset: 1, color: 'rgba(139, 92, 246, 0)' }
            ]
          }
        },
        lineStyle: { width: 3, color: '#8b5cf6' },
        itemStyle: { color: '#8b5cf6', borderColor: '#fff', borderWidth: 2 }
      }]
    })
  }
}

// 窗口大小变化时重绘所有图表
const handleResize = () => {
  departmentChart?.resize()
  salaryTrendChart?.resize()
  attendanceChart?.resize()
  hireResignChart?.resize()
  overtimeChart?.resize()
  leaveChart?.resize()
  salaryStructureChart?.resize()
  salaryAvgTrendChart?.resize()
}

// 获取数据
const fetchData = async () => {
  loading.value = true
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

    setTimeout(() => {
      initCharts()
      loading.value = false
    }, 100)
  } catch (error) {
    console.error('获取数据中心数据失败:', error)
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  departmentChart?.dispose()
  salaryTrendChart?.dispose()
  attendanceChart?.dispose()
  hireResignChart?.dispose()
  overtimeChart?.dispose()
  leaveChart?.dispose()
  salaryStructureChart?.dispose()
  salaryAvgTrendChart?.dispose()
})
</script>

<template>
  <div class="data-center-page" v-loading="loading">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-title">
        <h1>数据中心</h1>
        <p class="subtitle">企业运营数据全面分析与可视化</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" plain @click="fetchData">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px; margin-right: 6px;">
            <path d="M21 12a9 9 0 1 1-9-9"/>
            <path d="M21 3v6h-6"/>
          </svg>
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- KPI 卡片区域 - 8个指标 -->
    <div class="kpi-section">
      <div class="kpi-grid">
        <!-- 在职员工 -->
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
          <div class="kpi-trend up">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 15l-6-6-6 6"/>
            </svg>
          </div>
          <div class="kpi-accent employee-accent"></div>
        </div>

        <!-- 本月入职 -->
        <div class="kpi-card">
          <div class="kpi-icon-wrapper hire">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">+{{ stats.new_hires_this_month }}</div>
            <div class="kpi-label">本月入职</div>
          </div>
          <div class="kpi-trend up">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 15l-6-6-6 6"/>
            </svg>
          </div>
          <div class="kpi-accent hire-accent"></div>
        </div>

        <!-- 本月离职 -->
        <div class="kpi-card">
          <div class="kpi-icon-wrapper resign">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">-{{ stats.resigned_this_month }}</div>
            <div class="kpi-label">本月离职</div>
          </div>
          <div class="kpi-trend down">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="kpi-accent resign-accent"></div>
        </div>

        <!-- 本月薪资总额 -->
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

        <!-- 平均薪资 -->
        <div class="kpi-card">
          <div class="kpi-icon-wrapper avg-salary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">¥{{ formatNumber(avgSalary) }}</div>
            <div class="kpi-label">人均薪资</div>
          </div>
          <div class="kpi-trend up">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 15l-6-6-6 6"/>
            </svg>
          </div>
          <div class="kpi-accent avg-salary-accent"></div>
        </div>

        <!-- 员工留存率 -->
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

        <!-- 考勤异常率 -->
        <div class="kpi-card">
          <div class="kpi-icon-wrapper anomaly">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ attendanceAnomalyRate }}%</div>
            <div class="kpi-label">考勤异常率</div>
          </div>
          <div class="kpi-trend down" v-if="parseFloat(attendanceAnomalyRate) < 5">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 15l-6-6-6 6"/>
            </svg>
          </div>
          <div class="kpi-accent anomaly-accent"></div>
        </div>

        <!-- 加班总时长 -->
        <div class="kpi-card">
          <div class="kpi-icon-wrapper overtime">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <div class="kpi-content">
            <div class="kpi-value">{{ totalOvertimeHours }}h</div>
            <div class="kpi-label">本月加班时长</div>
          </div>
          <div class="kpi-accent overtime-accent"></div>
        </div>
      </div>
    </div>

    <!-- 分析区域 -->
    <div class="analysis-section">
      <!-- 考勤分析 -->
      <div class="analysis-block">
        <div class="block-header">
          <div class="block-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <h2>考勤分析</h2>
          </div>
          <span class="block-desc">本月各部门考勤异常统计</span>
        </div>
        <div class="analysis-content">
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">考勤异常分布</span>
            </div>
            <div ref="attendanceChartRef" class="chart-container"></div>
          </div>
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">请假统计</span>
            </div>
            <div ref="leaveChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- 薪资分析 -->
      <div class="analysis-block">
        <div class="block-header">
          <div class="block-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
            <h2>薪资分析</h2>
          </div>
          <span class="block-desc">薪资结构与成本趋势</span>
        </div>
        <div class="analysis-content">
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">近6月薪资趋势</span>
            </div>
            <div ref="salaryTrendChartRef" class="chart-container"></div>
          </div>
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">薪资结构分布</span>
            </div>
            <div ref="salaryStructureChartRef" class="chart-container"></div>
          </div>
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">人均薪资趋势</span>
            </div>
            <div ref="salaryAvgTrendChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- 人事分析 -->
      <div class="analysis-block">
        <div class="block-header">
          <div class="block-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <h2>人事分析</h2>
          </div>
          <span class="block-desc">员工结构与流动趋势</span>
        </div>
        <div class="analysis-content">
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">部门人数分布</span>
            </div>
            <div ref="departmentChartRef" class="chart-container"></div>
          </div>
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">近6月入离职趋势</span>
            </div>
            <div ref="hireResignChartRef" class="chart-container"></div>
          </div>
          <div class="analysis-card">
            <div class="card-header">
              <span class="card-title">加班统计</span>
            </div>
            <div ref="overtimeChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.data-center-page {
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 0 0;
}

.header-title h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
}

.subtitle {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* KPI 卡片 */
.kpi-section {
  margin-bottom: 4px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 16px;
}

.kpi-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.kpi-accent {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
}

.employee-accent { background: linear-gradient(180deg, #4f46e5 0%, #6366f1 100%); }
.hire-accent { background: linear-gradient(180deg, #10b981 0%, #34d399 100%); }
.resign-accent { background: linear-gradient(180deg, #ef4444 0%, #f87171 100%); }
.salary-accent { background: linear-gradient(180deg, #f59e0b 0%, #fbbf24 100%); }
.avg-salary-accent { background: linear-gradient(180deg, #06b6d4 0%, #22d3ee 100%); }
.retention-accent { background: linear-gradient(180deg, #8b5cf6 0%, #a78bfa 100%); }
.anomaly-accent { background: linear-gradient(180deg, #f97316 0%, #fb923c 100%); }
.overtime-accent { background: linear-gradient(180deg, #ec4899 0%, #f472b6 100%); }

.kpi-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-icon-wrapper svg {
  width: 22px;
  height: 22px;
}

.kpi-icon-wrapper.employee { background: rgba(79, 70, 229, 0.1); }
.kpi-icon-wrapper.employee svg { color: #4f46e5; }

.kpi-icon-wrapper.hire { background: rgba(16, 185, 129, 0.1); }
.kpi-icon-wrapper.hire svg { color: #10b981; }

.kpi-icon-wrapper.resign { background: rgba(239, 68, 68, 0.1); }
.kpi-icon-wrapper.resign svg { color: #ef4444; }

.kpi-icon-wrapper.salary { background: rgba(245, 158, 11, 0.1); }
.kpi-icon-wrapper.salary svg { color: #f59e0b; }

.kpi-icon-wrapper.avg-salary { background: rgba(6, 182, 212, 0.1); }
.kpi-icon-wrapper.avg-salary svg { color: #06b6d4; }

.kpi-icon-wrapper.retention { background: rgba(139, 92, 246, 0.1); }
.kpi-icon-wrapper.retention svg { color: #8b5cf6; }

.kpi-icon-wrapper.anomaly { background: rgba(249, 115, 22, 0.1); }
.kpi-icon-wrapper.anomaly svg { color: #f97316; }

.kpi-icon-wrapper.overtime { background: rgba(236, 72, 153, 0.1); }
.kpi-icon-wrapper.overtime svg { color: #ec4899; }

.kpi-content {
  flex: 1;
}

.kpi-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
  margin-bottom: 4px;
}

.kpi-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

.kpi-trend {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-trend svg {
  width: 14px;
  height: 14px;
}

.kpi-trend.up {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.kpi-trend.down {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* 分析区域 */
.analysis-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.analysis-block {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(to bottom, var(--color-gray-50), var(--color-bg-secondary));
}

.block-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.block-title svg {
  width: 22px;
  height: 22px;
  color: var(--color-primary);
}

.block-title h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.block-desc {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.analysis-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 20px;
}

.analysis-card {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.analysis-card .card-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border-light);
  background: var(--color-gray-50);
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.chart-container {
  height: 260px;
  width: 100%;
  padding: 12px;
}

/* 响应式 */
@media (max-width: 1600px) {
  .kpi-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  .analysis-content {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .analysis-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  .block-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
