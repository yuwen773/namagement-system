<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { feedbackApi } from '@/api'
import { useUserStore } from '@/stores/user'
import { Message, List, Plus, Check, Close } from '@element-plus/icons-vue'

const userStore = useUserStore()

const loading = ref(false)
const submitLoading = ref(false)
const activeTab = ref('submit')
const myFeedbackList = ref([])
const feedbackLoading = ref(false)

const feedbackForm = reactive({
  title: '',
  content: '',
  contact: ''
})

// 提交反馈
const submitFeedback = async () => {
  if (!validateForm()) return

  submitLoading.value = true
  try {
    const res = await feedbackApi.create({
      title: feedbackForm.title,
      content: feedbackForm.content,
      contact: feedbackForm.contact
    })
    if (res.code === 0) {
      ElMessage.success('反馈提交成功')
      resetForm()
      activeTab.value = 'list'
      fetchMyFeedbacks()
    } else {
      ElMessage.error(res.message || '提交失败')
    }
  } catch (error) {
    console.error('Failed to submit feedback:', error)
    ElMessage.error('提交失败，请稍后重试')
  } finally {
    submitLoading.value = false
  }
}

// 验证表单
const validateForm = () => {
  if (!feedbackForm.title.trim()) {
    ElMessage.warning('请输入反馈标题')
    return false
  }
  if (feedbackForm.title.length > 200) {
    ElMessage.warning('标题不能超过200个字符')
    return false
  }
  if (!feedbackForm.content.trim()) {
    ElMessage.warning('请输入反馈内容')
    return false
  }
  return true
}

// 重置表单
const resetForm = () => {
  feedbackForm.title = ''
  feedbackForm.content = ''
  feedbackForm.contact = ''
}

