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

<template>
  <div class="settings-container">
    <!-- 装饰叶子 -->
    <div class="leaf-decoration leaf-decoration--1">
      <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
        <path d="M50 5C50 5 85 25 85 55C85 85 65 95 50 95C35 95 15 85 15 55C15 25 50 5 50 5Z" fill="currentColor" opacity="0.04"/>
        <path d="M50 5L50 95" stroke="currentColor" stroke-width="1" opacity="0.06"/>
      </svg>
    </div>
    <div class="leaf-decoration leaf-decoration--2">
      <svg width="70" height="70" viewBox="0 0 70 70" fill="none">
        <path d="M35 3C35 3 60 14 60 35C60 56 48 65 35 65C22 65 10 56 10 35C10 14 35 3 35 3Z" fill="currentColor" opacity="0.05"/>
      </svg>
    </div>

    <!-- 主标题区 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-icon-wrapper">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M12 1v6m0 6v6"></path>
            <path d="m4.93 4.93 4.24 4.24m5.66 5.66 4.24 4.24"></path>
            <path d="M1 12h6m6 0h6"></path>
          </svg>
        </div>
        <div>
          <h1 class="page-title">系统设置中心</h1>
          <p class="page-subtitle">配置系统参数与功能选项</p>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="content-grid">
      <!-- 左侧：设置卡片组 -->
      <div class="settings-column">
        <!-- 基本设置 -->
        <div class="setting-card">
          <div class="card-header">
            <div class="header-left">
              <div class="card-icon card-icon--green">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                  <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
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
                <span>系统名称</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.system_name"
                  placeholder="输入系统名称"
                  class="setting-input"
                />
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <span>Logo URL</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.logo_url"
                  placeholder="https://example.com/logo.png"
                  class="setting-input"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 爬虫设置 -->
        <div class="setting-card">
          <div class="card-header">
            <div class="header-left">
              <div class="card-icon card-icon--teal">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
                  <path d="M12 2a10 10 0 0 1 10 10"></path>
                  <path d="M12 12 2.1 12"></path>
                </svg>
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
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
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
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
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
              </div>
            </div>
          </div>
        </div>

        <!-- 邮件设置 -->
        <div class="setting-card">
          <div class="card-header">
            <div class="header-left">
              <div class="card-icon card-icon--blue">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
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
                <span>SMTP 服务器</span>
              </label>
              <div class="input-wrapper">
                <el-input
                  v-model="settingsForm.smtp_host"
                  placeholder="smtp.example.com"
                  class="setting-input"
                />
              </div>
            </div>

            <div class="setting-row">
              <div class="setting-item setting-item--half">
                <label class="setting-label">
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
                </div>
              </div>

              <div class="setting-item setting-item--half">
                <label class="setting-label">
                  <span>发件人</span>
                </label>
                <div class="input-wrapper">
                  <el-input
                    v-model="settingsForm.smtp_from"
                    placeholder="noreply@example.com"
                    class="setting-input"
                  />
                </div>
              </div>
            </div>

            <div class="setting-item">
              <label class="setting-label">
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
              </div>
            </div>

            <div class="setting-item setting-item--toggle">
              <label class="setting-label">
                <span>启用邮件通知</span>
              </label>
              <el-switch
                v-model="settingsForm.email_enabled"
                class="custom-switch"
                size="large"
              />
            </div>
          </div>
        </div>

        <!-- 通知设置 -->
        <div class="setting-card">
          <div class="card-header">
            <div class="header-left">
              <div class="card-icon card-icon--accent">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
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
        </div>

        <!-- 操作按钮 -->
        <div class="action-bar">
          <button class="action-btn action-btn--primary" @click="handleSave">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17 21 17 13 7 13 7 21"></polyline>
              <polyline points="7 3 7 8 15 8"></polyline>
            </svg>
            <span>保存设置</span>
          </button>
          <button class="action-btn action-btn--secondary" @click="handleReset">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span>重置默认</span>
          </button>
        </div>
      </div>

      <!-- 右侧：快捷状态卡片 -->
      <div class="status-column">
        <div class="status-card">
          <div class="card-header">
            <div class="header-left">
              <div class="card-icon card-icon--status">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="3" y1="9" x2="21" y2="9"></line>
                  <line x1="9" y1="21" x2="9" y2="9"></line>
                </svg>
              </div>
              <div>
                <h3 class="card-title">设置概览</h3>
                <p class="card-subtitle">当前配置状态</p>
              </div>
            </div>
          </div>

          <div class="status-list">
            <div class="status-item" :class="{ active: settingsForm.system_name }">
              <div class="status-icon status-icon--green">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                </svg>
              </div>
              <div class="status-content">
                <span class="status-label">基本设置</span>
                <span class="status-value">{{ settingsForm.system_name ? '已配置' : '未配置' }}</span>
              </div>
            </div>

            <div class="status-item" :class="{ active: settingsForm.crawl_interval }">
              <div class="status-icon status-icon--teal">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </div>
              <div class="status-content">
                <span class="status-label">爬虫设置</span>
                <span class="status-value">{{ settingsForm.crawl_interval ? '已配置' : '未配置' }}</span>
              </div>
            </div>

            <div class="status-item" :class="{ active: settingsForm.smtp_host }">
              <div class="status-icon status-icon--blue">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                </svg>
              </div>
              <div class="status-content">
                <span class="status-label">邮件设置</span>
                <span class="status-value">{{ settingsForm.smtp_host ? '已配置' : '未配置' }}</span>
              </div>
            </div>

            <div class="status-item" :class="{ active: settingsForm.notify_email || settingsForm.notify_browser }">
              <div class="status-icon status-icon--accent">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                </svg>
              </div>
              <div class="status-content">
                <span class="status-label">通知设置</span>
                <span class="status-value">{{ settingsForm.notify_email || settingsForm.notify_browser ? '已启用' : '未启用' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 提示卡片 -->
        <div class="tips-card">
          <h4 class="tips-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
            使用提示
          </h4>
          <ul class="tips-list">
            <li class="tip-item">保存设置后立即生效，无需重启</li>
            <li class="tip-item">爬虫并发数建议设置为 3-5</li>
            <li class="tip-item">邮件功能需要正确的 SMTP 配置</li>
            <li class="tip-item">建议启用错误告警以监控系统</li>
          </ul>
        </div>

        <!-- 版本信息 -->
        <div class="version-card">
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.settings-container {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  min-height: calc(100vh - 140px);
  padding: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
  animation: pageFadeIn 0.5s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Leaf Decorations
   ============================================ */
.leaf-decoration {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  color: var(--primary-green);
}

.leaf-decoration--1 {
  top: -20px;
  right: -20px;
  opacity: 0.5;
}

.leaf-decoration--2 {
  bottom: 80px;
  left: -30px;
  opacity: 0.4;
}

/* ============================================
   Page Header
   ============================================ */
.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  position: relative;
  z-index: 1;
}

.header-icon-wrapper {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(82, 183, 136, 0.08));
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 20px;
  color: var(--primary-green);
  animation: headerFloat 4s ease-in-out infinite;
}

@keyframes headerFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.01em;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* ============================================
   Content Grid
   ============================================ */
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
}

