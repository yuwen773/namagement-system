<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getProductDetailApi, getProductReviewsApi, createProductReviewApi, getProductListApi } from '@/api'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { addBrowsingHistoryApi } from '@/api/modules/user'
import { formatCurrency, fromNow } from '@/utils'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const loading = ref(false)
const product = ref(null)
const notFound = ref(false)
const reviews = ref([])
const selectedImage = ref(0)
const quantity = ref(1)

// Image zoom states
const zoomActive = ref(false)
const zoomPosition = ref({ x: 0, y: 0 })
const imageContainerRef = ref(null)

// Review images
const reviewImages = ref([])
const imagePreviewVisible = ref(false)
const previewImageUrl = ref('')

const newReview = ref({
  rating: 5,
  comment: ''
})
const showReviewForm = ref(false)

onMounted(async () => {
  await fetchProduct()
  await fetchReviews()
})

async function fetchProduct() {
  loading.value = true
  notFound.value = false
  try {
    const data = await getProductDetailApi(route.params.id)
    product.value = data
    selectedImage.value = 0

    // Track browsing history for logged-in users (静默失败，不影响主流程)
    if (authStore.isAuthenticated) {
      try {
        await addBrowsingHistoryApi({
          product_id: data.id,
          product_name: data.name,
          product_image: data.main_image || data.image,
          product_price: data.price
        })
      } catch (error) {
        // 浏览历史记录失败静默处理
        console.error('Failed to track browsing history:', error)
      }
    }

    // Fetch related products
    await fetchRelatedProducts()
  } catch (error) {
    // 错误已在拦截器中显示，这里只设置状态
    if (error.response?.status === 404) {
      notFound.value = true
    }
    product.value = null
  } finally {
    loading.value = false
  }
}

async function fetchReviews() {
  try {
    const data = await getProductReviewsApi(route.params.id)
    reviews.value = data.results || []
  } catch (error) {
    console.error('Failed to fetch reviews:', error)
  }
}

function handleAddToCart() {
  cartStore.addItem(product.value.id, quantity.value)
  ElMessage.success('已加入购物车')
}

function handleBuyNow() {
  handleAddToCart()
  router.push('/cart')
}

async function submitReview() {
  if (!newReview.value.comment) {
    ElMessage.warning('请输入评价内容')
    return
  }

  try {
    const reviewData = {
      ...newReview.value,
      images: reviewImages.value
    }
    await createProductReviewApi(route.params.id, reviewData)
    ElMessage.success('评价提交成功')
    newReview.value = { rating: 5, comment: '' }
    reviewImages.value = []
    showReviewForm.value = false
    await fetchReviews()
  } catch (error) {
    ElMessage.error(error.message || '评价提交失败')
  }
}

const averageRating = computed(() => {
  if (reviews.value.length === 0) return 0
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  return (sum / reviews.value.length).toFixed(1)
})

const stockStatus = computed(() => {
  if (!product.value) return ''
  const stock = product.value.stock_quantity || 0
  if (stock === 0) return 'out'
  if (stock < 10) return 'low'
  return 'available'
})

const stockText = computed(() => {
  if (!product.value) return ''
  const stock = product.value.stock_quantity || 0
  if (stock === 0) return '缺货'
  if (stock < 10) return `库存紧张 (仅剩 ${stock} 件)`
  return `库存充足 (${stock} 件可售)`
})

const discountPercent = computed(() => {
  if (!product.value?.original_price || product.value.original_price <= product.value.price) return 0
  return Math.round(((product.value.original_price - product.value.price) / product.value.original_price) * 100)
})

// Image zoom handlers
function handleMouseMove(event) {
  if (!imageContainerRef.value) return

  const rect = imageContainerRef.value.getBoundingClientRect()
  const x = ((event.clientX - rect.left) / rect.width) * 100
  const y = ((event.clientY - rect.top) / rect.height) * 100

  zoomPosition.value = { x, y }
}

function handleMouseEnter() {
  zoomActive.value = true
}

