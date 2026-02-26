<template>
  <div class="heritage-list-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">非遗项目库</h1>
        <p class="page-subtitle">探索世界各地的非物质文化遗产</p>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <el-form :model="filters" class="filter-form" @submit.prevent="handleSearch">
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="关键词">
              <el-input
                v-model="filters.name"
                placeholder="搜索项目名称"
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
            <el-form-item label="分类">
              <el-select
                v-model="filters.category"
                placeholder="选择分类"
                clearable
                @change="handleSearch"
              >
                <el-option
                  v-for="cat in categories"
                  :key="cat.id"
                  :label="cat.name"
                  :value="cat.id"
                />
              </el-select>
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
        </el-row>
      </el-form>
    </div>

    <!-- Table Section -->
    <div class="table-section">
      <el-table
        v-loading="loading"
        :data="heritageList"
        stripe
        class="heritage-table"
        @row-click="handleRowClick"
      >
        <el-table-column prop="name" label="项目名称" min-width="200">
          <template #default="{ row }">
            <div class="name-cell">
              <span class="name-text">{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="category.name" label="分类" width="150" />
        
        <el-table-column prop="level" label="级别" width="120">
          <template #default="{ row }">
            <el-tag :type="getLevelTagType(row.level)" size="small">
              {{ getLevelText(row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="region.country_name" label="国家" width="150" />
        
        <el-table-column prop="area" label="地区" width="150" show-overflow-tooltip />
        
        <el-table-column prop="protection_unit" label="保护单位" min-width="180" show-overflow-tooltip />
        
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click.stop="handleViewDetail(row.id)"
            >
              查看详情
            </el-button>
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
    
    // Remove empty filters
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

const getLevelTagType = (level: string) => {
  const typeMap: Record<string, any> = {
    national: 'danger',
    provincial: 'warning',
    city_county: 'info'
  }
  return typeMap[level] || 'info'
}

// Lifecycle
onMounted(() => {
  fetchCategories()
  fetchRegions()
  fetchHeritageList()
})
</script>

<style scoped>
.heritage-list-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fdfbf7 0%, #f8f4ed 100%);
}

.page-header {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
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

.heritage-table {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.heritage-table :deep(.el-table__row) {
  cursor: pointer;
  transition: all 0.3s ease;
}

.heritage-table :deep(.el-table__row:hover) {
  background-color: #fdf6e3 !important;
  transform: translateY(-1px);
}

.name-cell {
  display: flex;
  align-items: center;
}

.name-text {
  font-weight: 500;
  color: #8b4513;
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
