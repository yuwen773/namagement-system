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
  <div class="announcements-container">
    <!-- 顶部欢迎区 -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">公告管理</h1>
        <p class="header-subtitle">管理系统通知与公告发布，支持优先级和置顶设置</p>
      </div>
      <div class="header-actions">
        <button class="action-btn action-btn--primary" @click="handleCreate">
          <Plus class="icon" />
          <span>新建公告</span>
        </button>
        <button class="action-btn action-btn--secondary" @click="loadAnnouncements" :class="{ loading }">
          <Refresh class="icon" :class="{ spinning: loading }" />
          <span>刷新数据</span>
        </button>
      </div>
    </div>

    <!-- 统计指标卡片 -->
    <div class="metrics-grid">
      <div class="metric-card metric-card--orange" style="--i: 0">
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
        <div class="metric-bg">📢</div>
      </div>

      <div class="metric-card metric-card--cyan" style="--i: 1">
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
        <div class="metric-bg">✓</div>
      </div>

      <div class="metric-card metric-card--purple" style="--i: 2">
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
        <div class="metric-bg">📌</div>
      </div>

      <div class="metric-card metric-card--gold" style="--i: 3">
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
        <div class="metric-bg">📝</div>
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
          <div class="panel-icon-wrapper panel-icon-wrapper--orange">
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
              'card--draft': announcement.status === 'draft',
              'card--urgent': announcement.priority === 3,
              'card--important': announcement.priority === 2
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.announcements-container {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(255, 255, 255, 0.15);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  animation: pageFadeIn 0.4s ease;
}

@keyframes pageFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ============================================
   Dashboard Header
   ============================================ */
.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  animation: slideInDown 0.5s ease;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-content {
  flex: 1;
}

.header-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 400;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
  transform: translateY(-2px);
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-orange));
  border: none;
  color: white;
}

.action-btn--primary:hover {
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

.action-btn--secondary {
  background: rgba(255, 255, 255, 0.03);
  border-color: var(--border-subtle);
}

.action-btn.loading {
  opacity: 0.7;
  pointer-events: none;
}

.action-btn .icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.action-btn .icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============================================
   Metrics Grid
   ============================================ */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  animation: fadeInUp 0.5s ease;
  animation-delay: 0.1s;
  animation-fill-mode: both;
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

.metric-card {
  position: relative;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  animation: metricSlideIn 0.5s ease backwards;
  animation-delay: calc(var(--i) * 0.08s);
}

@keyframes metricSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.metric-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-default);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.metric-card--orange {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.08), transparent);
  border-color: rgba(255, 107, 53, 0.15);
}

.metric-card--orange:hover {
  border-color: rgba(255, 107, 53, 0.3);
  box-shadow: 0 12px 40px rgba(255, 107, 53, 0.15);
}

.metric-card--cyan {
  background: linear-gradient(135deg, rgba(6, 255, 165, 0.06), transparent);
  border-color: rgba(6, 255, 165, 0.12);
}

.metric-card--cyan:hover {
  border-color: rgba(6, 255, 165, 0.25);
  box-shadow: 0 12px 40px rgba(6, 255, 165, 0.1);
}

.metric-card--purple {
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.08), transparent);
  border-color: rgba(123, 44, 191, 0.15);
}

.metric-card--purple:hover {
  border-color: rgba(123, 44, 191, 0.3);
  box-shadow: 0 12px 40px rgba(123, 44, 191, 0.15);
}

.metric-card--gold {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.06), transparent);
  border-color: rgba(255, 215, 0, 0.12);
}

.metric-card--gold:hover {
  border-color: rgba(255, 215, 0, 0.25);
  box-shadow: 0 12px 40px rgba(255, 215, 0, 0.1);
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.metric-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
}

.metric-icon .icon {
  width: 20px;
  height: 20px;
  color: var(--text-secondary);
}

.metric-card--orange .metric-icon {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.2);
}

.metric-card--orange .metric-icon .icon {
  color: var(--primary-orange);
}

.metric-card--cyan .metric-icon {
  background: rgba(6, 255, 165, 0.1);
  border-color: rgba(6, 255, 165, 0.2);
}

.metric-card--cyan .metric-icon .icon {
  color: var(--primary-cyan);
}

.metric-card--purple .metric-icon {
  background: rgba(123, 44, 191, 0.1);
  border-color: rgba(123, 44, 191, 0.2);
}

.metric-card--purple .metric-icon .icon {
  color: #9D4EDD;
}

.metric-card--gold .metric-icon {
  background: rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.2);
}

