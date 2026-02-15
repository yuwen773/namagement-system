<template>
  <div class="min-h-screen flex">
    <!-- 左侧登录表单区域 -->
    <div class="flex-1 flex items-center justify-center p-8 lg:p-16 relative overflow-hidden">
      <!-- 背景装饰：电影胶片孔纹理 -->
      <div class="absolute inset-0 opacity-5 pointer-events-none">
        <div class="absolute left-0 top-0 bottom-0 w-24 bg-repeat-x"
             style="background-image: repeating-linear-gradient(
               0deg,
               transparent,
               transparent 40px,
               rgba(255,255,255,0.1) 40px,
               rgba(255,255,255,0.1) 48px
             );">
        </div>
      </div>

      <!-- 装饰性圆形光晕 -->
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-amber-500/20 to-transparent rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-blue-500/10 to-transparent rounded-full blur-3xl"></div>

      <div class="w-full max-w-md relative z-10">
        <!-- Logo 和标题 -->
        <div class="text-center mb-10">
          <div class="inline-flex items-center justify-center w-20 h-20 rounded-2xl mb-6 shadow-2xl shadow-amber-500/20"
               style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 1px solid rgba(251,191,36,0.3);">
            <svg class="w-10 h-10 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold mb-2 tracking-tight" style="color: #1a1a2e;">
            票房预测系统
          </h1>
          <p class="text-sm tracking-widest uppercase" style="color: #6b7280;">
            Box Office Analytics
          </p>
        </div>

        <!-- 登录表单 -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          size="large"
          class="space-y-6"
        >
          <!-- 用户名字段 -->
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              class="login-input"
              :disabled="loading"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 密码字段 -->
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
              class="login-input"
              :disabled="loading"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 登录按钮 -->
          <el-form-item class="mt-8">
            <button
              type="button"
              class="w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-300 cursor-pointer relative overflow-hidden group"
              :disabled="loading"
              @click="handleLogin"
              style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);"
            >
              <span class="relative z-10 flex items-center justify-center gap-2">
                <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
                </svg>
                <span>{{ loading ? '登录中...' : '登 录' }}</span>
              </span>
              <!-- 按钮悬停光效 -->
              <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                   style="background: linear-gradient(135deg, rgba(251,191,36,0.2) 0%, rgba(251,191,36,0.05) 100%);">
              </div>
            </button>
          </el-form-item>
        </el-form>

        <!-- 注册链接 -->
        <div class="text-center mt-8">
          <span class="text-gray-500 text-sm">还没有账号？</span>
          <router-link
            to="/register"
            class="text-sm ml-2 hover:underline cursor-pointer transition-colors duration-200"
            style="color: #d97706;"
          >
            立即注册
          </router-link>
        </div>

        <!-- 演示账号提示 -->
        <div class="mt-8 p-4 rounded-xl border bg-gray-50" style="border-color: rgba(251,191,36,0.3);">
          <p class="text-xs font-medium mb-2" style="color: #92400e;">演示账号</p>
          <div class="space-y-1 text-xs" style="color: #6b7280;">
            <p><span class="font-medium">管理员：</span>admin / admin123</p>
            <p><span class="font-medium">普通用户：</span>test / test123</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧视觉展示区域 -->
    <div class="hidden lg:flex flex-1 relative overflow-hidden" style="background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%);">
      <!-- 动态背景：票房曲线抽象画 -->
      <div class="absolute inset-0">
        <!-- 网格背景 -->
        <svg class="absolute inset-0 w-full h-full opacity-10">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" stroke-width="0.5" style="color: rgba(255,255,255,0.3);"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)"/>
        </svg>

        <!-- 抽象票房曲线装饰 -->
        <svg class="absolute inset-0 w-full h-full" viewBox="0 0 400 300" preserveAspectRatio="none">
          <defs>
            <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:0" />
              <stop offset="50%" style="stop-color:#fbbf24;stop-opacity:0.6" />
              <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:0" />
            </linearGradient>
            <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:0.15" />
              <stop offset="100%" style="stop-color:#fbbf24;stop-opacity:0" />
            </linearGradient>
          </defs>

          <!-- 票房增长曲线 -->
          <path
            d="M 0 250 Q 50 240, 80 220 T 150 180 T 220 140 T 280 100 T 350 60 T 400 40"
            fill="none"
            stroke="url(#goldGradient)"
            stroke-width="3"
            class="animate-pulse"
          />
          <path
            d="M 0 250 Q 50 240, 80 220 T 150 180 T 220 140 T 280 100 T 350 60 T 400 40 L 400 300 L 0 300 Z"
            fill="url(#areaGradient)"
          />

          <!-- 第二条曲线 -->
          <path
            d="M 0 280 Q 100 270, 140 250 T 200 220 T 280 180 T 360 140 T 400 120"
            fill="none"
            stroke="rgba(96,165,250,0.4)"
            stroke-width="2"
            stroke-dasharray="5,5"
          />
        </svg>

        <!-- 电影胶片装饰元素 -->
        <div class="absolute top-1/4 right-12 w-32 h-48 border-4 border-amber-500/30 rounded-lg rotate-12 opacity-50">
          <div class="flex h-full">
            <div class="flex-1 border-r border-amber-500/20"></div>
            <div class="flex-1 border-r border-amber-500/20"></div>
            <div class="flex-1"></div>
          </div>
        </div>

        <div class="absolute bottom-1/4 right-24 w-24 h-36 border-4 border-amber-500/20 rounded-lg -rotate-6 opacity-40">
          <div class="grid grid-cols-3 h-full gap-1 p-1">
            <div v-for="i in 18" :key="i" class="bg-amber-500/20 rounded-sm"></div>
          </div>
        </div>

        <!-- 粒子装饰 -->
        <div class="absolute inset-0 overflow-hidden">
          <div
            v-for="(particle, index) in particles"
            :key="index"
            class="absolute rounded-full animate-float"
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
          ></div>
        </div>
      </div>

      <!-- 内容卡片 -->
      <div class="relative z-10 flex flex-col justify-center items-center w-full px-12">
        <div class="text-center">
          <!-- 大标题 -->
          <h2 class="text-5xl font-bold text-white mb-4 tracking-tight">
            数据驱动
            <span style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
              票房预测
            </span>
          </h2>
          <p class="text-xl text-gray-400 mb-8 font-light">
            基于 AI 的智能票房分析平台
          </p>

          <!-- 特性标签 -->
          <div class="flex flex-wrap justify-center gap-3">
            <span
              v-for="feature in features"
              :key="feature"
              class="px-4 py-2 rounded-full text-sm border backdrop-blur-sm"
              style="border-color: rgba(251,191,36,0.3); color: #fbbf24; background: rgba(251,191,36,0.05);"
            >
              {{ feature }}
            </span>
          </div>

          <!-- 数据展示 -->
          <div class="mt-12 grid grid-cols-3 gap-6">
            <div class="text-center">
              <p class="text-3xl font-bold text-white">10K+</p>
              <p class="text-sm text-gray-500">历史影片</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold text-white">98%</p>
              <p class="text-sm text-gray-500">预测准确率</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold text-white">500+</p>
              <p class="text-sm text-gray-500">合作影院</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部装饰 -->
      <div class="absolute bottom-0 left-0 right-0 h-1" style="background: linear-gradient(90deg, transparent, #fbbf24, transparent);"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref(null)
