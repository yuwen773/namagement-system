<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">公告管理</h2>
      <el-button type="primary" @click="showDialog = true">发布公告</el-button>
    </div>
    <el-table :data="announcements" stripe v-loading="loading">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="content" label="内容" show-overflow-tooltip />
      <el-table-column prop="createdAt" label="发布时间">
        <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button type="danger" size="small" @click="deleteAnnouncement(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <el-dialog v-model="showDialog" title="发布公告" width="500px">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input v-model="form.content" type="textarea" :rows="4" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showDialog = false">取消</el-button>
      <el-button type="primary" @click="publish">发布</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

const announcements = ref([])
const loading = ref(false)
const showDialog = ref(false)
const formRef = ref(null)
const form = reactive({ title: '', content: '' })
const rules = { title: [{ required: true, message: '请输入标题', trigger: 'blur' }], content: [{ required: true, message: '请输入内容', trigger: 'blur' }] }

async function fetchAnnouncements() {
  loading.value = true
  try {
    const res = await request.get('/notifications/announcements/')
    announcements.value = res.data || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function publish() {
  await formRef.value.validate()
  await request.post('/notifications/announcement/', form)
  ElMessage.success('发布成功')
  showDialog.value = false
  form.title = ''
  form.content = ''
  fetchAnnouncements()
}

async function deleteAnnouncement(row) {
  await ElMessageBox.confirm('确定要删除该公告吗？', '提示', { type: 'warning' })
  await request.delete(`/notifications/announcement/${row.id}/`)
  ElMessage.success('删除成功')
  fetchAnnouncements()
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchAnnouncements)
</script>
