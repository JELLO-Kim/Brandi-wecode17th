<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%" :column="2">
      <a-descriptions-item label="PG사(결제사)" :span="2">
        네이버페이(신용카드)
      </a-descriptions-item>
      <a-descriptions-item label="주문 번호">
        {{ dataStore.detailData.number }}
      </a-descriptions-item>
      <a-descriptions-item label="주문 일시">
        {{ dataStore.detailData.order_date }}
      </a-descriptions-item>

      <a-descriptions-item label="외부거래번호">
        20201029NP1001576783
      </a-descriptions-item>
      <a-descriptions-item label="결제정보">
        네이버페이(신용카드)
      </a-descriptions-item>

      <a-descriptions-item label="총 결제 금액">
        {{ dataStore.detailData.total_price | makeComma }} 원
      </a-descriptions-item>
      <a-descriptions-item label="배송비">
        0 원
      </a-descriptions-item>

      <a-descriptions-item label="총 포인트결제금액">
        0 원
      </a-descriptions-item>
      <a-descriptions-item label="쿠폰 할인금액">
        0 원
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
