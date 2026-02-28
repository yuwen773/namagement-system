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
  { label: '普通', value: 1, color: '#60a5fa', icon: '📢' },
  { label: '重要', value: 2, color: '#fbbf24', icon: '⚠️' },
  { label: '紧急', value: 3, color: '#f87171', icon: '🔔' }
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
        <button class="back-btn" @click="handleBack">
          <ArrowLeft :size="18" />
          <span>返回</span>
        </button>
        <div class="title-section">
          <div class="title-badge">
            <span class="badge-icon">📢</span>
            <span class="badge-text">ANNOUNCEMENT</span>
          </div>
          <h1 class="page-title">
            <span class="title-gradient">{{ pageTitle }}</span>
          </h1>
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
      <div class="header-visual">
        <div class="floating-icon icon-1">📢</div>
        <div class="floating-icon icon-2">✨</div>
        <div class="floating-icon icon-3">🎯</div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="content-grid">
      <!-- 左侧：编辑表单 -->
      <div class="editor-column">
        <div v-loading="loading" class="editor-card glass-card">
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
                  <div class="input-decoration"></div>
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
                      '--priority-bg': form.priority === option.value ? option.color + '20' : 'transparent'
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
                <div class="editor-toolbar">
                  <div class="toolbar-group">
                    <button class="toolbar-btn" :disabled="isView" title="加粗">
                      <span>B</span>
                    </button>
                    <button class="toolbar-btn" :disabled="isView" title="斜体">
                      <span>I</span>
                    </button>
                    <button class="toolbar-btn" :disabled="isView" title="下划线">
                      <span>U</span>
                    </button>
                  </div>
                  <div class="toolbar-group">
                    <button class="toolbar-btn" :disabled="isView" title="链接">
                      <span>🔗</span>
                    </button>
                    <button class="toolbar-btn" :disabled="isView" title="列表">
                      <span>☰</span>
                    </button>
                  </div>
                  <div class="toolbar-info">
                    <span>{{ form.content.length }} / 5000</span>
                  </div>
                </div>
                <div class="editor-wrapper">
                  <el-input
                    v-model="form.content"
                    type="textarea"
                    :rows="15"
                    placeholder="请输入公告内容..."
                    maxlength="5000"
                    class="content-editor"
                  />
                  <div class="editor-decoration"></div>
                </div>
              </div>
            </el-form>
          </div>

          <!-- 卡片装饰 -->
          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>
      </div>

      <!-- 右侧：实时预览 -->
      <div class="preview-column">
        <div class="preview-card glass-card">
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
                '--preview-accent': priorityOptions.find(p => p.value === form.priority)?.color || '#60a5fa'
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

          <!-- 卡片装饰 -->
          <div class="card-decoration">
            <div class="deco-line deco-1"></div>
            <div class="deco-line deco-2"></div>
            <div class="deco-dot"></div>
          </div>
        </div>

        <!-- 快捷操作卡片 -->
        <div v-if="!isView" class="quick-actions glass-card">
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* ========== 全局样式 ========== */
.announcement-edit-container {
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
  display: flex;
  align-items: flex-start;
  gap: 24px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 107, 53, 0.3);
  color: #fff;
  transform: translateX(-2px);
}

.title-section {
  flex: 1;
}

.title-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 24px;
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
  font-size: 38px;
  font-weight: 700;
  margin: 0 0 10px 0;
  line-height: 1.2;
}

.title-gradient {
  background: linear-gradient(135deg, #FF6B35 0%, #FFD700 50%, #7B2CBF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
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
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.draft-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.draft-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.publish-btn {
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
}

.publish-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 16px;
}

.header-visual {
  position: relative;
  width: 180px;
  height: 90px;
}

.floating-icon {
  position: absolute;
  font-size: 28px;
  animation: iconFloat 3s ease-in-out infinite;
}

.icon-1 { top: 0; right: 0; animation-delay: 0s; }
.icon-2 { top: 25px; right: 50px; animation-delay: 0.5s; }
.icon-3 { top: 45px; right: 15px; animation-delay: 1s; }

@keyframes iconFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}

/* ========== 内容网格 ========== */
.content-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
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
    gap: 20px;
  }
  .header-content {
    flex-direction: column;
    align-items: stretch;
  }
  .header-visual {
    display: none;
  }
  .header-actions {
    width: 100%;
    justify-content: flex-end;
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
  animation: cardSlideIn 0.4s ease backwards;
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

.editor-card { animation-delay: 0.1s; }
.preview-card { animation-delay: 0.2s; }

/* ========== 卡片头部 ========== */
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

.edit-icon {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(255, 107, 53, 0.05));
  border: 1px solid rgba(255, 107, 53, 0.3);
}

.preview-icon {
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

.view-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #06FFA5;
}

/* ========== 卡片主体 ========== */
.card-body {
  position: relative;
  z-index: 1;
}

.form-section {
  margin-bottom: 28px;
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
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 12px;
}

