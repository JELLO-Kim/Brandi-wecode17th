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
            <div
              class="product"
              v-for="product in product.data"
              v-bind:key="product.product_id"
            >
              <div class="productImage" @click="linkToDetail(product)">
                <img :src="product.thumbnail_image" alt="thumbnail  img" />
              </div>
              <div class="productName">{{ product.product_name }}</div>
              <div class="productPrice">
                <span class="discountRate" v-if="product.discount_rate"
                  >{{ product.discount_rate }}%</span
                >
                <span class="discountPrice" v-if="product.discount_rate">
                  {{ product.sales_price | makeComma }}
                </span>
                <span
                  :class="{
                    noneDisCountPrice: !product.discount_rate,
                    price: product.discount_rate,
                  }"
                  >{{
                      Math.round(product.original_price / 10) * 10 | makeComma
                  }}</span
                >
              </div>
            </div>
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

export default {
  components: {
    Banner
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
      .productList {
        .product {
          display: inline-block;
          width: 255px;
          padding: 0 0.5% 30px 0.5%;
          .productImage {
            height: 254px;
            cursor: pointer;
            img {
              width: 100%;
              height: 100%;
            }
          }
          .productName {
            height: 20px;
            margin-top: 15px;
            font-size: 16px;
            font-weight: 500;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
          }
          .productPrice {
            margin-top: 5px;
            .discountRate {
              font-size: 20px;
              font-weight: 600;
              padding-right: 6px;
              color: #ff204b;
            }
            .price {
              font-size: 15px;
              color: #757575;
              text-decoration: line-through;
            }
            .noneDisCountPrice {
              font-size: 20px;
              font-weight: 600;
              padding-right: 6px;
            }

            .discountPrice {
              font-size: 20px;
              font-weight: 600;
              padding-right: 6px;
            }
          }
        }
      }
    }
  }
}
</style>
