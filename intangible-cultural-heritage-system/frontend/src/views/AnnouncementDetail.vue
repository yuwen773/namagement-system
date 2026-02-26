<template>
  <div class="announcement-detail-page">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <el-button class="back-btn" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
      </div>
    </header>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="loading-spinner"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <!-- 公告内容 -->
    <div v-else-if="announcement.id" class="detail-container">
      <article class="announcement-article">
        <header class="article-header">
          <div v-if="announcement.is_top" class="top-badge">
            <el-icon><Top /></el-icon>
            置顶
          </div>
          <h1 class="article-title">{{ announcement.title }}</h1>
          <div class="article-meta">
            <span class="meta-item">
              <el-icon><User /></el-icon>
              {{ announcement.author_name }}
            </span>
            <span class="meta-item">
              <el-icon><Calendar /></el-icon>
              {{ formatDate(announcement.created_at) }}
            </span>
            <span v-if="announcement.updated_at !== announcement.created_at" class="meta-item">
              <el-icon><Edit /></el-icon>
              更新于 {{ formatDate(announcement.updated_at) }}
            </span>
          </div>
        </header>

        <div class="article-content" v-html="announcement.content"></div>
      </article>
    </div>

    <!-- 不存在 -->
    <div v-else class="empty-container">
      <el-icon :size="64"><DocumentDelete /></el-icon>
      <h2>公告不存在</h2>
      <p>您访问的公告可能已被删除或不存在</p>
      <el-button type="primary" @click="goBack">返回公告列表</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading, ArrowLeft, Top, User, Calendar, Edit, DocumentDelete } from '@element-plus/icons-vue'
import { getAnnouncementDetail } from '@/api/announcement'
import type { Announcement } from '@/types'

const route = useRoute()
const router = useRouter()
const announcement = ref<Announcement>({} as Announcement)
const loading = ref(true)

const fetchDetail = async () => {
  loading.value = true
  try {
    const id = Number(route.params.id)
    const res = await getAnnouncementDetail(id)
    announcement.value = res.data.data
  } catch (error) {
    ElMessage.error('获取公告详情失败')
    announcement.value = {} as Announcement
  } finally {
    loading.value = false
  }
}

const goBack = () => router.push('/announcements')

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchDetail)
</script>

<style scoped>
.announcement-detail-page {
  min-height: 100%;
  background: #F7F4ED;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #2F3640 0%, #1a2026 100%);
  padding: 16px 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-content {
  display: flex;
  align-items: center;
}

.back-btn {
  background: rgba(247, 244, 237, 0.1) !important;
  border: 1px solid rgba(212, 175, 55, 0.3) !important;
  color: #F7F4ED !important;
  border-radius: 20px !important;
  padding: 8px 20px !important;
}

.back-btn:hover {
  background: rgba(212, 175, 55, 0.2) !important;
  border-color: #D4AF37 !important;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
  color: #909399;
  gap: 12px;
}

.loading-spinner {
  font-size: 40px;
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 详情容器 */
.detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px;
}

.announcement-article {
  background: #FFFBF5;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.article-header {
  position: relative;
  padding: 32px 32px 24px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.top-badge {
  position: absolute;
  top: 24px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  background: #C23531;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  border-radius: 14px;
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  color: #2F3640;
  margin: 0 0 20px 0;
  line-height: 1.4;
  padding-right: 80px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #909399;
}

.article-content {
  padding: 32px;
  line-height: 1.8;
  font-size: 16px;
  color: #303133;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3) {
  color: #2F3640;
  margin: 24px 0 16px;
}

.article-content :deep(p) {
  margin: 16px 0;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  margin: 16px 0;
  padding-left: 24px;
}

.article-content :deep(li) {
  margin: 8px 0;
}

.article-content :deep(a) {
  color: #C23531;
}

.article-content :deep(blockquote) {
  margin: 16px 0;
  padding: 12px 20px;
  background: rgba(212, 175, 55, 0.1);
  border-left: 4px solid #D4AF37;
  font-style: italic;
}

.article-content :deep(code) {
  background: rgba(47, 54, 64, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

.article-content :deep(pre) {
  background: #2F3640;
  color: #F7F4ED;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

/* 空状态 */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
  color: #909399;
}

.empty-container h2 {
  margin: 24px 0 12px;
  color: #606266;
}

.empty-container p {
  margin-bottom: 24px;
}
</style>