.metric-card--gold .metric-icon .icon {
  color: var(--primary-gold);
}

.metric-badge {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 6px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-tertiary);
}

.metric-badge--success {
  background: rgba(6, 255, 165, 0.1);
  color: var(--primary-cyan);
}

.metric-badge--admin {
  background: rgba(123, 44, 191, 0.1);
  color: #9D4EDD;
}

.metric-badge--warning {
  background: rgba(255, 215, 0, 0.1);
  color: var(--primary-gold);
}

.metric-body {
  position: relative;
  z-index: 1;
}

.metric-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-tertiary);
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1;
}

.metric-bg {
  position: absolute;
  right: -10px;
  bottom: -10px;
  font-size: 80px;
  opacity: 0.03;
  pointer-events: none;
  user-select: none;
}

/* ============================================
   Filter Panel
   ============================================ */
.filter-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.4s ease;
  animation-delay: calc(0.15s + var(--i) * 0.05s);
  animation-fill-mode: both;
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

.filter-header + .filter-body {
  border-top: 1px solid var(--border-subtle);
}

.filter-search {
  position: relative;
  flex: 1;
  max-width: 420px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--text-tertiary);
  pointer-events: none;
  transition: color 0.3s ease;
}

.search-input {
  width: 100%;
  padding: 13px 16px 13px 48px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-orange);
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.search-input:focus ~ .search-icon {
  color: var(--primary-orange);
}

.filter-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.filter-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 13px 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.filter-toggle.active {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.2);
  color: var(--primary-orange);
}

.filter-toggle .icon {
  width: 16px;
  height: 16px;
}

.filter-count {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 6px;
  background: var(--primary-orange);
  border-radius: 9px;
  font-size: 11px;
  font-weight: 700;
  color: white;
}

.filter-btn {
  padding: 13px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.filter-btn--search {
  width: 46px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-btn--search .icon {
  width: 16px;
  height: 16px;
}

.filter-body {
  padding: 24px;
  animation: filterExpand 0.3s ease;
}

@keyframes filterExpand {
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
  gap: 16px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.filter-label .label-icon {
  width: 16px;
  height: 16px;
}

.filter-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-option {
  padding: 10px 20px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 10px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-option:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

.filter-option.active {
  background: rgba(255, 107, 53, 0.15);
  border-color: var(--primary-orange);
  color: var(--primary-orange);
}

.filter-divider {
  height: 1px;
  background: var(--border-subtle);
  margin: 20px 0;
}

/* ============================================
   Announcements Panel
   ============================================ */
.announcements-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  animation: panelSlideIn 0.4s ease;
  animation-delay: calc(0.2s + var(--i) * 0.05s);
  animation-fill-mode: both;
}

.announcements-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-subtle);
}

.panel-title-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.panel-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 14px;
  position: relative;
  overflow: hidden;
}

.panel-icon-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent, rgba(255, 107, 53, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.panel-icon-wrapper:hover::before {
  opacity: 1;
}

.panel-icon-wrapper .icon {
  width: 22px;
  height: 22px;
  color: var(--primary-orange);
  position: relative;
  z-index: 1;
}

.panel-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.panel-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.panel-badge {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 8px 16px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
  color: var(--primary-orange);
}

.announcements-list-wrapper {
  position: relative;
  min-height: 400px;
}

/* Loading Overlay */
.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(13, 13, 20, 0.85);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--primary-orange);
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
  text-align: center;
}

.empty-icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
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
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-desc {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0 0 24px 0;
}

.empty-action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-orange));
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

.empty-action-btn .icon {
  width: 16px;
  height: 16px;
}

/* Announcement Cards */
.announcement-cards {
  display: grid;
  gap: 16px;
  padding: 24px 28px;
}

.announcement-card {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 20px 24px;
  transition: all 0.3s ease;
  animation: cardSlideIn 0.4s ease backwards;
  animation-delay: calc(var(--i) * 0.05s);
  overflow: hidden;
}

@keyframes cardSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.announcement-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.announcement-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--border-default);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.announcement-card:hover::before {
  opacity: 1;
}

.card-accent {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--border-subtle);
  transition: all 0.3s ease;
}

