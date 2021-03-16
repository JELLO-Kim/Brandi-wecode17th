<template>
  <div class="region">
    <div class="fixed-header">
      <h2>셀러정보 {{ modName }}페이지
        <a-button type="success" @click="save">{{ modName }}하기</a-button>
        <a-button type="normal" @click="cancel">취소</a-button>
        <a-spin spin v-show="this.dataStore.loading"/>
      </h2>
      <div class="divide">
        회원 관리 > 셀러 계정 관리 > 셀러 정보 조회 / 수정
      </div>
      <div class="form-header">
        <a-tabs type="card" :tabBarStyle="{'padding-bottom': 0, 'margin-bottom': '-1px'}" v-model="tabNo" @change="scrollTab">
          <a-tab-pane :key="0" tab="기본 정보" />
          <a-tab-pane :key="1" tab="상세 정보"/>
          <a-tab-pane :key="2" tab="배송정보 및 교환/환불 정보" />
        </a-tabs>
      </div>
    </div>
    <a-page-header title="기본 정보" key="1" sub-title="기본 정보" class="page-content" v-multi-ref:pageContent>
      <seller-basic-info-form :data-store="dataStore"></seller-basic-info-form>
    </a-page-header>
    <a-page-header title="상세 정보" key="2" class="page-content" v-multi-ref:pageContent>
      <seller-detail-info-form :data-store="dataStore"></seller-detail-info-form>
    </a-page-header>
    <a-page-header title="배송정보 및 교환/환불 정보" key="3" class="page-content" v-multi-ref:pageContent>
      <seller-delivery-info-form :data-store="dataStore"></seller-delivery-info-form>
    </a-page-header>

    <transition name="fade-spiner">
      <div class="spiner-box" v-show="dataStore.loading">
        <div class="spiner">
          <a-spin tip="Loading...">
          </a-spin>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import SellerBasicInfoForm from './seller-basic-info-form'
import SellerDetailInfoForm from './seller-detail-info-form'
import SellerDeliveryInfoForm from './seller-delivery-info-form'
import 'vue-multi-ref'
import Vue from 'vue'
import store from '../seller-store'

export default {
  name: 'register-seller',
  data () {
    return {
      dataStore: new Vue(store),
      tabNo: 0,
      working: false
    }
  },
  props: {
    sellerNo: {
      default () {
        return 0
      }
    }
  },
  components: {
    SellerBasicInfoForm,
    SellerDetailInfoForm,
    SellerDeliveryInfoForm
  },
  mounted () {
    // 최상 단으로
    document.body.scrollTop = 0
    // 수정일땐 셀러 번호가 있고, 0 이면 등록
    if (this.sellerNo) {
      this.dataStore.getDetail(this.sellerNo)
    }
    document.addEventListener('scroll', this.scrollEvent)
  },
  computed: {
    isModify () {
      return this.sellerNo !== 0
    },
    modName () {
      return this.isModify ? '수정' : '등록'
    }
  },
  destroyed () {
    document.removeEventListener('scroll', this.scrollEvent)
  },
  methods: {
    save () {
      const detailData = JSON.parse(JSON.stringify(this.dataStore.detailData))
      delete detailData.account
      delete detailData.status_histories
      delete detailData.id
      this.dataStore.putDetail(this.sellerNo, detailData)

      console.log('save', detailData)
      // this.putDetail
    },
    cancel () {
      this.$router.go(-1)
    },
    scrollEvent (event) {
      const pageContents = this.$refs.pageContent
      const len = pageContents.length
      // 마지막은 끝으로 인식
      if (document.body.scrollHeight - document.body.offsetHeight === document.body.scrollTop) {
        this.tabNo = len - 1
        return
      }
      const elTop = this.getOffset2(this.$refs.pageContent[0].$el).top
      for (let i = 0; i < len; i++) {
        if (pageContents[i].$el.getBoundingClientRect().top < elTop && pageContents[i].$el.getBoundingClientRect().bottom > elTop) {
          this.tabNo = i
        }
      }
    },
    scrollTab (tabNo) {
      const pageContents = this.$refs.pageContent
      const elTop = this.getOffset2(this.$refs.pageContent[0].$el).top
      window.scrollTo({ top: this.getOffset2(pageContents[tabNo].$el).top - elTop, behavior: 'smooth' })
    },
    getOffset (el) {
      let _x = 0
      let _y = 0
      while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
        _x += el.offsetLeft - el.scrollLeft
        _y += el.offsetTop - el.scrollTop
        el = el.offsetParent
      }
      return { top: _y, left: _x }
    },
    getOffset2 (el) {
      let _x = 0
      let _y = 0
      while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
        _x += el.offsetLeft
        _y += el.offsetTop
        el = el.offsetParent
        // if (el == document.body) break
      }
      return { top: _y, left: _x }
    }
  },
  watch: {
    tabNo (v) {
      console.log('changeV', v)
    }
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
.region {
  position: relative;
}
.spiner-box {
  /*opacity: 1;*/
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: 300;
  background: rgba(0,0,0,0.2);
}
.fade-spiner-enter-active, .fade-spiner-leave-active { transition: opacity .3s } .fade-spiner-enter, .fade-spiner-leave-to { opacity: 0 }

</style>
<style>
.seller-from .ant-descriptions-item-label {
  width: 190px
}
</style>
