<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const predictionHistory = ref([])

const loadData = async () => {
  loading.value = true
  try {
    // TODO: 调用 API
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="prediction-page">
    <h2 class="text-2xl font-bold mb-6">趋势预测分析</h2>

    <!-- 预测概览 -->
    <el-row :gutter="20" class="mb-6">
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="text-center">
            <el-icon :size="48" color="#409eff"><TrendCharts /></el-icon>
            <div class="text-xl font-bold mt-2">预测准确率</div>
            <div class="text-3xl font-bold text-primary mt-2">--</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="text-center">
            <el-icon :size="48" color="#67c23a"><DataAnalysis /></el-icon>
            <div class="text-xl font-bold mt-2">本月预测次数</div>
            <div class="text-3xl font-bold text-success mt-2">--</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="text-center">
            <el-icon :size="48" color="#e6a23c"><InfoFilled /></el-icon>
            <div class="text-xl font-bold mt-2">算法模型</div>
            <div class="text-gray-500 mt-2">线性回归 / 移动平均</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预测历史 -->
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <span>预测历史记录</span>
          <el-button type="primary">执行新预测</el-button>
        </div>
      </template>

      <el-table :data="predictionHistory" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="movie" label="影片" min-width="150" />
        <el-table-column prop="algorithm" label="算法" width="120" />
        <el-table-column prop="predicted_date" label="预测日期" width="120" />
        <el-table-column prop="predicted_revenue" label="预测票房(万)" width="140" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminPrediction'
}
</script>
