<template>
  <div>
    <Header class="header"></Header>
    <router-view class="layout"></router-view>
    <Footer class="footer"></Footer>
  </div>
</template>
<script>
import Header from '@/service/Components/Header'
import Footer from '@/service/Components/Footer'

export default {
  components: {
    Header,
    Footer
  },
  created () {
  },
  updated () {
    window.scrollTo(0, 0)
  },
  data () {
    return {
    }
  }
}
</script>
<style lang="scss" scoped>
.header {
  min-width: 900px;
}
.layout {
  max-width: 1300px;
  min-width: 900px;
  margin: 0 auto;
}
.footer {
  min-width: 900px;
  width: 100%;
  overflow: hidden;
}
</style>
