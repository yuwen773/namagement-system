<template>
  <div>
    <!-- 筛选区域 -->
    <div class="bg-white rounded-xl shadow-md p-6 mb-6">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select v-model="filters.category" placeholder="景点类别" clearable>
            <el-option label="自然风光" value="NATURE" />
            <el-option label="人文古迹" value="HISTORY" />
            <el-option label="主题乐园" value="THEME" />
            <el-option label="其他" value="OTHER" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filters.region" placeholder="地区" clearable>
            <el-option label="朝阳区" value="chaoyang" />
            <el-option label="海淀区" value="haidian" />
            <el-option label="东城区" value="dongcheng" />
            <el-option label="西城区" value="xicheng" />
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-input v-model="filters.keyword" placeholder="搜索景点名称..." prefix-icon="Search" />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="fetchAttractions">查询</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 景点列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="item in attractions" :key="item.id" class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer" @click="$router.push(`/attractions/${item.id}`)">
        <el-image :src="item.coverImage" fit="cover" class="w-full h-56" />
        <div class="p-5">
          <div class="flex items-start justify-between mb-2">
            <h3 class="font-semibold text-lg">{{ item.name }}</h3>
            <el-tag size="small">{{ item.category }}</el-tag>
          </div>
          <p class="text-gray-500 text-sm mb-3 flex items-center">
            <el-icon class="mr-1"><Location /></el-icon>
            {{ item.address }}
          </p>
          <div class="flex items-center justify-between">
            <el-rate v-model="item.rating" disabled show-score text-color="#ff9900" />
            <span class="text-blue-600 font-bold text-lg">¥{{ item.price || '免费' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="mt-8 flex justify-center">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :page-sizes="[6, 12, 18, 24]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchAttractions"
        @current-change="fetchAttractions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '@/api/request'
import { Location, Search } from '@element-plus/icons-vue'

const attractions = ref([])
const filters = reactive({
  category: '',
  region: '',
  keyword: ''
})
const pagination = reactive({
  page: 1,
  size: 12,
  total: 0
})

async function fetchAttractions() {
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...(filters.category && { category: filters.category }),
      ...(filters.region && { region: filters.region }),
      ...(filters.keyword && { keyword: filters.keyword })
    }
    const res = await request.get('/attractions/', { params })
    attractions.value = res.data || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error(error)
  }
}

onMounted(fetchAttractions)
</script>
