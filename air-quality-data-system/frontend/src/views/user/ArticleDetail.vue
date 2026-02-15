<template>
  <div class="article-detail-page grid-background">
    <!-- Floating Particles -->
    <div class="particles">
      <div v-for="i in 10" :key="i" class="particle" :style="{ '--delay': `${i * 0.7}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
    </div>

    <div class="container">
      <!-- Back Button -->
      <div class="back-button fade-in" @click="goBack">
        <span class="back-icon">←</span>
        <span>返回知识库</span>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container fade-in">
        <div class="loading-spinner"></div>
        <p>加载文章中...</p>
      </div>

      <!-- Article Content -->
      <div v-else-if="article" class="article-content">
        <!-- Article Header -->
        <header class="article-header glass-card fade-in-down">
          <div class="article-category-badge" :style="{ background: getCategoryColor(article.category) }">
            {{ article.category_name || '未分类' }}
          </div>
          <h1 class="article-title">{{ article.title }}</h1>
          <p v-if="article.summary" class="article-summary">{{ article.summary }}</p>
          <div class="article-meta">
            <div class="meta-item">
              <span class="meta-icon">👤</span>
              <span>{{ article.author || '管理员' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">📅</span>
              <span>{{ formatDate(article.created_at) }}</span>
            </div>
            <div v-if="article.view_count" class="meta-item">
              <span class="meta-icon">👁️</span>
              <span>{{ article.view_count }} 次浏览</span>
            </div>
          </div>
        </header>

        <!-- Article Cover Image -->
        <div v-if="article.cover_image" class="article-cover fade-in" style="animation-delay: 0.1s">
          <img :src="article.cover_image" :alt="article.title" class="cover-image" />
        </div>

        <!-- Article Body -->
        <article class="article-body glass-card fade-in" style="animation-delay: 0.2s">
          <div class="article-content-wrapper" v-html="article.content"></div>
        </article>

        <!-- Article Tags -->
        <div v-if="article.tags && article.tags.length > 0" class="article-tags glass-card fade-in" style="animation-delay: 0.3s">
          <span class="tags-label">文章标签：</span>
          <span v-for="tag in article.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <!-- Share Section -->
        <div class="share-section glass-card fade-in" style="animation-delay: 0.4s">
          <h3>分享文章</h3>
          <div class="share-buttons">
            <button class="share-btn" @click="copyLink" title="复制链接">
              <span class="share-icon">🔗</span>
              <span>复制链接</span>
            </button>
            <button class="share-btn" @click="shareWeibo" title="分享到微博">
              <span class="share-icon">📱</span>
              <span>微博</span>
            </button>
          </div>
        </div>

        <!-- Related Articles -->
        <div v-if="relatedArticles.length > 0" class="related-articles glass-card fade-in" style="animation-delay: 0.5s">
          <h3 class="section-title">
            <span class="title-icon">📖</span>
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
      <div v-else class="error-container glass-card">
        <span class="error-icon">📄</span>
        <h3>文章不存在</h3>
        <p>{{ error || '未找到该文章' }}</p>
        <button class="back-btn" @click="goBack">返回知识库</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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
    'pollution': '#f59e0b',
    'health': '#ec4899',
    'protection': '#10b981',
    'policy': '#8b5cf6'
  }
  return colors[categoryId] || '#60a5fa'
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
    'pollution': 'linear-gradient(135deg, #f59e0b, #d97706)',
    'health': 'linear-gradient(135deg, #ec4899, #db2777)',
    'protection': 'linear-gradient(135deg, #10b981, #059669)',
    'policy': 'linear-gradient(135deg, #8b5cf6, #7c3aed)'
  }
  return gradients[categoryId] || 'linear-gradient(135deg, #60a5fa, #3b82f6)'
}

const copyLink = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    alert('链接已复制到剪贴板')
  }).catch(() => {
    alert('复制失败，请手动复制链接')
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
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.article-detail-page {
  min-height: 100vh;
  padding: 2rem;
  position: relative;
  overflow-x: hidden;
  font-family: 'IBM Plex Sans', sans-serif;
  color: #e2e8f0;
}

.grid-background {
  background-color: #020617;
  background-image:
    linear-gradient(rgba(30, 41, 59, 0.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30, 41, 59, 0.3) 1px, transparent 1px);
  background-size: 50px 50px;
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(148, 163, 184, 0.3);
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
  animation-delay: var(--delay);
  left: var(--x);
  top: var(--y);
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100vh) translateX(50px); opacity: 0; }
}

