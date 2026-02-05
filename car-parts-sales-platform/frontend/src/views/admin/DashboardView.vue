<template>
  <div class="dashboard-view">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">数据统计</h1>
        <p class="page-subtitle">实时监控平台运营数据</p>
      </div>
      <div class="header-actions">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :clearable="true"
          class="date-picker"
          @change="handleDateChange"
        />
        <el-button type="primary" :icon="Refresh" @click="fetchStatistics" class="refresh-btn">
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- 统计卡片行 -->
    <el-row :gutter="20" class="stats-cards-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card gradient-purple">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 20L20 32L40 12" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ orderStats.totalOrders }}</div>
            <div class="stat-label">总订单数</div>
            <div class="stat-trend" :class="{ positive: orderStats.totalOrdersTrend > 0, negative: orderStats.totalOrdersTrend < 0 }">
              <el-icon><component :is="orderStats.totalOrdersTrend > 0 ? ArrowUp : ArrowDown" /></el-icon>
              <span>{{ Math.abs(orderStats.totalOrdersTrend) }}%</span>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card gradient-orange">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="16" stroke="currentColor" stroke-width="4"/>
                <path d="M24 16V24L30 30" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
              </svg>
            </div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ orderStats.pendingOrders }}</div>
            <div class="stat-label">待处理订单</div>
            <div class="stat-desc">需要关注</div>
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card gradient-green">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 4L4 14V34L24 44L44 34V14L24 4Z" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/>
                <path d="M24 24V44" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
                <path d="M24 24L4 14" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
                <path d="M24 24L44 14" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
              </svg>
            </div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ orderStats.completedOrders }}</div>
            <div class="stat-label">已完成订单</div>
            <div class="stat-trend positive">
              <el-icon><ArrowUp /></el-icon>
              <span>{{ orderStats.completedRate }}%</span>
            </div>
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card gradient-cyan">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="4"/>
                <path d="M24 14V24L32 32" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
                <path d="M30 6L36 10L34 4" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
          <div class="stat-content">
            <div class="stat-value">¥{{ formatAmount(orderStats.totalAmount) }}</div>
            <div class="stat-label">总销售额</div>
            <div class="stat-trend" :class="{ positive: orderStats.amountTrend > 0, negative: orderStats.amountTrend < 0 }">
              <el-icon><component :is="orderStats.amountTrend > 0 ? ArrowUp : ArrowDown" /></el-icon>
              <span>{{ Math.abs(orderStats.amountTrend) }}%</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 销售趋势图 -->
      <el-col :xs="24" :lg="16">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <div class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 3V21H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M19 9L14 14L10 10L7 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span>销售趋势</span>
            </div>
            <el-radio-group v-model="trendPeriod" size="small" class="period-selector" @change="handleTrendPeriodChange">
              <el-radio-button label="day">日</el-radio-button>
              <el-radio-button label="week">周</el-radio-button>
              <el-radio-button label="month">月</el-radio-button>
            </el-radio-group>
          </div>
          <div ref="trendChartRef" class="chart-container"></div>
        </div>
      </el-col>

      <!-- 订单状态分布 -->
      <el-col :xs="24" :lg="8">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <div class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <span>订单状态分布</span>
            </div>
          </div>
          <div ref="statusChartRef" class="chart-container"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 第二行图表 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 热销商品排行 -->
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <div class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                </svg>
              </div>
              <span>热销商品 TOP10</span>
            </div>
            <el-radio-group v-model="topProductType" size="small" class="period-selector" @change="handleTopProductTypeChange">
              <el-radio-button label="sales">按销量</el-radio-button>
              <el-radio-button label="amount">按金额</el-radio-button>
            </el-radio-group>
          </div>
          <div ref="topProductsChartRef" class="chart-container"></div>
        </div>
      </el-col>

      <!-- 优惠券核销统计 -->
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <div class="title-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20 6H4C2.89543 6 2 6.89543 2 8V16C2 17.1046 2.89543 18 4 18H20C21.1046 18 22 17.1046 22 16V8C22 6.89543 21.1046 6 20 6Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M13 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M9 12H11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <span>优惠券核销统计</span>
            </div>
          </div>
          <div ref="couponChartRef" class="chart-container"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import {
  getOrderListApi
} from '@/api/modules/order'
import {
  getProductListApi
} from '@/api/modules/product'
import {
  getCouponListApi,
  getUserCouponsApi
} from '@/api/modules/marketing'

// ECharts 实例
let trendChart = null
let statusChart = null
let topProductsChart = null
let couponChart = null

