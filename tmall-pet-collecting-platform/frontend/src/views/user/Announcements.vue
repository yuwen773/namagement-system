<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { announcementApi } from '@/api'
import Pagination from '@/components/common/Pagination.vue'
import {
  Bell, Top, Refresh, Star
} from '@element-plus/icons-vue'

const announcements = ref([])
const loading = ref(false)
const total = ref(0)

const pagination = ref({
  page: 1,
  page_size: 10
})

const pinnedAnnouncements = computed(() => {
  return announcements.value.filter(a => a.is_pinned)
})

const normalAnnouncements = computed(() => {
  return announcements.value.filter(a => !a.is_pinned)
})

const loadAnnouncements = async () => {
  try {
    loading.value = true
    const params = { ...pagination.value }

    const res = await announcementApi.getList(params)
    if (res.code === 0) {
      announcements.value = res.data || []
      total.value = res.total || 0
    }
  } catch (error) {
    ElMessage.error('加载公告失败')
  } finally {
    loading.value = false
  }
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

const getPriorityConfig = (priority) => {
  const configs = {
    1: {
      color: '#52B788',
      bg: 'linear-gradient(135deg, #40916C 0%, #52B788 100%)',
      text: '普通',
      icon: '📢'
    },
    2: {
      color: '#00B4D8',
      bg: 'linear-gradient(135deg, #0096B4 0%, #00B4D8 100%)',
      text: '重要',
      icon: '⚠️'
    },
    3: {
      color: '#74C69D',
      bg: 'linear-gradient(135deg, #52B788 0%, #74C69D 100%)',
      text: '紧急',
      icon: '🔔'
    }
  }
  return configs[priority] || configs[1]
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getRelativeTime = (time) => {
  if (!time) return ''
  const now = new Date()
  const target = new Date(time)
  const diff = now - target
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor(diff / (1000 * 60))

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return formatTime(time)
}

onMounted(() => {
  loadAnnouncements()
})
</script>

<template>
  <div class="announcement-center-page">
    <!-- 装饰性叶子 -->
    <div class="leaf-decoration leaf-1"></div>
    <div class="leaf-decoration leaf-2"></div>

    <!-- Hero Header -->
    <div class="hero-header">
      <div class="hero-bg">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
      </div>
      <div class="hero-content">
        <div class="hero-badge">
          <Star :size="16" />
          <span>系统公告</span>
        </div>
        <h1 class="hero-title">公告中心</h1>
        <p class="hero-subtitle">了解最新动态与重要通知</p>
        <button class="refresh-btn" @click="loadAnnouncements">
          <Refresh :size="18" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <div v-loading="loading" class="content-wrapper">
      <!-- Pinned Announcements -->
      <div v-if="pinnedAnnouncements.length > 0" class="pinned-section">
        <div class="section-header pinned">
          <div class="header-icon">
            <Top :size="20" />
          </div>
          <div>
            <h2>置顶公告</h2>
            <p>重要通知，请务必阅读</p>
          </div>
        </div>
        <div class="announcement-grid pinned">
          <div
            v-for="item in pinnedAnnouncements"
            :key="item.id"
            class="announcement-card pinned-card"
            :style="{ '--priority-color': getPriorityConfig(item.priority).color }"
          >
            <div class="card-decoration"></div>
            <div class="card-header">
              <div class="priority-badge" :style="{ background: getPriorityConfig(item.priority).bg }">
                <span class="priority-icon">{{ getPriorityConfig(item.priority).icon }}</span>
                <span>{{ getPriorityConfig(item.priority).text }}</span>
              </div>
              <div class="pin-indicator">
                <Top :size="16" />
                <span>置顶</span>
              </div>
            </div>
            <h3 class="card-title">{{ item.title }}</h3>
            <p class="card-content">{{ item.content }}</p>
            <div class="card-footer">
              <span class="time-badge">
                {{ getRelativeTime(item.published_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Normal Announcements -->
      <div class="normal-section">
        <div class="section-header">
          <div class="header-icon">
            <Bell :size="20" />
          </div>
          <div>
            <h2>全部公告</h2>
            <p>查看历史通知与公告</p>
          </div>
        </div>
        <div v-if="normalAnnouncements.length > 0" class="announcement-list">
          <div
            v-for="(item, index) in normalAnnouncements"
            :key="item.id"
            class="announcement-item"
            :style="{ '--delay': index * 50 + 'ms' }"
          >
            <div class="item-timeline">
              <div class="timeline-dot" :style="{ backgroundColor: getPriorityConfig(item.priority).color }"></div>
              <div v-if="index < normalAnnouncements.length - 1" class="timeline-line"></div>
            </div>
            <div class="item-content">
              <div class="item-header">
                <div class="priority-tag" :style="{ color: getPriorityConfig(item.priority).color }">
                  {{ getPriorityConfig(item.priority).icon }} {{ getPriorityConfig(item.priority).text }}
                </div>
                <span class="item-time">{{ formatTime(item.published_at) }}</span>
              </div>
              <h3 class="item-title">{{ item.title }}</h3>
              <p class="item-text">{{ item.content }}</p>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <div class="empty-illustration">
            <div class="empty-icon">📭</div>
            <p>暂无公告</p>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="total > 0" class="pagination-section">
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
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.announcement-center-page {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1A4D3A;
  --text-secondary: #4A7C6A;
  --text-tertiary: #8BA89A;
  --border-light: #E8F0EC;
  --border-default: #D0E2D8;

  min-height: 100vh;
  background: var(--bg-cream);
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
  padding: 24px;
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: fixed;
  opacity: 0.03;
  pointer-events: none;
  z-index: 0;
}

.leaf-1 {
  top: 8%;
  right: 4%;
  width: 280px;
  height: 280px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2352B788'%3E%3Cpath d='M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z'/%3E%3C/svg%3E") center/contain no-repeat;
}

.leaf-2 {
  bottom: 12%;
  left: 3%;
  width: 220px;
  height: 220px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2300B4D8'%3E%3Cpath d='M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z'/%3E%3C/svg%3E") center/contain no-repeat;
  transform: rotate(25deg);
}

/* ============================================
   Hero Header
   ============================================ */
.hero-header {
  position: relative;
  padding: 48px 24px;
  overflow: hidden;
  border-radius: 24px;
  margin-bottom: 32px;
  box-shadow: 0 8px 30px rgba(45, 106, 79, 0.1);
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-teal) 100%);
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 30% 20%, rgba(82, 183, 136, 0.4) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(64, 145, 108, 0.4) 0%, transparent 50%);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}

.hero-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  color: #fff;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 30px;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.hero-title {
  margin: 0 0 16px 0;
  font-size: 44px;
  font-weight: 800;
  letter-spacing: -1px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Noto Serif SC', serif;
}

.hero-subtitle {
  margin: 0 0 32px 0;
  font-size: 18px;
  opacity: 0.95;
  font-weight: 400;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 14px;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* ============================================
   Content Wrapper
   ============================================ */
.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 0 48px;
  position: relative;
  z-index: 1;
}

/* ============================================
   Section Headers
   ============================================ */
.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.section-header.pinned h2 {
  color: var(--primary-light);
}

.header-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-teal) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 20px rgba(82, 183, 136, 0.25);
}

