<template>
  <div class="cart">
    <span class="title">장바구니</span>
    <div class="selectBox">
      <div>
        <label>
          <CheckBox v-model="isSelectAll" />
          <span>전체선택 (1/1)</span>
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
        <div></div>
        <CartOption />
      </tbody>
    </table>

    <div class="price-box">
      <span class="price-title">총 결재 예상 금액</span>
      <div>
        <span>총 상품 금액 99,999원 - 즉시할인 + 총 배송비 0원</span>
        <span>총 결재 예상 금액 <span class="price">99,999</span>원</span>
      </div>
    </div>

    <button class="buy-btn">구매하기</button>
  </div>
</template>

<script>
import CheckBox from '@/service/Components/CheckBox'
import CartOption from '@/service/Cart/CartOption'

export default {
  data () {
    return {
      isSelectAll: false,
      selectItems: []
    }
  },
  components: {
    CheckBox,
    CartOption
  },
  methods: {
    selectDelete () {
      this.selectItems = []
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
    .cart-list-brand {
      font-size: 15px;

      td {
        border-bottom: solid 1px rgb(228, 228, 228);
        padding: 20px 0;
      }
      td:first-child {
        font-size: 18px;
        font-weight: 600;
        text-align: left;
      }
    }
    .cart-list-product {
      padding: 15px 0;

      td {
        padding: 15px 15px 15px 0;
      }
      td:nth-child(2) {
        width: 80px;
        height: 80px;
        overflow: hidden;

        img {
          width: 80px;
          height: auto;
        }
      }
      td:nth-child(3) {
        width: 60%;
        text-align: left;

        div:first-child {
          font-size: 17px;
        }
        div:last-child {
          color: rgb(135, 135, 135);
        }
      }
      td:nth-child(4) {
        div {
          text-align: center;

          button {
            background-color: white;
            border: solid 1px rgb(228, 228, 228);
            width: 25px;
          }
          span {
            font-size: 10px;
            padding: 4px 4px;
          }
        }
      }
      td:nth-child(5) {
        display: flex;
        flex-direction: column;
        * {
          display: inline-block;
        }
        span {
          font-size: 23px;
          font-weight: 600;
        }
        button {
          font-size: 13px;
          margin: 0 auto;
          width: 120px;
          background-color: black;
          color: white;
          padding: 10px 20px;
        }
      }
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
