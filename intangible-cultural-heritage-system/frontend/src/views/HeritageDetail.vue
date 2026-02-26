<template>
  <div class="heritage-detail-page">
    <!-- 动态水墨背景 -->
    <div class="ink-background">
      <div class="ink-layer layer-1"></div>
      <div class="ink-layer layer-2"></div>
      <div class="floating-particles">
        <div v-for="i in 12" :key="i" class="particle" :style="{ '--delay': `${i * 3}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }"></div>
      </div>
    </div>

    <div v-loading="loading" class="detail-container">
      <!-- 返回按钮 -->
      <div class="back-section">
        <button class="back-btn" @click="handleBack">
          <span class="back-seal">返</span>
          <span>返回列表</span>
          <span class="back-arrow">←</span>
        </button>
      </div>

      <div v-if="heritageItem" class="detail-content">
        <!-- 顶部英雄区 -->
        <header class="hero-section">
          <div class="hero-decoration">
            <div class="decoration-wave left"></div>
            <div class="hero-seal-group">
              <div class="main-seal">
                <div class="seal-outer">
                  <div class="seal-inner">
                    <span class="seal-text">珍宝</span>
                  </div>
                </div>
              </div>
              <div class="seal-glow"></div>
            </div>
            <div class="decoration-wave right"></div>
          </div>

          <div class="hero-content">
            <h1 class="hero-title">{{ heritageItem.name }}</h1>
            <div class="hero-meta">
              <span class="meta-badge" :class="getLevelClass(heritageItem.level)">
                {{ getLevelText(heritageItem.level) }}
              </span>
              <span class="meta-divider">·</span>
              <span class="meta-item">{{ heritageItem.category.name }}</span>
              <span class="meta-divider">·</span>
              <span class="meta-item">{{ heritageItem.region.country_name }}</span>
              <span v-if="heritageItem.area" class="meta-divider">·</span>
              <span v-if="heritageItem.area" class="meta-item">{{ heritageItem.area }}</span>
            </div>
          </div>

          <div class="hero-waves">
            <svg class="wave" viewBox="0 0 1200 120" preserveAspectRatio="none">
              <path d="M0,50 C150,100 350,0 600,50 C850,100 1050,0 1200,50 L1200,120 L0,120 Z" fill="rgba(212, 175, 55, 0.1)"></path>
            </svg>
            <svg class="wave wave-2" viewBox="0 0 1200 120" preserveAspectRatio="none">
              <path d="M0,60 C200,110 400,10 600,60 C800,110 1000,10 1200,60 L1200,120 L0,120 Z" fill="rgba(212, 175, 55, 0.05)"></path>
            </svg>
          </div>
        </header>

        <!-- 信息卡片组 -->
        <div class="info-cards">
          <div class="info-card basic-info">
            <div class="card-header">
              <div class="header-decoration">
                <span class="card-seal">基</span>
                <h3 class="card-title">基本信息</h3>
              </div>
              <div class="header-line"></div>
            </div>
            <div class="card-body">
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">项目名称</span>
                  <span class="info-value">{{ heritageItem.name }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">分类</span>
                  <span class="info-value category-tag">{{ heritageItem.category.name }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">级别</span>
                  <span class="info-value" :class="getLevelClass(heritageItem.level)">
                    {{ getLevelText(heritageItem.level) }}
                  </span>
                </div>
                <div class="info-item">
                  <span class="info-label">国家</span>
                  <span class="info-value">{{ heritageItem.region.country_name }}</span>
                </div>
                <div v-if="heritageItem.area" class="info-item">
                  <span class="info-label">地区</span>
                  <span class="info-value">{{ heritageItem.area }}</span>
                </div>
                <div v-if="heritageItem.protection_unit" class="info-item full-width">
                  <span class="info-label">保护单位</span>
                  <span class="info-value">{{ heritageItem.protection_unit }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="info-card geo-info">
            <div class="card-header">
              <div class="header-decoration">
                <span class="card-seal">地</span>
                <h3 class="card-title">地理信息</h3>
              </div>
              <div class="header-line"></div>
            </div>
            <div class="card-body">
              <div class="info-grid">
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
                  <span class="info-value">{{ heritageItem.region.longitude.toFixed(4) }}°</span>
                </div>
                <div class="info-item">
                  <span class="info-label">纬度</span>
                  <span class="info-value">{{ heritageItem.region.latitude.toFixed(4) }}°</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 项目简介 -->
        <div v-if="heritageItem.description" class="description-card">
          <div class="card-header">
            <div class="header-decoration">
              <span class="card-seal">介</span>
              <h3 class="card-title">项目简介</h3>
            </div>
            <div class="header-line"></div>
          </div>
          <div class="description-body">
            <p class="description-text">{{ heritageItem.description }}</p>
          </div>
        </div>

        <!-- 相关传承人 -->
        <div class="inheritors-card">
          <div class="card-header">
            <div class="header-decoration">
              <span class="card-seal">传</span>
              <h3 class="card-title">相关传承人</h3>
              <span class="count-badge">{{ inheritors.length }}</span>
            </div>
            <div class="header-line"></div>
          </div>

          <div v-if="inheritors.length > 0" class="inheritors-grid">
            <div
              v-for="inheritor in inheritors"
              :key="inheritor.id"
              class="inheritor-card"
            >
              <div class="inheritor-avatar">
                <span class="avatar-text">{{ inheritor.name.charAt(0) }}</span>
                <div class="avatar-ring"></div>
              </div>
              <div class="inheritor-content">
                <h4 class="inheritor-name">{{ inheritor.name }}</h4>
                <div class="inheritor-meta">
                  <span v-if="inheritor.level" class="inheritor-level" :class="getLevelClass(inheritor.level)">
                    {{ getLevelText(inheritor.level) }}
                  </span>
                  <span v-if="inheritor.gender" class="inheritor-gender">
                    {{ getGenderText(inheritor.gender) }}
                  </span>
                </div>
                <p v-if="inheritor.area" class="inheritor-location">
                  📍 {{ inheritor.area }}
                </p>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <div class="empty-icon">—</div>
            <p>暂无相关传承人</p>
          </div>
        </div>

        <!-- 时间戳 -->
        <div class="timestamps">
          <div class="timestamp-item">
            <span class="timestamp-label">创建时间</span>
            <span class="timestamp-value">{{ formatDate(heritageItem.created_at) }}</span>
          </div>
          <div class="timestamp-divider"></div>
          <div class="timestamp-item">
            <span class="timestamp-label">更新时间</span>
            <span class="timestamp-value">{{ formatDate(heritageItem.updated_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
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
/* ========== 全局样式 ========== */
.heritage-detail-page {
  min-height: 100%;
  padding: 32px;
  background: #F7F4ED;
  position: relative;
}

/* ========== 动态水墨背景 ========== */
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

.ink-layer {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.08;
  animation: inkDrift 45s ease-in-out infinite;
}

.ink-layer.layer-1 {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle at center, #C23531 0%, transparent 70%);
  top: -200px;
  right: -200px;
}

.ink-layer.layer-2 {
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
    transform: translate(60px, -50px) scale(1.05);
  }
  66% {
    transform: translate(-50px, 60px) scale(0.95);
  }
}

.floating-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 5px;
  height: 5px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.5) 0%, transparent 70%);
  border-radius: 50%;
  left: var(--x);
  top: var(--y);
  animation: particleFloat 30s ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes particleFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translate(80px, -100px) scale(2);
    opacity: 0.7;
  }
}

/* ========== 主容器 ========== */
.detail-container {
  position: relative;
  z-index: 1;
  max-width: 1000px;
  margin: 0 auto;
}

/* ========== 返回按钮 ========== */
.back-section {
  margin-bottom: 28px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  padding: 12px 28px;
  background: white;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(47, 54, 64, 0.08);
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

.back-btn:hover {
  border-color: #D4AF37;
  transform: translateX(-6px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.2);
  color: #2F3640;
}

.back-seal {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #D4AF37;
  color: #2F3640;
  font-size: 14px;
  font-weight: 700;
  border-radius: 4px;
  font-family: "STSong", "SimSun", serif;
}

.back-arrow {
  transition: transform 0.35s;
}

.back-btn:hover .back-arrow {
  transform: translateX(-4px);
}

/* ========== 英雄区 ========== */
.hero-section {
  position: relative;
  text-align: center;
  padding: 56px 48px 80px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border-radius: 16px;
  margin-bottom: 32px;
  box-shadow: 0 16px 48px rgba(194, 35, 49, 0.35);
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}

.hero-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  margin-bottom: 32px;
  position: relative;
}

.decoration-wave {
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.6), transparent);
  position: relative;
}

