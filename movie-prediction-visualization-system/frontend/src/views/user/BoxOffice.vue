<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const tableData = ref([])
const loading = ref(false)
const total = ref(0)
const queryParams = ref({
  page: 1,
  pageSize: 10,
  movie: '',
  dateRange: []
})

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

const handleSearch = () => {
  queryParams.value.page = 1
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="boxoffice-page">
    <h2 class="text-2xl font-bold mb-6">票房查询中心</h2>

    <!-- 搜索栏 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="queryParams">
        <el-form-item label="影片名称">
          <el-input v-model="queryParams.movie" placeholder="请输入影片名称" clearable />
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="queryParams.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card>
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="movie" label="影片名称" min-width="150" />
        <el-table-column prop="cinema" label="影院" min-width="150" />
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="revenue" label="票房收入" width="120">
          <template #default="{ row }">
            {{ row.revenue?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="audience" label="观影人数" width="100" />
      </el-table>

      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :total="total"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'UserBoxOffice'
}
</script>
