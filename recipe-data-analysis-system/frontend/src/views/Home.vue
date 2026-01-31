<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-gradient"></div>
        <div class="hero-pattern">
          <svg v-for="i in 20" :key="i" class="floating-icon" :style="{ '--delay': `${i * 0.3}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 100}%` }" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1" opacity="0.15"/>
          </svg>
        </div>
      </div>

      <div class="hero-content">
        <div class="hero-badge">探索 20,000+ 精选菜谱</div>
        <h1 class="hero-title">
          <span class="title-line">发现</span>
          <span class="title-line highlight">美食的奥秘</span>
        </h1>
        <p class="hero-description">
          数据驱动的美食发现之旅，探索八大菜系，解锁烹饪秘籍
        </p>
        <div class="hero-actions">
          <router-link to="/recipes" class="btn-primary">
            <span>开始探索</span>
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 10h12m0 0l-4-4m4 4l-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </router-link>
          <router-link to="/hot" class="btn-secondary">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2c-2 0-3.5 1.5-4 3.5C7.5 3.5 6 2 4 2 1.5 2 0 4.5 0 7.5c0 4 5 8.5 10 12.5 5-4 10-8.5 10-12.5C20 4.5 18.5 2 16 2c-2 0-3.5 1.5-4 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>热门菜谱</span>
          </router-link>
        </div>

        <!-- 统计数据 -->
        <div class="hero-stats">
          <div class="stat-item" v-for="stat in stats" :key="stat.label">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 快速入口 -->
    <section class="quick-access-section">
      <div class="section-container">
        <div class="quick-access-grid">
          <router-link to="/recipes" class="quick-card cuisine-card">
            <div class="card-icon">
              <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="4" y="8" width="32" height="26" rx="3" stroke="currentColor" stroke-width="2"/>
                <path d="M4 16L36 16" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
                <circle cx="18" cy="12" r="1.5" fill="currentColor"/>
              </svg>
            </div>
            <div class="card-content">
              <h3>全部菜谱</h3>
              <p>浏览 20,000+ 菜谱</p>
            </div>
            <div class="card-arrow">
              <svg viewBox="0 0 16 16" fill="none">
                <path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </router-link>

          <router-link to="/category/cuisine" class="quick-card category-card">
            <div class="card-icon">
              <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 8h10M8 14h10M8 20h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="28" cy="14" r="8" stroke="currentColor" stroke-width="2"/>
                <path d="M25 14h6M28 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="card-content">
              <h3>菜系分类</h3>
              <p>八大菜系任你选</p>
            </div>
            <div class="card-arrow">
              <svg viewBox="0 0 16 16" fill="none">
                <path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </router-link>

          <router-link to="/hot" class="quick-card hot-card">
            <div class="card-icon">
              <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 5c-3 0-5 2-5 5 0 2-2 3-3 3-3 0-5 3-5 7 0 5 6 10 13 15 7-5 13-10 13-15 0-4-2-7-5-7-1 0-3-1-3-3 0-3-2-5-5-5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="card-content">
              <h3>热门推荐</h3>
              <p>最受欢迎的菜谱</p>
            </div>
            <div class="card-arrow">
              <svg viewBox="0 0 16 16" fill="none">
                <path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 菜系预览 -->
    <section class="cuisine-preview-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L15 9L22 9L17 14L19 21L12 17L5 21L7 14L2 9L9 9L12 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            探索菜系
          </h2>
          <router-link to="/category/cuisine" class="view-all-link">
            查看全部
            <svg viewBox="0 0 16 16" fill="none">
              <path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </router-link>
        </div>

        <div class="cuisine-grid">
          <router-link
            v-for="cuisine in cuisines"
            :key="cuisine.name"
            :to="`/category/cuisine/${cuisine.name}`"
            class="cuisine-card"
            :style="{ '--accent-color': cuisine.color }"
          >
            <div class="cuisine-image" :style="{ backgroundImage: `url(${cuisine.image})` }">
              <div class="cuisine-overlay"></div>
            </div>
            <div class="cuisine-info">
              <span class="cuisine-emoji">{{ cuisine.emoji }}</span>
              <h3 class="cuisine-name">{{ cuisine.name }}</h3>
              <p class="cuisine-desc">{{ cuisine.desc }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- 功能特色 -->
    <section class="features-section">
      <div class="section-container">
        <div class="section-header centered">
          <h2 class="section-title">为什么选择我们</h2>
          <p class="section-subtitle">数据驱动的美食发现平台</p>
        </div>

        <div class="features-grid">
          <div class="feature-card" v-for="(feature, index) in features" :key="index">
            <div class="feature-icon" :style="{ '--delay': `${index * 0.1}s` }">
              <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" v-html="feature.icon"></svg>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-container">
        <div class="cta-content">
          <h2 class="cta-title">准备好开启美食之旅了吗？</h2>
          <p class="cta-description">加入我们的社区，探索无限可能</p>
          <div class="cta-actions">
            <router-link v-if="!userStore.isLoggedIn" to="/register" class="btn-primary large">
              免费注册
            </router-link>
            <router-link to="/recipes" class="btn-secondary large">
              浏览菜谱
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 统计数据
const stats = [
  { value: '20K+', label: '菜谱' },
  { value: '8', label: '菜系' },
  { value: '500+', label: '食材' },
  { value: '10K+', label: '用户' }
]

// 菜系数据
const cuisines = [
  // { name: '川菜', value: 'sichuan', emoji: '🌶️', desc: '麻辣鲜香', color: '#e74c3c', image: 'https://images.unsplash.com/
  // photo-1564579829002-64eb95778513?w=400&h=300&fit=crop' },
   { name: '川菜', value: 'sichuan', emoji: '🌶️', desc: '麻辣鲜香', color: '#e74c3c', image: 'https://loremflickr.com/400/300/spicy,hotpot?lock=10' },
  { name: '粤菜', value: 'cantonese', emoji: '🥢', desc: '清淡鲜美', color: '#3498db', image: 'https://images.unsplash.com/photo-1534256958597-7fe685cbd745?w=400&h=300&fit=crop' },
  { name: '湘菜', value: 'hunan', emoji: '🔥', desc: '香辣浓郁', color: '#e67e22', image: 'https://images.unsplash.com/photo-1552611052-33e04de081de?w=400&h=300&fit=crop' },
  { name: '鲁菜', value: 'shandong', emoji: '🍲', desc: '咸鲜醇厚', color: '#f39c12', image: 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400&h=300&fit=crop' },
  { name: '苏菜', value: 'jiangsu', emoji: '🐟', desc: '清淡甜美', color: '#1abc9c', image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop' },
  // { name: '浙菜', value: 'zhejiang', emoji: '🦐', desc: '鲜嫩软滑', color: '#9b59b6', image: 'https://images.unsplash.com/photo-1511690656952-34342e732595?w=400&h=300&fit=crop' },
    { name: '浙菜', value: 'zhejiang', emoji: '🦐', desc: '鲜嫩软滑', color: '#9b59b6', image: 'https://loremflickr.com/400/300/steamed,fish?lock=20' },
  { name: '闽菜', value: 'fujian', emoji: '🦀', desc: '鲜香清淡', color: '#34495e', image: 'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=400&h=300&fit=crop' },
  { name: '徽菜', value: 'anhui', emoji: '🍄', desc: '重油重色', color: '#795548', image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&h=300&fit=crop' }
]

// 功能特色
const features = [
  {
    title: '海量菜谱',
    desc: '超过 20,000 精选菜谱，涵盖八大菜系，满足各种口味需求',
    icon: '<rect x="8" y="8" width="24" height="26" rx="3" stroke="currentColor" stroke-width="2" fill="none"/><path d="M8 16h24" stroke="currentColor" stroke-width="2"/>'
  },
  {
    title: '智能搜索',
    desc: '支持菜名、食材搜索，快速找到您想做的菜谱',
    icon: '<circle cx="20" cy="20" r="10" stroke="currentColor" stroke-width="2"/><circle cx="20" cy="20" r="4" fill="currentColor"/><path d="M32 32l-8-8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
  },
  {
    title: '数据分析',
    desc: '深度分析菜谱数据，洞察烹饪趋势和口味偏好',
    icon: '<rect x="6" y="14" width="4" height="18" rx="2" stroke="currentColor" stroke-width="2" fill="none"/><rect x="16" y="6" width="4" height="26" rx="2" stroke="currentColor" stroke-width="2" fill="none"/><rect x="26" y="10" width="4" height="22" rx="2" stroke="currentColor" stroke-width="2" fill="none"/>'
  },
  {
    title: '收藏管理',
    desc: '收藏喜爱的菜谱，打造专属的美食收藏夹',
    icon: '<path d="M20 35L8 25V5h24v20L20 35z" stroke="currentColor" stroke-width="2" fill="none"/><path d="M20 30v-8" stroke="currentColor" stroke-width="2"/>'
  },
  {
    title: '详细步骤',
    desc: '每道菜谱都有详细的制作步骤，即使是新手也能轻松上手',
    icon: '<path d="M8 4h24v32H8z" stroke="currentColor" stroke-width="2" fill="none"/><path d="M14 14h12M14 20h12M14 26h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
  },
  {
    title: '社区互动',
    desc: '加入美食社区，与千万美食爱好者一起交流分享',
    icon: '<circle cx="14" cy="14" r="8" stroke="currentColor" stroke-width="2" fill="none"/><circle cx="26" cy="26" r="8" stroke="currentColor" stroke-width="2" fill="none"/><path d="M20 20l4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
  }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.home-page {
  background: #faf8f5;
  font-family: 'DM Sans', sans-serif;
}

/* ========== Hero Section ========== */
.hero-section {
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #fffaf5 0%, #faf8f5 50%, #f5f0e8 100%);
}

.hero-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(212, 119, 58, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 100% 50%, rgba(194, 98, 46, 0.1), transparent),
    radial-gradient(ellipse 60% 40% at 0% 80%, rgba(255, 107, 53, 0.08), transparent);
}

.hero-pattern {
  position: absolute;
  inset: 0;
}

.floating-icon {
  position: absolute;
  width: 24px;
  height: 24px;
  color: #c2622e;
  animation: float 6s ease-in-out infinite;
  animation-delay: var(--delay);
  left: var(--x);
  top: var(--y);
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.3; }
  50% { transform: translateY(-20px) rotate(10deg); opacity: 0.6; }
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  padding: 2rem;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(194, 98, 46, 0.1);
  color: #c2622e;
  border-radius: 24px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 2rem;
  animation: fadeInUp 0.6s ease-out;
}

.hero-title {
  font-family: 'Noto Serif SC', serif;
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.title-line {
  display: block;
  color: #3d2914;
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

.title-line.highlight {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.hero-description {
  font-size: 1.15rem;
  color: #6b5c4d;
  max-width: 500px;
  margin: 0 auto 2.5rem;
  line-height: 1.7;
  animation: fadeInUp 0.6s ease-out 0.3s both;
}

.hero-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 4rem;
  animation: fadeInUp 0.6s ease-out 0.4s both;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.75rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(194, 98, 46, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.4);
}

.btn-primary svg {
  width: 18px;
  height: 18px;
}

.btn-secondary {
  background: white;
  color: #3d2914;
  border: 1.5px solid #e5ddd3;
}

.btn-secondary:hover {
  border-color: #c2622e;
  color: #c2622e;
  background: rgba(194, 98, 46, 0.05);
}

.btn-secondary svg {
  width: 18px;
  height: 18px;
}

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
  animation: fadeInUp 0.6s ease-out 0.5s both;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-value {
  font-family: 'Noto Serif SC', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #c2622e;
}

.stat-label {
  font-size: 0.9rem;
  color: #8b7355;
}

/* ========== Section Container ========== */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* ========== Quick Access Section ========== */
.quick-access-section {
  padding: 4rem 0;
  background: white;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.quick-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  background: #faf8f5;
  border-radius: 16px;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.quick-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #d4773a, #c2622e);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.quick-card:hover::before {
  transform: scaleX(1);
}

.quick-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(61, 41, 20, 0.1);
}

.card-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 14px;
  color: #c2622e;
  flex-shrink: 0;
}

.card-icon svg {
  width: 28px;
  height: 28px;
}

.cuisine-card .card-icon {
  color: #d4773a;
}

.category-card .card-icon {
  color: #27ae60;
}

.hot-card .card-icon {
  color: #ff6b35;
}

.card-content {
  flex: 1;
}

.card-content h3 {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 0.25rem 0;
}

.card-content p {
  font-size: 0.9rem;
  color: #8b7355;
  margin: 0;
}

.card-arrow {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
  color: #b8a99a;
  transition: all 0.3s ease;
}

.quick-card:hover .card-arrow {
  color: #c2622e;
  transform: translateX(4px);
}

.card-arrow svg {
  width: 14px;
  height: 14px;
}

/* ========== Cuisine Preview Section ========== */
.cuisine-preview-section {
  padding: 5rem 0;
  background: #faf8f5;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2.5rem;
}

.section-header.centered {
  flex-direction: column;
  text-align: center;
}

.section-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(194, 98, 46, 0.1);
  border-radius: 10px;
  color: #c2622e;
}

.title-icon svg {
  width: 20px;
  height: 20px;
}

.section-subtitle {
  color: #8b7355;
  font-size: 1.1rem;
  margin-top: 0.75rem;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #c2622e;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: gap 0.2s ease;
}

.view-all-link:hover {
  gap: 0.75rem;
}

.view-all-link svg {
  width: 16px;
  height: 16px;
}

.cuisine-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.cuisine-card {
  position: relative;
  height: 220px;
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.4s ease;
  cursor: pointer;
}

.cuisine-image {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transition: transform 0.5s ease;
}

.cuisine-card:hover .cuisine-image {
  transform: scale(1.1);
}

.cuisine-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 50%, transparent 100%);
  transition: background 0.3s ease;
}

