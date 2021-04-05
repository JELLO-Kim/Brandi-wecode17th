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
// eslint-disable-next-line no-unused-vars
import mockup from '@/Data/ProductList.json'
import ProductBox from '@/service/Components/ProductBox'
import DropDown from '@/service/Components/DropDown'
import API from '@/service/util/service-api'
import SERVER from '@/config.js'
import { EventBus } from '@/service/util/event-bus'

export default {
  name: 'ProductList',
  created () {
    // const url = `${SERVER.SERVER}/products/list`
    // API.methods
    //   .get(this.subId === 0 ? url : url + '?category=' + this.subId)
    //   .then((res) => {
    //     console.log(res.data.result.data)
    //     // console.log(res.result.data)
    //     this.productList = res.data.result.data
    //     // this.productList = res.data.result.product
    //   })
    //   .catch(() => {
    //     this.$router.push('/main')
    //     alert('존재하지 않는 서비스 상품입니다.')
    //   })

    EventBus.$on('select-sub', item => {
      this.subId = item
    })
    API.methods
      .get(`${SERVER.IP}/products/list`)
      .then((res) => {
        console.log(res.data.result.data)
        // console.log(res.result.data)
        this.productList = res.data.result.data
        // this.productList = res.data.result.product
      })
      .catch(() => {
        // console.log(error)
        this.$router.push('/main')
        alert('존재하지 않는 서비스 상품입니다.')
      })
  },
  components: {
    ProductBox,
    DropDown
  },
  data () {
    return {
      productList: [],
      // productList: [],
      orderList: [
        { key: 'daily', label: '일간' },
        { key: 'weekly', label: '주간' },
        { key: 'mothy', label: '월간' }
      ],
      offset: 0,
      limit: 8,
      subId: 0
    }
  },
  methods: {
    linkToDetail (product) {
      this.$router.push(`/detail/${product.productId}`)
    },
    moreItemBtn () {
      this.offset++
      API.methods
        .get(`${SERVER.IP}/products/list?offset=${this.offset}`)
        .then(res => {
          this.productList.concat(res.data)
        })
        .catch(error => {
          alert(error)
        })
    }
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