function handleMouseLeave() {
  zoomActive.value = false
}

// Review image handlers
function handleReviewImageUpload(file) {
  // In production, upload to server and get URL
  // For now, create a local preview URL
  const url = URL.createObjectURL(file.raw)
  reviewImages.value.push(url)
  return false // Prevent auto upload
}

function removeReviewImage(index) {
  reviewImages.value.splice(index, 1)
}

function previewImage(url) {
  previewImageUrl.value = url
  imagePreviewVisible.value = true
}

// Related products (same category products)
const relatedProducts = ref([])

async function fetchRelatedProducts() {
  if (!product.value?.category?.id) return

  try {
    const data = await getProductListApi({
      category: product.value.category.id,
      page: 1,
      page_size: 4
    })
    // Filter out current product
    relatedProducts.value = data.results?.filter(p => p.id !== product.value.id).slice(0, 4) || []
  } catch (error) {
    console.error('Failed to fetch related products:', error)
  }
}
</script>

<template>
  <div class="product-detail-view">
    <!-- Breadcrumb -->
    <div class="breadcrumb-nav">
      <div class="breadcrumb-container">
        <router-link to="/" class="breadcrumb-link">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          首页
        </router-link>
        <span class="breadcrumb-separator">/</span>
        <router-link to="/products" class="breadcrumb-link">商品列表</router-link>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-current">{{ product?.name || '商品详情' }}</span>
      </div>
    </div>

    <!-- 商品不存在提示 -->
    <div v-if="notFound || (!loading && !product)" class="not-found-container">
      <div class="not-found-content">
        <div class="not-found-icon">
          <svg viewBox="0 0 24 24" fill="none" width="80" height="80">
            <path d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2 class="not-found-title">商品不存在</h2>
        <p class="not-found-desc">抱歉，您访问的商品可能已下架或不存在</p>
        <div class="not-found-actions">
          <router-link to="/products" class="btn btn-primary">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            浏览商品
          </router-link>
          <router-link to="/" class="btn btn-secondary">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            返回首页
          </router-link>
        </div>
      </div>
    </div>

    <div v-else v-loading="loading" class="detail-container">
      <!-- Product Gallery -->
      <div class="product-gallery">
        <div
          ref="imageContainerRef"
          class="main-image-container"
          @mousemove="handleMouseMove"
          @mouseenter="handleMouseEnter"
          @mouseleave="handleMouseLeave"
        >
          <img
            :src="product?.images?.[selectedImage]?.image || product?.image"
            :alt="product?.name"
            class="main-image"
            :class="{ 'zoom-active': zoomActive }"
            :style="zoomActive ? {
              transformOrigin: `${zoomPosition.x}% ${zoomPosition.y}%`,
              transform: 'scale(2)'
            } : {}"
          />
          <div v-if="discountPercent > 0" class="discount-badge">
            -{{ discountPercent }}%
          </div>
          <div v-if="zoomActive" class="zoom-hint">
            悬停查看放大细节
          </div>
        </div>

        <div v-if="product?.images?.length" class="thumbnails-container">
          <div
            v-for="(img, index) in product.images"
            :key="img.id"
            :class="['thumbnail-item', { active: selectedImage === index }]"
            @click="selectedImage = index"
          >
            <img :src="img.image" :alt="`${product.name} - ${index + 1}`" />
          </div>
        </div>
      </div>

      <!-- Product Info -->
      <div class="product-info-section">
        <!-- Category Badge -->
        <div class="product-category-badge">
          <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
            <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2"/>
          </svg>
          {{ product?.category?.name || '配件' }}
        </div>

        <!-- Product Title -->
        <h1 class="product-title">{{ product?.name }}</h1>

        <!-- Rating & Stock -->
        <div class="product-meta-row">
          <div class="rating-display">
            <div class="stars">
              <svg v-for="i in 5" :key="i" class="star-icon" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l8.91-1.01L12 2z"
                  :fill="i <= Math.round(averageRating) ? 'currentColor' : 'none'"
                  stroke="currentColor"
                  stroke-width="2"
                />
              </svg>
            </div>
            <span class="rating-value">{{ averageRating }}</span>
            <span class="review-count">({{ reviews.length }} 条评价)</span>
          </div>
          <div :class="['stock-status', stockStatus]">
            <span class="status-dot"></span>
            {{ stockText }}
          </div>
        </div>

        <!-- Price Section -->
        <div class="price-section">
          <div class="price-main">
            <span class="price-label">价格</span>
            <div class="price-values">
              <span class="current-price">{{ formatCurrency(product?.price) }}</span>
              <span v-if="product?.original_price && product.original_price > product.price" class="original-price">
                {{ formatCurrency(product.original_price) }}
              </span>
            </div>
          </div>
          <div v-if="discountPercent > 0" class="savings-tag">
            节省 {{ formatCurrency(product.original_price - product.price) }}
          </div>
        </div>

        <!-- Description -->
        <div class="product-description">
          <p>{{ product?.description }}</p>
        </div>

        <!-- Quantity Selector -->
        <div class="quantity-section">
          <span class="quantity-label">数量</span>
          <div class="quantity-controls">
            <button
              class="qty-btn"
              @click="quantity = Math.max(1, quantity - 1)"
              :disabled="quantity <= 1"
            >
              <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                <path d="M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
            <input v-model.number="quantity" type="number" min="1" :max="product?.stock_quantity" class="qty-input" />
            <button
              class="qty-btn"
              @click="quantity++"
              :disabled="quantity >= (product?.stock_quantity || 999)"
            >
              <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="btn btn-cart" @click="handleAddToCart" :disabled="stockStatus === 'out'">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
              <path d="M3 3h2l3.6 15.4A2 2 0 0010.5 20h8.9a2 2 0 001.9-1.4L23 8H6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="9" cy="21" r="1" fill="currentColor"/>
              <circle cx="20" cy="21" r="1" fill="currentColor"/>
            </svg>
            <span>加入购物车</span>
          </button>
          <button class="btn btn-buy" @click="handleBuyNow" :disabled="stockStatus === 'out'">
            <span>立即购买</span>
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
              <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <!-- Product Attributes -->
        <div v-if="product?.attributes?.length" class="attributes-section">
          <h3 class="attributes-title">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            规格参数
          </h3>
          <div class="attributes-grid">
            <div v-for="attr in product.attributes" :key="attr.id" class="attribute-item">
              <span class="attribute-name">{{ attr.name }}</span>
              <span class="attribute-value">{{ attr.value }}</span>
            </div>
          </div>
        </div>

        <!-- Service Guarantees -->
        <div class="service-guarantees">
          <div class="guarantee-item">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
              <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>正品保证</span>
          </div>
          <div class="guarantee-item">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
              <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>7天退换</span>
          </div>
          <div class="guarantee-item">
            <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
              <rect x="1" y="3" width="15" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
              <path d="M16 8h4a2 2 0 012 2v8a2 2 0 01-2 2H6a2 2 0 01-2-2v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>顺丰包邮</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Reviews Section -->
    <div class="reviews-section">
      <div class="section-header">
        <h2 class="section-title">用户评价</h2>
        <button class="btn btn-outline" @click="showReviewForm = true">
          <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          写评价
        </button>
      </div>

      <!-- Review Form -->
      <transition name="fade">
        <div v-if="showReviewForm" class="review-form-container">
          <h3 class="form-title">分享您的使用体验</h3>
          <div class="rating-selector">
            <span class="rating-label">评分:</span>
            <el-rate v-model="newReview.rating" size="large" />
          </div>
          <el-input
            v-model="newReview.comment"
            type="textarea"
            placeholder="请输入您的评价内容（不少于10个字）"
            :rows="4"
            maxlength="500"
            show-word-limit
            class="review-textarea"
          />
          <!-- Image Upload -->
          <div class="review-images-section">
            <span class="image-upload-label">添加图片（可选）:</span>
            <el-upload
              :auto-upload="false"
              :on-change="handleReviewImageUpload"
              :show-file-list="false"
              accept="image/*"
              list-type="picture-card"
              class="review-image-uploader"
            >
              <div class="upload-trigger">
                <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
                  <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span>上传图片</span>
              </div>
            </el-upload>
            <div v-if="reviewImages.length" class="uploaded-images-preview">
              <div v-for="(img, index) in reviewImages" :key="index" class="uploaded-image-item">
                <img :src="img" @click="previewImage(img)" />
                <button class="remove-image-btn" @click="removeReviewImage(index)">
                  <svg viewBox="0 0 24 24" fill="none" width="14" height="14">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="form-actions">
            <button class="btn btn-cancel" @click="showReviewForm = false">取消</button>
            <button class="btn btn-submit" @click="submitReview">提交评价</button>
          </div>
        </div>
      </transition>

      <!-- Reviews List -->
      <div class="reviews-list">
        <div v-if="reviews.length === 0" class="empty-reviews">
          <svg viewBox="0 0 24 24" fill="none" width="64" height="64">
            <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>暂无评价，成为第一个评价的人吧！</p>
        </div>
        <div v-for="review in reviews" :key="review.id" class="review-card">
          <div class="review-header">
            <div class="reviewer-info">
              <div class="reviewer-avatar">{{ review.user?.nickname?.charAt(0) || 'U' }}</div>
              <div class="reviewer-meta">
                <span class="reviewer-name">{{ review.user?.nickname || '用户' }}</span>
                <span class="review-date">{{ fromNow(review.created_at) }}</span>
              </div>
            </div>
            <div class="review-rating">
              <svg v-for="i in review.rating" :key="i" class="review-star" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l8.91-1.01L12 2z"/>
              </svg>
            </div>
          </div>
          <p class="review-comment">{{ review.comment }}</p>
          <!-- Review Images -->
          <div v-if="review.images?.length" class="review-images">
            <div
              v-for="(img, imgIndex) in review.images"
              :key="imgIndex"
              class="review-image-item"
              @click="previewImage(img)"
            >
              <img :src="img" :alt="`评价图片 ${imgIndex + 1}`" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Related Products Section -->
    <div v-if="relatedProducts.length" class="related-products-section">
      <div class="section-header-centered">
        <h2 class="section-title">相关推荐</h2>
        <p class="section-subtitle">更多同类型商品供您选择</p>
      </div>
      <div class="related-products-grid">
        <router-link
          v-for="relatedProduct in relatedProducts"
          :key="relatedProduct.id"
          :to="`/product/${relatedProduct.id}`"
          class="related-product-card"
        >
          <div class="related-product-image">
            <img :src="relatedProduct.image || relatedProduct.images?.[0]?.image" :alt="relatedProduct.name" />
            <div v-if="relatedProduct.original_price && relatedProduct.original_price > relatedProduct.price" class="related-discount-badge">
              -{{ Math.round(((relatedProduct.original_price - relatedProduct.price) / relatedProduct.original_price) * 100) }}%
            </div>
          </div>
          <div class="related-product-info">
            <h3 class="related-product-name">{{ relatedProduct.name }}</h3>
            <div class="related-product-price-row">
              <span class="related-product-price">{{ formatCurrency(relatedProduct.price) }}</span>
              <span v-if="relatedProduct.sales" class="related-product-sales">已售 {{ relatedProduct.sales }}</span>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Image Preview Dialog -->
    <el-dialog
      v-model="imagePreviewVisible"
      :show-close="true"
      :append-to-body="true"
      class="image-preview-dialog"
    >
      <img :src="previewImageUrl" alt="预览图片" class="preview-image" />
    </el-dialog>
  </div>
