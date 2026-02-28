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
  <div class="detail-container">
    <!-- 返回按钮 -->
    <div class="back-nav">
      <button class="back-btn" @click="goBack">
        <ArrowLeft class="back-icon" />
        返回商品列表
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载商品详情...</p>
    </div>

    <!-- 商品详情 -->
    <div v-else-if="product" class="product-detail">
      <!-- 商品主图和信息 -->
      <div class="main-section">
        <!-- 商品图片 -->
        <div class="image-gallery">
          <div
            ref="imageContainer"
            class="main-image"
            @mousemove="handleMouseMove"
            @mouseenter="handleMouseEnter"
            @mouseleave="handleMouseLeave"
          >
            <img :src="product.image_url" :alt="product.title" />

            <!-- 放大镜 -->
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
                <!-- 十字准星 -->
                <div class="crosshair horizontal"></div>
                <div class="crosshair vertical"></div>

                <!-- 角落标记 -->
                <div class="corner-mark top-left"></div>
                <div class="corner-mark top-right"></div>
                <div class="corner-mark bottom-left"></div>
                <div class="corner-mark bottom-right"></div>

                <!-- 刻度线 -->
                <div class="scale-marks">
                  <span v-for="i in 12" :key="'h-' + i" class="scale-mark horizontal"></span>
                  <span v-for="i in 12" :key="'v-' + i" class="scale-mark vertical"></span>
                </div>

                <!-- 中心发光点 -->
                <div class="center-glow"></div>

                <!-- 数据显示 -->
                <div class="lens-data">
                  <span class="data-label">ZOOM {{ ZOOM_LEVEL }}x</span>
                  <span class="data-coords">
                    {{ Math.round(cursorPos.x) }},{{ Math.round(cursorPos.y) }}
                  </span>
                </div>
              </div>
            </Transition>

            <!-- 脉冲波纹效果 -->
            <Transition name="pulse">
              <div v-if="isHovering" class="pulse-ring"></div>
            </Transition>
          </div>

          <!-- 提示文字 -->
          <div class="zoom-hint">
            <span class="hint-icon">🔍</span>
            <span>悬停查看细节</span>
          </div>
        </div>

        <!-- 商品信息 -->
        <div class="product-info">
          <div class="info-header">
            <div class="category-tag">{{ product.category || '宠物用品' }}</div>
            <h1 class="product-title">{{ product.title }}</h1>
          </div>

          <div class="price-section">
            <div class="price-label">价格</div>
            <div class="price-main">
              <span class="price-currency">¥</span>
              <span class="price-value">{{ formatPrice(product.price) }}</span>
            </div>
            <div class="price-meta">
              <span class="sales">
                <Star class="meta-icon" />
                {{ product.rating || 4.8 }} 分 ({{ product.reviews || 0 }} 条评价)
              </span>
            </div>
          </div>

          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">{{ formatSales(product.sales) }}</span>
              <span class="stat-label">累计销量</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-value">{{ product.brand || '宠物品牌' }}</span>
              <span class="stat-label">所属品牌</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-value">{{ product.shop }}</span>
              <span class="stat-label">店铺</span>
            </div>
          </div>

          <!-- 商品详细信息 -->
          <div class="detail-info-grid">
            <div class="detail-item">
              <span class="detail-label">商品ID</span>
              <span class="detail-value">{{ product.product_id || '-' }}</span>
            </div>
            <div class="detail-item" v-if="product.category">
              <span class="detail-label">类目</span>
              <span class="detail-value">{{ product.category }}</span>
            </div>
            <div class="detail-item" v-if="product.region">
              <span class="detail-label">发货地</span>
              <span class="detail-value">{{ product.region }}</span>
            </div>
            <div class="detail-item" v-if="product.seller_nick">
              <span class="detail-label">卖家</span>
              <span class="detail-value">{{ product.seller_nick }}</span>
            </div>
            <div class="detail-item" v-if="product.batch_no">
              <span class="detail-label">批次号</span>
              <span class="detail-value">{{ product.batch_no }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">采集时间</span>
              <span class="detail-value">{{ formatTime(product.crawl_time) }}</span>
            </div>
          </div>

          <!-- 商品标签 -->
          <div v-if="product.tags" class="tags-section">
            <span class="tags-label">标签</span>
            <div class="tags-list">
              <span
                v-for="(tag, index) in parseTags(product.tags)"
                :key="index"
                class="tag-item"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- 商品属性 -->
          <div v-if="product.product_attributes && Object.keys(product.product_attributes).length > 0" class="attributes-section">
            <span class="attributes-label">商品属性</span>
            <div class="attributes-list">
              <div
                v-for="(value, key) in product.product_attributes"
                :key="key"
                class="attribute-item"
              >
                <span class="attr-key">{{ key }}</span>
                <span class="attr-value">{{ value }}</span>
              </div>
            </div>
          </div>

          <div class="action-section">
            <button class="action-btn primary" @click="openTmallLink">
              <ShoppingCart class="btn-icon" />
              前往天猫购买
            </button>
            <button class="action-btn secondary" @click="openTmallLink">
              <Link class="btn-icon" />
              复制链接
            </button>
          </div>

          <div class="shop-info">
            <div class="shop-header">
              <Location class="shop-icon" />
              <span class="shop-name">{{ product.shop }}</span>
            </div>
            <p class="shop-desc">正品保障 · 优质服务 · 快速发货</p>
          </div>
        </div>
      </div>

      <!-- 商品描述 -->
      <div class="description-section">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-icon">📋</span>
            商品描述
          </h2>
        </div>
        <div class="description-content">
          <p>{{ product.description || '暂无详细描述' }}</p>
          <ul class="feature-list">
            <li>正品保障，正规渠道进货</li>
            <li>精美包装，适合收藏送礼</li>
            <li>支持七天无理由退换</li>
            <li>优质售后服务，购物无忧</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>商品不存在</h3>
      <p>该商品可能已被下架或删除</p>
      <button class="back-btn-large" @click="goBack">返回列表</button>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Share+Tech+Mono&display=swap');

.detail-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 返回导航 */
.back-nav {
  padding: 16px 0;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  border-color: rgba(255, 107, 53, 0.3);
  color: #FF6B35;
  background: rgba(255, 107, 53, 0.1);
}

.back-icon {
  width: 16px;
  height: 16px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: rgba(255, 255, 255, 0.4);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 107, 53, 0.2);
  border-top-color: #FF6B35;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 主区域 */
.main-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

/* 图片画廊 */
.image-gallery {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  align-self: start;
  position: sticky;
  top: 100px;
}

.main-image {
  aspect-ratio: 1;
  max-height: 500px;
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  cursor: crosshair;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 放大镜透镜 */
.magnifier-lens {
  position: absolute;
  border-radius: 50%;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 10;

  /* 霓虹边框效果 - 增强版 */
  box-shadow:
    0 0 0 3px rgba(255, 107, 53, 0.9),
    0 0 0 6px rgba(6, 255, 165, 0.7),
    0 0 50px rgba(255, 107, 53, 0.6),
    0 0 80px rgba(6, 255, 165, 0.3),
    inset 0 0 40px rgba(0, 0, 0, 0.4);

  /* 扫描线纹理 */
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(6, 255, 165, 0.05) 2px,
      rgba(6, 255, 165, 0.05) 4px
    );
    pointer-events: none;
  }

  /* 添加内发光效果 */
  &::after {
    content: '';
    position: absolute;
    inset: 3px;
    border-radius: 50%;
    box-shadow: inset 0 0 30px rgba(6, 255, 165, 0.2);
    pointer-events: none;
  }
}

