<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import {
  ElCard, ElTable, ElTableColumn, ElButton, ElTag, ElInput,
  ElDialog, ElForm, ElFormItem, ElSelect, ElOption,
  ElSwitch, ElMessage, ElMessageBox, ElPagination, ElEmpty
} from 'element-plus'
import {
  getNoticeList, createNotice, updateNotice, deleteNotice,
  publishNotice, unpublishNotice
} from '@/api/notice'
import { formatDateTime } from '@/utils/format'

// 响应式状态
const noticeList = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新建公告')
const isEditing = ref(false)
const currentNotice = ref(null)

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const filters = reactive({
  is_published: '',  // '', 'true', 'false'
  is_pinned: ''      // '', 'true', 'false'
})

// 表单数据
const formData = reactive({
  title: '',
  content: '',
  is_pinned: false,
  is_published: false
})

const formRules = {
  title: [
    { required: true, message: '请输入公告标题', trigger: 'blur' },
    { min: 2, max: 200, message: '标题长度在 2-200 个字符之间', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入公告内容', trigger: 'blur' }
  ]
}

const formRef = ref(null)

// 获取公告列表
const fetchNoticeList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (filters.is_published !== '') {
      params.is_published = filters.is_published
    }
    if (filters.is_pinned !== '') {
      params.is_pinned = filters.is_pinned
    }

    const res = await getNoticeList(params)
    const responseData = res.data?.data || res.data?.results || []
    const totalCount = res.data?.total || res.data?.count || 0

    noticeList.value = responseData.map(item => ({
      id: item.id,
      title: item.title,
      content: item.content,
      is_pinned: item.is_pinned,
      is_published: item.is_published,
      published_by_name: item.published_by_name,
      published_at: item.published_at,
      created_at: item.created_at,
      updated_at: item.updated_at
    }))
    pagination.total = totalCount
  } catch (error) {
    console.error('获取公告列表失败:', error)
    ElMessage.error('获取公告列表失败')
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  formData.title = ''
  formData.content = ''
  formData.is_pinned = false
  formData.is_published = false
  currentNotice.value = null
  isEditing.value = false
  dialogTitle.value = '新建公告'
}

// 打开新建对话框
const openCreateDialog = () => {
  resetForm()
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (row) => {
  currentNotice.value = row
  isEditing.value = true
  dialogTitle.value = '编辑公告'

  formData.title = row.title
  formData.content = row.content
  formData.is_pinned = row.is_pinned
  formData.is_published = row.is_published

  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    const data = {
      title: formData.title,
      content: formData.content,
      is_pinned: formData.is_pinned,
      is_published: formData.is_published
    }

    if (isEditing.value) {
      await updateNotice(currentNotice.value.id, data)
      ElMessage.success('更新公告成功')
    } else {
      await createNotice(data)
      ElMessage.success('创建公告成功')
    }

    dialogVisible.value = false
    fetchNoticeList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('提交失败:', error)
    }
  }
}

// 删除公告
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除公告「${row.title}」吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteNotice(row.id)
    ElMessage.success('删除公告成功')
    fetchNoticeList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 发布/撤回公告
