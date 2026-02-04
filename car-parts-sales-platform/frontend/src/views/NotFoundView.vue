<script setup>
import { useRouter } from 'vue-router'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()

function goHome() {
  router.push({ name: 'home' })
}

function goBack() {
  router.back()
}
</script>

<template>
  <div class="not-found-view">
    <div class="not-found-bg"></div>
    <div class="not-found-grid"></div>
    <div class="not-found-content">
      <div class="error-code">404</div>
      <div class="error-divider"></div>
      <h1 class="error-title">Page Not Found</h1>
      <p class="error-subtitle">
        The part you're looking for doesn't exist or has been moved to a different location.
      </p>
      <div class="error-actions">
        <button class="btn btn-primary" @click="goHome">
          <span>Go Home</span>
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
            <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <button class="btn btn-secondary" @click="goBack">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M12 19L5 12M12 19L19 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Go Back</span>
        </button>
      </div>
      <div class="error-hints">
        <div class="hint-item">
          <svg class="hint-icon" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 16V12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <div class="hint-content">
            <span class="hint-title">Check the URL</span>
            <span class="hint-text">Make sure you entered the correct address</span>
          </div>
        </div>
        <div class="hint-item">
          <svg class="hint-icon" viewBox="0 0 24 24" fill="none">
            <path d="M15 15L10 10M15 10L10 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
          </svg>
          <div class="hint-content">
            <span class="hint-title">Broken Link</span>
            <span class="hint-text">The link may be outdated or incorrect</span>
          </div>
        </div>
        <div class="hint-item">
          <svg class="hint-icon" viewBox="0 0 24 24" fill="none">
            <path d="M21 21L9 9M9 9H3M9 9V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="hint-content">
            <span class="hint-title">Content Moved</span>
            <span class="hint-text">Try using the search or navigation menu</span>
          </div>
        </div>
      </div>
    </div>
    <div class="not-found-accent"></div>
  </div>
</template>

<style scoped>
.not-found-view {
  --font-display: 'Oswald', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0a0a0a;
  overflow: hidden;
}

.not-found-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(255, 77, 0, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 100% 50%, rgba(255, 77, 0, 0.1), transparent);
}

.not-found-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
}

.not-found-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 60px 40px;
  max-width: 700px;
}

.error-code {
  font-family: var(--font-display);
  font-size: clamp(120px, 20vw, 200px);
  font-weight: 700;
  color: #ff4d00;
  line-height: 0.8;
  letter-spacing: -10px;
  text-shadow: 0 0 60px rgba(255, 77, 0, 0.3);
}

.error-divider {
  width: 200px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #ff4d00, transparent);
  margin: 32px auto;
}

.error-title {
  font-family: var(--font-display);
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 700;
  text-transform: uppercase;
  color: white;
  margin-bottom: 16px;
}

.error-subtitle {
  font-family: var(--font-body);
  font-size: 16px;
  color: #9ca3af;
  line-height: 1.6;
  max-width: 500px;
  margin: 0 auto 48px;
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 64px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 14px 28px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.btn:hover .btn-icon {
  transform: translateX(4px);
}

.btn-primary {
  background: #ff4d00;
  color: white;
}

.btn-primary:hover {
  background: #e64600;
  transform: translateY(-2px);
  box-shadow: 0 15px 35px -10px rgba(255, 77, 0, 0.6);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.4);
}

.btn-secondary .btn-icon {
  transform: translateX(-4px);
}

.btn-secondary:hover .btn-icon {
  transform: translateX(-8px);
}

.error-hints {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
}

.hint-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
  transition: all 0.3s ease;
}

.hint-item:hover {
  background: rgba(255, 77, 0, 0.05);
  border-color: rgba(255, 77, 0, 0.2);
  transform: translateX(8px);
}

.hint-icon {
  width: 24px;
  height: 24px;
  color: #ff4d00;
  flex-shrink: 0;
}

.hint-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.hint-title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  color: white;
}

.hint-text {
  font-family: var(--font-body);
  font-size: 13px;
  color: #9ca3af;
}

.not-found-accent {
  position: absolute;
  bottom: -150px;
  right: -150px;
  width: 400px;
  height: 400px;
  background: radial-gradient(ellipse, rgba(255, 77, 0, 0.2) 0%, transparent 70%);
  filter: blur(100px);
}

/* Responsive */
@media (max-width: 768px) {
  .error-actions {
    flex-direction: column;
  }

  .error-hints {
    align-items: stretch;
  }

  .hint-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>
