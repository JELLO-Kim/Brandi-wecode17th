<template>
  <div id="app">
    <!-- <Header v-if="$route.path.indexOf('admin') == -1" /> -->
    <router-view/>
    <!-- <Footer v-if="$route.path.indexOf('admin') == -1" /> -->
  </div>
</template>

<script>
// import Header from '@/service/Components/Header'
// import Footer from '@/service/Components/Footer'

export default {
  name: 'app',
  components: {
    // Header,
    // Footer
  }
}
</script>

<style lang="scss">
* {
  -webkit-box-align: center;
}
// #app {
//   // font-family: Avenir, Helvetica, Arial, sans-serif;
//   // -webkit-font-smoothing: antialiased;
//   // -moz-osx-font-smoothing: grayscale;
//   // // text-align: center;
//   // color: #2c3e50;
// }

</style>
