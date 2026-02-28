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
  search: '',
  status: '',
  priority: ''
})

const showFilters = ref(false)

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
  searchForm.value = { search: '', status: '', priority: '' }
  showFilters.value = false
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
    1: { color: '#00B4D8', bg: 'rgba(0, 180, 216, 0.12)', text: '普通' },
    2: { color: '#FFB800', bg: 'rgba(255, 184, 0, 0.12)', text: '重要' },
    3: { color: '#DC2626', bg: 'rgba(220, 38, 38, 0.12)', text: '紧急' }
  }
  return configs[priority] || configs[1]
}

const getStatusConfig = (status) => {
  const configs = {
    draft: { color: '#A8A29E', text: '草稿' },
    published: { color: '#52B788', text: '已发布' }
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
  <div class="announcements-container">
    <!-- 装饰叶子 -->
    <div class="leaf-decoration leaf-decoration--1">
      <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
        <path d="M50 5C50 5 85 25 85 55C85 85 65 95 50 95C35 95 15 85 15 55C15 25 50 5 50 5Z" fill="currentColor" opacity="0.04"/>
      </svg>
    </div>

    <!-- 顶部欢迎区 -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-icon-wrapper">
          <Bell class="header-icon" />
        </div>
        <div>
          <h1 class="header-title">公告管理</h1>
          <p class="header-subtitle">管理系统通知与公告发布，支持优先级和置顶设置</p>
        </div>
      </div>
      <div class="header-actions">
        <button class="action-btn action-btn--primary" @click="handleCreate">
          <Plus class="icon" />
          <span>新建公告</span>
        </button>
        <button class="action-btn action-btn--secondary" @click="loadAnnouncements" :class="{ loading }">
          <Refresh class="icon" :class="{ spinning: loading }" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <!-- 统计指标卡片 -->
    <div class="metrics-grid">
      <div class="metric-card metric-card--green" style="--i: 0">
        <div class="metric-header">
          <div class="metric-icon">
            <Bell class="icon" />
          </div>
          <span class="metric-badge">总计</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">公告总数</p>
          <p class="metric-value">{{ total }}</p>
        </div>
        <div class="metric-leaf">
          <svg width="45" height="45" viewBox="0 0 45 45" fill="none">
            <path d="M22.5 4C22.5 4 40 14 40 28C40 42 32 45 22.5 45C13 45 5 42 5 28C5 14 22.5 4 22.5 4Z" fill="currentColor" opacity="0.1"/>
          </svg>
        </div>
      </div>

      <div class="metric-card metric-card--teal" style="--i: 1">
        <div class="metric-header">
          <div class="metric-icon">
            <CircleCheck class="icon" />
          </div>
          <span class="metric-badge metric-badge--success">已发布</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">已发布</p>
          <p class="metric-value">{{ announcements.filter(a => a.status === 'published').length }}</p>
        </div>
        <div class="metric-leaf">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <path d="M20 4C20 4 36 13 36 26C36 39 28 42 20 42C12 42 4 39 4 26C4 13 20 4 20 4Z" fill="currentColor" opacity="0.1"/>
          </svg>
        </div>
      </div>

      <div class="metric-card metric-card--blue" style="--i: 2">
        <div class="metric-header">
          <div class="metric-icon">
            <Top class="icon" />
          </div>
          <span class="metric-badge metric-badge--admin">置顶</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">置顶公告</p>
          <p class="metric-value">{{ announcements.filter(a => a.is_pinned).length }}</p>
        </div>
        <div class="metric-leaf">
          <svg width="35" height="35" viewBox="0 0 35 35" fill="none">
            <path d="M17.5 3C17.5 3 32 11 32 24C32 37 24 40 17.5 40C11 40 3 37 3 24C3 11 17.5 3 17.5 3Z" fill="currentColor" opacity="0.1"/>
          </svg>
        </div>
      </div>

      <div class="metric-card metric-card--warning" style="--i: 3">
        <div class="metric-header">
          <div class="metric-icon">
            <Edit class="icon" />
          </div>
          <span class="metric-badge metric-badge--warning">草稿</span>
        </div>
        <div class="metric-body">
          <p class="metric-label">草稿箱</p>
          <p class="metric-value">{{ announcements.filter(a => a.status === 'draft').length }}</p>
        </div>
        <div class="metric-leaf">
          <svg width="35" height="35" viewBox="0 0 35 35" fill="none">
            <path d="M17.5 3C17.5 3 32 11 32 24C32 37 24 40 17.5 40C11 40 3 37 3 24C3 11 17.5 3 17.5 3Z" fill="currentColor" opacity="0.1"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 搜索筛选区 -->
    <div class="filter-panel" style="--i: 0">
      <div class="filter-header">
        <div class="filter-search">
          <Search class="search-icon" />
          <input
            v-model="searchForm.search"
            type="text"
            placeholder="搜索公告标题或内容..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
        </div>
        <div class="filter-actions">
          <button
            class="filter-toggle"
            :class="{ active: showFilters || searchForm.priority || searchForm.status !== '' }"
            @click="showFilters = !showFilters"
          >
            <Filter class="icon" />
            <span>筛选条件</span>
            <span v-if="searchForm.priority || searchForm.status !== ''" class="filter-count">
              {{ [searchForm.priority, searchForm.status !== '' ? searchForm.status : null].filter(Boolean).length }}
            </span>
          </button>
          <button class="filter-btn filter-btn--search" @click="handleSearch">
            <Search class="icon" />
          </button>
          <button class="filter-btn filter-btn--reset" @click="handleReset">
            <span>重置</span>
          </button>
        </div>
      </div>

      <!-- 展开的筛选条件 -->
      <div v-if="showFilters" class="filter-body">
        <div class="filter-group">
          <label class="filter-label">
            <Bell class="label-icon" />
            <span>公告状态</span>
          </label>
          <div class="filter-options">
            <button
              v-for="option in [{value: '', label: '全部'}, {value: 'published', label: '已发布'}, {value: 'draft', label: '草稿'}]"
              :key="option.value"
              class="filter-option"
              :class="{ active: searchForm.status === option.value }"
              @click="searchForm.status = option.value"
            >
              {{ option.label }}
            </button>
          </div>
        </div>

        <div class="filter-divider"></div>

        <div class="filter-group">
          <label class="filter-label">
            <Top class="label-icon" />
            <span>优先级别</span>
          </label>
          <div class="filter-options">
            <button
              v-for="option in [{value: '', label: '全部'}, {value: 1, label: '普通'}, {value: 2, label: '重要'}, {value: 3, label: '紧急'}]"
              :key="option.value"
              class="filter-option"
              :class="{ active: searchForm.priority === option.value }"
              @click="searchForm.priority = option.value"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 公告列表 -->
    <div class="announcements-panel" style="--i: 1">
      <div class="announcements-panel-header">
        <div class="panel-title-group">
          <div class="panel-icon-wrapper">
            <Bell class="icon" />
          </div>
          <div>
            <h3 class="panel-title">公告列表</h3>
            <p class="panel-subtitle">管理所有系统公告和通知消息</p>
          </div>
        </div>
        <div class="panel-badge">列表</div>
      </div>

      <div class="announcements-list-wrapper">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-overlay">
          <div class="loading-content">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="announcements.length === 0" class="empty-state">
          <div class="empty-icon-wrapper">
            <Bell class="empty-icon" />
          </div>
          <p class="empty-title">暂无公告数据</p>
          <p class="empty-desc">点击"新建公告"按钮创建第一个公告</p>
          <button class="empty-action-btn" @click="handleCreate">
            <Plus class="icon" />
            <span>创建第一个公告</span>
          </button>
        </div>

        <!-- 公告卡片列表 -->
        <div v-else class="announcement-cards">
          <div
            v-for="(announcement, index) in announcements"
            :key="announcement.id"
            class="announcement-card"
            :class="{
              'card--pinned': announcement.is_pinned,
              'card--draft': announcement.status === 'draft'
            }"
            :style="{ '--i': index }"
          >
            <!-- 卡片左侧装饰条 -->
            <div class="card-accent" :data-priority="announcement.priority"></div>

            <!-- 卡片内容区 -->
            <div class="card-main">
              <!-- 卡片顶部 -->
              <div class="card-header">
                <div class="header-left">
                  <div class="priority-indicator" :class="`priority--${announcement.priority}`">
                    <span class="priority-dot"></span>
                    <span class="priority-text">{{ getPriorityConfig(announcement.priority).text }}</span>
                  </div>

                  <div class="status-indicator" :class="`status--${announcement.status}`">
                    <component :is="announcement.status === 'published' ? CircleCheck : Edit" class="status-icon" />
                    <span class="status-text">{{ getStatusConfig(announcement.status).text }}</span>
                  </div>

                  <div v-if="announcement.is_pinned" class="pin-badge">
                    <Top class="pin-icon" />
                    <span>置顶</span>
                  </div>
                </div>

                <div class="header-right">
                  <span class="card-id">#{{ announcement.id }}</span>
                </div>
              </div>

              <!-- 卡片主体 -->
              <div class="card-body">
                <h3 class="card-title">{{ announcement.title }}</h3>
                <p class="card-content">{{ announcement.content }}</p>

                <div class="card-meta">
                  <div class="meta-item">
                    <span class="meta-icon">📅</span>
                    <span class="meta-label">创建于</span>
                    <span class="meta-value">{{ formatTime(announcement.created_at) }}</span>
                  </div>
                  <div v-if="announcement.published_at" class="meta-item">
                    <span class="meta-icon">✈️</span>
                    <span class="meta-label">发布于</span>
                    <span class="meta-value">{{ formatTime(announcement.published_at) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 卡片操作区 -->
            <div class="card-actions">
              <button class="action-icon-btn action-icon-btn--view" title="查看" @click="handleView(announcement.id)">
                <View class="icon" />
              </button>
              <button class="action-icon-btn action-icon-btn--edit" title="编辑" @click="handleEdit(announcement.id)">
                <Edit class="icon" />
              </button>
              <button
                v-if="announcement.status === 'draft'"
                class="action-icon-btn action-icon-btn--publish"
                title="发布"
                @click="handleTogglePublish(announcement)"
              >
                <CircleCheck class="icon" />
              </button>
              <button
                v-else
                class="action-icon-btn action-icon-btn--unpublish"
                title="撤回"
                @click="handleTogglePublish(announcement)"
              >
                <CircleClose class="icon" />
              </button>
              <button
                class="action-icon-btn action-icon-btn--delete"
                title="删除"
                @click="handleDelete(announcement)"
              >
                <Delete class="icon" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="total > 0" class="announcements-pagination">
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.announcements-container {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
  animation: pageFadeIn 0.5s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  color: var(--primary-green);
}

.leaf-decoration--1 {
  top: -20px;
  right: -20px;
  opacity: 0.5;
}

/* ============================================
   Dashboard Header
   ============================================ */
.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 18px;
}

.header-icon-wrapper {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(82, 183, 136, 0.08));
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 20px;
  animation: headerFloat 4s ease-in-out infinite;
}

@keyframes headerFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.header-icon {
  width: 28px;
  height: 28px;
  color: var(--primary-green);
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 22px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-btn .icon {
  width: 17px;
  height: 17px;
  transition: transform 0.3s ease;
}

.action-btn .icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-green), var(--primary-teal));
  color: white;
  box-shadow: 0 4px 15px rgba(45, 106, 79, 0.25);
}