const togglePublish = async (row) => {
  try {
    if (row.is_published) {
      await unpublishNotice(row.id)
      ElMessage.success('已撤回公告')
    } else {
      await publishNotice(row.id)
      ElMessage.success('已发布公告')
    }
    fetchNoticeList()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 切换置顶状态
const togglePinned = async (row) => {
  try {
    const data = { is_pinned: !row.is_pinned }
    await updateNotice(row.id, data)
    ElMessage.success(row.is_pinned ? '已取消置顶' : '已设为置顶')
    fetchNoticeList()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 筛选处理
const handleFilterChange = () => {
  pagination.page = 1
  fetchNoticeList()
}

// 分页处理
const handlePageChange = (page) => {
  pagination.page = page
  fetchNoticeList()
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  fetchNoticeList()
}

// 状态文本和颜色
const publishedStatus = computed(() => ({
  text: (val) => val ? '已发布' : '草稿',
  type: (val) => val ? 'success' : 'info'
}))

onMounted(() => {
  fetchNoticeList()
})
</script>

<template>
  <div class="notice-management-container">
    <div class="page-header">
      <div class="header-left">
        <h2>公告管理</h2>
        <p class="subtitle">管理系统公告，支持发布、置顶和删除</p>
      </div>
      <el-button type="primary" @click="openCreateDialog">
        + 新建公告
      </el-button>
    </div>

    <!-- 筛选区域 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" class="filter-form">
        <el-form-item label="发布状态">
          <el-select
            v-model="filters.is_published"
            placeholder="全部"
            clearable
            @change="handleFilterChange"
          >
            <el-option label="已发布" value="true" />
            <el-option label="草稿" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="置顶状态">
          <el-select
            v-model="filters.is_pinned"
            placeholder="全部"
            clearable
            @change="handleFilterChange"
          >
            <el-option label="已置顶" value="true" />
            <el-option label="普通" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchNoticeList">
            查询
          </el-button>
          <el-button @click="filters.is_published = ''; filters.is_pinned = ''; fetchNoticeList()">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 公告列表 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="noticeList"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="title" label="公告标题" min-width="200">
          <template #default="{ row }">
            <div class="title-cell">
              <el-tag
                v-if="row.is_pinned"
                type="warning"
                size="small"
                effect="dark"
                class="pinned-tag"
              >
                置顶
              </el-tag>
              <span class="title-text">{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="is_published" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="publishedStatus.type(row.is_published)">
              {{ publishedStatus.text(row.is_published) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="published_by_name" label="发布人" width="120" align="center" />

        <el-table-column prop="published_at" label="发布时间" width="160" align="center">
          <template #default="{ row }">
            {{ formatDateTime(row.published_at || row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                type="primary"
                link
                size="small"
                @click="openEditDialog(row)"
              >
                编辑
              </el-button>

              <el-button
                :type="row.is_published ? 'warning' : 'success'"
                link
                size="small"
                @click="togglePublish(row)"
              >
                {{ row.is_published ? '撤回' : '发布' }}
              </el-button>

              <el-button
                :type="row.is_pinned ? 'info' : ''"
                link
                size="small"
                @click="togglePinned(row)"
              >
                {{ row.is_pinned ? '取消置顶' : '置顶' }}
              </el-button>

              <el-button
                type="danger"
                link
                size="small"
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && noticeList.length === 0" description="暂无公告" />

      <div class="pagination-wrapper" v-if="pagination.total > pagination.page_size">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 30, 50]"
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
      :title="dialogTitle"
      width="700px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="formData.title"
            placeholder="请输入公告标题"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="formData.content"
            type="textarea"
            :rows="10"
            placeholder="请输入公告内容（支持 Markdown 格式）"
          />
        </el-form-item>

        <el-form-item label="置顶">
          <el-switch v-model="formData.is_pinned" />
          <span class="form-tip">置顶公告将在列表中优先显示</span>
        </el-form-item>

        <el-form-item label="发布">
          <el-switch v-model="formData.is_published" />
          <span class="form-tip">发布后所有用户都可查看</span>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">
          {{ isEditing ? '保存修改' : '创建公告' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.notice-management-container {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 112px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-left h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.filter-card {
  margin-bottom: 16px;
  border-radius: 8px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
}

.table-card {
  border-radius: 8px;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pinned-tag {
  flex-shrink: 0;
}

.title-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 16px 0;
}

.form-tip {
  margin-left: 8px;
  color: #909399;
  font-size: 13px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .filter-section {
    flex-wrap: wrap;
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

  .filter-section {
    flex-direction: column;
  }

  .filter-item {
    width: 100%;
    min-width: unset;
  }

  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .notice-title {
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

@media (max-width: 480px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }

  .action-btns {
    flex-direction: column;
    gap: 8px;
  }

  .action-btns .el-button {
    width: 100%;
  }

  .pagination-wrapper {
    padding: 12px 0;
  }

  .pagination-wrapper .el-pagination {
    justify-content: center;
  }
}
</style>
