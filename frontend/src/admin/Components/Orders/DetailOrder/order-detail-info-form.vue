<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%" :column="2">
      <a-descriptions-item label="주문 상세 번호">
        {{ dataStore.detailData.cartNumber }}
      </a-descriptions-item>
      <a-descriptions-item label="주문 상태">

        <a-select class="small-size">
          <a-select-option value="1">상품준비</a-select-option>
        </a-select>
        <a-button type="info">CS 등록</a-button>

      </a-descriptions-item>
      <a-descriptions-item label="결제일시">
        {{ dataStore.detailData.orderDate }}
      </a-descriptions-item>

      <a-descriptions-item label="정산예정일">
        아직 구매확정이 되지 않은 주문건입니다.
      </a-descriptions-item>

      <a-descriptions-item label="주문상세배송비">
        0 원
      </a-descriptions-item>
      <a-descriptions-item label="연락처">
        {{ dataStore.detailData.orderPhone }}
        <a-button type="danger">변경</a-button>
      </a-descriptions-item>
    </a-descriptions>
    <product-history-modal ref="historyModal"/>
  </div>
</template>

<script>
export default {
  name: 'order-detail-info-form',
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
