<template>
  <div>
    <a-descriptions bordered size="small" class="seller-from" label-width="20%" :column="2">
      <a-descriptions-item label="회원번호">
        -
      </a-descriptions-item>
      <a-descriptions-item label="주문자명">
        {{ dataStore.detailData.user_name }}
      </a-descriptions-item>

      <a-descriptions-item label="수령자명">
        {{ dataStore.detailData.user_name }}
      </a-descriptions-item>
      <a-descriptions-item label="연락처">
        {{ dataStore.detailData.phone_number }}
         <a-button type="danger" size="small">변경</a-button>
      </a-descriptions-item>

      <a-descriptions-item label="배송지">
        {{ dataStore.detailData.address }} ({{ dataStore.detailData.zip_code }})
      </a-descriptions-item>
      <a-descriptions-item label="배송시 요청사항">
        일반배송 : 직접 받겠습니다
        <a-button type="info">배송지 변경</a-button>
      </a-descriptions-item>

    </a-descriptions>
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
