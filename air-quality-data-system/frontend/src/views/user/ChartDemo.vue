<template>
  <div class="chart-demo-page">
    <h1 class="page-title">ECharts 组件库演示</h1>

    <!-- Gauge Charts -->
    <div class="demo-section">
      <h2 class="section-title">仪表盘组件（AQI 等级）</h2>
      <div class="gauge-row">
        <div class="gauge-item">
          <GaugeChart :value="35" title="北京" :size="'small'" />
        </div>
        <div class="gauge-item">
          <GaugeChart :value="85" title="上海" :size="'medium'" />
        </div>
        <div class="gauge-item">
          <GaugeChart :value="145" title="广州" :size="'medium'" />
        </div>
        <div class="gauge-item">
          <GaugeChart :value="280" title="成都" :size="'large'" />
        </div>
      </div>
    </div>

    <!-- Line Chart -->
    <div class="demo-section">
      <h2 class="section-title">折线图（24 小时 AQI 趋势）</h2>
      <LineChart
        :data="lineData"
        :x-axis="lineXAxis"
        :legend="['北京', '上海', '广州']"
        :area-style="true"
        :show-data-zoom="true"
        unit="AQI"
      />
    </div>

    <!-- Bar Chart -->
    <div class="demo-section">
      <h2 class="section-title">柱状图（城市 AQI 对比）</h2>
      <BarChart
        :data="barData"
        :x-axis="barXAxis"
        :legend="['AQI 指数', 'PM2.5']"
        :show-values="true"
        unit=""
      />
    </div>

    <!-- Pie Chart -->
    <div class="demo-section">
      <h2 class="section-title">饼图（AQI 等级分布）</h2>
      <PieChart
        :data="pieData"
        :donut="true"
        :show-percentage="true"
      />
    </div>

    <!-- Scatter Chart -->
    <div class="demo-section">
      <h2 class="section-title">散点图（PM2.5 vs PM10 相关性）</h2>
      <ScatterChart
        :data="scatterData"
        :x-axis-name="'PM2.5'"
        :y-axis-name="'PM10'"
        :x-axis-unit="'μg/m³'"
        :y-axis-unit="'μg/m³'"
        :show-labels="false"
      />
    </div>

    <!-- Data Table -->
    <div class="demo-section">
      <h2 class="section-title">数据表格</h2>
      <DataTable
        :data="tableData"
        :columns="tableColumns"
        :pagination="true"
        :total="50"
        :page-size="10"
        :selectable="true"
        :show-index="true"
        theme="dark"
      >
        <template #actions="{ row }">
          <el-button size="small" type="primary">查看</el-button>
          <el-button size="small" type="warning">编辑</el-button>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  GaugeChart,
  DataTable
} from '@/components/charts'

// Line chart data
const lineXAxis = ref(['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'])
const lineData = ref([
  { name: '北京', values: [45, 52, 78, 95, 88, 65, 50] },
  { name: '上海', values: [35, 42, 55, 68, 72, 58, 40] },
  { name: '广州', values: [55, 65, 85, 110, 125, 98, 70] }
])

// Bar chart data
const barXAxis = ref(['北京', '上海', '广州', '深圳', '成都', '杭州', '武汉', '西安'])
const barData = ref([
  { name: 'AQI 指数', values: [78, 65, 95, 55, 110, 72, 88, 125] },
  { name: 'PM2.5', values: [45, 38, 55, 32, 65, 42, 52, 75] }
])

// Pie chart data
const pieData = ref([
  { name: '优 (0-50)', value: 156 },
  { name: '良 (51-100)', value: 198 },
  { name: '轻度污染 (101-150)', value: 72 },
  { name: '中度污染 (151-200)', value: 28 },
  { name: '重度污染 (201-300)', value: 12 },
  { name: '严重污染 (301-500)', value: 4 }
])

// Scatter chart data (PM2.5 vs PM10 correlation)
const scatterData = ref([
  [25, 45], [35, 62], [45, 78], [55, 95], [65, 110],
  [75, 125], [85, 142], [95, 158], [105, 172], [115, 188],
  [30, 52], [40, 68], [50, 85], [60, 98], [70, 115],
  [80, 130], [90, 148], [100, 165], [110, 180], [120, 195],
  [28, 48], [38, 65], [48, 80], [58, 96], [68, 112],
  [78, 128], [88, 145], [98, 162], [108, 178], [118, 192]
])

// Table data
const tableColumns = ref([
  { prop: 'city', label: '城市', width: 120 },
  { prop: 'aqi', label: 'AQI', width: 100, align: 'center' },
  { prop: 'level', label: '等级', width: 120 },
  { prop: 'pm25', label: 'PM2.5', width: 100, align: 'right' },
  { prop: 'pm10', label: 'PM10', width: 100, align: 'right' },
  { prop: 'so2', label: 'SO₂', width: 100, align: 'right' },
  { prop: 'no2', label: 'NO₂', width: 100, align: 'right' },
  { prop: 'time', label: '监测时间', minWidth: 180 }
])

const tableData = ref([
  { city: '北京', aqi: 78, level: '良', pm25: 45, pm10: 85, so2: 12, no2: 38, time: '2026-02-15 14:00' },
  { city: '上海', aqi: 65, level: '良', pm25: 38, pm10: 72, so2: 8, no2: 42, time: '2026-02-15 14:00' },
  { city: '广州', aqi: 95, level: '良', pm25: 55, pm10: 98, so2: 15, no2: 48, time: '2026-02-15 14:00' },
  { city: '深圳', aqi: 55, level: '良', pm25: 32, pm10: 65, so2: 6, no2: 35, time: '2026-02-15 14:00' },
  { city: '成都', aqi: 110, level: '轻度污染', pm25: 65, pm10: 125, so2: 18, no2: 52, time: '2026-02-15 14:00' },
  { city: '杭州', aqi: 72, level: '良', pm25: 42, pm10: 78, so2: 10, no2: 40, time: '2026-02-15 14:00' },
  { city: '武汉', aqi: 88, level: '良', pm25: 52, pm10: 95, so2: 14, no2: 45, time: '2026-02-15 14:00' },
  { city: '西安', aqi: 125, level: '轻度污染', pm25: 75, pm10: 145, so2: 22, no2: 58, time: '2026-02-15 14:00' },
  { city: '南京', aqi: 68, level: '良', pm25: 38, pm10: 72, so2: 9, no2: 36, time: '2026-02-15 14:00' },
  { city: '重庆', aqi: 82, level: '良', pm25: 48, pm10: 88, so2: 13, no2: 44, time: '2026-02-15 14:00' }
])
</script>

<style scoped>
.chart-demo-page {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.demo-section {
  margin-bottom: 48px;
  padding: 24px;
  background: rgba(17, 24, 39, 0.6);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #e5e7eb;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.gauge-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  align-items: center;
}

.gauge-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  background: rgba(31, 41, 55, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
