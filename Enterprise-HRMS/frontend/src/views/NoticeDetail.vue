<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElCard, ElButton, ElTag, ElSkeleton, ElEmpty } from 'element-plus'
import { getPublicNoticeDetail } from '@/api/notice'
import { formatDateTime } from '@/utils/format'

const route = useRoute()
const router = useRouter()

const notice = ref(null)
const loading = ref(true)
const error = ref(false)

// 获取公告详情
const fetchNoticeDetail = async () => {
  const id = route.params.id
  if (!id) {
    error.value = true
    loading.value = false
    return
  }

  loading.value = true
  error.value = false
  try {
    const res = await getPublicNoticeDetail(id)
    notice.value = res.data?.data || res.data
  } catch (err) {
    console.error('获取公告详情失败:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.push('/notices')
}

// 计算 Markdown 渲染后的内容（简化版本，仅做基本转换）
const renderedContent = computed(() => {
  if (!notice.value?.content) return ''
  return renderSimpleMarkdown(notice.value.content)
})

// 简单的 Markdown 转 HTML（用于预览展示）
const renderSimpleMarkdown = (text) => {
  if (!text) return ''

  let html = text
    // 标题
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // 粗体
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // 斜体
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // 删除线
    .replace(/~~(.*?)~~/g, '<del>$1</del>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    // 引用
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    // 链接
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
    // 图片
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width:100%;"/>')
    // 无序列表
    .replace(/^\s*[-*+] (.*$)/gim, '<li>$1</li>')
    // 有序列表
    .replace(/^\s*\d+\. (.*$)/gim, '<li>$1</li>')
    // 段落
    .replace(/\n\n/g, '</p><p>')
    // 换行
    .replace(/\n/g, '<br>')

  return `<p>${html}</p>`
}

onMounted(() => {
  fetchNoticeDetail()
})
</script>

<template>
  <div class="notice-detail-container">
    <div class="page-header">
      <el-button
        type="primary"
        plain
        @click="goBack"
        class="back-btn"
      >
        ← 返回公告列表
      </el-button>
    </div>

    <div v-loading="loading" class="notice-content">
      <!-- 骨架屏 -->
      <template v-if="loading">
        <el-card class="notice-card">
          <el-skeleton :rows="10" animated />
        </el-card>
      </template>

      <!-- 错误状态 -->
      <template v-else-if="error">
        <el-empty description="公告不存在或已被删除" />
      </template>

      <!-- 公告详情 -->
      <template v-else-if="notice">
        <el-card class="notice-card">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <el-tag
                  v-if="notice.is_pinned"
                  type="warning"
                  effect="dark"
                  size="small"
                >
                  置顶公告
                </el-tag>
                <h1 class="notice-title">{{ notice.title }}</h1>
              </div>
            </div>
          </template>

          <div class="notice-meta">
            <span class="meta-item">
              <svg class="meta-icon" viewBox="0 0 24 24" width="16" height="16">
                <path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
              </svg>
              发布于 {{ formatDateTime(notice.published_at || notice.created_at) }}
            </span>
            <span class="meta-item" v-if="notice.published_by_name">
              <svg class="meta-icon" viewBox="0 0 24 24" width="16" height="16">
                <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
              发布人：{{ notice.published_by_name }}
            </span>
          </div>

          <el-divider />

          <div
            class="notice-body"
            v-html="renderedContent"
          />

          <div class="notice-footer" v-if="notice.updated_at && notice.updated_at !== notice.created_at">
            <span class="update-time">
              最后更新：{{ formatDateTime(notice.updated_at) }}
            </span>
          </div>
        </el-card>
      </template>
    </div>
  </div>
</template>

<style scoped>
.notice-detail-container {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 112px);
}

.page-header {
  margin-bottom: 24px;
}

.back-btn {
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateX(-4px);
}

.notice-content {
  max-width: 900px;
  margin: 0 auto;
  min-height: 400px;
}

.notice-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

.notice-title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
  word-break: break-word;
}

.notice-meta {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #909399;
  font-size: 14px;
}

.meta-icon {
  opacity: 0.7;
}

.notice-body {
  color: #303133;
  font-size: 16px;
  line-height: 1.8;
  min-height: 200px;
}

/* Markdown 内容样式 */
.notice-body :deep(h1) {
  font-size: 24px;
  margin: 24px 0 16px 0;
  color: #303133;
}

.notice-body :deep(h2) {
  font-size: 20px;
  margin: 20px 0 14px 0;
  color: #303133;
}

.notice-body :deep(h3) {
  font-size: 18px;
  margin: 16px 0 12px 0;
  color: #303133;
}

.notice-body :deep(p) {
  margin: 12px 0;
}

.notice-body :deep(ul),
.notice-body :deep(ol) {
  padding-left: 24px;
  margin: 12px 0;
}

.notice-body :deep(li) {
  margin: 6px 0;
}

.notice-body :deep(blockquote) {
  border-left: 4px solid #409eff;
  margin: 16px 0;
  padding: 12px 20px;
  background: #f4f4f5;
  color: #606266;
}

.notice-body :deep(pre) {
  background: #282c34;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
}

.notice-body :deep(code) {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
}

.notice-body :deep(pre code) {
  color: #abb2bf;
}

.notice-body :deep(inline-code) {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  color: #e06c75;
}

.notice-body :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.notice-body :deep(a:hover) {
  text-decoration: underline;
}

.notice-body :deep(del) {
  color: #909399;
}

.notice-footer {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
  text-align: right;
}

.update-time {
  color: #909399;
  font-size: 13px;
}
</style>
