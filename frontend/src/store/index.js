// import Vue from 'vue' //header.php의 vue사용
import Vuex from 'vuex'
import Vue from 'vue'

// modules
import * as modules from './modules/index'

Vue.use(Vuex)

// 공통 스토어
export default new Vuex.Store({
  state: {
  },
  getter: {
  },
  mutations: {
  },
  modules: modules.default
})
