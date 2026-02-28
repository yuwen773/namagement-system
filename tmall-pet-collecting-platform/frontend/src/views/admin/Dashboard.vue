<script setup>
import { ref, onMounted, computed } from 'vue'
import { statisticsApi, crawlerApi } from '@/api'
import ChartContainer from '@/components/common/ChartContainer.vue'
import { TrendCharts, ShoppingCart, ShoppingBag, Wallet, DataAnalysis, Loading } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const loading = ref(true)
const overview = ref({
  total_products: 0,
  total_shops: 0,
  total_brands: 0,
  avg_price: 0
})

const priceDistribution = ref([])
const shopRanking = ref([])
const petTypeDistribution = ref([])
const systemStatus = ref({
  database: 'normal',
  crawler: 'idle',
  activeTasks: 0,
  lastCrawlTime: null
})

const fetchOverview = async () => {
  try {
    const res = await statisticsApi.getOverview()
    if (res.code === 0) {
      overview.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch overview:', error)
  }
}

const fetchPriceDistribution = async () => {
  try {
    const res = await statisticsApi.getPriceDistribution()
    if (res.code === 0) {
      priceDistribution.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch price distribution:', error)
  }
}

const fetchShopRanking = async () => {
  try {
    const res = await statisticsApi.getShopRanking({ limit: 10 })
    if (res.code === 0) {
      shopRanking.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch shop ranking:', error)
  }
}

const fetchSystemStatus = async () => {
  try {
    const res = await crawlerApi.getSystemHealth()
    if (res.code === 0) {
      systemStatus.value = {
        database: res.data.database,
        crawler: res.data.crawler,
        activeTasks: res.data.active_tasks,
        lastCrawlTime: res.data.last_crawl_time
      }
    }
  } catch (error) {
    console.error('Failed to fetch system status:', error)
  }
}

const fetchPetTypeDistribution = async () => {
  try {
    const res = await statisticsApi.getPetTypeDistribution()
    if (res.code === 0) {
      petTypeDistribution.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch pet type distribution:', error)
  }
}

const priceChartOption = computed(() => {
  // 如果没有数据，返回空配置
  if (!priceDistribution.value || priceDistribution.value.length === 0) {
    return null
  }

  const colors = ['#FF6B35', '#FFD700', '#7B2CBF', '#06FFA5']
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 15, 26, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' },
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: 'rgba(255,255,255,0.7)', fontSize: 13 }
    },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 12,
        borderColor: '#0f0f1a',
        borderWidth: 3
      },
      label: {
        show: true,
        color: 'rgba(255,255,255,0.8)',
        fontSize: 13,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold' },
        itemStyle: {
          shadowBlur: 20,
          shadowOffsetX: 0,
          shadowColor: 'rgba(255, 107, 53, 0.5)'
        }
      },
      labelLine: {
        lineStyle: { color: 'rgba(255,255,255,0.3)' },
        smooth: 0.3
      },
      data: priceDistribution.value.map((item, index) => ({
        value: item.count,
        name: item.range,
        itemStyle: { color: colors[index] }
      }))
    }]
  }
})

const shopChartOption = computed(() => {
  // 如果没有数据，返回空配置
  if (!shopRanking.value || shopRanking.value.length === 0) {
    return null
  }

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(15, 15, 26, 0.95)',
      borderColor: 'rgba(255, 107, 53, 0.3)',
      textStyle: { color: '#fff' }
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
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: 'rgba(255,255,255,0.5)' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    yAxis: {
      type: 'category',
      data: shopRanking.value.map(item => item.shop),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 12,
        width: 120,
        overflow: 'truncate'
      }
    },
    series: [{
      type: 'bar',
      data: shopRanking.value.map((item, index) => ({
        value: item.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#7B2CBF' },
            { offset: 0.5, color: '#FF6B35' },
            { offset: 1, color: '#FFD700' }
          ]),
          borderRadius: [0, 8, 8, 0]
        }
      })),
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        color: 'rgba(255,255,255,0.8)',
        fontSize: 12
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 15,
          shadowColor: 'rgba(255, 107, 53, 0.4)'
        }
      }
    }]
  }
})

