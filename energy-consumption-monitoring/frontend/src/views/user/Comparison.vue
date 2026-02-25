<template>
  <div class="comparison-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="page-title">
            <span class="title-icon"><icon-ep-trophy /></span>
            能耗对比与排名
          </h1>
          <p class="page-subtitle">了解您的能耗水平，向节能达人学习</p>
        </div>
        <div class="header-rank">
          <div class="rank-badge">
            <span class="rank-label">当前排名</span>
            <span class="rank-number">{{ myRank }}</span>
          </div>
          <div class="rank-trend" :class="rankTrendClass">
            <el-icon><icon-ep-caret-top v-if="rankTrend > 0" /><icon-ep-minus v-else-if="rankTrend === 0" /><icon-ep-caret-bottom v-else /></el-icon>
            <span>{{ rankTrendText }}</span>
          </div>
        </div>
      </div>
      <div class="header-decoration">
        <div class="medal medal-1">🥇</div>
        <div class="medal medal-2">🥈</div>
        <div class="medal medal-3">🥉</div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="stats-bar">
      <div v-for="(stat, index) in comparisonStats" :key="index" class="stat-pill">
        <div class="pill-icon" :style="{ background: stat.color + '15', color: stat.color }">
          <component :is="stat.icon" />
        </div>
        <div class="pill-content">
          <span class="pill-label">{{ stat.label }}</span>
          <span class="pill-value">{{ stat.value }}</span>
        </div>
        <div class="pill-indicator" :class="stat.indicatorClass">
          <el-icon><icon-ep-check v-if="stat.indicatorClass === 'good'" /><icon-ep-close v-else /></el-icon>
          <span>{{ stat.indicator }}</span>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Left Column: Charts -->
      <div class="charts-column">
        <!-- Radar Comparison -->
        <div class="chart-card radar-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-data-analysis /></span>
              能耗维度对比
            </h3>
            <el-select v-model="radarCompareTarget" size="small" style="width: 140px" @change="loadRadarData">
              <el-option label="vs 全校平均" value="school" />
              <el-option label="vs 楼宇平均" value="building" />
              <el-option label="vs 同类用户" value="similar" />
            </el-select>
          </div>
          <div class="card-body">
            <div ref="radarChartRef" class="chart-container"></div>
          </div>
        </div>

        <!-- Trend Comparison -->
        <div class="chart-card trend-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-trend-charts /></span>
              同比环比趋势
            </h3>
          </div>
          <div class="card-body">
            <div ref="trendChartRef" class="chart-container"></div>
          </div>
        </div>

        <!-- History Ranking -->
        <div class="chart-card history-card">
          <div class="card-header">
            <h3 class="card-title">
              <span class="title-icon"><icon-ep-data-line /></span>
              历史排名变化
            </h3>
          </div>
          <div class="card-body">
            <div ref="historyChartRef" class="chart-container"></div>
          </div>
        </div>
      </div>

      <!-- Right Column: Ranking List -->
      <div class="ranking-column">
        <div class="ranking-card">
          <div class="ranking-header">
            <h3 class="ranking-title">
              <span class="title-icon"><icon-ep-trophy /></span>
              节能排行榜
            </h3>
            <el-radio-group v-model="rankingType" size="small" @change="loadRankingData">
              <el-radio-button value="week">本周</el-radio-button>
              <el-radio-button value="month">本月</el-radio-button>
              <el-radio-button value="semester">学期</el-radio-button>
            </el-radio-group>
          </div>

          <!-- Top 3 Podium -->
          <div class="podium-section">
            <div class="podium">
              <div class="podium-place place-2">
                <div class="place-avatar">👤</div>
                <div class="place-name">{{ rankingList[1]?.name || '-' }}</div>
                <div class="place-score">{{ rankingList[1]?.score || '-' }}</div>
                <div class="place-badge">🥈</div>
              </div>
              <div class="podium-place place-1">
                <div class="place-avatar">👑</div>
                <div class="place-name">{{ rankingList[0]?.name || '-' }}</div>
                <div class="place-score">{{ rankingList[0]?.score || '-' }}</div>
                <div class="place-badge">🥇</div>
              </div>
              <div class="podium-place place-3">
                <div class="place-avatar">👤</div>
                <div class="place-name">{{ rankingList[2]?.name || '-' }}</div>
                <div class="place-score">{{ rankingList[2]?.score || '-' }}</div>
                <div class="place-badge">🥉</div>
              </div>
            </div>
          </div>

          <!-- Ranking List -->
          <div class="ranking-list">
            <div
              v-for="(user, index) in rankingList"
              :key="user.id"
              class="ranking-item"
              :class="{ 'is-me': user.is_me, ['top-' + (index + 1)]: index < 3 }"
            >
              <div class="rank-number" :class="`rank-${index + 1}`">
                <span v-if="index < 3" class="medal-icon">
                  {{ index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉' }}
                </span>
                <span v-else>{{ index + 1 }}</span>
              </div>
              <div class="user-info">
                <div class="user-avatar">
                  <img v-if="user.avatar" :src="user.avatar" alt="avatar" />
                  <el-icon v-else><icon-ep-user /></el-icon>
                </div>
                <div class="user-details">
                  <span class="user-name">{{ user.name }}</span>
                  <span class="user-room">{{ user.room }}</span>
                </div>
              </div>
              <div class="user-stats">
                <div class="stat-item">
                  <span class="stat-label">节能指数</span>
                  <span class="stat-value" :class="{ 'is-excellent': user.score >= 90 }">
                    {{ user.score }}
                  </span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">节能量</span>
                  <span class="stat-value saving">{{ user.saving }}</span>
                </div>
              </div>
              <div class="user-trend" :class="user.trend_class">
                <el-icon><icon-ep-caret-top v-if="user.trend > 0" /><icon-ep-minus v-if="user.trend === 0" /><icon-ep-caret-bottom v-if="user.trend < 0" /></el-icon>
                <span>{{ user.trend_text }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Achievement Badges -->
        <div class="achievements-card">
          <div class="achievements-header">
            <h3 class="achievements-title">
              <span class="title-icon">🏆</span>
              我的成就
            </h3>
            <el-badge :value="achievementCount" class="achievement-badge">
              <span class="achievement-count">{{ achievementCount }}/{{ totalAchievements }}</span>
            </el-badge>
          </div>
          <div class="achievements-grid">
            <div
              v-for="achievement in achievements"
              :key="achievement.id"
              class="achievement-item"
              :class="{ unlocked: achievement.unlocked }"
            >
              <div class="achievement-icon">{{ achievement.icon }}</div>
              <div class="achievement-info">
                <span class="achievement-name">{{ achievement.name }}</span>
                <span class="achievement-desc">{{ achievement.desc }}</span>
              </div>
              <el-icon v-if="achievement.unlocked" class="check-icon"><icon-ep-check /></el-icon>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getComparisonData, getRankingData } from '@/api/analysis'

// Chart refs
const radarChartRef = ref(null)
const trendChartRef = ref(null)
const historyChartRef = ref(null)

// Chart instances using shallowRef
const radarChart = shallowRef(null)
const trendChart = shallowRef(null)
const historyChart = shallowRef(null)

// Data
// NOTE: 以下数据从 API 获取:
// - myRank, rankTrend 从排名 API 获取
// - comparisonStats 从对比分析 API 获取 (待后端实现)
// - achievements 成就系统需要后端支持 (暂为静态数据)
const myRank = ref(null) // 从排名 API 获取
const rankTrend = ref(0) // 从排名 API 获取
const radarCompareTarget = ref('school')
const rankingType = ref('week')

// Comparison stats - 从 API 获取对比数据 (待后端实现完整接口)
const comparisonStats = ref([])

// Ranking list
const rankingList = ref([])

// Achievements - 静态数据，待后端实现成就系统API
const achievements = ref([
  { id: 1, name: '节能先锋', desc: '连续7天低于平均', icon: '🌟', unlocked: true },
  { id: 2, name: '节水达人', desc: '用水量低于平均30%', icon: '💧', unlocked: true },
  { id: 3, name: '低碳生活', desc: '碳排放减少50kg', icon: '🌿', unlocked: true },
  { id: 4, name: '月度冠军', desc: '月度排名前10', icon: '🏆', unlocked: false },
  { id: 5, name: '百日坚持', desc: '连续100天记录', icon: '🔥', unlocked: false },
  { id: 6, name: '能源管家', desc: '绑定3个房间', icon: '🏠', unlocked: true },
])

const achievementCount = computed(() => achievements.value.filter(a => a.unlocked).length)
const totalAchievements = computed(() => achievements.value.length)

const rankTrendClass = computed(() => {
  if (rankTrend.value > 0) return 'trend-up'
  if (rankTrend.value < 0) return 'trend-down'
  return 'trend-same'
})

const rankTrendText = computed(() => {
  if (rankTrend.value > 0) return `上升 ${rankTrend.value} 位`
  if (rankTrend.value < 0) return `下降 ${Math.abs(rankTrend.value)} 位`
  return '持平'
})

// ECharts colors
const chartColors = {
  primary: '#f97316',
  secondary: '#eab308',
  water: '#3b82f6',
  gas: '#ef4444',
  green: '#22c55e',
  text: '#64748b',
  grid: '#e2e8f0',
}

// Initialize radar chart
function initRadarChart() {
  if (!radarChartRef.value) return

  radarChart.value = echarts.init(radarChartRef.value)

  const option = {
    grid: { top: 40, bottom: 40, left: 60, right: 60 },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
    },
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text, fontSize: 12 },
      itemGap: 20,
    },
    radar: {
      indicator: [
        { name: '用电', max: 100 },
        { name: '用水', max: 100 },
        { name: '用气', max: 100 },
        { name: '费用', max: 100 },
        { name: '碳排', max: 100 },
        { name: '节能', max: 100 },
      ],
      radius: 65,
      center: ['50%', '50%'],
      axisName: {
        color: chartColors.text,
        fontSize: 12,
        fontWeight: 500,
      },
      splitLine: {
        lineStyle: { color: chartColors.grid, type: 'dashed' },
      },
      splitArea: { show: false },
      axisLine: { lineStyle: { color: chartColors.grid } },
    },
    series: [
      {
        name: '能耗对比',
        type: 'radar',
        data: [
          {
            value: [65, 70, 80, 60, 75, 82],
            name: '我的数据',
            itemStyle: { color: chartColors.primary },
            areaStyle: {
              color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                { offset: 0, color: 'rgba(249, 115, 22, 0.4)' },
                { offset: 1, color: 'rgba(249, 115, 22, 0.1)' },
              ]),
            },
            lineStyle: { width: 2, color: chartColors.primary },
          },
          {
            value: [75, 75, 75, 75, 75, 70],
            name: '全校平均',
            itemStyle: { color: chartColors.water },
            areaStyle: {
              color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                { offset: 0, color: 'rgba(59, 130, 246, 0.2)' },
                { offset: 1, color: 'rgba(59, 130, 246, 0.05)' },
              ]),
            },
            lineStyle: { width: 2, color: chartColors.water, type: 'dashed' },
          },
        ],
      },
    ],
  }

  radarChart.value.setOption(option)
}

