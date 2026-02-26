<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-heritage-gold/10">
    <div class="w-full max-w-md">
      <!-- 登录卡片 -->
      <div class="bg-white rounded-2xl shadow-2xl p-8 space-y-6">
        <!-- Logo 和标题 -->
        <div class="text-center space-y-2">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-heritage-bronze mb-4">
            <el-icon :size="32" class="text-white">
              <Collection />
            </el-icon>
          </div>
          <h1 class="text-3xl font-display font-bold text-gray-900">
            非遗数据平台
          </h1>
          <p class="text-gray-500">Intangible Cultural Heritage System</p>
        </div>

        <!-- 登录表单 -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="用户名"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="w-full"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <!-- 提示信息 -->
        <div class="text-center text-sm text-gray-500">
          <p>测试账号：admin / password123</p>
        </div>
      </div>

      <!-- 底部装饰 -->
      <div class="mt-8 text-center text-sm text-gray-400">
        <p>© 2026 Intangible Cultural Heritage System</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock, Collection } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const success = await userStore.login(loginForm)
      if (success) {
        ElMessage.success('登录成功')
        router.push('/dashboard')
      } else {
        ElMessage.error('登录失败，请检查用户名和密码')
      }
    } catch (error) {
      console.error('Login error:', error)
      ElMessage.error('登录失败，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
:deep(.el-input__wrapper) {
  padding: 12px 16px;
}

:deep(.el-button--large) {
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
}
</style>
