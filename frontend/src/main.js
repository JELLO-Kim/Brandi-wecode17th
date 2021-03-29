import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Utils from '@/admin/utils/utils.js'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.use(VueToast)
Vue.filter('makeComma', val => {
  return Utils.makeComma(val)
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