.card-accent[data-priority="1"] {
  background: linear-gradient(180deg, #60a5fa, #3b82f6);
}

.card-accent[data-priority="2"] {
  background: linear-gradient(180deg, #fbbf24, #f59e0b);
}

.card-accent[data-priority="3"] {
  background: linear-gradient(180deg, #f87171, #ef4444);
}

.announcement-card:hover .card-accent {
  width: 5px;
}

.card-main {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.priority-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
}

.priority-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-tertiary);
}

.priority-indicator.priority--1 .priority-dot {
  background: #60a5fa;
}

.priority-indicator.priority--2 .priority-dot {
  background: #fbbf24;
}

.priority-indicator.priority--3 .priority-dot {
  background: #f87171;
}

.priority-text {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
}

.priority-indicator.priority--1 .priority-text {
  color: #60a5fa;
}

.priority-indicator.priority--2 .priority-text {
  color: #fbbf24;
}

.priority-indicator.priority--3 .priority-text {
  color: #f87171;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
}

.status-indicator .status-icon {
  width: 12px;
  height: 12px;
}

.status-indicator.status--published .status-icon {
  color: var(--primary-cyan);
}

.status-indicator.status--draft .status-icon {
  color: var(--text-tertiary);
}

.status-text {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
}

.status-indicator.status--published .status-text {
  color: var(--primary-cyan);
}

.status-indicator.status--draft .status-text {
  color: var(--text-tertiary);
}

.pin-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 6px;
}

.pin-badge .pin-icon {
  width: 12px;
  height: 12px;
  color: var(--primary-orange);
}

.pin-badge span {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--primary-orange);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-tertiary);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.4;
}

.card-content {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}

.meta-icon {
  font-size: 14px;
}

.meta-label {
  color: var(--text-tertiary);
}

.meta-value {
  color: var(--text-secondary);
  font-family: 'JetBrains Mono', monospace;
}

/* Card Actions */
.card-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-self: center;
}

.action-icon-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-icon-btn .icon {
  width: 16px;
  height: 16px;
  color: var(--text-tertiary);
  transition: all 0.3s ease;
}

.action-icon-btn:hover {
  transform: scale(1.1);
}

.action-icon-btn--view:hover {
  background: rgba(96, 165, 250, 0.1);
  border-color: rgba(96, 165, 250, 0.3);
}

.action-icon-btn--view:hover .icon {
  color: #60a5fa;
}

.action-icon-btn--edit:hover {
  background: rgba(123, 44, 191, 0.1);
  border-color: rgba(123, 44, 191, 0.3);
}

.action-icon-btn--edit:hover .icon {
  color: #9D4EDD;
}

.action-icon-btn--publish:hover {
  background: rgba(6, 255, 165, 0.1);
  border-color: rgba(6, 255, 165, 0.3);
}

.action-icon-btn--publish:hover .icon {
  color: var(--primary-cyan);
}

.action-icon-btn--unpublish:hover {
  background: rgba(255, 215, 0, 0.1);
  border-color: rgba(255, 215, 0, 0.3);
}

.action-icon-btn--unpublish:hover .icon {
  color: var(--primary-gold);
}

.action-icon-btn--delete:hover {
  background: rgba(255, 107, 107, 0.1);
  border-color: rgba(255, 107, 107, 0.3);
}

.action-icon-btn--delete:hover .icon {
  color: #FF6B6B;
}

/* Card Special States */
.card--pinned {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.06), rgba(0, 0, 0, 0.2));
  border-color: rgba(255, 107, 53, 0.15);
}

.card--pinned:hover {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(0, 0, 0, 0.2));
  border-color: rgba(255, 107, 53, 0.25);
}

.card--draft {
  opacity: 0.85;
}

.card--draft .card-title {
  color: var(--text-secondary);
}

.card--urgent {
  background: linear-gradient(135deg, rgba(248, 113, 113, 0.06), rgba(0, 0, 0, 0.2));
  border-color: rgba(248, 113, 113, 0.15);
}

.card--urgent:hover {
  background: linear-gradient(135deg, rgba(248, 113, 113, 0.1), rgba(0, 0, 0, 0.2));
  border-color: rgba(248, 113, 113, 0.25);
}

.card--important {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.06), rgba(0, 0, 0, 0.2));
  border-color: rgba(251, 191, 36, 0.15);
}

.card--important:hover {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(0, 0, 0, 0.2));
  border-color: rgba(251, 191, 36, 0.25);
}

/* Pagination */
.announcements-pagination {
  padding: 20px 28px;
  border-top: 1px solid var(--border-subtle);
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
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .filter-header {
    flex-wrap: wrap;
  }

  .filter-search {
    max-width: 100%;
    order: 1;
    flex-basis: 100%;
  }

  .filter-actions {
    order: 2;
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .header-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1;
    min-width: 140px;
  }

  .announcement-card {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: row;
    justify-content: flex-start;
  }

  .filter-options {
    flex-direction: column;
  }

  .filter-option {
    width: 100%;
  }

  .panel-title-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
