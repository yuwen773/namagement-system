<template>
  <div class="user-manage-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>用户管理</h2>
    </div>

    <!-- 筛选条件 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="搜索">
          <el-input
            v-model="filterForm.search"
            placeholder="手机号/昵称"
            clearable
            style="width: 200px"
            :prefix-icon="Search"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="全部状态" clearable style="width: 120px">
            <el-option label="正常" value="active" />
            <el-option label="已禁用" value="banned" />
          </el-select>
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="filterForm.is_staff" placeholder="全部类型" clearable style="width: 120px">
            <el-option label="管理员" :value="true" />
            <el-option label="普通用户" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :src="row.avatar" :size="50">
              {{ row.nickname?.charAt(0) || 'U' }}
            </el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="nickname" label="昵称" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="points" label="积分" width="100" align="right">
          <template #default="{ row }">
            <span class="points">{{ row.points?.toLocaleString() || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
              {{ row.status === 'active' ? '正常' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_staff" label="用户类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_staff ? 'warning' : 'info'" size="small">
              {{ row.is_staff ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" :icon="View" @click="handleView(row)">查看</el-button>
            <el-button
              v-if="row.status === 'active'"
              link
              type="danger"
              size="small"
              @click="handleToggleStatus(row)"
            >
              禁用
            </el-button>
            <el-button
              v-else
              link
              type="success"
              size="small"
              @click="handleToggleStatus(row)"
            >
              启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
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
    </el-card>

    <!-- 用户详情对话框 -->
    <UserDetailDialog
      v-model="detailDialogVisible"
      :user-id="currentUserId"
      @refresh="fetchUserList"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, View
} from '@element-plus/icons-vue'
import {
  getUserListApi,
  getUserDetailApi,
  updateUserStatusApi
} from '@/api/modules/user'
import UserDetailDialog from './components/UserDetailDialog.vue'

// 筛选表单
const filterForm = reactive({
  search: '',
  status: '',
  is_staff: null
})

// 表格数据
const loading = ref(false)
const tableData = ref([])

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框
const detailDialogVisible = ref(false)
const currentUserId = ref(null)

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取用户列表
const fetchUserList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: filterForm.search || undefined,
      status: filterForm.status || undefined,
      is_staff: filterForm.is_staff
    }

    const response = await getUserListApi(params)
    tableData.value = response.results || []
    pagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchUserList()
}

// 重置
const handleReset = () => {
  Object.assign(filterForm, {
    search: '',
    status: '',
    is_staff: null
  })
  pagination.page = 1
  fetchUserList()
}

// 分页变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchUserList()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchUserList()
}

// 查看用户详情
const handleView = (row) => {
  currentUserId.value = row.id
  detailDialogVisible.value = true
}

// 切换用户状态
const handleToggleStatus = async (row) => {
  const newStatus = row.status === 'active' ? 'banned' : 'active'
  const action = newStatus === 'banned' ? '禁用' : '启用'

  try {
    await ElMessageBox.confirm(
      `确定要${action}用户"${row.nickname || row.phone}"吗？${newStatus === 'banned' ? '禁用后该用户将无法登录系统。' : ''}`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await updateUserStatusApi(row.id, newStatus)
    ElMessage.success(`${action}成功`)
    fetchUserList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`${action}失败`)
    }
  }
}

// 初始化
onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
.user-manage-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.filter-card {
  border: 1px solid #e8e8e8;
}

.filter-form {
  margin: 0;
}

.table-card {
  border: 1px solid #e8e8e8;
}

.points {
  font-weight: 600;
  color: #f97316;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

/* Element Plus 样式调整 */
:deep(.el-card__body) {
  padding: 16px;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table .cell) {
  padding: 8px 0;
}

:deep(.el-avatar) {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
}
</style>
