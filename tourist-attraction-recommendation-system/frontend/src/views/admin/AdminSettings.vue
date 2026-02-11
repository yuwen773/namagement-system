<template>
  <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-md p-6">
    <h2 class="text-xl font-bold mb-6">个人设置</h2>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="profile">
        <el-form :model="profileForm" label-width="100px">
          <el-form-item label="用户名">
            <el-input v-model="profileForm.username" disabled />
          </el-form-item>
          <el-form-item label="真实姓名">
            <el-input v-model="profileForm.realName" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="profileForm.phone" />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="profileForm.email" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveProfile">保存</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="password">
        <el-form :model="passwordForm" label-width="100px" :rules="passwordRules" ref="passwordFormRef">
          <el-form-item label="旧密码" prop="oldPassword">
            <el-input v-model="passwordForm.oldPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="changePassword">修改密码</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('profile')
const passwordFormRef = ref(null)
const profileForm = reactive({ username: '', realName: '', phone: '', email: '' })
const passwordForm = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })
const passwordRules = {
  oldPassword: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  newPassword: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (r, v, cb) => v !== passwordForm.newPassword ? cb(new Error('两次密码不一致')) : cb(), trigger: 'blur' }
  ]
}

onMounted(async () => {
  const info = await userStore.getUserInfo()
  Object.assign(profileForm, info)
})

async function saveProfile() {
  await userStore.updateProfile(profileForm)
  ElMessage.success('保存成功')
}

async function changePassword() {
  await passwordFormRef.value.validate()
  await userStore.changePassword(passwordForm.oldPassword, passwordForm.newPassword)
  ElMessage.success('密码修改成功')
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}
</script>
