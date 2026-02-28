<template>
  <div class="settings-container">
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
          <span class="badge-text">SYSTEM SETTINGS</span>
        </div>
        <h1 class="page-title">
          <span class="title-gradient">系统设置中心</span>
        </h1>
        <p class="page-subtitle">配置系统参数与功能选项</p>
      </div>
      <div class="header-visual">
        <div class="floating-icon icon-1">🎛️</div>
        <div class="floating-icon icon-2">🔧</div>
        <div class="floating-icon icon-3">⚡</div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="content-grid">
      <!-- 左侧：设置卡片组 -->
      <div class="settings-column">
        <!-- 基本设置 -->
        <div class="setting-card glass-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper basic-icon">
                <span>🏠</span>
              </div>
              <div>
                <h3 class="card-title">基本设置</h3>
                <p class="card-subtitle">系统基础信息配置</p>
              </div>
            </div>
          </div>

          <div class="card-body">
            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">📝</span>
                <span>系统名称</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.system_name"
                  placeholder="输入系统名称"
                  class="setting-input"
                />
                <div class="input-decoration"></div>
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">🖼️</span>
                <span>Logo URL</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.logo_url"
                  placeholder="https://example.com/logo.png"
                  class="setting-input"
                />
                <div class="input-decoration"></div>
              </div>
            </div>
          </div>

          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>

        <!-- 爬虫设置 -->
        <div class="setting-card glass-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper crawler-icon">
                <span>🕷️</span>
              </div>
              <div>
                <h3 class="card-title">爬虫设置</h3>
                <p class="card-subtitle">数据采集参数配置</p>
              </div>
            </div>
          </div>

          <div class="card-body">
            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">⏱️</span>
                <span>采集间隔（秒）</span>
              </label>
              <div class="input-wrapper">
                <el-input-number
                  v-model="settingsForm.crawl_interval"
                  :min="1"
                  :max="3600"
                  :step="1"
                  class="setting-number"
                />
                <div class="input-decoration"></div>
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">🔀</span>
                <span>并发数</span>
              </label>
              <div class="input-wrapper">
                <el-input-number
                  v-model="settingsForm.concurrent_tasks"
                  :min="1"
                  :max="10"
                  :step="1"
                  class="setting-number"
                />
                <div class="input-decoration"></div>
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">⏳</span>
                <span>超时时间（秒）</span>
              </label>
              <div class="input-wrapper">
                <el-input-number
                  v-model="settingsForm.request_timeout"
                  :min="5"
                  :max="300"
                  :step="5"
                  class="setting-number"
                />
                <div class="input-decoration"></div>
              </div>
            </div>
          </div>

          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>

        <!-- 邮件设置 -->
        <div class="setting-card glass-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper email-icon">
                <span>📧</span>
              </div>
              <div>
                <h3 class="card-title">邮件设置</h3>
                <p class="card-subtitle">SMTP 邮件服务配置</p>
              </div>
            </div>
          </div>

          <div class="card-body">
            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">🖥️</span>
                <span>SMTP 服务器</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.smtp_host"
                  placeholder="smtp.example.com"
                  class="setting-input"
                />
                <div class="input-decoration"></div>
              </div>
            </div>

            <div class="setting-row">
              <div class="setting-item setting-item--half">
                <label class="setting-label">
                  <span class="label-icon">🔌</span>
                  <span>端口</span>
                </label>
                <div class="input-wrapper">
                  <el-input-number
                    v-model="settingsForm.smtp_port"
                    :min="1"
                    :max="65535"
                    :step="1"
                    class="setting-number"
                  />
                  <div class="input-decoration"></div>
                </div>
              </div>

              <div class="setting-item setting-item--half">
                <label class="setting-label">
                  <span class="label-icon">👤</span>
                  <span>发件人</span>
                </label>
                <div class="input-wrapper">
                  <el-input
                    v-model="settingsForm.smtp_from"
                    placeholder="noreply@example.com"
                    class="setting-input"
                  />
                  <div class="input-decoration"></div>
                </div>
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">🔐</span>
                <span>SMTP 密码</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.smtp_password"
                  type="password"
                  placeholder="输入 SMTP 密码"
                  class="setting-input"
                  show-password
                />
                <div class="input-decoration"></div>
              </div>
            </div>

            <div class="setting-item setting-item--toggle">
              <label class="setting-label">
                <span class="label-icon">✉️</span>
                <span>启用邮件通知</span>
              </label>
              <el-switch
                v-model="settingsForm.email_enabled"
                class="custom-switch"
                size="large"
              />
            </div>
          </div>

          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>

        <!-- 通知设置 -->
        <div class="setting-card glass-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper notification-icon">
                <span>🔔</span>
              </div>
              <div>
                <h3 class="card-title">通知设置</h3>
                <p class="card-subtitle">系统通知偏好配置</p>
              </div>
            </div>
          </div>

          <div class="card-body">
            <div class="setting-item setting-item--toggle">
              <div class="toggle-content">
                <label class="setting-label">
                  <span class="label-icon">📬</span>
                  <span>邮件通知</span>
                </label>
                <p class="toggle-description">接收系统重要邮件通知</p>
              </div>
              <el-switch
                v-model="settingsForm.notify_email"
                class="custom-switch"
                size="large"
              />
            </div>

            <div class="setting-item setting-item--toggle">
              <div class="toggle-content">
                <label class="setting-label">
                  <span class="label-icon">🌐</span>
                  <span>浏览器通知</span>
                </label>
                <p class="toggle-description">接收浏览器推送通知</p>
              </div>
              <el-switch
                v-model="settingsForm.notify_browser"
                class="custom-switch"
                size="large"
              />
            </div>

            <div class="setting-item setting-item--toggle">
              <div class="toggle-content">
                <label class="setting-label">
                  <span class="label-icon">📊</span>
                  <span>爬虫完成通知</span>
                </label>
                <p class="toggle-description">数据采集完成时通知</p>
              </div>
              <el-switch
                v-model="settingsForm.notify_crawler_complete"
                class="custom-switch"
                size="large"
              />
            </div>

            <div class="setting-item setting-item--toggle">
              <div class="toggle-content">
                <label class="setting-label">
                  <span class="label-icon">⚠️</span>
                  <span>错误告警通知</span>
                </label>
                <p class="toggle-description">系统异常时发送告警</p>
              </div>
              <el-switch
                v-model="settingsForm.notify_error_alert"
                class="custom-switch"
                size="large"
              />
            </div>
          </div>

          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-bar">
          <button class="action-btn action-btn--primary" @click="handleSave">
            <span class="btn-icon">💾</span>
            <span>保存设置</span>
          </button>
          <button class="action-btn action-btn--secondary" @click="handleReset">
            <span class="btn-icon">🔄</span>
            <span>重置默认</span>
          </button>
        </div>
      </div>

      <!-- 右侧：快捷状态卡片 -->
      <div class="status-column">
        <div class="status-card glass-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper status-icon">
                <span>📊</span>
              </div>
              <div>
                <h3 class="card-title">设置概览</h3>
                <p class="card-subtitle">当前配置状态</p>
              </div>
            </div>
          </div>

          <div class="status-list">
            <div class="status-item" :class="{ active: settingsForm.system_name }">
              <span class="status-icon">🏠</span>
              <div class="status-content">
                <span class="status-label">基本设置</span>
                <span class="status-value">{{ settingsForm.system_name ? '已配置' : '未配置' }}</span>
              </div>
            </div>

            <div class="status-item" :class="{ active: settingsForm.crawl_interval }">
              <span class="status-icon">🕷️</span>
              <div class="status-content">
                <span class="status-label">爬虫设置</span>
                <span class="status-value">{{ settingsForm.crawl_interval ? '已配置' : '未配置' }}</span>
              </div>
            </div>

            <div class="status-item" :class="{ active: settingsForm.smtp_host }">
              <span class="status-icon">📧</span>
              <div class="status-content">
                <span class="status-label">邮件设置</span>
                <span class="status-value">{{ settingsForm.smtp_host ? '已配置' : '未配置' }}</span>
              </div>
            </div>

            <div class="status-item" :class="{ active: settingsForm.notify_email || settingsForm.notify_browser }">
              <span class="status-icon">🔔</span>
              <div class="status-content">
                <span class="status-label">通知设置</span>
                <span class="status-value">{{ settingsForm.notify_email || settingsForm.notify_browser ? '已启用' : '未启用' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 提示卡片 -->
        <div class="tips-card glass-card">
          <h4 class="tips-title">💡 使用提示</h4>
          <ul class="tips-list">
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>保存设置后立即生效，无需重启</span>
            </li>
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>爬虫并发数建议设置为 3-5</span>
            </li>
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>邮件功能需要正确的 SMTP 配置</span>
            </li>
            <li class="tip-item">
              <span class="tip-bullet">→</span>
              <span>建议启用错误告警以监控系统</span>
            </li>
          </ul>
        </div>

        <!-- 版本信息 -->
        <div class="version-card glass-card">
          <div class="version-content">
            <div class="version-main">
              <span class="version-label">系统版本</span>
              <span class="version-number">v1.0.0</span>
            </div>
            <div class="version-meta">
              <span>最后更新：2024-02-28</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 设置表单数据
const settingsForm = reactive({
  // 基本设置
  system_name: '天猫宠物用品采集系统',
  logo_url: '',

  // 爬虫设置
  crawl_interval: 60,
  concurrent_tasks: 3,
  request_timeout: 30,

  // 邮件设置
  smtp_host: '',
  smtp_port: 587,
  smtp_from: '',
  smtp_password: '',
  email_enabled: false,

  // 通知设置
  notify_email: false,
  notify_browser: false,
  notify_crawler_complete: true,
  notify_error_alert: true
})

// 默认设置
const defaultSettings = {
  system_name: '天猫宠物用品采集系统',
  logo_url: '',
  crawl_interval: 60,
  concurrent_tasks: 3,
  request_timeout: 30,
  smtp_host: '',
  smtp_port: 587,
  smtp_from: '',
  smtp_password: '',
  email_enabled: false,
  notify_email: false,
  notify_browser: false,
  notify_crawler_complete: true,
  notify_error_alert: true
}

// 加载设置
const loadSettings = async () => {
  try {
    // TODO: 从后端 API 加载设置
    // const response = await request.get('/users/configs/system/')
    // if (response.code === 0) {
    //   Object.assign(settingsForm, response.data)
    // }
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

// 保存设置
const handleSave = async () => {
  try {
    // TODO: 调用后端 API 保存设置
    // const response = await request.put('/users/configs/system/', settingsForm)
    // if (response.code === 0) {
    //   ElMessage.success('设置保存成功')
    // }

    // 临时模拟保存成功
    ElMessage.success('设置保存成功')
    console.log('保存设置:', settingsForm)
  } catch (error) {
    ElMessage.error('保存设置失败')
    console.error(error)
  }
}

// 重置默认
const handleReset = () => {
  Object.assign(settingsForm, defaultSettings)
  ElMessage.info('已重置为默认设置')
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* ========== 全局样式 ========== */
.settings-container {
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
  grid-template-columns: 1.5fr 1fr;
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

/* ========== 设置卡片 ========== */
.setting-card {
  margin-bottom: 20px;
  animation: cardSlideIn 0.4s ease backwards;
}

.setting-card:nth-child(1) { animation-delay: 0.1s; }
.setting-card:nth-child(2) { animation-delay: 0.2s; }
.setting-card:nth-child(3) { animation-delay: 0.3s; }
.setting-card:nth-child(4) { animation-delay: 0.4s; }

@keyframes cardSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

.basic-icon {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(255, 107, 53, 0.05));
  border: 1px solid rgba(255, 107, 53, 0.3);
}

.crawler-icon {
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.2), rgba(123, 44, 191, 0.05));
  border: 1px solid rgba(123, 44, 191, 0.3);
}

.email-icon {
  background: linear-gradient(135deg, rgba(6, 255, 165, 0.2), rgba(6, 255, 165, 0.05));
  border: 1px solid rgba(6, 255, 165, 0.3);
}

.notification-icon {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 215, 0, 0.05));
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.status-icon {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(123, 44, 191, 0.05));
  border: 1px solid rgba(255, 107, 53, 0.3);
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

/* ========== 设置项 ========== */
.card-body {
  position: relative;
  z-index: 1;
}

.setting-item {
  margin-bottom: 20px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.setting-item--half {
  margin-bottom: 0;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 10px;
}

.label-icon {
  font-size: 16px;
}

.input-wrapper {
  position: relative;
}

.setting-input {
  --el-input-bg-color: rgba(0, 0, 0, 0.3);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-input-text-color: rgba(255, 255, 255, 0.9);
  --el-input-placeholder-color: rgba(255, 255, 255, 0.3);
}

.setting-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  transition: all 0.3s ease;
}

.setting-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.setting-input :deep(.el-input__wrapper.is-focus) {
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.setting-number {
  width: 100%;
}

.setting-number :deep(.el-input__wrapper) {
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

.setting-number :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.setting-number :deep(.el-input__wrapper.is-focus) {
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.setting-number :deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  text-align: left;
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

/* ========== 开关控件 ========== */
.setting-item--toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.setting-item--toggle:hover {
  background: rgba(255, 107, 53, 0.05);
  border-color: rgba(255, 107, 53, 0.1);
}

.toggle-content {
  flex: 1;
}

.toggle-content .setting-label {
  margin-bottom: 4px;
}

.toggle-description {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
  margin-left: 24px;
}

.custom-switch {
  --el-switch-on-color: #FF6B35;
  --el-switch-off-color: rgba(255, 255, 255, 0.1);
  --el-switch-border-color: rgba(255, 255, 255, 0.1);
}

.custom-switch :deep(.el-switch__core) {
  height: 24px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.custom-switch :deep(.el-switch__action) {
  width: 20px;
  height: 20px;
  left: 2px;
}

.custom-switch.is-checked :deep(.el-switch__action) {
  left: calc(100% - 22px);
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

/* ========== 操作栏 ========== */
.action-bar {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 48px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.action-btn--primary {
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  color: white;
}

.action-btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3);
}

.action-btn--secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.action-btn--secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-icon {
  font-size: 16px;
}

/* ========== 状态列 ========== */
.status-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-card,
.tips-card,
.version-card {
  animation: cardSlideIn 0.4s ease backwards;
}

.status-card { animation-delay: 0.3s; }
.tips-card { animation-delay: 0.4s; }
.version-card { animation-delay: 0.5s; }

.status-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.status-item.active {
  border-color: rgba(255, 107, 53, 0.3);
  background: rgba(255, 107, 53, 0.05);
}

.status-icon {
  font-size: 20px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.status-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.status-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 2px;
}

.status-value {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.status-item.active .status-value {
  color: #FF6B35;
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

/* ========== 版本卡片 ========== */
.version-card {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(123, 44, 191, 0.05));
  border-color: rgba(255, 107, 53, 0.2);
}

.version-content {
  text-align: center;
}

.version-main {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.version-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.version-number {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #FF6B35, #7B2CBF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.version-meta {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .settings-container {
    padding: 16px;
  }

  .page-title {
    font-size: 28px;
  }

  .content-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .setting-row {
    grid-template-columns: 1fr;
  }

  .action-bar {
    flex-direction: column;
  }

  .status-column {
    order: -1;
  }
}
</style>
