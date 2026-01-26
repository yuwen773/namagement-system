<template>
  <div class="application-center">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>申请中心</h2>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        提交申请
      </el-button>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filter">
        <el-form-item label="类型">
          <el-select
            v-model="filter.request_type"
            placeholder="全部"
            clearable
            style="width: 120px"
          >
            <el-option label="请假" value="leave" />
            <el-option label="加班" value="overtime" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="filter.status"
            placeholder="全部"
            clearable
            style="width: 120px"
          >
            <el-option label="待审批" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已驳回" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadApplications">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 申请列表 -->
    <el-table :data="applications" v-loading="loading" stripe>
      <el-table-column prop="id" label="编号" width="80" />
      <el-table-column label="类型" width="100">
        <template #default="{ row }">
          <el-tag
            :type="row.request_type === 'leave' ? 'primary' : 'warning'"
            size="small"
          >
            {{ row.request_type === "leave" ? "请假" : "加班" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="详情" min-width="200">
        <template #default="{ row }">
          <template v-if="row.request_type === 'leave'">
            {{ getLeaveTypeText(row.leave_type) }} ·
            {{ formatDateTime(row.start_time) }} 至
            {{ formatDateTime(row.end_time) }}
          </template>
          <template v-else>
            加班 {{ row.hours }} 小时 ·
            {{ formatDateTime(row.start_time) }} 至
            {{ formatDateTime(row.end_time) }}
          </template>
        </template>
      </el-table-column>
      <el-table-column
        prop="reason"
        label="原因"
        min-width="150"
        show-overflow-tooltip
      />
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
      <el-table-column label="操作" width="140" fixed="right">
        <template #default="{ row }">
          <div class="action-buttons">
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              link
              size="small"
              @click="cancelApplication(row)"
            >
              撤回
            </el-button>
            <el-button
              type="primary"
              link
              size="small"
              @click="viewApplication(row)"
            >
              查看
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-section">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="loadApplications"
        @current-change="loadApplications"
      />
    </div>

    <!-- 提交申请对话框 -->
    <el-dialog v-model="createDialogVisible" title="提交申请" width="500px">
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="100px"
      >
        <el-form-item label="申请类型" prop="request_type">
          <el-radio-group v-model="createForm.request_type">
            <el-radio-button value="leave">请假</el-radio-button>
            <el-radio-button value="overtime">加班</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <!-- 请假类型（仅请假时显示） -->
        <el-form-item
          v-if="createForm.request_type === 'leave'"
          label="请假类型"
          prop="leave_type"
        >
          <el-select
            v-model="createForm.leave_type"
            placeholder="请选择请假类型"
            style="width: 100%"
          >
            <el-option label="病假" value="sick" />
            <el-option label="事假" value="personal" />
            <el-option label="年假" value="annual" />
          </el-select>
        </el-form-item>

        <!-- 加班时长（仅加班时显示） -->
        <el-form-item
          v-if="createForm.request_type === 'overtime'"
          label="加班时长"
          prop="hours"
        >
          <el-input-number
            v-model="createForm.hours"
            :min="0.5"
            :step="0.5"
            :precision="1"
            style="width: 100%"
          />
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
          <el-input
            v-model="createForm.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入申请原因"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="submitting"
          @click="submitCreateForm"
        >
          提交
        </el-button>
      </template>
    </el-dialog>

    <!-- 申请详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="申请详情" width="500px">
      <el-descriptions :column="1" border v-if="currentApplication">
        <el-descriptions-item label="申请编号">{{
          currentApplication.id
        }}</el-descriptions-item>
        <el-descriptions-item label="类型">
          <el-tag
            :type="
              currentApplication.request_type === 'leave'
                ? 'primary'
                : 'warning'
            "
            size="small"
          >
            {{ currentApplication.request_type === "leave" ? "请假" : "加班" }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentApplication.request_type === 'leave'"
          label="请假类型"
        >
          {{ getLeaveTypeText(currentApplication.leave_type) }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentApplication.request_type === 'overtime'"
          label="加班时长"
        >
          {{ currentApplication.hours }} 小时
        </el-descriptions-item>
        <el-descriptions-item label="时间范围">
          {{ formatDateTime(currentApplication.start_time) }} 至
          {{ formatDateTime(currentApplication.end_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="申请原因">{{
          currentApplication.reason
        }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentApplication.status)" size="small">
            {{ getStatusText(currentApplication.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">{{
          formatDateTime(currentApplication.created_at)
        }}</el-descriptions-item>
        <el-descriptions-item v-if="currentApplication.approver" label="审批人">
          {{ currentApplication.approver_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentApplication.approver_reason"
          label="审批意见"
        >
          {{ currentApplication.approver_reason }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentApplication.updated_at"
          label="审批时间"
        >
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
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import {
  getApplicationList,
  submitApplication,
  deleteApplication,
  STATUS_TEXT,
  STATUS_TYPE,
  LEAVE_TYPE_TEXT,
} from "../api/approval";

// ========== 列表数据 ==========
const loading = ref(false);
const applications = ref([]);
const filter = reactive({
  request_type: "",
  status: "",
  dateRange: [],
});
const page = ref(1);
const pageSize = ref(10);
const total = ref(0);

// ========== 创建申请对话框 ==========
const createDialogVisible = ref(false);
const createFormRef = ref(null);
const submitting = ref(false);
const createForm = reactive({
  request_type: "leave",
  leave_type: "",
  hours: 2,
  timeRange: [],
  reason: "",
});

const createRules = {
  request_type: [
    { required: true, message: "请选择申请类型", trigger: "change" },
  ],
  leave_type: [
    { required: true, message: "请选择请假类型", trigger: "change" },
  ],
  hours: [{ required: true, message: "请填写加班时长", trigger: "blur" }],
  timeRange: [{ required: true, message: "请选择时间范围", trigger: "change" }],
  reason: [{ required: true, message: "请输入申请原因", trigger: "blur" }],
};

// ========== 详情对话框 ==========
const detailDialogVisible = ref(false);
const currentApplication = ref(null);

// ========== 方法 ==========

// 加载我的申请
const loadApplications = async () => {
  loading.value = true;
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
    };
    if (filter.request_type) params.request_type = filter.request_type;
    if (filter.status) params.status = filter.status;
    if (filter.dateRange && filter.dateRange.length === 2) {
      params.date_start = filter.dateRange[0];
      params.date_end = filter.dateRange[1];
    }

    const res = await getApplicationList(params);
    applications.value = res.data?.data || [];
    total.value = res.data?.total || 0;
  } catch (e) {
    ElMessage.error("加载申请列表失败");
  } finally {
    loading.value = false;
  }
};

// 重置筛选
const resetFilter = () => {
  filter.request_type = "";
  filter.status = "";
  filter.dateRange = [];
  page.value = 1;
  loadApplications();
};

// 显示创建对话框
const showCreateDialog = () => {
  createForm.request_type = "leave";
  createForm.leave_type = "";
  createForm.hours = 2;
  createForm.timeRange = [];
  createForm.reason = "";
  createDialogVisible.value = true;
};

// 提交创建表单
const submitCreateForm = async () => {
  try {
    await createFormRef.value.validate();
    submitting.value = true;

    const data = {
      request_type: createForm.request_type,
      start_time: createForm.timeRange[0],
      end_time: createForm.timeRange[1],
      reason: createForm.reason,
    };

    if (createForm.request_type === "leave") {
      data.leave_type = createForm.leave_type;
    } else {
      data.hours = createForm.hours;
    }

    await submitApplication(data);
    ElMessage.success("申请提交成功");
    createDialogVisible.value = false;
    loadApplications();
  } catch (e) {
    if (e !== false) {
      ElMessage.error("提交申请失败");
    }
  } finally {
    submitting.value = false;
  }
};

// 撤回申请
const cancelApplication = async (row) => {
  try {
    await ElMessageBox.confirm("确定要撤回该申请吗？", "提示", {
      type: "warning",
    });
    await deleteApplication(row.id);
    ElMessage.success("撤回成功");
    loadApplications();
  } catch (e) {
    if (e !== "cancel") {
      ElMessage.error("撤回失败");
    }
  }
};

// 查看申请详情
const viewApplication = (row) => {
  currentApplication.value = row;
  detailDialogVisible.value = true;
};

// 格式化日期时间
const formatDateTime = (datetime) => {
  if (!datetime) return "-";
  return datetime.replace("T", " ").substring(0, 16);
};

// 获取状态文本
const getStatusText = (status) => {
  return STATUS_TEXT[status] || status;
};

// 获取状态类型
const getStatusType = (status) => {
  return STATUS_TYPE[status] || "info";
};

// 获取请假类型文本
const getLeaveTypeText = (type) => {
  return LEAVE_TYPE_TEXT[type] || type;
};

// 初始化
onMounted(() => {
  loadApplications();
});
</script>

<style scoped>
/* ========================================
   Application Center - Refined Corporate Design
   ======================================== */
.application-center {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
}

.application-center::before {
  content: "";
  position: absolute;
  top: -50px;
  right: -30px;
  width: 300px;
  height: 300px;
  background: radial-gradient(
    circle,
    rgba(79, 70, 229, 0.03) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: 0;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.page-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    var(--color-primary),
    var(--color-primary-light),
    var(--color-success)
  );
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-header h2::before {
  content: "";
  width: 4px;
  height: 24px;
  background: linear-gradient(
    180deg,
    var(--color-primary) 0%,
    var(--color-primary-light) 100%
  );
  border-radius: 2px;
}

.page-header .el-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
}

.page-header .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

/* 筛选区域 */
.filter-section {
  margin-bottom: 20px;
  padding: 20px 24px;
  background: var(--color-gray-50);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  transition: all 0.3s ease;
}

.filter-section:hover {
  border-color: var(--color-primary-light);
  background: var(--color-bg-secondary);
}

.filter-section :deep(.el-form) {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.filter-section :deep(.el-form-item) {
  margin: 0;
}

.filter-section :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-text-secondary);
  padding-right: 12px;
}

.filter-section :deep(.el-input__wrapper),
.filter-section :deep(.el-select .el-input__wrapper) {
  border-radius: var(--radius-md);
}

.filter-section .el-button {
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
}

.filter-section .el-button:first-of-type {
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    var(--color-primary-light) 100%
  );
  border: none;
}

.filter-section .el-button:first-of-type:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

/* 表格样式 */
.el-table {
  border-radius: var(--radius-md);
  overflow: hidden;
}

.el-table::before {
  display: none;
}

.el-table :deep(.el-table__header) {
  background: var(--color-gray-50);
}

.el-table :deep(.el-table__header th) {
  background: transparent;
  font-weight: 600;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-light);
}

.el-table :deep(.el-table__row) {
  transition: all 0.2s ease;
}

.el-table :deep(.el-table__row:hover) {
  background: var(--color-gray-50);
}

/* 状态标签 */
.el-table :deep(.el-tag) {
  font-weight: 500;
  border-radius: var(--radius-full);
  padding: 2px 12px;
}

/* 操作按钮 */
.el-table :deep(.el-button--small) {
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  transition: all 0.2s ease;
}

.el-table :deep(.el-button--small:hover) {
  transform: translateY(-1px);
}

/* 操作按钮组 */
.action-buttons {
  display: flex;
  align-items: center;
}

/* 分页 */
.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 20px;
  background: var(--color-gray-50);
  border: 1px solid var(--color-border-light);
  border-top: none;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}

/* 表单提示文字 */
.form-tip {
  margin-left: 10px;
  color: var(--color-text-tertiary);
  font-size: 13px;
}

/* 对话框样式 */
.el-dialog {
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.el-dialog :deep(.el-dialog__header) {
  padding: 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: var(--color-gray-50);
}

.el-dialog :deep(.el-dialog__title) {
  font-weight: 600;
  font-size: 18px;
  color: var(--color-text-primary);
}

.el-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.el-dialog :deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border-light);
  background: var(--color-gray-50);
}

.el-dialog :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.el-dialog :deep(.el-textarea__inner) {
  border-radius: var(--radius-md);
  resize: none;
}

/* 描述列表 */
.el-descriptions {
  border-radius: var(--radius-md);
  overflow: hidden;
}

.el-descriptions :deep(.el-descriptions__label) {
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-gray-50);
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

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .filter-section :deep(.el-form) {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-section :deep(.el-form-item) {
    width: 100%;
  }

  .filter-section :deep(.el-select),
  .filter-section :deep(.el-input) {
    width: 100%;
  }

  .pagination-section {
    justify-content: center;
  }
}
</style>
