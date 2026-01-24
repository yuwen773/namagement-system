<template>
  <div class="salary-page">
    <div class="page-header">
      <h2>薪资管理</h2>
      <el-date-picker
        v-model="selectedMonth"
        type="month"
        placeholder="选择月份"
        format="YYYY-MM"
        value-format="YYYY-MM"
        :disabled-date="disabledDate"
        @change="handleMonthChange"
      />
    </div>

    <!-- 薪资记录列表 -->
    <el-card v-loading="loading">
      <el-table :data="salaryRecords" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="real_name" label="员工姓名" width="120" />
        <el-table-column prop="month" label="月份" width="100" />
        <el-table-column prop="base_salary" label="基本工资" width="120">
          <template #default="{ row }">
            ¥{{ row.base_salary?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="final_salary" label="实发工资" width="120">
          <template #default="{ row }">
            <span style="color: #67c23a; font-weight: bold;">
              ¥{{ row.final_salary?.toLocaleString() }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'info'" size="small">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ row.created_at?.replace('T', ' ').substring(0, 19) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">
              查看详情
            </el-button>
            <el-button
              v-if="isHR && row.status === 'draft'"
              type="success"
              link
              size="small"
              @click="publishSalary(row)"
            >
              发布
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && salaryRecords.length === 0" description="暂无薪资记录" />
    </el-card>

    <!-- 薪资详情抽屉 -->
    <el-drawer v-model="detailDrawerVisible" title="薪资详情" size="400px">
      <div v-if="currentRecord" class="salary-detail">
        <div class="detail-header">
          <h3>{{ currentRecord.month }} 月薪资单</h3>
          <el-tag :type="currentRecord.status === 'published' ? 'success' : 'info'">
            {{ currentRecord.status === 'published' ? '已发布' : '草稿' }}
          </el-tag>
        </div>

        <el-descriptions :column="1" border>
          <el-descriptions-item label="员工姓名">
            {{ currentRecord.real_name }}
          </el-descriptions-item>
          <el-descriptions-item label="部门">
            {{ currentRecord.department_name || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="基本工资">
            <span class="amount">¥{{ currentRecord.base_salary?.toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="加班费">
            <span class="amount add">+¥{{ currentRecord.overtime_pay?.toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="考勤扣款">
            <span class="amount minus">-¥{{ currentRecord.attendance_deduction?.toLocaleString() }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="迟到次数">
            {{ currentRecord.late_count || 0 }} 次
          </el-descriptions-item>
          <el-descriptions-item label="早退次数">
            {{ currentRecord.early_count || 0 }} 次
          </el-descriptions-item>
        </el-descriptions>

        <div class="final-salary">
          <span>实发工资</span>
          <span class="amount-total">¥{{ currentRecord.final_salary?.toLocaleString() }}</span>
        </div>
      </div>
    </el-drawer>

    <!-- HR/管理员：薪资计算对话框 -->
    <el-dialog v-model="calculateDialogVisible" title="薪资计算" width="500px">
      <el-form ref="calculateFormRef" :model="calculateForm" :rules="calculateRules" label-width="100px">
        <el-form-item label="员工" prop="user_id">
          <el-select
            v-model="calculateForm.user_id"
            placeholder="选择员工"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="emp in employeeList"
              :key="emp.id"
              :label="`${emp.real_name} (${emp.employee_no})`"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="月份" prop="month">
          <el-date-picker
            v-model="calculateForm.month"
            type="month"
            placeholder="选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="calculateDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="calculating" @click="handleCalculate">
          计算并保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { getSalaryRecords, getSalaryRecordDetail, saveSalaryRecord } from '@/api/salary'
import { getEmployeeList } from '@/api/employee'

// 状态
const loading = ref(false)
const calculating = ref(false)
const salaryRecords = ref([])
const selectedMonth = ref(new Date().toISOString().slice(0, 7))
const detailDrawerVisible = ref(false)
const currentRecord = ref(null)
const calculateDialogVisible = ref(false)
const calculateFormRef = ref(null)
const employeeList = ref([])

// 计算表单
const calculateForm = ref({
  user_id: null,
  month: ''
})

const calculateRules = {
  user_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  month: [{ required: true, message: '请选择月份', trigger: 'change' }]
}

// 权限判断
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const isHR = computed(() => ['hr', 'admin'].includes(user.value?.role))

// 禁用未来月份
const disabledDate = (time) => {
  return time.getTime() > Date.now()
}

// 获取薪资记录列表
const fetchSalaryRecords = async () => {
  if (!selectedMonth.value) return

  loading.value = true
  try {
    const params = { month: selectedMonth.value }
    const res = await getSalaryRecords(params)
    if (res.data?.code === 0) {
      salaryRecords.value = res.data.data || []
    }
  } catch (error) {
    console.error('获取薪资记录失败:', error)
    ElMessage.error('获取薪资记录失败')
  } finally {
    loading.value = false
  }
}

// 月份切换
const handleMonthChange = () => {
  fetchSalaryRecords()
}

// 查看详情
const viewDetail = async (row) => {
  try {
    const res = await getSalaryRecordDetail(row.id)
    if (res.data?.code === 0) {
      currentRecord.value = res.data.data
      detailDrawerVisible.value = true
    }
  } catch (error) {
    console.error('获取详情失败:', error)
    ElMessage.error('获取详情失败')
  }
}

// 发布薪资
const publishSalary = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认发布 ${row.real_name} 的 ${row.month} 月薪资？`,
      '发布确认',
      { type: 'warning' }
    )

    // TODO: 实现发布接口
    ElMessage.success('薪资已发布')
    fetchSalaryRecords()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发布失败:', error)
    }
  }
}

// 获取员工列表（用于计算薪资）
const fetchEmployeeList = async () => {
  try {
    const res = await getEmployeeList({ status: 'active' })
    if (res.data?.code === 0) {
      employeeList.value = res.data.data || []
    }
  } catch (error) {
    console.error('获取员工列表失败:', error)
  }
}

// 打开计算对话框
const openCalculateDialog = () => {
  calculateForm.value = {
    user_id: null,
    month: selectedMonth.value || new Date().toISOString().slice(0, 7)
  }
  calculateDialogVisible.value = true
}

// 计算并保存薪资
const handleCalculate = async () => {
  if (!calculateFormRef.value) return

  try {
    await calculateFormRef.value.validate()
    calculating.value = true

    const res = await saveSalaryRecord(calculateForm.value)
    if (res.data?.code === 0) {
      ElMessage.success('薪资计算并保存成功')
      calculateDialogVisible.value = false
      fetchSalaryRecords()
    } else {
      ElMessage.error(res.data?.message || '保存失败')
    }
  } catch (error) {
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error !== 'cancel') {
      ElMessage.error('保存失败')
    }
  } finally {
    calculating.value = false
  }
}

// 初始化
onMounted(() => {
  fetchSalaryRecords()
  if (isHR.value) {
    fetchEmployeeList()
  }
})
</script>

<style scoped>
.salary-page {
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

.salary-detail {
  padding: 0 10px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.detail-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.amount {
  font-weight: bold;
  color: #303133;
}

.amount.add {
  color: #67c23a;
}

.amount.minus {
  color: #f56c6c;
}

.final-salary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.final-salary span:first-child {
  font-size: 16px;
  color: #606266;
}

.amount-total {
  font-size: 28px;
  font-weight: bold;
  color: #67c23a;
}
</style>
