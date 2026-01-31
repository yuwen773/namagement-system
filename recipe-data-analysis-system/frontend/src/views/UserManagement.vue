<template>
  <div class="user-management-page">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          用户管理
        </h1>
        <p class="page-subtitle">管理系统用户账户及权限</p>
      </div>
    </div>

    <div class="content-wrapper">
      <!-- 搜索和筛选栏 -->
      <div class="toolbar">
        <div class="search-box">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l-4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索用户名或邮箱..."
            @keyup.enter="handleSearch"
          >
        </div>

        <div class="filter-group">
          <select v-model="roleFilter" @change="handleSearch" class="role-select">
            <option value="">全部角色</option>
            <option value="admin">管理员</option>
            <option value="user">普通用户</option>
          </select>
        </div>
      </div>

      <!-- 用户列表 -->
      <div v-loading="loading" class="user-list-container">
        <div v-if="userList.length === 0 && !loading" class="empty-state">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M17 20H3a2 2 0 01-2-2V6a2 2 0 012-2h4a2 2 0 012 2h6a2 2 0 012 2h4a2 2 0 012 2v12a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="9" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
            <path d="M4 16c0-2 2.5-3 5-3s5 1 5 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <p>暂无用户数据</p>
        </div>

        <div v-else class="user-table-wrapper">
          <table class="user-table">
            <thead>
              <tr>
                <th>用户信息</th>
                <th>角色</th>
                <th>状态</th>
                <th>注册时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in userList" :key="user.id" :class="{ 'banned-row': !user.is_active }">
                <td class="user-info-cell">
                  <div class="user-avatar">
                    {{ user.username.charAt(0).toUpperCase() }}
                  </div>
                  <div class="user-details">
                    <div class="user-name">{{ user.username }}</div>
                    <div class="user-email">{{ user.email || '无邮箱' }}</div>
                  </div>
                </td>
                <td class="role-cell">
                  <span class="role-badge" :class="user.role">
                    {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                  </span>
                </td>
                <td class="status-cell">
                  <span class="status-badge" :class="{ active: user.is_active, banned: !user.is_active }">
                    {{ user.is_active ? '正常' : '已封禁' }}
                  </span>
                </td>
                <td class="date-cell">
                  {{ formatDate(user.created_at) }}
                </td>
                <td class="action-cell">
                  <button
                    v-if="user.is_active && user.id !== currentUserId"
                    @click="handleBan(user)"
                    class="action-btn ban-btn"
                    :disabled="banningUserId === user.id"
                  >
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M18 10a8 8 0 11-16 0 8 8 0 0116 0z" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M10 6v4m0 0v4m0-4h4m-4 0H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    {{ banningUserId === user.id ? '处理中...' : '封禁' }}
                  </button>
                  <button
                    v-if="!user.is_active"
                    @click="handleUnban(user)"
                    class="action-btn unban-btn"
                    :disabled="unbanningUserId === user.id"
                  >
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M18 10a8 8 0 11-16 0 8 8 0 0116 0z" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M10 6l4 4m0 0l-4 4m4-4H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    {{ unbanningUserId === user.id ? '处理中...' : '解封' }}
                  </button>
                  <span v-if="user.id === currentUserId" class="self-hint">当前用户</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalCount > 0" class="pagination">
        <button
          @click="handlePrevPage"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 15l-4-4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          上一页
        </button>
        <span class="pagination-info">{{ currentPage }} / {{ totalPages }}</span>
        <button
          @click="handleNextPage"
          :disabled="currentPage >= totalPages"
          class="pagination-btn"
        >
          下一页
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 15l4-4-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getUserList, banUser, unbanUser } from '@/api/auth'

const userStore = useUserStore()

// 状态
const loading = ref(false)
const userList = ref([])
const searchQuery = ref('')
const roleFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const totalCount = ref(0)
const banningUserId = ref(null)
const unbanningUserId = ref(null)

// 当前用户ID
const currentUserId = computed(() => userStore.userInfo?.id)

// 总页数
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))

// 获取用户列表
const fetchUserList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (roleFilter.value) {
      params.role = roleFilter.value
    }

    const response = await getUserList(params)
    userList.value = response.data.results || []
    totalCount.value = response.data.count || 0
  } catch (error) {
    ElMessage.error(error.message || '获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchUserList()
}

// 上一页
const handlePrevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchUserList()
  }
}

// 下一页
const handleNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchUserList()
  }
}

