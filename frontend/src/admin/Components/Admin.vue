<template>
  <a-config-provider :locale="locale">
    <div>
      <Header />
      <div class="container">
        <Aside />
        <main>
          <router-view :key="$route.fullPath" />
        </main>
      </div>
    </div>
  </a-config-provider>
</template>

<script>
// 한국어 대응
import koKr from 'ant-design-vue/lib/locale-provider/ko_KR'
import Vue from 'vue'
import Header from '@/admin/Components/Common/header'
import Aside from '@/admin/Components/Common/aside'
import 'ant-design-vue/dist/antd.css'
import 'antd-button-color/dist/css/style.css' // or 'antd-button-color/dist/css/style.less'
import VueCurrencyInput from 'vue-currency-input'
import Antd from 'ant-design-vue'
import VueTheMask from 'vue-the-mask'

const pluginOptions = {
  /* see config reference */
  globalOptions: { currency: { distractionFree: { hidecrrencySymbol: true } }, locale: 'en', precision: 0 }
}
// import VueMoney from 'v-money'

// Vue.use(VueMoney, {precision: 0,  thousands: ','})

Vue.use(VueTheMask)
Vue.config.productionTip = false
Vue.use(Antd)
Vue.use(VueCurrencyInput, pluginOptions)
Vue.filter('emptyDash', val => {
  if (val === undefined) return '-'
  if (val === null) return '-'
  if (val === '') return '-'
  return val
})
export default {
  name: 'Home',
  components: {
    Header,
    Aside
  },
  data () {
    return {
      locale: koKr
    }
  },
  created () {
    Vue.filter('typeToName', (val, type) => {
      const statusItem = this.$store.state.const[type].filter((d) => { return d.value === val })
      if (statusItem.length > 0) return statusItem[0].label
      return ''
    })
  }
}
</script>

<style lang="scss">
.container {
  margin-top: 45px;
  color: #222;

  main {
    position: relative;
    height: calc(100% - 45px);
    min-height: 695px;
    margin-left: 215px;
    padding: 25px 20px 20px 20px;
    border-radius: 0 0 0 4px;
    margin-top: 0px;
    background-color: #fafafa;
  }
}
</style>
<style lang="scss" scoped>
/*@import './styles/_reset.scss';*/
</style>
<style>
/*공통 CSS*/
i {
  font-style: normal;
}
span.info {
  color: #298ae6;
}
.required {
  color: red
}
.large-size {
  width: 400px;
}
.normal-size {
  width: 200px;
}
.small-size {
  width: 100px;
}
table.bordered th {
  background: #fafafa;
}
table.bordered th, table.bordered td{
  border: 1px solid #e8e8e8;
  padding: 10px 15px;
  font-size: 13px;
}
h2 > span {
  font-size: 14px;
  font-weight: normal;
  color: #999;
}
</style>
