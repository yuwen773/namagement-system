<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-800">
    <div class="max-w-md w-full bg-white rounded-xl shadow-2xl p-8">
      <div class="text-center mb-8">
        <el-icon :size="48" class="text-blue-600"><MapLocation /></el-icon>
        <h2 class="mt-4 text-2xl font-bold text-gray-900">管理员登录</h2>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="w-full" size="large" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { MapLocation } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    if (userStore.user?.role === 'ADMIN') {
      ElMessage.success('登录成功')
      router.push('/admin')
    } else {
      userStore.logout()
      ElMessage.error('非管理员账号')
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