/* ============================================
   Settings Card
   ============================================ */
.setting-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.setting-card:hover {
  border-color: var(--accent-green);
  box-shadow: var(--shadow-hover);
}

.card-header {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
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
  border-radius: 14px;
}

.card-icon--green {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.12), rgba(82, 183, 136, 0.08));
  color: var(--primary-green);
}

.card-icon--teal {
  background: linear-gradient(135deg, rgba(64, 145, 108, 0.12), rgba(82, 183, 136, 0.08));
  color: var(--primary-teal);
}

.card-icon--blue {
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.12), rgba(144, 224, 239, 0.08));
  color: var(--accent-blue);
}

.card-icon--accent {
  background: linear-gradient(135deg, rgba(116, 198, 157, 0.12), rgba(82, 183, 136, 0.08));
  color: var(--accent-green);
}

.card-icon--status {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(82, 183, 136, 0.06));
  color: var(--primary-green);
}

.card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px 0;
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.card-body {
  padding: 24px;
}

/* ============================================
   Setting Item
   ============================================ */
.setting-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-item--half {
  flex: 1;
}

.setting-row {
  display: flex;
  gap: 20px;
}

.setting-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
}

.setting-input {
  --el-input-bg-color: var(--bg-sand);
  --el-input-border-color: var(--border-light);
  --el-input-text-color: var(--text-primary);
  --el-input-placeholder-color: var(--text-tertiary);
  --el-input-focus-border-color: var(--border-focus);
}

