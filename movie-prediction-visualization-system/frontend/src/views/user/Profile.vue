<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getCurrentUser, changePassword, updateProfile } from '@/api/auth'
import { ElMessage } from 'element-plus'
import {
  User,
  Lock,
  Setting
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('profile')
const loading = ref(false)
const passwordLoading = ref(false)

const form = reactive({
  username: '',
  real_name: '',
  email: '',
  phone: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// Role display
const roleDisplay = computed(() => {
  const role = userStore.user?.role
  if (role === 'ADMIN') return '管理员'
  if (role === 'USER') return '普通用户'
  return '未知'
})

// Avatar color
const avatarGradient = computed(() => {
  const username = userStore.user?.username || ''
  const colors = [
    'from-blue-500 to-cyan-500',
    'from-emerald-500 to-green-500',
    'from-violet-500 to-purple-500',
    'from-amber-500 to-orange-500',
    'from-pink-500 to-rose-500'
  ]
  const index = username.charCodeAt(0) % colors.length
  return colors[index]
})

// Load user profile
const loadProfile = async () => {
  try {
    loading.value = true
    const res = await getCurrentUser()
    const userData = res.data

    form.username = userData.username || ''
    form.real_name = userData.real_name || ''
    form.email = userData.email || ''
    form.phone = userData.phone || ''

    // Update user store
    userStore.setUser(userData)
  } catch (error) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  } finally {
    loading.value = false
  }
}

// Handle save profile
const handleSaveProfile = async () => {
  try {
    loading.value = true
    await updateProfile({
      real_name: form.real_name,
      email: form.email,
      phone: form.phone
    })
    ElMessage.success('个人信息更新成功')

    // Refresh user data
    await loadProfile()
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.message || '更新失败')
  } finally {
    loading.value = false
  }
}

// Handle change password
const handleChangePassword = async () => {
  // Validation
  if (!passwordForm.old_password) {
    ElMessage.warning('请输入当前密码')
    return
  }
  if (!passwordForm.new_password) {
    ElMessage.warning('请输入新密码')
    return
  }
  if (passwordForm.new_password.length < 6) {
    ElMessage.warning('新密码长度不能少于6位')
    return
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  if (passwordForm.old_password === passwordForm.new_password) {
    ElMessage.warning('新密码不能与当前密码相同')
    return
  }

  try {
    passwordLoading.value = true
    await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    ElMessage.success('密码修改成功，请重新登录')

    // Clear password form
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''

    // Logout after password change (optional, for security)
    setTimeout(() => {
      userStore.logout()
      router.push('/login')
    }, 1500)
  } catch (error) {
    console.error('密码修改失败:', error)
    ElMessage.error(error.response?.data?.message || '密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}

// Format account creation date
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  if (userStore.user) {
    form.username = userStore.user.username || ''
    form.real_name = userStore.user.real_name || ''
    form.email = userStore.user.email || ''
    form.phone = userStore.user.phone || ''
  }
  loadProfile()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6 lg:p-8">
    <!-- Animated background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none -z-10">
      <div class="grid-bg"></div>
      <div class="gradient-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <!-- Header -->
    <div class="mb-8 animate-fade-in">
      <div class="glass-card rounded-2xl p-6 border border-white/10">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
            <Setting class="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">个人中心</h1>
            <p class="text-slate-400 mt-1">管理您的账户信息</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile card -->
      <div class="animate-slide-up">
        <div class="glass-card rounded-2xl border border-white/10 p-6 h-full">
          <div class="text-center">
            <div class="w-28 h-28 rounded-2xl bg-gradient-to-br mx-auto flex items-center justify-center shadow-lg"
                 :class="avatarGradient">
              <span class="text-4xl font-bold text-white">
                {{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
              </span>
            </div>
            <h3 class="text-xl font-bold text-white mt-4">
              {{ userStore.user?.real_name || userStore.user?.username || '用户' }}
            </h3>
            <p class="text-slate-400 mt-1">{{ roleDisplay }}</p>
            <p class="text-slate-500 text-sm mt-1">@{{ userStore.user?.username }}</p>

            <div class="mt-6 pt-6 border-t border-white/10">
              <div class="grid grid-cols-2 gap-4 text-left">
                <div class="p-3 rounded-lg bg-white/5">
                  <p class="text-xs text-slate-500">注册时间</p>
                  <p class="text-sm text-slate-300 mt-1">{{ formatDate(userStore.user?.created_at) }}</p>
                </div>
                <div class="p-3 rounded-lg bg-white/5">
                  <p class="text-xs text-slate-500">账户状态</p>
                  <p class="text-sm text-emerald-400 mt-1">正常</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings card -->
      <div class="lg:col-span-2 animate-slide-up" style="animation-delay: 0.2s">
        <div class="glass-card rounded-2xl border border-white/10">
          <!-- Tabs -->
          <div class="border-b border-white/10">
            <div class="flex">
              <button
                @click="activeTab = 'profile'"
                :class="[
                  'flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2',
                  activeTab === 'profile'
                    ? 'text-blue-400 border-blue-400'
                    : 'text-slate-400 border-transparent hover:text-white'
                ]"
              >
                <User class="w-4 h-4" />
                基本信息
              </button>
              <button
                @click="activeTab = 'security'"
                :class="[
                  'flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2',
                  activeTab === 'security'
                    ? 'text-blue-400 border-blue-400'
                    : 'text-slate-400 border-transparent hover:text-white'
                ]"
              >
                <Lock class="w-4 h-4" />
                安全设置
              </button>
            </div>
          </div>

          <!-- Tab content -->
          <div class="p-6">
            <!-- Profile tab -->
            <div v-show="activeTab === 'profile'">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-slate-400 mb-2">用户名</label>
                  <div class="px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-slate-300">
                    {{ form.username }}
                  </div>
                  <p class="text-xs text-slate-500 mt-1">用户名不可修改</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-400 mb-2">真实姓名</label>
                  <input
                    v-model="form.real_name"
                    type="text"
                    class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="请输入真实姓名"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-400 mb-2">邮箱地址</label>
                  <input
                    v-model="form.email"
                    type="email"
                    class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="请输入邮箱地址"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-400 mb-2">手机号码</label>
                  <input
                    v-model="form.phone"
                    type="tel"
                    class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="请输入手机号码"
                  />
                </div>
              </div>
              <div class="mt-6 flex justify-end">
                <button
                  @click="handleSaveProfile"
                  :disabled="loading"
                  class="px-6 py-2.5 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ loading ? '保存中...' : '保存修改' }}
                </button>
              </div>
            </div>

            <!-- Security tab -->
            <div v-show="activeTab === 'security'">
              <div class="max-w-lg">
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-2">当前密码</label>
                    <input
                      v-model="passwordForm.old_password"
                      type="password"
                      class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 transition-colors"
                      placeholder="请输入当前密码"
                      show-password
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-2">新密码</label>
                    <input
                      v-model="passwordForm.new_password"
                      type="password"
                      class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 transition-colors"
                      placeholder="请输入新密码（至少6位）"
                      show-password
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-400 mb-2">确认新密码</label>
                    <input
                      v-model="passwordForm.confirm_password"
                      type="password"
                      class="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white focus:outline-none focus:border-blue-500 transition-colors"
                      placeholder="请再次输入新密码"
                      show-password
                      @keyup.enter="handleChangePassword"
                    />
                  </div>
                </div>
                <div class="mt-6 flex justify-end">
                  <button
                    @click="handleChangePassword"
                    :disabled="passwordLoading || !passwordForm.old_password || !passwordForm.new_password"
                    class="px-6 py-2.5 rounded-lg bg-gradient-to-r from-violet-500 to-purple-500 text-white font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ passwordLoading ? '修改中...' : '修改密码' }}
                  </button>
                </div>
                <div class="mt-6 p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                  <p class="text-sm text-amber-400">
                    <span class="font-semibold">提示：</span>修改密码后，您将需要重新登录系统。
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Grid background */
.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* Gradient orbs */
.gradient-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #10b981, #3b82f6);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -20px) scale(1.05); }
  50% { transform: translate(-10px, 20px) scale(0.95); }
  75% { transform: translate(-20px, -10px) scale(1.02); }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-slide-up {
  opacity: 0;
  animation: slide-up 0.6s ease-out forwards;
}

/* Input styling */
input:focus {
  outline: none;
}
</style>
