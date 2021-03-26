<template>
  <div class="box">
    <div class="order">
      <DropDown class="order-box" :items="orderList"></DropDown>
    </div>
    <div class="products">
      <ProductBox :product="product" v-for="product in productList" :key="product" @linkToDetail="linkToDetail"></ProductBox>
    </div>
  </div>
</template>

<script>
import mockup from '@/Data/ProductList.json'
import ProductBox from '@/service/Components/ProductBox'
import DropDown from '@/service/Components/DropDown'
// import API from '@/service/util/service-api'
// import SERVER from '@/config.js'

export default {
  name: 'ProductList',
  created () {
    // API.methods
    //   .get(`${SERVER.IP}/main`)
    //   .then((res) => {
    //     console.log(res.data.result.data)
    //     // console.log(res.result.data)
    //     this.productList = res.data.result.data
    //     // this.productList = res.data.result.product
    //   })
    //   .catch(() => {
    //     // console.log(error)
    //     this.$router.push('/main')
    //     alert('존재하지 않는 서비스 상품입니다.')
    //   })
  },
  components: {
    ProductBox,
    DropDown
  },
  data () {
    return {
      productList: mockup.data,
      // productList: [],
      orderList: [
        { key: 'daily', label: '일간' },
        { key: 'weekly', label: '주간' },
        { key: 'mothy', label: '월간' }
      ]
    }
  },
  methods: {
    linkToDetail (product) {
      this.$router.push(`/detail/${product.id}`)
    }
  }
}
</script>

<style lang="scss" scoped>
.box {
  .order {
    margin: 5px 0;
    text-align: right;
    .order-box {
      width: 200px;
    }
  }
  .products {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
}
</style>
