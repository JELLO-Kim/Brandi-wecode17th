<template>
  <div v-if="order.data.length">
    <div class="container">
      <div
        class="orderContainer"
        v-for="order in order.data"
        v-bind:key="order.order_detail_no"
      >
        <div class="orderTop">
          <div class="topLeft">
            <div>{{ getDate(order.start_time) }}</div>
            <div class="divider"></div>
            <div class="orderDetailNo">
              {{ getOrderDetailNo(order.start_time, order.order_detail_no) }}
            </div>
          </div>
          <div
            class="toDetail"
            @click="linkToOrderDetail(order.order_detail_no)"
          >
            <span>주문상세보기</span>
            <img
              src="/Images/ic-titleic-detailpage-moreaction@3x.png"
              alt=">"
            />
          </div>
        </div>
        <div class="orderMid">판매자 배송 상품</div>
        <div class="orderDetail">
          <div class="detailTop">
            <div class="cellerName">브랜디</div>
            <div class="topMenu">
              <div>주문금액</div>
              <div>진행상황</div>
            </div>
          </div>
          <div class="detailBottom">
            <div class="imgContainer">
              <img
                :src="order.image_small"
                alt="small_image"
                @click="linkToProductDetail"
                :value="order.product_no"
              />
            </div>
            <div class="productDetail">
              <div
                class="productName"
                @click="linkToProductDetail"
                :value="order.product_no"
              >
                {{ order.product_name }}
              </div>
              <div class="productOption">
                {{ order.color }} / {{ order.size }}
              </div>
              <div class="orderQuantity">{{ order.quantity }} 개</div>
            </div>
            <div class="orderPrice">
              {{ numberWithCommas(order.total_price) }} 원
            </div>
            <div class="orderStatus">{{ order.order_status }}</div>
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
import axios from 'axios'
import { SERVER_IP } from '@/config'
import { mapGetters } from 'vuex'

const serviceStore = 'serviceStore'

export default {
  created () {
    this.getOrderData()
  },
  data () {
    return {
      order: { data: [] },
      orderData: false
    }
  },
  methods: {
    getOrderData () {
      const token = this.getToken
      axios
        .get(`${SERVER_IP}/user/mypage/orderlist`, {
          headers: {
            Authorization: token
          }
        })
        .then((res) => {
          this.order = res.data
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.$router.push('/error/400')
          } else if (error.response.status === 400) {
            this.$router.push('/error/400')
          }
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
    linkToProductDetail (e) {
      console.log(e.target.attributes.value.value)
      this.$router.push(`/detail/${e.target.attributes.value.value}`)
    },
    // 주문 상세페이지로 이동
    linkToOrderDetail (orderDetailId) {
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
