<template>
  <div class="attraction-edit-page">
    <!-- Header -->
    <div class="page-header">
      <button @click="router.back()" class="back-button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        <span>返回</span>
      </button>
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">{{ isEdit ? '编辑景点' : '新增景点' }}</h1>
          <p class="page-subtitle">{{ isEdit ? '修改景点信息' : '创建新的旅游景点' }}</p>
        </div>
      </div>
    </div>

    <!-- Form Container -->
    <div class="form-container">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="attraction-form">
        <!-- Basic Info Section -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <div>
              <h3 class="section-title">基本信息</h3>
              <p class="section-subtitle">填写景点的基本资料</p>
            </div>
          </div>

          <div class="form-grid">
            <el-form-item label="景点名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入景点名称" size="large" />
            </el-form-item>

            <el-form-item label="景点类别" prop="category">
              <el-select v-model="form.category" placeholder="选择类别" size="large" class="full-width">
                <el-option label="自然风光" value="NATURE">
                  <div class="option-item">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                    <span>自然风光</span>
                  </div>
                </el-option>
                <el-option label="人文古迹" value="HISTORY">
                  <div class="option-item">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd"/></svg>
                    <span>人文古迹</span>
                  </div>
                </el-option>
                <el-option label="主题乐园" value="THEME">
                  <div class="option-item">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.699-3.181a1 1 0 011.827 1.035L17.13 7.84l3.928.786a1 1 0 01.17 1.933l-3.486 1.243 1.037 3.877a1 1 0 01-1.558 1.075l-3.073-2.384L11.582 15.5a1 1 0 01-1.164 0l-2.436-1.8-3.073 2.384a1 1 0 01-1.558-1.075l1.037-3.877-3.486-1.243a1 1 0 01.17-1.933l3.928-.786 1.094-4.081a1 1 0 011.827-1.035L8.046 4.323V3a1 1 0 011-1z" clip-rule="evenodd"/></svg>
                    <span>主题乐园</span>
                  </div>
                </el-option>
                <el-option label="其他" value="OTHER">
                  <div class="option-item">
                    <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 4.5A2.5 2.5 0 014.5 2h11a2.5 2.5 0 010 5h-11A2.5 2.5 0 012 4.5zM2.5 9.5A1.5 1.5 0 014 8h12a1.5 1.5 0 010 3H4a1.5 1.5 0 01-1.5-1.5zm0 5A1.5 1.5 0 014 13h12a1.5 1.5 0 010 3H4a1.5 1.5 0 01-1.5-1.5z"/></svg>
                    <span>其他</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="所属地区" prop="region">
              <el-input v-model="form.region" placeholder="如: 北京" size="large" />
            </el-form-item>

            <el-form-item label="详细地址" prop="address">
              <el-input v-model="form.address" placeholder="请输入详细地址" size="large" />
            </el-form-item>

            <el-form-item label="开放时间" prop="openingHours">
              <el-input v-model="form.openingHours" placeholder="如: 9:00-18:00" size="large" />
            </el-form-item>

            <el-form-item label="门票价格" prop="price">
              <el-input-number v-model="form.price" :min="0" :precision="2" size="large" class="full-width" />
            </el-form-item>
          </div>
        </div>

        <!-- Description Section -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
            </div>
            <div>
              <h3 class="section-title">景点介绍</h3>
              <p class="section-subtitle">详细描述景点特色</p>
            </div>
          </div>

          <el-form-item label="景点描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="6"
              placeholder="请输入景点详细介绍，包括历史背景、特色亮点等..."
              maxlength="2000"
              show-word-limit
            />
          </el-form-item>
        </div>

        <!-- Images Section -->
        <div class="form-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
            </div>
            <div>
              <h3 class="section-title">图片上传</h3>
              <p class="section-subtitle">上传景点封面和展示图片</p>
            </div>
          </div>

          <el-form-item label="封面图片" prop="coverImage">
            <div class="upload-wrapper">
              <el-upload
                action="/api/attractions/upload/"
                :show-file-list="false"
                :on-success="handleCoverSuccess"
                :before-upload="beforeUpload"
                drag
                class="cover-upload"
              >
                <div v-if="form.coverImage" class="preview-image">
                  <img :src="form.coverImage" alt="封面预览" />
                  <div class="preview-overlay">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="17 8 12 3 7 8"/>
                      <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                    <span>点击更换</span>
                  </div>
                </div>
                <div v-else class="upload-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21 15 16 10 5 21"/>
                  </svg>
                  <div class="upload-text">
                    <p class="upload-title">拖拽图片到此处</p>
                    <p class="upload-hint">或点击上传</p>
                  </div>
                </div>
              </el-upload>
            </div>
          </el-form-item>
        </div>

        <!-- Form Actions -->
        <div class="form-actions">
          <button type="button" @click="router.back()" class="action-button cancel">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            取消
          </button>
          <button type="button" @click="saveAttraction" class="action-button save" :disabled="loading">
            <svg v-if="!loading" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="spin" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity="0.3"/>
              <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
            </svg>
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  name: '',
  category: '',
  region: '',
  address: '',
  openingHours: '',
  price: 0,
  coverImage: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入景点名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
}

