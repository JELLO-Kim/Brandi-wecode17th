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
            <ProductBox :product="product" v-for="product in products" :key="product.productId" @linkToDetail="linkToDetail"></ProductBox>
          </article>
        </section>
        <div>
          <button class="moreItemBtn" @click="moreItemBtn">더보기</button>
        </div>
      </div>
    </main>
  </div>
</template>
<script>
import Banner from '@/service/Components/Banner'
import ProductBox from '@/service/Components/ProductBox'
// eslint-disable-next-line no-unused-vars
import API from '@/service/util/service-api'
// eslint-disable-next-line no-unused-vars
import SERVER from '@/config.js'
// eslint-disable-next-line no-unused-vars
import mockup from '@/Data/ProductMain.json'
// import axios from 'axios'

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
      products: []
    }
  },
  methods: {
    getProductData () {
      // this.products = mockup.result.data
      API.methods.get(`${SERVER.IP}/products/list`)
        .then((res) => {
          // console.log(res)
          this.products = res.data.result.data
        })
        .catch(() => {
          this.$router.push('/error/500')
        })
    },
    numberWithCommas (x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    linkToDetail (product) {
      // console.log(product)
      this.$router.push(`/detail/${product.productId}`)
    },
    moreItemBtn () {
      this.$router.push('/category')
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

.moreItemBtn {
  display: block;
  margin: 30px auto 70px;
  padding: 15px 120px;
  border: solid 1px black;
  background-color: white;
  color: black;
}
.moreItemBtn:hover {
  background-color: black;
  color: white;
  cursor: pointer;
}
</style>