// 获取我的反馈列表
const fetchMyFeedbacks = async () => {
  feedbackLoading.value = true
  try {
    const res = await feedbackApi.getMyList()
    if (res.code === 0) {
      myFeedbackList.value = res.data || []
    }
  } catch (error) {
    console.error('Failed to fetch feedbacks:', error)
  } finally {
    feedbackLoading.value = false
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '---'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取状态标签
const getStatusTag = (status) => {
  return status === 'processed'
    ? { type: 'success', text: '已处理' }
    : { type: 'warning', text: '待处理' }
}

onMounted(() => {
  fetchMyFeedbacks()
})
</script>

<template>
  <div class="feedback-container">
    <!-- 页面标题 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon-wrapper">
            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="28" cy="28" r="26" fill="url(#feedbackHeaderGrad)" fill-opacity="0.15"/>
              <path d="M18 20C18 16 21 14 24 14H32C35 14 38 16 38 20V36C38 38 36 40 34 40H22C20 40 18 38 18 36V20Z" fill="url(#feedbackHeaderLeaf)" stroke="white" stroke-width="1"/>
              <path d="M28 24V32M24 28H32" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <defs>
                <linearGradient id="feedbackHeaderGrad" x1="2" y1="2" x2="54" y2="54">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="feedbackHeaderLeaf" x1="18" y1="14" x2="38" y2="40">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#52B788"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="header-title">意见反馈</h1>
            <p class="header-subtitle">提交您对系统的建议或问题反馈</p>
          </div>
        </div>
        <div class="header-right">
          <div class="user-status-badge">
            <span class="status-dot"></span>
            <span>{{ userStore.userInfo?.username || '用户' }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- 标签页导航 -->
    <nav class="tabs-navigation">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'submit' }"
        @click="activeTab = 'submit'"
      >
        <div class="tab-icon-wrapper">
          <Plus class="tab-icon" />
        </div>
        <span class="tab-label">提交反馈</span>
        <span class="tab-indicator"></span>
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'list' }"
        @click="activeTab = 'list'"
      >
        <div class="tab-icon-wrapper">
          <List class="tab-icon" />
        </div>
        <span class="tab-label">我的反馈</span>
        <span class="tab-indicator"></span>
      </button>
    </nav>

    <!-- 提交反馈表单 -->
    <div v-if="activeTab === 'submit'" class="content-section">
      <div class="feedback-card">
        <div class="feedback-card-header">
          <div class="feedback-header-left">
            <div class="feedback-icon-wrapper">
              <Message class="feedback-icon" />
            </div>
            <div class="feedback-header-text">
              <h2 class="feedback-card-title">反馈表单</h2>
              <p class="feedback-card-subtitle">请详细描述您遇到的问题或建议</p>
            </div>
          </div>
        </div>

        <div class="feedback-card-body">
          <el-form :model="feedbackForm" label-position="top" class="feedback-form">
            <div class="form-field">
              <el-form-item label="反馈标题">
                <el-input
                  v-model="feedbackForm.title"
                  placeholder="请简要描述问题或建议"
                  class="styled-input"
                  maxlength="200"
                  show-word-limit
                />
              </el-form-item>
            </div>
            <div class="form-field">
              <el-form-item label="详细内容">
                <el-input
                  v-model="feedbackForm.content"
                  type="textarea"
                  placeholder="请详细描述您遇到的问题、建议或改进意见..."
                  class="styled-textarea"
                  :rows="6"
                />
              </el-form-item>
            </div>
            <div class="form-field">
              <el-form-item label="联系方式（选填）">
                <el-input
                  v-model="feedbackForm.contact"
                  placeholder="邮箱或手机号，方便我们回复您"
                  class="styled-input"
                />
              </el-form-item>
            </div>

            <div class="form-actions">
              <button class="action-btn action-btn--primary" @click="submitFeedback" :disabled="submitLoading">
                <Message class="btn-icon" />
                {{ submitLoading ? '提交中...' : '提交反馈' }}
              </button>
              <button class="action-btn action-btn--ghost" @click="resetForm">
                <Close class="btn-icon" />
                重置
              </button>
            </div>
          </el-form>
        </div>

        <!-- 装饰植物 -->
        <div class="card-plant">
          <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
            <path d="M30 55V30C30 30 42 22 42 16C42 10 38 6 34 6C34 6 30 10 30 10" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
            <path d="M30 30C30 30 40 24 40 18C40 12 36 8 32 8C32 8 30 12 30 12" stroke="#52B788" stroke-width="1.5" stroke-linecap="round" opacity="0.3"/>
            <circle cx="30" cy="8" r="3" fill="#52B788" opacity="0.5"/>
          </svg>
        </div>
      </div>

      <!-- 提示卡片 -->
      <div class="tips-section">
        <div class="tips-header">
          <div class="tips-icon-wrapper">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="20" fill="url(#tipsLightGrad)" fill-opacity="0.1"/>
              <path d="M24 14V34M24 14L18 20M24 14L30 20" stroke="url(#tipsLightPath)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M24 38V40" stroke="url(#tipsLightPath)" stroke-width="2" stroke-linecap="round"/>
              <defs>
                <linearGradient id="tipsLightGrad" x1="4" y1="4" x2="44" y2="44">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="tipsLightPath" x1="18" y1="14" x2="30" y2="34">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#52B788"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="tips-header-text">
            <h3 class="tips-title">提交提示</h3>
            <p class="tips-subtitle">感谢您的反馈</p>
          </div>
        </div>
        <div class="tips-list">
          <div class="tip-item">
            <div class="tip-check">1</div>
            <span class="tip-text">请确保反馈内容真实有效</span>
          </div>
          <div class="tip-item">
            <div class="tip-check">2</div>
            <span class="tip-text">提供联系方式可帮助我们更快回复</span>
          </div>
          <div class="tip-item">
            <div class="tip-check">3</div>
            <span class="tip-text">我们会在1-3个工作日内处理</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 我的反馈列表 -->
    <div v-if="activeTab === 'list'" class="content-section">
      <div class="list-card">
        <div class="list-card-header">
          <div class="list-header-left">
            <h2 class="list-card-title">我的反馈记录</h2>
            <p class="list-card-subtitle">查看您提交的所有反馈</p>
          </div>
          <div class="list-count">
            <span class="count-number">{{ myFeedbackList.length }}</span>
            <span class="count-label">条反馈</span>
          </div>
        </div>

        <div class="list-card-body">
          <div v-if="feedbackLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>加载中...</span>
          </div>

          <div v-else-if="myFeedbackList.length === 0" class="empty-state">
            <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
              <circle cx="40" cy="40" r="30" fill="url(#emptyGrad)" fill-opacity="0.1"/>
              <path d="M25 35C25 31 28 28 32 28H48C52 28 55 31 55 35V50C55 52 53 54 51 54H29C27 54 25 52 25 50V35Z" stroke="url(#emptyPath)" stroke-width="2" stroke-linecap="round"/>
              <path d="M40 38V46M40 50V50.5" stroke="url(#emptyPath)" stroke-width="2" stroke-linecap="round"/>
              <defs>
                <linearGradient id="emptyGrad" x1="10" y1="10" x2="70" y2="70">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="emptyPath" x1="25" y1="28" x2="55" y2="54">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#52B788"/>
                </linearGradient>
              </defs>
            </svg>
            <p class="empty-text">暂无反馈记录</p>
            <p class="empty-subtext">点击上方"提交反馈"开始反馈</p>
          </div>

          <div v-else class="feedback-list">
            <div
              v-for="item in myFeedbackList"
              :key="item.id"
              class="feedback-item"
            >
              <div class="feedback-item-header">
                <div class="feedback-item-title">{{ item.title }}</div>
                <el-tag
                  :type="getStatusTag(item.status).type"
                  class="status-tag"
                  effect="light"
                  round
                >
                  {{ getStatusTag(item.status).text }}
                </el-tag>
              </div>
              <div class="feedback-item-meta">
                <span class="meta-time">{{ formatDate(item.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页面装饰植物 -->
    <div class="page-plant page-plant--1">
      <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
        <path d="M40 75V35C40 35 60 20 60 20C60 20 50 30 50 30C50 30 40 35 40 35V75" stroke="#74C69D" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
        <path d="M40 35C40 35 50 42 50 30C50 30 42 25 42 25C42 25 40 20 40 20C40 20 30 25 30 25Z" fill="#74C69D" fill-opacity="0.1"/>
      </svg>
    </div>
    <div class="page-plant page-plant--2">
      <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
        <path d="M30 55V25C30 25 45 32 45 32C45 32 35 35 35 35C35 35 30 38 30 38Z" stroke="#52B788" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
        <path d="M30 25C30 25 38 20 38 18C38 16 35 14 35 14C35 14 30 17 30 17Z" fill="#52B788" fill-opacity="0.1"/>
      </svg>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.feedback-container {
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

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  max-width: 900px;
  margin: 0 auto;
  animation: pageFadeIn 0.4s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Page Header
   ============================================ */
.page-header {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: fadeInDown 0.5s ease;
  box-shadow: var(--shadow-soft);
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-15px); }
  to { opacity: 1; transform: translateY(0); }
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28px 32px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon-wrapper {
  width: 56px;
  height: 56px;
  flex-shrink: 0;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.01em;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-status-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  background: rgba(116, 198, 157, 0.1);
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 24px;
  font-size: 13px;
  font-weight: 500;
  color: var(--primary-green);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--primary-green);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ============================================
   Tabs Navigation
   ============================================ */
.tabs-navigation {
  display: flex;
  gap: 12px;
  padding: 8px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.tab-btn {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 14px 24px;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Noto Serif SC', sans-serif;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.tab-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg-card);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tab-btn:hover::before {
  opacity: 1;
}

.tab-btn:hover {
  color: var(--primary-green);
}

.tab-btn.active {
  color: var(--primary-green);
  background: rgba(116, 198, 157, 0.15);
}

.tab-btn.active::before {
  opacity: 0;
}

.tab-icon-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.tab-btn:hover .tab-icon {
  transform: scale(1.1);
}

.tab-label {
  position: relative;
  z-index: 1;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-green), var(--primary-light));
  border-radius: 2px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-btn.active .tab-indicator {
  transform: translateX(-50%) scaleX(1);
}

/* ============================================
   Content Section
   ============================================ */
.content-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInContent 0.5s ease;
}

@keyframes fadeInContent {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Feedback Card
   ============================================ */
.feedback-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
  position: relative;
}

.feedback-card:hover {
  border-color: var(--border-focus);
  box-shadow: var(--shadow-hover);
}

.feedback-card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
}

.feedback-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.feedback-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(116, 198, 157, 0.15), rgba(116, 198, 157, 0.05));
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 12px;
}

