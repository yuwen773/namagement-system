<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '@/api'
import { ArrowLeft, Location, Timer, Star, ShoppingCart, Link } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const product = ref(null)

// 放大镜相关状态
const imageContainer = ref(null)
const isHovering = ref(false)
const magnifierPos = ref({ x: 0, y: 0 })
const cursorPos = ref({ x: 0, y: 0 })
const ZOOM_LEVEL = 4
const MAGNIFIER_SIZE = 200

// 获取商品详情
const fetchProduct = async () => {
  const id = route.params.id
  loading.value = true
  try {
    const res = await productApi.getDetail(id)
    if (res.code === 0) {
      product.value = res.data
    }
  } catch (error) {
    console.error('Failed to fetch product:', error)
    // 使用模拟数据
    product.value = generateMockProduct(id)
  }

  loading.value = false
}

// 生成模拟商品数据
const generateMockProduct = (id) => {
  const shops = ['皇家宠物旗舰店', '渴望官方旗舰店', '冠能官方店', '耐威克旗舰店']
  const titles = [
    '皇家猫粮 成猫用鸡肉配方 5kg 营养均衡',
    '渴望 六种鱼猫粮 成猫专用 1.8kg 高蛋白',
    '冠能 狗粮 中大型犬成犬 15kg',
    '耐威克 猫砂 豆腐砂 混合型 6L*3 除臭'
  ]
  const idx = (parseInt(id) - 1) % 4

  return {
    id: id,
    title: titles[idx],
    price: [199, 268, 580, 89][idx],
    sales: [50000, 38000, 22000, 20000][idx],
    shop: shops[idx],
    image_url: `https://picsum.photos/seed/${id}/1200/1200`,
    detail_url: `https://detail.tmall.com/item.htm?id=${id}`,
    category: ['猫粮', '猫粮', '狗粮', '猫砂'][idx],
    brand: ['皇家', '渴望', '冠能', '耐威克'][idx],
    description: '优质宠物用品，正品保障，让爱宠健康快乐。',
    rating: 4.8,
    reviews: 1234
  }
}

// 处理鼠标移动
const handleMouseMove = (e) => {
  if (!imageContainer.value) return

  const rect = imageContainer.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  // 限制在容器范围内
  const clampedX = Math.max(0, Math.min(x, rect.width))
  const clampedY = Math.max(0, Math.min(y, rect.height))

  cursorPos.value = { x: clampedX, y: clampedY }

  // 计算放大镜位置（以鼠标为中心）
  magnifierPos.value = {
    x: clampedX - MAGNIFIER_SIZE / 2,
    y: clampedY - MAGNIFIER_SIZE / 2
  }
}

// 处理鼠标进入
const handleMouseEnter = () => {
  isHovering.value = true
}

// 处理鼠标离开
const handleMouseLeave = () => {
  isHovering.value = false
}

// 计算背景图片位置
const backgroundPosition = computed(() => {
  if (!imageContainer.value) return '0 0'

  const rect = imageContainer.value.getBoundingClientRect()
  const xPercent = (cursorPos.value.x / rect.width) * 100
  const yPercent = (cursorPos.value.y / rect.height) * 100

  return `${xPercent}% ${yPercent}%`
})

// 返回列表
const goBack = () => {
  router.push('/user/products')
}

// 打开天猫链接
const openTmallLink = () => {
  if (product.value?.detail_url) {
    window.open(product.value.detail_url, '_blank')
  }
}

// 格式化价格
const formatPrice = (price) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2
  }).format(price)
}

