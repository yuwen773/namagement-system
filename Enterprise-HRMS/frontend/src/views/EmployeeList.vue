<template>
  <div class="employee-list">
    <div class="page-header">
      <h2>员工管理</h2>
      <el-button type="primary" @click="handleOnboarding">
        <el-icon><Plus /></el-icon> 入职办理
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="全部" clearable @change="fetchEmployees">
            <el-option label="在职" value="active" />
            <el-option label="待入职" value="pending" />
            <el-option label="已离职" value="resigned" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <!-- 员工列表 -->
    <el-table :data="employeeList" v-loading="loading" stripe border>
      <el-table-column prop="employee_no" label="工号" width="160" />
      <el-table-column prop="real_name" label="姓名" width="100" />
      <el-table-column prop="department_name" label="部门" min-width="120" />
      <el-table-column prop="post_name" label="岗位" width="120" />
      <el-table-column prop="hire_date" label="入职日期" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="viewDetail(row)">
            查看详情
          </el-button>
          <el-button
            v-if="row.status === 'active'"
            type="warning"
            link
            size="small"
            @click="handleResign(row)"
          >
            离职
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 空状态 -->
    <el-empty v-if="!loading && employeeList.length === 0" description="暂无员工数据" />

    <!-- 员工详情抽屉 -->
    <el-drawer v-model="drawerVisible" title="员工详情" size="400px">
      <el-descriptions v-if="currentEmployee" :column="1" border>
        <el-descriptions-item label="工号">{{ currentEmployee.employee_no }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentEmployee.real_name }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ currentEmployee.username }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentEmployee.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentEmployee.email }}</el-descriptions-item>
        <el-descriptions-item label="部门">{{ currentEmployee.department_name }}</el-descriptions-item>
        <el-descriptions-item label="岗位">{{ currentEmployee.post_name }}</el-descriptions-item>
        <el-descriptions-item label="入职日期">{{ currentEmployee.hire_date }}</el-descriptions-item>
        <el-descriptions-item label="基本工资">¥{{ Number(currentEmployee?.salary_base || 0).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentEmployee.status)">
            {{ getStatusText(currentEmployee.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentEmployee.resigned_date" label="离职日期">
          {{ currentEmployee.resigned_date }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentEmployee.resigned_reason" label="离职原因">
          {{ currentEmployee.resigned_reason }}
        </el-descriptions-item>
      </el-descriptions>
      <div class="drawer-footer" v-if="currentEmployee?.status === 'active'">
        <el-button type="primary" @click="handleEdit(currentEmployee)">
          <el-icon><Edit /></el-icon> 编辑信息
        </el-button>
        <el-button type="warning" @click="handleResign(currentEmployee)">
          <el-icon><Switch /></el-icon> 办理离职
        </el-button>
      </div>
    </el-drawer>

    <!-- 编辑员工对话框 -->
    <el-dialog v-model="editVisible" title="编辑员工信息" width="500px">
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="100px">
        <el-form-item label="员工姓名">
          <el-input :value="currentEmployee?.real_name" disabled />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-select v-model="editForm.department" placeholder="请选择部门">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位" prop="post">
          <el-select v-model="editForm.post" placeholder="请选择岗位">
            <el-option
              v-for="post in posts"
              :key="post.id"
              :label="post.name"
              :value="post.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="入职日期" prop="hire_date">
          <el-date-picker
            v-model="editForm.hire_date"
            type="date"
            placeholder="请选择入职日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="基本工资" prop="salary_base">
          <el-input-number v-model="editForm.salary_base" :min="0" :precision="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>

    <!-- 离职办理对话框 -->
    <el-dialog v-model="resignVisible" title="办理离职" width="500px">
      <el-form ref="resignFormRef" :model="resignForm" :rules="resignRules" label-width="100px">
        <el-form-item label="员工姓名">
          <el-input :value="currentEmployee?.real_name" disabled />
        </el-form-item>
        <el-form-item label="离职日期" prop="resigned_date">
          <el-date-picker
            v-model="resignForm.resigned_date"
            type="date"
            placeholder="请选择离职日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="离职原因" prop="resigned_reason">
          <el-input
            v-model="resignForm.resigned_reason"
            type="textarea"
            :rows="3"
            placeholder="请输入离职原因（选填）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resignVisible = false">取消</el-button>
        <el-button type="warning" @click="submitResign" :loading="submitting">确认离职</el-button>
      </template>
    </el-dialog>

    <!-- 入职办理对话框 -->
    <el-dialog v-model="onboardingVisible" title="入职办理" width="500px">
      <el-form ref="onboardingFormRef" :model="onboardingForm" :rules="onboardingRules" label-width="100px">
        <el-form-item label="选择用户" prop="user_id">
          <el-select v-model="onboardingForm.user_id" placeholder="请选择待入职用户" filterable>
            <el-option
              v-for="user in pendingUsers"
              :key="user.id"
              :label="`${user.real_name} (${user.username})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-select v-model="onboardingForm.department" placeholder="请选择部门">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位" prop="post">
          <el-select v-model="onboardingForm.post" placeholder="请选择岗位">
            <el-option
              v-for="post in posts"
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
            placeholder="请选择入职日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="基本工资" prop="salary_base">
          <el-input-number v-model="onboardingForm.salary_base" :min="0" :precision="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="onboardingVisible = false">取消</el-button>
        <el-button type="primary" @click="submitOnboarding" :loading="submitting">确认入职</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Switch } from '@element-plus/icons-vue'
import { getEmployeeList, getEmployeeDetail, getPendingUsers, createEmployee, updateEmployee, resignEmployee } from '@/api/employee'
import { getDepartmentList } from '@/api/department'
import { getPostList } from '@/api/post'

// 员工列表
const employeeList = ref([])
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  status: ''
})

// 详情抽屉
const drawerVisible = ref(false)
const currentEmployee = ref(null)

// 编辑对话框
const editVisible = ref(false)
const editFormRef = ref(null)
const editForm = reactive({
  department: null,
  post: null,
  hire_date: '',
  salary_base: 0
})
const editRules = {
  department: [{ required: true, message: '请选择部门', trigger: 'change' }],
  post: [{ required: true, message: '请选择岗位', trigger: 'change' }],
  hire_date: [{ required: true, message: '请选择入职日期', trigger: 'change' }],
  salary_base: [{ required: true, message: '请输入基本工资', trigger: 'blur' }]
}

// 离职对话框
const resignVisible = ref(false)
const resignFormRef = ref(null)
const resignForm = reactive({
  resigned_date: '',
  resigned_reason: ''
})
const resignRules = {
  resigned_date: [{ required: true, message: '请选择离职日期', trigger: 'change' }]
}

// 入职办理
const onboardingVisible = ref(false)
const onboardingFormRef = ref(null)
const submitting = ref(false)
const onboardingForm = reactive({
  user_id: null,
  department: null,
  post: null,
  hire_date: '',
  salary_base: 5000
})
const pendingUsers = ref([])
const departments = ref([])
const posts = ref([])

// 表单验证规则
const onboardingRules = {
  user_id: [{ required: true, message: '请选择用户', trigger: 'change' }],
  department: [{ required: true, message: '请选择部门', trigger: 'change' }],
  post: [{ required: true, message: '请选择岗位', trigger: 'change' }],
  hire_date: [{ required: true, message: '请选择入职日期', trigger: 'change' }],
  salary_base: [{ required: true, message: '请输入基本工资', trigger: 'blur' }]
}

// 状态映射
const statusMap = {
  active: { type: 'success', text: '在职' },
  pending: { type: 'warning', text: '待入职' },
  resigned: { type: 'info', text: '已离职' }
}

const getStatusType = (status) => statusMap[status]?.type || 'info'
const getStatusText = (status) => statusMap[status]?.text || status

// 获取员工列表
const fetchEmployees = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterForm.status) {
      params.status = filterForm.status
    }
    const res = await getEmployeeList(params)
    employeeList.value = res.data?.data || []
  } catch (error) {
    console.error('获取员工列表失败:', error)
    ElMessage.error('获取员工列表失败')
  } finally {
    loading.value = false
  }
}

