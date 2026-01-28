<template>
  <div class="schedule-manage-view">
    <!-- 顶部操作栏 -->
    <div class="top-bar">
      <div class="date-picker-wrapper">
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

      <div class="view-switcher">
        <el-radio-group v-model="viewMode" @change="handleViewModeChange">
          <el-radio-button value="calendar">
            <el-icon><Calendar /></el-icon>
            日历视图
          </el-radio-button>
          <el-radio-button value="list">
            <el-icon><List /></el-icon>
            列表视图
          </el-radio-button>
        </el-radio-group>
      </div>

      <div class="actions">
        <el-button type="primary" @click="handleBatchCreate">
          <el-icon><Plus /></el-icon>
          批量排班
        </el-button>
        <el-button @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 日历视图 -->
    <div v-if="viewMode === 'calendar'" class="calendar-view" v-loading="loading">
      <el-calendar v-model="calendarDate">
        <template #date-cell="{ data }">
          <div class="calendar-cell">
            <div class="date-number">{{ data.day.split('-').slice(-1)[0] }}</div>
            <div class="schedule-list">
              <div
                v-for="schedule in getSchedulesForDate(data.day)"
                :key="schedule.id"
                class="schedule-item"
                :class="{ 'is-swapped': schedule.is_swapped }"
                @click="handleViewSchedule(schedule)"
              >
                <el-tag :type="getShiftTagType(schedule.shift_name)" size="small">
                  {{ schedule.employee_name }}
                </el-tag>
                <span class="shift-name">{{ schedule.shift_name }}</span>
                <el-icon v-if="schedule.is_swapped" class="swap-icon"><RefreshRight /></el-icon>
              </div>
            </div>
          </div>
        </template>
      </el-calendar>
    </div>

    <!-- 列表视图 -->
    <div v-else class="list-view" v-loading="loading">
      <el-table :data="scheduleList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="employee_name" label="员工姓名" width="120" />
        <el-table-column prop="shift_name" label="班次" width="120">
          <template #default="{ row }">
            <el-tag :type="getShiftTagType(row.shift_name)">
              {{ row.shift_name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="work_date" label="排班日期" width="120" />
        <el-table-column prop="start_time" label="开始时间" width="100" />
        <el-table-column prop="end_time" label="结束时间" width="100" />
        <el-table-column prop="is_swapped" label="是否调班" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_swapped" type="warning" size="small">已调班</el-tag>
            <el-tag v-else type="info" size="small">正常</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleViewSchedule(row)">查看</el-button>
            <el-button link type="primary" @click="handleEditSchedule(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDeleteSchedule(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 批量排班对话框 -->
    <el-dialog
      v-model="batchDialogVisible"
      title="批量排班"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="batchForm" :rules="batchRules" ref="batchFormRef" label-width="100px">
        <el-form-item label="员工" prop="employee_ids">
          <el-select
            v-model="batchForm.employee_ids"
            multiple
            placeholder="请选择员工"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="employee in employeeList"
              :key="employee.id"
              :label="`${employee.name} - ${employee.position_display}`"
              :value="employee.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="班次" prop="shift_id">
          <el-select v-model="batchForm.shift_id" placeholder="请选择班次" style="width: 100%">
            <el-option
              v-for="shift in shiftList"
              :key="shift.id"
              :label="`${shift.name} (${shift.start_time} - ${shift.end_time})`"
              :value="shift.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="日期范围" prop="dateRange">
          <el-date-picker
            v-model="batchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="batchDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmBatch" :loading="batchLoading">
          确认批量排班
        </el-button>
      </template>
    </el-dialog>

    <!-- 排班详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="排班详情"
      width="500px"
    >
      <el-descriptions :column="2" border v-if="currentSchedule">
        <el-descriptions-item label="员工姓名">
          {{ currentSchedule.employee_name }}
        </el-descriptions-item>
        <el-descriptions-item label="岗位">
          {{ currentSchedule.employee_position }}
        </el-descriptions-item>
        <el-descriptions-item label="班次">
          <el-tag :type="getShiftTagType(currentSchedule.shift_name)">
            {{ currentSchedule.shift_name }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="排班日期">
          {{ currentSchedule.work_date }}
        </el-descriptions-item>
        <el-descriptions-item label="开始时间">
          {{ currentSchedule.start_time }}
        </el-descriptions-item>
        <el-descriptions-item label="结束时间">
          {{ currentSchedule.end_time }}
        </el-descriptions-item>
        <el-descriptions-item label="是否调班" :span="2">
          <el-tag v-if="currentSchedule.is_swapped" type="warning">已调班</el-tag>
          <el-tag v-else type="info">正常</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEditFromDetail">编辑</el-button>
      </template>
    </el-dialog>

    <!-- 编辑排班对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑排班"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item label="员工" prop="employee">
          <el-select v-model="editForm.employee_id" placeholder="请选择员工" style="width: 100%">
            <el-option
              v-for="employee in employeeList"
              :key="employee.id"
              :label="`${employee.name} - ${employee.position_display}`"
              :value="employee.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="班次" prop="shift_id">
          <el-select v-model="editForm.shift_id" placeholder="请选择班次" style="width: 100%">
            <el-option
              v-for="shift in shiftList"
              :key="shift.id"
              :label="`${shift.name} (${shift.start_time} - ${shift.end_time})`"
              :value="shift.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="排班日期" prop="work_date">
          <el-date-picker
            v-model="editForm.work_date"
            type="date"
            placeholder="请选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmEdit" :loading="editLoading">
          确认修改
        </el-button>
      </template>
    </el-dialog>

    <!-- 调班审批对话框 -->
    <el-dialog
      v-model="approvalDialogVisible"
      title="调班审批"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-descriptions :column="2" border v-if="currentRequest">
        <el-descriptions-item label="申请人">
          {{ currentRequest.requester_name }}
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">
          {{ formatDate(currentRequest.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="原班次" :span="2">
          {{ currentRequest.original_schedule_info }}
        </el-descriptions-item>
        <el-descriptions-item label="期望调整" :span="2">
          {{ currentRequest.target_schedule_info }}
        </el-descriptions-item>
        <el-descriptions-item label="申请原因" :span="2">
          {{ currentRequest.reason || '-' }}
        </el-descriptions-item>
      </el-descriptions>

      <el-form :model="approvalForm" :rules="approvalRules" ref="approvalFormRef" label-width="100px" style="margin-top: 20px">
        <el-form-item label="审批意见" prop="approval_remark">
          <el-input
            v-model="approvalForm.approval_remark"
            type="textarea"
            :rows="3"
            placeholder="请输入审批意见"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="approvalDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="handleReject" :loading="approvalLoading">
          拒绝
        </el-button>
        <el-button type="primary" @click="handleApprove" :loading="approvalLoading">
          批准
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, List, Plus, Refresh, RefreshRight } from '@element-plus/icons-vue'
import {
  getShiftList,
  getScheduleList,
  deleteSchedule,
  batchCreateSchedule,
  updateSchedule,
  getCalendarView,
  getPendingShiftRequests,
  approveShiftRequest
} from '@/api/schedule'
import { getEmployeeList } from '@/api/employee'

// ==================== 数据状态 ====================
const loading = ref(false)
const viewMode = ref('calendar') // calendar | list
const calendarDate = ref(new Date())
const dateRange = ref([
  // 默认显示当前月
  new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
  new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).toISOString().split('T')[0]
])

const scheduleList = ref([])
const calendarData = ref({})
const shiftList = ref([])
const employeeList = ref([])

// ==================== 对话框状态 ====================
const batchDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const editDialogVisible = ref(false)
const approvalDialogVisible = ref(false)
const batchLoading = ref(false)
const editLoading = ref(false)
const approvalLoading = ref(false)

const currentSchedule = ref(null)
const currentRequest = ref(null)

// ==================== 表单数据 ====================
const batchForm = reactive({
  employee_ids: [],
  shift_id: null,
  dateRange: []
})

const editForm = reactive({
  id: null,
  employee_id: null,
  shift_id: null,
  work_date: ''
})

const approvalForm = reactive({
  approval_remark: ''
})

// ==================== 表单验证规则 ====================
const batchRules = {
  employee_ids: [{ required: true, message: '请选择员工', trigger: 'change' }],
  shift_id: [{ required: true, message: '请选择班次', trigger: 'change' }],
  dateRange: [{ required: true, message: '请选择日期范围', trigger: 'change' }]
}

const editRules = {
  employee_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  shift_id: [{ required: true, message: '请选择班次', trigger: 'change' }],
  work_date: [{ required: true, message: '请选择排班日期', trigger: 'change' }]
}

const approvalRules = {
  approval_remark: [{ required: true, message: '请输入审批意见', trigger: 'blur' }]
}

// ==================== Ref 引用 ====================
const batchFormRef = ref(null)
const editFormRef = ref(null)
const approvalFormRef = ref(null)

// ==================== 生命周期 ====================
onMounted(() => {
  loadShifts()
  loadEmployees()
  loadSchedules()
})

// ==================== 数据加载 ====================
async function loadShifts() {
  try {
    const { data } = await getShiftList()
    shiftList.value = data.data || []
  } catch (error) {
    ElMessage.error('加载班次列表失败')
  }
}

async function loadEmployees() {
  try {
    const { data } = await getEmployeeList({ status: 'ACTIVE', page_size: 1000 })
    employeeList.value = data.data.results || []
  } catch (error) {
    ElMessage.error('加载员工列表失败')
  }
}

async function loadSchedules() {
  if (!dateRange.value || dateRange.value.length !== 2) {
    return
  }

  loading.value = true
  try {
    if (viewMode.value === 'calendar') {
      // 加载日历视图数据
      const { data } = await getCalendarView({
        start_date: dateRange.value[0],
        end_date: dateRange.value[1]
      })
      calendarData.value = data.data || {}
    } else {
      // 加载列表视图数据
      const { data } = await getScheduleList({
        work_date__gte: dateRange.value[0],
        work_date__lte: dateRange.value[1],
        ordering: 'work_date,employee_id'
      })
      scheduleList.value = data.data.results || []
    }
  } catch (error) {
    ElMessage.error('加载排班数据失败')
  } finally {
    loading.value = false
  }
}

// ==================== 事件处理 ====================
function handleDateChange() {
  loadSchedules()
}

function handleViewModeChange() {
  loadSchedules()
}

function handleRefresh() {
  loadSchedules()
  ElMessage.success('刷新成功')
}

function handleBatchCreate() {
  batchDialogVisible.value = true
}

async function handleConfirmBatch() {
  const valid = await batchFormRef.value.validate()
  if (!valid) return

  batchLoading.value = true
  try {
    const { data } = await batchCreateSchedule({
      employee_ids: batchForm.employee_ids,
      shift_id: batchForm.shift_id,
      start_date: batchForm.dateRange[0],
      end_date: batchForm.dateRange[1]
    })

    ElMessage.success(`成功创建 ${data.data.created_count} 条排班记录`)

    // 关闭对话框并重置表单
    batchDialogVisible.value = false
    batchFormRef.value.resetFields()

    // 刷新数据
    loadSchedules()
  } catch (error) {
    ElMessage.error('批量排班失败')
  } finally {
    batchLoading.value = false
  }
}

function handleViewSchedule(schedule) {
  currentSchedule.value = schedule
  detailDialogVisible.value = true
}

function handleEditFromDetail() {
  detailDialogVisible.value = false
  editForm.id = currentSchedule.value.id
  editForm.employee_id = currentSchedule.value.employee_id
  editForm.shift_id = currentSchedule.value.shift_id
  editForm.work_date = currentSchedule.value.work_date
  editDialogVisible.value = true
}

function handleEditSchedule(schedule) {
  editForm.id = schedule.id
  editForm.employee_id = schedule.employee_id
  editForm.shift_id = schedule.shift_id
  editForm.work_date = schedule.work_date
  editDialogVisible.value = true
}

async function handleConfirmEdit() {
  const valid = await editFormRef.value.validate()
  if (!valid) return

  editLoading.value = true
  try {
    await updateSchedule(editForm.id, {
      employee_id: editForm.employee_id,
      shift_id: editForm.shift_id,
      work_date: editForm.work_date
    })

    ElMessage.success('修改排班成功')
    editDialogVisible.value = false
    editFormRef.value.resetFields()
    loadSchedules()
  } catch (error) {
    ElMessage.error('修改排班失败')
  } finally {
    editLoading.value = false
  }
}

async function handleDeleteSchedule(schedule) {
  try {
    await ElMessageBox.confirm(
      `确定要删除 ${schedule.employee_name} 在 ${schedule.work_date} 的排班记录吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteSchedule(schedule.id)
    ElMessage.success('删除排班成功')
    loadSchedules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除排班失败')
    }
  }
}

// ==================== 调班审批相关 ====================
async function loadPendingRequests() {
  // 这个方法可以用于显示待审批调班申请的徽章数量
  // 具体实现可以根据需要添加
}

async function handleApprove() {
  const valid = await approvalFormRef.value.validate()
  if (!valid) return

  approvalLoading.value = true
  try {
    await approveShiftRequest(currentRequest.value.id, {
      approve: true,
      approval_remark: approvalForm.approval_remark
    })

    ElMessage.success('调班申请已批准')
    approvalDialogVisible.value = false
    approvalFormRef.value.resetFields()
    loadSchedules()
  } catch (error) {
    ElMessage.error('审批失败')
  } finally {
    approvalLoading.value = false
  }
}

async function handleReject() {
  const valid = await approvalFormRef.value.validate()
  if (!valid) return

  approvalLoading.value = true
  try {
    await approveShiftRequest(currentRequest.value.id, {
      approve: false,
      approval_remark: approvalForm.approval_remark
    })

    ElMessage.success('调班申请已拒绝')
    approvalDialogVisible.value = false
    approvalFormRef.value.resetFields()
    loadSchedules()
  } catch (error) {
    ElMessage.error('审批失败')
  } finally {
    approvalLoading.value = false
  }
}

// ==================== 工具函数 ====================
function getSchedulesForDate(date) {
  return calendarData.value[date] || []
}

function getShiftTagType(shiftName) {
  // 根据班次名称返回不同的标签颜色
  const typeMap = {
    '早班': 'success',
    '中班': 'warning',
    '晚班': 'danger',
    '全天': 'info'
  }
  return typeMap[shiftName] || 'default'
}

function formatDate(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}
</script>

<style scoped>
.schedule-manage-view {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  min-height: 100vh;
}

/* 顶部操作栏 */
.top-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #FFF8F0 0%, #fff 100%);
  border-radius: 8px;
  flex-wrap: wrap;
}

.date-picker-wrapper {
  flex: 1;
  min-width: 280px;
}

.view-switcher {
  flex-shrink: 0;
}

.actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

/* 日历视图 */
.calendar-view {
  background: #fff;
  border-radius: 8px;
}

:deep(.el-calendar) {
  --el-calendar-border: #e4e7ed;
}

:deep(.el-calendar__header) {
  padding: 12px 20px;
  border-bottom: 1px solid #e4e7ed;
}

:deep(.el-calendar__body) {
  padding: 12px 20px 20px;
}

:deep(.el-calendar-table .el-calendar-day) {
  height: 120px;
  min-height: 120px;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.date-number {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.schedule-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.schedule-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  background: #f5f7fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 12px;
}

.schedule-item:hover {
  background: #e6f7ff;
  transform: translateX(2px);
}

.schedule-item.is-swapped {
  background: #fff7e6;
  border-left: 3px solid #F7C52D;
}

.shift-name {
  flex: 1;
  color: #606266;
}

.swap-icon {
  color: #F7C52D;
  font-size: 14px;
}

/* 列表视图 */
.list-view {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #FFF8F0;
  color: #333;
  font-weight: 600;
}

/* 对话框样式 */
:deep(.el-dialog) {
  border-radius: 12px;
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
  color: #fff;
  border-radius: 12px 12px 0 0;
  padding: 16px 20px;
}

:deep(.el-dialog__title) {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: #fff;
}

:deep(.el-descriptions__label) {
  background-color: #FFF8F0;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .date-picker-wrapper,
  .view-switcher,
  .actions {
    width: 100%;
  }

  .actions {
    justify-content: center;
  }

  :deep(.el-calendar-table .el-calendar-day) {
    height: 100px;
    min-height: 100px;
  }
}

@media (max-width: 480px) {
  .schedule-manage-view {
    padding: 12px;
  }

  .date-number {
    font-size: 14px;
  }

  .schedule-item {
    font-size: 11px;
  }
}
</style>
