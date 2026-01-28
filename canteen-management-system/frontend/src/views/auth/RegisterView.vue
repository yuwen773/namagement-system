<template>
  <div class="register-container">
    <div class="register-card">
      <h1>注册页面（待开发）</h1>
      <p>这是阶段三第2步的内容</p>
      <router-link to="/login">返回登录</router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FF6B35, #F7C52D);
}

.register-card {
  background: white;
  padding: 40px;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.register-card h1 {
  color: #FF6B35;
  margin-bottom: 16px;
}

.register-card p {
  color: #666;
  margin-bottom: 24px;
}

.register-card a {
  color: #FF6B35;
  text-decoration: none;
  font-weight: 600;
}
</style>
