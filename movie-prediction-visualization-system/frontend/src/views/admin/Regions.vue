<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const tableData = ref([])
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    // TODO: 调用 API
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="regions-page">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">地域管理</h2>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon> 新增地域
      </el-button>
    </div>

    <el-card>
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="地域名称" min-width="150" />
        <el-table-column prop="code" label="地域代码" width="120" />
        <el-table-column prop="parent" label="上级地域" width="120" />
        <el-table-column prop="level" label="层级" width="80" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default>
            <el-button type="primary" link size="small">编辑</el-button>
            <el-button type="danger" link size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminRegions'
}
</script>
