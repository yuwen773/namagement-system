<template>
  <div class="employee-manage-view">
    <!-- 顶部操作栏 -->
    <div class="action-bar">
      <el-button type="primary" :icon="Plus" @click="handleAdd">
        新增员工
      </el-button>
      <div class="search-area">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索姓名、电话、身份证号"
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
          v-model="filters.position"
          placeholder="岗位筛选"
          clearable
          style="width: 150px"
          @change="handleFilter"
        >
          <el-option label="厨师" value="CHEF" />
          <el-option label="面点" value="PASTRY" />
          <el-option label="切配" value="PREP" />
          <el-option label="保洁" value="CLEANER" />
          <el-option label="服务员" value="SERVER" />
          <el-option label="经理" value="MANAGER" />
        </el-select>
        <el-select
          v-model="filters.status"
          placeholder="状态筛选"
          clearable
          style="width: 150px"
          @change="handleFilter"
        >
          <el-option label="在职" value="ACTIVE" />
          <el-option label="离职" value="INACTIVE" />
          <el-option label="停薪留职" value="LEAVE_WITHOUT_PAY" />
        </el-select>
      </div>
    </div>

    <!-- 员工列表表格 -->
    <el-table
      v-loading="loading"
      :data="employeeList"
      stripe
      style="width: 100%"
      :header-cell-style="{ background: '#FFF8F0', color: '#333' }"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="gender_display" label="性别" width="80">
        <template #default="{ row }">
          <el-tag :type="row.gender === 'MALE' ? 'primary' : 'danger'" size="small">
            {{ row.gender_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="position_display" label="岗位" width="100">
        <template #default="{ row }">
          <el-tag :type="getPositionTagType(row.position)" size="small">
            {{ row.position_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="id_card" label="身份证号" width="180" />
      <el-table-column prop="entry_date" label="入职日期" width="120" />
      <el-table-column prop="status_display" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusTagType(row.status)" size="small">
            {{ row.status_display }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleView(row)">
            查看
          </el-button>
          <el-button link type="primary" size="small" @click="handleEdit(row)">
            编辑
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-tabs v-model="activeTab">
          <!-- 基础信息 -->
          <el-tab-pane label="基础信息" name="basic">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="formData.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="formData.gender">
                <el-radio value="MALE">男</el-radio>
                <el-radio value="FEMALE">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item label="身份证号" prop="id_card">
              <el-input v-model="formData.id_card" placeholder="请输入身份证号" />
            </el-form-item>
            <el-form-item label="家庭住址" prop="address">
              <el-input
                v-model="formData.address"
                type="textarea"
                :rows="2"
                placeholder="请输入家庭住址"
              />
            </el-form-item>
          </el-tab-pane>

          <!-- 岗位信息 -->
          <el-tab-pane label="岗位信息" name="position">
            <el-form-item label="岗位" prop="position">
              <el-select v-model="formData.position" placeholder="请选择岗位">
                <el-option label="厨师" value="CHEF" />
                <el-option label="面点" value="PASTRY" />
                <el-option label="切配" value="PREP" />
                <el-option label="保洁" value="CLEANER" />
                <el-option label="服务员" value="SERVER" />
                <el-option label="经理" value="MANAGER" />
              </el-select>
            </el-form-item>
            <el-form-item label="入职日期" prop="entry_date">
              <el-date-picker
                v-model="formData.entry_date"
                type="date"
                placeholder="请选择入职日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择状态">
                <el-option label="在职" value="ACTIVE" />
                <el-option label="离职" value="INACTIVE" />
                <el-option label="停薪留职" value="LEAVE_WITHOUT_PAY" />
              </el-select>
            </el-form-item>
          </el-tab-pane>

          <!-- 资质证书 -->
          <el-tab-pane label="资质证书" name="certificate">
            <el-form-item label="健康证号" prop="health_certificate_no">
              <el-input v-model="formData.health_certificate_no" placeholder="请输入健康证号" />
            </el-form-item>
            <el-form-item label="健康证有效期" prop="health_certificate_expiry">
              <el-date-picker
                v-model="formData.health_certificate_expiry"
                type="date"
                placeholder="请选择有效期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="健康证图片" prop="health_certificate_url">
              <el-input v-model="formData.health_certificate_url" placeholder="请输入图片URL" />
            </el-form-item>
            <el-form-item label="厨师等级证" prop="chef_certificate_level">
              <el-select v-model="formData.chef_certificate_level" placeholder="请选择等级" clearable>
                <el-option label="初级厨师" value="初级" />
                <el-option label="中级厨师" value="中级" />
                <el-option label="高级厨师" value="高级" />
                <el-option label="技师" value="技师" />
                <el-option label="高级技师" value="高级技师" />
              </el-select>
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="员工档案详情" width="700px">
      <div v-if="currentEmployee" class="employee-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ currentEmployee.name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ currentEmployee.gender_display }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentEmployee.phone }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ currentEmployee.id_card || '-' }}</el-descriptions-item>
          <el-descriptions-item label="家庭住址" :span="2">{{ currentEmployee.address || '-' }}</el-descriptions-item>
          <el-descriptions-item label="岗位">{{ currentEmployee.position_display }}</el-descriptions-item>
          <el-descriptions-item label="入职日期">{{ currentEmployee.entry_date }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTagType(currentEmployee.status)">
              {{ currentEmployee.status_display }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentEmployee.created_at }}</el-descriptions-item>
          <el-descriptions-item label="健康证号">{{ currentEmployee.health_certificate_no || '-' }}</el-descriptions-item>
          <el-descriptions-item label="健康证有效期">
            {{ currentEmployee.health_certificate_expiry || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="厨师等级证">
            {{ currentEmployee.chef_certificate_level || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentEmployee.updated_at }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button type="primary" @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import {
  getEmployeeList,
  getEmployeeDetail,
  createEmployee,
  updateEmployee,
  deleteEmployee
} from '@/api/employee'

// 数据列表
const loading = ref(false)
const employeeList = ref([])
const searchKeyword = ref('')

// 筛选条件
const filters = reactive({
  position: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = computed(() => (isEdit.value ? '编辑员工' : '新增员工'))
const isEdit = ref(false)
const activeTab = ref('basic')

// 表单
const formRef = ref(null)
const submitting = ref(false)
const formData = reactive({
  name: '',
  gender: 'MALE',
  phone: '',
  id_card: '',
  address: '',
  position: '',
  entry_date: '',
  status: 'ACTIVE',
  health_certificate_no: '',
  health_certificate_expiry: '',
  health_certificate_url: '',
  chef_certificate_level: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  position: [{ required: true, message: '请选择岗位', trigger: 'change' }],
  entry_date: [{ required: true, message: '请选择入职日期', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 当前员工
const currentEmployee = ref(null)

// 加载员工列表
const loadEmployeeList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ordering: '-created_at'
    }
    if (filters.position) params.position = filters.position
    if (filters.status) params.status = filters.status
    if (searchKeyword.value) params.search = searchKeyword.value

    const res = await getEmployeeList(params)
    if (res.code === 200) {
      employeeList.value = res.data.results || res.data
      pagination.total = res.data.count || res.data.length
    } else {
      ElMessage.error(res.message || '加载员工列表失败')
    }
  } catch (error) {
    console.error('加载员工列表失败:', error)
    ElMessage.error('加载员工列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadEmployeeList()
}

// 筛选
const handleFilter = () => {
  pagination.page = 1
  loadEmployeeList()
}

// 分页
const handlePageChange = () => {
  loadEmployeeList()
}

const handleSizeChange = () => {
  pagination.page = 1
  loadEmployeeList()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(formData, {
    id: row.id,
    name: row.name,
    gender: row.gender,
    phone: row.phone,
    id_card: row.id_card || '',
    address: row.address || '',
    position: row.position,
    entry_date: row.entry_date,
    status: row.status,
    health_certificate_no: row.health_certificate_no || '',
    health_certificate_expiry: row.health_certificate_expiry || '',
    health_certificate_url: row.health_certificate_url || '',
    chef_certificate_level: row.chef_certificate_level || ''
  })
  activeTab.value = 'basic'
  dialogVisible.value = true
}

// 查看
const handleView = async (row) => {
  try {
    const res = await getEmployeeDetail(row.id)
    if (res.code === 200) {
      currentEmployee.value = res.data
      detailVisible.value = true
    } else {
      ElMessage.error(res.message || '获取员工详情失败')
    }
  } catch (error) {
    console.error('获取员工详情失败:', error)
    ElMessage.error('获取员工详情失败')
  }
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除员工 "${row.name}" 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        const res = await deleteEmployee(row.id)
        if (res.code === 200) {
          ElMessage.success('删除成功')
          loadEmployeeList()
        } else {
          ElMessage.error(res.message || '删除失败')
        }
      } catch (error) {
        console.error('删除员工失败:', error)
        ElMessage.error('删除员工失败')
      }
    })
    .catch(() => {})
}

// 提交表单
const handleSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      const data = { ...formData }
      delete data.id

      let res
      if (isEdit.value) {
        res = await updateEmployee(formData.id, data)
      } else {
        res = await createEmployee(data)
      }

      if (res.code === 200 || res.code === 201) {
        ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        loadEmployeeList()
      } else {
        ElMessage.error(res.message || '操作失败')
      }
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    } finally {
      submitting.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    name: '',
    gender: 'MALE',
    phone: '',
    id_card: '',
    address: '',
    position: '',
    entry_date: '',
    status: 'ACTIVE',
    health_certificate_no: '',
    health_certificate_expiry: '',
    health_certificate_url: '',
    chef_certificate_level: ''
  })
  formRef.value?.clearValidate()
}

// 岗位标签颜色
const getPositionTagType = (position) => {
  const typeMap = {
    CHEF: 'warning',      // 厨师 - 橙色
    PASTRY: 'danger',     // 面点 - 红色
    PREP: 'info',         // 切配 - 蓝色
    CLEANER: 'success',   // 保洁 - 绿色
    SERVER: '',           // 服务员 - 默认灰色
    MANAGER: 'primary'    // 经理 - 深蓝色
  }
  return typeMap[position] || ''
}

// 状态标签颜色
const getStatusTagType = (status) => {
  const typeMap = {
    ACTIVE: 'success',             // 在职 - 绿色
    INACTIVE: 'info',              // 离职 - 灰色
    LEAVE_WITHOUT_PAY: 'warning'   // 停薪留职 - 橙色
  }
  return typeMap[status] || ''
}

// 初始化
onMounted(() => {
  loadEmployeeList()
})
</script>

<style scoped>
.employee-manage-view {
  padding: 20px;
  background-color: #fff8f0;
  min-height: 100vh;
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

.search-area {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.filter-area {
  display: flex;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

.employee-detail {
  padding: 10px;
}

/* 食堂主题样式优化 */
:deep(.el-button--primary) {
  background-color: #ff6b35;
  border-color: #ff6b35;
}

:deep(.el-button--primary:hover) {
  background-color: #ff8c42;
  border-color: #ff8c42;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(255, 107, 53, 0.08);
}

:deep(.el-dialog) {
  border-radius: 16px;
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 50%, #f7c52d 100%);
  color: white;
  border-radius: 16px 16px 0 0;
  padding: 20px;
}

:deep(.el-dialog__title) {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-tabs__item.is-active) {
  color: #ff6b35;
}

:deep(.el-tabs__active-bar) {
  background-color: #ff6b35;
}

:deep(.el-tag--warning) {
  background-color: #fff3e0;
  border-color: #ffb74d;
  color: #f57c00;
}

:deep(.el-tag--success) {
  background-color: #e8f5e9;
  border-color: #81c784;
  color: #2e7d32;
}

:deep(.el-tag--info) {
  background-color: #e3f2fd;
  border-color: #64b5f6;
  color: #1565c0;
}

:deep(.el-tag--primary) {
  background-color: #ffe0b2;
  border-color: #ffcc80;
  color: #e65100;
}

:deep(.el-tag--danger) {
  background-color: #ffebee;
  border-color: #ef5350;
  color: #c62828;
}

:deep(.el-descriptions) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-descriptions__label) {
  background-color: #fff8f0 !important;
  font-weight: 600;
}
</style>
