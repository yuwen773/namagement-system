<template>
  <div class="heritage-detail-page">
    <div v-loading="loading" class="detail-container">
      <!-- Back Button -->
      <div class="back-section">
        <el-button @click="handleBack" class="back-btn">
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </el-button>
      </div>

      <div v-if="heritageItem" class="detail-content">
        <!-- Header Card -->
        <div class="header-card">
          <div class="header-main">
            <h1 class="item-title">{{ heritageItem.name }}</h1>
            <el-tag :type="getLevelTagType(heritageItem.level)" size="large" class="level-tag">
              {{ getLevelText(heritageItem.level) }}
            </el-tag>
          </div>
          <div class="header-meta">
            <div class="meta-item">
              <span class="meta-label">分类</span>
              <span class="meta-value">{{ heritageItem.category.name }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">国家</span>
              <span class="meta-value">{{ heritageItem.region.country_name }}</span>
            </div>
            <div v-if="heritageItem.area" class="meta-item">
              <span class="meta-label">地区</span>
              <span class="meta-value">{{ heritageItem.area }}</span>
            </div>
          </div>
        </div>

        <!-- Info Cards -->
        <el-row :gutter="20" class="info-section">
          <el-col :xs="24" :md="12">
            <div class="info-card">
              <h3 class="card-title">基本信息</h3>
              <div class="info-list">
                <div class="info-item">
                  <span class="info-label">项目名称</span>
                  <span class="info-value">{{ heritageItem.name }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">分类</span>
                  <span class="info-value">{{ heritageItem.category.name }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">级别</span>
                  <span class="info-value">{{ getLevelText(heritageItem.level) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">国家</span>
                  <span class="info-value">{{ heritageItem.region.country_name }}</span>
                </div>
                <div v-if="heritageItem.area" class="info-item">
                  <span class="info-label">地区</span>
                  <span class="info-value">{{ heritageItem.area }}</span>
                </div>
                <div v-if="heritageItem.protection_unit" class="info-item">
                  <span class="info-label">保护单位</span>
                  <span class="info-value">{{ heritageItem.protection_unit }}</span>
                </div>
              </div>
            </div>
          </el-col>

          <el-col :xs="24" :md="12">
            <div class="info-card">
              <h3 class="card-title">地理信息</h3>
              <div class="info-list">
                <div class="info-item">
                  <span class="info-label">国家代码</span>
                  <span class="info-value">{{ heritageItem.region.country_code }}</span>
                </div>
                <div v-if="heritageItem.region.continent" class="info-item">
                  <span class="info-label">所属洲</span>
                  <span class="info-value">{{ heritageItem.region.continent }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">经度</span>
                  <span class="info-value">{{ heritageItem.region.longitude.toFixed(4) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">纬度</span>
                  <span class="info-value">{{ heritageItem.region.latitude.toFixed(4) }}</span>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>

        <!-- Description Card -->
        <div v-if="heritageItem.description" class="description-card">
          <h3 class="card-title">项目简介</h3>
          <p class="description-text">{{ heritageItem.description }}</p>
        </div>

        <!-- Related Inheritors -->
        <div class="inheritors-section">
          <div class="section-header">
            <h3 class="section-title">相关传承人</h3>
            <span class="count-badge">{{ inheritors.length }} 人</span>
          </div>
          
          <div v-if="inheritors.length > 0" class="inheritors-grid">
            <div
              v-for="inheritor in inheritors"
              :key="inheritor.id"
              class="inheritor-card"
              @click="handleViewInheritor(inheritor.id)"
            >
              <div class="inheritor-header">
                <h4 class="inheritor-name">{{ inheritor.name }}</h4>
                <el-tag v-if="inheritor.level" size="small" :type="getLevelTagType(inheritor.level)">
                  {{ getLevelText(inheritor.level) }}
                </el-tag>
              </div>
              <div class="inheritor-info">
                <div v-if="inheritor.gender" class="inheritor-meta">
                  <span class="meta-label">性别：</span>
                  <span>{{ getGenderText(inheritor.gender) }}</span>
                </div>
                <div v-if="inheritor.area" class="inheritor-meta">
                  <span class="meta-label">地区：</span>
                  <span>{{ inheritor.area }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <el-empty v-else description="暂无相关传承人" />
        </div>

        <!-- Timestamps -->
        <div class="timestamps">
          <span class="timestamp-item">创建时间：{{ formatDate(heritageItem.created_at) }}</span>
          <span class="timestamp-item">更新时间：{{ formatDate(heritageItem.updated_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getHeritageDetail } from '@/api/heritage'
import { getInheritorList } from '@/api/inheritor'
import type { HeritageItem, Inheritor } from '@/types'

const route = useRoute()
const router = useRouter()

// Data
const loading = ref(false)
const heritageItem = ref<HeritageItem | null>(null)
const inheritors = ref<Inheritor[]>([])

// Methods
const fetchHeritageDetail = async () => {
  loading.value = true
  try {
    const id = Number(route.params.id)
    const response = await getHeritageDetail(id)
    
    if (response.data.code === 0) {
      heritageItem.value = response.data.data
      // Fetch related inheritors
      await fetchInheritors(id)
    } else {
      ElMessage.error('获取项目详情失败')
      router.push({ name: 'HeritageList' })
    }
  } catch (error) {
    ElMessage.error('获取项目详情失败')
    console.error(error)
    router.push({ name: 'HeritageList' })
  } finally {
    loading.value = false
  }
}

const fetchInheritors = async (heritageId: number) => {
  try {
    const response = await getInheritorList({ heritage_item: heritageId })
    if (response.data.code === 0) {
      inheritors.value = response.data.data
    }
  } catch (error) {
    console.error('获取传承人列表失败:', error)
  }
}

const handleBack = () => {
  router.push({ name: 'HeritageList' })
}

const handleViewInheritor = (id: number) => {
  // Navigate to inheritor detail if needed
  console.log('View inheritor:', id)
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

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  fetchHeritageDetail()
})
</script>

<style scoped>
.heritage-detail-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fdfbf7 0%, #f8f4ed 100%);
  padding: 2rem;
}

.detail-container {
  max-width: 1200px;
  margin: 0 auto;
}

.back-section {
  margin-bottom: 1.5rem;
}

.back-btn {
  border: none;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #8b4513;
  color: #fff;
  transform: translateX(-4px);
}

.detail-content {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-card {
  background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
  padding: 2.5rem;
  border-radius: 16px;
  margin-bottom: 2rem;
  box-shadow: 0 8px 24px rgba(139, 69, 19, 0.2);
  color: #fff;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.item-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.02em;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.level-tag {
  font-size: 1rem;
  padding: 0.5rem 1rem;
}

.header-meta {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-label {
  font-size: 0.875rem;
  opacity: 0.8;
  font-weight: 300;
}

.meta-value {
  font-size: 1.125rem;
  font-weight: 500;
}

.info-section {
  margin-bottom: 2rem;
}

.info-card {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  height: 100%;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #8b4513;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #f0e6d2;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f5f5f5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #666;
  min-width: 100px;
}

.info-value {
  color: #333;
  text-align: right;
  flex: 1;
}

.description-card {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.description-text {
  font-size: 1rem;
  line-height: 1.8;
  color: #555;
  margin: 0;
  white-space: pre-wrap;
}

.inheritors-section {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #8b4513;
  margin: 0;
}

.count-badge {
  background: #f0e6d2;
  color: #8b4513;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
}

.inheritors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.inheritor-card {
  background: #fdfbf7;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #f0e6d2;
  cursor: pointer;
  transition: all 0.3s ease;
}

.inheritor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(139, 69, 19, 0.15);
  border-color: #8b4513;
}

.inheritor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.inheritor-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.inheritor-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.inheritor-meta {
  font-size: 0.875rem;
  color: #666;
}

.timestamps {
  display: flex;
  gap: 2rem;
  justify-content: center;
  padding: 1rem;
  font-size: 0.875rem;
  color: #999;
}

.timestamp-item {
  display: flex;
  align-items: center;
}

/* Responsive */
@media (max-width: 768px) {
  .heritage-detail-page {
    padding: 1rem;
  }
  
  .item-title {
    font-size: 1.75rem;
  }
  
  .header-card {
    padding: 1.5rem;
  }
  
  .info-card,
  .description-card,
  .inheritors-section {
    padding: 1.5rem;
  }
  
  .inheritors-grid {
    grid-template-columns: 1fr;
  }
  
  .timestamps {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
