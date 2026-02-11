<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">评论审核</h2>
    </div>
    <el-table :data="comments" stripe v-loading="loading">
      <el-table-column label="用户">
        <template #default="{ row }">
          <div class="flex items-center">
            <el-avatar :size="32">{{ row.user?.realName?.charAt(0) }}</el-avatar>
            <span class="ml-2">{{ row.user?.realName }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="景点">
        <template #default="{ row }">
          <router-link :to="`/admin/attractions/${row.attraction.id}/edit`" class="text-blue-600 hover:underline">
            {{ row.attraction?.name }}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="评论内容" show-overflow-tooltip />
      <el-table-column prop="rating" label="评分">
        <template #default="{ row }">
          <el-rate v-model="row.rating" disabled />
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="发布时间">
        <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="success" size="small" @click="review(row, 'APPROVED')">通过</el-button>
          <el-button type="danger" size="small" @click="review(row, 'REJECTED')">驳回</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="mt-4 flex justify-end">
      <el-pagination v-model:current-page="page" :total="total" @current-change="fetchComments" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const comments = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function fetchComments() {
  loading.value = true
  try {
    const res = await request.get('/statistics/comments/', { params: { page: page.value, page_size: 10, status: 'PENDING' } })
    comments.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function review(comment, status) {
  try {
    await request.put(`/comments/${comment.id}/review/`, { status })
    ElMessage.success(status === 'APPROVED' ? '已通过' : '已驳回')
    fetchComments()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchComments)
</script>