// 封禁用户
const handleBan = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要封禁用户 "${user.username}" 吗？封禁后该用户将无法登录系统。`,
      '封禁确认',
      {
        confirmButtonText: '确定封禁',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    banningUserId.value = user.id
    await banUser(user.id)
    ElMessage.success(`用户 "${user.username}" 已封禁`)
    fetchUserList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '封禁失败')
    }
  } finally {
    banningUserId.value = null
  }
}

// 解封用户
const handleUnban = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要解封用户 "${user.username}" 吗？解封后该用户将可以正常登录。`,
      '解封确认',
      {
        confirmButtonText: '确定解封',
        cancelButtonText: '取消',
        type: 'success'
      }
    )

    unbanningUserId.value = user.id
    await unbanUser(user.id)
    ElMessage.success(`用户 "${user.username}" 已解封`)
    fetchUserList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '解封失败')
    }
  } finally {
    unbanningUserId.value = null
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 页面加载时获取用户列表
onMounted(() => {
  fetchUserList()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.user-management-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #faf8f5 0%, #f5f0e8 100%);
  padding-top: 80px;
  font-family: 'DM Sans', sans-serif;
}

/* 页面头部 */
.page-header {
  background: white;
  border-bottom: 1px solid #f0ebe3;
  padding: 2rem 2rem 1.5rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Noto Serif SC', serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.page-title svg {
  width: 32px;
  height: 32px;
  color: #c2622e;
}

.page-subtitle {
  font-size: 0.95rem;
  color: #8b7355;
  margin: 0;
}

/* 内容区域 */
.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 工具栏 */
.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 280px;
  display: flex;
  align-items: center;
  background: white;
  border: 1.5px solid #e5ddd3;
  border-radius: 12px;
  padding: 0 1rem;
  transition: border-color 0.2s ease;
}

.search-box:focus-within {
  border-color: #c2622e;
}

.search-box svg {
  width: 18px;
  height: 18px;
  color: #a89078;
  flex-shrink: 0;
}

.search-box input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0.75rem;
  font-size: 0.95rem;
  font-family: inherit;
  color: #3d2914;
  background: transparent;
}

.search-box input::placeholder {
  color: #b8a99a;
}

.filter-group {
  display: flex;
  gap: 0.75rem;
}

.role-select {
  padding: 0.75rem 1.5rem;
  border: 1.5px solid #e5ddd3;
  border-radius: 12px;
  font-size: 0.95rem;
  font-family: inherit;
  color: #3d2914;
  background: white;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s ease;
}

.role-select:hover {
  border-color: #d4c4b0;
}

.role-select:focus {
  border-color: #c2622e;
}

/* 用户列表容器 */
.user-list-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(61, 41, 20, 0.06);
  min-height: 400px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #a89078;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1rem;
  margin: 0;
}

/* 表格包装器 */
.user-table-wrapper {
  overflow-x: auto;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table thead {
  background: #faf8f5;
}

.user-table th {
  padding: 1rem 1.5rem;
  text-align: left;
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b5c4d;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #f0ebe3;
}

.user-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f5f0e8;
}

.user-table tr:last-child td {
  border-bottom: none;
}

.user-table tbody tr {
  transition: background-color 0.15s ease;
}

.user-table tbody tr:hover {
  background: #faf8f5;
}

.user-table tbody tr.banned-row {
  background: rgba(231, 76, 60, 0.03);
  opacity: 0.7;
}

/* 用户信息单元格 */
.user-info-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-name {
  font-weight: 600;
  color: #3d2914;
  font-size: 0.95rem;
}

.user-email {
  font-size: 0.85rem;
  color: #8b7355;
}

/* 角色标签 */
.role-badge {
  display: inline-block;
  padding: 0.4rem 0.85rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.role-badge.admin {
  background: rgba(194, 98, 46, 0.1);
  color: #c2622e;
}

.role-badge.user {
  background: rgba(168, 144, 120, 0.15);
  color: #6b5c4d;
}

/* 状态标签 */
.status-badge {
  display: inline-block;
  padding: 0.4rem 0.85rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(46, 125, 50, 0.1);
  color: #2e7d32;
}

.status-badge.banned {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

/* 日期单元格 */
.date-cell {
  color: #8b7355;
  font-size: 0.9rem;
}

/* 操作单元格 */
.action-cell {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.85rem;
  border: 1.5px solid;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background: white;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ban-btn {
  border-color: #e74c3c;
  color: #e74c3c;
}

.ban-btn:hover:not(:disabled) {
  background: #e74c3c;
  color: white;
}

.unban-btn {
  border-color: #2e7d32;
  color: #2e7d32;
}

.unban-btn:hover:not(:disabled) {
  background: #2e7d32;
  color: white;
}

.self-hint {
  font-size: 0.8rem;
  color: #a89078;
  font-style: italic;
}

/* 分页 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  border: 1.5px solid #e5ddd3;
  border-radius: 10px;
  background: white;
  color: #6b5c4d;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  border-color: #c2622e;
  color: #c2622e;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-btn svg {
  width: 16px;
  height: 16px;
}

.pagination-info {
  font-size: 0.9rem;
  color: #6b5c4d;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-management-page {
    padding-top: 72px;
  }

  .content-wrapper {
    padding: 1rem;
  }

  .page-header {
    padding: 1.5rem 1rem 1rem;
  }

  .page-title {
    font-size: 1.4rem;
  }

  .page-title svg {
    width: 28px;
    height: 28px;
  }

  .toolbar {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .filter-group {
    width: 100%;
  }

  .role-select {
    flex: 1;
  }

  .user-table th,
  .user-table td {
    padding: 0.85rem 1rem;
  }

  .user-info-cell {
    gap: 0.75rem;
  }

  .user-avatar {
    width: 38px;
    height: 38px;
    font-size: 1rem;
  }

  .action-btn {
    padding: 0.4rem 0.7rem;
    font-size: 0.8rem;
  }
}
</style>
