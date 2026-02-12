<template>
  <div class="attraction-manage-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">景点管理</h1>
          <p class="page-subtitle">管理系统内所有旅游景点信息</p>
        </div>
      </div>
      <router-link to="/admin/attractions/create" class="add-button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>新增景点</span>
      </router-link>
    </div>

    <!-- Filters -->
    <div class="filters-section">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input v-model="searchQuery" placeholder="搜索景点名称、地区..." class="search-input" />
      </div>
      <ViewToggle v-model="viewMode" />
      <div class="category-filter">
        <el-select v-model="selectedCategory" placeholder="全部分类" clearable>
          <el-option label="全部分类" value="" />
          <el-option label="自然风光" value="自然风光" />
          <el-option label="人文古迹" value="人文古迹" />
          <el-option label="主题乐园" value="主题乐园" />
          <el-option label="其他" value="其他" />
        </el-select>
      </div>
    </div>

    <!-- List View -->
    <div v-if="viewMode === 'list'" v-loading="loading" class="list-view-container">
      <el-table :data="filteredAttractions" class="attractions-table">
        <el-table-column label="封面" width="100">
          <template #default="{ row }">
            <img :src="row.cover_image || row.coverImage || '/placeholder.jpg'" class="table-cover" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="景点名称" min-width="200" />
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <span :class="['category-tag', row.category]">
              {{ getCategoryLabel(row.category) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="region" label="地区" min-width="150" />
        <el-table-column prop="level" label="景区等级" width="100">
          <template #default="{ row }">
            <span v-if="row.level" class="level-badge">{{ row.level }}</span>
            <span v-else class="text-gray">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="ranking" label="城市排名" width="100">
          <template #default="{ row }">
            <span v-if="row.ranking">#{{ row.ranking }}</span>
            <span v-else class="text-gray">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="rating_percentage" label="好评率" width="100">
          <template #default="{ row }">
            <span v-if="row.rating_percentage" class="rating-cell">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              {{ (row.rating_percentage * 100).toFixed(0) }}%
            </span>
            <span v-else class="text-gray">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="view_count" label="浏览量" width="100">
          <template #default="{ row }">
            {{ formatNumber(row.view_count || row.viewCount || 0) }}
          </template>
        </el-table-column>
        <el-table-column prop="guide_count" label="攻略数" width="100">
          <template #default="{ row }">
            {{ row.guide_count || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="$router.push(`/admin/attractions/${row.id}/edit`)">编辑</el-button>
            <el-button link type="danger" @click="deleteAttraction(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Empty State for List -->
      <div v-if="filteredAttractions.length === 0" class="empty-state-list">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <polyline points="21 15 16 10 5 21"/>
        </svg>
        <p>暂无景点数据</p>
      </div>
    </div>

    <!-- Card View -->
    <div v-else v-loading="loading" class="attractions-grid">
      <div v-for="attraction in filteredAttractions" :key="attraction.id" class="attraction-card">
        <div class="card-image">
          <img :src="attraction.cover_image || attraction.coverImage || '/placeholder.jpg'" :alt="attraction.name" />
          <div class="image-overlay">
            <div class="overlay-rating" v-if="attraction.rating_percentage">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              <span>{{ (attraction.rating_percentage * 100).toFixed(0) }}%</span>
            </div>
            <div class="category-badge">{{ getCategoryLabel(attraction.category) }}</div>
          </div>
        </div>

        <div class="card-body">
          <h3 class="attraction-name">{{ attraction.name }}</h3>
          <p class="attraction-location">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
            </svg>
            {{ attraction.region }}
          </p>

          <div class="attraction-stats">
            <div class="stat-item">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
              </svg>
              <span>{{ formatNumber(attraction.view_count || attraction.viewCount || 0) }}</span>
            </div>
            <div class="stat-item">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
              </svg>
              <span>{{ attraction.guide_count || 0 }} 攻略</span>
            </div>
            <div class="stat-item" v-if="attraction.level">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span>{{ attraction.level }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <button @click="$router.push(`/admin/attractions/${attraction.id}/edit`)" class="action-button edit">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
            </svg>
            编辑
          </button>
          <button @click="deleteAttraction(attraction)" class="action-button delete">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            删除
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredAttractions.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <polyline points="21 15 16 10 5 21"/>
        </svg>
        <p>暂无景点数据</p>
        <router-link to="/admin/attractions/create" class="add-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          添加第一个景点
        </router-link>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="total > 10" class="pagination-section">
      <el-pagination
        v-model:current-page="page"
        :total="total"
        :page-size="10"
        layout="prev, pager, next"
        @current-change="fetchAttractions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'
import ViewToggle from '@/components/ViewToggle.vue'

const router = useRouter()
const attractions = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const searchQuery = ref('')
const selectedCategory = ref('')
const viewMode = ref('list') // 默认列表视图

const filteredAttractions = computed(() => {
  let result = attractions.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(a =>
      a.name?.toLowerCase().includes(query) ||
      a.region?.toLowerCase().includes(query)
    )
  }

  if (selectedCategory.value) {
    result = result.filter(a => a.category === selectedCategory.value)
  }

  return result
})

async function fetchAttractions() {
  loading.value = true
  try {
    const res = await request.get('/attractions/', { params: { page: page.value, page_size: 50 } })
    attractions.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error(error)
    ElMessage.error('获取景点列表失败')
  } finally {
    loading.value = false
  }
}

async function deleteAttraction(row) {
  try {
    await ElMessageBox.confirm('确定要删除该景点吗？此操作不可恢复。', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await request.delete(`/attractions/${row.id}/`)
    ElMessage.success('删除成功')
    fetchAttractions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function getCategoryLabel(category) {
  // 后端返回中文值，直接返回
  return category
}

function formatNumber(num) {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toLocaleString()
}

onMounted(fetchAttractions)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.attraction-manage-page {
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
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
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

.add-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  color: white;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3);
}

.add-button svg {
  width: 18px;
  height: 18px;
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 58, 95, 0.4);
}

/* Filters */
.filters-section {
  display: flex;
  gap: 16px;
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

.category-filter {
  width: 200px;
}

:deep(.category-filter .el-select__wrapper) {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  padding: 4px 12px;
  transition: all 0.3s ease;
  box-shadow: none !important;
  min-height: 50px;
}

:deep(.category-filter .el-select__wrapper:hover) {
  border-color: #fbbf24;
}

:deep(.category-filter .el-select__wrapper.is-focused) {
  border-color: #fbbf24;
  box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.1) !important;
}

/* List View */
.list-view-container {
  margin-bottom: 32px;
}

:deep(.attractions-table) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  font-family: 'DM Sans', sans-serif;
}

:deep(.attractions-table th) {
  background: #f9fafb;
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
}

:deep(.attractions-table tr:hover) {
  background: #fffbeb;
}

:deep(.attractions-table td) {
  border-color: #f3f4f6;
}

.table-cover {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 8px;
}

.category-tag {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.category-tag.自然风光 {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.category-tag.人文古迹 {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

.category-tag.主题乐园 {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.category-tag.其他 {
  background: rgba(107, 114, 128, 0.15);
  color: #6b7280;
}

.level-badge {
  padding: 2px 8px;
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
  color: #9a3412;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.text-gray {
  color: #9ca3af;
}

.rating-cell {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #fbbf24;
  font-weight: 600;
}

.rating-cell svg {
  width: 14px;
  height: 14px;
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
.attractions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.attraction-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.attraction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: #fbbf24;
}

.card-image {
  position: relative;
  aspect-ratio: 16/10;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.attraction-card:hover .card-image img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6) 0%, transparent 50%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
  gap: 8px;
}

.overlay-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #fbbf24;
  font-weight: 600;
  font-size: 14px;
}

.overlay-rating svg {
  width: 16px;
  height: 16px;
}

.category-badge {
  align-self: flex-start;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #1e3a5f;
}

.card-body {
  padding: 20px;
}

.attraction-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.attraction-location {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 16px;
}

.attraction-location svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.attraction-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #9ca3af;
}

.stat-item svg {
  width: 16px;
  height: 16px;
}

.card-footer {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  border-top: 1px solid #f3f4f6;
}

.action-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-button svg {
  width: 16px;
  height: 16px;
}

.action-button.edit {
  background: #f0f4f8;
  color: #1e3a5f;
}

.action-button.edit:hover {
  background: #e2e8f0;
}

.action-button.delete {
  background: #fee2e2;
  color: #ef4444;
}

.action-button.delete:hover {
  background: #fecaca;
}

/* Empty State */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
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
  margin-bottom: 24px;
}

.add-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.add-link svg {
  width: 18px;
  height: 18px;
}

.add-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(251, 191, 36, 0.4);
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

  .add-button {
    width: 100%;
    justify-content: center;
  }

  .filters-section {
    flex-direction: column;
  }

  .category-filter {
    width: 100%;
  }

  .attractions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
