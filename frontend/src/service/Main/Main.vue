<template>
  <div>
    <Banner />
    <main>
      <div class="mainProducts">
        <section class="productContainer">
          <div class="productTitle">
            <h1>
              <span class="mainTitle">브랜디는 하루배송</span>
              <span class="subTitleText">오늘 사고 내일 바로 입자!</span>
            </h1>
          </div>
          <article class="productList">
            <ProductBox :product="product" v-for="product in product.data" :key="product"></ProductBox>
          </article>
        </section>
      </div>
    </main>
  </div>
</template>
<script>
// import axios from 'axios'
import Banner from '@/service/Components/Banner'
// import { SERVER_IP } from '@/config'
import mockup from '@/Data/ProductList.json'
import ProductBox from '@/service/Components/ProductBox'

export default {
  components: {
    Banner,
    ProductBox
  },
  created () {
    this.getProductData()
  },
  data () {
    return {
      product: []
    }
  },
  methods: {
    getProductData () {
      this.product = mockup
      // axios.get(`${SERVER_IP}/product`).then((res) => {
      //   this.product = res.data
      // })
    },
    numberWithCommas (x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    linkToDetail (product) {
      this.$router.push(`/detail/${product.product_no}`)
    }
  }
}
</script>
<style lang="scss" scoped>
main {
  display: flex;
  justify-content: center;
  .mainProducts {
    max-width: 1275px;
    .productContainer {
      display: flex;
      flex-direction: column;
      .productTitle {
        margin-top: 100px;
        margin-bottom: 15px;
        .mainTitle {
          font-size: 26px;
          font-weight: bold;
        }
        .subTitleText {
          font-size: 20px;
          margin-left: 5px;
          color: #4a4a4a;
        }
      }
    }
  }
}
</style>
