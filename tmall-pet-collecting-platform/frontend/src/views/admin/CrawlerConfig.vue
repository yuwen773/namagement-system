<template>
  <div class="config-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="grid-overlay"></div>
      <div class="noise-texture"></div>
    </div>

    <!-- 主标题区 -->
    <header class="page-header">
      <div class="header-content">
        <div class="title-badge">
          <span class="badge-icon">⚙️</span>
          <span class="badge-text">SYSTEM CONFIG</span>
        </div>
        <h1 class="page-title">
          <span class="title-gradient">爬虫配置中心</span>
        </h1>
        <p class="page-subtitle">配置淘宝 Cookie 以启用数据采集功能</p>
      </div>
      <div class="header-visual">
        <div class="floating-icon icon-1">🦊</div>
        <div class="floating-icon icon-2">🎮</div>
        <div class="floating-icon icon-3">🎯</div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="content-grid">
      <!-- 左侧：配置卡片 -->
      <div class="left-column">
        <!-- Cookie 配置卡片 -->
        <div class="config-card glass-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper cookie-icon">
                <span>🍪</span>
              </div>
              <div>
                <h3 class="card-title">Cookie 配置</h3>
                <p class="card-subtitle">淘宝/天猫 采集凭证</p>
              </div>
            </div>
            <div class="status-indicator" :class="statusClass">
              <span class="status-dot"></span>
              <span class="status-text">{{ statusText }}</span>
            </div>
          </div>

          <div class="card-body">
            <!-- Cookie 输入区 -->
            <div class="input-section">
              <div class="input-label-row">
                <label class="input-label">
                  <span class="label-icon">🔑</span>
                  Cookie 值
                </label>
                <el-button
                  :icon="showCookie ? Hide : View"
                  @click="showCookie = !showCookie"
                  class="toggle-btn"
                  text
                />
              </div>
              <div class="input-wrapper">
                <el-input
                  v-model="configForm.taobao_cookie"
                  :type="showCookie ? 'textarea' : 'password'"
                  :rows="showCookie ? 6 : 2"
                  placeholder="粘贴从浏览器获取的完整 Cookie..."
                  class="cookie-input"
                />
                <div class="input-decoration"></div>
              </div>
              <div class="input-hint">
                <span class="hint-icon">💡</span>
                <span>从浏览器开发者工具 Network 标签中复制</span>
              </div>
            </div>

            <!-- 测试结果展示 -->
            <transition name="result-fade">
              <div v-if="configForm.test_result" class="result-section" :class="resultClass">
                <div class="result-icon">{{ resultIcon }}</div>
                <div class="result-content">
                  <h4 class="result-title">{{ resultTitle }}</h4>
                  <p class="result-message">{{ configForm.test_result }}</p>
                  <p v-if="configForm.last_test_time" class="result-time">
                    测试时间: {{ formatTime(configForm.last_test_time) }}
                  </p>
                </div>
              </div>
            </transition>

            <!-- 操作按钮组 -->
            <div class="action-buttons">
              <el-button
                type="primary"
                size="large"
                @click="saveConfig"
                :loading="saving"
                class="save-btn"
              >
                <span class="btn-icon">💾</span>
                <span>{{ saving ? '保存中...' : '保存配置' }}</span>
              </el-button>
              <el-button
                size="large"
                @click="testCookie"
                :loading="testing"
                :disabled="!configForm.taobao_cookie"
                class="test-btn"
              >
                <span class="btn-icon">🧪</span>
                <span>{{ testing ? '测试中...' : '测试 Cookie' }}</span>
              </el-button>
            </div>
          </div>

          <!-- 卡片装饰 -->
          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>

        <!-- 快捷状态卡片 -->
        <div class="status-cards">
          <div class="mini-card" :class="{ active: configForm.cookie_status !== 'not_configured' }">
            <span class="mini-icon">📊</span>
            <div class="mini-content">
              <span class="mini-label">配置状态</span>
              <span class="mini-value">{{ statusText }}</span>
            </div>
          </div>
          <div class="mini-card" :class="{ active: configForm.last_test_time }">
            <span class="mini-icon">⏰</span>
            <div class="mini-content">
              <span class="mini-label">最后测试</span>
              <span class="mini-value">{{ configForm.last_test_time ? formatTime(configForm.last_test_time) : '未测试' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：获取指南 -->
      <div class="right-column">
        <div class="guide-card glass-card">
          <div class="card-header guide-header">
            <div class="icon-wrapper guide-icon">
              <span>📖</span>
            </div>
            <div>
              <h3 class="card-title">获取指南</h3>
              <p class="card-subtitle">如何获取 Cookie</p>
            </div>
          </div>

          <div class="guide-steps">
            <div
              v-for="(step, index) in cookieSteps"
              :key="index"
              class="guide-step"
              :style="{ '--step-index': index }"
            >
              <div class="step-number">{{ String(index + 1).padStart(2, '0') }}</div>
              <div class="step-content">
                <h4 class="step-title">{{ step.title }}</h4>
                <p class="step-description">{{ step.description }}</p>
              </div>
              <div class="step-icon">{{ step.icon }}</div>
            </div>
          </div>

          <div class="guide-footer">
            <div class="footer-tip">
              <span class="tip-icon">🔒</span>
              <span>Cookie 仅用于数据采集，请妥善保管</span>
            </div>
          </div>
        </div>

        <!-- 提示卡片 -->
        <div class="tips-card glass-card">
          <h4 class="tips-title">⚡ 快速提示</h4>
          <ul class="tips-list">
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>Cookie 有效期通常为 7-30 天</span>
            </li>
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>测试失败请重新获取 Cookie</span>
            </li>
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>配置后无需重启服务即可生效</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { View, Hide } from '@element-plus/icons-vue'
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
    description: '访问 www.taobao.com 并登录账号',
    icon: '🌐'
  },
  {
    title: '打开开发者工具',
    description: '按 F12 或右键选择"检查"',
    icon: '🛠️'
  },
  {
    title: '切换 Network 标签',
    description: '在开发者工具中找到 Network 选项',
    icon: '📡'
  },
  {
    title: '刷新或搜索',
    description: '按 F5 刷新或搜索任意商品',
    icon: '🔄'
  },
  {
    title: '查找请求',
    description: '点击列表中的任意请求',
    icon: '🔍'
  },
  {
    title: '复制 Cookie',
    description: 'Headers → Request Headers → Cookie',
    icon: '📋'
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

const resultIcon = computed(() => {
  return isTestSuccess.value ? '✅' : '❌'
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
      // 注意：后端返回的是截断的 Cookie（仅用于显示），不要覆盖用户输入
      // 只有当用户没有输入时才显示占位符
      if (!configForm.taobao_cookie && data.taobao_cookie) {
        // 如果 Cookie 包含省略号，说明是截断的，不加载到表单
        if (!data.taobao_cookie.includes('...')) {
          configForm.taobao_cookie = data.taobao_cookie
        }
      }
      configForm.cookie_status = data.cookie_status || 'not_configured'
      configForm.last_test_time = data.last_test_time || null
      configForm.test_result = data.test_result || ''
    }
  } catch (error) {
    // 400错误可能表示配置不存在，这是正常的
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
    // 尝试从响应中获取详细错误信息
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* ========== 全局样式 ========== */
.config-container {
  min-height: 100vh;
  padding: 24px;
  position: relative;
  overflow-x: hidden;
  font-family: 'Noto Sans SC', sans-serif;
}

/* ========== 背景装饰 ========== */
.bg-decoration {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  top: -200px;
  right: -200px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(225deg, #06FFA5 0%, #FF6B35 100%);
  bottom: -100px;
  left: -100px;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 107, 53, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 107, 53, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.noise-texture {
  position: absolute;
  inset: 0;
  opacity: 0.02;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  position: relative;
  z-index: 1;
}

.header-content {
  flex: 1;
}

.title-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 20px;
  margin-bottom: 16px;
}

.badge-icon {
  font-size: 16px;
}

.badge-text {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #FF6B35;
  font-family: 'Orbitron', sans-serif;
}

.page-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 12px 0;
  line-height: 1.1;
}

.title-gradient {
  background: linear-gradient(135deg, #FF6B35 0%, #FFD700 50%, #7B2CBF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.header-visual {
  position: relative;
  width: 200px;
  height: 100px;
}

.floating-icon {
  position: absolute;
  font-size: 32px;
  animation: iconFloat 3s ease-in-out infinite;
}

.icon-1 { top: 0; right: 0; animation-delay: 0s; }
.icon-2 { top: 30px; right: 60px; animation-delay: 0.5s; }
.icon-3 { top: 50px; right: 20px; animation-delay: 1s; }

@keyframes iconFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

/* ========== 内容网格 ========== */
.content-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
  position: relative;
  z-index: 1;
}

@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  .page-header {
    flex-direction: column;
    gap: 24px;
  }
  .header-visual {
    display: none;
  }
}

/* ========== 玻璃态卡片 ========== */
.glass-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg,
    rgba(255, 107, 53, 0.05) 0%,
    transparent 50%,
    rgba(123, 44, 191, 0.05) 100%
  );
  pointer-events: none;
}

