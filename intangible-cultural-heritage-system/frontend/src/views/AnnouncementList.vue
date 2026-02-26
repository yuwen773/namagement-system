<template>
  <div class="announcement-list-page">
    <!-- 水墨晕染背景 -->
    <div class="ink-background">
      <div class="ink-spot spot-1"></div>
      <div class="ink-spot spot-2"></div>
    </div>

    <!-- 页面头部 - 卷轴式 -->
    <header class="page-header">
      <div class="scroll-mount left"></div>
      <div class="header-center">
        <div class="header-decoration">
          <div class="decoration-line"></div>
          <div class="header-seal">
            <div class="seal-frame">
              <div class="seal-inner">
                <span class="seal-text-vertical">公告</span>
              </div>
            </div>
          </div>
          <div class="decoration-line"></div>
        </div>
        <div class="header-texts">
          <h1 class="page-title">通知公告</h1>
          <p class="page-subtitle">平台最新动态与通知信息</p>
        </div>
      </div>
      <div class="scroll-mount right"></div>
    </header>

    <!-- 公告列表 -->
    <div class="announcement-section">
      <div class="scroll-decoration">
        <div class="scroll-pattern"></div>
      </div>
      <div class="announcement-content">
        <div v-if="loading" class="loading-container">
          <el-icon class="loading-spinner"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        <div v-else-if="list.length === 0" class="empty-container">
          <el-icon :size="48"><Document /></el-icon>
          <span>暂无公告</span>
        </div>
        <div v-else class="announcement-grid">
          <div
            v-for="item in list"
            :key="item.id"
            class="announcement-card"
            @click="goDetail(item.id)"
          >
            <div v-if="item.is_top" class="top-badge">
              <el-icon><Top /></el-icon>
              置顶
            </div>
            <h3 class="card-title">{{ item.title }}</h3>
            <div class="card-summary">{{ getSummary(item.content) }}</div>
            <div class="card-meta">
              <span class="meta-author">
                <el-icon><User /></el-icon>
                {{ item.author_name }}
              </span>
              <span class="meta-date">
                <el-icon><Calendar /></el-icon>
                {{ formatDate(item.created_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, total"
        background
        @current-change="fetchList"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading, Document, Top, User, Calendar } from '@element-plus/icons-vue'
import { getAnnouncementList } from '@/api/announcement'
import type { Announcement } from '@/types'

const router = useRouter()
const list = ref<Announcement[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)

const fetchList = async () => {
  loading.value = true
  try {
    const res = await getAnnouncementList({ page: page.value, page_size: pageSize.value })
    list.value = res.data.data || []
    total.value = res.data.total || 0
  } catch (error) {
    ElMessage.error('获取公告列表失败')
  } finally {
    loading.value = false
  }
}

const goDetail = (id: number) => {
  router.push(`/announcements/${id}`)
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getSummary = (content: string) => {
  // 去除 HTML 标签，获取纯文本摘要
  const text = content.replace(/<[^>]+>/g, '')
  return text.length > 100 ? text.substring(0, 100) + '...' : text
}

onMounted(fetchList)
</script>

<style scoped>
.announcement-list-page {
  min-height: 100%;
  position: relative;
}

/* 背景效果 */
.ink-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.ink-spot {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}

.spot-1 {
  width: 400px;
  height: 400px;
  background: #C23531;
  top: -100px;
  right: -100px;
}

.spot-2 {
  width: 300px;
  height: 300px;
  background: #D4AF37;
  bottom: -50px;
  left: -50px;
}

/* 页面头部 */
.page-header {
  position: relative;
  display: flex;
  align-items: stretch;
  background: linear-gradient(135deg, #2F3640 0%, #1a2026 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.scroll-mount {
  width: 40px;
  background: linear-gradient(180deg,
    #D4AF37 0%,
    #B8860B 15%,
    #8B6914 30%,
    #B8860B 50%,
    #D4AF37 70%,
    #B8860B 85%,
    #8B6914 100%
  );
  position: relative;
  flex-shrink: 0;
}

.scroll-mount.left {
  border-radius: 0 8px 8px 0;
}

.scroll-mount.right {
  border-radius: 8px 0 0 8px;
}

.header-center {
  flex: 1;
  padding: 24px 40px;
}

.header-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 16px;
}

.decoration-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
}

.header-seal {
  flex-shrink: 0;
}

.seal-frame {
  width: 64px;
  height: 64px;
  background: #C23531;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(194, 35, 49, 0.4);
  position: relative;
}

.seal-frame::before {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  right: 4px;
  bottom: 4px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}

.seal-inner {
  width: 48px;
  height: 48px;
  background: rgba(194, 35, 49, 0.9);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seal-text-vertical {
  color: #F7F4ED;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
}

.header-texts {
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #F7F4ED;
  margin: 0 0 8px 0;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.page-subtitle {
  font-size: 14px;
  color: rgba(247, 244, 237, 0.7);
  margin: 0;
  letter-spacing: 2px;
}

/* 公告列表区域 */
.announcement-section {
  position: relative;
  display: flex;
  margin: 24px 32px;
  background: #FFFBF5;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.scroll-decoration {
  width: 24px;
  background: linear-gradient(180deg,
    rgba(212, 175, 55, 0.3) 0%,
    rgba(212, 175, 55, 0.1) 50%,
    rgba(212, 175, 55, 0.3) 100%
  );
  border-radius: 8px 0 0 8px;
  flex-shrink: 0;
}

.scroll-pattern {
  width: 8px;
  height: 100%;
  margin: 8px auto;
  background: repeating-linear-gradient(
    180deg,
    transparent 0px,
    transparent 8px,
    rgba(212, 175, 55, 0.3) 8px,
    rgba(212, 175, 55, 0.3) 10px
  );
}

.announcement-content {
  flex: 1;
  padding: 24px;
}

.loading-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #909399;
  gap: 12px;
}

.loading-spinner {
  font-size: 32px;
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.announcement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.announcement-card {
  position: relative;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(212, 175, 55, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.announcement-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: rgba(212, 175, 55, 0.4);
}

.top-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #C23531;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  border-radius: 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #2F3640;
  margin: 0 0 12px 0;
  padding-right: 80px;
  line-height: 1.4;
}

.card-summary {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 16px;
  min-height: 42px;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  color: #909399;
}

.meta-author,
.meta-date {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 24px 0 48px;
}

:deep(.el-pagination) {
  --el-pagination-bg-color: #fff;
  --el-pagination-text-color: #606266;
  --el-pagination-button-bg-color: #fff;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #C23531;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled):hover) {
  color: #C23531;
}
</style>
