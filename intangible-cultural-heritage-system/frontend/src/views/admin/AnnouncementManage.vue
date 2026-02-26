<template>
  <div class="announcement-manage">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-seal">
          <span class="seal-text">公告</span>
        </div>
        <div class="header-texts">
          <h1 class="page-title">公告管理</h1>
          <p class="page-subtitle">管理平台通知公告</p>
        </div>
      </div>
      <button class="add-btn" @click="handleAdd">
        <span class="btn-seal">增</span>
        <span>新增公告</span>
      </button>
    </header>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="公告标题">
          <el-input
            v-model="filters.title"
            placeholder="搜索标题"
            clearable
            @clear="handleSearch"
            class="heritage-input"
          />
        </el-form-item>
        <el-form-item label="发布状态">
          <el-select
            v-model="filters.is_published"
            placeholder="选择状态"
            clearable
            @change="handleSearch"
            class="heritage-select"
          >
            <el-option label="已发布" :value="true" />
            <el-option label="草稿" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <button class="action-btn search-btn" @click="handleSearch">搜索</button>
          <button class="action-btn reset-btn" @click="handleReset">重置</button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 表格 -->
    <div class="table-frame">
      <el-table
        :data="tableData"
        v-loading="loading"
        class="data-table"
        row-key="id"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="250">
          <template #default="{ row }">
            <div class="title-cell">
              <span v-if="row.is_top" class="top-tag">置顶</span>
              <span>{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_published ? 'success' : 'info'" size="small">
              {{ row.is_published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="置顶" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.is_top" type="warning" size="small">置顶</el-tag>
            <span v-else class="empty-text">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="author_name" label="作者" width="120" />
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <button class="table-action-btn edit-btn" @click="handleEdit(row)">编辑</button>
            <button
              class="table-action-btn"
              :class="row.is_published ? 'unpublish-btn' : 'publish-btn'"
              @click="handleTogglePublish(row)"
            >
              {{ row.is_published ? '下架' : '发布' }}
            </button>
            <button
              class="table-action-btn"
              :class="row.is_top ? 'untop-btn' : 'top-btn'"
              @click="handleToggleTop(row)"
            >
              {{ row.is_top ? '取消置顶' : '置顶' }}
            </button>
            <button class="table-action-btn delete-btn" @click="handleDelete(row)">删除</button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          background
          @current-change="fetchList"
        />
      </div>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑公告' : '新增公告'"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form :model="form" label-width="80px" class="announcement-form">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" placeholder="请输入公告标题" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="内容" required>
          <div class="editor-container">
            <el-input
              v-model="form.content"
              type="textarea"
              :rows="12"
              placeholder="请输入公告内容（支持 HTML 格式）"
              class="content-editor"
            />
            <div class="preview-toggle">
              <el-checkbox v-model="showPreview">显示预览</el-checkbox>
            </div>
            <div v-if="showPreview" class="content-preview">
              <div class="preview-label">预览效果</div>
              <div class="preview-content" v-html="sanitizeContent(form.content)"></div>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="发布">
          <el-switch v-model="form.is_published" />
          <span class="switch-hint">{{ form.is_published ? '发布后用户可见' : '保存为草稿' }}</span>
        </el-form-item>
        <el-form-item label="置顶">
          <el-switch v-model="form.is_top" />
          <span class="switch-hint">{{ form.is_top ? '置顶显示在列表最前面' : '普通公告' }}</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="saving" @click="handleSave">
            {{ isEdit ? '保存修改' : '创建公告' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAnnouncementList, createAnnouncement, updateAnnouncement, deleteAnnouncement } from '@/api/announcement'
import type { Announcement, AnnouncementCreate, AnnouncementListParams } from '@/types'
import DOMPurify from 'dompurify'

const sanitizeContent = (content: string) => {
  return DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['p', 'br', 'b', 'i', 'em', 'strong', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                   'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'pre', 'code', 'span', 'div', 'table',
                   'tr', 'td', 'th', 'thead', 'tbody'],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style']
  })
}

const tableData = ref<Announcement[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const filters = reactive({
  title: '',
  is_published: undefined as boolean | undefined
})
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(0)
const saving = ref(false)
const showPreview = ref(false)
const form = reactive<AnnouncementCreate>({
  title: '',
  content: '',
  is_published: false,
  is_top: false
})

const fetchList = async () => {
  loading.value = true
  try {
    const params: AnnouncementListParams = {
      page: page.value,
      page_size: pageSize.value
    }
    if (filters.title) {
      params.title = filters.title
    }
    if (filters.is_published !== undefined) {
      params.is_published = filters.is_published
    }
    const res = await getAnnouncementList(params)
    tableData.value = res.data.data || []
    total.value = res.data.total || 0
  } catch (error) {
    ElMessage.error('获取公告列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  fetchList()
}

const handleReset = () => {
  filters.title = ''
  filters.is_published = undefined
  handleSearch()
}

const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, {
    title: '',
    content: '',
    is_published: false,
    is_top: false
  })
  showPreview.value = false
  dialogVisible.value = true
}

const handleEdit = (row: Announcement) => {
  isEdit.value = true
  editingId.value = row.id
  Object.assign(form, {
    title: row.title,
    content: row.content,
    is_published: row.is_published,
    is_top: row.is_top
  })
  showPreview.value = false
  dialogVisible.value = true
}

const handleSave = async () => {
  if (!form.title.trim()) {
    ElMessage.warning('请输入公告标题')
    return
  }
  if (!form.content.trim()) {
    ElMessage.warning('请输入公告内容')
    return
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await updateAnnouncement(editingId.value, form)
      ElMessage.success('公告更新成功')
    } else {
      await createAnnouncement(form)
      ElMessage.success('公告创建成功')
    }
    dialogVisible.value = false
    fetchList()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新公告失败' : '创建公告失败')
  } finally {
    saving.value = false
  }
}

const handleDelete = async (row: Announcement) => {
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
    await deleteAnnouncement(row.id)
    ElMessage.success('公告删除成功')
    fetchList()
  } catch (error) {
    // 用户取消或删除失败
  }
}

const handleTogglePublish = async (row: Announcement) => {
  const newStatus = !row.is_published
  try {
    await updateAnnouncement(row.id, { is_published: newStatus })
    ElMessage.success(newStatus ? '公告已发布' : '公告已下架')
    fetchList()
  } catch (error) {
    ElMessage.error(newStatus ? '发布失败' : '下架失败')
  }
}

const handleToggleTop = async (row: Announcement) => {
  const newStatus = !row.is_top
  try {
    await updateAnnouncement(row.id, { is_top: newStatus })
    ElMessage.success(newStatus ? '公告已置顶' : '已取消置顶')
    fetchList()
  } catch (error) {
    ElMessage.error(newStatus ? '置顶失败' : '取消置顶失败')
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchList)
</script>

<style scoped>
.announcement-manage {
  padding: 0;
}

/* 页面头部 */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  background: linear-gradient(135deg, #2F3640 0%, #1a2026 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-seal {
  width: 56px;
  height: 56px;
  background: #C23531;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(194, 35, 49, 0.5);
}

.seal-text {
  color: #F7F4ED;
  font-size: 18px;
  font-weight: 700;
  font-family: "STSong", "SimSun", serif;
}

.header-texts {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #F7F4ED;
  margin: 0;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
}

.page-subtitle {
  font-size: 12px;
  color: rgba(247, 244, 237, 0.7);
  margin: 4px 0 0;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #C23531;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.add-btn:hover {
  background: #DC143C;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(194, 35, 49, 0.4);
}

.btn-seal {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "STSong", "SimSun", serif;
}

/* 筛选区域 */
.filter-section {
  margin: 24px 32px;
  padding: 20px 24px;
  background: #FFFBF5;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.heritage-input {
  width: 200px;
}

.heritage-select {
  width: 150px;
}

.action-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn {
  background: #C23531;
  color: #fff;
}

.search-btn:hover {
  background: #DC143C;
}

.reset-btn {
  background: #909399;
  color: #fff;
}

.reset-btn:hover {
  background: #606266;
}

/* 表格 */
.table-frame {
  margin: 0 32px 24px;
  background: #FFFBF5;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.data-table {
  width: 100%;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.top-tag {
  padding: 2px 8px;
  background: #E6A23C;
  color: #fff;
  font-size: 12px;
  border-radius: 4px;
  flex-shrink: 0;
}

.table-action-btn {
  padding: 4px 10px;
  margin-right: 4px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
  background: #409EFF;
  color: #fff;
}

.table-action-btn:hover {
  opacity: 0.8;
}

.edit-btn {
  background: #409EFF;
}

.publish-btn {
  background: #67C23A;
}

.unpublish-btn {
  background: #E6A23C;
}

.top-btn {
  background: #E6A23C;
}

.untop-btn {
  background: #909399;
}

.delete-btn {
  background: #F56C6C;
}

.delete-btn:hover {
  background: #DC143C;
}

.empty-text {
  color: #C0C4CC;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  background: #fff;
  border-top: 1px solid #EBEEF5;
}

/* 编辑对话框 */
.announcement-form {
  padding: 0 20px;
}

.editor-container {
  width: 100%;
}

.content-editor {
  font-family: monospace;
}

.preview-toggle {
  margin: 12px 0;
}

.content-preview {
  margin-top: 16px;
  padding: 16px;
  background: #F5F7FA;
  border-radius: 8px;
}

.preview-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 12px;
}

.preview-content {
  line-height: 1.8;
}

.preview-content :deep(img) {
  max-width: 100%;
}

.switch-hint {
  margin-left: 12px;
  font-size: 13px;
  color: #909399;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-table) {
  --el-table-border-color: rgba(212, 175, 55, 0.2);
  --el-table-header-bg-color: #FAFAFA;
}

:deep(.el-table th.el-table__cell) {
  background: #FAFAFA;
  font-weight: 600;
  color: #606266;
}
</style>
