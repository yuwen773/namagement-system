<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="ink-background">
      <div class="ink-splash s1"></div>
      <div class="ink-splash s2"></div>
      <div class="ink-splash s3"></div>
    </div>

    <!-- 云纹装饰 -->
    <div class="cloud-decoration">
      <svg class="cloud-svg c1" viewBox="0 0 200 100">
        <path d="M20,60 Q40,30 70,50 T130,50 T180,60" stroke="rgba(212,175,55,0.15)" fill="none" stroke-width="2"/>
      </svg>
      <svg class="cloud-svg c2" viewBox="0 0 200 100">
        <path d="M20,50 Q50,20 90,40 T160,40" stroke="rgba(194,35,49,0.1)" fill="none" stroke-width="2"/>
      </svg>
    </div>

    <div class="login-container">
      <!-- 左侧装饰区 -->
      <div class="decoration-side">
        <div class="vertical-text">
          <span class="text-char" v-for="(char, i) in welcomeText" :key="i" :style="{ '--delay': `${i * 100}ms` }">
            {{ char }}
          </span>
        </div>
        <div class="seal-stamp">
          <div class="seal-outer">
            <div class="seal-inner">
              <span class="seal-char">非遗</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 登录表单区 -->
      <div class="form-side">
        <div class="login-scroll">
          <div class="scroll-top"></div>
          <div class="scroll-content">
            <!-- 顶部印章 Logo -->
            <div class="form-logo">
              <div class="logo-seal">
                <div class="seal-frame">
                  <el-icon :size="36" class="seal-icon">
                    <Collection />
                  </el-icon>
                </div>
              </div>
              <div class="logo-texts">
                <h1 class="logo-title">非遗数据平台</h1>
                <p class="logo-subtitle">Intangible Cultural Heritage System</p>
              </div>
            </div>

            <!-- 登录表单 -->
            <el-form
              ref="loginFormRef"
              :model="loginForm"
              :rules="loginRules"
              class="login-form"
              @submit.prevent="handleLogin"
            >
              <el-form-item prop="username">
                <div class="input-group">
                  <span class="input-label">用户名</span>
                  <el-input
                    v-model="loginForm.username"
                    placeholder="请输入用户名"
                    size="large"
                    class="heritage-input"
                  >
                    <template #prefix>
                      <el-icon><User /></el-icon>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item prop="password">
                <div class="input-group">
                  <span class="input-label">密码</span>
                  <el-input
                    v-model="loginForm.password"
                    type="password"
                    placeholder="请输入密码"
                    size="large"
                    class="heritage-input"
                    show-password
                    @keyup.enter="handleLogin"
                  >
                    <template #prefix>
                      <el-icon><Lock /></el-icon>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item>
                <button
                  type="submit"
                  class="login-btn"
                  :class="{ loading: loading }"
                  :disabled="loading"
                >
                  <span v-if="!loading">登录</span>
                  <span v-else class="loading-text">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                  </span>
                </button>
              </el-form-item>
            </el-form>

            <!-- 提示信息 -->
            <div class="login-hint">
              <div class="hint-seal">试</div>
              <p>测试账号：admin / password123</p>
            </div>
          </div>
          <div class="scroll-bottom"></div>
        </div>

        <!-- 底部装饰 -->
        <div class="footer-decoration">
          <div class="decoration-line"></div>
          <p>© 2026 非遗数据平台 · 传承文化 记录历史</p>
        </div>
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

const welcomeText = '欢迎登录非遗数据平台'

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
/* ========== 全局样式 ========== */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: #F7F4ED;
  position: relative;
  overflow: hidden;
}

/* ========== 水墨背景 ========== */
.ink-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.ink-splash {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.08;
  animation: inkFloat 30s ease-in-out infinite;
}

.ink-splash.s1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #2F3640 0%, transparent 70%);
  top: -150px;
  right: -100px;
}

.ink-splash.s2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #C23531 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation-delay: -10s;
}

.ink-splash.s3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #D4AF37 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -20s;
}

@keyframes inkFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(-30px, -30px) scale(1.02); }
}

/* ========== 云纹装饰 ========== */
.cloud-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.cloud-svg {
  position: absolute;
  opacity: 0.6;
}

.cloud-svg.c1 {
  top: 10%;
  left: 5%;
  width: 200px;
  animation: cloudDrift 40s linear infinite;
}

.cloud-svg.c2 {
  bottom: 15%;
  right: 8%;
  width: 180px;
  animation: cloudDrift 50s linear infinite reverse;
}

@keyframes cloudDrift {
  0% { transform: translateX(0); }
  50% { transform: translateX(30px); }
  100% { transform: translateX(0); }
}

/* ========== 登录容器 ========== */
.login-container {
  position: relative;
  z-index: 1;
  display: flex;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: 16px;
  box-shadow:
    0 1px 0 0 rgba(212, 175, 55, 0.3) inset,
    0 -1px 0 0 rgba(212, 175, 55, 0.3) inset,
    0 20px 60px rgba(47, 54, 64, 0.15);
  overflow: hidden;
}

/* ========== 左侧装饰区 ========== */
.decoration-side {
  width: 200px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
}

