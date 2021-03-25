<template>
  <div class="box">
    <div class="order">
      <DropDown class="order-box" :items="orderList"></DropDown>
    </div>
    <div class="products">
      <ProductBox :product="product" v-for="product in productList" :key="product" @linkToDetail="linkToDetail"></ProductBox>
    </div>
    <div>
      <button class="moreItemBtn" @click="moreItemBtn">더보기</button>
    </div>
  </div>
</template>

<script>
import mockup from '@/Data/ProductList.json'
import ProductBox from '@/service/Components/ProductBox'
import DropDown from '@/service/Components/DropDown'

export default {
  name: 'ProductList',
  components: {
    ProductBox,
    DropDown
  },
  data () {
    return {
      productList: mockup.data,
      orderList: [
        { key: 'daily', label: '일간' },
        { key: 'weekly', label: '주간' },
        { key: 'mothy', label: '월간' }
      ]
    }
  },
  methods: {
    linkToDetail () {
      console.log('linkToDetail')
    },
    moreItemBtn () {}
  }
}
</script>

<style lang="scss" scoped>
.box {
  .order {
    margin: 5px 0;
    text-align: right;
    .order-box {
      width: 200px;
    }
  }
  .products {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
}
.moreItemBtn {
  display: block;
  margin: 30px auto 70px;
  padding: 15px 120px;
  border: solid 1px black;
  background-color: white;
  color: black;
}
.moreItemBtn:hover {
  background-color: black;
  color: white;
  cursor: pointer;
}
</style>
