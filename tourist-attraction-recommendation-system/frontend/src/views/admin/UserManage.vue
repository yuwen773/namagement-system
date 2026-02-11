<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">用户管理</h2>
    </div>
    <el-table :data="users" stripe v-loading="loading">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="realName" label="真实姓名" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色">
        <template #default="{ row }">
          <el-tag :type="row.role === 'ADMIN' ? 'danger' : 'primary'">{{ row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="isActive" label="状态">
        <template #default="{ row }">
          <el-switch v-model="row.isActive" @change="updateStatus(row)" />
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="注册时间">
        <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
      </el-table-column>
    </el-table>
    <div class="mt-4 flex justify-end">
      <el-pagination v-model:current-page="page" :total="total" @current-change="fetchUsers" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const users = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function fetchUsers() {
  loading.value = true
  try {
    const res = await request.get('/statistics/users/', { params: { page, page_size: 10 } })
    users.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function updateStatus(user) {
  try {
    await request.put(`/statistics/users/${user.id}/status/`, { is_active: user.isActive })
    ElMessage.success('状态已更新')
  } catch (error) {
    ElMessage.error('更新失败')
    user.isActive = !user.isActive
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchUsers)
</script>
