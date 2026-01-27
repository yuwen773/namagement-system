<template>
  <div class="profile-edit-container">
    <div class="page-header">
      <h2>个人信息</h2>
      <p class="subtitle">查看和管理您的个人信息、部门和岗位信息</p>
    </div>

    <!-- 当前信息展示 -->
    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">{{
          user?.username
        }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{
          user?.real_name
        }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{
          user?.phone || "未设置"
        }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{
          user?.email || "未设置"
        }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{
          user?.id_card || "未设置"
        }}</el-descriptions-item>
        <el-descriptions-item label="通讯地址">{{
          user?.address || "未设置"
        }}</el-descriptions-item>
        <el-descriptions-item label="紧急联系人">{{
          user?.emergency_contact || "未设置"
        }}</el-descriptions-item>
        <el-descriptions-item label="角色">{{ roleText }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">{{
          formatDate(user?.date_joined)
        }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 我的部门 -->
    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>我的部门</span>
        </div>
      </template>
      <div v-if="employeeProfile" class="department-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="工号">{{
            employeeProfile.employee_no
          }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{
            employeeProfile.department_name || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="岗位">{{
            employeeProfile.post_name || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="入职日期">{{
            formatDate(employeeProfile.hire_date)
          }}</el-descriptions-item>
          <el-descriptions-item label="基本工资"
            >¥{{
              formatCurrency(employeeProfile.salary_base)
            }}</el-descriptions-item
          >
          <el-descriptions-item label="状态">
            <el-tag :type="employeeStatusType" size="small">{{
              employeeStatusText
            }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <el-empty v-else description="暂无员工档案信息" :image-size="80" />
    </el-card>

    <!-- 组织架构 -->
    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>组织架构</span>
          <!-- <el-button type="primary" link @click="showOrgDialog = true">
            <el-icon><View /></el-icon>
            查看完整架构
          </el-button> -->
        </div>
      </template>
      <div v-if="departmentTree.length > 0" class="org-preview">
        <el-tree
          :data="departmentTree"
          :props="{ label: 'name', children: 'children' }"
          default-expand-all
          :expand-on-click-node="false"
          node-key="id"
        >
          <template #default="{ node, data }">
            <div class="tree-node">
              <span>{{ data.name }}</span>
              <el-tag v-if="data.code" size="small" type="info">{{
                data.code
              }}</el-tag>
            </div>
          </template>
        </el-tree>
      </div>
      <el-empty v-else description="暂无组织架构信息" :image-size="80" />
    </el-card>

    <!-- 修改密码 -->
    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span
            ><el-icon><Lock /></el-icon> 修改密码</span
          >
          <el-button type="primary" link @click="showPasswordDialog = true">
            <el-icon><Edit /></el-icon>
            修改密码
          </el-button>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="密码状态">
          <el-tag type="success" size="small">已设置</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="安全等级">
          <el-rate v-model="passwordStrength" disabled text-color="#ff9900" />
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showPasswordDialog"
      title="修改密码"
      width="450px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="旧密码" prop="old_password">
          <el-input
            v-model="passwordForm.old_password"
            type="text"
            placeholder="请输入旧密码"
            clearable
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="passwordForm.new_password"
            type="text"
            placeholder="请输入新密码"
            clearable
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="new_password2">
          <el-input
            v-model="passwordForm.new_password2"
            type="text"
            placeholder="请再次输入新密码"
            clearable
            autocomplete="off"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPasswordDialog = false">取消</el-button>
          <el-button
            type="primary"
            @click="handlePasswordSubmit"
            :loading="passwordLoading"
          >
            确认修改
          </el-button>
        </span>
      </template>
    </el-dialog>

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
          <el-radio-group
            v-model="formData.edit_type"
            @change="handleTypeChange"
          >
            <el-radio-button value="phone">手机号</el-radio-button>
            <el-radio-button value="email">邮箱</el-radio-button>
            <el-radio-button value="emergency_contact"
              >紧急联系人</el-radio-button
            >
            <el-radio-button value="address">通讯地址</el-radio-button>
            <el-radio-button value="id_card">身份证号</el-radio-button>
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
          <el-button
            type="primary"
            @click="handleSubmit"
            :loading="submitLoading"
          >
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
            <span class="old-value">{{ row.old_value || "未设置" }}</span>
            <el-icon><Right /></el-icon>
            <span class="new-value">{{ row.new_value }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="reason" label="修改原因" min-width="150">
          <template #default="{ row }">
            <el-tooltip
              :content="row.reason"
              placement="top"
              :disabled="!row.reason"
            >
              <span class="reason-text">{{ row.reason || "-" }}</span>
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

    <!-- 组织架构完整视图对话框 -->
    <el-dialog v-model="showOrgDialog" title="组织架构" width="600px">
      <div class="org-tree-container">
        <el-tree
          v-if="fullDepartmentTree.length > 0"
          :data="fullDepartmentTree"
          :props="{ label: 'name', children: 'children' }"
          default-expand-all
          :expand-on-click-node="false"
          node-key="id"
        >
          <template #default="{ node, data }">
            <div class="tree-node">
              <span>{{ data.name }}</span>
              <el-tag v-if="data.code" size="small" type="info">{{
                data.code
              }}</el-tag>
            </div>
          </template>
        </el-tree>
        <el-empty v-else description="暂无组织架构信息" :image-size="80" />
      </div>
      <template #footer>
        <el-button @click="showOrgDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Right, Refresh, View, Lock } from "@element-plus/icons-vue";
import { useAuthStore } from "../stores/auth";
import {
  getCurrentUser,
  getEditRequestList,
  createEditRequest,
  getMyEmployeeProfile,
  getDepartmentTree,
  changePassword,
  EDIT_TYPE,
  EDIT_TYPE_TEXT,
  STATUS,
  STATUS_TEXT,
  STATUS_TYPE,
} from "../api/profile";
import { formatCurrency } from "../utils/format";

// 打开组织架构对话框
const handleViewOrg = () => {
  showOrgDialog.value = true;
  if (departmentTree.value.length > 0) {
    fullDepartmentTree.value = departmentTree.value;
  }
};

const authStore = useAuthStore();
const user = ref(null);
const isHR = computed(() => authStore.isHR || authStore.isAdmin);

// 员工档案信息
const employeeProfile = ref(null);
const departmentTree = ref([]);
const fullDepartmentTree = ref([]);
const showOrgDialog = ref(false);

// 员工状态
const employeeStatusText = computed(() => {
  const statusMap = {
    active: "在职",
    pending: "待入职",
    resigned: "已离职",
  };
  return statusMap[employeeProfile.value?.status] || "-";
});

const employeeStatusType = computed(() => {
  const typeMap = {
    active: "success",
    pending: "warning",
    resigned: "info",
  };
  return typeMap[employeeProfile.value?.status] || "info";
});

const roleText = computed(() => {
  const roleMap = {
    admin: "系统管理员",
    hr: "人事专员",
    employee: "普通员工",
  };
  return roleMap[user.value?.role] || "-";
});

// 获取当前用户信息
const loadCurrentUser = async () => {
  try {
    const res = await getCurrentUser();
    user.value = res.data?.data;
  } catch (error) {
    console.error("获取用户信息失败:", error);
  }
};

// 获取当前用户的员工档案
const loadEmployeeProfile = async () => {
  try {
    const res = await getMyEmployeeProfile();
    if (res.data?.code === 0) {
      employeeProfile.value = res.data?.data;
    }
  } catch (error) {
    // 404 表示没有员工档案，这是正常的
    console.log("暂无员工档案信息");
  }
};

// 获取部门树
const loadDepartmentTree = async () => {
  try {
    const res = await getDepartmentTree();
    if (res.data?.code === 0) {
      departmentTree.value = res.data?.data || [];
    }
  } catch (error) {
    console.error("获取部门树失败:", error);
  }
};

// 表单数据
const formRef = ref(null);
const formData = reactive({
  edit_type: EDIT_TYPE.PHONE,
  new_value: "",
  reason: "",
});

const submitLoading = ref(false);

// 表单验证规则
const validatePhone = (rule, value, callback) => {
  const phoneRegex = /^1[3-9]\d{9}$/;
  if (!phoneRegex.test(value)) {
    callback(new Error("请输入正确的手机号格式"));
  } else {
    callback();
  }
};

const validateEmail = (rule, value, callback) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(value)) {
    callback(new Error("请输入正确的邮箱格式"));
  } else {
    callback();
  }
};

const validateIdCard = (rule, value, callback) => {
  const idCardRegex = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
  if (!idCardRegex.test(value)) {
    callback(new Error("请输入正确的身份证号格式"));
  } else {
    callback();
  }
};

const rules = computed(() => ({
  edit_type: [{ required: true, message: "请选择修改类型", trigger: "change" }],
  new_value: [
    { required: true, message: `请输入${currentLabel.value}`, trigger: "blur" },
    {
      validator: (rule, value, callback) => {
        if (formData.edit_type === EDIT_TYPE.PHONE)
          return validatePhone(rule, value, callback);
        if (formData.edit_type === EDIT_TYPE.EMAIL)
          return validateEmail(rule, value, callback);
        if (formData.edit_type === EDIT_TYPE.ID_CARD)
          return validateIdCard(rule, value, callback);
        callback();
      },
      trigger: "blur",
    },
  ],
  reason: [{ required: true, message: "请输入修改原因", trigger: "blur" }],
}));

const currentLabel = computed(() => {
  const map = {
    [EDIT_TYPE.PHONE]: "新手机号",
    [EDIT_TYPE.EMAIL]: "新邮箱",
    [EDIT_TYPE.EMERGENCY_CONTACT]: "新紧急联系人",
    [EDIT_TYPE.ADDRESS]: "新通讯地址",
    [EDIT_TYPE.ID_CARD]: "新身份证号",
  };
  return map[formData.edit_type] || "新值";
});

const currentPlaceholder = computed(() => {
  const map = {
    [EDIT_TYPE.PHONE]: "请输入新手机号",
    [EDIT_TYPE.EMAIL]: "请输入新邮箱",
    [EDIT_TYPE.EMERGENCY_CONTACT]: "请输入新紧急联系人信息",
    [EDIT_TYPE.ADDRESS]: "请输入新通讯地址",
    [EDIT_TYPE.ID_CARD]: "请输入新身份证号",
  };
  return map[formData.edit_type] || "请输入新值";
});

// 申请记录列表
const applications = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 密码修改相关
const showPasswordDialog = ref(false);
const passwordFormRef = ref(null);
const passwordForm = reactive({
  old_password: "",
  new_password: "",
  new_password2: "",
});
const passwordLoading = ref(false);
const passwordStrength = ref(4);

// 密码验证规则
const validateOldPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请输入旧密码"));
  } else {
    callback();
  }
};

const validateNewPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请输入新密码"));
  } else if (value.length < 8) {
    callback(new Error("密码长度至少8位"));
  } else {
    // 检查密码强度
    const hasLetter = /[a-zA-Z]/.test(value);
    const hasNumber = /\d/.test(value);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);
    let strength = 0;
    if (hasLetter) strength++;
    if (hasNumber) strength++;
    if (hasSpecial) strength++;
    if (value.length >= 12) strength++;
    passwordStrength.value = Math.min(strength, 5);

    if (!hasLetter || !hasNumber || !hasSpecial) {
      callback(new Error("密码必须包含字母、数字和特殊字符"));
    } else {
      callback();
    }
  }
};

