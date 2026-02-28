<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminAnnouncementApi } from '@/api'
import { ArrowLeft, Check, View, Sparkles } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const saving = ref(false)
const isView = ref(false)
const isEdit = ref(false)

const form = ref({
  id: '',
  title: '',
  content: '',
  priority: 1,
  is_pinned: false,
  status: 'draft'
})

const formRules = {
  title: [{ required: true, message: '请输入公告标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入公告内容', trigger: 'blur' }]
}

const formRef = ref(null)

const priorityOptions = [
  { label: '普通', value: 1, color: '#74C69D', icon: '📢' },
  { label: '重要', value: 2, color: '#52B788', icon: '⚠️' },
  { label: '紧急', value: 3, color: '#2D6A4F', icon: '🔔' }
]

const pageTitle = computed(() => {
  if (isView.value) return '查看公告'
  if (isEdit.value) return '编辑公告'
  return '新建公告'
})

const loadAnnouncement = async (id) => {
  try {
    loading.value = true
    const res = await adminAnnouncementApi.getDetail(id)
    if (res.code === 0) {
      form.value = {
        id: res.data.id,
        title: res.data.title,
        content: res.data.content,
        priority: res.data.priority,
        is_pinned: res.data.is_pinned,
        status: res.data.status
      }
    }
  } catch (error) {
    ElMessage.error('加载公告详情失败')
  } finally {
    loading.value = false
  }
}

const handleSaveDraft = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      saving.value = true
      const data = {
        title: form.value.title,
        content: form.value.content,
        priority: form.value.priority,
        is_pinned: form.value.is_pinned,
        status: 'draft'
      }

      let res
      if (isEdit.value) {
        res = await adminAnnouncementApi.update(form.value.id, data)
      } else {
        res = await adminAnnouncementApi.create(data)
      }

      if (res.code === 0) {
        ElMessage.success('草稿保存成功')
        if (!isEdit.value) {
          form.value.id = res.data.id
          isEdit.value = true
        }
      }
    } catch (error) {
      ElMessage.error('保存失败')
    } finally {
      saving.value = false
    }
  })
}

const handlePublish = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      saving.value = true
      const data = {
        title: form.value.title,
        content: form.value.content,
        priority: form.value.priority,
        is_pinned: form.value.is_pinned,
        status: 'published'
      }

      let res
      if (isEdit.value) {
        res = await adminAnnouncementApi.update(form.value.id, data)
      } else {
        res = await adminAnnouncementApi.create(data)
      }

      if (res.code === 0) {
        ElMessage.success('发布成功')
        router.back()
      }
    } catch (error) {
      ElMessage.error('发布失败')
    } finally {
      saving.value = false
    }
  })
}

const handleBack = () => {
  router.back()
}

const getPriorityDesc = (value) => {
  const descs = {
    1: '常规公告',
    2: '重要通知',
    3: '紧急公告'
  }
  return descs[value] || ''
}

const handleClear = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有内容吗？此操作不可撤销。',
      '清空确认',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    form.value.title = ''
    form.value.content = ''
    form.value.priority = 1
    form.value.is_pinned = false
    ElMessage.success('内容已清空')
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  const id = route.query.id
  const view = route.query.view

  if (id) {
    isEdit.value = true
    loadAnnouncement(id)
  }

  if (view) {
    isView.value = true
  }
})
</script>

