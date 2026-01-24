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
.notice-list-container {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 112px);
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.notice-content {
  min-height: 200px;
}

.notice-item {
  margin-bottom: 16px;
}

.notice-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.notice-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.pinned-tag {
  flex-shrink: 0;
}

.notice-title {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-date {
  color: #909399;
  font-size: 13px;
  flex-shrink: 0;
  margin-left: 16px;
}

.notice-preview {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
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
  color: #409eff;
  font-size: 13px;
  transition: color 0.3s;
}

.notice-card:hover .read-more {
  color: #66b1ff;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  padding: 16px 0;
}
</style>