.setting-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.setting-input :deep(.el-input__wrapper):hover {
  border-color: rgba(116, 198, 157, 0.3);
}

.setting-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.setting-number {
  width: 100%;
}

.setting-number :deep(.el-input-number__decrease),
.setting-number :deep(.el-input-number__increase) {
  background: var(--bg-card);
  border-left: 1px solid var(--border-light);
  color: var(--text-secondary);
}

.setting-number :deep(.el-input__wrapper) {
  border-radius: 12px;
}

/* Toggle Items */
.setting-item--toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
  padding: 16px;
  background: var(--bg-sand);
  border-radius: 14px;
}

.toggle-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toggle-description {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

.custom-switch {
  --el-switch-on-color: var(--primary-green);
}

/* ============================================
   Action Bar
   ============================================ */
.action-bar {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-green), var(--primary-teal));
  color: white;
  box-shadow: 0 4px 15px rgba(45, 106, 79, 0.25);
}

.action-btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(45, 106, 79, 0.35);
}

.action-btn--secondary {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
  box-shadow: var(--shadow-soft);
}

.action-btn--secondary:hover {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
}

/* ============================================
   Status Card
   ============================================ */
.status-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
}

.status-list {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: var(--bg-sand);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.status-item.active {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.08), rgba(116, 198, 157, 0.04));
  border: 1px solid rgba(116, 198, 157, 0.2);
}

.status-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.status-icon--green {
  background: rgba(45, 106, 79, 0.12);
  color: var(--primary-green);
}

.status-icon--teal {
  background: rgba(64, 145, 108, 0.12);
  color: var(--primary-teal);
}

.status-icon--blue {
  background: rgba(0, 180, 216, 0.12);
  color: var(--accent-blue);
}

.status-icon--accent {
  background: rgba(116, 198, 157, 0.12);
  color: var(--accent-green);
}

.status-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.status-value {
  font-size: 12px;
  color: var(--text-tertiary);
}

.status-item.active .status-value {
  color: var(--primary-green);
  font-weight: 600;
}

/* ============================================
   Tips Card
   ============================================ */
.tips-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  padding: 20px;
  box-shadow: var(--shadow-soft);
}

.tips-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.tips-title svg {
  color: var(--accent-blue);
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  position: relative;
  padding-left: 20px;
}

.tip-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 7px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-green);
}

/* ============================================
   Version Card
   ============================================ */
.version-card {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.08), rgba(116, 198, 157, 0.04));
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 20px;
  padding: 20px;
  box-shadow: var(--shadow-soft);
}

.version-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.version-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.version-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.version-number {
  font-family: 'Nunito', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-green);
}

.version-meta {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-icon-wrapper {
    width: 50px;
    height: 50px;
  }

  .page-title {
    font-size: 22px;
  }

  .setting-row {
    flex-direction: column;
    gap: 16px;
  }

  .action-bar {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .leaf-decoration {
    display: none;
  }
}
</style>
