<template>
  <div class="min-h-screen flex">
    <!-- 左侧视觉区域（与登录页对称） -->
    <div class="hidden lg:flex flex-1 relative overflow-hidden" style="background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);">
      <!-- 背景装饰 -->
      <div class="absolute inset-0">
        <!-- 网格 -->
        <svg class="absolute inset-0 w-full h-full opacity-10">
          <defs>
            <pattern id="grid2" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" stroke-width="0.5" style="color: rgba(255,255,255,0.3);"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid2)"/>
        </svg>

        <!-- 装饰性胶片元素 -->
        <div class="absolute top-1/3 left-16 w-28 h-42 border-4 border-amber-500/25 rounded-lg -rotate-12 opacity-40">
          <div class="flex h-full">
            <div class="flex-1 border-r border-amber-500/15"></div>
            <div class="flex-1 border-r border-amber-500/15"></div>
            <div class="flex-1"></div>
          </div>
        </div>

        <div class="absolute bottom-1/3 left-28 w-20 h-30 border-4 border-amber-500/20 rounded-lg rotate-6 opacity-35">
          <div class="grid grid-cols-3 h-full gap-1 p-1">
            <div v-for="i in 15" :key="i" class="bg-amber-500/15 rounded-sm"></div>
          </div>
        </div>

        <!-- 粒子 -->
        <div class="absolute inset-0 overflow-hidden">
          <div
            v-for="(particle, index) in particles"
            :key="index"
            class="absolute rounded-full"
            :style="{
              left: particle.x + '%',
              top: particle.y + '%',
              width: particle.size + 'px',
              height: particle.size + 'px',
              background: particle.color,
              animationDelay: particle.delay + 's',
              animationDuration: particle.duration + 's'
            }"
            :class="particle.opacity"
            style="animation: float linear infinite;"
          ></div>
        </div>
      </div>

      <!-- 内容 -->
      <div class="relative z-10 flex flex-col justify-center items-center w-full px-12">
        <div class="text-center">
          <div class="inline-flex items-center justify-center w-24 h-24 rounded-2xl mb-6 shadow-2xl shadow-amber-500/20"
               style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 1px solid rgba(251,191,36,0.3);">
            <svg class="w-14 h-14 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
          </div>

          <h2 class="text-4xl font-bold text-white mb-3">
            加入我们
          </h2>
          <p class="text-lg text-gray-400 mb-8 font-light">
            开启您的票房数据分析之旅
          </p>

          <!-- 特性列表 -->
          <div class="text-left space-y-4 max-w-sm mx-auto">
            <div v-for="(benefit, index) in benefits" :key="index" class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center"
                   style="background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3);">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <span class="text-gray-300">{{ benefit }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="absolute bottom-0 left-0 right-0 h-1" style="background: linear-gradient(90deg, transparent, #fbbf24, transparent);"></div>
    </div>

    <!-- 右侧注册表单区域 -->
    <div class="flex-1 flex items-center justify-center p-8 lg:p-16 relative overflow-hidden">
      <!-- 背景装饰 -->
      <div class="absolute inset-0 opacity-5 pointer-events-none">
        <div class="absolute right-0 top-0 bottom-0 w-24 bg-repeat-y"
             style="background-image: repeating-linear-gradient(
               0deg,
               transparent,
               transparent 40px,
               rgba(255,255,255,0.1) 40px,
               rgba(255,255,255,0.1) 48px
             );">
        </div>
      </div>

      <div class="w-full max-w-md relative z-10">
        <!-- 标题 -->
        <div class="text-center mb-10 lg:hidden">
          <h1 class="text-3xl font-bold mb-2" style="color: #1a1a2e;">注册账号</h1>
          <p class="text-gray-500">创建您的票房预测系统账号</p>
        </div>

        <!-- PC端标题 -->
        <div class="hidden lg:block text-center mb-10">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-xl mb-4"
               style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
            <svg class="w-8 h-8 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold mb-2 tracking-tight" style="color: #1a1a2e;">
            创建账号
          </h1>
          <p class="text-sm tracking-widest uppercase text-gray-500">
            Create Account
          </p>
        </div>

        <!-- 注册表单 -->
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          size="large"
          class="space-y-5"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="用户名 (3-20位字母或数字)"
              class="register-input"
              :disabled="loading"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱地址"
              class="register-input"
              :disabled="loading"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="密码 (6-20位)"
              show-password
              class="register-input"
              :disabled="loading"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="确认密码"
              show-password
              class="register-input"
              :disabled="loading"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 条款同意 -->
          <el-form-item>
            <label class="flex items-center gap-2 cursor-pointer">
              <el-checkbox v-model="registerForm.agreeTerms">
                <span class="text-sm text-gray-600">我已阅读并同意</span>
              </el-checkbox>
              <a href="#" class="text-sm hover:underline" style="color: #d97706;">《服务条款》</a>
              <span class="text-sm text-gray-400">和</span>
              <a href="#" class="text-sm hover:underline" style="color: #d97706;">《隐私政策》</a>
            </label>
          </el-form-item>

          <!-- 注册按钮 -->
          <el-form-item class="mt-6">
            <button
              type="button"
              class="w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-300 cursor-pointer relative overflow-hidden group"
              :disabled="loading"
              @click="handleRegister"
              style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);"
            >
              <span class="relative z-10 flex items-center justify-center gap-2">
                <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                </svg>
                <span>{{ loading ? '注册中...' : '立即注册' }}</span>
              </span>
              <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                   style="background: linear-gradient(135deg, rgba(251,191,36,0.2) 0%, rgba(251,191,36,0.05) 100%);">
              </div>
            </button>
          </el-form-item>
        </el-form>

        <!-- 登录链接 -->
        <div class="text-center mt-8">
          <span class="text-gray-500 text-sm">已有账号？</span>
          <router-link
            to="/login"
            class="text-sm ml-2 hover:underline cursor-pointer transition-colors duration-200"
            style="color: #d97706;"
          >
            立即登录
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)

