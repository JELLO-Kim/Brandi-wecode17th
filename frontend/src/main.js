import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Utils from '@/admin/utils/utils.js'

Vue.config.productionTip = false
Vue.config.silent = true
Vue.filter('makeComma', val => {
  return Utils.makeComma(val)
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
