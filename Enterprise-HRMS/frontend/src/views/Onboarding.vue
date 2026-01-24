<template>
  <div class="onboarding-container">
    <div class="page-header">
      <h2>入职管理</h2>
      <p class="subtitle">管理待入职用户，为其办理入职手续</p>
    </div>

    <!-- 待入职用户列表 -->
    <el-card class="user-list-card">
      <template #header>
        <div class="card-header">
          <span>待入职用户列表</span>
          <el-button type="primary" :loading="loading" @click="fetchPendingUsers">
            <el-icon><Refresh /></el-icon>
            刷新列表
          </el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="pendingUsers"
        stripe
        style="width: 100%"
        :empty-text="loading ? '加载中...' : '暂无待入职用户'"
      >
        <el-table-column prop="id" label="用户ID" width="80" />
        <el-table-column prop="username" label="账号" width="120" />
        <el-table-column prop="real_name" label="真实姓名" width="100" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="date_joined" label="注册时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.date_joined) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openOnboardingDialog(row)">
              办理入职
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchPendingUsers"
          @current-change="fetchPendingUsers"
        />
      </div>
    </el-card>

    <!-- 入职办理对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="办理入职"
      width="500px"
      :close-on-click-modal="false"
      @close="handleDialogClose"
    >
      <el-form
        ref="onboardingFormRef"
        :model="onboardingForm"
        :rules="formRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="用户信息">
          <div class="user-info-display">
            <span class="name">{{ selectedUser?.real_name }}</span>
            <span class="username">({{ selectedUser?.username }})</span>
          </div>
        </el-form-item>

        <el-form-item label="所属部门" prop="department">
          <el-tree-select
            v-model="onboardingForm.department"
            :data="departmentTree"
            :props="{ label: 'name', value: 'id', children: 'children' }"
            placeholder="请选择部门"
            check-strictly
            width="100%"
            filterable
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="分配岗位" prop="post">
          <el-select
            v-model="onboardingForm.post"
            placeholder="请选择岗位"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="post in postList"
              :key="post.id"
              :label="post.name"
              :value="post.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="入职日期" prop="hire_date">
          <el-date-picker
            v-model="onboardingForm.hire_date"
            type="date"
            placeholder="选择入职日期"
            style="width: 100%"
            value-format="YYYY-MM-DD"
            :disabled-date="disabledDate"
          />
        </el-form-item>

        <el-form-item label="基本工资" prop="salary_base">
          <el-input-number
            v-model="onboardingForm.salary_base"
            :min="0"
            :precision="2"
            :step="100"
            style="width: 100%"
          >
            <template #prefix>¥</template>
          </el-input-number>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="submitting"
            @click="handleSubmit(onboardingFormRef)"
          >
            确认入职
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { getPendingUsers, createEmployee } from '@/api/employee'
import { getDepartmentTree } from '@/api/department'
import { getPostList } from '@/api/post'

// 数据
const loading = ref(false)
const submitting = ref(false)
const pendingUsers = ref([])
const departmentTree = ref([])
const postList = ref([])
const selectedUser = ref(null)
const dialogVisible = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 表单
const onboardingFormRef = ref(null)
const onboardingForm = reactive({
  user_id: null,
  department: null,
  post: null,
  hire_date: '',
  salary_base: 0
})

// 表单验证规则
const formRules = {
  department: [
    { required: true, message: '请选择所属部门', trigger: 'change' }
  ],
  post: [
    { required: true, message: '请选择分配岗位', trigger: 'change' }
  ],
  hire_date: [
    { required: true, message: '请选择入职日期', trigger: 'change' }
  ],
  salary_base: [
    { required: true, message: '请输入基本工资', trigger: 'blur' },
    { type: 'number', min: 0, message: '基本工资必须大于等于0', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 禁用未来日期
const disabledDate = (time) => {
  return time.getTime() > Date.now()
}

// 获取待入职用户列表
const fetchPendingUsers = async () => {
  loading.value = true
  try {
    const res = await getPendingUsers({
      page: currentPage.value,
      page_size: pageSize.value
    })
    pendingUsers.value = res.data?.data || []
    total.value = res.data?.total || 0
  } catch (error) {
    console.error('获取待入职用户列表失败:', error)
    ElMessage.error('获取待入职用户列表失败')
  } finally {
    loading.value = false
  }
}

// 获取部门树
const fetchDepartmentTree = async () => {
  try {
    const res = await getDepartmentTree()
    departmentTree.value = res.data?.data || []
  } catch (error) {
    console.error('获取部门树失败:', error)
  }
}

// 获取岗位列表
const fetchPostList = async () => {
  try {
    const res = await getPostList({ only_active: true })
    postList.value = res.data?.data || []
  } catch (error) {
    console.error('获取岗位列表失败:', error)
  }
}

// 打开入职办理对话框
const openOnboardingDialog = (user) => {
  selectedUser.value = user
  onboardingForm.user_id = user.id
  onboardingForm.department = null
  onboardingForm.post = null
  onboardingForm.hire_date = ''
  onboardingForm.salary_base = 0
  dialogVisible.value = true
}

// 关闭对话框
const handleDialogClose = () => {
  onboardingFormRef.value?.resetFields()
  selectedUser.value = null
}

// 提交入职表单
const handleSubmit = async (formEl) => {
  if (!formEl) return

  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        await createEmployee({
          user_id: onboardingForm.user_id,
          department: onboardingForm.department,
          post: onboardingForm.post,
          hire_date: onboardingForm.hire_date,
          salary_base: onboardingForm.salary_base
        })
        ElMessage.success('入职办理成功')
        dialogVisible.value = false
        fetchPendingUsers()
      } catch (error) {
        console.error('入职办理失败:', error)
        ElMessage.error(error.response?.data?.message || '入职办理失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchPendingUsers()
  fetchDepartmentTree()
  fetchPostList()
})
</script>

<style scoped>
.onboarding-container {
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

.user-list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-weight: 600;
  font-size: 16px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.user-info-display {
  background: #f5f7fa;
  padding: 10px 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-info-display .name {
  font-weight: 600;
  color: #303133;
}

.user-info-display .username {
  color: #909399;
  font-size: 13px;
}
</style>
