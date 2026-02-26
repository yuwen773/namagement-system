<template>
  <div class="inheritor-list-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">传承人库</h1>
        <p class="page-subtitle">记录非遗文化的守护者与传播者</p>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <el-form :model="filters" class="filter-form" @submit.prevent="handleSearch">
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="姓名">
              <el-input
                v-model="filters.name"
                placeholder="搜索传承人姓名"
                clearable
                @clear="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="级别">
              <el-select
                v-model="filters.level"
                placeholder="选择级别"
                clearable
                @change="handleSearch"
              >
                <el-option label="国家级" value="national" />
                <el-option label="省级" value="provincial" />
                <el-option label="市县级" value="city_county" />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="国家">
              <el-select
                v-model="filters.region"
                placeholder="选择国家"
                clearable
                filterable
                @change="handleSearch"
              >
                <el-option
                  v-for="reg in regions"
                  :key="reg.id"
                  :label="reg.country_name"
                  :value="reg.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="所属项目">
              <el-select
                v-model="filters.heritage_item"
                placeholder="选择项目"
                clearable
                filterable
                @change="handleSearch"
              >
                <el-option
                  v-for="item in heritageItems"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- Table Section -->
    <div class="table-section">
      <el-table
        v-loading="loading"
        :data="inheritorList"
        stripe
        class="inheritor-table"
      >
        <el-table-column prop="name" label="姓名" width="150">
          <template #default="{ row }">
            <div class="name-cell">
              <span class="name-text">{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="{ row }">
            <span v-if="row.gender">{{ getGenderText(row.gender) }}</span>
            <span v-else class="empty-text">-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="heritage_item.name" label="所属项目" min-width="200">
          <template #default="{ row }">
            <el-link
              type="primary"
              :underline="false"
              @click="handleViewHeritage(row.heritage_item.id)"
            >
              {{ row.heritage_item.name }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="level" label="级别" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.level" :type="getLevelTagType(row.level)" size="small">
              {{ getLevelText(row.level) }}
            </el-tag>
            <span v-else class="empty-text">-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="region.country_name" label="国家" width="150" />
        
        <el-table-column prop="area" label="地区" width="150" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.area">{{ row.area }}</span>
            <span v-else class="empty-text">-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="description" label="简介" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.description">{{ row.description }}</span>
            <span v-else class="empty-text">-</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-wrapper">
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
    
    // Remove empty filters
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

const getLevelTagType = (level: string) => {
  const typeMap: Record<string, any> = {
    national: 'danger',
    provincial: 'warning',
    city_county: 'info'
  }
  return typeMap[level] || 'info'
}

const getGenderText = (gender: string) => {
  const genderMap: Record<string, string> = {
    male: '男',
    female: '女',
    other: '其他'
  }
  return genderMap[gender] || gender
}

// Lifecycle
onMounted(() => {
  fetchHeritageItems()
  fetchRegions()
  fetchInheritorList()
})
</script>

<style scoped>
.inheritor-list-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fdfbf7 0%, #f8f4ed 100%);
}

.page-header {
  background: linear-gradient(135deg, #a0522d 0%, #8b4513 100%);
  padding: 3rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.15);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
  letter-spacing: 0.05em;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.page-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 300;
}

.filter-section {
  max-width: 1400px;
  margin: 0 auto 2rem;
  padding: 0 2rem;
}

.filter-form {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.table-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}

.inheritor-table {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.inheritor-table :deep(.el-table__row) {
  transition: all 0.3s ease;
}

.inheritor-table :deep(.el-table__row:hover) {
  background-color: #fdf6e3 !important;
}

.name-cell {
  display: flex;
  align-items: center;
}

.name-text {
  font-weight: 500;
  color: #8b4513;
}

.empty-text {
  color: #ccc;
  font-style: italic;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding: 1.5rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 2rem 1rem;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .filter-section,
  .table-section {
    padding: 0 1rem 1rem;
  }
}
</style>