.feedback-icon {
  width: 24px;
  height: 24px;
  color: var(--primary-green);
}

.feedback-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.feedback-card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.feedback-card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.feedback-card-body {
  padding: 28px;
}

.feedback-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-field {
  position: relative;
}

.feedback-form :deep(.el-form-item__label) {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}

.styled-input {
  width: 100%;
}

.styled-input :deep(.el-input__wrapper) {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  box-shadow: none;
  padding: 12px 16px;
  transition: all 0.3s ease;
}

.styled-input :deep(.el-input__wrapper:hover) {
  border-color: var(--accent-green);
  background: var(--bg-sand);
}

.styled-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-green);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.1);
}

.styled-input :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
}

.styled-input :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

.styled-textarea :deep(.el-textarea__inner) {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  box-shadow: none;
  padding: 12px 16px;
  transition: all 0.3s ease;
  font-size: 14px;
  font-family: inherit;
}

.styled-textarea :deep(.el-textarea__inner:hover) {
  border-color: var(--accent-green);
  background: var(--bg-sand);
}

.styled-textarea :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-green);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.1);
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  padding-top: 24px;
  border-top: 1px solid var(--border-light);
}

.action-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 28px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Nunito', sans-serif;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: inherit;
  filter: brightness(1.1);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.action-btn:hover::before {
  opacity: 1;
}