.action-btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(45, 106, 79, 0.35);
}

.action-btn--secondary {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
  box-shadow: var(--shadow-soft);
}

.action-btn--secondary:hover {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
}

.action-btn.loading {
  opacity: 0.7;
  pointer-events: none;
}

/* ============================================
   Metrics Grid
   ============================================ */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  position: relative;
  z-index: 1;
}

.metric-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  padding: 24px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-soft);
  animation: metricSlideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: calc(var(--i) * 0.1s);
}

@keyframes metricSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(15px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 20px 20px 0 0;
}

.metric-card--green::before { background: linear-gradient(90deg, var(--primary-green), var(--accent-green)); }
.metric-card--teal::before { background: linear-gradient(90deg, var(--primary-teal), var(--primary-light)); }
.metric-card--blue::before { background: linear-gradient(90deg, var(--accent-blue), var(--accent-blue-light)); }
.metric-card--warning::before { background: linear-gradient(90deg, #FFB800, #FFD700); }

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.metric-icon {
  width: 46px;
  height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.metric-card--green .metric-icon { background: rgba(45, 106, 79, 0.1); }
.metric-card--teal .metric-icon { background: rgba(64, 145, 108, 0.1); }
.metric-card--blue .metric-icon { background: rgba(0, 180, 216, 0.1); }
.metric-card--warning .metric-icon { background: rgba(255, 184, 0, 0.1); }

.metric-icon .icon {
  width: 20px;
  height: 20px;
}

.metric-card--green .metric-icon .icon { color: var(--primary-green); }
.metric-card--teal .metric-icon .icon { color: var(--primary-teal); }
.metric-card--blue .metric-icon .icon { color: var(--accent-blue); }
.metric-card--warning .metric-icon .icon { color: #FFB800; }

.metric-badge {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 5px 12px;
  border-radius: 20px;
  background: rgba(45, 106, 79, 0.08);
  color: var(--primary-green);
  border: 1px solid rgba(45, 106, 79, 0.15);
}

.metric-badge--success {
  background: rgba(82, 183, 136, 0.1);
  color: var(--primary-light);
  border-color: rgba(82, 183, 136, 0.2);
}

.metric-badge--admin {
  background: rgba(0, 180, 216, 0.1);
  color: var(--accent-blue);
  border-color: rgba(0, 180, 216, 0.2);
}

.metric-badge--warning {
  background: rgba(255, 184, 0, 0.1);
  color: #FFB800;
  border-color: rgba(255, 184, 0, 0.2);
}

.metric-body {
  position: relative;
  z-index: 1;
}

.metric-label {
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
  margin: 0 0 10px 0;
}

.metric-value {
  font-family: 'Nunito', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-card--green .metric-value { color: var(--primary-green); }
.metric-card--teal .metric-value { color: var(--primary-teal); }
.metric-card--blue .metric-value { color: var(--accent-blue); }
.metric-card--warning .metric-value { color: #FFB800; }

.metric-leaf {
  position: absolute;
  bottom: -8px;
  right: -8px;
  color: var(--primary-green);
  opacity: 0.12;
  pointer-events: none;
}

/* ============================================
   Filter Panel
   ============================================ */
.filter-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.5s ease backwards;
  animation-delay: 0.2s;
  box-shadow: var(--shadow-soft);
  position: relative;
  z-index: 1;
}

@keyframes panelSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
}

.filter-search {
  position: relative;
  flex: 1;
  max-width: 420px;
}

.filter-search .search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--text-tertiary);
  pointer-events: none;
}

.filter-search .search-input {
  width: 100%;
  padding: 13px 16px 13px 48px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.filter-search .search-input::placeholder {
  color: var(--text-tertiary);
}

.filter-search .search-input:focus {
  outline: none;
  border-color: var(--border-focus);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 13px 18px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: var(--bg-card);
  border-color: var(--accent-green);
}

.filter-toggle.active {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.06));
  border-color: var(--primary-green);
  color: var(--primary-green);
}

.filter-toggle .icon {
  width: 16px;
  height: 16px;
}

.filter-toggle .filter-count {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: var(--primary-green);
  color: white;
  font-size: 11px;
  font-weight: 700;
  border-radius: 10px;
}

.filter-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: var(--bg-card);
  border-color: var(--accent-green);
}

