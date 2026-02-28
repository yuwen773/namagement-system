<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
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
  <div class="announcement-edit-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <button class="back-btn" @click="handleBack">
          <ArrowLeft :size="20" />
          <span>返回</span>
        </button>
        <div class="title-section">
          <div class="icon-wrapper">
            <View :size="24" />
          </div>
          <div>
            <h1>{{ pageTitle }}</h1>
            <p class="subtitle">{{ isView ? '只读模式' : '编辑模式' }}</p>
          </div>
        </div>
        <div v-if="!isView" class="actions">
          <el-button
            type="info"
            :icon="Check"
            :loading="saving"
            @click="handleSaveDraft"
            class="draft-btn"
          >
            保存草稿
          </el-button>
          <el-button
            type="primary"
            :icon="Sparkles"
            :loading="saving"
            @click="handlePublish"
            class="publish-btn"
          >
            立即发布
          </el-button>
        </div>
      </div>
    </div>

    <!-- Form -->
    <div v-loading="loading" class="form-section">
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-position="top"
        :disabled="isView"
        class="announcement-form"
      >
        <!-- Title -->
        <div class="form-group">
          <label class="form-label">
            <span class="label-icon">✨</span>
            公告标题
          </label>
          <el-input
            v-model="form.title"
            placeholder="请输入公告标题..."
            maxlength="200"
            show-word-limit
            class="title-input"
          />
        </div>

        <!-- Priority Selection -->
        <div class="form-group">
          <label class="form-label">
            <span class="label-icon">🎯</span>
            优先级
          </label>
          <div class="priority-cards">
            <div
              v-for="option in priorityOptions"
              :key="option.value"
              :class="['priority-card', { active: form.priority === option.value }]"
              :style="{ borderColor: form.priority === option.value ? option.color : '' }"
              @click="!isView && (form.priority = option.value)"
            >
              <span class="priority-icon">{{ option.icon }}</span>
              <span class="priority-label">{{ option.label }}</span>
            </div>
          </div>
        </div>

        <!-- Pin Toggle -->
        <div class="form-group">
          <div class="pin-toggle">
            <div class="toggle-info">
              <span class="toggle-icon">📌</span>
              <div class="toggle-text">
                <span class="toggle-title">置顶公告</span>
                <span class="toggle-desc">置顶公告将显示在列表最前面</span>
              </div>
            </div>
            <el-switch
              v-model="form.is_pinned"
              :disabled="isView"
              size="large"
              class="pin-switch"
            />
          </div>
        </div>

        <!-- Content -->
        <div class="form-group">
          <label class="form-label">
            <span class="label-icon">📝</span>
            公告内容
          </label>
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="12"
            placeholder="请输入公告内容..."
            maxlength="5000"
            show-word-limit
            class="content-textarea"
          />
        </div>
      </el-form>

      <!-- Preview Card -->
      <div v-if="form.title || form.content" class="preview-section">
        <div class="preview-header">
          <span class="preview-icon">👁️</span>
          <span>实时预览</span>
        </div>
        <div
          class="preview-card"
          :class="{ pinned: form.is_pinned }"
          :style="{ borderLeftColor: priorityOptions.find(p => p.value === form.priority)?.color }"
        >
          <div class="preview-priority" :style="{ backgroundColor: priorityOptions.find(p => p.value === form.priority)?.color + '20', color: priorityOptions.find(p => p.value === form.priority)?.color }">
            {{ priorityOptions.find(p => p.value === form.priority)?.label }}
          </div>
          <div v-if="form.is_pinned" class="preview-pin">📌 置顶</div>
          <h3 class="preview-title">{{ form.title || '公告标题' }}</h3>
          <p class="preview-content">{{ form.content || '公告内容将在这里显示...' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.announcement-edit-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.25);
}

h1 {
  margin: 0 0 4px 0;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
}

.subtitle {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.actions {
  display: flex;
  gap: 12px;
}

.draft-btn {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.publish-btn {
  background: linear-gradient(135deg, #FF6B35 0%, #7B2CBF 100%);
  border: none;
  color: #fff;
  font-weight: 600;
}

/* Form Section */
.form-section {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
  align-items: start;
}

.announcement-form {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 28px;
}

.form-group {
  margin-bottom: 28px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 12px;
}

.label-icon {
  font-size: 16px;
}

/* Title Input */
.title-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 14px 18px;
  box-shadow: none;
  transition: all 0.2s ease;
}

.title-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.title-input :deep(.el-input__wrapper.is-focus) {
  border-color: #FF6B35;
  background: rgba(255, 107, 53, 0.03);
}

.title-input :deep(.el-input__inner) {
  color: #fff;
  font-size: 15px;
}

.title-input :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.title-input :deep(.el-input__count) {
  color: rgba(255, 255, 255, 0.4);
  background: transparent;
}

/* Priority Cards */
.priority-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.priority-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 2px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.priority-card:hover:not(.active) {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
}

.priority-card.active {
  background: rgba(255, 107, 53, 0.08);
  border-width: 2px;
}

.priority-icon {
  font-size: 28px;
}

.priority-label {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.priority-card.active .priority-label {
  color: #fff;
}

/* Pin Toggle */
.pin-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 22px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
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

.pin-switch :deep(.el-switch__core) {
  background: rgba(255, 255, 255, 0.1);
}

/* Content Textarea */
.content-textarea :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px 18px;
  color: #fff;
  font-size: 14px;
  line-height: 1.7;
  resize: vertical;
}

.content-textarea :deep(.el-textarea__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.content-textarea :deep(.el-textarea__inner:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.content-textarea :deep(.el-textarea__inner:focus) {
  border-color: #FF6B35;
  background: rgba(255, 107, 53, 0.03);
}

.content-textarea :deep(.el-input__count) {
  color: rgba(255, 255, 255, 0.4);
  background: transparent;
}

/* Preview Section */
.preview-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  position: sticky;
  top: 24px;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 20px;
}

.preview-icon {
  font-size: 18px;
}

.preview-card {
  background: rgba(255, 255, 255, 0.05);
  border-left: 4px solid #60a5fa;
  border-radius: 12px;
  padding: 20px;
  position: relative;
  transition: all 0.3s ease;
}

.preview-card.pinned {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%);
}

.preview-priority {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.preview-pin {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 12px;
  color: #FF6B35;
  font-weight: 600;
}

.preview-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
}

.preview-content {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.7;
  white-space: pre-wrap;
}

/* Responsive */
@media (max-width: 1024px) {
  .form-section {
    grid-template-columns: 1fr;
  }

  .preview-section {
    position: static;
  }
}
</style>
