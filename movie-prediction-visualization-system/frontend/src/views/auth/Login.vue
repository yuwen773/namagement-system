<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 表单数据
const form = reactive({
  username: '',
  password: ''
})

// 表单规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6-20 个字符', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const loading = ref(false)

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    const result = await userStore.doLogin(form)

    loading.value = false

    if (result.success) {
      ElMessage.success('登录成功')

      // 跳转到重定向页面或首页
      const redirect = route.query.redirect || (userStore.isAdmin ? '/admin' : '/')
      router.push(redirect)
    } else {
      ElMessage.error(result.message || '登录失败')
    }
  })
}

// 跳转到注册
const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="login-page flex items-center justify-center min-h-screen bg-gray-100">
    <div class="login-card bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-800">电影票房预测系统</h1>
        <p class="text-gray-500 mt-2">登录您的账户</p>
      </div>

      <!-- 登录表单 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        size="large"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleSubmit"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            class="w-full"
            :loading="loading"
            @click="handleSubmit"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 注册链接 -->
      <div class="text-center mt-4">
        <span class="text-gray-500">还没有账户？</span>
        <el-button type="primary" link @click="goToRegister">立即注册</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 100%;
  max-width: 400px;
}
</style>
