<template>
  <div class="cart">
    <span class="title">장바구니</span>
    <div class="selectBox">
      <div>
        <label>
          <CheckBox v-model="allCheckBtn" />
          <span> 전체선택 ({{ this.selectItems.length }}/{{ this.totalCount }})</span>
        </label>
      </div>
      <div>
        <span @click="selectDelete">선택삭제</span>
        <span>품절삭제</span>
      </div>
    </div>

    <table class="cart-list">
      <thead>
        <tr class="cart-list-title">
          <td colspan="5">일반 배송</td>
        </tr>
      </thead>
      <tbody>
        <CartOption v-for="cart in cartList" :brand="cart" :key="cart" />
      </tbody>
    </table>

    <div class="price-box">
      <span class="price-title">총 결재 예상 금액</span>
      <div>
        <span>총 상품 금액 {{ this.totalPrice | makeComma }}원 - 즉시할인 + 총 배송비 {{ this.totalPrice > 30000 ? 0 : 3000 | makeComma}}원</span>
        <span>총 결재 예상 금액 <span class="price">{{ this.totalPrice > 30000 ? this.totalPrice : this.totalPrice + 3000 | makeComma }}</span>원</span>
      </div>
    </div>

    <button class="buy-btn" @click="buyBtn">구매하기</button>
  </div>
</template>

<script>
import CheckBox from '@/service/Components/CheckBox'
import CartOption from '@/service/Cart/CartOption'
// import SERVER_IP from '@/config'
// import API from '@/service/util/service-api'
import mock from '@/Data/Cart'
import { EventBus } from '@/service/util/event-bus'

// const thisTarget = this

