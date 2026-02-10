<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const tableData = ref([])
const loading = ref(false)
const total = ref(0)
const queryParams = ref({
  page: 1,
  pageSize: 10,
  search: ''
})

// TODO: 导入 API
// import { getMovies, deleteMovie } from '@/api/movie'

const handleSearch = () => {
  queryParams.value.page = 1
  loadData()
}

const handleSizeChange = (val) => {
  queryParams.value.pageSize = val
  loadData()
}

const handleCurrentChange = (val) => {
  queryParams.value.page = val
  loadData()
}

const loadData = async () => {
  loading.value = true
  try {
    // TODO: 调用 API
    // const res = await getMovies(queryParams.value)
    // tableData.value = res.data
    // total.value = res.total
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
  <div class="movies-page">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">影片管理</h2>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon> 新增影片
      </el-button>
    </div>

    <!-- 搜索栏 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="queryParams">
        <el-form-item label="影片名称">
          <el-input v-model="queryParams.search" placeholder="请输入影片名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card>
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="影片名称" min-width="150" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="release_date" label="上映日期" width="120" />
        <el-table-column prop="duration" label="时长(分钟)" width="100" />
        <el-table-column prop="box_office" label="票房(万)" width="100" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default>
            <el-button type="primary" link size="small">编辑</el-button>
            <el-button type="danger" link size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
// 导出组件
export default {
  name: 'AdminMovies'
}
</script>
