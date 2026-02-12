<template>
  <div class="user-manage-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">用户管理</h1>
          <p class="page-subtitle">管理系统用户账号与权限</p>
        </div>
      </div>
      <div class="header-stats">
        <div class="stat-badge">
          <span class="stat-number">{{ users.length }}</span>
          <span class="stat-label">总用户</span>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input v-model="searchQuery" placeholder="搜索用户名、姓名、手机号..." class="search-input" />
      </div>
      <ViewToggle v-model="viewMode" />
      <div class="filter-tabs">
        <button
          v-for="tab in filterTabs"
          :key="tab.key"
          :class="['filter-tab', { active: activeFilter === tab.key }]"
          @click="activeFilter = tab.key"
        >
          <svg viewBox="0 0 20 20" fill="currentColor">
            <circle cx="10" cy="10" r="6"/>
          </svg>
          <span>{{ tab.label }}</span>
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>
    </div>

    <!-- List View -->
    <div v-if="viewMode === 'list'" v-loading="loading" class="list-view-container">
      <el-table :data="filteredUsers" class="users-table">
        <el-table-column label="头像" width="80">
          <template #default="{ row }">
            <div class="table-avatar">
              {{ row.realName?.charAt(0) || row.username?.charAt(0) || 'U' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="realName" label="真实姓名" width="150">
          <template #default="{ row }">
            {{ row.realName || '未设置' }}
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <span :class="['role-tag', row.role]">
              {{ row.role === 'ADMIN' ? '管理员' : '用户' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="isActive" label="状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.isActive" @change="updateStatus(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button link type="primary" @click="editUser(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Empty State for List -->
      <div v-if="filteredUsers.length === 0" class="empty-state-list">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <p>没有找到用户</p>
      </div>
    </div>

    <!-- Card View -->
    <div v-else v-loading="loading" class="users-grid">
      <div v-for="user in filteredUsers" :key="user.id" class="user-card">
        <div class="card-header">
          <div class="user-avatar">
            {{ user.realName?.charAt(0) || user.username?.charAt(0) || 'U' }}
          </div>
          <div class="role-badge" :class="user.role">
            <svg v-if="user.role === 'ADMIN'" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2L3 7v11c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V7l-7-5z"/>
            </svg>
            <svg v-else viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
            </svg>
            <span>{{ user.role === 'ADMIN' ? '管理员' : '用户' }}</span>
          </div>
        </div>

        <div class="card-body">
          <h3 class="user-name">{{ user.realName || '未设置' }}</h3>
          <p class="user-username">@{{ user.username }}</p>

          <div class="user-details">
            <div class="detail-item">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
              </svg>
              <span>{{ user.phone || '-' }}</span>
            </div>
            <div class="detail-item">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
              </svg>
              <span>{{ user.email || '-' }}</span>
            </div>
            <div class="detail-item">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
              </svg>
              <span>注册于 {{ formatDate(user.createdAt) }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <div class="status-toggle">
            <span class="status-label">账号状态</span>
            <el-switch v-model="user.isActive" @change="updateStatus(user)" />
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredUsers.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <p>没有找到用户</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="total > 10" class="pagination-section">
      <el-pagination
        v-model:current-page="page"
        :total="total"
        :page-size="10"
        layout="prev, pager, next"
        @current-change="fetchUsers"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'
import ViewToggle from '@/components/ViewToggle.vue'

const users = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const searchQuery = ref('')
const activeFilter = ref('all')
const viewMode = ref('list') // 默认列表视图

const filterTabs = [
  { key: 'all', label: '全部', count: 0 },
  { key: 'ADMIN', label: '管理员', count: 0 },
  { key: 'USER', label: '普通用户', count: 0 }
]

const filteredUsers = computed(() => {
  let result = users.value

  // Filter by role
  if (activeFilter.value !== 'all') {
    result = result.filter(u => u.role === activeFilter.value)
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(u =>
      u.username?.toLowerCase().includes(query) ||
      u.realName?.toLowerCase().includes(query) ||
      u.phone?.includes(query)
    )
  }

  return result
})

async function fetchUsers() {
  loading.value = true
  try {
    const res = await request.get('/statistics/users/', { params: { page: page.value, page_size: 50 } })
    users.value = res.data || []
    total.value = res.total || 0

    // Update filter counts
    filterTabs[0].count = users.value.length
    filterTabs[1].count = users.value.filter(u => u.role === 'ADMIN').length
    filterTabs[2].count = users.value.filter(u => u.role === 'USER').length
  } catch (error) {
    console.error(error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

async function updateStatus(user) {
  try {
    await request.put(`/statistics/users/${user.id}/status/`, { is_active: user.isActive })
    ElMessage.success(user.isActive ? '账号已激活' : '账号已禁用')
  } catch (error) {
    ElMessage.error('更新失败')
    user.isActive = !user.isActive
  }
}

function editUser(user) {
  // TODO: 实现用户编辑功能
  ElMessage.info('用户编辑功能待实现')
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(fetchUsers)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.user-manage-page {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 16px;
  color: #1e3a5f;
}

.header-icon svg {
  width: 28px;
  height: 28px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
}

.header-stats {
  display: flex;
  gap: 12px;
}

.stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #f97316;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
}

/* Filters */
.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #9ca3af;
}

.search-input {
  width: 80%;
  padding: 14px 16px 14px 48px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  color: #1f2937;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.search-input:focus {
  outline: none;
  border-color: #fbbf24;
  box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.1);
}

.search-input::placeholder {
  color: #9ca3af;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.filter-tab svg {
  width: 14px;
  height: 14px;
  color: #9ca3af;
}

.filter-tab:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.filter-tab.active {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  border-color: transparent;
  color: white;
}

.filter-tab.active svg {
  color: white;
}

.tab-count {
  font-size: 12px;
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  font-weight: 600;
}

.filter-tab:not(.active) .tab-count {
  background: #f3f4f6;
  color: #6b7280;
}

/* List View */
.list-view-container {
  margin-bottom: 32px;
}

:deep(.users-table) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-family: 'DM Sans', sans-serif;
}

:deep(.users-table th) {
  background: #f9fafb;
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
}

:deep(.users-table tr:hover) {
  background: #fffbeb;
}

:deep(.users-table td) {
  border-color: #f3f4f6;
}

.table-avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  font-size: 16px;
  font-weight: 700;
  border-radius: 10px;
}

.role-tag {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.role-tag.ADMIN {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.role-tag.USER {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.empty-state-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-state-list svg {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-state-list p {
  font-size: 16px;
  color: #9ca3af;
}

/* Card View */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.user-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: #fbbf24;
}

.card-header {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
}

.user-avatar {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  font-size: 24px;
  font-weight: 700;
  border-radius: 14px;
}

.role-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.role-badge.ADMIN {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.role-badge.USER {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.role-badge svg {
  width: 14px;
  height: 14px;
}

.card-body {
  padding: 24px;
}

.user-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.user-username {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 20px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #6b7280;
}

.detail-item svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #9ca3af;
}

.card-footer {
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
}

.status-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: #9ca3af;
}

/* Pagination */
.pagination-section {
  display: flex;
  justify-content: center;
  padding: 24px;
  background: white;
  border-radius: 16px;
}

:deep(.el-pagination) {
  display: flex;
  gap: 8px;
}

:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next),
:deep(.el-pagination .el-pager li) {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.3s ease;
}

:deep(.el-pagination .btn-prev:hover),
:deep(.el-pagination .btn-next:hover),
:deep(.el-pagination .el-pager li:hover) {
  background: #f9fafb;
  border-color: #fbbf24;
  color: #1e3a5f;
}

:deep(.el-pagination .el-pager li.active) {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  border-color: transparent;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .filters-section {
    flex-direction: column;
  }

  .users-grid {
    grid-template-columns: 1fr;
  }
}
</style>
