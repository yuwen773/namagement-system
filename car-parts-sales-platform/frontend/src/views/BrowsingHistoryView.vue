<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { getBrowsingHistoryApi, clearBrowsingHistoryApi } from '@/api/modules/user'
import { formatCurrency, formatRelativeTime } from '@/utils'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const clearing = ref(false)
const historyList = ref([])

onMounted(async () => {
  await fetchHistory()
})

async function fetchHistory() {
  loading.value = true
  try {
    const data = await getBrowsingHistoryApi()
    historyList.value = data || []
  } catch (error) {
    console.error('获取浏览历史失败:', error)
    ElMessage.error('获取浏览历史失败')
  } finally {
    loading.value = false
  }
}

// 按日期分组浏览历史
const groupedHistory = computed(() => {
  const groups = {}
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  const weekAgo = new Date(today)
  weekAgo.setDate(weekAgo.getDate() - 7)

  historyList.value.forEach(item => {
    const itemDate = new Date(item.viewed_at)
    let groupKey = ''

    if (itemDate >= today) {
      groupKey = 'today'
    } else if (itemDate >= yesterday) {
      groupKey = 'yesterday'
    } else if (itemDate >= weekAgo) {
      groupKey = 'week'
    } else {
      groupKey = 'older'
    }

    if (!groups[groupKey]) {
      groups[groupKey] = []
    }
    groups[groupKey].push(item)
  })

  const groupOrder = ['today', 'yesterday', 'week', 'older']
  const groupLabels = {
    today: '今天',
    yesterday: '昨天',
    week: '最近 7 天',
    older: '更早'
  }

  return groupOrder
    .filter(key => groups[key])
    .map(key => ({
      key,
      label: groupLabels[key],
      items: groups[key],
      count: groups[key].length
    }))
})

