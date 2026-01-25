<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElCard, ElRow, ElCol, ElTag, ElEmpty, ElPagination } from 'element-plus'
import { getPublicNoticeList } from '@/api/notice'
import { formatDateTime } from '@/utils/format'

const router = useRouter()

const noticeList = ref([])
const loading = ref(false)
const pagination = ref({
  page: 1,
  page_size: 10,
  total: 0
})

// 获取公告列表
const fetchNoticeList = async () => {
  loading.value = true
  try {
    const res = await getPublicNoticeList({
      page: pagination.value.page,
      page_size: pagination.value.page_size
    })
    // 处理响应格式：{code: 0, data: [...], total: n} 或 {count, results}
    const responseData = res.data?.data || res.data?.results || []
    const totalCount = res.data?.total || res.data?.count || 0

    noticeList.value = responseData.map(item => ({
      id: item.id,
      title: item.title,
      is_pinned: item.is_pinned,
      published_at: item.published_at,
      created_at: item.created_at,
      // 截取内容预览（去除 Markdown 格式）
      content_preview: stripMarkdown(item.content).substring(0, 150) + '...'
    }))
    pagination.value.total = totalCount
  } catch (error) {
    console.error('获取公告列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 去除 Markdown 格式获取纯文本
const stripMarkdown = (content) => {
  if (!content) return ''
  return content
    .replace(/#{1,6}\s+/g, '')  // 标题
    .replace(/\*\*(.*?)\*\*/g, '$1')  // 粗体
    .replace(/\*(.*?)\*/g, '$1')  // 斜体
    .replace(/`{1,3}[^`]*`{1,3}/g, '')  // 行内代码
    .replace(/!\[.*?\]\(.*?\)/g, '')  // 图片
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')  // 链接
    .replace(/^\s*[-*+]\s+/gm, '')  // 列表项
    .replace(/^\s*\d+\.\s+/gm, '')  // 数字列表
    .replace(/>\s+/g, '')  // 引用
    .replace(/\n+/g, ' ')  // 换行转空格
    .trim()
}

// 跳转到公告详情
const goToDetail = (id) => {
  router.push(`/notices/${id}`)
}

// 分页处理
const handlePageChange = (page) => {
  pagination.value.page = page
  fetchNoticeList()
}

const handleSizeChange = (size) => {
  pagination.value.page_size = size
  pagination.value.page = 1
  fetchNoticeList()
}

onMounted(() => {
  fetchNoticeList()
})
</script>

<template>
  <div class="notice-list-container">
    <div class="page-header">
      <h2>系统公告</h2>
      <p class="subtitle">查看公司最新通知和公告</p>
    </div>

    <!-- 公告列表 -->
    <div v-loading="loading" class="notice-content">
      <el-row :gutter="20" v-if="noticeList.length > 0">
        <el-col
          v-for="notice in noticeList"
          :key="notice.id"
          :span="24"
          class="notice-item"
        >
          <el-card
            class="notice-card"
            shadow="hover"
            @click="goToDetail(notice.id)"
          >
            <div class="notice-header">
              <div class="notice-title-wrapper">
                <el-tag
                  v-if="notice.is_pinned"
                  type="warning"
                  size="small"
                  effect="dark"
                  class="pinned-tag"
                >
                  置顶
                </el-tag>
                <h3 class="notice-title">{{ notice.title }}</h3>
              </div>
              <span class="notice-date">
                {{ formatDateTime(notice.published_at || notice.created_at) }}
              </span>
            </div>
            <p class="notice-preview">{{ notice.content_preview }}</p>
            <div class="notice-footer">
              <span class="read-more">查看详情 →</span>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-empty v-else-if="!loading" description="暂无公告" />
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="pagination.total > pagination.page_size">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 30, 50]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Notice List - Refined Corporate Design
   ======================================== */
.notice-list-container {
  padding: 24px;
  min-height: calc(100vh - 112px);
  position: relative;
}

.notice-list-container::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -30px;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.page-header {
  margin-bottom: 24px;
  padding: 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light), var(--color-warning));
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-header h2::before {
  content: '';
  width: 4px;
  height: 24px;
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  border-radius: 2px;
}

.subtitle {
  margin: 0;
  color: var(--color-text-tertiary);
  font-size: 14px;
  padding-left: 16px;
}

.notice-content {
  min-height: 200px;
  position: relative;
  z-index: 1;
}

.notice-item {
  margin-bottom: 16px;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
}

.notice-item:nth-child(1) { animation-delay: 0.1s; }
.notice-item:nth-child(2) { animation-delay: 0.2s; }
.notice-item:nth-child(3) { animation-delay: 0.3s; }
.notice-item:nth-child(4) { animation-delay: 0.4s; }
.notice-item:nth-child(5) { animation-delay: 0.5s; }

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

.notice-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  background: var(--color-bg-secondary);
  overflow: hidden;
  position: relative;
}

.notice-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.notice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.12);
  border-color: var(--color-primary-light);
}

.notice-card:hover::before {
  opacity: 1;
}

.notice-card :deep(.el-card__body) {
  padding: 24px;
}

.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.notice-title-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.pinned-tag {
  flex-shrink: 0;
  font-weight: 500;
  border-radius: var(--radius-full);
  padding: 2px 10px;
}

.notice-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  letter-spacing: 0.3px;
}

.notice-date {
  color: var(--color-text-tertiary);
  font-size: 13px;
  flex-shrink: 0;
  margin-left: 16px;
  font-weight: 400;
}

.notice-preview {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
  margin: 0 0 16px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notice-footer {
  text-align: right;
}

.read-more {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.read-more::after {
  content: '→';
  transition: transform 0.3s ease;
}

.notice-card:hover .read-more {
  color: var(--color-primary-dark);
}

.notice-card:hover .read-more::after {
  transform: translateX(4px);
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 32px;
  padding: 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  position: relative;
  z-index: 1;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    padding: 20px;
  }

  .page-header h2 {
    font-size: 20px;
  }

  .subtitle {
    padding-left: 0;
    padding-top: 8px;
  }

  .notice-card :deep(.el-card__body) {
    padding: 16px;
  }

  .notice-header {
    flex-direction: column;
    gap: 8px;
  }

  .notice-date {
    margin-left: 0;
    font-size: 12px;
  }
}
</style>
