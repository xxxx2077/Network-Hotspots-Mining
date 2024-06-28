import Vue from 'vue'
import App from './App.vue'
import router from './router'
import dataV from '@jiaminghi/data-view'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false

Vue.use(dataV)
Vue.use(ElementUI)

new Vue({
  router,
  render: h => h(App),
  data() {
    return {
      topic: '',
    }
  }
}).$mount('#app')