</template>

<style scoped>
.product-detail-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 20px 0 60px;
}

/* Not Found State */
.not-found-container {
  max-width: 600px;
  margin: 80px auto;
  padding: 0 20px;
}

.not-found-content {
  text-align: center;
  padding: 60px 40px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.not-found-icon {
  margin-bottom: 24px;
  color: #64748b;
}

.not-found-title {
  font-size: 28px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
}

.not-found-desc {
  font-size: 15px;
  color: #94a3b8;
  margin-bottom: 32px;
}

.not-found-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.not-found-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.not-found-actions .btn-primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
}

.not-found-actions .btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

.not-found-actions .btn-secondary {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  color: #e2e8f0;
}

.not-found-actions .btn-secondary:hover {
  border-color: #f97316;
  color: #f97316;
}

.not-found-actions .btn svg {
  color: currentColor;
}

/* Breadcrumb Navigation */
.breadcrumb-nav {
  margin-bottom: 24px;
}

.breadcrumb-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.breadcrumb-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: #f97316;
}

.breadcrumb-link svg {
  color: #64748b;
}

.breadcrumb-separator {
  color: #475569;
  font-size: 12px;
}

.breadcrumb-current {
  font-size: 13px;
  color: #e2e8f0;
  font-weight: 500;
}

