<template>
  <div class="approval-page">
    <!-- 背景装饰 -->
    <div class="bg-gradient-1"></div>
    <div class="bg-gradient-2"></div>
    <div class="bg-grid"></div>

    <!-- 主容器 -->
    <div class="container">
      <!-- 页头 -->
      <header class="page-header">
        <div class="header-content">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M19 21V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5m-4 0h4"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">房间绑定审核</h1>
            <p class="page-subtitle">Review and manage room binding requests</p>
          </div>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-row">
          <div class="stat-card stat-pending">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ pendingCount }}</span>
              <span class="stat-label">待审核</span>
            </div>
          </div>
          <div class="stat-card stat-total">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ userCount }}</span>
              <span class="stat-label">申请人数</span>
            </div>
          </div>
          <div class="stat-card stat-rooms">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ roomCount }}</span>
              <span class="stat-label">申请房间</span>
            </div>
          </div>
        </div>
      </header>

      <!-- 申请列表 -->
      <main class="requests-section">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else-if="pendingRequests.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="empty-title">暂无待审核申请</h3>
          <p class="empty-desc">当前没有需要处理的房间绑定申请</p>
        </div>

        <div v-else class="requests-grid">
          <div
            v-for="(request, index) in pendingRequests"
            :key="request.user_id"
            class="request-card"
            :style="{ animationDelay: `${index * 80}ms` }"
          >
            <!-- 卡片头部 -->
            <div class="card-header">
              <div class="user-info">
                <div class="user-avatar">
                  {{ (request.real_name || request.username).charAt(0).toUpperCase() }}
                </div>
                <div class="user-details">
                  <span class="user-name">{{ request.real_name || request.username }}</span>
                  <span class="user-handle">@{{ request.username }}</span>
                </div>
              </div>
              <div class="request-badge">
                <span class="badge-dot"></span>
                待审核
              </div>
            </div>

            <!-- 房间列表 -->
            <div class="rooms-container">
              <div class="rooms-label">申请房间 ({{ request.rooms.length }})</div>
              <div class="rooms-list">
                <div
                  v-for="room in request.rooms"
                  :key="room.id"
                  class="room-item"
                >
                  <div class="room-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                    </svg>
                  </div>
                  <div class="room-details">
                    <span class="room-number">{{ room.room_number }}</span>
                    <span class="room-location">{{ room.building_name }} · {{ room.floor_name }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="card-actions">
              <button
                class="action-btn btn-reject"
                @click="handleReject(request)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                拒绝
              </button>
              <button
                class="action-btn btn-approve"
                @click="handleApprove(request)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                批准
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getAllPendingBindRequests, approveBindRequest } from '@/api/system'

const loading = ref(false)
const pendingRequests = ref([])

const pendingCount = computed(() => pendingRequests.value.length)
const userCount = computed(() => pendingRequests.value.length)
const roomCount = computed(() =>
  pendingRequests.value.reduce((sum, req) => sum + req.rooms.length, 0)
)

async function loadPendingRequests() {
  loading.value = true
  try {
    const response = await getAllPendingBindRequests()
    pendingRequests.value = response.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('加载待审核申请失败')
  } finally {
    loading.value = false
  }
}