/* 十字准星 */
.crosshair {
  position: absolute;
  background: rgba(6, 255, 165, 0.8);
  pointer-events: none;
}

.crosshair.horizontal {
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  box-shadow: 0 0 8px rgba(6, 255, 165, 0.8);
}

.crosshair.vertical {
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  box-shadow: 0 0 8px rgba(6, 255, 165, 0.8);
}

/* 角落标记 */
.corner-mark {
  position: absolute;
  width: 12px;
  height: 12px;
  pointer-events: none;
}

.corner-mark::before,
.corner-mark::after {
  content: '';
  position: absolute;
  background: #06FFA5;
  box-shadow: 0 0 6px #06FFA5;
}

.corner-mark.top-left {
  top: 8px;
  left: 8px;
}

.corner-mark.top-left::before {
  width: 10px;
  height: 2px;
  top: 0;
  left: 0;
}

.corner-mark.top-left::after {
  width: 2px;
  height: 10px;
  top: 0;
  left: 0;
}

.corner-mark.top-right {
  top: 8px;
  right: 8px;
}

.corner-mark.top-right::before {
  width: 10px;
  height: 2px;
  top: 0;
  right: 0;
}

.corner-mark.top-right::after {
  width: 2px;
  height: 10px;
  top: 0;
  right: 0;
}

