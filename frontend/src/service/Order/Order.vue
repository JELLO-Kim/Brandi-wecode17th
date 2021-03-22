<template>
  <div class="order">
    <div class="title"><span>주문하기</span></div>

    <span class="order-title">주문상품 정보</span>
    <table class="order-list">
      <colgroup>
        <col width="5%">
        <col>
        <col width="10%">
      </colgroup>
      <thead>
        <tr class="order-list-title">
            <td colspan="3">일반 배송</td>
        </tr>
        <tr class="order-list-brand">
            <td colspan="2">가게명</td>
            <td>주문금액</td>
        </tr>
      </thead>
      <tbody>
        <tr class="order-list-product">
            <td>
                <img src="https://image.brandi.me/cproduct/2021/02/26/SB000000000020525602_1614328241_image1_S.jpeg" alt="">
            </td>
            <td>
                <div>상품이름</div>
                <div>color / size (일반배송)</div>
                <div>1개</div>
            </td>
            <td>
                <span>99,999 원</span>
            </td>
        </tr>
      </tbody>
    </table>
    <div class="resultPrice">
      <span>총 주문 금액</span>
      <sapn>99,999 원</sapn>
    </div>

    <span class="info-title">주문자 정보</span>
    <table class="info-box">
      <tr>
        <td>이름</td>
        <td><input type="text" placeholder="이름" class="from-name input-name"></td>
      </tr>
      <tr>
        <td>휴대폰</td>
        <td>
          <input type="text" class="from-phone-first input-phone">
          &nbsp;-&nbsp;
          <input type="text" class="from-phone-second input-phone">
          &nbsp;-&nbsp;
          <input type="text" class="from-phone-third input-phone">
        </td>
      </tr>
      <tr>
        <td>이메일</td>
        <td>
          <input type="text" class="email-address input-email">
          &nbsp;@&nbsp;
          <input type="text" class="email-domain input-email">
        </td>
      </tr>
    </table>

    <span class="info-title">배송지 정보</span>
    <table class="info-box">
      <tr>
        <td>수령인</td>
        <td><input type="text" placeholder="이름" class="to-name input-name"></td>
      </tr>
      <tr>
        <td>휴대폰</td>
        <td>
          <input type="text" class="to-phone-first input-phone">
          &nbsp;-&nbsp;
          <input type="text" class="to-phone-second input-phone">
          &nbsp;-&nbsp;
          <input type="text" class="to-phone-third input-phone">
        </td>
      </tr>
      <tr>
        <td>배송주소</td>
        <td class="address">
          <input type="text" class="address-code input-address">
          <input type="text" class="address-first input-address">
          <input type="text" class="address-second input-address">
          <span>* 제주도, 도서 산간 지역 등은 배송이 하루 이상 추가 소요될 수 있습니다</span>
        </td>
      </tr>
      <tr>
        <td>배송메모</td>
        <td>
          <DropDown :item="arr">
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import DropDown from '@/service/Components/DropDown'

export default {
  data () {
    return {
      arr: []
    }
  },
  components: {
    DropDown
  }
}
</script>

<style lang="scss" scoped>
.order {
  display: flex;
  justify-content: center;
  flex-direction: column;
  padding: 0 30px;
  color: black;

  .title {
    font-size: 30px;
    font-weight: 500;
    text-align: center;
    margin: 50px auto;
  }

  .order-title{
    display: inline-block;
    font-size: 25px;
    font-weight: 500;
    margin-bottom: 15px;
  }
  .order-list {
    width: 100%;
    border-top: solid 1px black;
    border-bottom: solid 1px black;
    text-align: center;

    tr {
      border-bottom: solid 1px rgb(228, 228, 228);
    }
    tr:last-child {
      border: 0;
    }

    .order-list-title>td {
      font-size: 20px;
      font-weight: 600;
      padding: 20px 0;
      text-align: left;
    }
    .order-list-brand {
      font-size: 15px;

      td {
        padding: 20px 0;
        border-bottom: solid 1px rgb(228, 228, 228);
      }
      td:first-child {
        font-size: 18px;
        font-weight: 600;
        text-align: left;
      }
    }
    .order-list-product {
        padding: 15px 0;

      td {
        padding: 15px 15px 15px 0;
      }
      td:nth-child(1) {
        width: 80px;
        height: 80px;
        overflow: hidden;

      img {
        width: 80px;
        height: auto;
        }
      }
      td:nth-child(2) {
        width: 60%;
        text-align: left;

        div:first-child {
          font-size: 17px;
        }
        div:last-child {
          color: rgb(135, 135, 135);
        }
      }
      td:nth-child(3) {
        font-size: 20px;
        font-weight: 600;
      }
      td:nth-child(4) {
        font-size: 20px;
        font-weight: 600;
      }
    }
  }

  .resultPrice {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 70px;
    padding: 30px 20px;
    font-size: 25px;
    font-weight: 600;
    color: red;

    span:first-child {
      padding-right: 20px;
      color: black;
    }
  }

input {
  padding: 10px;
  background: #f5f5f5;
  border: 0;
  font-size: 15px;
  outline: 0;
}

.input-name {
  width: 100%
}
.input-phone {
  width: 100px;
}
.input-email {
  width: 250px;
}
.address {
  .input-address {
    margin-bottom: 5px;
    width: 49%;
  }
  span {
    display: block;
    margin-top: 5px;
    color: #9e9e9e;
    font-size: 12px;
  }
}

  .info-title {
    display: inline-block;
    font-size: 25px;
    font-weight: 300;
    margin-bottom: 15px;
  }
  .info-box {
    width: 100%;
    border-top: solid 1px black;
    border-bottom: solid 1px black;
    margin-bottom: 70px;
    font-size: 17px;

    tr {
      td {
        padding: 15px 0;
        border-bottom: solid 1px rgb(228, 228, 228);
      }
      td:first-child {
        width: 20%;
        padding-left: 15px;
        font-weight: 600;
      }
      td:last-child {
        width: 80%;
        font-weight: 400;
      }
    }
    tr:last-child>td {
      border: 0;
    }
  }
}
</style>
