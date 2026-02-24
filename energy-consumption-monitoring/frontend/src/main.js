import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import './style.css'

// Import Element Plus theme customization
import './styles/element-plus.scss'

// Import Element Plus default styles
import 'element-plus/dist/index.css'

const app = createApp(App)

// Create pinia instance with persistence
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus, {
  // Element Plus global configuration
  size: 'default',
  zIndex: 3000,
})

app.mount('#app')