<template>
  <div class="announcement-edit-container">
    <!-- Leaf Decoration Top Left -->
    <div class="leaf-decoration leaf-decoration--top-left">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 95C50 95 20 80 15 50C10 20 30 5 50 5C70 5 90 20 85 50C80 80 50 95 50 95Z" fill="url(#leafGrad1)" opacity="0.25"/>
        <path d="M50 5L50 95M50 50C35 40 20 45 15 50M50 50C65 40 80 45 85 50" stroke="#40916C" stroke-width="1" opacity="0.3"/>
        <defs>
          <linearGradient id="leafGrad1" x1="15" y1="5" x2="85" y2="95">
            <stop offset="0%" stop-color="#74C69D"/>
            <stop offset="100%" stop-color="#2D6A4F"/>
          </linearGradient>
        </defs>
      </svg>
    </div>

    <!-- Leaf Decoration Bottom Right -->
    <div class="leaf-decoration leaf-decoration--bottom-right">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 95C50 95 20 80 15 50C10 20 30 5 50 5C70 5 90 20 85 50C80 80 50 95 50 95Z" fill="url(#leafGrad2)" opacity="0.25"/>
        <path d="M50 5L50 95M50 50C35 40 20 45 15 50M50 50C65 40 80 45 85 50" stroke="#00B4D8" stroke-width="1" opacity="0.3"/>
        <defs>
          <linearGradient id="leafGrad2" x1="15" y1="5" x2="85" y2="95">
            <stop offset="0%" stop-color="#90E0EF"/>
            <stop offset="100%" stop-color="#00B4D8"/>
          </linearGradient>
        </defs>
      </svg>
    </div>

    <!-- 主标题区 -->
    <header class="page-header">
      <div class="header-content">
        <button class="back-btn" @click="handleBack">
          <ArrowLeft :size="18" />
          <span>返回</span>
        </button>
        <div class="title-section">
          <div class="title-badge">
            <span class="badge-icon">📢</span>
            <span class="badge-text">公告管理</span>
          </div>
          <h1 class="page-title">{{ pageTitle }}</h1>
          <p class="page-subtitle">{{ isView ? '只读模式 - 预览公告内容' : '编辑模式 - 创建或修改公告' }}</p>
        </div>
        <div v-if="!isView" class="header-actions">
          <button class="action-btn draft-btn" :disabled="saving" @click="handleSaveDraft">
            <span class="btn-icon">💾</span>
            <span>{{ saving ? '保存中...' : '保存草稿' }}</span>
          </button>
          <button class="action-btn publish-btn" :disabled="saving" @click="handlePublish">
            <span class="btn-icon">🚀</span>
            <span>{{ saving ? '发布中...' : '立即发布' }}</span>
          </button>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="content-grid">
      <!-- 左侧：编辑表单 -->
      <div class="editor-column">
        <div v-loading="loading" class="editor-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper edit-icon">
                <span>✏️</span>
              </div>
              <div>
                <h3 class="card-title">公告编辑</h3>
                <p class="card-subtitle">{{ isView ? '只读模式' : '填写公告信息' }}</p>
              </div>
            </div>
            <div v-if="isView" class="view-badge">
              <span>👁️ 只读</span>
            </div>
          </div>

          <div class="card-body">
            <el-form
              ref="formRef"
              :model="form"
              :rules="formRules"
              label-position="top"
              :disabled="isView"
            >
              <!-- 标题输入 -->
              <div class="form-section">
                <label class="form-label">
                  <span class="label-icon">✨</span>
                  <span>公告标题</span>
                  <span class="label-required">*</span>
                </label>
                <div class="input-wrapper">
                  <el-input
                    v-model="form.title"
                    placeholder="请输入公告标题..."
                    maxlength="200"
                    show-word-limit
                    class="title-input"
                  />
                </div>
              </div>

              <!-- 优先级选择 -->
              <div class="form-section">
                <label class="form-label">
                  <span class="label-icon">🎯</span>
                  <span>优先级</span>
                </label>
                <div class="priority-grid">
                  <div
                    v-for="option in priorityOptions"
                    :key="option.value"
                    :class="['priority-option', { active: form.priority === option.value }]"
                    :style="{
                      '--priority-color': option.color,
                      '--priority-bg': form.priority === option.value ? option.color + '15' : '#F5F5F4'
                    }"
                    @click="!isView && (form.priority = option.value)"
                  >
                    <div class="priority-icon">{{ option.icon }}</div>
                    <div class="priority-info">
                      <span class="priority-name">{{ option.label }}</span>
                      <span class="priority-desc">{{ getPriorityDesc(option.value) }}</span>
                    </div>
                    <div v-if="form.priority === option.value" class="priority-check">
                      <Check :size="16" />
                    </div>
                  </div>
                </div>
              </div>

              <!-- 置顶开关 -->
              <div class="form-section">
                <div class="toggle-row">
                  <div class="toggle-info">
                    <span class="toggle-icon">📌</span>
                    <div class="toggle-text">
                      <span class="toggle-title">置顶公告</span>
                      <span class="toggle-desc">置顶公告将固定显示在列表顶部</span>
                    </div>
                  </div>
                  <el-switch
                    v-model="form.is_pinned"
                    :disabled="isView"
                    size="large"
                    class="custom-switch"
                  />
                </div>
              </div>

              <!-- 内容编辑 -->
              <div class="form-section">
                <label class="form-label">
                  <span class="label-icon">📝</span>
                  <span>公告内容</span>
                  <span class="label-required">*</span>
                </label>
                <div class="editor-wrapper">
                  <el-input
                    v-model="form.content"
                    type="textarea"
                    :rows="12"
                    placeholder="请输入公告内容..."
                    maxlength="5000"
                    show-word-limit
                    class="content-editor"
                  />
                </div>
              </div>
            </el-form>
          </div>
        </div>
      </div>

      <!-- 右侧：实时预览 -->
      <div class="preview-column">
        <div class="preview-card">
          <div class="card-header">
            <div class="header-left">
              <div class="icon-wrapper preview-icon">
                <span>👁️</span>
              </div>
              <div>
                <h3 class="card-title">实时预览</h3>
                <p class="card-subtitle">查看公告展示效果</p>
              </div>
            </div>
          </div>

          <div class="preview-body">
            <div
              class="announcement-preview"
              :class="{ pinned: form.is_pinned }"
              :style="{
                '--preview-accent': priorityOptions.find(p => p.value === form.priority)?.color || '#74C69D'
              }"
            >
              <!-- 预览顶部信息 -->
              <div class="preview-meta">
                <div
                  class="preview-priority"
                  :style="{
                    backgroundColor: priorityOptions.find(p => p.value === form.priority)?.color + '20',
                    color: priorityOptions.find(p => p.value === form.priority)?.color
                  }"
                >
                  <span class="priority-dot"></span>
                  <span>{{ priorityOptions.find(p => p.value === form.priority)?.label }}</span>
                </div>
                <div v-if="form.is_pinned" class="preview-pin">
                  <span>📌</span>
                  <span>置顶</span>
                </div>
              </div>

              <!-- 预览内容 -->
              <div class="preview-content">
                <h3 class="preview-title">{{ form.title || '公告标题' }}</h3>
                <div class="preview-divider"></div>
                <p class="preview-text">{{ form.content || '公告内容将在这里显示...' }}</p>
              </div>

              <!-- 预览底部 -->
              <div class="preview-footer">
                <div class="preview-time">
                  <span>🕐</span>
                  <span>发布时间：刚刚</span>
                </div>
                <div class="preview-status" :class="{ published: !isEdit || form.status === 'published' }">
                  <span>{{ form.status === 'published' ? '已发布' : '草稿' }}</span>
                </div>
              </div>
            </div>

            <!-- 预览提示 -->
            <div class="preview-tips">
              <div class="tip-item">
                <span class="tip-icon">💡</span>
                <span>预览仅供参考，实际效果可能因显示位置而异</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 快捷操作卡片 -->
        <div v-if="!isView" class="quick-actions">
          <h4 class="actions-title">⚡ 快捷操作</h4>
          <div class="actions-list">
            <button class="quick-action" @click="form.title = '【系统通知】'; form.content = '这是一条系统通知的示例内容...'">
              <span class="action-icon">📋</span>
              <span>使用系统模板</span>
            </button>
            <button class="quick-action" @click="form.priority = 3; form.is_pinned = true">
              <span class="action-icon">🔥</span>
              <span>设为紧急置顶</span>
            </button>
            <button class="quick-action" @click="handleClear">
              <span class="action-icon">🗑️</span>
              <span>清空内容</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ========== 全局样式 ========== */
