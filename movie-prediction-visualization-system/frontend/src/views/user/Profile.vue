<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

const form = reactive({
  username: userStore.user?.username || '',
  email: userStore.user?.email || '',
  real_name: userStore.user?.real_name || '',
  phone: userStore.user?.phone || ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const activeTab = ref('profile')

const handleSaveProfile = async () => {
  try {
    // TODO: 调用 API 保存个人信息
    ElMessage.success('个人信息更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const handleChangePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  try {
    // TODO: 调用 API 修改密码
    ElMessage.success('密码修改成功')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error) {
    ElMessage.error('密码修改失败')
  }
}
</script>

<template>
  <div class="profile-page">
    <h2 class="text-2xl font-bold mb-6">个人中心</h2>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div class="text-center">
            <el-avatar :size="120" :src="userStore.user?.avatar">
              {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
            </el-avatar>
            <h3 class="text-xl font-bold mt-4">{{ userStore.user?.real_name || userStore.user?.username }}</h3>
            <p class="text-gray-500">{{ userStore.user?.role === 'ADMIN' ? '管理员' : '普通用户' }}</p>
          </div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="基本信息" name="profile">
              <el-form :model="form" label-width="100px" style="max-width: 500px;">
                <el-form-item label="用户名">
                  <el-input v-model="form.username" disabled />
                </el-form-item>
                <el-form-item label="真实姓名">
                  <el-input v-model="form.real_name" />
                </el-form-item>
                <el-form-item label="邮箱">
                  <el-input v-model="form.email" />
                </el-form-item>
                <el-form-item label="手机号">
                  <el-input v-model="form.phone" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleSaveProfile">保存修改</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="安全设置" name="security">
              <el-form :model="passwordForm" label-width="100px" style="max-width: 500px;">
                <el-form-item label="当前密码">
                  <el-input v-model="passwordForm.oldPassword" type="password" show-password />
                </el-form-item>
                <el-form-item label="新密码">
                  <el-input v-model="passwordForm.newPassword" type="password" show-password />
                </el-form-item>
                <el-form-item label="确认密码">
                  <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'UserProfile'
}
</script>
