<template>
  <div class="inheritor-list-page">
    <!-- 墨韵背景 -->
    <div class="ink-background">
      <div class="ink-cloud cloud-1"></div>
      <div class="ink-cloud cloud-2"></div>
      <div class="floating-spots">
        <div v-for="i in 10" :key="i" class="ink-spot" :style="{ '--delay': `${i * 2.5}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
      </div>
    </div>

    <!-- 页面头部 -->
    <header class="page-header">
      <div class="scroll-mount left"></div>
      <div class="header-center">
        <div class="header-decoration">
          <div class="decoration-line"></div>
          <div class="seal-group">
            <div class="main-seal">
              <div class="seal-frame">
                <div class="seal-inner">
                  <span class="seal-text-vertical">传承</span>
                </div>
              </div>
            </div>
          </div>
          <div class="decoration-line"></div>
        </div>
        <div class="header-texts">
          <h1 class="page-title">传承人库</h1>
          <p class="page-subtitle">记录非遗文化的守护者与传播者</p>
        </div>
      </div>
      <div class="scroll-mount right"></div>
    </header>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="scroll-top"></div>
      <div class="filter-content">
        <el-form :model="filters" class="filter-form" @submit.prevent="handleSearch">
          <div class="filter-grid">
            <div class="filter-item">
              <label class="filter-label">
                <span class="label-icon">👤</span>
                姓名
              </label>
              <el-input
                v-model="filters.name"
                placeholder="搜索传承人姓名"
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

            <div class="filter-item">
              <label class="filter-label">
                <span class="label-icon">📜</span>
                所属项目
              </label>
              <el-select
                v-model="filters.heritage_item"
                placeholder="选择项目"
                clearable
                filterable
                @change="handleSearch"
                class="heritage-select"
              >
                <el-option
                  v-for="item in heritageItems"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </div>
          </div>
        </el-form>
      </div>
      <div class="scroll-bottom"></div>
    </div>

    <!-- 表格区域 -->
    <div class="table-section">
      <div class="table-frame">
        <div class="frame-corner top-left"></div>
        <div class="frame-corner top-right"></div>
        <div class="frame-corner bottom-left"></div>
        <div class="frame-corner bottom-right"></div>

        <el-table
          v-loading="loading"
          :data="inheritorList"
          class="inheritor-table"
          :row-class-name="getRowClassName"
        >
          <el-table-column prop="name" label="姓名" width="180">
            <template #default="{ row }">
              <div class="name-cell">
                <div class="avatar-circle">
                  <span class="avatar-text">{{ row.name.charAt(0) }}</span>
                  <div class="avatar-glow"></div>
                </div>
                <span class="name-text">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="gender" label="性别" width="90">
            <template #default="{ row }">
              <span v-if="row.gender" class="gender-badge" :class="row.gender">
                {{ getGenderText(row.gender) }}
              </span>
              <span v-else class="empty-text">—</span>
            </template>
          </el-table-column>

          <el-table-column prop="heritage_item.name" label="所属项目" min-width="240">
            <template #default="{ row }">
              <a class="heritage-link" @click="handleViewHeritage(row.heritage_item.id)">
                <span class="link-icon">📜</span>
                <span>{{ row.heritage_item.name }}</span>
                <span class="link-arrow">→</span>
              </a>
            </template>
          </el-table-column>

          <el-table-column prop="level" label="级别" width="130">
            <template #default="{ row }">
              <span v-if="row.level" class="level-badge" :class="getLevelClass(row.level)">
                {{ getLevelText(row.level) }}
              </span>
              <span v-else class="empty-text">—</span>
            </template>
          </el-table-column>

          <el-table-column prop="region.country_name" label="国家" width="150" />

          <el-table-column prop="area" label="地区" width="170">
            <template #default="{ row }">
              <span v-if="row.area">{{ row.area }}</span>
              <span v-else class="empty-text">—</span>
            </template>
          </el-table-column>

          <el-table-column prop="description" label="简介" min-width="220">
            <template #default="{ row }">
              <span v-if="row.description" class="description-text">{{ row.description }}</span>
              <span v-else class="empty-text">—</span>
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
import { getInheritorList } from '@/api/inheritor'
import { getHeritageList } from '@/api/heritage'
import { getRegionList } from '@/api/region'
import type { Inheritor, HeritageItem, Region } from '@/types'

const router = useRouter()

