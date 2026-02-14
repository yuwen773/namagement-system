import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

import './style.css'
import 'element-plus/dist/index.css'

const app = createApp(App)

// 注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用 Pinia
const pinia = createPinia()
app.use(pinia)

// 使用 Element Plus
app.use(ElementPlus)

// 使用路由
app.use(router)

app.mount('#app')