// Initialize trend chart
function initTrendChart() {
  if (!trendChartRef.value) return

  trendChart.value = echarts.init(trendChartRef.value)

  const months = ['1月', '2月', '3月', '4月', '5月', '6月']

  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '10%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: {
        type: 'line',
        lineStyle: { color: '#f97316', type: 'dashed' },
      },
    },
    legend: {
      bottom: 0,
      textStyle: { color: chartColors.text, fontSize: 12 },
      itemGap: 20,
    },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: {
        color: chartColors.text,
        fontSize: 11,
        formatter: '{value}%',
      },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
    },
    series: [
      {
        name: '同比',
        type: 'line',
        smooth: true,
        data: [-15, -12, -18, -10, -8, -5],
        lineStyle: { width: 3, color: chartColors.green },
        itemStyle: { color: chartColors.green, borderWidth: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(34, 197, 94, 0.3)' },
            { offset: 1, color: 'rgba(34, 197, 94, 0)' },
          ]),
        },
      },
      {
        name: '环比',
        type: 'line',
        smooth: true,
        data: [5, -3, 8, -5, 2, -8],
        lineStyle: { width: 3, color: chartColors.secondary },
        itemStyle: { color: chartColors.secondary, borderWidth: 2 },
      },
    ],
  }

  trendChart.value.setOption(option)
}

