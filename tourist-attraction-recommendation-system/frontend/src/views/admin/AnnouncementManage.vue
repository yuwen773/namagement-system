<template>
  <div class="announcement-manage-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">公告管理</h1>
          <p class="page-subtitle">发布和管理系统公告</p>
        </div>
      </div>
      <button @click="openDialog" class="add-button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>发布公告</span>
      </button>
    </div>

    <!-- Announcements List -->
    <div v-loading="loading" class="announcements-list">
      <div v-for="announcement in announcements" :key="announcement.id" class="announcement-card">
        <div class="card-header">
          <div class="announcement-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div class="announcement-info">
            <h3 class="announcement-title">{{ announcement.title }}</h3>
            <p class="announcement-date">{{ formatDate(announcement.createdAt) }}</p>
          </div>
          <button @click="deleteAnnouncement(announcement)" class="delete-button">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
        <div class="card-content">
          <p>{{ announcement.content }}</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="announcements.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        <p>暂无公告</p>
        <button @click="openDialog" class="add-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          发布第一个公告
        </button>
      </div>
    </div>

    <!-- Publish Dialog -->
    <el-dialog v-model="showDialog" title="发布公告" width="500px" class="publish-dialog">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入公告标题" size="large" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="5" placeholder="请输入公告内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <button @click="showDialog = false" class="dialog-button cancel">取消</button>
          <button @click="publish" class="dialog-button confirm" :disabled="publishing">
            {{ publishing ? '发布中...' : '发布' }}
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

const announcements = ref([])
const loading = ref(false)
const showDialog = ref(false)
const publishing = ref(false)
const formRef = ref(null)

const form = reactive({
  title: '',
  content: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

async function fetchAnnouncements() {
  loading.value = true
  try {
    const res = await request.get('/notifications/announcements/')
    announcements.value = res.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('获取公告列表失败')
  } finally {
    loading.value = false
  }
}

function openDialog() {
  form.title = ''
  form.content = ''
  showDialog.value = true
}

async function publish() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    publishing.value = true
    await request.post('/notifications/announcement/', form)
    ElMessage.success('发布成功')
    showDialog.value = false
    form.title = ''
    form.content = ''
    fetchAnnouncements()
  } catch (error) {
    if (error !== false) {
      console.error(error)
      ElMessage.error('发布失败')
    }
  } finally {
    publishing.value = false
  }
}

async function deleteAnnouncement(row) {
  try {
    await ElMessageBox.confirm('确定要删除该公告吗？', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await request.delete(`/notifications/announcement/${row.id}/`)
    ElMessage.success('删除成功')
    fetchAnnouncements()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchAnnouncements)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.announcement-manage-page {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 16px;
  color: #1e3a5f;
}

.header-icon svg {
  width: 28px;
  height: 28px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
}

.add-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3);
}

.add-button svg {
  width: 18px;
  height: 18px;
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 58, 95, 0.4);
}

/* Announcements List */
.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.announcement-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid transparent;
  overflow: hidden;
}

.announcement-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #fbbf24;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 20%, #ffffff 20%);
  border-bottom: 1px solid #f3f4f6;
}

.announcement-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  border-radius: 12px;
  color: white;
  flex-shrink: 0;
}

.announcement-icon svg {
  width: 24px;
  height: 24px;
}

.announcement-info {
  flex: 1;
  min-width: 0;
}

.announcement-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.announcement-date {
  font-size: 13px;
  color: #9ca3af;
}

.delete-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fee2e2;
  border: none;
  border-radius: 10px;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.delete-button svg {
  width: 18px;
  height: 18px;
}

.delete-button:hover {
  background: #fecaca;
  transform: scale(1.05);
}

.card-content {
  padding: 20px 24px;
}

.card-content p {
  font-size: 15px;
  color: #4b5563;
  line-height: 1.7;
  white-space: pre-wrap;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: #9ca3af;
  margin-bottom: 24px;
}

.add-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.add-link svg {
  width: 18px;
  height: 18px;
}

.add-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(251, 191, 36, 0.4);
}

/* Dialog */
:deep(.publish-dialog) {
  border-radius: 16px;
}

:deep(.publish-dialog .el-dialog__header) {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #f3f4f6;
}

:deep(.publish-dialog .el-dialog__title) {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

:deep(.publish-dialog .el-dialog__body) {
  padding: 24px;
}

:deep(.publish-dialog .el-dialog__footer) {
  padding: 16px 24px 24px;
}

:deep(.publish-dialog .el-input__wrapper),
:deep(.publish-dialog .el-textarea__inner) {
  border-radius: 10px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

:deep(.publish-dialog .el-input__wrapper:hover),
:deep(.publish-dialog .el-textarea__inner:hover) {
  border-color: #fbbf24;
}

:deep(.publish-dialog .el-input__wrapper.is-focus),
:deep(.publish-dialog .el-textarea__inner:focus) {
  border-color: #fbbf24;
  box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.1);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.dialog-button {
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.dialog-button.cancel {
  background: #f3f4f6;
  color: #6b7280;
}

.dialog-button.cancel:hover {
  background: #e5e7eb;
}

.dialog-button.confirm {
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  color: white;
}

.dialog-button.confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 58, 95, 0.3);
}

.dialog-button.confirm:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .add-button {
    width: 100%;
    justify-content: center;
  }

  .card-header {
    background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 30%, #ffffff 30%);
  }
}
</style>
