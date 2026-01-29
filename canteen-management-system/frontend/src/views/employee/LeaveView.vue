<template>
  <div class="leave-view">
    <div class="page-header">
      <h1>请假申请</h1>
      <p>提交请假申请并查看审批进度</p>
    </div>

    <el-card class="action-card" shadow="hover">
      <div class="action-bar">
        <div class="action-info">
          <el-icon :size="20" color="#FF6B35"><DocumentAdd /></el-icon>
          <span>提交新的请假申请</span>
        </div>
        <el-button type="primary" :icon="Plus" @click="openCreateDialog">新增请假</el-button>
      </div>
    </el-card>

    <el-card class="tab-card" shadow="hover">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="申请记录" name="all">
          <template #label>
            <span class="tab-label">
              <el-icon><List /></el-icon>
              申请记录
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="审批中" name="PENDING">
          <template #label>
            <span class="tab-label">
              <el-icon><Clock /></el-icon>
              审批中
              <el-badge v-if="pendingCount > 0" :value="pendingCount" class="tab-badge" />
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="已通过" name="APPROVED">
          <template #label>
            <span class="tab-label">
              <el-icon><CircleCheck /></el-icon>
              已通过
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="已驳回" name="REJECTED">
          <template #label>
            <span class="tab-label">
              <el-icon><CircleClose /></el-icon>
              已驳回
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>

      <div v-loading="loading" class="leave-list">
        <el-empty v-if="!loading && leaveList.length === 0" description="暂无请假记录" />
        <div v-for="leave in leaveList" :key="leave.id" class="leave-item">
          <div class="leave-header">
            <div class="leave-type">
              <el-tag :type="getLeaveTypeTagType(leave.leave_type)" size="large">
                {{ getLeaveTypeLabel(leave.leave_type) }}
              </el-tag>
            </div>
            <div class="leave-status">
              <el-tag :type="getStatusTagType(leave.status)" effect="plain">
                {{ getStatusLabel(leave.status) }}
              </el-tag>
            </div>
          </div>

          <div class="leave-time">
            <el-icon><Clock /></el-icon>
            <span>{{ formatLeaveTime(leave.start_time, leave.end_time) }}</span>
          </div>

          <div class="leave-duration">
            <el-icon><Timer /></el-icon>
            <span>共 {{ leave.days }} 天</span>
          </div>

          <div class="leave-reason">
            <el-icon><Document /></el-icon>
            <span>{{ leave.reason || '无' }}</span>
          </div>

          <div v-if="leave.status === 'REJECTED' && leave.approval_remark" class="approval-remark">
            <el-icon><WarningFilled /></el-icon>
            <span class="remark-label">审批意见：</span>
            <span class="remark-content">{{ leave.approval_remark }}</span>
          </div>

          <div v-if="leave.status !== 'PENDING'" class="approval-info">
            <el-icon><User /></el-icon>
            <span v-if="leave.approver">审批人：{{ leave.approver_name || '管理员' }}</span>
            <span v-if="leave.approval_time">{{ formatApprovalTime(leave.approval_time) }}</span>
          </div>

          <div class="leave-actions">
            <el-button v-if="leave.status === 'PENDING'" type="danger" size="small" :icon="Delete" @click="handleCancel(leave)">撤销申请</el-button>
            <el-button type="info" size="small" :icon="View" @click="handleViewDetail(leave)">查看详情</el-button>
          </div>
        </div>
      </div>
    </el-card>
    <el-dialog v-model="createDialogVisible" title="新增请假申请" width="500px" :close-on-click-modal="false">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="100px" label-position="left">
        <el-form-item label="请假类型" prop="leave_type">
          <el-select v-model="createForm.leave_type" placeholder="请选择请假类型" style="width: 100%">
            <el-option label="年假" value="ANNUAL" />
            <el-option label="病假" value="SICK" />
            <el-option label="事假" value="PERSONAL" />
            <el-option label="产假" value="MATERNITY" />
            <el-option label="陪产假" value="PATERNITY" />
            <el-option label="其他" value="OTHER" />
          </el-select>
        </el-form-item>

        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="createForm.start_time" type="datetime" placeholder="请选择开始时间" format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%" :disabled-date="disableStartDate" />
        </el-form-item>

        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="createForm.end_time" type="datetime" placeholder="请选择结束时间" format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%" :disabled-date="disableEndDate" />
        </el-form-item>

        <el-form-item label="请假原因" prop="reason">
          <el-input v-model="createForm.reason" type="textarea" :rows="4" placeholder="请输入请假原因（必填，5-200字）" maxlength="200" show-word-limit />
        </el-form-item>

        <el-form-item label="预计天数">
          <div class="days-preview">
            <el-icon :size="18" color="#FF6B35"><Timer /></el-icon>
            <span class="days-number">{{ calculatedDays }}</span>
            <span class="days-unit">天</span>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">提交申请</el-button>
      </template>
    </el-dialog>
    <el-dialog v-model="detailDialogVisible" title="请假详情" width="500px">
      <div v-if="currentLeave" class="leave-detail">
        <div class="detail-item"><span class="detail-label">请假类型：</span><el-tag :type="getLeaveTypeTagType(currentLeave.leave_type)">{{ getLeaveTypeLabel(currentLeave.leave_type) }}</el-tag></div>
        <div class="detail-item"><span class="detail-label">开始时间：</span><span>{{ formatDateTime(currentLeave.start_time) }}</span></div>
        <div class="detail-item"><span class="detail-label">结束时间：</span><span>{{ formatDateTime(currentLeave.end_time) }}</span></div>
        <div class="detail-item"><span class="detail-label">请假天数：</span><span class="detail-value">{{ currentLeave.days }} 天</span></div>
        <div class="detail-item"><span class="detail-label">请假原因：</span><p class="detail-reason">{{ currentLeave.reason || '无' }}</p></div>
        <div class="detail-item"><span class="detail-label">申请状态：</span><el-tag :type="getStatusTagType(currentLeave.status)">{{ getStatusLabel(currentLeave.status) }}</el-tag></div>
        <div v-if="currentLeave.status === 'REJECTED' && currentLeave.approval_remark" class="detail-item"><span class="detail-label">审批意见：</span><p class="detail-remark">{{ currentLeave.approval_remark }}</p></div>
        <div v-if="currentLeave.approver" class="detail-item"><span class="detail-label">审批人：</span><span>{{ currentLeave.approver_name || '管理员' }}</span></div>
        <div v-if="currentLeave.approval_time" class="detail-item"><span class="detail-label">审批时间：</span><span>{{ formatDateTime(currentLeave.approval_time) }}</span></div>
        <div class="detail-item"><span class="detail-label">申请时间：</span><span>{{ formatDateTime(currentLeave.created_at) }}</span></div>
      </div>
      <template #footer><el-button type="primary" @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, View, DocumentAdd, List, Clock, CircleCheck, CircleClose, Timer, Document, WarningFilled, User } from '@element-plus/icons-vue'