// Data
const loading = ref(false)
const inheritorList = ref<Inheritor[]>([])
const heritageItems = ref<HeritageItem[]>([])
const regions = ref<Region[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// Filters
const filters = ref({
  name: '',
  level: '',
  region: undefined as number | undefined,
  heritage_item: undefined as number | undefined
})

// Methods
const fetchInheritorList = async () => {
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

    const response = await getInheritorList(params)
    if (response.data.code === 0) {
      inheritorList.value = response.data.data
      total.value = response.data.total || 0
    }
  } catch (error) {
    ElMessage.error('获取传承人列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchHeritageItems = async () => {
  try {
    const response = await getHeritageList({ page: 1 })
    if (response.data.code === 0) {
      heritageItems.value = response.data.data
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
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
  fetchInheritorList()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchInheritorList()
}

const handleViewHeritage = (id: number) => {
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

const getGenderText = (gender: string) => {
  const genderMap: Record<string, string> = {
    male: '男',
    female: '女',
    other: '其他'
  }
  return genderMap[gender] || gender
}

const getRowClassName = ({ rowIndex }: { rowIndex: number }) => {
  return `table-row-${rowIndex % 2}`
}

// Lifecycle
onMounted(() => {
  fetchHeritageItems()
  fetchRegions()
  fetchInheritorList()
})
</script>

<style scoped>
/* ========== 全局样式 ========== */
.inheritor-list-page {
  padding: 32px;
  min-height: 100%;
  background: #F7F4ED;
  position: relative;
}

/* ========== 墨韵背景 ========== */
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

.ink-cloud {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.06;
  animation: cloudDrift 60s ease-in-out infinite;
}

.ink-cloud.cloud-1 {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle at center, #2F3640 0%, transparent 70%);
  top: -250px;
  right: -250px;
}

.ink-cloud.cloud-2 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle at center, #5D8AA8 0%, transparent 70%);
  bottom: -200px;
  left: -200px;
  animation-delay: -30s;
}

@keyframes cloudDrift {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(70px, -60px) scale(1.08);
  }
  66% {
    transform: translate(-60px, 70px) scale(0.92);
  }
}

.floating-spots {
  position: absolute;
  width: 100%;
  height: 100%;
}

.ink-spot {
  position: absolute;
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, rgba(93, 138, 168, 0.4) 0%, transparent 70%);
  border-radius: 50%;
  left: var(--x);
  top: var(--y);
  animation: spotFloat 35s ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes spotFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.2;
  }
  50% {
    transform: translate(100px, -120px) scale(2.5);
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
  background: linear-gradient(135deg, #2F3640 0%, #1a2026 100%);
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(47, 54, 64, 0.35);
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M40 40c0-22.091-17.909-40-40-40S0 17.909 0 40s17.909 40 40 40 40-17.909 40-40S62.091 0 40 0z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
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
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.6), transparent);
}

.seal-group {
  flex-shrink: 0;
}

.main-seal {
  position: relative;
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
  animation: sealPulse 5s ease-in-out infinite;
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
  color: #F7F4ED;
  margin: 0 0 10px 0;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
  text-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);
}

.page-subtitle {
  font-size: 14px;
  color: rgba(247, 244, 237, 0.75);
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

.scroll-top,
.scroll-bottom {
  height: 14px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(212, 175, 55, 0.5) 20%,
    rgba(212, 175, 55, 0.8) 50%,
    rgba(212, 175, 55, 0.5) 80%,
    transparent 100%
  );
}

.scroll-bottom {
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(212, 175, 55, 0.5) 20%,
    rgba(212, 175, 55, 0.8) 50%,
    rgba(212, 175, 55, 0.5) 80%,
    transparent 100%
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
  border-color: #2F3640;
  box-shadow: 0 0 0 4px rgba(47, 54, 64, 0.12);
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
  background: linear-gradient(90deg, transparent, #2F3640, transparent);
}

.frame-corner {
  position: absolute;
  width: 28px;
  height: 28px;
  border: 2px solid #2F3640;
  opacity: 0.35;
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

.inheritor-table {
  margin-bottom: 24px;
}

:deep(.inheritor-table th) {
  background: #F7F4ED !important;
  color: #2F3640 !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.5px !important;
}

:deep(.inheritor-table td) {
  padding: 16px 0 !important;
}

:deep(.inheritor-table .el-table__row:hover) {
  background: rgba(47, 54, 64, 0.04) !important;
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar-circle {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #D4AF37, #CD7F32);
  border-radius: 50%;
  position: relative;
  flex-shrink: 0;
}

.avatar-text {
  color: #2F3640;
  font-size: 18px;
  font-weight: 700;
  font-family: "STSong", "SimSun", serif;
  position: relative;
  z-index: 1;
}

.avatar-glow {
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  background: transparent;
  border: 2px solid rgba(212, 175, 55, 0.3);
  animation: glowRipple 3s ease-in-out infinite;
}

@keyframes glowRipple {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.name-text {
  font-weight: 500;
  color: #2F3640;
  font-size: 15px;
}

.gender-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
}

.gender-badge.male {
  background: rgba(93, 138, 168, 0.15);
  color: #5D8AA8;
}

.gender-badge.female {
  background: rgba(194, 35, 49, 0.12);
  color: #C23531;
}

.gender-badge.other {
  background: rgba(149, 165, 166, 0.15);
  color: #95A5A6;
}

.heritage-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #2F3640;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  padding: 6px 12px;
  border-radius: 8px;
}

.heritage-link:hover {
  color: #2F3640;
  background: rgba(47, 54, 64, 0.06);
}

.link-icon {
  font-size: 14px;
}

.link-arrow {
  transition: transform 0.3s;
}

.heritage-link:hover .link-arrow {
  transform: translateX(4px);
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

.description-text {
  color: #606266;
  line-height: 1.7;
  font-size: 14px;
}

.empty-text {
  color: #C0C4CC;
  font-style: italic;
  font-size: 14px;
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
  background: #2F3640 !important;
  border-color: #2F3640 !important;
  font-weight: 600 !important;
}

:deep(.el-pagination button:hover) {
  color: #2F3640 !important;
}

:deep(.el-pagination .el-pager li:hover) {
  color: #2F3640 !important;
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .filter-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .inheritor-list-page {
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