// 粒子配置
const particles = ref([
  { x: 15, y: 25, size: 4, color: '#fbbf24', opacity: 'bg-amber-400/25', delay: 0, duration: 9 },
  { x: 35, y: 55, size: 3, color: '#60a5fa', opacity: 'bg-blue-400/20', delay: 1.5, duration: 11 },
  { x: 55, y: 35, size: 5, color: '#fbbf24', opacity: 'bg-amber-400/30', delay: 2.5, duration: 8 },
  { x: 75, y: 65, size: 3, color: '#f472b6', opacity: 'bg-pink-400/20', delay: 0.5, duration: 10 },
  { x: 25, y: 75, size: 4, color: '#fbbf24', opacity: 'bg-amber-400/20', delay: 3, duration: 9 },
  { x: 65, y: 20, size: 3, color: '#60a5fa', opacity: 'bg-blue-400/20', delay: 1, duration: 10 },
])

const benefits = ref([
  '获取专业票房数据分析报告',
  'AI 驱动的影片票房预测',
  '实时掌握市场动态趋势',
  '智能推荐潜力影片'
])

// 表单数据
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'user',
  agreeTerms: false
})

// 自定义验证器：确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3-20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9]+$/, message: '用户名只能包含字母和数字', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6-20 个字符', trigger: 'blur' },
    { pattern: /^(?=.*[a-zA-Z])(?=.*[0-9])/, message: '密码需包含字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return

    if (!registerForm.agreeTerms) {
      ElMessage.warning('请阅读并同意服务条款和隐私政策')
      return
    }

    loading.value = true

    try {
      // 调用注册 API
      const response = await register({
        username: registerForm.username,
        email: registerForm.email,
        password: registerForm.password,
        password_confirm: registerForm.confirmPassword
      })

      if (response.code === 0) {
        ElMessage.success({
          message: '注册成功！请登录',
          type: 'success',
          duration: 2000
        })
        
        // 跳转到登录页
        router.push('/login')
      }
    } catch (error) {
      console.error('注册错误:', error)
      ElMessage.error(error.message || '注册失败，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* 输入框样式 */
:deep(.el-input__wrapper) {
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: none;
  border: 1px solid transparent;
  transition: all 0.3s ease;
  padding-left: 4px;
  padding-right: 4px;
}

:deep(.el-input__wrapper:hover) {
  border-color: rgba(251, 191, 36, 0.3);
}

:deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  border-color: rgba(251, 191, 36, 0.5);
  box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.1);
}

:deep(.el-input__inner) {
  height: 52px;
  color: #1a1a2e;
  font-size: 15px;
}

:deep(.el-input__inner::placeholder) {
  color: #9ca3af;
}

:deep(.el-input__prefix) {
  color: #9ca3af;
  left: 12px;
}

/* 错误状态 */
:deep(.el-form-item.is-error .el-input__wrapper) {
  border-color: #ef4444;
}

:deep(.el-form-item.is-error .el-input__wrapper:hover) {
  border-color: #ef4444;
}

:deep(.el-form-item.is-error .el-input__wrapper.is-focus) {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Checkbox 样式 */
:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #d97706;
  border-color: #d97706;
}

:deep(.el-checkbox__input.is-focus .el-checkbox__inner) {
  border-color: #d97706;
}

:deep(.el-checkbox__label) {
  color: #6b7280;
}

/* 动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 移动端 */
@media (max-width: 1024px) {
  .hidden\.lg\:flex {
    display: none !important;
  }
}

@media (max-width: 640px) {
  .min-h-screen {
    padding: 1rem;
  }

  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
