<template>
  <div class="cart-option">
    <tr class="cart-list-brand">
      <td colspan="20">{{ brand.brandName }}</td>
      <td>수량</td>
      <td>주문금액</td>
    </tr>
    <CartDetailOption v-for="list in brand.detail" :list="list" :key="list"/>
  </div>
</template>

<script>
import CartDetailOption from '@/service/Cart/CartDetailOption'

export default {
  created () {
  },
  components: {
    CartDetailOption
  },
  props: {
    brand: {
      type: Object,
      default () {
        return {
          brandName: String,
          detail: Array
        }
      }
    }
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
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

</style>
