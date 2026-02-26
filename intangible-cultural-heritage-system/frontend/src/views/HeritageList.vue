<template>
  <div class="heritage-list-page">
    <!-- 水墨晕染背景 -->
    <div class="ink-background">
      <div class="ink-spot spot-1"></div>
      <div class="ink-spot spot-2"></div>
      <div class="floating-ink">
        <div v-for="i in 8" :key="i" class="ink-particle" :style="{ '--delay': `${i * 2}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
      </div>
    </div>

    <!-- 页面头部 - 卷轴式 -->
    <header class="page-header">
      <div class="scroll-mount left"></div>
      <div class="header-center">
        <div class="header-decoration">
          <div class="decoration-line"></div>
          <div class="header-seal">
            <div class="seal-frame">
              <div class="seal-inner">
                <span class="seal-text-vertical">宝库</span>
              </div>
            </div>
          </div>
          <div class="decoration-line"></div>
        </div>
        <div class="header-texts">
          <h1 class="page-title">非遗项目库</h1>
          <p class="page-subtitle">探索世界各地的非物质文化遗产</p>
        </div>
      </div>
      <div class="scroll-mount right"></div>
    </header>

    <!-- 筛选区域 - 书卷式 -->
    <div class="filter-section">
      <div class="scroll-decoration">
        <div class="scroll-pattern"></div>
      </div>
      <div class="filter-content">
        <el-form :model="filters" class="filter-form" @submit.prevent="handleSearch">
          <div class="filter-grid">
            <div class="filter-item">
              <label class="filter-label">
                <span class="label-icon">🔍</span>
                关键词
              </label>
              <el-input
                v-model="filters.name"
                placeholder="搜索项目名称"
                clearable
                @clear="handleSearch"
                class="heritage-input"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>

            <div class="filter-item">
              <label class="filter-label">
                <span class="label-icon">📂</span>
                分类
              </label>
              <el-select
                v-model="filters.category"
                placeholder="选择分类"
                clearable
                @change="handleSearch"
                class="heritage-select"
              >
                <el-option
                  v-for="cat in categories"
                  :key="cat.id"
                  :label="cat.name"
                  :value="cat.id"
                />
              </el-select>
            </div>

            <div class="filter-item">
              <label class="filter-label">
                <span class="label-icon">🏅</span>
                级别
              </label>
              <el-select
                v-model="filters.level"
                placeholder="选择级别"
                clearable
                @change="handleSearch"
                class="heritage-select"
              >
                <el-option label="国家级" value="national" />
                <el-option label="省级" value="provincial" />
                <el-option label="市县级" value="city_county" />
              </el-select>
            </div>

            <div class="filter-item">
              <label class="filter-label">
                <span class="label-icon">🌍</span>
                国家
              </label>
              <el-select
                v-model="filters.region"
                placeholder="选择国家"
                clearable
                filterable
                @change="handleSearch"
                class="heritage-select"
              >
                <el-option
                  v-for="reg in regions"
                  :key="reg.id"
                  :label="reg.country_name"
                  :value="reg.id"
                />
              </el-select>
            </div>
          </div>
        </el-form>
      </div>
    </div>

    <!-- 表格区域 - 宣纸式 -->
    <div class="table-section">
      <div class="table-frame">
        <div class="frame-corner top-left"></div>
        <div class="frame-corner top-right"></div>
        <div class="frame-corner bottom-left"></div>
        <div class="frame-corner bottom-right"></div>

        <el-table
          v-loading="loading"
          :data="heritageList"
          class="heritage-table"
          @row-click="handleRowClick"
          :row-class-name="getRowClassName"
        >
          <el-table-column prop="name" label="项目名称" min-width="240">
            <template #default="{ row, $index }">
              <div class="name-cell" :style="{ '--delay': `${$index * 0.05}s` }">
                <span class="name-seal" :class="getLevelSealClass(row.level)">
                  {{ getLevelSeal(row.level) }}
                </span>
                <span class="name-text">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="category.name" label="分类" width="150">
            <template #default="{ row }">
              <span class="category-tag">{{ row.category.name }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="level" label="级别" width="130">
            <template #default="{ row }">
              <span class="level-badge" :class="getLevelClass(row.level)">
                {{ getLevelText(row.level) }}
              </span>
            </template>
          </el-table-column>

          <el-table-column prop="region.country_name" label="国家" width="150" />

          <el-table-column prop="area" label="地区" width="160" show-overflow-tooltip />

          <el-table-column prop="protection_unit" label="保护单位" min-width="200" show-overflow-tooltip />

          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <button class="action-btn detail-btn" @click.stop="handleViewDetail(row.id)">
                <span>查看</span>
                <span class="btn-arrow">→</span>
              </button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-section">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="total"
            layout="total, prev, pager, next, jumper"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getHeritageList } from '@/api/heritage'
