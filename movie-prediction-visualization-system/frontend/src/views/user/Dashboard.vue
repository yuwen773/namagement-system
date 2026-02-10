<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// Top10 影片数据
const topMovies = ref([
  { rank: 1, title: '流浪地球2', box_office: 4040 },
  { rank: 2, title: '满江红', box_office: 3210 },
  { rank: 3, title: '熊出没·伴我熊芯', box_office: 1850 },
  { rank: 4, title: '深海', box_office: 980 },
  { rank: 5, title: '无名', box_office: 870 }
])

onMounted(() => {
  // TODO: 加载数据
})
</script>

<template>
  <div class="dashboard">
    <h2 class="text-2xl font-bold mb-6">数据看板</h2>

    <!-- 欢迎语 -->
    <el-card class="mb-6">
      <div class="flex items-center">
        <el-avatar :size="64" :src="userStore.user?.avatar">
          {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
        </el-avatar>
        <div class="ml-4">
          <h3 class="text-xl font-bold">欢迎回来，{{ userStore.user?.real_name || userStore.user?.username }}</h3>
          <p class="text-gray-500 mt-1">今天是 {{ new Date().toLocaleDateString('zh-CN') }}</p>
        </div>
      </div>
    </el-card>

    <!-- Top10 票房榜 -->
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <span class="font-bold">票房总榜 Top10</span>
          <el-button type="primary" link>查看更多</el-button>
        </div>
      </template>

      <el-table :data="topMovies" stripe>
        <el-table-column prop="rank" label="排名" width="80">
          <template #default="{ row }">
            <el-tag :type="row.rank <= 3 ? 'danger' : 'info'" size="small">
              {{ row.rank }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="影片名称" min-width="150" />
        <el-table-column prop="box_office" label="票房(万)" width="120">
          <template #default="{ row }">
            {{ row.box_office?.toLocaleString() }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'UserDashboard'
}
</script>