const petTypeChartOption = computed(() => {
  if (!petTypeDistribution.value || petTypeDistribution.value.length === 0) {
    return null
  }

  return {
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', right: '5%', top: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['40%', '50%'],
      data: petTypeDistribution.value.map(item => ({
        name: item.label,
        value: item.count
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
})

const loadData = async () => {
  loading.value = true
  await Promise.all([
    fetchOverview(),
    fetchPriceDistribution(),
    fetchShopRanking(),
    fetchSystemStatus(),
    fetchPetTypeDistribution()
  ])
  loading.value = false
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2
  }).format(price)
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="dashboard-container">
    <!-- 统计卡片区域 -->
    <div class="stats-grid">
      <div class="stat-card" style="--card-color: #FF6B35; --card-glow: rgba(255, 107, 53, 0.3);">
        <div class="stat-icon">
          <ShoppingBag class="icon" />
        </div>
        <div class="stat-content">
          <p class="stat-label">商品总数</p>
          <p class="stat-value">{{ formatNumber(overview.total_products) }}</p>
        </div>
        <div class="stat-bg-icon">📦</div>
      </div>

      <div class="stat-card" style="--card-color: #7B2CBF; --card-glow: rgba(123, 44, 191, 0.3);">
        <div class="stat-icon">
          <ShoppingCart class="icon" />
        </div>
        <div class="stat-content">
          <p class="stat-label">店铺数量</p>
          <p class="stat-value">{{ formatNumber(overview.total_shops) }}</p>
        </div>
        <div class="stat-bg-icon">🏪</div>
      </div>

      <div class="stat-card" style="--card-color: #FFD700; --card-glow: rgba(255, 215, 0, 0.3);">
        <div class="stat-icon">
          <TrendCharts class="icon" />
        </div>
        <div class="stat-content">
          <p class="stat-label">品牌数量</p>
          <p class="stat-value">{{ formatNumber(overview.total_brands) }}</p>
        </div>
        <div class="stat-bg-icon">🎯</div>
      </div>

      <div class="stat-card" style="--card-color: #06FFA5; --card-glow: rgba(6, 255, 165, 0.3);">
        <div class="stat-icon">
          <Wallet class="icon" />
        </div>
        <div class="stat-content">
          <p class="stat-label">平均价格</p>
          <p class="stat-value">{{ formatPrice(overview.price?.avg || 0) }}</p>
        </div>
        <div class="stat-bg-icon">💰</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-row">
      <!-- 价格分布图 -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title">
            <DataAnalysis class="title-icon" />
            <h3>价格区间分布</h3>
          </div>
          <div class="chart-badge">分布分析</div>
        </div>
        <div class="chart-body">
          <ChartContainer
            v-if="!loading && priceDistribution.length > 0"
            :option="priceChartOption"
            height="320px"
          />
          <div v-else class="chart-placeholder">
            <Loading class="loading-icon" />
            <p>加载价格分布数据...</p>
          </div>
        </div>
      </div>

      <!-- 店铺排行榜 -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title">
            <ShoppingCart class="title-icon" />
            <h3>店铺商品排行 TOP 10</h3>
          </div>
          <div class="chart-badge">数据洞察</div>
        </div>
        <div class="chart-body">
          <ChartContainer
            v-if="!loading && shopRanking.length > 0"
            :option="shopChartOption"
            height="320px"
          />
          <div v-else class="chart-placeholder">
            <Loading class="loading-icon" />
            <p>加载店铺排行数据...</p>
          </div>
        </div>
      </div>

      <!-- 宠物类型分布图 -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title">
            <DataAnalysis class="title-icon" />
            <h3>宠物类型分布</h3>
          </div>
          <div class="chart-badge">类型分析</div>
        </div>
        <div class="chart-body">
          <ChartContainer
            v-if="!loading && petTypeDistribution.length > 0"
            :option="petTypeChartOption"
            height="320px"
          />
          <div v-else class="chart-placeholder">
            <Loading class="loading-icon" />
            <p>加载宠物类型数据...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 系统状态 -->
    <div class="system-status-card">
      <div class="status-header">
        <div class="status-title">
          <div class="status-dot" :class="{ active: systemStatus.crawler === 'running' }"></div>
          <h3>系统运行状态</h3>
        </div>
        <div class="status-info">
          <span class="status-item">
            <span class="label">活跃任务:</span>
            <span class="value">{{ systemStatus.activeTasks }}</span>
          </span>
          <span class="status-item">
            <span class="label">上次采集:</span>
            <span class="value">{{ systemStatus.lastCrawlTime || '暂无记录' }}</span>
          </span>
        </div>
      </div>
      <div class="status-metrics">
        <div class="metric">
          <span class="metric-label">数据库连接</span>
          <span class="metric-status" :class="systemStatus.database === 'normal' ? 'online' : 'error'">
            {{ systemStatus.database === 'normal' ? '正常' : '异常' }}
          </span>
        </div>
        <div class="metric">
          <span class="metric-label">爬虫服务</span>
          <span class="metric-status" :class="systemStatus.crawler === 'running' ? 'online' : 'idle'">
            {{ systemStatus.crawler === 'running' ? '运行中' : '空闲' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-card {
  position: relative;
  padding: 24px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--card-color), transparent);
  opacity: 0.8;
}

.stat-card:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: var(--card-color);
  box-shadow: 0 20px 40px var(--card-glow),
              0 0 60px var(--card-glow);
}

.stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--card-color), var(--card-glow));
  border-radius: 14px;
  margin-bottom: 16px;
}