.section-header h2 {
  margin: 0 0 4px 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Noto Serif SC', serif;
}

.section-header p {
  margin: 0;
  font-size: 14px;
  color: var(--text-tertiary);
}

/* ============================================
   Pinned Section
   ============================================ */
.pinned-section {
  margin-bottom: 48px;
}

.announcement-grid.pinned {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.pinned-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}

.pinned-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 40px rgba(82, 183, 136, 0.2);
  border-color: var(--border-default);
}

.card-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 140px;
  height: 140px;
  background: radial-gradient(circle at top right, var(--priority-color) 0%, transparent 70%);
  opacity: 0.12;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.priority-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.priority-icon {
  font-size: 14px;
}

.pin-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--primary-light);
  font-size: 12px;
  font-weight: 700;
}

.card-title {
  margin: 0 0 14px 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  font-family: 'Noto Serif SC', serif;
}

.card-content {
  margin: 0 0 18px 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  white-space: pre-wrap;
}

.card-footer {
  padding-top: 14px;
  border-top: 1px solid var(--border-light);
}

.time-badge {
  font-size: 13px;
  color: var(--text-tertiary);
}

/* ============================================
   Normal Section
   ============================================ */
.normal-section {
  margin-bottom: 32px;
}

.announcement-list {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.08);
}

.announcement-item {
  display: flex;
  gap: 24px;
  padding: 20px 0;
  position: relative;
}

.announcement-item:last-child .timeline-line {
  display: none;
}

.item-timeline {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.timeline-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 4px rgba(82, 183, 136, 0.1);
}

.timeline-line {
  flex: 1;
  width: 2px;
  background: linear-gradient(180deg, rgba(82, 183, 136, 0.15) 0%, transparent 100%);
  min-height: 50px;
}

.item-content {
  flex: 1;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.priority-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
}

.item-time {
  font-size: 13px;
  color: var(--text-tertiary);
}

.item-title {
  margin: 0 0 10px 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Noto Serif SC', serif;
}

.item-text {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  white-space: pre-wrap;
}

/* ============================================
   Empty State
   ============================================ */
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.empty-illustration {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.4;
}

.empty-illustration p {
  margin: 0;
  font-size: 16px;
  color: var(--text-tertiary);
}

/* ============================================
   Pagination
   ============================================ */
.pagination-section {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.08);
}

.pagination-section :deep(.el-pagination) {
  justify-content: center;
}

.pagination-section :deep(.el-pager li) {
  background: var(--bg-sand);
  border-color: var(--border-light);
  border-radius: 10px;
  color: var(--text-secondary);
  font-weight: 600;
}

.pagination-section :deep(.el-pager li:hover) {
  background: rgba(82, 183, 136, 0.15);
  color: var(--primary-light);
}

.pagination-section :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, var(--primary-light), var(--primary-teal));
  border-color: transparent;
  color: #fff;
}

.pagination-section :deep(.btn-prev),
.pagination-section :deep(.btn-next) {
  background: var(--bg-sand);
  border-color: var(--border-light);
  border-radius: 10px;
  color: var(--text-secondary);
}

.pagination-section :deep(.btn-prev:hover),
.pagination-section :deep(.btn-next:hover) {
  background: rgba(82, 183, 136, 0.15);
  color: var(--primary-light);
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .announcement-center-page {
    padding: 16px;
  }

  .hero-header {
    padding: 36px 20px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .announcement-grid.pinned {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