const validateNewPassword2 = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请再次输入新密码"));
  } else if (value !== passwordForm.new_password) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const passwordRules = {
  old_password: [{ validator: validateOldPassword, trigger: "blur" }],
  new_password: [{ validator: validateNewPassword, trigger: "blur" }],
  new_password2: [{ validator: validateNewPassword2, trigger: "blur" }],
};

// 提交密码修改
const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return;

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        passwordLoading.value = true;
        await changePassword({
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password,
          new_password2: passwordForm.new_password2,
        });
        ElMessage.success("密码修改成功，请重新登录");

        // 关闭对话框并清除表单
        showPasswordDialog.value = false;
        passwordForm.old_password = "";
        passwordForm.new_password = "";
        passwordForm.new_password2 = "";
        passwordFormRef.value.resetFields();

        // 提示用户重新登录
        setTimeout(() => {
          ElMessageBox.confirm(
            "为了安全起见，密码修改后需要重新登录。是否立即重新登录？",
            "重新登录",
            {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "info",
            },
          )
            .then(() => {
              authStore.logout();
              window.location.reload();
            })
            .catch(() => {});
        }, 500);
      } catch (error) {
        const msg =
          error.response?.data?.message ||
          error.response?.data?.old_password?.[0] ||
          "密码修改失败";
        ElMessage.error(msg);
      } finally {
        passwordLoading.value = false;
      }
    }
  });
};