// Initialize history chart
function initHistoryChart() {
  if (!historyChartRef.value) return

  historyChart.value = echarts.init(historyChartRef.value)

  const weeks = ['第1周', '第2周', '第3周', '第4周', '第5周', '第6周']

  const option = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '8%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#f97316',
      borderWidth: 1,
      textStyle: { color: '#fff' },
      axisPointer: { type: 'line' },
    },
    xAxis: {
      type: 'category',
      data: weeks,
      axisLine: { lineStyle: { color: chartColors.grid } },
      axisLabel: { color: chartColors.text, fontSize: 10 },
    },
    yAxis: {
      type: 'value',
      inverse: true,
      axisLine: { show: false },
      axisLabel: { color: chartColors.text, fontSize: 11 },
      splitLine: { lineStyle: { color: chartColors.grid, type: 'dashed' } },
      min: 1,
      max: 30,
    },
    series: [
      {
        name: '排名',
        type: 'line',
        smooth: true,
        data: [25, 22, 18, 15, 12, 15],
        lineStyle: { width: 3, color: chartColors.primary },
        itemStyle: { color: chartColors.primary, borderWidth: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(249, 115, 22, 0.3)' },
            { offset: 1, color: 'rgba(249, 115, 22, 0)' },
          ]),
        },
        markLine: {
          data: [{ yAxis: 15, label: { formatter: '当前排名' } }],
          lineStyle: { color: chartColors.secondary, type: 'dashed' },
        },
      },
    ],
  }

  historyChart.value.setOption(option)
}

