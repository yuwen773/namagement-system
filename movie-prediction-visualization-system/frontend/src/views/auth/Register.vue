<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 表单数据
const form = reactive({
  username: '',
  email: '',
  password: '',
  passwordConfirm: '',
  real_name: ''
})

// 表单规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  passwordConfirm: [
    { required: true, message: '请确认密码', trigger: 'blur' }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const loading = ref(false)

// 提交表单
const handleSubmit = async () => {
  console.log('handleSubmit 被调用')

  if (!formRef.value) {
    console.log('formRef.value 是 null')
    return
  }

  try {
    const valid = await formRef.value.validate()
    console.log('验证结果:', valid)

    if (!valid) {
      console.log('验证失败')
      ElMessage.warning('请检查输入信息')
      return
    }

    console.log('开始注册...')
    loading.value = true

    await register(form)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    console.log('注册错误:', error)
    // 错误已由 request.js 拦截器处理并显示
  } finally {
    loading.value = false
  }
}

// 跳转到登录
const goToLogin = () => {
  router.push('/login')
}
</script>

<template>
  <div class="register-page flex items-center justify-center min-h-screen bg-gray-100">
    <div class="register-card bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-800">电影票房预测系统</h1>
        <p class="text-gray-500 mt-2">创建您的账户</p>
      </div>

      <!-- 注册表单 -->
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

        <el-form-item prop="real_name">
          <el-input
            v-model="form.real_name"
            placeholder="真实姓名"
            prefix-icon="Postcard"
            clearable
          />
        </el-form-item>

        <el-form-item prop="email">
          <el-input
            v-model="form.email"
            placeholder="邮箱"
            prefix-icon="Message"
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
          />
        </el-form-item>

        <el-form-item prop="passwordConfirm">
          <el-input
            v-model="form.passwordConfirm"
            type="password"
            placeholder="确认密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            class="w-full"
            :loading="loading"
            @click="handleSubmit"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 登录链接 -->
      <div class="text-center mt-4">
        <span class="text-gray-500">已有账户？</span>
        <el-button type="primary" link @click="goToLogin">立即登录</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  width: 100%;
  max-width: 400px;
}
</style>
