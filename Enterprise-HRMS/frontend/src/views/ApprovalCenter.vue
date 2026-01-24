<template>
  <div class="approval-center">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>审批中心</h2>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        提交申请
      </el-button>
    </div>

    <!-- Tab 切换 -->
    <el-tabs v-model="activeTab" class="approval-tabs">
      <!-- 我的申请 -->
      <el-tab-pane label="我的申请" name="my-applications">
        <!-- 筛选条件 -->
        <div class="filter-section">
          <el-form :inline="true" :model="myFilter">
            <el-form-item label="类型">
              <el-select v-model="myFilter.request_type" placeholder="全部" clearable style="width: 120px">
                <el-option label="请假" value="leave" />
                <el-option label="加班" value="overtime" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="myFilter.status" placeholder="全部" clearable style="width: 120px">
                <el-option label="待审批" value="pending" />
                <el-option label="已通过" value="approved" />
                <el-option label="已驳回" value="rejected" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadMyApplications">查询</el-button>
              <el-button @click="resetMyFilter">重置</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 申请列表 -->
        <el-table :data="myApplications" v-loading="myLoading" stripe>
          <el-table-column prop="id" label="编号" width="80" />
          <el-table-column label="类型" width="100">
            <template #default="{ row }">
              <el-tag :type="row.request_type === 'leave' ? 'primary' : 'warning'" size="small">
                {{ row.request_type === 'leave' ? '请假' : '加班' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="详情" min-width="200">
            <template #default="{ row }">
              <template v-if="row.request_type === 'leave'">
                {{ getLeaveTypeText(row.leave_type) }} ·
                {{ formatDateTime(row.start_time) }} 至 {{ formatDateTime(row.end_time) }}
              </template>
              <template v-else>
                加班 {{ row.hours }} 小时 ·
                {{ formatDateTime(row.start_time) }} 至 {{ formatDateTime(row.end_time) }}
              </template>
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="原因" min-width="150" show-overflow-tooltip />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="160">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button v-if="row.status === 'pending'" type="danger" link size="small" @click="cancelApplication(row)">
                撤回
              </el-button>
              <el-button type="primary" link size="small" @click="viewApplication(row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-section">
          <el-pagination
            v-model:current-page="myPage"
            v-model:page-size="myPageSize"
            :page-sizes="[10, 20, 50]"
            :total="myTotal"
            layout="total, sizes, prev, pager, next"
            @size-change="loadMyApplications"
            @current-change="loadMyApplications"
          />
        </div>
      </el-tab-pane>

      <!-- 待我审批（HR/Admin） -->
      <el-tab-pane v-if="isHROrAdmin" label="待我审批" name="pending-approvals">
        <!-- 筛选条件 -->
        <div class="filter-section">
          <el-form :inline="true" :model="pendingFilter">
            <el-form-item label="类型">
              <el-select v-model="pendingFilter.request_type" placeholder="全部" clearable style="width: 120px">
                <el-option label="请假" value="leave" />
                <el-option label="加班" value="overtime" />
              </el-select>
            </el-form-item>
            <el-form-item label="申请人">
              <el-input v-model="pendingFilter.applicant" placeholder="申请人姓名" clearable style="width: 150px" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadPendingApprovals">查询</el-button>
              <el-button @click="resetPendingFilter">重置</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 待审批列表 -->
        <el-table :data="pendingApprovals" v-loading="pendingLoading" stripe>
          <el-table-column prop="id" label="编号" width="80" />
          <el-table-column label="申请人" width="100">
            <template #default="{ row }">
              {{ row.user_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="类型" width="100">
            <template #default="{ row }">
              <el-tag :type="row.request_type === 'leave' ? 'primary' : 'warning'" size="small">
                {{ row.request_type === 'leave' ? '请假' : '加班' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="详情" min-width="220">
            <template #default="{ row }">
              <template v-if="row.request_type === 'leave'">
                {{ getLeaveTypeText(row.leave_type) }} ·
                {{ formatDateTime(row.start_time) }} 至 {{ formatDateTime(row.end_time) }}
              </template>
              <template v-else>
                加班 {{ row.hours }} 小时 ·
                {{ formatDateTime(row.start_time) }} 至 {{ formatDateTime(row.end_time) }}
              </template>
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="原因" min-width="150" show-overflow-tooltip />
          <el-table-column prop="created_at" label="申请时间" width="160">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <el-button type="success" link size="small" @click="openApprovalDialog(row, 'approve')">
                通过
              </el-button>
              <el-button type="danger" link size="small" @click="openApprovalDialog(row, 'reject')">
                驳回
              </el-button>
              <el-button type="primary" link size="small" @click="viewApplication(row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-section">
          <el-pagination
            v-model:current-page="pendingPage"
            v-model:page-size="pendingPageSize"
            :page-sizes="[10, 20, 50]"
            :total="pendingTotal"
            layout="total, sizes, prev, pager, next"
            @size-change="loadPendingApprovals"
            @current-change="loadPendingApprovals"
          />
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 提交申请对话框 -->
    <el-dialog v-model="createDialogVisible" title="提交申请" width="500px">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="100px">
        <el-form-item label="申请类型" prop="request_type">
          <el-radio-group v-model="createForm.request_type">
            <el-radio-button value="leave">请假</el-radio-button>
            <el-radio-button value="overtime">加班</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 请假类型（仅请假时显示） -->
        <el-form-item v-if="createForm.request_type === 'leave'" label="请假类型" prop="leave_type">
          <el-select v-model="createForm.leave_type" placeholder="请选择请假类型" style="width: 100%">
            <el-option label="病假" value="sick" />
            <el-option label="事假" value="personal" />
            <el-option label="年假" value="annual" />
          </el-select>
        </el-form-item>

        <!-- 加班时长（仅加班时显示） -->
        <el-form-item v-if="createForm.request_type === 'overtime'" label="加班时长" prop="hours">
          <el-input-number v-model="createForm.hours" :min="0.5" :step="0.5" :precision="1" style="width: 100%" />
          <span class="form-tip">小时</span>
        </el-form-item>

        <!-- 时间范围 -->
        <el-form-item label="时间范围" prop="timeRange">
          <el-date-picker
            v-model="createForm.timeRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>

        <!-- 申请原因 -->
        <el-form-item label="申请原因" prop="reason">
          <el-input v-model="createForm.reason" type="textarea" :rows="3" placeholder="请输入申请原因" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitCreateForm">
          提交
        </el-button>
      </template>
    </el-dialog>

    <!-- 审批操作对话框 -->
    <el-dialog v-model="approvalDialogVisible" :title="approvalAction === 'approve' ? '通过申请' : '驳回申请'" width="450px">
      <el-form ref="approvalFormRef" :model="approvalForm" :rules="approvalRules" label-width="100px">
        <el-form-item label="审批意见">
          <el-input v-model="approvalForm.approver_reason" type="textarea" :rows="3" placeholder="请输入审批意见（可选）" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="approvalDialogVisible = false">取消</el-button>
        <el-button
          :type="approvalAction === 'approve' ? 'success' : 'danger'"
          :loading="approvalSubmitting"
          @click="submitApprovalForm"
        >
          {{ approvalAction === 'approve' ? '确认通过' : '确认驳回' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 申请详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="申请详情" width="500px">
      <el-descriptions :column="1" border v-if="currentApplication">
        <el-descriptions-item label="申请编号">{{ currentApplication.id }}</el-descriptions-item>
        <el-descriptions-item label="申请人">{{ currentApplication.user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="类型">
          <el-tag :type="currentApplication.request_type === 'leave' ? 'primary' : 'warning'" size="small">
            {{ currentApplication.request_type === 'leave' ? '请假' : '加班' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentApplication.request_type === 'leave'" label="请假类型">
          {{ getLeaveTypeText(currentApplication.leave_type) }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentApplication.request_type === 'overtime'" label="加班时长">
          {{ currentApplication.hours }} 小时
        </el-descriptions-item>
        <el-descriptions-item label="时间范围">
          {{ formatDateTime(currentApplication.start_time) }} 至 {{ formatDateTime(currentApplication.end_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="申请原因">{{ currentApplication.reason }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentApplication.status)" size="small">
            {{ getStatusText(currentApplication.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ formatDateTime(currentApplication.created_at) }}</el-descriptions-item>
        <el-descriptions-item v-if="currentApplication.approver" label="审批人">
          {{ currentApplication.approver_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentApplication.approver_reason" label="审批意见">
          {{ currentApplication.approver_reason }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentApplication.updated_at" label="审批时间">
          {{ formatDateTime(currentApplication.updated_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'
import {
  getApplicationList,
  getPendingApprovals,
  submitApplication,
  deleteApplication,
  approveApplication,
  rejectApplication,
  STATUS_TEXT,
  STATUS_TYPE,
  REQUEST_TYPE_TEXT,
  LEAVE_TYPE_TEXT
} from '../api/approval'

// Auth Store
const authStore = useAuthStore()

// 计算属性：是否为 HR 或 Admin
const isHROrAdmin = computed(() => {
  const role = authStore.user?.role
  return role === 'hr' || role === 'admin'
})

// Tab 控制
const activeTab = ref('my-applications')

// ========== 我的申请 ==========
const myLoading = ref(false)
const myApplications = ref([])
const myFilter = reactive({
  request_type: '',
  status: ''
})
const myPage = ref(1)
const myPageSize = ref(10)
const myTotal = ref(0)

// ========== 待我审批 ==========
const pendingLoading = ref(false)
const pendingApprovals = ref([])
const pendingFilter = reactive({
  request_type: '',
  applicant: ''
})
const pendingPage = ref(1)
const pendingPageSize = ref(10)
const pendingTotal = ref(0)

// ========== 创建申请对话框 ==========
const createDialogVisible = ref(false)
const createFormRef = ref(null)
const submitting = ref(false)
const createForm = reactive({
  request_type: 'leave',
  leave_type: '',
  hours: 2,
  timeRange: [],
  reason: ''
})

const createRules = {
  request_type: [{ required: true, message: '请选择申请类型', trigger: 'change' }],
  leave_type: [{ required: true, message: '请选择请假类型', trigger: 'change' }],
  hours: [{ required: true, message: '请填写加班时长', trigger: 'blur' }],
  timeRange: [{ required: true, message: '请选择时间范围', trigger: 'change' }],
  reason: [{ required: true, message: '请输入申请原因', trigger: 'blur' }]
}

// ========== 审批操作对话框 ==========
const approvalDialogVisible = ref(false)
const approvalFormRef = ref(null)
const approvalSubmitting = ref(false)
const currentApprovalItem = ref(null)
const approvalAction = ref('approve')
const approvalForm = reactive({
  approver_reason: ''
})

const approvalRules = {}

// ========== 详情对话框 ==========
const detailDialogVisible = ref(false)
const currentApplication = ref(null)

// ========== 方法 ==========

// 加载我的申请
const loadMyApplications = async () => {
  myLoading.value = true
  try {
    const params = {
      page: myPage.value,
      page_size: myPageSize.value
    }
    if (myFilter.request_type) params.request_type = myFilter.request_type
    if (myFilter.status) params.status = myFilter.status

    const res = await getApplicationList(params)
    myApplications.value = res.data?.data || []
    myTotal.value = res.data?.total || 0
  } catch (e) {
    ElMessage.error('加载申请列表失败')
  } finally {
    myLoading.value = false
  }
}

// 重置我的筛选
const resetMyFilter = () => {
  myFilter.request_type = ''
  myFilter.status = ''
  myPage.value = 1
  loadMyApplications()
}

// 加载待审批列表
const loadPendingApprovals = async () => {
  if (!isHROrAdmin.value) return
  pendingLoading.value = true
  try {
    const params = {
      page: pendingPage.value,
      page_size: pendingPageSize.value
    }
    if (pendingFilter.request_type) params.request_type = pendingFilter.request_type
    if (pendingFilter.applicant) params.applicant = pendingFilter.applicant

    const res = await getPendingApprovals(params)
    pendingApprovals.value = res.data?.data || []
    pendingTotal.value = res.data?.total || 0
  } catch (e) {
    ElMessage.error('加载待审批列表失败')
  } finally {
    pendingLoading.value = false
  }
}

// 重置待审批筛选
const resetPendingFilter = () => {
  pendingFilter.request_type = ''
  pendingFilter.applicant = ''
  pendingPage.value = 1
  loadPendingApprovals()
}

// 显示创建对话框
const showCreateDialog = () => {
  createForm.request_type = 'leave'
  createForm.leave_type = ''
  createForm.hours = 2
  createForm.timeRange = []
  createForm.reason = ''
  createDialogVisible.value = true
}

// 提交创建表单
const submitCreateForm = async () => {
  try {
    await createFormRef.value.validate()
    submitting.value = true

    const data = {
      request_type: createForm.request_type,
      start_time: createForm.timeRange[0],
      end_time: createForm.timeRange[1],
      reason: createForm.reason
    }

    if (createForm.request_type === 'leave') {
      data.leave_type = createForm.leave_type
    } else {
      data.hours = createForm.hours
    }

    await submitApplication(data)
    ElMessage.success('申请提交成功')
    createDialogVisible.value = false
    loadMyApplications()
  } catch (e) {
    if (e !== false) {
      ElMessage.error('提交申请失败')
    }
  } finally {
    submitting.value = false
  }
}

// 撤回申请
const cancelApplication = async (row) => {
  try {
    await ElMessageBox.confirm('确定要撤回该申请吗？', '提示', {
      type: 'warning'
    })
    await deleteApplication(row.id)
    ElMessage.success('撤回成功')
    loadMyApplications()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('撤回失败')
    }
  }
}

// 查看申请详情
const viewApplication = (row) => {
  currentApplication.value = row
  detailDialogVisible.value = true
}

// 打开审批对话框
const openApprovalDialog = (row, action) => {
  currentApprovalItem.value = row
  approvalAction.value = action
  approvalForm.approver_reason = ''
  approvalDialogVisible.value = true
}

// 提交审批
const submitApprovalForm = async () => {
  try {
    approvalSubmitting.value = true
    const data = {
      approver_reason: approvalForm.approver_reason
    }

    if (approvalAction.value === 'approve') {
      await approveApplication(currentApprovalItem.value.id, data)
      ElMessage.success('审批通过')
    } else {
      await rejectApplication(currentApprovalItem.value.id, data)
      ElMessage.success('已驳回申请')
    }

    approvalDialogVisible.value = false
    loadMyApplications()
    loadPendingApprovals()
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    approvalSubmitting.value = false
  }
}

// 格式化日期时间
const formatDateTime = (datetime) => {
  if (!datetime) return '-'
  return datetime.replace('T', ' ').substring(0, 16)
}

// 获取状态文本
const getStatusText = (status) => {
  return STATUS_TEXT[status] || status
}

// 获取状态类型
const getStatusType = (status) => {
  return STATUS_TYPE[status] || 'info'
}

// 获取请假类型文本
const getLeaveTypeText = (type) => {
  return LEAVE_TYPE_TEXT[type] || type
}

// Tab 切换监听
const handleTabChange = (tab) => {
  if (tab === 'my-applications') {
    loadMyApplications()
  } else if (tab === 'pending-approvals' && isHROrAdmin.value) {
    loadPendingApprovals()
  }
}

// 监听 Tab 变化
import { watch } from 'vue'
watch(activeTab, handleTabChange)

// 初始化
onMounted(() => {
  loadMyApplications()
  if (isHROrAdmin.value) {
    loadPendingApprovals()
  }
})
</script>

<style scoped>
.approval-center {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.approval-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
}

.filter-section {
  margin-bottom: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.pagination-section {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.form-tip {
  margin-left: 10px;
  color: #909399;
  font-size: 13px;
}
</style>
