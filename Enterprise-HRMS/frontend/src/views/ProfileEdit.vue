<template>
  <div class="profile-edit-container">
    <div class="page-header">
      <h2>个人信息编辑</h2>
      <p class="subtitle">管理您的个人信息，修改手机号或邮箱需要提交审批</p>
    </div>

    <!-- 当前信息展示 -->
    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>当前信息</span>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">{{ user?.username }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ user?.real_name }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ user?.phone || '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ user?.email || '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="角色">{{ roleText }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ formatDate(user?.date_joined) }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 修改信息表单 -->
    <el-card class="edit-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>提交修改申请</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="修改类型" prop="edit_type">
          <el-radio-group v-model="formData.edit_type" @change="handleTypeChange">
            <el-radio-button value="phone">手机号</el-radio-button>
            <el-radio-button value="email">邮箱</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item :label="currentLabel" prop="new_value">
          <el-input
            v-model="formData.new_value"
            :placeholder="currentPlaceholder"
            clearable
          />
        </el-form-item>

        <el-form-item label="修改原因" prop="reason">
          <el-input
            v-model="formData.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入修改原因..."
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            提交申请
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 我的申请记录 -->
    <el-card class="history-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>我的申请记录</span>
          <el-button type="primary" link @click="loadApplications">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <el-table
        :data="applications"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="edit_type_display" label="修改类型" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ row.edit_type_display }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="原值 → 新值" min-width="200">
          <template #default="{ row }">
            <span class="old-value">{{ row.old_value || '未设置' }}</span>
            <el-icon><Right /></el-icon>
            <span class="new-value">{{ row.new_value }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="reason" label="修改原因" min-width="150">
          <template #default="{ row }">
            <el-tooltip :content="row.reason" placement="top" :disabled="!row.reason">
              <span class="reason-text">{{ row.reason || '-' }}</span>
            </el-tooltip>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="STATUS_TYPE[row.status]" size="small">
              {{ STATUS_TEXT[row.status] }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="申请时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column v-if="isHR" label="操作" width="120">
          <template #default="{ row }">
            <template v-if="row.status === 'pending'">
              <el-button type="success" link size="small" @click="handleApprove(row)">
                通过
              </el-button>
              <el-button type="danger" link size="small" @click="handleReject(row)">
                驳回
              </el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 审批对话框 -->
    <el-dialog v-model="approveDialogVisible" title="审批修改申请" width="400px">
      <el-form :model="approvalForm" label-width="80px">
        <el-form-item label="申请人">
          <span>{{ currentEditRequest?.user_name }}</span>
        </el-form-item>
        <el-form-item label="修改类型">
          <span>{{ currentEditRequest?.edit_type_display }}</span>
        </el-form-item>
        <el-form-item label="原值 → 新值">
          <span>{{ currentEditRequest?.old_value }} → {{ currentEditRequest?.new_value }}</span>
        </el-form-item>
        <el-form-item label="审批意见" v-if="approvalAction === 'reject'">
          <el-input
            v-model="approvalForm.reviewer_comment"
            type="textarea"
            :rows="2"
            placeholder="请输入驳回原因..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="approveDialogVisible = false">取消</el-button>
          <el-button
            :type="approvalAction === 'approve' ? 'success' : 'danger'"
            @click="submitApproval"
            :loading="approvalLoading"
          >
            {{ approvalAction === 'approve' ? '通过' : '驳回' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Right, Refresh } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'
import {
  getCurrentUser,
  getEditRequestList,
  createEditRequest,
  getPendingEditRequests,
  approveEditRequest,
  rejectEditRequest,
  EDIT_TYPE,
  EDIT_TYPE_TEXT,
  STATUS,
  STATUS_TEXT,
  STATUS_TYPE
} from '../api/profile'

const authStore = useAuthStore()
const user = ref(null)
const isHR = computed(() => authStore.isHR || authStore.isAdmin)

const roleText = computed(() => {
  const roleMap = {
    admin: '系统管理员',
    hr: '人事专员',
    employee: '普通员工'
  }
  return roleMap[user.value?.role] || '-'
})

// 获取当前用户信息
const loadCurrentUser = async () => {
  try {
    const res = await getCurrentUser()
    user.value = res.data?.data
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 表单数据
const formRef = ref(null)
const formData = reactive({
  edit_type: EDIT_TYPE.PHONE,
  new_value: '',
  reason: ''
})

const submitLoading = ref(false)

// 表单验证规则
const validatePhone = (rule, value, callback) => {
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(value)) {
    callback(new Error('请输入正确的手机号格式'))
  } else {
    callback()
  }
}

const validateEmail = (rule, value, callback) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(value)) {
    callback(new Error('请输入正确的邮箱格式'))
  } else {
    callback()
  }
}

const rules = computed(() => ({
  edit_type: [{ required: true, message: '请选择修改类型', trigger: 'change' }],
  new_value: [
    { required: true, message: `请输入${currentLabel.value}`, trigger: 'blur' },
    { validator: formData.edit_type === EDIT_TYPE.PHONE ? validatePhone : validateEmail, trigger: 'blur' }
  ],
  reason: [{ required: true, message: '请输入修改原因', trigger: 'blur' }]
}))

const currentLabel = computed(() => formData.edit_type === EDIT_TYPE.PHONE ? '新手机号' : '新邮箱')
const currentPlaceholder = computed(() => formData.edit_type === EDIT_TYPE.PHONE ? '请输入新手机号' : '请输入新邮箱')

// 申请记录列表
const applications = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 审批对话框
const approveDialogVisible = ref(false)
const approvalAction = ref('')
const approvalForm = reactive({
  reviewer_comment: ''
})
const approvalLoading = ref(false)
const currentEditRequest = ref(null)

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

// 处理修改类型变化
const handleTypeChange = () => {
  formData.new_value = ''
  formData.reason = ''
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

// 提交修改申请
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitLoading.value = true
        await createEditRequest({
          edit_type: formData.edit_type,
          new_value: formData.new_value,
          reason: formData.reason
        })
        ElMessage.success('修改申请已提交，请等待审批')
        resetForm()
        loadApplications()
      } catch (error) {
        const msg = error.response?.data?.message || '提交申请失败'
        ElMessage.error(msg)
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  formData.new_value = ''
  formData.reason = ''
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 加载申请列表
const loadApplications = async () => {
  try {
    loading.value = true
    let res
    if (isHR.value) {
      // HR/Admin 加载待审批列表
      res = await getPendingEditRequests()
      applications.value = res.data?.data || res.data?.results || []
      total.value = res.data?.total || res.data?.count || applications.value.length
    } else {
      // 普通员工加载自己的申请列表
      res = await getEditRequestList({
        page: currentPage.value,
        page_size: pageSize.value
      })
      applications.value = res.data?.data || res.data?.results || []
      total.value = res.data?.total || res.data?.count || 0
    }
  } catch (error) {
    ElMessage.error('加载申请列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 处理分页
const handlePageChange = (page) => {
  currentPage.value = page
  loadApplications()
}

// 审批通过
const handleApprove = (row) => {
  currentEditRequest.value = row
  approvalAction.value = 'approve'
  approvalForm.reviewer_comment = ''
  approveDialogVisible.value = true
}

// 审批驳回
const handleReject = (row) => {
  currentEditRequest.value = row
  approvalAction.value = 'reject'
  approvalForm.reviewer_comment = ''
  approveDialogVisible.value = true
}

// 提交审批
const submitApproval = async () => {
  try {
    approvalLoading.value = true
    if (approvalAction.value === 'approve') {
      await approveEditRequest(currentEditRequest.value.id, {
        reviewer_comment: approvalForm.reviewer_comment
      })
      ElMessage.success('已通过该申请')
    } else {
      if (!approvalForm.reviewer_comment.trim()) {
        ElMessage.warning('请输入驳回原因')
        return
      }
      await rejectEditRequest(currentEditRequest.value.id, {
        reviewer_comment: approvalForm.reviewer_comment
      })
      ElMessage.success('已驳回该申请')
    }
    approveDialogVisible.value = false
    loadApplications()
  } catch (error) {
    const msg = error.response?.data?.message || '操作失败'
    ElMessage.error(msg)
  } finally {
    approvalLoading.value = false
  }
}

onMounted(async () => {
  await loadCurrentUser()
  loadApplications()
})
</script>

<style scoped>
.profile-edit-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.info-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.edit-card {
  margin-bottom: 20px;
}

.history-card {
  margin-bottom: 20px;
}

.old-value {
  color: #909399;
  text-decoration: line-through;
}

.new-value {
  color: #67c23a;
  font-weight: 500;
}

.reason-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
