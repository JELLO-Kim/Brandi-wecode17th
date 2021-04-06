<template>
  <div>
    <!--
    address: "서울시 동작구 사당동 123-1"
    brand_name: "민트"
    color_name: "Silver"
    count: 3
    detail_number: "20201101444"
    discount_price: 13720
    discount_rate: 86
    number: "2020110100004"
    order_date: "2020-11-01 01:34:27"
    order_histories: [{order_status_id: 1, update_time: "2020-11-01 01:34:27"}]
    order_status_id: 1
    phone_number: "010-1235-7820"
    price: 98000
    product_name: "빼빼로 데이 특가 신모델 보석감별서 탠디 다이아몬드시계"
    product_number: 37
    size_name: "free"
    total_price: 41160
    user_name: "김땡땡"
    zip_code: 12345
    -->

    <a-descriptions bordered size="small" class="seller-from" label-width="20%" :column="2">
      <a-descriptions-item label="상품번호">

        {{ dataStore.detailData.productId }}
      </a-descriptions-item>
      <a-descriptions-item label="상품명">
        {{ dataStore.detailData.productName }}
      </a-descriptions-item>

      <a-descriptions-item label="상품 판매가">
        {{ dataStore.detailData.discountPrice | makeComma }} 원
      </a-descriptions-item>
      <a-descriptions-item label="상품 할인율">
        {{ dataStore.detailData.discountRate | makeComma }} %
      </a-descriptions-item>

      <a-descriptions-item label="브랜드명">
        {{ dataStore.detailData.brandName }}
      </a-descriptions-item>
      <a-descriptions-item label="옵션정보">
        {{ dataStore.detailData.colorName }}
        / {{ dataStore.detailData.sizeName }}
      </a-descriptions-item>

      <a-descriptions-item label="구매수량">
        {{ dataStore.detailData.quantity }} 개
      </a-descriptions-item>
      <a-descriptions-item label="적립예정포인트">
        0 포인트
      </a-descriptions-item>
    </a-descriptions>
    <product-history-modal ref="historyModal"/>
  </div>
</template>

<script>
export default {
  components: {
  },
  props: {
    dataStore: {
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      data: {
        seller_property_id: 1,
        brand_name_english: '',
        brand_name_korean: '',
        gosiType: 1
      }
    }
  },
  computed: {
    firstCategory () {
      return this.$store.state.const.firstCategory
    },
    secondCategory () {
      return this.$store.state.const.secondCategory
    }
  },
  methods: {
    showHistoryModal () {
      this.$refs.historyModal.show()
    },
    setFormData (value) {

    },
    getFromData () {
      return JSON.stringify(JSON.parse(this.data))
    },
    validate () {
      return true
    }
  }
}
</script>

<style type="scss" scoped>
.normal-size {
  width: 200px;
}
</style>
<style type="scss" scoped>
.normal-size {
  width: 200px;
}
br + .normal-size {
  margin-top: 5px;
}
.manager {
  display: inline-block;
}
.manager-button {
  display: inline-block;
}
.find-post-button {
  margin-left: 5px;
}
hr {
  border: none;
  border-top: 1px solid #CCC;
}

</style>
