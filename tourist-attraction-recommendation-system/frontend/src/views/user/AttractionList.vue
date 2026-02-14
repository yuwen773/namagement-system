<template>
  <div class="attraction-list-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">探索精彩世界</h1>
        <p class="hero-subtitle">发现值得奔赴的每一处风景</p>
      </div>
      <div class="hero-decoration"></div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-container">
      <div class="filter-card">
        <div class="filter-row">
          <div class="filter-group">
            <label class="filter-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/>
              </svg>
              景点类别
            </label>
            <el-select v-model="filters.category" placeholder="选择类别" clearable class="filter-select">
              <el-option label="自然风光" value="NATURE">
                <span class="option-icon">🏔️</span> 自然风光
              </el-option>
              <el-option label="人文古迹" value="HISTORY">
                <span class="option-icon">🏛️</span> 人文古迹
              </el-option>
              <el-option label="主题乐园" value="THEME">
                <span class="option-icon">🎢</span> 主题乐园
              </el-option>
              <el-option label="其他" value="OTHER">
                <span class="option-icon">✨</span> 其他
              </el-option>
            </el-select>
          </div>

          <div class="filter-group">
            <label class="filter-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="10" r="3"/>
                <path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 7 8 11.7z"/>
              </svg>
              地区
            </label>
            <el-select v-model="filters.region" placeholder="选择地区" clearable class="filter-select">
              <el-option label="朝阳区" value="chaoyang" />
              <el-option label="海淀区" value="haidian" />
              <el-option label="东城区" value="dongcheng" />
              <el-option label="西城区" value="xicheng" />
            </el-select>
          </div>

          <div class="filter-group filter-group-search">
            <label class="filter-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
              搜索景点
            </label>
            <div class="search-input-wrapper">
              <el-input
                v-model="filters.keyword"
                placeholder="输入景点名称..."
                class="search-input"
                @keyup.enter="fetchAttractions"
              >
                <template #prefix>
                  <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="m21 21-4.35-4.35"/>
                  </svg>
                </template>
              </el-input>
              <button class="search-btn" @click="fetchAttractions">
                <span>查询</span>
                <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Header -->
    <div class="results-header">
      <p class="results-count">
        找到 <span class="count-number">{{ pagination.total }}</span> 个景点
      </p>
      <div class="view-toggle">
        <button
          :class="['view-btn', { active: viewMode === 'grid' }]"
          @click="viewMode = 'grid'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
        </button>
        <button
          :class="['view-btn', { active: viewMode === 'list' }]"
          @click="viewMode = 'list'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"/>
            <line x1="8" y1="12" x2="21" y2="12"/>
            <line x1="8" y1="18" x2="21" y2="18"/>
            <circle cx="4" cy="6" r="1"/>
            <circle cx="4" cy="12" r="1"/>
            <circle cx="4" cy="18" r="1"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Attractions Grid -->
    <div v-if="!loading && attractions.length > 0" :class="['attractions-grid', `view-${viewMode}`]">
      <div
        v-for="(item, index) in attractions"
        :key="item.id"
        :class="['attraction-card', `stagger-${index % 4}`]"
        :style="{ animationDelay: `${index * 0.08}s` }"
        @click="goToDetail(item.id)"
      >
        <div class="card-image-wrapper">
          <el-image :src="item.cover_image" fit="cover" class="card-image" lazy>
            <template #error>
              <div class="image-slot">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <circle cx="8.5" cy="8.5" r="1.5"></circle>
                  <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
              </div>
            </template>
          </el-image>
          <div class="card-overlay">
            <div class="card-badge">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
              {{ item.rating_percentage ? (item.rating_percentage * 100).toFixed(0) + '%' : '4.5' }}
            </div>
            <!-- Removed price display as it's not in the data model -->
          </div>
          <div class="card-category-tag">
            {{ getCategoryLabel(item.category) }}
          </div>
        </div>

        <div class="card-content">
          <h3 class="card-title">{{ item.name }}</h3>

          <div class="card-location">
            <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            <span>{{ item.address || item.region }}</span>
          </div>

          <div class="card-meta">
            <div class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              {{ formatNumber(item.view_count || 0) }}
            </div>
            <div class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              {{ item.comment_count || 0 }}
            </div>
          </div>

          <div class="card-action">
            <span class="action-text">查看详情</span>
            <svg class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在加载精彩景点...</p>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && attractions.length === 0" class="empty-state">
      <div class="empty-illustration">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
          <path d="M2 12h20"/>
        </svg>
      </div>
      <h3>没有找到相关景点</h3>
      <p>试试调整筛选条件，发现更多精彩</p>
      <button class="reset-btn" @click="resetFilters">重置筛选</button>
    </div>

    <!-- Pagination -->
    <div v-if="attractions.length > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :page-sizes="[6, 12, 18, 24]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchAttractions"
        @current-change="fetchAttractions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/api/request'

const router = useRouter()

const attractions = ref([])
const loading = ref(false)
const viewMode = ref('grid')

const filters = reactive({
  category: '',
  region: '',
  keyword: ''
})

const pagination = reactive({
  page: 1,
  size: 12,
  total: 0
})

const categoryMap = {
  'NATURE': '自然风光',
  'HISTORY': '人文古迹',
  'THEME': '主题乐园',
  'OTHER': '其他'
}

function getCategoryLabel(value) {
  return categoryMap[value] || value
}

