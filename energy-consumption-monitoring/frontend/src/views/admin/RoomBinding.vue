<template>
  <div class="room-binding-page">
    <div class="page-header">
      <h2>房间绑定审核</h2>
      <p class="page-subtitle">审核用户提交的房间绑定申请</p>
    </div>

    <el-card v-if="pendingRequests.length > 0">
      <el-table :data="pendingRequests" v-loading="loading">
        <el-table-column label="用户" width="180">
          <template #default="{ row }">
            <div class="user-cell">
              <span class="user-name">{{ row.real_name || row.username }}</span>
              <span class="user-username">@{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="申请房间" min-width="300">
          <template #default="{ row }">
            <el-tag v-for="room in row.rooms" :key="room.id" class="room-tag">
              {{ room.building_name }} - {{ room.floor_name }} - {{ room.room_number }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleApprove(row)">
              批准
            </el-button>
            <el-button type="danger" size="small" @click="handleReject(row)">
              拒绝
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-empty v-else description="暂无待审核的绑定申请" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAllPendingBindRequests, approveBindRequest } from '@/api/system'

const loading = ref(false)
const pendingRequests = ref([])

async function loadPendingRequests() {
  loading.value = true
  try {
    const response = await getAllPendingBindRequests()
    pendingRequests.value = response.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('加载待审核申请失败')
  } finally {
    loading.value = false
  }
}

async function handleApprove(row) {
  try {
    await ElMessageBox.confirm(`批准用户 "${row.real_name || row.username}" 的绑定申请？`, '确认批准')
    await approveBindRequest({
      user_id: row.user_id,
      room_ids: row.rooms.map(r => r.id),
      approve: true
    })
    ElMessage.success('已批准绑定申请')
    loadPendingRequests()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

async function handleReject(row) {
  try {
    await ElMessageBox.confirm(`拒绝用户 "${row.real_name || row.username}" 的绑定申请？`, '确认拒绝')
    await approveBindRequest({
      user_id: row.user_id,
      room_ids: row.rooms.map(r => r.id),
      approve: false
    })
    ElMessage.success('已拒绝绑定申请')
    loadPendingRequests()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  loadPendingRequests()
})
</script>

<style scoped>
.room-binding-page {
  padding: 20px;
}
.page-header {
  margin-bottom: 20px;
}
.page-header h2 {
  margin: 0 0 8px;
}
.page-subtitle {
  color: #909399;
  margin: 0;
}
.user-cell {
  display: flex;
  flex-direction: column;
}
.user-name {
  font-weight: 500;
}
.user-username {
  font-size: 12px;
  color: #909399;
}
.room-tag {
  margin: 2px 4px;
}
</style>