export default {
  created () {
    // API.methods
    //   .get(`${SERVER_IP}/cart`)
    //   .then((res) => {
    //     // 한번 수정하기
    //     this.cartList = res.data
    //   })
    //   .catch()
    const copyMock = JSON.parse(JSON.stringify(mock))
    for (let i = 0, len = copyMock.cartList.length; i < len; i++) {
      for (let z = 0, len2 = copyMock.cartList[i].detail.length; z < len2; z++) {
        copyMock.cartList[i].detail[z].checked = false
      }
    }

    this.cartList = copyMock.cartList
    this.totalCount = mock.totalCount

    EventBus.$on('check-item', item => {
      this.selectItems.push(item)

      if (this.totalCount === this.selectItems.length) {
        document.getElementById('allSelect').arrt('checked')
      } else {
        document.getElementById('allSelect').removeAttribute('checked')
      }
    })

    EventBus.$on('unCheck-item', item => {
      for (let i = 0; i < this.selectItems.length; i++) {
        if (this.selectItems[i].id === item.id) {
          this.selectItems.splice(i, 1)
          break
        }
      }
    })

    EventBus.$on('cal-price', () => {
      // this.totalPrice = this.calTotalPrice()
    })
  },
  updated () {
    // this.totalPrice = this.calTotalPrice()
  },
  data () {
    return {
      cartList: [],
      totalCount: 0
      // totalPrice: 0
    }
  },
  computed: {
    selectItems () {
      const list = []
      for (let i = 0, len = this.cartList.length; i < len; i++) {
        for (let z = 0, len2 = this.cartList[i].detail.length; z < len2; z++) {
          if (this.cartList[i].detail[z].checked) {
            list.push(this.cartList[i].detail[z])
          }
        }
      }
      return list
    },
    totalPrice () {
      let sum = 0
      for (let i = 0; i < this.selectItems.length; i++) {
        sum += (this.selectItems[i].price * this.selectItems[i].quantity)
      }

      return sum
    },
    allCheckBtn: {
      get () {
        return this.selectItems.length === this.totalCount
      },
      set (v) {
        for (let i = 0, len = this.cartList.length; i < len; i++) {
          for (let z = 0, len2 = this.cartList[i].detail.length; z < len2; z++) {
            this.cartList[i].detail[z].checked = v
          }
        }
      }
    }
  },
  components: {
    CheckBox,
    CartOption
  },
  methods: {
    selectDelete () {
      for (let i = 0, len = this.cartList.length; i < len; i++) {
        for (let z = 0, len2 = this.cartList[i].detail.length; z < len2; z++) {
          this.cartList[i].detail[z].checked = false
        }
      }
      this.selectItems = []
    },
    buyBtn () {
      if (this.selectItems.length > 0) {
        const data = {
          items: this.selectItems,
          totalPrice: this.totalPrice
        }
        localStorage.removeItem('cart')
        localStorage.setItem('cart', JSON.stringify(data))
        this.$router.push('/order')
      } else {
        // 여기에 Toast 넣기! data에 errorMessage도 넣기!
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.cart {
  display: flex;
  flex-direction: column;
  width: 85%;
  margin: 0 auto;
  color: black;

  .title {
    display: inline-block;
    width: 100%;
    margin: 70px auto;
    font-size: 30px;
    text-align: center;
  }
  .selectBox {
    display: flex;
    width: 100%;
    background-color: #f2f2f2;
    padding: 30px 20px;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 90px;

    div:first-child {
      font-size: 20px;
      span {
        margin-left: 5px;
      }
    }

    div:last-child {
      span {
        padding: 15px;
        border: solid 1px black;
        font-size: 16px;
        margin-left: 10px;
      }
      span:hover {
          background-color: black;
          color: white;
          cursor: pointer;
      }
    }
  }

  .cart-list {
    width: 100%;
    border-top: solid 1px black;
    border-bottom: solid 1px black;
    text-align: center;
    margin-bottom: 70px;

    tr {
      border-bottom: solid 1px rgb(228, 228, 228);
    }
    tr:last-child {
      border: 0;
    }

    .cart-list-title > td {
      font-size: 20px;
      font-weight: 600;
      padding: 30px 0;
      text-align: left;
    }
    // .cart-list-brand {
    //   font-size: 15px;

    //   td {
    //     border-bottom: solid 1px rgb(228, 228, 228);
    //     padding: 20px 0;
    //   }
    //   td:first-child {
    //     font-size: 18px;
    //     font-weight: 600;
    //     text-align: left;
    //   }
    // }
    // .cart-list-product {
    //   padding: 15px 0;

    //   td {
    //     padding: 15px 15px 15px 0;
    //   }
    //   td:nth-child(2) {
    //     width: 80px;
    //     height: 80px;
    //     overflow: hidden;

    //     img {
    //       width: 80px;
    //       height: auto;
    //     }
    //   }
    //   td:nth-child(3) {
    //     width: 60%;
    //     text-align: left;

    //     div:first-child {
    //       font-size: 17px;
    //     }
    //     div:last-child {
    //       color: rgb(135, 135, 135);
    //     }
    //   }
    //   td:nth-child(4) {
    //     div {
    //       text-align: center;

    //       button {
    //         background-color: white;
    //         border: solid 1px rgb(228, 228, 228);
    //         width: 25px;
    //       }
    //       span {
    //         font-size: 10px;
    //         padding: 4px 4px;
    //       }
    //     }
    //   }
    //   td:nth-child(5) {
    //     display: flex;
    //     flex-direction: column;
    //     * {
    //       display: inline-block;
    //     }
    //     span {
    //       font-size: 23px;
    //       font-weight: 600;
    //     }
    //     button {
    //       font-size: 13px;
    //       margin: 0 auto;
    //       width: 120px;
    //       background-color: black;
    //       color: white;
    //       padding: 10px 20px;
    //     }
    //   }
    // }
  }
  .price-box {
    font-size: 25px;
    margin-bottom: 70px;

    .price-title {
      font-weight: 200;
    }
    div {
      display: flex;
      border-top: solid 1px black;
      border-bottom: solid 1px black;
      padding: 30px 15px;
      justify-content: space-between;
      font-weight: 600;

      .price {
        color: #ff204b;
      }
    }
  }

  .buy-btn {
    color: white;
    background-color: black;
    font-size: 20px;
    font-weight: 600;
    padding: 20px 100px;
    margin-bottom: 70px;
  }
}
</style>
