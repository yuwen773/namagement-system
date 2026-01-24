<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>员工总数</span>
              <el-icon><User /></el-icon>
            </div>
          </template>
          <div class="stat-value">{{ stats.employeeCount }}</div>
          <div class="stat-desc">在职员工</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>部门总数</span>
              <el-icon><OfficeBuilding /></el-icon>
            </div>
          </template>
          <div class="stat-value">{{ stats.departmentCount }}</div>
          <div class="stat-desc">已创建部门</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>岗位总数</span>
              <el-icon><Postcard /></el-icon>
            </div>
          </template>
          <div class="stat-value">{{ stats.postCount }}</div>
          <div class="stat-desc">已创建岗位</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="chart-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>快捷操作</span>
        </div>
      </template>
      <div class="quick-actions">
        <el-button type="primary" @click="$router.push('/employees')">
          <el-icon><User /></el-icon> 员工管理
        </el-button>
        <el-button type="success" @click="$router.push('/departments')">
          <el-icon><OfficeBuilding /></el-icon> 部门管理
        </el-button>
        <el-button type="warning" @click="$router.push('/attendance')">
          <el-icon><Clock /></el-icon> 考勤管理
        </el-button>
        <el-button type="danger" @click="$router.push('/salary')">
          <el-icon><Money /></el-icon> 薪资管理
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, OfficeBuilding, Postcard } from '@element-plus/icons-vue'
import { getEmployeeList } from '@/api/employee'
import { getDepartmentList } from '@/api/department'
import { getPostList } from '@/api/post'

const stats = ref({
  employeeCount: 0,
  departmentCount: 0,
  postCount: 0
})

onMounted(async () => {
  try {
    const [empRes, deptRes, postRes] = await Promise.all([
      getEmployeeList(),
      getDepartmentList(),
      getPostList()
    ])
    stats.value.employeeCount = empRes.data?.total || 0
    stats.value.departmentCount = Array.isArray(deptRes.data?.data) ? deptRes.data.data.length : 0
    stats.value.postCount = Array.isArray(postRes.data?.data) ? postRes.data.data.length : 0
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
.home {
  padding: 0;
}

.stat-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
  text-align: center;
  padding: 20px 0;
}

.stat-desc {
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.chart-card {
  margin-top: 20px;
}

.quick-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  padding: 20px 0;
}
</style>
