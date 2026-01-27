<template>
  <div class="performance-review-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h2>绩效评估</h2>
        <p class="description">管理员工绩效评估，创建、编辑和发布绩效评估</p>
      </div>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新建评估
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <el-card class="filter-card" shadow="hover">
      <el-form :model="filterForm" inline>
        <el-form-item label="评估周期">
          <el-select
            v-model="filterForm.review_period"
            placeholder="请选择评估周期"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="item in REVIEW_PERIOD_OPTIONS"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="filterForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 150px"
          >
            <el-option label="全部" value="" />
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
          </el-select>
        </el-form-item>
        <el-form-item label="员工姓名">
          <el-input
            v-model="filterForm.keyword"
            placeholder="请输入员工姓名"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="分数范围">
          <el-input-number
            v-model="filterForm.score_min"
            placeholder="最低分"
            :min="0"
            :max="5"
            :precision="1"
            style="width: 130px"
          />
          <span style="margin: 0 8px">至</span>
          <el-input-number
            v-model="filterForm.score_max"
            placeholder="最高分"
            :min="0"
            :max="5"
            :precision="1"
            style="width: 130px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="data-card" shadow="hover">
      <el-table
        v-loading="loading"
        :data="reviewList"
        stripe
        style="width: 100%"
        :default-sort="{ prop: 'created_at', order: 'descending' }"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column
          prop="employee_name"
          label="被评估员工"
          min-width="120"
        />
        <el-table-column prop="review_period" label="评估周期" width="140">
          <template #default="{ row }">
            <el-tag size="small">{{ formatPeriod(row.review_period) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="score" label="评分" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              v-if="row.score"
              :type="getScoreType(row.score)"
              size="small"
            >
              {{ row.score }}分
            </el-tag>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="reviewer_name" label="评估人" width="100" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="STATUS_TYPE[row.status]" size="small">
              {{ STATUS_TEXT[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="180"
          sortable
        >
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              size="small"
              @click="openDetailDialog(row)"
            >
              查看
            </el-button>
            <el-button
              v-if="row.status === 'draft'"
              type="success"
              link
              size="small"
              @click="handlePublish(row.id)"
            >
              发布
            </el-button>
            <el-button
              v-if="row.status === 'published'"
              type="warning"
              link
              size="small"
              @click="handleUnpublish(row.id)"
            >
              撤回
            </el-button>
            <el-button
              v-if="row.status === 'draft'"
              type="primary"
              link
              size="small"
              @click="openEditDialog(row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="row.status === 'draft'"
              type="danger"
              link
              size="small"
              @click="handleDelete(row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建绩效评估' : '编辑绩效评估'"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="被评估员工" prop="employee">
          <el-select
            v-model="formData.employee"
            placeholder="请选择被评估员工"
            filterable
            style="width: 100%"
            :disabled="dialogType === 'edit'"
          >
            <el-option
              v-for="emp in employeeOptions"
              :key="emp.id"
              :label="`${emp.real_name} (${emp.employee_no || emp.username})`"
              :value="emp.user_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评估周期" prop="review_period">
          <el-select
            v-model="formData.review_period"
            placeholder="请选择评估周期"
            style="width: 100%"
            :disabled="dialogType === 'edit'"
          >
            <el-option
              v-for="item in REVIEW_PERIOD_OPTIONS"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评分" prop="score">
          <el-rate
            v-model="formData.score"
            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
          />
          <span class="score-label">{{ getScoreLabel(formData.score) }}</span>
        </el-form-item>
        <el-form-item label="优点" prop="strengths">
          <el-input
            v-model="formData.strengths"
            type="textarea"
            :rows="3"
            placeholder="请填写员工的工作优点"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="改进建议" prop="improvements">
          <el-input
            v-model="formData.improvements"
            type="textarea"
            :rows="3"
            placeholder="请填写改进建议"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="设定目标" prop="goals">
          <el-input
            v-model="formData.goals"
            type="textarea"
            :rows="3"
            placeholder="请填写下一阶段的工作目标"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ dialogType === "create" ? "创建" : "保存" }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="绩效评估详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="被评估员工">
          {{ currentReview.employee_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="评估周期">
          {{ formatPeriod(currentReview.review_period) }}
        </el-descriptions-item>
        <el-descriptions-item label="评分">
          <el-tag
            v-if="currentReview.score"
            :type="getScoreType(currentReview.score)"
          >
            {{ currentReview.score }}分
          </el-tag>
          <span v-else class="text-muted">-</span>
        </el-descriptions-item>
        <el-descriptions-item label="评估人">
          {{ currentReview.reviewer_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="STATUS_TYPE[currentReview.status]">
            {{ STATUS_TEXT[currentReview.status] }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="优点">
          <div class="content-text">{{ currentReview.strengths || "-" }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="改进建议">
          <div class="content-text">
            {{ currentReview.improvements || "-" }}
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="设定目标">
          <div class="content-text">{{ currentReview.goals || "-" }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDateTime(currentReview.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间">
          {{ formatDateTime(currentReview.updated_at) }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Plus, Search, Refresh } from "@element-plus/icons-vue";
import {
  getPerformanceReviewList,
  getPerformanceReviewDetail,
  createPerformanceReview,
  updatePerformanceReview,
  deletePerformanceReview,
  publishPerformanceReview,
  unpublishPerformanceReview,
  getEmployeeOptions,
  REVIEW_PERIOD_OPTIONS,
  SCORE_OPTIONS,
  STATUS,
  STATUS_TEXT,
  STATUS_TYPE,
} from "@/api/performance";
import { formatDateTime } from "@/utils/format";

// 响应式状态
const loading = ref(false);
const submitting = ref(false);
const reviewList = ref([]);
const employeeOptions = ref([]);
const dialogVisible = ref(false);
const detailDialogVisible = ref(false);
const dialogType = ref("create");
const formRef = ref(null);
const currentReview = ref({});

// 分页参数
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0,
});

// 筛选表单
const filterForm = reactive({
  review_period: "",
  status: "",
  keyword: "",
  score_min: null,
  score_max: null,
});

// 表单数据
const formData = reactive({
  employee: null,
  review_period: "",
  score: null,
  strengths: "",
  improvements: "",
  goals: "",
});

// 表单验证规则
const formRules = {
  employee: [
    { required: true, message: "请选择被评估员工", trigger: "change" },
  ],
  review_period: [
    { required: true, message: "请选择评估周期", trigger: "change" },
  ],
};

// 评分选项
const scoreOptions = SCORE_OPTIONS;

// 格式化评估周期
const formatPeriod = (period) => {
  if (!period) return "-";
  const option = REVIEW_PERIOD_OPTIONS.find((item) => item.value === period);
  return option ? option.label : period;
};

// 获取评分标签颜色
const getScoreType = (score) => {
  if (!score) return "info";
  if (score >= 4) return "success";
  if (score >= 3) return "warning";
  return "danger";
};

// 获取评分标签文本
const getScoreLabel = (score) => {
  if (!score) return "未评分";
  const option = SCORE_OPTIONS.find((item) => item.value === score);
  return option ? option.label.split(" - ")[1] : "";
};

// 加载绩效评估列表
const fetchReviewList = async () => {
  loading.value = true;
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
    };
    if (filterForm.review_period) {
      params.review_period = filterForm.review_period;
    }
    if (filterForm.status) {
      params.status = filterForm.status;
    }
    if (filterForm.keyword) {
      params.keyword = filterForm.keyword;
    }
    if (filterForm.score_min !== null && filterForm.score_min !== "") {
      params.score_min = filterForm.score_min;
    }
    if (filterForm.score_max !== null && filterForm.score_max !== "") {
      params.score_max = filterForm.score_max;
    }
    const response = await getPerformanceReviewList(params);
    // 处理分页数据格式
    const data = response.data?.data || response.data?.results || [];
    const total = response.data?.total || response.data?.count || 0;
    reviewList.value = data;
    pagination.total = total;
  } catch (error) {
    console.error("获取绩效评估列表失败:", error);
    ElMessage.error("获取绩效评估列表失败");
  } finally {
    loading.value = false;
  }
};

// 加载员工选项
const fetchEmployeeOptions = async () => {
  try {
    const response = await getEmployeeOptions({});
    const data = response.data?.data || response.data?.results || [];
    employeeOptions.value = data;
  } catch (error) {
    console.error("获取员工列表失败:", error);
  }
};

// 筛选
const handleFilter = () => {
  pagination.page = 1;
  fetchReviewList();
};

// 重置筛选
const resetFilter = () => {
  filterForm.review_period = "";
  filterForm.status = "";
  filterForm.keyword = "";
  filterForm.score_min = null;
  filterForm.score_max = null;
  pagination.page = 1;
  fetchReviewList();
};

// 分页处理
const handleSizeChange = (size) => {
  pagination.page_size = size;
  fetchReviewList();
};

const handlePageChange = (page) => {
  pagination.page = page;
  fetchReviewList();
};

// 打开新建对话框
const openCreateDialog = () => {
  dialogType.value = "create";
  resetForm();
  dialogVisible.value = true;
};

// 打开编辑对话框
const openEditDialog = async (row) => {
  dialogType.value = "edit";
  try {
    const response = await getPerformanceReviewDetail(row.id);
    const review = response.data?.data || response.data;
    Object.assign(formData, {
      employee: review.employee, // 后端返回的是 employee 的 user_id
      review_period: review.review_period,
      score: review.score,
      strengths: review.strengths || "",
      improvements: review.improvements || "",
      goals: review.goals || "",
    });
    dialogVisible.value = true;
  } catch (error) {
    console.error("获取评估详情失败:", error);
    ElMessage.error("获取评估详情失败");
  }
};

// 打开详情对话框
const openDetailDialog = async (row) => {
  try {
    const response = await getPerformanceReviewDetail(row.id);
    currentReview.value = response.data?.data || response.data;
    detailDialogVisible.value = true;
  } catch (error) {
    console.error("获取评估详情失败:", error);
    ElMessage.error("获取评估详情失败");
  }
};

// 重置表单
const resetForm = () => {
  formData.employee = null;
  formData.review_period = "";
  formData.score = null;
  formData.strengths = "";
  formData.improvements = "";
  formData.goals = "";
  if (formRef.value) {
    formRef.value.resetFields();
  }
};

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate();
    submitting.value = true;
    if (dialogType.value === "create") {
      await createPerformanceReview(formData);
      ElMessage.success("创建成功");
    } else {
      await updatePerformanceReview(currentReview.value.id, formData);
      ElMessage.success("保存成功");
    }
    dialogVisible.value = false;
    fetchReviewList();
  } catch (error) {
    console.error("提交失败:", error);
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message);
    }
  } finally {
    submitting.value = false;
  }
};

// 发布
const handlePublish = async (id) => {
  try {
    await ElMessageBox.confirm(
      "确定要发布此绩效评估吗？发布后员工将可以看到。",
      "确认发布",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );
    await publishPerformanceReview(id);
    ElMessage.success("发布成功");
    fetchReviewList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("发布失败:", error);
      ElMessage.error("发布失败");
    }
  }
};

// 撤回
const handleUnpublish = async (id) => {
  try {
    await ElMessageBox.confirm(
      "确定要撤回此绩效评估吗？撤回后员工将无法看到。",
      "确认撤回",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );
    await unpublishPerformanceReview(id);
    ElMessage.success("撤回成功");
    fetchReviewList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("撤回失败:", error);
      ElMessage.error("撤回失败");
    }
  }
};

// 删除
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      "确定要删除此绩效评估吗？此操作不可恢复。",
      "确认删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "danger",
      },
    );
    await deletePerformanceReview(id);
    ElMessage.success("删除成功");
    fetchReviewList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除失败:", error);
      ElMessage.error("删除失败");
    }
  }
};

// 生命周期
onMounted(() => {
  fetchReviewList();
  fetchEmployeeOptions();
});
</script>

<style scoped>
.performance-review-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.description {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.filter-card {
  margin-bottom: 20px;
}

.data-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.text-muted {
  color: #909399;
}

.score-label {
  margin-left: 8px;
  color: #606266;
  font-size: 14px;
}

.content-text {
  white-space: pre-wrap;
  word-break: break-all;
  color: #303133;
}

/* 响应式 */
@media (max-width: 1024px) {
  .filter-row {
    flex-wrap: wrap;
    gap: 12px;
  }

  .filter-item {
    flex: 1;
    min-width: 150px;
  }

  .filter-item.search {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .filter-row {
    flex-direction: column;
  }

  .filter-item {
    width: 100%;
    min-width: unset;
  }

  .review-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .review-info {
    width: 100%;
  }

  .employee-cell {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .employee-details {
    font-size: 12px;
  }

  .action-btns {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 480px) {
  .action-btns {
    flex-wrap: wrap;
    gap: 8px;
  }

  .action-btns .el-button {
    flex: 1;
    min-width: 80px;
  }

  .pagination-container {
    justify-content: center;
  }
}
</style>
