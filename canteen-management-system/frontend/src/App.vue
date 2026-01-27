<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div>
    <!-- 食堂管理系统 - 测试验证 -->
    <h1>食堂管理系统 - 前端项目初始化成功</h1>
    <p>热更新测试文字 - 如果您能看到这段文字，说明热更新正常工作</p>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