// 格式化销量
const formatSales = (sales) => {
  return new Intl.NumberFormat('zh-CN').format(sales)
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  return new Date(timeStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 解析标签
const parseTags = (tags) => {
  if (!tags) return []
  if (Array.isArray(tags)) return tags
  return tags.split(',').map(t => t.trim()).filter(t => t)
}

onMounted(() => {
  fetchProduct()
})
</script>

<template>
  <div class="product-detail-page">
    <!-- 背景装饰 -->
    <div class="page-bg">
      <div class="bg-gradient-orb orb-1"></div>
      <div class="bg-gradient-orb orb-2"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- 返回导航 -->
    <nav class="detail-nav">
      <button class="nav-back" @click="goBack">
        <ArrowLeft class="back-icon" />
        <span>返回列表</span>
      </button>
      <div class="nav-breadcrumb">
        <span class="breadcrumb-item">商品</span>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-item current">详情</span>
      </div>
    </nav>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-wrapper">
      <div class="loading-card">
        <div class="loader-ring">
          <div class="ring-segment segment-1"></div>
          <div class="ring-segment segment-2"></div>
          <div class="ring-segment segment-3"></div>
        </div>
        <p class="loading-text">加载商品详情中...</p>
      </div>
    </div>

    <!-- 商品详情内容 -->
    <div v-else-if="product" class="detail-content">
      <!-- 主要信息区 -->
      <section class="product-hero">
        <!-- 商品图片区 -->
        <div class="product-gallery">
          <div
            ref="imageContainer"
            class="gallery-main"
            @mousemove="handleMouseMove"
            @mouseenter="handleMouseEnter"
            @mouseleave="handleMouseLeave"
          >
            <img :src="product.image_url" :alt="product.title" class="product-image" />

            <!-- 放大镜透镜 -->
            <Transition name="magnifier">
              <div
                v-if="isHovering"
                class="magnifier-lens"
                :style="{
                  left: magnifierPos.x + 'px',
                  top: magnifierPos.y + 'px',
                  width: MAGNIFIER_SIZE + 'px',
                  height: MAGNIFIER_SIZE + 'px',
                  backgroundImage: `url(${product.image_url})`,
                  backgroundSize: `${ZOOM_LEVEL * 100}%`,
                  backgroundPosition: backgroundPosition
                }"
              >
                <div class="lens-crosshair h"></div>
                <div class="lens-crosshair v"></div>
                <div class="lens-corners">
                  <span class="corner tl"></span>
                  <span class="corner tr"></span>
                  <span class="corner bl"></span>
                  <span class="corner br"></span>
                </div>
                <div class="lens-center"></div>
              </div>
            </Transition>
          </div>

          <!-- 放大提示 -->
          <div class="gallery-hint">
            <div class="hint-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
                <path d="M11 8v6M8 11h6"/>
              </svg>
            </div>
            <span>悬停放大查看</span>
          </div>
        </div>

        <!-- 商品信息区 -->
        <div class="product-details">
          <!-- 类目标签 -->
          <div class="product-meta">
            <span class="category-badge">{{ product.category || '宠物用品' }}</span>
            <div class="rating-badge">
              <Star class="star-icon" />
              <span>{{ product.rating || 4.8 }}</span>
            </div>
          </div>

          <!-- 商品标题 -->
          <h1 class="product-title">{{ product.title }}</h1>

          <!-- 价格卡片 -->
          <div class="price-card">
            <div class="price-header">
              <span class="price-label">商品价格</span>
              <span class="price-trend" v-if="product.sales > 10000">热销商品</span>
            </div>
            <div class="price-display">
              <span class="price-symbol">¥</span>
              <span class="price-amount">{{ formatPrice(product.price) }}</span>
            </div>
            <div class="price-footer">
              <span class="review-count">{{ product.reviews || 0 }} 条评价</span>
              <span class="sales-count">已售 {{ formatSales(product.sales) }}</span>
            </div>
          </div>

          <!-- 核心数据 -->
          <div class="data-grid">
            <div class="data-item">
              <div class="data-icon">
                <ShoppingCart />
              </div>
              <div class="data-content">
                <span class="data-label">所属店铺</span>
                <span class="data-value">{{ product.shop }}</span>
              </div>
            </div>
            <div class="data-item">
              <div class="data-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21v-8a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v8"/>
                  <path d="M12 3a6 6 0 0 1 6 6v2H6V9a6 6 0 0 1 6-6z"/>
                  <path d="M12 11v6"/>
                </svg>
              </div>
              <div class="data-content">
                <span class="data-label">品牌</span>
                <span class="data-value">{{ product.brand || '知名品牌' }}</span>
              </div>
            </div>
          </div>

          <!-- 详细信息 -->
          <div class="info-panels">
            <div class="info-panel">
              <div class="panel-row">
                <span class="panel-label">商品ID</span>
                <span class="panel-value">{{ product.product_id || '-' }}</span>
              </div>
              <div class="panel-row" v-if="product.region">
                <span class="panel-label">发货地</span>
                <span class="panel-value">{{ product.region }}</span>
              </div>
              <div class="panel-row" v-if="product.seller_nick">
                <span class="panel-label">卖家</span>
                <span class="panel-value">{{ product.seller_nick }}</span>
              </div>
              <div class="panel-row">
                <span class="panel-label">采集时间</span>
                <span class="panel-value">{{ formatTime(product.crawl_time) }}</span>
              </div>
            </div>
          </div>

          <!-- 标签 -->
          <div v-if="product.tags" class="tags-wrapper">
            <span
              v-for="(tag, index) in parseTags(product.tags)"
              :key="index"
              class="product-tag"
            >
              {{ tag }}
            </span>
          </div>

          <!-- 属性 -->
          <div v-if="product.product_attributes && Object.keys(product.product_attributes).length > 0" class="attributes-wrapper">
            <div
              v-for="(value, key) in product.product_attributes"
              :key="key"
              class="attribute-pair"
            >
              <span class="attr-key">{{ key }}</span>
              <span class="attr-val">{{ value }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-buttons">
            <button class="btn-action btn-primary" @click="openTmallLink">
              <ShoppingCart class="btn-icon" />
              <span>前往天猫购买</span>
            </button>
            <button class="btn-action btn-secondary" @click="openTmallLink">
              <Link class="btn-icon" />
              <span>复制链接</span>
            </button>
          </div>

          <!-- 店铺信息 -->
          <div class="shop-card">
            <div class="shop-badge">
              <Location class="shop-badge-icon" />
              <span>官方店铺</span>
            </div>
            <div class="shop-name">{{ product.shop }}</div>
            <div class="shop-features">
              <span class="feature-tag">正品保障</span>
              <span class="feature-tag">快速发货</span>
              <span class="feature-tag">售后无忧</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 商品描述 -->
      <section class="description-panel">
        <div class="panel-header">
          <h2 class="panel-title">商品描述</h2>
          <div class="panel-deco"></div>
        </div>
        <div class="panel-body">
          <p class="description-text">{{ product.description || '暂无详细描述' }}</p>
          <div class="feature-grid">
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                  <path d="m2 17 10 5 10-5"/>
                  <path d="m2 12 10 5 10-5"/>
                </svg>
              </div>
              <span>正品保障</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                </svg>
              </div>
              <span>精美包装</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <path d="M14 2v6h6"/>
                  <path d="M16 13H8"/>
                  <path d="M16 17H8"/>
                </svg>
              </div>
              <span>七天退换</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <span>优质售后</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-wrapper">
      <div class="empty-card">
        <div class="empty-illustration">
          <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
            <path d="M3 6h18"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
        </div>
        <h3 class="empty-title">商品不存在</h3>
        <p class="empty-desc">该商品可能已被下架或删除</p>
        <button class="btn-back" @click="goBack">返回商品列表</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ============================================
   Design Tokens
   ============================================ */
.product-detail-page {
  --color-orange: #FF6B35;
  --color-purple: #7B2CBF;
  --color-gold: #FFD700;
  --color-cyan: #06FFA5;
  --bg-primary: #0a0a12;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-accent: rgba(255, 107, 53, 0.3);

  position: relative;
  min-height: 100vh;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
}

/* ============================================
   Background Effects
   ============================================ */
.page-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.bg-gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.15;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--color-orange) 0%, transparent 70%);
  top: -200px;
  right: -150px;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, var(--color-purple) 0%, transparent 70%);
  bottom: -150px;
  left: -100px;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 70%);
}

