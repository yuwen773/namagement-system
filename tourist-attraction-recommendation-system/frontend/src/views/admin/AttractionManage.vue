<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">景点管理</h2>
      <router-link to="/admin/attractions/create">
        <el-button type="primary">新增景点</el-button>
      </router-link>
    </div>
    <el-table :data="attractions" stripe v-loading="loading">
      <el-table-column label="封面">
        <template #default="{ row }">
          <el-image :src="row.coverImage" fit="cover" class="w-16 h-16 rounded" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="category" label="类别">
        <template #default="{ row }">
          <el-tag>{{ row.category }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="region" label="地区" />
      <el-table-column prop="viewCount" label="浏览量" />
      <el-table-column prop="rating" label="评分">
        <template #default="{ row }">{{ row.rating?.toFixed(1) || '-' }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="$router.push(`/admin/attractions/${row.id}/edit`)">编辑</el-button>
          <el-button type="danger" size="small" @click="deleteAttraction(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="mt-4 flex justify-end">
      <el-pagination v-model:current-page="page" :total="total" @current-change="fetchAttractions" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

const attractions = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function fetchAttractions() {
  loading.value = true
  try {
    const res = await request.get('/attractions/', { params: { page: page.value, page_size: 10 } })
    attractions.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function deleteAttraction(row) {
  await ElMessageBox.confirm('确定要删除该景点吗？', '提示', { type: 'warning' })
  await request.delete(`/attractions/${row.id}/`)
  ElMessage.success('删除成功')
  fetchAttractions()
}

onMounted(fetchAttractions)
</script>
