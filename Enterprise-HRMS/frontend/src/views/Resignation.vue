<template>
  <div class="resignation-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="8.5" cy="7" r="4" />
            <line x1="23" y1="11" x2="17" y2="11" />
            <line x1="20" y1="8" x2="20" y2="14" />
          </svg>
        </div>
        <div class="header-text">
          <h2>离职管理</h2>
          <p class="subtitle">管理在职员工，办理离职手续</p>
        </div>
      </div>
      <div class="header-right">
        <el-button type="primary" :loading="loading" @click="fetchEmployees">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M23 4v6h-6" />
            <path d="M1 20v-6h6" />
            <path
              d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"
            />
          </svg>
          刷新列表
        </el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索员工姓名或工号..."
        prefix-icon="Search"
        clearable
        class="search-input"
        @clear="fetchEmployees"
        @keyup.enter="fetchEmployees"
      />
      <el-select
        v-model="filterStatus"
        placeholder="状态筛选"
        clearable
        class="status-select"
      >
        <el-option label="在职" value="active" />
        <el-option label="待入职" value="pending" />
        <el-option label="已离职" value="resigned" />
      </el-select>
      <el-button type="primary" @click="fetchEmployees">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
        </svg>
        搜索
      </el-button>
    </div>

    <!-- 在职员工列表 -->
    <div class="table-section" v-loading="loading">
      <el-table :data="employeeList" stripe class="custom-table">
        <el-table-column prop="employee_id" label="工号" width="150" />
        <el-table-column prop="real_name" label="姓名" min-width="120">
          <template #default="{ row }">
            <div class="employee-name">
              <div class="employee-avatar">
                {{ row.real_name?.charAt(0) }}
              </div>
              <span>{{ row.real_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="post_name" label="岗位" width="200" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="hire_date" label="入职日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.hire_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'active'"
              type="warning"
              link
              size="small"
              @click="handleResign(row)"
              class="action-btn"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              办理离职
            </el-button>
            <el-button
              v-else-if="row.status === 'resigned'"
              type="info"
              link
              size="small"
              @click="viewResignDetail(row)"
              class="action-btn"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              查看详情
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

    <!-- 离职办理对话框 -->
    <el-dialog
      v-model="resignDialogVisible"
      title="办理离职"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="resignFormRef"
        :model="resignForm"
        :rules="resignRules"
        label-width="100px"
        class="custom-form"
      >
        <el-form-item label="员工信息">
          <div class="employee-info-display">
            <span class="name">{{ selectedEmployee?.real_name }}</span>
            <span class="employee-id"
              >({{ selectedEmployee?.employee_id }})</span
            >
          </div>
        </el-form-item>

        <el-form-item label="离职日期" prop="resigned_date">
          <el-date-picker
            v-model="resignForm.resigned_date"
            type="date"
            placeholder="选择离职日期"
            style="width: 100%"
            value-format="YYYY-MM-DD"
            :disabled-date="disabledFutureDate"
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
        <span class="dialog-footer">
          <el-button @click="resignDialogVisible = false">取消</el-button>
          <el-button type="warning" :loading="submitting" @click="submitResign">
            确认离职
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 离职详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="离职详情" width="450px">
      <div v-if="selectedEmployee" class="detail-content">
        <div class="detail-item">
          <span class="label">员工姓名：</span>
          <span class="value">{{ selectedEmployee.real_name }}</span>
        </div>
        <div class="detail-item">
          <span class="label">工号：</span>
          <span class="value">{{ selectedEmployee.employee_id }}</span>
        </div>
        <div class="detail-item">
          <span class="label">离职日期：</span>
          <span class="value">{{
            formatDate(selectedEmployee.resigned_date)
          }}</span>
        </div>
        <div class="detail-item">
          <span class="label">离职原因：</span>
          <span class="value">{{
            selectedEmployee.resigned_reason || "-"
          }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { getEmployeeList, resignEmployee } from "@/api/employee";

const loading = ref(false);
const submitting = ref(false);
const employeeList = ref([]);
const searchKeyword = ref("");
const filterStatus = ref("");
const selectedEmployee = ref(null);
const resignDialogVisible = ref(false);
const detailDialogVisible = ref(false);
const resignFormRef = ref(null);

// 分页状态
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const resignForm = reactive({
  resigned_date: "",
  resigned_reason: "",
});

const resignRules = {
  resigned_date: [
    { required: true, message: "请选择离职日期", trigger: "change" },
  ],
};

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return "-";
  const date = new Date(dateStr);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
};

// 状态类型
const getStatusType = (status) => {
  const types = {
    active: "success",
    pending: "warning",
    resigned: "info",
  };
  return types[status] || "info";
};

// 状态文本
const getStatusText = (status) => {
  const texts = {
    active: "在职",
    pending: "待入职",
    resigned: "已离职",
  };
  return texts[status] || status;
};

// 禁用未来日期
const disabledFutureDate = (time) => {
  return time.getTime() > Date.now();
};

// 获取员工列表
const fetchEmployees = async () => {
  loading.value = true;
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: searchKeyword.value || undefined,
      status: filterStatus.value || undefined,
    };
    const res = await getEmployeeList(params);
    employeeList.value = res.data.data || [];
    pagination.total = res.data.total || 0;
  } catch (error) {
    console.error("获取员工列表失败:", error);
    ElMessage.error("获取员工列表失败");
  } finally {
    loading.value = false;
  }
};

