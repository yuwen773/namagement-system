<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { formatCurrency } from '@/utils/format'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const loading = ref(false)
const hotProducts = ref([])
const newProducts = ref([])
const categories = ref([])

// 模拟数据
const heroSlides = ref([
  {
    image: 'https://images.unsplash.com/photo-1619405399517-d7fce0f13302?w=1200&h=600&fit=crop',
    title: '释放你的',
    highlight: '爱车潜能',
    subtitle: '专业改装件 · 品质保证 · 极速发货'
  }
])

onMounted(async () => {
  await fetchData()
})

async function fetchData() {
  loading.value = true
  try {
    // 使用模拟数据，实际项目中从 API 获取
    hotProducts.value = [
      { id: 1, name: 'AKRAPOVIC 排气系统', category: { name: '排气' }, price: 8999, sales: 1234, image: 'https://images.unsplash.com/photo-1619405399517-d7fce0f13302?w=400&h=400&fit=crop' },
      { id: 2, name: 'BILSTEIN B16 避震器', category: { name: '避震' }, price: 12999, sales: 892, image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop' },
      { id: 3, name: 'BBS RF 轮毂 19寸', category: { name: '轮毂' }, price: 15800, sales: 567, image: 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=400&h=400&fit=crop' },
      { id: 4, name: 'BREMBO GT6 刹车套件', category: { name: '刹车' }, price: 18800, sales: 423, image: 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=400&h=400&fit=crop' }
    ]
    newProducts.value = [
      { id: 5, name: 'HKS 泄压阀', category: { name: '进气' }, price: 2999, sales: 156, image: 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400&h=400&fit=crop' },
      { id: 6, name: 'DEFI 温度表', category: { name: '仪表' }, price: 1599, sales: 234, image: 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=400&h=400&fit=crop' },
      { id: 7, name: 'Cusco 防倾杆', category: { name: '底盘' }, price: 2200, sales: 189, image: 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&h=400&fit=crop' },
      { id: 8, name: 'Project MU 刹车皮', category: { name: '刹车' }, price: 899, sales: 312, image: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=400&fit=crop' }
    ]
    categories.value = [
      { id: 1, name: '发动机系统', icon: '发动机', count: 256 },
      { id: 2, name: '底盘悬挂', icon: '底盘', count: 189 },
      { id: 3, name: '车身外观', icon: '外观', count: 342 },
      { id: 4, name: '内饰改装', icon: '内饰', count: 156 },
      { id: 5, name: '电子系统', icon: '电子', count: 98 },
      { id: 6, name: '轮胎轮毂', icon: '轮毂', count: 215 }
    ]
  } finally {
    loading.value = false
  }
}

function goToProduct(id) {
  router.push(`/products/${id}`)
}

function goToCategory(categoryId) {
  router.push({ path: '/products', query: { category: categoryId } })
}

async function addToCart(productId) {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    await cartStore.addItem(productId)
    ElMessage.success('已添加到购物车')
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}
</script>

<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-bg">
        <div class="grid-overlay"></div>
        <div class="gradient-mesh"></div>
      </div>

      <div class="hero-content">
        <div class="hero-text">
          <div class="hero-badge">PREMIUM AFTERMARKET PARTS</div>
          <h1 class="hero-title">
            <span class="title-line">释放你的</span>
            <span class="title-line title-accent">爱车潜能</span>
          </h1>
          <p class="hero-subtitle">专业改装件 · 品质保证 · 极速发货</p>
          <div class="hero-actions">
            <router-link to="/products" class="btn btn-primary">
              <span>探索改装件</span>
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </router-link>
            <router-link to="/products?sort=-created_at" class="btn btn-secondary">
              <span>新品首发</span>
            </router-link>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-value">10,000+</span>
              <span class="stat-label">商品</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-value">500+</span>
              <span class="stat-label">品牌</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-value">24/7</span>
              <span class="stat-label">支持</span>
            </div>
          </div>
        </div>

        <!-- Hero Visual -->
        <div class="hero-visual">
          <div class="product-showcase">
            <img src="https://images.unsplash.com/photo-1619405399517-d7fce0f13302?w=600&h=400&fit=crop" alt="Car Parts" class="hero-image">
            <div class="product-card-floating">
              <div class="mini-product-card">
                <img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=80&h=80&fit=crop" alt="">
                <div>
                  <p class="mini-name">BILSTEIN B16</p>
                  <p class="mini-price">¥12,999</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="scroll-indicator">
        <span>向下滚动</span>
        <div class="scroll-line"></div>
      </div>
    </section>

    <!-- Category Navigation -->
    <section class="categories-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-icon">◇</span>
            按车型选购
          </h2>
          <router-link to="/products" class="view-all-link">
            查看全部
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </router-link>
        </div>

        <div class="category-grid" v-loading="loading">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-card"
            @click="goToCategory(category.id)"
          >
            <div class="category-icon">
              <span>{{ category.icon }}</span>
            </div>
            <div class="category-info">
              <h3>{{ category.name }}</h3>
              <p>{{ category.count }}+ 商品</p>
            </div>
            <div class="category-arrow">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Hot Products -->
    <section class="products-section hot-section">
      <div class="section-bg">
        <div class="noise-texture"></div>
      </div>

      <div class="container">
        <div class="section-header-inline">
          <div class="section-label">
            <span class="label-dot"></span>
            <span>TRENDING NOW</span>
          </div>
          <h2 class="section-title-inline">本周热销</h2>
          <router-link to="/products?sort=-sales" class="view-all-link">
            查看全部
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12H19M19 12L12 5M19 12L12 19"/>
            </svg>
          </router-link>
        </div>

        <div class="product-grid" v-loading="loading">
          <div
            v-for="(product, index) in hotProducts"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <div class="product-rank" :class="`rank-${index + 1}`">
              {{ index + 1 }}
            </div>
            <div class="product-image-wrapper">
              <img :src="product.image" :alt="product.name" class="product-image">
              <div class="product-overlay">
                <button class="quick-view-btn">快速查看</button>
              </div>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <div class="product-meta">
                <span class="product-category">{{ product.category?.name }}</span>
                <span class="product-sales">已售 {{ product.sales }}+</span>
              </div>
              <div class="product-footer">
                <span class="product-price">{{ formatCurrency(product.price) }}</span>
                <button class="btn-add-cart" @click.stop="addToCart(product.id)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- New Products -->
    <section class="products-section new-section">
      <div class="container">
        <div class="section-header-inline">
          <div class="section-label section-label--accent">
            <span class="label-dot"></span>
            <span>FRESH ARRIVALS</span>
          </div>
          <h2 class="section-title-inline">新品首发</h2>
          <router-link to="/products?sort=-created_at" class="view-all-link">
            查看全部
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12H19M19 12L12 5M19 12L12 19"/>
            </svg>
          </router-link>
        </div>

        <div class="product-grid" v-loading="loading">
          <div
            v-for="product in newProducts"
            :key="product.id"
            class="product-card product-card--new"
            @click="goToProduct(product.id)"
          >
            <div class="product-badge product-badge--new">NEW</div>
            <div class="product-image-wrapper">
              <img :src="product.image" :alt="product.name" class="product-image">
              <div class="product-overlay">
                <button class="quick-view-btn">快速查看</button>
              </div>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <div class="product-meta">
                <span class="product-category">{{ product.category?.name }}</span>
                <span class="product-sales">已售 {{ product.sales }}+</span>
              </div>
              <div class="product-footer">
                <span class="product-price">{{ formatCurrency(product.price) }}</span>
                <button class="btn-add-cart" @click.stop="addToCart(product.id)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Promo Banner -->
    <section class="promo-section">
      <div class="container">
        <div class="promo-banner">
          <div class="promo-content">
            <div class="promo-text">
              <span class="promo-label">限时特惠</span>
              <h2>全场改装件满1000减200</h2>
              <p>使用优惠码: <strong>BOOST2024</strong></p>
            </div>
            <router-link to="/products" class="btn btn-promo">
              立即选购
            </router-link>
          </div>
          <div class="promo-decoration">
            <div class="deco-circle deco-1"></div>
            <div class="deco-circle deco-2"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services -->
    <section class="services-section">
      <div class="container">
        <div class="services-grid">
          <div class="service-item">
            <div class="service-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
              </svg>
            </div>
            <h3>正品保证</h3>
            <p>100% 正品，假一赔十</p>
          </div>
          <div class="service-item">
            <div class="service-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <h3>极速发货</h3>
            <p>24小时内闪电发货</p>
          </div>
          <div class="service-item">
            <div class="service-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
            <h3>专业支持</h3>
            <p>技师团队在线答疑</p>
          </div>
          <div class="service-item">
            <div class="service-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
              </svg>
            </div>
            <h3>安全支付</h3>
            <p>多种支付方式保障</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ========== Global Styles ========== */
.home-view {
  --font-display: 'Arial Black', 'Impact', sans-serif;
  --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --primary: #f97316;
  --primary-dark: #ea580c;
  --dark: #0f172a;
  --gray: #64748b;
  background: #ffffff;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ========== Hero Section ========== */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: var(--dark);
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

.gradient-mesh {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(249, 115, 22, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(59, 130, 246, 0.15) 0%, transparent 50%);
  animation: meshMove 20s ease-in-out infinite;
}

@keyframes meshMove {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(5%, 5%) scale(1.1); }
}

.hero-content {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 24px;
  z-index: 2;
}

.hero-text {
  color: #ffffff;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 20px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.3);
  color: var(--primary);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 32px;
  animation: fadeInUp 0.8s ease forwards;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(48px, 8vw, 72px);
  font-weight: 900;
  line-height: 1.1;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.title-line {
  display: block;
  opacity: 0;
  animation: fadeInUp 0.8s ease forwards;
}

.title-line:nth-child(2) {
  animation-delay: 0.2s;
}

.title-accent {
  color: var(--primary);
  position: relative;
  padding-left: 20px;
}

.title-accent::after {
  content: '';
  position: absolute;
  left: 0;
  top: 10%;
  height: 80%;
  width: 4px;
  background: var(--primary);
}

.hero-subtitle {
  font-size: 18px;
  color: #94a3b8;
  margin-bottom: 40px;
  opacity: 0;
  animation: fadeInUp 1s ease 0.4s forwards;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 64px;
  opacity: 0;
  animation: fadeInUp 1s ease 0.6s forwards;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 32px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.btn:hover .btn-icon {
  transform: translateX(4px);
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: #ffffff;
  box-shadow: 0 10px 30px rgba(249, 115, 22, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(249, 115, 22, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.hero-stats {
  display: flex;
  gap: 48px;
  padding-top: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  opacity: 0;
  animation: fadeInUp 1s ease 0.8s forwards;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
}

.stat-label {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.stat-divider {
  width: 1px;
  background: rgba(255, 255, 255, 0.1);
}

/* Hero Visual */
.hero-visual {
  position: relative;
}

.product-showcase {
  position: relative;
}

.hero-image {
  width: 100%;
  border-radius: 16px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
}

.product-card-floating {
  position: absolute;
  bottom: -20px;
  right: -20px;
}

.mini-product-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.mini-product-card img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
}

.mini-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--dark);
}

.mini-price {
  font-size: 14px;
  font-weight: 700;
  color: var(--primary);
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--gray);
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, var(--gray), transparent);
  animation: scrollPulse 2s ease-in-out infinite;
}

@keyframes scrollPulse {
  0%, 100% { opacity: 0.3; transform: scaleY(1); }
  50% { opacity: 1; transform: scaleY(1.2); }
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

/* ========== Categories Section ========== */
.categories-section {
  padding: 80px 0;
  background: #f8fafc;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 48px;
}

.section-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 900;
  color: var(--dark);
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  color: var(--primary);
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--gray);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.view-all-link:hover {
  color: var(--primary);
}

.view-all-link svg {
  width: 20px;
  height: 20px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.category-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: #ffffff;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.category-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
}

.category-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.category-info h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 4px;
}

.category-info p {
  font-size: 14px;
  color: var(--gray);
}

.category-arrow svg {
  width: 24px;
  height: 24px;
  color: #cbd5e1;
  transition: all 0.3s ease;
}

.category-card:hover .category-arrow svg {
  color: var(--primary);
  transform: translateX(4px);
}

/* ========== Products Section ========== */
.products-section {
  padding: 80px 0;
  position: relative;
}

.hot-section {
  background: #f8fafc;
}

.section-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.noise-texture {
  position: absolute;
  inset: 0;
  opacity: 0.3;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

.section-header-inline {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 48px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.2);
}

.section-label--accent {
  background: rgba(15, 23, 42, 0.05);
  border-color: rgba(15, 23, 42, 0.1);
}

.label-dot {
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.section-label span {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--primary);
}

.section-label--accent span {
  color: var(--dark);
}

.section-title-inline {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 900;
  text-transform: uppercase;
  color: var(--dark);
  flex: 1;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.product-card {
  position: relative;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
}

.product-rank {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--dark);
  color: #ffffff;
  font-weight: 900;
  font-size: 14px;
  border-radius: 8px;
  z-index: 10;
}

.product-rank.rank-1 {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
}

.product-rank.rank-2 {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.product-rank.rank-3 {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
}

.product-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 10;
  padding: 6px 12px;
  background: var(--primary);
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  border-radius: 4px;
}

.product-badge--new {
  background: var(--dark);
}

.product-image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  background: #f3f4f6;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image {
  transform: scale(1.08);
}

.product-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.8);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .product-overlay {
  opacity: 1;
}

.quick-view-btn {
  padding: 12px 24px;
  background: #ffffff;
  color: var(--dark);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transform: translateY(20px);
  transition: transform 0.3s ease;
}

.product-card:hover .quick-view-btn {
  transform: translateY(0);
}

.product-info {
  padding: 20px;
}

.product-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 13px;
}

.product-category {
  color: var(--primary);
  font-weight: 600;
}

.product-sales {
  color: var(--gray);
}

.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-price {
  font-size: 20px;
  font-weight: 900;
  color: var(--primary);
}

.btn-add-cart {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--dark);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #ffffff;
}

.btn-add-cart:hover {
  background: var(--primary);
  transform: scale(1.1);
}

.btn-add-cart svg {
  width: 20px;
  height: 20px;
}

/* ========== Promo Section ========== */
.promo-section {
  padding: 80px 0;
}

.promo-banner {
  position: relative;
  background: linear-gradient(135deg, var(--dark) 0%, #1e293b 100%);
  border-radius: 24px;
  padding: 64px;
  overflow: hidden;
}

.promo-content {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
}

.promo-label {
  display: inline-block;
  padding: 8px 16px;
  background: var(--primary);
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-radius: 100px;
  margin-bottom: 16px;
}

.promo-text h2 {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 900;
  color: #ffffff;
  margin-bottom: 12px;
}

.promo-text p {
  font-size: 18px;
  color: #94a3b8;
}

.promo-text strong {
  color: var(--primary);
  font-family: 'Courier New', monospace;
  letter-spacing: 0.1em;
}

.btn-promo {
  padding: 16px 40px;
  background: var(--primary);
  color: #ffffff;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-promo:hover {
  background: var(--primary-dark);
  transform: scale(1.05);
}

.promo-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(249, 115, 22, 0.2);
}

.deco-1 {
  width: 400px;
  height: 400px;
  top: -200px;
  right: -100px;
}

.deco-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  right: 200px;
}

/* ========== Services Section ========== */
.services-section {
  padding: 60px 0;
  background: #f8fafc;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}

.service-item {
  text-align: center;
  padding: 32px 24px;
  background: #ffffff;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.service-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
}

.service-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.service-icon svg {
  width: 32px;
  height: 32px;
}

.service-item h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 8px;
}

.service-item p {
  font-size: 14px;
  color: var(--gray);
}

/* ========== Responsive ========== */
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-actions {
    justify-content: center;
  }

  .hero-stats {
    justify-content: center;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .category-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }

  .product-grid,
  .category-grid,
  .services-grid {
    grid-template-columns: 1fr;
  }

  .promo-banner {
    padding: 32px;
  }

  .promo-content {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }

  .section-header-inline {
    flex-wrap: wrap;
  }
}
</style>