.filter-btn--search {
  background: linear-gradient(135deg, var(--primary-teal), var(--primary-light));
  border: none;
  color: white;
}

.filter-btn--search:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(64, 145, 108, 0.3);
}

.filter-btn--search .icon {
  width: 18px;
  height: 18px;
}

.filter-btn--reset {
  padding: 0 18px;
  width: auto;
  color: var(--text-tertiary);
  font-size: 14px;
  font-weight: 600;
}

.filter-btn--reset:hover {
  border-color: var(--text-secondary);
  color: var(--text-secondary);
}

.filter-body {
  padding: 0 24px 24px;
  animation: slideDown 0.4s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.filter-group:last-of-type {
  margin-bottom: 0;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.filter-label .label-icon {
  width: 16px;
  height: 16px;
  color: var(--primary-green);
}

.filter-options {
  display: flex;
  gap: 12px;
}

.filter-option {
  padding: 10px 20px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-option:hover {
  background: var(--bg-card);
  border-color: var(--accent-green);
}

.filter-option.active {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.06));
  border-color: var(--primary-green);
  color: var(--primary-green);
}

.filter-divider {
  height: 1px;
  background: var(--border-light);
  margin: 20px 0;
}

/* ============================================
   Announcements Panel
   ============================================ */
.announcements-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.5s ease backwards;
  animation-delay: 0.3s;
  box-shadow: var(--shadow-soft);
  position: relative;
  z-index: 1;
}

