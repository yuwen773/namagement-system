<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSystemConfig, updateSystemConfig } from '../../api/system-config'
import { useAuthStore } from '../../stores/auth'

// 响应式状态
const loading = ref(false)
const saving = ref(false)
const config = reactive({
  // 注册配置
  require_registration_approval: false,
  // 密码策略配置
  password_min_length: 6,
  password_require_uppercase: false,
  password_require_lowercase: true,
  password_require_number: true,
  password_require_special: false,
  // 登录安全配置
  max_login_attempts: 5,
  login_lockout_duration: 30,
  session_timeout: 120,
  // 其他配置
  allow_multiple_sessions: true
})

// 备份原始配置，用于取消时恢复
const originalConfig = ref(null)

// 获取系统配置
const fetchConfig = async () => {
  loading.value = true
  try {
    const res = await getSystemConfig()
    const data = res.data?.data || res.data
    if (data) {
      // 更新响应式对象
      Object.assign(config, {
        require_registration_approval: data.require_registration_approval,
        password_min_length: data.password_min_length,
        password_require_uppercase: data.password_require_uppercase,
        password_require_lowercase: data.password_require_lowercase,
        password_require_number: data.password_require_number,
        password_require_special: data.password_require_special,
        max_login_attempts: data.max_login_attempts,
        login_lockout_duration: data.login_lockout_duration,
        session_timeout: data.session_timeout,
        allow_multiple_sessions: data.allow_multiple_sessions
      })
      // 备份原始配置
      originalConfig.value = { ...config }
    }
  } catch (error) {
    console.error('获取系统配置失败:', error)
    ElMessage.error('获取系统配置失败')
  } finally {
    loading.value = false
  }
}

// 保存配置
const saveConfig = async () => {
  saving.value = true
  try {
    await updateSystemConfig(config)
    ElMessage.success('系统配置已保存')
    // 更新备份
    originalConfig.value = { ...config }
  } catch (error) {
    console.error('保存系统配置失败:', error)
    ElMessage.error(error.response?.data?.message || '保存系统配置失败')
  } finally {
    saving.value = false
  }
}

// 重置配置
const resetConfig = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要将所有配置恢复为默认值吗？此操作不可撤销。',
      '重置确认',
      {
        confirmButtonText: '确定重置',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    // 恢复到原始配置（从后端获取）
    await fetchConfig()
    ElMessage.success('已恢复为默认值')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重置失败:', error)
      ElMessage.error('重置失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchConfig()
})
</script>