.announcement-edit-container {
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
  --shadow-card: 0 2px 12px rgba(45, 106, 79, 0.06);

  position: relative;
  min-height: 100vh;
  padding: 24px 32px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  background: linear-gradient(135deg, var(--bg-cream) 0%, var(--bg-sand) 100%);
  overflow-x: hidden;
}

/* ========== 背景装饰 ========== */
.leaf-decoration {
  position: fixed;
  width: 150px;
  height: 150px;
  pointer-events: none;
  z-index: 0;
  opacity: 0.7;
}

.leaf-decoration--top-left {
  top: -30px;
  left: -30px;
  animation: leafFloat1 8s ease-in-out infinite;
}

.leaf-decoration--bottom-right {
  bottom: -30px;
  right: -30px;
  animation: leafFloat2 10s ease-in-out infinite;
}

@keyframes leafFloat1 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(12px, 12px) rotate(3deg); }
}

@keyframes leafFloat2 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(-12px, -12px) rotate(-3deg); }
}

/* ========== 页面头部 ========== */
.page-header {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}

.header-content {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 24px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  box-shadow: var(--shadow-card);
}

.back-btn:hover {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
  transform: translateX(-2px);
}

.title-section {
  flex: 1;
}

.title-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1) 0%, rgba(116, 198, 157, 0.1) 100%);
  border: 1px solid rgba(116, 198, 157, 0.3);
  border-radius: 20px;
  margin-bottom: 14px;
}