async function handleClearHistory() {
  if (historyList.value.length === 0) {
    ElMessage.warning('浏览历史已经是空的了')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要清空所有浏览历史吗？此操作不可恢复。',
      '清空浏览历史',
      {
        confirmButtonText: '清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    clearing.value = true
    await clearBrowsingHistoryApi()
    historyList.value = []
    ElMessage.success('浏览历史已清空')
  } catch {
    // 用户取消
  } finally {
    clearing.value = false
  }
}

function goToProduct(productId) {
  router.push(`/products/${productId}`)
}

async function handleAddToCart(item) {
  try {
    await cartStore.addItem(item.product_id, 1, {
      product_name: item.product_name,
      product_image: item.product_image,
      price: item.product_price
    })
    ElMessage.success('已加入购物车')
  } catch (error) {
    ElMessage.error(error.message || '加入购物车失败')
  }
}

async function handleBuyNow(item) {
  try {
    await cartStore.addItem(item.product_id, 1, {
      product_name: item.product_name,
      product_image: item.product_image,
      price: item.product_price
    })
    router.push('/checkout')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  }
}
</script>

<template>
  <div class="browsing-history-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-mesh"></div>
      <div class="header-grid"></div>
      <div class="header-circuit"></div>
      <div class="header-content">
        <div class="header-badge">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>浏览足迹</span>
        </div>
        <h1 class="page-title">浏览历史</h1>
        <p class="page-subtitle">{{ historyList.length }} 件商品</p>
      </div>
      <div class="header-circle header-circle-1"></div>
      <div class="header-circle header-circle-2"></div>
      <div class="header-circle header-circle-3"></div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Empty State -->
      <div v-if="!loading && historyList.length === 0" class="empty-state">
        <div class="empty-icon-wrapper">
          <div class="empty-icon-ring"></div>
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" width="96" height="96">
              <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
        <h2 class="empty-title">暂无浏览记录</h2>
        <p class="empty-desc">浏览过的商品会出现在这里</p>
        <button class="btn btn-primary" @click="router.push('/products')">
          <span>开始浏览</span>
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
            <path d="M13 7l5 5m0 0l-5 5m5-5H6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- History Content -->
      <div v-else class="history-content">
        <!-- Actions Bar -->
        <div class="actions-bar">
          <div class="actions-info">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>按时间分组显示</span>
          </div>
          <button
            class="btn btn-clear"
            :disabled="clearing || historyList.length === 0"
            @click="handleClearHistory"
          >
            <svg v-if="!clearing" viewBox="0 0 24 24" fill="none" width="16" height="16">
              <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else class="spin" viewBox="0 0 24 24" fill="none" width="16" height="16">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-opacity="0.25"/>
              <path d="M12 2a10 10 0 0110 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>{{ clearing ? '清空中...' : '清空历史' }}</span>
          </button>
        </div>

        <!-- History Groups -->
        <div v-if="!loading" class="history-groups">
          <div
            v-for="group in groupedHistory"
            :key="group.key"
            class="history-group"
          >
            <div class="group-header">
              <div class="group-label">{{ group.label }}</div>
              <div class="group-count">{{ group.count }} 件</div>
            </div>

            <div class="history-grid">
              <div
                v-for="item in group.items"
                :key="item.id"
                class="history-card"
                @click="goToProduct(item.product_id)"
              >
                <div class="card-image-wrapper">
                  <img
                    :src="item.product_image || 'https://placehold.co/300x300/e2e8f0/1e293b?text=No+Image'"
                    :alt="item.product_name"
                    class="card-image"
                  />
                  <div class="card-overlay">
                    <div class="overlay-actions">
                      <button class="overlay-btn" @click.stop="handleAddToCart(item)">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                          <path d="M3 3h2l.4 2M7 5h10l1.4 8.4A2 2 0 0116.4 16H7.6a2 2 0 01-2-1.6L3 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <circle cx="9" cy="21" r="1" fill="currentColor"/>
                          <circle cx="20" cy="21" r="1" fill="currentColor"/>
                        </svg>
                        加入购物车
                      </button>
                      <button class="overlay-btn overlay-btn-primary" @click.stop="handleBuyNow(item)">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                          <path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        立即购买
                      </button>
                    </div>
                  </div>
                  <div class="card-badge">
                    <svg viewBox="0 0 24 24" fill="none" width="12" height="12">
                      <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2"/>
                      <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                </div>

                <div class="card-info">
                  <h3 class="card-name">{{ item.product_name }}</h3>
                  <div class="card-footer">
                    <div class="card-price">{{ formatCurrency(item.product_price) }}</div>
                    <div class="card-time">{{ formatRelativeTime(item.viewed_at) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载浏览历史中...</p>
        </div>
      </div>
    </div>

    <!-- Bottom Decorative Elements -->
    <div class="bottom-decoration">
      <div class="deco-line deco-line-1"></div>
      <div class="deco-line deco-line-2"></div>
    </div>
  </div>
</template>

<style scoped>
.browsing-history-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  position: relative;
}

/* Page Header */
.page-header {
  position: relative;
  padding: 80px 40px 60px;
  overflow: hidden;
  background: #0f172a;
}

.header-mesh {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 40%, rgba(249, 115, 22, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 60%, rgba(59, 130, 246, 0.1), transparent),
    radial-gradient(ellipse 50% 50% at 50% 80%, rgba(34, 197, 94, 0.08), transparent);
  animation: meshMove 20s ease-in-out infinite;
}

@keyframes meshMove {
  0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
  33% { opacity: 0.7; transform: scale(1.05) rotate(-2deg); }
  66% { opacity: 0.9; transform: scale(1.08) rotate(1deg); }
}

.header-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black, transparent);
}

.header-circuit {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(90deg, transparent 49.5%, rgba(249, 115, 22, 0.1) 49.5%, rgba(249, 115, 22, 0.1) 50.5%, transparent 50.5%),
    linear-gradient(0deg, transparent 49.5%, rgba(249, 115, 22, 0.05) 49.5%, rgba(249, 115, 22, 0.05) 50.5%, transparent 50.5%);
  background-size: 120px 120px;
  background-position: 60px 60px;
  opacity: 0.5;
  animation: circuitPulse 8s ease-in-out infinite;
}

@keyframes circuitPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.header-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: rgba(249, 115, 22, 0.12);
  border: 1px solid rgba(249, 115, 22, 0.35);
  border-radius: 100px;
  color: #f97316;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.15);
  animation: badgePulse 3s ease-in-out infinite;
}

@keyframes badgePulse {
  0%, 100% { box-shadow: 0 4px 20px rgba(249, 115, 22, 0.15); }
  50% { box-shadow: 0 4px 30px rgba(249, 115, 22, 0.3); }
}

.page-title {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.03em;
  color: #ffffff;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 50%, #f97316 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 60px rgba(249, 115, 22, 0.3);
}

.page-subtitle {
  font-size: 18px;
  color: #94a3b8;
  font-weight: 500;
}

.header-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.35;
}

.header-circle-1 {
  width: 500px;
  height: 500px;
  background: #f97316;
  top: -150px;
  right: -150px;
  animation: float1 15s ease-in-out infinite;
}

.header-circle-2 {
  width: 350px;
  height: 350px;
  background: #3b82f6;
  bottom: -80px;
  left: -80px;
  animation: float2 18s ease-in-out infinite;
}