<template>
  <div class="security-config">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h2 class="page-title">安全配置</h2>
        <p class="page-desc">管理系统登录、注册规则和密码策略</p>
      </div>
      <div class="header-actions">
        <el-button @click="fetchConfig">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          刷新
        </el-button>
        <el-button type="warning" @click="resetConfig">重置默认</el-button>
        <el-button type="primary" :loading="saving" @click="saveConfig">保存配置</el-button>
      </div>
    </div>

    <div class="config-container" v-loading="loading">
      <!-- 注册配置 -->
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <div class="card-title-group">
              <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
              </svg>
              <span class="card-title">注册配置</span>
            </div>
          </div>
        </template>

        <div class="config-form">
          <div class="form-item">
            <div class="form-info">
              <span class="form-label">注册需审批</span>
              <span class="form-desc">新用户注册后需要管理员审批才能登录系统</span>
            </div>
            <el-switch v-model="config.require_registration_approval" />
          </div>
        </div>
      </el-card>

      <!-- 密码策略配置 -->
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <div class="card-title-group">
              <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4"/>
              </svg>
              <span class="card-title">密码策略</span>
            </div>
          </div>
        </template>

        <div class="config-form">
          <div class="form-item">
            <div class="form-info">
              <span class="form-label">密码最小长度</span>
              <span class="form-desc">密码至少需要包含的字符数（6-32位）</span>
            </div>
            <el-input-number
              v-model="config.password_min_length"
              :min="6"
              :max="32"
              controls-position="right"
              style="width: 120px"
            />
          </div>

          <div class="form-divider"></div>

          <div class="form-item">
            <div class="form-info">
              <span class="form-label">需要大写字母</span>
              <span class="form-desc">密码必须包含 A-Z 大写字母</span>
            </div>
            <el-switch v-model="config.password_require_uppercase" />
          </div>

          <div class="form-item">
            <div class="form-info">
              <span class="form-label">需要小写字母</span>
              <span class="form-desc">密码必须包含 a-z 小写字母</span>
            </div>
            <el-switch v-model="config.password_require_lowercase" />
          </div>

          <div class="form-item">
            <div class="form-info">
              <span class="form-label">需要数字</span>
              <span class="form-desc">密码必须包含 0-9 数字</span>
            </div>
            <el-switch v-model="config.password_require_number" />
          </div>

          <div class="form-item">
            <div class="form-info">
              <span class="form-label">需要特殊字符</span>
              <span class="form-desc">密码必须包含 !@#$%^&* 等特殊字符</span>
            </div>
            <el-switch v-model="config.password_require_special" />
          </div>
        </div>
      </el-card>

      <!-- 登录安全配置 -->
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <div class="card-title-group">
              <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <span class="card-title">登录安全</span>
            </div>
          </div>
        </template>

        <div class="config-form">
          <div class="form-item">
            <div class="form-info">
              <span class="form-label">最大登录尝试次数</span>
              <span class="form-desc">连续登录失败后账户被锁定的次数（3-20次）</span>
            </div>
            <el-input-number
              v-model="config.max_login_attempts"
              :min="3"
              :max="20"
              controls-position="right"
              style="width: 120px"
            />
          </div>

          <div class="form-item">
            <div class="form-info">
              <span class="form-label">账户锁定时间</span>
              <span class="form-desc">登录失败达到最大次数后，账户锁定时间（5-1440分钟）</span>
            </div>
            <el-input-number
              v-model="config.login_lockout_duration"
              :min="5"
              :max="1440"
              controls-position="right"
              style="width: 120px"
            />
            <span class="unit">分钟</span>
          </div>

          <div class="form-item">
            <div class="form-info">
              <span class="form-label">会话超时时间</span>
              <span class="form-desc">用户无操作后自动退出的时间（10-1440分钟）</span>
            </div>
            <el-input-number
              v-model="config.session_timeout"
              :min="10"
              :max="1440"
              controls-position="right"
              style="width: 120px"
            />
            <span class="unit">分钟</span>
          </div>
        </div>
      </el-card>

      <!-- 其他配置 -->
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <div class="card-title-group">
              <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
              </svg>
              <span class="card-title">其他配置</span>
            </div>
          </div>
        </template>

        <div class="config-form">
          <div class="form-item">
            <div class="form-info">
              <span class="form-label">允许多端登录</span>
              <span class="form-desc">是否允许同一账号在多个设备同时登录</span>
            </div>
            <el-switch v-model="config.allow_multiple_sessions" />
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Security Config - Refined Corporate Design
   ======================================== */
.security-config {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
}

.security-config::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -30px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #f59e0b, #fbbf24, var(--color-warning));
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: 0.5px;
}

.page-desc {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

.btn-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .el-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
}

.header-actions .el-button:hover {
  transform: translateY(-2px);
}

.header-actions .el-button[type="primary"]:hover {
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}

.header-actions .el-button[type="warning"]:hover {
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
}

/* 配置容器 */
.config-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  z-index: 1;
}

/* 配置卡片 */
.config-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all 0.3s ease;
}

.config-card:hover {
  border-color: var(--color-primary-light);
  box-shadow: var(--shadow-md);
}

.config-card :deep(.el-card__header) {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(135deg, var(--color-gray-50) 0%, var(--color-bg-secondary) 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon {
  width: 24px;
  height: 24px;
  color: #f59e0b;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

/* 表单样式 */
.config-form {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 8px 0;
}

.form-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  margin: 0 16px;
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.form-item:hover {
  background: var(--color-gray-50);
}

.form-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.form-desc {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.form-divider {
  height: 1px;
  background: var(--color-border-light);
  margin: 8px 16px;
}

.unit {
  margin-left: 8px;
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .form-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .config-card :deep(.el-card__header) {
    padding: 16px;
  }
}
</style>