/* ========== 配置卡片 ========== */
.config-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 24px;
}

.cookie-icon {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(255, 107, 53, 0.05));
  border: 1px solid rgba(255, 107, 53, 0.3);
}

.guide-icon {
  background: linear-gradient(135deg, rgba(6, 255, 165, 0.2), rgba(6, 255, 165, 0.05));
  border: 1px solid rgba(6, 255, 165, 0.3);
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 4px 0;
}

.card-subtitle {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-empty { background: rgba(255, 255, 255, 0.05); color: rgba(255, 255, 255, 0.4); }
.status-pending { background: rgba(255, 215, 0, 0.15); color: #FFD700; }
.status-success { background: rgba(6, 255, 165, 0.15); color: #06FFA5; }
.status-error { background: rgba(255, 107, 107, 0.15); color: #FF6B6B; }

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ========== 输入区 ========== */
.card-body {
  position: relative;
  z-index: 1;
}

.input-section {
  margin-bottom: 20px;
}

.input-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.label-icon {
  font-size: 16px;
}

.toggle-btn {
  color: rgba(255, 255, 255, 0.4);
}

.toggle-btn:hover {
  color: rgba(255, 255, 255, 0.7);
}

.input-wrapper {
  position: relative;
}

.cookie-input {
  --el-input-bg-color: rgba(0, 0, 0, 0.3);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-input-text-color: rgba(255, 255, 255, 0.9);
  --el-input-placeholder-color: rgba(255, 255, 255, 0.3);
}

.cookie-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 107, 53, 0.5) 50%,
    transparent 100%
  );
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.hint-icon {
  font-size: 14px;
}

/* ========== 测试结果 ========== */
.result-section {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  border: 1px solid;
}

.result-success {
  background: rgba(6, 255, 165, 0.1);
  border-color: rgba(6, 255, 165, 0.3);
}

.result-error {
  background: rgba(255, 107, 107, 0.1);
  border-color: rgba(255, 107, 107, 0.3);
}

.result-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.result-content {
  flex: 1;
}

.result-title {
  font-size: 14px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.result-success .result-title { color: #06FFA5; }
.result-error .result-title { color: #FF6B6B; }

.result-message {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 4px 0;
}

.result-time {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.result-fade-enter-active,
.result-fade-leave-active {
  transition: all 0.3s ease;
}

.result-fade-enter-from,
.result-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========== 操作按钮 ========== */
.action-buttons {
  display: flex;
  gap: 12px;
}

.save-btn,
.test-btn {
  flex: 1;
  height: 48px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.save-btn {
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  color: white;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3);
}

.test-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.test-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.test-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 16px;
}

/* ========== 卡片装饰 ========== */
.card-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.deco-line {
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 107, 53, 0.3) 50%,
    transparent 100%
  );
}

.deco-1 {
  top: 0;
  left: 0;
  right: 0;
}

.deco-2 {
  bottom: 0;
  left: 0;
  right: 0;
}

.deco-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #FF6B35;
  border-radius: 50%;
  top: 20px;
  right: 20px;
  box-shadow: 0 0 10px rgba(255, 107, 53, 0.5);
}

/* ========== 状态小卡片 ========== */
.status-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.mini-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.mini-card.active {
  border-color: rgba(255, 107, 53, 0.3);
  background: rgba(255, 107, 53, 0.05);
}

.mini-icon {
  font-size: 20px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.mini-content {
  display: flex;
  flex-direction: column;
}

.mini-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 2px;
}

.mini-value {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

/* ========== 指南卡片 ========== */
.guide-card {
  margin-bottom: 20px;
}

.guide-header {
  margin-bottom: 20px;
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.guide-step {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  position: relative;
}

.guide-step::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg,
    #FF6B35 0%,
    #7B2CBF 100%
  );
  border-radius: 12px 0 0 12px;
}

.guide-step:hover {
  background: rgba(255, 107, 53, 0.05);
  border-color: rgba(255, 107, 53, 0.2);
  transform: translateX(4px);
}

.step-number {
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #FF6B35;
}

.step-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 4px 0;
}

.step-description {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.step-icon {
  font-size: 24px;
  opacity: 0.8;
}

.guide-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.tip-icon {
  font-size: 14px;
}

/* ========== 提示卡片 ========== */
.tips-card {
  background: rgba(6, 255, 165, 0.05);
  border-color: rgba(6, 255, 165, 0.15);
}

.tips-title {
  font-size: 15px;
  font-weight: 700;
  color: #06FFA5;
  margin: 0 0 16px 0;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.tip-item:last-child {
  border-bottom: none;
}

.tip-bullet {
  color: #06FFA5;
  font-weight: 700;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .config-container {
    padding: 16px;
  }

  .page-title {
    font-size: 28px;
  }

  .content-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .status-cards {
    grid-template-columns: 1fr;
  }

  .guide-step {
    grid-template-columns: auto 1fr;
  }

  .step-icon {
    display: none;
  }
}
</style>