.announcements-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
}

.panel-title-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.panel-icon-wrapper {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: rgba(45, 106, 79, 0.1);
}

.panel-icon-wrapper .icon {
  width: 20px;
  height: 20px;
  color: var(--primary-green);
}

.panel-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.panel-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.panel-badge {
  padding: 6px 16px;
  background: rgba(45, 106, 79, 0.1);
  border: 1px solid rgba(45, 106, 79, 0.2);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  color: var(--primary-green);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ============================================
   Announcements List
   ============================================ */
.announcements-list-wrapper {
  position: relative;
  min-height: 300px;
}

/* Loading Overlay */
.loading-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 44px;
  height: 44px;
  border: 4px solid var(--border-light);
  border-top-color: var(--primary-green);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
}

.empty-icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 106, 79, 0.05);
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 24px;
  margin-bottom: 24px;
}

.empty-icon {
  width: 36px;
  height: 36px;
  color: var(--text-tertiary);
  opacity: 0.5;
}

.empty-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-desc {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0 0 24px 0;
}

.empty-action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--primary-green), var(--primary-teal));
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(45, 106, 79, 0.3);
}

.empty-action-btn .icon {
  width: 16px;
  height: 16px;
}

/* Announcement Cards */
.announcement-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 24px;
}

.announcement-card {
  position: relative;
  display: flex;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 18px;
  overflow: hidden;
  transition: all 0.3s ease;
  animation: cardFadeIn 0.5s ease backwards;
  animation-delay: calc(var(--i) * 0.05s);
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.announcement-card:hover {
  border-color: var(--accent-green);
  box-shadow: var(--shadow-hover);
  transform: translateY(-3px);
}

.announcement-card.card--pinned {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.05), rgba(116, 198, 157, 0.02));
  border-color: rgba(116, 198, 157, 0.2);
}