// DOM 引用
const trendChartRef = ref(null)
const statusChartRef = ref(null)
const topProductsChartRef = ref(null)
const couponChartRef = ref(null)

// 数据筛选
const dateRange = ref([])
const trendPeriod = ref('day')
const topProductType = ref('sales')

// 订单统计数据
const orderStats = reactive({
  totalOrders: 0,
  totalOrdersTrend: 12.5,
  pendingOrders: 0,
  completedOrders: 0,
  completedRate: 0,
  totalAmount: '0.00',
  amountTrend: 8.3
})

// 订单状态映射
const orderStatusMap = {
  pending_payment: { label: '待付款', color: '#f59e0b' },
  pending_shipment: { label: '待发货', color: '#6b7280' },
  shipped: { label: '已发货', color: '#3b82f6' },
  completed: { label: '已完成', color: '#10b981' },
  cancelled: { label: '已取消', color: '#ef4444' },
  return_processing: { label: '退货中', color: '#f97316' }
}

// 格式化金额
const formatAmount = (amount) => {
  const num = parseFloat(amount) || 0
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取订单统计数据
const fetchOrderStats = async () => {
  try {
    let allOrders = []
    let page = 1
    let hasMore = true

    while (hasMore) {
      const response = await getOrderListApi({
        page,
        page_size: 100,
        ordering: '-created_at'
      })

      allOrders = [...allOrders, ...response.results]
      hasMore = response.next !== null
      page++
    }

    let filteredOrders = allOrders
    if (dateRange.value && dateRange.value.length === 2) {
      const [startDate, endDate] = dateRange.value
      const start = new Date(startDate).getTime()
      const end = new Date(endDate).setHours(23, 59, 59, 999)
      filteredOrders = allOrders.filter(order => {
        const orderTime = new Date(order.created_at).getTime()
        return orderTime >= start && orderTime <= end
      })
    }

    orderStats.totalOrders = filteredOrders.length
    orderStats.pendingOrders = filteredOrders.filter(o =>
      o.status === 'pending_payment' || o.status === 'pending_shipment'
    ).length
    orderStats.completedOrders = filteredOrders.filter(o =>
      o.status === 'completed'
    ).length
    orderStats.completedRate = orderStats.totalOrders > 0
      ? Math.round((orderStats.completedOrders / orderStats.totalOrders) * 100)
      : 0

    const totalAmount = filteredOrders
      .filter(o => o.status === 'completed')
      .reduce((sum, order) => sum + parseFloat(order.pay_amount || 0), 0)
    orderStats.totalAmount = totalAmount.toFixed(2)

    return filteredOrders
  } catch (error) {
    ElMessage.error('获取订单统计数据失败')
    return []
  }
}

// 渲染销售趋势图
const renderTrendChart = (orders) => {
  if (!trendChartRef.value) return

  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value)
  }

  const groupedData = groupOrdersByPeriod(orders, trendPeriod.value)
  const dates = Object.keys(groupedData).sort()
  const amounts = dates.map(date => groupedData[date].amount)
  const counts = dates.map(date => groupedData[date].count)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: {
        color: '#1e293b'
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);'
    },
    legend: {
      data: ['销售额', '订单数'],
      textStyle: {
        color: '#64748b'
      },
      top: 0
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
      data: dates,
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: '#e2e8f0'
        }
      },
      axisLabel: {
        color: '#64748b'
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '销售额 (元)',
        position: 'left',
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        splitLine: {
          lineStyle: {
            color: '#f1f5f9',
            type: 'dashed'
          }
        },
        axisLabel: {
          color: '#64748b'
        },
        nameTextStyle: {
          color: '#64748b'
        }
      },
      {
        type: 'value',
        name: '订单数',
        position: 'right',
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: false
        },
        axisLabel: {
          color: '#64748b'
        },
        nameTextStyle: {
          color: '#64748b'
        }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'line',
        smooth: true,
        data: amounts,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#06b6d4' },
            { offset: 1, color: '#3b82f6' }
          ])
        },
        itemStyle: {
          color: '#3b82f6',
          borderColor: '#fff',
          borderWidth: 2
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(6, 182, 212, 0.3)' },
            { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
          ])
        }
      },
      {
        name: '订单数',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        data: counts,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: '#10b981'
        },
        itemStyle: {
          color: '#10b981',
          borderColor: '#fff',
          borderWidth: 2
        }
      }
    ]
  }

  trendChart.setOption(option)
}

