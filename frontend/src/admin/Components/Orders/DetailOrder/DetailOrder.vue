<template>
  <div>
    <div class="fixed-header">
      <h2>주문 상세 관리
<!--        <a-button type="success" @click="working=true">저장하기</a-button>-->
        <a-button type="normal" @click="cancel">취소</a-button>
        <a-spin spin v-show="working"/>
      </h2>
      <div class="divide">
        주문관리 > 주문 상세 페이지
      </div>
      <div class="form-header">
        <a-tabs type="card" :tabBarStyle="{'padding-bottom': 0, 'margin-bottom': '-1px'}" v-model="tabNo" @change="scrollTab">
          <a-tab-pane :key="0" tab="주문 정보" />
          <a-tab-pane :key="1" tab="주문 상세 정보"/>
          <a-tab-pane :key="2" tab="상품 정보" />
          <a-tab-pane :key="3" tab="수취자 정보" />
          <a-tab-pane :key="4" tab="주문상태 변경 정보" />
<!--          <a-tab-pane :key="5" tab="CS 정보" />-->
        </a-tabs>
      </div>
    </div>
    <a-page-header title="주문 정보" key="0" sub-title="기본 정보" class="page-content" v-multi-ref:pageContent>
      <order-info-form :data-store="dataStore"/>
    </a-page-header>
    <a-page-header title="주문 상세 정보" key="1" class="page-content" v-multi-ref:pageContent>
      <order-detail-info-form :data-store="dataStore"/>
    </a-page-header>
    <a-page-header title="상품 정보" key="2" class="page-content" v-multi-ref:pageContent>
      <order-product-info-form :data-store="dataStore"/>
    </a-page-header>
    <a-page-header title="수취자 정보" key="3" class="page-content" v-multi-ref:pageContent>
      <order-delivery-info-form :data-store="dataStore"/>
    </a-page-header>
    <a-page-header title="주문상태 변경 정보" key="4" class="page-content" v-multi-ref:pageContent>
      <order-history-info-form :data-store="dataStore"/>
    </a-page-header>
<!--    <a-page-header title="CS 정보" key="5" class="page-content" v-multi-ref:pageContent>-->
<!--      <order-cs-info-form :data-store="dataStore"/>-->
<!--    </a-page-header>-->
  </div>
</template>

<script>
import Vue from 'vue'
import OrderInfoForm from './order-info-form'
import OrderDetailInfoForm from './order-detail-info-form'
import OrderProductInfoForm from './order-product-info-form'
import OrderDeliveryInfoForm from './order-delivery-info-form'
import OrderHistoryInfoForm from './order-history-info-form'
// import OrderCsInfoForm from './order-cs-info-form'
import 'vue-multi-ref'
import store from '../order-store'
import CommonMixin from '@/admin/mixins/common-mixin'
import Utils from '@/admin/utils/utils'

export default {
  name: 'register-seller',
  mixins: [CommonMixin],
  components: {
    OrderInfoForm,
    OrderDetailInfoForm,
    OrderProductInfoForm,
    OrderDeliveryInfoForm,
    OrderHistoryInfoForm
  },
  data () {
    return {
      dataStore: new Vue(store),
      tabNo: 0,
      working: false
    }
  },
  props: {
    // path param
    detailNo: {
      default () {
        return 0
      }
    }
  },
  mounted () {
    this.dataStore.getDetail(this.detailNo)
    document.addEventListener('scroll', this.scrollEvent)
  },
  destroyed () {
    document.removeEventListener('scroll', this.scrollEvent)
  },
  methods: {
    cancel () {
      this.$router.go(-1)
    },
    scrollEvent (event) {
      const pageContents = this.$refs.pageContent
      const len = pageContents.length
      // 마지막은 끝으로 인식
      // eslint-disable-next-line eqeqeq
      if (document.body.scrollHeight - document.body.offsetHeight == document.body.scrollTop) {
        this.tabNo = len - 1
        return
      }
      const elTop = Utils.getOffset(this.$refs.pageContent[0].$el).top
      for (let i = 0; i < len; i++) {
        if (pageContents[i].$el.getBoundingClientRect().top < elTop && pageContents[i].$el.getBoundingClientRect().bottom > elTop) {
          this.tabNo = i
        }
      }
    },
    scrollTab (tabNo) {
      const pageContents = this.$refs.pageContent
      const elTop = Utils.getOffset(this.$refs.pageContent[0].$el).top
      window.scrollTo({ top: Utils.getOffset(pageContents[tabNo].$el).top - elTop, behavior: 'smooth' })
    }
  },
  watch: {
  }
}
</script>

<style type="scss" scoped>
.fixed-header {
  position: sticky;
  top: 45px;
  background: #FFF;
  z-index: 100;
  margin-top: -25px
}
.form-header {
  margin-top: 5px;
}
.divide {
  background: #F1F1F1;
  padding: 5px 10px;
  margin-left: -20px;
  margin-right: -20px;
  font-size: 12px;
  font-weight: bold;
}
.page-content {
  border: 1px solid #CCC;
  margin-bottom: 1em;
  background: #FFF;
}
h2 {
  padding-top: 10px
}
</style>
<style>
.seller-from .ant-descriptions-item-label {
  width: 190px
}
</style>