// 格式化日期
const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("zh-CN");
};

const formatDateTime = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleString("zh-CN");
};

// 处理修改类型变化
const handleTypeChange = () => {
  formData.new_value = "";
  formData.reason = "";
  if (formRef.value) {
    formRef.value.clearValidate();
  }
};

// 提交修改申请
const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitLoading.value = true;
        await createEditRequest({
          edit_type: formData.edit_type,
          new_value: formData.new_value,
          reason: formData.reason,
        });
        ElMessage.success("修改申请已提交，请等待审批");
        resetForm();
        loadApplications();
      } catch (error) {
        const msg = error.response?.data?.message || "提交申请失败";
        ElMessage.error(msg);
      } finally {
        submitLoading.value = false;
      }
    }
  });
};

// 重置表单
const resetForm = () => {
  formData.new_value = "";
  formData.reason = "";
  if (formRef.value) {
    formRef.value.resetFields();
  }
};

// 加载申请列表
const loadApplications = async () => {
  try {
    loading.value = true;
    // 个人中心始终加载当前登录用户的申请记录
    const res = await getEditRequestList({
      page: currentPage.value,
      page_size: pageSize.value,
    });
    applications.value = res.data?.data || res.data?.results || [];
    total.value = res.data?.total || res.data?.count || 0;
  } catch (error) {
    ElMessage.error("加载申请列表失败");
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 处理分页
const handlePageChange = (page) => {
  currentPage.value = page;
  loadApplications();
};

onMounted(async () => {
  await loadCurrentUser();
  await loadEmployeeProfile();
  await loadDepartmentTree();
  loadApplications();
});
</script>

<style scoped>
/* ========================================
   Profile Edit - Refined Corporate Design
   ======================================== */
.profile-edit-container {
  padding: 24px;
  position: relative;
}

.profile-edit-container::before {
  content: "";
  position: absolute;
  top: -50px;
  right: -30px;
  width: 400px;
  height: 400px;
  background: radial-gradient(
    circle,
    rgba(79, 70, 229, 0.03) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: 0;
}

.page-header {
  margin-bottom: 24px;
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
  margin: 0 0 8px 0;
  font-size: 24px;
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

.subtitle {
  margin: 0;
  color: var(--color-text-tertiary);
  font-size: 14px;
  padding-left: 16px;
}

.info-card,
.edit-card,
.history-card {
  margin-bottom: 20px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  overflow: hidden;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.info-card:hover,
.edit-card:hover,
.history-card:hover {
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow-md);
}

.info-card::before,
.edit-card::before,
.history-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    var(--color-primary),
    var(--color-primary-light)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.info-card:hover::before,
.edit-card:hover::before,
.history-card:hover::before {
  opacity: 1;
}

.info-card :deep(.el-card__header),
.edit-card :deep(.el-card__header),
.history-card :deep(.el-card__header) {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(
    135deg,
    var(--color-gray-50) 0%,
    var(--color-bg-secondary) 100%
  );
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
  color: var(--color-text-primary);
}

.info-card :deep(.el-descriptions__label),
.edit-card :deep(.el-descriptions__label) {
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-gray-50);
}

.info-card :deep(.el-descriptions__cell),
.edit-card :deep(.el-descriptions__cell) {
  background: var(--color-bg-secondary);
}

.old-value {
  color: var(--color-text-tertiary);
  text-decoration: line-through;
  font-size: 13px;
}

.new-value {
  color: var(--color-success);
  font-weight: 500;
}

.reason-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border-light);
}

/* 组织架构样式 */
.org-preview {
  max-height: 300px;
  overflow-y: auto;
}

.org-tree-container {
  max-height: 400px;
  overflow-y: auto;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

/* 表格样式 */
.history-card :deep(.el-table__header) {
  background: var(--color-gray-50);
}

.history-card :deep(.el-table__header th) {
  background: transparent;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* 响应式 */
@media (max-width: 1024px) {
  .info-card :deep(.el-descriptions) {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .profile-edit-container {
    padding: 16px;
  }

  .page-header {
    padding: 20px;
  }

  .page-header h2 {
    font-size: 20px;
  }

  .subtitle {
    padding-left: 0;
    padding-top: 8px;
  }

  .info-card :deep(.el-card__header),
  .edit-card :deep(.el-card__header),
  .history-card :deep(.el-card__header) {
    padding: 16px;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .info-card :deep(.el-descriptions) {
    grid-template-columns: 1fr;
  }

  .info-card :deep(.el-descriptions-item__label),
  .info-card :deep(.el-descriptions-item__content) {
    padding: 12px 16px;
  }

  .pagination-container {
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
  }

  .pagination-container .el-pagination {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .profile-edit-container {
    padding: 12px;
  }

  .page-header {
    padding: 16px;
    margin-bottom: 16px;
  }

  .page-header h2 {
    font-size: 18px;
  }

  .page-header h2::before {
    width: 3px;
    height: 18px;
  }

  .info-card,
  .edit-card,
  .history-card {
    margin-bottom: 16px;
    border-radius: var(--radius-lg);
  }

  .card-header {
    font-size: 15px;
  }

  .reason-text {
    -webkit-line-clamp: 3;
  }
}
</style>