import { getCategoryList } from '@/api/category'
import { getRegionList } from '@/api/region'
import type { HeritageItem, Category, Region } from '@/types'

const router = useRouter()

// Data
const loading = ref(false)
const heritageList = ref<HeritageItem[]>([])
const categories = ref<Category[]>([])
const regions = ref<Region[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// Filters
const filters = ref({
  name: '',
  category: undefined as number | undefined,
  level: '',
  region: undefined as number | undefined
})

// Methods
const fetchHeritageList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      ...filters.value
    }

    Object.keys(params).forEach(key => {
      if (params[key as keyof typeof params] === '' || params[key as keyof typeof params] === undefined) {
        delete params[key as keyof typeof params]
      }
    })

    const response = await getHeritageList(params)
    if (response.data.code === 0) {
      heritageList.value = response.data.data
      total.value = response.data.total || 0
    }
  } catch (error) {
    ElMessage.error('获取项目列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await getCategoryList({ page: 1 })
    if (response.data.code === 0) {
      categories.value = response.data.data
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

const fetchRegions = async () => {
  try {
    const response = await getRegionList({ page: 1 })
    if (response.data.code === 0) {
      regions.value = response.data.data
    }
  } catch (error) {
    console.error('获取地区列表失败:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchHeritageList()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchHeritageList()
}

const handleRowClick = (row: HeritageItem) => {
  handleViewDetail(row.id)
}

const handleViewDetail = (id: number) => {
  router.push({ name: 'HeritageDetail', params: { id } })
}

const getLevelText = (level: string) => {
  const levelMap: Record<string, string> = {
    national: '国家级',
    provincial: '省级',
    city_county: '市县级'
  }
  return levelMap[level] || level
}

const getLevelClass = (level: string) => {
  return `level-${level}`
}

const getLevelSeal = (level: string) => {
  const sealMap: Record<string, string> = {
    national: '国',
    provincial: '省',
    city_county: '市'
  }
  return sealMap[level] || ''
}

const getLevelSealClass = (level: string) => {
  return `seal-${level}`
}

const getRowClassName = ({ rowIndex }: { rowIndex: number }) => {
  return `table-row-${rowIndex % 2}`
}

// Lifecycle
onMounted(() => {
  fetchCategories()
  fetchRegions()
  fetchHeritageList()
})
</script>

<style scoped>
/* ========== 全局样式 ========== */
.heritage-list-page {
  padding: 32px;
  min-height: 100%;
  background: #F7F4ED;
  position: relative;
}

/* ========== 水墨晕染背景 ========== */
.ink-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.ink-spot {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.06;
  animation: inkDrift 50s ease-in-out infinite;
}

.ink-spot.spot-1 {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle at center, #C23531 0%, transparent 70%);
  top: -200px;
  right: -200px;
}

.ink-spot.spot-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle at center, #D4AF37 0%, transparent 70%);
  bottom: -150px;
  left: -150px;
  animation-delay: -20s;
}

@keyframes inkDrift {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(50px, -40px) scale(1.05);
  }
  66% {
    transform: translate(-40px, 50px) scale(0.95);
  }
}

.floating-ink {
  position: absolute;
  width: 100%;
  height: 100%;
}

.ink-particle {
  position: absolute;
  width: 6px;
  height: 6px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.4) 0%, transparent 70%);
  border-radius: 50%;
  left: var(--x);
  top: var(--y);
  animation: particleFloat 25s ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes particleFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.2;
  }
  50% {
    transform: translate(60px, -80px) scale(2);
    opacity: 0.6;
  }
}

