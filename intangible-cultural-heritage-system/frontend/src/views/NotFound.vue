<template>
  <div class="not-found-page">
    <!-- 背景装饰 -->
    <div class="ink-background">
      <div class="ink-spot s1"></div>
      <div class="ink-spot s2"></div>
      <div class="ink-spot s3"></div>
    </div>

    <!-- 云纹装饰 -->
    <div class="cloud-decoration">
      <svg class="cloud-svg" viewBox="0 0 200 100">
        <path d="M20,60 Q40,30 70,50 T130,50 T180,60" stroke="rgba(212,175,55,0.2)" fill="none" stroke-width="2"/>
      </svg>
    </div>

    <!-- 主内容 -->
    <div class="not-found-content">
      <!-- 404 印章 -->
      <div class="error-seal">
        <div class="seal-frame">
          <div class="seal-inner">
            <span class="error-number">404</span>
          </div>
        </div>
      </div>

      <!-- 文字说明 -->
      <div class="error-texts">
        <h1 class="error-title">页面未找到</h1>
        <p class="error-subtitle">
          <span class="vertical-char" v-for="(char, i) in subtitleChars" :key="i" :style="{ '--delay': `${i * 100}ms` }">
            {{ char }}
          </span>
        </p>
        <p class="error-description">您访问的页面似乎已消失在历史长河中</p>
      </div>

      <!-- 返回按钮 -->
      <div class="action-section">
        <button class="return-btn" @click="goHome">
          <span class="btn-seal">返</span>
          <span class="btn-text">返回首页</span>
          <span class="btn-decoration"></span>
        </button>
      </div>

      <!-- 底部装饰 -->
      <div class="bottom-decoration">
        <div class="decoration-line"></div>
        <div class="decoration-text">非遗数据平台 · 传承文化</div>
        <div class="decoration-line"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const subtitleChars = ref('迷途知返，回归正途'.split(''))

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
/* ========== 全局样式 ========== */
.not-found-page {
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

.ink-spot {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.06;
  animation: inkFloat 30s ease-in-out infinite;
}

.ink-spot.s1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #2F3640 0%, transparent 70%);
  top: -150px;
  right: -100px;
}

.ink-spot.s2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #C23531 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation-delay: -10s;
}

.ink-spot.s3 {
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
  top: 15%;
  left: 8%;
  width: 200px;
  opacity: 0.6;
  animation: cloudDrift 40s linear infinite;
}

@keyframes cloudDrift {
  0% { transform: translateX(0); }
  50% { transform: translateX(30px); }
  100% { transform: translateX(0); }
}

/* ========== 主内容 ========== */
.not-found-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 600px;
}

/* ========== 404 印章 ========== */
.error-seal {
  margin-bottom: 48px;
}

.seal-frame {
  width: 180px;
  height: 180px;
  margin: 0 auto;
  background: #C23531;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 12px 32px rgba(194, 35, 49, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: rotate(-5deg);
  animation: sealFloat 6s ease-in-out infinite;
}

@keyframes sealFloat {
  0%, 100% { transform: rotate(-5deg) translateY(0); }
  50% { transform: rotate(-5deg) translateY(-10px); }
}

.seal-frame::before {
  content: '';
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  bottom: 8px;
  border: 3px solid rgba(212, 175, 55, 0.4);
  border-radius: 6px;
}

.seal-inner {
  width: 156px;
  height: 156px;
  background: rgba(194, 35, 49, 0.9);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.error-number {
  font-size: 72px;
  font-weight: 700;
  color: #F7F4ED;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 8px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* ========== 错误文字 ========== */
.error-texts {
  margin-bottom: 48px;
}

.error-title {
  font-size: 36px;
  font-weight: 700;
  color: #2F3640;
  margin: 0 0 24px 0;
  letter-spacing: 8px;
  font-family: "STSong", "SimSun", serif;
}

.error-subtitle {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 0 0 16px 0;
}

.vertical-char {
  font-size: 20px;
  color: #C23531;
  font-family: "STSong", "SimSun", serif;
  font-weight: 600;
  opacity: 0;
  animation: charFadeIn 0.6s ease-out forwards;
  animation-delay: var(--delay);
}

@keyframes charFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-description {
  font-size: 16px;
  color: #909399;
  margin: 0;
  letter-spacing: 2px;
}

/* ========== 操作按钮 ========== */
.action-section {
  margin-bottom: 48px;
}

.return-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 16px;
  padding: 16px 48px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.4s;
  box-shadow: 0 4px 16px rgba(194, 35, 49, 0.3);
}

.return-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(194, 35, 49, 0.4);
}

.return-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.return-btn:hover::before {
  left: 100%;
}

.btn-seal {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #D4AF37;
  color: #2F3640;
  font-size: 16px;
  font-weight: 600;
  border-radius: 4px;
  font-family: "STSong", "SimSun", serif;
  flex-shrink: 0;
}

.btn-text {
  font-size: 16px;
  font-weight: 600;
  color: white;
  letter-spacing: 4px;
}

.btn-decoration {
  position: absolute;
  right: 16px;
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
}

/* ========== 底部装饰 ========== */
.bottom-decoration {
  display: flex;
  align-items: center;
  gap: 16px;
}

.decoration-line {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #D4AF37, transparent);
}

.decoration-text {
  font-size: 12px;
  color: #C0C4CC;
  letter-spacing: 4px;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .seal-frame {
    width: 140px;
    height: 140px;
  }

  .seal-inner {
    width: 120px;
    height: 120px;
  }

  .error-number {
    font-size: 56px;
  }

  .error-title {
    font-size: 28px;
    letter-spacing: 4px;
  }

  .error-subtitle {
    flex-wrap: wrap;
  }

  .error-description {
    font-size: 14px;
  }

  .return-btn {
    padding: 14px 32px;
  }

  .btn-text {
    font-size: 14px;
  }

  .bottom-decoration {
    flex-direction: column;
    gap: 8px;
  }

  .decoration-line {
    width: 60px;
  }
}
</style>