// 页码变化
const handlePageChange = (page) => {
  pagination.page = page;
  fetchEmployees();
};

// 打开离职对话框
const handleResign = (employee) => {
  selectedEmployee.value = employee;
  resignForm.resigned_date = "";
  resignForm.resigned_reason = "";
  resignDialogVisible.value = true;
};

// 查看离职详情
const viewResignDetail = (employee) => {
  selectedEmployee.value = employee;
  detailDialogVisible.value = true;
};

// 提交离职
const submitResign = async () => {
  if (!resignFormRef.value) return;

  try {
    await resignFormRef.value.validate();
    submitting.value = true;

    await ElMessageBox.confirm(
      "确定要办理离职吗？离职后该员工账号将被禁用。",
      "离职确认",
      {
        confirmButtonText: "确定离职",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    await resignEmployee(selectedEmployee.value.id, {
      resigned_date: resignForm.resigned_date,
      resigned_reason: resignForm.resigned_reason,
    });

    ElMessage.success("离职办理成功");
    resignDialogVisible.value = false;
    fetchEmployees();
  } catch (error) {
    if (error !== "cancel") {
      console.error("离职办理失败:", error);
      ElMessage.error(error.response?.data?.detail || "离职办理失败");
    }
  } finally {
    submitting.value = false;
  }
};

onMounted(() => {
  fetchEmployees();
});
</script>

<style scoped>
.resignation-container {
  padding: 20px;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text h2 {
  margin: 0 0 4px 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.subtitle {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.header-right .el-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
}

.header-right svg {
  width: 16px;
  height: 16px;
}

/* 搜索区域 */
.search-section {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.search-input {
  width: 280px;
}

.status-select {
  width: 140px;
}

.search-section .el-button svg {
  width: 16px;
  height: 16px;
}

/* 表格区域 */
.table-section {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.custom-table {
  border-radius: 0;
}

/* 员工名称列样式 */
.employee-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.employee-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

/* 操作按钮 */
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
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

/* 员工信息显示 */
.employee-info-display {
  background: #f5f7fa;
  padding: 10px 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.employee-info-display .name {
  font-weight: 600;
  color: #303133;
}

.employee-info-display .employee-id {
  color: #909399;
  font-size: 13px;
}

/* 详情内容 */
.detail-content {
  padding: 10px 0;
}

.detail-item {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item .label {
  width: 100px;
  color: #909399;
  flex-shrink: 0;
}

.detail-item .value {
  color: #303133;
  font-weight: 500;
}

/* 表单样式 */
.custom-form .form-input {
  width: 100%;
}
</style>
