<template>
  <div class="attendance-manage-view">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <div class="date-picker">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="handleDateChange"
        />
      </div>
      <div class="search-area">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索姓名、电话、地点"
          :prefix-icon="Search"
          clearable
          style="width: 280px"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        />
        <el-button :icon="Search" @click="handleSearch">搜索</el-button>
      </div>
      <div class="filter-area">
        <el-select
          v-model="filters.status"
          placeholder="状态筛选"
          clearable
          style="width: 150px"
          @change="handleFilter"
        >
          <el-option label="正常" value="NORMAL" />
          <el-option label="迟到" value="LATE" />
          <el-option label="早退" value="EARLY_LEAVE" />
          <el-option label="缺卡" value="MISSING" />
          <el-option label="异常" value="ABNORMAL" />
        </el-select>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="statistics-cards">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #FF6B35, #FF8C42)">
          <el-icon :size="32"><User /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.late_count || 0 }}</div>
          <div class="stat-label">迟到次数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #F7C52D, #FFA726)">
          <el-icon :size="32"><Warning /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.missing_count || 0 }}</div>
          <div class="stat-label">缺卡次数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #4CAF50, #66BB6A)">
          <el-icon :size="32"><Clock /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.overtime_hours?.toFixed(1) || '0.0' }}</div>
          <div class="stat-label">加班时长</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #2196F3, #42A5F5)">
          <el-icon :size="32"><Calendar /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics.present_days || 0 }}</div>
          <div class="stat-label">出勤天数</div>
        </div>
      </div>
    </div>

    <!-- 考勤记录表格 -->
    <el-table
      v-loading="loading"
      :data="attendanceList"
      stripe
      style="width: 100%"
      :header-cell-style="{ background: '#FFF8F0', color: '#333' }"
      :row-class-name="getRowClassName"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="employee_name" label="姓名" width="120" />
      <el-table-column prop="work_date" label="工作日期" width="120" />
      <el-table-column prop="shift_name" label="班次" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.shift_name" type="info" size="small">
            {{ row.shift_name }}
          </el-tag>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="clock_in_time" label="签到时间" width="160">
        <template #default="{ row }">
          <span v-if="row.clock_in_time">{{ formatDateTime(row.clock_in_time) }}</span>
          <span v-else class="text-muted">未签到</span>
        </template>
      </el-table-column>
      <el-table-column prop="clock_out_time" label="签退时间" width="160">
        <template #default="{ row }">
          <span v-if="row.clock_out_time">{{ formatDateTime(row.clock_out_time) }}</span>
          <span v-else class="text-muted">未签退</span>
        </template>
      </el-table-column>
      <el-table-column prop="status_display" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusTagType(row.status)" size="small">
            {{ row.status_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="overtime_hours" label="加班(h)" width="90" align="right">
        <template #default="{ row }">
          <span :class="{ 'text-success': row.overtime_hours > 0 }">
            {{ row.overtime_hours?.toFixed(1) || '-' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleView(row)">
            查看
          </el-button>
          <el-button
            v-if="row.status !== 'NORMAL'"
            link
            type="warning"
            size="small"
            @click="handleCorrect(row)"
          >
            修正
          </el-button>
          <el-button link type="danger" size="small" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="考勤记录详情"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-descriptions v-if="currentRecord" :column="2" border>
        <el-descriptions-item label="员工姓名">
          {{ currentRecord.employee_name }}
        </el-descriptions-item>
        <el-descriptions-item label="岗位">
          <el-tag :type="getPositionTagType(currentRecord.employee_position)" size="small">
            {{ currentRecord.employee_position_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="工作日期">
          {{ currentRecord.work_date }}
        </el-descriptions-item>
        <el-descriptions-item label="班次">
          {{ currentRecord.shift_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="签到时间">
          <span v-if="currentRecord.clock_in_time">{{ formatDateTime(currentRecord.clock_in_time) }}</span>
          <span v-else class="text-muted">未签到</span>
        </el-descriptions-item>
        <el-descriptions-item label="签退时间">
          <span v-if="currentRecord.clock_out_time">{{ formatDateTime(currentRecord.clock_out_time) }}</span>
          <span v-else class="text-muted">未签退</span>
        </el-descriptions-item>
        <el-descriptions-item label="签到地点">
          {{ currentRecord.clock_in_location || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="签退地点">
          {{ currentRecord.clock_out_location || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="考勤状态">
          <el-tag :type="getStatusTagType(currentRecord.status)" size="small">
            {{ currentRecord.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="加班时长">
          {{ currentRecord.overtime_hours ? currentRecord.overtime_hours.toFixed(1) + ' 小时' : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="更正备注" :span="2">
          {{ currentRecord.correction_remark || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">
          {{ formatDateTime(currentRecord.created_at) }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 异常处理对话框 -->
    <el-dialog
      v-model="correctDialogVisible"
      title="异常考勤处理"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="correctFormRef"
        :model="correctForm"
        :rules="correctRules"
        label-width="100px"
      >
        <el-form-item label="员工姓名">
          <el-input :value="currentRecord?.employee_name" disabled />
        </el-form-item>
        <el-form-item label="工作日期">
          <el-input :value="currentRecord?.work_date" disabled />
        </el-form-item>
        <el-form-item label="原状态">
          <el-tag :type="getStatusTagType(currentRecord?.status)" size="small">
            {{ currentRecord?.status_display }}
          </el-tag>
        </el-form-item>
        <el-form-item label="修改为" prop="status">
          <el-select v-model="correctForm.status" placeholder="选择新状态" style="width: 100%">
            <el-option label="正常" value="NORMAL" />
            <el-option label="迟到" value="LATE" />
            <el-option label="早退" value="EARLY_LEAVE" />
            <el-option label="缺卡" value="MISSING" />
            <el-option label="异常" value="ABNORMAL" />
          </el-select>
        </el-form-item>
        <el-form-item label="修改备注" prop="correction_remark">
          <el-input
            v-model="correctForm.correction_remark"
            type="textarea"
            :rows="3"
            placeholder="请输入修改原因（必填）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="correctDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="correctLoading" @click="handleConfirmCorrect">
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User, Warning, Clock, Calendar, Search, Plus
} from '@element-plus/icons-vue'
import {
  getAttendanceList,
  getAttendanceDetail,
  deleteAttendance,
  correctAttendance,
  getAttendanceStatistics
} from '@/api/attendance'

// 响应式数据
const loading = ref(false)
const attendanceList = ref([])
const searchKeyword = ref('')
const dateRange = ref([])
const filters = reactive({
  status: ''
})

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 统计数据
const statistics = reactive({
  late_count: 0,
  missing_count: 0,
  overtime_hours: 0,
  present_days: 0
})

// 详情对话框
const detailDialogVisible = ref(false)
const currentRecord = ref(null)

// 异常处理对话框
const correctDialogVisible = ref(false)
const correctLoading = ref(false)
const correctFormRef = ref(null)
const correctForm = reactive({
  status: '',
  correction_remark: ''
})

// 表单验证规则
const correctRules = {
  status: [
    { required: true, message: '请选择新状态', trigger: 'change' }
  ],
  correction_remark: [
    { required: true, message: '请输入修改备注', trigger: 'blur' },
    { min: 5, message: '备注至少5个字符', trigger: 'blur' }
  ]
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    'NORMAL': 'success',
    'LATE': 'warning',
    'EARLY_LEAVE': 'danger',
    'MISSING': 'info',
    'ABNORMAL': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取岗位标签类型
const getPositionTagType = (position) => {
  const typeMap = {
    'CHEF': 'warning',
    'PASTRY': 'danger',
    'PREP': 'info',
    'CLEANER': 'success',
    'SERVER': '',
    'MANAGER': 'primary'
  }
  return typeMap[position] || ''
}

// 获取表格行类名（用于异常记录高亮）
const getRowClassName = ({ row }) => {
  if (row.status === 'LATE' || row.status === 'EARLY_LEAVE' || row.status === 'MISSING' || row.status === 'ABNORMAL') {
    return 'warning-row'
  }
  return ''
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  const date = new Date(dateTimeStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

// 加载考勤列表
const loadAttendanceList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ordering: '-created_at'
    }

    // 添加搜索关键字
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }

    // 添加状态筛选
    if (filters.status) {
      params.status = filters.status
    }

    // 添加日期范围筛选
    if (dateRange.value && dateRange.value.length === 2) {
      params.created_at__gte = dateRange.value[0] + ' 00:00:00'
      params.created_at__lte = dateRange.value[1] + ' 23:59:59'
    }

    const response = await getAttendanceList(params)

    if (response.code === 200) {
      attendanceList.value = response.data.results || []
      pagination.total = response.data.count || 0
    } else {
      ElMessage.error(response.message || '获取考勤列表失败')
    }
  } catch (error) {
    console.error('加载考勤列表失败:', error)
    ElMessage.error('加载考勤列表失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    // 默认统计最近30天
    const endDate = new Date()
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - 30)

    const data = {
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    }

    const response = await getAttendanceStatistics(data)

    if (response.code === 200) {
      Object.assign(statistics, response.data)
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  loadAttendanceList()
}

// 筛选处理
const handleFilter = () => {
  pagination.page = 1
  loadAttendanceList()
}

// 日期变化处理
const handleDateChange = () => {
  pagination.page = 1
  loadAttendanceList()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadAttendanceList()
}

// 页码变化
const handlePageChange = (page) => {
  pagination.page = page
  loadAttendanceList()
}

// 查看详情
const handleView = async (row) => {
  try {
    const response = await getAttendanceDetail(row.id)
    if (response.code === 200) {
      currentRecord.value = response.data
      detailDialogVisible.value = true
    } else {
      ElMessage.error(response.message || '获取详情失败')
    }
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败')
  }
}

// 异常处理
const handleCorrect = (row) => {
  currentRecord.value = row
  correctForm.status = ''
  correctForm.correction_remark = ''
  correctDialogVisible.value = true
}

// 确认异常处理
const handleConfirmCorrect = async () => {
  try {
    // 验证表单
    await correctFormRef.value.validate()

    correctLoading.value = true

    const response = await correctAttendance(currentRecord.value.id, {
      status: correctForm.status,
      correction_remark: correctForm.correction_remark
    })

    if (response.code === 200) {
      ElMessage.success('考勤状态修改成功')
      correctDialogVisible.value = false
      loadAttendanceList()
      loadStatistics() // 重新加载统计数据
    } else {
      ElMessage.error(response.message || '修改失败')
    }
  } catch (error) {
    if (error !== false) { // 排除表单验证取消的情况
      console.error('修改失败:', error)
      ElMessage.error('修改失败，请检查网络连接')
    }
  } finally {
    correctLoading.value = false
  }
}

// 删除考勤记录
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除 ${row.employee_name} 在 ${row.work_date} 的考勤记录吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await deleteAttendance(row.id)
      if (response.code === 200) {
        ElMessage.success('删除成功')
        loadAttendanceList()
        loadStatistics() // 重新加载统计数据
      } else {
        ElMessage.error(response.message || '删除失败')
      }
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 组件挂载时加载数据
onMounted(() => {
  loadAttendanceList()
  loadStatistics()
})
</script>

<style scoped>
.attendance-manage-view {
  padding: 20px;
  background: #f5f5f5;
  min-height: 100vh;
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.date-picker {
  flex-shrink: 0;
}

.search-area {
  display: flex;
  gap: 8px;
  flex: 1;
  min-width: 300px;
}

.filter-area {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

/* 统计卡片区域 */
.statistics-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #FF6B35;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

/* 表格样式 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.text-muted {
  color: #999;
}

.text-success {
  color: #4CAF50;
  font-weight: bold;
}

/* 异常记录行高亮 */
:deep(.el-table .warning-row) {
  background-color: #fff7e6 !important;
}

:deep(.el-table .warning-row:hover > td) {
  background-color: #ffeacc !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .action-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-area {
    width: 100%;
  }

  .filter-area {
    width: 100%;
    flex-direction: column;
  }

  .filter-area .el-select {
    width: 100% !important;
  }

  .statistics-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
  }

  .stat-icon :deep(.el-icon) {
    font-size: 24px !important;
  }
}

@media (max-width: 480px) {
  .attendance-manage-view {
    padding: 12px;
  }

  .statistics-cards {
    grid-template-columns: 1fr;
  }
}
</style>