.badge-icon {
  font-size: 14px;
}

.badge-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--primary-green);
  font-family: 'Noto Serif SC', serif;
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.draft-btn {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
  box-shadow: var(--shadow-card);
}

.draft-btn:hover:not(:disabled) {
  background: var(--bg-sand);
  border-color: var(--accent-green);
  color: var(--primary-green);
  transform: translateY(-2px);
}

.publish-btn {
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent-green) 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(82, 183, 136, 0.3);
}

.publish-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(82, 183, 136, 0.4);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 14px;
}

/* ========== 内容网格 ========== */
.content-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 24px;
}

/* ========== 编辑器卡片 ========== */
.editor-card,
.preview-card,
.quick-actions {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  padding: 24px;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s ease;
}

.editor-card:hover,
.preview-card:hover {
  box-shadow: var(--shadow-hover);
}

.quick-actions {
  padding: 20px;
}

/* ========== 卡片头部 ========== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 20px;
}

.edit-icon {
  background: linear-gradient(135deg, rgba(45, 106, 79, 0.1), rgba(116, 198, 157, 0.1));
  border: 1px solid rgba(116, 198, 157, 0.3);
}

.preview-icon {
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.1), rgba(144, 224, 239, 0.1));
  border: 1px solid rgba(0, 180, 216, 0.3);
}

.card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  font-weight: 500;
}

.view-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(0, 180, 216, 0.1);
  border: 1px solid rgba(0, 180, 216, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent-blue);
}

/* ========== 卡片主体 ========== */
.card-body {
  position: relative;
}

.form-section {
  margin-bottom: 24px;
}

.form-section:last-child {
  margin-bottom: 0;
}

/* ========== 表单标签 ========== */
.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 10px;
  font-family: 'Noto Serif SC', serif;
}

.label-icon {
  font-size: 14px;
}

.label-required {
  color: #E76F51;
  font-size: 14px;
}

/* ========== 输入框 ========== */
.input-wrapper {
  position: relative;
}

.title-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  background: var(--bg-sand);
  border: 2px solid var(--border-light);
  padding: 14px 18px;
  box-shadow: none;
  transition: all 0.3s ease;
}

.title-input :deep(.el-input__wrapper:hover) {
  border-color: var(--accent-green);
  background: white;
}

.title-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--border-focus);
  background: white;
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.title-input :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 500;
}

.title-input :deep(.el-input__count) {
  color: var(--text-tertiary);
  background: transparent;
}

/* ========== 优先级选择 ========== */
.priority-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.priority-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 16px 12px;
  background: var(--bg-sand);
  border: 2px solid var(--border-light);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.priority-option:hover:not(.active) {
  background: white;
  border-color: var(--accent-green);
}