// 查看员工详情
const viewDetail = async (row) => {
  try {
    const res = await getEmployeeDetail(row.id)
    currentEmployee.value = res.data.data
    drawerVisible.value = true
  } catch (error) {
    console.error('获取员工详情失败:', error)
    ElMessage.error('获取员工详情失败')
  }
}

// 打开编辑对话框
const handleEdit = (employee) => {
  editForm.department = employee.department
  editForm.post = employee.post
  editForm.hire_date = employee.hire_date
  editForm.salary_base = employee.salary_base
  editVisible.value = true
}

// 提交编辑
const submitEdit = async () => {
  if (!editFormRef.value) return

  try {
    await editFormRef.value.validate()
    submitting.value = true

    await updateEmployee(currentEmployee.value.id, {
      department: editForm.department,
      post: editForm.post,
      hire_date: editForm.hire_date,
      salary_base: editForm.salary_base
    })

    ElMessage.success('更新成功')
    editVisible.value = false
    drawerVisible.value = false
    fetchEmployees()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('更新员工信息失败:', error)
      ElMessage.error(error.response?.data?.message || '更新失败')
    }
  } finally {
    submitting.value = false
  }
}

// 打开离职对话框
const handleResign = (employee) => {
  currentEmployee.value = employee
  resignForm.resigned_date = ''
  resignForm.resigned_reason = ''
  resignVisible.value = true
}