.action-btn:active {
  transform: scale(0.98);
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-green), var(--primary-light));
  border: none;
  color: white;
  box-shadow: var(--shadow-soft);
}

.action-btn--primary:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.action-btn--ghost {
  background: transparent;
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
}

.action-btn--ghost:hover {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.btn-icon {
  position: relative;
  width: 16px;
  height: 16px;
  z-index: 1;
}

.card-plant {
  position: absolute;
  bottom: 20px;
  right: 20px;
  opacity: 0.5;
  pointer-events: none;
}

/* ============================================
   Tips Section
   ============================================ */
.tips-section {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 24px 28px;
  position: relative;
  overflow: hidden;
}

.tips-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(116, 198, 157, 0.06) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.tips-icon-wrapper {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.tips-header-text {
  flex: 1;
}

.tips-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.tips-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.tip-item:hover {
  background: rgba(116, 198, 157, 0.05);
  border-color: rgba(116, 198, 157, 0.15);
  transform: translateX(4px);
}

.tip-check {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 106, 79, 0.1);
  border: 1px solid rgba(45, 106, 79, 0.2);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--primary-green);
}

.tip-text {
  font-size: 14px;
  color: var(--text-secondary);
}

/* ============================================
   List Card
   ============================================ */
.list-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.list-card:hover {
  border-color: var(--border-focus);
}

.list-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
}

.list-header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.list-card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.list-card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.list-count {
  display: flex;
  align-items: baseline;
  gap: 6px;
  padding: 10px 20px;
  background: rgba(116, 198, 157, 0.1);
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 16px;
}

.count-number {
  font-family: 'Nunito', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-green);
}

.count-label {
  font-size: 13px;
  color: var(--primary-teal);
}

.list-card-body {
  padding: 20px;
  min-height: 300px;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 60px 20px;
  color: var(--text-tertiary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-light);
  border-top-color: var(--primary-green);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.empty-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 24px 0 8px;
}

.empty-subtext {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* Feedback List */
.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feedback-item {
  padding: 16px 20px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  transition: all 0.3s ease;
}

.feedback-item:hover {
  border-color: var(--accent-green);
  transform: translateX(4px);
}

.feedback-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.feedback-item-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-tag {
  flex-shrink: 0;
}

.feedback-item-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.meta-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* Page Plants */
.page-plant {
  position: fixed;
  pointer-events: none;
  z-index: 0;
  opacity: 0.15;
}

.page-plant--1 {
  bottom: 10%;
  left: 5%;
}

.page-plant--2 {
  top: 20%;
  right: 8%;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 24px;
  }

  .header-right {
    width: 100%;
  }

  .user-status-badge {
    width: 100%;
    justify-content: center;
  }

  .tabs-navigation {
    flex-direction: row;
  }

  .tab-btn {
    padding: 12px 16px;
  }

  .tab-label {
    display: block;
  }

  .feedback-card-body,
  .tips-section,
  .list-card-header {
    padding: 20px;
  }

  .form-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }

  .page-plant {
    display: none;
  }
}
</style>
