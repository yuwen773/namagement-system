<template>
  <div class="notices-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M24 6L8 16V32C8 37.5225 12.4772 42 18 42H30C35.5228 42 40 37.5225 40 32V16L24 6Z" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="24" cy="26" r="6" stroke="currentColor" stroke-width="2.5"/>
            <path d="M24 14V20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="page-title">节能公告</h1>
          <p class="page-subtitle">了解最新动态与节能知识</p>
        </div>
      </div>
      <div class="header-decoration">
        <div class="deco-blob blob-1"></div>
        <div class="deco-blob blob-2"></div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-navigation">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-btn', { active: activeTab === tab.key }]"
        @click="switchTab(tab.key)"
      >
        <span class="tab-icon">
          <component :is="tab.icon" />
        </span>
        <span class="tab-label">{{ tab.label }}</span>
        <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
      </button>
    </div>

    <!-- Content Area -->
    <div class="content-area">
      <!-- Notices Tab -->
      <transition name="tab-fade" mode="out-in">
        <div v-if="activeTab === 'notices'" key="notices" class="notices-content">
          <!-- Filter Bar -->
          <div class="filter-bar">
            <div class="filter-group">
              <button
                v-for="filter in noticeFilters"
                :key="filter.key"
                :class="['filter-chip', { active: activeNoticeFilter === filter.key }]"
                @click="activeNoticeFilter = filter.key"
              >
                {{ filter.label }}
                <span v-if="filter.count" class="count">{{ filter.count }}</span>
              </button>
            </div>
            <div class="search-box">
              <el-icon><icon-ep-search /></el-icon>
              <input
                v-model="searchKeyword"
                type="text"
                placeholder="搜索通知..."
                class="search-input"
              />
            </div>
          </div>

          <!-- Notice List -->
          <div class="notice-list">
            <div
              v-for="notice in filteredNotices"
              :key="notice.id"
              :class="['notice-card', { unread: !notice.is_read }]"
              @click="viewNotice(notice)"
            >
              <div class="notice-priority" :class="`priority-${notice.priority}`">
                <el-icon>
                  <icon-ep-warning v-if="notice.priority === 'high'" />
                  <icon-ep-info-filled v-else-if="notice.priority === 'medium'" />
                  <icon-ep-bell v-else />
                </el-icon>
              </div>
              <div class="notice-body">
                <div class="notice-header-row">
                  <h3 class="notice-title">{{ notice.title }}</h3>
                  <span class="notice-type" :class="`type-${notice.notice_type}`">
                    {{ typeLabel(notice.notice_type) }}
                  </span>
                </div>
                <p class="notice-preview">{{ notice.content?.substring(0, 80) }}...</p>
                <div class="notice-footer">
                  <span class="notice-time">{{ formatTime(notice.publish_time) }}</span>
                  <span v-if="!notice.is_read" class="unread-badge">未读</span>
                </div>
              </div>
              <div class="notice-arrow">
                <el-icon><icon-ep-arrow-right /></el-icon>
              </div>
            </div>

            <el-empty v-if="filteredNotices.length === 0" description="暂无通知公告" />
          </div>
        </div>

        <!-- Tips Tab -->
        <div v-else key="tips" class="tips-content">
          <!-- Categories -->
          <div class="categories-bar">
            <div class="category-scroll">
              <button
                v-for="cat in tipCategories"
                :key="cat.key"
                :class="['category-chip', { active: activeTipCategory === cat.key }]"
                @click="activeTipCategory = cat.key"
              >
                <span class="cat-icon">{{ cat.icon }}</span>
                <span class="cat-label">{{ cat.label }}</span>
              </button>
            </div>
          </div>

          <!-- Tips Grid -->
          <div class="tips-grid">
            <div
              v-for="(tip, index) in filteredTips"
              :key="index"
              :class="['tip-card', `tip-color-${index % 5}`]"
            >
              <div class="tip-background">
                <div class="bg-pattern"></div>
              </div>
              <div class="tip-icon">
                <el-icon><icon-ep-opportunity /></el-icon>
              </div>
              <h3 class="tip-title">{{ tip.title }}</h3>
              <p class="tip-description">{{ tip.content }}</p>
              <div class="tip-footer">
                <span class="tip-category">{{ tip.category }}</span>
                <button class="tip-action">了解更多</button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- Notice Detail Dialog -->
    <el-dialog
      v-model="showNoticeDetail"
      :title="selectedNotice?.title"
      width="600px"
      class="notice-detail-dialog"
      :close-on-click-modal="false"
    >
      <div v-if="selectedNotice" class="notice-detail">
        <div class="detail-meta">
          <span class="detail-type" :class="`type-${selectedNotice.notice_type}`">
            {{ typeLabel(selectedNotice.notice_type) }}
          </span>
          <span class="detail-time">{{ formatFullTime(selectedNotice.publish_time) }}</span>
        </div>
        <div class="detail-content">
          {{ selectedNotice.content }}
        </div>
      </div>
      <template #footer>
        <el-button @click="showNoticeDetail = false">关闭</el-button>
        <el-button v-if="selectedNotice && !selectedNotice.is_read" type="primary" @click="markAsRead">
          标记已读
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getNotices, getNotice, getTips } from '@/api/system'