async function handleApprove(request) {
  try {
    await approveBindRequest({
      user_id: request.user_id,
      room_ids: request.rooms.map(r => r.id),
      approve: true
    })

    // 动画移除卡片
    const index = pendingRequests.value.findIndex(r => r.user_id === request.user_id)
    if (index > -1) {
      pendingRequests.value.splice(index, 1)
    }

    ElMessage.success({
      message: `已批准 ${request.real_name || request.username} 的绑定申请`,
      duration: 2500,
      customClass: 'approval-toast'
    })
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

async function handleReject(request) {
  try {
    await approveBindRequest({
      user_id: request.user_id,
      room_ids: request.rooms.map(r => r.id),
      approve: false
    })

    // 动画移除卡片
    const index = pendingRequests.value.findIndex(r => r.user_id === request.user_id)
    if (index > -1) {
      pendingRequests.value.splice(index, 1)
    }

    ElMessage.success({
      message: `已拒绝 ${request.real_name || request.username} 的绑定申请`,
      duration: 2500,
      customClass: 'approval-toast'
    })
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  loadPendingRequests()
})
</script>

<style scoped>
/* ==================== 基础样式 ==================== */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

.approval-page {
  min-height: 100vh;
  padding: 32px;
  font-family: 'Noto Sans SC', 'Poppins', sans-serif;
  position: relative;
  overflow-x: hidden;
  background: linear-gradient(135deg, #fef7f0 0%, #fdf6e3 50%, #fef3ec 100%);
}

/* ==================== 背景装饰 ==================== */
.bg-gradient-1 {
  position: fixed;
  top: -30%;
  right: -10%;
  width: 60%;
  height: 60%;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.15) 0%, transparent 70%);
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}

.bg-gradient-2 {
  position: fixed;
  bottom: -20%;
  left: -10%;
  width: 50%;
  height: 50%;
  background: radial-gradient(circle, rgba(249, 115, 22, 0.1) 0%, transparent 70%);
  filter: blur(60px);
  pointer-events: none;
  z-index: 0;
}

.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(251, 191, 36, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(251, 191, 36, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* ==================== 容器 ==================== */
.container {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
}

/* ==================== 页头 ==================== */
.page-header {
  margin-bottom: 40px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.header-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  border-radius: 20px;
  color: #fff;
  box-shadow:
    0 8px 24px rgba(251, 191, 36, 0.35),
    0 0 0 1px rgba(251, 191, 36, 0.1),
    inset 0 -2px 0 rgba(0, 0, 0, 0.1);
}

.header-icon svg {
  width: 32px;
  height: 32px;
}

.header-text {
  flex: 1;
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  letter-spacing: -0.5px;
}

.page-subtitle {
  font-family: 'Poppins', 'Noto Sans SC', sans-serif;
  font-size: 15px;
  color: #9ca3af;
  margin: 4px 0 0 0;
  letter-spacing: 0.5px;
}

/* ==================== 统计卡片 ==================== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.04),
    0 0 0 1px rgba(0, 0, 0, 0.02);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.02);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.stat-pending .stat-icon {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #d97706;
}

.stat-total .stat-icon {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #2563eb;
}

.stat-rooms .stat-icon {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  color: #16a34a;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: 'Poppins', sans-serif;
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
  color: #1f2937;
}

.stat-label {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 4px;
}

/* ==================== 主内容区 ==================== */
.requests-section {
  min-height: 300px;
}

/* ==================== 加载状态 ==================== */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(251, 191, 36, 0.2);
  border-top-color: #fbbf24;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  margin-top: 16px;
  color: #9ca3af;
  font-size: 14px;
}

/* ==================== 空状态 ==================== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  animation: fadeInUp 0.5s ease-out;
}

.empty-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 24px;
  color: #22c55e;
  margin-bottom: 24px;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.empty-desc {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

/* ==================== 申请卡片网格 ==================== */
.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
}

.request-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.06),
    0 0 0 1px rgba(0, 0, 0, 0.02);
  padding: 24px;
  animation: cardEnter 0.5s cubic-bezier(0.4, 0, 0.2, 1) both;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes cardEnter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.request-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 12px 32px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(0, 0, 0, 0.02);
}

/* ==================== 卡片头部 ==================== */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #fff;
  font-family: 'Poppins', sans-serif;
  font-size: 18px;
  font-weight: 600;
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.user-handle {
  font-family: 'Poppins', sans-serif;
  font-size: 13px;
  color: #9ca3af;
}

.request-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #d97706;
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: #f59e0b;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ==================== 房间容器 ==================== */
.rooms-container {
  margin-bottom: 20px;
}

.rooms-label {
  font-size: 13px;
  font-weight: 500;
  color: #9ca3af;
  margin-bottom: 12px;
}

.rooms-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.room-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.room-item:hover {
  background: rgba(251, 191, 36, 0.06);
  border-color: rgba(251, 191, 36, 0.2);
}

.room-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(251, 191, 36, 0.1);
  color: #f59e0b;
  border-radius: 10px;
  flex-shrink: 0;
}

.room-icon svg {
  width: 18px;
  height: 18px;
}

.room-details {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.room-number {
  font-family: 'Poppins', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.room-location {
  font-size: 13px;
  color: #9ca3af;
}

/* ==================== 操作按钮 ==================== */
.card-actions {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 14px;
  font-weight: 500;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.btn-reject {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.btn-reject:hover {
  background: rgba(239, 68, 68, 0.15);
  transform: translateY(-1px);
}

.btn-approve {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
}

.btn-approve:hover {
  box-shadow: 0 6px 16px rgba(251, 191, 36, 0.4);
  transform: translateY(-1px);
}

/* ==================== 淡入动画 ==================== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ==================== 响应式 ==================== */
@media (max-width: 768px) {
  .approval-page {
    padding: 20px 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .stats-row {
    grid-template-columns: 1fr;
  }

  .requests-grid {
    grid-template-columns: 1fr;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

<!-- 全局Toast样式 -->
<style>
.approval-toast {
  font-family: 'Noto Sans SC', sans-serif !important;
  border-radius: 12px !important;
  padding: 12px 20px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}
</style>
