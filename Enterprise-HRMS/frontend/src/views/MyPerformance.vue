<template>
  <div class="my-performance-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h2>我的绩效</h2>
        <p class="description">查看您的绩效评估记录，了解评估结果和改进建议</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ stats.totalReviews }}</div>
            <div class="stat-label">评估次数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ stats.avgScore?.toFixed(1) || '-' }}</div>
            <div class="stat-label">平均评分</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ stats.latestPeriod || '-' }}</div>
            <div class="stat-label">最近评估周期</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选区域 -->
    <el-card class="filter-card" shadow="hover">
      <el-form :model="filterForm" inline>
        <el-form-item label="评估周期">
          <el-select
            v-model="filterForm.review_period"
            placeholder="请选择评估周期"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="item in REVIEW_PERIOD_OPTIONS"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 绩效列表 -->
    <el-card class="data-card" shadow="hover">
      <el-table
        v-loading="loading"
        :data="reviewList"
        stripe
        style="width: 100%"
        :default-sort="{ prop: 'review_period', order: 'descending' }"
      >
        <el-table-column prop="review_period" label="评估周期" width="150" sortable>
          <template #default="{ row }">
            <el-tag size="small">{{ formatPeriod(row.review_period) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="score" label="评分" width="120" align="center">
          <template #default="{ row }">
            <div v-if="row.score" class="score-display">
              <el-rate
                :model-value="Number(row.score)"
                disabled
                :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                :score-style="{ color: '#FF9900' }"
              />
              <span class="score-text">{{ row.score }}分</span>
            </div>
            <span v-else class="text-muted">暂无评分</span>
          </template>
        </el-table-column>
        <el-table-column prop="reviewer_name" label="评估人" width="100" />
        <el-table-column prop="strengths" label="优点" min-width="150">
          <template #default="{ row }">
            <el-tooltip :content="row.strengths_short || '暂无优点评价'" placement="top" :disabled="!row.strengths_short">
              <el-text truncated :lines="2">
                {{ truncateText(row.strengths_short, 20) || '-' }}
              </el-text>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="improvements" label="改进建议" min-width="150">
          <template #default="{ row }">
            <el-tooltip :content="row.improvements_short || '暂无改进建议'" placement="top" :disabled="!row.improvements_short">
              <el-text truncated :lines="2">
                {{ truncateText(row.improvements_short, 20) || '-' }}
              </el-text>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="goals" label="工作目标" min-width="150">
          <template #default="{ row }">
            <el-tooltip :content="row.goals_short || '暂无目标设定'" placement="top" :disabled="!row.goals_short">
              <el-text truncated :lines="2">
                {{ truncateText(row.goals_short, 20) || '-' }}
              </el-text>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="评估时间" width="180" sortable>
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openDetailDialog(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty v-if="!loading && reviewList.length === 0" description="暂无绩效评估记录">
        <template #description>
          <p>您还没有被进行绩效评估，请联系HR或管理员。</p>
        </template>
      </el-empty>

      <!-- 分页 -->
      <div v-if="pagination.total > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="绩效评估详情" width="650px">
      <div class="detail-header">
        <el-tag type="success" size="large">
          {{ formatPeriod(currentReview.review_period) }}
        </el-tag>
        <span class="detail-period">绩效评估</span>
      </div>

      <el-divider content-position="left">评估信息</el-divider>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="评估周期">
          {{ formatPeriod(currentReview.review_period) }}
        </el-descriptions-item>
        <el-descriptions-item label="评估人">
          {{ currentReview.reviewer_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="评分">
          <div v-if="currentReview.score" class="score-detail">
            <el-rate
              :model-value="Number(currentReview.score)"
              disabled
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
              :score-style="{ color: '#FF9900' }"
            />
            <span class="score-value">{{ currentReview.score }}分</span>
          </div>
          <span v-else class="text-muted">-</span>
        </el-descriptions-item>
        <el-descriptions-item label="评估时间">
          {{ formatDateTime(currentReview.created_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">评估内容</el-divider>

      <div class="detail-section">
        <div class="section-title">
          <el-icon><Trophy /></el-icon>
          <span>优点</span>
        </div>
        <div class="section-content">
          {{ currentReview.strengths || '暂无优点评价' }}
        </div>
      </div>

      <div class="detail-section">
        <div class="section-title">
          <el-icon><Opportunity /></el-icon>
          <span>改进建议</span>
        </div>
        <div class="section-content">
          {{ currentReview.improvements || '暂无改进建议' }}
        </div>
      </div>

      <div class="detail-section">
        <div class="section-title">
          <el-icon><Aim /></el-icon>
          <span>工作目标</span>
        </div>
        <div class="section-content">
          {{ currentReview.goals || '暂无目标设定' }}
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh, Trophy, Opportunity, Aim } from '@element-plus/icons-vue'
import {
  getMyPerformanceReviews,
  getPerformanceReviewDetail,
  REVIEW_PERIOD_OPTIONS,
  STATUS_TEXT,
  STATUS_TYPE
} from '@/api/performance'
import { formatDateTime } from '@/utils/format'

// 响应式状态
const loading = ref(false)
const reviewList = ref([])
const detailDialogVisible = ref(false)
const currentReview = ref({})

// 分页参数
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

// 筛选表单
const filterForm = reactive({
  review_period: ''
})

// 统计数据
const stats = reactive({
  totalReviews: 0,
  avgScore: null,
  latestPeriod: '-'
})

// 格式化评估周期
const formatPeriod = (period) => {
  if (!period) return '-'
  const option = REVIEW_PERIOD_OPTIONS.find(item => item.value === period)
  return option ? option.label : period
}

// 截取文本（超出指定长度显示省略号）
const truncateText = (text, maxLength = 20) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// 计算统计数据
const calculateStats = (list) => {
  stats.totalReviews = list.length
  if (list.length > 0) {
    const scores = list.filter(item => item.score).map(item => Number(item.score))
    if (scores.length > 0) {
      stats.avgScore = scores.reduce((a, b) => a + b, 0) / scores.length
    }
    // 找到最近的评估周期
    const sorted = [...list].sort((a, b) => {
      return new Date(b.created_at) - new Date(a.created_at)
    })
    stats.latestPeriod = formatPeriod(sorted[0]?.review_period)
  }
}

// 加载我的绩效列表
const fetchReviewList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (filterForm.review_period) {
      params.review_period = filterForm.review_period
    }
    const response = await getMyPerformanceReviews(params)
    console.log('我的绩效响应:', response.data)
    // 处理分页数据格式
    const data = response.data?.data || response.data?.results || []
    const total = response.data?.total || response.data?.count || 0
    console.log('绩效数据:', data)
    reviewList.value = data
    pagination.total = total
    calculateStats(data)
  } catch (error) {
    console.error('获取我的绩效列表失败:', error)
    ElMessage.error('获取我的绩效列表失败')
  } finally {
    loading.value = false
  }
}

// 筛选
const handleFilter = () => {
  pagination.page = 1
  fetchReviewList()
}

// 重置筛选
const resetFilter = () => {
  filterForm.review_period = ''
  pagination.page = 1
  fetchReviewList()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.page_size = size
  fetchReviewList()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchReviewList()
}

// 打开详情对话框
const openDetailDialog = async (row) => {
  try {
    const response = await getPerformanceReviewDetail(row.id)
    currentReview.value = response.data?.data || response.data
    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取评估详情失败:', error)
    ElMessage.error('获取评估详情失败')
  }
}

// 生命周期
onMounted(() => {
  fetchReviewList()
})
</script>

<style scoped>
.my-performance-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.description {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px 0;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #409EFF;
  line-height: 1.2;
}

.stat-label {
  margin-top: 8px;
  color: #909399;
  font-size: 14px;
}

.filter-card {
  margin-bottom: 20px;
}

.data-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.text-muted {
  color: #909399;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-text {
  font-weight: 600;
  color: #FF9900;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.detail-period {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.detail-section {
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.section-title .el-icon {
  color: #409EFF;
}

.section-content {
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
  color: #606266;
}

.score-detail {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-value {
  font-size: 18px;
  font-weight: 600;
  color: #FF9900;
}
</style>