// 按时间段分组订单数据
const groupOrdersByPeriod = (orders, period) => {
  const grouped = {}

  orders.forEach(order => {
    const date = new Date(order.created_at)
    let key = ''

    if (period === 'day') {
      key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    } else if (period === 'week') {
      const weekStart = new Date(date)
      weekStart.setDate(date.getDate() - date.getDay())
      key = `${weekStart.getFullYear()}-${String(weekStart.getMonth() + 1).padStart(2, '0')}-${String(weekStart.getDate()).padStart(2, '0')}`
    } else if (period === 'month') {
      key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    }

    if (!grouped[key]) {
      grouped[key] = { amount: 0, count: 0 }
    }

    if (order.status === 'completed') {
      grouped[key].amount += parseFloat(order.pay_amount || 0)
    }
    grouped[key].count++
  })

  return grouped
}

// 渲染订单状态分布图
const renderStatusChart = (orders) => {
  if (!statusChartRef.value) return

  if (!statusChart) {
    statusChart = echarts.init(statusChartRef.value)
  }

  const statusCount = {}
  orders.forEach(order => {
    if (!statusCount[order.status]) {
      statusCount[order.status] = 0
    }
    statusCount[order.status]++
  })

  const data = Object.entries(statusCount).map(([status, count]) => ({
    name: orderStatusMap[status]?.label || status,
    value: count,
    itemStyle: {
      color: orderStatusMap[status]?.color || '#94a3b8'
    }
  }))

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: {
        color: '#1e293b'
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: '#64748b'
      }
    },
    series: [
      {
        name: '订单状态',
        type: 'pie',
        radius: ['45%', '70%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        labelLine: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 600,
            color: '#1e293b'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.1)'
          }
        },
        data
      }
    ]
  }

  statusChart.setOption(option)
}

// 渲染热销商品排行图
const renderTopProductsChart = async () => {
  if (!topProductsChartRef.value) return

  if (!topProductsChart) {
    topProductsChart = echarts.init(topProductsChartRef.value)
  }

  try {
    const ordering = topProductType.value === 'sales' ? '-sales_count' : '-price'
    const response = await getProductListApi({
      ordering,
      page_size: 10,
      status: 'published'
    })

    const products = response.results || []

    const names = products.map(p => p.name.length > 12 ? p.name.substring(0, 12) + '...' : p.name)
    const values = products.map(p =>
      topProductType.value === 'sales' ? p.sales_count || 0 : parseFloat(p.price || 0)
    )

    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        textStyle: {
          color: '#1e293b'
        },
        extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);',
        formatter: (params) => {
          const value = params[0].value
          if (topProductType.value === 'sales') {
            return `${params[0].name}<br/>销量: ${value} 件`
          }
          return `${params[0].name}<br/>价格: ¥${value.toFixed(2)}`
        }
      },
      grid: {
        left: '3%',
        right: '8%',
        bottom: '3%',
        top: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        splitLine: {
          lineStyle: {
            color: '#f1f5f9',
            type: 'dashed'
          }
        },
        axisLabel: {
          color: '#64748b'
        }
      },
      yAxis: {
        type: 'category',
        data: names.reverse(),
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#475569',
          fontSize: 13
        }
      },
      series: [
        {
          name: topProductType.value === 'sales' ? '销量' : '价格',
          type: 'bar',
          data: values.reverse(),
          barWidth: '60%',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#06b6d4' },
              { offset: 0.5, color: '#3b82f6' },
              { offset: 1, color: '#6366f1' }
            ]),
            borderRadius: [0, 8, 8, 0]
          },
          label: {
            show: true,
            position: 'right',
            color: '#475569',
            fontSize: 12,
            formatter: (params) => {
              if (topProductType.value === 'sales') {
                return params.value + ' 件'
              }
              return '¥' + params.value.toFixed(2)
            }
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#0891b2' },
                { offset: 0.5, color: '#2563eb' },
                { offset: 1, color: '#4f46e5' }
              ])
            }
          }
        }
      ]
    }

    topProductsChart.setOption(option)
  } catch (error) {
    ElMessage.error('获取热销商品数据失败')
  }
}

