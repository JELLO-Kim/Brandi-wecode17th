<template>
  <div>
    <section class="main">
      <main class="article">
        <img src="/images/erdetail.jpeg">

        <div class="buttons">
          <button type="button" class="selected">버튼명1</button>
          <button type="button">버튼명1</button>
        </div>

        <div class="productBox">
          <ProductBox :product="product" v-for="product in productList" :key="product" @linkToDetail="linkToDetail"></ProductBox>
        </div>
      </main>
    </section>
  </div>
</template>

<script>
import { ClientId } from '@/config.js'
// import axios from 'axios'
import ProductBox from '@/service/Components/ProductBox'
// import Footer from '@/service/Components/Footer'
import { mapMutations } from 'vuex'
import mockup from '@/Data/ProductList.json'

const serviceStore = 'serviceStore'

export default {
  components: {
    // Footer
    ProductBox
  },
  data () {
    return {
      productList: mockup.data,
      // 구글 로그인 하기
      params: {
        client_id: ClientId
      },
      renderParams: {
        width: 250,
        height: 50,
        longtitle: true
      }
    }
  },
  methods: {
    ...mapMutations(serviceStore, ['getStorageToken']),
    linkToDetail (product) {
      this.$router.push(`/detail/${product.product_no}`)
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  .article {
    width: 1240px;
    margin: 50px auto 50px auto;
    // display: flex;
    // flex-direction: column;
    // align-items: center;
    text-align: center;
    > img {
      width: 100%;
    }
    .buttons {
      margin: 20px 0;
      button {
        padding: 10px 20px;
        margin: 0 10px;
        border: none;
        border-radius: 30px;
        background: #CCC;
        font-size: 18px;
        font-weight: bold;
        color: #FFF;
        &.selected {
          background: linear-gradient(250deg, #FF5E7E, #ff204b 45%)
        }
      }
    }
  }
}
</style>
