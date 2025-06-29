import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css'

window.addEventListener('pywebviewready', async function () {
    const app = createApp(App)
    app.mount('#app')
})