/* Detail Container */
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  margin-bottom: 60px;
}

/* Product Gallery */
.product-gallery {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.main-image-container {
  position: relative;
  aspect-ratio: 1;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.main-image-container:hover .main-image {
  transform: scale(1.05);
}

.main-image.zoom-active {
  cursor: crosshair;
}

.zoom-hint {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 16px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  font-size: 12px;
  color: #ffffff;
  pointer-events: none;
}

.discount-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  border-radius: 8px;
}

.thumbnails-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.thumbnail-item {
  aspect-ratio: 1;
  border: 2px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.thumbnail-item:hover,
.thumbnail-item.active {
  border-color: #f97316;
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2);
}

.thumbnail-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Product Info Section */
.product-info-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.product-category-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 100px;
  color: #f97316;
  font-size: 12px;
  font-weight: 600;
  width: fit-content;
}

.product-category-badge svg {
  color: #f97316;
}

.product-title {
  font-size: 28px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.3;
}

.product-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star-icon {
  width: 18px;
  height: 18px;
  color: #fbbf24;
}

.rating-value {
  font-size: 16px;
  font-weight: 700;
  color: #fbbf24;
}

.review-count {
  font-size: 13px;
  color: #94a3b8;
}

.stock-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}

.stock-status .status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.stock-status.available {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.stock-status.low {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.stock-status.out {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

/* Price Section */
.price-section {
  padding: 24px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
}

.price-main {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 12px;
}

.price-label {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

.price-values {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.current-price {
  font-size: 36px;
  font-weight: 800;
  color: #f97316;
}

.original-price {
  font-size: 18px;
  color: #64748b;
  text-decoration: line-through;
}

.savings-tag {
  padding: 4px 12px;
  background: rgba(34, 197, 94, 0.15);
  border-radius: 6px;
  color: #22c55e;
  font-size: 13px;
  font-weight: 600;
}

/* Description */
.product-description {
  padding: 20px;
  background: rgba(30, 41, 59, 0.3);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 12px;
}

.product-description p {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.7;
}

/* Quantity Selector */
.quantity-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quantity-label {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  min-width: 60px;
}

.quantity-controls {
  display: flex;
  align-items: center;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  overflow: hidden;
}

.qty-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.5);
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.qty-btn:hover:not(:disabled) {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-input {
  width: 70px;
  height: 44px;
  background: none;
  border: none;
  text-align: center;
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
}

.qty-input:focus {
  outline: none;
}

.qty-input::-webkit-inner-spin-button,
.qty-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-cart {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  color: #e2e8f0;
}

.btn-cart:hover:not(:disabled) {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
}

.btn-buy {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
}

.btn-buy:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-outline:hover {
  border-color: #f97316;
  color: #f97316;
}

/* Attributes Section */
.attributes-section {
  padding: 20px;
  background: rgba(30, 41, 59, 0.3);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 12px;
}

.attributes-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 16px;
}

.attributes-title svg {
  color: #f97316;
}

.attributes-grid {
  display: grid;
  gap: 12px;
}

.attribute-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(71, 85, 105, 0.2);
}

.attribute-item:last-child {
  border-bottom: none;
}

.attribute-name {
  font-size: 13px;
  color: #94a3b8;
}

.attribute-value {
  font-size: 13px;
  color: #e2e8f0;
  font-weight: 600;
}

/* Service Guarantees */
.service-guarantees {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.guarantee-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: rgba(30, 41, 59, 0.3);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 10px;
  text-align: center;
}

.guarantee-item svg {
  color: #f97316;
}

.guarantee-item span {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
}

/* Reviews Section */
.reviews-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
}

.review-form-container {
  padding: 24px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  margin-bottom: 32px;
}

.form-title {
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 20px;
}

.rating-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.rating-label {
  font-size: 14px;
  font-weight: 600;
  color: #94a3b8;
}

.review-textarea :deep(.el-textarea__inner) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #e2e8f0;
}

.review-textarea :deep(.el-textarea__inner):focus {
  border-color: #f97316;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn-cancel {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  border-color: #64748b;
  color: #e2e8f0;
}

.btn-submit {
  padding: 10px 24px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.4);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-reviews {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-reviews svg {
  margin-bottom: 16px;
  color: #475569;
}

.empty-reviews p {
  font-size: 14px;
}

.review-card {
  padding: 20px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
}

.reviewer-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.reviewer-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.review-date {
  font-size: 12px;
  color: #64748b;
}

.review-rating {
  display: flex;
  gap: 2px;
}

.review-star {
  width: 16px;
  height: 16px;
  color: #fbbf24;
}

.review-comment {
  font-size: 14px;
  color: #94a3b8;
  line-height: 1.6;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Review Images Section */
.review-images-section {
  margin-top: 16px;
}

.image-upload-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 12px;
}

.review-image-uploader {
  margin-bottom: 16px;
}

.upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px dashed rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-trigger:hover {
  border-color: #f97316;
  background: rgba(249, 115, 22, 0.05);
}

.upload-trigger svg {
  color: #64748b;
}

.upload-trigger span {
  font-size: 13px;
  color: #94a3b8;
}

.uploaded-images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
}

.uploaded-image-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
}