/* ============================================
   Navigation
   ============================================ */
.detail-nav {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
  margin-bottom: 24px;
}

.nav-back {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 14px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-back:hover {
  border-color: var(--border-accent);
  color: var(--color-orange);
  background: var(--bg-card-hover);
}

.nav-back .back-icon {
  width: 18px;
  height: 18px;
}

.nav-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.breadcrumb-item {
  color: var(--text-tertiary);
  transition: color 0.2s ease;
}

.breadcrumb-item.current {
  color: var(--color-orange);
  font-weight: 600;
}

.breadcrumb-separator {
  color: var(--text-tertiary);
}

/* ============================================
   Loading State
   ============================================ */
.loading-wrapper {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.loading-card {
  text-align: center;
}

.loader-ring {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
}

.ring-segment {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 3px solid transparent;
  animation: rotate 1.5s linear infinite;
}

.segment-1 {
  border-top-color: var(--color-orange);
  border-right-color: var(--color-orange);
  animation-duration: 1.5s;
}

.segment-2 {
  inset: 8px;
  border-bottom-color: var(--color-purple);
  border-left-color: var(--color-purple);
  animation-duration: 2s;
  animation-direction: reverse;
}

.segment-3 {
  inset: 16px;
  border-top-color: var(--color-gold);
  animation-duration: 2.5s;
}

@keyframes rotate {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* ============================================
   Detail Content
   ============================================ */
.detail-content {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* ============================================
   Product Hero Section
   ============================================ */
.product-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Gallery */
.product-gallery {
  position: relative;
}

.gallery-main {
  position: relative;
  aspect-ratio: 1;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 24px;
  overflow: hidden;
  cursor: crosshair;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.gallery-main:hover .product-image {
  transform: scale(1.02);
}

/* Magnifier Lens */
.magnifier-lens {
  position: absolute;
  border-radius: 50%;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 10;
  box-shadow:
    0 0 0 3px var(--color-orange),
    0 0 0 6px var(--color-cyan),
    0 0 40px rgba(255, 107, 53, 0.5),
    inset 0 0 30px rgba(0, 0, 0, 0.3);
}

.magnifier-lens::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 3px,
    rgba(6, 255, 165, 0.03) 3px,
    rgba(6, 255, 165, 0.03) 6px
  );
}

.lens-crosshair {
  position: absolute;
  background: var(--color-cyan);
  box-shadow: 0 0 10px var(--color-cyan);
}

.lens-crosshair.h {
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
}

.lens-crosshair.v {
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
}

.lens-corners {
  position: absolute;
  inset: 12px;
}

.lens-corners .corner {
  position: absolute;
  width: 16px;
  height: 16px;
}

.lens-corners .corner::before,
.lens-corners .corner::after {
  content: '';
  position: absolute;
  background: var(--color-cyan);
  box-shadow: 0 0 8px var(--color-cyan);
}

.lens-corners .corner.tl { top: 0; left: 0; }
.lens-corners .corner.tl::before { width: 14px; height: 2px; top: 0; left: 0; }
.lens-corners .corner.tl::after { width: 2px; height: 14px; top: 0; left: 0; }

.lens-corners .corner.tr { top: 0; right: 0; }
.lens-corners .corner.tr::before { width: 14px; height: 2px; top: 0; right: 0; }
.lens-corners .corner.tr::after { width: 2px; height: 14px; top: 0; right: 0; }

.lens-corners .corner.bl { bottom: 0; left: 0; }
.lens-corners .corner.bl::before { width: 14px; height: 2px; bottom: 0; left: 0; }
.lens-corners .corner.bl::after { width: 2px; height: 14px; bottom: 0; left: 0; }

.lens-corners .corner.br { bottom: 0; right: 0; }
.lens-corners .corner.br::before { width: 14px; height: 2px; bottom: 0; right: 0; }
.lens-corners .corner.br::after { width: 2px; height: 14px; bottom: 0; right: 0; }

.lens-center {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 10px;
  height: 10px;
  transform: translate(-50%, -50%);
  background: var(--color-cyan);
  border-radius: 50%;
  box-shadow:
    0 0 15px var(--color-cyan),
    0 0 30px rgba(6, 255, 165, 0.5);
  animation: lensPulse 1.5s ease-in-out infinite;
}

@keyframes lensPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.4); }
}