.cuisine-card:hover .cuisine-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 50%, transparent 100%);
}

.cuisine-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.5rem;
  color: white;
  z-index: 2;
}

.cuisine-emoji {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

.cuisine-name {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.cuisine-desc {
  font-size: 0.9rem;
  opacity: 0.9;
  margin: 0;
}

/* ========== Features Section ========== */
.features-section {
  padding: 5rem 0;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem 1.5rem;
}

.feature-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(212, 119, 58, 0.1) 0%, rgba(194, 98, 46, 0.1) 100%);
  border-radius: 18px;
  color: #c2622e;
  animation: fadeInUp 0.6s ease-out var(--delay) both;
}

.feature-icon svg {
  width: 32px;
  height: 32px;
}

.feature-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #3d2914;
  margin: 0 0 0.75rem 0;
}

.feature-desc {
  color: #8b7355;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* ========== CTA Section ========== */
.cta-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 50%, #a35220 100%);
}

.cta-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: 0 2rem;
}

.cta-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 1rem 0;
}

.cta-description {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.15rem;
  margin-bottom: 2rem;
}

.cta-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.btn-primary.large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.btn-secondary.large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.btn-secondary.large:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
}

/* ========== Animations ========== */
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

/* ========== Responsive Design ========== */
@media (max-width: 1024px) {
  .cuisine-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-actions {
    flex-direction: column;
  }

  .hero-stats {
    gap: 2rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .quick-access-grid {
    grid-template-columns: 1fr;
  }

  .cuisine-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .cta-actions {
    flex-direction: column;
  }

  .cta-title {
    font-size: 2rem;
  }
}
</style>
