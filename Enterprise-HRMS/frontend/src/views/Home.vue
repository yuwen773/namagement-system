<template>
  <div class="dashboard">
    <!-- KPI 卡片区域 -->
    <el-row :gutter="20" class="kpi-row">
      <el-col :span="6">
        <el-card class="kpi-card" shadow="hover">
          <div class="kpi-content">
            <div class="kpi-icon employee-icon">
              <el-icon :size="28"><User /></el-icon>
            </div>
            <div class="kpi-info">
              <div class="kpi-value">{{ stats.total_employees }}</div>
              <div class="kpi-label">在职员工</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card" shadow="hover">
          <div class="kpi-content">
            <div class="kpi-icon hire-icon">
              <el-icon :size="28"><Plus /></el-icon>
            </div>
            <div class="kpi-info">
              <div class="kpi-value">{{ stats.new_hires_this_month }}</div>
              <div class="kpi-label">本月入职</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card" shadow="hover">
          <div class="kpi-content">
            <div class="kpi-icon resign-icon">
              <el-icon :size="28"><Minus /></el-icon>
            </div>
            <div class="kpi-info">
              <div class="kpi-value">{{ stats.resigned_this_month }}</div>
              <div class="kpi-label">本月离职</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="kpi-card" shadow="hover">
          <div class="kpi-content">
            <div class="kpi-icon salary-icon">
              <el-icon :size="28"><Money /></el-icon>
            </div>
            <div class="kpi-info">
              <div class="kpi-value">¥{{ formatNumber(stats.total_salary_this_month) }}</div>
              <div class="kpi-label">本月薪资总额</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <!-- 部门人数分布饼图 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>部门人数分布</span>
            </div>
          </template>
          <div ref="departmentChartRef" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 薪资趋势折线图 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>近6月薪资趋势</span>
            </div>
          </template>
          <div ref="salaryChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 考勤异常柱状图 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>本月考勤异常统计</span>
              <span class="subtitle">按部门分组统计迟到、早退、缺勤次数</span>
            </div>
          </template>
          <div ref="attendanceChartRef" class="chart-container-wide"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { User, Plus, Minus, Money } from '@element-plus/icons-vue'
import { getDashboardStats } from '@/api/dashboard'

// 统计数据
const stats = ref({
  total_employees: 0,
  new_hires_this_month: 0,
  resigned_this_month: 0,
  total_salary_this_month: 0,
  department_distribution: [],
  salary_trend: [],
  attendance_anomalies: []
})

// 图表引用
const departmentChartRef = ref(null)
const salaryChartRef = ref(null)
const attendanceChartRef = ref(null)

// 图表实例
let departmentChart = null
let salaryChart = null
let attendanceChart = null

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
    departmentChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}人 ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: '5%',
        top: 'center'
      },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: departmentData,
        color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#B37FEB', '#36CFCC']
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
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['薪资总额', '人数'],
        bottom: 0
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
        data: months
      },
      yAxis: [{
        type: 'value',
        name: '金额(元)',
        position: 'left',
        axisLabel: {
          formatter: (value) => {
            if (value >= 10000) {
              return (value / 10000) + '万'
            }
            return value
          }
        }
      }, {
        type: 'value',
        name: '人数',
        position: 'right',
        splitLine: {
          show: false
        }
      }],
      series: [{
        name: '薪资总额',
        type: 'line',
        smooth: true,
        data: amounts,
        areaStyle: {
          opacity: 0.3
        },
        itemStyle: {
          color: '#67C23A'
        }
      }, {
        name: '人数',
        type: 'line',
        yAxisIndex: 1,
        smooth: true,
        data: counts,
        itemStyle: {
          color: '#409EFF'
        }
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
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['迟到', '早退', '缺勤'],
        bottom: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'value'
      },
      yAxis: {
        type: 'category',
        data: departments.reverse()
      },
      series: [{
        name: '迟到',
        type: 'bar',
        stack: 'total',
        data: lateData,
        itemStyle: { color: '#E6A23C' }
      }, {
        name: '早退',
        type: 'bar',
        stack: 'total',
        data: earlyData,
        itemStyle: { color: '#F56C6C' }
      }, {
        name: '缺勤',
        type: 'bar',
        stack: 'total',
        data: absentData,
        itemStyle: { color: '#909399' }
      }]
    })
  }
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  departmentChart?.resize()
  salaryChart?.resize()
  attendanceChart?.resize()
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
      attendance_anomalies: data.attendance_anomalies || []
    }

    // 数据更新后重新渲染图表
    initCharts()
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
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.kpi-row {
  margin-bottom: 20px;
}

.kpi-card {
  border-radius: 8px;
}

.kpi-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.kpi-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.employee-icon {
  background: linear-gradient(135deg, #409EFF, #66b1ff);
}

.hire-icon {
  background: linear-gradient(135deg, #67C23A, #85ce61);
}

.resign-icon {
  background: linear-gradient(135deg, #F56C6C, #f89898);
}

.salary-icon {
  background: linear-gradient(135deg, #E6A23C, #f3c06b);
}

.kpi-info {
  flex: 1;
}

.kpi-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.kpi-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 8px;
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header .subtitle {
  font-size: 12px;
  color: #909399;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.chart-container-wide {
  height: 300px;
  width: 100%;
}
</style>