.uploaded-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.remove-image-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-image-btn:hover {
  background: #ef4444;
}

.remove-image-btn svg {
  color: #ffffff;
}

/* Review Images Display */
.review-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.review-image-item {
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.review-image-item:hover {
  transform: scale(1.05);
}

.review-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Related Products Section */
.related-products-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.section-header-centered {
  text-align: center;
  margin-bottom: 40px;
}

.section-subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 8px;
}

.related-products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.related-product-card {
  display: block;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s ease;
}

.related-product-card:hover {
  border-color: #f97316;
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(249, 115, 22, 0.2);
}

.related-product-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.related-product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.related-product-card:hover .related-product-image img {
  transform: scale(1.1);
}

.related-discount-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  border-radius: 6px;
}

.related-product-info {
  padding: 16px;
}

.related-product-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-product-price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.related-product-price {
  font-size: 18px;
  font-weight: 800;
  color: #f97316;
}

.related-product-sales {
  font-size: 12px;
  color: #64748b;
}

/* Image Preview Dialog */
.image-preview-dialog {
  background: transparent;
}

.image-preview-dialog :deep(.el-dialog) {
  background: transparent;
  box-shadow: none;
}

.image-preview-dialog :deep(.el-dialog__header) {
  display: none;
}

.image-preview-dialog :deep(.el-dialog__body) {
  padding: 0;
  background: transparent;
}

.preview-image {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 12px;
  display: block;
}

/* Responsive */
@media (max-width: 1024px) {
  .detail-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .product-gallery {
    position: static;
  }

  .service-guarantees {
    grid-template-columns: 1fr;
  }

  .related-products-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

@media (max-width: 640px) {
  .product-title {
    font-size: 22px;
  }

  .current-price {
    font-size: 28px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .related-products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .uploaded-images-preview,
  .review-images {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
