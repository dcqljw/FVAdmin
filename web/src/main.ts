import './assets/main.css'
import 'virtual:uno.css'
import {createApp} from 'vue'
import {createPinia} from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'


import App from './App.vue'
import {initStore} from "./stores";
import {initRouter} from './router'

const app = createApp(App)
initStore(app)
initRouter(app)
app.use(ElementPlus, {
    locale: zhCn
})
app.mount('#app')