// Load radar data
async function loadRadarData() {
  try {
    const response = await getComparisonData({
      type: radarCompareTarget.value,
    })
    if (response.code === 0 && response.data) {
      // Update radar chart with real data
      if (radarChart.value && response.data.series) {
        radarChart.value.setOption({
          series: [{
            data: response.data.series,
          }],
        })
      }
    }
  } catch (error) {
    console.error('Failed to load comparison data:', error)
    ElMessage.error('加载对比数据失败，请稍后重试')
  }
}

// Load ranking data
async function loadRankingData() {
  try {
    const response = await getRankingData({
      type: rankingType.value,
      limit: 20,
    })
    if (response.code === 0 && response.data) {
      rankingList.value = response.data.map((user, index) => ({
        id: user.id || index,
        name: user.name || `用户${index + 1}`,
        room: user.room || '301宿舍',
        score: user.score || Math.floor(70 + Math.random() * 30),
        saving: user.saving || `${Math.floor(Math.random() * 50)} kWh`,
        trend: user.trend || Math.floor(Math.random() * 5) - 2,
        trend_text: user.trend_text || `${Math.floor(Math.random() * 5) - 2} 位`,
        trend_class: user.trend_class || (Math.random() > 0.5 ? 'trend-up' : 'trend-down'),
        avatar: user.avatar || null,
        is_me: user.is_me || false,
      }))

      // Update my rank
      const meIndex = rankingList.value.findIndex(u => u.is_me)
      if (meIndex !== -1) {
        myRank.value = meIndex + 1
      }
    }
  } catch (error) {
    console.error('Failed to load ranking data:', error)
    ElMessage.error('加载排名数据失败，请稍后重试')
    rankingList.value = []
  }
}

// Handle resize
function handleResize() {
  radarChart.value?.resize()
  trendChart.value?.resize()
  historyChart.value?.resize()
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    new Promise(resolve => setTimeout(resolve, 100)).then(() => initRadarChart()),
    new Promise(resolve => setTimeout(resolve, 100)).then(() => initTrendChart()),
    new Promise(resolve => setTimeout(resolve, 100)).then(() => initHistoryChart()),
  ])

  loadRadarData()
  loadRankingData()

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  radarChart.value?.dispose()
  trendChart.value?.dispose()
  historyChart.value?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Orbitron:wght@400;500;600;700&display=swap');

.comparison-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   PAGE HEADER
   ======================================== */