.gallery-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 16px;
  padding: 12px 20px;
  background: rgba(255, 107, 53, 0.08);
  border: 1px solid rgba(255, 107, 53, 0.15);
  border-radius: 12px;
  font-size: 13px;
  color: var(--text-tertiary);
}

.hint-icon {
  display: flex;
  color: var(--color-orange);
}

/* Magnifier Transitions */
.magnifier-enter-active,
.magnifier-leave-active {
  transition: all 0.15s ease-out;
}

.magnifier-enter-from,
.magnifier-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* Product Details */
.product-details {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.product-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.category-badge {
  padding: 8px 18px;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(123, 44, 191, 0.1));
  border: 1px solid rgba(255, 107, 53, 0.25);
  border-radius: 24px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-orange);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-gold);
}

.rating-badge .star-icon {
  width: 14px;
  height: 14px;
}

.product-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

/* Price Card */
.price-card {
  padding: 28px;
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.12) 0%, rgba(255, 107, 53, 0.08) 100%);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
}

.price-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.price-label {
  font-size: 13px;
  color: var(--text-tertiary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.price-trend {
  padding: 4px 12px;
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 16px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-orange);
}

.price-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 16px;
}

.price-symbol {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-orange);
}

.price-amount {
  font-family: 'JetBrains Mono', monospace;
  font-size: 48px;
  font-weight: 700;
  color: var(--color-orange);
  line-height: 1;
}

