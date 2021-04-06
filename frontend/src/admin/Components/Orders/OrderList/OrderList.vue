<template>
  <div>
    <h2>주문 관리 <span class="small">{{menuName}}</span></h2>
    <order-filter-box @search="search"/>
    <div class="divide">
      <a-select style="width: 100px; float:right; " v-model="dataStore.pageLen">
        <a-select-option :value="item.value" v-for="item in rowCounts" :key="item.value">{{ item.label }}</a-select-option>
      </a-select>
      <div style="float:left; line-height: 32px;">주문관리 > {{menuName}} > 리스트</div>
      <div style="clear:both"></div>
    </div>
    <div class="table-header-buttons">
      <a-button size="small" type="success" @click="processDelivery">배송처리</a-button>

      <a-button size="small" type="success">선택한주문 엑셀다운로드</a-button>
      <a-button size="small" type="success">전체주문 엑셀다운로드</a-button>
    </div>

    <board-list :data-store="dataStore" :height="500">
      <template slot="header">
        <th>결제일자</th>
        <th>주문번호</th>
        <th>주문상세번호</th>
        <th>셀러명</th>
<!--        <th>셀러구분</th>-->
<!--        <th>헬피구분</th>-->
<!--        <th>배송구분</th>-->
        <th>상품명</th>
        <th>옵션정보</th>
<!--        <th>옵션추가금액</th>-->
        <th>수량</th>
        <th>주문자명</th>
        <th>핸드폰번호</th>
        <th>결제금액</th>
<!--        <th>사용포인트</th>-->
<!--        <th>쿠폰할인</th>-->
<!--        <th>결제수단</th>-->
        <th>주문상태</th>
      </template>
      <template slot="row" slot-scope="{item}">
        <!--
        additionalPrice: 0
        colorName: "레드"
        name: "말랑말랑"
        orderDate: "2021-04-05 00:00:00"
        orderDetailNumber: "110004"
        orderName: "아버지"
        orderNumber: "10002"
        orderPhone: "010-1111-2222"
        orderStatus: "결제완료"
        productName: "따듯한 아우터"
        quantity: 1
        sizeName: "Medium"
        totalPrice: 21000
        userInfoId: 3
        -->
        <td>{{ item.orderDate }}</td> <!-- 결제일자 -->
        <td>{{ item.orderDetailNumber }}</td> <!-- 주문번호 -->
        <td><router-link :to="''+item.orderDetailNumber">{{ item.orderDetailNumber }}</router-link></td> <!-- 주문상세번호 -->
        <td>{{ item.name }}</td> <!-- 셀러명 -->
        <!--        <th>셀러구분</th>-->
        <!--        <th>헬피구분</th>-->
        <!--        <th>배송구분</th>-->
        <td>{{ item.productName }}</td> <!-- 상품명 -->
        <td>{{ item.colorName }} / {{ item.sizeName }}</td> <!-- 옵션정보 -->
        <!--        <th>옵션추가금액</th>-->
        <td>{{ item.quantity }}</td> <!-- 수량 -->
        <td>{{ item.orderName }}</td> <!-- 주문자명 -->
        <td>{{ item.orderPhone }}</td> <!-- 핸드폰번호 -->
        <td>{{ item.totalPrice | makeComma }}</td> <!-- 결제금액 -->
        <!--        <th>사용포인트</th>-->
        <!--        <th>쿠폰할인</th>-->
        <!--        <th>결제수단</th>-->
        <td>{{ item.orderStatus }}</td> <!-- 주문상태 -->
      </template>
    </board-list>
  </div>
</template>

<script>
import Vue from 'vue'
import store from '../order-store'
import OrderFilterBox from './order-filter-box'
import BoardList from '@/admin/Components/Common/BoardList'
import CommonMixin from '@/admin/mixins/common-mixin'
import Message from '@/admin/utils/message'
import { Modal } from 'ant-design-vue'
const { confirm } = Modal

export default {
  name: 'product-list',
  mixins: [CommonMixin],
  components: { BoardList, OrderFilterBox },
  props: {
    status_id: {
      default () {
        return 0
      }
    }
  },
  data () {
    return {
      dataStore: new Vue(store),
      menuName: '',
      rowCounts: [
        { label: '10개', value: 10 },
        { label: '20개', value: 20 },
        { label: '50개', value: 50 },
        { label: '100개', value: 100 },
        { label: '150개', value: 150 }
      ]
    }
  },
  mounted () {
    this.menuName = this.getSellerPropertyName(this.status_id)
    // this.dataStore.setFilter()
  },
  methods: {
    search (filter) {
      filter = JSON.parse(JSON.stringify(filter))
      filter.status_id = this.status_id
      this.dataStore.page = 1
      this.dataStore.setFilter(filter)
      this.dataStore.load()
    },
    // 상품 구매
    buyProduct (row) {
      console.log('상품 구매', row)
    },
    getSellerPropertyName (orderStatusId) {
      const statusItem = this.constants.orderStatusTypes.filter((d) => { return d.value === orderStatusId })
      if (statusItem.length > 0) return statusItem[0].label
      return ''
    },
    processDelivery () {
      // 체크 리스트가 없다면 처리 불가
      const len = this.dataStore.checkedList.length
      if (len > 0) {
        confirm({
          content: len + '건의 주문을 배송처리 하시겠습니까?',
          onOk: () => {
            this.dataStore.setDelivery(this.dataStore.checkedList)
          }
        })
      } else {
        Message.error('선택된 리스트가 없습니다.')
      }
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
