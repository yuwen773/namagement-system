<template>
  <footer class="app-footer">
    <!-- 主要内容区 -->
    <div class="footer-main">
      <div class="footer-container">
        <!-- 关于我们 -->
        <div class="footer-section about-section">
          <div class="footer-logo">
            <div class="logo-icon">
              <svg viewBox="0 0 24 24" fill="none" width="28" height="28">
                <path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z" fill="currentColor"/>
              </svg>
            </div>
            <div class="logo-text">
              <span class="logo-name">CAR PARTS</span>
              <span class="logo-tag">PRO</span>
            </div>
          </div>
          <p class="footer-desc">
            专业的汽车改装件销售与推荐平台，为爱车人士提供优质的改装配件和专业的技术建议。
          </p>
          <!-- 社交媒体 -->
          <div class="social-links">
            <a href="#" class="social-link" aria-label="微信">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path d="M8 12c-2.21 0-4-1.61-4-3.6S5.79 4.8 8 4.8s4 1.61 4 3.6-1.79 3.6-4 3.6z" stroke="currentColor" stroke-width="2"/>
                <path d="M8 16c-3.31 0-6-2.24-6-5 0-2.76 2.69-5 6-5s6 2.24 6 5c0 2.76-2.69 5-6 5z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </a>
            <a href="#" class="social-link" aria-label="微博">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M16 8l-4 4 4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </a>
            <a href="#" class="social-link" aria-label="抖音">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <rect x="6" y="2" width="12" height="20" rx="2" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="16" r="2" fill="currentColor"/>
              </svg>
            </a>
            <a href="#" class="social-link" aria-label="B站">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <rect x="2" y="4" width="20" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
                <polygon points="10 9 14 9 13 15 11 15" fill="currentColor"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- 新手指南 -->
        <div class="footer-section">
          <h3 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="9" y="3" width="6" height="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            新手指南
          </h3>
          <ul class="section-links">
            <li><router-link to="/help/register">注册新用户</router-link></li>
            <li><router-link to="/help/login">登录/密码找回</router-link></li>
            <li><router-link to="/help/shopping">购物流程</router-link></li>
            <li><router-link to="/help/payment">支付方式</router-link></li>
          </ul>
        </div>

        <!-- 配送方式 -->
        <div class="footer-section">
          <h3 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <rect x="1" y="3" width="15" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
              <path d="M16 8h4a2 2 0 012 2v8a2 2 0 01-2 2H6a2 2 0 01-2-2v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            配送方式
          </h3>
          <ul class="section-links">
            <li><router-link to="/help/shipping">配送范围</router-link></li>
            <li><router-link to="/help/fee">运费标准</router-link></li>
            <li><router-link to="/help/time">配送时间</router-link></li>
            <li><router-link to="/help/track">物流查询</router-link></li>
          </ul>
        </div>

        <!-- 售后服务 -->
        <div class="footer-section">
          <h3 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            售后服务
          </h3>
          <ul class="section-links">
            <li><router-link to="/help/return">退换货政策</router-link></li>
            <li><router-link to="/help/refund">退款说明</router-link></li>
            <li><router-link to="/help/warranty">质保服务</router-link></li>
            <li><router-link to="/help/complaint">投诉建议</router-link></li>
          </ul>
        </div>

        <!-- 客户服务 -->
        <div class="footer-section contact-section">
          <h3 class="section-title">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            客户服务
          </h3>
          <div class="contact-box">
            <div class="contact-item">
              <svg class="contact-icon" viewBox="0 0 24 24" fill="none" width="24" height="24">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <div class="contact-info">
                <span class="contact-label">客服热线</span>
                <span class="contact-value">400-888-8888</span>
              </div>
            </div>
            <div class="contact-time">服务时间：9:00 - 21:00</div>
            <div class="contact-qr">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 14h2v2h-2zM14 18h2v2h-2zM18 18h2v2h-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>扫码关注公众号</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 友情链接 -->
    <div class="footer-links">
      <div class="links-container">
        <span class="links-label">友情链接:</span>
        <div class="links-list">
          <a v-for="link in friendLinks" :key="link.url" :href="link.url" target="_blank" rel="noopener" class="link-item">
            {{ link.name }}
          </a>
        </div>
      </div>
    </div>

    <!-- 底部版权 -->
    <div class="footer-bottom">
      <div class="bottom-container">
        <div class="copyright">
          <p>&copy; {{ currentYear }} CAR PARTS PRO. All rights reserved.</p>
          <p class="icp-links">
            <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener">京ICP备12345678号</a>
            <span class="separator">|</span>
            <a href="#" target="_blank" rel="noopener">京公网安备 11010802012345号</a>
          </p>
        </div>
        <div class="trust-badges">
          <div class="trust-badge" title="可信网站">
            <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
              <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="trust-badge" title="安全联盟">
            <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
              <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
              <path d="M7 11V7c0-2.76 2.24-5 5-5s5 2.24 5 5v4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="trust-badge" title="诚信网站">
            <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l8.91-1.01L12 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