.header-circle-3 {
  width: 250px;
  height: 250px;
  background: #22c55e;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.15;
  animation: float3 12s ease-in-out infinite;
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-30px, 30px) scale(1.05); }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(40px, -20px) scale(0.95); }
}

@keyframes float3 {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.2); }
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 100px 40px;
  background: rgba(30, 41, 59, 0.4);
  border: 2px dashed rgba(71, 85, 105, 0.4);
  border-radius: 24px;
  position: relative;
  overflow: hidden;
}

.empty-state::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 70% at 50% 50%, rgba(249, 115, 22, 0.05), transparent);
  pointer-events: none;
}

.empty-icon-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 0 auto 32px;
}

.empty-icon-ring {
  position: absolute;
  inset: 0;
  border: 2px solid rgba(249, 115, 22, 0.2);
  border-radius: 50%;
  animation: ringPulse 3s ease-in-out infinite;
}

.empty-icon-ring::before {
  content: '';
  position: absolute;
  inset: 10px;
  border: 2px solid rgba(249, 115, 22, 0.15);
  border-radius: 50%;
  animation: ringPulse 3s ease-in-out infinite 0.5s;
}

@keyframes ringPulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.2; }
}

.empty-icon {
  position: absolute;
  inset: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #475569;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
  animation: iconFloat 4s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-title {
  font-size: 28px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 12px;
}

.empty-desc {
  font-size: 16px;
  color: #64748b;
  margin-bottom: 40px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(249, 115, 22, 0.5);
}

.btn-icon {
  width: 20px;
  height: 20px;
}

/* History Content */
.history-content {
  position: relative;
}

/* Actions Bar */
.actions-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 20px 24px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.actions-info {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
}

.actions-info svg {
  color: #f97316;
}

.btn-clear {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  color: #ef4444;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-clear:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  transform: translateY(-1px);
}

.btn-clear:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* History Groups */
.history-groups {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.history-group {
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid rgba(249, 115, 22, 0.2);
}

.group-label {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 12px;
}

.group-label::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(180deg, #f97316, #ea580c);
  border-radius: 2px;
}

.group-count {
  font-size: 14px;
  font-weight: 600;
  color: #94a3b8;
  padding: 6px 12px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 100px;
}

/* History Grid */
.history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.history-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.history-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.history-card:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(249, 115, 22, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 40px rgba(249, 115, 22, 0.1);
}

.history-card:hover::before {
  opacity: 1;
}

.card-image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.history-card:hover .card-image {
  transform: scale(1.1);
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
}

.history-card:hover .card-overlay {
  opacity: 1;
}

.overlay-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
}

.overlay-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(71, 85, 105, 0.6);
  border-radius: 10px;
  color: #e2e8f0;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.overlay-btn:hover {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
  transform: scale(1.05);
}

.overlay-btn-primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-color: transparent;
  color: #ffffff;
}

.overlay-btn-primary:hover {
  background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%);
  color: #ffffff;
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.4);
}

.card-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 32px;
  height: 32px;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #f97316;
  backdrop-filter: blur(10px);
}

.card-info {
  padding: 16px;
}

.card-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
  min-height: 42px;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.card-price {
  font-size: 18px;
  font-weight: 800;
  color: #f97316;
}

.card-time {
  font-size: 12px;
  color: #64748b;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  color: #94a3b8;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(249, 115, 22, 0.2);
  border-top-color: #f97316;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-state p {
  font-size: 14px;
}

/* Bottom Decoration */
.bottom-decoration {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  pointer-events: none;
  z-index: 1;
}

.deco-line {
  position: absolute;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.5), transparent);
}

.deco-line-1 {
  bottom: 100px;
  left: 0;
  right: 0;
  animation: lineMove1 8s ease-in-out infinite;
}

.deco-line-2 {
  bottom: 80px;
  left: 0;
  right: 0;
  animation: lineMove2 10s ease-in-out infinite;
  opacity: 0.5;
}

@keyframes lineMove1 {
  0%, 100% { transform: translateX(-5%); opacity: 0.8; }
  50% { transform: translateX(5%); opacity: 0.3; }
}

@keyframes lineMove2 {
  0%, 100% { transform: translateX(5%); opacity: 0.4; }
  50% { transform: translateX(-5%); opacity: 0.7; }
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 60px 20px 40px;
  }

  .history-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
  }

  .actions-bar {
    flex-direction: column;
    gap: 16px;
  }

  .card-name {
    font-size: 13px;
    min-height: 40px;
  }

  .card-price {
    font-size: 16px;
  }

  .overlay-actions {
    padding: 12px;
  }

  .overlay-btn {
    padding: 10px 16px;
    font-size: 12px;
  }
}
</style>