.container {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* Back Button */
.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  margin-bottom: 2rem;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.back-button:hover {
  color: #60a5fa;
  transform: translateX(-5px);
}

.back-icon {
  font-size: 1.2rem;
}

/* Loading & Error */
.loading-container {
  text-align: center;
  padding: 6rem 2rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1.5rem;
  border: 3px solid rgba(96, 165, 250, 0.2);
  border-top-color: #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-container p {
  color: #94a3b8;
}

.error-container {
  text-align: center;
  padding: 6rem 2rem;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.error-container h3 {
  color: #f1f5f9;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

.back-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
}

/* Article Content */
.article-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Article Header */
.article-header {
  padding: 2.5rem;
  text-align: center;
}

.article-category-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1.5rem;
}

.article-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.article-summary {
  font-size: 1.1rem;
  color: #94a3b8;
  max-width: 700px;
  margin: 0 auto 1.5rem;
  line-height: 1.6;
}

.article-meta {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.9rem;
  font-family: 'JetBrains Mono', monospace;
}

.meta-icon {
  font-size: 1.1rem;
}

/* Article Cover */
.article-cover {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.cover-image {
  width: 100%;
  height: auto;
  display: block;
}

/* Article Body */
.article-body {
  padding: 3rem;
}

.article-content-wrapper {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.1rem;
  line-height: 1.9;
  color: #cbd5e1;
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
  font-family: 'Rajdhani', sans-serif;
  color: #f1f5f9;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.article-content-wrapper :deep(h1) { font-size: 2rem; }
.article-content-wrapper :deep(h2) { font-size: 1.75rem; }
.article-content-wrapper :deep(h3) { font-size: 1.5rem; }

.article-content-wrapper :deep(p) {
  margin-bottom: 1.25rem;
}

.article-content-wrapper :deep(a) {
  color: #60a5fa;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s ease;
}

.article-content-wrapper :deep(a:hover) {
  border-bottom-color: #60a5fa;
}

.article-content-wrapper :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 1.5rem 0;
}

.article-content-wrapper :deep(blockquote) {
  border-left: 4px solid #60a5fa;
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  color: #94a3b8;
  font-style: italic;
}

.article-content-wrapper :deep(ul),
.article-content-wrapper :deep(ol) {
  margin: 1.25rem 0;
  padding-left: 2rem;
}

.article-content-wrapper :deep(li) {
  margin-bottom: 0.5rem;
}

.article-content-wrapper :deep(code) {
  background: rgba(15, 23, 42, 0.6);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
  color: #60a5fa;
}

.article-content-wrapper :deep(pre) {
  background: rgba(15, 23, 42, 0.8);
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.article-content-wrapper :deep(pre code) {
  background: none;
  padding: 0;
  color: #cbd5e1;
}

.article-content-wrapper :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.article-content-wrapper :deep(th),
.article-content-wrapper :deep(td) {
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 0.75rem;
  text-align: left;
}

.article-content-wrapper :deep(th) {
  background: rgba(15, 23, 42, 0.6);
  font-weight: 600;
  color: #f1f5f9;
}

/* Article Tags */
.article-tags {
  padding: 1.25rem 2rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tags-label {
  color: #94a3b8;
  font-weight: 500;
}

.tag {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.9rem;
  border: 1px solid rgba(96, 165, 250, 0.3);
}

/* Share Section */
.share-section {
  padding: 1.5rem 2rem;
  text-align: center;
}

.share-section h3 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.25rem;
  color: #f1f5f9;
  margin-bottom: 1rem;
}

.share-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.share-btn {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #cbd5e1;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.share-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
  color: #60a5fa;
  transform: translateY(-2px);
}

.share-icon {
  font-size: 1.2rem;
}

/* Related Articles */
.related-articles {
  padding: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.title-icon {
  font-size: 1.5rem;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.related-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.related-item:hover {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(96, 165, 250, 0.4);
  transform: translateX(5px);
}

.related-image {
  width: 100px;
  height: 80px;
  border-radius: 8px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.related-placeholder-icon {
  font-size: 2rem;
  opacity: 0.8;
}

.related-info {
  flex: 1;
  min-width: 0;
}

.related-info h4 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-summary {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
}

.related-category {
  font-weight: 600;
}

.related-date {
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
}

/* Glass Card */
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  transition: all 0.3s ease;
}

/* Animations */
.fade-in {
  animation: fade-in 0.5s ease forwards;
  opacity: 0;
}

@keyframes fade-in {
  to { opacity: 1; }
}

.fade-in-down {
  animation: fade-in-down 0.6s ease forwards;
  opacity: 0;
}

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .article-detail-page {
    padding: 1rem;
  }

  .article-header {
    padding: 1.5rem;
  }

  .article-title {
    font-size: 1.75rem;
  }

  .article-summary {
    font-size: 1rem;
  }

  .article-meta {
    flex-direction: column;
    gap: 0.75rem;
  }

  .article-body {
    padding: 1.5rem;
  }

  .article-content-wrapper {
    font-size: 1rem;
  }

  .article-content-wrapper :deep(h1) {
    font-size: 1.5rem;
  }

  .article-content-wrapper :deep(h2) {
    font-size: 1.3rem;
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

  .share-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