function formatNumber(num) {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

function goToDetail(id) {
  router.push(`/attractions/${id}`)
}

function resetFilters() {
  filters.category = ''
  filters.region = ''
  filters.keyword = ''
  pagination.page = 1
  fetchAttractions()
}

async function fetchAttractions() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...(filters.category && { category: filters.category }),
      ...(filters.region && { region: filters.region }),
      ...(filters.keyword && { keyword: filters.keyword })
    }
    const res = await request.get('/attractions/', { params })
    attractions.value = res.data || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error('Failed to fetch attractions:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchAttractions)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.attraction-list-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  padding-bottom: 60px;
}

/* Hero Section */
.hero-section {
  position: relative;
  padding: 60px 0 40px;
  text-align: center;
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 600px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 3rem;
  font-weight: 700;
  color: #1e3a5f;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 400;
}

.hero-decoration {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 300px;
  background: radial-gradient(ellipse at center, rgba(30, 58, 95, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

/* Filter Container */
.filter-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  margin-bottom: 32px;
}

.filter-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(30, 58, 95, 0.08);
}

.filter-row {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  flex: 1;
  min-width: 180px;
}

.filter-group-search {
  flex: 2;
  min-width: 280px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.label-icon {
  width: 16px;
  height: 16px;
  color: #f59e0b;
}

.filter-select {
  width: 100%;
}

.filter-select :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  box-shadow: none;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

.filter-select :deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
}

.filter-select :deep(.el-input__wrapper.is-focus) {
  border-color: #1e3a5f;
  box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.1);
}

.filter-select :deep(.el-input__inner) {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
}

.option-icon {
  margin-right: 8px;
  font-size: 1rem;
}

/* Search Input */
.search-input-wrapper {
  display: flex;
  gap: 12px;
}

.search-input {
  flex: 1;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  box-shadow: none;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

.search-input :deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #1e3a5f;
  box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.1);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #94a3b8;
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(30, 58, 95, 0.25);
}

.btn-arrow {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.search-btn:hover .btn-arrow {
  transform: translateX(4px);
}

/* Results Header */
.results-header {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.results-count {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  font-size: 0.95rem;
}

.count-number {
  font-weight: 700;
  color: #1e3a5f;
  font-size: 1.1rem;
}

.view-toggle {
  display: flex;
  gap: 8px;
  background: white;
  padding: 4px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(30, 58, 95, 0.06);
}

.view-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.view-btn svg {
  width: 18px;
  height: 18px;
}

.view-btn:hover {
  background: #f8fafc;
  color: #64748b;
}

.view-btn.active {
  background: #1e3a5f;
  color: white;
}

/* Attractions Grid */
.attractions-grid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  gap: 24px;
  animation: fadeInUp 0.6s ease;
}

.attractions-grid.view-grid {
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}

.attractions-grid.view-list {
  grid-template-columns: 1fr;
}

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

/* Attraction Card */
.attraction-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(30, 58, 95, 0.08);
}

.attraction-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(30, 58, 95, 0.15);
}

.card-image-wrapper {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  transition: transform 0.6s ease;
}

.attraction-card:hover .card-image {
  transform: scale(1.08);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(30, 58, 95, 0.1) 0%, rgba(30, 58, 95, 0.5) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.attraction-card:hover .card-overlay {
  opacity: 1;
}

.card-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  color: #1e3a5f;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-badge svg {
  width: 14px;
  height: 14px;
  color: #f59e0b;
}

.card-price {
  position: absolute;
  bottom: 16px;
  left: 16px;
  padding: 8px 16px;
  background: rgba(30, 58, 95, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-category-tag {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 12px;
  background: rgba(245, 158, 11, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.75rem;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-content {
  padding: 20px;
}

.card-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 12px;
  line-height: 1.4;
}

.card-location {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 16px;
}

.location-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #f59e0b;
}

.card-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 500;
}

.meta-item svg {
  width: 16px;
  height: 16px;
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.action-text {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #1e3a5f;
  font-size: 0.9rem;
}

.action-icon {
  width: 18px;
  height: 18px;
  color: #f59e0b;
  transition: transform 0.3s ease;
}

.attraction-card:hover .action-icon {
  transform: translateX(4px);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 20px;
  border: 4px solid #e2e8f0;
  border-top-color: #1e3a5f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  font-size: 1rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-illustration {
  margin-bottom: 24px;
}

.empty-illustration svg {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  color: #cbd5e1;
}

.empty-state h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  color: #1e3a5f;
  margin-bottom: 8px;
}

.empty-state p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  margin-bottom: 24px;
}

.reset-btn {
  padding: 12px 28px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(30, 58, 95, 0.25);
}

/* Pagination */
.pagination-container {
  max-width: 1200px;
  margin: 48px auto 0;
  padding: 0 20px;
  display: flex;
  justify-content: center;
}

.pagination-container :deep(.el-pagination) {
  font-family: 'DM Sans', sans-serif;
}

.pagination-container :deep(.el-pagination.is-background .el-pager li) {
  border-radius: 8px;
}

.pagination-container :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 0.95rem;
  }

  .filter-row {
    flex-direction: column;
  }

  .filter-group,
  .filter-group-search {
    width: 100%;
    min-width: 0;
  }

  .search-input-wrapper {
    flex-direction: column;
  }

  .search-btn {
    width: 100%;
  }

  .attractions-grid.view-grid {
    grid-template-columns: 1fr;
  }

  .results-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 40px 0 24px;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .filter-card {
    padding: 16px;
  }

  .card-content {
    padding: 16px;
  }

  .card-title {
    font-size: 1.1rem;
  }
}
</style>