.price-footer {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.review-count,
.sales-count {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Data Grid */
.data-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.data-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  transition: all 0.3s ease;
}

.data-item:hover {
  border-color: var(--border-default);
  background: var(--bg-card-hover);
}

.data-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 53, 0.1);
  border-radius: 12px;
  color: var(--color-orange);
}

.data-icon svg {
  width: 20px;
  height: 20px;
}

.data-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.data-label {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.data-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

/* Info Panels */
.info-panels {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-panel {
  padding: 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
}

.panel-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.panel-row:last-child {
  border-bottom: none;
}

.panel-label {
  font-size: 13px;
  color: var(--text-tertiary);
}

.panel-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Tags */
.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.product-tag {
  padding: 8px 16px;
  background: rgba(123, 44, 191, 0.1);
  border: 1px solid rgba(123, 44, 191, 0.2);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-purple);
}

/* Attributes */
.attributes-wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.attribute-pair {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.attr-key {
  font-size: 12px;
  color: var(--text-tertiary);
}

.attr-val {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* Action Buttons */
.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.btn-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 24px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-action .btn-icon {
  width: 20px;
  height: 20px;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-orange), var(--color-gold));
  border: none;
  color: #000;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(255, 107, 53, 0.4);
}

.btn-secondary {
  background: transparent;
  border: 1px solid rgba(255, 107, 53, 0.3);
  color: var(--color-orange);
}

.btn-secondary:hover {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.5);
}

/* Shop Card */
.shop-card {
  padding: 20px;
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.08), rgba(255, 107, 53, 0.04));
  border: 1px solid rgba(123, 44, 191, 0.15);
  border-radius: 16px;
}

.shop-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.2);
  border-radius: 16px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-cyan);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  width: fit-content;
  margin-bottom: 12px;
}

.shop-badge-icon {
  width: 14px;
  height: 14px;
}

.shop-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.shop-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.feature-tag {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

/* ============================================
   Description Panel
   ============================================ */
.description-panel {
  padding: 32px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  animation: fadeInUp 0.6s ease-out 0.2s backwards;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.panel-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.panel-deco {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--border-accent), transparent);
}

.panel-body {
  padding: 8px 0;
}

.description-text {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin: 0 0 28px 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  text-align: center;
}

.feature-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(6, 255, 165, 0.1);
  border-radius: 12px;
  color: var(--color-cyan);
}

.feature-icon svg {
  width: 22px;
  height: 22px;
}

.feature-item span {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* ============================================
   Empty State
   ============================================ */
.empty-wrapper {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.empty-card {
  text-align: center;
  padding: 48px 60px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
}

.empty-illustration {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
  background: rgba(255, 107, 53, 0.05);
  border-radius: 50%;
  color: var(--text-tertiary);
}

.empty-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.empty-desc {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0 0 28px 0;
}

.btn-back {
  padding: 14px 32px;
  background: linear-gradient(135deg, var(--color-orange), var(--color-gold));
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 107, 53, 0.4);
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 1200px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .product-hero {
    grid-template-columns: 1fr;
  }

  .gallery-main {
    max-height: 500px;
  }
}

@media (max-width: 768px) {
  .detail-nav {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .product-title {
    font-size: 22px;
  }

  .price-amount {
    font-size: 36px;
  }

  .data-grid,
  .attributes-wrapper {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .description-panel {
    padding: 24px;
  }

  .empty-card {
    padding: 32px 24px;
  }
}
</style>
