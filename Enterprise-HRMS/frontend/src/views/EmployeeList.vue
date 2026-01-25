<template>
  <div class="employee-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <span class="page-title">员工管理</span>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="handleOnboarding">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          入职办理
        </el-button>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-content">
        <div class="filter-item">
          <label class="filter-label">状态</label>
          <el-select v-model="filterForm.status" placeholder="全部" clearable @change="fetchEmployees" class="filter-select">
            <el-option label="在职" value="active" />
            <el-option label="待入职" value="pending" />
            <el-option label="已离职" value="resigned" />
          </el-select>
        </div>
      </div>
    </div>

    <!-- 员工列表 -->
    <div class="table-section">
      <el-table :data="employeeList" v-loading="loading" stripe class="custom-table">
        <el-table-column prop="employee_no" label="工号" width="160" />
        <el-table-column prop="real_name" label="姓名" width="100">
          <template #default="{ row }">
            <div class="employee-name">
              <div class="name-avatar">{{ row.real_name?.charAt(0) }}</div>
              <span>{{ row.real_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="department_name" label="部门" min-width="120" />
        <el-table-column prop="post_name" label="岗位" width="120" />
        <el-table-column prop="hire_date" label="入职日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small" class="status-tag">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)" class="action-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              查看详情
            </el-button>
            <el-button
              v-if="row.status === 'active'"
              type="warning"
              link
              size="small"
              @click="handleResign(row)"
              class="action-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              离职
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchEmployees"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 空状态 -->
    <el-empty v-if="!loading && employeeList.length === 0" description="暂无员工数据" />

    <!-- 员工详情抽屉 -->
    <el-drawer v-model="drawerVisible" title="员工详情" size="420px">
      <div v-if="currentEmployee" class="drawer-content">
        <div class="employee-header">
          <div class="avatar-large">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <div class="info">
            <h3>{{ currentEmployee.real_name }}</h3>
            <p>{{ currentEmployee.employee_no }}</p>
          </div>
          <el-tag :type="getStatusType(currentEmployee.status)" class="status-badge">
            {{ getStatusText(currentEmployee.status) }}
          </el-tag>
        </div>

        <el-descriptions :column="1" border class="info-descriptions">
          <el-descriptions-item label="用户名">{{ currentEmployee.username }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentEmployee.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ currentEmployee.email }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{ currentEmployee.department_name }}</el-descriptions-item>
          <el-descriptions-item label="岗位">{{ currentEmployee.post_name }}</el-descriptions-item>
          <el-descriptions-item label="入职日期">{{ currentEmployee.hire_date }}</el-descriptions-item>
          <el-descriptions-item label="基本工资">
            <span class="salary-highlight">¥{{ Number(currentEmployee?.salary_base || 0).toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item v-if="currentEmployee.resigned_date" label="离职日期">
            {{ currentEmployee.resigned_date }}
          </el-descriptions-item>
          <el-descriptions-item v-if="currentEmployee.resigned_reason" label="离职原因">
            {{ currentEmployee.resigned_reason }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="drawer-footer" v-if="currentEmployee?.status === 'active'">
          <el-button type="primary" @click="handleEdit(currentEmployee)" class="footer-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            编辑信息
          </el-button>
          <el-button type="warning" @click="handleResign(currentEmployee)" class="footer-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            办理离职
          </el-button>
        </div>
      </div>
    </el-drawer>

    <!-- 编辑员工对话框 -->
    <el-dialog v-model="editVisible" title="编辑员工信息" width="500px">
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="100px" class="custom-form">
        <el-form-item label="员工姓名">
          <el-input :value="currentEmployee?.real_name" disabled class="form-input" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-select v-model="editForm.department" placeholder="请选择部门" class="form-input">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位" prop="post">
          <el-select v-model="editForm.post" placeholder="请选择岗位" class="form-input">
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
            class="form-input"
          />
        </el-form-item>
        <el-form-item label="基本工资" prop="salary_base">
          <el-input-number v-model="editForm.salary_base" :min="0" :precision="2" class="form-input" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>

    <!-- 离职办理对话框 -->
    <el-dialog v-model="resignVisible" title="办理离职" width="500px">
      <el-form ref="resignFormRef" :model="resignForm" :rules="resignRules" label-width="100px" class="custom-form">
        <el-form-item label="员工姓名">
          <el-input :value="currentEmployee?.real_name" disabled class="form-input" />
        </el-form-item>
        <el-form-item label="离职日期" prop="resigned_date">
          <el-date-picker
            v-model="resignForm.resigned_date"
            type="date"
            placeholder="请选择离职日期"
            value-format="YYYY-MM-DD"
            class="form-input"
          />
        </el-form-item>
        <el-form-item label="离职原因" prop="resigned_reason">
          <el-input
            v-model="resignForm.resigned_reason"
            type="textarea"
            :rows="3"
            placeholder="请输入离职原因（选填）"
            class="form-input"
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
      <el-form ref="onboardingFormRef" :model="onboardingForm" :rules="onboardingRules" label-width="100px" class="custom-form">
        <el-form-item label="选择用户" prop="user_id">
          <el-select v-model="onboardingForm.user_id" placeholder="请选择待入职用户" filterable class="form-input">
            <el-option
              v-for="user in pendingUsers"
              :key="user.id"
              :label="`${user.real_name} (${user.username})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-select v-model="onboardingForm.department" placeholder="请选择部门" class="form-input">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位" prop="post">
          <el-select v-model="onboardingForm.post" placeholder="请选择岗位" class="form-input">
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
            class="form-input"
          />
        </el-form-item>
        <el-form-item label="基本工资" prop="salary_base">
          <el-input-number v-model="onboardingForm.salary_base" :min="0" :precision="2" class="form-input" />
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
import { getEmployeeList, getEmployeeDetail, getPendingUsers, createEmployee, updateEmployee, resignEmployee } from '@/api/employee'
import { getDepartmentList } from '@/api/department'
import { getPostList } from '@/api/post'

// 员工列表
const employeeList = ref([])
const loading = ref(false)

// 分页状态
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

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
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    if (filterForm.status) {
      params.status = filterForm.status
    }
    const res = await getEmployeeList(params)
    if (res.data?.code === 0) {
      employeeList.value = res.data?.data || []
      pagination.total = res.data?.total || 0
    }
  } catch (error) {
    console.error('获取员工列表失败:', error)
    ElMessage.error('获取员工列表失败')
  } finally {
    loading.value = false
  }
}

// 页码变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchEmployees()
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
  editForm.department = employee.department?.id
  editForm.post = employee.post?.id
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
      department_id: editForm.department,
      post_id: editForm.post,
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

  try {
    const [usersRes, deptsRes, postsRes] = await Promise.all([
      getPendingUsers({ page: 1, page_size: 100 }),
      getDepartmentList({ only_root: true }),
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
      emp_no: `EMP${new Date().toISOString().slice(0, 7).replace('-', '')}${String(onboardingForm.department).padStart(3, '0')}`,
      department_id: onboardingForm.department,
      post_id: onboardingForm.post,
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
/* ========================================
   Employee List - Refined Corporate Design
   ======================================== */
.employee-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
}

.employee-page::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -30px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  padding: 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light), var(--color-success));
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.25);
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.5px;
}