.decoration-wave::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  background: #D4AF37;
  border-radius: 50%;
  box-shadow: 0 0 0 6px rgba(212, 175, 55, 0.3);
}

.hero-seal-group {
  position: relative;
}

.main-seal {
  position: relative;
}

.seal-outer {
  width: 96px;
  height: 96px;
  background: #D4AF37;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 10px 30px rgba(212, 175, 55, 0.5),
    inset 0 2px 0 rgba(255, 255, 255, 0.3);
  animation: sealFloat 6s ease-in-out infinite;
  position: relative;
  z-index: 1;
}

@keyframes sealFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-12px) rotate(3deg);
  }
}

.seal-outer::before {
  content: '';
  position: absolute;
  top: 6px;
  left: 6px;
  right: 6px;
  bottom: 6px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
}

.seal-inner {
  width: 82px;
  height: 82px;
  background: rgba(212, 175, 55, 0.9);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.25);
}

.seal-text {
  font-size: 32px;
  font-weight: 700;
  color: #2F3640;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 6px;
}

.seal-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.4) 0%, transparent 70%);
  border-radius: 50%;
  z-index: 0;
  animation: glowPulse 3s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 42px;
  font-weight: 700;
  color: white;
  margin: 0 0 20px 0;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
  text-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  line-height: 1.3;
}

