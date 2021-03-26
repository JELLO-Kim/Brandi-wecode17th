<template>
  <div class="cart-option">
    <tr class="cart-list-brand">
      <td colspan="20">가게명</td>
      <td>수량</td>
      <td>주문금액</td>
    </tr>
    <tr class="cart-list-product">
      <td>
        <CheckBox></CheckBox>
      </td>
      <td>
        <img
          src="https://image.brandi.me/cproduct/2021/02/26/SB000000000020525602_1614328241_image1_S.jpeg"
          alt=""
        />
      </td>
      <td>
        <div>상품이름</div>
        <div>color / size (일반배송)</div>
      </td>
      <td>
        <div>
          <button>-</button>
          <span>1</span>
          <button>+</button>
        </div>
      <td>
        <span>99,999원</span>
        <button>바로주문</button>
      </td>
    </tr>
  </div>
</template>

<script>
// import CheckBox from '@/service/Components/CheckBox'

export default {
  components: {
    // CheckBox
  },
  props: {
    product: {
      brandName: String,
      ThumbnailImage: String,
      name: String,
      color: String,
      size: String,
      quantity: Number,
      totalprice: Number
    }
  }
}
</script>

<style lang="scss" scoped>
.cart-option {
  width: 100%;
}
</style>