/* ========== 页面头部 ========== */
.page-header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: stretch;
  margin-bottom: 32px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(194, 35, 49, 0.35);
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.4;
}

.scroll-mount {
  width: 28px;
  background: linear-gradient(180deg,
    #D4AF37 0%,
    #B8860B 15%,
    #8B6914 30%,
    #B8860B 50%,
    #D4AF37 70%,
    #B8860B 85%,
    #8B6914 100%
  );
  position: relative;
  flex-shrink: 0;
}

.scroll-mount::before {
  content: '';
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 85%;
  background: repeating-linear-gradient(
    180deg,
    transparent 0px,
    transparent 10px,
    rgba(0, 0, 0, 0.2) 10px,
    rgba(0, 0, 0, 0.2) 12px
  );
  border-radius: 2px;
}

.header-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 36px 48px;
}

.header-decoration {
  display: flex;
  align-items: center;
  gap: 28px;
  margin-bottom: 20px;
}

.decoration-line {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.7), transparent);
}

.header-seal {
  flex-shrink: 0;
}

.seal-frame {
  width: 80px;
  height: 80px;
  background: #D4AF37;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 8px 24px rgba(212, 175, 55, 0.5),
    inset 0 2px 0 rgba(255, 255, 255, 0.3);
  animation: sealPulse 4s ease-in-out infinite;
}

@keyframes sealPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.seal-frame::before {
  content: '';
  position: absolute;
  top: 5px;
  left: 5px;
  right: 5px;
  bottom: 5px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 4px;
}

.seal-inner {
  width: 68px;
  height: 68px;
  background: rgba(212, 175, 55, 0.9);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.seal-text-vertical {
  writing-mode: vertical-rl;
  color: #2F3640;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
}

.header-texts {
  text-align: center;
}

.page-title {
  font-size: 38px;
  font-weight: 700;
  color: white;
  margin: 0 0 10px 0;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
  text-shadow: 0 3px 12px rgba(0, 0, 0, 0.25);
}

.page-subtitle {
  font-size: 14px;
  color: rgba(247, 244, 237, 0.9);
  margin: 0;
  letter-spacing: 3px;
}

/* ========== 筛选区域 ========== */
.filter-section {
  position: relative;
  z-index: 1;
  margin-bottom: 28px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(47, 54, 64, 0.1);
  overflow: hidden;
}

.scroll-decoration {
  height: 12px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(212, 175, 55, 0.4) 20%,
    rgba(212, 175, 55, 0.7) 50%,
    rgba(212, 175, 55, 0.4) 80%,
    transparent 100%
  );
}

.scroll-pattern {
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    90deg,
    transparent 0px,
    transparent 20px,
    rgba(0, 0, 0, 0.05) 20px,
    rgba(0, 0, 0, 0.05) 22px
  );
}

.filter-content {
  padding: 28px 32px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 28px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  letter-spacing: 1px;
}

.label-icon {
  font-size: 14px;
}

:deep(.heritage-input .el-input__wrapper),
:deep(.heritage-select .el-select__wrapper) {
  background: #F7F4ED;
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 10px;
  box-shadow: none;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.heritage-input .el-input__wrapper:hover),
:deep(.heritage-select .el-select__wrapper:hover) {
  border-color: #D4AF37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.1);
}

:deep(.heritage-input .el-input__wrapper.is-focus),
:deep(.heritage-select .el-select__wrapper.is-focus) {
  border-color: #C23531;
  box-shadow: 0 0 0 4px rgba(194, 35, 49, 0.15);
}

