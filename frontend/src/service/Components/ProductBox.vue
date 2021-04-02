<template>
  <div class="product">
    <div class="productImage" @click="linkToDetail(product)">
      <img :src="product.thumbnailImage" alt="thumbnail img" />
    </div>
    <div class="brandName">{{ product.sellerName }}</div>
    <div class="productName">{{ product.name }}</div>
    <div class="productPrice">
      <span class="discountRate" v-if="product.discountRate"
        >{{ product.discountRate }}%</span
      >
      <span class="discountPrice" v-if="product.discountRate">
        {{ product.discountPrice | makeComma }}
      </span>
      <span
        :class="{
          noneDisCountPrice: !product.discountRate,
          price: product.discountRate,
        }"
        >{{
            product.price | makeComma
        }}</span
      >
    </div>
    <!-- <div class="saleCount">
      <span>{{ product.totalSales }}</span>
    </div> -->
  </div>
</template>
<script>
// const global = this
export default {
  props: {
    product: {
      type: Object,
      default () {
        return {
          thumbnailImage: '',
          name: '',
          // sales_price: this.methods.getDiscountPrice(this.original_price, this.discount_rate),
          price: 0,
          discountRate: 0,
          totalSales: 0,
          sellerName: ''
        }
      }
    }
  },
  data () {
    return {}
  },
  methods: {
    linkToDetail (product) {
      this.$emit('linkToDetail', product)
    }
  }
}
</script>
<style lang="scss">
.product {
  display: inline-block;
  text-align: left;
  width: 255px;
  padding: 0 0.5% 30px 0.5%;

  .brandName {
    margin-top: 15px;
    font-size: 16px;
    font-weight: 500;
    color: #757575
  }

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
    margin-top: 5px;
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
      color: black;
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
