<template>
  <div class="crawler-config-container">
    <!-- 页面头部 -->
    <div class="config-header">
      <div class="header-content">
        <h1 class="page-title">爬虫配置中心</h1>
        <p class="page-subtitle">配置采集凭证以启用数据采集功能</p>
      </div>
      <div class="header-status">
        <div class="status-badge" :class="statusClass">
          <span class="status-dot"></span>
          <span class="status-text">{{ statusText }}</span>
        </div>
      </div>
    </div>

    <!-- 主内容网格 -->
    <div class="config-layout">
      <!-- 左侧：配置表单 -->
      <div class="config-main">
        <!-- Cookie 配置卡片 -->
        <div class="config-card config-card--primary">
          <div class="card-header">
            <div class="header-left">
              <div class="card-icon card-icon--orange">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M12 6v6l4 2"></path>
                </svg>
              </div>
              <div class="header-text">
                <h2 class="card-title">Cookie 配置</h2>
                <p class="card-subtitle">淘宝/天猫 采集凭证</p>
              </div>
            </div>
          </div>

          <div class="card-body">
            <!-- Cookie 输入 -->
            <div class="form-group">
              <div class="form-label-row">
                <label class="form-label">
                  <span class="label-text">Cookie 值</span>
                  <span class="label-required">*</span>
                </label>
                <button
                  class="visibility-toggle"
                  @click="showCookie = !showCookie"
                  type="button"
                >
                  <svg v-if="showCookie" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
              </div>
              <div class="input-wrapper">
                <el-input
                  v-model="configForm.taobao_cookie"
                  :type="showCookie ? 'textarea' : 'password'"
                  :rows="showCookie ? 5 : 2"
                  placeholder="粘贴从浏览器获取的完整 Cookie..."
                  class="config-input"
                />
                <div class="input-border"></div>
              </div>
              <p class="form-hint">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
                从浏览器开发者工具 Network 标签中复制请求头中的 Cookie
              </p>
            </div>

            <!-- 测试结果 -->
            <transition name="result">
              <div v-if="configForm.test_result" class="result-banner" :class="resultClass">
                <div class="result-icon">
                  <svg v-if="isTestSuccess" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                  <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="15" y1="9" x2="9" y2="15"></line>
                    <line x1="9" y1="9" x2="15" y2="15"></line>
                  </svg>
                </div>
                <div class="result-content">
                  <span class="result-title">{{ resultTitle }}</span>
                  <span class="result-message">{{ configForm.test_result }}</span>
                  <span v-if="configForm.last_test_time" class="result-time">{{ formatTime(configForm.last_test_time) }}</span>
                </div>
              </div>
            </transition>

            <!-- 操作按钮 -->
            <div class="form-actions">
              <button
                class="btn btn--primary"
                @click="saveConfig"
                :disabled="saving || !configForm.taobao_cookie"
                :class="{ loading: saving }"
              >
                <svg v-if="!saving" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
                <svg v-else class="spinning" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="2" x2="12" y2="6"></line>
                  <line x1="12" y1="18" x2="12" y2="22"></line>
                  <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
                  <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
                  <line x1="2" y1="12" x2="6" y2="12"></line>
                  <line x1="18" y1="12" x2="22" y2="12"></line>
                  <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
                  <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
                </svg>
                <span>{{ saving ? '保存中...' : '保存配置' }}</span>
              </button>
              <button
                class="btn btn--secondary"
                @click="testCookie"
                :disabled="testing || !configForm.taobao_cookie"
                :class="{ loading: testing }"
              >
                <svg v-if="!testing" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path>
                </svg>
                <svg v-else class="spinning" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="2" x2="12" y2="6"></line>
                  <line x1="12" y1="18" x2="12" y2="22"></line>
                  <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
                  <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
                  <line x1="2" y1="12" x2="6" y2="12"></line>
                  <line x1="18" y1="12" x2="22" y2="12"></line>
                  <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
                  <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
                </svg>
                <span>{{ testing ? '测试中...' : '测试连接' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 状态概览卡片 -->
        <div class="status-grid">
          <div class="status-card" :class="{ active: configForm.cookie_status !== 'not_configured' }">
            <div class="status-card-icon status-card-icon--orange">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <div class="status-card-content">
              <span class="status-card-label">配置状态</span>
              <span class="status-card-value">{{ statusText }}</span>
            </div>
          </div>
          <div class="status-card" :class="{ active: configForm.last_test_time }">
            <div class="status-card-icon status-card-icon--purple">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="status-card-content">
              <span class="status-card-label">最后测试</span>
              <span class="status-card-value">{{ configForm.last_test_time ? formatTime(configForm.last_test_time) : '未测试' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：帮助信息 -->
      <div class="config-sidebar">
        <!-- 获取指南 -->
        <div class="guide-card">
          <div class="guide-header">
            <div class="guide-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
            </div>
            <div>
              <h3 class="guide-title">Cookie 获取指南</h3>
              <p class="guide-subtitle">按步骤操作获取有效凭证</p>
            </div>
          </div>

          <div class="guide-steps">
            <div
              v-for="(step, index) in cookieSteps"
              :key="index"
              class="guide-step"
            >
              <span class="step-number">{{ String(index + 1).padStart(2, '0') }}</span>
              <div class="step-content">
                <span class="step-title">{{ step.title }}</span>
                <span class="step-desc">{{ step.description }}</span>
              </div>
            </div>
          </div>

          <div class="guide-footer">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span>Cookie 仅用于数据采集，请妥善保管</span>
          </div>
        </div>

        <!-- 快速提示 -->
        <div class="tips-card">
          <h4 class="tips-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
            快速提示
          </h4>
          <ul class="tips-list">
            <li class="tips-item">Cookie 有效期通常为 7-30 天</li>
            <li class="tips-item">测试失败请重新获取 Cookie</li>
            <li class="tips-item">配置后无需重启服务即可生效</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const configForm = reactive({
  taobao_cookie: '',
  cookie_status: 'not_configured',
  last_test_time: null,
  test_result: ''
})

const showCookie = ref(false)
const saving = ref(false)
const testing = ref(false)

const cookieSteps = [
  {
    title: '打开淘宝网站',
    description: '访问 www.taobao.com 并登录账号'
  },
  {
    title: '打开开发者工具',
    description: '按 F12 或右键选择"检查"'
  },
  {
    title: '切换 Network 标签',
    description: '在开发者工具中找到 Network 选项'
  },
  {
    title: '刷新或搜索',
    description: '按 F5 刷新或搜索任意商品'
  },
  {
    title: '查找请求',
    description: '点击列表中的任意请求'
  },
  {
    title: '复制 Cookie',
    description: 'Headers → Request Headers → Cookie'
  }
]

// 计算属性
const statusClass = computed(() => {
  const classes = {
    not_configured: 'status-empty',
    configured: 'status-pending',
    tested: 'status-success',
    failed: 'status-error'
  }
  return classes[configForm.cookie_status] || 'status-empty'
})

const statusText = computed(() => {
  const texts = {
    not_configured: '未配置',
    configured: '已配置',
    tested: '测试通过',
    failed: '测试失败'
  }
  return texts[configForm.cookie_status] || '未知'
})

const isTestSuccess = computed(() => {
  if (!configForm.test_result) return false
  const result = configForm.test_result.toLowerCase()
  return result.includes('成功') ||
         result.includes('success') ||
         result.includes('通过') ||
         result.includes('有效')
})

const resultClass = computed(() => {
  return isTestSuccess.value ? 'result-success' : 'result-error'
})

const resultTitle = computed(() => {
  return isTestSuccess.value ? '测试通过' : '测试失败'
})

// 方法
const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadConfig = async () => {
  try {
    const response = await request.get('/users/configs/crawler/')
    if (response.code === 0) {
      const data = response.data || {}
      if (!configForm.taobao_cookie && data.taobao_cookie) {
        if (!data.taobao_cookie.includes('...')) {
          configForm.taobao_cookie = data.taobao_cookie
        }
      }
      configForm.cookie_status = data.cookie_status || 'not_configured'
      configForm.last_test_time = data.last_test_time || null
      configForm.test_result = data.test_result || ''
    }
  } catch (error) {
    console.log('Config not yet set:', error.message)
    configForm.cookie_status = 'not_configured'
  }
}

const saveConfig = async () => {
  if (!configForm.taobao_cookie.trim()) {
    ElMessage.warning('Cookie 不能为空')
    return
  }

  saving.value = true
  try {
    const response = await request.post('/users/configs/crawler/', {
      taobao_cookie: configForm.taobao_cookie
    })
    if (response.code === 0) {
      ElMessage.success('配置保存成功')
      configForm.cookie_status = 'configured'
    }
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const testCookie = async () => {
  testing.value = true
  try {
    const response = await request.post('/users/configs/crawler/test-cookie/')
    if (response.code === 0) {
      ElMessage.success('Cookie 测试成功')
      configForm.test_result = '测试通过，Cookie 有效'
      loadConfig()
    } else {
      const errorMsg = response.message || '测试失败'
      ElMessage.error(errorMsg)
      configForm.test_result = errorMsg
      loadConfig()
    }
  } catch (error) {
    let errorMsg = '测试失败'
    if (error.response && error.response.data && error.response.data.message) {
      errorMsg = error.response.data.message
    } else if (error.message) {
      errorMsg = error.message
    }
    ElMessage.error(errorMsg)
    configForm.test_result = errorMsg
  } finally {
    testing.value = false
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* ============================================
   Design Tokens
   ============================================ */
.crawler-config-container {
  --orange: #FF6B35;
  --orange-rgb: 255, 107, 53;
  --purple: #7B2CBF;
  --purple-rgb: 123, 44, 191;
  --gold: #FFD700;
  --cyan: #06FFA5;
  --red: #FF3B30;

  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --bg-input: rgba(0, 0, 0, 0.25);

  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);

  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-focus: rgba(var(--orange-rgb), 0.5);

  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ============================================
   Header
   ============================================ */
.config-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.header-content {
  flex: 1;
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border-radius: 24px;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.status-badge.status-empty {
  color: var(--text-tertiary);
  border: 1px solid var(--border-subtle);
}

.status-badge.status-pending {
  color: var(--gold);
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.status-badge.status-success {
  color: var(--cyan);
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.2);
}

.status-badge.status-error {
  color: var(--red);
  background: rgba(255, 59, 48, 0.1);
  border: 1px solid rgba(255, 59, 48, 0.2);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-badge.status-success .status-dot {
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ============================================
   Layout
   ============================================ */
.config-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
}

@media (max-width: 1200px) {
  .config-layout {
    grid-template-columns: 1fr;
  }
}

/* ============================================
   Config Card
   ============================================ */
.config-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.config-card--primary {
  position: relative;
}

.config-card--primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--orange), var(--purple));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.config-card--primary:hover::before {
  opacity: 1;
}

.config-card:hover {
  border-color: var(--border-default);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 20px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.card-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.card-icon--orange {
  background: rgba(var(--orange-rgb), 0.15);
  color: var(--orange);
}

.card-icon--purple {
  background: rgba(var(--purple-rgb), 0.15);
  color: var(--purple);
}

.card-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.card-body {
  padding: 24px;
}

/* ============================================
   Form Elements
   ============================================ */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.label-required {
  color: var(--red);
}

.visibility-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.visibility-toggle:hover {
  background: var(--bg-card-hover);
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
}

.config-input {
  --el-input-bg-color: var(--bg-input);
  --el-input-border-color: var(--border-subtle);
  --el-input-text-color: var(--text-primary);
  --el-input-placeholder-color: var(--text-tertiary);
  --el-input-focus-border-color: var(--border-focus);
}

.config-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  padding: 14px 16px;
  transition: all 0.2s ease;
}

.config-input :deep(.el-textarea__inner):focus {
  box-shadow: 0 0 0 3px rgba(var(--orange-rgb), 0.1);
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--orange), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.config-input:focus-within + .input-border {
  opacity: 0.5;
}

.form-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.form-hint svg {
  flex-shrink: 0;
  color: var(--purple);
}

/* ============================================
   Result Banner
   ============================================ */
.result-banner {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  border: 1px solid;
  background: rgba(0, 0, 0, 0.2);
}

.result-success {
  border-color: rgba(6, 255, 165, 0.3);
  background: rgba(6, 255, 165, 0.05);
}

.result-error {
  border-color: rgba(255, 59, 48, 0.3);
  background: rgba(255, 59, 48, 0.05);
}

.result-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  flex-shrink: 0;
}

.result-success .result-icon {
  color: var(--cyan);
}

.result-error .result-icon {
  color: var(--red);
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.result-title {
  font-size: 14px;
  font-weight: 600;
}

.result-success .result-title {
  color: var(--cyan);
}

.result-error .result-title {
  color: var(--red);
}

.result-message {
  font-size: 13px;
  color: var(--text-secondary);
}

.result-time {
  font-size: 11px;
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
}

.result-enter-active,
.result-leave-active {
  transition: all 0.3s ease;
}

.result-enter-from,
.result-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ============================================
   Buttons
   ============================================ */
.form-actions {
  display: flex;
  gap: 12px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  padding: 0 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
}

.btn--primary {
  background: linear-gradient(135deg, var(--orange), var(--purple));
  border: none;
  color: white;
}

.btn--primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(var(--orange-rgb), 0.3);
}

.btn--primary:disabled,
.btn--primary.loading {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn--secondary {
  background: transparent;
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--bg-card-hover);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.btn--secondary:disabled,
.btn--secondary.loading {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn svg {
  flex-shrink: 0;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============================================
   Status Grid
   ============================================ */
.status-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 24px;
}

.status-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.status-card.active {
  border-color: rgba(var(--orange-rgb), 0.3);
  background: rgba(var(--orange-rgb), 0.05);
}

.status-card-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.status-card-icon--orange {
  background: rgba(var(--orange-rgb), 0.15);
  color: var(--orange);
}

.status-card-icon--purple {
  background: rgba(var(--purple-rgb), 0.15);
  color: var(--purple);
}

.status-card-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.status-card-label {
  font-size: 11px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.status-card-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

/* ============================================
   Sidebar
   ============================================ */
.config-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ============================================
   Guide Card
   ============================================ */
.guide-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 20px;
}

.guide-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.guide-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--purple-rgb), 0.15);
  color: var(--purple);
  border-radius: 10px;
}

.guide-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.guide-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.guide-step {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  position: relative;
  padding-left: 44px;
}

.guide-step::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, var(--orange), var(--purple));
  border-radius: 3px 0 0 3px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.guide-step:hover {
  border-color: rgba(var(--orange-rgb), 0.2);
  background: rgba(var(--orange-rgb), 0.05);
}

.guide-step:hover::before {
  opacity: 1;
}

.step-number {
  position: absolute;
  left: 8px;
  top: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: var(--orange);
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.step-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.step-desc {
  font-size: 12px;
  color: var(--text-tertiary);
}

.guide-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
  font-size: 12px;
  color: var(--text-tertiary);
}

.guide-footer svg {
  flex-shrink: 0;
  color: var(--purple);
}

/* ============================================
   Tips Card
   ============================================ */
.tips-card {
  background: linear-gradient(135deg, rgba(6, 255, 165, 0.05), rgba(6, 255, 165, 0.02));
  backdrop-filter: blur(20px);
  border: 1px solid rgba(6, 255, 165, 0.1);
  border-radius: 20px;
  padding: 20px;
}

.tips-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--cyan);
  margin: 0 0 14px 0;
}

.tips-title svg {
  flex-shrink: 0;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tips-item {
  position: relative;
  padding-left: 16px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.tips-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 7px;
  width: 6px;
  height: 6px;
  background: var(--cyan);
  border-radius: 50%;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
  .config-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .status-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