.decoration-side::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  bottom: 20px;
  border: 2px solid rgba(212, 175, 55, 0.3);
  border-radius: 8px;
}

.vertical-text {
  writing-mode: vertical-rl;
  display: flex;
  gap: 8px;
  margin-bottom: 60px;
}

.text-char {
  font-size: 20px;
  color: rgba(247, 244, 237, 0.9);
  font-family: "STSong", "SimSun", serif;
  font-weight: 500;
  letter-spacing: 8px;
  opacity: 0;
  animation: charFadeIn 0.8s ease-out forwards;
  animation-delay: var(--delay);
}

@keyframes charFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.seal-stamp {
  position: relative;
}

.seal-outer {
  width: 80px;
  height: 80px;
  background: #D4AF37;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 8px 24px rgba(212, 175, 55, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transform: rotate(-5deg);
}

.seal-inner {
  width: 68px;
  height: 68px;
  background: rgba(212, 175, 55, 0.9);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.seal-char {
  writing-mode: horizontal-tb;
  font-size: 24px;
  color: #2F3640;
  font-family: "STSong", "SimSun", serif;
  font-weight: 700;
  letter-spacing: 4px;
}

/* ========== 右侧表单区 ========== */
.form-side {
  flex: 1;
  padding: 48px 56px;
  display: flex;
  flex-direction: column;
}

.login-scroll {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.scroll-top,
.scroll-bottom {
  height: 16px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(212, 175, 55, 0.3) 20%,
    rgba(212, 175, 55, 0.5) 50%,
    rgba(212, 175, 55, 0.3) 80%,
    transparent 100%
  );
}

.scroll-bottom {
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(212, 175, 55, 0.3) 20%,
    rgba(212, 175, 55, 0.5) 50%,
    rgba(212, 175, 55, 0.3) 80%,
    transparent 100%
  );
}

.scroll-content {
  flex: 1;
  padding: 32px 0;
}

/* ========== Logo ========== */
.form-logo {
  text-align: center;
  margin-bottom: 40px;
}

.logo-seal {
  display: inline-flex;
  justify-content: center;
  margin-bottom: 20px;
}

.seal-frame {
  width: 72px;
  height: 72px;
  background: #C23531;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 6px 20px rgba(194, 35, 49, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
}

.seal-frame::before {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  right: 4px;
  bottom: 4px;
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-radius: 2px;
}

.seal-icon {
  color: #F7F4ED;
}

.logo-texts {
  text-align: center;
}

.logo-title {
  font-size: 28px;
  font-weight: 700;
  color: #2F3640;
  margin: 0 0 8px 0;
  letter-spacing: 4px;
  font-family: "STSong", "SimSun", serif;
  background: linear-gradient(135deg, #C23531 0%, #2F3640 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-subtitle {
  font-size: 12px;
  color: #909399;
  margin: 0;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* ========== 表单 ========== */
.login-form {
  margin-bottom: 24px;
}

.input-group {
  width: 100%;
}

.input-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

:deep(.heritage-input) {
  --el-input-border-color: rgba(212, 175, 55, 0.3);
  --el-input-hover-border-color: #D4AF37;
  --el-input-focus-border-color: #C23531;
  --el-input-bg-color: #F7F4ED;
}

:deep(.heritage-input .el-input__wrapper) {
  padding: 14px 16px;
  border-radius: 8px;
  box-shadow: none;
  background: #F7F4ED;
  transition: all 0.3s;
}

:deep(.heritage-input .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #D4AF37 inset;
}

:deep(.heritage-input .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #C23531 inset;
}

:deep(.heritage-input .el-input__inner) {
  color: #2F3640;
  font-weight: 500;
}

:deep(.heritage-input .el-input__prefix) {
  color: #909399;
}

/* ========== 登录按钮 ========== */
.login-btn {
  width: 100%;
  padding: 16px 32px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(194, 35, 49, 0.3);
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 35, 49, 0.4);
}

.login-btn:hover::before {
  left: 100%;
}

.login-btn:active {
  transform: translateY(0);
}

.login-btn.loading {
  background: linear-gradient(135deg, #909399 0%, #606266 100%);
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: dotBounce 1.4s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBounce {
  0%, 80%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  40% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* ========== 提示信息 ========== */
.login-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  background: rgba(212, 175, 55, 0.1);
  border-radius: 8px;
  border: 1px dashed rgba(212, 175, 55, 0.3);
}

.hint-seal {
  width: 32px;
  height: 32px;
  background: #D4AF37;
  color: #2F3640;
  font-size: 14px;
  font-weight: 600;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "STSong", "SimSun", serif;
  flex-shrink: 0;
}

.login-hint p {
  margin: 0;
  font-size: 13px;
  color: #606266;
}

/* ========== 底部装饰 ========== */
.footer-decoration {
  text-align: center;
  padding-top: 24px;
}

.decoration-line {
  width: 100px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #D4AF37, transparent);
  margin: 0 auto 16px;
}

.footer-decoration p {
  margin: 0;
  font-size: 12px;
  color: #909399;
  letter-spacing: 1px;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .decoration-side {
    display: none;
  }

  .form-side {
    padding: 32px 24px;
  }

  .logo-title {
    font-size: 24px;
  }
}
</style>