.priority-option.active {
  background: var(--priority-bg);
  border-color: var(--priority-color);
  box-shadow: 0 4px 15px rgba(116, 198, 157, 0.2);
}

.priority-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 10px;
}

.priority-info {
  text-align: center;
}

.priority-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  display: block;
}

.priority-desc {
  font-size: 11px;
  color: var(--text-tertiary);
  display: block;
}

.priority-check {
  position: absolute;
  top: 8px;
  right: 8px;
  color: var(--priority-color);
}

/* ========== 开关控件 ========== */
.toggle-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 18px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.toggle-row:hover {
  background: white;
  border-color: var(--accent-green);
}

.toggle-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-icon {
  font-size: 20px;
}

.toggle-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toggle-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.toggle-desc {
  font-size: 12px;
  color: var(--text-tertiary);
}

.custom-switch {
  --el-switch-on-color: var(--primary-light);
  --el-switch-off-color: var(--border-light);
}

.custom-switch :deep(.el-switch__core) {
  height: 24px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

/* ========== 富文本编辑器 ========== */
.editor-wrapper {
  position: relative;
}

.content-editor :deep(.el-textarea__inner) {
  border-radius: 12px;
  background: var(--bg-sand);
  border: 2px solid var(--border-light);
  padding: 16px 18px;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.7;
  resize: vertical;
  font-family: inherit;
  transition: all 0.3s ease;
}

.content-editor :deep(.el-textarea__inner:hover) {
  border-color: var(--accent-green);
  background: white;
}

.content-editor :deep(.el-textarea__inner:focus) {
  border-color: var(--border-focus);
  background: white;
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.15);
}

.content-editor :deep(.el-input__count) {
  color: var(--text-tertiary);
  background: transparent;
}

/* ========== 预览列 ========== */
.preview-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-body {
  position: relative;
}

.announcement-preview {
  background: var(--bg-sand);
  border-radius: 16px;
  padding: 20px;
  border-left: 4px solid var(--preview-accent);
  transition: all 0.3s ease;
}

.announcement-preview.pinned {
  background: linear-gradient(135deg, rgba(116, 198, 157, 0.1) 0%, var(--bg-sand) 100%);
  box-shadow: 0 6px 25px rgba(45, 106, 79, 0.15);
}

.preview-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.preview-priority {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.priority-dot {
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

.preview-pin {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: var(--primary-green);
  background: rgba(45, 106, 79, 0.1);
  padding: 5px 10px;
  border-radius: 12px;
}

.preview-content {
  margin-bottom: 16px;
}

.preview-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.preview-divider {
  height: 1px;
  background: linear-gradient(90deg,
    var(--border-light) 0%,
    transparent 100%
  );
  margin-bottom: 12px;
}

.preview-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.preview-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid var(--border-light);
}

.preview-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.preview-status {
  padding: 5px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  background: var(--bg-cream);
  color: var(--text-tertiary);
}

.preview-status.published {
  background: rgba(82, 183, 136, 0.15);
  color: var(--primary-green);
}

.preview-tips {
  margin-top: 14px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: rgba(0, 180, 216, 0.08);
  border: 1px solid rgba(0, 180, 216, 0.2);
  border-radius: 10px;
  font-size: 12px;
  color: var(--text-secondary);
}

.tip-icon {
  font-size: 14px;
}

/* ========== 快捷操作 ========== */
.actions-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 14px 0;
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-action {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.quick-action:hover {
  background: white;
  border-color: var(--accent-green);
  color: var(--primary-green);
  transform: translateX(3px);
}

.action-icon {
  font-size: 16px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    gap: 20px;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .announcement-edit-container {
    padding: 16px;
  }

  .page-title {
    font-size: 26px;
  }

  .content-grid {
    gap: 16px;
  }

  .header-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .priority-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    order: -1;
  }

  .leaf-decoration {
    width: 100px;
    height: 100px;
  }
}
</style>