const loading = ref(false)

// 粒子效果配置
const particles = ref([
  { x: 10, y: 20, size: 4, color: '#fbbf24', opacity: 'bg-amber-400/30', delay: 0, duration: 8 },
  { x: 25, y: 60, size: 3, color: '#60a5fa', opacity: 'bg-blue-400/20', delay: 1, duration: 10 },
  { x: 40, y: 30, size: 5, color: '#fbbf24', opacity: 'bg-amber-400/25', delay: 2, duration: 7 },
  { x: 55, y: 70, size: 3, color: '#f472b6', opacity: 'bg-pink-400/20', delay: 0.5, duration: 9 },
  { x: 70, y: 40, size: 4, color: '#fbbf24', opacity: 'bg-amber-400/30', delay: 3, duration: 11 },
  { x: 85, y: 25, size: 3, color: '#60a5fa', opacity: 'bg-blue-400/20', delay: 1.5, duration: 8 },
  { x: 15, y: 80, size: 4, color: '#fbbf24', opacity: 'bg-amber-400/20', delay: 2.5, duration: 9 },
  { x: 75, y: 75, size: 3, color: '#f472b6', opacity: 'bg-pink-400/20', delay: 4, duration: 10 },
])

const features = ref([
  '实时票房分析', 'AI 趋势预测', '多维度报表', '智能推荐'
])

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6-20 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  // 验证表单
  const valid = await loginFormRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    const result = await userStore.doLogin({
      username: loginForm.username,
      password: loginForm.password
    })

    if (result.success) {
      ElMessage.success({
        message: `欢迎回来，${userStore.user?.real_name || userStore.user?.username}！`,
        type: 'success',
        duration: 2000
      })

      // 根据角色跳转
      setTimeout(() => {
        if (userStore.isAdmin) {
          router.push('/admin/dashboard')
        } else {
          router.push('/')
        }
      }, 500)
    } else {
      ElMessage.error(result.message || '登录失败，请检查用户名和密码')
    }
  } catch (error) {
    console.error('登录错误:', error)
    ElMessage.error('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 登录页面加载时，清除可能存在的旧登录状态（但不调用 API）
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  // 清除 store 状态
  userStore.token = ''
  userStore.user = null
})
</script>

<style scoped>
/* 自定义输入框样式 */
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

:deep(.el-input__prefix .el-icon) {
  font-size: 18px;
}

/* 表单验证错误样式 */
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

/* 动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float linear infinite;
}

/* 移动端适配 */
@media (max-width: 1024px) {
  .hidden\:lg\:flex {
    display: none !important;
  }
}

/* 响应式调整 */
@media (max-width: 640px) {
  .min-h-screen {
    padding: 1rem;
  }

  .text-3xl {
    font-size: 1.75rem;
  }
}
</style>
