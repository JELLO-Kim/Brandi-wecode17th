<template>
  <div class="product">
    <div class="productImage" @click="linkToDetail(product)">
      <img :src="product.thumbnail_image" alt="thumbnail img" />
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
</template>
<script>
export default {
  props: {
    product: {
      type: Object,
      default () {
        return {
          thumbnail_image: '',
          product_name: '',
          sales_price: 0,
          original_price: 0,
          discount_rate: 0
        }
      }
    }
  },
  data () {
    return {}
  }
}
</script>
<style lang="scss">
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

</style>
