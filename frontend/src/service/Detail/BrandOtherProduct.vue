<template>
  <div class="brand-other-product">
    <ProductBox :product="product" v-for="product in this.products" :key="product" @linkToDetail="linkToDetail"></ProductBox>
  </div>
</template>

<script>
import ProductBox from '@/service/Components/ProductBox'

export default {
  components: {
    ProductBox
  },
  props: {
    products: Array
  },
  methods: {
    linkToDetail (product) {
      this.$router.push(`/detail/${product.id}`)
    }
  }
}
</script>

<style>

</style>