async function fetchAttraction() {
  if (!isEdit.value) return
  try {
    const res = await request.get(`/attractions/${route.params.id}/`)
    Object.assign(form, res.data)
  } catch (error) {
    console.error(error)
    ElMessage.error('获取景点信息失败')
  }
}

function beforeUpload(file) {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB')
    return false
  }
  return true
}

function handleCoverSuccess(res) {
  form.coverImage = res.data?.url || res.data
}

async function saveAttraction() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    if (isEdit.value) {
      await request.put(`/attractions/${route.params.id}/`, form)
    } else {
      await request.post('/attractions/', form)
    }

    ElMessage.success('保存成功')
    router.push('/admin/attractions')
  } catch (error) {
    if (error !== false) { // Not a validation error
      console.error(error)
      ElMessage.error('保存失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchAttraction)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.attraction-edit-page {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Header */
.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button svg {
  width: 18px;
  height: 18px;
}

.back-button:hover {
  background: #f9fafb;
  border-color: #fbbf24;
  color: #1e3a5f;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.header-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
  border-radius: 12px;
  color: #1e3a5f;
}

.header-icon svg {
  width: 24px;
  height: 24px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
}

/* Form Container */
.form-container {
  max-width: 900px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.attraction-form {
  padding: 32px;
}

/* Form Sections */
.form-section {
  margin-bottom: 32px;
}

.form-section:last-of-type {
  margin-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.section-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 10px;
  color: #1e3a5f;
}

.section-icon svg {
  width: 20px;
  height: 20px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.section-subtitle {
  font-size: 13px;
  color: #9ca3af;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* Custom Input Styling */
:deep(.el-input__wrapper),
:deep(.el-textarea__inner) {
  border-radius: 10px;
  border: 2px solid #e5e7eb;
  padding: 8px 16px;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

:deep(.el-input__wrapper:hover),
:deep(.el-textarea__inner:hover) {
  border-color: #fbbf24;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-textarea__inner:focus) {
  border-color: #fbbf24;
  box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.1);
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  font-size: 14px;
  color: #1f2937;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.full-width {
  width: 100%;
}

/* Select Options */
:deep(.option-item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.option-item svg) {
  width: 18px;
  height: 18px;
  color: #f97316;
}

/* Upload */
.upload-wrapper {
  width: 100%;
}

.cover-upload {
  width: 100%;
}

:deep(.cover-upload .el-upload) {
  width: 100%;
}

:deep(.cover-upload .el-upload-dragger) {
  width: 100%;
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  background: #f9fafb;
  transition: all 0.3s ease;
}

:deep(.cover-upload .el-upload-dragger:hover) {
  border-color: #fbbf24;
  background: #fef3c7;
}

.preview-image {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
  border-radius: 12px;
  overflow: hidden;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.preview-overlay:hover {
  opacity: 1;
}

.preview-overlay svg {
  width: 32px;
  height: 32px;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #9ca3af;
}

.upload-placeholder svg {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
}

.upload-text {
  text-align: center;
}

.upload-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.upload-hint {
  font-size: 14px;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 32px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  min-width: 120px;
}

.action-button svg {
  width: 18px;
  height: 18px;
}

.action-button.cancel {
  background: #f3f4f6;
  color: #6b7280;
}

.action-button.cancel:hover {
  background: #e5e7eb;
}

.action-button.save {
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  color: white;
}

.action-button.save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 58, 95, 0.3);
}

.action-button.save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .back-button {
    width: 100%;
    justify-content: center;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .attraction-form {
    padding: 20px;
  }

  .form-actions {
    flex-direction: column;
  }

  .action-button {
    width: 100%;
  }
}
</style>