.hero-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.meta-badge {
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.meta-badge.level-national {
  background: rgba(212, 175, 55, 0.35);
  border-color: rgba(212, 175, 55, 0.5);
}

.meta-divider {
  color: rgba(247, 244, 237, 0.5);
  font-size: 16px;
}

.meta-item {
  color: rgba(247, 244, 237, 0.95);
  font-size: 15px;
  font-weight: 500;
}

.hero-waves {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  overflow: hidden;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.wave-2 {
  animation: waveDelay 4s ease-in-out infinite;
}

@keyframes waveDelay {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(-20px);
  }
}

/* ========== 信息卡片 ========== */
.info-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.info-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(47, 54, 64, 0.1);
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(47, 54, 64, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: linear-gradient(135deg, #F7F4ED 0%, #EDF2ED 100%);
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.header-decoration {
  display: flex;
  align-items: center;
  gap: 14px;
}

.card-seal {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #C23531;
  color: white;
  font-size: 16px;
  font-weight: 700;
  border-radius: 6px;
  font-family: "STSong", "SimSun", serif;
  box-shadow: 0 4px 12px rgba(194, 35, 49, 0.3);
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #2F3640;
  margin: 0;
  letter-spacing: 2px;
  font-family: "STSong", "SimSun", serif;
}

.header-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.4), transparent);
  margin-left: 20px;
}