// 渲染优惠券核销统计图
const renderCouponChart = async () => {
  if (!couponChartRef.value) return

  if (!couponChart) {
    couponChart = echarts.init(couponChartRef.value)
  }

  try {
    const couponResponse = await getCouponListApi({ page_size: 100 })
    const userCouponResponse = await getUserCouponsApi({ page_size: 1000 })

    const coupons = couponResponse.results || []
    const userCoupons = userCouponResponse.results || []

    const usedCount = userCoupons.filter(uc => uc.status === 'used').length
    const unusedCount = userCoupons.filter(uc => uc.status === 'unused').length
    const expiredCount = userCoupons.filter(uc => uc.status === 'expired').length

    const data = [
      { name: '已使用', value: usedCount, itemStyle: { color: '#10b981' } },
      { name: '未使用', value: unusedCount, itemStyle: { color: '#3b82f6' } },
      { name: '已过期', value: expiredCount, itemStyle: { color: '#ef4444' } }
    ].filter(d => d.value > 0)

    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        textStyle: {
          color: '#1e293b'
        },
        extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
          color: '#64748b'
        }
      },
      series: [
        {
          name: '优惠券状态',
          type: 'pie',
          radius: ['45%', '70%'],
          center: ['35%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 8,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false
          },
          labelLine: {
            show: false
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 600,
              color: '#1e293b'
            }
          },
          data
        }
      ]
    }

    couponChart.setOption(option)
  } catch (error) {
    ElMessage.error('获取优惠券统计数据失败')
  }
}

// 获取所有统计数据
const fetchStatistics = async () => {
  try {
    const orders = await fetchOrderStats()
    renderTrendChart(orders)
    renderStatusChart(orders)
    await renderTopProductsChart()
    await renderCouponChart()
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

// 日期范围变化
const handleDateChange = () => {
  fetchStatistics()
}

// 趋势周期变化
const handleTrendPeriodChange = () => {
  fetchOrderStats().then(orders => {
    renderTrendChart(orders)
  })
}

// 热销商品类型变化
const handleTopProductTypeChange = () => {
  renderTopProductsChart()
}

// 窗口大小变化时重新渲染图表
const handleResize = () => {
  trendChart?.resize()
  statusChart?.resize()
  topProductsChart?.resize()
  couponChart?.resize()
}

// 初始化
onMounted(async () => {
  await nextTick()
  await fetchStatistics()
  window.addEventListener('resize', handleResize)
})

// 清理
onUnmounted(() => {
  trendChart?.dispose()
  statusChart?.dispose()
  topProductsChart?.dispose()
  couponChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-view {
  --accent-purple: #8b5cf6;
  --accent-orange: #f97316;
  --accent-green: #10b981;
  --accent-cyan: #06b6d4;
  --accent-blue: #3b82f6;

  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   页面标题区
   ======================================== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  flex: 1;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.page-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: #64748b;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-picker {
  width: 280px;
}

.refresh-btn {
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  border: none;
  font-weight: 500;
}

.refresh-btn:hover {
  background: linear-gradient(135deg, #0891b2, #2563eb);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

/* ========================================
   统计卡片
   ======================================== */
.stats-cards-row {
  margin-bottom: 0;
}

.stat-card {
  position: relative;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: inherit;
  opacity: 0.1;
  z-index: 0;
}

.stat-card.gradient-purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
}

.stat-card.gradient-orange {
  background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
}

.stat-card.gradient-green {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
}

.stat-card.gradient-cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon-wrapper {
  position: relative;
  z-index: 1;
}

.stat-icon {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
}

.stat-icon svg {
  width: 32px;
  height: 32px;
}

.stat-content {
  position: relative;
  z-index: 1;
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin-bottom: 4px;
  letter-spacing: -1px;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 6px;
}

.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
}

.stat-trend.positive {
  color: #fff;
}

.stat-trend.negative {
  color: #fecaca;
}

.stat-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.75);
}

/* ========================================
   图表卡片
   ======================================== */
.charts-row {
  margin-bottom: 0;
}

.chart-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
}

.chart-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.title-icon svg {
  width: 18px;
  height: 18px;
}

.chart-title span {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.period-selector :deep(.el-radio-button__inner) {
  border-color: #e2e8f0;
  color: #64748b;
}

.period-selector :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  border-color: transparent;
  color: #fff;
}

.chart-container {
  width: 100%;
  height: 320px;
}

/* ========================================
   响应式设计
   ======================================== */
@media (max-width: 1024px) {
  .page-title {
    font-size: 20px;
  }

  .stat-value {
    font-size: 28px;
  }

  .chart-container {
    height: 280px;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    flex-direction: column;
    width: 100%;
  }

  .date-picker {
    width: 100%;
  }

  .refresh-btn {
    width: 100%;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-icon {
    width: 56px;
    height: 56px;
  }

  .stat-value {
    font-size: 24px;
  }

  .chart-container {
    height: 260px;
  }
}
</style>