// State
const activeTab = ref('notices')
const activeNoticeFilter = ref('all')
const activeTipCategory = ref('all')
const searchKeyword = ref('')
const showNoticeDetail = ref(false)
const selectedNotice = ref(null)

// Tab configuration
const tabs = [
  { key: 'notices', label: '通知公告', icon: 'icon-ep-bell', badge: null },
  { key: 'tips', label: '节能知识', icon: 'icon-ep-opportunity', badge: null },
]

// Notice filters
const noticeFilters = [
  { key: 'all', label: '全部', count: 0 },
  { key: 'high', label: '重要', count: 0 },
  { key: 'unread', label: '未读', count: 0 },
]

// Data
const notices = ref([])

// Tips data - 从API获取
const tips = ref([])

const tipCategoryIconRules = [
  { pattern: /电|electricity|energy/i, icon: '⚡' },
  { pattern: /水|water/i, icon: '💧' },
  { pattern: /气|gas|燃气|天然气/i, icon: '🔥' },
  { pattern: /日常|daily|生活|习惯/i, icon: '🏠' },
  { pattern: /技术|方案|改造|technology/i, icon: '🛠️' },
  { pattern: /管理|实践|运营|运维/i, icon: '📋' },
  { pattern: /政策|法规|标准|policy/i, icon: '📜' },
]

function normalizeTipCategory(value) {
  return String(value || '').trim().toLowerCase()
}

function getTipCategoryIcon(category) {
  const normalizedCategory = normalizeTipCategory(category)
  const matchedRule = tipCategoryIconRules.find(rule => rule.pattern.test(normalizedCategory))
  return matchedRule ? matchedRule.icon : '📚'
}

const tipCategories = computed(() => {
  const categories = Array.from(
    new Set(
      tips.value
        .map(item => String(item.category || '').trim())
        .filter(Boolean)
    )
  )

  return [
    { key: 'all', label: '全部', icon: '🌍' },
    ...categories.map(category => ({
      key: category,
      label: category,
      icon: getTipCategoryIcon(category),
    })),
  ]
})

// Load tips from API
async function loadTips() {
  try {
    const response = await getTips()
    if (response.code === 0 && response.data) {
      tips.value = response.data
      const hasActiveCategory =
        activeTipCategory.value === 'all' ||
        tips.value.some(
          tip => normalizeTipCategory(tip.category) === normalizeTipCategory(activeTipCategory.value)
        )
      if (!hasActiveCategory) {
        activeTipCategory.value = 'all'
      }
    }
  } catch (error) {
    console.error('Failed to load tips:', error)
  }
}

// Computed
const filteredNotices = computed(() => {
  let result = notices.value

  // Filter by status
  if (activeNoticeFilter.value === 'unread') {
    result = result.filter(n => !n.is_read)
  } else if (activeNoticeFilter.value === 'high') {
    result = result.filter(n => n.priority === 'high')
  }

  // Filter by search
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(n =>
      n.title?.toLowerCase().includes(keyword) ||
      n.content?.toLowerCase().includes(keyword)
    )
  }

  return result
})

const filteredTips = computed(() => {
  if (activeTipCategory.value === 'all') return tips.value
  const selectedCategory = normalizeTipCategory(activeTipCategory.value)
  return tips.value.filter(t => normalizeTipCategory(t.category) === selectedCategory)
})

// Methods
function switchTab(tab) {
  activeTab.value = tab
}

function typeLabel(type) {
  const labels = {
    NOTICE: '通知',
    ANNOUNCEMENT: '公告',
    TIP: '贴士',
    WARNING: '警告',
  }
  return labels[type] || '通知'
}

function formatTime(timeStr) {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)

  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  if (diff < 43200) return `${Math.floor(diff / 1440)}天前`
  return date.toLocaleDateString('zh-CN')
}

