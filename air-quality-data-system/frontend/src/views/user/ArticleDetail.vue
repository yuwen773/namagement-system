<template>
  <div class="article-detail-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button link @click="goBack" class="back-button">
          <el-icon><ArrowLeft /></el-icon>
          返回知识库
        </el-button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <!-- Article Content -->
    <div v-else-if="article" class="article-content">
      <!-- Article Header Card -->
      <div class="card header-card">
        <el-tag :style="{ background: getCategoryColor(article.category), border: 'none' }" size="large">
          {{ article.category_name || '未分类' }}
        </el-tag>
        <h1 class="article-title">{{ article.title }}</h1>
        <p v-if="article.summary" class="article-summary">{{ article.summary }}</p>
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><User /></el-icon>
            {{ article.author || '管理员' }}
          </span>
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(article.created_at) }}
          </span>
          <span v-if="article.view_count" class="meta-item">
            <el-icon><View /></el-icon>
            {{ article.view_count }} 次浏览
          </span>
        </div>
      </div>

      <!-- Article Cover Image -->
      <div v-if="article.cover_image" class="article-cover">
        <img :src="article.cover_image" :alt="article.title" class="cover-image" />
      </div>

      <!-- Article Body -->
      <div class="card body-card">
        <div class="article-content-wrapper" v-html="article.content"></div>
      </div>

      <!-- Article Tags -->
      <div v-if="article.tags && article.tags.length > 0" class="card tags-card">
        <span class="tags-label">文章标签：</span>
        <el-tag v-for="tag in article.tags" :key="tag" type="info" effect="light">
          {{ tag }}
        </el-tag>
      </div>

      <!-- Share Section -->
      <div class="card share-card">
        <h3 class="section-title">
          <el-icon><Share /></el-icon>
          分享文章
        </h3>
        <div class="share-buttons">
          <el-button @click="copyLink">
            <el-icon><Link /></el-icon>
            复制链接
          </el-button>
          <el-button @click="shareWeibo">
            <el-icon><Message /></el-icon>
            分享到微博
          </el-button>
        </div>
      </div>

      <!-- Related Articles -->
      <div v-if="relatedArticles.length > 0" class="card related-card">
        <h3 class="section-title">
          <el-icon><Document /></el-icon>
          相关文章
        </h3>
        <div class="related-list">
          <div
            v-for="related in relatedArticles"
            :key="related.id"
            class="related-item"
            @click="goToArticle(related.id)"
          >
            <div class="related-image" :style="{ background: getArticleGradient(related.category) }">
              <span class="related-placeholder-icon">{{ getCategoryIcon(related.category_name) }}</span>
            </div>
            <div class="related-info">
              <h4>{{ related.title }}</h4>
              <p class="related-summary">{{ related.summary || '点击查看详情' }}</p>
              <div class="related-meta">
                <span class="related-category" :style="{ color: getCategoryColor(related.category) }">
                  {{ related.category_name }}
                </span>
                <span class="related-date">{{ formatDate(related.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="card error-card">
      <el-result icon="error" title="文章不存在" :sub-title="error || '未找到该文章'">
        <template #extra>
          <el-button type="primary" @click="goBack">返回知识库</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, User, Calendar, View, Share, Link, Message, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getArticleDetail, getArticles } from '@/api/airquality'

const router = useRouter()
const route = useRoute()

const article = ref(null)
const relatedArticles = ref([])
const loading = ref(false)
const error = ref('')

const fetchArticle = async () => {
  loading.value = true
  error.value = ''
  try {
    const articleId = route.params.id
    const response = await getArticleDetail(articleId)
    article.value = response.data

    // Fetch related articles from same category
    if (article.value.category) {
      try {
        const relatedResponse = await getArticles({
          category: article.value.category,
          page: 1,
          page_size: 4
        })
        // Filter out current article
        relatedArticles.value = (relatedResponse.data.results || [])
          .filter(a => a.id !== article.value.id)
          .slice(0, 3)
      } catch (err) {
        console.error('Failed to fetch related articles:', err)
      }
    }
  } catch (err) {
    console.error('Failed to fetch article:', err)
    error.value = '加载文章失败'
    article.value = null
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push({ name: 'KnowledgeBase' })
}

const goToArticle = (articleId) => {
  router.push({ name: 'ArticleDetail', params: { id: articleId } })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const formatDate = (dateString) => {
  if (!dateString) return '未知日期'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getCategoryColor = (categoryId) => {
  const colors = {
    'pollution': '#F59E0B',
    'health': '#EC4899',
    'protection': '#10B981',
    'policy': '#8B5CF6'
  }
  return colors[categoryId] || '#0066CC'
}

const getCategoryIcon = (categoryName) => {
  const icons = {
    '污染原理': '🏭',
    '健康知识': '🏥',
    '防护指南': '🛡️',
    '政策法规': '⚖️'
  }
  return icons[categoryName] || '📄'
}

const getArticleGradient = (categoryId) => {
  const gradients = {
    'pollution': 'linear-gradient(135deg, #F59E0B, #D97706)',
    'health': 'linear-gradient(135deg, #EC4899, #DB2777)',
    'protection': 'linear-gradient(135deg, #10B981, #059669)',
    'policy': 'linear-gradient(135deg, #8B5CF6, #7C3AED)'
  }
  return gradients[categoryId] || 'linear-gradient(135deg, #0066CC, #0052A3)'
}

const copyLink = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    ElMessage.success('链接已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败，请手动复制链接')
  })
}

const shareWeibo = () => {
  const url = encodeURIComponent(window.location.href)
  const title = encodeURIComponent(article.value?.title || '空气质量科普文章')
  window.open(`https://service.weibo.com/share/share.php?url=${url}&title=${title}`, '_blank')
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-detail-page {
  padding: var(--spacing-xl);
  max-width: 900px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: var(--spacing-lg);
}

.back-button {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-lg);
}

.card:last-child {
  margin-bottom: 0;
}

/* Header Card */
.header-card {
  padding: var(--spacing-2xl);
  text-align: center;
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  margin: var(--spacing-md) 0;
  line-height: 1.3;
}

.article-summary {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 700px;
  margin: 0 auto var(--spacing-lg);
  line-height: 1.6;
}

.article-meta {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-secondary);
  font-size: 14px;
}

/* Article Cover */
.article-cover {
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.cover-image {
  width: 100%;
  height: auto;
  display: block;
}

/* Body Card */
.body-card {
  padding: var(--spacing-2xl);
}

.article-content-wrapper {
  font-size: 16px;
  line-height: 1.9;
  color: var(--text-secondary);
  max-width: 100%;
  overflow-wrap: break-word;
}

/* Article Content Styling */
.article-content-wrapper :deep(h1),
.article-content-wrapper :deep(h2),
.article-content-wrapper :deep(h3),
.article-content-wrapper :deep(h4),
.article-content-wrapper :deep(h5),
.article-content-wrapper :deep(h6) {
  color: var(--text);
  margin-top: var(--spacing-xl);
  margin-bottom: var(--spacing-md);
  font-weight: 600;
}

.article-content-wrapper :deep(h1) { font-size: 24px; }
.article-content-wrapper :deep(h2) { font-size: 20px; }
.article-content-wrapper :deep(h3) { font-size: 18px; }

.article-content-wrapper :deep(p) {
  margin-bottom: var(--spacing-md);
}

.article-content-wrapper :deep(a) {
  color: var(--primary);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color var(--transition-base);
}

.article-content-wrapper :deep(a:hover) {
  border-bottom-color: var(--primary);
}

.article-content-wrapper :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-md);
  margin: var(--spacing-lg) 0;
}