// 提交离职
const submitResign = async () => {
  if (!resignFormRef.value) return

  try {
    await resignFormRef.value.validate()
    submitting.value = true

    await ElMessageBox.confirm(
      '确定要办理离职吗？离职后该员工账号将被禁用。',
      '离职确认',
      {
        confirmButtonText: '确定离职',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await resignEmployee(currentEmployee.value.id, {
      resigned_date: resignForm.resigned_date,
      resigned_reason: resignForm.resigned_reason
    })

    ElMessage.success('离职办理成功')
    resignVisible.value = false
    drawerVisible.value = false
    fetchEmployees()
  } catch (error) {
    if (error !== 'confirm') {
      if (error !== 'cancel') {
        console.error('离职办理失败:', error)
        ElMessage.error(error.response?.data?.message || '离职办理失败')
      }
    }
  } finally {
    submitting.value = false
  }
}

// 入职办理
const handleOnboarding = async () => {
  onboardingForm.user_id = null
  onboardingForm.department = null
  onboardingForm.post = null
  onboardingForm.hire_date = ''
  onboardingForm.salary_base = 5000

  // 加载待入职用户
  try {
    const [usersRes, deptsRes, postsRes] = await Promise.all([
      getPendingUsers(),
      getDepartmentList(),
      getPostList({ only_active: true })
    ])
    pendingUsers.value = usersRes.data?.data || []
    departments.value = deptsRes.data?.data || []
    posts.value = postsRes.data?.data || []

    if (pendingUsers.value.length === 0) {
      ElMessage.warning('暂无待入职用户')
      return
    }

    onboardingVisible.value = true
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  }
}

// 提交入职
const submitOnboarding = async () => {
  if (!onboardingFormRef.value) return

  try {
    await onboardingFormRef.value.validate()
    submitting.value = true

    await createEmployee({
      user_id: onboardingForm.user_id,
      department: onboardingForm.department,
      post: onboardingForm.post,
      hire_date: onboardingForm.hire_date,
      salary_base: onboardingForm.salary_base
    })

    ElMessage.success('入职办理成功')
    onboardingVisible.value = false
    fetchEmployees()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('入职办理失败:', error)
      ElMessage.error(error.response?.data?.message || '入职办理失败')
    }
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchEmployees()
})
</script>

<style scoped>
.employee-list {
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

.filter-section {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.drawer-footer {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 10px;
}
</style>