function formatFullTime(timeStr) {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function viewNotice(notice) {
  selectedNotice.value = notice
  showNoticeDetail.value = true

  // Mark as read
  if (!notice.is_read) {
    notice.is_read = true
    updateFilterCounts()
  }
}

async function markAsRead() {
  if (selectedNotice.value) {
    selectedNotice.value.is_read = true
    updateFilterCounts()
    ElMessage.success('已标记为已读')
  }
}

function updateFilterCounts() {
  noticeFilters[0].count = notices.value.length
  noticeFilters[1].count = notices.value.filter(n => n.priority === 'high').length
  noticeFilters[2].count = notices.value.filter(n => !n.is_read).length

  // Update tab badge
  const unreadCount = notices.value.filter(n => !n.is_read).length
  tabs[0].badge = unreadCount > 0 ? unreadCount : null
}

async function loadNotices() {
  try {
    const response = await getNotices()
    if (response.code === 0 && response.data) {
      notices.value = response.data
      updateFilterCounts()
    }
  } catch (error) {
    console.error('Failed to load notices:', error)
    // Mock data for development
    notices.value = [
      {
        id: 1,
        title: '停水通知',
        content: '因管道维护，明日9:00-17:00将暂停供水，请提前储水。给您带来不便，敬请谅解。',
        notice_type: 'NOTICE',
        priority: 'high',
        is_read: false,
        publish_time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: 2,
        title: '节能月活动通知',
        content: '为响应国家节能减排号召，本月定为节能宣传月。期间将举办节能知识竞赛、节能小妙招征集等活动，欢迎广大师生积极参与，赢取精美礼品！',
        notice_type: 'ANNOUNCEMENT',
        priority: 'medium',
        is_read: false,
        publish_time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: 3,
        title: '夏季用电高峰提醒',
        content: '进入夏季用电高峰期，请合理用电，错峰使用大功率电器。空调温度建议设置在26℃以上，共同维护电网稳定运行。',
        notice_type: 'TIP',
        priority: 'medium',
        is_read: true,
        publish_time: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ]
    updateFilterCounts()
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadNotices(),
    loadTips(),
  ])
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

.notices-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   PAGE HEADER
   ======================================== */
.page-header {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #dc2626 100%);
  border-radius: 20px;
  padding: 28px 32px;
  color: white;
  box-shadow: 0 20px 40px rgba(249, 115, 22, 0.25);
}

.header-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.header-text .page-title {
  margin: 0 0 4px;
  font-size: 24px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

.header-text .page-subtitle {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
}

.header-decoration {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 12px;
}

.deco-blob {
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.blob-1 {
  width: 60px;
  height: 60px;
  animation: float 3s ease-in-out infinite;
}

.blob-2 {
  width: 36px;
  height: 36px;
  animation: float 3s ease-in-out infinite 0.5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* ========================================
   TAB NAVIGATION
   ======================================== */
.tab-navigation {
  display: flex;
  gap: 8px;
  background: white;
  padding: 6px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.tab-btn:hover {
  background: #f8fafc;
  color: #f97316;
}

.tab-btn.active {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.tab-icon {
  display: flex;
  align-items: center;
  font-size: 18px;
}

.tab-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ========================================
   CONTENT AREA
   ======================================== */
.content-area {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  padding: 20px;
  min-height: 400px;
}

/* Tab Transition */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: all 0.3s ease;
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========================================
   NOTICES CONTENT
   ======================================== */
.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  color: #64748b;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-chip:hover {
  background: #fef3c7;
  border-color: #fcd34d;
  color: #92400e;
}

.filter-chip.active {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-color: transparent;
  color: white;
}

.filter-chip .count {
  font-size: 11px;
  opacity: 0.8;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  min-width: 240px;
  transition: all 0.2s ease;
}

.search-box:focus-within {
  background: white;
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.search-box .el-icon {
  color: #9ca3af;
  font-size: 16px;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
  color: #1f2937;
}

.search-input::placeholder {
  color: #9ca3af;
}

/* Notice List */
.notice-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notice-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.notice-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #f97316, #ea580c);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.notice-card.unread {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border-color: #fcd34d;
}

.notice-card.unread::before {
  opacity: 1;
}

.notice-card:hover {
  transform: translateX(4px);
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.12);
  border-color: #f97316;
}

.notice-priority {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  font-size: 18px;
}

.notice-priority.priority-high {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.notice-priority.priority-medium {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.notice-priority.priority-low {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.notice-body {
  flex: 1;
  min-width: 0;
}

.notice-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.notice-title {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.notice-type {
  flex-shrink: 0;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.notice-type.type-NOTICE {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.notice-type.type-ANNOUNCEMENT {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.notice-type.type-TIP {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.notice-type.type-WARNING {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.notice-preview {
  margin: 0 0 8px;
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

.notice-footer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.notice-time {
  font-size: 12px;
  color: #9ca3af;
}

.unread-badge {
  padding: 2px 8px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  border-radius: 6px;
}

.notice-arrow {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 8px;
  color: #9ca3af;
  transition: all 0.3s ease;
}

.notice-card:hover .notice-arrow {
  background: #f97316;
  color: white;
  transform: translateX(4px);
}

/* ========================================
   TIPS CONTENT
   ======================================== */
.categories-bar {
  margin-bottom: 20px;
  overflow-x: auto;
  scrollbar-width: none;
}

.category-scroll {
  display: flex;
  gap: 8px;
  padding: 4px;
}

.category-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-chip:hover {
  background: #fef3c7;
  border-color: #fcd34d;
}

.category-chip.active {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border-color: transparent;
  color: white;
}

.cat-icon {
  font-size: 16px;
}

.cat-label {
  font-size: 13px;
  font-weight: 500;
}

/* Tips Grid */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.tip-card {
  position: relative;
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tip-card .tip-background {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1);
}

.tip-card:hover .tip-background {
  opacity: 0.5;
}

.tip-color-0 { border-color: rgba(234, 179, 8, 0.3); }
.tip-color-0:hover { border-color: #eab308; }
.tip-color-0 .tip-icon { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); }
.tip-color-0 .tip-background { background: linear-gradient(135deg, rgba(251, 191, 36, 0.05) 0%, rgba(245, 158, 11, 0.02) 100%); }

.tip-color-1 { border-color: rgba(59, 130, 246, 0.3); }
.tip-color-1:hover { border-color: #3b82f6; }
.tip-color-1 .tip-icon { background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%); }
.tip-color-1 .tip-background { background: linear-gradient(135deg, rgba(96, 165, 250, 0.05) 0%, rgba(59, 130, 246, 0.02) 100%); }

.tip-color-2 { border-color: rgba(34, 197, 94, 0.3); }
.tip-color-2:hover { border-color: #22c55e; }
.tip-color-2 .tip-icon { background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%); }
.tip-color-2 .tip-background { background: linear-gradient(135deg, rgba(74, 222, 128, 0.05) 0%, rgba(34, 197, 94, 0.02) 100%); }

.tip-color-3 { border-color: rgba(239, 68, 68, 0.3); }
.tip-color-3:hover { border-color: #ef4444; }
.tip-color-3 .tip-icon { background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); }
.tip-color-3 .tip-background { background: linear-gradient(135deg, rgba(248, 113, 113, 0.05) 0%, rgba(239, 68, 68, 0.02) 100%); }

.tip-color-4 { border-color: rgba(168, 85, 247, 0.3); }
.tip-color-4:hover { border-color: #a855f7; }
.tip-color-4 .tip-icon { background: linear-gradient(135deg, #c084fc 0%, #a855f7 100%); }
.tip-color-4 .tip-background { background: linear-gradient(135deg, rgba(192, 132, 252, 0.05) 0%, rgba(168, 85, 247, 0.02) 100%); }

.tip-icon {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  color: white;
  font-size: 20px;
  margin-bottom: 12px;
}

.tip-title {
  position: relative;
  z-index: 1;
  margin: 0 0 8px;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.tip-description {
  position: relative;
  z-index: 1;
  margin: 0 0 16px;
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

.tip-footer {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tip-category {
  font-size: 11px;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tip-action {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tip-action:hover {
  background: #f97316;
  border-color: #f97316;
  color: white;
}

/* ========================================
   NOTICE DETAIL DIALOG
   ======================================== */
:deep(.notice-detail-dialog) {
  border-radius: 16px;
}

:deep(.notice-detail-dialog .el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

:deep(.notice-detail-dialog .el-dialog__title) {
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

:deep(.notice-detail-dialog .el-dialog__body) {
  padding: 24px;
}

.notice-detail .detail-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-type {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.detail-type.type-NOTICE {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.detail-type.type-ANNOUNCEMENT {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.detail-type.type-TIP {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.detail-time {
  font-size: 12px;
  color: #9ca3af;
}

.notice-detail .detail-content {
  font-size: 14px;
  line-height: 1.8;
  color: #374151;
  white-space: pre-wrap;
}

:deep(.notice-detail-dialog .el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 768px) {
  .page-header {
    padding: 20px;
  }

  .header-decoration {
    display: none;
  }

  .header-text .page-title {
    font-size: 20px;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: 100%;
  }

  .tips-grid {
    grid-template-columns: 1fr;
  }

  .notice-card {
    padding: 14px;
  }

  .notice-preview {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-empty) {
  padding: 40px 20px;
}

:deep(.el-empty__description) {
  color: #9ca3af;
}
</style>