.corner-mark.bottom-left {
  bottom: 8px;
  left: 8px;
}

.corner-mark.bottom-left::before {
  width: 10px;
  height: 2px;
  bottom: 0;
  left: 0;
}

.corner-mark.bottom-left::after {
  width: 2px;
  height: 10px;
  bottom: 0;
  left: 0;
}

.corner-mark.bottom-right {
  bottom: 8px;
  right: 8px;
}

.corner-mark.bottom-right::before {
  width: 10px;
  height: 2px;
  bottom: 0;
  right: 0;
}

.corner-mark.bottom-right::after {
  width: 2px;
  height: 10px;
  bottom: 0;
  right: 0;
}

/* 刻度线 */
.scale-marks {
  position: absolute;
  inset: 20px;
  pointer-events: none;
}

.scale-mark {
  position: absolute;
  background: rgba(6, 255, 165, 0.4);
}

.scale-mark.horizontal {
  width: 6px;
  height: 1px;
}

.scale-mark.vertical {
  width: 1px;
  height: 6px;
}

/* 水平刻度分布 */
.scale-mark.horizontal:nth-child(1) { top: 0%; left: 10%; }
.scale-mark.horizontal:nth-child(2) { top: 0%; left: 30%; }
.scale-mark.horizontal:nth-child(3) { top: 0%; left: 50%; }
.scale-mark.horizontal:nth-child(4) { top: 0%; left: 70%; }
.scale-mark.horizontal:nth-child(5) { top: 0%; left: 90%; }
.scale-mark.horizontal:nth-child(6) { top: 100%; left: 10%; }
.scale-mark.horizontal:nth-child(7) { top: 100%; left: 30%; }
.scale-mark.horizontal:nth-child(8) { top: 100%; left: 50%; }
.scale-mark.horizontal:nth-child(9) { top: 100%; left: 70%; }
.scale-mark.horizontal:nth-child(10) { top: 100%; left: 90%; }

/* 垂直刻度分布 */
.scale-mark.vertical:nth-child(11) { left: 0%; top: 10%; }
.scale-mark.vertical:nth-child(12) { left: 0%; top: 30%; }
.scale-mark.vertical:nth-child(13) { left: 0%; top: 50%; }
.scale-mark.vertical:nth-child(14) { left: 0%; top: 70%; }
.scale-mark.vertical:nth-child(15) { left: 0%; top: 90%; }
.scale-mark.vertical:nth-child(16) { left: 100%; top: 10%; }
.scale-mark.vertical:nth-child(17) { left: 100%; top: 30%; }
.scale-mark.vertical:nth-child(18) { left: 100%; top: 50%; }
.scale-mark.vertical:nth-child(19) { left: 100%; top: 70%; }
.scale-mark.vertical:nth-child(20) { left: 100%; top: 90%; }

/* 中心发光点 */
.center-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px;
  height: 8px;
  transform: translate(-50%, -50%);
  background: #06FFA5;
  border-radius: 50%;
  box-shadow:
    0 0 10px #06FFA5,
    0 0 20px rgba(6, 255, 165, 0.6),
    0 0 30px rgba(6, 255, 165, 0.3);
  pointer-events: none;
  animation: pulse-glow 1.5s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0.8;
  }
}