.stat-icon .icon {
  width: 28px;
  height: 28px;
  color: white;
}

.stat-content {
  position: relative;
  z-index: 1;
}

.stat-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 500;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
}

.stat-value {
  font-family: 'Orbitron', monospace;
  font-size: 28px;
  font-weight: 700;
  color: var(--card-color);
  margin: 0;
  line-height: 1;
  text-shadow: 0 0 30px var(--card-glow);
}

.stat-bg-icon {
  position: absolute;
  right: -10px;
  bottom: -10px;
  font-size: 80px;
  opacity: 0.08;
  filter: blur(2px);
  pointer-events: none;
}

/* 图表区域 */
.charts-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.chart-card {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.01) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.chart-card:hover {
  border-color: rgba(255, 107, 53, 0.2);
  box-shadow: 0 10px 40px rgba(255, 107, 53, 0.1);
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chart-title .title-icon {
  width: 20px;
  height: 20px;
  color: #FF6B35;
}

.chart-title h3 {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.chart-badge {
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(123, 44, 191, 0.2));
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: #FF6B35;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.chart-body {
  padding: 24px;
  min-height: 320px;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 320px;
  color: rgba(255, 255, 255, 0.4);
}

.chart-placeholder .loading-icon {
  width: 40px;
  height: 40px;
  color: #FF6B35;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.chart-placeholder p {
  font-size: 14px;
  margin: 0;
}

/* 系统状态卡片 */
.system-status-card {
  background: linear-gradient(135deg,
    rgba(123, 44, 191, 0.1) 0%,
    rgba(255, 107, 53, 0.05) 100%);
  border: 1px solid rgba(123, 44, 191, 0.2);
  border-radius: 24px;
  padding: 24px;
  position: relative;
  overflow: hidden;
}

.system-status-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: radial-gradient(ellipse at top right,
    rgba(255, 107, 53, 0.1) 0%,
    transparent 60%);
  pointer-events: none;
}

.status-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.status-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  position: relative;
}

.status-dot::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid rgba(255, 107, 53, 0.3);
  animation: pulse 2s ease-in-out infinite;
}

.status-dot.active {
  background: #06FFA5;
  box-shadow: 0 0 20px #06FFA5;
}

.status-dot.active::after {
  border-color: #06FFA5;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.5; }
}

.status-title h3 {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.status-info {
  display: flex;
  gap: 24px;
}

.status-item {
  display: flex;
  gap: 8px;
  font-size: 13px;
}

.status-item .label {
  color: rgba(255, 255, 255, 0.5);
}

.status-item .value {
  color: #FF6B35;
  font-weight: 600;
  font-family: 'Orbitron', monospace;
}

.status-metrics {
  display: flex;
  gap: 16px;
  position: relative;
  z-index: 1;
}

.metric {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.metric-status {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}

.metric-status.online {
  background: rgba(6, 255, 165, 0.15);
  color: #06FFA5;
  border: 1px solid rgba(6, 255, 165, 0.3);
}

.metric-status.idle {
  background: rgba(255, 215, 0, 0.15);
  color: #FFD700;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.metric-status.error {
  background: rgba(255, 59, 48, 0.15);
  color: #FF3B30;
  border: 1px solid rgba(255, 59, 48, 0.3);
}

/* 响应式 */
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .status-info {
    flex-direction: column;
    gap: 8px;
  }

  .status-metrics {
    flex-direction: column;
  }
}
</style>