// 当前年份
const currentYear = computed(() => new Date().getFullYear())

// 友情链接
const friendLinks = [
  { name: '汽车之家', url: 'https://www.autohome.com.cn' },
  { name: '懂车帝', url: 'https://www.dcdapp.com' },
  { name: '易车网', url: 'https://www.yiche.com' },
  { name: '太平洋汽车', url: 'https://www.pcauto.com.cn' },
  { name: '搜狐汽车', url: 'https://auto.sohu.com' }
]
</script>

<style scoped>
.app-footer {
  background: rgba(15, 23, 42, 0.95);
  border-top: 1px solid rgba(71, 85, 105, 0.5);
  margin-top: auto;
}

/* 主要内容区 */
.footer-main {
  padding: 60px 0 40px;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1.5fr repeat(4, 1fr);
  gap: 40px;
}

/* 底部区块 */
.footer-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-title svg {
  color: #f97316;
}

.section-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-links a {
  color: #94a3b8;
  text-decoration: none;
  font-size: 13px;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
}

.section-links a::before {
  content: '';
  width: 4px;
  height: 4px;
  background: #475569;
  border-radius: 50%;
  margin-right: 8px;
  transition: all 0.2s ease;
}

.section-links a:hover {
  color: #f97316;
}

.section-links a:hover::before {
  background: #f97316;
}

/* 关于我们 */
.about-section {
  grid-column: span 1;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.footer-logo .logo-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 10px;
  color: #ffffff;
}

.footer-logo .logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.footer-logo .logo-name {
  font-size: 16px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.footer-logo .logo-tag {
  font-size: 10px;
  font-weight: 700;
  color: #f97316;
  letter-spacing: 0.1em;
}

.footer-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 20px;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-link {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
  transform: translateY(-2px);
}

/* 客户服务 */
.contact-section {
  grid-column: span 1;
}

.contact-box {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  padding: 20px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.contact-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(249, 115, 22, 0.15);
  border-radius: 8px;
  color: #f97316;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.contact-label {
  font-size: 11px;
  color: #94a3b8;
}

.contact-value {
  font-size: 16px;
  font-weight: 700;
  color: #f97316;
}

.contact-time {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 16px;
}

.contact-qr {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #94a3b8;
  padding-top: 16px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.contact-qr svg {
  color: #64748b;
}

/* 友情链接 */
.footer-links {
  border-top: 1px solid rgba(71, 85, 105, 0.3);
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
}

.links-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.links-label {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
}

.links-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.link-item {
  color: #94a3b8;
  text-decoration: none;
  font-size: 13px;
  transition: color 0.2s ease;
  padding: 4px 0;
}

.link-item:hover {
  color: #f97316;
}

.link-item:not(:last-child)::after {
  content: '|';
  margin-left: 8px;
  color: rgba(71, 85, 105, 0.5);
}

/* 底部版权 */
.footer-bottom {
  background: rgba(30, 41, 59, 0.5);
}

.bottom-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.copyright p {
  margin: 0;
  font-size: 12px;
  color: #64748b;
}

.icp-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icp-links a {
  color: #64748b;
  text-decoration: none;
  font-size: 12px;
  transition: color 0.2s ease;
}

.icp-links a:hover {
  color: #f97316;
}

.separator {
  color: rgba(71, 85, 105, 0.5);
}

.trust-badges {
  display: flex;
  gap: 16px;
}

.trust-badge {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.trust-badge:hover {
  border-color: #f97316;
  color: #f97316;
}

/* 响应式 */
@media (max-width: 1200px) {
  .footer-container {
    grid-template-columns: repeat(3, 1fr);
  }

  .about-section {
    grid-column: span 3;
    grid-row: 1;
  }

  .contact-section {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .footer-main {
    padding: 40px 0 24px;
  }

  .footer-container {
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }

  .about-section {
    grid-column: span 2;
  }

  .contact-section {
    grid-column: span 2;
  }

  .bottom-container {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .links-container {
    justify-content: center;
  }

  .footer-links {
    display: none;
  }
}

@media (max-width: 480px) {
  .footer-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .about-section,
  .contact-section {
    grid-column: span 1;
  }

  .social-links {
    justify-content: flex-start;
  }
}
</style>
