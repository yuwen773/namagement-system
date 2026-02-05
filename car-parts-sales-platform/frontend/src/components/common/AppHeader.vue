<template>
  <header class="app-header">
    <!-- 顶部通知栏 -->
    <div class="top-bar">
      <div class="top-bar-container">
        <div class="welcome-text">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>欢迎来到汽车改装件销售推荐平台</span>
        </div>
        <div class="top-links">
          <template v-if="authStore.isAuthenticated">
            <!-- 管理员专属入口 -->
            <router-link v-if="authStore.user?.is_staff" to="/admin/dashboard" class="top-link admin-link">
              <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              后台管理
            </router-link>
            <router-link to="/user" class="top-link">
              <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
              个人中心
            </router-link>
            <router-link to="/orders" class="top-link">
              <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 2v6a2 2 0 002 2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M16 13H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M16 17H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M10 9H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              我的订单
            </router-link>
            <a href="#" class="top-link message-link" @click.prevent="handleMessageClick">
              <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                <path d="M18 8A6 6 0 006 2c0 2.97-2.16 5.56-5 5.92V10l-2 2v6a2 2 0 002 2h8a2 2 0 002-2v-6l-2-2v-2.08A6 6 0 0018 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span v-if="unreadCount > 0" class="badge-count">{{ unreadCount }}</span>
              消息中心
            </a>
            <a href="#" class="top-link logout-link" @click.prevent="handleLogout">
              <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="16 17 21 12 16 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              退出登录
            </a>
          </template>
          <template v-else>
            <router-link to="/login" class="top-link login-link">请登录</router-link>
            <router-link to="/register" class="top-link register-link">免费注册</router-link>
          </template>
        </div>
      </div>
    </div>

    <!-- 主头部 -->
    <div class="main-header">
      <div class="main-header-container">
        <!-- Logo -->
        <router-link to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" width="32" height="32">
              <path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z" fill="currentColor"/>
            </svg>
          </div>
          <div class="logo-text">
            <span class="logo-name">CAR PARTS</span>
            <span class="logo-tag">PRO</span>
          </div>
        </router-link>

        <!-- 搜索框 -->
        <div class="search-container">
          <div class="search-box">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" width="18" height="18">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
              <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索您需要的改装件..."
              class="search-input"
              @keyup.enter="handleSearch"
            />
            <button class="search-button" @click="handleSearch">搜索</button>
          </div>
          <!-- 热门搜索词 -->
          <div class="hot-keywords">
            <span class="hot-label">热门:</span>
            <a v-for="keyword in hotKeywords" :key="keyword" href="#" class="hot-keyword" @click.prevent="handleHotSearch(keyword)">
              {{ keyword }}
            </a>
          </div>
        </div>

        <!-- 购物车 -->
        <router-link to="/cart" class="cart-link">
          <svg class="cart-icon" viewBox="0 0 24 24" fill="none" width="22" height="22">
            <path d="M3 3h2l.4 2M7 5h10l1.4 8.4A2 2 0 0116.4 16H7.6A2 2 0 015.6 14L3 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="9" cy="21" r="1" fill="currentColor"/>
            <circle cx="20" cy="21" r="1" fill="currentColor"/>
          </svg>
          <span class="cart-text">购物车</span>
          <span v-if="cartStore.totalQuantity > 0" class="cart-badge">{{ cartStore.totalQuantity }}</span>
        </router-link>
      </div>
    </div>

    <!-- 导航菜单 -->
    <nav class="nav-bar">
      <div class="nav-container">
        <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="9 22 9 12 15 12 15 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>首页</span>
        </router-link>
        <router-link to="/products" class="nav-item" :class="{ active: isActive('/products') }">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <rect x="3" y="3" width="7" height="7" stroke="currentColor" stroke-width="2"/>
            <rect x="14" y="3" width="7" height="7" stroke="currentColor" stroke-width="2"/>
            <rect x="14" y="14" width="7" height="7" stroke="currentColor" stroke-width="2"/>
            <rect x="3" y="14" width="7" height="7" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>全部商品</span>
        </router-link>

        <!-- 分类下拉 -->
        <div class="nav-dropdown" @mouseenter="showCategories = true" @mouseleave="showCategories = false">
          <button class="nav-item dropdown-toggle">
            <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
              <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>商品分类</span>
            <svg class="dropdown-arrow" viewBox="0 0 24 24" fill="none" width="14" height="14">
              <polyline points="6 9 12 15 18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <transition name="dropdown">
            <div v-show="showCategories" class="dropdown-menu">
              <router-link
                v-for="category in topCategories"
                :key="category.id"
                :to="`/products?category=${category.id}`"
                class="dropdown-item"
              >
                <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ category.name }}
              </router-link>
            </div>
          </transition>
        </div>

        <router-link to="/products?sort=-sales" class="nav-item" :class="{ active: $route.query.sort === '-sales' }">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M12 2c0 0-4 4-4 9 0 2.5 2 4 2 6s-2 3-2 5c0 2.5 2.5 5 6 5s6-2.5 6-5c0-2-2-3-2-5s2-3.5 2-6c0-5-4-9-4-9z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>热销排行</span>
        </router-link>
        <router-link to="/products?sort=-created_at" class="nav-item" :class="{ active: $route.query.sort === '-created_at' }">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l8.91-1.01L12 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>新品上市</span>
        </router-link>
        <router-link to="/user/coupons" class="nav-item coupon-link">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M20 12v8H4v-8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 12V6a2 2 0 012-2h12a2 2 0 012 2v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 2v20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 6l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>领券中心</span>
          <span class="new-tag">NEW</span>
        </router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCategoryListApi } from '@/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const cartStore = useCartStore()