.announcement-card.card--draft {
  opacity: 0.8;
}

.card-accent {
  width: 5px;
  border-radius: 18px 0 0 18px;
}

.card-accent[data-priority="1"] { background: var(--accent-blue); }
.card-accent[data-priority="2"] { background: #FFB800; }
.card-accent[data-priority="3"] { background: #DC2626; }

.card-main {
  flex: 1;
  padding: 20px;
  min-width: 0;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.priority-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.priority-indicator.priority--1 {
  background: rgba(0, 180, 216, 0.12);
  color: var(--accent-blue);
}

.priority-indicator.priority--2 {
  background: rgba(255, 184, 0, 0.12);
  color: #FFB800;
}

.priority-indicator.priority--3 {
  background: rgba(220, 38, 38, 0.12);
  color: #DC2626;
}

.priority-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.status-indicator.status--published {
  background: rgba(82, 183, 136, 0.12);
  color: var(--primary-light);
}

.status-indicator.status--draft {
  background: rgba(168, 162, 158, 0.12);
  color: var(--text-tertiary);
}

.status-indicator .status-icon {
  width: 12px;
  height: 12px;
}

.pin-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.12), rgba(116, 198, 157, 0.08));
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: var(--primary-green);
}

.pin-badge .pin-icon {
  width: 12px;
  height: 12px;
}

.header-right {
  flex-shrink: 0;
}

.card-id {
  font-family: 'Nunito', monospace;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-tertiary);
}

.card-body {
  margin-bottom: 16px;
}

.card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 10px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-content {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 14px 0;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.meta-icon {
  font-size: 12px;
}

.meta-label {
  color: var(--text-tertiary);
}

.meta-value {
  color: var(--text-secondary);
  font-weight: 500;
}

.card-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 12px;
  background: var(--bg-card);
  border-left: 1px solid var(--border-light);
}

.action-icon-btn {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-icon-btn:hover {
  transform: scale(1.1);
}

.action-icon-btn .icon {
  width: 16px;
  height: 16px;
}

.action-icon-btn--view:hover {
  background: rgba(0, 180, 216, 0.12);
  border-color: var(--accent-blue);
  color: var(--accent-blue);
}

.action-icon-btn--edit:hover {
  background: rgba(45, 106, 79, 0.12);
  border-color: var(--primary-green);
  color: var(--primary-green);
}

.action-icon-btn--publish:hover {
  background: rgba(82, 183, 136, 0.12);
  border-color: var(--primary-light);
  color: var(--primary-light);
}

.action-icon-btn--unpublish:hover {
  background: rgba(255, 184, 0, 0.12);
  border-color: #FFB800;
  color: #FFB800;
}

.action-icon-btn--delete:hover {
  background: rgba(220, 38, 38, 0.12);
  border-color: #DC2626;
  color: #DC2626;
}

/* Pagination */
.announcements-pagination {
  padding: 20px 24px;
  border-top: 1px solid var(--border-light);
  background: linear-gradient(180deg, transparent, var(--bg-sand) 100%);
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 1400px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .announcement-cards {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .header-actions {
    width: 100%;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .filter-header {
    flex-direction: column;
    gap: 12px;
  }

  .filter-search {
    max-width: 100%;
  }

  .filter-actions {
    width: 100%;
    justify-content: space-between;
  }

  .leaf-decoration {
    display: none;
  }
}
</style>
