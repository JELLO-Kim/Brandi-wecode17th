<template>
  <div v-if="orderList.length">
    <div class="container">
      <div
        class="orderContainer"
        v-for="order in orderList"
        v-bind:key="order.order_detail_no"
      >
        <div class="orderTop">
          <div class="topLeft">
            <div>{{ getDate(order.orderTime) }}</div>
            <div class="divider"></div>
            <div class="orderDetailNo">
              <!-- {{ getOrderDetailNo(order.start_time, order.order_detail_no) }} -->
            </div>
          </div>
          <div
            class="toDetail"
            @click="linkToOrderDetail(order.orderId)"
          >
            <span>주문상세보기</span>
            <img
              src="/images/ic-titleic-detailpage-moreaction@3x.png"
              alt=">"
            />
          </div>
        </div>
        <div class="orderMid">판매자 배송 상품</div>
        <div class="orderDetail" v-for="product in order.product" :key="product">
          <div class="detailTop">
            <div class="cellerName">{{product.brand}}</div>
            <div class="topMenu">
              <div>주문금액</div>
              <div>진행상황</div>
            </div>
          </div>
          <div class="detailBottom" v-for="option in product.option" :key="option">
            <div class="imgContainer">
              <img
                :src="option.productImage"
                alt="small_image"
                @click="linkToProductDetail(option.productId)"
              />
            </div>
            <div class="productDetail">
              <div
                class="productName"
                @click="linkToProductDetail(option.productId)"
              >
                {{ option.name }}
              </div>
              <div class="productOption">
                {{ option.productColor }} / {{ option.productSize }}
              </div>
              <div class="orderQuantity">{{ option.quantity }} 개</div>
            </div>
            <div class="orderPrice">
              {{ option.totalPrice | makeComma }} 원
            </div>
            <div class="orderStatus">{{ option.status }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="noOrder">주문한 상품이 없습니다.</div>
  </div>
</template>

<script>
// import axios from 'axios'
// eslint-disable-next-line no-unused-vars
import mockup from '@/Data/MypageOrderList.json'
import { mapGetters } from 'vuex'
// eslint-disable-next-line no-unused-vars
import API from '@/service/util/service-api'
// eslint-disable-next-line no-unused-vars
import SERVER from '@/config.js'
const serviceStore = 'serviceStore'

export default {
  created () {
    this.getOrderData()
  },
  data () {
    return {
      orderList: [],
      order: { data: [] },
      offset: 0,
      orderData: false
    }
  },
  methods: {
    getOrderData () {
      // const token = this.getToken
      // this.orderList = this.orderList.concat(mockup.result.data)
      API.methods
        .get(`${SERVER.IP}/mypage/order`)
        .then(res => {
          // console.log(res.data.result.data)
          this.orderList = this.orderList.concat(res.data.result.data)
        })
        .catch(error => {
          alert(error)
        })
    },
    // 2020-08-29 형태로 변환
    getDate (x) {
      const dates = new Date(x)
      const month =
        (dates.getMonth() + 1 < 10 ? '0' : '') + (dates.getMonth() + 1)
      const date = (dates.getDate() < 10 ? '0' : '') + dates.getDate()
      return `${dates.getFullYear()}.${month}.${date}`
    },
    getOrderDetailNo (orderdate, orderid) {
      const dates = new Date(orderdate)
      const month =
        (dates.getMonth() + 1 < 10 ? '0' : '') + (dates.getMonth() + 1)
      const date = (dates.getDate() < 10 ? '0' : '') + dates.getDate()
      return `${dates.getFullYear()}${month}${date}${orderid}`
    },
    numberWithCommas (x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    // 상품 상세페이지로 이동
    linkToProductDetail (no) {
      this.$router.push(`/detail/${no}`)
    },
    // 주문 상세페이지로 이동
    linkToOrderDetail (orderDetailId) {
      // console.log(orderDetailId)
      this.$router.push(`/mypage/orderDetail/${orderDetailId}`)
    },

    getDiscountPrice (price, discountRate) {
      return price * ((100 - discountRate) / 100)
    }
  },
  computed: {
    ...mapGetters(serviceStore, ['getToken'])
  }
}
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.orderContainer {
  margin-bottom: 100px;
  width: 1260px;

  .orderTop {
    display: flex;
    justify-content: space-between;
    font-size: 25px;
    font-weight: bold;
    padding-bottom: 15px;
    border-bottom: 3px solid black;

    .topLeft {
      display: flex;

      .divider {
        background-color: black;
        width: 2px;
        height: 17px;
        margin: 12px 10px 0 10px;
      }
    }

    .toDetail {
      cursor: pointer;
      img {
        width: 10px;
      }
    }
  }

  .orderMid {
    font-size: 27px;
    font-weight: bold;
    padding: 15px 0;
    border-bottom: 1px solid black;
  }

  .orderDetail {
    .detailTop {
      border-bottom: 1px solid lightgray;
      display: flex;
      justify-content: space-between;
      padding: 20px 10px;

      .cellerName {
        font-size: 18px;
        font-weight: bold;
      }

      .topMenu {
        display: flex;

        div {
          padding: 0 50px;
          margin-left: 70px;
        }
      }
    }

    .detailBottom {
      padding: 20px 10px;
      display: flex;
      align-items: center;
      border-bottom: 1px solid black;

      .imgContainer {
        cursor: pointer;
        img {
          width: 100px;
        }
      }

      .productDetail {
        width: 750px;
        font-size: 17px;
        margin: 8px 0 8px 35px;

        .productName {
          cursor: pointer;
          font-weight: 500;
          margin-bottom: 5px;
        }

        .productOption,
        .orderQuantity {
          color: gray;
        }
      }

      .orderPrice {
        margin-left: 15px;
        font-size: 20px;
        font-weight: bold;
      }

      .orderStatus {
        font-size: 18px;
        font-weight: bold;
        margin-left: 145px;
      }
    }
  }
}
.noOrder {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}
</style>