/* ========== 表格区域 ========== */
.table-section {
  position: relative;
  z-index: 1;
}

.table-frame {
  position: relative;
  background: white;
  padding: 28px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(47, 54, 64, 0.1);
  overflow: hidden;
}

.table-frame::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #D4AF37, transparent);
}

.frame-corner {
  position: absolute;
  width: 28px;
  height: 28px;
  border: 2px solid #D4AF37;
  opacity: 0.4;
}

.frame-corner.top-left {
  top: 14px;
  left: 14px;
  border-right: none;
  border-bottom: none;
}

.frame-corner.top-right {
  top: 14px;
  right: 14px;
  border-left: none;
  border-bottom: none;
}

.frame-corner.bottom-left {
  bottom: 14px;
  left: 14px;
  border-right: none;
  border-top: none;
}

.frame-corner.bottom-right {
  bottom: 14px;
  right: 14px;
  border-left: none;
  border-top: none;
}

.heritage-table {
  margin-bottom: 24px;
}

:deep(.heritage-table .el-table__row) {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.heritage-table .el-table__row:hover) {
  background: rgba(212, 175, 55, 0.06) !important;
  transform: scale(1.005);
}

:deep(.heritage-table .el-table__row:hover .name-text) {
  color: #C23531;
  font-weight: 600;
}

:deep(.heritage-table th) {
  background: #F7F4ED !important;
  color: #2F3640 !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.5px !important;
}

:deep(.heritage-table td) {
  padding: 16px 0 !important;
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.name-seal {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  border-radius: 4px;
  font-family: "STSong", "SimSun", serif;
  flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
}

.name-seal.seal-national {
  background: #C23531;
  color: white;
}

.name-seal.seal-provincial {
  background: #D4AF37;
  color: #2F3640;
}

.name-seal.seal-city_county {
  background: #5D8AA8;
  color: white;
}

.name-text {
  font-weight: 500;
  color: #2F3640;
  transition: all 0.3s;
}

.category-tag {
  display: inline-block;
  padding: 6px 14px;
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid rgba(212, 175, 55, 0.2);
}

.level-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
}

.level-badge.level-national {
  background: rgba(194, 35, 49, 0.12);
  color: #C23531;
  border: 1px solid rgba(194, 35, 49, 0.2);
}

.level-badge.level-provincial {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  border: 1px solid rgba(212, 175, 55, 0.3);
}

.level-badge.level-city_county {
  background: rgba(93, 138, 168, 0.15);
  color: #5D8AA8;
  border: 1px solid rgba(93, 138, 168, 0.3);
}

.action-btn {
  padding: 8px 18px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 6px;
}

.detail-btn {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
  border: 1px solid rgba(194, 35, 49, 0.2);
}

.detail-btn:hover {
  background: #C23531;
  color: white;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(194, 35, 49, 0.35);
}

.btn-arrow {
  transition: transform 0.35s;
}

.detail-btn:hover .btn-arrow {
  transform: translateX(4px);
}

/* ========== 分页 ========== */
.pagination-section {
  display: flex;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, rgba(247, 244, 237, 0.6) 0%, rgba(247, 244, 237, 0.3) 100%);
  border-radius: 10px;
}

:deep(.el-pagination .el-pager li.is-active) {
  background: #C23531 !important;
  border-color: #C23531 !important;
  font-weight: 600 !important;
}

:deep(.el-pagination button:hover) {
  color: #C23531 !important;
}

:deep(.el-pagination .el-pager li:hover) {
  color: #C23531 !important;
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .filter-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .heritage-list-page {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
  }

  .scroll-mount {
    display: none;
  }

  .header-center {
    padding: 28px 24px;
  }

  .header-decoration {
    gap: 16px;
  }

  .decoration-line {
    width: 50px;
  }

  .page-title {
    font-size: 28px;
    letter-spacing: 4px;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .table-frame {
    padding: 16px;
    overflow-x: auto;
  }

  .frame-corner {
    display: none;
  }
}
</style>