/* 数据显示 */
.lens-data {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  white-space: nowrap;
  pointer-events: none;
}

.data-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  color: #FF6B35;
  text-shadow: 0 0 10px rgba(255, 107, 53, 0.8);
  letter-spacing: 1px;
}

.data-coords {
  font-family: 'Share Tech Mono', monospace;
  font-size: 9px;
  color: rgba(6, 255, 165, 0.7);
  letter-spacing: 0.5px;
}

/* 脉冲环 */
.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  transform: translate(-50%, -50%);
  border: 2px solid rgba(6, 255, 165, 0.8);
  border-radius: 50%;
  pointer-events: none;
  animation: pulse-expand 0.8s ease-out infinite;
}

@keyframes pulse-expand {
  0% {
    width: 20px;
    height: 20px;
    opacity: 1;
  }
  100% {
    width: 100px;
    height: 100px;
    opacity: 0;
  }
}

/* 提示文字 */
.zoom-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  padding: 10px 16px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.hint-icon {
  font-size: 14px;
}

/* 过渡动画 */
.magnifier-enter-active,
.magnifier-leave-active {
  transition: all 0.2s ease-out;
}

.magnifier-enter-from,
.magnifier-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.pulse-enter-active {
  transition: all 0.3s ease-out;
}

.pulse-leave-active {
  transition: all 0.2s ease-in;
}

.pulse-enter-from,
.pulse-leave-to {
  opacity: 0;
}

/* 商品信息 */
.product-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(123, 44, 191, 0.2));
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #FF6B35;
  width: fit-content;
}

.product-title {
  font-size: 24px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  line-height: 1.4;
}

/* 价格区域 */
.price-section {
  padding: 24px;
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.1) 0%, rgba(255, 107, 53, 0.08) 100%);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 16px;
}

.price-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 8px;
}

.price-main {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 12px;
}

.price-currency {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #FF6B35;
}

.price-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 36px;
  font-weight: 700;
  color: #FF6B35;
}

.price-meta {
  display: flex;
  gap: 16px;
}

.sales {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.meta-icon {
  width: 14px;
  height: 14px;
  color: #FFD700;
}

/* 统计数据 */
.stats-grid {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-value {
  display: block;
  font-family: 'Orbitron', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
}

/* 详细信息网格 */
.detail-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* 标签区域 */
.tags-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.tags-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  padding: 6px 12px;
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  font-size: 12px;
  color: #FF6B35;
  font-weight: 500;
}

/* 属性区域 */
.attributes-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.attributes-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.attributes-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attribute-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.attr-key {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.attr-value {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* 操作按钮 */
.action-section {
  display: flex;
  gap: 16px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  border: none;
  color: #000;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
}

.action-btn.secondary {
  background: transparent;
  border: 1px solid rgba(255, 107, 53, 0.3);
  color: #FF6B35;
}

.action-btn.secondary:hover {
  background: rgba(255, 107, 53, 0.1);
  border-color: rgba(255, 107, 53, 0.5);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* 店铺信息 */
.shop-info {
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.shop-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.shop-icon {
  width: 18px;
  height: 18px;
  color: #FF6B35;
}

.shop-name {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.shop-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.title-icon {
  font-size: 20px;
}

.section-badge {
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(123, 44, 191, 0.2));
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: #FF6B35;
}

/* 描述区域 */
.description-section {
  padding: 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

.description-content {
  padding: 16px 0;
}

.description-content p {
  font-size: 14px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 20px 0;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.feature-list li::before {
  content: '✓';
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: rgba(6, 255, 165, 0.2);
  border-radius: 50%;
  font-size: 12px;
  color: #06FFA5;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 24px 0;
}

.back-btn-large {
  padding: 12px 32px;
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
}

/* 响应式 */
@media (max-width: 1024px) {
  .main-section {
    grid-template-columns: 1fr;
  }

  .feature-list {
    grid-template-columns: 1fr;
  }

  .image-gallery {
    position: static;
  }
}
</style>
