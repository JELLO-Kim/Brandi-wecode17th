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
// eslint-disable-next-line no-unused-vars
import SERVER from '@/config'
// eslint-disable-next-line no-unused-vars
import API from '@/service/util/service-api'
// import mock from '@/Data/Cart'
import { EventBus } from '@/service/util/event-bus'

// const thisTarget = this

export default {
  created () {
    API.methods
      .get(`${SERVER.IP}/cart`)
      .then((res) => {
        // 한번 수정하기
        const result = res.data.result.data.cartList
        for (let i = 0, len = result.length; i < len; i++) {
          for (let z = 0, len2 = result[i].detail.length; z < len2; z++) {
            result[i].detail[z].checked = false
          }
        }
        this.cartList = result
        this.totalCount = res.data.result.totalCount
      })

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
  },
  updated () {
    // this.totalPrice = this.calTotalPrice()
  },
  data () {
    return {
      cartList: []
      // totalCount: 0
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
    totalCount () {
      let total = 0
      for (let i = 0, len = this.cartList.length; i < len; i++) {
        for (let z = 0, len2 = this.cartList[i].detail.length; z < len2; z++) {
          total++
        }
      }
      return total
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
      if (this.selectItems.length > 0) {
        API.methods
          .delete(`${SERVER.IP}/cart`, {
            data: {
              productOptionIds: this.selectItems.map(d => { return d.id })
            }
          })
          .then((res) => {
            if (res.data.message === 'SUCCESS') {
              // 삭제 하였다면 리스트 삭제
              for (let i = 0, len = this.cartList.length; i < len; i++) {
                for (let z = 0; z < this.cartList[i].detail.length; z++) {
                  if (this.cartList[i].detail[z].checked) {
                    this.cartList[i].detail.splice(z, 1)
                    z--
                  }
                }
              }
            }
            // alert(res)
          })
      }
    },
    buyBtn () {
      if (this.selectItems.length > 0) {
        // const cartArray = []
        // for (let i = 0; i < this.selectItems.length; i++) {
        //   this.selectItems[i]
        // }

        const data = {
          userId: localStorage.getItem('userId'),
          items: this.selectItems,
          totalPrice: this.totalPrice
        }
        localStorage.removeItem('cart')
        localStorage.setItem('cart', JSON.stringify(data))
        this.$router.push('/order')
      } else {
        this.$toast.open({
          message: '옵션을 한개 이상 선택해주세요.',
          position: 'bottom',
          duration: 3000,
          type: 'default'
        })
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
