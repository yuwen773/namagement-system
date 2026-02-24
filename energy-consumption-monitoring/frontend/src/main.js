import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router, { setupRouterGuards } from './router'
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

// Register all Element Plus icons with both original name and icon-ep- prefix
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  // Register with original name (e.g., User, Lock)
  app.component(key, component)
  // Register with icon-ep- prefix (e.g., icon-ep-user, icon-ep-lock)
  app.component(`icon-ep-${kebabCase(key)}`, component)
}

// Helper function to convert PascalCase to kebab-case
function kebabCase(str) {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase()
}

app.use(pinia)
// Setup router guards after Pinia is installed
setupRouterGuards(pinia)
app.use(router)
app.use(ElementPlus, {
  // Element Plus global configuration
  size: 'default',
  zIndex: 3000,
})

app.mount('#app')