.label-icon {
  font-size: 16px;
}

.label-required {
  color: #FF6B6B;
  font-size: 14px;
}

/* ========== 输入框 ========== */
.input-wrapper {
  position: relative;
}

.title-input {
  --el-input-bg-color: rgba(0, 0, 0, 0.3);
  --el-input-border-color: rgba(255, 255, 255, 0.1);
  --el-input-text-color: rgba(255, 255, 255, 0.9);
  --el-input-placeholder-color: rgba(255, 255, 255, 0.3);
}

.title-input :deep(.el-input__wrapper) {
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 16px 20px;
  box-shadow: none;
  transition: all 0.3s ease;
}

.title-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.title-input :deep(.el-input__wrapper.is-focus) {
  border-color: #FF6B35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.title-input :deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: 500;
}

.title-input :deep(.el-input__count) {
  color: rgba(255, 255, 255, 0.4);
  background: transparent;
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

/* ========== 优先级选择 ========== */
.priority-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.priority-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.priority-option:hover:not(.active) {
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.15);
}

.priority-option.active {
  background: var(--priority-bg);
  border-color: var(--priority-color);
}

.priority-icon {
  font-size: 28px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.priority-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.priority-name {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.priority-desc {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

.priority-check {
  color: var(--priority-color);
}

/* ========== 开关控件 ========== */
.toggle-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  transition: all 0.3s ease;
}

.toggle-row:hover {
  background: rgba(255, 107, 53, 0.03);
  border-color: rgba(255, 107, 53, 0.1);
}

.toggle-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.toggle-icon {
  font-size: 24px;
}

.toggle-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toggle-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.toggle-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.custom-switch {
  --el-switch-on-color: #FF6B35;
  --el-switch-off-color: rgba(255, 255, 255, 0.1);
}

.custom-switch :deep(.el-switch__core) {
  height: 26px;
  border-radius: 13px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ========== 富文本编辑器 ========== */
.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-bottom: none;
  border-radius: 14px 14px 0 0;
}

.toolbar-group {
  display: flex;
  gap: 4px;
}

.toolbar-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Georgia', serif;
}

.toolbar-btn:hover:not(:disabled) {
  background: rgba(255, 107, 53, 0.2);
  border-color: rgba(255, 107, 53, 0.3);
  color: #FF6B35;
}

.toolbar-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.toolbar-info {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.editor-wrapper {
  position: relative;
}

.content-editor {
  --el-input-bg-color: rgba(0, 0, 0, 0.3);
  --el-input-border-color: rgba(255, 255, 255, 0.08);
}

.content-editor :deep(.el-textarea__inner) {
  border-radius: 0 0 14px 14px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-top: none;
  padding: 16px 20px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  line-height: 1.7;
  resize: vertical;
  font-family: inherit;
}

.content-editor :deep(.el-textarea__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.content-editor :deep(.el-textarea__inner:hover) {
  border-color: rgba(255, 107, 53, 0.2);
}

.content-editor :deep(.el-textarea__inner:focus) {
  border-color: #FF6B35;
  background: rgba(255, 107, 53, 0.02);
}

.editor-decoration {
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

/* ========== 预览列 ========== */
.preview-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-body {
  position: relative;
  z-index: 1;
}

.announcement-preview {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid var(--preview-accent);
  transition: all 0.3s ease;
}

.announcement-preview.pinned {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(0, 0, 0, 0.2) 100%);
  box-shadow: 0 8px 30px rgba(255, 107, 53, 0.15);
}

.preview-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.preview-priority {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
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
  font-size: 12px;
  font-weight: 600;
  color: #FF6B35;
  background: rgba(255, 107, 53, 0.1);
  padding: 6px 12px;
  border-radius: 16px;
}

.preview-content {
  margin-bottom: 20px;
}

.preview-title {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.preview-divider {
  height: 1px;
  background: linear-gradient(90deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 100%
  );
  margin-bottom: 16px;
}

.preview-text {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.7;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.preview-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.preview-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.preview-status {
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.5);
}

.preview-status.published {
  background: rgba(6, 255, 165, 0.15);
  color: #06FFA5;
}

.preview-tips {
  margin-top: 16px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(6, 255, 165, 0.05);
  border: 1px solid rgba(6, 255, 165, 0.15);
  border-radius: 10px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.tip-icon {
  font-size: 14px;
}

/* ========== 快捷操作 ========== */
.quick-actions {
  animation-delay: 0.3s;
}

.actions-title {
  font-size: 15px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 16px 0;
  position: relative;
  z-index: 1;
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
  z-index: 1;
}

.quick-action {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}

.quick-action:hover {
  background: rgba(255, 107, 53, 0.08);
  border-color: rgba(255, 107, 53, 0.2);
  transform: translateX(4px);
}

.action-icon {
  font-size: 18px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .announcement-edit-container {
    padding: 16px;
  }

  .page-title {
    font-size: 28px;
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
}
</style>