.article-content-wrapper :deep(blockquote) {
  border-left: 4px solid var(--primary);
  padding-left: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
  color: var(--text-secondary);
  font-style: italic;
}

.article-content-wrapper :deep(ul),
.article-content-wrapper :deep(ol) {
  margin: var(--spacing-md) 0;
  padding-left: var(--spacing-2xl);
}

.article-content-wrapper :deep(li) {
  margin-bottom: var(--spacing-sm);
}

.article-content-wrapper :deep(code) {
  background: var(--bg-hover);
  padding: 0.2rem 0.4rem;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--primary);
}

.article-content-wrapper :deep(pre) {
  background: var(--bg-hover);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: var(--spacing-lg) 0;
}

.article-content-wrapper :deep(pre code) {
  background: none;
  padding: 0;
}

.article-content-wrapper :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-lg) 0;
}

.article-content-wrapper :deep(th),
.article-content-wrapper :deep(td) {
  border: 1px solid var(--border);
  padding: var(--spacing-md);
  text-align: left;
}

.article-content-wrapper :deep(th) {
  background: var(--bg-hover);
  font-weight: 600;
  color: var(--text);
}

/* Tags Card */
.tags-card {
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.tags-label {
  color: var(--text-secondary);
  font-weight: 500;
}

/* Share Card */
.share-card {
  padding: var(--spacing-lg);
  text-align: center;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-md) 0;
}

.share-buttons {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

/* Related Card */
.related-card {
  padding: var(--spacing-lg);
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.related-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-hover);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.related-item:hover {
  background: var(--border);
}

.related-image {
  width: 100px;
  height: 80px;
  border-radius: var(--radius-md);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.related-placeholder-icon {
  font-size: 32px;
  opacity: 0.8;
}

.related-info {
  flex: 1;
  min-width: 0;
}

.related-info h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin: 0 0 var(--spacing-xs) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-summary {
  color: var(--text-secondary);
  font-size: 13px;
  margin-bottom: var(--spacing-xs);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-meta {
  display: flex;
  gap: var(--spacing-md);
  font-size: 12px;
}

.related-category {
  font-weight: 600;
}

.related-date {
  color: var(--text-secondary);
}

/* Error Card */
.error-card {
  padding: var(--spacing-2xl);
}

/* Loading */
.loading-container {
  padding: var(--spacing-2xl);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
}

/* Responsive */
@media (max-width: 768px) {
  .article-detail-page {
    padding: var(--spacing-md);
  }

  .header-card {
    padding: var(--spacing-lg);
  }

  .article-title {
    font-size: 22px;
  }

  .article-summary {
    font-size: 14px;
  }

  .article-meta {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .body-card {
    padding: var(--spacing-lg);
  }

  .article-content-wrapper {
    font-size: 15px;
  }

  .article-content-wrapper :deep(h1) {
    font-size: 20px;
  }

  .article-content-wrapper :deep(h2) {
    font-size: 18px;
  }

  .related-item {
    flex-direction: column;
  }

  .related-image {
    width: 100%;
    height: 120px;
  }

  .share-buttons {
    flex-direction: column;
  }
}
</style>