.card-body {
  padding: 24px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item.full-width {
  grid-column: span 2;
}

.info-label {
  font-size: 13px;
  font-weight: 600;
  color: #909399;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.info-value {
  font-size: 15px;
  font-weight: 500;
  color: #2F3640;
}

.info-value.level-national {
  color: #C23531;
  font-weight: 600;
}

.info-value.level-provincial {
  color: #CD7F32;
  font-weight: 600;
}

.info-value.level-city_county {
  color: #5D8AA8;
  font-weight: 600;
}

.category-tag {
  display: inline-block;
  padding: 6px 14px;
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid rgba(212, 175, 55, 0.25);
}

/* ========== 描述卡片 ========== */
.description-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(47, 54, 64, 0.1);
  margin-bottom: 24px;
  overflow: hidden;
}

.description-body {
  padding: 28px 32px;
}

.description-text {
  font-size: 15px;
  line-height: 2.2;
  color: #606266;
  margin: 0;
  white-space: pre-wrap;
  text-align: justify;
  text-indent: 2em;
}

/* ========== 传承人卡片 ========== */
.inheritors-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(47, 54, 64, 0.1);
  margin-bottom: 24px;
  overflow: hidden;
}

.count-badge {
  margin-left: auto;
  padding: 6px 14px;
  background: rgba(212, 175, 55, 0.2);
  color: #CD7F32;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 600;
}

.inheritors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 24px 32px;
}

.inheritor-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 20px;
  background: linear-gradient(135deg, #FFFBF7 0%, #F7F4ED 100%);
  border-radius: 12px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.inheritor-card:hover {
  border-color: #D4AF37;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.2);
  transform: translateY(-4px);
}

.inheritor-avatar {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #D4AF37, #CD7F32);
  color: #2F3640;
  font-size: 22px;
  font-weight: 700;
  border-radius: 50%;
  font-family: "STSong", "SimSun", serif;
  flex-shrink: 0;
  position: relative;
}

.avatar-ring {
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid rgba(212, 175, 55, 0.3);
  animation: ringPulse 3s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

.avatar-text {
  position: relative;
  z-index: 1;
}

.inheritor-content {
  flex: 1;
}

.inheritor-name {
  font-size: 17px;
  font-weight: 600;
  color: #2F3640;
  margin: 0 0 8px 0;
}

.inheritor-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 6px;
}

.inheritor-level {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.inheritor-level.level-national {
  background: rgba(194, 35, 49, 0.12);
  color: #C23531;
}

.inheritor-level.level-provincial {
  background: rgba(212, 175, 55, 0.15);
  color: #CD7F32;
}

.inheritor-level.level-city_county {
  background: rgba(93, 138, 168, 0.15);
  color: #5D8AA8;
}

.inheritor-gender {
  font-size: 13px;
  color: #909399;
}

.inheritor-location {
  font-size: 13px;
  color: #606266;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 56px;
  color: #C0C4CC;
  display: block;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 15px;
  color: #909399;
  margin: 0;
}

/* ========== 时间戳 ========== */
.timestamps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 20px 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(47, 54, 64, 0.1);
}

.timestamp-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.timestamp-label {
  font-size: 12px;
  color: #909399;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.timestamp-value {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.timestamp-divider {
  width: 1px;
  height: 40px;
  background: linear-gradient(180deg, transparent, #D4AF37, transparent);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .heritage-detail-page {
    padding: 16px;
  }

  .hero-section {
    padding: 40px 24px 60px;
  }

  .hero-decoration {
    flex-direction: column;
    gap: 16px;
  }

  .decoration-wave {
    width: 60px;
  }

  .hero-title {
    font-size: 32px;
    letter-spacing: 4px;
  }

  .hero-meta {
    flex-direction: column;
    gap: 8px;
  }

  .meta-divider {
    display: none;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .inheritors-grid {
    grid-template-columns: 1fr;
    padding: 20px;
  }

  .timestamps {
    flex-direction: column;
    gap: 16px;
  }

  .timestamp-divider {
    width: 40px;
    height: 1px;
  }
}
</style>
