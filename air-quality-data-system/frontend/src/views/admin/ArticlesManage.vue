<template>
  <div class="articles-manage-container">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-indicator"></div>
          <div class="header-title-group">
            <h1 class="header-title">文章管理</h1>
            <span class="header-subtitle">ARTICLE MANAGEMENT</span>
          </div>
        </div>
        <div class="header-actions">
          <button @click="openCategoryDialog" class="secondary-btn">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M7 7h.01M7 11h.01M7 15h.01M17 7v8a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h10a2 2 0 012 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span>分类管理</span>
          </button>
          <button @click="openCreateDialog" class="primary-btn">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M10 5v10M5 10h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span>新建文章</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Tabs -->
    <div class="tabs-section">
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="{ active: activeTab === tab.key }"
          class="tab-item"
        >
          <svg class="tab-icon" viewBox="0 0 20 20" fill="none">
            <path d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ tab.label }}
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>
    </div>

    <!-- Articles List -->
    <section class="content-section">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载文章数据...</p>
      </div>
      <div v-else-if="filteredArticles.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 20 20" fill="none">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p class="empty-text">暂无文章数据</p>
        <button @click="openCreateDialog" class="empty-action">创建第一篇文章</button>
      </div>
      <div v-else class="articles-grid">
        <article
          v-for="article in paginatedArticles"
          :key="article.id"
          class="article-card"
          :class="{ announcement: article.is_announcement }"
        >
          <div class="card-header">
            <span class="category-badge">{{ article.category_name || '未分类' }}</span>
            <div class="card-actions">
              <label class="announcement-toggle" :title="article.is_announcement ? '设为公告' : '取消公告'">
                <input
                  type="checkbox"
                  :checked="article.is_announcement"
                  @change="toggleAnnouncement(article)"
                  class="toggle-input"
                />
                <svg class="announcement-icon" viewBox="0 0 20 20" fill="none">
                  <path d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </label>
              <button @click="openEditDialog(article)" class="icon-btn edit-btn">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <button @click="handleDelete(article)" class="icon-btn delete-btn">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-preview">{{ truncateContent(article.content) }}</p>
          <div class="card-footer">
            <span class="article-status" :class="getStatusClass(article.status)">
              {{ getStatusText(article.status) }}
            </span>
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
          </div>
        </article>
      </div>
    </section>

    <!-- Pagination -->
    <section v-if="filteredArticles.length > pageSize" class="pagination-section">
      <div class="pagination-info">
        <span class="pagination-text">显示 {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, filteredArticles.length) }} 条，共 {{ filteredArticles.length }} 条</span>
      </div>
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1" class="page-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="{ active: page === currentPage }"
            class="page-number"
          >
            {{ page }}
          </button>
        </div>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="page-btn">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </section>

    <!-- Article Form Dialog -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="articleDialogVisible" class="modal-overlay large" @click="closeArticleDialog">
          <div class="modal-container large" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ isEditMode ? '编辑文章' : '新建文章' }}</h2>
              <button @click="closeArticleDialog" class="modal-close">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <form @submit.prevent="handleArticleSubmit" class="modal-form">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">文章标题</label>
                  <input
                    v-model="articleForm.title"
                    type="text"
                    class="form-input"
                    placeholder="请输入文章标题"
                    required
                    maxlength="255"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">文章分类</label>
                  <select v-model="articleForm.category_id" class="form-select" required>
                    <option value="">请选择分类</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                      {{ cat.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">发布状态</label>
                  <select v-model="articleForm.status" class="form-select" required>
                    <option value="DRAFT">草稿</option>
                    <option value="PUBLISHED">已发布</option>
                    <option value="OFFLINE">已下线</option>
                  </select>
                </div>
                <div class="form-group switch-group">
                  <label class="form-label">设为公告</label>
                  <label class="switch">
                    <input v-model="articleForm.is_announcement" type="checkbox" class="switch-input" />
                    <span class="switch-slider"></span>
                  </label>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">文章内容</label>
                <textarea
                  v-model="articleForm.content"
                  class="form-textarea content-editor"
                  rows="12"
                  placeholder="请输入文章内容，支持纯文本格式..."
                  required
                ></textarea>
                <span class="char-count">{{ articleForm.content.length }} 字符</span>
              </div>
              <div class="modal-footer">
                <button type="button" @click="closeArticleDialog" class="cancel-btn">取消</button>
                <button type="submit" class="submit-btn" :disabled="submitting">
                  <span v-if="submitting">保存中...</span>
                  <span v-else>{{ isEditMode ? '保存修改' : '发布文章' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Category Dialog -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="categoryDialogVisible" class="modal-overlay" @click="closeCategoryDialog">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">分类管理</h2>
              <button @click="closeCategoryDialog" class="modal-close">
                <svg viewBox="0 0 20 20" fill="none">
                  <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="category-form">
                <div class="form-row">
                  <div class="form-group">
                    <input
                      v-model="newCategoryName"
                      type="text"
                      class="form-input"
                      placeholder="新分类名称"
                      @keyup.enter="addCategory"
                    />
                  </div>
                  <button type="button" @click="addCategory" class="add-btn">添加</button>
                </div>
              </div>
              <div class="category-list">
                <div
                  v-for="category in categories"
                  :key="category.id"
                  class="category-item"
                >
                  <span class="category-name">{{ category.name }}</span>
                  <button @click="deleteCategory(category.id)" class="category-delete">
                    <svg viewBox="0 0 20 20" fill="none">
                      <path d="M6 18L18 6M6 6l12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Delete Confirmation -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="deleteDialogVisible" class="modal-overlay" @click="closeDeleteDialog">
          <div class="modal-container delete-modal" @click.stop>
            <div class="delete-icon-wrapper">
              <svg class="delete-icon" viewBox="0 0 20 20" fill="none">
                <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="delete-title">确认删除文章</h3>
            <p class="delete-message">
              您确定要删除文章 "{{ deleteTarget?.title }}" 吗？此操作无法撤销。
            </p>
            <div class="delete-actions">
              <button @click="closeDeleteDialog" class="cancel-btn">取消</button>
              <button @click="confirmDelete" class="delete-btn" :disabled="deleting">
                {{ deleting ? '删除中...' : '确认删除' }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getAdminArticles, createArticle, updateArticle, deleteArticleById } from '@/api/admin'
import { getAdminCategories, createCategory, deleteCategoryById } from '@/api/admin'

const loading = ref(false)
const articlesList = ref([])
const categories = ref([])
const activeTab = ref('all')
const currentPage = ref(1)
const pageSize = 12

const articleDialogVisible = ref(false)
const categoryDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)
const editingId = ref(null)
const deleteTarget = ref(null)
const deleting = ref(false)
const newCategoryName = ref('')

const articleForm = ref({
  title: '',
  category_id: '',
  content: '',
  status: 'DRAFT',
  is_announcement: false
})

const tabs = computed(() => [
  { key: 'all', label: '全部', count: articlesList.value.length },
  { key: 'PUBLISHED', label: '已发布', count: articlesList.value.filter(a => a.status === 'PUBLISHED').length },
  { key: 'DRAFT', label: '草稿', count: articlesList.value.filter(a => a.status === 'DRAFT').length },
  { key: 'OFFLINE', label: '已下线', count: articlesList.value.filter(a => a.status === 'OFFLINE').length }
])

const filteredArticles = computed(() => {
  if (activeTab.value === 'all') return articlesList.value
  return articlesList.value.filter(a => a.status === activeTab.value)
})

const totalPages = computed(() => Math.ceil(filteredArticles.value.length / pageSize))

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredArticles.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    }
  }
  return pages
})

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await getAdminArticles()
    if (response.code === 0) {
      articlesList.value = response.data || []
    }
  } catch (error) {
    ElMessage.error('加载文章失败')
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await getAdminCategories()
    if (response.code === 0) {
      categories.value = response.data || []
    }
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const goToPage = (page) => { if (typeof page === 'number') currentPage.value = page }

watch(activeTab, () => { currentPage.value = 1 })

const openCreateDialog = () => {
  isEditMode.value = false
  editingId.value = null
  articleForm.value = { title: '', category_id: '', content: '', status: 'DRAFT', is_announcement: false }
  articleDialogVisible.value = true
}

const openEditDialog = (article) => {
  isEditMode.value = true
  editingId.value = article.id
  articleForm.value = {
    title: article.title,
    category_id: article.category_id,
    content: article.content || '',
    status: article.status,
    is_announcement: article.is_announcement
  }
  articleDialogVisible.value = true
}

const closeArticleDialog = () => {
  articleDialogVisible.value = false
  setTimeout(() => {
    articleForm.value = { title: '', category_id: '', content: '', status: 'DRAFT', is_announcement: false }
  }, 300)
}

const handleArticleSubmit = async () => {
  submitting.value = true
  try {
    if (isEditMode.value) {
      await updateArticle(editingId.value, articleForm.value)
      ElMessage.success('文章更新成功')
    } else {
      await createArticle(articleForm.value)
      ElMessage.success('文章创建成功')
    }
    closeArticleDialog()
    await fetchArticles()
  } catch (error) {
    ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

const toggleAnnouncement = async (article) => {
  try {
    await updateArticle(article.id, { is_announcement: !article.is_announcement })
    article.is_announcement = !article.is_announcement
    ElMessage.success(article.is_announcement ? '已设为公告' : '已取消公告')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = (article) => {
  deleteTarget.value = article
  deleteDialogVisible.value = true
}

const closeDeleteDialog = () => {
  deleteDialogVisible.value = false
  deleteTarget.value = null
}

const confirmDelete = async () => {
  deleting.value = true
  try {
    await deleteArticleById(deleteTarget.value.id)
    ElMessage.success('文章删除成功')
    closeDeleteDialog()
    await fetchArticles()
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    deleting.value = false
  }
}

const openCategoryDialog = async () => {
  await fetchCategories()
  categoryDialogVisible.value = true
}

const closeCategoryDialog = () => {
  categoryDialogVisible.value = false
  newCategoryName.value = ''
}

const addCategory = async () => {
  if (!newCategoryName.value.trim()) {
    ElMessage.warning('请输入分类名称')
    return
  }
  try {
    await createCategory({ name: newCategoryName.value.trim() })
    ElMessage.success('分类添加成功')
    newCategoryName.value = ''
    await fetchCategories()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

const deleteCategory = async (id) => {
  try {
    await deleteCategoryById(id)
    ElMessage.success('分类删除成功')
    await fetchCategories()
  } catch (error) {
    ElMessage.error('删除失败：' + (error.response?.data?.message || '该分类下存在文章'))
  }
}

const truncateContent = (content) => {
  if (!content) return '暂无内容'
  const text = content.replace(/<[^>]*>/g, '').trim()
  return text.length > 120 ? text.substring(0, 120) + '...' : text
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getStatusClass = (status) => {
  const classes = { DRAFT: 'draft', PUBLISHED: 'published', OFFLINE: 'offline' }
  return classes[status] || ''
}

const getStatusText = (status) => {
  const texts = { DRAFT: '草稿', PUBLISHED: '已发布', OFFLINE: '已下线' }
  return texts[status] || status
}

onMounted(() => {
  fetchArticles()
  fetchCategories()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

:root {
  --bg-primary: #0a0e1a;
  --bg-secondary: #0d121d;
  --bg-card: #111827;
  --bg-hover: #1a2332;
  --border-color: #1e293b;
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-cyan: #22d3ee;
  --accent-cyan-dim: rgba(34, 211, 238, 0.1);
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #fbbf24;
}

.articles-manage-container {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Noto Sans SC', sans-serif;
}

.page-header {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px 28px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-indicator {
  width: 4px;
  height: 32px;
  background: linear-gradient(180deg, var(--accent-cyan) 0%, rgba(34, 211, 238, 0.3) 100%);
  border-radius: 2px;
}

.header-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.header-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.secondary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-btn:hover {
  background: var(--bg-hover);
}

.secondary-btn svg {
  width: 18px;
  height: 18px;
}

.primary-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--accent-cyan);
  border: none;
  border-radius: 12px;
  color: var(--bg-primary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.primary-btn:hover {
  background: #1ed5f3;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(34, 211, 238, 0.3);
}

.primary-btn svg {
  width: 18px;
  height: 18px;
}

.tabs-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 8px;
}

.tabs {
  display: flex;
  gap: 4px;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-item:hover {
  background: var(--bg-hover);
}

.tab-item.active {
  background: var(--accent-cyan-dim);
  color: var(--accent-cyan);
}

.tab-icon {
  width: 16px;
  height: 16px;
}

.tab-count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  padding: 2px 6px;
  background: var(--bg-secondary);
  border-radius: 10px;
}

.content-section {
  min-height: 400px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 20px;
  color: var(--text-muted);
  font-size: 14px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.empty-text {
  color: var(--text-muted);
  font-size: 16px;
  margin-bottom: 20px;
}

.empty-action {
  padding: 10px 20px;
  background: var(--accent-cyan);
  border: none;
  border-radius: 10px;
  color: var(--bg-primary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.empty-action:hover {
  background: #1ed5f3;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.2s;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  border-color: var(--accent-cyan-dim);
}

.article-card.announcement {
  border-color: rgba(34, 211, 238, 0.3);
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.03) 0%, var(--bg-card) 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.category-badge {
  padding: 4px 10px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.announcement-toggle {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-muted);
}

.announcement-toggle:hover {
  background: var(--bg-hover);
}

.announcement-toggle input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.announcement-toggle:has(input:checked) {
  color: var(--warning);
}

.announcement-icon {
  width: 16px;
  height: 16px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-muted);
}

.icon-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.edit-btn:hover {
  color: var(--accent-cyan);
  background: var(--accent-cyan-dim);
}

.delete-btn:hover {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
}

.icon-btn svg {
  width: 16px;
  height: 16px;
}

.article-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-preview {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
  min-height: 60px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.article-status {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.article-status.draft {
  background: rgba(100, 116, 139, 0.1);
  color: var(--text-muted);
}

.article-status.published {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.article-status.offline {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.article-date {
  font-size: 12px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.pagination-info {
  color: var(--text-secondary);
  font-size: 13px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.page-btn:hover:not(:disabled) {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-number {
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.page-number:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.page-number.active {
  background: var(--accent-cyan);
  color: var(--bg-primary);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 14, 26, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-overlay.large {
  padding: 40px;
}

.modal-container {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
}

.modal-container.large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-color);
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s;
}

.modal-close:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.modal-close svg {
  width: 18px;
  height: 18px;
}

.modal-form {
  padding: 28px;
}

.modal-body {
  padding: 28px;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.2s;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.form-textarea {
  width: 100%;
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  transition: all 0.2s;
}

.form-textarea:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px var(--accent-cyan-dim);
}

.content-editor {
  line-height: 1.6;
}

.char-count {
  position: absolute;
  bottom: 10px;
  right: 16px;
  font-size: 11px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}

.switch-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
}

.switch-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-hover);
  border-radius: 26px;
  transition: all 0.3s;
}

.switch-slider::before {
  content: '';
  position: absolute;
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s;
}

.switch-input:checked + .switch-slider {
  background: var(--accent-cyan);
}

.switch-input:checked + .switch-slider::before {
  transform: translateX(22px);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 8px;
}

.cancel-btn,
.submit-btn {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.cancel-btn:hover {
  background: var(--bg-hover);
  border-color: var(--text-muted);
}

.submit-btn {
  background: var(--accent-cyan);
  border: none;
  color: var(--bg-primary);
}

.submit-btn:hover:not(:disabled) {
  background: #1ed5f3;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Category Management */
.category-form {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.add-btn {
  padding: 12px 20px;
  background: var(--accent-cyan);
  border: none;
  border-radius: 10px;
  color: var(--bg-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: #1ed5f3;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
}

.category-name {
  font-size: 14px;
  color: var(--text-primary);
}

.category-delete {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s;
}

.category-delete:hover {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.category-delete svg {
  width: 16px;
  height: 16px;
}

/* Delete Modal */
.delete-modal {
  max-width: 400px;
  text-align: center;
}

.delete-icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.delete-icon {
  width: 56px;
  height: 56px;
  color: var(--danger);
}

.delete-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.delete-message {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 24px;
}

.delete-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.delete-btn {
  padding: 12px 24px;
  background: var(--danger);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover:not(:disabled) {
  background: #f87171;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

/* Scrollbar */
.modal-container::-webkit-scrollbar,
.category-list::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track,
.category-list::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.modal-container::-webkit-scrollbar-thumb,
.category-list::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb:hover,
.category-list::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}

/* Responsive */
@media (max-width: 1024px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .articles-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }

  .secondary-btn,
  .primary-btn {
    flex: 1;
    justify-content: center;
  }

  .pagination-section {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
