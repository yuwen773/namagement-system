<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminAnnouncementApi } from '@/api'
import Pagination from '@/components/common/Pagination.vue'
import {
  Bell, Search, Plus, Refresh, Delete, Edit, View,
  Filter, CircleCheck, CircleClose, Top
} from '@element-plus/icons-vue'

const router = useRouter()

const announcements = ref([])
const loading = ref(false)
const total = ref(0)

const searchForm = ref({
  status: '',
  priority: ''
})

const pagination = ref({
  page: 1,
  page_size: 20
})

const priorityOptions = [
  { label: '普通', value: 1 },
  { label: '重要', value: 2 },
  { label: '紧急', value: 3 }
]

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' }
]

const loadAnnouncements = async () => {
  try {
    loading.value = true
    const params = {
      ...pagination.value,
      ...searchForm.value
    }

    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key]
      }
    })

    const res = await adminAnnouncementApi.getList(params)
    if (res.code === 0) {
      announcements.value = res.data || []
      total.value = res.total || 0
    }
  } catch (error) {
    ElMessage.error('加载公告数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  loadAnnouncements()
}

const handleReset = () => {
  searchForm.value = { status: '', priority: '' }
  pagination.value.page = 1
  loadAnnouncements()
}

const handlePageChange = (page) => {
  pagination.value.page = page
  loadAnnouncements()
}

const handlePageSizeChange = (size) => {
  pagination.value.page_size = size
  pagination.value.page = 1
  loadAnnouncements()
}

const handleCreate = () => {
  router.push('/admin/announcements/edit')
}

const handleEdit = (id) => {
  router.push(`/admin/announcements/edit?id=${id}`)
}

const handleView = (id) => {
  router.push(`/admin/announcements/edit?id=${id}&view=1`)
}

const handleDelete = (announcement) => {
  ElMessageBox.confirm(
    `确定要删除公告 "${announcement.title}" 吗？`,
    '确认删除',
    { type: 'warning' }
  ).then(async () => {
    try {
      const res = await adminAnnouncementApi.delete(announcement.id)
      if (res.code === 0) {
        ElMessage.success('删除成功')
        loadAnnouncements()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const handleTogglePublish = async (announcement) => {
  const isPublishing = announcement.status === 'draft'
  const actionText = isPublishing ? '发布' : '取消发布'
  const message = isPublishing
    ? `确定要发布公告 "${announcement.title}" 吗？`
    : `确定要取消发布 "${announcement.title}" 吗？`

  ElMessageBox.confirm(message, `确认${actionText}`, {
    type: isPublishing ? 'info' : 'warning'
  }).then(async () => {
    try {
      let res
      if (isPublishing) {
        res = await adminAnnouncementApi.publish(announcement.id)
      } else {
        res = await adminAnnouncementApi.unpublish(announcement.id)
      }
      if (res.code === 0) {
        ElMessage.success(`${actionText}成功`)
        loadAnnouncements()
      }
    } catch (error) {
      ElMessage.error(`${actionText}失败`)
    }
  }).catch(() => {})
}

const getPriorityConfig = (priority) => {
  const configs = {
    1: { color: '#60a5fa', bg: 'rgba(96, 165, 250, 0.15)', text: '普通' },
    2: { color: '#fbbf24', bg: 'rgba(251, 191, 36, 0.15)', text: '重要' },
    3: { color: '#f87171', bg: 'rgba(248, 113, 113, 0.15)', text: '紧急' }
  }
  return configs[priority] || configs[1]
}

const getStatusConfig = (status) => {
  const configs = {
    draft: { color: '#9ca3af', text: '草稿' },
    published: { color: '#34d399', text: '已发布' }
  }
  return configs[status] || configs.draft
}

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

onMounted(() => {
  loadAnnouncements()
})
</script>

<template>
  <div class="announcements-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <div class="icon-wrapper">
            <Bell :size="24" />
          </div>
          <div>
            <h1>公告管理</h1>
            <p class="subtitle">管理系统通知与公告发布</p>
          </div>
        </div>
        <div class="actions">
          <el-button type="primary" :icon="Plus" @click="handleCreate" class="create-btn">
            新建公告
          </el-button>
          <el-button :icon="Refresh" @click="loadAnnouncements" class="refresh-btn">
            刷新
          </el-button>
        </div>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="filter-tabs">
        <button
          :class="['filter-tab', { active: searchForm.status === '' }]"
          @click="searchForm.status = ''; loadAnnouncements()"
        >
          全部
        </button>
        <button
          :class="['filter-tab', { active: searchForm.status === 'published' }]"
          @click="searchForm.status = 'published'; loadAnnouncements()"
        >
          已发布
        </button>
        <button
          :class="['filter-tab', { active: searchForm.status === 'draft' }]"
          @click="searchForm.status = 'draft'; loadAnnouncements()"
        >
          草稿
        </button>
      </div>
      <div class="filter-controls">
        <el-select
          v-model="searchForm.priority"
          placeholder="优先级"
          clearable
          class="priority-select"
        >
          <el-option
            v-for="item in priorityOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-button type="primary" :icon="Filter" @click="handleSearch" class="filter-btn">
          筛选
        </el-button>
      </div>
    </div>

    <!-- Table Section -->
    <div class="table-section">
      <div v-loading="loading" class="table-container">
        <div class="announcement-list">
          <div
            v-for="item in announcements"
            :key="item.id"
            class="announcement-row"
            :class="{ pinned: item.is_pinned }"
          >
            <div class="row-main">
              <div class="row-header">
                <div class="priority-badge" :style="getPriorityConfig(item.priority)">
                  {{ getPriorityConfig(item.priority).text }}
                </div>
                <div class="status-dot" :style="{ backgroundColor: getStatusConfig(item.status).color }"></div>
                <h3 class="announcement-title">{{ item.title }}</h3>
                <Top v-if="item.is_pinned" :size="16" class="pin-icon" />
              </div>
              <p class="announcement-preview">{{ item.content }}</p>
              <div class="row-meta">
                <span class="meta-item">
                  <span class="meta-label">状态:</span>
                  <span :style="{ color: getStatusConfig(item.status).color }">
                    {{ getStatusConfig(item.status).text }}
                  </span>
                </span>
                <span class="meta-item">
                  <span class="meta-label">创建:</span>
                  {{ formatTime(item.created_at) }}
                </span>
                <span v-if="item.published_at" class="meta-item">
                  <span class="meta-label">发布:</span>
                  {{ formatTime(item.published_at) }}
                </span>
              </div>
            </div>
            <div class="row-actions">
              <el-button :icon="View" size="small" text @click="handleView(item.id)">
                查看
              </el-button>
              <el-button :icon="Edit" size="small" text @click="handleEdit(item.id)">
                编辑
              </el-button>
              <el-button
                v-if="item.status === 'draft'"
                :icon="CircleCheck"
                size="small"
                type="success"
                text
                @click="handleTogglePublish(item)"
              >
                发布
              </el-button>
              <el-button
                v-else
                :icon="CircleClose"
                size="small"
                type="warning"
                text
                @click="handleTogglePublish(item)"
              >
                撤回
              </el-button>
              <el-button :icon="Delete" size="small" type="danger" text @click="handleDelete(item)">
                删除
              </el-button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && announcements.length === 0" class="empty-state">
          <div class="empty-icon">📢</div>
          <p>暂无公告</p>
          <el-button type="primary" :icon="Plus" @click="handleCreate">
            创建第一个公告
          </el-button>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="total > 0" class="pagination-wrapper">
        <Pagination
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="total"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.announcements-page {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title-section {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.3);
}

h1 {
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.5px;
}

.subtitle {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.actions {
  display: flex;
  gap: 12px;
}

.create-btn {
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  border: none;
  padding: 12px 24px;
  font-weight: 600;
}

.create-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.refresh-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* Filter Section */
.filter-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
}

.filter-tab {
  padding: 10px 20px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
  font-size: 14px;
  font-weight: 500;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.filter-tab.active {
  background: rgba(255, 107, 53, 0.15);
  color: #FF6B35;
}

.filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.priority-select {
  width: 120px;
}

.priority-select :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.filter-btn {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Table Section */
.table-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
}

.table-container {
  min-height: 400px;
}

.announcement-list {
  display: flex;
  flex-direction: column;
}

.announcement-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
  gap: 24px;
}

.announcement-row:last-child {
  border-bottom: none;
}

.announcement-row:hover {
  background: rgba(255, 255, 255, 0.03);
}

.announcement-row.pinned {
  background: linear-gradient(90deg, rgba(255, 107, 53, 0.08) 0%, transparent 100%);
  border-left: 3px solid #FF6B35;
}

.row-main {
  flex: 1;
  min-width: 0;
}

.row-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.priority-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.announcement-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pin-icon {
  color: #FF6B35;
  flex-shrink: 0;
}

.announcement-preview {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
}

.meta-item {
  display: flex;
  gap: 6px;
  color: rgba(255, 255, 255, 0.4);
}

.meta-label {
  color: rgba(255, 255, 255, 0.3);
}

.row-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.row-actions .el-button {
  color: rgba(255, 255, 255, 0.6);
}

.row-actions .el-button:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.4);
}

/* Pagination */
.pagination-wrapper {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.pagination-wrapper :deep(.el-pagination) {
  justify-content: center;
}

.pagination-wrapper :deep(.el-pager li) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}

.pagination-wrapper :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  border-color: transparent;
  color: #fff;
}
</style>
