import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Import Bootstrap 5 CSS
import 'bootstrap/dist/css/bootstrap.min.css'
// Import Custom Glassmorphism styles
import './assets/styles/custom.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')
