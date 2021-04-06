<template>
  <div>
    <h2>상품 관리</h2>
    <product-filter-box @search="search"/>
    <div class="divide">
      <a-select style="width: 100px; float:right; " v-model="dataStore.pageLen">
        <a-select-option :value="item.value" v-for="item in rowCounts" :key="item.value">{{ item.label }}</a-select-option>
      </a-select>
      <div style="float:left; line-height: 32px;">상품관리 / 상품 관리 > 상품관리 관리 > 리스트</div>
      <div style="clear:both"></div>
    </div>
    <div class="table-header-buttons">
      <a-button size="small" type="success">선택한상품 엑셀다운로드</a-button>
      <a-button size="small" type="success">전체상품 엑셀다운로드</a-button>
    </div>

    <board-list :data-store="dataStore" :height="500" @change-page="changePage">
      <template slot="header">
        <th>등록일</th>
        <th>대표이미지</th>
        <th>상품명</th>
        <th>상품코드</th>
        <th>상품번호</th>
        <th>셀러속성</th>
        <th>셀러명</th>
        <th>판매가</th>
        <th>할인가</th>
        <th>판매여부</th>
        <th>진열여부</th>
        <th>할인여부</th>
        <th>Actions</th>
      </template>
      <template slot="row" slot-scope="{item}">
        <td>{{ item.created_at }}</td> <!-- 등록일 -->
        <td><img :src="item.main_image" width="70" height="70"></td> <!-- 대표이미지 -->
        <td>{{ item.name }}</td> <!-- 상품명 -->
        <td><router-link :to="'products/'+item.product_id">{{ item.code_number }}</router-link></td> <!-- 상품코드 -->
        <td>{{ item.product_id }}</td> <!-- 상품번호 -->
        <td>{{ item.seller_property_id | typeToName('sellerSections') }}</td> <!-- 셀러속성 -->
        <td>{{ item.brand_name_korean }}</td> <!-- 셀러명 -->
        <td>{{ item.price | makeComma }}</td> <!-- 판매가 -->
        <td>{{ item.discount_price | makeComma }} <span class="discount-rate" v-if="item.discount_rate > 0">({{ item.discount_rate }}%)</span></td> <!-- 할인가 -->
        <td>{{ item.is_sell | typeToName('saleTypes') }}</td> <!-- 판매여부 -->
        <td>{{ item.is_display | typeToName('exhibitTypes') }}</td> <!-- 진열여부 -->
        <td><!--{{ getProductDiscountTypeName(item.is_discount) }}-->
          {{ item.is_discount | typeToName('discountTypes') }}
        </td> <!-- 할인여부 -->
        <td>
          <a-button type="primary" size="small" @click="buyProduct(item)">구매하기</a-button>
        </td>
      </template>
    </board-list>
    <order-modal
       ref="orderModal"
    />
  </div>
</template>

<script>
import Vue from 'vue'
import store from '../product-store'
import ProductFilterBox from './product-filter-box'
import BoardList from '@/admin/Components/Common/BoardList'
import CommonMixin from '@/admin/mixins/common-mixin'
import Message from '@/admin/utils/message'
import errors from '@/admin/errors/errors'
import OrderModal from './order-modal'
const ExpireTokenException = errors.ExpireTokenException
const TimeoutException = errors.TimeoutException

export default {
  name: 'product-list',
  mixins: [CommonMixin],
  components: { BoardList, ProductFilterBox, OrderModal },
  data () {
    return {
      dataStore: new Vue(store),
      rowCounts: [
        { label: '10개', value: 10 },
        { label: '20개', value: 20 },
        { label: '50개', value: 50 }
      ]
    }
  },
  mounted () {
    this.dataStore.$on('test', (d) => {
      console.log('aa', d)
    })
  },
  methods: {
    search (filter) {
      this.dataStore.page = 1
      this.dataStore.setFilter(filter)
      this.load()
    },
    // 상품 구매
    buyProduct (row) {
      console.log('상품 구매', row)
      this.$refs.orderModal.show(row)
    },
    changePage (page) {
      console.log('page', page)
      this.dataStore.changePage(page)
      this.load()
    },
    load () {
      this.dataStore.load()
        .then((res) => {})
        .catch((e) => {
          // 토큰 만료 처리
          if (e instanceof ExpireTokenException) {
            Message.error(e.message, () => {
              this.$router.push('/')
            })
          } else if (e instanceof TimeoutException) {
            Message.error(e.message)
          } else {
            Message.error(e.message)
          }
        })
    }
  },
  computed: {
  }
}
</script>
<style scoped>
.divide {
  background: #F1F1F1;
  padding: 5px 10px;
  margin-left: -20px;
  margin-right: -20px;
  font-size: 12px;
  font-weight: bold;
}
.table-header-buttons {
  text-align: right;
  margin: 5px;
}
.discount-rate {
  color: red;
}

</style>