.page-header {
  position: relative;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #dc2626 100%);
  border-radius: 20px;
  padding: 28px 32px;
  color: white;
  overflow: hidden;
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-text .page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

.title-icon {
  display: flex;
  font-size: 24px;
}

.page-subtitle {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.header-rank {
  display: flex;
  align-items: center;
  gap: 16px;
}

.rank-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.rank-label {
  font-size: 11px;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.rank-number {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 36px;
  font-weight: 700;
  line-height: 1;
}

.rank-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
}

.rank-trend.trend-up {
  color: #86efac;
}

.rank-trend.trend-down {
  color: #fca5a5;
}

.rank-trend.trend-same {
  color: #fde047;
}

.header-decoration {
  position: absolute;
  right: 200px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 20px;
  opacity: 0.3;
}

.medal {
  font-size: 56px;
  animation: float 3s ease-in-out infinite;
}

.medal-2 { animation-delay: 0.5s; font-size: 48px; }
.medal-3 { animation-delay: 1s; font-size: 40px; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

/* ========================================
   STATS BAR
   ======================================== */
.stats-bar {
  display: flex;
  gap: 12px;
  animation: fadeInUp 0.5s ease-out 0.1s both;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 18px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.stat-pill:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.pill-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  font-size: 16px;
}

.pill-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.pill-label {
  font-size: 11px;
  color: #64748b;
}

.pill-value {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.pill-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
}

.pill-indicator.good {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.pill-indicator.bad {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* ========================================
   CONTENT GRID
   ======================================== */
.content-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
  animation: fadeInUp 0.5s ease-out 0.2s both;
}

.charts-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ranking-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ========================================
   CHART CARDS
   ======================================== */
.chart-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.title-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 18px;
}

.card-body {
  flex: 1;
  padding: 16px 20px;
  min-height: 280px;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 250px;
}

/* ========================================
   RANKING CARD
   ======================================== */
.ranking-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.ranking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.ranking-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

/* Podium */
.podium-section {
  padding: 24px 20px;
  background: linear-gradient(180deg, #fef9c3 0%, #fff 100%);
  border-bottom: 1px solid #f1f5f9;
}

.podium {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 16px;
  height: 140px;
}

.podium-place {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding: 16px 12px;
  border-radius: 12px;
  position: relative;
  transition: all 0.3s ease;
}

.podium-place:hover {
  transform: translateY(-4px);
}

.place-2 {
  height: 90px;
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
}

.place-1 {
  height: 110px;
  background: linear-gradient(135deg, #fcd34d 0%, #f59e0b 100%);
  z-index: 1;
}

.place-3 {
  height: 70px;
  background: linear-gradient(135deg, #f97316 0%, #b45309 100%);
}

.place-avatar {
  font-size: 28px;
  margin-bottom: 4px;
}

.place-name {
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 2px;
}

.place-score {
  font-size: 14px;
  font-weight: 700;
  color: #1f2937;
}

.place-badge {
  position: absolute;
  top: 8px;
  font-size: 20px;
}

/* Ranking List */
.ranking-list {
  flex: 1;
  overflow-y: auto;
  max-height: 500px;
}

.ranking-item {
  display: grid;
  grid-template-columns: 50px 1fr auto auto;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s ease;
  cursor: pointer;
}

.ranking-item:hover {
  background: #fef7f0;
}

.ranking-item.is-me {
  background: linear-gradient(90deg, rgba(249, 115, 22, 0.1) 0%, transparent 100%);
  border-left: 3px solid #f97316;
}

.ranking-item.top-1 {
  background: linear-gradient(90deg, rgba(251, 191, 36, 0.1) 0%, transparent 100%);
}

.ranking-item.top-2 {
  background: linear-gradient(90deg, rgba(229, 231, 235, 0.3) 0%, transparent 100%);
}

.ranking-item.top-3 {
  background: linear-gradient(90deg, rgba(249, 115, 22, 0.1) 0%, transparent 100%);
}

.rank-number {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: #64748b;
}

.medal-icon {
  font-size: 22px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 10px;
  color: white;
  font-size: 18px;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.user-room {
  font-size: 11px;
  color: #64748b;
}

.user-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.stat-label {
  font-size: 10px;
  color: #64748b;
  text-transform: uppercase;
}

.stat-value {
  font-size: 14px;
  font-weight: 700;
  color: #1f2937;
}

.stat-value.is-excellent {
  color: #22c55e;
}

.stat-value.saving {
  color: #3b82f6;
}

.user-trend {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
}

.user-trend.trend-up {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.user-trend.trend-down {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* ========================================
   ACHIEVEMENTS CARD
   ======================================== */
.achievements-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.achievements-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.achievements-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.achievement-badge :deep(.el-badge__content) {
  background: #22c55e;
  border: 2px solid #fff;
}

.achievement-count {
  font-size: 12px;
  color: #64748b;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1px;
  background: #f1f5f9;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: white;
  transition: all 0.2s ease;
  position: relative;
}

.achievement-item.unlocked {
  background: linear-gradient(135deg, #f0fdf4 0%, #fff 100%);
}

.achievement-icon {
  font-size: 24px;
  filter: grayscale(1);
  opacity: 0.5;
}

.achievement-item.unlocked .achievement-icon {
  filter: grayscale(0);
  opacity: 1;
}

.achievement-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.achievement-name {
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
}

.achievement-desc {
  font-size: 10px;
  color: #64748b;
}

.check-icon {
  color: #22c55e;
  font-size: 16px;
}

/* ========================================
   ANIMATIONS
   ======================================== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .ranking-column {
    order: -1;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .stats-bar {
    flex-wrap: wrap;
  }

  .stat-pill {
    flex: 1 1 calc(50% - 6px);
  }

  .podium {
    height: 120px;
  }

  .ranking-item {
    grid-template-columns: 40px 1fr;
    gap: 8px;
  }

  .user-stats,
  .user-trend {
    display: none;
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-radio-button__inner) {
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: #f97316;
  border-color: #f97316;
  color: white;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 10px;
}
</style>