// 搜索关键词
const searchKeyword = ref('')
const showCategories = ref(false)

// 未读消息数量（模拟数据）
const unreadCount = ref(0)

// 顶级分类（从API动态获取）
const topCategories = ref([])

// 热门搜索词
const hotKeywords = ref(['刹车片', '避震器', '进气系统', '大灯', '轮毂'])

// 判断是否激活
const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}

// 搜索
const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  router.push({
    path: '/products',
    query: { search: searchKeyword.value }
  })
}

// 热门搜索
const handleHotSearch = (keyword) => {
  router.push({
    path: '/products',
    query: { search: keyword }
  })
}

// 消息中心点击
const handleMessageClick = () => {
  router.push('/user/messages')
}

// 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    authStore.logout()
    cartStore.clearCart()
    ElMessage.success('已退出登录')
    router.push('/')
  } catch {
    // 取消退出
  }
}

// 初始化
onMounted(async () => {
  // 获取分类列表
  try {
    // 使用较大的page_size获取所有分类
    const response = await getCategoryListApi({ page: 1, page_size: 100 })
    // 响应拦截器已返回data对象，格式为 { count, results }
    // 只显示顶级分类（没有父分类的）
    const allCategories = response?.results || []
    console.log('分类数据:', allCategories.filter(c => !c.parent))  // 调试日志
    topCategories.value = allCategories.filter(c => !c.parent)
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }

  // 获取购物车
  if (authStore.isAuthenticated) {
    try {
      await cartStore.fetchCart()
    } catch (error) {
      console.error('获取购物车失败:', error)
    }
  }
})
</script>

<style scoped>
.app-header {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(71, 85, 105, 0.5);
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* 顶部栏 */
.top-bar {
  background: rgba(30, 41, 59, 0.5);
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
}

.top-bar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 36px;
}

.welcome-text {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #94a3b8;
}

.welcome-text svg {
  color: #f97316;
}

.top-links {
  display: flex;
  gap: 20px;
}

.top-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 12px;
  transition: all 0.2s ease;
  position: relative;
}

.top-link:hover {
  color: #f97316;
}

.badge-count {
  position: absolute;
  top: -4px;
  right: -8px;
  min-width: 14px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  background: #ef4444;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  border-radius: 100px;
}

.login-link:hover {
  color: #e2e8f0;
}

.register-link {
  color: #f97316;
  font-weight: 600;
}

.logout-link:hover {
  color: #ef4444;
}

.admin-link {
  color: #f97316;
  font-weight: 600;
}

.admin-link:hover {
  color: #ea580c;
}

/* 主头部 */
.main-header {
  padding: 16px 0;
}

.main-header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 40px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 12px;
  color: #ffffff;
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-name {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.logo-tag {
  font-size: 10px;
  font-weight: 700;
  color: #f97316;
  letter-spacing: 0.1em;
}

/* 搜索容器 */
.search-container {
  flex: 1;
  max-width: 560px;
}

.search-box {
  display: flex;
  align-items: center;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  padding: 4px;
  transition: all 0.3s ease;
}

.search-box:focus-within {
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
  margin: 0 12px;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  color: #e2e8f0;
  font-size: 14px;
  outline: none;
}

.search-input::placeholder {
  color: #64748b;
}

.search-button {
  padding: 8px 16px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.search-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.hot-keywords {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
  padding-left: 46px;
}

.hot-label {
  font-size: 11px;
  color: #64748b;
}

.hot-keyword {
  font-size: 12px;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.2s ease;
}

.hot-keyword:hover {
  color: #f97316;
}

/* 购物车 */
.cart-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  color: #e2e8f0;
  text-decoration: none;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.cart-link:hover {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
}

.cart-icon {
  color: #94a3b8;
}

.cart-text {
  font-size: 14px;
  font-weight: 500;
}

.cart-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  border-radius: 100px;
}

/* 导航栏 */
.nav-bar {
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
  position: relative;
}

.nav-item:hover {
  color: #e2e8f0;
  background: rgba(30, 41, 59, 0.3);
}

.nav-item.active {
  color: #f97316;
  background: rgba(249, 115, 22, 0.1);
}

.nav-item svg {
  color: currentColor;
}

.coupon-link {
  position: relative;
}

.coupon-link .new-tag {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 2px 6px;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: #ffffff;
  font-size: 9px;
  font-weight: 700;
  border-radius: 4px;
  line-height: 1;
}

/* 下拉菜单 */
.nav-dropdown {
  position: relative;
}

.dropdown-toggle {
  all: unset;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-dropdown:hover .dropdown-toggle {
  color: #e2e8f0;
  background: rgba(30, 41, 59, 0.3);
}

.dropdown-arrow {
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
}

.nav-dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 180px;
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 13px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.dropdown-item svg {
  color: #64748b;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* 响应式 */
@media (max-width: 1200px) {
  .hot-keywords {
    display: none;
  }
}

@media (max-width: 1024px) {
  .top-bar {
    display: none;
  }

  .main-header-container {
    gap: 20px;
  }

  .search-container {
    max-width: 400px;
  }
}

@media (max-width: 768px) {
  .main-header-container {
    flex-wrap: wrap;
  }

  .logo-text {
    display: none;
  }

  .search-container {
    order: 3;
    flex-basis: 100%;
    max-width: none;
  }

  .hot-keywords {
    display: none;
  }

  .nav-container {
    overflow-x: auto;
    gap: 2px;
  }

  .nav-item {
    padding: 10px 12px;
    font-size: 13px;
    white-space: nowrap;
  }

  .cart-text {
    display: none;
  }

  .dropdown-menu {
    position: fixed;
    left: 20px;
    right: 20px;
    top: auto;
  }
}
</style>