import { getMyLeaves, createLeave, deleteLeave } from '@/api/leave'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const activeTab = ref('all')
const pendingCount = ref(0)
const loading = ref(false)
const leaveList = ref([])
const employeeId = computed(() => userStore.userInfo?.employee_id || userStore.userInfo?.employee)

const createDialogVisible = ref(false)
const createFormRef = ref(null)
const submitting = ref(false)
const createForm = ref({ leave_type: '', start_time: '', end_time: '', reason: '' })

const detailDialogVisible = ref(false)
const currentLeave = ref(null)

const createRules = {
  leave_type: [{ required: true, message: '请选择请假类型', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
  reason: [{ required: true, message: '请输入请假原因', trigger: 'blur' }, { min: 5, max: 200, message: '请假原因长度在 5 到 200 个字符', trigger: 'blur' }]
}

const calculatedDays = computed(() => {
  if (!createForm.value.start_time || !createForm.value.end_time) return 0
  const start = new Date(createForm.value.start_time)
  const end = new Date(createForm.value.end_time)
  const diff = end - start
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
  return days > 0 ? days : 0
})

const disableStartDate = (time) => time.getTime() < Date.now() - 8.64e7
const disableEndDate = (time) => createForm.value.start_time ? time.getTime() < new Date(createForm.value.start_time).getTime() : false

const getLeaveTypeTagType = (type) => ({ ANNUAL: 'success', SICK: 'danger', PERSONAL: 'warning', MATERNITY: 'info', PATERNITY: 'info', OTHER: 'info' }[type] || 'info')
const getLeaveTypeLabel = (type) => ({ ANNUAL: '年假', SICK: '病假', PERSONAL: '事假', MATERNITY: '产假', PATERNITY: '陪产假', OTHER: '其他' }[type] || type)
const getStatusTagType = (status) => ({ PENDING: 'warning', APPROVED: 'success', REJECTED: 'danger', CANCELLED: 'info' }[status] || 'info')
const getStatusLabel = (status) => ({ PENDING: '审批中', APPROVED: '已通过', REJECTED: '已驳回', CANCELLED: '已取消' }[status] || status)
const formatLeaveTime = (start, end) => {
  const startDate = new Date(start), endDate = new Date(end)
  const formatDate = (date) => {
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return month + '-' + day + ' ' + hours + ':' + minutes
  }
  const isSameDay = startDate.toDateString() === endDate.toDateString()
  if (isSameDay) {
    return formatDate(startDate) + ' ~ ' + formatDate(endDate).split(' ')[1]
  } else {
    return formatDate(startDate) + ' ~ ' + formatDate(endDate)
  }
}

const formatDateTime = (datetime) => {
  if (!datetime) return ''
  const date = new Date(datetime)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes
}

const formatApprovalTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天 ' + formatDateTime(time).split(' ')[1]
  if (days === 1) return '昨天 ' + formatDateTime(time).split(' ')[1]
  if (days < 7) return days + '天前'
  return formatDateTime(time)
}
const loadLeaveList = async () => {
  if (!employeeId.value) {
    ElMessage.warning('未关联员工档案，无法查看请假记录')
    return
  }
  loading.value = true
  try {
    const params = { employee_id: employeeId.value }
    if (activeTab.value !== 'all') params.status = activeTab.value
    const response = await getMyLeaves(params)
    leaveList.value = response.data || []
    const pendingResponse = await getMyLeaves({ employee_id: employeeId.value, status: 'PENDING' })
    pendingCount.value = (pendingResponse.data || []).length
  } catch (error) {
    console.error('加载请假列表失败:', error)
    ElMessage.error('加载请假列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = () => { loadLeaveList() }

const openCreateDialog = () => {
  createForm.value = { leave_type: '', start_time: '', end_time: '', reason: '' }
  createDialogVisible.value = true
}

const handleSubmit = async () => {
  if (!createFormRef.value) return
  try {
    await createFormRef.value.validate()
  } catch { return }
  if (new Date(createForm.value.end_time) <= new Date(createForm.value.start_time)) {
    ElMessage.warning('结束时间必须晚于开始时间')
    return
  }
  submitting.value = true
  try {
    await createLeave({
      employee: employeeId.value,
      leave_type: createForm.value.leave_type,
      start_time: createForm.value.start_time,
      end_time: createForm.value.end_time,
      reason: createForm.value.reason
    })
    ElMessage.success('请假申请提交成功')
    createDialogVisible.value = false
    loadLeaveList()
  } catch (error) {
    console.error('提交请假申请失败:', error)
    ElMessage.error(error.response?.data?.message || '提交失败')
  } finally {
    submitting.value = false
  }
}

const handleCancel = async (leave) => {
  try {
    await ElMessageBox.confirm('确定要撤销该请假申请吗？', '撤销确认', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' })
    await deleteLeave(leave.id)
    ElMessage.success('已撤销申请')
    loadLeaveList()
  } catch {}
}

const handleViewDetail = (leave) => {
  currentLeave.value = leave
  detailDialogVisible.value = true
}

onMounted(() => { loadLeaveList() })
</script>

<style scoped>
.leave-view { max-width: 1200px; margin: 0 auto; padding: 20px; }
.page-header { margin-bottom: 20px; }
.page-header h1 { font-size: 28px; font-weight: 600; color: #333; margin: 0 0 8px 0; }
.page-header p { font-size: 14px; color: #999; margin: 0; }
.action-card { margin-bottom: 20px; }
.action-bar { display: flex; justify-content: space-between; align-items: center; }
.action-info { display: flex; align-items: center; gap: 12px; font-size: 16px; font-weight: 500; color: #333; }
.tab-card { min-height: 500px; }
.tab-label { display: flex; align-items: center; gap: 6px; }
.tab-badge { margin-left: 4px; }
.leave-list { margin-top: 20px; }
.leave-item { position: relative; padding: 20px; margin-bottom: 16px; background: #fafafa; border-radius: 8px; border-left: 4px solid #FF6B35; transition: all 0.3s; }
.leave-item:hover { background: #f5f5f5; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1); transform: translateX(4px); }
.leave-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.leave-time, .leave-duration, .leave-reason { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; color: #666; font-size: 14px; }
.approval-remark { display: flex; align-items: flex-start; gap: 8px; padding: 10px 12px; margin-top: 12px; background: #fef5e7; border-left: 3px solid #E6A23C; border-radius: 4px; color: #E6A23C; font-size: 14px; }
.remark-label { font-weight: 500; white-space: nowrap; }
.remark-content { flex: 1; }
.approval-info { display: flex; align-items: center; gap: 8px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; color: #999; font-size: 13px; }
.leave-actions { display: flex; gap: 8px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; }
.days-preview { display: flex; align-items: center; gap: 8px; padding: 12px 16px; background: linear-gradient(135deg, #FFF8F0 0%, #fef3e2 100%); border-radius: 6px; }
.days-number { font-size: 24px; font-weight: 600; color: #FF6B35; }
.days-unit { color: #999; }
.leave-detail { padding: 10px 0; }
.detail-item { display: flex; align-items: flex-start; margin-bottom: 16px; font-size: 14px; }
.detail-label { min-width: 100px; font-weight: 500; color: #666; }
.detail-value { color: #FF6B35; font-weight: 600; font-size: 16px; }
.detail-reason, .detail-remark { flex: 1; margin: 0; padding: 12px; background: #f5f7fa; border-radius: 4px; line-height: 1.6; }
.detail-remark { background: #fef5e7; color: #E6A23C; }
@media (max-width: 768px) {
  .leave-view { padding: 16px; }
  .page-header h1 { font-size: 24px; }
  .action-bar { flex-direction: column; gap: 12px; align-items: stretch; }
  .action-info { justify-content: center; }
  .leave-actions { flex-direction: column; }
  .leave-actions .el-button { width: 100%; }
}
</style>