.header-right .el-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
}

.header-right .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.header-right svg {
  width: 18px;
  height: 18px;
}

/* 筛选区域 */
.filter-section {
  padding: 20px 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  position: relative;
  z-index: 1;
}

.filter-content {
  display: flex;
  gap: 24px;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.filter-select {
  width: 140px;
}

/* 表格区域 */
.table-section {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  overflow: hidden;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  animation-delay: 0.2s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.custom-table {
  border-radius: 0;
}

.custom-table :deep(.el-table__header) {
  background: var(--color-gray-50);
}

.custom-table :deep(.el-table__header th) {
  background: transparent;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* 员工姓名列样式 */
.employee-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.name-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
}

.status-tag {
  font-weight: 500;
  border-radius: var(--radius-full);
  padding: 2px 12px;
}

/* 操作按钮 */
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--color-primary-subtle);
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 20px;
  background: var(--color-gray-50);
  border-top: 1px solid var(--color-border-light);
}

/* 抽屉样式 */
.drawer-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.employee-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--color-border-light);
  position: relative;
}

.employee-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--color-primary) 0%, transparent 100%);
}

.avatar-large {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.25);
  position: relative;
}

.avatar-large::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: var(--radius-xl);
  padding: 2px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-success));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}

.avatar-large svg {
  width: 36px;
  height: 36px;
}

.info {
  flex: 1;
}

.info h3 {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px 0;
  letter-spacing: 0.3px;
}

.info p {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

.status-badge {
  font-weight: 500;
  border-radius: var(--radius-full);
  padding: 4px 12px;
}

.info-descriptions {
  border-radius: var(--radius-md);
  overflow: hidden;
}

.info-descriptions :deep(.el-descriptions__label) {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.info-descriptions :deep(.el-descriptions__content) {
  color: var(--color-text-primary);
}

.salary-highlight {
  font-weight: 600;
  color: var(--color-success);
  font-size: 16px;
  font-family: 'SF Mono', 'Monaco', monospace;
}

.drawer-footer {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border-light);
}

.footer-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
}

.footer-btn:hover {
  transform: translateY(-2px);
}

.footer-btn svg {
  width: 18px;
  height: 18px;
}

/* 表单样式 */
.custom-form .form-input {
  width: 100%;
}

.custom-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-text-secondary);
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .filter-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .employee-header {
    flex-direction: column;
    text-align: center;
  }

  .drawer-footer {
    flex-direction: column;
  }

  .pagination-wrapper {
    justify-content: center;
  }
}
</style>
