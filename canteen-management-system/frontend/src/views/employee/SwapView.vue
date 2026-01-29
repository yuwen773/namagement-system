<template>
  <div class="swap-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">调班申请</h1>
      <p class="page-subtitle">提交调班申请并查看审批进度</p>
    </div>

    <!-- 操作卡片 -->
    <el-card class="action-card" shadow="hover">
      <div class="action-content">
        <div class="action-left">
          <el-icon class="action-icon" :size="32" color="#F7C52D"><Switch /></el-icon>
          <div class="action-text">
            <div class="action-title">需要调整班次？</div>
            <div class="action-desc">选择原班次和期望调整的班次，填写申请原因</div>
          </div>
        </div>
        <el-button type="primary" size="large" @click="openCreateDialog">
          <el-icon><Switch /></el-icon>
          新增调班申请
        </el-button>
      </div>
    </el-card>

    <!-- 调班记录列表 -->
    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">调班记录</span>
          <el-tag v-if="swapList.length > 0" type="info" size="large">共 {{ swapList.length }} 条</el-tag>
        </div>
      </template>

      <div v-loading="loading" class="swap-list">
        <el-empty v-if="!loading && swapList.length === 0" description="暂无调班记录">
          <el-button type="primary" @click="openCreateDialog">提交第一份申请</el-button>
        </el-empty>

        <div v-for="item in swapList" :key="item.id" class="swap-card">
          <div class="swap-header">
            <el-tag :type="getStatusTagType(item.status)" size="large">
              {{ getStatusLabel(item.status) }}
            </el-tag>
            <div class="swap-date">
              <el-icon><Clock /></el-icon>
              申请时间: {{ formatDateTime(item.created_at) }}
            </div>
          </div>

          <div class="swap-content">
            <div class="swap-section">
              <div class="section-label original">
                <el-icon><Back /></el-icon>
                原班次
              </div>
              <div class="schedule-info">
                <div class="schedule-date">{{ formatDate(item.original_schedule_date) }}</div>
                <el-tag type="warning" size="small">{{ item.original_shift_name }}</el-tag>
                <div class="schedule-time">{{ item.original_shift_time }}</div>
              </div>
            </div>

            <div class="swap-arrow">
              <el-icon><Right /></el-icon>
            </div>

            <div class="swap-section">
              <div class="section-label target">
                <el-icon><Right /></el-icon>
                期望调整
              </div>
              <div class="schedule-info">
                <div class="schedule-date">{{ formatDate(item.target_date) }}</div>
                <el-tag type="success" size="small">{{ item.target_shift_name }}</el-tag>
                <div class="schedule-time">{{ item.target_shift_time }}</div>
              </div>
            </div>
          </div>

          <div v-if="item.reason" class="swap-reason">
            <el-icon><Document /></el-icon>
            <span>申请原因: {{ item.reason }}</span>
          </div>

          <div v-if="item.status === 'REJECTED' && item.approval_remark" class="approval-remark">
            <el-icon><WarningFilled /></el-icon>
            <div class="remark-content">
              <div class="remark-label">驳回原因:</div>
              <div class="remark-text">{{ item.approval_remark }}</div>
            </div>
          </div>

          <div v-if="item.status === 'APPROVED'" class="approval-info">
            <el-icon><CircleCheckFilled /></el-icon>
            <span>已通过 {{ item.approver_name ? `· 审批人: ${item.approver_name}` : '' }}</span>
          </div>

          <div class="swap-actions">
            <el-button v-if="item.status === 'PENDING'" type="danger" plain size="small" @click="handleDelete(item)">
              <el-icon><Delete /></el-icon>
              撤销申请
            </el-button>
            <el-button type="primary" plain size="small" @click="handleViewDetail(item)">
              <el-icon><View /></el-icon>
              查看详情
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 新增调班申请对话框 -->
    <el-dialog v-model="createDialogVisible" title="新增调班申请" width="600px" :close-on-click-modal="false">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="100px">
        <el-form-item label="原班次" prop="original_schedule_id">
          <el-select
            v-model="createForm.original_schedule_id"
            placeholder="请选择要调整的原班次"
            style="width: 100%"
            filterable
            @change="handleOriginalScheduleChange"
          >
            <el-option
              v-for="schedule in mySchedules"
              :key="schedule.id"
              :label="`${schedule.work_date} ${schedule.shift_name}`"
              :value="schedule.id"
            >
              <div class="schedule-option">
                <span class="option-date">{{ formatDate(schedule.work_date) }}</span>
                <el-tag size="small" :type="getShiftTagType(schedule.shift_name)">
                  {{ schedule.shift_name }}
                </el-tag>
                <span class="option-time">{{ schedule.shift_time }}</span>
              </div>
            </el-option>
          </el-select>
          <div v-if="selectedOriginalSchedule" class="selected-schedule-tip">
            <el-icon><InfoFilled /></el-icon>
            已选择: {{ formatDate(selectedOriginalSchedule.work_date) }} {{ selectedOriginalSchedule.shift_name }} ({{ selectedOriginalSchedule.shift_time }})
          </div>
        </el-form-item>

        <el-form-item label="目标日期" prop="target_date">
          <el-date-picker
            v-model="createForm.target_date"
            type="date"
            placeholder="选择目标日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :disabled-date="disableTargetDate"
            style="width: 100%"
            @change="handleTargetDateChange"
          />
        </el-form-item>

        <el-form-item label="目标班次" prop="target_shift_id">
          <el-select
            v-model="createForm.target_shift_id"
            placeholder="请选择目标班次"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="shift in shiftList"
              :key="shift.id"
              :label="`${shift.name} (${shift.start_time} - ${shift.end_time})`"
              :value="shift.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="申请原因" prop="reason">
          <el-input
            v-model="createForm.reason"
            type="textarea"
            :rows="4"
            placeholder="请输入调班原因（5-200字）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          提交申请
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="调班申请详情" width="600px">
      <div v-if="currentSwap" class="detail-content">
        <div class="detail-section">
          <div class="detail-label">申请状态</div>
          <el-tag :type="getStatusTagType(currentSwap.status)" size="large">
            {{ getStatusLabel(currentSwap.status) }}
          </el-tag>
        </div>

        <div class="detail-row">
          <div class="detail-item">
            <div class="detail-label">原班次日期</div>
            <div class="detail-value">{{ formatDate(currentSwap.original_schedule_date) }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">原班次</div>
            <div class="detail-value">
              <el-tag type="warning">{{ currentSwap.original_shift_name }}</el-tag>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-label">原班次时间</div>
            <div class="detail-value">{{ currentSwap.original_shift_time }}</div>
          </div>
        </div>

        <div class="detail-row">
          <div class="detail-item">
            <div class="detail-label">目标日期</div>
            <div class="detail-value">{{ formatDate(currentSwap.target_date) }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">目标班次</div>
            <div class="detail-value">
              <el-tag type="success">{{ currentSwap.target_shift_name }}</el-tag>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-label">目标班次时间</div>
            <div class="detail-value">{{ currentSwap.target_shift_time }}</div>
          </div>
        </div>

        <div class="detail-section">
          <div class="detail-label">申请原因</div>
          <div class="detail-value">{{ currentSwap.reason || '-' }}</div>
        </div>

        <div v-if="currentSwap.approval_remark" class="detail-section approval-section">
          <div class="detail-label">审批意见</div>
          <div class="detail-value">{{ currentSwap.approval_remark }}</div>
        </div>

        <div class="detail-row">
          <div class="detail-item">
            <div class="detail-label">申请人</div>
            <div class="detail-value">{{ currentSwap.requester_name || '-' }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">审批人</div>
            <div class="detail-value">{{ currentSwap.approver_name || '-' }}</div>
          </div>
        </div>

        <div class="detail-row">
          <div class="detail-item">
            <div class="detail-label">申请时间</div>
            <div class="detail-value">{{ formatDateTime(currentSwap.created_at) }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">审批时间</div>
            <div class="detail-value">{{ formatDateTime(currentSwap.approval_time) || '-' }}</div>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button type="primary" @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Switch, Clock, Document, Back, Right, Delete, View,
  WarningFilled, CircleCheckFilled, InfoFilled
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getShiftList } from '@/api/schedule'
import { getMyShiftRequests, createShiftRequest, deleteShiftRequest } from '@/api/schedule'
import { getEmployeeSchedules } from '@/api/schedule'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const swapList = ref([])
const createDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const submitting = ref(false)
const currentSwap = ref(null)
const mySchedules = ref([])
const shiftList = ref([])

// 新增表单
const createFormRef = ref(null)
const createForm = reactive({
  original_schedule_id: null,
  target_date: null,
  target_shift_id: null,
  reason: ''
})

// 选中的原班次
const selectedOriginalSchedule = computed(() => {
  if (!createForm.original_schedule_id) return null
  return mySchedules.value.find(s => s.id === createForm.original_schedule_id)
})

// 表单验证规则
const createRules = {
  original_schedule_id: [
    { required: true, message: '请选择原班次', trigger: 'change' }
  ],
  target_date: [
    { required: true, message: '请选择目标日期', trigger: 'change' }
  ],
  target_shift_id: [
    { required: true, message: '请选择目标班次', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入调班原因', trigger: 'blur' },
    { min: 5, max: 200, message: '调班原因长度在 5 到 200 个字符', trigger: 'blur' }
  ]
}

// 加载调班列表
const loadSwapList = async () => {
  const employeeId = userStore.userInfo?.employee
  if (!employeeId) {
    ElMessage.warning('未关联员工档案，无法查看调班记录')
    return
  }

  loading.value = true
  try {
    const res = await getMyShiftRequests({ employee_id: employeeId })
    if (res.code === 200) {
      swapList.value = res.data || []
    }
  } catch (error) {
    console.error('加载调班列表失败:', error)
    ElMessage.error('加载调班列表失败')
  } finally {
    loading.value = false
  }
}

// 加载我的排班
const loadMySchedules = async () => {
  const employeeId = userStore.userInfo?.employee
  if (!employeeId) return

  try {
    const startDate = new Date()
    const endDate = new Date()
    endDate.setDate(endDate.getDate() + 30) // 未来30天

    const res = await getEmployeeSchedules(
      employeeId,
      formatDateToString(startDate),
      formatDateToString(endDate)
    )

    if (res.code === 200) {
      // 处理排班数据
      mySchedules.value = await Promise.all((res.data.results || res.data || []).map(async schedule => {
        // 获取班次详情
        const shiftRes = await getShiftDetail(schedule.shift)
        return {
          id: schedule.id,
          work_date: schedule.work_date,
          shift_id: schedule.shift,
          shift_name: shiftRes.data?.name || '',
          shift_time: shiftRes.data ? `${shiftRes.data.start_time} - ${shiftRes.data.end_time}` : ''
        }
      }))
    }
  } catch (error) {
    console.error('加载排班失败:', error)
  }
}

// 加载班次列表
const loadShiftList = async () => {
  try {
    const res = await getShiftList()
    if (res.code === 200) {
      shiftList.value = res.data.results || res.data || []
    }
  } catch (error) {
    console.error('加载班次列表失败:', error)
  }
}

// 获取班次详情
const getShiftDetail = async (shiftId) => {
  try {
    return await fetch(`/api/schedules/shifts/${shiftId}/`).then(res => res.json()).then(data => ({ data }))
  } catch (error) {
    return { data: null }
  }
}

// 打开创建对话框
const openCreateDialog = async () => {
  createDialogVisible.value = true
  await loadMySchedules()
  await loadShiftList()
  resetCreateForm()
}

// 重置创建表单
const resetCreateForm = () => {
  createForm.original_schedule_id = null
  createForm.target_date = null
  createForm.target_shift_id = null
  createForm.reason = ''
  createFormRef.value?.resetFields()
}

// 原班次选择变化
const handleOriginalScheduleChange = () => {
  // 可以在这里添加逻辑，比如自动填充目标日期等
}

// 目标日期变化
const handleTargetDateChange = () => {
  // 可以在这里添加逻辑
}

// 禁用目标日期
const disableTargetDate = (time) => {
  // 禁用今天之前的日期
  return time.getTime() < Date.now() - 8.64e7
}

// 提交表单
const handleSubmit = async () => {
  const valid = await createFormRef.value?.validate()
  if (!valid) return

  const employeeId = userStore.userInfo?.employee
  if (!employeeId) {
    ElMessage.warning('未关联员工档案，无法提交申请')
    return
  }

  submitting.value = true
  try {
    const data = {
      original_schedule: createForm.original_schedule_id,
      target_date: createForm.target_date,
      target_shift: createForm.target_shift_id,
      reason: createForm.reason,
      requester_id: employeeId
    }

    const res = await createShiftRequest(data)
    if (res.code === 200) {
      ElMessage.success('调班申请提交成功')
      createDialogVisible.value = false
      await loadSwapList()
    }
  } catch (error) {
    console.error('提交调班申请失败:', error)
    ElMessage.error('提交调班申请失败')
  } finally {
    submitting.value = false
  }
}

// 删除调班申请
const handleDelete = (item) => {
  ElMessageBox.confirm(
    '确定要撤销该调班申请吗？撤销后需要重新提交申请。',
    '确认撤销',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const res = await deleteShiftRequest(item.id)
      if (res.code === 200) {
        ElMessage.success('撤销成功')
        await loadSwapList()
      }
    } catch (error) {
      console.error('撤销失败:', error)
      ElMessage.error('撤销失败')
    }
  }).catch(() => {})
}

// 查看详情
const handleViewDetail = (item) => {
  currentSwap.value = item
  detailDialogVisible.value = true
}

// 状态标签类型
const getStatusTagType = (status) => {
  const map = {
    'PENDING': 'warning',
    'APPROVED': 'success',
    'REJECTED': 'danger'
  }
  return map[status] || 'info'
}

// 状态标签文本
const getStatusLabel = (status) => {
  const map = {
    'PENDING': '审批中',
    'APPROVED': '已通过',
    'REJECTED': '已驳回'
  }
  return map[status] || status
}

// 班次标签类型
const getShiftTagType = (shiftName) => {
  const map = {
    '早班': 'success',
    '中班': 'warning',
    '晚班': 'danger',
    '全天': 'primary'
  }
  return map[shiftName] || 'info'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const weekday = weekdays[date.getDay()]
  return `${month}-${day} ${weekday}`
}

// 格式化日期时间
const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

// 格式化日期为字符串 YYYY-MM-DD
const formatDateToString = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 页面加载时执行
onMounted(() => {
  loadSwapList()
})
</script>

<style scoped>
.swap-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

/* 操作卡片 */
.action-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.action-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-icon {
  flex-shrink: 0;
}

.action-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.action-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.action-desc {
  font-size: 13px;
  color: #999;
}

/* 记录卡片 */
.records-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.swap-list {
  min-height: 200px;
}

.swap-card {
  background: #fafafa;
  border-left: 4px solid #FF6B35;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.swap-card:hover {
  background: #f5f5f5;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.swap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.swap-date {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #999;
}

.swap-content {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.swap-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 500;
}

.section-label.original {
  color: #E6A23C;
}

.section-label.target {
  color: #4CAF50;
}

.schedule-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.schedule-date {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.schedule-time {
  font-size: 12px;
  color: #999;
}

.swap-arrow {
  color: #FF6B35;
  font-size: 20px;
}

.swap-reason {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 13px;
  color: #666;
  background: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
}

.approval-remark {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  background: #fef5e7;
  border-left: 3px solid #E6A23C;
  padding: 10px;
  border-radius: 4px;
  font-size: 13px;
  color: #E6A23C;
}

.remark-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.remark-label {
  font-weight: 500;
}

.remark-text {
  color: #E6A23C;
}

.approval-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #4CAF50;
}

.swap-actions {
  display: flex;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

/* 表单样式 */
.schedule-option {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.option-date {
  flex: 1;
  font-size: 14px;
}

.option-time {
  font-size: 12px;
  color: #999;
}

.selected-schedule-tip {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 12px;
  color: #4CAF50;
}

/* 详情对话框 */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  font-size: 13px;
  color: #999;
}

.detail-value {
  font-size: 14px;
  color: #333;
}

.detail-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.approval-section {
  background: #fef5e7;
  padding: 12px;
  border-radius: 4px;
  border-left: 3px solid #E6A23C;
}

.approval-section .detail-label {
  color: #E6A23C;
}

.approval-section .detail-value {
  color: #E6A23C;
}

/* 响应式 */
@media (max-width: 768px) {
  .swap-view {
    padding: 12px;
  }

  .page-title {
    font-size: 22px;
  }

  .action-content {
    flex-direction: column;
    gap: 12px;
  }

  .action-content .el-button {
    width: 100%;
  }

  .swap-content {
    flex-direction: column;
    align-items: stretch;
  }

  .swap-arrow {
    transform: rotate(90deg);
    align-self: center;
  }

  .detail-row {
    grid-template-columns: 1fr;
  }
}
</style>
